"""Shared Matplotlib style helpers for NEPU PPT scientific charts."""

from __future__ import annotations

from pathlib import Path


NEPU_PPT_PALETTE = {
    "blue": "#00508F",
    "dark_blue": "#00335C",
    "red": "#C41230",
    "gold": "#CFB87C",
    "ink": "#1A1A2E",
    "body": "#3A4658",
    "muted": "#6B778A",
    "teal": "#2A9D8F",
    "orange": "#E69F00",
    "purple": "#7B61A8",
    "green": "#2D6A4F",
}

# Cross-platform CJK font fallback chain, ordered by preference.
# System-specific fonts are tried first, with universal fallbacks at the end.
_CJK_FONT_CANDIDATES = [
    # Windows
    "Microsoft YaHei",
    "DengXian",
    "SimHei",
    # macOS
    "PingFang SC",
    "Heiti SC",
    # Linux / cross-platform
    "Source Han Sans SC",
    "Noto Sans CJK SC",
    "HarmonyOS Sans SC",
    "WenQuanYi Micro Hei",
    "WenQuanYi Zen Hei",
    # Japanese / Korean fallbacks (often include CJK glyphs)
    "Hiragino Sans",
    "Nanum Gothic",
    # Latin-only fallback
    "Arial",
    "DejaVu Sans",
]


def _detect_available_cjk_font() -> str | None:
    """Detect the first available CJK-capable font on the current system.

    Uses matplotlib's font_manager when available, otherwise returns None.
    """
    try:
        from matplotlib.font_manager import findfont, FontProperties
    except ImportError:
        return None

    available: set[str] = set()
    try:
        from matplotlib.font_manager import fontManager
        available = {f.name for f in fontManager.ttflist}
    except Exception:
        pass

    for candidate in _CJK_FONT_CANDIDATES:
        if candidate in available:
            return candidate
        # Try findfont as a fallback
        try:
            fp = FontProperties(family=candidate)
            found = findfont(fp, fallback_to_default=False)
            if found and not str(found).endswith("DejaVu Sans"):
                return candidate
        except Exception:
            continue
    return None


def _build_font_family_list(preferred: str | None = None) -> list[str]:
    """Build the font.sans-serif list with detected fonts or safe fallbacks."""
    if preferred:
        return [preferred] + [f for f in _CJK_FONT_CANDIDATES if f != preferred]
    detected = _detect_available_cjk_font()
    if detected:
        # Put detected font first, followed by the rest of the chain
        chain = [detected]
        for f in _CJK_FONT_CANDIDATES:
            if f != detected and f not in chain:
                chain.append(f)
        return chain
    # No CJK font detected: use safe fallback chain as-is
    return list(_CJK_FONT_CANDIDATES)


def apply_nepu_ppt_style(plt, *, font_family: str | None = None) -> None:
    """Apply a restrained NEPU/Nature-like style to a Matplotlib pyplot module.

    If *font_family* is omitted, auto-detects the best available CJK font.
    """
    font_list = _build_font_family_list(font_family)
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
            "font.family": "sans-serif",
            "font.sans-serif": font_list,
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.linewidth": 0.8,
            "axes.edgecolor": NEPU_PPT_PALETTE["ink"],
            "axes.labelcolor": NEPU_PPT_PALETTE["ink"],
            "xtick.color": NEPU_PPT_PALETTE["body"],
            "ytick.color": NEPU_PPT_PALETTE["body"],
            "grid.color": "#D0D8E8",
            "grid.linewidth": 0.5,
            "grid.alpha": 0.55,
            "legend.frameon": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def ppt_figure_size(kind: str = "wide") -> tuple[float, float]:
    """Return practical Matplotlib figure sizes for 16:9 PPT slides."""
    sizes = {
        "wide": (7.2, 4.05),
        "half": (4.7, 3.1),
        "square": (4.2, 4.2),
        "tall": (4.2, 5.4),
    }
    if kind not in sizes:
        raise ValueError(f"Unknown figure size '{kind}'. Choose from: {list(sizes)}")
    return sizes[kind]


def save_ppt_figure(fig, output_base: str | Path, *, transparent: bool = False) -> dict[str, str]:
    """Save PNG, editable SVG, and PDF copies for PPT use and regeneration."""
    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    png = base.with_suffix(".png")
    svg = base.with_suffix(".svg")
    pdf = base.with_suffix(".pdf")
    fig.savefig(png, transparent=transparent)
    fig.savefig(svg, transparent=transparent)
    fig.savefig(pdf, transparent=transparent)
    return {"png": str(png), "svg": str(svg), "pdf": str(pdf)}
