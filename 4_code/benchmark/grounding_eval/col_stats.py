# -*- coding: utf-8 -*-
"""增广列统计(不调用 LLM):
1) 每个增广表格 / 每个增广列的 unknown|none|空 缺失率
2) 每个增广列的值域枚举与各值占比
输出: per_column.csv, per_table.csv, value_domain.jsonl, report.md
"""
from __future__ import annotations
import csv, json, os, glob, sys, re
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(10 ** 9)

ROOT = Path(__file__).resolve().parent.parent / "augment_table"
OUT = Path(__file__).resolve().parent

VARIANTS = [
    ("haiku", "skill_off_update", "haiku__skill_off_update"),
    ("sonnet", "skill_off_update", "sonnet__skill_off_update"),
    ("haiku", "skill_on_e2e", "haiku__skill_on_e2e-v11"),
    ("sonnet", "skill_on_e2e", "sonnet__skill_on_e2e-v11"),
    ("haiku", "skill_on", "haiku__skill_on-v11"),
    ("sonnet", "skill_on", "sonnet__skill_on-v11"),
]

# 判定为"缺失/未知"的规范化字面量
NULL_TOKENS = {
    "", "none", "null", "nan", "na", "n/a", "n.a.", "-", "--",
    "unknown", "unspecified", "not specified", "not_specified",
    "not mentioned", "not_mentioned", "notmentioned",
    "not applicable", "not_applicable", "not available", "not_available",
    "no data", "no_data", "missing", "undetermined", "indeterminate",
    "not stated", "not_stated", "not provided", "not_provided",
    "无", "未知", "未提及", "不适用",
}
UNKNOWN_RE = re.compile(r"^(unknown|none|not[ _-]?(mentioned|specified|stated|provided|available|applicable))\b", re.I)

# 值域枚举阈值: 唯一值数 <= 该值或唯一率 <= 0.2 视为类别列
CAT_MAX_UNIQUE = 60
CAT_MAX_UNIQ_RATIO = 0.2
TOPK = 40


def norm(v):
    return re.sub(r"\s+", " ", str(v)).strip()


def is_null_like(v):
    s = norm(v).lower().strip(".。")
    return s in NULL_TOKENS or bool(UNKNOWN_RE.match(s))


def read_csv(path):
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        r = csv.reader(f)
        try:
            header = next(r)
        except StopIteration:
            return [], []
        rows = list(r)
    return header, rows


def main():
    scenarios = sorted(glob.glob(str(ROOT / "*" / "*" / "original.csv")))
    per_col_rows = []
    per_tab_rows = []
    domain_f = (OUT / "value_domain.jsonl").open("w", encoding="utf-8")
    print("scenarios=%d" % len(scenarios), flush=True)

    for k, orig_path in enumerate(scenarios, 1):
        sd = Path(orig_path).parent
        dataset, scenario = sd.parent.name, sd.name
        ohdr, _ = read_csv(orig_path)
        oset = set(ohdr)
        for model, config, fname in VARIANTS:
            fp = sd / (fname + ".csv")
            if not fp.exists():
                per_tab_rows.append(dict(dataset=dataset, scenario=scenario, model=model,
                                         config=config, status="MISSING", n_rows=0,
                                         n_aug_cols=0, n_cells=0, n_null=0, null_rate=""))
                continue
            hdr, rows = read_csv(fp)
            aug_cols = [c for c in hdr if c not in oset]
            idx = {c: hdr.index(c) for c in aug_cols}
            n = len(rows)
            tab_cells = tab_null = 0
            for c in aug_cols:
                j = idx[c]
                vals = [norm(r[j]) if j < len(r) else "" for r in rows]
                cnt = Counter(vals)
                nulls = sum(m for v, m in cnt.items() if is_null_like(v))
                uniq = len(cnt)
                uniq_ratio = uniq / n if n else 0.0
                is_cat = uniq <= CAT_MAX_UNIQUE or uniq_ratio <= CAT_MAX_UNIQ_RATIO
                tab_cells += n
                tab_null += nulls
                per_col_rows.append(dict(
                    dataset=dataset, scenario=scenario, model=model, config=config,
                    column=c, n_rows=n, n_unique=uniq, unique_ratio=round(uniq_ratio, 4),
                    n_null_like=nulls, null_rate=round(nulls / n, 4) if n else "",
                    is_categorical=int(is_cat),
                    top_value=(cnt.most_common(1)[0][0][:80] if cnt else ""),
                    top_share=round(cnt.most_common(1)[0][1] / n, 4) if (cnt and n) else "",
                ))
                domain_f.write(json.dumps({
                    "dataset": dataset, "scenario": scenario, "model": model, "config": config,
                    "column": c, "n_rows": n, "n_unique": uniq, "is_categorical": bool(is_cat),
                    "n_null_like": nulls,
                    "domain": [{"value": v[:200], "count": m, "share": round(m / n, 4) if n else 0,
                                "null_like": is_null_like(v)}
                               for v, m in cnt.most_common(TOPK)],
                    "truncated": uniq > TOPK,
                }, ensure_ascii=False) + "\n")
            per_tab_rows.append(dict(dataset=dataset, scenario=scenario, model=model, config=config,
                                     status="OK", n_rows=n, n_aug_cols=len(aug_cols),
                                     n_cells=tab_cells, n_null=tab_null,
                                     null_rate=round(tab_null / tab_cells, 4) if tab_cells else ""))
        if k % 20 == 0:
            print("  %d/%d" % (k, len(scenarios)), flush=True)
    domain_f.close()

    def dump(path, rows):
        if not rows:
            return
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    dump(OUT / "per_column.csv", per_col_rows)
    dump(OUT / "per_table.csv", per_tab_rows)
    print("per_column=%d per_table=%d" % (len(per_col_rows), len(per_tab_rows)))


if __name__ == "__main__":
    main()
