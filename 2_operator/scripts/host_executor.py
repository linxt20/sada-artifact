"""Skill-owned host executor for TA++ v10.

This module moves the prompt-stage orchestration that used to live in Lab6/Lab8
experiment runners back under the skill. Runners should call
`python scripts/run_tapp.py augment-e2e ...` instead of importing prompts,
choosing TAPP chunks, retrying tag calls, or normalizing specs themselves.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

import pandas as pd

from visual_preview import generate_visual_preview


SKILL_ROOT = Path(__file__).resolve().parents[1]
LAB_DIR = SKILL_ROOT.parent
REPO_ROOT = LAB_DIR.parent
TAPP_SCRIPT = SKILL_ROOT / "scripts" / "run_tapp.py"
PROMPTS_DIR = SKILL_ROOT / "prompts"
PRINT_LOCK = threading.Lock()
MANIFEST_LOCK = threading.Lock()
STAGE_SEMAPHORE: Optional[threading.Semaphore] = None
CLAUDE_TIMEOUT_S = 900
TAPP_STAGE_TIMEOUT_S = 300


TEXT_EXCLUDED_EXACT = {
    "link",
    "url",
    "href",
    "model number",
    "part number",
    "serial number",
    "sku",
}
TEXT_EXCLUDED_TOKENS = ("url", "href")
TEXT_LOW_PRIORITY_TOKENS = (
    "warranty",
    "covered in warranty",
    "not covered",
    "sales package",
    "service type",
    "other accessories",
)
TEXT_HIGH_PRIORITY = (
    ("additional features", 120),
    ("screen type", 115),
    ("graphic processor", 110),
    ("processor name", 105),
    ("name", 100),
    ("title", 95),
    ("summary", 90),
    ("description", 85),
    ("type", 80),
    ("suitable for", 75),
    ("keyboard", 70),
    ("sound", 65),
    ("included software", 60),
    ("usb port", 55),
    ("hdmi port", 50),
    ("battery", 45),
    ("wireless", 40),
    ("color gamut", 35),
    ("security chip", 30),
)


def _tprint(message: str) -> None:
    with PRINT_LOCK:
        print(message, flush=True)


def _popen_group_kwargs() -> dict[str, Any]:
    if os.name == "nt":
        flag = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        return {"creationflags": flag} if flag else {}
    return {"start_new_session": True}


def _kill_process_tree(proc: subprocess.Popen[bytes]) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except Exception:
        proc.kill()


def _run_capture_timeout(
    cmd: Sequence[str],
    *,
    input_bytes: Optional[bytes] = None,
    cwd: Optional[Path] = None,
    env: Optional[dict[str, str]] = None,
    timeout_s: int,
) -> tuple[int, bytes, bytes, bool]:
    proc = subprocess.Popen(
        list(map(str, cmd)),
        stdin=subprocess.PIPE if input_bytes is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd) if cwd is not None else None,
        env=env,
        **_popen_group_kwargs(),
    )
    try:
        stdout, stderr = proc.communicate(input=input_bytes, timeout=timeout_s)
        return proc.returncode, stdout or b"", stderr or b"", False
    except subprocess.TimeoutExpired as exc:
        stdout = exc.output or b""
        stderr = exc.stderr or b""
        _kill_process_tree(proc)
        try:
            proc.wait(timeout=3)
        except Exception:
            pass
        timeout_msg = f"timeout after {timeout_s}s".encode("utf-8")
        stderr = (stderr or b"") + (b"\n" if stderr else b"") + timeout_msg
        return 124, stdout or b"", stderr, True


def find_claude() -> str:
    exe = shutil.which("claude")
    if not exe:
        candidate = os.path.expandvars(r"%APPDATA%\npm\claude.CMD")
        if Path(candidate).exists():
            exe = candidate
    if not exe or not Path(exe).exists():
        raise SystemExit("claude CLI not found on PATH or at %APPDATA%\\npm\\claude.CMD")
    path = Path(exe)
    if os.name == "nt" and path.suffix.lower() in {".cmd", ".bat"}:
        native = path.parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
        if native.exists():
            return str(native)
    return exe


def invoke_claude(
    prompt: str,
    *,
    model: str,
    cwd: Path,
    timeout_s: int,
    log_path: Path,
    attempts: int,
    fallback_model: Optional[str] = None,
    use_global_timeout: bool = True,
) -> tuple[int, str, str]:
    effective_timeout_s = max(1, int((CLAUDE_TIMEOUT_S if use_global_timeout else 0) or timeout_s))
    cmd = [
        find_claude(),
        "-p",
        "--bare",
        "--no-session-persistence",
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
        "--model",
        model,
    ]
    if fallback_model and fallback_model != model:
        cmd += ["--fallback-model", fallback_model]

    env = os.environ.copy()
    env["CLAUDE_CODE_SIMPLE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    last_rc = -1
    last_text = ""
    last_stderr = ""
    for attempt in range(1, max(1, attempts) + 1):
        started = time.time()
        rc, stdout, stderr, timed_out = _run_capture_timeout(
            cmd,
            input_bytes=prompt.encode("utf-8"),
            cwd=cwd,
            env=env,
            timeout_s=effective_timeout_s,
        )
        stdout_raw = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr.decode("utf-8", errors="replace")
        if timed_out and not stderr_text:
            stderr_text = f"timeout after {effective_timeout_s}s"

        text = stdout_raw
        is_error = False
        try:
            payload = json.loads(stdout_raw)
            if isinstance(payload, dict):
                is_error = bool(payload.get("is_error"))
                text = payload.get("result") or payload.get("response") or ""
        except Exception:
            pass

        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            json.dumps(
                {
                    "attempt": attempt,
                    "model": model,
                    "fallback_model": fallback_model,
                    "rc": rc,
                    "is_error": is_error,
                    "wall_seconds": round(time.time() - started, 2),
                    "stdout_text": text,
                    "stderr_text": stderr_text[:4000],
                    "raw_stdout_head": stdout_raw[:4000],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        last_rc, last_text, last_stderr = rc, text, stderr_text
        if rc == 0 and not is_error and text.strip():
            return rc, text, stderr_text
        time.sleep(min(10, 2 * attempt))
    return last_rc, last_text, last_stderr


def _read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path)
    if suffix == ".csv":
        for encoding in ("utf-8-sig", "utf-8", "latin1", "cp1252"):
            try:
                return pd.read_csv(path, encoding=encoding)
            except UnicodeDecodeError:
                continue
        return pd.read_csv(path, encoding="latin1")
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix in (".pkl", ".pickle"):
        payload = pd.read_pickle(path)
        if isinstance(payload, dict) and isinstance(payload.get("data"), pd.DataFrame):
            return payload["data"]
        if isinstance(payload, pd.DataFrame):
            return payload
        raise ValueError(f"pickle does not contain a DataFrame: {path}")
    raise ValueError(f"unsupported table format: {path}")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def _run_tapp_cli(args: Sequence[str], *, timeout_s: int = 600) -> tuple[int, str, str]:
    cmd = [sys.executable, str(TAPP_SCRIPT), *map(str, args)]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    rc, stdout, stderr, _timed_out = _run_capture_timeout(
        cmd,
        cwd=REPO_ROOT,
        env=env,
        timeout_s=timeout_s,
    )
    return (
        rc,
        stdout.decode("utf-8", errors="replace"),
        stderr.decode("utf-8", errors="replace"),
    )


def _extract_json_payload(text: str) -> Optional[Any]:
    raw = (text or "").strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        pass
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", raw, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except Exception:
            pass
    decoder = json.JSONDecoder()
    for idx, char in enumerate(raw):
        if char not in "[{":
            continue
        try:
            payload, _ = decoder.raw_decode(raw[idx:])
            return payload
        except Exception:
            continue
    return None


def _prompt_template(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def _text_stats_for_frame(frame: pd.DataFrame) -> dict[str, dict[str, int]]:
    stats: dict[str, dict[str, int]] = {}
    for col in frame.columns:
        series = frame[col]
        if not (pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)):
            continue
        values = series.dropna().astype(str)
        if values.empty:
            continue
        lengths = values.str.len()
        stats[str(col)] = {
            "non_null": int(lengths.count()),
            "mean_chars": int(lengths.mean()),
            "median_chars": int(lengths.median()),
            "p95_chars": int(lengths.quantile(0.95)),
            "max_chars": int(lengths.max()),
        }
    return stats


def _evidence_priority(col: str) -> int:
    name = str(col).strip().lower()
    if any(token in name for token in TEXT_LOW_PRIORITY_TOKENS):
        return -100
    for token, score in TEXT_HIGH_PRIORITY:
        if token in name:
            return score
    return 0


def _is_evidence_column(frame: pd.DataFrame, col: str) -> bool:
    if col not in frame.columns:
        return False
    name = str(col).strip().lower()
    if name in TEXT_EXCLUDED_EXACT or any(token in name for token in TEXT_EXCLUDED_TOKENS):
        return False
    series = frame[col]
    if not (pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)):
        return False
    values = series.dropna().astype(str).str.strip()
    if values.empty:
        return False
    sample = values.head(200)
    url_like = sample.str.contains(r"https?://|www\.", case=False, regex=True, na=False).mean()
    return float(url_like) < 0.05


def _text_columns_for_tapp(frame: pd.DataFrame) -> list[str]:
    stats = _text_stats_for_frame(frame)
    useful = [
        col
        for col, item in stats.items()
        if _is_evidence_column(frame, col)
        if int(item.get("median_chars", 0)) > 10 or int(item.get("p95_chars", 0)) > 40
    ]
    useful.sort(
        key=lambda col: (
            _evidence_priority(col),
            int(stats[col].get("p95_chars", 0)),
            int(stats[col].get("median_chars", 0)),
            int(stats[col].get("non_null", 0)),
        ),
        reverse=True,
    )
    if useful:
        return useful
    return [str(col) for col in frame.columns if _is_evidence_column(frame, str(col))]


def _combined_text_p95(frame: pd.DataFrame, text_cols: Sequence[str], sample_rows: int = 200) -> int:
    if not text_cols or frame.empty:
        return 0
    sampled = frame.head(min(sample_rows, len(frame))).reset_index(drop=True)
    lengths: list[int] = []
    for idx in range(len(sampled)):
        total = 0
        for col in text_cols:
            if col not in sampled.columns:
                continue
            value = sampled.at[idx, col]
            if pd.isna(value):
                continue
            total += len(str(value))
        lengths.append(total)
    if not lengths:
        return 0
    return int(pd.Series(lengths).quantile(0.95))


def _host_execution_config() -> dict[str, Any]:
    try:
        payload = json.loads((SKILL_ROOT / "config" / "model_recipe.json").read_text(encoding="utf-8"))
        cfg = payload.get("skill_v10_host_execution") or payload.get("skill_v9_host_execution") or payload.get("skill_v7_host_execution")
        return cfg if isinstance(cfg, dict) else {}
    except Exception:
        return {}


def _profile_for_model(model: str, cfg: dict[str, Any]) -> dict[str, Any]:
    lower = str(model or "").lower()
    profiles = cfg.get("model_chunk_profiles") or []
    if isinstance(profiles, list):
        for profile in profiles:
            if not isinstance(profile, dict):
                continue
            for exact in profile.get("models") or []:
                if lower == str(exact).lower():
                    result = dict(profile)
                    result["match_kind"] = "exact"
                    result["match_value"] = str(exact)
                    return result
            for pattern in profile.get("patterns") or []:
                pattern_text = str(pattern).lower()
                if pattern_text and pattern_text in lower:
                    result = dict(profile)
                    result["match_kind"] = "pattern"
                    result["match_value"] = str(pattern)
                    return result

    # Backward-compatible fallback for older recipe drafts.
    fast_patterns = [str(item).lower() for item in (cfg.get("fast_or_budget_model_patterns") or ["gemini", "haiku"])]
    if any(pattern and pattern in lower for pattern in fast_patterns):
        return {
            "name": "fast_or_budget_fallback",
            "categorize_chunk_cap": int(cfg.get("fast_categorize_chunk_cap", 250)),
            "tag_chunk_cap": int(cfg.get("fast_tag_chunk_cap", 200)),
            "match_kind": "fallback_pattern",
            "match_value": ",".join(fast_patterns),
        }
    if "opus" in lower:
        return {
            "name": "opus_fallback",
            "categorize_chunk_cap": int(cfg.get("opus_categorize_chunk_cap", 300)),
            "tag_chunk_cap": int(cfg.get("opus_tag_chunk_cap", 250)),
            "match_kind": "fallback_pattern",
            "match_value": "opus",
        }
    return {
        "name": "default",
        "categorize_chunk_cap": int(cfg.get("default_categorize_chunk_cap", 400)),
        "tag_chunk_cap": int(cfg.get("default_tag_chunk_cap", 400)),
        "match_kind": "default",
        "match_value": "",
    }


def _profile_int(profile: dict[str, Any], cfg: dict[str, Any], key: str, default: int) -> int:
    if key in profile:
        return int(profile[key])
    if key in cfg:
        return int(cfg[key])
    return int(default)


def _model_policy(model: str, p95_chars: int) -> dict[str, Any]:
    cfg = _host_execution_config()
    profile = _profile_for_model(model, cfg)
    cat_cap = _profile_int(profile, cfg, "categorize_chunk_cap", int(cfg.get("default_categorize_chunk_cap", 400)))
    tag_cap = _profile_int(profile, cfg, "tag_chunk_cap", int(cfg.get("default_tag_chunk_cap", 400)))
    very_wide = int(cfg.get("very_wide_text_p95_chars", 12000))
    wide = int(cfg.get("wide_text_p95_chars", 7000))
    if p95_chars >= very_wide:
        cat_cap = min(cat_cap, _profile_int(profile, cfg, "very_wide_text_categorize_chunk_cap", 150))
        tag_cap = min(tag_cap, _profile_int(profile, cfg, "very_wide_text_tag_chunk_cap", 100))
    elif p95_chars >= wide:
        cat_cap = min(cat_cap, _profile_int(profile, cfg, "wide_text_categorize_chunk_cap", 250))
        tag_cap = min(tag_cap, _profile_int(profile, cfg, "wide_text_tag_chunk_cap", 150))
    tag_subchunk = int(cfg.get("tag_retry_subchunk_size", 200))
    categorize_subchunk = int(cfg.get("categorize_retry_subchunk_size", max(50, min(200, cat_cap // 2 or 1))))
    return {
        "model_chunk_profile": str(profile.get("name") or "default"),
        "model_chunk_match_kind": str(profile.get("match_kind") or ""),
        "model_chunk_match_value": str(profile.get("match_value") or ""),
        "categorize_chunk_cap": max(1, cat_cap),
        "tag_chunk_cap": max(1, tag_cap),
        "categorize_retry_subchunk_size": max(1, categorize_subchunk),
        "tag_retry_subchunk_size": max(1, tag_subchunk),
    }


def _decide_workers(model: str, max_workers: int, p95_chars: int, row_count: int) -> tuple[int, dict[str, Any]]:
    budget = max(1, int(max_workers or 1))
    lower = str(model or "").lower()
    very_wide = p95_chars >= int(_host_execution_config().get("very_wide_text_p95_chars", 12000))
    wide = p95_chars >= int(_host_execution_config().get("wide_text_p95_chars", 7000))

    if "gemini" in lower or "haiku" in lower:
        decided = min(budget, 3)
        reason = "fast_or_budget_model"
    elif "opus" in lower:
        decided = min(budget, 2)
        reason = "opus_quality_model"
    elif very_wide:
        decided = min(budget, 2)
        reason = "very_wide_text"
    elif wide:
        decided = min(budget, 3)
        reason = "wide_text"
    elif row_count < 1000:
        decided = min(budget, 2)
        reason = "small_table"
    else:
        decided = min(budget, 4)
        reason = "default_large_model"

    return max(1, decided), {
        "worker_decision_source": "skill_v10_policy",
        "max_worker_budget": budget,
        "worker_decision_reason": reason,
    }


def _chunk_ranges(total: int, chunk_size: int) -> list[tuple[int, int]]:
    size = max(1, int(chunk_size or total or 1))
    return [(start, min(total, start + size)) for start in range(0, total, size)]


def _truncate_cell(value: Any, limit: int = 700) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    return text[: limit - 3] + "..." if len(text) > limit else text


def _build_text_items(frame: pd.DataFrame, indices: Sequence[int], text_cols: Sequence[str]) -> list[str]:
    items: list[str] = []
    for idx in indices:
        parts: list[str] = []
        for col in text_cols:
            if col not in frame.columns:
                continue
            value = _truncate_cell(frame.iloc[int(idx)][col])
            if value:
                parts.append(f"{col}: {value}")
        if not parts:
            row = frame.iloc[int(idx)]
            parts = [
                f"{col}: {_truncate_cell(row[col], 240)}"
                for col in frame.columns[:8]
                if _truncate_cell(row[col], 240)
            ]
        items.append(f"[{int(idx)}] " + " | ".join(parts))
    return items


def _safe_facet_name(value: str, used: set[str]) -> str:
    name = re.sub(r"[^0-9A-Za-z_]+", "_", str(value or "facet").strip()).strip("_")
    if not name:
        name = "facet"
    if name[0].isdigit():
        name = f"facet_{name}"
    base = name[:80]
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def _extract_vocab(description: str) -> list[str]:
    match = re.search(r"\{([^}]+)\}", description or "")
    if not match:
        return []
    return [token.strip() for token in match.group(1).split(",") if token.strip()]


def _items_payload(payload: Any) -> Optional[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("Results"), dict):
        items = payload["Results"].get("Items")
        return items if isinstance(items, dict) else None
    return payload if isinstance(payload, dict) else None


def _items_cover_indices(payload: Any, indices: Sequence[int]) -> bool:
    items = _items_payload(payload)
    if not isinstance(items, dict):
        return False
    expected = {str(int(idx)) for idx in indices}
    return set(map(str, items.keys())) == expected


def _register_artifact(workdir: Path, kind: str, path: Path, stage: str) -> Optional[str]:
    with MANIFEST_LOCK:
        rc, stdout, stderr = _run_tapp_cli(
            [
                "record-artifact",
                "--workdir",
                str(workdir.resolve()),
                "--kind",
                kind,
                "--path",
                str(path.resolve()),
                "--stage",
                stage,
            ],
            timeout_s=120,
        )
    if rc != 0:
        _tprint(f"[tapp-artifact] failed kind={kind} stage={stage} rc={rc} stderr={stderr[:200]!r}")
        return None
    match = re.search(r"Placeholder:\s*(\S+)", stdout)
    return match.group(1) if match else None


def _record_trace(
    workdir: Path,
    *,
    stage: str,
    model: str,
    plan_id: Optional[str],
    output_ref: Optional[str] = None,
    status: str = "ok",
    reasoning_summary: str = "stage completed by TA++ v10 skill-owned executor",
) -> None:
    args: list[str] = [
        "record-trace",
        "--workdir",
        str(workdir.resolve()),
        "--stage",
        stage,
        "--status",
        status,
        "--model",
        model,
        "--reasoning-summary",
        reasoning_summary[:500],
    ]
    if plan_id:
        args.extend(["--plan-id", plan_id])
    if output_ref:
        args.extend(["--output-ref", output_ref])
    with MANIFEST_LOCK:
        rc, _stdout, stderr = _run_tapp_cli(args, timeout_s=120)
    if rc != 0:
        _tprint(f"[tapp-trace] failed stage={stage} rc={rc} stderr={stderr[:200]!r}")


def _write_stage_json(
    workdir: Path,
    rel_path: str,
    payload: Any,
    *,
    kind: str,
    stage: str,
    model: str,
    plan_id: Optional[str],
    reasoning_summary: str,
) -> Path:
    path = workdir / rel_path
    _write_json(path, payload)
    output_ref = _register_artifact(workdir, kind, path, stage)
    _record_trace(
        workdir,
        stage=stage,
        model=model,
        plan_id=plan_id,
        output_ref=output_ref,
        reasoning_summary=reasoning_summary,
    )
    return path


def _invoke_json_stage(
    prompt: str,
    *,
    stage: str,
    model: str,
    workdir: Path,
    log_name: str,
    attempts: int,
    timeout_s: int,
    validator: Optional[Callable[[Any], None]] = None,
) -> Any:
    last_text = ""
    validation_feedback = ""
    stage_timeout_s = min(max(1, int(timeout_s)), max(1, int(TAPP_STAGE_TIMEOUT_S)))
    for parse_attempt in range(1, max(1, attempts) + 1):
        suffix = f"_{parse_attempt}" if parse_attempt > 1 else ""
        if parse_attempt == 1:
            stage_prompt = prompt
        else:
            feedback = validation_feedback or "Previous response was not valid strict JSON."
            stage_prompt = prompt + f"\n\nPrevious response was invalid: {feedback}\nReturn the corrected JSON object only."
        semaphore = STAGE_SEMAPHORE
        if semaphore is None:
            rc, text, stderr = invoke_claude(
                stage_prompt,
                model=model,
                cwd=REPO_ROOT,
                timeout_s=stage_timeout_s,
                log_path=workdir / "stage_logs" / f"{log_name}{suffix}.json",
                attempts=1,
                use_global_timeout=False,
            )
        else:
            with semaphore:
                rc, text, stderr = invoke_claude(
                    stage_prompt,
                    model=model,
                    cwd=REPO_ROOT,
                    timeout_s=stage_timeout_s,
                    log_path=workdir / "stage_logs" / f"{log_name}{suffix}.json",
                    attempts=1,
                    use_global_timeout=False,
                )
        last_text = text
        payload = _extract_json_payload(text)
        if rc == 0 and payload is not None:
            if validator is not None:
                try:
                    validator(payload)
                except Exception as exc:  # noqa: BLE001
                    validation_feedback = str(exc)[:800]
                    _tprint(f"[tapp stage retry] stage={stage} attempt={parse_attempt} validation={validation_feedback!r}")
                    continue
            return payload
        _tprint(f"[tapp stage retry] stage={stage} attempt={parse_attempt} rc={rc} stderr={stderr[:160]!r}")
    detail = f" validation={validation_feedback!r}" if validation_feedback else ""
    raise RuntimeError(f"{stage} did not return valid JSON;{detail} tail={last_text[-300:]!r}")


def _subagent_prompt(prompt_body: str, input_payload: dict[str, Any]) -> str:
    return f"""You are a TA++ v10 isolated subagent. Do not use prior conversation state.
