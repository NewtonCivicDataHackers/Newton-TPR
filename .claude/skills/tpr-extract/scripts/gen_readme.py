#!/usr/bin/env python3
"""Regenerate extracted_data/README.md from the tpr-extract skill's manifest
and schemas. Never edit that README by hand — schema drift between docs and
data is exactly what this generator exists to prevent."""

import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]


def load_json(path):
    return json.loads(Path(path).read_text())


def main():
    manifest = load_json(SKILL_DIR / "manifest.json")
    common = load_json(SKILL_DIR / "schemas" / "_common.json")
    index = load_json(REPO_ROOT / "index.json")
    em_path = REPO_ROOT / "extracted_data" / "extraction_manifest.json"
    em = load_json(em_path) if em_path.exists() else {"datasets": {}}

    by_status = {}
    for d in manifest["datasets"]:
        by_status.setdefault(d["status"], []).append(d)

    out = []
    out.append("# Newton TPR Extracted Data")
    out.append("")
    out.append("<!-- GENERATED FILE — do not edit. -->")
    out.append("<!-- Regenerate with: python3 .claude/skills/tpr-extract/scripts/gen_readme.py -->")
    out.append("")
    out.append(
        "Structured TSV datasets extracted from the Newton Traffic and Parking "
        "Regulations section text in [sections/](../sections/). The extraction "
        "contract — schemas, vocabulary, per-section specs, and validation — "
        "lives in the `tpr-extract` skill at `.claude/skills/tpr-extract/`."
    )
    out.append("")
    out.append(f"- **TPR revision**: {em.get('revision_date', 'UNKNOWN')}")
    out.append(f"- **Format**: TSV (tab-separated, UTF-8, no quoting); every row "
               f"carries a verbatim `source_text` provenance column")
    out.append("")

    out.append("## Datasets")
    out.append("")
    for d in by_status.get("active", []):
        stem = Path(d["output"]).stem
        schema = load_json(SKILL_DIR / d["schema"])
        rows = em.get("datasets", {}).get(stem, {}).get("rows", "?")
        out.append(f"### {d['section']} — {d['title']}")
        out.append("")
        out.append(f"[{Path(d['output']).name}]({Path(d['output']).name}) — {rows} rows")
        out.append("")
        out.append("| Column | Description |")
        out.append("|--------|-------------|")
        for col in schema["columns"]:
            field = schema["fields"][col]
            desc = field.get("description")
            if desc is None and "$ref" in field:
                desc = common["defs"][field["$ref"].split("#", 1)[1]].get("description", "")
            flags = []
            if field.get("required") or (
                "$ref" in field
                and common["defs"][field["$ref"].split("#", 1)[1]].get("required")
            ):
                flags.append("required")
            if "$ref" in field:
                flags.append(f"vocabulary: `{field['$ref'].split('#', 1)[1]}`")
            suffix = f" ({'; '.join(flags)})" if flags else ""
            out.append(f"| `{col}` | {desc}{suffix} |")
        out.append("")

    planned = by_status.get("planned", [])
    if planned:
        out.append("## Planned")
        out.append("")
        out.append("Sections with extraction coverage planned but not yet built:")
        out.append("")
        for d in planned:
            out.append(f"- **{d['section']}** — {d['title']} → `{Path(d['output']).name}`")
        out.append("")

    other = by_status.get("excluded", []) + by_status.get("review", [])
    if other:
        out.append("## Not extracted")
        out.append("")
        out.append("| Section | Title | Status | Reason |")
        out.append("|---------|-------|--------|--------|")
        for d in other:
            out.append(
                f"| {d['section']} | {d['title']} | {d['status']} | {d.get('reason', '')} |"
            )
        out.append("")

    legacy = sorted((REPO_ROOT / "extracted_data").glob("*.csv"))
    if legacy:
        out.append("## Legacy CSV files")
        out.append("")
        out.append(
            "The remaining `*.csv` files are one-off extractions from March 2025 "
            "(two TPR revisions stale, no provenance, inconsistent schemas). "
            "Treat them as deprecated; they are removed as each section's TSV "
            "dataset goes active."
        )
        out.append("")

    (REPO_ROOT / "extracted_data" / "README.md").write_text("\n".join(out) + "\n")
    print(f"wrote extracted_data/README.md "
          f"({len(by_status.get('active', []))} active, {len(planned)} planned)")


if __name__ == "__main__":
    main()
