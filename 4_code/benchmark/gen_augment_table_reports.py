"""Generate analysis reports for ``augment_table`` tables into ``analysis_report``.

Scope (per user request):
  * ``<ds>/<scen>/haiku__skill_on-v11.csv``   -> ``haiku__skill_on-v11.md``
  * ``<ds>/<scen>/sonnet__skill_on-v11.csv``  -> ``sonnet__skill_on-v11.md``
  * ``<ds>/<scen>/original.csv``              -> ``haiku__original.md`` and
    ``sonnet__original.md``, but ONLY for scenarios that have no original report
    yet (the 45 supplement scenarios).

Output layout mirrors ``augment_table``::

    analysis_report/<dataset>/<scenario>/<report>.md

The prompt is a faithful replica of the one used for the original 63 scenarios
(recovered from ``analyses/<variant>/_sent_prompt_analyze_<variant>.txt``) so the
new reports stay comparable with the existing corpus. ``skill_on_e2e`` tables use
the lab6 TAPP-aware e2e prompt (which names the augmented columns and imposes the
extra reporting requirements); every other variant uses the neutral prompt. Pass
``--neutral-e2e`` to fall back to the neutral prompt for e2e as well.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
AUGMENT_TABLE = ROOT / "augment_table"
OUT_ROOT = ROOT / "analysis_report"
GT_ROOTS = (ROOT / "gt_annotations", ROOT / "gt_annotations_supplement")

MODEL_BY_PREFIX = {
    "haiku": "substrate-claude-haiku-4-5",
    "sonnet": "substrate-claude-sonnet-4-6",
}

# table kind -> variant label used in the prompt (kept identical to the labels
# used for the original 63 scenarios so old and new reports stay comparable)
VARIANT_BY_KIND = {
    "skill_off": "skill_off",
    # agentic skill-off (2026-07-28): table + query + tools, no runner-provided
    # pipeline. Analysed under the same neutral "skill_off" prompt label as the
    # other skill-off variants so the reports stay comparable.
    "skill_off_update": "skill_off",
    "skill_on": "skill_on",
    "skill_on-v11": "skill_on",
    "skill_on_e2e": "skill_on_e2e",
    "skill_on_e2e-v11": "skill_on_e2e",
    "original": "original",
}

BEGIN = "REPORT_MD_BEGIN"
END = "REPORT_MD_END"

PROMPT_TEMPLATE = """Analyze this table and answer the query. The runner will save your report to:
{dest}

Do not write files and do not claim that you saved a report. Your job is to return the full Markdown report in this response.

Dataset:
{table}

Query from {query_source}:
{query}

Variant label: {variant}

Report requirements:
- Ground claims in visible columns and concrete patterns from the data.
- Discuss factors relevant to the query and the dataset's focus variable.
- Mention important exceptions or weak evidence instead of overclaiming.
- Keep the report concise but decision-ready.
- Return the complete Markdown report between the exact marker lines below. Do not omit either marker.

{begin}
<complete Markdown report>
{end}

When finished, print exactly one final line:
ANALYSIS_OK <absolute path to the report>

If you cannot complete the analysis, print exactly one final line:
ANALYSIS_FAIL <short reason>
"""

# skill_on_e2e uses the TAPP-aware prompt instead of the neutral one, replicating
# the lab6 e2e prompt (recovered from
# ``analyses/skill_on_e2e/_sent_prompt_analyze_skill_on_e2e.txt``) so the e2e arm
# stays a genuinely different condition from skill_on rather than a second
# independent sample of it. Only the skill version and workdir differ.
E2E_PROMPT_TEMPLATE = """Execution framework:
Claude Code CLI (`claude -p`) is the execution framework; model names are passed through `--model` to the Agent Maestro reverse proxy. This is not the Codex CLI framework.

The TA++ v11 augmentation has already been completed by the bounded chunk orchestrator under this workdir:
{workdir}

Analyze the augmented table. The runner will save your report to:
{dest}

Do not write the report file yourself and do not claim that you saved a report. Your job is to return the full Markdown report in this response.

Augmented dataset:
{table}

Query from {query_source}:
{query}

Executor model for analysis:
{model}

TAPP-generated columns available in the augmented table:
{aug_columns}

