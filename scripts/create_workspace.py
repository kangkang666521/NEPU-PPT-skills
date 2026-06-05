#!/usr/bin/env python3
"""Create a clean local workspace for a NEPU-style presentation task."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
BUNDLED_ASSETS = SKILL_DIR / "assets"

PROFILES = [
    "academic-report",
    "thesis-defense",
    "course-presentation",
    "group-meeting",
    "student-activity",
    "admin-briefing",
]

ASSET_MODES = ["none", "logos", "selected", "all"]
QUALITY_MODES = ["auto", "standard", "rigorous"]
TEMPLATE_STYLES = ["auto", "petro-blue", "nepu-red", "petro-gold", "oilfield-green", "clean-white", "none"]

QUALITY_FIRST_PROFILES = {"academic-report", "thesis-defense", "group-meeting"}
PROFILE_TEMPLATE_STYLE = {
    "academic-report": "petro-blue",
    "thesis-defense": "petro-gold",
    "course-presentation": "petro-blue",
    "group-meeting": "petro-blue",
    "student-activity": "oilfield-green",
    "admin-briefing": "nepu-red",
}
TEMPLATE_PATTERNS = {
    "petro-blue": ["2.*/*16*9*.pptx", "3.*.pptx"],
    "nepu-red": ["1.*.pptx"],
    "petro-gold": ["4.*.pptx", "6.*.pptx"],
    "oilfield-green": ["5.*.pptx", "7.*/*.pptx"],
    "clean-white": ["2.*/*16*9*.pptx"],
}

# Data-driven seed files: (relative_path, initial_content, is_json)
SEED_FILES: list[tuple[str, str, bool]] = [
    (
        "planning/revision-log.md",
        "# Revision Log\n\nRecord every PPTX update here. Each revision should name the base file, "
        "new file, user request, preserved user edits, and image habit updates.\n",
        False,
    ),
    (
        "planning/image-preferences.md",
        "# Image Preferences\n\nRecord user image habits here: source type, crop style, placement, "
        "caption style, tone, and repeated preferences.\n",
        False,
    ),
    (
        "planning/image-inventory.json",
        json.dumps({"images": []}, ensure_ascii=False, indent=2),
        True,
    ),
    (
        "planning/figure-plan.md",
        "# Figure Plan\n\nRecord chart claims, data sources, chart types, output paths, "
        "and whether each chart is native PPT or externally generated.\n",
        False,
    ),
    (
        "planning/diagram-plan.md",
        "# Diagram Plan\n\nRecord flowcharts, structure diagrams, node lists, connector logic, "
        "color semantics, and editability decisions.\n",
        False,
    ),
    (
        "planning/visual-qa.md",
        "# Visual QA\n\nRecord rendered-preview checks, text/image overlap issues, contrast issues, "
        "diagram clarity issues, fixes, and final pass status.\n",
        False,
    ),
    (
        "planning/web-sources.md",
        "# Web Sources\n\nRecord collected web pages, text snippets, candidate images, "
        "source URLs, access dates, and usage/permission decisions.\n",
        False,
    ),
    (
        "assets/web/sources.json",
        json.dumps({"sources": []}, ensure_ascii=False, indent=2),
        True,
    ),
    (
        "figures/_shared/README.md",
        "# Figure Workflow\n\nCreate one folder per important chart with code/, data/, outputs/, "
        "sources/, and README.md. Keep generated charts reproducible.\n",
        False,
    ),
    (
        "planning/speaker-notes.md",
        "# Speaker Notes\n\nRecord generated or user-provided per-slide speaker notes here. "
        "Mirror inserted PPT speaker notes for review.\n",
        False,
    ),
    (
        "planning/speaker-note-locks.json",
        json.dumps({"slides": {}}, ensure_ascii=False, indent=2),
        True,
    ),
]


def copy_tree_contents(src: Path, dst: Path) -> list[str]:
    copied: list[str] = []
    if not src.exists():
        return copied
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        if item.name == ".gitkeep":
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        shutil.copy2(item, target)
        copied.append(str(target.relative_to(dst)))
    return copied


def first_existing_template(style: str) -> Path | None:
    templates_root = BUNDLED_ASSETS / "templates" / "nepu-civilization-office"
    for pattern in TEMPLATE_PATTERNS.get(style, []):
        for candidate in sorted(templates_root.glob(pattern)):
            if candidate.is_file():
                return candidate
    return None


def copy_selected_template(style: str, dst: Path) -> str | None:
    if style == "none":
        return None
    template = first_existing_template(style)
    if template is None:
        return None
    target = dst / template.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(template, target)
    return str(target.relative_to(dst))


def seed_workspace_files(workspace: Path) -> None:
    """Create initial planning/config files if they don't already exist."""
    for rel_path, content, _is_json in SEED_FILES:
        target = workspace / rel_path
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "profile": args.profile,
        "language": args.language,
        "planned_slides": args.slides,
        "quality_mode": args.quality,
        "asset_mode": args.assets,
        "template_style": args.template_style,
        "directories": {
            "source": "source",
            "raw_data": "data/raw",
            "processed_data": "data/processed",
            "logos": "assets/logos",
            "templates": "assets/templates",
            "fonts": "assets/fonts",
            "figures": "figures",
            "private_output": "output/private",
            "preview_output": "output/previews",
            "version_output": "output/versions",
        },
        "planning_files": {
            "revision_log": "planning/revision-log.md",
            "image_preferences": "planning/image-preferences.md",
            "image_inventory": "planning/image-inventory.json",
            "figure_plan": "planning/figure-plan.md",
            "diagram_plan": "planning/diagram-plan.md",
            "visual_qa": "planning/visual-qa.md",
            "web_sources": "planning/web-sources.md",
            "speaker_notes": "planning/speaker-notes.md",
            "speaker_note_locks": "planning/speaker-note-locks.json",
        },
        "web_manifest": "assets/web/sources.json",
        "bundled_assets_copied": args.assets != "none",
        "selected_template": None,
        "notes": [
            "Built-in NEPU logos and the selected scene template are copied by default when present.",
            "Place additional authorized NEPU logos and PPT templates in assets/.",
            "Place raw CSV, Excel, or statistical data in data/raw/.",
            "Place or collect web-supported material under assets/web/ and record provenance in planning/web-sources.md.",
            "Keep private source files inside the task workspace, not inside the skill folder.",
            "Never overwrite user-provided or previously delivered PPTX files; write revisions to output/versions/.",
            "For generated charts, keep plotting code, data, source notes, and outputs under figures/.",
            "For generated diagrams, keep a diagram plan and verify rendered clarity/editability.",
            "Use the selected template as the visual base; copy more bundled assets only when the deck actually needs them.",
        ],
    }


