---
name: nepu-ppt-template
description: Create Northeast Petroleum University (东北石油大学 / NEPU / 东油) style editable PowerPoint decks from research papers, DOCX, notes, outlines, reports, datasets, course materials, or draft slides. Use when the user asks for 东北石油大学, 东油, NEPU, school-branded PPT, academic report slides, seminar decks, thesis defense slides, group meeting slides, journal club, 文献汇报, paper-to-slides, course presentation decks, template selection, speaker notes, 演讲稿, 备注, data visualization, scientific charts, Nature-style figures, publication-quality Python plotting, editable flowcharts, structure diagrams, visual QA, web text/image acquisition, or converting Chinese research writing into a polished editable NEPU-style presentation.
---

# NEPU PPT Template

为东北石油大学（Northeast Petroleum University，简称 NEPU / 东油）师生创建可编辑的演示文稿。本项目非东北石油大学官方发布；使用或再分发前请参见 [ASSET_NOTICE.md](ASSET_NOTICE.md)。

## 快速开始

1. 创建工作区：`python scripts/create_workspace.py ./my-nepu-deck --profile academic-report --quality auto`
2. 将素材放入 `source/`、`assets/logos/`、`assets/templates/`、`assets/fonts/`
3. 识别场景：学术汇报 / 答辩 / 课程展示 / 学生活动 / 课题组会 / 行政党建 / 文献汇报
4. 选风格 → [references/nepu-template-selection.md](references/nepu-template-selection.md)
5. 构建可编辑幻灯片，按需参考子流程：
   - 流程图 → [references/diagram-workflow.md](references/diagram-workflow.md)
   - 数据图表 → [references/data-visualization.md](references/data-visualization.md)（**先建 figure contract 再写代码**）
   - 网页素材 → [references/web-content-acquisition.md](references/web-content-acquisition.md)
   - 演讲稿 → [references/speaker-notes.md](references/speaker-notes.md)
   - 修订已有 PPT → [references/revision-safety.md](references/revision-safety.md)
6. 结构审计 + 视觉自审 → [references/visual-qa.md](references/visual-qa.md)
7. Office 验证（按需）→ [references/office-compatibility.md](references/office-compatibility.md) + `scripts/office_bridge.ps1`

## 质量优先的提速规则

默认使用 `auto`：普通任务进入 `standard`，答辩自动进入 `rigorous`。两档都保留结构审计和视觉 QA，只跳过不影响质量的重复工作：

- **按需加载**：只读取当前任务需要的 reference；不要预读全部参考资料、图集或演示文件。
- **按需资源**：工作区默认仅复制 logo。模板和字体直接从技能目录读取，确定使用后只复制所选文件；不要复制全部约 320 MB 资源。
- **一次构建，一次必检**：生成后运行 `scripts/validate_pptx.py`，渲染一次全 deck 并检查 contact sheet；对图表、表格、流程图、密集文本页查看全尺寸预览。
- **发现缺陷才重生成**：必须修复 high 缺陷和可修复的 medium 缺陷并重新验证；若首轮无这些缺陷，不做形式化的二次生成。
- **自动升级 `rigorous`**：论文/文献汇报、答辩、科研评审、复杂图表/流程图、已有 PPT 修订，或用户明确要求高质量时，执行完整视觉复核和修订循环。
- **真正按需**：演讲者备注仅在用户要求时生成；网页采集和新科研图仅在任务内容确实依赖或用户要求时执行。打开失败、兼容性敏感或用户要求时才运行 Office/WPS 验证。
- **禁止无关任务**：生成用户 PPT 时不要运行 `run_evals.py`、`generate_gallery.py`，也不要遍历或复制未使用模板。

## 核心行为准则

- 理解源材料，提取论点主线 (claim spine)，而非机械复制段落。
- 产出可编辑 PPTX，非全页截图。默认 16:9。
- **保守修订模式**：对已有 PPT 保留好内容，仅修复可验证问题。每次修订创建带时间戳新版本文件，不覆盖源文件。
- **论文输入**：从 PDF 提取论证主线，分类论文类型，裁剪图表为证据非装饰。
- **演讲者备注**：仅在用户要求时生成并插入 PPT 备注区；用户修正过的页面锁定不动。
- **图片习惯追踪**：学习用户插入的图片风格，后续修订保持一致性。
- **科研绘图**：Python (matplotlib + seaborn)，使用 `scripts/plot_style.py`。
- **流程图**：原生 PowerPoint 形状优先，保持可编辑。

