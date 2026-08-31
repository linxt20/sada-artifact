# -*- coding: utf-8 -*-
"""Grounding 三分类逐行判定核心模块。
chunk=20 行一次调用; payload 每行带 row_index; 严格校验返回行对齐。
判官走 scorer/semantic_reference_recall.py 的 _invoke_judge (OpenAI 兼容端点)。"""
from __future__ import annotations
import json, sys, os
from pathlib import Path

# Artifact note: the sibling `scorer/` directory shipped here is tried first so
# the import resolves from a fresh checkout; the original absolute path is kept
# as the fallback so the as-run resolution order stays visible.
sys.path.insert(0, "/mnt/data/benchmark_quick/scorer")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scorer"))
import semantic_reference_recall as srr  # _invoke_judge/_read_table/_extract_json_object/_read_json

VERDICTS = {"SUPPORTED", "INFERABLE", "HALLUCINATED"}
MAX_SRC_CHARS = 8000

SYSTEM = """You audit AI-generated augmented columns of a data table, ROW BY ROW.
Each augmented value was produced by a model that read the row's original data (mostly free text plus some structured columns). For EACH augmented (column,value) on EACH row, decide whether the value is grounded in THAT ROW's original data:

- SUPPORTED: the value has a direct, literal basis in the row's original text/structured columns.
- INFERABLE: no literal basis, but the value can be inferred from SPECIFIC WORDS/PHRASES in THIS ROW's original text. The inference chain MUST be anchored to the row's actual content — NOT world knowledge, NOT guessing beyond the text.
- HALLUCINATED: the value contradicts the row's original data, or the row contains nothing that supports it.

Judge each row independently using ONLY that row's original data. Be strict: if the only support is generic world knowledge not tied to this row's words, it is HALLUCINATED, not INFERABLE.

You are given a BATCH of rows. For EVERY row_index in the input you MUST return exactly one entry, with a verdict for EVERY augmented column given for that row. Output STRICT JSON ONLY:
{"rows":[{"row_index":<int>,"verdicts":[{"column":"<name>","verdict":"SUPPORTED|INFERABLE|HALLUCINATED","evidence":"<short phrase from the row's original data, or why hallucinated>"}]}]}
Return the SAME number of rows as the input, same row_index values. No prose outside the JSON."""


def _clip(v):
    s = "" if v is None else str(v)
    if len(s) > MAX_SRC_CHARS:
        s = s[:MAX_SRC_CHARS] + "...[clip]"
    return s


def is_empty(v):
    import pandas as pd
    if v is None:
        return True
    try:
        if pd.isna(v):
            return True
    except (ValueError, TypeError):
        pass
    return str(v).strip() == ""


def build_prompt(goal, src_cols, rows_payload):
    """rows_payload: [{"row_index":N,"source_row":{...},"augmented_values":[{"column","value"}]}]"""
    body = {
        "analytical_goal": goal,
        "source_columns": src_cols,
        "rows": rows_payload,
    }
    return SYSTEM + "\n\n== BATCH ==\n" + json.dumps(body, ensure_ascii=False)


def parse_response(parsed, expected_indices, expected_cols_per_row):
    """严格对齐校验。返回 (ok, result_map, err)。
    result_map: {row_index: {column: {"verdict","evidence"}}}"""
    if not isinstance(parsed, dict) or "rows" not in parsed:
        return False, {}, "no_rows_key"
    out = {}
    got = set()
    for r in parsed.get("rows", []):
        if not isinstance(r, dict):
            continue
        ri = r.get("row_index")
        if ri not in expected_indices:
            continue
        got.add(ri)
        vmap = {}
        for v in r.get("verdicts", []):
            if not isinstance(v, dict):
                continue
            col = v.get("column")
            verd = v.get("verdict")
            if col is None:
                continue
            if verd not in VERDICTS:
                verd = "PARSE_ERROR"
            vmap[str(col)] = {"verdict": verd, "evidence": str(v.get("evidence", ""))[:300]}
        out[ri] = vmap
    missing_rows = set(expected_indices) - got
    if missing_rows:
        return False, out, "missing_rows:%d" % len(missing_rows)
    # 逐行补齐漏列
    for ri in expected_indices:
        for col in expected_cols_per_row.get(ri, []):
            if col not in out.get(ri, {}):
                out.setdefault(ri, {})[col] = {"verdict": "MISSING_IN_RESPONSE", "evidence": ""}
    return True, out, None


def judge_chunk(model, goal, src_cols, rows_payload, timeout_s=600, attempts=3, log_path=None):
    """对一个 chunk (<=20行) 调一次判官, 返回 (ok, result_map, err)。"""
    expected_indices = [r["row_index"] for r in rows_payload]
    expected_cols = {r["row_index"]: [a["column"] for a in r["augmented_values"]] for r in rows_payload}
    prompt = build_prompt(goal, src_cols, rows_payload)
    try:
        parsed = srr._invoke_judge(prompt, model=model, timeout_s=timeout_s, attempts=attempts, log_path=log_path)
    except Exception as e:
        return False, {}, "judge_error:%s" % str(e)[:120]
    return parse_response(parsed, expected_indices, expected_cols)
