# Section 147 — Obedience to isolated stop signs

## Source shape

Section header plus boilerplate paragraphs (a)–(b); paragraph (b) ends with
"…unless otherwise indicated:". Entries follow, one per blank-line-separated
paragraph, until the ordinance-history footer beginning `(Rev. Ords.`.
989 countable paragraphs as of revision 2026-01-16. Two of those paragraphs
each contain TWO regulations merged by a source-text artifact (see
Source-text quirks), so the section actually states 991 atomic regulations;
the counting contract fixes the row count at 989.

## Entry grammars observed

Roughly in frequency order:

1. `STREET at CROSS, DIRECTION.` → street, cross_street, direction
   - "Acacia Avenue at Lee Road, southbound."
2. `STREET at CROSS, DIRECTION and DIRECTION.` → direction set
   - "Adams Avenue at Sheridan Street, eastbound and westbound."
   - The pair need not be opposites: "Cloverdale Road at Miller Road,
     northbound and westbound."
3. `STREET[,] DIRECTION at CROSS.` → same fields, direction before `at`
   - "Bowdoin Street, southbound at Erie Avenue."
   - "Clifton Road northbound at Hartman Road." (no comma)
4. `STREET at CROSS, all directions.` → direction = `all`
   - "Chase Street at Herrick Road, all directions."
5. `STREET and CROSS, DIRECTION.` — `and` works exactly like `at`
   (9 entries): "Berkeley Street and Prince Street, eastbound and westbound."
   One entry uses `to`: "Crehore Drive to Pierrepont Road, eastbound and
   westbound." (see gold rows).
6. Intersection-wide, no single stop street: "Melrose Street, Staniford
   Street and West Pine Street, all directions." → `street` = full
   designation as written, `cross_street` empty, direction = `all`.
7. Midblock/offset point: `STREET at a point N feet DIR of X, DIRECTION.` →
   offset_feet = N, offset_direction = DIR, offset_from = X
   - "Commonwealth Avenue, North Drive at a point 100 feet east of Irving
     Street, eastbound."
8. Lane/ramp movements: "Hammond Pond Parkway, northbound, from right turn
   lane onto Beacon Street." → lane in `location_detail`, `onto`/`at` target
   in `cross_street`.
9. No direction at all: "Capital Street at Watertown Street." → direction
   empty.

## Normalization rules

- `westerly` / `southerly` (and any other `-erly` form) normalize to the
  corresponding `-bound` value: "Commonwealth Avenue, North Drive at Bullough
  Park, westerly." → direction = `westbound`; "Marriott Hotel Driveway at
  Commonwealth Avenue North Drive, southerly." → `southbound`.
- `DIRECTION and DIRECTION` → comma-joined set in source order:
  "southbound and northbound" → `southbound,northbound`.
