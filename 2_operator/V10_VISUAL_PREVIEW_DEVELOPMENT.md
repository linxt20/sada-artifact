# TA++ Skill v10 图片预览改造开发文档

## 目标

Skill v10 基于 skill v9 改造，新增一个有边界的图片预览通道。核心思路是：在 schema planning、category proposal、analysis reading 之前，先把原始表格中的部分行和关键列预处理成一张或多张固定分辨率图片，让支持视觉输入的模型通过图片理解数据形态、字段语义、常见文本信号和候选 facet，而不是把大量原始文本预览直接塞进 prompt。

这个改造不能削弱 TA++ 的严格表格增强能力。凡是需要精确逐行标注、精确计数、join、数值计算、闭集校验或 merge gate 的阶段，都必须继续以原始数据表或逐行文本 payload 为准。图片只作为上下文压缩和数据预览，不作为严格数据源。

## 当前结论

当前建议：**v10 第一阶段继续使用高分辨率图片预览作为画布基线，但渲染方式应切换到 OCR/dense 信息密度思路**。也就是说，画布仍使用当前原型中的 `1600x2200`，但通过更小字体、更紧凑行高、更窄结构化列、更宽文本列和更少留白，让一张固定大小的图尽可能容纳更多信息。低分辨率不是不能完整展示内容，但需要更复杂的分页和布局；在真实模型 token 计量没有跑清楚之前，不把低分辨率作为默认方案。

高分辨率路线的理由：

- 当前 `1600x2200` readable 预览两页即可完整展示 60 行样本；新增 OCR/dense 模式后，同样 60 行可以压缩到 1 页，并且主要文本证据仍可读。
- 对 schema planning 和 category proposal，模型需要读懂语义线索，过早压低分辨率容易牺牲可读性。
- 低分辨率 `768x1056` 修复分页后也可以完整展示，但 60 行会变成 4 页；总 token 成本不一定更低。
- 真正要优化的是 `page_count * image_tokens_per_page` 和单位图片可读信息量，不是单张图片分辨率本身。

## 复杂度判断

这是一个中等复杂度改造，不是完整重写。

- 预处理和渲染复杂度较低到中等：可以新增 skill-owned renderer，输出 PNG 图片、manifest 和 metrics。
- executor 接入复杂度中等：v9 现在是文本 payload 链路，v10 需要新增 vision-capability gate、图片 artifact 引用和 text fallback。
- 如果把图片用于 tagging，风险较高：OCR 错误、截断、行号误读都会破坏严格行对齐。因此 v10 必须明确禁止 image-only tagging。
- v9 已有的 validation、merge、trace、artifact manifest、strict row-index 逻辑大部分可以保留。

预期加速主要来自减少 category planning 和 analysis reading 中重复进入上下文的大段文本预览。它不会直接加速最终 tagging，除非图片预览提升 schema 质量，从而减少坏 facet、重试或后续修正。

## Step 1：可行性验证

状态：本地初步原型已完成。

原型脚本：

- [scripts/visual_preview_feasibility.py](scripts/visual_preview_feasibility.py)

已生成的实验产物：

- [prototypes/visual_preview_feasibility/preview_page_01.png](prototypes/visual_preview_feasibility/preview_page_01.png)
- [prototypes/visual_preview_feasibility/preview_page_02.png](prototypes/visual_preview_feasibility/preview_page_02.png)
- [prototypes/visual_preview_feasibility/equivalent_text_preview.json](prototypes/visual_preview_feasibility/equivalent_text_preview.json)
- [prototypes/visual_preview_feasibility/visual_prompt.md](prototypes/visual_preview_feasibility/visual_prompt.md)
- [prototypes/visual_preview_feasibility/visual_prompt_dry_run.json](prototypes/visual_preview_feasibility/visual_prompt_dry_run.json)
- [prototypes/visual_preview_feasibility/metrics.json](prototypes/visual_preview_feasibility/metrics.json)
- [prototypes/visual_preview_feasibility/report.md](prototypes/visual_preview_feasibility/report.md)

OCR/dense 高信息密度验证产物：

- [prototypes/visual_preview_ocr_density_1600x2200/preview_page_01.png](prototypes/visual_preview_ocr_density_1600x2200/preview_page_01.png)
- [prototypes/visual_preview_ocr_density_1600x2200/metrics.json](prototypes/visual_preview_ocr_density_1600x2200/metrics.json)

