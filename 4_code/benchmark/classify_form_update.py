# -*- coding: utf-8 -*-
"""实验A 第6指标: 分析形态分类 (C1/C2/C3), update 布局.
输入: analysis_report_update/<model>/<dataset>/<query>/<variant>.md
输出: analysis_result_update/form_class/<dataset>/<ds>__<query>__<model>__<variant>.json
复用 classify_form_expA.py 的 PROMPT/judge/三分类逻辑, 仅改 I/O。"""
import os, json, glob, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = "/mnt/data/benchmark/analysis_report_update"
OUT = "/mnt/data/benchmark/analysis_result_update/form_class"
CLAUDE = shutil.which("claude") or "/root/.local/bin/claude"
MODEL = "claude-opus-4.8-xhigh"

# 报告文件名(去 .md) -> 规范变体名
VARMAP = {
    "original": "original",
    "skill_off_update": "skill_off",
    "skill_on_v11_update": "skill_on",
    "skill_on_e2e_v11_update": "skill_on_e2e",
}

PROMPT = """You are classifying the ANALYTICAL FORM of a data-analysis report. The report analyzes a table that has both TEXT columns and NUMERIC columns, answering an analytical goal.

Classify the report into EXACTLY ONE of three categories by HOW it treats text vs numeric signal:

- C1_all_qualitative: the report is essentially qualitative; little or no quantitative computation (few/no numbers, rates, group means, correlations). Conclusions are descriptive.
- C2_text_qual_numeric_quant: the report does QUANTITATIVE analysis on the ORIGINAL numeric columns, but treats the TEXT columns only QUALITATIVELY (mentions/among themes, no structured quantification of text-derived signal).
- C3_text_augmented_quant: the report QUANTIFIES signal DERIVED FROM TEXT (i.e. text is turned into structured/categorical/numeric features and then used in quantitative analysis: group rates, comparisons, model over text-derived columns), AND also quantifies numeric columns.

Key distinction C2 vs C3: does the report compute quantitative results OVER SIGNAL EXTRACTED FROM TEXT (C3), or does it only quantify pre-existing numeric columns while text stays qualitative (C2)?

== ANALYTICAL GOAL ==
{goal}

== REPORT ==
{report}
== END ==

Return STRICT JSON ONLY:
{{\"category\": \"C1_all_qualitative\" | \"C2_text_qual_numeric_quant\" | \"C3_text_augmented_quant\", \"confidence\": 0.0-1.0, \"reason\": \"one short sentence\"}}"""


def _goalmap():
    m = {}
    try:
        d = json.load(open("/mnt/data/benchmark/analysis_report/manifest.json", encoding="utf-8"))
        for e in d.get("reports", []):
            m[(e["dataset"], e["scenario"])] = e.get("query") or ""
    except Exception:
        pass
    return m

GOAL = _goalmap()


def call(prompt):
    env = dict(os.environ); env["IS_SANDBOX"] = "1"; env.pop("CLAUDECODE", None); env["CLAUDE_CODE_SIMPLE"] = "1"
    r = subprocess.run([CLAUDE, "-p", "--no-session-persistence", "--permission-mode", "bypassPermissions",
        "--output-format", "json", "--model", MODEL], input=prompt, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=300, env=env)
    try:
        w = json.loads(r.stdout); txt = w.get("result", r.stdout) if isinstance(w, dict) else r.stdout
    except Exception:
        txt = r.stdout
    i, j = txt.find("{"), txt.rfind("}")
    return json.loads(txt[i:j + 1])


def tasks():
    ts = []
    for f in glob.glob(ROOT + "/*/*/*/*.md"):
        stem = os.path.basename(f)[:-3]
        if stem not in VARMAP:
            continue
        parts = f.split("/")
        model, dataset, query = parts[-4], parts[-3], parts[-2]
        ts.append({"file": f, "model": model, "variant": VARMAP[stem],
                   "dataset": dataset, "query": query})
    return ts


def do(t):
    dsdir = os.path.join(OUT, t["dataset"]); os.makedirs(dsdir, exist_ok=True)
    of = os.path.join(dsdir, "%s__%s__%s__%s.json" % (t["dataset"], t["query"], t["model"], t["variant"]))
    if os.path.exists(of) and os.path.getsize(of) > 2:
        return
    rep = open(t["file"], encoding="utf-8", errors="replace").read()[:12000]
    goal = GOAL.get((t["dataset"], t["query"])) or ("%s / %s" % (t["dataset"], t["query"]))
    try:
        res = call(PROMPT.format(goal=goal, report=rep))
    except Exception as e:
        res = {"category": "ERR", "reason": str(e)[:120]}
    rec = dict(t); rec.pop("file"); rec.update(res)
    json.dump(rec, open(of, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    os.makedirs(OUT, exist_ok=True)
    ts = tasks(); print("tasks:", len(ts), flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=48) as ex:
        futs = {ex.submit(do, t): t for t in ts}
        for fu in as_completed(futs):
            fu.result(); done += 1
            if done % 50 == 0:
                print("done %d/%d" % (done, len(ts)), flush=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
