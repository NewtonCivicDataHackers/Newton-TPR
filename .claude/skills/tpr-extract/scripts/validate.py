#!/usr/bin/env python3
"""Validate extracted TPR datasets against the tpr-extract skill contract.

For every dataset with status "active" in manifest.json:
  1. The TSV header matches the schema's column order exactly.
  2. Every cell is whitespace-normalized; required fields are non-empty;
     enum, pattern, and type constraints hold.
  3. Columns listed in the schema's "unique" array have no duplicate values.
  4. The row count equals the number of entries counted in the source
     section text using the manifest's counting rules.
  5. extraction_manifest.json agrees on row count, and its revision_date
     matches index.json's (staleness check).

Stdlib only. Exit 0 = all checks pass; details on stderr.
"""

import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]


def load_json(path):
    return json.loads(Path(path).read_text())


def resolve_field(field, common):
    """Merge a field spec with its common# ref, local keys winning."""
    if "$ref" not in field:
        return field
    name = field["$ref"].split("#", 1)[1]
    try:
        base = common["defs"][name]
    except KeyError:
        raise SystemExit(f"unknown $ref common#{name}")
    merged = dict(base)
    merged.update({k: v for k, v in field.items() if k != "$ref"})
    return merged


def split_paragraphs(text):
    paras, cur = [], []
    for line in text.splitlines():
        if line.strip():
            cur.append(line.strip())
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    if cur:
        paras.append(" ".join(cur))
    return paras


def count_entries(source_text, counting):
    m = re.search(counting["region_start"], source_text)
    if not m:
        raise ValueError(f"region_start not found: {counting['region_start']!r}")
    region = source_text[m.end():]
    m_end = re.search(counting["region_end"], region)
    if m_end:
        region = region[: m_end.start()]
    entry_re = re.compile(counting.get("entry_start", "^[A-Z]"))
    # "paragraph" (default): entries are blank-line-separated, possibly multi-line.
    # "line": entries are one-per-line (lists with no blank lines between them).
    if counting.get("unit") == "line":
        units = [ln.strip() for ln in region.splitlines() if ln.strip()]
    else:
        units = split_paragraphs(region)
    return sum(1 for u in units if entry_re.search(u))


def check_cell(value, spec, loc, errors):
    if value == "":
        if spec.get("required"):
            errors.append(f"{loc}: required field is empty")
        return
    if value != value.strip() or "  " in value:
        errors.append(f"{loc}: whitespace not normalized: {value!r}")
    ftype = spec.get("type", "string")
    if ftype == "integer" and not re.fullmatch(r"-?\d+", value):
        errors.append(f"{loc}: not an integer: {value!r}")
    elif ftype == "number" and not re.fullmatch(r"-?\d+(\.\d+)?", value):
        errors.append(f"{loc}: not a number: {value!r}")
    if "enum" in spec and value not in spec["enum"]:
        errors.append(f"{loc}: {value!r} not in enum {spec['enum']}")
    if "pattern" in spec and not re.fullmatch(spec["pattern"], value):
        errors.append(f"{loc}: {value!r} does not match {spec['pattern']!r}")


def validate_dataset(ds, common, extraction_manifest, errors):
    name = Path(ds["output"]).stem
    schema = load_json(SKILL_DIR / ds["schema"])
    columns = schema["columns"]
    fields = {k: resolve_field(v, common) for k, v in schema["fields"].items()}

    unknown = set(columns) - set(fields)
    if unknown:
        errors.append(f"{name}: columns missing field specs: {sorted(unknown)}")
        return

    tsv_path = REPO_ROOT / ds["output"]
    if not tsv_path.exists():
        errors.append(f"{name}: output file missing: {ds['output']}")
        return
    lines = tsv_path.read_text().splitlines()
    if not lines:
        errors.append(f"{name}: empty file")
        return

    header = lines[0].split("\t")
    if header != columns:
        errors.append(f"{name}: header {header} != schema columns {columns}")
        return

    rows = []
    for i, line in enumerate(lines[1:], start=2):
        cells = line.split("\t")
        if len(cells) != len(columns):
            errors.append(f"{name}:{i}: {len(cells)} cells, expected {len(columns)}")
            continue
        row = dict(zip(columns, cells))
        rows.append(row)
        for col, value in row.items():
            check_cell(value, fields[col], f"{name}:{i}:{col}", errors)

    for col in schema.get("unique", []):
        seen = {}
        for i, row in enumerate(rows, start=2):
            v = row[col]
            if v in seen:
                errors.append(f"{name}:{i}:{col}: duplicate of line {seen[v]}: {v!r}")
            seen[v] = i

    counting = ds.get("counting")
    if counting and counting.get("region_start"):
        source_text = (REPO_ROOT / ds["source"]).read_text()
        try:
            expected = count_entries(source_text, counting)
        except ValueError as e:
            errors.append(f"{name}: counting failed: {e}")
        else:
            if expected != len(rows):
                errors.append(
                    f"{name}: source has {expected} entries but TSV has "
                    f"{len(rows)} rows — entries dropped or invented"
                )
    elif counting and counting.get("verified_by"):
        # Section's completeness can't be checked by a single regex (e.g. mixed
        # formats / PDF-table rows). Completeness is established by the means
        # named here and documented in the spec; skip the regex count.
        print(f"  {name}: regex-count skipped — verified by {counting['verified_by']}")
    else:
        errors.append(f"{name}: active dataset has no counting rules in manifest")

    recorded = extraction_manifest.get("datasets", {}).get(name, {}).get("rows")
    if recorded != len(rows):
        errors.append(
            f"{name}: extraction_manifest.json records {recorded} rows, file has {len(rows)}"
        )
    return len(rows)


def main():
    manifest = load_json(SKILL_DIR / "manifest.json")
    common = load_json(SKILL_DIR / "schemas" / "_common.json")
    index = load_json(REPO_ROOT / "index.json")

    em_path = REPO_ROOT / "extracted_data" / "extraction_manifest.json"
    if not em_path.exists():
        print("FAIL: extracted_data/extraction_manifest.json missing", file=sys.stderr)
        return 1
    extraction_manifest = load_json(em_path)

    errors = []
    if extraction_manifest.get("revision_date") != index["revision_date"]:
        errors.append(
            f"stale: extraction_manifest revision_date "
            f"{extraction_manifest.get('revision_date')!r} != index.json "
            f"{index['revision_date']!r} — datasets need regeneration"
        )

    active = [d for d in manifest["datasets"] if d["status"] == "active"]
    for ds in active:
        n = validate_dataset(ds, common, extraction_manifest, errors)
        if n is not None:
            print(f"  {Path(ds['output']).stem}: {n} rows")

    if errors:
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"OK: {len(active)} active dataset(s) valid, revision {index['revision_date']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