低分辨率分页修复验证产物：

- [prototypes/visual_preview_resolution_768x1056_fixed/preview_page_01.png](prototypes/visual_preview_resolution_768x1056_fixed/preview_page_01.png)
- [prototypes/visual_preview_resolution_768x1056_fixed/preview_page_04.png](prototypes/visual_preview_resolution_768x1056_fixed/preview_page_04.png)

使用的数据集：

- `healthcare_visit_notes.xlsx`
- 查询：`What visit-note signals suggest high urgency?`
- 总行数：250
- 预览行数：60
- 预览列：`visit_id`、`department`、`urgency`、`age_group`、`visit_duration_min`、`reason_for_visit`

已观察到的指标：

- 等价文本预览：23,987 字符，按 chars/4 粗略估算约 5,997 text tokens。
- 高分辨率图片预览：2 张 PNG，分辨率为 1600x2200。
- 高分辨率 PNG 总大小：560,774 bytes。
- OCR/dense 高信息密度版本：1 张 PNG，分辨率仍为 1600x2200，容纳同样 60 行样本；PNG 大小约 301,383 bytes。粗略 image-token 估算约为 1,105 tokens（512 tile high-detail 口径）或 1,534 tokens（capped patch/area 口径），约为 readable 两页方案的一半。
- 图片 token 粗估和 provider 强相关：按 512 tile high-detail 估算，图片约 2,210 tokens；按 capped patch/area 估算，图片约 3,070 tokens。
- `visual_prompt.md` 额外约 472 text tokens。因此当前图片请求粗略约 2.7k-3.5k tokens，对比等价文本预览约 6.0k tokens。
- 加上 prompt 文本后，当前图片方案约节省 40%-55%；只比较图片 token 和行文本预览时，约节省 49%-63%。这个结果足够支撑继续做 preview-heavy 阶段的 v10 原型，但必须用目标模型的实报 image-token accounting 复测。

关于分辨率和布局的修正结论：

- 内容缺失是布局 bug，不是低分辨率本身的问题。
- 低分辨率也可以完整展示内容，前提是分页、行高、换行、列选择正确。
- 固定大小图片的信息容量不是固定的。可以通过调小字体、压缩行高、减少边距、压窄结构化列、加宽文本列、增加每行可见字符数来显著提高单位图片信息密度。这一点更接近 DeepSeek OCR 一类“把视觉输入当作高密度文本载体”的思路。
- OCR/dense 模式的初步结果表明：同一张 `1600x2200` 图片可以完整展示 60 行样本，而 readable 模式需要 2 页。这说明 v10 的优先优化方向应该是“高分辨率画布 + dense/OCR 排版”，而不是简单降低分辨率。
- OCR/dense 模式不能把少量行强行拉伸到整张画布高度。renderer 已调整为内容贴合高度：当 30 行样本只需要约 1064px 高度时，实际输出图片为 `1600x1064`，而不是保留大量空白的 `1600x2200`。manifest 会记录 `max_resolution` 和每页实际 `width` / `height`，image-token 估算也按实际页面尺寸计算。
- 第一版 768x1056 渲染仍然强行每页放 30 行，但在最小可读行高下画布只能容纳约 17 行，所以后面的行被画到图片外。
- 原型脚本已修复：现在会计算 `max_rows_per_image_at_resolution`，必要时自动降低 `rows_per_image` 并增加页数。
- 修复后 768x1056 可以完整显示，但 60 行样本从 2 页变成 4 页。页数增加后，低分辨率不一定更省 token。
- v10 后续优化目标应是 `page_count * image_tokens_per_page`，同时最大化每页可读信息量并保证内容完整可见。分辨率只是一个 knob，其他 knob 包括 rows/page、列选择、字体大小、行高、边距、换行策略、长文本是否单独做 focused preview。

定性结果：

- 高分辨率预览页在表格级和行级都清晰可读。
- 图片中可见的 urgency 信号包括 emergency department、chest pain/STEMI、stroke symptoms、seizure、suicidal ideation、sepsis、pulmonary embolism、burn transfer、acute infection/injury 等。
- 按视觉 prompt 结构做的 dry run 已保存到 [prototypes/visual_preview_feasibility/visual_prompt_dry_run.json](prototypes/visual_preview_feasibility/visual_prompt_dry_run.json)。其中恢复出的候选 facet 包括 acute emergency pattern、cardiopulmonary red flags、neurologic/psychiatric crisis、infection/systemic severity、urgent escalation 和 department context。
- 图片预览足以支持 schema planning 和 candidate facet discovery。
- 图片预览不适合做精确逐行 tagging 或计算，因为单元格可能被截断，模型 OCR 也可能不稳定。

