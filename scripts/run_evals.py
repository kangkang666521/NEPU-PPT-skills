#!/usr/bin/env python3
"""Lightweight eval runner for NEPU PPT skill evaluations.

Reads evals/evals.json and prints a summary of available test cases.
Does NOT auto-execute assertions (these require an AI in the loop).
Use this to list, filter, or validate the eval file structure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EVALS_PATH = Path(__file__).resolve().parents[1] / "evals" / "evals.json"


def load_evals(path: Path | None = None) -> dict:
    path = path or EVALS_PATH
    if not path.exists():
        print(f"Eval file not found: {path}", file=sys.stderr)
        return {"evals": []}
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evals(data: dict) -> list[str]:
    """Validate eval structure. Returns list of issues."""
    issues: list[str] = []
    evals = data.get("evals", [])
    if not evals:
        issues.append("No eval cases found")
        return issues

    seen_ids: set[str] = set()
    for i, case in enumerate(evals):
        case_id = case.get("id", f"<unnamed-{i}>")
        if case_id in seen_ids:
            issues.append(f"Duplicate eval id: {case_id}")
        seen_ids.add(case_id)

        for field in ("id", "prompt", "expected_output", "assertions"):
            if field not in case:
                issues.append(f"'{case_id}': missing field '{field}'")

        assertions = case.get("assertions", [])
        if not assertions:
            issues.append(f"'{case_id}': no assertions defined")
        for j, a in enumerate(assertions):
            for af in ("name", "description"):
                if af not in a:
                    issues.append(f"'{case_id}' assertion {j}: missing '{af}'")

    return issues


def print_summary(data: dict) -> None:
    evals = data.get("evals", [])
    print(f"Skill: {data.get('skill_name', '(unknown)')}")
    print(f"Total eval cases: {len(evals)}")
    print()

    domains: dict[str, int] = {}
    for case in evals:
        # Derive domain from id prefix
        prefix = case["id"].split("-")[0] if "-" in case["id"] else "other"
        domains[prefix] = domains.get(prefix, 0) + 1

    print("By domain:")
    for domain, count in sorted(domains.items()):
        print(f"  {domain}: {count} case(s)")

    print()
    print(f"{'ID':<50} {'Assertions':>10}")
    print("-" * 62)
    for case in evals:
        n = len(case.get("assertions", []))
        print(f"{case['id']:<50} {n:>10}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals", type=Path, default=EVALS_PATH,
                        help="Path to evals.json")
    parser.add_argument("--validate", action="store_true",
                        help="Validate eval structure only")
    parser.add_argument("--filter", type=str, default="",
                        help="Filter cases by id substring")
    args = parser.parse_args()

    data = load_evals(args.evals)

    if args.validate:
        issues = validate_evals(data)
        if issues:
            print(f"FAIL: {len(issues)} issue(s) found:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        print("OK: Eval file structure is valid.")
        return 0

    if args.filter:
        data["evals"] = [c for c in data.get("evals", [])
                         if args.filter.lower() in c["id"].lower()]
        print(f"Filtered to {len(data['evals'])} case(s) matching '{args.filter}'\n")

    print_summary(data)

    issues = validate_evals(data)
    if issues:
        print(f"\nWARN: {len(issues)} structural issue(s) - run with --validate for details.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
