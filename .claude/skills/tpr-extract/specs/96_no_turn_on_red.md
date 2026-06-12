# Section 96 — No Turn on Red signs

## Source shape

Boilerplate paragraphs (a)–(b), then TWO entry lists in one dataset,
distinguished by the `turn` column:

- (c) "Right turns on red signals are prohibited at the following
  intersections:" → entries with `turn = right`
- (d) "Left turns on red signals are prohibited at the following
  intersections:" → entries with `turn = left` (2 entries as of revision
  2026-01-16)

Entries end at the ordinance-history footer beginning `(Ord No. R-33`.
The `(d) Left turns…` header paragraph starts with `(` so the counting
rules skip it automatically.

## Entry grammars observed

1. `STREET, DIRECTION at CROSS.` — "Beacon Street, westbound at Sumner Street."
2. `STREET at CROSS, DIRECTION.` — "Cabot Street at Walnut Street, westbound."
3. `STREET, DIRECTION, onto CROSS.` — "Dedham Street, westbound, onto
   Winchester Street." (`onto`/`towards` work like `at`)
4. `STREET, all directions at CROSS.` / `STREET at CROSS, all approaches.`
   → direction = `all`
5. Intersection-wide, no single approach street: "Edinboro Street, Walker
   Street, and Watertown Street, all directions." /
   "Watertown Street/Walnut Street, all approaches."
6. Trailing parenthetical qualifiers: lanes "(left two lanes)", conditions
   "(when illuminated)", positions "(opposite Elm Street)".

## Normalization rules

- `facing DIRECTIONbound traffic` → that direction ("Centre Street, facing
  eastbound traffic at Park Street." → direction = eastbound).
- Hyphenated or capitalized directions normalize to the vocabulary:
  "north-westbound" → northwestbound, "Northbound" → northbound.
- `all directions` / `all approaches` → direction = `all`.
- `DIRECTION and DIRECTION` → comma-joined set: "northbound and southbound"
  → `northbound,southbound`.
- Day ranges expand to tokens: "Monday–Friday" → `mon,tue,wed,thu,fri`.
- Times convert to 24-hour ranges, multiple windows comma-joined:
  "7:00 a.m. – 9:00 a.m. & 3:00 p.m. – 7:00 p.m." → `07:00-09:00,15:00-19:00`.
- Conditions drop parentheses and lowercase: "(when illuminated)" →
  `when illuminated`.

## Field placement rules

- Lane phrases go in `lane_detail`, never in `location_detail` or `notes`.
- Positional qualifiers ("at exit 125", "opposite Elm Street", "in Newton
  Corner") go in `location_detail`.
- For intersection-wide entries (grammar 5): `street` = the full multi-street
  designation exactly as written (whitespace-collapsed, not beautified —
  keep "Watertown Street/Albemarle Road/ Brookside Avenue" as-is),
  `cross_street` empty, `direction` = `all`.
- `notes` is reserved for source-text anomalies; it never carries data.
- **Movement qualifiers are data**: "merge", "continuing onto X" go in
  `location_detail` — never drop them. Join multiple distinct qualifiers
  with `; ` in source order ("one-way bridge; at exit 127").
- **`cross_street` holds only named streets/ways.** Landmark targets
  ("towards bridge over turnpike") go in `location_detail` and
  `cross_street` stays empty.
- **Street names never embed qualifiers**: "Washington Street northbound
  one-way bridge" → `street` = "Washington Street", direction =
  `northbound`, "one-way bridge" → `location_detail`.

## Gold rows for the adjudicated entries

Settled by Sonnet/Opus double-extraction adjudication (2026-06-12);
reproduce these unless the source text itself changes:

| source entry (abbrev.) | street | direction | cross_street | location_detail |
|---|---|---|---|---|
| Ward Street, north-eastbound, continuing onto Ward Street… | Ward Street | northeastbound | Waverley Avenue | continuing onto Ward Street |
| Washington Street continuing onto Washington Street… (opposite Elm Street) | Washington Street | eastbound | Washington Street | continuing onto Washington Street; opposite Elm Street |
| Washington Street eastbound merge onto Centre Avenue… | Washington Street | eastbound | Centre Avenue | merge in Newton Corner |
| Washington Street westbound merge onto Centre Avenue… (turn=left) | Washington Street | westbound | Centre Avenue | merge in Newton Corner |
| Washington Street northbound one-way bridge, onto the Massachusetts Turnpike entrance on-ramp… (turn=left) | Washington Street | northbound | Massachusetts Turnpike entrance on-ramp | one-way bridge; at exit 127 |
| Washington Street, facing northbound traffic towards bridge over turnpike. | Washington Street | northbound | | bridge over turnpike |

## Source-text quirks

- PDF line-wrap splits two entries across blank lines; fragments start
  lowercase ("p.m.", "far left two lanes.") and must be rejoined into the
  previous entry's `source_text`.
- "Perkins Street, Northbound, at Washington Street." has a capitalized
  direction mid-sentence — normalize, no note needed.
- Several Washington Street entries are merge/continuation movements
  ("Washington Street continuing onto Washington Street, eastbound (opposite
  Elm Street)."); keep `street` and `cross_street` as the named streets and
  the rest in `location_detail`.

## Counting rules (manifest)

```json
{"region_start": "Right turns on red signals are prohibited at the following intersections:", "region_end": "\\(Ord No\\. R-33", "entry_start": "^[A-Z]"}
```

Counts both the (c) and (d) lists; the (d) header paragraph is skipped by
`entry_start`.
