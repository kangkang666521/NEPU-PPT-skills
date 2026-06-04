#!/usr/bin/env python3
"""Run deterministic smoke checks for the NEPU PPT skill project."""

from __future__ import annotations

import base64
import re
import sys
import tempfile
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from scripts.create_workspace import resolve_quality_mode  # noqa: E402
from scripts.plot_style import _build_font_family_list, ppt_figure_size, save_ppt_figure  # noqa: E402
from scripts.slide_builder import NepuSlideBuilder  # noqa: E402
from scripts.validate_pptx import estimate_text_width_pt, validate_pptx  # noqa: E402
from scripts.web_collect import PageParser, validate_public_url  # noqa: E402


THEMES = ["petro-blue", "nepu-red", "petro-gold", "oilfield-green", "clean-white"]
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M/wHwAF"
    "gAJ/l5M9WQAAAABJRU5ErkJggg=="
)


def expect_exception(exc_type: type[BaseException], action, label: str) -> None:
    try:
        action()
    except exc_type:
        return
    raise AssertionError(f"Expected {exc_type.__name__}: {label}")


def contrast_ratio(first: str, second: str) -> float:
    def luminance(value: str) -> float:
        channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def check_builder(output_dir: Path) -> None:
    image = output_dir / "tiny.png"
    image.write_bytes(TINY_PNG)

    for theme in THEMES:
        builder = NepuSlideBuilder(theme=theme)
        if contrast_ratio(builder._c("text"), builder._c("bg")) < 4.5:
            raise AssertionError(f"{theme} text/background contrast is too low")
        if contrast_ratio(builder._c("body"), builder._c("bg")) < 3.0:
            raise AssertionError(f"{theme} body/background contrast is too low")
        builder.add_cover("项目烟雾检查", subtitle=theme)
        builder.add_section("主题与背景")
        builder.add_claim_slide("质量检查必须保留", bullets=["结构审计", "视觉复核"])
        builder.add_figure_slide(str(image), claim="图片存在时正常插入")
        picture = builder.prs.slides[3].shapes[0]
        if abs((picture.width / picture.height) - 1.0) > 0.01:
            raise AssertionError(f"{theme} figure insertion distorted the source aspect ratio")
        builder.add_matrix_slide(["模式", "用途"], [["standard", "常规"], ["rigorous", "严格"]])
        builder.set_speaker_notes(1, "封面备注")
        output = output_dir / f"{theme}.pptx"
        builder.save(output)

        report = validate_pptx(output)
        if not report["valid"] or report["errors"]:
            raise AssertionError(f"{theme} deck failed validation: {report}")
        expect_exception(FileExistsError, lambda: builder.save(output), "overwrite protection")

    missing_builder = NepuSlideBuilder()
    expect_exception(
        FileNotFoundError,
        lambda: missing_builder.add_figure_slide(str(output_dir / "missing.png")),
        "missing figure",
    )
    if missing_builder.slide_count != 0:
        raise AssertionError("Missing figure created a blank slide")

    expect_exception(
        ValueError,
        lambda: NepuSlideBuilder().add_matrix_slide(["A", "B"], [["only one"]]),
        "matrix row length",
    )
    expect_exception(
        ValueError,
        lambda: NepuSlideBuilder().add_image_grid_slide([str(image)], cols=0),
        "image grid columns",
    )


def check_helpers() -> None:
    if resolve_quality_mode("auto", "thesis-defense") != "rigorous":
        raise AssertionError("Thesis defense did not resolve to rigorous QA")
    if resolve_quality_mode("auto", "academic-report") != "standard":
        raise AssertionError("Academic report did not resolve to standard QA")

    parser = PageParser()
    parser.feed("<html><title>NEPU</title><p>alpha <strong>nested</strong> omega</p></html>")
    if parser.paragraphs != ["alpha nested omega"]:
        raise AssertionError(f"Nested HTML text extraction failed: {parser.paragraphs}")

    expect_exception(ValueError, lambda: validate_public_url("file:///tmp/private"), "URL scheme")
    expect_exception(ValueError, lambda: validate_public_url("http://127.0.0.1/private"), "private IP")
    validate_public_url("https://example.edu/page")

    if estimate_text_width_pt("1234567890\nx", 10) >= estimate_text_width_pt("1234567890x", 10):
        raise AssertionError("Multiline width estimation does not use the longest line")
    expect_exception(ValueError, lambda: ppt_figure_size("unknown"), "figure size")
    if _build_font_family_list("Explicit Font")[0] != "Explicit Font":
        raise AssertionError("Explicit font preference was not honored")

    class FakeFigure:
        def __init__(self) -> None:
            self.paths: list[Path] = []

        def savefig(self, path: Path, **_kwargs) -> None:
            self.paths.append(path)

    fake = FakeFigure()
    saved = save_ppt_figure(fake, PROJECT_DIR / "tmp" / "self-check-figure")
    if set(saved) != {"png", "svg", "pdf"}:
        raise AssertionError(f"Figure export bundle is incomplete: {saved}")
    if {path.suffix for path in fake.paths} != {".png", ".svg", ".pdf"}:
        raise AssertionError(f"Figure export suffixes are incomplete: {fake.paths}")


def check_project_files() -> None:
    skill = PROJECT_DIR / "SKILL.md"
    if skill.stat().st_size > 12 * 1024:
        raise AssertionError(f"SKILL.md exceeds 12 KiB: {skill.stat().st_size}")

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    ignored_parts = {".git", ".codegraph", "node_modules", "outputs", "tmp", "temp"}
    for markdown in PROJECT_DIR.rglob("*.md"):
        if ignored_parts.intersection(markdown.parts):
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (markdown.parent / target).resolve()
            if not resolved.exists():
                raise AssertionError(
                    f"Broken local Markdown link in {markdown.relative_to(PROJECT_DIR)}: {raw_target}"
                )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="nepu-ppt-self-check-") as temp_dir:
        output_dir = Path(temp_dir)
        check_builder(output_dir)
        check_helpers()
        check_project_files()
    print("OK: Project smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
