# -*- coding: utf-8 -*-
"""augment_table 的 grounding 评测运行器。
复用 scorer_grounding/_g_judge.py 的判定 prompt 与解析, 但适配 augment_table 目录布局
(无 meta.json; 场景=<dataset>/<scenario>/; 源表=original.csv; query 取自 query.md)。

单判官全量 pass, 断点续跑, 缓存写 grounding_eval/_cache/<ds>/<sc>/<variant>/<judge>.jsonl。
"""
from __future__ import annotations
import argparse, csv, glob, json, os, random, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

csv.field_size_limit(10 ** 9)
BASE = Path(__file__).resolve().parent
REPO = BASE.parent
sys.path.insert(0, str(REPO / "scorer"))
sys.path.insert(0, str(REPO / "scorer_grounding"))
import _g_judge as gj  # noqa: E402

ROOT = REPO / "augment_table"
CACHE = BASE / "_cache"
# Artifact note: this ran with `queries.json` beside the script. The artifact
# keeps one copy of that data at 5_reference/configs/grounding_queries.json
# (byte-equivalent content, 108 units); the original sibling path wins if present.
_QUERY_PATHS = (
    BASE / "queries.json",
    BASE.parents[2] / "5_reference" / "configs" / "grounding_queries.json",
)
_query_file = next((p for p in _QUERY_PATHS if p.exists()), _QUERY_PATHS[0])
QUERIES = json.loads(_query_file.read_text(encoding="utf-8"))

JUDGES = {"haiku": "claude-haiku-4-5-20251001", "sonnet": "claude-sonnet-4-6", "opus": "claude-opus-4.8"}
VARIANTS = {
    "haiku__skill_off_update": ("haiku", "skill_off_update"),
    "sonnet__skill_off_update": ("sonnet", "skill_off_update"),
    "haiku__skill_on-v11": ("haiku", "skill_on"),
    "sonnet__skill_on-v11": ("sonnet", "skill_on"),
    "haiku__skill_on_e2e-v11": ("haiku", "skill_on_e2e"),
    "sonnet__skill_on_e2e-v11": ("sonnet", "skill_on_e2e"),
}
CHUNK = 10


def read_csv(path):
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        r = csv.reader(f)
        hdr = next(r)
        return hdr, list(r)


def load_unit(dataset, scenario, variant):
    sd = ROOT / dataset / scenario
    ohdr, orows = read_csv(sd / "original.csv")
    ahdr, arows = read_csv(sd / (variant + ".csv"))
    oset = set(ohdr)
    aug_cols = [c for c in ahdr if c not in oset]
    aidx = {c: ahdr.index(c) for c in aug_cols}
    oidx = {c: ohdr.index(c) for c in ohdr}
    return ohdr, orows, oidx, arows, aidx, aug_cols


def sample_indices(n, limit, seed):
    """确定性采样: 行数<=limit 取全量, 否则等距抽样(覆盖全表, 避免只取表头段)。"""
    if not limit or n <= limit:
        return list(range(n))
    step = n / limit
    return sorted({int(i * step) for i in range(limit)})


def build_payload(orows, oidx, arows, aidx, aug_cols, ohdr, idxs):
    payload = []
    for i in idxs:
        if i >= len(arows):
            continue
        arow = arows[i]
        srow = {}
        if i < len(orows):
            orow = orows[i]
            srow = {c: gj._clip(orow[oidx[c]]) if oidx[c] < len(orow) else "" for c in ohdr}
        avals = []
        for c in aug_cols:
            j = aidx[c]
            v = arow[j] if j < len(arow) else None
            if gj.is_empty(v):
                continue
            avals.append({"column": c, "value": gj._clip(v)})
        if avals:
            payload.append({"row_index": int(i), "source_row": srow, "augmented_values": avals})
    return payload