Read the stage contract below and return strict JSON only. Do not include Markdown fences or explanatory prose.

STAGE_CONTRACT:
{prompt_body}

INPUT_JSON:
{json.dumps(input_payload, ensure_ascii=False, indent=2)}
"""


def _get_payload_value(payload: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in payload:
            return payload.get(key)
    return None


def _nullish_ref(value: Any) -> bool:
    if value is None:
        return True
    token = str(value).strip().lower()
    return token in {"", "null", "none", "parent_node_id_or_null"}


def _structure_errors(
    payload: Any,
    *,
    stage: str,
    category_keys: Sequence[str] = ("Categories", "ConsolidatedFacets"),
) -> list[str]:
    if not isinstance(payload, dict):
        return [f"{stage}: payload must be a JSON object"]
    errors: list[str] = []
    intent = str(_get_payload_value(payload, "IntentClass", "intent_class") or "").strip()
    structure = _get_payload_value(payload, "PlanningStructure", "planning_structure")
    expected_by_intent = {
        "predictive": "prediction_tree",
        "causal": "causal_graph",
        "concept_attribute": "concept_tree",
        "fallback_flat": "flat",
    }
    expected_structure = expected_by_intent.get(intent)
    if not isinstance(structure, dict):
        if intent == "fallback_flat":
            return []
        return [f"{stage}: missing PlanningStructure object for intent {intent or '<missing>'}"]

    structure_type = str(_get_payload_value(structure, "StructureType", "structure_type") or "").strip()
    if expected_structure and structure_type != expected_structure:
        errors.append(f"{stage}: IntentClass {intent} requires StructureType {expected_structure}, got {structure_type or '<missing>'}")
    if structure_type == "flat":
        return errors
    if structure_type not in {"prediction_tree", "causal_graph", "concept_tree"}:
        errors.append(f"{stage}: unsupported StructureType {structure_type or '<missing>'}")

    nodes = _get_payload_value(structure, "Nodes", "nodes")
    if not isinstance(nodes, list) or not nodes:
        errors.append(f"{stage}: non-flat PlanningStructure requires non-empty Nodes")
        nodes = []
    node_ids: set[str] = set()
    node_labels: set[str] = set()
    node_roles: set[str] = set()
    root = str(_get_payload_value(structure, "Root", "root") or "").strip()
    for idx, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"{stage}: node[{idx}] must be an object")
            continue
        node_id = str(_get_payload_value(node, "Id", "id") or "").strip()
        label = str(_get_payload_value(node, "Label", "label") or "").strip()
        role = str(_get_payload_value(node, "Role", "role") or "").strip()
        if not node_id:
            errors.append(f"{stage}: node[{idx}] missing Id")
        elif node_id in node_ids:
            errors.append(f"{stage}: duplicate node Id {node_id!r}")
        else:
            node_ids.add(node_id)
        if label:
            node_labels.add(label)
        else:
            errors.append(f"{stage}: node[{idx}] missing Label")
        if role:
            node_roles.add(role)
        else:
            errors.append(f"{stage}: node[{idx}] missing Role")

    if not root:
        errors.append(f"{stage}: PlanningStructure.Root is required")
    elif root not in node_ids:
        errors.append(f"{stage}: Root {root!r} must be a node Id, not only a label or free-form focus")

    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_id = str(_get_payload_value(node, "Id", "id") or "").strip()
        parent = _get_payload_value(node, "Parent", "parent")
        if node_id == root and not _nullish_ref(parent):
            errors.append(f"{stage}: root node {node_id!r} must have Parent null")
        if not _nullish_ref(parent) and str(parent).strip() not in node_ids:
            errors.append(f"{stage}: node {node_id!r} has dangling Parent {parent!r}")

    allowed_relations = {
        "prediction_tree": {"predicts", "part_of"},
        "causal_graph": {"causes", "confounds", "part_of"},
        "concept_tree": {"part_of", "dispatches_to"},
    }
    edges = _get_payload_value(structure, "Edges", "edges")
    if not isinstance(edges, list):
        errors.append(f"{stage}: Edges must be a list")
        edges = []
    if len(node_ids) > 1 and not edges:
        errors.append(f"{stage}: non-flat structure with multiple nodes requires edges")
    for idx, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"{stage}: edge[{idx}] must be an object")
            continue
        source = str(_get_payload_value(edge, "Source", "source") or "").strip()
        target = str(_get_payload_value(edge, "Target", "target") or "").strip()
        relation = str(_get_payload_value(edge, "Relation", "relation") or "").strip()
        if source not in node_ids:
            errors.append(f"{stage}: edge[{idx}] has dangling Source {source!r}")
        if target not in node_ids:
            errors.append(f"{stage}: edge[{idx}] has dangling Target {target!r}")
        if relation not in allowed_relations.get(structure_type, set()):
            errors.append(f"{stage}: edge[{idx}] relation {relation!r} is not valid for {structure_type}")

    selected = _get_payload_value(structure, "SelectedNodes", "selected_nodes")
    if not isinstance(selected, list):
        errors.append(f"{stage}: SelectedNodes must be a list")
        selected = []
    selected_ids = {str(item).strip() for item in selected if str(item).strip()}
    for selected_id in selected_ids:
        if selected_id not in node_ids:
            errors.append(f"{stage}: SelectedNodes contains unknown node id {selected_id!r}")

    categories: list[dict[str, Any]] = []
    for key in category_keys:
        value = payload.get(key)
        if isinstance(value, list):
            categories = [item for item in value if isinstance(item, dict)]
            break
    if categories and not selected_ids:
        errors.append(f"{stage}: materialized categories require non-empty SelectedNodes")
    category_roles: set[str] = set()
    for idx, category in enumerate(categories):
        name = str(_get_payload_value(category, "Name", "name") or f"category[{idx}]")
        selected_node_id = str(_get_payload_value(category, "SelectedNodeId", "selected_node_id") or "").strip()
        role = str(_get_payload_value(category, "Role", "role") or "").strip()
        parent = _get_payload_value(category, "Parent", "parent")
        structure_path = str(_get_payload_value(category, "StructurePath", "structure_path") or "").strip()
        if not selected_node_id:
            errors.append(f"{stage}: category {name!r} missing SelectedNodeId")
        elif selected_node_id not in node_ids:
            errors.append(f"{stage}: category {name!r} SelectedNodeId {selected_node_id!r} not found in Nodes")
        elif selected_node_id not in selected_ids:
            errors.append(f"{stage}: category {name!r} SelectedNodeId {selected_node_id!r} not listed in SelectedNodes")
        if not role:
            errors.append(f"{stage}: category {name!r} missing Role")
        else:
            category_roles.add(role)
        if not _nullish_ref(parent) and str(parent).strip() not in node_ids and str(parent).strip() not in node_labels:
            errors.append(f"{stage}: category {name!r} has Parent {parent!r} that is neither node id nor node label")
        if not structure_path:
            errors.append(f"{stage}: category {name!r} missing StructurePath")

    all_roles = node_roles | category_roles
    if structure_type == "prediction_tree" and not (all_roles & {"feature", "feature_group", "exploratory_driver"}):
        errors.append(f"{stage}: prediction_tree requires feature or feature_group roles")
    if structure_type == "causal_graph":
        if not (all_roles & {"outcome", "focus"}):
            errors.append(f"{stage}: causal_graph requires outcome or focus node")
        if not (all_roles & {"treatment", "causal_factor", "mechanism"}):
            errors.append(f"{stage}: causal_graph requires treatment, causal_factor, or mechanism node")
        if "confounder" not in all_roles:
            errors.append(f"{stage}: causal_graph requires at least one explicit confounder node or column")
    if structure_type == "concept_tree" and not (all_roles & {"concept", "facet", "proposed_focus"}):
        errors.append(f"{stage}: concept_tree requires concept, facet, or proposed_focus roles")
    return errors


def _repair_planning_node_roles(payload: Any, *, category_keys: Sequence[str]) -> None:
    if not isinstance(payload, dict):
        return
    structure = _get_payload_value(payload, "PlanningStructure", "planning_structure")
    if not isinstance(structure, dict):
        return
    nodes = _get_payload_value(structure, "Nodes", "nodes")
    if not isinstance(nodes, list):
        return
    for node in nodes:
        if not isinstance(node, dict) or str(_get_payload_value(node, "Label", "label") or "").strip():
            continue
        label = str(_get_payload_value(node, "Name", "name", "Id", "id") or "").strip()
        if label:
            node["Label"] = label
    structure_type = str(_get_payload_value(structure, "StructureType", "structure_type") or "").strip()
    root_id = str(_get_payload_value(structure, "Root", "root") or "").strip()
    role_by_node: dict[str, str] = {}
    for key in category_keys:
        categories = _get_payload_value(payload, key, key[:1].lower() + key[1:])
        if not isinstance(categories, list):
            continue
        for category in categories:
            if not isinstance(category, dict):
                continue
            node_id = str(_get_payload_value(category, "SelectedNodeId", "selected_node_id", "CandidateNodeId") or "").strip()
            role = str(_get_payload_value(category, "Role", "role") or "").strip()
            if node_id and role:
                role_by_node.setdefault(node_id, role)
    for node in nodes:
        if not isinstance(node, dict):
            continue
        if str(_get_payload_value(node, "Role", "role") or "").strip():
            continue
        node_id = str(_get_payload_value(node, "Id", "id") or "").strip()
        role = role_by_node.get(node_id, "")
        if not role:
            if node_id and node_id == root_id:
                role = "outcome" if structure_type in {"prediction_tree", "causal_graph"} else "concept"
            elif structure_type == "prediction_tree":
                role = "feature"
            elif structure_type == "causal_graph":
                role = "causal_factor"
            elif structure_type == "concept_tree":
                role = "facet"
        if role:
            node["Role"] = role


def _repair_planning_edge_relations(payload: Any) -> None:
    if not isinstance(payload, dict):
        return
    structure = _get_payload_value(payload, "PlanningStructure", "planning_structure")
    if not isinstance(structure, dict):
        return
    structure_type = str(_get_payload_value(structure, "StructureType", "structure_type") or "").strip()
    edges = _get_payload_value(structure, "Edges", "edges")
    nodes = _get_payload_value(structure, "Nodes", "nodes")
    if not isinstance(edges, list) or not isinstance(nodes, list):
        return
    parent_by_id: dict[str, str] = {}
    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_id = str(_get_payload_value(node, "Id", "id") or "").strip()
        parent = _get_payload_value(node, "Parent", "parent")
        if node_id and not _nullish_ref(parent):
            parent_by_id[node_id] = str(parent).strip()

    def set_edge(edge: dict[str, Any], source: str, target: str, relation: str) -> None:
        if "source" in edge and "Source" not in edge:
            edge["source"] = source
        else:
            edge["Source"] = source
        if "target" in edge and "Target" not in edge:
            edge["target"] = target
        else:
            edge["Target"] = target
        if "relation" in edge and "Relation" not in edge:
            edge["relation"] = relation
        else:
            edge["Relation"] = relation

    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source = str(_get_payload_value(edge, "Source", "source") or "").strip()
        target = str(_get_payload_value(edge, "Target", "target") or "").strip()
        relation = str(_get_payload_value(edge, "Relation", "relation") or "").strip()
        if not source or not target:
            continue
        if structure_type == "prediction_tree":
            if relation == "predicted_by":
                set_edge(edge, target, source, "predicts")
            elif relation in {"has_feature", "has_child", "contains", "includes", "refines"}:
                if parent_by_id.get(target) == source:
                    set_edge(edge, target, source, "part_of")
                elif parent_by_id.get(source) == target:
                    set_edge(edge, source, target, "part_of")
                else:
                    set_edge(edge, source, target, "part_of")
            elif relation == "part_of" and parent_by_id.get(target) == source:
                set_edge(edge, target, source, "part_of")
        elif structure_type == "concept_tree" and relation in {"has_facet", "has_child", "contains", "includes", "refines"}:
            if parent_by_id.get(target) == source:
                set_edge(edge, target, source, "part_of")
            else:
                set_edge(edge, source, target, "part_of")
        elif structure_type == "causal_graph" and relation == "caused_by":
            set_edge(edge, target, source, "causes")


def _validate_planning_payload(
    payload: Any,
    *,
    stage: str,
    category_keys: Sequence[str] = ("Categories", "ConsolidatedFacets"),
) -> None:
    _repair_planning_node_roles(payload, category_keys=category_keys)
    _repair_planning_edge_relations(payload)
    errors = _structure_errors(payload, stage=stage, category_keys=category_keys)
    if errors:
        raise ValueError("; ".join(errors[:8]))


def _categories_from_payload(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    context = {
        key: payload.get(key)
        for key in ("IntentClass", "IntentSubtype", "PlanningStructure", "SelectionStrategy")
        if payload.get(key) is not None
    }
    for key in ("Categories", "ConsolidatedFacets", "CandidateFacets"):
        value = payload.get(key)
        if isinstance(value, list):
            categories = []
            for item in value:
                if not isinstance(item, dict):
                    continue
                enriched = dict(item)
                for ctx_key, ctx_value in context.items():
                    enriched.setdefault(ctx_key, ctx_value)
                categories.append(enriched)
            return categories
    return []


def _is_token_limit_error(exc: BaseException) -> bool:
    text = repr(exc).lower()
    return "token limit" in text or "message exceeds" in text or "context_length" in text


def _compact_consolidation_payload(value: Any, depth: int = 0) -> Any:
    """Keep consolidation prompts below API request limits by dropping bulky evidence."""
    if depth > 6:
        return None
    if isinstance(value, str):
        return value if len(value) <= 600 else value[:600] + "..."
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        limit = 40 if depth <= 2 else 12
        return [_compact_consolidation_payload(item, depth + 1) for item in value[:limit]]
    if isinstance(value, dict):
        bulky_keys = {
            "TextItems",
            "items",
            "rows",
            "examples",
            "evidence",
            "evidence_examples",
            "row_evidence",
            "sample_rows",
            "raw_text",
        }
        kept: dict[str, Any] = {}
        for key, item in value.items():
            if str(key) in bulky_keys:
                continue
            kept[str(key)] = _compact_consolidation_payload(item, depth + 1)
        return kept
    return str(value)[:600]


def _label_has_compound_joiner(label: Any) -> bool:
    token = str(label or "").strip().lower()
    if not token:
        return False
    return any(joiner in token for joiner in (" or ", " and ", "/", "&", "|"))


def _description_has_compound_vocab(description: str) -> bool:
    return any(_label_has_compound_joiner(label) for label in _extract_vocab(description))


def _copy_schema_metadata(source: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    for src_key, dst_key in (
        ("SelectedNodeId", "selected_node_id"),
        ("selected_node_id", "selected_node_id"),
        ("CandidateNodeId", "selected_node_id"),
        ("Role", "role"),
        ("role", "role"),
        ("Parent", "parent"),
        ("parent", "parent"),
        ("StructurePath", "structure_path"),
        ("structure_path", "structure_path"),
        ("ExpectedCoverage", "expected_coverage"),
        ("expected_coverage", "expected_coverage"),
        ("Rationale", "rationale"),
        ("rationale", "rationale"),
        ("ConceptKey", "concept_key"),
        ("concept_key", "concept_key"),
    ):
        value = source.get(src_key)
        if value is not None and dst_key not in target:
            target[dst_key] = value
    return target


def _review_specs_prompt(
    *,
    categories: list[dict[str, Any]],
    frame: pd.DataFrame,
    text_cols: Sequence[str],
    query: str,
    query_contract: dict[str, Any],
    runtime: dict[str, Any],
) -> str:
    payload = {
        "CandidateCategories": categories,
        "ExistingColumns": [str(col) for col in frame.columns],
        "EvidenceColumns": list(text_cols),
        "UserQuery": query,
        "TaskContract": query_contract,
        "RuntimeMetadataTemplate": runtime,
    }
    return f"""You are the TA++ v10 review stage. Review candidate facets and emit the final specs.json payload.

