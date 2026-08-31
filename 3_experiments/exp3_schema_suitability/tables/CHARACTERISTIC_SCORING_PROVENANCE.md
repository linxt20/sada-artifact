# Characteristic Adherence (B-2) — 结果与评分标准索引

> 论文 **Table 4「Characteristic adherence by intent sub-type」** 的唯一权威来源。
> 本目录下有 12 个 `characteristic_*` 目录和多轮 v1/fair/fair2/v2 打分器，极易取错。
> 建档日期 2026-08-06；已逐格复核，Table 4 的 36 个数字全部对上。

---

## 1. 一句话结论

| 要查什么 | 去哪个文件 |
|---|---|
| **Table 4 的数字** | `augment_table_evaluation/augment_result_v11_update/SUMMARY_by_family.md`（"二、Subtype 细化"一节） |
| **评分标准 / adherence 公式** | `scorer_v2/b2_characteristic_adherence.py`（docstring 第 46–56 行给出全部六条公式） |
| **judge prompt 原文** | 同上，`build_prompt()`（第 282 行）及其上方各 subtype 的 rubric 字符串（第 130–280 行） |
| **逐 unit 明细** | `augment_table_evaluation/augment_result_v11_update/<dataset>/<model>/<scenario>__<variant>_b2.json` |
| **跑批驱动** | `scorer_v2/run_v11_update.py` |

**其余所有 `characteristic_evaluation_*` 目录都不是 Table 4 的来源**（见第 6 节）。

---

## 2. 结果来源链

```
augment_table/<dataset>/<scenario>/<model>__<variant>_update.csv      ← 被评的增广表
        │
        ├── scorer_v2/run_v11_update.py            （驱动，judge=claude-opus-4.8-xhigh）
        │        └── scorer_v2/b2_characteristic_adherence.py   （打分器 = 评分标准）
        │
        ▼
augment_table_evaluation/augment_result_v11_update/
        <dataset>/<model>/<scenario>__<variant>_b2.json        ← 逐 unit（含 judge 原始输出）
        <dataset>/<model>/<scenario>__<variant>_b2_call.json   ← 该次 judge 调用日志
        SUMMARY_by_family.md                                   ← 汇总 = 论文 Table 4
```

variant 后缀映射（定义在 `run_v11_update.py`）：

| 论文条件 | CSV 后缀 |
|---|---|
| `skill_off` | `<model>__skill_off_update.csv` |
| `skill_on` | `<model>__skill_on_v11_update.csv` |
| `skill_on_e2e` | `<model>__skill_on_e2e_v11_update.csv` |

judge 模型：`claude-opus-4.8-xhigh`（`run_v11_update.py:133` 默认值），全条件全 substrate 固定。

---

## 3. ⚠️ 单位筛选规则：116 → 108

`augment_result_v11_update/` 下每个 substrate 实际有 **116** 个 scored unit，Table 4 用的是 **108**。

**排除规则：丢掉 `airlines_review_full` 整个数据集（8 units × 2 substrate）。**

`airlines_review` 与 `airlines_review_full` 是同一张表的两次 scope，`_full` 为 2026-08-03 后加，未进论文口径。

复现命令（在 `augment_result_v11_update/` 下执行，输出与 Table 4 逐格一致）：

```bash
python3 -c "
import json,glob,collections,statistics
rows=collections.defaultdict(list)
for f in glob.glob('*/*/*_b2.json'):
    d=json.load(open(f))
    if d['dataset']=='airlines_review_full': continue          # ← 关键筛选
    a=(d.get('metrics') or {}).get('adherence')
    if a is not None: rows[(d['subtype'],d['model'],d['variant'])].append(a)
for st in ['causal_attribution','what_if','predictive_feature_engineering',
           'exploratory_data_analysis','faceted_decomposition','focus_inference']:
    for m in ['haiku','sonnet']:
        o=[f'{statistics.mean(rows[(st,m,v)]):.3f}/n{len(rows[(st,m,v)])}'
           for v in ['skill_off','skill_on','skill_on_e2e']]
        print(f'{st:32s} {m:7s} ' + ' | '.join(o))
"
```