Requirements:
- Analyze the complete augmented table: the original table plus TAPP-generated columns. The original structured columns remain first-class evidence.
- Answer the paper query using the whole table. Start from the outcome/focus variable and original structured drivers, then use TAPP-generated columns only where they add missing semantic signal or clarify a relationship.
- Include a short method note listing the exact TAPP-generated column names used in the report.
- Cite those exact augmented column names in the substantive analysis. Never cite or invent augmented columns that are absent from the augmented table.
- Use TAPP-generated columns as additional explanatory variables, not as replacements for raw evidence. If a TAPP facet is weak, redundant with an existing column, low-coverage, or not clearly related to the query, say so and do not center the report on it.
- Combine augmented semantic facets with original structured columns in the same claims and tables where possible.
- Do not write a TAPP-only facet summary. For each major analytical claim, include quantified evidence from the whole table such as counts, rates, means/medians, correlations, stratified tables, or clearly stated sample sizes.
- Cross-check semantic facet effects against relevant original structured fields when available, especially target/outcome columns, numeric measures, dates, groups, categories, users, departments, and other query-relevant columns.
- Keep the report concise but decision-ready.
- Return the complete Markdown report between the exact marker lines below. Do not omit either marker.

{begin}
<complete Markdown report>
{end}

When finished, print exactly one final line:
ANALYSIS_OK <absolute path to the report>

If you cannot complete the analysis, print exactly one final line:
ANALYSIS_FAIL <short reason>
"""


# --------------------------------------------------------------------------- #
# claude CLI
# --------------------------------------------------------------------------- #
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


def _popen_group_kwargs() -> dict[str, Any]:
    if os.name == "nt":
        flag = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        return {"creationflags": flag} if flag else {}
    return {"start_new_session": True}


def _kill_tree(proc: subprocess.Popen) -> None:
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
    proc.kill()


def _invoke_claude(exe: str, prompt: str, model: str, timeout_s: int) -> tuple[int, str]:
    cmd = [
        exe,
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
    env = os.environ.copy()
    env["CLAUDE_CODE_SIMPLE"] = "1"
    # ignore_cleanup_errors: on Windows the CLI may still hold a handle to the
    # sandbox when it exits, and an rmdir failure must not abort the whole run.
    with tempfile.TemporaryDirectory(prefix="analysis_run_", ignore_cleanup_errors=True) as sandbox:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=sandbox,
            env=env,
            **_popen_group_kwargs(),
        )
        try:
            out, _err = proc.communicate(input=prompt.encode("utf-8"), timeout=timeout_s)
            return proc.returncode, (out or b"").decode("utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            _kill_tree(proc)
            return -9, ""


def _extract_result_text(raw: str) -> str:
    if not raw:
        return ""
    try:
        data = json.loads(raw)
    except Exception:
        return raw
    if isinstance(data, dict):
        if data.get("is_error"):
            return ""
        return str(data.get("result") or data.get("response") or "")
    return ""


def _extract_report(text: str) -> str | None:
    if not text:
        return None
    if BEGIN in text and END in text:
        body = text.split(BEGIN, 1)[1].split(END, 1)[0].strip()
        return body or None
    # tolerate a dropped end marker
    if BEGIN in text:
        body = text.split(BEGIN, 1)[1].strip()
        body = re.sub(r"ANALYSIS_(OK|FAIL).*$", "", body, flags=re.S).strip()
        return body or None
    return None


# --------------------------------------------------------------------------- #
# metadata
# --------------------------------------------------------------------------- #
def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _gt_query(dataset: str, scenario: str) -> dict[str, str]:
    for gt_root in GT_ROOTS:
        for name in (dataset, dataset.replace("_", "-")):
            gt_path = gt_root / name / "augmentations" / scenario / "GT.json"
            if gt_path.exists():
                gt = _read_json(gt_path)
                q = gt.get("query") or {}
                return {
                    "text": str(q.get("text") or "").strip(),
                    "subtype": str(q.get("subtype") or ""),
                    "focus_variable": str(q.get("focus_variable") or ""),
                    "source": gt_path.relative_to(ROOT).as_posix(),
                }
    return {"text": "", "subtype": "", "focus_variable": "", "source": ""}


def _header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh):
            return [c.strip() for c in row]
    return []


def _augmented_columns(table: Path) -> list[str]:
    """Columns present in an augmented table but not in the scenario's original."""
    original = table.parent / "original.csv"
    if not original.exists():
        return []
    base = set(_header(original))
    return [c for c in _header(table) if c and c not in base]


