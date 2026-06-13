# Section 145 — Traffic-control signal locations

## Source shape

Three entry lists in one dataset, distinguished by `signal_type` and `owner`:

- (a) "Traffic control signals shall be placed at the following locations:"
  → `signal_type = traffic_signal`, `owner` empty (104 entries as of
  revision 2025-04-11)
- (b) "Pedestrian hybrid beacons shall be placed at the following
  locations:" → `signal_type = pedestrian_hybrid_beacon`, `owner` empty
  (4 entries)
- (c) "Traffic signals at the following locations are owned, operated and
  maintained by the state:" → `signal_type = traffic_signal`,
  `owner = state` (16 entries)

124 entries total. Entries end at the ordinance-history footer beginning
`(Rev. Ords.`. The (b) and (c) header paragraphs start with `(` so the
counting rules skip them automatically.

## Entry grammars observed

Roughly in frequency order:

1. `STREET and CROSS.` — plain two-leg intersection
   - "Beacon Street and Centre Street."
2. `STREET, CROSS and THIRD.` / `STREET, CROSS, THIRD and FOURTH.`
   (Oxford comma optional) — multi-leg intersection; first-named way →
   `street`, second → `cross_street`, rest → `additional_streets` joined
   with `; ` in source order
   - "Watertown Street, Edinboro Street, Page Road and Walker Street."
3. `STREET at CROSS[, DIRECTION].` — `at` works like `and` when the target
   is a named way; a trailing standalone direction fills `direction`
   - "Washington Street at Centre Avenue, eastbound."
4. `STREET at LANDMARK.` — landmark target is not a way → whole `at` phrase
   in `location_detail`, `cross_street` empty
   - "Lexington Street at Burr School."
5. `STREET near REF.` — proximity entry: signal is near but not stated to
   be at the junction → `from_point = REF`, `cross_street` empty
   - "Dedham Street near Oak Hill Street."
6. `STREET, N feet DIRECTION of REF.` — midblock offset →
   `from_point = REF`, `offset_feet = N`, `offset_direction = DIRECTION`
   - "Walnut Street, 100 feet north of Trowbridge Avenue."
7. `STREET[,] between X and Y[, at LANDMARK].` — segment entry (subsection
   (b) only) → `from_point = X`, `to_point = Y`, landmark phrase →
   `location_detail`
   - "Parker Street, between Daniel Street and Athelstane Road."

## Normalization rules

- Collapse all internal whitespace to single spaces; rejoin PDF line-wrap
  fragments into the previous entry's `source_text` (see quirks).
- `additional_streets` joins ways with `; ` (semicolon-space), never commas
  — way names can contain commas and the source's own list separator is a
  comma.