Rules:
- Keep only evidence-backed facets that can be tagged from the evidence columns.
- Keep a facet only if it has clear incremental utility for the UserQuery after considering ExistingColumns.
- In v10, also keep a facet only if it satisfies the TaskContract: it must support the focus variable, target contrast, required schema slot, or causal/concept role described there.
- Treat the TaskContract as a relevance floor, not a narrow ceiling. After task-critical slots are covered, keep complementary high-signal facets that improve downstream analysis specificity, evidence, depth, actionability, or coherence.
- Drop facets that duplicate existing structured columns, encode the target/outcome, use open-world vocabularies, cannot pass coverage gates, or are merely cosmetic details without a plausible relationship to the query.
- Prefer high-signal facets over broad or easy-to-tag facets. Do not discard complementary query-relevant facets solely to keep the count small.
- Before finalizing, ask whether the selected set can support a strong table analysis: concrete counts, segment comparisons, decision-tree splits, mechanism/confounder reasoning, useful negative contrasts, and action-oriented recommendations.
- For predictive requests, keep a compact non-redundant feature set when evidence supports it: object/aspect, severity or intensity, mechanism/root cause, scope/context, operational or action lever, and negative/low-risk contrast. Do not return only one or two specs unless the rejected candidates are unsupported, duplicative, or untaggable.
- For causal requests, keep treatment/change levers, mechanisms, confounders/context, outcome aspects, severity/intensity, and recommended-action proxies when supported.
- Compress narrow/broad duplicate facets, especially boolean pairs such as `CriticizesScript` plus `CriticizesScriptOrPlot`. Prefer a stable parent categorical facet plus genuinely complementary boolean or ordinal facets.
- Avoid final schemas dominated by mostly-Unknown, mostly-null, or single-valued facets when a more stable alternative is available.
- Prefer high- or medium-coverage categorical/boolean facets that will survive merge coverage gates. Numeric facets with many "None when not mentioned" values are allowed only as supporting specs.
- Use only these descriptions: categorical {{a, b, c, Unknown}}, ordinal {{1,2,3,4,5}}; None when not mentioned, numeric; <unit>; None when no explicit value, boolean mention {{true, false}}, boolean judgment {{true, false, Unknown}}.
- Preserve the intent metadata when available: intent_class, intent_subtype, planning_structure, selected_node_id, role, parent, and structure_path.
- Each returned spec must map to one selected planning node: `selected_node_id` must be in `planning_structure.SelectedNodes`, and `structure_path` must identify the root-to-selected-node path.
- For predictive requests, keep a non-redundant set of feature columns from the prediction tree that can support at least three useful splits or segment comparisons when the candidate pool supports it.
- For causal requests, keep treatment/causal-factor columns and explicit confounder columns when supported by evidence.
- For concept-attribute requests, keep useful concept-tree nodes; selected nodes do not have to be leaves.
- Reject any spec whose vocabulary label joins multiple concepts with or, and, /, &, or |. Split such concepts before returning specs.
- Use stable ASCII facet names with letters, digits, and underscores only.
- Return strict JSON only with this shape: {{"evidence_cols": [...], "task_mode": "attribution", "intent_class": "predictive|causal|concept_attribute|fallback_flat", "intent_subtype": "...", "planning_structure": <object>, "runtime": <runtime>, "specs": [{{"name": "FacetName", "description": "categorical {{...}}", "selected_node_id": "...", "role": "feature|confounder|facet|...", "parent": "...", "structure_path": "..."}}]}}.