def _e2e_workdir(dataset: str, scenario: str, model: str) -> Path | None:
    for portion in ("dataset_portion_1", "dataset_portion_2"):
        wd = ROOT / portion / model / f"{dataset}__{scenario}" / "analyses" / "skill_on_e2e_v11" / "tapp_workdir"
        if wd.is_dir():
            return wd
    return None


def _existing_original_scenarios() -> set[str]:
    """Scenario keys (``dataset__scenario``) that already have an original report."""
    keys: set[str] = set()
    for portion in ("dataset_portion_1", "dataset_portion_2"):
        base = ROOT / portion
        if not base.is_dir():
            continue
        for model_dir in base.iterdir():
            if not model_dir.is_dir():
                continue
            for scen_dir in model_dir.iterdir():
                if (scen_dir / "analyses" / "original" / "analysis.md").exists():
                    keys.add(scen_dir.name)
    return keys


def _front_matter(meta: dict[str, Any]) -> str:
    def esc(v: Any) -> str:
        return str(v).replace('"', '\\"')

    return (
        "---\n"
        f"dataset: {meta['dataset']}\n"
        f"scenario: {meta['scenario']}\n"
        f"variant: {meta['variant']}\n"
        f"model: {meta['model']}\n"
        f"prompt_style: {meta['prompt_style']}\n"
        f"query_subtype: {meta['query_subtype']}\n"
        f"focus_variable: \"{esc(meta['focus_variable'])}\"\n"
        f"query: \"{esc(meta['query'])}\"\n"
        f"source_table: {meta['source_table']}\n"
        f"generated_at: {meta['generated_at']}\n"
        f"wall_seconds: {meta['wall_seconds']}\n"
        "---\n\n"
    )


# --------------------------------------------------------------------------- #
# jobs
# --------------------------------------------------------------------------- #
def build_jobs(args: argparse.Namespace) -> list[dict[str, Any]]:
    have_original = _existing_original_scenarios()
    only_ds = set(args.dataset or [])
    only_scen = set(args.scenario or [])
    kinds = list(args.include)

    jobs: list[dict[str, Any]] = []
    for ds_dir in sorted(p for p in AUGMENT_TABLE.iterdir() if p.is_dir()):
        if only_ds and ds_dir.name not in only_ds:
            continue
        for scen_dir in sorted(p for p in ds_dir.iterdir() if p.is_dir()):
            if only_scen and scen_dir.name not in only_scen:
                continue
            key = f"{ds_dir.name}__{scen_dir.name}"
            targets: list[tuple[Path, str, str, str]] = []  # (table, report_stem, prefix, variant)

            for kind in kinds:
                if kind == "original":
                    table = scen_dir / "original.csv"
                    # the shared original table is analysed once per model, but only
                    # where no original report was produced by the earlier lab6 run
                    if table.exists() and (key not in have_original or args.force_original):
                        for prefix in ("haiku", "sonnet"):
                            targets.append((table, f"{prefix}__original", prefix, "original"))
                    continue
                for prefix in ("haiku", "sonnet"):
                    table = scen_dir / f"{prefix}__{kind}.csv"
                    if table.exists():
                        targets.append((table, f"{prefix}__{kind}", prefix, VARIANT_BY_KIND[kind]))

            for table, stem, prefix, variant in targets:
                dest = OUT_ROOT / ds_dir.name / scen_dir.name / f"{stem}.md"
                if dest.exists() and dest.stat().st_size > 0 and not args.force:
                    continue
                jobs.append(
                    {
                        "dataset": ds_dir.name,
                        "scenario": scen_dir.name,
                        "table": table,
                        "dest": dest,
                        "model": MODEL_BY_PREFIX[prefix],
                        "variant": variant,
                        "stem": stem,
                    }
                )
    if args.limit:
        jobs = jobs[: args.limit]
    return jobs