def process_unit(dataset, scenario, variant, judge_key, limit, seed, chunk_jobs, log_calls):
    key = "%s/%s" % (dataset, scenario)
    goal = QUERIES.get(key, {}).get("query", "")
    cdir = CACHE / dataset / scenario / variant
    cdir.mkdir(parents=True, exist_ok=True)
    cache_path = cdir / ("%s.jsonl" % judge_key)
    logdir = cdir / "calls"
    if log_calls:
        logdir.mkdir(exist_ok=True)
    try:
        ohdr, orows, oidx, arows, aidx, aug_cols = load_unit(dataset, scenario, variant)
    except Exception as e:
        return "LOAD_ERR:%s" % str(e)[:60]
    if not aug_cols:
        return "NO_AUG_COLS"

    idxs = sample_indices(len(arows), limit, seed)
    done = set()
    if cache_path.exists():
        for line in cache_path.open(encoding="utf-8"):
            try:
                done.add(json.loads(line)["row_index"])
            except Exception:
                pass
    todo = [i for i in idxs if i not in done]
    if not todo:
        return "DONE(cached %d)" % len(done)
    chunks = [todo[k:k + CHUNK] for k in range(0, len(todo), CHUNK)]

    def work(ci):
        payload = build_payload(orows, oidx, arows, aidx, aug_cols, ohdr, ci)
        if not payload:
            return [(i, {}) for i in ci]
        lp = (logdir / ("%s_%d.json" % (judge_key, ci[0]))) if log_calls else (logdir / "last.json")
        lp.parent.mkdir(parents=True, exist_ok=True)
        ok, rmap, err = gj.judge_chunk(judge_key and JUDGES[judge_key], goal, ohdr, payload, log_path=lp)
        if not ok and len(payload) > 1:
            merged = dict(rmap)
            for p in payload:
                ok1, rmap1, _ = gj.judge_chunk(JUDGES[judge_key], goal, ohdr, [p], log_path=lp)
                if ok1:
                    merged.update(rmap1)
                else:
                    merged[p["row_index"]] = {a["column"]: {"verdict": "JUDGE_ERROR", "evidence": ""}
                                              for a in p["augmented_values"]}
            rmap = merged
        return [(i, rmap.get(i, {})) for i in ci]

    written = 0
    with cache_path.open("a", encoding="utf-8") as cf:
        with ThreadPoolExecutor(max_workers=chunk_jobs) as ex:
            futs = [ex.submit(work, c) for c in chunks]
            for f in as_completed(futs):
                try:
                    res = f.result()
                except Exception as e:
                    print("   chunk fail: %s" % str(e)[:80], flush=True)
                    continue
                for i, vmap in res:
                    cf.write(json.dumps({"row_index": i, "verdicts": vmap}, ensure_ascii=False) + "\n")
                    written += 1
                cf.flush()
    return "DONE(%d rows)" % written


def discover(only_dataset, only_scenario, only_variant):
    units = []
    for p in sorted(glob.glob(str(ROOT / "*" / "*" / "original.csv"))):
        sd = Path(p).parent
        ds, sc = sd.parent.name, sd.name
        if only_dataset and ds != only_dataset:
            continue
        if only_scenario and sc != only_scenario:
            continue
        for v in VARIANTS:
            if only_variant and v != only_variant:
                continue
            if (sd / (v + ".csv")).exists():
                units.append((ds, sc, v))
    return units


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", required=True, choices=list(JUDGES))
    ap.add_argument("--limit-rows", type=int, default=30, help="每(场景,变体)判定行数; 0=全量")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--unit-jobs", type=int, default=6)
    ap.add_argument("--chunk-jobs", type=int, default=4)
    ap.add_argument("--dataset", default=None)
    ap.add_argument("--scenario", default=None)
    ap.add_argument("--variant", default=None)
    ap.add_argument("--limit-units", type=int, default=0)
    ap.add_argument("--log-calls", action="store_true")
    a = ap.parse_args()

    units = discover(a.dataset, a.scenario, a.variant)
    if a.limit_units:
        units = units[:a.limit_units]
    print("judge=%s units=%d rows/unit<=%d conc=%d" % (
        a.judge, len(units), a.limit_rows, a.unit_jobs * a.chunk_jobs), flush=True)
    n = 0
    with ThreadPoolExecutor(max_workers=a.unit_jobs) as ex:
        futs = {ex.submit(process_unit, ds, sc, v, a.judge, a.limit_rows, a.seed,
                          a.chunk_jobs, a.log_calls): (ds, sc, v) for ds, sc, v in units}
        for f in as_completed(futs):
            ds, sc, v = futs[f]
            n += 1
            try:
                st = f.result()
            except Exception as e:
                st = "ERR:%s" % str(e)[:60]
            print("[%d/%d] %-22s %s/%s/%s" % (n, len(units), st, ds, sc, v), flush=True)
    print("PASS_DONE judge=%s" % a.judge, flush=True)


if __name__ == "__main__":
    main()
