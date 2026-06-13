# Section 220 — Parking prohibitions for tow zones

## Source shape

A long boilerplate paragraph (the removal/storage/penalty machinery) opens the
section and ends with "…the fee established therefor by contract." Entries
follow until the ordinance-history footer beginning `(Rev. Ords.`. The
trailing `*Editor's note—…` paragraph is past the footer and never reached.

Two structural shapes for entries:

1. **Inline street entries** — a street name, an em/en/box dash, then the
   regulation on one paragraph:
   "Acacia Avenue — Tow-away zone, east side, Monday through Saturday."
2. **Sub-numbered streets** — a bare street-name header paragraph
   ("Beacon Street") followed by one paragraph per `(N)` sub-item, each a
   full regulation: "(1) Tow-away zone, north side, from Hammond Street
   easterly 300 feet." Each `(N)` is its own row; the bare header is NOT a
   row.

Plus three **citywide blanket rules** at the top of the list, before any named
street:

- "Any vehicle parked in violation of section 19-177…" → `prohibition_type =
  football_game_day`
- "In any fire lane at any time." → `prohibition_type = fire_lane`
- "In any bus stop at any time." → `prohibition_type = bus_stop`

62 entries (paragraphs counted by the validator) as of revision 2025-04-11.
See "Counting rules" and the Longfellow/Lothrup quirk below for why 62 ≠ the
63 distinct regulations a reader sees.

## Entry grammars observed

Core shape: `STREET — Tow-away zone[,] [SCHEDULE,] SIDE[,] SEGMENT.` with
parts in varying order. SCHEDULE (days/times) and SIDE float; SEGMENT is last.

Segment sub-grammars:

1. `from CROSS <bearing>erly N feet` → from_point = CROSS, length_feet = N,
   bearing = the compass token ("from Hammond Street easterly 300 feet" →
   from_point "Hammond Street", length_feet 300, bearing east).