## 模板选择

选择前阅读 [references/nepu-template-selection.md](references/nepu-template-selection.md) 和 [references/nepu-bundled-assets.md](references/nepu-bundled-assets.md)。

| 风格 | 场景 |
|---|---|
| `petro-blue` | 学术汇报、组会、课程展示 —— 白底蓝调，清晰克制 |
| `nepu-red` | 校庆、学院大会、党建 —— 庄重红色，工业仪式感 |
| `petro-gold` | 答辩、科研评审、重大项目 —— 深蓝底金缀，严谨正式 |
| `oilfield-green` | 学生活动、招生、社团 —— 黑土绿调，青春活力 |
| `clean-white` | 文字密集综述、研究梳理 —— 极简留白，矩阵友好 |

多模板时选最匹配受众的，非"最好看"的。

## 源材料转换流程

详见 [references/authoring-workflow.md](references/authoring-workflow.md)。核心步骤：

1. 提取标题、受众、目的和源内容章节。
2. 撰写论点主线：每页一句话，听众看完应相信什么。
3. 为每个论点匹配合适的证明对象（图表/表格/机理/时间线/矩阵/引用/视觉对比）。
4. 重写为演讲语言：缩短段落、列表转分组论点、表格转矩阵、机理转流程。
5. 应用 NEPU 风格体系 → [references/nepu-style-system.md](references/nepu-style-system.md)。

## Figure Contract（绘图前必建）

每张科研图表从 contract 开始，非代码开始：

1. **核心结论**：一句话带动词，听众看完应相信什么。
2. **图表原型**：`quantitative grid` / `schematic-led composite` / `image plate + quant` / `asymmetric mixed-modality`。
3. **后端**：Python (`matplotlib`+`seaborn`)，使用 `scripts/plot_style.py` 统一 NEPU 样式。
4. **面板映射**：每块面板回答一个独特问题。
5. **导出合同**：尺寸、格式（SVG/PDF/TIFF）、统计量、数据溯源。Python 必设 `svg.fonttype='none'`。

详见 [references/data-visualization.md](references/data-visualization.md) 和 [references/backend-selection.md](references/backend-selection.md)。

## 幻灯片构图

### 构图角色（每页选一种，避免全 deck 同布局）

- `figure-dominant`：图表主体，文字为边缘注释。
- `process-wide`：全宽流程图 + 小型阶段标签。
- `claim-led`：一句强力主张 + 2-3 支撑片段。
- `comparison`：表格/图表 + 单一结论行。
- `discussion`：开放式布局，锐利提示。

### 布局适应规则（不以 50/50 为默认）

从图表宽高比、密度和论证角色选择：
- 宽且复杂 → 全宽。纵向 → 高图+窄文字轨。需横向空间 → 上下堆叠。
- 一侧主导 → 非对称（70/30、75/25）。仅需少量注释 → 紧凑视觉+标注。
- **1:1 等权为例外，非默认。**

### 反模板设计规则

避免 AI 模板感：❌ 三等分卡片 ❌ 指标药丸行 ❌ 固定右解释轨 ❌ 嵌套矩形假仪表板 ❌ 泛型"问题/方案/影响"网格。

改为：让图表拥有整个页面、用单行大号引用式主张、用小边缘注释代替大解释框。≥5 张幻灯片共享同一构图时重新设计。

## 排版与文本预算

| 层级 | 字号 | 规则 |
|---|---|---|
| 标题 | 24-32 pt | 写结论非话题标签，首选一行 |
| 正文 | 12-16 pt | 2-3 要点，每个 ≤18 中文字或 8-10 英文词 |
| 来源/说明 | 7-9 pt | 安静不争抢 |

文本溢出时：缩短文字、增大文本框、或拆分幻灯片。不以缩小文字为代价。

## Nature 风格页面构图

