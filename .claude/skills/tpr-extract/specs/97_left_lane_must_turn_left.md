# Section 97 — Left lane must turn left

## Source shape

One boilerplate paragraph ("A left turn only shall be made by a person with a
vehicle in the left lane(s) at any of the following intersections:"), then a
single entry list, one entry per blank-line-separated paragraph, until the
ordinance-history footer beginning `(Ord. No. S-65`. 79 entries as of revision
2025-04-11. Every row is `turn = left` by definition of the section, so there
is no `turn` column.

## Entry grammars observed

Roughly in frequency order:

1. `STREET, DIRECTION onto CROSS.` — the dominant form (comma before
   `onto` varies freely and carries no meaning)
   - "Centre Street, northbound onto Beacon Street."
   - "Crafts Street, westbound, onto Waltham Street."
2. `STREET, DIRECTION at CROSS.` — `at` works like `onto`
   - "Beacon Street, eastbound at Hammond Street."
3. `STREET at CROSS, DIRECTIONS.` — direction(s) trailing
   - "Beacon Street at Centre Street, eastbound and westbound."
   - "Commonwealth Avenue at Walnut Street, all directions."
4. `STREET, DIRECTION onto CROSS CROSSDIRECTION.` — target street carries
   its own carriageway direction
   - "Boylston Street, westbound onto Winchester Street southbound."
5. `STREET, DIRECTION onto CROSS1 or/and CROSS2.` — multi-target forks
   - "Commonwealth Avenue, westbound onto Wachusett Road or Hammond Street."
   - "Langley Road, southbound onto Beacon Street and Sumner Street."
6. `STREET, DIRECTION, into PROPERTY.` — turn into a lot/driveway/address,
   not onto a way
   - "Grove Street, northbound, into 267-287 Grove Street."
7. `STREET, DIRECTION at ADDRESS.` — the point of application is a street
   address
   - "Needham Street, northbound at 233 Needham Street."
8. Trailing parenthetical qualifiers: lanes "(2 left lanes)", positions
   "(opposite Elm Street)", "(between Washington St and Foster St)".

## Normalization rules

- Hyphenated directions normalize to the vocabulary: "north-eastbound" →
  `northeastbound`.
- `DIRECTION and DIRECTION` → comma-joined set: "eastbound and westbound" →
  `eastbound,westbound`.
- `all directions` → direction = `all`.
- Drop a leading article from targets: "onto the Route 9 eastbound on-ramp" →
  cross_street = "Route 9 eastbound on-ramp"; "onto the Jewish Community
  Center Drive" → "Jewish Community Center Drive".
- Parentheses drop from extracted qualifiers: "(2 left lanes)" → lane_detail
  = `2 left lanes`; "(opposite Elm Street)" → location_detail =
  `opposite Elm Street`. Inner abbreviations stay as written ("between
  Washington St and Foster St" — not beautified).
- PDF hyphen-split repair: "Newton- Wellesley Hospital east driveway" →
  cross_street = "Newton-Wellesley Hospital east driveway" (the structured
  field is repaired, `source_text` stays verbatim, and the repair is flagged
  in `notes`).

## Field placement rules

- **The preposition decides the target column.** `onto X` and `at X` with a
  named street/way → `cross_street` (this includes named driveways, drives,
  parkways, and on-ramps: "Angier School Driveway", "Jewish Community Center
  Drive", "Hammond Pond Parkway", "Newton-Wellesley Hospital east driveway",
  "Route 9 eastbound on-ramp"). `into X` → `destination` (property, lot, or
  driveway-of-address). `at X` where X is a street address with a leading
  house number ("at 233 Needham Street") → `destination`.
- **A bare direction word trailing the target street name** goes in
  `cross_street_direction`: "onto Winchester Street southbound" →
  cross_street = "Winchester Street", cross_street_direction = `southbound`.
  A direction embedded in a ramp designation is part of the way's name and
  stays in `cross_street`: "Route 9 eastbound on-ramp", "Route 9 westbound
  on-ramp" — never split these.
- **Multi-target forks stay one row** (the counting rules force one row per
  source entry): keep the conjunction verbatim in `cross_street` —
  "Wachusett Road or Hammond Street", "Beacon Street and Sumner Street",
  "Fenno Road and Homer Street", "Quinobequin Road or Wales Street".
- **Carriageway designations are part of the street name**: street =
  "Commonwealth Avenue, North Drive"; cross_street = "Commonwealth Avenue,
  South Drive" or "Commonwealth Avenue South Drive" exactly as the source
  punctuates each entry (whitespace-collapsed, not beautified).
- **Multi-street approaches keep the full phrase as `street`**: "Winchester
  and Centre Streets" (northbound onto the Route 9 westbound on-ramp).
- Lane phrases go in `lane_detail`, never in `location_detail` or `notes`.
- **Movement and positional qualifiers are data** → `location_detail`:
  "continuing onto Washington Street", "opposite Elm Street", "on Washington
  Street Bridge over Mass. Turnpike", "at the southernmost intersection of
  Dedham Street and Nahanton Street", "between Washington St and Foster St".
  Join multiple distinct qualifiers with `; ` in source order.
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | cross_street | cross_street_direction | destination | lane_detail | location_detail | notes |
|---|---|---|---|---|---|---|---|---|
| Dedham Street, northbound onto Nahanton Street westbound at the southernmost intersection… | Dedham Street | northbound | Nahanton Street | westbound | | | at the southernmost intersection of Dedham Street and Nahanton Street | entry wraps across a blank line in source; rejoined |
| Washington Street, northbound two lanes on Washington Street Bridge over Mass. Turnpike, onto Washington Street. | Washington Street | northbound | Washington Street | | | two lanes | on Washington Street Bridge over Mass. Turnpike | |
| Washington Street, north-eastbound, continuing onto Washington Street (opposite Elm Street). | Washington Street | northeastbound | Washington Street | | | | continuing onto Washington Street; opposite Elm Street | |
| Grove Street, northbound, into 267-287 Grove Street. | Grove Street | northbound | | | 267-287 Grove Street | | | |
| Walnut Street, northbound, into Trio Parking Lot (between Washington St and Foster St). | Walnut Street | northbound | | | Trio Parking Lot | | between Washington St and Foster St | |
| Washington Street, westbound, into Driveway of 2150 Washington Street. | Washington Street | westbound | | | Driveway of 2150 Washington Street | | | |
| Needham Street, northbound at 233 Needham Street. | Needham Street | northbound | | | 233 Needham Street | | | |
| Needham Street, northbound onto Winchester Street (2 left lanes). | Needham Street | northbound | Winchester Street | | | 2 left lanes | | |
| Boylston Street, westbound onto Winchester Street southbound. | Boylston Street | westbound | Winchester Street | southbound | | | | |
| Winchester Street, northbound onto Needham Street northbound. | Winchester Street | northbound | Needham Street | northbound | | | | |
| Centre Street, southbound onto the Route 9 eastbound on-ramp. | Centre Street | southbound | Route 9 eastbound on-ramp | | | | | |
| Winchester and Centre Streets, northbound onto the Route 9 westbound on-ramp. | Winchester and Centre Streets | northbound | Route 9 westbound on-ramp | | | | | |
| Washington Street, westbound onto Newton- Wellesley Hospital east driveway. | Washington Street | westbound | Newton-Wellesley Hospital east driveway | | | | | hyphen split artifact in source ('Newton- Wellesley'); repaired |
| Beacon Street at Centre Street, eastbound and westbound. | Beacon Street | eastbound,westbound | Centre Street | | | | | |
| Commonwealth Avenue at Walnut Street, all directions. | Commonwealth Avenue | all | Walnut Street | | | | | |
| Nahanton Street, eastbound onto the Jewish Community Center Drive. | Nahanton Street | eastbound | Jewish Community Center Drive | | | | | |

## Source-text quirks

- **The Dedham Street entry wraps across a BLANK line and its continuation
  fragment starts uppercase** ("Nahanton Street."). This is why
  `entry_start` cannot be the usual `^[A-Z]` — see counting rules below.
  The extractor must rejoin the fragment into the previous entry's
  `source_text` ("…intersection of Dedham Street and Nahanton Street.").
- The Washington Street Bridge entry wraps across two consecutive lines with
  no blank between them ("…onto Washington / Street."); the paragraph
  splitter joins it automatically, but whitespace-collapse must produce
  "…onto Washington Street." in `source_text`.
- "Newton- Wellesley Hospital east driveway" has a hyphen-space PDF artifact;
  the very next entry spells "Newton-Wellesley" correctly. Repair in
  `cross_street`, keep verbatim in `source_text`, note it.
- Comma placement around the direction varies freely ("westbound onto" /
  "westbound, onto" / "eastbound, at") with no semantic difference.
- Exactly one row must carry a non-empty `cross_street` or a non-empty
  `destination` — never both, never neither (the validator cannot express
  this; check it by eye).

## Counting rules (manifest)

```json
{"region_start": "following intersections:", "region_end": "\\(Ord\\. No\\.", "entry_start": "^[A-Z].*(bound|all directions)"}
```

79 entries as of revision 2025-04-11. The `entry_start` regex requires a
direction token because the Dedham Street entry's line-wrap fragment
("Nahanton Street.") starts uppercase and would be miscounted by `^[A-Z]`.
Every genuine entry names at least one direction ("…bound") or says
"all directions"; verified that the direction-token rule excludes exactly the
one fragment relative to the naive rule. If a future revision adds an entry
with no direction token, the count will under-report and the validator will
fail loudly — revisit this rule then.
