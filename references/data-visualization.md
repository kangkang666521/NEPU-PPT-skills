# Data Visualization For NEPU PPT

Use this reference when a deck includes CSV, Excel, statistical tables, experimental data, survey results, chart screenshots, manuscript figures, or requests such as "make the chart better", "Nature style", "科研绘图", "数据处理", "图表美化", or "更适合学术汇报".

## Core Standard

Every chart should support one slide claim. Make it readable in a projected PPT, visually restrained, and reproducible from stored data and code when possible.

Use a Nature-like scientific style as a direction, not as a journal claim:

- clean axes and thin rules
- no decorative gradients, shadows, or 3D effects
- restrained color-blind-safe palette
- direct labels when they reduce legend searching
- consistent typography and capitalization
- short source notes when data are synthesized or user-provided
- enough contrast for projection

## Figure Contract — Plan Before Plotting

Every chart or figure task starts from a contract, not from code. Before writing any plotting script, establish:

```text
Core conclusion:    one sentence with a verb — what the audience must believe
Figure archetype:   quantitative grid / schematic-led composite / image plate + quant / asymmetric mixed-modality
Target use:         slide / poster / manuscript figure
Backend:            Python (matplotlib + seaborn)
Panel map:          a: [role], b: [role], c: [role]
Evidence hierarchy: hero evidence / validation evidence / controls
Statistics needed:  error bars, n, test type, confidence intervals
Source data:        origin and traceability
Reviewer risk:      what a skeptical reviewer would challenge first
```

**Core conclusion rules:**
- Must be one sentence with a verb: "Treatment X reduces Y by restoring Z", not "Treatment results".
- Every panel must answer a unique question. If removing a panel wouldn't weaken the argument, remove or merge it.
- Separate primary evidence from supporting evidence. Primary evidence gets the hero panel or clearest axis; controls and robustness panels should be visually quieter.

### Figure Archetypes

| Archetype | Use when | Hero panel | Supporting panels |
|---|---|---|---|
| `quantitative grid` | Claim is mainly numerical comparison | Optional dominant summary metric | Shared axes, aligned scales |
| `schematic-led composite` | Workflow/mechanism/device must be understood first | Left or top schematic, 35-60% of area | 2-4 quantitative validation panels |
| `image plate + quant` | Microscopy/imaging/histology leads the evidence | Image plate or representative image | Scale bars, crops, quantification |
| `asymmetric mixed-modality` | Combines schematic, raster, heatmaps, and quantitative plots | One panel spans rows/columns | Smaller panels ranked by evidence value |

### Panel Logic

Unless the story requires otherwise:
1. Establish the system: sample, method, cohort, device, or experimental design.
2. Show the main effect or primary comparison.
3. Show mechanism or localization.
4. Quantify the representative image or qualitative observation.
5. Add robustness, controls, subgroup, or sensitivity analysis.

## Native PPT vs Generated Figure

Use native PowerPoint charts when:

- the chart is simple: bar, line, scatter, pie/donut only if truly appropriate
- the user may need to edit values or labels inside PowerPoint
- the deck is business/admin/course-facing rather than manuscript-like

Use Python (matplotlib) outputs when:

- the chart needs publication-style polish
- there are multiple panels, error bars, confidence intervals, distributions, heatmaps, or dense annotations
- the source data should be reproducible
- the chart needs publication-grade export (SVG with editable text, PDF, high-DPI TIFF)

For generated figures, keep the data and code in the task workspace and insert the exported chart into PPT. If the user needs editability, also provide a simplified native PPT chart or a data table appendix.

## Workspace Pattern

For each important chart, create or maintain:

```text
figures/
  fig01_short_name/
    code/
    data/
    outputs/
    sources/
    README.md
```

Store:

- `code/`: one script that regenerates the chart.
- `data/`: CSV/JSON used directly by the script.
- `outputs/`: PNG for PPT, PDF/SVG for vector preservation when useful.
- `sources/`: a short note distinguishing user-provided data, cleaned data, reproduced metrics, and author-synthesized frameworks.
- `README.md`: chart purpose, command, output files, and source type.

Decide early whether labels should be in Chinese, English, or bilingual — this affects font choice, axis label length, and overall layout.

## Chart Type Guidance

- Trend over time: line chart or slope chart.
- Group comparison: bar chart with direct labels; use dot/interval plots for scientific comparisons.
- Distribution: box, violin, histogram, or ridgeline only when the audience can read it quickly.
- Relationship: scatter with modest fit line and annotation; avoid overplotting.
- Part-to-whole: stacked bar or small multiples; avoid pie charts unless categories are few and obvious.
- Process/mechanism: editable PPT flow or vector diagram, not a decorative infographic.
- Literature map or taxonomy: matrix, alluvial-like flow, or grouped table.
- Before/after or method comparison: paired dots, dumbbell chart, or two-column matrix.

## PPT Readability Rules

