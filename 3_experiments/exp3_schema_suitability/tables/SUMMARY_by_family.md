# B-2 Characteristic Adherence — Summary by Family / Subtype

Judge: `claude-opus-4.8-xhigh`。Adherence 由各 subtype 可核查子指标确定性合成(非判官自由打分)。
Variant:skill_off = skill_off_update,skill_on = skill_on_v11_update,skill_on_e2e = skill_on_e2e_v11_update。

## 一、Family 汇总(3 大类)

| Family | model | skill_off | skill_on | skill_on_e2e | n/variant |
| --- | --- | ---: | ---: | ---: | ---: |
| Causal 因果 | haiku | 0.102 | 0.358 | 0.427 | 36/35/35 |
| Causal 因果 | sonnet | 0.242 | 0.386 | 0.471 | 36/36/36 |
| Correlational 相关 | haiku | 0.356 | 0.567 | 0.512 | 37/37/37 |
| Correlational 相关 | sonnet | 0.316 | 0.583 | 0.566 | 37/37/37 |
| Focus-internal 焦点内部结构 | haiku | 0.357 | 0.489 | 0.512 | 35/35/35 |
| Focus-internal 焦点内部结构 | sonnet | 0.457 | 0.514 | 0.49 | 35/35/35 |

## 二、Subtype 细化(6 子类,按 family 分组)

### Causal 因果

| Subtype | 技术主张 | model | skill_off | skill_on | skill_on_e2e | n/variant |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `causal_attribution` | 因果归因(观测到的原因) | haiku | 0.138 | 0.339 | 0.413 | 19/19/19 |
| `causal_attribution` | 因果归因(观测到的原因) | sonnet | 0.297 | 0.379 | 0.472 | 19/19/19 |
| `what_if` | What-if 干预(可干预 treatment) | haiku | 0.062 | 0.381 | 0.443 | 17/16/16 |
| `what_if` | What-if 干预(可干预 treatment) | sonnet | 0.179 | 0.394 | 0.47 | 17/17/17 |

### Correlational 相关

| Subtype | 技术主张 | model | skill_off | skill_on | skill_on_e2e | n/variant |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `predictive_feature_engineering` | 预测特征工程(模型预测子) | haiku | 0.323 | 0.451 | 0.369 | 20/20/20 |
| `predictive_feature_engineering` | 预测特征工程(模型预测子) | sonnet | 0.318 | 0.474 | 0.487 | 20/20/20 |
| `exploratory_data_analysis` | 探索性分析(可解释关系) | haiku | 0.395 | 0.704 | 0.679 | 17/17/17 |
| `exploratory_data_analysis` | 探索性分析(可解释关系) | sonnet | 0.314 | 0.711 | 0.66 | 17/17/17 |

### Focus-internal 焦点内部结构

| Subtype | 技术主张 | model | skill_off | skill_on | skill_on_e2e | n/variant |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `faceted_decomposition` | 分面拆解(MECE 构成面) | haiku | 0.131 | 0.383 | 0.426 | 18/18/18 |
| `faceted_decomposition` | 分面拆解(MECE 构成面) | sonnet | 0.295 | 0.357 | 0.336 | 18/18/18 |
| `focus_inference` | 焦点推断(query 未给焦点) | haiku | 0.596 | 0.602 | 0.603 | 17/17/17 |
| `focus_inference` | 焦点推断(query 未给焦点) | sonnet | 0.629 | 0.68 | 0.653 | 17/17/17 |

## 三、要点

**Causal 因果** — 提升最猛,skill_off 基线最低。
- `causal_attribution` 因果归因:haiku 0.14→0.34→0.41,sonnet 0.30→0.38→0.47。
- `what_if` 干预:haiku skill_off 仅 0.06(几乎不产出可干预 treatment),skill_on 后 0.38,e2e 0.44。skill 价值最突出。

**Correlational 相关** — skill_on 收益最大,e2e 无额外增益甚至微降。
- `exploratory_data_analysis` 探索性分析:两模型 skill_on 均破 0.70,是全 6 子类最高;e2e 略降。
- `predictive_feature_engineering` 预测特征:提升温和(约 0.32→0.47),受 leakage / 冗余惩罚压制。

**Focus-internal 焦点内部结构** — 两子类分化极大,family 均值掩盖了它。
- `faceted_decomposition` 分面拆解:haiku 0.13→0.38→0.43;sonnet 提升平(0.30→0.36→0.34),MECE 难达。
- `focus_inference` 焦点推断:skill_off 就有 0.60–0.63(无需给定焦点、门槛低),skill 只小幅抬升。