def run_job(job: dict[str, Any], exe: str, args: argparse.Namespace) -> dict[str, Any]:
    q = _gt_query(job["dataset"], job["scenario"])
    if not q["text"]:
        return {**{k: str(v) for k, v in job.items()}, "status": "no_query"}

    if job["variant"] == "skill_on_e2e" and not args.neutral_e2e:
        aug_cols = _augmented_columns(job["table"])
        workdir = _e2e_workdir(job["dataset"], job["scenario"], job["model"])
        if not aug_cols or workdir is None:
            return {
                "dataset": job["dataset"],
                "scenario": job["scenario"],
                "stem": job["stem"],
                "status": "no_aug_context",
            }
        prompt_style = "e2e"
        prompt = E2E_PROMPT_TEMPLATE.format(
            workdir=workdir.resolve(),
            dest=job["dest"].resolve(),
            table=job["table"].resolve(),
            query_source=q["source"] or "GT.json",
            query=q["text"],
            model=job["model"],
            aug_columns=repr(aug_cols),
            begin=BEGIN,
            end=END,
        )
    else:
        prompt_style = "neutral"
        prompt = PROMPT_TEMPLATE.format(
            dest=job["dest"].resolve(),
            table=job["table"].resolve(),
            query_source=q["source"] or "GT.json",
            query=q["text"],
            variant=job["variant"],
            begin=BEGIN,
            end=END,
        )

    started = time.time()
    body: str | None = None
    rc = -1
    for attempt in range(1, args.attempts + 1):
        rc, raw = _invoke_claude(exe, prompt, job["model"], args.timeout)
        body = _extract_report(_extract_result_text(raw))
        if body and len(body) > 200:
            break
        time.sleep(min(8, 2 * attempt))
        body = None
    wall = round(time.time() - started, 2)

    if not body:
        return {
            "dataset": job["dataset"],
            "scenario": job["scenario"],
            "stem": job["stem"],
            "status": "failed",
            "rc": rc,
        }

    meta = {
        "dataset": job["dataset"],
        "scenario": job["scenario"],
        "variant": job["variant"],
        "model": job["model"],
        "prompt_style": prompt_style,
        "query": q["text"],
        "query_subtype": q["subtype"],
        "focus_variable": q["focus_variable"],
        "source_table": job["table"].relative_to(ROOT).as_posix(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "wall_seconds": wall,
    }
    job["dest"].parent.mkdir(parents=True, exist_ok=True)
    job["dest"].write_text(_front_matter(meta) + body + "\n", encoding="utf-8")
    return {
        "dataset": job["dataset"],
        "scenario": job["scenario"],
        "stem": job["stem"],
        "status": "ok",
        "chars": len(body),
        "wall_seconds": wall,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset", action="append", default=None)
    p.add_argument("--scenario", action="append", default=None)
    p.add_argument(
        "--include",
        action="append",
        choices=sorted(VARIANT_BY_KIND),
        default=None,
        help="table kinds to analyse (default: skill_on-v11 + original)",
    )
    p.add_argument("--force-original", action="store_true", help="also analyse originals that already have a lab6 report")
    p.add_argument(
        "--neutral-e2e",
        action="store_true",
        help="analyse skill_on_e2e tables with the neutral prompt (old v11 behaviour) instead of the TAPP-aware one",
    )
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--timeout", type=int, default=900)
    p.add_argument("--attempts", type=int, default=3)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if not args.include:
        args.include = ["skill_on-v11", "original"]
    return args


def main() -> int:
    args = parse_args()
    jobs = build_jobs(args)
    print(f"[analysis-gen] pending jobs: {len(jobs)}", flush=True)
    if args.dry_run:
        for j in jobs[:40]:
            print(f"  {j['dataset']}/{j['scenario']}/{j['stem']}.md  <- {j['table'].name}  [{j['model']}]")
        if len(jobs) > 40:
            print(f"  ... and {len(jobs) - 40} more")
        return 0
    if not jobs:
        return 0

    exe = find_claude()
    results: list[dict[str, Any]] = []
    done = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(run_job, j, exe, args): j for j in jobs}
        for fut in as_completed(futs):
            j = futs[fut]
            try:
                r = fut.result()
            except Exception as exc:  # noqa: BLE001
                r = {
                    "dataset": j["dataset"],
                    "scenario": j["scenario"],
                    "stem": j["stem"],
                    "status": "error",
                    "error": repr(exc)[:300],
                }
            results.append(r)
            done += 1
            print(
                f"[analysis-gen] ({done}/{len(jobs)}) "
                f"{r['dataset']}/{r['scenario']}/{r['stem']} -> {r['status']}",
                flush=True,
            )

    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"[analysis-gen] ok={ok} failed={len(results) - ok}")
    log = OUT_ROOT / "_generation_log.json"
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    prev = _read_json(log).get("runs", []) if log.exists() else []
    log.write_text(
        json.dumps(
            {"runs": prev + [{"at": datetime.now(timezone.utc).isoformat(), "results": results}]},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
