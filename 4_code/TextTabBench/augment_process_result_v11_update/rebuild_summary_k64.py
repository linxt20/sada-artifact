#!/usr/bin/env python3
"""Rebuild summary CSV from the k=64 text-regime reruns.

no_text columns are copied from the existing summary (unaffected by the embedding
budget change); text columns are re-read from the *_k{K}.json files.
"""
import json, glob, os, csv, sys

K = int(sys.argv[1]) if len(sys.argv) > 1 else 64
HERE = os.environ.get("TEXTTABBENCH_RESULTS_ROOT", os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "summary_v11_update.csv")
DST = os.path.join(HERE, f"summary_v11_update_k{K}.csv")

COLMAP = {
    ("baseline", ""): "baseline_text",
    ("skill_off", "haiku"): "haiku_skilloff_text",
    ("skill_on_e2e", "haiku"): "haiku_skillon_text",
    ("skill_off", "sonnet"): "sonnet_skilloff_text",
    ("skill_on_e2e", "sonnet"): "sonnet_skillon_text",
}


def read_cell(ds, variant, mtag):
    suf = "" if variant == "baseline" else f"_{mtag}"
    p = os.path.join(HERE, ds, variant, f"xgb_results_{ds}_text_skrub_shap{suf}_k{K}.json")
    if not os.path.exists(p):
        return None, None, None
    d = json.load(open(p))
    means, stds, keys = [], [], set()
    for run in d.values():
        for _, v in run.items():
            for k, m in v.get("xgb", {}).items():
                keys.add(k)
                means.append(m["mean"]["accuracy"])
                stds.append(m["std"]["accuracy"])
    if not means:
        return None, None, None
    return sum(means) / len(means), sum(stds) / len(stds), sorted(keys)


rows = list(csv.DictReader(open(SRC)))
missing, keyset = [], set()
for r in rows:
    ds = r["dataset"]
    for (variant, mtag), col in COLMAP.items():
        mean, std, keys = read_cell(ds, variant, mtag)
        if mean is None:
            missing.append(f"{ds}/{variant}/{mtag}")
            continue
        keyset.update(keys)
        r[col] = f"{mean:.4f}"
        r[col + "_std"] = f"{std:.4f}"

with open(DST, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

print(f"wrote {DST}")
print(f"selector keys seen: {sorted(keyset)}")
if missing:
    print(f"MISSING {len(missing)} cells:")
    for m in missing:
        print("  ", m)
else:
    print("all text cells present")
