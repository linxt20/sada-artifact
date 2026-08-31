"""Lab8 pairwise grader and trust utilities.

This module is an isolated Lab8 copy of the Lab7 pairwise grader
core. It keeps Lab5's pairwise + Bradley-Terry protocol, then extends the
pairwise record with auditable evidence citations, augmented-column citations,
per-dimension raw winner/margin, and human-review agreement helpers.

It deliberately has no dependency on paper/lab5/script/quality_v2.py and all
CLI outputs default to paper/lab8/grader_runs so existing lab outputs are not
rewritten by accident.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parent
LAB8_DIR = ROOT.parent
DEFAULT_OUTPUT_DIR = LAB8_DIR / "grader_runs"

PK_DIMENSIONS: Tuple[str, ...] = (
    "specificity",
    "evidence",
    "depth",
    "actionability",
    "coherence",
)

MARGIN_TO_WEIGHT: Dict[str, float] = {
    "small": 1.0,
    "medium": 1.5,
    "large": 2.0,
}


def strip_yaml_header(text: str) -> str:
    if "\n---\n" in text:
        return text.split("\n---\n", 1)[1]
    return text


def find_claude() -> str:
    exe = shutil.which("claude") or os.path.expandvars(r"%APPDATA%\npm\claude.CMD")
    if not Path(exe).exists():
        sys.exit(f"claude CLI not found: {exe}")
    path = Path(exe)
    if os.name == "nt" and path.suffix.lower() in {".cmd", ".bat"}:
        native = path.parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
        if native.exists():
            return str(native)
    return exe


def _popen_group_kwargs() -> Dict[str, Any]:
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
    env: Optional[Dict[str, str]] = None,
    timeout_s: int,
) -> Tuple[int, bytes, bytes, bool]:
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
            more_stdout, more_stderr = proc.communicate(timeout=5)
            stdout = more_stdout or stdout
            stderr = more_stderr or stderr
        except subprocess.TimeoutExpired:
            _kill_process_tree(proc)
            proc.kill()
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except Exception:
                        pass
            try:
                proc.wait(timeout=1)
            except Exception:
                pass
        timeout_msg = f"timeout after {timeout_s}s".encode("utf-8")
        stderr = (stderr or b"") + (b"\n" if stderr else b"") + timeout_msg
        return 124, stdout or b"", stderr, True


def _strip_to_json(text: str) -> Optional[str]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text)
    if text.startswith("{") and text.endswith("}"):
        return text
    a, b = text.find("{"), text.rfind("}")
    if a >= 0 and b > a:
        return text[a:b + 1]
    return None


def _extract_text_from_claude_json(raw: str) -> str:
    if not raw:
        return ""
    try:
        data = json.loads(raw)
    except Exception:
        return raw
    if isinstance(data, dict):
        if "is_error" in data and data.get("is_error"):
            return ""
        return data.get("result") or data.get("response") or ""
    return ""


def _invoke_claude(
    claude_exe: str,
    prompt: str,
    timeout_s: int,
    model: Optional[str],
    fallback_model: Optional[str],
) -> Tuple[int, str, str]:
    cmd = [
        claude_exe,
        "-p",
        "--bare",
        "--no-session-persistence",
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
    ]
    if model:
        cmd += ["--model", model]
    if fallback_model:
        cmd += ["--fallback-model", fallback_model]

    env = os.environ.copy()
    env["CLAUDE_CODE_SIMPLE"] = "1"
    with tempfile.TemporaryDirectory(prefix="lab8_grader_") as sandbox:
        rc, stdout, stderr, _timed_out = _run_capture_timeout(
            cmd,
            input_bytes=prompt.encode("utf-8"),
            env=env,
            timeout_s=timeout_s,
            cwd=Path(sandbox),
        )
        return (
            rc,
            stdout.decode("utf-8", errors="replace"),
            stderr.decode("utf-8", errors="replace"),
        )


def _call_claude_json(
    claude_exe: str,
    prompt: str,
    timeout_s: int,
    model: Optional[str],
    fallback_model: Optional[str],
    max_attempts: int,
) -> Tuple[Optional[Dict[str, Any]], str, int]:
    last_text = ""
    last_rc = -1
    for attempt in range(1, max_attempts + 1):
        attempt_prompt = prompt
        if attempt > 1:
            attempt_prompt = (
                prompt
                + "\n\nPrevious response was not parseable as the required JSON object. "
                + "Return the strict JSON object only, with no Markdown fences and no prose."
            )
        rc, stdout, _ = _invoke_claude(
            claude_exe, attempt_prompt, timeout_s, model, fallback_model
        )
        last_rc = rc
        text = _extract_text_from_claude_json(stdout)
        last_text = text or stdout
        if not text:
            time.sleep(min(5, 1 + attempt))
            continue
        js = _strip_to_json(text)
        if not js:
            time.sleep(1.0)
            continue
        try:
            parsed = json.loads(js)
        except Exception:
            time.sleep(1.0)
            continue
        if isinstance(parsed, dict):
            return parsed, text, rc
    return None, last_text, last_rc


PAIRWISE_PROMPT = """You are comparing two analyses (A and B) of the SAME dataset
answering the SAME goal. Decide which is BETTER and score each side along
5 fixed dimensions.

