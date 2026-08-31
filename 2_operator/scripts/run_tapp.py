"""CLI for the TAPP skill v10.

Commands:
    inspect  <input>                         Print schema, text profile, and recipe recommendation.
  plan     --input <path> --workdir <dir>  Write execution_plan.json from the calibrated recipe.
    augment-e2e --input <path> --workdir <dir>  Run plan/categorize/review/tag/merge inside the skill.
  merge    --input <path> --workdir <dir>  Strictly validate tag files, apply gates, and write output.

V10 treats LLM tagging as a constrained text-to-table operator: every generated
column must preserve row identity, respect closed vocabularies, avoid forced-fit
where possible, and leave metadata that can be audited later.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


SKILL_VERSION = "skill_v10"
_NOISE_MEMBERS = {"unknown", "not_mentioned", "other"}
_NULL_STRINGS = {"", "none", "null", "nan", "na", "n/a", "not mentioned", "not_mentioned"}
# Whole-table uninformative gate applied in _passes_coverage. The ceiling is
# per facet form, because "missing" means something different for each: a
# multi_label facet is sparse by construction once expanded to multi-hot, an
# ordinal facet is specified as "None when not mentioned" so only rows that
# raise the aspect carry a level, and a numeric facet extracts explicit numbers
# only. Categorical and boolean facets get the strict default -- they are the
# forms expected to have a value on most rows, and the form where an unbounded
# share of nulls previously went unchecked.
_DEFAULT_MAX_NULL_SHARE = 0.50
_FORM_MAX_NULL_SHARE = {
    "multi_label": 0.80,
    "ordinal": 0.70,
    "numeric": 0.50,
}
# A facet rescued by the low-coverage fallback must still carry some signal;
# reviving a near-empty column only turns an empty table into a useless one.
_FALLBACK_MAX_NULL_SHARE = 0.90
_DEFAULT_QUALITY_CONSTRAINTS = {
    "min_success_rate": 0.95,
    "min_returned_expected": 0.98,
    "max_forced_fit_rate": 0.2,
    "max_f2": 0.2,
    "post_merge_row_mismatch": 0,
}
_DEFAULT_PRICING = {
    "input_per_mtok_usd": 2.0,
    "cached_input_per_mtok_usd": 0.5,
    "output_per_mtok_usd": 8.0,
}


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_recipe_path() -> Path:
    return _skill_root() / "config" / "model_recipe.json"


def _load_recipe(path: str | None = None) -> dict[str, Any]:
    recipe_path = Path(path) if path else _default_recipe_path()
    with open(recipe_path, encoding="utf-8") as file:
        payload = json.load(file)
    payload["_path"] = str(recipe_path)
    return payload


def _read_table(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    if ext == ".csv":
        return pd.read_csv(path)
    if ext == ".parquet":
        return pd.read_parquet(path)
    if ext in (".pkl", ".pickle"):
        return pd.read_pickle(path)
    raise ValueError(f"Unsupported input extension: {ext}")


def _write_table(df: pd.DataFrame, path: str) -> None:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls"):
        df.to_excel(path, index=False)
    elif ext == ".csv":
        df.to_csv(path, index=False)
    elif ext == ".parquet":
        df.to_parquet(path, index=False)
    elif ext in (".pkl", ".pickle"):
        df.to_pickle(path)
    else:
        raise ValueError(f"Unsupported output extension: {ext}")


def _emit_dataframe(df: pd.DataFrame, workdir: str, output: str | None) -> tuple[str, str]:
    if output:
        _write_table(df, output)
        ext = os.path.splitext(output)[1].lower()
        loader = {
            ".xlsx": "pd.read_excel",
            ".xls": "pd.read_excel",
            ".csv": "pd.read_csv",
            ".parquet": "pd.read_parquet",
            ".pkl": "pd.read_pickle",
            ".pickle": "pd.read_pickle",
        }.get(ext, "pd.read_*")
        return output, loader

    default_path = os.path.join(workdir, "augmented.parquet")
    try:
        df.to_parquet(default_path, index=False)
        return default_path, "pd.read_parquet"
    except Exception:
        fallback_path = os.path.join(workdir, "augmented.pkl")
        df.to_pickle(fallback_path)
        return fallback_path, "pd.read_pickle"


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2, default=str)


# ---------------------------------------------------------------------------
# Pillar 4.B: artifact manifest + content-addressed placeholder resolver
# ---------------------------------------------------------------------------

ARTIFACT_MANIFEST_NAME = "artifact_manifest.json"
ARTIFACT_PLACEHOLDER_RE = re.compile(
    r"<<artifact:(?P<kind>[A-Za-z0-9_./\-]+)@sha256:(?P<sha>[0-9a-fA-F]{8,64})>>"
)


def _sha256_file(path: str | Path) -> str:
    path = Path(path)
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def _artifact_manifest_path(workdir: str | Path) -> Path:
    return Path(workdir) / ARTIFACT_MANIFEST_NAME


def _load_artifact_manifest(workdir: str | Path) -> dict[str, Any]:
    path = _artifact_manifest_path(workdir)
    if not path.exists():
        return {
            "manifest_version": 1,
            "skill_version": SKILL_VERSION,
            "workdir": str(Path(workdir).resolve()),
            "artifacts": {},
            "by_kind": {},
        }
    with open(path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    manifest.setdefault("manifest_version", 1)
    manifest.setdefault("skill_version", SKILL_VERSION)
    manifest.setdefault("workdir", str(Path(workdir).resolve()))
    manifest.setdefault("artifacts", {})
    manifest.setdefault("by_kind", {})
    return manifest


def _placeholder_for(kind: str, sha: str, length: int = 12) -> str:
    return f"<<artifact:{kind}@sha256:{sha[:length]}>>"


def _register_artifact(
    workdir: str | Path,
    kind: str,
    path: str | Path,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute sha256, append/update artifact_manifest.json, return the artifact entry.

    `kind` is a stable label such as `execution_plan`, `specs`, `tags`,
    `merge_report`, `facet_report`, `oos_report`, `trace`, or `augmented_table`.
    The same `(kind, path)` is updated in place when re-registered.
    """
    workdir_path = Path(workdir)
    workdir_path.mkdir(parents=True, exist_ok=True)
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"Cannot register missing artifact: {target}")
    sha = _sha256_file(target)
    size = target.stat().st_size
    try:
        rel_path = str(target.resolve().relative_to(workdir_path.resolve()))
    except ValueError:
        rel_path = str(target.resolve())
    placeholder = _placeholder_for(kind, sha)
    manifest = _load_artifact_manifest(workdir_path)
    key = f"{kind}:{rel_path}"
    entry = {
        "kind": kind,
        "path": rel_path,
        "abs_path": str(target.resolve()),
        "sha256": sha,
        "sha256_short": sha[:12],
        "size_bytes": int(size),
        "placeholder": placeholder,
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        for ek, ev in extra.items():
            if ek not in entry:
                entry[ek] = ev
    manifest["artifacts"][key] = entry
    by_kind = manifest["by_kind"].setdefault(kind, [])
    if key not in by_kind:
        by_kind.append(key)
    _write_json(_artifact_manifest_path(workdir_path), manifest)
    return entry


def _resolve_artifact_ref(workdir: str | Path, ref: str) -> dict[str, Any] | None:
    """Look up an artifact by `<<artifact:<kind>@sha256:<short>>>` in the manifest."""
    match = ARTIFACT_PLACEHOLDER_RE.search(ref or "")
    if not match:
        return None
    kind = match.group("kind")
    sha_prefix = match.group("sha").lower()
    manifest = _load_artifact_manifest(workdir)
    for key in manifest["by_kind"].get(kind, []):
        entry = manifest["artifacts"].get(key)
        if entry and entry.get("sha256", "").lower().startswith(sha_prefix):
            return entry
    return None


# ---------------------------------------------------------------------------
# Pillar 4.C: stage trace persistence (subagent reasoning as first-class artifact)
# ---------------------------------------------------------------------------

TRACES_DIR_NAME = "traces"


def _record_trace(
    workdir: str | Path,
    stage: str,
    *,
    status: str = "ok",
    model: str | None = None,
    input_refs: list[str] | None = None,
    output_refs: list[str] | None = None,
    started_at: str | None = None,
    finished_at: str | None = None,
    latency_ms: float | int | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    reasoning_summary: str | None = None,
    plan_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Persist a per-stage trace JSON and register it as a `trace` artifact.

    Designed for the host LLM to call after each subagent stage (categorize, review,
    tag, consolidation), so the audit trail is reproducible without depending on the
    runtime keeping CoT in memory. The trace itself is content-addressed.
    """
    workdir_path = Path(workdir)
    traces_dir = workdir_path / TRACES_DIR_NAME
    traces_dir.mkdir(parents=True, exist_ok=True)
    finished = finished_at or datetime.now(timezone.utc).isoformat()
    payload: dict[str, Any] = {
        "trace_version": 1,
        "skill_version": SKILL_VERSION,
        "stage": stage,
        "status": status,
        "model": model,
        "plan_id": plan_id,
        "input_refs": list(input_refs or []),
        "output_refs": list(output_refs or []),
        "started_at": started_at,
        "finished_at": finished,
        "latency_ms": float(latency_ms) if latency_ms is not None else None,
        "input_tokens": int(input_tokens) if input_tokens is not None else None,
        "output_tokens": int(output_tokens) if output_tokens is not None else None,
        "reasoning_summary": reasoning_summary,
    }
    if extra:
        for ek, ev in extra.items():
            if ek not in payload:
                payload[ek] = ev
    seed = json.dumps({"stage": stage, "finished_at": finished, "model": model, "input_refs": payload["input_refs"], "output_refs": payload["output_refs"]}, sort_keys=True, default=str)
    short_id = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:10]
    safe_stage = _slug(stage) if stage else "stage"
    safe_ts = re.sub(r"[^0-9A-Za-z]+", "", finished)[:18]
    trace_path = traces_dir / f"{safe_stage}_{safe_ts}_{short_id}.json"
    payload["trace_id"] = f"{safe_stage}_{safe_ts}_{short_id}"
    payload["trace_path"] = str(trace_path)
    _write_json(trace_path, payload)
    entry = _register_artifact(
        workdir_path,
        kind="trace",
        path=trace_path,
        extra={
            "stage": stage,
            "status": status,
            "model": model,
            "trace_id": payload["trace_id"],
            "input_refs": payload["input_refs"],
            "output_refs": payload["output_refs"],
        },
    )
    payload["placeholder"] = entry["placeholder"]
    return payload


def _print_df_preview(df: pd.DataFrame, new_cols: list[str]) -> None:
    if not new_cols:
        print("Preview skipped: no columns survived gates.")
        return
    with pd.option_context("display.max_columns", None, "display.width", 200, "display.max_colwidth", 60):
        base_cols = [col for col in df.columns if col not in new_cols][:3]
        preview_cols = base_cols + new_cols[:8]
        print("Preview (first 5 rows, key + new cols):")
        print(df[preview_cols].head().to_string(index=False))


# ---------------------------------------------------------------------------
# Inspect, profile, and planning
# ---------------------------------------------------------------------------


def _schema(df: pd.DataFrame) -> list[dict[str, str]]:
    return [{"name": str(col), "dtype": str(df[col].dtype)} for col in df.columns]


def _text_stats(df: pd.DataFrame) -> dict[str, dict[str, int]]:
    stats: dict[str, dict[str, int]] = {}
    for col in df.columns:
        if not (pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])):
            continue
        values = df[col].dropna().astype(str)
        if values.empty:
            continue
        lengths = values.str.len()
        if lengths.median() <= 30:
            continue
        stats[str(col)] = {
            "non_null": int(lengths.count()),
            "mean_chars": int(lengths.mean()),
            "median_chars": int(lengths.median()),
            "p95_chars": int(lengths.quantile(0.95)),
            "max_chars": int(lengths.max()),
        }
    return stats


def _json_index(index_value: Any) -> int | str:
    try:
        return int(index_value)
    except (TypeError, ValueError):
        return str(index_value)


def _records_with_index(df: pd.DataFrame, indices: list[Any]) -> list[dict[str, Any]]:
    frame = df.loc[indices].copy()
    frame.insert(0, "_row_index", [_json_index(idx) for idx in frame.index])
    return frame.astype(object).where(frame.notna(), None).to_dict(orient="records")


def _primary_text_col(text_stats: dict[str, dict[str, int]], requested: str | None = None) -> str | None:
    if requested:
        return requested
    if not text_stats:
        return None
    return max(
        text_stats,
        key=lambda col: (
            int(text_stats[col].get("non_null", 0)),
            int(text_stats[col].get("p95_chars", 0)),
            int(text_stats[col].get("median_chars", 0)),
        ),
    )


def _stratified_sample(df: pd.DataFrame, text_col: str | None, sample_size: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    requested = max(0, int(sample_size or 0))
    if requested == 0 or df.empty:
        return [], {"strategy": "none", "requested": requested, "returned": 0, "text_col": text_col}

    target = min(requested, len(df))
    if not text_col or text_col not in df.columns:
        indices = df.sample(n=target, random_state=17).sort_index().index.tolist()
        return _records_with_index(df, indices), {
            "strategy": "random_no_text_column",
            "requested": requested,
            "returned": len(indices),
            "text_col": text_col,
            "row_indices": [_json_index(idx) for idx in indices],
        }

    text_values = df[text_col]
    lengths = text_values.fillna("").astype(str).str.len()
    eligible = text_values.notna()
    if int(eligible.sum()) < 3:
        indices = df.sample(n=target, random_state=17).sort_index().index.tolist()
        return _records_with_index(df, indices), {
            "strategy": "random_sparse_text",
            "requested": requested,
            "returned": len(indices),
            "text_col": text_col,
            "row_indices": [_json_index(idx) for idx in indices],
        }

    q_short = float(lengths[eligible].quantile(1 / 3))
    q_long = float(lengths[eligible].quantile(2 / 3))
    bucket_masks = {
        "short": eligible & (lengths <= q_short),
        "medium": eligible & (lengths > q_short) & (lengths <= q_long),
        "long": eligible & (lengths > q_long),
    }
    # When target < 3 we cannot give every bucket a positive quota, so we set
    # per-bucket to floor(target/3) (which can be 0) and let the remainder fall
    # into the long bucket. This keeps quotas non-negative even for sample-size 1
    # or 2 and still preserves the long-tail bias for the residual.
    per_bucket = max(0, target // 3)
    remainder = max(0, target - per_bucket * 3)
    quotas = {"short": per_bucket, "medium": per_bucket, "long": per_bucket + remainder}

    selected: list[Any] = []
    bucket_meta: dict[str, dict[str, Any]] = {}
    for bucket_name, mask in bucket_masks.items():
        available = df.index[mask].tolist()
        take = min(len(available), quotas[bucket_name])
        if take:
            sampled = df.loc[available].sample(n=take, random_state=17 + len(selected)).index.tolist()
        else:
            sampled = []
        selected.extend(sampled)
        bucket_meta[bucket_name] = {
            "available": len(available),
            "selected": len(sampled),
            "length_range": [int(lengths.loc[available].min()) if available else None, int(lengths.loc[available].max()) if available else None],
        }

    if len(selected) < target:
        remaining = df.index.difference(pd.Index(selected)).tolist()
        fill_count = min(target - len(selected), len(remaining))
        if fill_count:
            selected.extend(df.loc[remaining].sample(n=fill_count, random_state=23).index.tolist())

    selected = sorted(dict.fromkeys(selected), key=lambda idx: df.index.get_loc(idx))[:target]
    return _records_with_index(df, selected), {
        "strategy": "text_length_stratified",
        "requested": requested,
        "returned": len(selected),
        "text_col": text_col,
        "quantiles": {"short_max": q_short, "medium_max": q_long},
        "buckets": bucket_meta,
        "row_indices": [_json_index(idx) for idx in selected],
    }


def _profile_dataframe(df: pd.DataFrame, text_stats: dict[str, dict[str, int]]) -> dict[str, Any]:
    numeric_cols = [str(col) for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    datetime_cols = [str(col) for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    categorical_cols: list[str] = []
    for col in df.columns:
        if str(col) in text_stats:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
        nunique = df[col].nunique(dropna=True)
        if 1 < nunique <= min(50, max(10, len(df) // 10)):
            categorical_cols.append(str(col))

    return {
        "rows": int(len(df)),
        "numeric_cols": numeric_cols,
        "datetime_cols": datetime_cols,
        "categorical_cols": categorical_cols[:25],
        "text_heavy_cols": [col for col, stat in text_stats.items() if stat["median_chars"] > 80 and stat["non_null"] >= 50],
        "candidate_group_cols": categorical_cols[:25],
    }


def _ceil_div(value: int, divisor: int) -> int:
    if value <= 0:
        return 0
    return int(math.ceil(value / max(1, divisor)))


def _clamp_rate(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _mean_text_chars(text_stats: dict[str, dict[str, int]] | None) -> int:
    if not text_stats:
        return 120
    selected = max(
        text_stats.values(),
        key=lambda stat: (
            int(stat.get("non_null", 0)),
            int(stat.get("p95_chars", 0)),
            int(stat.get("mean_chars", 0)),
        ),
    )
    return max(1, int(selected.get("mean_chars") or selected.get("median_chars") or 120))


def _quality_constraints(recipe: dict[str, Any], budget_usd: float | None, wall_time_s: float | None) -> dict[str, Any]:
    constraints = {**_DEFAULT_QUALITY_CONSTRAINTS, **(recipe.get("quality_constraints") or {})}
    if budget_usd is not None:
        constraints["budget_usd"] = float(budget_usd)
    if wall_time_s is not None:
        constraints["wall_time_s"] = float(wall_time_s)
    return constraints


def _pricing_for_model(recipe: dict[str, Any], model: str | None) -> dict[str, float]:
    pricing = recipe.get("pricing") or {}
    model_pricing = pricing.get(model or "") or pricing.get("default") or {}
    merged = {**_DEFAULT_PRICING, **model_pricing}
    out: dict[str, float] = {}
    for key, value in merged.items():
        if isinstance(value, (int, float)):
            out[key] = float(value)
            continue
        try:
            out[key] = float(value)
        except (TypeError, ValueError):
            # Non-numeric metadata entries such as "source" are kept out of
            # the numeric pricing payload so cost arithmetic stays safe.
            continue
    return out


def _cache_hit_rate(selected_tier: dict[str, Any], override: float | None) -> float:
    if override is not None:
        return _clamp_rate(override)
    policy = str(selected_tier.get("cache_policy", "")).lower()
    if "no" in policy or "0" in policy:
        return 0.0
    if "prefix" in policy or "cache" in policy:
        return 1.0
    return 0.0


def _effective_item_cap(selected_tier: dict[str, Any], facets_per_call: int, recipe: dict[str, Any]) -> int:
    base = max(1, int(selected_tier.get("max_items", 1000)))
    facets_per_call = max(1, int(facets_per_call))
    if facets_per_call == 1:
        return base
    cfg = recipe.get("bundled_tagging") or {}
    factors = cfg.get("effective_item_cap_factors") or {"1": 1.0, "3": 0.65, "5": 0.45}
    if str(facets_per_call) in factors:
        factor = float(factors[str(facets_per_call)])
    else:
        factor = max(0.25, 1.0 / (1.0 + 0.35 * (facets_per_call - 1)))
    return max(int(cfg.get("min_effective_items", 50)), int(base * factor))


def _range_preview(total: int, chunk_size: int, max_ranges: int = 8) -> list[dict[str, int]]:
    ranges: list[dict[str, int]] = []
    for start in range(0, max(0, total), max(1, chunk_size)):
        ranges.append({"start": start, "end": min(total, start + chunk_size)})
        if len(ranges) >= max_ranges:
            break
    return ranges


def _chunk_summary(total: int, chunk_size: int, axis: str) -> dict[str, Any]:
    chunk_size = max(1, int(chunk_size))
    return {
        "axis": axis,
        "count": _ceil_div(total, chunk_size),
        "size": chunk_size,
        "range_format": "zero_based_half_open_[start,end)",
        "ranges_preview": _range_preview(total, chunk_size),
    }


def _plan_id(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def _constraint_status(cost_model: dict[str, Any], constraints: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    budget = constraints.get("budget_usd")
    wall = constraints.get("wall_time_s")
    if budget is not None and cost_model.get("estimated_cost_usd") is not None and cost_model["estimated_cost_usd"] > float(budget):
        violations.append("budget_usd")
    if wall is not None and cost_model.get("estimated_wall_s") is not None and cost_model["estimated_wall_s"] > float(wall):
        violations.append("wall_time_s")
    return {"satisfied": not violations, "violations": violations}


def _estimate_cost_model(
    rows: int,
    labels: int,
    facets: int,
    facets_per_call: int,
    item_chunk_size: int,
    label_chunk_size: int,
    selected_tier: dict[str, Any],
    categorization: dict[str, Any],
    recipe: dict[str, Any],
    text_stats: dict[str, dict[str, int]] | None,
    cache_hit_rate: float,
    concurrency: int,
    host_model: str | None = None,
    host_pricing_key: str | None = None,
) -> dict[str, Any]:
    cost_cfg = recipe.get("cost_model") or {}
    item_chunks = _ceil_div(rows, item_chunk_size)
    label_chunks = _ceil_div(labels, label_chunk_size)
    facet_bundles = _ceil_div(facets, facets_per_call)
    tagging_calls = item_chunks * max(1, label_chunks) * max(1, facet_bundles)
    reducer_calls = item_chunks * max(1, facet_bundles) if label_chunks > 1 else 0
    if categorization.get("strategy") == "map_reduce":
        categorization_calls = _ceil_div(rows, int(categorization.get("chunk_proposal_rows", item_chunk_size))) + 2
    else:
        categorization_calls = 1

    mean_text_tokens = _mean_text_chars(text_stats) / 4.0
    average_items = min(max(rows, 1), max(1, item_chunk_size))
    average_labels = min(max(labels, 1), max(1, label_chunk_size))
    static_prompt_tokens = int(cost_cfg.get("static_prompt_tokens", 900))
    label_tokens = int(cost_cfg.get("tokens_per_label", 8)) * average_labels
    facet_tokens = int(cost_cfg.get("tokens_per_facet_spec", 80)) * max(1, facets_per_call)
    text_tokens = int(average_items * mean_text_tokens)
    tag_input_per_call = static_prompt_tokens + label_tokens + facet_tokens + text_tokens
    reducer_input_per_call = int(cost_cfg.get("reducer_static_tokens", 700)) + int(average_items * 16) + label_tokens
    categorization_input_per_call = static_prompt_tokens + int(average_items * mean_text_tokens) + int(cost_cfg.get("categorization_overhead_tokens", 500))
    output_per_tag_call = int(cost_cfg.get("output_tokens_per_item", 6) * average_items * max(1, facets_per_call))
    output_per_reducer_call = int(cost_cfg.get("output_tokens_per_item", 6) * average_items)
    output_per_categorization_call = int(cost_cfg.get("categorization_output_tokens", 1600))

    input_tokens = int(
        tagging_calls * tag_input_per_call
        + reducer_calls * reducer_input_per_call
        + categorization_calls * categorization_input_per_call
    )
    output_tokens = int(
        tagging_calls * output_per_tag_call
        + reducer_calls * output_per_reducer_call
        + categorization_calls * output_per_categorization_call
    )
    cacheable_prefix_tokens = int(cost_cfg.get("cacheable_prefix_tokens", 350))
    cached_tokens = int((tagging_calls + reducer_calls + categorization_calls) * cacheable_prefix_tokens * cache_hit_rate)
    cached_tokens = min(cached_tokens, input_tokens)
    billable_uncached_input_tokens = max(0, input_tokens - cached_tokens)
    calibration_model = selected_tier.get("calibration_model") or selected_tier.get("model")
    executor_model = host_model or calibration_model
    pricing_key = host_pricing_key or host_model or calibration_model
    pricing = _pricing_for_model(recipe, pricing_key)
    estimated_cost = (
        billable_uncached_input_tokens * pricing["input_per_mtok_usd"]
        + cached_tokens * pricing["cached_input_per_mtok_usd"]
        + output_tokens * pricing["output_per_mtok_usd"]
    ) / 1_000_000

    calibration = selected_tier.get("calibration") or {}
    calibration_wall = calibration.get("wall_s")
    if calibration_wall is None:
        wall_per_wave = float(137.0 if "claude" in str(calibration_model or "").lower() else 34.0)
    else:
        wall_per_wave = float(calibration_wall)
    parallelism = max(1, int(concurrency))
    llm_calls = tagging_calls + reducer_calls + categorization_calls
    estimated_wall = float(_ceil_div(llm_calls, parallelism) * wall_per_wave)
    retry_rate = float(cost_cfg.get("expected_retry_rate", 0.03))
    expected_retries = float(tagging_calls * retry_rate)

    return {
        "model": executor_model,
        "calibration_model": calibration_model,
        "pricing_key": pricing_key,
        "calls": {
            "categorization": int(categorization_calls),
            "tagging": int(tagging_calls),
            "label_consolidation": int(reducer_calls),
            "total_llm_calls": int(llm_calls),
        },
        "tokens": {
            "estimated_input_tokens": input_tokens,
            "estimated_cached_tokens": cached_tokens,
            "estimated_billable_uncached_input_tokens": billable_uncached_input_tokens,
            "estimated_output_tokens": output_tokens,
            "cache_hit_rate_assumption": cache_hit_rate,
        },
        "pricing": pricing,
        "estimated_cost_usd": round(float(estimated_cost), 6),
        "estimated_wall_s": round(estimated_wall, 3),
        "expected_full_chunk_retries": round(expected_retries, 3),
        "concurrency": parallelism,
        "source": "recipe_defaults_plus_shape_estimate",
        "executor_source": "host_model" if host_model else "calibration_model_fallback",
    }


def _plan_space_candidate_id(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:12]


def _host_model_compatibility(
    tier: dict[str, Any],
    host_model: str | None,
    recipe: dict[str, Any],
    policy: str,
    extra_allowlist: list[str] | None = None,
) -> dict[str, Any]:
    """Pillar 3.A guard: classify the host vs selected-tier calibration relationship.

    Status values:
      * `calibration_model_default` — no `--host-model` passed; planner falls
        back to the tier's calibration_model and assumes 1:1 calibration.
      * `calibrated` — host_model exactly matches tier.calibration_model; the
        accuracy / F2 gates apply directly.
      * `peer_class` — host_model is listed in `tier.host_model_allowlist`
        (or the per-call extra allowlist); calibration is assumed transferable
        but is not measured. A warning is recorded.
      * `unverified` — host_model is neither the calibration model nor in any
        allowlist. Reliability/F2 gates still pass on the tier numbers, but
        the actual host accuracy is unknown. Under `policy="strict"` the
        caller must abort the plan; under `policy="warn"` a warning is
        recorded but the plan proceeds.
    """
    policy_normalized = (policy or "warn").lower()
    if policy_normalized not in {"warn", "strict", "off"}:
        policy_normalized = "warn"
    calibration_model = tier.get("calibration_model") or tier.get("model")
    tier_name = tier.get("name")
    base_allowlist = list(tier.get("host_model_allowlist") or [])
    extra = list(extra_allowlist or [])
    full_allowlist = sorted({m for m in base_allowlist + extra if m})

    if not host_model:
        return {
            "status": "calibration_model_default",
            "host_model": None,
            "calibration_model": calibration_model,
            "tier": tier_name,
            "policy": policy_normalized,
            "allowlist": full_allowlist,
            "warnings": [],
            "aborted": False,
        }
    if host_model == calibration_model:
        return {
            "status": "calibrated",
            "host_model": host_model,
            "calibration_model": calibration_model,
            "tier": tier_name,
            "policy": policy_normalized,
            "allowlist": full_allowlist,
            "warnings": [],
            "aborted": False,
        }
    if host_model in full_allowlist:
        warning = (
            f"host_model '{host_model}' is on tier '{tier_name}' peer-class allowlist; "
            f"calibration of '{calibration_model}' is assumed transferable but not measured."
        )
        return {
            "status": "peer_class",
            "host_model": host_model,
            "calibration_model": calibration_model,
            "tier": tier_name,
            "policy": policy_normalized,
            "allowlist": full_allowlist,
            "warnings": [warning],
            "aborted": False,
        }
    warning = (
        f"host_model '{host_model}' is NOT calibrated for tier '{tier_name}' "
        f"(calibration_model='{calibration_model}'). reliability/F2 gates use that tier's "
        f"numbers but actual host accuracy is unknown. Add the host to '{tier_name}.host_model_allowlist' "
        f"or pass --host-model-allowlist to acknowledge the cross-model transfer."
    )
    aborted = policy_normalized == "strict"
    return {
        "status": "unverified",
        "host_model": host_model,
        "calibration_model": calibration_model,
        "tier": tier_name,
        "policy": policy_normalized,
        "allowlist": full_allowlist,
        "warnings": [warning],
        "aborted": aborted,
    }


def _reliability_estimate(
    tier: dict[str, Any],
    ni_factor: float,
    nl_factor: float,
    plan_search_cfg: dict[str, Any],
) -> dict[str, Any]:
    """Conservative reliability estimate per (tier, ni_factor, nl_factor) candidate.

    Two quantities are estimated:
    * `estimated_accuracy`: based on the per-tier `calibration.accuracy_mean`
      from the Justin recipe sweep. Oversize factors (> 1.0) degrade the
      estimate; downsize factors inherit the base accuracy.
    * `estimated_f2` (Pillar 3 forced-fit rate): if the tier publishes
      `calibration.forced_fit_rate`, that is used as the base. Otherwise we
      fall back to a conservative proxy `1 - accuracy_mean`. Oversize factors
      add to the F2 estimate using the same `degradation_per_oversize_factor`
      knob, since over-packed contexts are the primary forced-fit driver.
      Both `f2_basis` ("calibration_forced_fit_rate" / "accuracy_proxy" /
      "no_calibration") and `f2_oversize_penalty` are surfaced for audit.
    """
    calibration = tier.get("calibration") or {}
    base = calibration.get("accuracy_mean")
    base = float(base) if isinstance(base, (int, float)) else None
    base_ci = calibration.get("accuracy_ci")
    base_ci = float(base_ci) if isinstance(base_ci, (int, float)) else None
    deg_factor = float(plan_search_cfg.get("degradation_per_oversize_factor", 0.05))
    extra = max(0.0, ni_factor - 1.0) + max(0.0, nl_factor - 1.0)
    estimated = None if base is None else max(0.0, base - extra * deg_factor)

    raw_f2 = calibration.get("forced_fit_rate")
    f2_base: float | None
    f2_basis: str
    if isinstance(raw_f2, (int, float)):
        f2_base = float(raw_f2)
        f2_basis = "calibration_forced_fit_rate"
    elif base is not None:
        f2_base = max(0.0, 1.0 - base)
        f2_basis = "accuracy_proxy"
    else:
        f2_base = None
        f2_basis = "no_calibration"
    f2_oversize_penalty = round(extra * deg_factor, 4)
    estimated_f2 = None if f2_base is None else min(1.0, f2_base + f2_oversize_penalty)

    return {
        "calibration_accuracy": base,
        "calibration_ci": base_ci,
        "estimated_accuracy": estimated,
        "oversize_penalty": round(extra * deg_factor, 4),
        "calibration_forced_fit_rate": float(raw_f2) if isinstance(raw_f2, (int, float)) else None,
        "estimated_f2": estimated_f2,
        "f2_basis": f2_basis,
        "f2_oversize_penalty": f2_oversize_penalty,
    }


def _plan_space_search(
    rows: int,
    estimated_labels: int,
    estimated_facets: int,
    facets_per_call: int,
    recipe: dict[str, Any],
    text_stats: dict[str, dict[str, int]] | None,
    categorization_strategy: str,
    constraints: dict[str, Any],
    concurrency: int,
    cache_hit_rate_override: float | None,
    host_model: str | None,
    host_pricing_key: str | None,
    allow_opt_in_tiers: list[str] | None = None,
) -> dict[str, Any]:
    """Pillar 3: enumerate (tier x ni x nl x cache_hit_rate) candidates, filter by reliability + budget gate, pick min cost."""
    cfg = recipe.get("plan_search") or {}
    enabled = bool(cfg.get("enabled", True))
    min_acc = float(cfg.get("min_calibration_accuracy", 0.95))
    max_f2 = float(cfg.get("max_calibration_f2", 0.2))
    ni_factors = list(cfg.get("ni_grid_factors") or [1.0])
    nl_factors = list(cfg.get("nl_grid_factors") or [1.0])
    cache_grid = list(cfg.get("cache_hit_rate_grid") or [None])
    rank_by = str(cfg.get("rank_by") or "estimated_cost_usd")
    tiebreak_by = str(cfg.get("tiebreak_by") or "estimated_wall_s")

    if not enabled:
        return {"selected": None, "log": [], "enabled": False, "reason": "plan_search.disabled"}

    tiers = recipe.get("tiers") or []
    allow_opt_in_set = {str(name).strip() for name in (allow_opt_in_tiers or []) if name}
    selectable = [
        tier for tier in tiers
        if (not tier.get("opt_in_only")) or (str(tier.get("name") or "") in allow_opt_in_set)
    ]
    if not selectable:
        return {"selected": None, "log": [], "enabled": True, "reason": "no_selectable_tiers"}

    candidates: list[dict[str, Any]] = []
    for tier in selectable:
        tier_max_items = max(1, int(tier.get("max_items", 1000)))
        tier_max_labels = max(1, int(tier.get("max_labels", estimated_labels or 30)))
        tier_max_product = int(tier.get("max_item_label_product", tier_max_items * tier_max_labels))
        for ni_factor in ni_factors:
            ni_factor = float(ni_factor)
            ni = max(1, int(round(tier_max_items * ni_factor)))
            for nl_factor in nl_factors:
                nl_factor = float(nl_factor)
                nl = max(1, int(round(tier_max_labels * nl_factor)))
                for cache_choice in cache_grid:
                    cache_rate = (
                        _cache_hit_rate(tier, cache_hit_rate_override)
                        if cache_choice is None
                        else _clamp_rate(float(cache_choice))
                    )
                    categorization = _categorization_plan(rows, recipe, tier, text_stats, categorization_strategy)
                    cost_model = _estimate_cost_model(
                        rows=int(rows),
                        labels=int(estimated_labels),
                        facets=int(estimated_facets),
                        facets_per_call=int(facets_per_call),
                        item_chunk_size=int(ni),
                        label_chunk_size=int(nl),
                        selected_tier=tier,
                        categorization=categorization,
                        recipe=recipe,
                        text_stats=text_stats,
                        cache_hit_rate=cache_rate,
                        concurrency=concurrency,
                        host_model=host_model,
                        host_pricing_key=host_pricing_key,
                    )
                    reliability = _reliability_estimate(tier, ni_factor, nl_factor, cfg)
                    constraint_status = _constraint_status(cost_model, constraints)
                    reliability_acc = reliability["estimated_accuracy"]
                    estimated_f2 = reliability.get("estimated_f2")
                    require_calibration = bool(cfg.get("require_calibration_for_reliability_gate", True))
                    if require_calibration:
                        reliability_pass = reliability_acc is not None and reliability_acc >= min_acc
                        f2_pass = estimated_f2 is not None and float(estimated_f2) <= max_f2
                    else:
                        reliability_pass = reliability_acc is None or reliability_acc >= min_acc
                        f2_pass = estimated_f2 is None or float(estimated_f2) <= max_f2
                    envelope_pass = (
                        estimated_labels <= tier_max_labels
                        and rows * max(1, estimated_labels) <= tier_max_product
                    )
                    candidate = {
                        "candidate_id": _plan_space_candidate_id({
                            "tier": tier.get("name"),
                            "ni": ni,
                            "nl": nl,
                            "cache_rate": cache_rate,
                        }),
                        "tier": tier.get("name"),
                        "calibration_model": tier.get("calibration_model") or tier.get("model"),
                        "ni": ni,
                        "nl": nl,
                        "ni_factor": ni_factor,
                        "nl_factor": nl_factor,
                        "cache_hit_rate": cache_rate,
                        "estimated_cost_usd": float(cost_model.get("estimated_cost_usd", 0.0)),
                        "estimated_wall_s": float(cost_model.get("estimated_wall_s", 0.0)),
                        "expected_full_chunk_retries": float(cost_model.get("expected_full_chunk_retries", 0.0)),
                        "reliability": reliability,
                        "reliability_floor": min_acc,
                        "reliability_pass": bool(reliability_pass),
                        "envelope_pass": bool(envelope_pass),
                        "budget_pass": bool(constraint_status.get("satisfied", True)),
                        "budget_violations": list(constraint_status.get("violations") or []),
                        "f2_estimated": float(estimated_f2) if estimated_f2 is not None else None,
                        "f2_basis": reliability.get("f2_basis"),
                        "f2_floor": max_f2,
                        "f2_pass": bool(f2_pass),
                        "passed_all_gates": bool(reliability_pass and envelope_pass and constraint_status.get("satisfied", True) and f2_pass),
                    }
                    candidates.append(candidate)

    survivors = [c for c in candidates if c["passed_all_gates"]]
    if not survivors:
        return {
            "selected": None,
            "log": candidates,
            "enabled": True,
            "reason": "no_candidate_passes_gates",
            "min_calibration_accuracy": min_acc,
            "max_calibration_f2": max_f2,
        }

    survivors.sort(key=lambda c: (c.get(rank_by, 0.0), c.get(tiebreak_by, 0.0)))
    selected = survivors[0]
    return {
        "selected": selected,
        "log": candidates,
        "enabled": True,
        "reason": "min_cost_under_reliability_floor",
        "rank_by": rank_by,
        "tiebreak_by": tiebreak_by,
        "min_calibration_accuracy": min_acc,
        "max_calibration_f2": max_f2,
    }


def _categorization_plan(
    rows: int,
    recipe: dict[str, Any],
    selected_tier: dict[str, Any],
    text_stats: dict[str, dict[str, int]] | None = None,
    strategy_override: str = "auto",
) -> dict[str, Any]:
    cfg = recipe.get("categorization_planning") or {}
    single_pass_max_rows = int(cfg.get("single_pass_max_rows", selected_tier.get("max_items", 1000)))
    chunk_rows = int(cfg.get("chunk_proposal_rows", selected_tier.get("max_items", 1000)))
    long_text_p95_chars = int(cfg.get("long_text_p95_chars", 2000))
    has_long_text = any(int(stat.get("p95_chars", 0)) >= long_text_p95_chars for stat in (text_stats or {}).values())
    auto_strategy = "map_reduce" if rows > single_pass_max_rows or has_long_text else "single_pass"
    strategy = strategy_override if strategy_override in {"single_pass", "map_reduce"} else auto_strategy
    prompt = "prompts/categorization_large_scale.md" if strategy == "map_reduce" else "prompts/categorization.md"

    plan = {
        "strategy": strategy,
        "prompt": prompt,
        "reason": "selected by override" if strategy_override in {"single_pass", "map_reduce"} else "selected from row/text scale",
        "single_pass_max_rows": single_pass_max_rows,
        "long_text_p95_chars": long_text_p95_chars,
    }
    if strategy == "map_reduce":
        plan.update({
            "chunk_proposal_rows": min(rows, chunk_rows) if rows else chunk_rows,
            "max_chunk_proposals": int(cfg.get("max_chunk_proposals", 20)),
            "consolidation_top_k": int(cfg.get("consolidation_top_k", 30)),
            "rare_evidence_keep_min_rows": int(cfg.get("rare_evidence_keep_min_rows", 3)),
            "stages": cfg.get("stages") or ["chunk_proposal", "global_consolidation", "final_selection"],
        })
    return plan


def _visual_preview_plan(recipe: dict[str, Any]) -> dict[str, Any]:
    cfg = recipe.get("visual_preview") or {}
    resolution = cfg.get("resolution") or {}
    return {
        "enabled": bool(cfg.get("enabled", True)),
        "strategy": str(cfg.get("strategy") or "overview_dense_ocr"),
        "mode": "fixed_resolution_table_images",
        "density": str(cfg.get("density") or "ocr"),
        "resolution": {
            "width": int(resolution.get("width", cfg.get("width", 1600))),
            "height": int(resolution.get("height", cfg.get("height", 2200))),
        },
        "overview_rows": int(cfg.get("overview_rows", 60)),
        "rows_per_image": int(cfg.get("rows_per_image", 60)),
        "max_columns": int(cfg.get("max_columns", 6)),
        "max_pages_per_prompt": int(cfg.get("max_pages_per_prompt", 3)),
        "use_for": cfg.get("use_for") or ["inspect", "categorization", "review", "analysis_preview"],
        "not_for": cfg.get("not_for") or ["tagging", "merge", "exact_counts", "numeric_calculation"],
        "raw_data_required_for": ["tagging", "exact_counts", "joins", "numeric_calculation"],
    }


def _recommend_plan(
    rows: int,
    estimated_labels: int,
    recipe: dict[str, Any],
    text_stats: dict[str, dict[str, int]] | None = None,
    categorization_strategy: str = "auto",
    estimated_facets: int = 1,
    facets_per_call: int = 1,
    budget_usd: float | None = None,
    wall_time_s: float | None = None,
    concurrency: int = 1,
    cache_hit_rate_override: float | None = None,
    host_model: str | None = None,
    host_pricing_key: str | None = None,
    allow_opt_in_tiers: list[str] | None = None,
    host_model_allowlist: list[str] | None = None,
    host_model_policy: str | None = None,
    disable_plan_search: bool = False,
    static_plan_tier: str | None = None,
    static_plan_ni: int | None = None,
    static_plan_nl: int | None = None,
) -> dict[str, Any]:
    tiers = recipe.get("tiers") or []
    allow_opt_in_set = {str(name).strip() for name in (allow_opt_in_tiers or []) if name}
    selectable_tiers = [
        tier for tier in tiers
        if (not tier.get("opt_in_only")) or (str(tier.get("name") or "") in allow_opt_in_set)
    ]
    selected = selectable_tiers[-1] if selectable_tiers else (tiers[-1] if tiers else {})
    map_reduce_required = True
    total_product = max(1, rows) * max(1, estimated_labels)
    for tier in selectable_tiers:
        max_items = int(tier.get("max_items", rows or 1))
        max_labels = int(tier.get("max_labels", estimated_labels or 1))
        max_product = int(tier.get("max_item_label_product", max_items * max_labels))
        if estimated_labels <= max_labels and total_product <= max_product:
            selected = tier
            map_reduce_required = rows > max_items or estimated_labels > max_labels
            break

    estimated_facets = max(1, int(estimated_facets or 1))
    # v3 is per-facet only: tag exactly one facet per LLM call. The bundled-tagging
    # variant lives in skill-v4. We accept `facets_per_call` for back-compat and
    # silently force it to 1; the override is kept under `runtime.requested_facets_per_call_override`
    # for audit only.
    requested_facets_per_call = max(1, int(facets_per_call or 1))
    facets_per_call = 1

    # Pillar 3: explicit plan-space search. Enumerate (tier x ni x nl x cache_hit_rate),
    # filter by reliability + budget + envelope gates, pick min-cost survivor. If the
    # search returns nothing, fall back to the legacy first-fit selection above.
    constraints = _quality_constraints(recipe, budget_usd, wall_time_s)
    if disable_plan_search:
        # Ablation hook for E2.b: skip the search and pin the plan to the
        # legacy first-fit selection above. This isolates the contribution
        # of the plan-space search step itself.
        #
        # T12 (matrix v3.7): when all three --static-plan-* flags are passed,
        # the caller is asking for a *frozen* baseline plan (E3 "router oracle"
        # static arm). We record the requested triple here; the actual override
        # of `selected` / `chunk_size` / `label_chunk_size` happens just before
        # the effective_item_cap computation below so that all downstream uses
        # of `selected` (categorization, cost_model, ...) see the frozen tier.
        plan_search_result = {
            "enabled": False,
            "disabled": True,
            "selected": None,
            "reason": "plan_search_disabled_by_flag",
            "min_calibration_accuracy": None,
            "max_calibration_f2": None,
            "rank_by": None,
            "tiebreak_by": None,
            "log": [],
            "static_plan_request": {
                "tier": static_plan_tier,
                "ni": static_plan_ni,
                "nl": static_plan_nl,
            },
        }
    else:
        plan_search_result = _plan_space_search(
            rows=int(rows),
            estimated_labels=int(estimated_labels),
            estimated_facets=int(estimated_facets),
            facets_per_call=int(facets_per_call),
            recipe=recipe,
            text_stats=text_stats,
            categorization_strategy=categorization_strategy,
            constraints=constraints,
            concurrency=concurrency,
            cache_hit_rate_override=cache_hit_rate_override,
            host_model=host_model,
            host_pricing_key=host_pricing_key,
            allow_opt_in_tiers=list(allow_opt_in_set),
        )
    plan_selection_reason = "first_fit_legacy"
    plan_search_winner = plan_search_result.get("selected") if isinstance(plan_search_result, dict) else None
    if plan_search_winner:
        winner_tier_name = plan_search_winner.get("tier")
        for tier in selectable_tiers:
            if tier.get("name") == winner_tier_name:
                selected = tier
                map_reduce_required = rows > int(plan_search_winner.get("ni", rows)) or estimated_labels > int(plan_search_winner.get("nl", estimated_labels))
                plan_selection_reason = plan_search_result.get("reason") or "min_cost_under_reliability_floor"
                break

    # T12 (matrix v3.7): static-plan freeze override. Triggered only when the
    # caller passes ALL THREE of --static-plan-tier / --static-plan-ni /
    # --static-plan-nl together with --disable-plan-search. This forces the
    # planner to emit the requested (tier, n_items, n_labels) triple verbatim,
    # which is the static-baseline arm for E3 (router oracle vs frozen plan).
    static_plan_frozen = False
    static_plan_triple: dict[str, Any] | None = None
    if (
        disable_plan_search
        and static_plan_tier is not None
        and static_plan_ni is not None
        and static_plan_nl is not None
    ):
        forced_tier = next(
            (t for t in selectable_tiers if t.get("name") == static_plan_tier),
            None,
        )
        if forced_tier is None:
            raise ValueError(
                f"--static-plan-tier='{static_plan_tier}' not found in recipe "
                f"selectable tiers: {[t.get('name') for t in selectable_tiers]}"
            )
        if int(static_plan_ni) <= 0 or int(static_plan_nl) <= 0:
            raise ValueError(
                f"--static-plan-ni / --static-plan-nl must be >= 1; got "
                f"ni={static_plan_ni} nl={static_plan_nl}"
            )
        selected = forced_tier
        plan_selection_reason = "static_baseline_frozen"
        static_plan_frozen = True
        static_plan_triple = {
            "tier": str(static_plan_tier),
            "ni": int(static_plan_ni),
            "nl": int(static_plan_nl),
        }

    effective_item_cap = _effective_item_cap(selected, facets_per_call, recipe)
    if plan_search_winner:
        chunk_size = max(1, int(plan_search_winner.get("ni", min(rows, effective_item_cap) if rows else effective_item_cap)))
        label_chunk_size = max(1, int(plan_search_winner.get("nl", selected.get("max_labels", estimated_labels or 30))))
    else:
        chunk_size = min(rows, effective_item_cap) if rows else effective_item_cap
        label_chunk_size = int(selected.get("max_labels", estimated_labels or 30))
    if static_plan_frozen and static_plan_triple is not None:
        # T12: force chunk_size / label_chunk_size to the frozen triple AFTER
        # the legacy / plan-search defaults so all earlier branches stay intact.
        chunk_size = max(1, int(static_plan_triple["ni"]))
        label_chunk_size = max(1, int(static_plan_triple["nl"]))
        map_reduce_required = rows > chunk_size or estimated_labels > label_chunk_size
    payload_order = recipe.get("payload_order") or ["TextItems", "ColumnName", "UserQuery"]
    item_chunks = _chunk_summary(int(rows), int(chunk_size), "row")
    label_chunks = _chunk_summary(int(estimated_labels), int(label_chunk_size), "label")
    facet_bundles = _chunk_summary(int(estimated_facets), int(facets_per_call), "facet")
    tagging_map_reduce_required = bool(map_reduce_required or item_chunks["count"] > 1 or label_chunks["count"] > 1)
    categorization = _categorization_plan(rows, recipe, selected, text_stats, categorization_strategy)
    visual_preview = _visual_preview_plan(recipe)
    if plan_search_winner and plan_search_winner.get("cache_hit_rate") is not None:
        cache_rate = _clamp_rate(float(plan_search_winner["cache_hit_rate"]))
    else:
        cache_rate = _cache_hit_rate(selected, cache_hit_rate_override)
    cost_model = _estimate_cost_model(
        rows=int(rows),
        labels=int(estimated_labels),
        facets=int(estimated_facets),
        facets_per_call=int(facets_per_call),
        item_chunk_size=int(chunk_size),
        label_chunk_size=int(label_chunk_size),
        selected_tier=selected,
        categorization=categorization,
        recipe=recipe,
        text_stats=text_stats,
        cache_hit_rate=cache_rate,
        concurrency=concurrency,
        host_model=host_model,
        host_pricing_key=host_pricing_key,
    )
    prompt_template_order = ["system", *payload_order]
    calibration_model = selected.get("calibration_model") or selected.get("model")
    executor_model = host_model or calibration_model
    seed = {
        "rows": int(rows),
        "labels": int(estimated_labels),
        "facets": int(estimated_facets),
        "facets_per_call": int(facets_per_call),
        "tier": selected.get("name"),
        "executor_model": executor_model,
        "calibration_model": calibration_model,
        "chunk_size": int(chunk_size),
        "label_chunk_size": int(label_chunk_size),
        "payload_order": payload_order,
        "categorization": categorization,
    }
    plan = {
        "skill_version": SKILL_VERSION,
        "plan_id": _plan_id(seed),
        "recipe_source": recipe.get("_path"),
        "estimated_rows": int(rows),
        "estimated_labels": int(estimated_labels),
        "estimated_facets": int(estimated_facets),
        "tier": selected.get("name"),
        "model": executor_model,
        "calibration_model": calibration_model,
        "host_model_provided": bool(host_model),
        "chunk_size": int(chunk_size),
        "effective_item_cap": int(effective_item_cap),
        "label_chunk_size": int(label_chunk_size),
        "facets_per_call": int(facets_per_call),
        "payload_order": payload_order,
        "prompt_template_order": prompt_template_order,
        "map_reduce_required": tagging_map_reduce_required,
        "tagging_map_reduce_required": tagging_map_reduce_required,
        "tagging_reducer_prompt": "prompts/tagging_consolidation.md" if label_chunks["count"] > 1 else None,
        "categorization": categorization,
        "visual_preview": visual_preview,
        "reason": selected.get("notes", "Selected from calibrated recipe."),
        "blacklist": recipe.get("blacklist", []),
        "plan_space": {
            "model": [tier.get("calibration_model") or tier.get("model") for tier in tiers],
            "ni": sorted({int(tier.get("max_items", 0)) for tier in tiers if tier.get("max_items")}),
            "nl": sorted({int(tier.get("max_labels", 0)) for tier in tiers if tier.get("max_labels")}),
            "facets_per_call": [1],
            "item_chunking": [False, True],
            "label_chunking": [False, True],
            "retry_policy": ["full_chunk_retry_max_2_then_stop"],
            "payload_order": [payload_order],
        },
        "constraints": constraints,
        "operators": {
            "categorization": categorization,
            "tagging": {
                # v3 is per-facet only: always tag one facet at a time.
                "prompt": "prompts/tagging.md",
                "large_scale_prompt": "prompts/tagging_large_scale.md" if label_chunks["count"] > 1 else None,
                "item_chunking": item_chunks["count"] > 1,
                "label_chunking": label_chunks["count"] > 1,
                "facets_per_call": 1,
                "output_contract": "Results.Items keyed by original row index",
            },
            "label_consolidation": {
                "required": label_chunks["count"] > 1,
                "prompt": "prompts/tagging_consolidation.md" if label_chunks["count"] > 1 else None,
                "intermediate_shape": "{row_index: [{label_chunk, candidate_or_none, evidence?}]}",
                "weak_all_chunks_policy": "keep_json_null",
            },
            "merge": {
                "command": "python scripts/run_tapp.py merge --input <input_path> --workdir <workdir>",
                "strict_index_validation": True,
                "post_merge_row_mismatch_required": 0,
            },
            "visual_preview": {
                "required": bool(visual_preview.get("enabled")),
                "mode": visual_preview.get("mode"),
                "density": visual_preview.get("density"),
                "output_contract": "visual_preview_manifest.json plus fixed-resolution PNG pages; preview only, not tagging authority",
            },
        },
        "chunking": {
            "items": item_chunks,
            "labels": label_chunks,
            "facet_bundles": facet_bundles,
        },
        "map_reduce": {
            "required": tagging_map_reduce_required,
            "item_map_reduce": item_chunks["count"] > 1,
            "label_map_reduce": label_chunks["count"] > 1,
            "deterministic_item_reduce": "concat_then_strict_index_validation",
            "label_reduce": "strong_candidate_consolidation_with_null_preservation",
        },
        "cache": {
            "policy": selected.get("cache_policy"),
            "payload_order": payload_order,
            "prompt_template_order": prompt_template_order,
            "cache_hit_rate_assumption": cache_rate,
            "estimated_cached_tokens": cost_model["tokens"]["estimated_cached_tokens"],
            "estimated_cache_savings_usd": round(
                cost_model["tokens"]["estimated_cached_tokens"]
                * max(0.0, cost_model["pricing"]["input_per_mtok_usd"] - cost_model["pricing"]["cached_input_per_mtok_usd"])
                / 1_000_000,
                6,
            ),
        },
        "cost_model": cost_model,
        "constraint_status": _constraint_status(cost_model, constraints),
        "plan_search": {
            "enabled": bool(plan_search_result.get("enabled")),
            "disabled": bool(plan_search_result.get("disabled")),
            "selection_reason": plan_selection_reason,
            "min_calibration_accuracy": plan_search_result.get("min_calibration_accuracy"),
            "max_calibration_f2": plan_search_result.get("max_calibration_f2"),
            "selected_candidate": plan_search_result.get("selected"),
            "rank_by": plan_search_result.get("rank_by"),
            "tiebreak_by": plan_search_result.get("tiebreak_by"),
            "candidates": plan_search_result.get("log") or [],
        },
        "retry_policy": {
            "mode": "full_chunk_retry",
            "max_retries": 2,
            "row_level_fill_in": False,
            "expected_retries": cost_model["expected_full_chunk_retries"],
        },
        "runtime_metadata_template": {
            "skill_version": SKILL_VERSION,
            "plan_id": _plan_id(seed),
            "model": executor_model,
            "calibration_model": calibration_model,
            "host_model_provided": bool(host_model),
            "ni": int(chunk_size),
            "nl": int(label_chunk_size),
            "facets_per_call": 1,
            "requested_facets_per_call_override": int(requested_facets_per_call) if requested_facets_per_call != 1 else None,
            "payload_order": payload_order,
            "categorization_strategy": categorization.get("strategy"),
        },
    }
    compatibility_cfg = recipe.get("host_model_compatibility") or {}
    effective_policy = (
        host_model_policy
        or compatibility_cfg.get("policy_default")
        or "warn"
    )
    plan["host_model_compatibility"] = _host_model_compatibility(
        selected,
        host_model,
        recipe,
        effective_policy,
        extra_allowlist=host_model_allowlist,
    )
    return plan


def _inspect_payload(df: pd.DataFrame, args: argparse.Namespace, recipe: dict[str, Any]) -> dict[str, Any]:
    stats = _text_stats(df)
    plan = _recommend_plan(
        len(df),
        args.estimated_labels,
        recipe,
        stats,
        args.categorization_strategy,
        estimated_facets=getattr(args, "estimated_facets", 1),
        facets_per_call=getattr(args, "facets_per_call", 1),
        budget_usd=getattr(args, "budget_usd", None),
        wall_time_s=getattr(args, "wall_time_s", None),
        concurrency=getattr(args, "concurrency", 1),
        cache_hit_rate_override=getattr(args, "cache_hit_rate", None),
        host_model=getattr(args, "host_model", None),
        host_pricing_key=getattr(args, "host_pricing_key", None),
        allow_opt_in_tiers=getattr(args, "allow_opt_in_tiers", None) or [],
        host_model_allowlist=getattr(args, "host_model_allowlist", None) or [],
        host_model_policy=getattr(args, "host_model_policy", None),
    )
    text_col = _primary_text_col(stats, args.text_col)
    sample, sample_meta = _stratified_sample(df, text_col, args.sample_size)
    return {
        "path": args.input,
        "rows": int(len(df)),
        "columns": _schema(df),
        "text_stats": stats,
        "profile": _profile_dataframe(df, stats),
        "recommendation": plan,
        "sample_meta": sample_meta,
        "sample": sample,
    }


def cmd_inspect(args: argparse.Namespace) -> int:
    df = _read_table(args.input)
    recipe = _load_recipe(args.recipe)
    print(json.dumps(_inspect_payload(df, args, recipe), ensure_ascii=False, indent=2, default=str))
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    started_at = datetime.now(timezone.utc).isoformat()
    df = _read_table(args.input)
    recipe = _load_recipe(args.recipe)
    stats = _text_stats(df)
    plan = _recommend_plan(
        len(df),
        args.estimated_labels,
        recipe,
        stats,
        args.categorization_strategy,
        estimated_facets=args.estimated_facets,
        facets_per_call=args.facets_per_call,
        budget_usd=args.budget_usd,
        wall_time_s=args.wall_time_s,
        concurrency=args.concurrency,
        cache_hit_rate_override=args.cache_hit_rate,
        host_model=getattr(args, "host_model", None),
        host_pricing_key=getattr(args, "host_pricing_key", None),
        allow_opt_in_tiers=getattr(args, "allow_opt_in_tiers", None) or [],
        host_model_allowlist=getattr(args, "host_model_allowlist", None) or [],
        host_model_policy=getattr(args, "host_model_policy", None),
        disable_plan_search=bool(getattr(args, "disable_plan_search", False)),
        static_plan_tier=getattr(args, "static_plan_tier", None),
        static_plan_ni=getattr(args, "static_plan_ni", None),
        static_plan_nl=getattr(args, "static_plan_nl", None),
    )
    compatibility = plan.get("host_model_compatibility") or {}
    if compatibility.get("aborted"):
        print("STATUS: ERROR")
        for warning in compatibility.get("warnings", []):
            print(f"WARNING: {warning}")
        print("Plan aborted under host_model_policy='strict'. Pass --host-model-allowlist <name> or --host-model-policy warn to acknowledge the cross-model transfer.")
        print(json.dumps(compatibility, ensure_ascii=False, indent=2, default=str))
        return 1
    for warning in compatibility.get("warnings", []):
        print(f"WARNING: {warning}")
    created_at = datetime.now(timezone.utc).isoformat()
    plan["input"] = args.input
    plan["created_at"] = created_at
    plan["runtime_metadata_template"]["created_at"] = created_at
    out_path = Path(args.workdir) / "execution_plan.json"
    _write_json(out_path, plan)
    artifact_entry = _register_artifact(
        args.workdir,
        kind="execution_plan",
        path=out_path,
        extra={"plan_id": plan.get("plan_id"), "tier": plan.get("tier"), "model": plan.get("model")},
    )
    _record_trace(
        args.workdir,
        stage="plan",
        status="ok",
        model=plan.get("model"),
        plan_id=plan.get("plan_id"),
        input_refs=[args.input],
        output_refs=[artifact_entry["placeholder"]],
        started_at=started_at,
        extra={
            "plan_search_enabled": bool(plan.get("plan_search", {}).get("enabled")),
            "plan_search_selection_reason": plan.get("plan_search", {}).get("selection_reason"),
            "estimated_cost_usd": plan.get("cost_model", {}).get("estimated_cost_usd"),
        },
    )
    print("STATUS: SUCCESS")
    print(f"Output: {out_path}")
    print(f"Artifact: {artifact_entry['placeholder']}")
    print(json.dumps(plan, ensure_ascii=False, indent=2, default=str))
    return 0


# ---------------------------------------------------------------------------
# Normalization and coverage helpers
# ---------------------------------------------------------------------------


def _extract_vocab(description: str) -> list[str]:
    match = re.search(r"\{([^}]+)\}", description or "")
    if not match:
        return []
    return [token.strip() for token in match.group(1).split(",") if token.strip()]


def _label_has_compound_joiner(label: Any) -> bool:
    token = str(label or "").strip().lower()
    if not token:
        return False
    return any(joiner in token for joiner in (" or ", " and ", "/", "&", "|"))


def _is_multi_label(description: str) -> bool:
    return "multi_label" in (description or "").lower()


def _normalize_nulls(series: pd.Series) -> pd.Series:
    def fix(value: Any) -> Any:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        if isinstance(value, str) and value.strip().lower() in _NULL_STRINGS:
            return None
        return value
    return series.map(fix)


def _normalize_multilabel(series: pd.Series, description: str) -> pd.Series:
    vocab = set(_extract_vocab(description))

    def fix(value: Any) -> str | None:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        if isinstance(value, list):
            parts = [str(item).strip() for item in value]
        else:
            parts = [part.strip() for part in str(value).split("|")]
        parts = [part for part in parts if part]
        if vocab:
            parts = [part for part in parts if part in vocab]
        parts = sorted(set(parts))
        return "|".join(parts) if parts else None

    return series.map(fix)


def _apply_dtype(values: pd.Series, description: str) -> pd.Series:
    desc = (description or "").lower()
    if _is_multi_label(description):
        return _normalize_multilabel(values, description)
    if "ordinal" in desc or "numeric" in desc:
        return pd.to_numeric(values, errors="coerce")
    if "boolean" in desc:
        return values.astype("string").str.strip().str.lower().map({
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
            "1": True,
            "0": False,
            "unknown": None,
            "none": None,
            "null": None,
        })
    return values


def _enforce_closed_vocab(
    values: pd.Series,
    description: str,
) -> tuple[pd.Series, dict[str, Any]]:
    """Enforce closed vocabulary on categorical / ordinal / boolean specs.

    Returns the cleaned series plus a diagnostics dict with `vocab`, `oov_values`
    (the unique out-of-vocab values that were normalized to None), and counts.
    Multi-label is handled separately by `_normalize_multilabel`.
    """
    desc = (description or "").lower()
    diagnostics: dict[str, Any] = {
        "vocab_declared": False,
        "vocab": [],
        "oov_count": 0,
        "oov_values": [],
        "non_null_count": int(values.notna().sum()),
    }
    if _is_multi_label(description):
        # multi-label vocab is enforced inside _normalize_multilabel.
        return values, diagnostics

    declared_vocab = _extract_vocab(description)
    invalid_vocab = [token for token in declared_vocab if _label_has_compound_joiner(token)]
    raw_vocab = [token for token in declared_vocab if not _label_has_compound_joiner(token)]
    diagnostics["invalid_vocab_labels"] = invalid_vocab[:20]
    if declared_vocab and not raw_vocab:
        diagnostics["vocab_declared"] = True
        diagnostics["vocab"] = declared_vocab
        diagnostics["oov_count"] = int(values.notna().sum())
        diagnostics["oov_values"] = sorted({str(value) for value in values.dropna().unique()})[:20]
        return values.map(lambda _value: None), diagnostics
    if not raw_vocab:
        return values, diagnostics
    diagnostics["vocab_declared"] = True
    diagnostics["vocab"] = raw_vocab

    # Build a normalized lookup. Booleans normalize to {true, false, unknown}.
    if "boolean" in desc:
        accepted = {"true", "false"}
        if "judgment" in desc:
            accepted.add("unknown")

        def fix_bool(value: Any) -> Any:
            if value is None or (isinstance(value, float) and pd.isna(value)):
                return value
            token = str(value).strip().lower()
            if token in {"true"}:
                return True
            if token in {"false"}:
                return False
            if token == "unknown" and "unknown" in accepted:
                return None  # caller treats unknown as null share for judgment specs
            return "<<OOV>>"

        cleaned = values.map(fix_bool)
        oov_mask = cleaned == "<<OOV>>"
        oov_values = sorted({str(v) for v, m in zip(values, oov_mask) if bool(m)})
        cleaned = cleaned.map(lambda v: None if v == "<<OOV>>" else v)
        diagnostics["oov_count"] = int(oov_mask.sum())
        diagnostics["oov_values"] = oov_values[:20]
        return cleaned, diagnostics

    # Categorical / ordinal: case-insensitive match against declared vocab tokens.
    vocab_lookup: dict[str, str] = {}
    for token in raw_vocab:
        norm = str(token).strip().lower()
        if norm and norm not in vocab_lookup:
            vocab_lookup[norm] = str(token).strip()
    # Also accept the canonical noise members so legacy producers keep working.
    for noise in _NOISE_MEMBERS:
        vocab_lookup.setdefault(noise, noise)

    oov_seen: dict[str, int] = {}
    is_ordinal = "ordinal" in desc

    def _ordinal_norm_candidates(token: str) -> list[str]:
        try:
            numeric = float(token)
        except (TypeError, ValueError):
            return []
        if not math.isfinite(numeric):
            return []
        if numeric.is_integer():
            integer = int(numeric)
            return [str(integer), f"{integer}.0"]
        trimmed = (f"{numeric:.12f}").rstrip("0").rstrip(".")
        return [trimmed] if trimmed else []

    def fix(value: Any) -> Any:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return value
        token = str(value).strip()
        if not token:
            return None
        norm = token.lower()
        if norm in vocab_lookup:
            return vocab_lookup[norm]
        if is_ordinal:
            for candidate in _ordinal_norm_candidates(token):
                candidate_norm = candidate.lower()
                if candidate_norm in vocab_lookup:
                    return vocab_lookup[candidate_norm]
        oov_seen[token] = oov_seen.get(token, 0) + 1
        return None

    cleaned = values.map(fix)
    diagnostics["oov_count"] = int(sum(oov_seen.values()))
    diagnostics["oov_values"] = sorted(oov_seen.keys())[:20]
    return cleaned, diagnostics


def _uninformative_share(series: pd.Series) -> float:
    """Share of rows carrying no usable signal.

    Counts both abstention forms: NaN (JSON null / "None" / "" already collapsed
    by _normalize_nulls and _apply_dtype) and a literal noise member such as
    "Unknown" or "other" that a declared ValueSet kept as a real value.
    """
    if not len(series):
        return 0.0
    literal_noise = (
        series.astype("string").str.strip().str.lower().isin(_NOISE_MEMBERS).fillna(False)
    )
    return float((series.isna() | literal_noise).mean())


def _form_max_null_share(description: str, default: float = _DEFAULT_MAX_NULL_SHARE) -> tuple[float, str]:
    """Uninformative ceiling for a facet form, plus the form name for reporting.

    Sparsity means different things per form, so a single ceiling would either
    let sparse categorical facets through or discard ordinal/multi_label facets
    that are sparse by specification. A form listed in _FORM_MAX_NULL_SHARE keeps
    its own ceiling; ``default`` applies to the remaining forms (categorical and
    boolean), which is where an unbounded share of nulls previously went
    unchecked and where --max-null-share is meant to bite.
    """
    desc = (description or "").lower()
    for form, ceiling in _FORM_MAX_NULL_SHARE.items():
        if form in desc:
            return ceiling, form
    return default, "default"


def _passes_coverage(
    series: pd.Series,
    description: str,
    max_null_share: float = _DEFAULT_MAX_NULL_SHARE,
) -> tuple[bool, str]:
    desc = (description or "").lower()
    null_share = float(series.isna().mean())

    # Whole-table uninformative gate. This MUST run before the per-form branches
    # below, and it counts abstentions in BOTH forms they can take:
    #
    #   * JSON null / "None" / "" -> already collapsed to NaN by _normalize_nulls
    #     and _apply_dtype, so no literal test further down can see them (this is
    #     what made the old boolean-judgment `== "unknown"` branch unreachable).
    #   * a literal "Unknown" / "other" kept inside a declared ValueSet -> a real
    #     non-null value that isna() cannot see.
    #
    # Which form a sparse facet takes depends only on whether its spec declared
    # Unknown in the vocabulary, so gating one without the other lets half of the
    # sparse facets through. Both mean the same thing downstream: the row carries
    # no usable signal.
    #
    # The ceiling is per form: this gate replaces the multi_label / ordinal /
    # numeric coverage checks that used to sit below, which is why it carries
    # their thresholds rather than one flat value.
    ceiling, form = _form_max_null_share(description, max_null_share)
    uninformative_share = _uninformative_share(series)
    if uninformative_share > ceiling:
        return False, f"uninformative={uninformative_share:.0%} > {ceiling:.0%} [{form}] (null={null_share:.0%})"

    if "multi_label" in desc:
        return True, f"legacy multi_label coverage={1 - null_share:.0%}"
    if "ordinal" in desc:
        return True, f"ordinal mentioned={1 - null_share:.0%}"
    if "numeric" in desc:
        return True, f"numeric null={null_share:.0%}"
    if "boolean" in desc and "mention" in desc:
        cmp = (series.astype("string").str.lower() == "true").fillna(False)
        true_share = float(cmp.mean()) if len(cmp) else 0.0
        return 0.10 <= true_share <= 0.90, f"boolean-mention true={true_share:.0%}"
    if "categorical" in desc:
        non_null = series.dropna().astype(str)
        if non_null.empty:
            return False, "categorical empty"
        counts = non_null.value_counts(normalize=True)
        top_value = str(counts.index[0])
        top_share = float(counts.iloc[0])
        if top_share > 0.80:
            return False, f"categorical top={top_share:.0%} (=\"{top_value}\")"
        # A noise-member check used to live here, measured against non-null rows
        # only. The whole-table uninformative gate above now subsumes it: passing
        # that gate means null + noise <= max_null_share, so noise / (1 - null)
        # can never exceed max_null_share either. The gate is also strictly
        # broader, since it catches columns that mix nulls and literal Unknowns
        # in proportions neither check would have flagged on its own.
        return True, f"categorical top={top_share:.0%} (=\"{top_value}\")"
    return True, "unspecified"


def _has_low_coverage_signal(series: pd.Series) -> bool:
    non_null = series.dropna().astype(str).str.strip()
    non_null = non_null[non_null != ""]
    if non_null.empty:
        return False
    normalized = non_null.str.lower()
    return normalized.nunique(dropna=True) > 1


# ---------------------------------------------------------------------------
# Tag loading and strict validation
# ---------------------------------------------------------------------------


def _items_from_payload(payload: Any) -> Any:
    if isinstance(payload, dict) and isinstance(payload.get("Results"), dict):
        items = payload["Results"].get("Items")
        if items is not None:
            return items
    return payload


def _pairs_from_payload(payload: Any, offset: int) -> tuple[list[tuple[Any, Any]], int, str]:
    items = _items_from_payload(payload)
    if isinstance(items, list):
        return [(offset + idx, value) for idx, value in enumerate(items)], offset + len(items), "list"
    if isinstance(items, dict):
        pairs: list[tuple[Any, Any]] = []
        for key, value in items.items():
            token = str(key).strip()
            try:
                idx = int(token)
                pairs.append((idx, value))
            except ValueError:
                # Preserve malformed keys so strict-index validation can count/fail them.
                pairs.append((token, value))
        return pairs, offset, "dict"
    raise ValueError("tag payload must be a JSON array, Results.Items dict, or direct index dict")


def _load_tag_pairs(tags_dir: str, name: str) -> tuple[list[tuple[Any, Any]], dict[str, Any]]:
    diagnostics: dict[str, Any] = {"facet": name, "source_files": [], "payload_shapes": []}
    single_path = os.path.join(tags_dir, f"{name}.json")
    files = [single_path] if os.path.exists(single_path) else []
    if not files:
        files = sorted(glob.glob(os.path.join(tags_dir, f"{name}_chunk_*.json")))
        files.sort(key=lambda path: int(re.search(r"_chunk_(\d+)\.json$", path).group(1)) if re.search(r"_chunk_(\d+)\.json$", path) else -1)
    if not files:
        return [], {**diagnostics, "error": "missing_tag_file"}

    offset = 0
    pairs: list[tuple[Any, Any]] = []
    for path in files:
        with open(path, encoding="utf-8") as file:
            payload = json.load(file)
        file_pairs, offset, shape = _pairs_from_payload(payload, offset)
        pairs.extend(file_pairs)
        diagnostics["source_files"].append(path)
        diagnostics["payload_shapes"].append(shape)
    return pairs, diagnostics


def _validate_pairs(
    pairs: list[tuple[Any, Any]],
    row_count: int,
    *,
    allow_extra: bool = False,
    allow_duplicate: bool = False,
    allow_malformed: bool = False,
) -> tuple[list[Any] | None, dict[str, Any]]:
    """Strict-index integrity check on tag stage outputs.

    By default, ANY of {missing, extra, duplicate, malformed} pairs hard-fails the
    facet so the merge cannot silently drop or re-order rows. The `allow_*` flags
    exist for backwards compatibility and tests; production calls should keep all
    three false.
    """
    expected = set(range(row_count))
    seen: dict[int, Any] = {}
    duplicate: list[int] = []
    extra: list[int] = []
    malformed = 0
    for idx, value in pairs:
        if not isinstance(idx, int):
            malformed += 1
            continue
        if idx not in expected:
            extra.append(idx)
            continue
        if idx in seen:
            duplicate.append(idx)
            continue
        seen[idx] = value
    missing = sorted(expected - set(seen))
    extra_set = sorted(set(extra))
    duplicate_set = sorted(set(duplicate))
    failure_reasons: list[str] = []
    if missing:
        failure_reasons.append("missing")
    if extra_set and not allow_extra:
        failure_reasons.append("extra")
    if duplicate_set and not allow_duplicate:
        failure_reasons.append("duplicate")
    if malformed and not allow_malformed:
        failure_reasons.append("malformed")
    diagnostics = {
        "expected": row_count,
        "received_pairs": len(pairs),
        "unique_valid": len(seen),
        "missing": missing[:50],
        "missing_count": len(missing),
        "extra": extra_set[:50],
        "extra_count": len(extra_set),
        "duplicate": duplicate_set[:50],
        "duplicate_count": len(duplicate_set),
        "malformed_count": malformed,
        "complete": len(missing) == 0,
        "strict_index_pass": not failure_reasons,
        "strict_index_failure_reasons": failure_reasons,
        "strict_index_flags": {
            "allow_extra": bool(allow_extra),
            "allow_duplicate": bool(allow_duplicate),
            "allow_malformed": bool(allow_malformed),
        },
    }
    if failure_reasons:
        return None, diagnostics
    return [seen[idx] for idx in range(row_count)], diagnostics


def _runtime_counter(runtime: dict[str, Any], keys: list[str]) -> int | None:
    candidates: list[dict[str, Any]] = [runtime]
    for parent_key in ("metrics", "telemetry", "execution", "runtime"):
        child = runtime.get(parent_key)
        if isinstance(child, dict):
            candidates.append(child)
    for source in candidates:
        for key in keys:
            value = source.get(key)
            if value is not None:
                try:
                    return int(value)
                except (TypeError, ValueError):
                    continue
    return None


def _quality_metrics(validation_log: list[dict[str, Any]], runtime: dict[str, Any], row_count: int) -> dict[str, Any]:
    validation_entries = [item for item in validation_log if "expected" in item]
    total_expected = sum(int(item.get("expected", row_count)) for item in validation_entries)
    mismatch_total = sum(
        int(item.get("missing_count", 0))
        + int(item.get("extra_count", 0))
        + int(item.get("duplicate_count", 0))
        + int(item.get("malformed_count", 0))
        for item in validation_entries
    )
    mismatched_facets = sum(1 for item in validation_entries if not item.get("strict_index_pass", True))
    retry_count = _runtime_counter(runtime, ["full_chunk_retry_count", "chunk_retry_count", "retry_count"])
    chunk_attempts = _runtime_counter(runtime, ["full_chunk_attempt_count", "chunk_attempt_count", "chunk_attempts", "tagging_chunk_attempts"])
    fill_in_count = _runtime_counter(runtime, ["fill_in_count", "row_fill_in_count", "row_level_fill_in_count"])
    fill_in_denominator = _runtime_counter(runtime, ["expected_values", "tagged_value_count", "row_value_count"])
    if fill_in_denominator is None:
        fill_in_denominator = total_expected or row_count

    return {
        "index_mismatch_rate": float(mismatch_total / total_expected) if total_expected else 0.0,
        "index_mismatch_count": int(mismatch_total),
        "strict_index_mismatch_facet_rate": float(mismatched_facets / len(validation_entries)) if validation_entries else 0.0,
        "strict_index_mismatch_facets": int(mismatched_facets),
        "validated_facets": int(len(validation_entries)),
        "full_chunk_retry_rate": float(retry_count / chunk_attempts) if retry_count is not None and chunk_attempts else None,
        "full_chunk_retry_count": retry_count,
        "full_chunk_attempt_count": chunk_attempts,
        "fill_in_rate": float(fill_in_count / fill_in_denominator) if fill_in_count is not None and fill_in_denominator else 0.0,
        "fill_in_count": int(fill_in_count or 0),
        "fill_in_denominator": int(fill_in_denominator or 0),
        "fill_in_rate_source": "runtime_counter" if fill_in_count is not None else "default_no_row_level_fill_in_policy",
        "post_merge_row_mismatch": 0,
    }


def _slug(value: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z]+", "_", value.strip()).strip("_").lower()
    return slug or "value"


def _canonical_facet_key(name: str) -> str:
    """Normalize a facet name to a naming-style-invariant key so that columns
    differing only by casing/naming style (e.g. ``failure_pattern`` vs
    ``FailurePattern``) collapse to the same key. Splits camelCase/PascalCase
    boundaries, then lowercases to snake_case."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", str(name))
    spaced = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", spaced)
    return re.sub(r"[^0-9A-Za-z]+", "_", spaced).strip("_").lower() or "value"


def _expand_multihot(name: str, values: pd.Series, description: str) -> dict[str, pd.Series]:
    vocab = _extract_vocab(description)
    if not vocab:
        return {}
    result: dict[str, pd.Series] = {}
    split_values = values.map(lambda value: set(str(value).split("|")) if value else set())
    for label in vocab:
        col_name = f"{name}__{_slug(label)}"
        result[col_name] = split_values.map(lambda labels, target=label: target in labels)
    return result


def _load_execution_plan(workdir: str) -> dict[str, Any] | None:
    plan_path = os.path.join(workdir, "execution_plan.json")
    if not os.path.exists(plan_path):
        return None
    with open(plan_path, encoding="utf-8") as file:
        plan = json.load(file)
    plan.setdefault("_path", plan_path)
    return plan


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------


def cmd_merge(args: argparse.Namespace) -> int:
    workdir = os.path.abspath(args.workdir)
    specs_path = os.path.join(workdir, "specs.json")
    tags_dir = os.path.join(workdir, "tags")
    if not os.path.exists(specs_path):
        print("STATUS: ERROR")
        print(f"Missing {specs_path}. Complete categorization, review, and tagging first.")
        return 1

    with open(specs_path, encoding="utf-8") as file:
        specs_payload = json.load(file)
    specs = specs_payload.get("specs") or []
    if not specs:
        print("STATUS: ERROR")
        print("specs.json has empty `specs`. Nothing to merge.")
        return 1

    df = _read_table(args.input)
    recipe = _load_recipe(args.recipe)
    fallback_plan = _recommend_plan(len(df), args.estimated_labels, recipe)
    specs_runtime = specs_payload.get("runtime")
    execution_plan = _load_execution_plan(workdir)
    if specs_runtime and execution_plan:
        runtime = {**execution_plan, "runtime": specs_runtime, "specs_runtime": specs_runtime}
        for key, value in specs_runtime.items():
            if key not in runtime:
                runtime[key] = value
    else:
        runtime = specs_runtime or execution_plan or fallback_plan
    res_df = df.copy()
    kept: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    low_coverage_candidates: list[dict[str, Any]] = []
    low_coverage_fallback: list[dict[str, Any]] = []
    validation_log: list[dict[str, Any]] = []
    facet_report: list[dict[str, Any]] = []
    seen_canonical: dict[str, str] = {}

    for spec in specs:
        name = spec.get("name") or spec.get("Name")
        description = spec.get("description") or spec.get("Description") or ""
        if not name:
            dropped.append({"name": "<missing>", "reason": "missing spec name"})
            continue

        # Deterministic de-duplication: drop facets whose name is only a
        # casing/naming-style variant (or exact duplicate) of one already kept,
        # which would otherwise inflate the redundancy penalty downstream.
        canonical = _canonical_facet_key(name)
        if canonical in seen_canonical:
            dropped.append({"name": name, "reason": f"duplicate_facet_name: same canonical '{canonical}' as '{seen_canonical[canonical]}'"})
            facet_report.append({"name": name, "reason": "duplicate_facet_name", "dropped": True, "canonical": canonical, "kept_as": seen_canonical[canonical]})
            continue
        seen_canonical[canonical] = name

        pairs, load_diag = _load_tag_pairs(tags_dir, name)
        if load_diag.get("error"):
            dropped.append({"name": name, "reason": load_diag["error"]})
            validation_log.append(load_diag)
            facet_report.append({"name": name, "reason": load_diag["error"], "dropped": True})
            continue

        raw_values, validate_diag = _validate_pairs(
            pairs,
            len(df),
            allow_extra=bool(getattr(args, "allow_extra_indices", False)),
            allow_duplicate=bool(getattr(args, "allow_duplicate_indices", False)),
            allow_malformed=bool(getattr(args, "allow_malformed_indices", False)),
        )
        validate_diag.update(load_diag)
        validation_log.append(validate_diag)
        if raw_values is None:
            failure_reasons = validate_diag.get("strict_index_failure_reasons") or ["missing"]
            dropped.append({
                "name": name,
                "reason": "strict_index_mismatch:" + ",".join(failure_reasons),
                "diagnostics": validate_diag,
            })
            facet_report.append({
                "name": name,
                "reason": "strict_index_mismatch",
                "dropped": True,
                "failure_reasons": failure_reasons,
                "missing_count": validate_diag.get("missing_count", 0),
                "extra_count": validate_diag.get("extra_count", 0),
                "duplicate_count": validate_diag.get("duplicate_count", 0),
                "malformed_count": validate_diag.get("malformed_count", 0),
            })
            continue

        values = _apply_dtype(_normalize_nulls(pd.Series(raw_values)), description)

        # Closed-vocab enforcement for categorical / ordinal / boolean.
        # Multi-label vocabs are enforced by _normalize_multilabel; numeric specs
        # have no closed vocab.
        vocab_diag = {"vocab_declared": False, "vocab": [], "oov_count": 0, "oov_values": []}
        if not _is_multi_label(description) and "numeric" not in (description or "").lower():
            values, vocab_diag = _enforce_closed_vocab(values, description)
        non_null_for_oov = max(1, vocab_diag.get("non_null_count", 0))
        oov_rate = float(vocab_diag.get("oov_count", 0)) / float(non_null_for_oov)
        validate_diag.update({
            "vocab_declared": vocab_diag.get("vocab_declared", False),
            "oov_count": int(vocab_diag.get("oov_count", 0)),
            "oov_rate": round(oov_rate, 4),
            "oov_values": vocab_diag.get("oov_values", []),
        })
        if (
            vocab_diag.get("vocab_declared")
            and args.max_oov_rate is not None
            and oov_rate > float(args.max_oov_rate)
        ):
            dropped.append({
                "name": name,
                "reason": f"oov_rate {oov_rate:.3f} > {float(args.max_oov_rate):.3f}",
                "diagnostics": {
                    "oov_count": vocab_diag["oov_count"],
                    "oov_values": vocab_diag["oov_values"],
                    "vocab": vocab_diag["vocab"],
                },
            })
            facet_report.append({
                "name": name,
                "dropped": True,
                "reason": "closed_vocab_violation",
                "oov_rate": oov_rate,
                "oov_count": vocab_diag["oov_count"],
                "vocab": vocab_diag["vocab"],
            })
            continue

        if _is_multi_label(description) and not args.legacy_multilabel_cell:
            expanded = _expand_multihot(name, values, description)
            if not expanded:
                dropped.append({"name": name, "reason": "multi_label_without_vocab"})
                continue
            for col_name, col_values in expanded.items():
                true_share = float(col_values.mean()) if len(col_values) else 0.0
                res_df[col_name] = col_values
                kept.append({"name": col_name, "source": name, "reason": f"multi_hot true={true_share:.0%}"})
                facet_report.append({"name": col_name, "source": name, "coverage": true_share, "dropped": False})
            continue

        ok, coverage_reason = _passes_coverage(
            values,
            description,
            max_null_share=float(getattr(args, "max_null_share", _DEFAULT_MAX_NULL_SHARE)),
        )
        if not ok:
            if _has_low_coverage_signal(values):
                low_coverage_candidates.append({"name": name, "values": values, "reason": coverage_reason})
            dropped.append({"name": name, "reason": coverage_reason})
            facet_report.append({"name": name, "coverage_reason": coverage_reason, "dropped": True})
            continue

        res_df[name] = values
        kept_entry: dict[str, Any] = {
            "name": name,
            "reason": coverage_reason,
        }
        kept.append(kept_entry)
        facet_report.append({
            "name": name,
            "coverage_reason": coverage_reason,
            "dropped": False,
        })

    if not kept and bool(getattr(args, "allow_low_coverage_fallback", False)) and low_coverage_candidates:
        limit = max(1, int(getattr(args, "low_coverage_fallback_limit", 2) or 2))
        # Tightening the coverage gate makes this rescue path fire more often, so
        # it needs its own floor. Use the same uninformative definition as
        # _passes_coverage: rescuing a column that is almost entirely null or
        # Unknown only turns an empty table into a useless one.
        eligible = [
            candidate for candidate in low_coverage_candidates
            if _uninformative_share(candidate["values"]) <= _FALLBACK_MAX_NULL_SHARE
        ]
        fallback_names: set[str] = set()
        for candidate in eligible[:limit]:
            name = str(candidate["name"])
            res_df[name] = candidate["values"]
            reason = f"low_coverage_fallback: {candidate['reason']}"
            kept.append({"name": name, "reason": reason})
            low_coverage_fallback.append({"name": name, "reason": candidate["reason"]})
            fallback_names.add(name)
        if fallback_names:
            dropped = [item for item in dropped if str(item.get("name")) not in fallback_names]
            for item in facet_report:
                if str(item.get("name")) in fallback_names:
                    item["dropped"] = False
                    item["coverage_reason"] = "low_coverage_fallback: " + str(item.get("coverage_reason") or "")
                    item["low_coverage_fallback"] = True

    if len(res_df) != len(df):
        print("STATUS: ERROR")
        print(f"Row count changed: input={len(df)}, output={len(res_df)}")
        return 1

    out_path, loader = _emit_dataframe(res_df, workdir, args.output)
    facet_report_path = os.path.join(workdir, "facet_report.json")
    report_path = os.path.join(workdir, "merge_report.json")
    benchmark_metrics = _quality_metrics(validation_log, runtime, len(df))
    facet_report_payload: dict[str, Any] = {
        "items": facet_report,
        "benchmark_metrics": benchmark_metrics,
    }
    _write_json(facet_report_path, facet_report_payload)
    merge_report_payload: dict[str, Any] = {
        "status": "success",
        "skill_version": SKILL_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input": args.input,
        "output": out_path,
        "rows": len(res_df),
        "runtime": runtime,
        "kept": kept,
        "dropped": dropped,
        "low_coverage_fallback": low_coverage_fallback,
        "validation": validation_log,
        "benchmark_metrics": benchmark_metrics,
        "facet_report": facet_report_path,
        "post_merge_row_mismatch": int(len(res_df) != len(df)),
    }
    _write_json(report_path, merge_report_payload)

    augmented_artifact = _register_artifact(workdir, kind="augmented_table", path=out_path, extra={"rows": int(len(res_df))})
    facet_artifact = _register_artifact(workdir, kind="facet_report", path=facet_report_path, extra={"items": int(len(facet_report))})
    report_artifact = _register_artifact(workdir, kind="merge_report", path=report_path, extra={"kept": int(len(kept)), "dropped": int(len(dropped))})
    _record_trace(
        workdir,
        stage="merge",
        status="ok",
        model=(execution_plan or {}).get("model") if isinstance(execution_plan, dict) else None,
        plan_id=(execution_plan or {}).get("plan_id") if isinstance(execution_plan, dict) else None,
        input_refs=[args.input],
        output_refs=[augmented_artifact["placeholder"], report_artifact["placeholder"], facet_artifact["placeholder"]],
        extra={
            "kept": int(len(kept)),
            "dropped": int(len(dropped)),
            "low_coverage_fallback": int(len(low_coverage_fallback)),
            "post_merge_row_mismatch": int(len(res_df) != len(df)),
        },
    )

    new_cols = [col for col in res_df.columns if col not in df.columns]
    print("STATUS: SUCCESS")
    print(f"Output: {out_path}")
    if not args.output:
        print(f"(no --output given; load with {loader}(...))")
    print(f"Rows: {len(res_df)}")
    print(f"New columns ({len(new_cols)}): {new_cols}")
    print(f"Merge report: {report_path}")
    print(f"Facet report: {facet_report_path}")
    print(f"Artifacts: {augmented_artifact['placeholder']} | {report_artifact['placeholder']} | {facet_artifact['placeholder']}")
    _print_df_preview(res_df, new_cols)
    if kept:
        print("Kept:")
        for item in kept:
            print(f"  + {item['name']} ({item.get('reason')})")
    if dropped:
        print("Dropped:")
        for item in dropped:
            print(f"  - {item['name']} ({item.get('reason')})")
    return 0


# ---------------------------------------------------------------------------
# OOS / forced-fit reporting
# ---------------------------------------------------------------------------


def _expected_oos_map(path: str | None) -> dict[str, set[int]]:
    if not path:
        return {}
    with open(path, encoding="utf-8") as file:
        payload = json.load(file)
    if isinstance(payload, dict) and isinstance(payload.get("facets"), dict):
        payload = payload["facets"]
    result: dict[str, set[int]] = {}
    if isinstance(payload, dict):
        for facet, value in payload.items():
            if isinstance(facet, str) and facet.startswith("_"):
                continue  # skip metadata / annotation keys (e.g. _doc, _in_vocab_gold)
            if isinstance(value, dict):
                indices = value.get("oos_indices") or value.get("expected_null_indices") or value.get("indices") or []
            else:
                indices = value
            result[str(facet)] = {int(idx) for idx in indices}
        return result
    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            facet = item.get("facet") or item.get("name")
            idx = item.get("index")
            if facet is not None and idx is not None:
                result.setdefault(str(facet), set()).add(int(idx))
    return result


def _is_abstention(value: Any, description: str) -> bool:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return True
    if isinstance(value, str) and value.strip().lower() in _NULL_STRINGS | {"unknown"}:
        return True
    desc = (description or "").lower()
    if "boolean mention" in desc and value is False:
        return True
    return False


def _is_forced_fit(value: Any, description: str) -> bool:
    if _is_abstention(value, description):
        return False
    desc = (description or "").lower()
    if "boolean" in desc:
        return bool(value) is True
    return True


def cmd_oos_report(args: argparse.Namespace) -> int:
    workdir = os.path.abspath(args.workdir)
    specs_path = os.path.join(workdir, "specs.json")
    tags_dir = os.path.join(workdir, "tags")
    if not os.path.exists(specs_path):
        print("STATUS: ERROR")
        print(f"Missing {specs_path}. Complete tagging before OOS reporting.")
        return 1

    df = _read_table(args.input)
    with open(specs_path, encoding="utf-8") as file:
        specs_payload = json.load(file)
    expected_oos = _expected_oos_map(args.expected_oos)

    facet_reports: list[dict[str, Any]] = []
    forced_fit_count = 0
    total_oos_cases = 0
    for spec in specs_payload.get("specs") or []:
        name = spec.get("name") or spec.get("Name")
        description = spec.get("description") or spec.get("Description") or ""
        if not name:
            continue
        pairs, load_diag = _load_tag_pairs(tags_dir, name)
        if load_diag.get("error"):
            facet_reports.append({"name": name, "status": load_diag["error"]})
            continue
        raw_values, validate_diag = _validate_pairs(
            pairs,
            len(df),
            allow_extra=bool(getattr(args, "allow_extra_indices", False)),
            allow_duplicate=bool(getattr(args, "allow_duplicate_indices", False)),
            allow_malformed=bool(getattr(args, "allow_malformed_indices", False)),
        )
        if raw_values is None:
            facet_reports.append({"name": name, "status": "strict_index_mismatch", "validation": validate_diag})
            continue

        values = _apply_dtype(_normalize_nulls(pd.Series(raw_values)), description)
        vocab = set(_extract_vocab(description))
        non_abstain = int(sum(not _is_abstention(value, description) for value in values))
        out_of_vocab = 0
        if vocab:
            for value in values:
                if _is_abstention(value, description):
                    continue
                if str(value) not in vocab and not isinstance(value, bool):
                    out_of_vocab += 1

        oos_indices = expected_oos.get(str(name), set())
        facet_forced = 0
        for idx in oos_indices:
            if 0 <= idx < len(values) and _is_forced_fit(values.iloc[idx], description):
                facet_forced += 1
        forced_fit_count += facet_forced
        total_oos_cases += len(oos_indices)
        facet_reports.append({
            "name": name,
            "status": "ok",
            "rows": len(values),
            "assignment_rate": float(non_abstain / len(values)) if len(values) else 0.0,
            "abstention_rate": float(1 - (non_abstain / len(values))) if len(values) else 0.0,
            "out_of_vocab_rate": float(out_of_vocab / len(values)) if len(values) else 0.0,
            "expected_oos_cases": len(oos_indices),
            "forced_fit_count": facet_forced,
            "forced_fit_rate": float(facet_forced / len(oos_indices)) if oos_indices else None,
        })

    report = {
        "status": "ok",
        "skill_version": SKILL_VERSION,
        "runner_format": "justin_like_oos_summary_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input": args.input,
        "workdir": workdir,
        "expected_oos": args.expected_oos,
        "metrics": {
            "forced_fit_rate": float(forced_fit_count / total_oos_cases) if total_oos_cases else None,
            "forced_fit_count": forced_fit_count,
            "total_oos_cases": total_oos_cases,
        },
        "facets": facet_reports,
    }
    out_path = args.output or os.path.join(workdir, "oos_report.json")
    _write_json(out_path, report)
    oos_artifact = _register_artifact(
        workdir,
        kind="oos_report",
        path=out_path,
        extra={"forced_fit_rate": report["metrics"].get("forced_fit_rate"), "facets": int(len(facet_reports))},
    )
    _record_trace(
        workdir,
        stage="oos_report",
        status="ok",
        input_refs=[args.input] + ([args.expected_oos] if args.expected_oos else []),
        output_refs=[oos_artifact["placeholder"]],
        extra={"metrics": report["metrics"]},
    )
    print("STATUS: SUCCESS")
    print(f"Output: {out_path}")
    print(f"Artifact: {oos_artifact['placeholder']}")
    print(json.dumps(report["metrics"], ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Pillar 4.B / 4.C: artifact + trace CLI commands
# ---------------------------------------------------------------------------


def cmd_record_artifact(args: argparse.Namespace) -> int:
    if not os.path.exists(args.path):
        print("STATUS: ERROR")
        print(f"Path does not exist: {args.path}")
        return 1
    extra: dict[str, Any] = {}
    if args.note:
        extra["note"] = args.note
    if args.stage:
        extra["stage"] = args.stage
    entry = _register_artifact(args.workdir, kind=args.kind, path=args.path, extra=extra or None)
    print("STATUS: SUCCESS")
    print(f"Placeholder: {entry['placeholder']}")
    print(json.dumps(entry, ensure_ascii=False, indent=2, default=str))
    return 0


def _verify_artifact_entry(workdir: str | Path, entry: dict[str, Any]) -> dict[str, Any]:
    """Recompute sha256 of the artifact file and compare against the manifest entry.

    Pillar 4.B: closes the gap where `resolve` would happily return a placeholder
    even when the underlying file had been mutated since registration. Returns a
    dict with `verified` (bool), `manifest_sha256`, `current_sha256`, `path` and an
    `error` field when the file cannot be opened.
    """
    target = Path(entry.get("abs_path") or "")
    if not target.exists():
        target = Path(workdir) / entry.get("path", "")
    expected = str(entry.get("sha256") or "").lower()
    try:
        actual = _sha256_file(target).lower()
    except FileNotFoundError as exc:
        return {
            "verified": False,
            "manifest_sha256": expected,
            "current_sha256": None,
            "path": str(target),
            "error": f"missing_file: {exc}",
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "verified": False,
            "manifest_sha256": expected,
            "current_sha256": None,
            "path": str(target),
            "error": f"hash_failed: {exc}",
        }
    return {
        "verified": expected == actual,
        "manifest_sha256": expected,
        "current_sha256": actual,
        "path": str(target),
    }


def cmd_resolve(args: argparse.Namespace) -> int:
    entry = _resolve_artifact_ref(args.workdir, args.ref)
    if entry is None:
        print("STATUS: ERROR")
        print(f"No artifact in {args.workdir} matches {args.ref!r}.")
        return 1
    skip_verify = bool(getattr(args, "no_verify", False))
    verification: dict[str, Any] | None = None
    if not skip_verify:
        verification = _verify_artifact_entry(args.workdir, entry)
        entry = {**entry, "verification": verification}
        if not verification.get("verified"):
            print("STATUS: ERROR")
            print(
                "Artifact integrity check failed. Manifest sha256 != current sha256. "
                "Re-run record-artifact for the latest file or pass --no-verify to skip."
            )
            print(json.dumps(entry, ensure_ascii=False, indent=2, default=str))
            return 1
    if args.read:
        target = Path(entry.get("abs_path") or "")
        if not target.exists():
            target = Path(args.workdir) / entry.get("path", "")
        try:
            with open(target, encoding="utf-8") as handle:
                contents = handle.read()
        except Exception as exc:
            print("STATUS: ERROR")
            print(f"Cannot read artifact at {target}: {exc}")
            return 1
        print("STATUS: SUCCESS")
        print(f"Placeholder: {entry['placeholder']}")
        print(f"Path: {target}")
        if verification is not None:
            print(f"Integrity: verified sha256={verification['current_sha256']}")
        print("--- BEGIN CONTENT ---")
        print(contents)
        print("--- END CONTENT ---")
        return 0
    print("STATUS: SUCCESS")
    print(json.dumps(entry, ensure_ascii=False, indent=2, default=str))
    return 0


def cmd_record_trace(args: argparse.Namespace) -> int:
    extra: dict[str, Any] = {}
    if args.tier:
        extra["tier"] = args.tier
    if args.notes:
        extra["notes"] = args.notes
    payload = _record_trace(
        args.workdir,
        stage=args.stage,
        status=args.status,
        model=args.model,
        plan_id=args.plan_id,
        input_refs=args.input_ref or None,
        output_refs=args.output_ref or None,
        started_at=args.started_at,
        finished_at=args.finished_at,
        latency_ms=args.latency_ms,
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        reasoning_summary=args.reasoning_summary,
        extra=extra or None,
    )
    print("STATUS: SUCCESS")
    print(f"Placeholder: {payload['placeholder']}")
    print(f"Path: {payload['trace_path']}")
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    return 0


# ---------------------------------------------------------------------------
# Pillar 4: audit-traces (cross-check execution_plan.json against persisted traces)
# ---------------------------------------------------------------------------


def _expected_stages_for_plan(plan: dict[str, Any]) -> list[str]:
    """Derive the minimum stage set that `audit-traces` should enforce.

    Categorization stage names are canonicalized to the trace contract names
    (`categorize_*`) even if the recipe/plan stores map-reduce aliases such as
    `chunk_proposal` and `global_consolidation`.
    """
    expected: list[str] = ["plan"]
    cat = plan.get("categorization") or {}
    strategy = (plan.get("strategy") or cat.get("strategy") or "").lower()

    stage_aliases = {
        "chunk_proposal": "categorize_proposal",
        "global_consolidation": "categorize_consolidation",
        "final_selection": "categorize_final_selection",
    }

    if strategy == "map_reduce":
        stages = cat.get("stages") or [
            "categorize_proposal",
            "categorize_consolidation",
            "categorize_final_selection",
        ]
        for stage in stages:
            token = str(stage).strip().lower()
            expected.append(stage_aliases.get(token, token))
    else:
        expected.append("categorize")

    expected.append("review")
    expected.append("tag")

    operators = plan.get("operators") if isinstance(plan.get("operators"), dict) else {}
    label_consolidation = operators.get("label_consolidation") if isinstance(operators, dict) else {}
    needs_tag_consolidation = bool(plan.get("tag_consolidation_enabled"))
    if isinstance(label_consolidation, dict):
        needs_tag_consolidation = needs_tag_consolidation or bool(label_consolidation.get("required"))
    if needs_tag_consolidation:
        expected.append("tag_consolidation")

    expected.append("merge")
    seen: set[str] = set()
    deduped: list[str] = []
    for stage in expected:
        if stage in seen:
            continue
        seen.add(stage)
        deduped.append(stage)
    return deduped


def cmd_audit_traces(args: argparse.Namespace) -> int:
    workdir = Path(args.workdir)
    plan_path = workdir / "execution_plan.json"
    plan: dict[str, Any] = {}
    if plan_path.exists():
        try:
            with open(plan_path, encoding="utf-8") as handle:
                plan = json.load(handle)
        except Exception as exc:
            print("STATUS: ERROR")
            print(f"Cannot parse {plan_path}: {exc}")
            return 1

    expected_stages: list[str] = list(args.expect or []) or _expected_stages_for_plan(plan)
    manifest = _load_artifact_manifest(workdir)
    trace_keys = manifest.get("by_kind", {}).get("trace", []) or []
    by_stage: dict[str, list[dict[str, Any]]] = {}
    integrity_failures: list[dict[str, Any]] = []
    for key in trace_keys:
        entry = manifest.get("artifacts", {}).get(key)
        if not entry:
            continue
        stage = str(entry.get("stage") or "<unknown>")
        by_stage.setdefault(stage, []).append(entry)
        if not bool(getattr(args, "no_verify", False)):
            verification = _verify_artifact_entry(workdir, entry)
            if not verification.get("verified"):
                integrity_failures.append({
                    "stage": stage,
                    "trace_id": entry.get("trace_id"),
                    "placeholder": entry.get("placeholder"),
                    "verification": verification,
                })

    missing_stages = [stage for stage in expected_stages if stage not in by_stage]
    extra_stages = [stage for stage in by_stage.keys() if stage not in expected_stages]
    summary = {
        "workdir": str(workdir.resolve()),
        "plan_id": plan.get("plan_id"),
        "categorization_strategy": (plan.get("strategy") or (plan.get("categorization") or {}).get("strategy")),
        "expected_stages": expected_stages,
        "stages_with_traces": sorted(by_stage.keys()),
        "missing_stages": missing_stages,
        "extra_stages": extra_stages,
        "trace_count_by_stage": {stage: len(items) for stage, items in by_stage.items()},
        "integrity_failures": integrity_failures,
        "verification_skipped": bool(getattr(args, "no_verify", False)),
    }
    pass_audit = not missing_stages and not integrity_failures
    print("STATUS: SUCCESS" if pass_audit else "STATUS: ERROR")
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    return 0 if pass_audit else 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def _cmd_augment_e2e(args: argparse.Namespace) -> int:
    from host_executor import cmd_augment_e2e

    return cmd_augment_e2e(args)


def main() -> int:
    parser = argparse.ArgumentParser(prog="run_tapp_V10")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_inspect = sub.add_parser("inspect", help="Print schema, text profile, and recipe recommendation.")
    p_inspect.add_argument("input")
    p_inspect.add_argument("--recipe", default=None)
    p_inspect.add_argument("--estimated-labels", type=int, default=30)
    p_inspect.add_argument("--estimated-facets", type=int, default=1)
    p_inspect.add_argument(
        "--facets-per-call",
        type=int,
        default=1,
        help="DEPRECATED in v3. v3 always tags one facet per call (facets_per_call = 1). For bundled tagging use skill-v4. Value is recorded under runtime.requested_facets_per_call_override for audit only.",
    )
    p_inspect.add_argument("--budget-usd", type=float, default=None)
    p_inspect.add_argument("--wall-time-s", type=float, default=None)
    p_inspect.add_argument("--concurrency", type=int, default=1)
    p_inspect.add_argument("--cache-hit-rate", type=float, default=None, help="Override recipe cache-hit assumption for cost planning.")
    p_inspect.add_argument("--host-model", default=None, help="Actual executor model (e.g., claude-opus-4-7). Recorded in runtime metadata and used to look up pricing.")
    p_inspect.add_argument("--host-pricing-key", default=None, help="Optional pricing-table key override. Defaults to --host-model when unset.")
    p_inspect.add_argument("--sample-size", type=int, default=100)
    p_inspect.add_argument("--text-col", default=None, help="Text column used for short/medium/long stratified sampling. Defaults to the primary text-heavy column.")
    p_inspect.add_argument("--categorization-strategy", choices=["auto", "single_pass", "map_reduce"], default="auto")
    p_inspect.add_argument(
        "--allow-opt-in-tiers",
        action="append",
        default=None,
        help="Repeatable. Pillar 3.A: allow plan-space search to consider tiers marked opt_in_only in model_recipe.json. Used by Section 5.5 planner-vs-static comparisons.",
    )
    p_inspect.add_argument(
        "--host-model-allowlist",
        action="append",
        default=None,
        help="Repeatable. Pillar 3.A: extend the selected tier's host_model_allowlist for this run; treats the listed host_model as peer-class (calibration assumed transferable).",
    )
    p_inspect.add_argument(
        "--host-model-policy",
        choices=["warn", "strict", "off"],
        default=None,
        help="Pillar 3.A: policy when --host-model is neither the selected tier's calibration_model nor in the allowlist. 'warn' (default) records the warning in execution_plan and proceeds; 'strict' aborts; 'off' suppresses the check.",
    )
    p_inspect.set_defaults(func=cmd_inspect)

    p_plan = sub.add_parser("plan", help="Write execution_plan.json from the calibrated model recipe.")
    p_plan.add_argument("--input", required=True)
    p_plan.add_argument("--workdir", required=True)
    p_plan.add_argument("--recipe", default=None)
    p_plan.add_argument("--estimated-labels", type=int, default=30)
    p_plan.add_argument("--estimated-facets", type=int, default=1)
    p_plan.add_argument(
        "--facets-per-call",
        type=int,
        default=1,
        help="DEPRECATED in v3. v3 always tags one facet per call (facets_per_call = 1). For bundled tagging use skill-v4. Value is recorded under runtime.requested_facets_per_call_override for audit only.",
    )
    p_plan.add_argument("--budget-usd", type=float, default=None)
    p_plan.add_argument("--wall-time-s", type=float, default=None)
    p_plan.add_argument("--concurrency", type=int, default=1)
    p_plan.add_argument("--cache-hit-rate", type=float, default=None, help="Override recipe cache-hit assumption for cost planning.")
    p_plan.add_argument("--host-model", default=None, help="Actual executor model (e.g., claude-opus-4-7). Recorded in runtime metadata and used to look up pricing.")
    p_plan.add_argument("--host-pricing-key", default=None, help="Optional pricing-table key override. Defaults to --host-model when unset.")
    p_plan.add_argument("--categorization-strategy", choices=["auto", "single_pass", "map_reduce"], default="auto")
    p_plan.add_argument(
        "--allow-opt-in-tiers",
        action="append",
        default=None,
        help="Repeatable. Pillar 3.A: allow plan-space search to consider tiers marked opt_in_only in model_recipe.json. Used by Section 5.5 planner-vs-static comparisons.",
    )
    p_plan.add_argument(
        "--host-model-allowlist",
        action="append",
        default=None,
        help="Repeatable. Pillar 3.A: extend the selected tier's host_model_allowlist for this run; treats the listed host_model as peer-class (calibration assumed transferable).",
    )
    p_plan.add_argument(
        "--host-model-policy",
        choices=["warn", "strict", "off"],
        default=None,
        help="Pillar 3.A: policy when --host-model is neither the selected tier's calibration_model nor in the allowlist. 'warn' (default) records the warning in execution_plan and proceeds; 'strict' aborts the plan; 'off' suppresses the check.",
    )
    p_plan.add_argument(
        "--disable-plan-search",
        action="store_true",
        default=False,
        help="Ablation (E2.b): skip the plan-space search and pin the plan to the legacy first-fit tier selection. The resulting execution_plan.json carries plan_search.disabled=true.",
    )
    p_plan.add_argument(
        "--static-plan-tier",
        default=None,
        help="T12 / E3 static baseline arm: force selected tier to this name. Must be used together with --disable-plan-search, --static-plan-ni and --static-plan-nl; otherwise the flag is ignored.",
    )
    p_plan.add_argument(
        "--static-plan-ni",
        type=int,
        default=None,
        help="T12 / E3 static baseline arm: force chunk_size (n_items per LLM call). Required with --static-plan-tier and --static-plan-nl.",
    )
    p_plan.add_argument(
        "--static-plan-nl",
        type=int,
        default=None,
        help="T12 / E3 static baseline arm: force label_chunk_size (n_labels per LLM call). Required with --static-plan-tier and --static-plan-ni.",
    )
    p_plan.set_defaults(func=cmd_plan)

    p_aug = sub.add_parser(
        "augment-e2e",
        help="Run TA++ v10 plan -> query contract -> visual preview -> categorize -> review -> tag -> merge inside the skill-owned executor.",
    )
    p_aug.add_argument("--input", required=True)
    p_aug.add_argument("--workdir", required=True)
    p_aug.add_argument("--query", required=True)
    p_aug.add_argument(
        "--query-contract-json",
        default=None,
        help="Optional JSON object from the query registry. v10 uses it as the task contract for schema planning.",
    )
    p_aug.add_argument("--model", required=True, help="Actual host/executor model passed to Claude CLI --model.")
    p_aug.add_argument("--output", default=None, help="Output augmented table path. Defaults to <workdir>/augment.<output-format>.")
    p_aug.add_argument("--output-format", choices=("xlsx", "csv", "parquet"), default="xlsx")
    p_aug.add_argument(
        "--workers",
        type=int,
        default=0,
        help="Optional explicit host-decided workers for LLM categorize/tag stages. 0 lets v10 decide from --max-workers.",
    )
    p_aug.add_argument(
        "--max-workers",
        type=int,
        default=0,
        help="Maximum worker budget. Used by v10 when --workers is 0.",
    )
    p_aug.add_argument("--attempts", type=int, default=2, help="Retry budget for each JSON-producing LLM stage.")
    p_aug.add_argument("--force", action="store_true", help="Delete and recreate workdir before running.")
    p_aug.add_argument(
        "--categorize-chunk-size",
        type=int,
        default=0,
        help="Optional host-model execution decision for categorization proposal rows. 0 uses the v10 recipe/profile default.",
    )
    p_aug.add_argument(
        "--tag-chunk-size",
        type=int,
        default=0,
        help="Optional host-model execution decision for tag rows. 0 uses the v10 recipe/profile default.",
    )
    p_aug.add_argument(
        "--execution-decision-note",
        default=None,
        help="Short host-model rationale for any explicit workers/chunk choices. Recorded in execution_plan.json#skill_v10_host_execution.",
    )
    p_aug.add_argument("--estimated-labels", type=int, default=30)
    p_aug.add_argument("--estimated-facets", type=int, default=3)
    p_aug.add_argument("--categorization-strategy", choices=["auto", "single_pass", "map_reduce"], default="auto")
    p_aug.add_argument("--claude-timeout", type=int, default=900, help="Per Claude CLI call timeout in seconds.")
    p_aug.add_argument(
        "--max-null-share",
        type=float,
        default=_DEFAULT_MAX_NULL_SHARE,
        help="Pass through to merge. Whole-table null gate applied to every facet form.",
    )
    p_aug.add_argument(
        "--allow-low-coverage-fallback",
        action="store_true",
        help="Pass through to merge so runs can keep a small number of otherwise valid low-coverage facets.",
    )
    p_aug.set_defaults(func=_cmd_augment_e2e)

    p_merge = sub.add_parser("merge", help="Strictly validate tags, apply gates, and write augmented output.")
    p_merge.add_argument("--input", required=True)
    p_merge.add_argument("--workdir", required=True)
    p_merge.add_argument("--output", default=None)
    p_merge.add_argument("--recipe", default=None)
    p_merge.add_argument("--estimated-labels", type=int, default=30)
    p_merge.add_argument(
        "--max-oov-rate",
        type=float,
        default=0.0,
        help="Closed-vocab gate. For specs that declare a vocabulary like 'categorical {a, b, c}', any value outside the vocab is normalized to None and counted. If the OOV rate (oov_count / non_null_count) exceeds this threshold, the facet is dropped. Set to a value greater than 1.0 to effectively disable.",
    )
    p_merge.add_argument(
        "--max-null-share",
        type=float,
        default=_DEFAULT_MAX_NULL_SHARE,
        help="Whole-table null gate. A facet whose values are more than this share NaN is dropped, counting JSON null, 'Unknown', 'None' and empty cells alike. Applies to every facet form before the per-form concentration checks. Set to a value greater than 1.0 to effectively disable.",
    )
    p_merge.add_argument(
        "--allow-extra-indices",
        action="store_true",
        help="Strict-index opt-out: do NOT hard-fail when tag pairs include row indices outside the input range. Default is to fail the facet.",
    )
    p_merge.add_argument(
        "--allow-duplicate-indices",
        action="store_true",
        help="Strict-index opt-out: do NOT hard-fail when tag pairs include duplicate row indices. Default is to fail the facet.",
    )
    p_merge.add_argument(
        "--allow-malformed-indices",
        action="store_true",
        help="Strict-index opt-out: do NOT hard-fail when tag pairs include malformed (non-int) indices. Default is to fail the facet.",
    )
    p_merge.add_argument(
        "--allow-low-coverage-fallback",
        action="store_true",
        help="If all otherwise valid facets are dropped only by coverage gates, keep a small number of low-coverage facets so the augmented table remains usable. The merge report records the fallback.",
    )
    p_merge.add_argument(
        "--low-coverage-fallback-limit",
        type=int,
        default=2,
        help="Maximum number of low-coverage facets to keep when --allow-low-coverage-fallback is enabled.",
    )
    p_merge.add_argument("--legacy-multilabel-cell", action="store_true", help="Keep v1/v2 pipe-joined multi-label columns instead of expanding to multi-hot booleans.")
    p_merge.set_defaults(func=cmd_merge)

    p_oos = sub.add_parser("oos-report", help="Compute OOS abstention and forced-fit metrics from tag outputs.")
    p_oos.add_argument("--input", required=True)
    p_oos.add_argument("--workdir", required=True)
    p_oos.add_argument("--expected-oos", default=None, help="Optional JSON mapping facets to OOS row indices. Without it, forced_fit_rate is null and abstention/out-of-vocab rates are still reported.")
    p_oos.add_argument("--output", default=None, help="Optional output path. Defaults to <workdir>/oos_report.json.")
    p_oos.add_argument(
        "--allow-extra-indices",
        action="store_true",
        help="Mirror of merge --allow-extra-indices for OOS reporting on imperfect tag outputs.",
    )
    p_oos.add_argument(
        "--allow-duplicate-indices",
        action="store_true",
        help="Mirror of merge --allow-duplicate-indices for OOS reporting on imperfect tag outputs.",
    )
    p_oos.add_argument(
        "--allow-malformed-indices",
        action="store_true",
        help="Mirror of merge --allow-malformed-indices for OOS reporting on imperfect tag outputs.",
    )
    p_oos.set_defaults(func=cmd_oos_report)

    p_record = sub.add_parser(
        "record-artifact",
        help="Pillar 4.B: register a workdir file in artifact_manifest.json with sha256 + content-addressed placeholder.",
    )
    p_record.add_argument("--workdir", required=True)
    p_record.add_argument("--kind", required=True, help="Stable label, e.g., specs, tags, review_notes.")
    p_record.add_argument("--path", required=True, help="Path to the artifact file (must already exist).")
    p_record.add_argument("--stage", default=None, help="Optional stage label (e.g., categorize, review, tag, consolidation).")
    p_record.add_argument("--note", default=None, help="Optional free-form note recorded in the manifest entry.")
    p_record.set_defaults(func=cmd_record_artifact)

    p_resolve = sub.add_parser(
        "resolve",
        help="Pillar 4.B: resolve a `<<artifact:<kind>@sha256:<short>>>` reference against artifact_manifest.json.",
    )
    p_resolve.add_argument("--workdir", required=True)
    p_resolve.add_argument("--ref", required=True, help="Placeholder string such as <<artifact:specs@sha256:abc123>>.")
    p_resolve.add_argument("--read", action="store_true", help="Print the artifact contents in addition to the manifest entry.")
    p_resolve.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip Pillar 4.B integrity check (re-hash the file and compare against the manifest sha256). Default re-verifies on every resolve.",
    )
    p_resolve.set_defaults(func=cmd_resolve)

    p_trace = sub.add_parser(
        "record-trace",
        help="Pillar 4.C: persist a per-stage subagent reasoning trace as a content-addressed JSON artifact.",
    )
    p_trace.add_argument("--workdir", required=True)
    p_trace.add_argument("--stage", required=True, help="Stage name (e.g., categorize_proposal, categorize_consolidation, review, tag, tag_consolidation).")
    p_trace.add_argument("--status", default="ok", help="Stage status (ok / partial / failed / aborted).")
    p_trace.add_argument("--model", default=None, help="Executor model used for the stage (e.g., claude-opus-4-7).")
    p_trace.add_argument("--tier", default=None, help="Calibration tier name from model_recipe.json that the stage emulated.")
    p_trace.add_argument("--plan-id", default=None, help="execution_plan.json#plan_id this stage was bound to.")
    p_trace.add_argument("--input-ref", action="append", default=None, help="Repeatable. Placeholder reference for an input artifact.")
    p_trace.add_argument("--output-ref", action="append", default=None, help="Repeatable. Placeholder reference for an output artifact.")
    p_trace.add_argument("--started-at", default=None, help="ISO-8601 timestamp the stage started, if known.")
    p_trace.add_argument("--finished-at", default=None, help="ISO-8601 timestamp the stage finished. Defaults to now().")
    p_trace.add_argument("--latency-ms", type=float, default=None, help="Stage latency in milliseconds.")
    p_trace.add_argument("--input-tokens", type=int, default=None, help="Reported input token count.")
    p_trace.add_argument("--output-tokens", type=int, default=None, help="Reported output token count.")
    p_trace.add_argument("--reasoning-summary", default=None, help="Short subagent reasoning summary (host-LLM authored). Persisted as part of the trace.")
    p_trace.add_argument("--notes", default=None, help="Optional free-form notes for follow-up debugging.")
    p_trace.set_defaults(func=cmd_record_trace)

    p_audit = sub.add_parser(
        "audit-traces",
        help="Pillar 4: cross-check execution_plan.json against persisted traces and report missing stages or sha256 drift.",
    )
    p_audit.add_argument("--workdir", required=True)
    p_audit.add_argument(
        "--expect",
        action="append",
        default=None,
        help="Repeatable. Override the expected stage list (otherwise derived from execution_plan.json).",
    )
    p_audit.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip Pillar 4.B sha256 re-verification on each trace artifact.",
    )
    p_audit.set_defaults(func=cmd_audit_traces)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
