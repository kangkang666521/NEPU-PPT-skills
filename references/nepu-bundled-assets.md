# NEPU 内置资源

本技能在 `assets/logos/nepu/` 下包含用户提供的 NEPU logo 文件。

## Logo

文件夹: `assets/logos/nepu/`

- `nepu1.png` — NEPU logo 变体 1
- `nepu2.png` — NEPU logo 变体 2

## PPT 模板

当前无 NEPU 官方 PPTX 模板内置。**强烈建议 NEPU 用户提供自己院系/实验室/机关的授权 PPTX 模板**，放入工作区的 `assets/templates/` 中。技能在选择模板时会优先使用用户提供的模板。

无模板时的默认策略：使用空白 16:9 PPTX + NEPU 石油蓝色板（`#00508F`）+ NEPU logo 手建风格。详见 [nepu-style-system.md](nepu-style-system.md) 和 [nepu-template-selection.md](nepu-template-selection.md)。

## 字体

当前无内置字体包。技能会使用系统已安装的中文字体（Microsoft YaHei、DengXian、Source Han Sans SC 等）。

用户可自行在任务工作区的 `assets/fonts/` 中放入字体文件。

## 技能如何使用它们

运行 `python scripts/create_workspace.py` 时：

- 内置 NEPU logo（`assets/logos/nepu/`）复制到工作区。
- 使用 `--no-bundled-assets` 可创建空工作区，自行提供所有资源。
- 已有文件不会被覆盖。

## 重要提醒

- 本项目非东北石油大学官方发布。
- 内置 logo 为便利性素材，公开、商业、机构或再分发使用前需确认授权。
- 如不确定是否可使用某素材，请替换为自己的授权文件。
- 在大庆精神/铁人精神等红色主题场景中，注意使用授权的历史和人物图像。
