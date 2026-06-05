# Authoring Workflow

Use this workflow to convert user materials into an editable NEPU-style presentation.

## 1. Understand The Task

Identify:

- audience: teacher, student, committee, lab, course, public event, school office
- format: report, defense, seminar, group meeting, lecture, activity recap
- language: Chinese, English, or bilingual
- desired length
- must-use logos or templates
- whether the final PPTX must remain fully editable

## 2. Extract The Source Structure

For DOCX or long Chinese drafts:

- extract headings
- identify tables and lists
- preserve essential numbers and citations
- find the central thesis
- mark material that belongs in appendix rather than main slides

Do not copy long paragraphs verbatim into slides.

**If the source is a research paper (PDF, preprint, article text, abstract, or reading notes), skip to [论文输入通道](#论文输入通道-paper-input-path) below** — it has its own extraction, classification, and argument-building pipeline.

## 3. Build A Claim Spine

Write one claim per slide. Each claim should say what the audience should believe after seeing the slide.

Common deck structures:

- academic review: topic -> literature map -> reality base -> mechanism -> risk/problem -> governance/solution -> future agenda
- thesis defense: question -> method -> data -> results -> contribution -> limitations -> conclusion
- group meeting: goal -> progress -> experiment -> issue -> next step
- course presentation: concept -> case -> analysis -> reflection -> takeaway
- activity report: theme -> highlights -> timeline -> participation -> outcomes -> closing

## 4. Choose Proof Objects

Use the proof object that best fits the claim:

- table for classification
- matrix for risk, comparison, or governance mapping
- mechanism chain for formation processes
- timeline for development stages
- chart for trend or proportion
- quote/case panel for qualitative material
- visual montage for campus or event storytelling

If the proof object depends on CSV, Excel, experimental data, statistics, or existing chart screenshots, read [data-visualization.md](data-visualization.md) before drawing or inserting charts.

If the proof object is a process, mechanism, architecture, governance path, or structure diagram, read [diagram-workflow.md](diagram-workflow.md) before drawing. Plan nodes and connectors before placing shapes.

If the proof object depends on public online information or images, read [web-content-acquisition.md](web-content-acquisition.md) before collecting material. Keep source records and permission notes.

## 5. Build Editable Slides

Use the user-provided template or the selected bundled template as the visual base. `scripts/slide_builder.py` is a scaffold for simple pages and smoke tests; for paper reports, defenses, and complex academic decks, customize layouts against the template instead of relying on the default builder patterns alone.

Prefer native PowerPoint objects:

- text boxes
- shapes
- editable tables
- native charts or editable chart-like primitives
- image layers for photos, logos, and complex figures

Avoid full-slide screenshots except for temporary references or explicitly image-based deliverables.

For diagrams, use native editable shapes/connectors whenever feasible. For web-supported images, keep source records and verify that placement does not block text or logos.

## 6. Quality-First Visual QA Before Delivery

Always run the structural audit and render the PPTX once for visual inspection using [visual-qa.md](visual-qa.md).

Check:

- text and image overlap
- blocked labels, footers, logos, and titles
- low color contrast
- text overflow and awkward Chinese wrapping
- chart/table readability
- diagram connector clarity and label readability
- user-locked content preservation

Use the contact sheet for the whole deck, then inspect full-size previews for risky slides: charts, tables, diagrams, dense text, cropped evidence, and image-heavy layouts. If no high or fixable medium defects are found, do not regenerate solely to satisfy a process step.

Upgrade to rigorous QA for paper reports, defenses, scientific reviews, complex evidence, existing-deck revisions, or when the user explicitly requests high quality.

## 7. Revise Without Overwriting

When the task is an update to an existing deck, do not regenerate from scratch unless the user asks for a full rebuild. Read the latest user-edited deck, preserve their manual changes, then create a new versioned file before applying the new request.

Use [revision-safety.md](revision-safety.md) for naming, revision logs, and image habit tracking.

---

## 论文输入通道 (Paper Input Path)

When the source is a research paper (PDF, preprint, article text, abstract, figure legends, or structured reading notes), use this specialized pipeline. The end deliverable is the same — an editable NEPU-style PPTX — but the extraction, argument-building, and figure-handling steps are paper-specific.

### P1. Extract Source Material

Extract, when available:
- title, authors, journal/preprint server, year, DOI
- field and subfield
- paper type (see P2)
- central problem and knowledge gap
- main claim or thesis
- study design, workflow, model, dataset, or experimental system
- key methods and controls
- main results and quantitative findings
- key figures, tables, and figure legends
- validation, robustness, ablation, or sensitivity analyses
- limitations and unresolved questions
- broader scientific, clinical, technical, environmental, or translational meaning

Use a two-pass reading strategy: first capture metadata, abstract, headings, figure legends, and table captions; then read only the result and methods pages needed to support the slides. Do not invent missing numbers, mechanisms, datasets, or figure details.

Toolchain: PyMuPDF for PDF extraction, Pillow for figure crops, python-pptx for slide authoring. Use `pathlib` paths and Office-safe fonts. Avoid OS-specific font paths or platform-specific file locations.

### P2. Classify the Paper

Identify the primary paper type and the best presentation logic:

| Paper type | Presentation logic | Default arc |
|---|---|---|
| Discovery / mechanism | `question-to-evidence` | phenomenon → unknown → hypothesis → design → evidence → model → limits |
| Methods / algorithm / tool | `problem-to-solution` | bottleneck → proposed method → workflow → benchmarks → ablation → reuse |
| Resource / dataset / atlas / omics | `workflow-to-validation` | need → design → QC workflow → landscape → validation → access |
| Clinical / population / intervention | `design-to-inference` | problem → question → design → endpoints → primary result → bias/limits |
| Materials / chemistry / engineering | `property-to-mechanism` | target → design → synthesis → characterization → performance → stability |
| Review / perspective | `evidence-map` | why now → framework → theme 1/2/3 → controversy → synthesis → future |
| Benchmark / evaluation | `problem-to-solution` | gap → benchmark design → metrics → baselines → analysis → limits |

### P3. Build the Chinese Presentation Plan

Default length: 12-16 slides for a 15-20 minute report. The default spine:

1. 标题页
2. 研究背景：为什么这个问题重要
3. 知识缺口 / 技术瓶颈
4. 论文核心问题与主张
5. 研究设计 / 技术路线 / 分析框架
6. 关键证据1
7. 关键证据2
8. 关键证据3
9. 验证、对照或稳健性证据
10. 机制模型 / 方法优势 / 综合框架
11. 创新点与可复用价值
12. 局限性与未解决问题
13. 总结与讨论

Adapt this structure to the paper type. Do not force every paper into the same template. For quick requests, prefer 10-14 slides.

### P4. Plan Visual Rhythm

Before creating slides, assign each slide a visual role. Choose from:

- `figure-dominant`: figure owns most of the slide; text is a quiet margin note or bottom strip
- `process-wide`: full-width workflow with small stage labels
- `claim-led`: one strong sentence with 2-3 supporting fragments, no fake cards
- `comparison`: table/chart or two evidence blocks with a single conclusion line
- `discussion`: open layout with a few sharp prompts, not a dense bullet page

Do not create the whole deck from one generic layout family. If five or more slides share the same composition, redesign at least some of them.

### P5. Select Figures as Evidence

Prioritize figures that carry the paper's argument:
1. design/workflow
2. main evidence
3. validation or robustness
4. mechanism/model/synthesis
5. practical or conceptual implication

Prefer a few readable key panels over many unreadable full figures. For a standard 10-14 slide journal-club deck, usually select 4-8 figure/table assets.

### P6. Extract and Crop Figure Assets

- Extract original images from PDF or source package for selected figures only.
- Render high-resolution page images only for pages containing selected figures or tables.
- Crop relevant panels when full figures are too dense.
- Keep original data visuals unchanged.
- Save under `output/assets/figures/` with clear filenames (`fig1_workflow.png`, `fig2b_main_result.png`).
- Record source page, figure number, panel, crop status, and intended slide.

**Figure crop self-check** before slide insertion:
- Check every selected asset for clipped titles, axis labels, legends, panel labels.
- Check for irrelevant surrounding paper text included in the crop.
- Check for unreadable small text after planned slide scaling.
- Check dense multi-panel figures — split or crop to key panels when needed.
- Revise the crop before placing it in PPTX. A crop that loses a title, y-axis label, legend, or panel label is a defect.

### P7. Write Slide-by-Slide Content

For each slide, write: Chinese title (conclusion-style, not topic labels), 2-4 concise Chinese bullets, selected figure asset, Chinese figure caption and interpretation, and one core takeaway sentence. Add Chinese speaker notes only when the user requests notes or a presentation script.

**On-slide text budget:**
- Title: one line preferred; two lines only when vertical space allows.
- Normal slide: 2-3 bullets, each ≤18 Chinese characters or 8-10 English words.
- Result slide: 1 short interpretation sentence + ≤2 compact callouts.
- Source label: small and short; do not let source text compete with the figure.

If the point needs more words, split the slide or move explanation to speaker notes.

### P8. Layout Adaptation

Do not default to fixed 50/50 left-right splits. Choose layout from the figure's aspect ratio, density, and role:
- Full-width visual when the figure is wide, complex, or the slide's main evidence.
- Tall image + narrow text rail when the figure is vertically oriented.
- Top/bottom stack when the figure needs horizontal room.
- Asymmetric split (70/30, 75/25, 65/35) when one side clearly dominates.
- Compact visual-plus-callout when the slide only needs a few annotations.

Treat equal-weight 1:1 layouts as the exception. In most result slides, one side should dominate.

### P9. Anti-Template Design Rule

Avoid layouts that look like generic AI-generated slides:
- No three equal cards with icon/number strips.
- No rows of identical metric pills.
- No same right-hand interpretation rail on every figure slide.
- No nested rectangles and fake dashboard cards.
- No generic "problem / solution / impact" grids when the paper has a more specific structure.

Instead: let one figure own the page when it is the evidence; use a single large quote-like claim line for conceptual slides; use small edge annotations instead of big explanatory boxes; split dense figures across two slides instead of adding a crowded explanation rail.

### P10. Self-Review and Corrective Revision

After creating the first PPTX draft, run at least one explicit self-review pass:

1. Inspect the generated PPTX and extracted assets.
2. Write a short defect list with severity (`high`, `medium`, `low`) and slide numbers.
3. Correct every high-severity and fixable medium-severity issue.
4. Regenerate the PPTX only when edits were required.
5. Re-run verification after edits and update the QA record.

**Severity rules:**
- `high`: clipped scientific evidence (axes, legends, panel labels), unreadable main evidence, overlapping text/figures, text cut off by its box, wrong slide order, fabricated claims.
- `medium`: overly dense slides, rigid AI-looking layouts, weak crop margins, detached captions, excessive repeated layouts, or missing speaker notes when notes were requested.
- `low`: minor alignment imperfections, palette refinements, optional split of a readable but dense figure.

See [visual-qa.md](visual-qa.md) and [quality-gates.md](quality-gates.md) for detailed checklists.