Dimensions (score each from 1 to 5; 1=poor, 5=excellent):
  - specificity   : concrete entities, magnitudes, time windows, dataset rows
  - evidence      : claims tied to numbers / tables / column references
  - depth         : segmentation, comparison across groups, causal reasoning
                    (NOT just description)
  - actionability : conclusions are specific to this dataset and decision-ready
  - coherence     : internal consistency, no contradictions

Avoid superficial criteria like "longer is better" or "more sections is
better". Score A and B independently on each dimension before deciding
the overall winner. Do not use external ground truth.

Augmented-column citation is NOT a sixth quality dimension. It is an audit
field: cite a listed augmented column only when the report explicitly names
that column or a directly equivalent derived field.

Evidence references must be short quotes or table/column references visible
inside the reports. Prefer numeric evidence. If a side has no usable evidence
for a dimension, return an empty list for that side.

== ANALYTICAL GOAL ==
{goal}

== AUGMENTED COLUMNS FOR A ==
{aug_cols_a}

== AUGMENTED COLUMNS FOR B ==
{aug_cols_b}

== ANALYSIS A ==
{report_a}

== ANALYSIS B ==
{report_b}
== END ==

Return STRICT JSON ONLY:

{{
  "scores_a": {{"specificity": 1-5, "evidence": 1-5, "depth": 1-5,
                "actionability": 1-5, "coherence": 1-5}},
  "scores_b": {{"specificity": 1-5, "evidence": 1-5, "depth": 1-5,
                "actionability": 1-5, "coherence": 1-5}},
  "winner": "A" | "B" | "TIE",
  "margin": "small" | "medium" | "large",
  "confidence": <number 0.0-1.0>,
  "evidence_refs": {{
    "A": [{{"dimension": "specificity|evidence|depth|actionability|coherence", "quote": "short quote", "why": "short reason"}}],
    "B": [{{"dimension": "specificity|evidence|depth|actionability|coherence", "quote": "short quote", "why": "short reason"}}]
  }},
  "augmented_column_refs": {{
    "A": [{{"column": "column name", "quote": "short quote", "dependent": true | false}}],
    "B": [{{"column": "column name", "quote": "short quote", "dependent": true | false}}]
  }},
  "reason": "one short sentence"
}}

