# Section 146 — Flashing warning light locations

## Source shape

One boilerplate sentence ending "…shall be placed at the following locations:".
Entries follow, one per blank-line-separated paragraph, until the
ordinance-history footer beginning `(Rev. Ords.`. 63 entries as of revision
2025-04-11. No lowercase continuation fragments and no header paragraphs
inside the entry region (unusually clean for this PDF).

## Entry grammars observed

Two location shapes crossed with a trailing parenthetical signal descriptor:

1. **Intersection**: `STREET at CROSS (DESCRIPTOR).` — `at` and `and` are
   equivalent connectives.
   - "Adams Street at Middle Street (pedestrian activated RRFB)."
   - "Commonwealth Avenue and Oldham Road (flashing yellow)."
2. **Offset point**: `STREET, N feet COMPASS of REF (DESCRIPTOR).` — also the
   wordier `STREET at a point N feet COMPASS of REF (DESCRIPTOR).`
   - "Beacon Street, 20 feet east of Herrick Road (pedestrian activated RRFB)."
   - "Homer Street at a point 500 feet west of Walnut Street (flashing yellow
     pedestrian activated)."
3. **Direction of travel** (3 entries) appears between street and `at`:
   "Charlesbank Road, westbound, at St. James Street (flashing yellow)." —
   the comma after the direction is sometimes missing ("St. James Terrace,
   southbound at Charlesbank Road (flashing red).").
4. **Colon variant** (2 entries): the descriptor follows a colon and starts
   capitalized: "Waverley Avenue and Franklin Street: Flashing yellow
   (pedestrian activated)."
5. **Between variant** (1 entry): "Cypress Street, between the Cypress Street
   Parking Area entrance and exit (pedestrian activated RRFB)."

Signal descriptors observed: `(pedestrian activated RRFB)` (the bulk),
`(flashing yellow)`, `(flashing red)`, `(flashing yellow pedestrian
activated)`, `: Flashing yellow (pedestrian activated)`, `: Flashing yellow
(pedestrian activated RRFB)`, and one entry with no descriptor at all.

## Normalization rules

- Signal descriptor decomposes into two columns:
  - `signal_type`: `RRFB` → `rrfb`; `flashing yellow` → `flashing_yellow`;
    `flashing red` → `flashing_red`.
  - `pedestrian_activated`: `yes` iff the descriptor contains "pedestrian
    activated"; empty otherwise (plain `(flashing yellow)` / `(flashing red)`
    entries do not state activation — leave empty, do not guess).
  - "flashing yellow pedestrian activated" → `signal_type = flashing_yellow`,
    `pedestrian_activated = yes`.
  - When a descriptor names **both** flashing yellow and RRFB ("Flashing
    yellow (pedestrian activated RRFB)"), RRFB wins: an RRFB is by definition
    a yellow rapid-flashing device, so `signal_type = rrfb` — the more
    specific device type.
- Offset phrases decompose fully: "115 feet north of Crescent Avenue" →
  `offset_feet = 115`, `offset_direction = north`, `cross_street = Crescent
  Avenue`, `location_detail` empty. The "at a point" wording adds nothing —
  same decomposition.
- Compass words in offsets are bare points (north/…/southwest), distinct
  from the `-bound` travel directions in `direction`.
- Landmark references drop the leading article: "the Boston College Driveway"
  → `Boston College Driveway`; "the Brookline town line" → `Brookline town
  line`; "the Upper Falls Greenway" → `Upper Falls Greenway`.
- Street names are copied **as written** — including suspected typos — and
  the suspicion is flagged in `notes` (see quirks). Never silently "fix" a
  name; never carry the suspicion only in your head.

## Field placement rules

- **`cross_street` holds only named public streets/ways** (Street, Road,
  Avenue, Lane, Court, Circle, Terrace, Path, Parkway, Place…). Parks,
  greenways, driveways, parking areas, and town lines go in `landmark`
  ("Cold Springs Park", "Upper Falls Greenway", "Boston College Driveway",
  "Brookline town line"). Exactly one of `cross_street`/`landmark` is set
  per row except the no-reference case (none observed).
- **Slash-joined dual designations stay verbatim in `cross_street`**:
  "Hartman Road/Spaulding Lane", "Hyde Street/Woodcliff Road" — these are
  opposite legs of one intersection, not two rows.
- **Leg qualifiers go in `location_detail`**: "Crafts Street at Albemarle
  Road, eastern leg" → `cross_street = Albemarle Road`,
  `location_detail = eastern leg`.
- `offset_feet`/`offset_direction` are set together or not at all; the
  reference point of an offset goes in `cross_street` (named way) or
  `landmark` (feature), same rule as intersections.
- The signal descriptor never leaks into `location_detail` or `notes`; it
  lives only in `signal_type`/`pedestrian_activated` (and verbatim in
  `source_text`).
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | cross_street | landmark | offset_feet | offset_direction | signal_type | pedestrian_activated | location_detail | notes |
|---|---|---|---|---|---|---|---|---|---|
| Centre Street at Hyde Street/Woodcliff Road. | Centre Street | Hyde Street/Woodcliff Road | | | | | | | signal type not stated in source |
| Cypress Street, between the … Parking Area entrance and exit | Cypress Street | | Cypress Street Parking Area | | | rrfb | yes | between the entrance and exit | |
| Crafts Street at Albemarle Road, eastern leg | Crafts Street | Albemarle Road | | | | rrfb | yes | eastern leg | |
| Hammond Pond Parkway, 700 feet north of the Boston College Driveway | Hammond Pond Parkway | | Boston College Driveway | 700 | north | rrfb | yes | | |
| Lagrange Street, 60 feet south of the Brookline town line | Lagrange Street | | Brookline town line | 60 | south | rrfb | yes | | |
| Neeham Street, 185 feet southwest of Easy Street | Neeham Street | Easy Street | | 185 | southwest | rrfb | yes | | street as written; likely 'Needham Street' (adjacent entries) |
| Waverley Avenue and Franklin Street: Flashing yellow (pedestrian activated). | Waverley Avenue | Franklin Street | | | | flashing_yellow | yes | | |
| Waverley Avenue and Arlington Street: Flashing yellow (pedestrian activated RRFB). | Waverley Avenue | Arlington Street | | | | rrfb | yes | | descriptor names both flashing yellow and RRFB; see spec |
| St. James Terrace, southbound at Charlesbank Road (flashing red). | St. James Terrace | Charlesbank Road | | | | flashing_red | | | |

(`direction` is empty in all gold rows above except St. James Terrace, where
it is `southbound`.)

## Source-text quirks

- **"Neeham Street"** (185 feet southwest of Easy Street) is almost certainly
  a typo for "Needham Street" — two adjacent entries use Needham Street with
  the same grammar. Keep `street` verbatim, flag in `notes`.
- **"Elliot Street" vs "Elliott Street"** appear in consecutive entries
  (Wetherell Street / Cottage Street). Both spellings stay as written; no
  note required — there is no in-document basis to pick one.
- **Stray punctuation** before descriptors needs no note, just verbatim
  `source_text`: "…east of Manet Road. (pedestrian activated RRFB)." (stray
  period), "…375 feet west of Walnut Street: (flashing yellow pedestrian
  activated)." (stray colon).
- "Beacon Street at Cold Springs Park" — the park is the reference →
  `landmark = Cold Springs Park` (the city's park is usually spelled "Cold
  Spring Park"; copy as written, no note — same policy as Elliot/Elliott).
- One entry has **no signal descriptor** (Centre Street at Hyde
  Street/Woodcliff Road) — leave `signal_type` and `pedestrian_activated`
  empty and note it.
- Trailing spaces after every line in the PDF text; whitespace-collapse as
  usual.

## Proposed common vocabulary

`offset_direction` needs the eight bare compass points; `common#side` lacks
the intercardinals, so the enum is defined inline in this schema for now.
Proposal for `_common.json` (do not add until coordinated — other specs may
want it too, e.g. any section with "N feet DIRECTION of X" grammar):

```json
"compass_point": {
  "description": "Bare compass bearing (offset/leg direction, not direction of travel)",
  "enum": ["north", "south", "east", "west",
           "northeast", "northwest", "southeast", "southwest"]
}
```

## Counting rules (manifest)

```json
{"region_start": "following locations:", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```

Verified against revision 2025-04-11: 63 paragraphs in the region, all 63
match `entry_start` (no continuation fragments, no embedded headers).
