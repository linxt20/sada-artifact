# 实验A · update 语料评分总结

> 判官: `claude-opus-4.8-xhigh`。四变体: `original`(原始表) · `skill_off`(skill_off_update) · `skill_on`(skill_on_v11_update) · `skill_on_e2e`(skill_on_e2e_v11_update)。
> 全 17 数据集聚合, haiku / sonnet 分列。产物目录 `analysis_result_update/{bt,form_class}/`。

## 指标 A-1 · BT 5维 pairwise (BT strength 越高越好)

### haiku (units=108)

| variant | BT_strength | specificity | evidence | depth | actionability | coherence |
|---|--:|--:|--:|--:|--:|--:|
| original | -6.484 | 4.00 | 3.76 | 3.82 | 3.84 | 4.17 |
| skill_off | -1.983 | 4.37 | 4.39 | 4.08 | 4.11 | 3.91 |
| skill_on | 1.376 | 4.53 | 4.47 | 4.32 | 4.34 | 3.96 |
| **skill_on_e2e** | **7.170** | 4.93 | 4.93 | 4.83 | 4.44 | 4.07 |

### sonnet (units=108)

| variant | BT_strength | specificity | evidence | depth | actionability | coherence |
|---|--:|--:|--:|--:|--:|--:|
| original | -4.597 | 4.38 | 4.15 | 4.17 | 4.14 | 4.39 |
| skill_off | -5.291 | 4.30 | 4.38 | 4.04 | 4.16 | 4.27 |
| skill_on | 1.435 | 4.54 | 4.54 | 4.36 | 4.39 | 4.27 |
| **skill_on_e2e** | **8.453** | 4.96 | 4.98 | 4.90 | 4.81 | 4.52 |

## 指标 6 · 分析形态分布 (C1/C2/C3, 占比)

- **C1_all_qualitative**: 基本定性, 少/无定量计算
- **C2_text_qual_numeric_quant**: 仅对原始数值列定量, 文本仅定性
- **C3_text_augmented_quant**: 量化文本派生信号 + 数值列 (增广目标形态)

### haiku

| variant | n | C1_qualitative | C2_numeric_quant | C3_text_augmented |
|---|--:|--:|--:|--:|
| original | 108 | 23.1% | 13.0% | 63.9% |
| skill_off | 108 | 0.0% | 9.3% | 90.7% |
| skill_on | 107 | 0.0% | 1.9% | 98.1% |
| skill_on_e2e | 107 | 0.0% | 0.0% | 100.0% |

### sonnet

| variant | n | C1_qualitative | C2_numeric_quant | C3_text_augmented |
|---|--:|--:|--:|--:|
| original | 108 | 27.8% | 19.4% | 52.8% |
| skill_off | 108 | 0.0% | 9.3% | 90.7% |
| skill_on | 108 | 0.9% | 1.9% | 97.2% |
| skill_on_e2e | 108 | 0.0% | 0.0% | 100.0% |

## 要点

- 两模型上变体质量单调递增: `original < skill_off < skill_on < skill_on_e2e`。
- BT 强度 skill_on_e2e 大幅领先 (haiku +7.17 / sonnet +8.45), 五维几乎全部逼近满分。
- 形态分布: skill_on 后 C3 (文本增广定量) 占比逼近 100%, e2e 达 100%; 而 original 仍有 23–28% 停留在纯定性 (C1)。
- 唯一非单调点: sonnet 的 skill_off BT 强度 (−5.29) 略低于 original (−4.60)。
