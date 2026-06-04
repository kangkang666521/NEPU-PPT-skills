# NEPU PPT Template Skill

为东北石油大学（NEPU/东油）师生创建可编辑 PowerPoint 演示文稿的技能项目。

## Project

- 主入口：`SKILL.md`（加载到 Codex 上下文的技能定义，~10KB）
- 引用文档：`references/`（按需读取）
- 工具脚本：`scripts/`（Python/PowerShell）
- 内置资源：`assets/`（logos、模板、字体、图表参考）
- 评估：`evals/evals.json`

## Commands

```bash
# 创建工作区
python scripts/create_workspace.py ./output-dir --profile academic-report

# 独立 Python 环境安装依赖
python -m pip install -r requirements.txt

# 网页采集
python scripts/web_collect.py ./output-dir URL1 URL2 --download-images

# Office 兼容验证（PowerShell）
powershell -File scripts/office_bridge.ps1 -InputPptx file.pptx -ValidateOnly

# 项目烟雾检查
python scripts/self_check.py
```

## Architecture

- `SKILL.md`：技能入口，含快速开始流程、核心操作规则、模板选择、figure contract、构图规则、排版预算、自审循环、资源索引
- `references/`：按域组织的详细参考（authoring-workflow、data-visualization、visual-qa、revision-safety、diagram-workflow、web-content-acquisition、speaker-notes、office-compatibility、nepu-style-system、nepu-template-selection 等）
- `scripts/create_workspace.py`：引导式工作区创建（目录+种子文件+manifest）
- `scripts/plot_style.py`：Matplotlib NEPU/Nature 样式（色板常量、rcParams、figure 尺寸、保存辅助）
- `scripts/web_collect.py`：公开网页文本/图片采集（HTML 解析、编码检测、来源记录）
- `scripts/office_bridge.ps1`：PowerPoint/WPS COM 自动化验证和重新保存
- `scripts/self_check.py`：无需 pytest 的项目级烟雾检查

## Conventions

- SKILL.md 保持精简（≤12KB），详细规则放 references/，通过链接引用
- Python 脚本用 `from __future__ import annotations` + 类型注解
- 所有路径操作用 `pathlib.Path`
- JSON manifest 文件用 `ensure_ascii=False, indent=2`
- 版本化输出文件名模式：`<stem>__YYYYMMDD-HHMMSS__rNN.pptx`
- 保守修订为默认：不覆盖源文件/用户编辑过的 PPTX
- 科研绘图前先建 figure contract；Python/R 后端选定后不可交叉渲染

## Notes
