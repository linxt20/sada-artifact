import json
from collections import Counter
from pathlib import Path

root = Path("final_result")
models = {"substrate-claude-haiku-4-5": "haiku", "substrate-claude-sonnet-4-6": "sonnet"}
vs = ["skill_off", "skill_on", "skill_on_e2e"]


def load(p):
    try:
        j = json.loads(p.read_text(encoding="utf-8"))
        return j if j.get("status") == "scored" else None
    except Exception:
        return None


cat_win = Counter()
cat_tot = Counter()
focus_rows = []

for sd in sorted(root.iterdir()):
    if not sd.is_dir():
        continue
    for m, s in models.items():
        md = sd / m
        if not md.exists():
            continue
        js = {v: load(md / f"{v}_characteristic.json") for v in vs}
        if any(j is None for j in js.values()):
            continue
        adh = {v: (js[v].get("metrics") or {}).get("adherence") for v in vs}
        if any(a is None for a in adh.values()):
            continue
        cat = js["skill_off"].get("category") or "unknown"
        cat_tot[cat] += 1
        off_wins = adh["skill_off"] >= adh["skill_on"] and adh["skill_off"] >= adh["skill_on_e2e"]
        if off_wins:
            cat_win[cat] += 1
        if cat == "focus_internal_structure" and off_wins:
            mt = {v: (js[v].get("metrics") or {}) for v in vs}
            focus_rows.append(
                (sd.name[:44], s, adh, mt)
            )

print("=== skill_off >= BOTH on & e2e, by category ===")
for c in cat_tot:
    print(f"{c:28} {cat_win[c]:>3}/{cat_tot[c]}")
print("total skill_off-wins:", sum(cat_win.values()), "/", sum(cat_tot.values()))

print("\n=== focus_internal skill_off wins: facet/coverage/redundancy ===")
for name, s, adh, mt in focus_rows:
    off, on, e2e = mt["skill_off"], mt["skill_on"], mt["skill_on_e2e"]
    print(
        f"{name:44} {s:6} "
        f"OFF adh={adh['skill_off']:.2f} facet={off.get('facet_fraction')} cov={off.get('coverage')} red={off.get('redundancy')} | "
        f"ON adh={adh['skill_on']:.2f} facet={on.get('facet_fraction')} red={on.get('redundancy')} | "
        f"E2E adh={adh['skill_on_e2e']:.2f} facet={e2e.get('facet_fraction')} red={e2e.get('redundancy')}"
    )