def resolve_quality_mode(requested: str, profile: str) -> str:
    """Resolve automatic QA depth from the task profile."""
    if requested != "auto":
        return requested
    return "rigorous" if profile in QUALITY_FIRST_PROFILES else "standard"


def resolve_template_style(requested: str, profile: str) -> str:
    """Resolve the default visual template style from the task profile."""
    if requested != "auto":
        return requested
    return PROFILE_TEMPLATE_STYLE.get(profile, "petro-blue")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--profile", choices=PROFILES, default="academic-report")
    parser.add_argument("--language", choices=["zh", "en", "bilingual"], default="zh")
    parser.add_argument("--slides", type=int, default=9)
    parser.add_argument(
        "--quality",
        choices=QUALITY_MODES,
        default="auto",
        help="QA depth. Auto selects rigorous for thesis defenses; use rigorous for paper reports or complex evidence.",
    )
    parser.add_argument(
        "--assets",
        choices=ASSET_MODES,
        default="selected",
        help="Bundled assets to copy. Default copies logos plus one selected template; use all only when needed.",
    )
    parser.add_argument(
        "--template-style",
        choices=TEMPLATE_STYLES,
        default="auto",
        help="Scene template to copy when assets are not disabled. Auto maps the profile to a NEPU style.",
    )
    parser.add_argument(
        "--no-bundled-assets",
        action="store_true",
        help="Deprecated alias for --assets none.",
    )
    args = parser.parse_args()
    if args.no_bundled_assets:
        args.assets = "none"
    args.quality = resolve_quality_mode(args.quality, args.profile)
    args.template_style = resolve_template_style(args.template_style, args.profile)

    workspace = args.workspace.resolve()

    # Create directory tree
    dirs = [
        "source",
        "data/raw",
        "data/processed",
        "assets/logos",
        "assets/templates",
        "assets/fonts",
        "assets/images",
        "assets/web/images",
        "assets/web/pages",
        "figures/_shared",
        "planning",
        "output/private",
        "output/previews",
        "output/versions",
    ]
    for folder in dirs:
        (workspace / folder).mkdir(parents=True, exist_ok=True)

    # Seed planning files
    seed_workspace_files(workspace)

    # Build and write manifest
    manifest = build_manifest(args)

    # Copy bundled assets
    copied_assets: dict[str, list[str]] = {"logos": [], "templates": [], "fonts": []}
    asset_kinds = {
        "none": (),
        "logos": ("logos",),
        "selected": ("logos",),
        "all": ("logos", "templates", "fonts"),
    }[args.assets]
    if asset_kinds:
        for kind in asset_kinds:
            copied_assets[kind] = copy_tree_contents(
                BUNDLED_ASSETS / kind, workspace / "assets" / kind
            )
    if args.assets == "selected":
        selected_template = copy_selected_template(
            args.template_style, workspace / "assets" / "templates"
        )
        if selected_template:
            copied_assets["templates"].append(selected_template)
            manifest["selected_template"] = f"assets/templates/{selected_template}"
    elif args.assets == "all":
        selected_template_path = first_existing_template(args.template_style)
        if selected_template_path:
            rel_template = selected_template_path.relative_to(BUNDLED_ASSETS / "templates")
            manifest["selected_template"] = f"assets/templates/{rel_template.as_posix()}"
    manifest["copied_bundled_assets"] = copied_assets

    (workspace / "nepu_ppt_task.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"workspace": str(workspace), **manifest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