下一步验证动作：

用支持视觉输入的真实 host model，把 [prototypes/visual_preview_feasibility/visual_prompt.md](prototypes/visual_preview_feasibility/visual_prompt.md) 和两张 PNG 一起跑一遍，并和使用 [prototypes/visual_preview_feasibility/equivalent_text_preview.json](prototypes/visual_preview_feasibility/equivalent_text_preview.json) 的 text-only prompt 做对比。

第一步验收标准：

- vision run 返回的 candidate facets 与 text-only run 在主要紧急度信号上有明显重叠。
- vision run 明确标注 strict tagging / counting 不安全，必须回到 raw data。
- 在加入 provider-specific image-token accounting 后，prompt-body text reduction 仍然明显。
- 至少在两个数据集上保持图片可读：一个结构化程度较高的表，一个长文本表。

## Step 2：定义 v10 Artifact Contract

新增 skill-owned artifact 类型：`visual_preview`。

建议的 workdir 文件结构：

```text
<workdir>/visual_preview/
  visual_preview_manifest.json
  overview_page_001.png
  overview_page_002.png
  chunk_<chunk_id>_page_001.png
  text_fallback_preview.json
```

Manifest 建议结构：

```json
{
  "kind": "visual_preview",
  "skill_version": "skill_v10",
  "mode": "fixed_resolution_table_images",
  "source_table": "...",
  "query": "...",
  "resolution": {"width": 1600, "height": 2200},
  "row_sampling": {"strategy": "text_length_stratified", "rows": 60},
  "columns": ["..."],
  "pages": [{"path": "overview_page_001.png", "rows": [0, 1, 2]}],
  "limitations": [
    "lossy visual preview",
    "not authoritative for strict tagging",
    "not authoritative for exact counts or numeric calculations"
  ],
  "raw_data_required_for": ["tagging", "exact_counts", "joins", "numeric_calculation"]
}
```

Manifest 和 PNG 页面应该通过现有 artifact manifest 机制注册，这样 traces 可以像引用 `execution_plan`、`specs`、`tags` 一样引用 visual preview。

## Step 3：增加 Renderer 模块

建议新增 reusable v10 模块：

```text
skill-v10/scripts/visual_preview.py
```

职责：

- 优先接收 `host_executor.py` 已经加载好的 DataFrame，避免在 frame 已存在时重复读文件。
- 按 evidence-column priority 选择预览列。
- 用 text-length stratified sampling 加可选 focus / target contrast sampling 选择 overview rows。
- 渲染固定分辨率页面，保证稳定字体、稳定行高、最大单元格字符数、清晰 row id。
- 当 host model 或 CLI 不支持图片时，输出 text fallback。
- 记录 metrics：行数、列数、页数、PNG bytes、等价 text chars、粗略 text-token estimate。
- 自动检查画布容量，防止行被画到图片外面。

这个模块应该独立于 tagging 和 merge，不参与严格标签生成。

## Step 4：扩展 Planning 输出

在 v10 的 `run_tapp.py` planning 输出中加入 `visual_preview` block：

```json
{
  "visual_preview": {
    "enabled": true,
    "strategy": "overview_plus_category_chunks",
    "resolution": {"width": 1600, "height": 2200},
    "overview_rows": 60,
    "chunk_rows": 100,
    "max_pages_per_prompt": 3,
    "use_for": ["inspect", "categorization", "review", "analysis_preview"],
    "not_for": ["tagging", "merge", "exact_counts"]
  }
}
```

Planner policy：

- 当模型支持 vision，并且文本预览字符数超过阈值时启用 visual preview。
- 当模型是 text-only 时禁用图片，回退到 text fallback。
- 第一阶段阈值保守设置，例如 `equivalent_text_preview_chars >= 12000` 或 `p95 evidence chars >= 120`。
- 第一阶段默认 resolution 使用 `1600x2200`，先保证质量和完整性，再用真实模型报告的 image tokens 做 resolution/layout sweep。

## Step 5：接入 Categorization

v9 中最自然的插入点位于 [../skill-v9/scripts/host_executor.py](../skill-v9/scripts/host_executor.py)：