2. `from a point N feet DIR of CROSS <bearing>erly M feet` → from_point keeps
   the whole measured-point phrase "a point N feet DIR of CROSS"; length_feet
   = M, bearing = the trailing -erly word ("from a point 340 feet west of
   Walnut Street westerly a distance of 240 feet" → from_point "a point 340
   feet west of Walnut Street", length_feet 240, bearing west).
3. `from POINT to POINT` → from_point + to_point, no length/bearing
   ("from Beacon Street to Everett Street", "from Stone Avenue to Boston City
   Line", "from a point 170 feet west of Grant Avenue to a point 235 feet west
   of Hobart Road").
4. `entire length` / `entire length from POINT to POINT` → extent =
   "entire length"; if endpoints are also given keep them in from_point/to_point
   (Tudor Road: extent "entire length", from_point "Hammond Street", to_point
   "Beacon Street").
5. `between X and Y` and lettered/landmark anchors that are not plain streets
   ("between off-ramp and on-ramp at Boylston Street", "between 31 Elmwood
   Street and the rear entrance of 400 Centre Street", "from exit driveway of
   Newton Post #440") → put the un-atomizable phrase in `location_detail`
   (grammar 5) when it is not cleanly a from/to pair; when it IS a clean
   "between A and B" street pair, A→from_point, B→to_point.
6. No segment at all ("College Road — Tow-away zone, both sides." / "Quincy
   Road — Tow-away zone, south side.") → from_point/to_point/extent all empty.

## Normalization rules

- **prohibition_type**: "Tow-away zone" and the typo "Tow-way zone" both →
  `tow_away_zone` (note the typo in `notes`). "Parking prohibited" (Essex
  Road) → `parking_prohibited`. The three blanket rules → `fire_lane`,
  `bus_stop`, `football_game_day` respectively.
- **side**: lowercase compass; "both sides" → `both`; "north and west side"
  → `north,west` (comma-joined set in source order); "northeast side" →
  `northeast`. The "Tow-away, zone south side" / "Tow-away, zone" misplaced
  comma is a typo — side is still `south`; note the typo.
- **bearing**: the "-erly" word → compass token: easterly→east,
  westerly→west, northerly→north, southerly→south, southeasterly→southeast,
  northwesterly→northwest. This is the orientation of `length_feet`, not a
  travel direction, so it does NOT use `common#direction`.
- **days**: "Monday through Saturday" → `mon,tue,wed,thu,fri,sat`; "Monday
  through Friday" → `mon,tue,wed,thu,fri`; "all days" → `all`; "on school
  days" / "school days" → `school_days`; "Saturdays included" expands the
  base weekday set to include `sat`; "including Sundays and Holidays" adds
  `sun,holidays`. Empty `days` means every day.
- **times**: 12-hour → 24-hour; "12:00 midnight" → `00:00`; multiple windows
  comma-joined. Empty means at all times.
- **time_exception**: the `except HH to HH` form (Old Colony Road only) is an
  exemption window, NOT an applies-window. "except 7:00 p.m. to 12:00
  midnight" → time_exception = `19:00-00:00`, times empty.

## Field placement rules

- **Bare street-name headers** ("Beacon Street", "Commonwealth Avenue",
  "Adams Court", "Crosby Road", "Elm Road", "Grant Avenue", "Hammond Street",
  "Hartman Road", "Highland Street", "Suffolk Road") are NOT rows — they head
  the following `(N)` sub-items. Each `(N)` is one row whose `street` is the
  header street (the header supplies the street name; the `(N)` paragraph is
  the `source_text`).
- **The three blanket rules**: `street` = the categorical subject phrase
  ("any fire lane", "any bus stop", "any vehicle parked in violation of
  section 19-177"); side/segment/days/times empty ("at any time" = always);
  `prohibition_type` carries the category.
- **Measured-point references stay whole in from_point/to_point.** Do not
  shred "a point 340 feet west of Walnut Street" into separate offset columns
  — a geocoder resolves it as written, and the from/to slot keeps it
  geocodable. Only the trailing measured *length* of the zone is atomized
  (`length_feet` + `bearing`).
- **`location_detail`** holds segment qualifiers the from/to/length atoms
  cannot ("between off-ramp and on-ramp at Boylston Street (Route 9)", "from
  exit driveway of Newton Post #440"). It never holds side, day, or time data.
- **`notes`** is reserved for source-text anomalies (typos, the merged
  paragraph). It never carries regulation data.

## Source-text quirks

- **Longfellow/Lothrup merged paragraph** (the important one). Source lines
  140–141 have no blank line between them, so the validator's paragraph
  splitter joins them into ONE paragraph:
  "Longfellow Road — Tow-away zone, both sides, all days, from Washington
  Street easterly 75 feet. Lothrup Street - Tow-away zone, northeast side,
  from Pellegrini Playground 200 feet southeasterly."
  This is two regulations on two different streets, but the validator counts
  it as ONE entry (it counts paragraphs, and `.search` matches a paragraph at
  most once). To keep row-count == validator-count == 62, this paragraph is
  emitted as a **single row** keyed on Longfellow Road (the first-named
  street: street "Longfellow Road", side `both`, days `all`, from_point
  "Washington Street", length_feet 75, bearing east) and the entire Lothrup
  Street clause is recorded verbatim in `notes` with a flag that the source
  merged a second regulation here. `source_text` is the full merged paragraph.
  Downstream fix: a blank line between lines 140–141 in `process-tpr.py` would
  split these into two paragraphs and let them become two rows (then bump the
  count to 63); until then this row carries both and `notes` makes the loss
  visible rather than silent.
- **Tow-way typo**: Crosby Road (2) "Tow-way zone" and Beacon Street (3)/(4)
  "Tow-away, zone …" (comma after Tow-away) — normalize prohibition_type to
  `tow_away_zone`, side unaffected, note the typo.
- **Mixed dash glyphs** separate street from regulation: em dash "—", en dash
  "–", box-drawing dash "─", and plain hyphen "-" (and "—Tow-away" with no
  space on Park Street). All are the same separator; do not let the glyph
  affect parsing.
- **PDF line-wrap continuations** start lowercase ("northerly 320 feet.",
  "westerly of the intersection…", "point opposite Kimball Terrace…",
  "terminus easterly 25 feet.") OR capitalized ("Court.", "Everett Street.",
  "Centre Street.", "Street to Clifton Road.", "240 feet."). Each is its own
  blank-line-separated paragraph but is a fragment of the prior entry; rejoin
  it into that entry's `source_text`. The keyword `entry_start` does not match
  these fragments, so they are not miscounted.
- **(Route 9) parentheticals** (Chestnut Street, Ellis Street) name the state
  route; keep them in `location_detail` with the off-ramp/on-ramp phrase.

## Counting rules (manifest)

```json
{"region_start": "the fee established therefor by contract\\.", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "Tow-(away|way)|Parking prohibited|Any vehicle parked|In any fire lane|In any bus stop"}
```

`entry_start` keys off the regulation phrase (not `^[A-Z]`) because the
section has two confounders a leading-capital rule cannot separate:
bare street-name headers ("Beacon Street") would be over-counted, and
capitalized line-wrap continuations ("Everett Street.") would be over-counted,
while the real `(N)` sub-items start with "(" and would be under-counted.
Matching the regulation keyword instead counts exactly the blanket rules,
inline street entries, and `(N)` sub-items — and skips headers and
continuations. Verified: `count_entries` returns 62.

Note the 62 vs 63 gap: the Longfellow/Lothrup PDF merge collapses two
regulations into one counted paragraph (see Source-text quirks). 62 is the
validator-authoritative count and the required row count.

## Proposed common vocabulary

These were defined inline in `schemas/220_tow_zones.json` because
`_common.json` must not be edited by parallel agents. Promote them on the next
shared-vocab pass:

- **`side_set`** — extend the side concept to diagonal bearings and
  comma-joined multi-side sets, so "north and west side" → `north,west` and
  "northeast side" → `northeast`. Suggested pattern:
  `(north|south|east|west|northeast|northwest|southeast|southwest|both)(,(north|south|east|west|northeast|northwest|southeast|southwest))*`.
  The current `common#side` enum lacks the diagonals and is single-valued.
- **`bearing`** — a compass orientation (not travel direction) for measured
  distances: enum `["north","south","east","west","northeast","northwest","southeast","southwest"]`,
  the normalized form of the "-erly" words. Distinct from `common#direction`
  (which is `*bound` travel direction).