---

## 4. 评分标准：v2 六条 adherence 公式

全部在 `scorer_v2/b2_characteristic_adherence.py` docstring（46–56 行）与 `compute_metrics()`（333 行）：

```
predictive_feature_engineering : predictor_fraction * predictive_utility
exploratory_data_analysis      : predictor_fraction * relationship_informativeness
causal_attribution             : treatment_present      * (0.4 + 0.6*unnamed_bonus) * confounder_quality
what_if                        : treatment_intervenable * (0.4 + 0.6*unnamed_bonus) * confounder_quality
faceted_decomposition          : facet_fraction * mece * (1 - redundancy)
focus_inference                : focus_coherence * structure_quality * (1 - redundancy)

unnamed_bonus = 1  若至少一个 confounder 未在 query 中被点名，否则 0
mece          = sqrt(mutual_exclusivity * exhaustiveness)
redundancy    = 由列名确定性计算（_normalized_redundancy），非 judge 打分
```

**关键设计：adherence 一律由子指标确定性合成，judge 只提供分量，不输出 headline 分数。**
（docstring 第 5 条明确写了这是 v2 相对 v1 的修正："v1 let the judge emit a holistic `adherence` float …
so the headline number was a vibe rather than a function of the sub-claims."）

已抽查验证：`_b2.json` 的 `judge` 字段里**没有** `adherence` 键，`metrics.adherence` 为算出值。

### judge 实际输出的字段（全集）

```
subtype, per_column, rationale,
role (predictor|leakage|restatement|irrelevant), is_predictor, n_predictors,
predictive_utility, relationship_informativeness,
outcome_variable, treatment_present, treatment_intervenable,
confounders[{name, named_in_query}], confounder_quality,
concept, facet_columns, mutual_exclusivity, exhaustiveness,
implied_focus, focus_variable, focus_coherence, structure_quality, focus_actionability
```

注意：`focus_actionability` **被 judge 输出并记录，但不进入 focus_inference 的 adherence 公式**（公式只用
coherence × structure_quality × (1−redundancy)）。`leakage_rate` 同理，是记录出来的派生指标（PFE 分支，
`compute_metrics` 第 344 行），不直接乘进 adherence——leakage 通过 `role` 判定压低 `predictor_fraction` 生效。

---

## 5. Table 4 数值 + 每格 n（Haiku/Sonnet 各 108 units）

| Subtype | model | skill_off | skill_on | skill_on_e2e | n (off/on/e2e) |
|---|---|---:|---:|---:|---:|
| causal_attribution | haiku | 0.138 | 0.339 | 0.413 | 19/19/19 |
| causal_attribution | sonnet | 0.297 | 0.379 | 0.472 | 19/19/19 |
| what_if | haiku | 0.062 | 0.381 | 0.443 | **17/16/16** |
| what_if | sonnet | 0.179 | 0.394 | 0.470 | 17/17/17 |
| predictive_feature_engineering | haiku | 0.323 | 0.451 | 0.369 | 20/20/20 |
| predictive_feature_engineering | sonnet | 0.318 | 0.474 | 0.487 | 20/20/20 |
| exploratory_data_analysis | haiku | 0.395 | 0.704 | 0.679 | 17/17/17 |
| exploratory_data_analysis | sonnet | 0.314 | 0.711 | 0.660 | 17/17/17 |
| faceted_decomposition | haiku | 0.131 | 0.383 | 0.426 | 18/18/18 |
| faceted_decomposition | sonnet | 0.295 | 0.357 | 0.336 | 18/18/18 |
| focus_inference | haiku | 0.596 | 0.602 | 0.603 | 17/17/17 |
| focus_inference | sonnet | 0.629 | 0.680 | 0.653 | 17/17/17 |

Family 汇总（同一 SUMMARY 文件"一、Family 汇总"节，论文未用）：

| Family | haiku off/on/e2e | sonnet off/on/e2e |
|---|---|---|
| Causal | 0.102 / 0.358 / 0.427 | 0.242 / 0.386 / 0.471 |
| Correlational | 0.356 / 0.567 / 0.512 | 0.316 / 0.583 / 0.566 |
| Focus-internal | 0.357 / 0.489 / 0.512 | 0.457 / 0.514 / 0.490 |