- `_build_text_items(...)`
- `_categorize(...)`
- map-reduce categorization 内部的 `invoke_proposal(...)`
- `_run_consolidation(...)` 和 final selection payload 构造处

v10 行为：

- 对 `single_pass` categorization，附加 overview preview images 和 compact manifest，同时保留 text fallback。
- 对 `map_reduce` 的 `chunk_proposal`，尽可能为同一 row chunk 渲染 chunk preview images。
- 对 `global_consolidation`，默认不附加 raw row images；consolidation 应该消费 compact proposal JSON。
- 对 `final_selection`，可以附加 overview images 和 consolidated facets，帮助模型剔除 generic 或 non-taggable facets。

Prompt 修改：

- 在 `prompts/categorization.md` 和 `prompts/categorization_large_scale.md` 增加 visual-preview section。
- 明确要求模型只把图片用于 semantic discovery 和 data-shape preview。
- 要求每个 candidate facet 声明 strict tagging 是否需要 raw data。大多数文本语义 facet 应该标为 `true`。

## Step 6：Tagging 必须继续以 Raw Data 为准

不要用图片替代 `_tag_specs(...)` 中的 row `TextItems`。

允许的 v10 用法：

- 把 preview metadata 用于解释某个 facet 为什么被选中。
- 在调试 tag failure 时，把图片作为辅助上下文，而不是标签来源。

禁止的 v10 用法：

- image-only row labels。
- image-derived exact row indices。
- image-derived exact counts for merge gates。
- 当 source table 可以直接读取时，使用 image-derived numeric values。

v9 merge path 继续作为 row-index integrity、coverage、closed vocabulary 和输出表格的最终权威。

## Step 7：增加 Analysis Preview Path

对下游 analysis reading，v10 可以生成以下图片预览：

- 原始输入表 overview。
- merge 后 augmented table overview。
- facet distribution summary 小表。
- quality review 中的 error / unknown rows。

这个场景非常适合 visual preview，因为 analysis reading 通常需要上下文、模式和对比，而不是精确逐行标签。

## Step 8：Benchmark 设计

最小实验矩阵：

- v9 text-only baseline。
- v10 visual preview + raw-data tagging。
- v10 text fallback，使用同样 renderer-sampled rows。

需要测量：

- Categorization prompt-body characters / tokens。
- Provider-reported input tokens，包括 image tokens。
- Categorization 阶段 wall time。
- JSON failure / retry rate。
- 最终 spec 数量和相对 reference packages 的 expected-column recall。
- Tagging accuracy / coverage 必须持平或提升。

停止条件：

- 如果目标模型的 image-token accounting 在常见数据集上高于等价文本预览，则 visual preview 只保留为可选路径。
- 如果图片预览导致 candidate facets 丢失重要 rare signals，则增加 hybrid sampling 或保留少量 text excerpt payload。
- 如果 vision output 编造数据中不可见的 facets，则加强 prompt 约束，并要求 review / spec normalization 前必须做 raw-data verification。

## 实施顺序

1. 保留当前 prototype，用真实 vision model 在至少两个数据集上跑 `visual_prompt.md`。
2. 只有当第一步真实 vision run 成功后，再把 `skill-v9` 复制为 `skill-v10` 主体。
3. 增加 `scripts/visual_preview.py` 和图片生成 smoke tests。
4. 扩展 `execution_plan.json`，加入 `visual_preview` policy。
5. 在 evidence-column selection 之后、categorization 之前，把 visual-preview generation 接入 `augment-e2e`。
6. 更新 categorization prompts 和 payload construction。
7. 为 preview pages 和 manifest 增加 trace / artifact registration。
8. 在小数据集对上跑 v9 vs v10，检查 `specs.json`、tag outputs 和 merge reports。
9. 只有在 strict tagging parity 保持后，再扩展到 Lab8 benchmark matrix。

## 当前建议

继续推进 v10 staged prototype。图片预览对于减少 prompt-body text、压缩数据预览上下文、加速 schema planning 有明显潜力，但严格表格增强链路必须继续 raw-data-based。

第一阶段默认采用 `1600x2200` 高分辨率预览，原因是它已经验证可读、完整、页数少。低分辨率可以作为后续 layout sweep 的候选，但不作为当前默认。v10 应把 visual preview 视为上下文压缩层，而不是数据权威层。