- `all directions` → direction = `all`.
- `at the intersection of X` / `at the intersection with X` → cross_street =
  X; the wrapper phrase is dropped ("Chaske Avenue at the intersection of
  Melrose Street, eastbound." → cross_street = Melrose Street).
- `east end` / `west end` are NOT directions → `location_detail`, direction
  empty (John F. Kennedy Circle entries).
- Street names are kept as written, whitespace-collapsed, never beautified:
  "Tamworth road" (lowercase r), "Lagrange Street" vs "LaGrange Street",
  "Commonwealth Avenue South Drive" (missing comma) all stay as-is.
- Parenthetical qualifiers that move to `location_detail` or `notes` drop
  their parentheses; case is preserved.

## Field placement rules

- **`cross_street` = the second-named street** after `at`/`and`/`to`/`onto`.
  Multi-street cross designations stay verbatim in `cross_street`
  ("Homer and Water Streets", "Eddy Street/Eliot Avenue", "Rachel
  Road/Goddard Street", "Henshaw Street, Henshaw Place and Kilburn Road",
  "Short Street and Beacon Street").
- **`cross_street` holds only named streets/ways.** Named ramps and
  carriageways qualify ("Route 9 eastbound ramp", "westbound entrance ramp
  of Route 9", "Commonwealth Avenue, South Drive"). Unnamed targets —
  connector spurs, triangles, islands — go in `location_detail` and
  `cross_street` stays empty.
- **Named carriageways stay in the street name**: "Commonwealth Avenue,
  North Drive" / "South Drive" are part of `street`/`cross_street`
  (matches the 96/148 precedent). **Descriptive roadway qualifiers move to
  `location_detail`**: "Albemarle Road, southern roadway, at Brookside
  Avenue, eastbound." → street = Albemarle Road, location_detail =
  "southern roadway".
- **Parenthetical portion qualifiers stay in the street name** (148 rule):
  "Waban Avenue (one-way southbound portion)" stays intact in
  `cross_street`; "Boylston Street (westbound roadway)" stays intact.
- **Offsets are structured**: `N feet DIR of X` → offset_feet = N,
  offset_direction = DIR, offset_from = X. The three offset columns are
  always filled together. `cross_street` is filled independently when a
  second-named entered street exists ("at Commonwealth Avenue South Drive,
  97 feet east of Centre Street" → cross_street = Commonwealth Avenue South
  Drive, offset_from = Centre Street). For `at a point N feet DIR of X`
  there is no entered street: `cross_street` empty.
- **Positional/lane/ward/approach qualifiers go in `location_detail`** —
  "on traffic island", "west side of triangle at intersection", "Ward 5",
  "northern intersection", "easterly approach", "right turn lane",
  "near 432 Wolcott Street", "east side of triangle". Join multiple
  distinct qualifiers with `; ` in source order.
- **Street-instance qualifiers** ("Hollis Street, north, at…",
  "Wesley Street, south, at…") → street = the bare name, the qualifier
  ("north"/"south") goes in `location_detail`.
- **`from LANE onto/at TARGET`**: the lane phrase goes in `location_detail`,
  TARGET in `cross_street` (148 rule).
- `notes` is reserved for source-text anomalies; it never carries data.

## Proposed common vocabulary

- **`compass_point`** — enum `["north", "south", "east", "west",
  "northeast", "northwest", "southeast", "southwest"]`, description
  "Compass point (e.g. of an offset or side-of-intersection reference)".
  Needed for `offset_direction` here ("100 feet *east* of Irving Street");
  `common#direction` is travel-bound (`eastbound`) and `common#side` is
  side-of-street, so neither fits. Defined inline in
  `schemas/147_stop_signs.json` until adopted into `_common.json`.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here). Empty cells
shown blank; offset columns abbreviated `ft/dir/from`.

| source entry (abbrev.) | street | direction | cross_street | ft/dir/from | location_detail | notes |
|---|---|---|---|---|---|---|
| Comm Ave ND at Higgins St, westbound. Comm Ave ND at Irving St, eastbound. (one paragraph) | Commonwealth Avenue, North Drive | westbound | Higgins Street | | | source paragraph merges a second entry (at Irving Street, eastbound; missing blank line); one row per counting contract — see spec |
| Jacobs Terrace at Hartman Road, southbound. Jackson Street at Langley Road… (one paragraph) | Jacobs Terrace | southbound | Hartman Road | | | source paragraph merges a second entry (Jackson Street at Langley Road, eastbound and westbound); one row per counting contract — see spec |
| Comm Ave ND at Comm Ave South Drive, 97 feet east of Centre Street, southbound (rejoined fragment) | Commonwealth Avenue, North Drive | southbound | Commonwealth Avenue South Drive | 97/east/Centre Street | | |
| Comm Ave ND at a point 100 feet east of Irving Street, eastbound | Commonwealth Avenue, North Drive | eastbound | | 100/east/Irving Street | | |
| Commonwealth Avenue, northbound crossover from South Drive to North Drive, 253 feet west of Ransom Road | Commonwealth Avenue | northbound | | 253/west/Ransom Road | crossover from South Drive to North Drive | |
| East Side Parkway on the east side of the channelized island 76 feet south of Newtonville Avenue, southbound | East Side Parkway | southbound | | 76/south/Newtonville Avenue | east side of the channelized island | |
| Waban Avenue at Waban Avenue, southbound (approximately 120 feet south of Manitoba Road. | Waban Avenue | southbound | Waban Avenue | 120/south/Manitoba Road | | offset approximate in source; unclosed parenthesis in source |
| Waban Avenue (two-way portion, westbound direction) at Waban Avenue (one-way southbound portion). | Waban Avenue (two-way portion, westbound direction) | westbound | Waban Avenue (one-way southbound portion) | | | |
| Clark Street southbound on the traffic island… Clark Street and Rowena Road intersection (rejoined fragment) | Clark Street | southbound | Rowena Road | | on the traffic island at the northwest corner of the intersection | |
| Chestnut Street at Boylston Street, northbound at the eastbound ramp and southbound at the westbound ramp | Chestnut Street | northbound,southbound | Boylston Street | | northbound at the eastbound ramp and southbound at the westbound ramp | |
| Centre Street at connector spur from Sargent Street (east of the traffic island), southeastbound | Centre Street | southeastbound | | | at connector spur from Sargent Street; east of the traffic island | |
| Highland Street, at the connector between Highland Street and Chestnut Street, westbound, at Chestnut Street | Highland Street | westbound | Chestnut Street | | at the connector between Highland Street and Chestnut Street | |
| I-95 North, exit 21, dedicated left turn lane at Washington Street, northwestbound | I-95 North | northwestbound | Washington Street | | exit 21; dedicated left turn lane | |
| Crehore Drive to Pierrepont Road, eastbound and westbound | Crehore Drive | eastbound,westbound | Pierrepont Road | | | source reads 'to' where the list grammar elsewhere uses 'at' |
| Montclair Road at the intersection with Short Street and Beacon Street | Montclair Road | | Short Street and Beacon Street | | | |
| Melrose Street, Staniford Street and West Pine Street, all directions | Melrose Street, Staniford Street and West Pine Street | all | | | | |
| John F. Kennedy Circle at Green Street, east end | John F. Kennedy Circle | | Green Street | | east end | |
| Hollis Street, north, at Centre Street, westbound | Hollis Street | westbound | Centre Street | | north | |
| Homer Street, northbound, right turn lane at Commonwealth Avenue, South Drive, northbound | Homer Street | northbound | Commonwealth Avenue, South Drive | | right turn lane | direction stated twice in source |
| Hammond Pond Parkway, northbound, from right turn lane onto Beacon Street | Hammond Pond Parkway | northbound | Beacon Street | | from right turn lane | |
| Wells Avenue westbound from left-turn lane at Wells Avenue | Wells Avenue | westbound | Wells Avenue | | from left-turn lane | |
| Waltham Street at triangle facing Waltham, opposite Lyme Road, northwestbound | Waltham Street | northwestbound | | | at triangle facing Waltham; opposite Lyme Road | |
| Clark Street at the westbound entrance ramp of Route 9, eastbound | Clark Street | eastbound | westbound entrance ramp of Route 9 | | | |
| Peirce Elementary School parking lot, southbound at Ruane Road | Peirce Elementary School parking lot | southbound | Ruane Road | | | |

## Source-text quirks

- **Two merged paragraphs.** Two entries each got joined to their
  predecessor with no blank line between, forming single paragraphs that
  contain two regulations:
  1. "Commonwealth Avenue, North Drive at Higgins Street, westbound.
     Commonwealth Avenue, North Drive at Irving Street, eastbound."
  2. "Jacobs Terrace at Hartman Road, southbound. Jackson Street at Langley
     Road, eastbound and westbound."
  The validator counts each as ONE entry, so each gets ONE row: structure
  the FIRST statement, keep the full merged paragraph verbatim as
  `source_text`, and flag the second statement in `notes` (gold rows above).
  The second regulation is recoverable from `source_text`; if the source
  text is ever re-split upstream, the count rises by 2 and these become four
  normal rows.
- **Two lowercase continuation fragments** from PDF line-wrap must be
  rejoined into the previous entry's `source_text`: "intersection." (the
  Clark Street traffic-island entry) and "southbound." (the Comm Ave
  North-at-South-Drive 97-feet entry). `entry_start: ^[A-Z]` excludes them
  from the count automatically.
- A handful of entries lack the trailing period ("Alderwood Road at Centre
  Street, westbound", "West Street at Watertown Street, northbound",
  "Oldham Road at Commonwealth Avenue, South Drive, southbound") —
  reproduce verbatim in `source_text`.
- Missing commas before the direction occur ("Commonwealth Avenue, North
  Drive southbound", "Garrison Street at Commonwealth Avenue, North Drive
  southbound.") — parse normally, no note needed.
- The Waban-at-Waban entry has an unclosed parenthesis and an "approximately"
  offset — note both, reproduce verbatim in `source_text`.
- Inconsistent street-name casing is in the source ("Tamworth road",
  "Lagrange Street") — keep as written, no note needed.
- Near-duplicate pairs are real separate entries (e.g. "Adena Road at Derby
  Street, northbound." and "…southbound."; "Cobb Place at Dwhinda Road,
  eastbound."/"westbound."); there are no exact duplicate paragraphs, so
  `source_text` uniqueness holds without intervention.

## Counting rules (manifest)

```json
{"region_start": "unless otherwise indicated:", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```

Verified against revision 2026-01-16: 991 paragraphs in the region, of which
2 are lowercase continuation fragments → **989 entries**, hence 989 TSV rows
(two of them covering merged double-regulation paragraphs as described
above).
