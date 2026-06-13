# Section 221 — Signs to be erected (football game day)

## Source shape

One boilerplate sentence (wrap-split across two lines) ending "…parking
restrictions are in effect:". Entries follow, one per blank-line-separated
paragraph, until the ordinance-history footer beginning `(Ord. No. Z-19`.
7 countable paragraphs as of revision 2026-01-16. TWO of those paragraphs
each contain TWO sign locations merged by source-text artifacts (see
Source-text quirks), so the section actually states **9 sign locations** in
**7 paragraphs**. The counting contract fixes the row count at 7 (the
validator counts paragraphs); the schema's secondary-location columns
(`street_2` / `cross_street_2` / `city_line_2`) carry the extra two
locations so no geocodable sign location is dropped.

The signs are temporary, bear the scheduled game-commencement time, and are
posted only on days football game day parking restrictions (Sec. TPR-177)
are in effect. That applies uniformly to every row — it is section-level
context, not per-row data, so the dataset has no days/times columns.

## Entry grammars observed

Only two variants:

1. `STREET, at CROSS.` → street, cross_street
   - "Centre Street, at Cabot Street." → street = Centre Street,
     cross_street = Cabot Street
2. `STREET, at the TOWN line.` → street, city_line
   - "Commonwealth Avenue, at the Boston line." → street = Commonwealth
     Avenue, city_line = boston

No directions, sides, offsets, days, or times appear anywhere in the list.

## Normalization rules

- `at the TOWN line` → `city_line` = the municipality name as a lowercase
  token (`Boston` → `boston`, `Brookline` → `brookline`). The words
  "at the … line" are dropped; nothing goes in `cross_street`.
- Street names are kept as written, whitespace-collapsed, never beautified.

## Field placement rules

- **`cross_street` holds only named streets/ways** (96/147 rule). Municipal
  boundaries are not streets: they go in `city_line`, and `cross_street`
  stays empty.
- **Exactly one of `cross_street` / `city_line` is filled** for the primary
  location; likewise exactly one of `cross_street_2` / `city_line_2` when a
  second (merged) location exists. If a future revision adds an entry with
  neither (or both) for a location, leave the unparseable part out of the
  structured fields and flag it in `notes`.
- A location geocodes from `street` + `cross_street` (intersection) or
  `street` + `city_line` (street at municipal boundary); the `_2` columns
  geocode the same way.
- **The second sign location of a PDF-merged paragraph is data, not a
  note.** It goes in `street_2` / `cross_street_2` / `city_line_2` so it
  stays geocodable — the "Design for geocoding" convention forbids burying
  grammar-provided atoms in free text. `notes` only flags that the
  paragraph was merged.
- `street_2` / `cross_street_2` / `city_line_2` are empty for every normal
  single-location paragraph (all but two rows).
- `notes` is reserved for source-text anomalies; it never carries
  geocodable data.

## Proposed common vocabulary

- **`municipal_boundary`** — enum `["boston", "brookline", "needham",
  "waltham", "watertown", "wellesley", "weston"]` (the seven municipalities
  abutting Newton), description "Adjacent municipality whose Newton boundary
  line is the reference point, as a lowercase token". Needed for `city_line`
  and `city_line_2` here ("at the Boston line"); no existing common def
  covers boundary references, and other sections also use them (segment
  endpoints like "the Boston line", municipal-line references such as "the
  Newton–Weston line"). Defined inline in
  `schemas/221_game_day_sign_locations.json` until adopted into
  `_common.json`.

## Gold rows for the merged entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here). Empty cells
shown blank.

| source paragraph (abbrev.) | street | cross_street | city_line | street_2 | cross_street_2 | city_line_2 | notes |
|---|---|---|---|---|---|---|---|
| Beacon Street, at the Boston line. Beacon Street, at Centre Street. | Beacon Street | | boston | Beacon Street | Centre Street | | PDF dropped the blank line; paragraph merges two sign locations — second in street_2 |
| Hammond Street, at the Brookline line Waverley Avenue, at Kenrick Street. | Hammond Street | | brookline | Waverley Avenue | Kenrick Street | | PDF dropped period+line break after "Brookline line"; paragraph merges two sign locations — second in street_2 |

Both rows keep the FULL merged paragraph, whitespace-collapsed, as
`source_text`:

- "Beacon Street, at the Boston line. Beacon Street, at Centre Street."
- "Hammond Street, at the Brookline line Waverley Avenue, at Kenrick Street."

The other five paragraphs produce ordinary rows with all `_2` columns empty:

| source entry | street | cross_street | city_line |
|---|---|---|---|
| Centre Street, at Beacon Street. | Centre Street | Beacon Street | |
| Centre Street, at Cabot Street. | Centre Street | Cabot Street | |
| Commonwealth Avenue, at the Boston line. | Commonwealth Avenue | | boston |
| Commonwealth Avenue, at Centre Street. | Commonwealth Avenue | Centre Street | |
| Hammond Pond Parkway, at Beacon Street. | Hammond Pond Parkway | Beacon Street | |

## Source-text quirks

- **Two merged paragraphs** — here the PDF wrap *merged* entries (the
  opposite of 148/96, where it *split* one entry into a lowercase
  continuation):
  1. "Beacon Street, at the Boston line." and "Beacon Street, at Centre
     Street." sit on consecutive source lines with no blank line between, so
     the validator's blank-line splitter sees ONE paragraph. Put the first
     location in the primary columns and the second in the `_2` columns;
     keep the merged paragraph verbatim as `source_text`.
  2. "Hammond Street, at the Brookline line Waverley Avenue, at Kenrick
     Street." is a single source line missing the period and line break
     after "Brookline line" — same treatment: "Hammond Street, at the
     Brookline line" in the primary columns, "Waverley Avenue, at Kenrick
     Street." in the `_2` columns.
  If the source text is ever re-split upstream (blank lines restored), the
  region's paragraph count rises by 2 to 9, these become four ordinary
  single-location rows, and the `_2` columns go unused — update the counting
  expectation, the gold rows, and this note then.
- There are no lowercase continuation fragments in this section; every
  paragraph in the region is a countable entry, so `entry_start: ^[A-Z]`
  matches all 7.
- "Centre Street, at Beacon Street." and the merged "Beacon Street, at
  Centre Street." are distinct sign locations (one sign per street of the
  pair), not duplicates — do not dedupe them.

## Counting rules (manifest)

```json
{"region_start": "restrictions are in effect:", "region_end": "\\(Ord\\. No\\. Z-19", "entry_start": "^[A-Z]"}
```

Verified against revision 2026-01-16: 7 paragraphs in the region, all
matching `entry_start` → **7 entries**, hence 7 TSV rows. Two of those rows
cover merged double-location paragraphs (their second location lives in the
`_2` columns), so the dataset represents all 9 sign locations the section
states.