- 每张幻灯片一个主导视觉。默认非对称布局。
- 多子面板用小面板标签 (a, b, c)。跨面板重复类别用直接标注或共享图例。
- 跨幻灯片重用同一克制色板；绿/红仅用于方向性变化。
- 示意图+数据并存时，一个主导、另一个验证。
- 常规图表幻灯片保持浅色；深色背景仅用于图像板。
- 避免装饰框、假卡片、对齐双栏支架。

## 自审修订循环

每版 PPTX 至少一轮显式检查，不可初稿直接交付：

1. 结构审计 + 渲染检查 → 2. 列出缺陷+级别+幻灯片号 → 3. 修复 high/可修复 medium → 4. 有修复时重新生成并验证

首轮检查未发现 high 或可修复 medium 缺陷时，可直接交付，不为满足流程而重复生成。

| 级别 | 标准 | 处理 |
|---|---|---|
| `high` | 裁剪科学证据、不可读主证据、文字/图表重叠、文字溢出、错误顺序、捏造声明 | **必须修复** |
| `medium` | 过密幻灯片、僵硬 AI 布局、弱裁剪边距、脱离标题、过度重复布局、缺演讲者备注 | 尽量修复 |
| `low` | 轻微对齐、色板微调、密集图表可选拆分 | 记录推迟 |

详见 [references/visual-qa.md](references/visual-qa.md) 和 [references/quality-gates.md](references/quality-gates.md)。

## 设计默认值

详见 [references/nepu-style-system.md](references/nepu-style-system.md)。核心：

- 色板：石油蓝 `#00508F` / 工业红 `#C41230` / 金色 `#CFB87C` / 墨色 `#1A1A2E`
- 字体：Microsoft YaHei / DengXian / Source Han Sans SC → Arial 回退
- 使用精确 logo 文件，不重绘。图表克制，工业红仅作强调。

## 资源索引

| 类别 | 文件 | 用途 |
|---|---|---|
| 工作流 | `references/authoring-workflow.md` | 源材料转换 + 论文输入通道 |
| | `references/nepu-template-selection.md` | 风格选择规则 |
| | `references/nepu-style-system.md` | 布局/颜色/排版默认值 |
| | `references/revision-safety.md` | 非破坏性修订 |
| 科研绘图 | `references/data-visualization.md` | Figure contract + Python/R 双后端 + 审美集成 + 审稿人风险 |
| | `references/backend-selection.md` | Python vs R 选择决策 |
| | `references/api.md` | Python API 常量与辅助 |
| | `references/chart-types.md` / `common-patterns.md` / `design-theory.md` / `tutorials.md` / `demos.md` | 图表模式与教程 |

| 图表视觉 | `references/diagram-workflow.md` | 可编辑流程图 |
| | `references/visual-qa.md` | 视觉 QA + 质量关卡 |
| | `references/nature-2026-observations.md` / `qa-contract.md` | Nature 原型 / QA 合同 |
| | `references/animation.md` | 克制动画/过渡指南 |
| 内容 | `references/web-content-acquisition.md` / `speaker-notes.md` / `office-compatibility.md` / `nepu-bundled-assets.md` | 网页采集 / 备注 / 兼容性 / 内置资源 |
| 脚本 | `scripts/create_workspace.py` | 创建工作区 |
| | `scripts/slide_builder.py` | **高层幻灯片 API**（封面/章节/图表页/矩阵/结论） |
| | `scripts/plot_style.py` | Matplotlib NEPU 样式（自动字体检测） |
| | `scripts/web_collect.py` | 网页图文采集 |
| | `scripts/validate_pptx.py` | **跨平台 PPTX 结构校验**（无需 Office） |
| | `scripts/office_bridge.ps1` | Office/WPS COM 验证 |
| | `scripts/run_evals.py` / `scripts/generate_gallery.py` | 评估运行器 / 画廊生成 |
| 资源 | `assets/logos/nepu/` | 内置 logo（见 ASSET_NOTICE.md） |
| | `assets/templates/nepu-civilization-office/` | **7 套内置 PPTX 模板** |
| | `assets/chart-atlas/` / `assets/figures4papers/` / `assets/gallery/` | 图表参考 / 演示 / PPT 布局参考 |
| | `evals/evals.json` | 10 个评估用例 |