- Trailing periods: two entries lack them in the source ("Washington Street
  near Bacon Street", "Washington Street near Greenough Street") — keep
  `source_text` exactly as written, do not add the period.
- `offset_direction` uses bare compass points (north/east/…), not
  `common#direction` travel directions.

## Field placement rules

- **First-named way is always `street`**, second is `cross_street`, the
  rest go to `additional_streets` in source order. Do not reorder or
  beautify.
- **In the comma/`and` list grammar every element is a named way**, even
  facility-named ones: "Riverside Center", "Newton-Wellesley Hospital
  Driveway", "Woodland MBTA Station Driveway", "Chestnut Hill Mall
  Driveway" all go in `cross_street`/`additional_streets`. Only `at`
  phrases naming non-way landmarks go to `location_detail` (grammar 4).
- **Ramp and carriageway designations stay whole in the way columns**:
  "Massachusetts Turnpike Interchange 17 WB On/Off-Ramp", "Massachusetts
  Turnpike Interchange 16 Eastbound On-Ramp", "Boylston Street (Route 9)
  eastbound onramp and offramp", "Boylston Street (Route 9) westbound
  offramp". The embedded direction word is part of the facility name —
  it never fills `direction`.
- **Ways named "X to Y"** are ramp designations (148 precedent): "Grove
  Street to Route 16 Collector-Distributor Road" is one way name.
- **`direction` is filled only by a standalone trailing qualifier**, i.e.
  the four "Washington Street at Centre Avenue, eastbound./westbound."
  entries ((a) and (c) copies).
- **Parenthetical leg qualifiers stay in the way name** (148 precedent):
  "Auburn Street (east)", "Auburn Street (west)", "Boylston Street
  (Route 9)", "Washington Street (Route 16)".
- **"(shared with City of Boston)" is jurisdiction data**, not a note →
  `owner = shared with City of Boston`; drop the parenthetical from the
  way columns (it qualifies the signal, not a street name).
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | cross_street | additional_streets | signal_type | direction | from_point | to_point | offset_feet | offset_direction | owner | location_detail |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Centre Street, Charlesbank Road, … 17 WB On/Off-Ramp, and Washington [wrap] Street. | Centre Street | Charlesbank Road | Massachusetts Turnpike Interchange 17 WB On/Off-Ramp; Washington Street | traffic_signal | | | | | | | |
| Centre Street, … 17 Eastbound On-Ramp, Park Street, St. James Street, and [wrap] Washington Street. | Centre Street | Massachusetts Turnpike Interchange 17 Eastbound On-Ramp | Park Street; St. James Street; Washington Street | traffic_signal | | | | | | | |
| Commonwealth Avenue, Fr. Herlihy and Lake Street (shared with City of Boston). | Commonwealth Avenue | Fr. Herlihy | Lake Street | traffic_signal | | | | | | shared with City of Boston | |
| Centre Street and Tyler Terrace at the Fire Department Headquarters. | Centre Street | Tyler Terrace | | traffic_signal | | | | | | | at the Fire Department Headquarters |
| Lexington Street at Burr School. | Lexington Street | | | traffic_signal | | | | | | | at Burr School |
| Middlesex Road at Brimmer and May School. | Middlesex Road | | | traffic_signal | | | | | | | at Brimmer and May School |
| Dedham Street near Oak Hill Street. | Dedham Street | | | traffic_signal | | Oak Hill Street | | | | | |
| Walnut Street, 100 feet north of Trowbridge Avenue. | Walnut Street | | | traffic_signal | | Trowbridge Avenue | | 100 | north | | |
| Washington Street at Centre Avenue, eastbound. [(a) copy] | Washington Street | Centre Avenue | | traffic_signal | eastbound | | | | | | |
| Washington Street at Centre Avenue, eastbound. [(c) copy] | Washington Street | Centre Avenue | | traffic_signal | eastbound | | | | | state | |
| Grove Street and Riverside Center. | Grove Street | Riverside Center | | traffic_signal | | | | | | | |
| Beacon Street, 70 feet east of Lawrence Avenue. | Beacon Street | | | pedestrian_hybrid_beacon | | Lawrence Avenue | | 70 | east | | |
| Beacon Street between Collins Road and Windsor Road, at the staircase… | Beacon Street | | | pedestrian_hybrid_beacon | | Collins Road | Windsor Road | | | | at the staircase to the Waban train station |
| Boylston Street (Route 9) eastbound onramp and offramp and Parker Street. | Boylston Street (Route 9) eastbound onramp and offramp | Parker Street | | traffic_signal | | | | | | state | |
| Boylston Street (Route 9) westbound offramp and Parker Street and Clark Street Extension. | Boylston Street (Route 9) westbound offramp | Parker Street | Clark Street Extension | traffic_signal | | | | | | state | |
| Washington Street (Route 16), Grove Street to Route 16 Collector-Distributor Road, Quinobequin Road and Wales Street. | Washington Street (Route 16) | Grove Street to Route 16 Collector-Distributor Road | Quinobequin Road; Wales Street | traffic_signal | | | | | | state | |

The "Brimmer and May School" and "onramp and offramp" entries contain `and`
inside a single name — split the source list on `and`/commas only between
way names, never inside one.

## Source-text quirks

- **Two PDF line-wrap fragments start UPPERCASE** ("Street.",
  "Washington Street.") — the two long Centre Street interchange entries
  wrap mid-name. The plain `^[A-Z]` entry_start would over-count by 2, so
  this section's entry_start additionally requires a connective
  (`,`, ` and `, ` at `, ` near `) somewhere in the paragraph; the
  fragments contain none. The extractor must rejoin the fragments into the
  previous entry's `source_text`.
- **Two entries are verbatim duplicates between (a) and (c)**:
  "Washington Street at Centre Avenue, eastbound." and "…, westbound."
  appear in both lists (the (a) entries place them; the (c) entries declare
  them state-owned). Both occurrences are real entries and get rows
  (counting demands 124). To keep `source_text` unique, the **(c) copies
  are prefixed with the subsection label `(c) `** (verbatim from the (c)
  header), e.g. `(c) Washington Street at Centre Avenue, eastbound.`
  This is the only sanctioned deviation from verbatim `source_text`; apply
  it to no other rows. Put "also listed in subsection (a)" / "(c)" in
  `notes` on all four rows.
- Two entries lack trailing periods ("Washington Street near Bacon
  Street", "Washington Street near Greenough Street") — reproduce as-is.
- "Fr. Herlihy" appears without a way-type suffix (Way/Street); keep
  as written, no note needed.
- The ordinance footer contains a run-together citation
  ("TPR-204, 05-28-15TPR-212") — outside the counting region, ignore.

## Proposed common vocabulary

`compass_point` — bare compass directions for offset/relative-position
qualifiers, distinct from `direction` (travel) and `side` (which mixes in
both/odd/even):

```json
"compass_point": {
  "description": "Bare compass point for offsets and relative positions",
  "enum": ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
}
```

Used here inline as `offset_direction`'s enum (not added to `_common.json`
because other agents are editing in parallel). Sections 148/176-style
"N feet DIRECTION of X" grammars will want the same def; promote it to
`_common.json` and switch this schema to `"$ref": "common#compass_point"`
when convenient.

## Counting rules (manifest)

```json
{
  "region_start": "Traffic control signals shall be placed at the following locations:",
  "region_end": "\\(Rev\\. Ords\\.",
  "entry_start": "^[A-Z].*(,| and | at | near )"
}
```

Counts all three lists (124 as of revision 2025-04-11: 104 + 4 + 16). The
(b)/(c) header paragraphs start with `(` and the two uppercase wrap
fragments contain no connective, so all four are skipped. Verified with
`scripts/validate.py`'s `count_entries`.
