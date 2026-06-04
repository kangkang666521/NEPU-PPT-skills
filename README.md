# NEPU PPT 模板技能

为东北石油大学（Northeast Petroleum University，简称 NEPU / 东油）师生创建可编辑的 PowerPoint 演示文稿。

**核心能力**：源材料→论点主线转换、非破坏性版本管理、原生可编辑流程图、Nature 风格科研图表（Python/matplotlib）、视觉 QA 自审修订、网络图文采集、演讲者备注同步、7 套内置 PPTX 模板。

> 个人项目，非东北石油大学官方发布。内置资源仅为便利性提供；公开、商业或再分发使用前请确认权限。详见 [ASSET_NOTICE.md](ASSET_NOTICE.md)。

## 项目结构

```
├── SKILL.md                     ← 技能入口（AI 加载）
├── AGENTS.md                    ← 项目记忆文件
├── README.md
├── ASSET_NOTICE.md
├── requirements.txt             ← 独立运行所需 Python 依赖
│
├── scripts/
│   ├── create_workspace.py      ← 引导式创建工作区
│   ├── slide_builder.py         ← 高层幻灯片 API（封面/章节/图表/矩阵/结论）
│   ├── plot_style.py            ← Matplotlib NEPU 样式 + 自动字体检测
│   ├── web_collect.py           ← 公开网页图文采集
│   ├── validate_pptx.py         ← 跨平台 PPTX 结构校验（无需 Office）
│   ├── office_bridge.ps1        ← Office/WPS COM 兼容性验证
│   ├── self_check.py             ← 项目级烟雾检查
│   ├── run_evals.py             ← 评估用例运行器
│   └── generate_gallery.py      ← 布局参考 PPTX 生成
│
├── references/
│   ├── authoring-workflow.md    ← 源材料→幻灯片 + 论文输入通道
│   ├── nepu-template-selection.md ← 风格选择 + 7 套内置模板映射
│   ├── nepu-style-system.md     ← 颜色/字体/排版/Logo 规范
│   ├── revision-safety.md       ← 非破坏性版本管理
│   ├── data-visualization.md    ← Figure contract + 科研绘图全流程
│   ├── backend-selection.md     ← Python 后端规范
│   ├── diagram-workflow.md      ← 可编辑流程图/结构图
│   ├── visual-qa.md             ← 视觉 QA + 质量关卡
│   ├── animation.md             ← 克制动画/过渡指南
│   ├── speaker-notes.md         ← 演讲者备注生成与锁定
│   ├── web-content-acquisition.md ← 网络素材采集规范
│   ├── office-compatibility.md  ← PowerPoint/WPS/LibreOffice 验证
│   ├── nepu-bundled-assets.md   ← 内置资源清单
│   ├── api.md / chart-types.md / common-patterns.md / design-theory.md / tutorials.md / demos.md
│   ├── nature-2026-observations.md / qa-contract.md
│   ├── figure-contract.md       ← → data-visualization.md（重定向）
│   └── quality-gates.md         ← → visual-qa.md（重定向）
│
├── assets/
│   ├── logos/nepu/              ← 内置 NEPU logo PNG
│   ├── templates/nepu-civilization-office/ ← 7 套内置 PPTX 模板
│   ├── chart-atlas/             ← 10 种图表类型图集
│   ├── figures4papers/          ← 9 个 Python 绘图示例
│   ├── gallery/                 ← 5 张 Nature 多面板图 + slides/ 布局参考 PPTX
│   └── fonts/                   ← HarmonyOS Sans SC 字体
│
└── evals/
    └── evals.json               ← 10 个 AI 行为评估用例
```

## 快速开始

```bash
# 1. 创建任务工作区
python scripts/create_workspace.py ./my-deck --profile academic-report

# 2. 将素材放入工作区 source/ 目录

# 3. AI 读取源材料 → 构建论点主线 → 选择模板 → 生成 PPTX

# 4. 交付前校验（可选）
python scripts/validate_pptx.py output/versions/deck.pptx

# 5. 修改技能项目后运行烟雾检查
python scripts/self_check.py
```

工作区默认只复制内置 logo，避免每次任务重复复制约 320 MB 的全部模板和字体。需要全部资源时使用 `--assets all`；`--quality auto` 会让答辩自动进入严格模式，其他高风险交付使用 `--quality rigorous`。无论哪种质量模式，最终 PPTX 都应完成结构审计和至少一轮渲染视觉检查。

## 脚本速览

| 脚本 | 用途 |
|---|---|
| `create_workspace.py` | 一键创建标准化任务工作区（目录+种子文件+manifest） |
| `slide_builder.py` | `NepuSlideBuilder` — 封面/章节/claim页/图表页(3布局)/矩阵/要点/结论/图片网格 |
| `plot_style.py` | NEPU 色板常量、Matplotlib rcParams、自动 CJK 字体检测、PPT 尺寸预设 |
| `web_collect.py` | 公开网页文本/图片采集，自动编码检测，来源记录 |
| `validate_pptx.py` | 纯 Python 结构校验：边界/溢出/占位符/布局重复/图片尺寸 |
| `office_bridge.ps1` | Windows 下调 PowerPoint/WPS COM 验证和重新保存 |
| `self_check.py` | 检查主题构建、非覆盖保存、资源错误、结构验证、网页解析与质量模式 |
| `run_evals.py` | 评估用例验证和筛选 |
| `generate_gallery.py` | 生成 NEPU 风格布局参考 PPTX |

## 参考资料索引

### 工作流
| 文件 | 内容 |
|---|---|
| `authoring-workflow.md` | 源材料→幻灯片完整流程 + 论文输入通道 |
| `nepu-template-selection.md` | 5 种风格配置 + 7 套内置模板映射 + 决策规则 |
| `nepu-style-system.md` | 颜色体系、字体、版式家族、Logo 规范 |
| `revision-safety.md` | 版本化命名、保守修订模式、图片习惯追踪 |

### 科研绘图（Python/matplotlib）
| 文件 | 内容 |
|---|---|
| `data-visualization.md` | Figure contract、图表原型、面板逻辑、审美集成、QA |
| `backend-selection.md` | Python 默认栈与导出规范 |
| `api.md` | Nature Figure Python API 常量与辅助 |
| `chart-types.md` `common-patterns.md` `design-theory.md` `tutorials.md` `demos.md` | 图表模式、布局、教程 |

### 视觉与内容
| 文件 | 内容 |
|---|---|
| `diagram-workflow.md` | 可编辑流程图/结构图规则 |
| `visual-qa.md` | 视觉 QA 循环 + Package/Presentation 检查 + 缺陷分级 + 程序化审计 |
| `animation.md` | 克制动画/过渡指南（Appear/Fade/Wipe） |
| `speaker-notes.md` | 演讲者备注生成、插入、同步、锁定 |
| `web-content-acquisition.md` | 公开网页采集、出处记录、版权审查 |
| `office-compatibility.md` | Office/WPS/LibreOffice 验证工作流 |

## 安装

Codex 桌面运行时通常已提供文档与演示处理依赖。需要在独立 Python 环境运行脚本时：

```bash
python -m pip install -r requirements.txt
python scripts/self_check.py
```

将以下提示复制到 Codex 中：

```text
请帮我安装这个技能到本地https://github.com/kangkang666521/NEPU-PPT-skills。之后当我需要做东北石油大学（东油/NEPU）风格 PPT 时，请优先调用它：先理解我的材料，再根据场景选择合适的风格，保留我已经修改好的内容，必要时整理公开网页图文并记录来源，渲染预览检查遮挡和颜色问题，并生成一份可编辑的 PPTX。
```