- Titles should state conclusions, not chart types.
- Axis labels must be readable at slide size.
- Avoid more than 5-7 visual groups on one slide.
- Prefer direct labels over legends when space allows.
- Use annotations to explain the one thing the audience should notice.
- Keep gridlines light and minimal.
- Avoid tiny footnotes; move details to speaker notes or appendix.
- For Chinese slides, use Microsoft YaHei, DengXian, Source Han Sans SC, Noto Sans CJK SC, or HarmonyOS Sans SC.

## Python Quick-Start (matplotlib)

Use the bundled `scripts/plot_style.py` helper for NEPU palette integration, or set rcParams directly.

**Mandatory — editable text in SVG output** (must appear at the top of every script):

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",     # keeps text as editable <text> nodes
    "pdf.fonttype": 42,         # editable TrueType text in PDF
    "font.size": 7,             # use 15-24 only for large slide-sized panels
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
```

Use `text.usetex = True` only when LaTeX is installed and math-rich labels require it.

### Publication-Grade Export

```python
def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.tiff", dpi=dpi, bbox_inches="tight")
```

Minimum outputs for PPT use:
- `chart-name.png`: 200-300 dpi for reliable cross-platform slide display.
- `chart-name.svg` or `chart-name.pdf`: vector copy for future edits.
- Data file + script that regenerate the chart.

## Color Policy

Prefer **unified method families across all panels** over maximal hue separation. For dense multi-panel figure pages, use one low-saturation family and reserve green/red mainly for gains, drops, and directional cues.

Use the NEPU palette first, then extend with color-blind-safe accents:

- NEPU blue: `#00508F`
- NEPU dark blue: `#00335C`
- NEPU red: `#C41230`
- NEPU gold: `#CFB87C`
- Ink: `#1A1A2E`
- Muted gray: `#6B778A`
- Safe teal: `#2A9D8F`
- Safe orange: `#E69F00`
- Safe purple: `#7B61A8`

Do not make every chart red/blue only. Use NEPU red as emphasis, not as the default fill for all categories.

For extended palettes, see [Nature Figure API reference](api.md) for domain-specific color families (NMI pastel, Nature imaging, clinical, genomics, materials).

## Inserting Charts Into PPT

- Use native PPT charts for simple editable values.
- Use PNG for reliable cross-platform display.
- Keep SVG/PDF next to the deck for future edits or publication reuse.
- Do not stretch charts; preserve aspect ratio.
- Put charts in a layout with enough label room.
- If the chart is dense, give it a full slide rather than squeezing it into a small card.
- Add source notes only when they help trust or interpretation.

## Chart Atlas

For concrete visual references of each chart type, see the bundled chart atlas under `assets/chart-atlas/`:

| Atlas | Chart type |
|---|---|
| `atlas-01-bar-charts.png` | Grouped and stacked bars |
| `atlas-02-line-trends.png` | Multi-line trend and slope charts |
| `atlas-03-heatmaps.png` | 2D heatmaps and correlation matrices |
| `atlas-04-scatter-bubble.png` | Scatter, bubble, and relationship plots |
| `atlas-05-radar-polar.png` | Radar and polar charts |
| `atlas-06-distributions.png` | Box, violin, histogram, ridgeline |
| `atlas-07-forest-interval.png` | Forest plots and interval charts |
| `atlas-08-area-stacked.png` | Area and stacked area charts |
| `atlas-09-image-plates.png` | Microscopy and imaging plates |
| `atlas-10-network-matrix.png` | Networks and adjacency matrices |

## Aesthetic Integration

- Use one neutral family, one signal family, and one accent family.
- Keep the same condition/method color across all panels.
- Prefer direct labels for stable line identities, channels, and fixed spatial regions.
- Use a shared legend area when repeated legends would waste space.
- Avoid equal-sized panels when the evidence is not equally important.
- Keep schematic colors and quantitative plot colors related. A schematic-led figure should look like one integrated argument, not a pasted collage.

## Reviewer-Risk Prompts

Before finalizing, ask what a skeptical reviewer would challenge:

- Is the sample size visible in the legend or source data?
- Are error bars, intervals, and statistical tests defined?
- Are axes comparable across panels that invite comparison?
- Are representative images quantified and traceable to raw files?
- Are image adjustments global and documented?
- Could the same conclusion be made from fewer panels?

## Privacy Rule

Keep the figure contract user-facing, but keep the working trail private. Do not mention private paths, source filenames, internal reference documents, template identifiers, or where a private draft came from unless the user explicitly asks for provenance.

## QA Checklist

Before delivery:

- The chart supports the slide claim (traceable to the figure contract).
- The data source is recorded with origin and traceability.
- Outputs can be regenerated from code/data when generated externally.
- Text and labels are readable in rendered slide previews.
- Colors are distinguishable in grayscale or for common color-vision deficiencies.
- Important chart text is either editable in PPT or reproducible from code.
- SVG exports have editable text (`svg.fonttype = 'none'`).
- Error bars, n, and statistical tests are defined and visible.
- The chart style matches the selected NEPU deck style.
- Panel labels (a, b, c) are present and readable on multi-panel figures.
