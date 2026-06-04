# Visual QA

Use this checklist after every substantial deck generation or revision. The goal is to catch layout defects by looking at rendered slides, not only by inspecting the PPTX object tree, while avoiding repeated renders that do not improve quality.

## Required Outputs

For every delivery, create or update:

- `output/previews/`: one rendered image per slide.
- `output/previews/contact-sheet.png` or `.jpg`: all slides in one overview image.
- `planning/visual-qa.md`: a short record of defects found, fixes made, and remaining risks.

## Visual Review Loop

1. Render the current PPTX to slide images.
2. Review the contact sheet first to catch global rhythm, color, and spacing problems.
3. Open full-size previews for slides with dense text, images, charts, tables, or diagrams.
4. Fix the source PPTX, script, or JSX source.
5. If fixes were required, rerender and repeat until the deck passes the checks below.

Do not mark the deck complete after finding a visible defect unless the defect has been fixed or explicitly accepted by the user.

If the first structural audit and rendered review find no high or fixable medium defects, record the pass and deliver without a redundant second render.

## Layout Checks

Check every rendered slide for:

- Text boxes overlapping photos, logos, charts, or other text.
- Images covering titles, labels, footers, page numbers, or captions.
- Text cropped by shape boundaries or slide edges.
- Long Chinese lines breaking awkwardly or becoming too small.
- Title, subtitle, and body hierarchy collapsing into the same visual weight.
- Footer/logo/page-number alignment drifting across slides.
- Decorative elements competing with the main claim.

## Color And Contrast Checks

Check whether key text remains readable over fills, images, and template backgrounds.

Minimum practical rules:

- Use dark text on light backgrounds or white text on intentionally darkened image areas.
- If text sits over a photo, add a solid or semi-transparent overlay behind the text.
- Avoid NEPU red on dark blue or dark red backgrounds unless the text is large and contrast-tested.
- Use gold as accent, not as dense body text.
- Keep chart/category colors distinct enough in grayscale and projection conditions.

When in doubt, simplify the palette. Academic decks should be readable before they are decorative.

## Automated Geometry Checks

When the authoring tool exposes PPT shapes:

- Extract bounding boxes for text, images, charts, and logos.
- Flag text-image overlaps above a small threshold.
- Flag text boxes outside slide bounds.
- Flag very small text in dense diagrams or charts.
- Flag locked/manual user content before changing it.

Automated checks are advisory. A rendered visual pass is still required because background images, grouped shapes, and transparency can fool geometry-only checks.

### Programmatic PPTX Structural Audit

When generating with python-pptx, perform a lightweight audit in code after the first draft and again after revision:

- Reopen the PPTX with `Presentation(output_path)`.
- Count slides and embedded media.
- Count non-empty notes slides if notes were planned.
- Check every shape's left/top/right/bottom stays within the slide canvas.
- Flag text-heavy slides by character count and number of text boxes.
- Flag any text box whose estimated text length is too large for its width/height, especially mixed Chinese-English strings.
- Flag long unbroken tokens or labels that may overflow narrow boxes.
- Count repeated layout patterns and flag decks that reuse the same composition too often.
- Flag images whose displayed size is too small for their role.
- Scan for placeholder text such as `lorem`, `xxxx`, or accidental unreplaced labels.

These checks cannot prove visual perfection, but they reliably catch many failures and should trigger a manual/self-review pass.

## Self-Review and Corrective Revision Loop

After creating the first PPTX draft, run at least one explicit self-review pass before declaring the deck final:

1. Inspect the generated PPTX and extracted assets.
2. Write a short defect list with severity (`high`, `medium`, `low`) and slide numbers.
3. Correct every high-severity issue and every medium-severity issue that can be fixed without expanding the task substantially.
4. Regenerate the PPTX only when edits were required.
5. Re-run verification after edits and update `planning/visual-qa.md` with what was checked, what was fixed, and what remains.

### Defect Severity

| Severity | Criteria | Action |
|---|---|---|
| `high` | Clipped scientific evidence (axes, legends, panel labels), unreadable main evidence, overlapping text/figures, text cut off by box, wrong slide order, fabricated claims | Must fix before delivery |
| `medium` | Overly dense slides, rigid AI-looking layouts, weak crop margins, detached captions, excessive repeated layouts, missing requested/planned speaker notes | Fix when feasible |
| `low` | Minor alignment imperfections, palette refinements, optional split of readable but dense figure | Note and defer |

## Package & Delivery Checks

Before final handoff:

- Final `.pptx` exists and is non-empty.
- Final `.pptx` is a newly named revision file (not overwritten source/previous delivery).
- Slide count matches the planned outline.
- No empty media files.
- Important slide text is editable.
- User-provided logos and templates are not embedded in any public skill package unless authorized.
- `planning/revision-log.md` is updated when revising.
- `planning/image-preferences.md` and `planning/image-inventory.json` are updated.
- `planning/figure-plan.md` and `planning/diagram-plan.md` are updated when applicable.
- `planning/visual-qa.md` records what was checked and fixed.
- `planning/web-sources.md` and `assets/web/sources.json` are updated when web content is collected.
- `planning/speaker-note-locks.json` is checked before updating notes on revised decks.
- If the user reports open failures, validate with `scripts/office_bridge.ps1` per [office-compatibility.md](office-compatibility.md).

## Presentation-Level Checks

- The deck has a clear beginning, middle, and ending.
- Each slide has a distinct role.
- The chosen template style matches the user's context and audience.
- The deck looks like a coherent NEPU-style deck, not a generic template with a school name pasted on.
- User edits and user-added images from the base deck are preserved.
- Existing strong pages are preserved in conservative revision mode.
- Each data chart has a clear claim and avoids decorative effects.
- User-corrected speaker notes and content on locked slides are preserved.
- Flowcharts and structure diagrams are clear enough to explain verbally.
- Web-collected facts and images have provenance notes.

## QA Record Template

```markdown
# Visual QA

- Deck:
- Rendered at:
- Slide count:
- Preview folder:
- Contact sheet:

## Issues Found

| Slide | Issue | Fix |
| --- | --- | --- |
|  |  |  |

## Final Pass

- Text/image overlap:
- Text overflow:
- Contrast/readability:
- Diagram clarity:
- Chart/table readability:
- User-locked content preserved:
```
