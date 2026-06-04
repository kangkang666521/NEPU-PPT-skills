# Slide Animation & Transitions

Use animations sparingly to guide audience focus, not as decoration. NEPU academic decks default to no animation; add only when the user explicitly requests or when the presentation format clearly benefits.

## When To Use Animations

- **Thesis defense / research seminar**: light entrance animations (Appear/Fade) for bullet points that should appear one at a time, keeping the audience on your pace rather than reading ahead.
- **Course lecture**: step-by-step reveal for diagrams, equations, or process stages.
- **Student activity / promotional**: slightly more motion is acceptable, but still avoid gimmicky effects.

## When NOT To Use

- Document-based reports converted to slides.
- Slides that will be printed or distributed as PDF.
- Dense data slides — animation distracts from evidence.
- Any deck where the user did not request animation.

## Recommended Effects

Use only these three effects; never others unless the user requests:

| Effect | Use case | PPT name |
|---|---|---|
| Appear | Text bullets, labels, simple reveals | `appear` / `fade` |
| Fade | Smooth transitions between sections | `fade` |
| Wipe (from left/ bottom) | Process steps, timeline reveals, mechanism chains | `wipe` |

**Forbidden by default**: Fly In, Bounce, Spin, Grow/Shrink, Zoom, Typewriter, Swivel, Boomerang, or any effect that draws attention to the animation itself.

## Implementation Notes (python-pptx)

python-pptx does not natively support animation. To add animations, two approaches:

### Approach A: Post-process with lxml (recommended for simple needs)

Modify the PPTX XML directly to add `<p:animEffect>` elements. This is fragile and should only be attempted when animations are explicitly requested.

### Approach B: Defer to PowerPoint

Generate a static PPTX first. Add a note in `planning/visual-qa.md` listing which slides should receive which animations, and suggest the user apply them in PowerPoint/WPS manually (takes ~2 minutes for a whole deck).

**Recommendation**: Use Approach B for most NEPU decks. The animation workload rarely justifies the fragility of XML manipulation.

## Timing & Rhythm

If applying animations manually or via script:

- **Entrance delay**: 0.2–0.5s between items on the same slide.
- **Transition between slides**: none or Fade (0.5s).
- **Total animation time per slide**: ≤ 3 seconds. A 30-slide deck with animations on every slide should not add more than 90 seconds of cumulative animation time.
- **Reveal order**: top-to-bottom, left-to-right. Never random or diagonal.

## Slide Transitions

Between slides, use transitions only when they serve a narrative purpose:

| Transition | Use |
|---|---|
| None | Default for academic decks |
| Fade (0.5s) | Major section changes (e.g., Introduction → Results → Conclusion) |
| Push (from right) | Timeline or process sequences |

Never use: Morph (unless template-native), Dissolve, Gallery, Cube, Doors, Origami.

## QA For Animated Decks

- Render each slide in its final state (all elements visible) and check for overlap.
- Verify that the first state of each animated slide (before any reveals) still makes sense — it should not be empty or confusing.
- Check that no essential information is permanently hidden behind an animation trigger that a presenter might skip.
