# Backend: Python (matplotlib + seaborn)

All scientific figures for NEPU PPT decks are drawn with Python.

## Default Stack

- Core plotting: `matplotlib`
- Statistical plots: `seaborn`
- Layout: `subplot_mosaic`, `GridSpec`
- Data: `pandas`, `numpy`, `statsmodels`
- Images: `matplotlib.imshow`, `skimage`, `tifffile` when needed
- Export: `fig.savefig(... .svg/.pdf/.tiff)`, `svg.fonttype='none'`, `pdf.fonttype=42`

Use the bundled `scripts/plot_style.py` helper for NEPU palette integration and auto font detection.

## Export Contract

Every figure must produce:
- `chart-name.png` (200-300 dpi) for reliable cross-platform PPT display
- `chart-name.svg` or `chart-name.pdf` for future edits
- Data file + script that regenerates the chart

## If matplotlib Is Unavailable

If `matplotlib` or a required Python plotting package is not installed, do not fall back to any other plotting backend (R, plotly, etc.). Stop, report the missing dependency, and provide the Python-only script plus install instructions.