Use TIE only when the two are genuinely indistinguishable in quality.
The winner / margin should be consistent with the dimension scores but
you may weight dimensions by your own judgment.
Output ONLY the JSON.
"""


def _format_aug_cols(cols: Sequence[str]) -> str:
    cleaned = [str(c).strip() for c in cols if str(c).strip()]
    return ", ".join(cleaned) if cleaned else "(none)"


def build_pairwise_prompt(
    goal: str,
    report_a: str,
    report_b: str,
    aug_cols_a: Sequence[str] = (),
    aug_cols_b: Sequence[str] = (),
    max_chars: int = 9000,
) -> str:
    a = strip_yaml_header(report_a).strip()
    b = strip_yaml_header(report_b).strip()
    if len(a) > max_chars:
        a = a[:max_chars] + "\n\n...[truncated]..."
    if len(b) > max_chars:
        b = b[:max_chars] + "\n\n...[truncated]..."
    return PAIRWISE_PROMPT.format(
        goal=goal or "(no goal)",
        report_a=a,
        report_b=b,
        aug_cols_a=_format_aug_cols(aug_cols_a),
        aug_cols_b=_format_aug_cols(aug_cols_b),
    )


def _coerce_dim_scores(raw: Any) -> Optional[Dict[str, int]]:
    if not isinstance(raw, dict):
        return None
    out: Dict[str, int] = {}
    for dim in PK_DIMENSIONS:
        value = raw.get(dim)
        if value is None:
            continue
        try:
            score = int(round(float(value)))
        except (TypeError, ValueError):
            continue
        out[dim] = max(1, min(5, score))
    return out or None


def _coerce_confidence(value: Any) -> Optional[float]:
    try:
        conf = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(conf):
        return None
    return max(0.0, min(1.0, conf))


def _coerce_text(value: Any, max_len: int = 280) -> str:
    text = str(value or "").strip()
    if len(text) > max_len:
        text = text[: max_len - 3].rstrip() + "..."
    return text


def _coerce_evidence_refs(raw: Any) -> Dict[str, List[Dict[str, str]]]:
    out: Dict[str, List[Dict[str, str]]] = {"A": [], "B": []}
    if not isinstance(raw, dict):
        return out
    for side in ("A", "B"):
        items = raw.get(side) or raw.get(side.lower()) or []
        if not isinstance(items, list):
            continue
        for item in items[:12]:
            if not isinstance(item, dict):
                continue
            dim = str(item.get("dimension", "")).strip().lower()
            if dim not in PK_DIMENSIONS:
                continue
            quote = _coerce_text(item.get("quote"))
            why = _coerce_text(item.get("why"))
            if quote or why:
                out[side].append({"dimension": dim, "quote": quote, "why": why})
    return out


def _coerce_aug_refs(raw: Any) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {"A": [], "B": []}
    if not isinstance(raw, dict):
        return out
    for side in ("A", "B"):
        items = raw.get(side) or raw.get(side.lower()) or []
        if not isinstance(items, list):
            continue
        for item in items[:12]:
            if not isinstance(item, dict):
                continue
            column = _coerce_text(item.get("column"), max_len=120)
            quote = _coerce_text(item.get("quote"))
            if not column and not quote:
                continue
            out[side].append(
                {
                    "column": column,
                    "quote": quote,
                    "dependent": bool(item.get("dependent")),
                }
            )
    return out


def dimension_decisions(
    scores_a: Optional[Dict[str, int]],
    scores_b: Optional[Dict[str, int]],
) -> Dict[str, Dict[str, Any]]:
    decisions: Dict[str, Dict[str, Any]] = {}
    if not scores_a or not scores_b:
        return decisions
    for dim in PK_DIMENSIONS:
        if dim not in scores_a or dim not in scores_b:
            continue
        delta = scores_a[dim] - scores_b[dim]
        if delta > 0:
            winner = "A"
        elif delta < 0:
            winner = "B"
        else:
            winner = "TIE"
        abs_delta = abs(delta)
        if abs_delta == 0:
            margin = "tie"
        elif abs_delta == 1:
            margin = "small"
        elif abs_delta == 2:
            margin = "medium"
        else:
            margin = "large"
        decisions[dim] = {
            "score_a": scores_a[dim],
            "score_b": scores_b[dim],
            "delta_a_minus_b": delta,
            "winner": winner,
            "margin": margin,
        }
    return decisions


def _validation_warnings(
    winner: str,
    scores_a: Optional[Dict[str, int]],
    scores_b: Optional[Dict[str, int]],
    evidence_refs: Dict[str, List[Dict[str, str]]],
) -> List[str]:
    warnings: List[str] = []
    if not scores_a or not scores_b:
        warnings.append("missing_dimension_scores")
    else:
        score_delta = sum(scores_a[d] - scores_b[d] for d in PK_DIMENSIONS)
        if winner == "A" and score_delta < 0:
            warnings.append("winner_conflicts_with_dimension_sum")
        elif winner == "B" and score_delta > 0:
            warnings.append("winner_conflicts_with_dimension_sum")
    if not evidence_refs.get("A") and not evidence_refs.get("B"):
        warnings.append("missing_evidence_refs")
    return warnings


def judge_pairwise(
    claude_exe: str,
    goal: str,
    report_a_md: str,
    report_b_md: str,
    *,
    aug_cols_a: Sequence[str] = (),
    aug_cols_b: Sequence[str] = (),
    timeout_s: int = 240,
    model: Optional[str] = None,
    fallback_model: Optional[str] = "sonnet",
    max_attempts: int = 3,
) -> Dict[str, Any]:
    prompt = build_pairwise_prompt(goal, report_a_md, report_b_md, aug_cols_a, aug_cols_b)
    parsed, raw_text, rc = _call_claude_json(
        claude_exe, prompt, timeout_s, model, fallback_model, max_attempts
    )
    if parsed is None:
        warnings = ["parse_failed"]
        if rc == 124:
            warnings.append("timeout")
        return {
            "ok": False,
            "rc": rc,
            "raw_text_head": raw_text[:400],
            "validation_warnings": warnings,
        }

    winner = str(parsed.get("winner", "")).strip().upper()
    if winner not in ("A", "B", "TIE"):
        winner = "TIE"
    margin = str(parsed.get("margin", "")).strip().lower()
    if margin not in ("small", "medium", "large"):
        margin = "small"
    scores_a = _coerce_dim_scores(parsed.get("scores_a"))
    scores_b = _coerce_dim_scores(parsed.get("scores_b"))
    evidence_refs = _coerce_evidence_refs(parsed.get("evidence_refs"))
    aug_refs = _coerce_aug_refs(parsed.get("augmented_column_refs"))

    return {
        "ok": True,
        "rc": rc,
        "winner": winner,
        "margin": margin,
        "confidence": _coerce_confidence(parsed.get("confidence")),
        "reason": parsed.get("reason"),
        "scores_a": scores_a,
        "scores_b": scores_b,
        "dimension_decisions": dimension_decisions(scores_a, scores_b),
        "evidence_refs": evidence_refs,
        "augmented_column_refs": aug_refs,
        "validation_warnings": _validation_warnings(winner, scores_a, scores_b, evidence_refs),
    }


@dataclass
class PKOutcome:
    var_a: str
    var_b: str
    raw_winner: str
    margin: str
    ok: bool = True
    swap: bool = False
    scores_a: Optional[Dict[str, int]] = None
    scores_b: Optional[Dict[str, int]] = None
    dimension_decisions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    evidence_refs: Dict[str, List[Dict[str, str]]] = field(
        default_factory=lambda: {"A": [], "B": []}
    )
    augmented_column_refs: Dict[str, List[Dict[str, Any]]] = field(
        default_factory=lambda: {"A": [], "B": []}
    )
    confidence: Optional[float] = None
    reason: Optional[str] = None
    validation_warnings: List[str] = field(default_factory=list)

    def winner_var(self) -> Optional[str]:
        if self.raw_winner == "A":
            return self.var_a
        if self.raw_winner == "B":
            return self.var_b
        return None

    def scores_for(self, variant: str) -> Optional[Dict[str, int]]:
        if variant == self.var_a:
            return self.scores_a
        if variant == self.var_b:
            return self.scores_b
        return None

    def side_for(self, variant: str) -> Optional[str]:
        if variant == self.var_a:
            return "A"
        if variant == self.var_b:
            return "B"
        return None

    def to_dict(self, drop_empty: bool = True) -> Dict[str, Any]:
        record: Dict[str, Any] = {
            "var_a": self.var_a,
            "var_b": self.var_b,
            "swap": self.swap,
            "winner": self.raw_winner,
            "margin": self.margin,
            "ok": self.ok,
        }
        optional = {
            "confidence": self.confidence,
            "scores_a": self.scores_a,
            "scores_b": self.scores_b,
            "dimension_decisions": self.dimension_decisions,
            "evidence_refs": self.evidence_refs,
            "augmented_column_refs": self.augmented_column_refs,
            "reason": self.reason,
            "validation_warnings": self.validation_warnings,
        }
        for key, value in optional.items():
            if drop_empty and value in (None, {}, [], {"A": [], "B": []}):
                continue
            record[key] = value
        return record

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PKOutcome":
        scores_a = _coerce_dim_scores(data.get("scores_a"))
        scores_b = _coerce_dim_scores(data.get("scores_b"))
        decisions = data.get("dimension_decisions")
        if not isinstance(decisions, dict):
            decisions = dimension_decisions(scores_a, scores_b)
        return cls(
            var_a=str(data.get("var_a", "A")),
            var_b=str(data.get("var_b", "B")),
            swap=bool(data.get("swap", False)),
            raw_winner=str(data.get("winner", "TIE")).upper(),
            margin=str(data.get("margin", "small")).lower(),
            ok=bool(data.get("ok", True)),
            scores_a=scores_a,
            scores_b=scores_b,
            dimension_decisions=decisions,
            evidence_refs=_coerce_evidence_refs(data.get("evidence_refs")),
            augmented_column_refs=_coerce_aug_refs(data.get("augmented_column_refs")),
            confidence=_coerce_confidence(data.get("confidence")),
            reason=data.get("reason"),
            validation_warnings=list(data.get("validation_warnings") or []),
        )


def bradley_terry_mm(
    outcomes: Iterable[PKOutcome],
    items: Optional[Sequence[str]] = None,
    iters: int = 500,
    eps: float = 1e-9,
    use_margin_weight: bool = False,
) -> Dict[str, float]:
    outcomes = list(outcomes)
    seen = sorted({v for o in outcomes for v in (o.var_a, o.var_b)} | set(items or ()))
    if not seen:
        return {}

    wins: Dict[str, float] = defaultdict(float)
    games: Dict[Tuple[str, str], float] = defaultdict(float)

    for outcome in outcomes:
        if not outcome.ok:
            continue
        weight = MARGIN_TO_WEIGHT.get(outcome.margin, 1.0) if use_margin_weight else 1.0
        winner = outcome.winner_var()
        if winner is None:
            # Lab8 BT policy: ties count as 0.5 wins for each side, not as dropped games.
            wins[outcome.var_a] += 0.5 * weight
            wins[outcome.var_b] += 0.5 * weight
        else:
            loser = outcome.var_b if winner == outcome.var_a else outcome.var_a
            wins[winner] += 1.0 * weight
            wins[loser] += 0.0
        games[(outcome.var_a, outcome.var_b)] += weight
        games[(outcome.var_b, outcome.var_a)] += weight

    for i in seen:
        for j in seen:
            if i != j:
                games[(i, j)] += eps
                wins[i] += eps / 2
                wins[j] += eps / 2

    strengths = {x: 1.0 for x in seen}
    for _ in range(iters):
        new_strengths: Dict[str, float] = {}
        for i in seen:
            denom = 0.0
            for j in seen:
                if i == j:
                    continue
                nij = games[(i, j)]
                if nij == 0:
                    continue
                denom += nij / (strengths[i] + strengths[j])
            new_strengths[i] = max(eps, wins[i] / denom) if denom > 0 else strengths[i]
        log_vals = [math.log(v) for v in new_strengths.values()]
        gm_log = sum(log_vals) / len(log_vals)
        for key in new_strengths:
            new_strengths[key] = math.exp(math.log(new_strengths[key]) - gm_log)
        diff = max(abs(new_strengths[k] - strengths[k]) for k in seen)
        strengths = new_strengths
        if diff < 1e-7:
            break
    return {key: math.log(value) for key, value in strengths.items()}


def load_pairwise(path: Path) -> List[PKOutcome]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("outcomes") or []
    if not isinstance(data, list):
        raise ValueError(f"pairwise file must contain a list or an outcomes object: {path}")
    return [PKOutcome.from_dict(item) for item in data if isinstance(item, dict)]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def aggregate_dimension_scores(
    outcomes: Sequence[PKOutcome], items: Optional[Sequence[str]] = None
) -> Dict[str, Any]:
    variants = sorted({v for o in outcomes for v in (o.var_a, o.var_b)} | set(items or ()))
    score_values: Dict[str, Dict[str, List[int]]] = {
        v: {dim: [] for dim in PK_DIMENSIONS} for v in variants
    }
    dim_record = {
        v: {
            dim: {"wins": 0, "losses": 0, "ties": 0, "large_wins": 0, "large_losses": 0}
            for dim in PK_DIMENSIONS
        }
        for v in variants
    }
    citation_record = {
        v: {
            "appearances_count": 0,
            "evidence_ref_count": 0,
            "aug_column_ref_count": 0,
            "aug_dependent_ref_count": 0,
        }
        for v in variants
    }

    for outcome in outcomes:
        for variant in (outcome.var_a, outcome.var_b):
            citation_record[variant]["appearances_count"] += 1
            scores = outcome.scores_for(variant)
            if scores:
                for dim, score in scores.items():
                    if dim in PK_DIMENSIONS:
                        score_values[variant][dim].append(score)

            side = outcome.side_for(variant)
            if side:
                citation_record[variant]["evidence_ref_count"] += len(
                    outcome.evidence_refs.get(side, [])
                )
                aug_refs = outcome.augmented_column_refs.get(side, [])
                citation_record[variant]["aug_column_ref_count"] += len(aug_refs)
                citation_record[variant]["aug_dependent_ref_count"] += sum(
                    1 for ref in aug_refs if ref.get("dependent")
                )

        for dim, decision in outcome.dimension_decisions.items():
            winner = decision.get("winner")
            margin = decision.get("margin")
            if winner == "TIE":
                dim_record[outcome.var_a][dim]["ties"] += 1
                dim_record[outcome.var_b][dim]["ties"] += 1
            elif winner == "A":
                dim_record[outcome.var_a][dim]["wins"] += 1
                dim_record[outcome.var_b][dim]["losses"] += 1
                if margin == "large":
                    dim_record[outcome.var_a][dim]["large_wins"] += 1
                    dim_record[outcome.var_b][dim]["large_losses"] += 1
            elif winner == "B":
                dim_record[outcome.var_b][dim]["wins"] += 1
                dim_record[outcome.var_a][dim]["losses"] += 1
                if margin == "large":
                    dim_record[outcome.var_b][dim]["large_wins"] += 1
                    dim_record[outcome.var_a][dim]["large_losses"] += 1

    mean_scores: Dict[str, Dict[str, Optional[float]]] = {}
    for variant, dim_values in score_values.items():
        mean_scores[variant] = {}
        for dim, values in dim_values.items():
            mean_scores[variant][dim] = statistics.mean(values) if values else None

    for variant, citation_counts in citation_record.items():
        appearances = citation_counts["appearances_count"]
        if appearances <= 0:
            citation_counts.update(
                {
                    "evidence_ref_rate": None,
                    "aug_col_citation_rate": None,
                    "aug_dependent_ref_rate": None,
                }
            )
            continue
        citation_counts.update(
            {
                "evidence_ref_rate": citation_counts["evidence_ref_count"] / appearances,
                "aug_col_citation_rate": citation_counts["aug_column_ref_count"] / appearances,
                "aug_dependent_ref_rate": citation_counts["aug_dependent_ref_count"] / appearances,
            }
        )

    return {
        "mean_dimension_scores": mean_scores,
        "dimension_win_loss": dim_record,
        "citation_counts": citation_record,
    }


def _rank_order(scores: Dict[str, float], items: Sequence[str]) -> List[str]:
    return sorted(items, key=lambda item: (-scores.get(item, 0.0), item))


def _average_ranks(scores: Dict[str, float], items: Sequence[str]) -> Dict[str, float]:
    ordered = sorted(items, key=lambda item: (-scores.get(item, 0.0), item))
    ranks: Dict[str, float] = {}
    position = 0
    while position < len(ordered):
        score = scores.get(ordered[position], 0.0)
        end = position + 1
        while end < len(ordered) and scores.get(ordered[end], 0.0) == score:
            end += 1
        average_rank = (position + 1 + end) / 2.0
        for item in ordered[position:end]:
            ranks[item] = average_rank
        position = end
    return ranks


def _spearman_score_maps(
    primary_scores: Dict[str, float],
    secondary_scores: Dict[str, float],
    items: Sequence[str],
) -> Optional[float]:
    common_items = [item for item in items if item in primary_scores and item in secondary_scores]
    if len(common_items) < 2:
        return None
    primary_ranks = _average_ranks(primary_scores, common_items)
    secondary_ranks = _average_ranks(secondary_scores, common_items)
    primary_values = [primary_ranks[item] for item in common_items]
    secondary_values = [secondary_ranks[item] for item in common_items]
    primary_mean = statistics.mean(primary_values)
    secondary_mean = statistics.mean(secondary_values)
    numerator = sum(
        (primary_value - primary_mean) * (secondary_value - secondary_mean)
        for primary_value, secondary_value in zip(primary_values, secondary_values)
    )
    primary_denominator = math.sqrt(sum((value - primary_mean) ** 2 for value in primary_values))
    secondary_denominator = math.sqrt(sum((value - secondary_mean) ** 2 for value in secondary_values))
    if primary_denominator == 0 or secondary_denominator == 0:
        return None
    return numerator / (primary_denominator * secondary_denominator)


def _margin_floor(margins: Sequence[str]) -> str:
    if not margins:
        return "small"
    order = {"small": 0, "medium": 1, "large": 2}
    normalised = [str(margin).lower() for margin in margins if str(margin).lower() in order]
    if not normalised:
        return "small"
    return min(normalised, key=lambda margin: order[margin])


def _mean_confidence(outcomes: Sequence[PKOutcome]) -> Optional[float]:
    values = [outcome.confidence for outcome in outcomes if outcome.confidence is not None]
    return round(statistics.mean(values), 4) if values else None


def _mean_scores_for_variant(outcomes: Sequence[PKOutcome], variant: str) -> Optional[Dict[str, int]]:
    values: Dict[str, List[int]] = {dim: [] for dim in PK_DIMENSIONS}
    for outcome in outcomes:
        scores = outcome.scores_for(variant)
        if not scores:
            continue
        for dim in PK_DIMENSIONS:
            score = scores.get(dim)
            if isinstance(score, (int, float)):
                values[dim].append(int(score))
    if not all(values[dim] for dim in PK_DIMENSIONS):
        return None
    return {dim: int(round(statistics.mean(values[dim]))) for dim in PK_DIMENSIONS}


def stabilize_swap_outcomes(
    outcomes: Sequence[PKOutcome],
    items: Optional[Sequence[str]] = None,
) -> Tuple[List[PKOutcome], Dict[str, Any]]:
    groups: Dict[Tuple[str, str], List[PKOutcome]] = defaultdict(list)
    for outcome in outcomes:
        pair = tuple(sorted((outcome.var_a, outcome.var_b)))
        if len(pair) == 2 and pair[0] != pair[1]:
            groups[pair].append(outcome)

    expected_pairs = set()
    item_list = list(items or [])
    for idx, left in enumerate(item_list):
        for right in item_list[idx + 1 :]:
            expected_pairs.add(tuple(sorted((left, right))))
    for pair in expected_pairs:
        groups.setdefault(pair, [])

    stable: List[PKOutcome] = []
    details: List[Dict[str, Any]] = []
    comparable = 0
    consistent = 0
    disagreements = 0
    single_order = 0
    invalid = 0

    for pair in sorted(groups):
        grouped = groups[pair]
        ok_group = [outcome for outcome in grouped if outcome.ok]
        ordered_winners = [outcome.winner_var() or "TIE" for outcome in ok_group]
        stable_winner: Optional[str]
        warnings: List[str] = []

        if not ok_group:
            stable_winner = None
            invalid += 1
            warnings.append("no_valid_ordered_judgment")
        elif len(ok_group) == 1:
            stable_winner = ok_group[0].winner_var()
            single_order += 1
            warnings.append("single_order_only")
        else:
            comparable += 1
            unique_winners = set(ordered_winners)
            if len(unique_winners) == 1:
                stable_winner = ok_group[0].winner_var()
                consistent += 1
            else:
                stable_winner = None
                disagreements += 1
                warnings.append("swap_disagreement_collapsed_to_tie")

        raw_winner = "TIE"
        if stable_winner == pair[0]:
            raw_winner = "A"
        elif stable_winner == pair[1]:
            raw_winner = "B"

        scores_a = _mean_scores_for_variant(ok_group, pair[0]) if ok_group else None
        scores_b = _mean_scores_for_variant(ok_group, pair[1]) if ok_group else None
        margin = _margin_floor([outcome.margin for outcome in ok_group if outcome.winner_var() == stable_winner]) if stable_winner else "small"
        reason = (
            f"swap-stabilized from {len(ok_group)} valid ordered judgments; "
            f"ordered_winners={ordered_winners}; stable_winner={stable_winner or 'TIE'}"
        )
        stable_outcome = PKOutcome(
            var_a=pair[0],
            var_b=pair[1],
            raw_winner=raw_winner,
            margin=margin,
            ok=bool(ok_group),
            swap=False,
            scores_a=scores_a,
            scores_b=scores_b,
            dimension_decisions=dimension_decisions(scores_a, scores_b),
            confidence=_mean_confidence(ok_group),
            reason=reason,
            validation_warnings=warnings,
        )
        stable.append(stable_outcome)
        details.append(
            {
                "pair": list(pair),
                "ordered_judgments": len(grouped),
                "valid_ordered_judgments": len(ok_group),
                "ordered_winners": ordered_winners,
                "stable_winner": stable_winner or "TIE",
                "policy": "unanimous ordered winners keep winner; disagreement collapses to TIE",
                "warnings": warnings,
            }
        )

    return stable, {
        "n_pairs": len(stable),
        "n_raw_outcomes": len(outcomes),
        "comparable_pairs": comparable,
        "consistent_pairs": consistent,
        "swap_disagreement_pairs": disagreements,
        "single_order_pairs": single_order,
        "invalid_pairs": invalid,
        "swap_consistency_rate": (consistent / comparable) if comparable else None,
        "details": details,
    }


def compute_bt_payload(
    dataset: str,
    outcomes: Sequence[PKOutcome],
    items: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    items = list(items or sorted({v for o in outcomes for v in (o.var_a, o.var_b)}))
    stabilized_outcomes, stability = stabilize_swap_outcomes(outcomes, items=items)
    primary_outcomes = stabilized_outcomes or list(outcomes)
    bt = bradley_terry_mm(primary_outcomes, items=items)
    margin_bt = bradley_terry_mm(primary_outcomes, items=items, use_margin_weight=True)
    raw_bt = bradley_terry_mm(outcomes, items=items)
    raw_margin_bt = bradley_terry_mm(outcomes, items=items, use_margin_weight=True)
    primary_rank = _rank_order(bt, items)
    secondary_rank = _rank_order(margin_bt, items)
    spearman = _spearman_score_maps(bt, margin_bt, items)
    return {
        "dataset": dataset,
        "n_outcomes": len(primary_outcomes),
        "n_ok": sum(1 for outcome in primary_outcomes if outcome.ok),
        "n_raw_outcomes": len(outcomes),
        "n_raw_ok": sum(1 for outcome in outcomes if outcome.ok),
        "aggregation_policy": "swap_stabilized_unanimous_else_tie",
        "pairwise_stability": stability,
        "bt_score": bt,
        "bt_score_margin_weighted_secondary": margin_bt,
        "bt_score_raw_ordered": raw_bt,
        "bt_score_raw_ordered_margin_weighted": raw_margin_bt,
        "bt_secondary_consistency": {
            "spearman_rank_correlation": round(spearman, 6) if spearman is not None else None,
            "same_rank_order": primary_rank == secondary_rank,
            "primary_rank": primary_rank,
            "secondary_rank": secondary_rank,
        },
        "dimension_summary": aggregate_dimension_scores(primary_outcomes, items=items),
        "dimension_summary_raw_ordered": aggregate_dimension_scores(outcomes, items=items),
        "stabilized_outcomes": [outcome.to_dict() for outcome in primary_outcomes],
        "outcomes": [outcome.to_dict() for outcome in outcomes],
        "computed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "metric_notes": {
            "primary": "bt_score is computed after swap-stabilizing each unordered pair: unanimous A/B and B/A judgments keep the winner; disagreements collapse to TIE; TIE counts as 0.5 wins for each side.",
            "secondary": "bt_score_margin_weighted_secondary uses small/medium/large as 1.0/1.5/2.0 and is diagnostic only.",
            "raw_ordered": "bt_score_raw_ordered preserves the old 12 ordered judgments and is diagnostic only.",
        },
    }


def audit_pairwise_fields(outcomes: Sequence[PKOutcome]) -> Dict[str, Any]:
    total = len(outcomes)
    ok_total = sum(1 for outcome in outcomes if outcome.ok)
    n_ties = sum(1 for outcome in outcomes if outcome.ok and outcome.raw_winner == "TIE")
    warnings_breakdown: Dict[str, int] = defaultdict(int)
    for outcome in outcomes:
        for warning in outcome.validation_warnings:
            warnings_breakdown[str(warning)] += 1
    with_scores = sum(1 for outcome in outcomes if outcome.scores_a and outcome.scores_b)
    with_decisions = sum(1 for outcome in outcomes if outcome.dimension_decisions)
    with_evidence = sum(
        1 for outcome in outcomes if outcome.evidence_refs.get("A") or outcome.evidence_refs.get("B")
    )
    with_aug_refs = sum(
        1
        for outcome in outcomes
        if outcome.augmented_column_refs.get("A") or outcome.augmented_column_refs.get("B")
    )
    return {
        "n_outcomes": total,
        "n_ok": ok_total,
        "n_ties": n_ties,
        "tie_rate": (n_ties / ok_total) if ok_total else None,
        "tie_policy": "TIE outcomes count as 0.5 wins for each side in BT.",
        "with_dimension_scores": with_scores,
        "with_dimension_decisions": with_decisions,
        "with_evidence_refs": with_evidence,
        "with_augmented_column_refs": with_aug_refs,
        "warnings_breakdown": dict(sorted(warnings_breakdown.items())),
        "missing": {
            "dimension_scores": total - with_scores,
            "dimension_decisions": total - with_decisions,
            "evidence_refs": total - with_evidence,
            "augmented_column_refs": total - with_aug_refs,
        },
    }


def _parse_aug_cols(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    path = Path(raw)
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = raw
    return [part.strip() for part in re.split(r"[,\n]", text) if part.strip()]


def cmd_judge_pair(args: argparse.Namespace) -> int:
    claude_exe = find_claude()
    report_a = Path(args.report_a).read_text(encoding="utf-8", errors="replace")
    report_b = Path(args.report_b).read_text(encoding="utf-8", errors="replace")
    result = judge_pairwise(
        claude_exe,
        args.goal,
        report_a,
        report_b,
        aug_cols_a=_parse_aug_cols(args.aug_cols_a),
        aug_cols_b=_parse_aug_cols(args.aug_cols_b),
        timeout_s=args.timeout,
        model=args.model,
        fallback_model=args.fallback_model,
        max_attempts=args.attempts,
    )
    outcome = PKOutcome(
        var_a=args.var_a,
        var_b=args.var_b,
        swap=args.swap,
        raw_winner=result.get("winner", "TIE"),
        margin=result.get("margin", "small"),
        ok=bool(result.get("ok")),
        scores_a=result.get("scores_a"),
        scores_b=result.get("scores_b"),
        dimension_decisions=result.get("dimension_decisions") or {},
        evidence_refs=result.get("evidence_refs") or {"A": [], "B": []},
        augmented_column_refs=result.get("augmented_column_refs") or {"A": [], "B": []},
        confidence=result.get("confidence"),
        reason=result.get("reason"),
        validation_warnings=result.get("validation_warnings") or [],
    )
    payload = outcome.to_dict(drop_empty=False)
    if "rc" in result:
        payload["judge_rc"] = result.get("rc")
    if "raw_text_head" in result:
        payload["raw_text_head"] = result.get("raw_text_head")
    if args.output:
        write_json(Path(args.output), payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if outcome.ok else 1


def cmd_bt(args: argparse.Namespace) -> int:
    outcomes: List[PKOutcome] = []
    for path_text in args.pairwise:
        outcomes.extend(load_pairwise(Path(path_text)))
    items = args.items or sorted({v for outcome in outcomes for v in (outcome.var_a, outcome.var_b)})
    payload = compute_bt_payload(args.dataset, outcomes, items=items)
    if args.output:
        write_json(Path(args.output), payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    outcomes: List[PKOutcome] = []
    for path_text in args.pairwise:
        outcomes.extend(load_pairwise(Path(path_text)))
    payload = audit_pairwise_fields(outcomes)
    if args.output:
        write_json(Path(args.output), payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_judge = sub.add_parser("judge-pair", help="run one pairwise grading call")
    p_judge.add_argument("--goal", required=True)
    p_judge.add_argument("--report-a", required=True)
    p_judge.add_argument("--report-b", required=True)
    p_judge.add_argument("--var-a", default="A")
    p_judge.add_argument("--var-b", default="B")
    p_judge.add_argument("--swap", action="store_true")
    p_judge.add_argument("--aug-cols-a", default=None, help="comma/newline list or path")
    p_judge.add_argument("--aug-cols-b", default=None, help="comma/newline list or path")
    p_judge.add_argument("--timeout", type=int, default=240)
    p_judge.add_argument("--attempts", type=int, default=3)
    p_judge.add_argument("--model", default=None)
    p_judge.add_argument("--fallback-model", default="sonnet")
    p_judge.add_argument("--output", default=None)
    p_judge.set_defaults(func=cmd_judge_pair)

    p_bt = sub.add_parser("bt", help="compute BT + dimension summary from pairwise JSON")
    p_bt.add_argument("--pairwise", nargs="+", required=True)
    p_bt.add_argument("--dataset", default="lab8")
    p_bt.add_argument("--items", nargs="*", default=None)
    p_bt.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR / "bt_v3.json"))
    p_bt.set_defaults(func=cmd_bt)

    p_audit = sub.add_parser("audit", help="audit whether pairwise records have v3 fields")
    p_audit.add_argument("--pairwise", nargs="+", required=True)
    p_audit.add_argument("--output", default=None)
    p_audit.set_defaults(func=cmd_audit)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())