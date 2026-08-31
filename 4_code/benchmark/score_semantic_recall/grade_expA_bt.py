# -*- coding: utf-8 -*-
"""实验A A-1: 5指标 pairwise + BT, 适配新布局 analysis_report/<dataset>/<query>/<model>__<variant>.md
复用 grader_v3 的 prompt/judge_pairwise/BT; 仅改 I/O。产物独立写入 expA_bt_out/, 不覆盖旧产物。
goal 取自 manifest 的真实 query 文本; 记录 query_subtype 供按 6 类 FOI 分层聚合。"""
import os, sys, json, glob, time
from pathlib import Path
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grader_v3 as grader


def wj(path, data):
    grader.write_json(Path(path), data)

ROOT = "/mnt/data/benchmark/analysis_report"
OUT = "/mnt/data/benchmark/expA_bt_out"
MANIFEST = "/mnt/data/benchmark/analysis_report/manifest.json"
JUDGE = "claude-opus-4.8-xhigh"
VARIANTS = ["original", "skill_off", "skill_on", "skill_on_e2e"]
FILEVAR = {"original": "original", "skill_off": "skill_off",
           "skill_on": "skill_on-v11", "skill_on_e2e": "skill_on_e2e-v11"}


def _load_goalmap():
    m = {}
    try:
        d = json.load(open(MANIFEST, encoding="utf-8"))
        for e in d.get("reports", []):
            m[(e["dataset"], e["scenario"], e["prefix"])] = (e.get("query") or "", e.get("query_subtype") or "")
    except Exception:
        pass
    return m


GOALMAP = _load_goalmap()


def find_claude():
    return "/root/.local/bin/claude"


def units():
    us = []
    for qdir in sorted(glob.glob(ROOT + "/*/*/")):
        parts = qdir.rstrip("/").split("/")
        dataset, query = parts[-2], parts[-1]
        for model in ("haiku", "sonnet"):
            reports = {}
            for v in VARIANTS:
                f = os.path.join(qdir, "%s__%s.md" % (model, FILEVAR[v]))
                if os.path.exists(f):
                    reports[v] = open(f, encoding="utf-8", errors="replace").read()
            avail = [v for v in VARIANTS if v in reports]
            if len(avail) >= 2:
                g, sub = GOALMAP.get((dataset, query, model), ("", ""))
                us.append({"dataset": dataset, "query": query, "model": model,
                           "uid": "%s__%s__%s" % (dataset, query, model),
                           "goal": g or ("%s / %s" % (dataset, query)),
                           "subtype": sub, "reports": reports, "available": avail})
    return us


def pk_path(udir, a, b, swap):
    return os.path.join(udir, "_pk_%s__%s__swap%d.json" % (a, b, int(swap)))


def run_pair(claude_exe, u, udir, a, b, swap):
    p = pk_path(udir, a, b, swap)
    if os.path.exists(p) and os.path.getsize(p) > 2:
        try:
            if json.load(open(p)).get("judge_model") == JUDGE:
                return
        except Exception:
            pass
    var_a, var_b = (b, a) if swap else (a, b)
    r = grader.judge_pairwise(claude_exe, u["goal"], u["reports"][var_a], u["reports"][var_b],
                              timeout_s=420, model=JUDGE, fallback_model=None, max_attempts=3)
    o = grader.PKOutcome(var_a=var_a, var_b=var_b, swap=swap, raw_winner=r.get("winner", "TIE"),
                         margin=r.get("margin", "small"), ok=bool(r.get("ok")),
                         scores_a=r.get("scores_a"), scores_b=r.get("scores_b"),
                         dimension_decisions=r.get("dimension_decisions") or {},
                         evidence_refs=r.get("evidence_refs") or {"A": [], "B": []},
                         augmented_column_refs=r.get("augmented_column_refs") or {"A": [], "B": []},
                         confidence=r.get("confidence"), reason=r.get("reason"),
                         validation_warnings=r.get("validation_warnings") or [])
    d = o.to_dict(drop_empty=False)
    d["judge_rc"] = r.get("rc")
    d["judge_model"] = JUDGE
    wj(p, d)


def assemble(u, udir):
    outs = []
    for a, b in combinations(u["available"], 2):
        for swap in (False, True):
            p = pk_path(udir, a, b, swap)
            if os.path.exists(p):
                try:
                    outs.append(grader.PKOutcome.from_dict(json.load(open(p))))
                except Exception:
                    pass
    if not outs:
        return
    wj(os.path.join(udir, "pairwise_4way.json"), [o.to_dict(drop_empty=False) for o in outs])
    bt = grader.compute_bt_payload(u["uid"], outs, items=u["available"])
    wj(os.path.join(udir, "bt_4way.json"), bt)
    wj(os.path.join(udir, "meta.json"),
                      {"dataset": u["dataset"], "query": u["query"], "model": u["model"],
                       "available": u["available"], "subtype": u.get("subtype"),
                       "goal": u["goal"], "judge_model": JUDGE})


def do_unit(u):
    ce = find_claude()
    udir = os.path.join(OUT, u["uid"])
    os.makedirs(udir, exist_ok=True)
    for a, b in combinations(u["available"], 2):
        for swap in (False, True):
            try:
                run_pair(ce, u, udir, a, b, swap)
            except Exception as e:
                wj(pk_path(udir, a, b, swap), {"ok": False, "err": str(e)[:120], "judge_model": JUDGE})
    assemble(u, udir)
    return u["uid"]


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    us = units()
    if a.limit:
        us = us[:a.limit]
    print("units:", len(us), "judgments total:", len(us) * 12, flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(do_unit, u): u for u in us}
        for f in as_completed(futs):
            f.result()
            done += 1
            if done % 5 == 0:
                print("units done %d/%d" % (done, len(us)), flush=True)
    print("ALL_BT_DONE", flush=True)


if __name__ == "__main__":
    main()
