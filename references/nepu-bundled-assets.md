# NEPU 内置资源

本技能在 `assets/logos/nepu/` 下包含用户提供的 NEPU logo 文件。

## Logo

文件夹: `assets/logos/nepu/`

- `nepu1.png` — NEPU logo 变体 1
- `nepu2.png` — NEPU logo 变体 2

## PPT 模板

`assets/templates/nepu-civilization-office/` 提供 7 套便利性 PPTX 模板，但它们不是 NEPU 官方模板。**优先使用用户提供的院系/实验室/机关授权模板**；内置模板的场景映射见 [nepu-template-selection.md](nepu-template-selection.md)。

无合适模板时，使用空白 16:9 PPTX + NEPU 石油蓝色板（`#00508F`）+ NEPU logo 手建风格。详见 [nepu-style-system.md](nepu-style-system.md) 和 [nepu-template-selection.md](nepu-template-selection.md)。

## 字体

内置 HarmonyOS Sans SC 字体包可按需使用。优先使用系统已安装的中文字体（Microsoft YaHei、DengXian、Source Han Sans SC 等），避免每个任务复制或安装字体包。

用户可自行在任务工作区的 `assets/fonts/` 中放入字体文件。

## 技能如何使用它们

运行 `python scripts/create_workspace.py` 时：

- 默认只把内置 NEPU logo（`assets/logos/nepu/`）复制到工作区，避免每个任务重复复制大体积模板和字体。
- 确定使用某个模板或字体后，只复制所选文件；也可直接从技能目录读取。
- 使用 `--assets all` 可复制全部内置 logo、模板和字体。
- 使用 `--assets none` 或兼容参数 `--no-bundled-assets` 可创建空资源工作区。
- 已有文件不会被覆盖。

## 重要提醒

- 本项目非东北石油大学官方发布。
- 内置 logo 为便利性素材，公开、商业、机构或再分发使用前需确认授权。
- 如不确定是否可使用某素材，请替换为自己的授权文件。
- 在大庆精神/铁人精神等红色主题场景中，注意使用授权的历史和人物图像。