INPUT_JSON:
{json.dumps(payload, ensure_ascii=False, indent=2)}
"""


def _coverage_rank(candidate: dict[str, Any]) -> int:
    coverage = str(candidate.get("ExpectedCoverage") or candidate.get("expected_coverage") or "").strip().lower()
    return {"high": 0, "medium": 1, "low": 2}.get(coverage, 3)


def _spec_is_merge_friendly(spec: dict[str, str]) -> bool:
    desc = spec.get("description", "").strip().lower()
    if _description_has_compound_vocab(desc):
        return False
    if desc.startswith("numeric"):
        return False
    if "none when no explicit value" in desc:
        return False
    return desc.startswith("categorical") or desc.startswith("boolean") or desc.startswith("ordinal")


def _candidate_to_spec(candidate: dict[str, Any], used: set[str]) -> Optional[dict[str, str]]:
    raw_name = candidate.get("name") or candidate.get("Name")
    raw_desc = candidate.get("description") or candidate.get("Description") or candidate.get("ValueSet")
    if not raw_name or not raw_desc:
        return None
    spec = {"name": _safe_facet_name(str(raw_name), used), "description": str(raw_desc).strip()}
    _copy_schema_metadata(candidate, spec)
    if not _spec_is_merge_friendly(spec):
        return None
    return spec


def _supplement_specs_from_candidates(
    specs: list[dict[str, str]],
    candidate_categories: Optional[Sequence[dict[str, Any]]],
    used: set[str],
) -> list[dict[str, str]]:
    if not candidate_categories:
        return specs
    existing = {spec["name"] for spec in specs}
    ordered_candidates = sorted(
        [candidate for candidate in candidate_categories if isinstance(candidate, dict)],
        key=lambda candidate: (_coverage_rank(candidate), str(candidate.get("Name") or candidate.get("name") or "")),
    )
    for candidate in ordered_candidates:
        candidate_name = str(candidate.get("Name") or candidate.get("name") or "")
        if candidate_name and _safe_facet_name(candidate_name, set()) in existing:
            continue
        spec = _candidate_to_spec(candidate, used)
        if spec is None:
            continue
        specs.append(spec)
        existing.add(spec["name"])
    return specs


def _normalize_specs_payload(
    payload: Any,
    runtime: dict[str, Any],
    text_cols: Sequence[str],
    candidate_categories: Optional[Sequence[dict[str, Any]]] = None,
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("review stage did not return a JSON object")
    specs = payload.get("specs") or payload.get("Specs") or []
    if not isinstance(specs, list):
        raise ValueError("review stage returned non-list specs")
    candidate_lookup: dict[str, dict[str, Any]] = {}
    for candidate in candidate_categories or []:
        if not isinstance(candidate, dict):
            continue
        candidate_name = str(candidate.get("Name") or candidate.get("name") or "")
        if candidate_name:
            candidate_lookup.setdefault(candidate_name, candidate)
            candidate_lookup.setdefault(_safe_facet_name(candidate_name, set()), candidate)
    used: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for item in specs:
        if not isinstance(item, dict):
            continue
        raw_name = item.get("name") or item.get("Name")
        raw_desc = item.get("description") or item.get("Description")
        if not raw_name or not raw_desc:
            continue
        spec = {"name": _safe_facet_name(str(raw_name), used), "description": str(raw_desc).strip()}
        if not _spec_is_merge_friendly(spec):
            continue
        _copy_schema_metadata(item, spec)
        metadata_source = candidate_lookup.get(str(raw_name)) or candidate_lookup.get(spec["name"])
        if metadata_source:
            _copy_schema_metadata(metadata_source, spec)
        normalized.append(spec)
    if not normalized:
        raise ValueError("review stage produced no usable specs")
    normalized = _supplement_specs_from_candidates(normalized, candidate_categories, used)
    runtime_payload = dict(runtime)
    runtime_payload["skill_version"] = "skill_v10"
    candidate_context = next((candidate for candidate in (candidate_categories or []) if isinstance(candidate, dict)), {})
    candidate_structure = candidate_context.get("PlanningStructure") or candidate_context.get("planning_structure") or {}
    review_structure = payload.get("planning_structure") or payload.get("PlanningStructure") or {}
    planning_structure = dict(review_structure) if isinstance(review_structure, dict) else {}
    if isinstance(candidate_structure, dict):
        for key in ("StructureType", "Root", "Nodes", "Edges"):
            if not planning_structure.get(key) and candidate_structure.get(key) is not None:
                planning_structure[key] = candidate_structure.get(key)
        selected_from_specs = [
            str(spec.get("selected_node_id") or spec.get("SelectedNodeId") or "").strip()
            for spec in normalized
            if str(spec.get("selected_node_id") or spec.get("SelectedNodeId") or "").strip()
        ]
        if selected_from_specs:
            planning_structure["SelectedNodes"] = list(dict.fromkeys(selected_from_specs))
        elif not planning_structure.get("SelectedNodes") and candidate_structure.get("SelectedNodes") is not None:
            planning_structure["SelectedNodes"] = candidate_structure.get("SelectedNodes")
    result = {
        "evidence_cols": list(payload.get("evidence_cols") or payload.get("EvidenceColumns") or text_cols),
        "task_mode": payload.get("task_mode") or "attribution",
        "intent_class": payload.get("intent_class") or payload.get("IntentClass") or candidate_context.get("IntentClass"),
        "intent_subtype": payload.get("intent_subtype") or payload.get("IntentSubtype") or candidate_context.get("IntentSubtype"),
        "planning_structure": planning_structure or candidate_structure,
        "runtime": {**runtime_payload, "created_at": runtime_payload.get("created_at") or datetime.now(timezone.utc).isoformat()},
        "specs": normalized,
    }
    planning_structure = result.get("planning_structure") or {}
    selected_nodes = set(planning_structure.get("SelectedNodes") or planning_structure.get("selected_nodes") or [])
    if selected_nodes:
        result["specs"] = [
            spec for spec in result["specs"]
            if str(spec.get("selected_node_id") or spec.get("SelectedNodeId") or "") in selected_nodes
        ]
    if not result["specs"]:
        raise ValueError("review stage produced no usable specs after selected-node filtering")
    _validate_planning_payload(result, stage="review_specs", category_keys=("specs",))
    return result


def _parse_query_contract(raw: Any) -> dict[str, Any]:
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    text = str(raw).strip()
    if not text:
        return {}
    if text.startswith("@"):
        return json.loads(Path(text[1:]).read_text(encoding="utf-8"))
    if text.startswith("{") or text.startswith("["):
        return json.loads(text)
    path = Path(text)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(text)


def _series_profile(series: pd.Series) -> dict[str, Any]:
    non_null = series.dropna()
    profile: dict[str, Any] = {
        "dtype": str(series.dtype),
        "missing_count": int(series.isna().sum()),
        "non_null_count": int(non_null.shape[0]),
        "unique_count": int(series.nunique(dropna=True)),
    }
    if non_null.empty:
        return profile
    if pd.api.types.is_numeric_dtype(series):
        quantiles = non_null.quantile([0.25, 0.5, 0.75]).to_dict()
        profile["numeric_summary"] = {
            "min": float(non_null.min()),
            "p25": float(quantiles.get(0.25)),
            "median": float(quantiles.get(0.5)),
            "p75": float(quantiles.get(0.75)),
            "max": float(non_null.max()),
        }
        return profile
    counts = series.astype(str).value_counts(dropna=True).head(12).to_dict()
    profile["top_values"] = {str(key): int(value) for key, value in counts.items()}
    return profile


def _focus_contrast_summary(frame: pd.DataFrame, query: str, query_contract: dict[str, Any]) -> dict[str, Any]:
    focus = str(query_contract.get("focus_variable") or "").strip()
    lowered_query = query.lower()
    summary: dict[str, Any] = {"focus_variable": focus or None, "status": "not_found"}
    if focus and focus in frame.columns:
        series = frame[focus]
        summary.update({"status": "existing_column", "column": focus, "profile": _series_profile(series)})
        if pd.api.types.is_numeric_dtype(series) and series.dropna().shape[0] > 0:
            q25 = float(series.dropna().quantile(0.25))
            q75 = float(series.dropna().quantile(0.75))
            summary["contrast_groups"] = {
                "low_or_short": {"rule": f"{focus} <= p25", "threshold": q25, "rows": int((series <= q25).sum())},
                "high_or_long": {"rule": f"{focus} >= p75", "threshold": q75, "rows": int((series >= q75).sum())},
            }
        else:
            counts = series.astype(str).value_counts(dropna=True).head(8).to_dict()
            summary["contrast_groups"] = {str(key): int(value) for key, value in counts.items()}
        return summary

    heuristic_columns: list[str] = []
    for column in frame.columns:
        name = str(column)
        lname = name.lower()
        if ("declin" in lowered_query and lname == "state") or lname in {"label_pos", "urgency", "resolution_minutes", "satisfaction_1to5"}:
            heuristic_columns.append(name)
        if focus and focus.lower() in lname:
            heuristic_columns.append(name)
    if "regional" in lowered_query and {"Latitude", "Longitude"}.issubset(set(map(str, frame.columns))):
        heuristic_columns.extend(["Latitude", "Longitude"])
    if "resolution" in lowered_query:
        for candidate in ("opened_at", "closed_at", "sys_updated_on"):
            if candidate in frame.columns:
                heuristic_columns.append(candidate)
    heuristic_columns = list(dict.fromkeys(heuristic_columns))[:6]
    if heuristic_columns:
        summary.update(
            {
                "status": "computable_or_proxy_columns",
                "proxy_columns": heuristic_columns,
                "profiles": {column: _series_profile(frame[column]) for column in heuristic_columns if column in frame.columns},
            }
        )
        return summary
    return summary


def _required_schema_slots(query_contract: dict[str, Any]) -> list[str]:
    family = str(query_contract.get("family") or "").strip()
    subtype = str(query_contract.get("subtype") or "").strip()
    if family == "predictive":
        return [
            "target-relevant object or aspect",
            "severity, intensity, or risk level",
            "mechanism or root-cause signal",
            "scope or context segment",
            "operational action, routing, or intervention proxy",
            "negative or low-risk contrast signal",
        ]
    if family == "causal":
        return [
            "outcome or experience aspect",
            "treatment or change lever",
            "mechanism",
            "confounder or context segment",
            "severity or intensity",
            "recommended action proxy",
        ]
    if family == "concept_attribute":
        return [
            "parent concept",
            "stable decomposition axis",
            "taggable facet",
            "useful internal node or summary facet",
            "context segment for comparing facets",
        ]
    if subtype:
        return ["task-relevant facet", "evidence-backed closed value domain", "analysis-supporting segment"]
    return []


def _build_task_contract(
    *,
    frame: pd.DataFrame,
    query: str,
    query_contract: dict[str, Any],
    text_cols: Sequence[str],
) -> dict[str, Any]:
    columns = []
    evidence = set(text_cols)
    for column in frame.columns:
        name = str(column)
        role = "text_evidence" if name in evidence else "structured_context"
        if name == str(query_contract.get("focus_variable") or ""):
            role = "focus_or_target"
        columns.append({"name": name, "dtype": str(frame[column].dtype), "role": role, "unique_count": int(frame[column].nunique(dropna=True))})
    return {
        "query_record": query_contract,
        "user_query": query,
        "evidence_columns": list(text_cols),
        "focus_contrast_summary": _focus_contrast_summary(frame, query, query_contract),
        "required_schema_slots": _required_schema_slots(query_contract),
        "column_roles": columns[:80],
        "selection_objective": (
            "Choose materialized columns that serve the query focus and target contrast. "
            "Do not select merely recurring text themes unless they explain, predict, decompose, or confound the focus described here. "
            "After task-critical slots are covered, keep complementary facets that improve downstream analysis specificity, evidence, depth, actionability, and coherence."
        ),
        "analysis_yield_guidelines": [
            "Support concrete counts, group comparisons, or prediction-tree splits.",
            "Preserve orthogonal roles: aspect/object, severity, mechanism, scope/context, action lever, and negative contrast when evidence supports them.",
            "Avoid returning only one or two columns unless all other candidates are unsupported or duplicative.",
            "Compress narrow/broad duplicate boolean columns into one stable categorical or the least redundant boolean set.",
            "Prefer columns that can lead to routing, triage, outreach, repair, quality-improvement, or diagnostic recommendations.",
        ],
    }


def _contract_user_query(query: str, existing: str, allowed: str, task_contract: dict[str, Any], stage_note: str | None = None) -> str:
    prefix = f"Stage: {stage_note}.\n" if stage_note else ""
    return (
        f"{prefix}Analysis task: {query}\n"
        f"Task contract JSON: {json.dumps(task_contract, ensure_ascii=False)}\n"
        f"Existing columns: {existing}\n"
        f"{allowed}\n"
        "V10 selection rules: first satisfy the Task contract, target/focus contrast, and required schema slots; "
        "then preserve complementary high-signal facets that improve specificity, evidence, depth, actionability, and coherence. "
        "The contract is a relevance floor, not a narrow ceiling; avoid one-facet schemas and narrow/broad duplicate booleans when richer non-redundant features are supported."
    )


def _categorize(
    *,
    frame: pd.DataFrame,
    workdir: Path,
    query: str,
    query_contract: dict[str, Any],
    model: str,
    attempts: int,
    workers: int,
    plan: dict[str, Any],
    text_cols: Sequence[str],
    execution_policy: dict[str, Any],
) -> list[dict[str, Any]]:
    categorization = plan.get("categorization") or {}
    strategy = str(categorization.get("strategy") or "single_pass")
    plan_id = plan.get("plan_id")
    column_name = " + ".join(text_cols)
    existing = ", ".join(str(col) for col in frame.columns)
    allowed = "Allowed representations: categorical, ordinal, numeric, boolean mention, boolean judgment."
    task_contract = _build_task_contract(frame=frame, query=query, query_contract=query_contract, text_cols=text_cols)
    visual_manifest = (plan.get("visual_preview") or {}).get("runtime_manifest")
    if isinstance(visual_manifest, dict):
        task_contract["visual_preview"] = {
            "mode": visual_manifest.get("mode"),
            "density": visual_manifest.get("density"),
            "resolution": visual_manifest.get("resolution"),
            "columns": visual_manifest.get("columns"),
            "pages": [
                {"path": page.get("path"), "row_count": len(page.get("rows") or [])}
                for page in (visual_manifest.get("pages") or [])
                if isinstance(page, dict)
            ],
            "limitations": visual_manifest.get("limitations"),
            "raw_data_required_for": visual_manifest.get("raw_data_required_for"),
            "usage_note": "Use attached visual preview images only for schema planning and semantic discovery; raw table/text remains authoritative for tagging, counts, calculations, and merge gates.",
        }
    planned_chunk_size = int(categorization.get("chunk_proposal_rows") or plan.get("chunk_size") or len(frame) or 1)
    cap = max(1, int(execution_policy.get("categorize_chunk_cap") or planned_chunk_size))
    chunk_size = min(planned_chunk_size, cap)
    forced_map_reduce = len(frame) > chunk_size
    if forced_map_reduce:
        strategy = "map_reduce"

    if strategy != "map_reduce":
        indices = list(range(len(frame)))
        payload = _invoke_json_stage(
            _subagent_prompt(
                _prompt_template("categorization.md"),
                {
                    "TextItems": _build_text_items(frame, indices, text_cols),
                    "ColumnName": column_name,
                    "UserQuery": _contract_user_query(query, existing, allowed, task_contract),
                },
            ),
            stage="categorize",
            model=model,
            workdir=workdir,
            log_name="categorize",
            attempts=attempts,
            timeout_s=900,
            validator=lambda value: _validate_planning_payload(value, stage="categorize", category_keys=("Categories",)),
        )
        _write_stage_json(
            workdir,
            "categorization.json",
            payload,
            kind="categorization",
            stage="categorize",
            model=model,
            plan_id=plan_id,
            reasoning_summary="single-pass categorization completed",
        )
        return _categories_from_payload(payload)

    prompt_body = _prompt_template("categorization_large_scale.md")
    max_chunks = max(
        int(categorization.get("max_chunk_proposals") or 20),
        (len(frame) + chunk_size - 1) // chunk_size,
    )
    ranges = _chunk_ranges(len(frame), chunk_size)[:max_chunks]
    retry_subchunk_size = max(1, int(execution_policy.get("categorize_retry_subchunk_size") or max(1, chunk_size // 2)))
    _tprint(
        f"[tapp-V10 categorize] strategy=map_reduce rows={len(frame)} "
        f"chunk_size={chunk_size} chunks={len(ranges)} retry_subchunk_size={retry_subchunk_size}"
    )

    fallback_events: list[dict[str, Any]] = []
    fallback_events_lock = threading.Lock()

    def invoke_proposal(*, log_name: str, artifact_name: str, chunk_label: str, indices: Sequence[int]) -> dict[str, Any]:
        start = int(indices[0]) if indices else 0
        end = int(indices[-1]) + 1 if indices else start
        input_payload = {
            "TextItems": _build_text_items(frame, indices, text_cols),
            "ColumnName": column_name,
            "UserQuery": _contract_user_query(
                query,
                existing,
                allowed,
                task_contract,
                f"chunk_proposal. Chunk {chunk_label} rows {start}-{end - 1}",
            ),
        }
        payload = _invoke_json_stage(
            _subagent_prompt(prompt_body, input_payload),
            stage="categorize_proposal",
            model=model,
            workdir=workdir,
            log_name=log_name,
            attempts=attempts,
            timeout_s=900,
        )
        _write_stage_json(
            workdir,
            f"categorization/{artifact_name}.json",
            payload,
            kind="categorize_proposal",
            stage="categorize_proposal",
            model=model,
            plan_id=plan_id,
            reasoning_summary=f"chunk proposal completed for rows {start}-{end - 1}",
        )
        return payload

    def run_proposal(chunk_id: int, start: int, end: int) -> list[dict[str, Any]]:
        indices = list(range(start, end))
        try:
            return [
                invoke_proposal(
                    log_name=f"categorize_proposal_{chunk_id}",
                    artifact_name=f"chunk_proposal_{chunk_id}",
                    chunk_label=str(chunk_id),
                    indices=indices,
                )
            ]
        except Exception as exc:  # noqa: BLE001
            if len(indices) <= retry_subchunk_size:
                raise
            _tprint(
                f"[tapp-V10 categorize fallback] chunk={chunk_id} rows={start}-{end - 1} "
                f"sub_size={retry_subchunk_size} reason={str(exc)[:200]!r}"
            )
            sub_payloads: list[dict[str, Any]] = []
            sub_errors: list[str] = []
            for sub_id, sub_start in enumerate(range(start, end, retry_subchunk_size)):
                sub_end = min(end, sub_start + retry_subchunk_size)
                sub_indices = list(range(sub_start, sub_end))
                try:
                    sub_payloads.append(
                        invoke_proposal(
                            log_name=f"categorize_proposal_{chunk_id}_sub_{sub_id}",
                            artifact_name=f"chunk_proposal_{chunk_id}_sub_{sub_id}",
                            chunk_label=f"{chunk_id}.{sub_id}",
                            indices=sub_indices,
                        )
                    )
                except Exception as sub_exc:  # noqa: BLE001
                    sub_errors.append(f"sub={sub_id} rows={sub_start}-{sub_end - 1} exc={sub_exc!r}")
                    _tprint(f"[tapp-V10 categorize warning] fallback failed chunk={chunk_id} sub={sub_id} exc={sub_exc!r}")
            event = {
                "chunk": chunk_id,
                "rows": [start, end - 1],
                "subchunk_size": retry_subchunk_size,
                "primary_error": repr(exc),
                "successful_subproposals": len(sub_payloads),
                "failed_subproposals": sub_errors,
            }
            with fallback_events_lock:
                fallback_events.append(event)
            _write_stage_json(
                workdir,
                f"categorization/chunk_proposal_{chunk_id}_fallback.json",
                event,
                kind="categorize_proposal_fallback",
                stage="categorize_proposal",
                model=model,
                plan_id=plan_id,
                reasoning_summary="categorization proposal chunk recovered by skill-owned subchunk fallback",
            )
            if not sub_payloads:
                raise RuntimeError(f"categorization proposal chunk {chunk_id} failed and fallback produced no proposals") from exc
            _tprint(
                f"[tapp-V10 categorize fallback ok] chunk={chunk_id} "
                f"sub_proposals={len(sub_payloads)} failed_subchunks={len(sub_errors)}"
            )
            return sub_payloads

    proposal_errors: list[str] = []
    if workers <= 1 or len(ranges) <= 1:
        proposals = []
        for chunk_id, (start, end) in enumerate(ranges):
            try:
                proposals.extend(run_proposal(chunk_id, start, end))
            except Exception as exc:  # noqa: BLE001
                proposal_errors.append(f"chunk={chunk_id} exc={exc!r}")
                _tprint(f"[tapp-V10 categorize warning] proposal failed chunk={chunk_id} exc={exc!r}")
    else:
        results: list[Optional[list[dict[str, Any]]]] = [None] * len(ranges)
        with ThreadPoolExecutor(max_workers=max(1, workers), thread_name_prefix="tapp-V10-cat") as ex:
            futures = {ex.submit(run_proposal, i, start, end): i for i, (start, end) in enumerate(ranges)}
            for fut in as_completed(futures):
                idx = futures[fut]
                try:
                    results[idx] = fut.result()
                except Exception as exc:  # noqa: BLE001
                    proposal_errors.append(f"chunk={idx} exc={exc!r}")
                    _tprint(f"[tapp-V10 categorize warning] proposal failed chunk={idx} exc={exc!r}")
        proposals = [payload for item in results if item is not None for payload in item]

    if proposal_errors or fallback_events:
        _write_stage_json(
            workdir,
            "categorization/proposal_errors.json",
            {
                "errors": proposal_errors,
                "fallback_events": fallback_events,
                "successful_proposals": len(proposals),
            },
            kind="categorization_errors",
            stage="categorize_proposal",
            model=model,
            plan_id=plan_id,
            reasoning_summary="categorization proposal failures and skill-owned fallback recovery events",
        )
    if not proposals:
        raise RuntimeError("categorization map-reduce produced no proposals")

    # Hierarchical (multi-level) consolidation reduce.
    # A single global_consolidation pass jams every chunk proposal into one prompt,
    # which overflows the model context when there are many proposals. When the
    # proposal set is too large we split it into batches, consolidate each batch into
    # partial facets, then feed the partial consolidations back as proposals and
    # consolidate again. This recurses to second/third levels as needed until the
    # input fits in one prompt.
    max_batch_items = max(2, int(execution_policy.get("consolidation_max_batch_proposals") or 24))
    max_batch_chars = max(20000, int(execution_policy.get("consolidation_max_input_chars") or 60000))

    def _proposals_chars(items: Sequence[dict[str, Any]]) -> int:
        return len(json.dumps(_compact_consolidation_payload(list(items)), ensure_ascii=False))

    def _facets_to_proposal(payload: dict[str, Any]) -> dict[str, Any]:
        facets = payload.get("ConsolidatedFacets") or payload.get("Categories") or []
        return {
            "TaskType": "CategorizationLargeScale",
            "Stage": "chunk_proposal",
            "IntentClass": payload.get("IntentClass"),
            "IntentSubtype": payload.get("IntentSubtype"),
            "CandidateFacets": [
                {
                    "Name": facet.get("Name"),
                    "Description": facet.get("Description"),
                    "ValueSet": facet.get("ValueSet"),
                    "CandidateNodeId": facet.get("SelectedNodeId") or facet.get("ConceptKey"),
                    "Role": facet.get("Role"),
                    "Parent": facet.get("Parent"),
                    "StructurePath": facet.get("StructurePath"),
                    "Rationale": facet.get("Rationale"),
                    "ExpectedCoverage": facet.get("ExpectedCoverage"),
                    "ConceptKey": facet.get("ConceptKey"),
                }
                for facet in facets
                if isinstance(facet, dict)
            ],
        }

    def _run_consolidation(
        items: Sequence[dict[str, Any]], *, log_name: str, artifact_name: str, canonical: bool
    ) -> dict[str, Any]:
        payload = _invoke_json_stage(
            _subagent_prompt(
                prompt_body,
                {
                    "TextItems": [],
                    "ColumnName": column_name,
                    "UserQuery": (
                        _contract_user_query(query, existing, allowed, task_contract, "global_consolidation")
                        + "\nPrior chunk proposals JSON: "
                        + json.dumps(_compact_consolidation_payload(list(items)), ensure_ascii=False)
                    ),
                },
            ),
            stage="categorize_consolidation",
            model=model,
            workdir=workdir,
            log_name=log_name,
            attempts=attempts,
            timeout_s=900,
            validator=lambda value: _validate_planning_payload(value, stage="categorize_consolidation", category_keys=("ConsolidatedFacets",)),
        )
        _write_stage_json(
            workdir,
            artifact_name,
            payload,
            kind="categorize_consolidation",
            stage="categorize_consolidation",
            model=model,
            plan_id=plan_id,
            reasoning_summary=(
                "global facet consolidation completed"
                if canonical
                else "partial facet consolidation completed"
            ),
        )
        return payload

    def _run_consolidation_resilient(
        items: list[dict[str, Any]],
        *,
        level: int,
        top: bool,
        log_name: str,
        artifact_name: str,
        canonical: bool,
    ) -> dict[str, Any]:
        try:
            return _run_consolidation(items, log_name=log_name, artifact_name=artifact_name, canonical=canonical)
        except RuntimeError as exc:
            if not _is_token_limit_error(exc) or len(items) <= 1:
                raise
            midpoint = max(1, len(items) // 2)
            _tprint(
                f"[tapp-v10 consolidate split] level={level} top={top} "
                f"items={len(items)} reason=token_limit"
            )
            left = _consolidate_hierarchical(items[:midpoint], level + 1, top=False)
            right = _consolidate_hierarchical(items[midpoint:], level + 1, top=False)
            return _run_consolidation_resilient(
                [_facets_to_proposal(left), _facets_to_proposal(right)],
                level=level + 1,
                top=top,
                log_name=f"{log_name}_split_retry",
                artifact_name=artifact_name,
                canonical=canonical,
            )

    def _consolidate_hierarchical(items: list[dict[str, Any]], level: int, top: bool) -> dict[str, Any]:
        fits = len(items) <= max_batch_items and _proposals_chars(items) <= max_batch_chars
        # Build batches that each merge >= 2 proposals so the partial count strictly
        # decreases every level. Chunking by item-count alone can yield a single batch
        # == all items when the char budget (not the count) is what is exceeded, which
        # makes the recursion re-process an identical set forever (observed
        # RecursionError on large tables). Greedy char-aware packing with a >= 2
        # items-per-batch floor guarantees termination.
        batches: list[list[dict[str, Any]]] = []
        if not fits and len(items) > 1:
            cur: list[dict[str, Any]] = []
            cur_chars = 0
            for it in items:
                it_chars = _proposals_chars([it])
                if cur and len(cur) >= 2 and (
                    len(cur) >= max_batch_items or cur_chars + it_chars > max_batch_chars
                ):
                    batches.append(cur)
                    cur = []
                    cur_chars = 0
                cur.append(it)
                cur_chars += it_chars
            if cur:
                if len(cur) == 1 and batches:
                    batches[-1].extend(cur)  # avoid a trailing singleton (no merge progress)
                else:
                    batches.append(cur)
        # Single consolidation call when the input already fits, is a singleton, or
        # could not be split into >= 2 progress-making batches (e.g. only two huge
        # proposals). This is the termination guarantee.
        if fits or len(items) <= 1 or len(batches) <= 1:
            if top:
                return _run_consolidation_resilient(
                    items,
                    level=level,
                    top=top,
                    log_name="categorize_consolidation",
                    artifact_name="categorization/global_consolidation.json",
                    canonical=True,
                )
            return _run_consolidation_resilient(
                items,
                level=level,
                top=top,
                log_name=f"categorize_consolidation_l{level}",
                artifact_name=f"categorization/consolidation_level_{level}/single.json",
                canonical=False,
            )
        batch_workers = max(1, min(int(workers), len(batches)))
        _tprint(
            f"[tapp-v10 consolidate] level={level} proposals={len(items)} "
            f"batches={len(batches)} batch_size={max_batch_items} batch_workers={batch_workers} "
            f"chars={_proposals_chars(items)}"
        )

        def _consolidate_batch(batch_id: int, batch: list[dict[str, Any]]) -> dict[str, Any]:
            # Sibling batches at the same level are independent, so they run in parallel.
            if len(batch) > 1 and _proposals_chars(batch) > max_batch_chars:
                part = _consolidate_hierarchical(batch, level + 1, top=False)
            else:
                part = _run_consolidation_resilient(
                    batch,
                    level=level,
                    top=False,
                    log_name=f"categorize_consolidation_l{level}_b{batch_id}",
                    artifact_name=f"categorization/consolidation_level_{level}/partial_{batch_id}.json",
                    canonical=False,
                )
            return _facets_to_proposal(part)

        partials: list[Optional[dict[str, Any]]] = [None] * len(batches)
        if batch_workers <= 1 or len(batches) <= 1:
            for batch_id, batch in enumerate(batches):
                partials[batch_id] = _consolidate_batch(batch_id, batch)
        else:
            with ThreadPoolExecutor(max_workers=batch_workers, thread_name_prefix="tapp-v10-consol") as ex:
                futures = {ex.submit(_consolidate_batch, i, batch): i for i, batch in enumerate(batches)}
                for fut in as_completed(futures):
                    partials[futures[fut]] = fut.result()
        return _consolidate_hierarchical([p for p in partials if p is not None], level + 1, top=top)

    consolidated = _consolidate_hierarchical(list(proposals), level=0, top=True)

    final_payload = _invoke_json_stage(
        _subagent_prompt(
            prompt_body,
            {
                "TextItems": [],
                "ColumnName": column_name,
                "UserQuery": (
                    _contract_user_query(query, existing, allowed, task_contract, "final_selection")
                    + "\nSelection budget: keep a stable set of useful facets that satisfy the Task contract.\n"
                    + f"Consolidated facets JSON: {json.dumps(consolidated, ensure_ascii=False)}"
                ),
            },
        ),
        stage="categorize_final_selection",
        model=model,
        workdir=workdir,
        log_name="categorize_final_selection",
        attempts=attempts,
        timeout_s=900,
        validator=lambda value: _validate_planning_payload(value, stage="categorize_final_selection", category_keys=("Categories",)),
    )
    _write_stage_json(
        workdir,
        "categorization/final_selection.json",
        final_payload,
        kind="categorize_final_selection",
        stage="categorize_final_selection",
        model=model,
        plan_id=plan_id,
        reasoning_summary="final facet selection completed",
    )
    return _categories_from_payload(final_payload)


def _tag_specs(
    *,
    frame: pd.DataFrame,
    workdir: Path,
    query: str,
    model: str,
    attempts: int,
    workers: int,
    plan: dict[str, Any],
    text_cols: Sequence[str],
    specs_payload: dict[str, Any],
    execution_policy: dict[str, Any],
) -> None:
    tags_dir = workdir / "tags"
    tags_dir.mkdir(parents=True, exist_ok=True)
    plan_chunk_size = int(plan.get("chunk_size") or len(frame) or 1)
    tag_cap = max(1, int(execution_policy.get("tag_chunk_cap") or plan_chunk_size))
    chunk_size = min(plan_chunk_size, tag_cap)
    ranges = _chunk_ranges(len(frame), chunk_size)
    label_chunk_size = int(plan.get("label_chunk_size") or 10)
    label_chunking = bool((plan.get("operators") or {}).get("tagging", {}).get("label_chunking"))
    column_name = " + ".join(text_cols)
    plan_id = plan.get("plan_id")
    tagging_prompt = _prompt_template("tagging.md")
    tagging_large_prompt = _prompt_template("tagging_large_scale.md")
    consolidation_prompt = _prompt_template("tagging_consolidation.md")
    _tprint(f"[tapp-V10 tag] facets={len(specs_payload.get('specs') or [])} chunk_size={chunk_size} chunks={len(ranges)}")

    def invoke_checked(prompt: str, *, log_name: str, indices: Sequence[int], stage: str) -> Any:
        last_payload: Any = None
        last_issue = "unknown"
        required_indices = [int(idx) for idx in indices]
        required_indices_json = json.dumps(required_indices, ensure_ascii=False)
        for validate_attempt in range(1, max(1, attempts) + 1):
            retry_note = (
                "\n\nSTRICT CORRECTION REQUIRED. The previous output was not parseable strict JSON "
                "or did not exactly cover the required row indices.\n"
                f"Required original row indices ({len(required_indices)} total): {required_indices_json}\n"
                "Return corrected strict JSON only. Results.Items must contain exactly one key for every listed "
                "original row index and no other keys. Do not renumber later chunks from 0. Do not use ranges, "
                "ellipses, compressed keys, or summary keys. If uncertain, use Unknown for that row."
            )
            try:
                payload = _invoke_json_stage(
                    prompt if validate_attempt == 1 else prompt + retry_note,
                    stage=stage,
                    model=model,
                    workdir=workdir,
                    log_name=f"{log_name}_try{validate_attempt}",
                    attempts=1,
                    timeout_s=900,
                )
            except Exception as exc:  # noqa: BLE001
                last_payload = repr(exc)
                last_issue = "parse_error"
                _tprint(f"[tapp-V10 tag retry] stage={stage} log={log_name} validation_attempt={validate_attempt} issue=parse_error exc={exc!r}")
                continue
            last_payload = payload
            if _items_cover_indices(payload, indices):
                return payload
            last_issue = "index_coverage"
            _tprint(f"[tapp-V10 tag retry] stage={stage} log={log_name} validation_attempt={validate_attempt} issue=index_coverage")
        raise RuntimeError(f"{stage} failed strict validation for {log_name}: issue={last_issue} payload={last_payload!r}")

    def tag_one(spec: dict[str, Any], chunk_id: int, start: int, end: int) -> Path:
        name = str(spec["name"])
        description = str(spec.get("description") or "")
        indices = list(range(start, end))
        text_items = _build_text_items(frame, indices, text_cols)
        vocab = _extract_vocab(description)
        use_label_chunks = label_chunking and len(vocab) > label_chunk_size > 0
        final_path = tags_dir / f"{name}_chunk_{chunk_id}.json"
        if final_path.exists():
            try:
                existing_payload = json.loads(final_path.read_text(encoding="utf-8"))
                if _items_cover_indices(existing_payload, indices):
                    _tprint(f"[tapp-V10 tag reuse] facet={name} chunk={chunk_id}")
                    return final_path
            except Exception:
                pass
        required_indices_json = json.dumps([int(idx) for idx in indices], ensure_ascii=False)
        coverage_contract = (
            f"Required original row indices ({len(indices)} total): {required_indices_json}\n"
            "Results.Items must contain exactly these keys as original row-index strings and no other keys. "
            "Do not renumber this chunk from 0. Do not omit rows. Do not use ranges, ellipses, compressed keys, "
            "or summary keys. If uncertain, return Unknown for that row."
        )

        if not use_label_chunks:
            def build_tag_input(sub_indices: Sequence[int]) -> dict[str, Any]:
                sub_required_json = json.dumps([int(i) for i in sub_indices], ensure_ascii=False)
                sub_coverage = (
                    f"Required original row indices ({len(sub_indices)} total): {sub_required_json}\n"
                    "Results.Items must contain exactly these keys as original row-index strings and no other keys. "
                    "Do not renumber this chunk from 0. Do not omit rows. Do not use ranges, ellipses, compressed keys, "
                    "or summary keys. If uncertain, return Unknown for that row."
                )
                return {
                    "TextItems": _build_text_items(frame, sub_indices, text_cols),
                    "ColumnName": column_name,
                    "UserQuery": (
                        f"Analysis task: {query}\nFacet name: {name}\nFacet description: {description}\n"
                        f"Return one scalar value per listed row index.\n{sub_coverage}"
                    ),
                }

            try:
                payload = invoke_checked(
                    _subagent_prompt(tagging_prompt, build_tag_input(indices)),
                    log_name=f"tag_{name}_chunk_{chunk_id}",
                    indices=indices,
                    stage="tag",
                )
            except RuntimeError as exc:
                fallback_size = int(execution_policy.get("tag_retry_subchunk_size") or 200)
                if len(indices) <= fallback_size:
                    raise
                _tprint(f"[tapp-V10 tag fallback] facet={name} chunk={chunk_id} sub_size={fallback_size} reason={str(exc)[:200]!r}")
                merged_results: dict[str, Any] = {}
                last_sub_payload: dict[str, Any] | None = None
                sub_count = 0
                for sub_id, sub_start in enumerate(range(0, len(indices), fallback_size)):
                    sub_indices = indices[sub_start:sub_start + fallback_size]
                    last_sub_payload = invoke_checked(
                        _subagent_prompt(tagging_prompt, build_tag_input(sub_indices)),
                        log_name=f"tag_{name}_chunk_{chunk_id}_sub_{sub_id}",
                        indices=sub_indices,
                        stage="tag",
                    )
                    sub_results = _items_payload(last_sub_payload)
                    if not isinstance(sub_results, dict):
                        sub_results = {}
                    merged_results.update({str(k): v for k, v in sub_results.items()})
                    sub_count += 1
                payload = dict(last_sub_payload or {})
                payload["Results"] = {"Items": merged_results}
                _tprint(f"[tapp-V10 tag fallback ok] facet={name} chunk={chunk_id} sub_chunks={sub_count} merged_rows={len(merged_results)}")
            _write_json(final_path, payload)
            ref = _register_artifact(workdir, "tags", final_path, "tag")
            _record_trace(
                workdir,
                stage="tag",
                model=model,
                plan_id=plan_id,
                output_ref=ref,
                reasoning_summary=f"tagged {name} rows {start}-{end - 1}",
            )
            return final_path

        label_chunks = [vocab[i:i + label_chunk_size] for i in range(0, len(vocab), label_chunk_size)]
        candidate_chunks: list[dict[str, Any]] = []
        for label_id, labels in enumerate(label_chunks):
            input_payload = {
                "TextItems": text_items,
                "ColumnName": column_name,
                "UserQuery": (
                    f"Analysis task: {query}\nFacet name: {name}\nFacet description: {description}\n"
                    f"Current allowed label chunk: {labels}\nFull vocabulary: {vocab}\n{coverage_contract}"
                ),
            }
            payload = invoke_checked(
                _subagent_prompt(tagging_large_prompt, input_payload),
                log_name=f"tag_{name}_chunk_{chunk_id}_labels_{label_id}",
                indices=indices,
                stage="tag",
            )
            tmp_path = tags_dir / "_label_chunks" / f"{name}_chunk_{chunk_id}_labels_{label_id}.json"
            _write_json(tmp_path, payload)
            candidate_chunks.append({"ChunkName": f"labels_{label_id}", "AllowedLabels": labels, "Results": payload.get("Results")})

        final_payload = invoke_checked(
            _subagent_prompt(
                consolidation_prompt,
                {
                    "TextItems": text_items,
                    "ColumnName": column_name,
                    "UserQuery": f"Facet name: {name}\nFacet description: {description}\nFull vocabulary: {vocab}\n{coverage_contract}",
                    "CandidateChunks": candidate_chunks,
                },
            ),
            log_name=f"tag_consolidation_{name}_chunk_{chunk_id}",
            indices=indices,
            stage="tag_consolidation",
        )
        _write_json(final_path, final_payload)
        ref = _register_artifact(workdir, "tags", final_path, "tag_consolidation")
        _record_trace(
            workdir,
            stage="tag_consolidation",
            model=model,
            plan_id=plan_id,
            output_ref=ref,
            reasoning_summary=f"consolidated label chunks for {name} rows {start}-{end - 1}",
        )
        return final_path

    tasks = [(spec, chunk_id, start, end) for spec in specs_payload["specs"] for chunk_id, (start, end) in enumerate(ranges)]
    tag_errors: list[dict[str, Any]] = []
    if workers <= 1 or len(tasks) <= 1:
        for spec, chunk_id, start, end in tasks:
            try:
                tag_one(spec, chunk_id, start, end)
            except Exception as exc:  # noqa: BLE001
                name = str(spec.get("name"))
                tag_errors.append({"facet": name, "chunk": chunk_id, "rows": [start, end - 1], "error": repr(exc)})
                _tprint(f"[tapp-V10 tag error] facet={name} chunk={chunk_id} exc={exc!r}; continuing")
        if tag_errors:
            _write_json(tags_dir / "tag_errors.json", tag_errors)
        return
    with ThreadPoolExecutor(max_workers=max(1, workers), thread_name_prefix="tapp-V10-tag") as ex:
        futures = {ex.submit(tag_one, spec, chunk_id, start, end): (spec["name"], chunk_id) for spec, chunk_id, start, end in tasks}
        for fut in as_completed(futures):
            name, chunk_id = futures[fut]
            try:
                fut.result()
                _tprint(f"[tapp-V10 tag done] facet={name} chunk={chunk_id}")
            except Exception as exc:  # noqa: BLE001
                tag_errors.append({"facet": str(name), "chunk": chunk_id, "error": repr(exc)})
                _tprint(f"[tapp-V10 tag error] facet={name} chunk={chunk_id} exc={exc!r}; continuing")
    if tag_errors:
        _write_json(tags_dir / "tag_errors.json", tag_errors)


def _locate_augmented_table(workdir: Path) -> Optional[Path]:
    for name in ("augment.xlsx", "augmented.xlsx", "augment.csv", "augmented.csv", "augment.parquet", "augmented.parquet"):
        path = workdir / name
        if path.exists() and path.is_file():
            return path
    return None


def _prepare_plan(args: Any, input_table: Path, workdir: Path, model: str, workers: int) -> dict[str, Any]:
    rc, stdout, stderr = _run_tapp_cli(
        [
            "plan",
            "--input",
            str(input_table.resolve()),
            "--workdir",
            str(workdir.resolve()),
            "--estimated-labels",
            str(args.estimated_labels),
            "--estimated-facets",
            str(args.estimated_facets),
            "--host-model",
            model,
            "--concurrency",
            str(max(1, workers)),
            "--categorization-strategy",
            str(args.categorization_strategy),
        ],
        timeout_s=600,
    )
    (workdir / "_V10_plan_stdout.txt").write_text(stdout, encoding="utf-8")
    (workdir / "_V10_plan_stderr.txt").write_text(stderr, encoding="utf-8")
    if rc != 0:
        raise RuntimeError(f"plan failed rc={rc} stderr={stderr[:300]!r}")
    return json.loads((workdir / "execution_plan.json").read_text(encoding="utf-8"))


def _merge(input_table: Path, workdir: Path, output: Path, args: Any) -> None:
    cmd = [
        "merge",
        "--input",
        str(input_table.resolve()),
        "--workdir",
        str(workdir.resolve()),
        "--output",
        str(output.resolve()),
    ]
    max_null_share = getattr(args, "max_null_share", None)
    if max_null_share is not None:
        cmd += ["--max-null-share", str(float(max_null_share))]
    if args.allow_low_coverage_fallback:
        cmd.append("--allow-low-coverage-fallback")
    rc, stdout, stderr = _run_tapp_cli(cmd, timeout_s=900)
    (workdir / "_V10_merge_stdout.txt").write_text(stdout, encoding="utf-8")
    (workdir / "_V10_merge_stderr.txt").write_text(stderr, encoding="utf-8")
    if rc != 0:
        raise RuntimeError(f"merge failed rc={rc} stderr={stderr[:300]!r}")
    merge_report_path = workdir / "merge_report.json"
    if not merge_report_path.exists():
        raise RuntimeError("merge did not write merge_report.json")
    merge_report = json.loads(merge_report_path.read_text(encoding="utf-8"))
    kept = merge_report.get("kept")
    kept_count = len(kept) if isinstance(kept, list) else int(kept or 0) if isinstance(kept, int) else 0
    if merge_report.get("status") != "success" or kept_count <= 0:
        raise RuntimeError("merge did not keep any facets")


def cmd_augment_e2e(args: Any) -> int:
    global STAGE_SEMAPHORE, CLAUDE_TIMEOUT_S
    input_table = Path(args.input).resolve()
    workdir = Path(args.workdir).resolve()
    model = str(args.model)
    attempts = max(1, int(args.attempts))
    CLAUDE_TIMEOUT_S = max(1, int(args.claude_timeout))

    if args.force and workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    output_format = str(args.output_format or "xlsx")
    output = Path(args.output).resolve() if args.output else (workdir / f"augment.{output_format}").resolve()
    if output.exists() and not args.force:
        print(f"AUGMENT_OK {output}")
        return 0

    try:
        frame = _read_table(input_table).reset_index(drop=True)
        query_contract = _parse_query_contract(getattr(args, "query_contract_json", None))
        text_cols = _text_columns_for_tapp(frame)
        contract_evidence_cols = [str(col) for col in query_contract.get("text_evidence_columns") or [] if str(col) in frame.columns]
        if contract_evidence_cols:
            text_cols = contract_evidence_cols
        if not text_cols:
            raise RuntimeError("no text evidence columns available")
        p95_chars = _combined_text_p95(frame, text_cols)
        policy = _model_policy(model, p95_chars)
        explicit_workers = max(0, int(getattr(args, "workers", 0) or 0))
        max_worker_budget = max(0, int(getattr(args, "max_workers", 0) or 0))
        if max_worker_budget > 0:
            # The harness worker budget is a FLOOR for the independent map stages
            # (chunk proposals, hierarchical consolidation batches, tagging). These
            # calls are order-independent and idempotent, so a conservative host
            # model must not be allowed to starve throughput by passing a lower
            # --workers. A higher explicit --workers is still capped at the budget.
            workers = max_worker_budget
            worker_decision = {
                "worker_decision_source": "harness_budget_floor",
                "max_worker_budget": max_worker_budget,
                "host_requested_workers": explicit_workers or None,
                "worker_decision_reason": "budget_enforced_as_floor",
            }
        elif explicit_workers > 0:
            workers = explicit_workers
            worker_decision = {
                "worker_decision_source": "host_llm_execution_decision",
                "max_worker_budget": explicit_workers,
                "worker_decision_reason": "explicit_workers_argument",
            }
        else:
            workers, worker_decision = _decide_workers(model, 2, p95_chars, len(frame))
        STAGE_SEMAPHORE = threading.Semaphore(workers) if workers > 1 else None
        explicit_categorize_chunk_size = max(0, int(getattr(args, "categorize_chunk_size", 0) or 0))
        explicit_tag_chunk_size = max(0, int(getattr(args, "tag_chunk_size", 0) or 0))
        explicit_decisions: dict[str, Any] = {}
        if explicit_categorize_chunk_size > 0:
            policy["categorize_chunk_cap"] = explicit_categorize_chunk_size
            explicit_decisions["categorize_chunk_size"] = explicit_categorize_chunk_size
        if explicit_tag_chunk_size > 0:
            policy["tag_chunk_cap"] = explicit_tag_chunk_size
            explicit_decisions["tag_chunk_size"] = explicit_tag_chunk_size
        if explicit_decisions:
            policy["selected_by"] = "host_llm_execution_decision"
            policy["host_llm_overrides"] = explicit_decisions
        decision_note = getattr(args, "execution_decision_note", None)
        if decision_note:
            policy["execution_decision_note"] = str(decision_note)[:1000]
        policy.update(
            {
                "skill_version": "skill_v10",
                "selected_by": policy.get("selected_by") or "skill_v10_recipe_default",
                "workers": workers,
                **worker_decision,
                "stage_concurrency": {
                    "category_proposals": workers,
                    "category_consolidation": workers,
                    "tag_chunks": workers,
                    "llm_call_semaphore": workers,
                },
                "text_cols": list(text_cols),
                "combined_text_p95_chars": p95_chars,
            }
        )
        _write_json(workdir / "evidence_columns.json", {"evidence_cols": text_cols, "combined_text_p95_chars": p95_chars})

        plan = _prepare_plan(args, input_table, workdir, model, workers)
        plan["skill_version"] = "skill_v10"
        plan["skill_v10_host_execution"] = policy
        if query_contract:
            plan["query_contract"] = query_contract
        plan.setdefault("runtime_metadata_template", {})["skill_version"] = "skill_v10"
        if query_contract:
            plan.setdefault("runtime_metadata_template", {})["query_contract_id"] = query_contract.get("id")

        visual_plan = plan.get("visual_preview") or {}
        if visual_plan.get("enabled", True):
            resolution = visual_plan.get("resolution") or {}
            visual_manifest = generate_visual_preview(
                frame,
                workdir,
                query=str(args.query),
                text_cols=text_cols,
                source_table=input_table,
                width=int(resolution.get("width", 1600)),
                height=int(resolution.get("height", 2200)),
                density=str(visual_plan.get("density") or "ocr"),
                overview_rows=int(visual_plan.get("overview_rows") or 60),
                rows_per_image=int(visual_plan.get("rows_per_image") or 60),
                max_columns=int(visual_plan.get("max_columns") or 6),
            )
            visual_manifest_path = Path(str(visual_manifest.get("manifest_path")))
            visual_ref = _register_artifact(workdir, "visual_preview", visual_manifest_path, "visual_preview")
            page_refs: list[str] = []
            for page in visual_manifest.get("pages") or []:
                page_path = visual_manifest_path.parent / str(page.get("path"))
                if page_path.exists():
                    ref = _register_artifact(workdir, "visual_preview_page", page_path, "visual_preview")
                    if ref:
                        page_refs.append(ref)
            plan["visual_preview"] = {
                **visual_plan,
                "runtime_manifest": {
                    key: value
                    for key, value in visual_manifest.items()
                    if key not in {"manifest_path"}
                },
                "manifest_path": str(visual_manifest_path.relative_to(workdir)),
                "artifact_ref": visual_ref,
                "page_refs": page_refs,
            }
        _write_json(workdir / "execution_plan.json", plan)
        _register_artifact(workdir, "execution_plan", workdir / "execution_plan.json", "plan")

        categories = _categorize(
            frame=frame,
            workdir=workdir,
            query=str(args.query),
            query_contract=query_contract,
            model=model,
            attempts=attempts,
            workers=workers,
            plan=plan,
            text_cols=text_cols,
            execution_policy=policy,
        )
        if not categories:
            raise RuntimeError("categorization returned no candidate facets")

        review_payload = _invoke_json_stage(
            _review_specs_prompt(
                categories=categories,
                frame=frame,
                text_cols=text_cols,
                query=str(args.query),
                query_contract=query_contract,
                runtime=plan.get("runtime_metadata_template") or {},
            ),
            stage="review",
            model=model,
            workdir=workdir,
            log_name="review",
            attempts=attempts,
            timeout_s=900,
        )
        specs_payload = _normalize_specs_payload(
            review_payload,
            plan.get("runtime_metadata_template") or {},
            text_cols,
            categories,
        )
        _write_stage_json(
            workdir,
            "specs.json",
            specs_payload,
            kind="specs",
            stage="review",
            model=model,
            plan_id=plan.get("plan_id"),
            reasoning_summary="reviewed final TA++ v10 specs",
        )

        _tag_specs(
            frame=frame,
            workdir=workdir,
            query=str(args.query),
            model=model,
            attempts=attempts,
            workers=workers,
            plan=plan,
            text_cols=text_cols,
            specs_payload=specs_payload,
            execution_policy=policy,
        )
        _merge(input_table, workdir, output, args)
        print(f"AUGMENT_OK {output}")
        return 0
    except Exception as exc:  # noqa: BLE001
        failure = {"status": "failed", "error": repr(exc), "finished_at": datetime.now(timezone.utc).isoformat()}
        _write_json(workdir / "augment_e2e_error.json", failure)
        print(f"AUGMENT_FAIL {exc!r}", file=sys.stderr)
        return 1

