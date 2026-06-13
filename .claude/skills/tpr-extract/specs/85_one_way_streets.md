# Section 85 — One-way streets

## Source shape

One boilerplate paragraph ("Upon the following streets or parts of streets
vehicular traffic shall move only in the direction indicated below:"), then
entries until the ordinance-history footer, which in this section reads
`(Rev . Ords.` — note the stray space before the period (PDF artifact).

Two paragraph shapes carry entries:

1. **Simple entries** — one blank-line-separated paragraph per street:
   "Acacia Avenue, from Beacon Street to Lee Road."
2. **Grouped entries** — a header paragraph naming the street and ending
   with a colon ("Commonwealth Avenue:"), followed by numbered paragraphs
   `(1) …`, `(2) …`. Each numbered paragraph is one atomic regulation (one
   row); the header is NOT a row — it only supplies `street`.

11 groups as of revision 2025-04-11: Albemarle Road (3), Centre Street (2),
College Road (2), Commonwealth Avenue (14), Grafton Street (2), Page Road
(2), Park Street (3), Sumner Street (3), Vernon Street (2), Washington Park
(2), Washington Street (5) — 40 numbered rows, plus 70 simple entries =
**110 rows**.

Hagen Road appears twice as two separate simple entries (different
segments), not as a group — two rows, no special handling.

## Entry grammars observed

1. `STREET, from A to B.` — the dominant form. from_point = A,
   to_point = B, direction EMPTY (the from→to order is the direction;
   see normalization rule 1).
   - "Acacia Avenue, from Beacon Street to Lee Road."
2. `STREET, from A DIRECTLY-ADVERB to B.` — adverb states the heading:
   - "Bowen Street, from Centre Street westerly to Homer Street." →
     direction = westbound.
3. `STREET, DIRECTION, from A to B.` — bound-form direction:
   - "Waban Avenue, southbound, from Beacon Street to Collins Road."
4. `STREET, ADVERB from A to B.` — "Charlesbank Road, westerly from
   St. James Street to Centre Street."
5. Offset endpoints: `from a point N feet DIR of X` / `to a point N feet
   DIR of X` → anchor X in from_point/to_point, N in *_offset_feet, DIR in
   *_offset_direction.
   - "Jefferson Street, from a point 205 feet east of Centre Street to
     Williams Street."
6. Length extent instead of a second endpoint:
   - "(1) North Drive from the Boston line two hundred fifteen (215) feet
     westerly." → from_point = Boston line, length_feet = 215,
     direction = westbound, to_point empty.
7. Whole-street with direction only: "Hull Street, westerly." →
   direction = westbound, no endpoints.
8. Loop entries: `STREET, loop portion, counterclockwise direction.` →
   roadway = "loop portion", direction = counterclockwise (Stein Circle,
   Waban Park, Walnut Park).
9. Roadway-portion sub-entries: "(1) Southern roadway, from Eddy Street to
   Brookside Avenue." / "(2) North Drive, from a point 215 ft west of the
   Boston line westerly to Mt. Alvernia Road." → the portion designator
   goes in `roadway`.
10. Carriageway crossovers (Commonwealth Avenue (4) and (13)): "Crossing
    over to/the X from/to the Y, at/opposite Z." → roadway = "crossover";
    see gold rows.
11. Vehicle exception suffix: ", except non-motorized vehicles." →
    exception = "non-motorized vehicles".

## Normalization rules

1. **Direction is never inferred.** Most entries state no direction word;
   the from→to order IS "the direction indicated below". Leave `direction`
   empty for those rows. Fill it only when the source has an explicit
   adverb ("westerly"), bound form ("northbound"), or "counterclockwise
   direction".
2. `-erly` adverbs → `-bound`: westerly → westbound, southerly →
   southbound, southeasterly → southeastbound, etc.
3. "southwesterly and southeasterly" → comma-joined set
   `southwestbound,southeastbound` (Crescent Square).
4. PDF-split "north eastbound" (Baldpate Hill Road) → northeastbound.
5. "counterclockwise direction" → `counterclockwise`.
6. Spelled-out numbers with numerals — "two hundred fifteen (215) feet",
   "one hundred eighty-seven and five-tenths (187.5) feet" — take the
   numeral: 215, 187.5. "215 ft" (Comm. Ave. (2)) is feet.
7. Drop leading articles from endpoints: "the Boston line" → "Boston
   line", "the Massachusetts Turnpike ramp" → "Massachusetts Turnpike
   ramp", "the end of the public way portion" → "end of the public way
   portion".
8. Exceptions drop the leading "except": "except non-motorized vehicles"
   → `non-motorized vehicles`.

## Field placement rules

- **Group headers supply `street` only.** Sub-entry rows repeat the header
  street; the header paragraph itself is never a row.
- **`roadway` holds carriageway/portion designators**: "North Drive",
  "South Drive", "Southern roadway", "Eastern roadway", "Western and
  northern roadway", "east roadway", "west roadway", "north fork",
  "loop portion", "crossover". Never fold these into `street` or
  `location_detail`.
- **Endpoints may be features, not just streets**: municipal lines
  ("Boston line", "Brookline border", "Weston line"), ramps, "westerly end
  of the loop at Newton Corner", "west end of the median strip near the
  Weston line", "end of the public way portion", "No. 22" (a street
  number on the entry's own street — Court Street), "Collins Road/Collins
  Road intersection", "Rowe Street Extension" (a named way; keep whole).
- **Fuzzy endpoint qualifiers stay in the endpoint cell** (deviation from
  148, where position qualifiers go in `location_detail`: here the
  qualified phrase IS the endpoint): "near Auburn Street" → from_point =
  "near Auburn Street"; "opposite Elm Street" → to_point = "opposite Elm
  Street". Geocoders strip the qualifier; the named street stays in the
  geocodable column.
- **Offset micro-grammar is decomposed**: "a point N feet DIR of X" never
  appears verbatim in an endpoint cell — anchor in `*_point`, N in
  `*_offset_feet`, DIR in `*_offset_direction`.
- **`location_detail`** takes non-endpoint qualifiers: "at Kenrick Park"
  (Park Street (1)/(2)), "at triangle" (Grafton (2)), "on the southwest
  leg" (Baldpate), "on that part of Centre Street known as Centre Green"
  (Centre Street (1)), "Ward 3" (Warren Avenue), "(bridge over Turnpike)"
  → "bridge over Turnpike" (Washington (3)), and the crossover positions
  "opposite Water Street" / "at Rowe Street west intersection".
- **`notes` never carries data** — anomaly remarks only.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | roadway | direction | from_point | from_offset_feet | from_offset_dir | to_point | to_offset_feet | to_offset_dir | length_feet | location_detail | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Baldpate Hill Road, from a point 450 feet west of Brookline Street continuing 50 feet… | Baldpate Hill Road | | northeastbound | Brookline Street | 450 | west | | | | 50 | on the southwest leg | source repeats '50 feet' and states 'one way' redundantly; 'north eastbound' split in source |
| Comm. Ave. (1) North Drive from the Boston line two hundred fifteen (215) feet westerly | Commonwealth Avenue | North Drive | westbound | Boston line | | | | | | 215 | | |
| Comm. Ave. (4) Crossing over to … Carriage Lane (north drive) from the main portion… | Commonwealth Avenue | crossover | | main portion of Commonwealth Avenue (south drive) | | | Commonwealth Avenue Carriage Lane (north drive) | | | | opposite Water Street | from/to assigned by the 'from'/'to' words, not text order |
| Comm. Ave. (12) South Drive, from a point one hundred eighty-seven and five-tenths (187.5) feet west of the Boston line, easterly to the Boston line | Commonwealth Avenue | South Drive | eastbound | Boston line | 187.5 | west | Boston line | | | | | |
| Comm. Ave. (13) Crossing over the … Carriage Lane (north drive) to the main portion… | Commonwealth Avenue | crossover | | Commonwealth Avenue Carriage Lane (north drive) | | | main portion of Commonwealth Avenue (south drive) | | | | at Rowe Street west intersection | |
| Comm. Ave. (14) South Drive, from near Auburn Street easterly to Woodbine Street | Commonwealth Avenue | South Drive | eastbound | near Auburn Street | | | Woodbine Street | | | | | |
| Court Street, from Central Avenue to No. 22 | Court Street | | | Central Avenue | | | No. 22 | | | | | 'No. 22' is a street number on Court Street |
| Collins Road, northbound, from the Collins Road/Collins Road intersection… | Collins Road | | northbound | Collins Road/Collins Road intersection | | | Beacon Street | | | | | self-intersection as written in source |
| Crescent Square, … southwesterly and southeasterly to Waban Street | Crescent Square | | southwestbound,southeastbound | Thornton Street | | | Waban Street | | | | | |
| Grafton Street (2) on north fork at triangle westerly to Homer Street | Grafton Street | north fork | westbound | | | | Homer Street | | | | at triangle | no start point stated |
| Hull Street, westerly | Hull Street | | westbound | | | | | | | | | |
| Stein Circle, loop portion, counterclockwise direction | Stein Circle | loop portion | counterclockwise | | | | | | | | | |
| Vernon Street (1) from Baldwin Street to a point 325 feet east of Centre Street | Vernon Street | | | Baldwin Street | | | Centre Street | 325 | east | | | |
| Washington Street (2) northerly from a point 100 feet south of Centre Street to Centre Street | Washington Street | | northbound | Centre Street | 100 | south | Centre Street | | | | | |
| Washington Street (5) from Perkins Street easterly to opposite Elm Street | Washington Street | | eastbound | Perkins Street | | | opposite Elm Street | | | | | |

## source_text construction

- Simple entries: the paragraph verbatim, whitespace-collapsed.
- Numbered sub-entries: prefix the group header (with its colon), joined
  by a single space — "Commonwealth Avenue: (2) North Drive, from a point
  215 ft west of the Boston line westerly to Mt. Alvernia Road." This
  keeps each row's provenance self-contained and uniqueness robust even
  if two groups ever share identical numbered text.
- Split entries (see quirks): rejoin fragments with a single space —
  except when the first fragment ends with a hyphen, then join with no
  space, healing the hyphen-wrap ("except non-" + "motorized vehicles."
  → "except non-motorized vehicles.").

## Source-text quirks

- **Capital-letter continuation fragments.** PDF line-wrap splits four
  entries across blank lines, and two of the fragments start with a
  CAPITAL letter — the usual `^[A-Z]` heuristic would miscount them:
  - Comm. Ave. (4): "…from the main portion of" + "Commonwealth Avenue
    (south drive), opposite Water Street."
  - Comm. Ave. (13): "…to the main portion of Commonwealth" + "Avenue
    (south drive), at Rowe Street west intersection."
  - Comm. Ave. (5): "…except non-" + "motorized vehicles." (lowercase)
  - Comm. Ave. (12): "…west of the Boston line," + "easterly to the
    Boston line." (lowercase)
  The counting `entry_start` regex below excludes the capital fragments
  because a parenthesis precedes their first comma — this is load-bearing;
  re-verify if the section text changes.
- The ordinance footer reads `(Rev . Ords.` with a space before the
  period; `region_end` must match that form.
- Baldpate Hill Road states the 50-foot length twice and includes a
  redundant "one way"; "north eastbound" is split by a wrap. Note it.
- Comm. Ave. (11) says "Windermere Street" where (5)/(6) say "Windermere
  Road" — transcribe each as written; never reconcile.
- Comm. Ave. (2) uses the abbreviation "ft".
- Group sub-entries under Page Road are indented with a leading space in
  the raw text; the validator strips per-line whitespace so this is
  invisible to counting.

## Counting rules (manifest)

```json
{
  "region_start": "direction indicated below:",
  "region_end": "\\(Rev \\. Ords\\.",
  "entry_start": "^(\\(\\d+\\)|[A-Z][^():]*,)"
}
```

Verified count: **110** (70 simple + 40 numbered) as of revision
2025-04-11. `entry_start` counts numbered sub-entries `(n) …` and
capital-letter paragraphs whose first comma precedes any parenthesis or
colon; it skips the 11 group headers (colon before any comma) and all
four continuation fragments (the two capital ones have "(south drive)"
before their first comma).

## Proposed common vocabulary

Not added to `_common.json` (parallel agents); defined inline in this
dataset's schema. Candidates for promotion:

1. **`compass_point`** — bare compass bearings used by offset phrases
   ("a point 450 feet **west** of Brookline Street"):
   `["north", "south", "east", "west", "northeast", "northwest",
   "southeast", "southwest"]`. `common#side` is close but carries
   `both/odd/even` and lacks intercardinals; a distinct def is cleaner.
   Used here by `from_offset_direction` and `to_offset_direction`.
2. **`counterclockwise` (and `clockwise`) in `common#direction` /
   `common#direction_set`** — loop roadways (Stein Circle, Waban Park,
   Walnut Park) are one-way "counterclockwise direction"; this dataset's
   `direction` column inlines the `direction_set` pattern extended with
   `counterclockwise`.