**⚠️ `what_if` / haiku 的 n 不齐（17/16/16）**：skill_on 与 skill_on_e2e 各缺 1 个 unit。
论文最醒目的对比 0.062 → 0.443 因此建立在略有差异的 unit 集上，制表时应注明或补齐。

---

## 6. 版本谱系：哪些目录**不要**用

打分器共三代，都还在仓库里：

| 代 | 文件 | adherence 来源 | faceted 指标 | 状态 |
|---|---|---|---|---|
| v1 | `scorer_characteristic/characteristic_adherence.py` | causal/correlational **由 judge 自由打分**（`judge["adherence"]`，第 324 行）；focus-internal 才合成 | 声明了 `mece` 但从未向 judge 索取、也没用进分数 | **废弃** |
| fair2 | `scorer_characteristic/characteristic_adherence_fair2.py` | 全部合成 | 用 `coverage` 代替 mece | **废弃** |
| **v2** | **`scorer_v2/b2_characteristic_adherence.py`** | **全部合成，per-subtype** | **mece = sqrt(mut_ex × exhaust)，显式索取** | **✅ 当前唯一权威** |

结果目录对应关系：

| 目录 | 是什么 | 用不用 |
|---|---|---|
| **`augment_table_evaluation/augment_result_v11_update/`** | **v2 打分 × `_update`（agentic 重跑）增广表，2026-07-30** | **✅ Table 4** |
| `characteristic_evaluation_v2/SUMMARY.json` | v2 打分 × **非** `_update`（第一轮 chunk 分块）增广表，2026-07-28 | ❌ 同 scorer 但被评对象不同，数值不同（如 causal_attribution/haiku/skill_off = 0.3079 vs 0.138） |
| `augment_table_evaluation/augment_result_v11/` | v11 早期，含 B-1 | ❌ |
| `characteristic_evaluation_{fair,fair2,fair2_dedup,fair2_regen,fair_dedup,fair_dedup2,aligned,new,v11,v11_foi_gt}/` | v1/fair/fair2 各轮迭代 | ❌ 全部过期 |
| `characteristic_result/`、`characteristic_skilloff_update/` | 中间聚合 | ❌ |

判别小技巧:`_b2.json` 里带 `"scorer": "B-2 characteristic adherence (per-subtype)"` 的才是 v2。

---

## 7. 与论文正文的对照（2026-08-06 核对）

**主文 §5.4 的表述与 v2 一致，无需改动：**

- ✅ "The judge never outputs the headline number … adherence is composed from them by a fixed
  deterministic rule" —— 与 v2 docstring 第 5 条完全吻合。
- ✅ "PFE additionally penalising leakage" —— `role="leakage"` 分类 + `leakage_rate`。
- ✅ "EDA rewarding interpretable relationships" —— `relationship_informativeness`。
- ✅ "What-If further requiring the treatment to be intervenable" —— `treatment_intervenable` 作为 gate。
- ✅ "Faceted scores the facet fraction and MECE" —— `facet_fraction × mece`。
- ⚠️ "Focus-Inf … scores the **coherence and actionability** of the focus proposed" —— **不准确**。
  公式用的是 `focus_coherence × structure_quality`；`focus_actionability` 只被记录，不进分数。
  建议改为 "the coherence and structural quality of the focus proposed"。

**附录 §4.3（`paper-tapp-vldb/appendix.tex`）印的是过期 prompt：**

现有附录复制的是 v1 / fair2 的 rubric —— 特征是 correlational 与 causal rubric 里带
`"adherence": 0.0` 输出字段、faceted 用 `coverage` 而非 MECE、无 `predictive_utility` /
`relationship_informativeness` / `treatment_intervenable`。这与 Table 4 的实际打分器（v2）不符，
是审稿意见"无法据附录复现 Table 4"的真实原因。

**待办**：把附录 §4.3 换成 `scorer_v2/b2_characteristic_adherence.py` 的 prompt 与六条公式。
属纯文档改动，不需重跑任何实验。
