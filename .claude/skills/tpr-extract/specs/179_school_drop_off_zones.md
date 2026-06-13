# Section 179 — School drop off zones

## Source shape

Boilerplate paragraph (a) (one-minute drop-off/pick-up rule), then (b)
"The following locations are designated as school drop off zones on days
that school is in session, during the following times:" followed by two
numbered TIME paragraphs — "(1) from thirty minutes prior…" and "(2) from
one hour prior… until one-half hour after the scheduled end of school." —
which are NOT location entries. Location entries follow, ending before
boilerplate paragraph (c) (commissioner erects signs) and the
`(Rev. Ords.` footer. 30 atomic entries as of revision 2025-04-11.

The schedule in (b)(1)–(2) is uniform across all entries and is relative
to each school's scheduled start/end times, not clock times — it cannot
be normalized to `common#time_range` and is NOT represented per-row.
Effectively: days = school days in session, times = 30 min before start
until start, and 1 hour before end until 30 min after end.

Unlike 148/96, the list is **hierarchical**. Three paragraph shapes:

1. Flat entries: `STREET, SIDE side, SEGMENT.` — one paragraph, one row.
2. Street headers (`Brookline Street:`, `Dedham Street:`, … and
   `Wheeler Road` — no colon) followed by numbered sub-entries
   `(1) East side, SEGMENT.` — one row per sub-entry.
3. Brookline Street only: street header, then side sub-headers
   (`North side:` / `South side:`), then lettered sub-entries
   `a) from a point 55’ west of Hartman, 87’ westerly.` — one row per
   lettered sub-entry (the letter sequence restarts under each side).

## Entry grammars observed (segment clause)

- A `from a point N feet DIR of REF, DIRerly M feet.` /
  `…, M feet DIRerly.` → from_point=REF, from_offset_feet=N,
  from_offset_direction=DIR, extent_direction=DIR2, length_feet=M.
  - "Beethoven Avenue, east side, from a point 275 feet south of Beacon
    Street, southerly 275 feet."
- B `from a point N feet DIR of REF to TARGET.` → from_* as above,
  to_point=TARGET, no length.
  - "(2) East side, from a point 575 feet north of Mandalay Road to
    Fellsmere Road." (under Dolphin Road)
- C `from a point N feet DIR of REF, DIRerly to the intersection of
  STREET and X.` → to_point=X (the intersection is with the subject
  street; record only the other street).
  - Dedham Street (2): to_point = "Walnut Street".
- D `from REF M feet DIRerly.` (zone begins at REF, no offset) →
  from_point=REF, from_offset_* empty, extent_direction, length_feet.
  - "Jackson Road, east side, from Pearl Street 190 feet northerly."
- E `from REF to a point N feet DIR of REF2.` → from_point=REF,
  to_point=REF2, to_offset_feet=N, to_offset_direction=DIR.
  - "Walnut Street, west side, from Florence Court to a point 110 feet
    south of Minot Place."
- F `from a point N feet DIR of REF to REF.` (start measured from the
  same street the zone runs to) → both from_point and to_point = REF.
  - "Hancock Street, east side, from a point 75 feet south of Lasell
    Street to Lasell Street."
- G Landmark endpoints: "Wells Avenue, odd side, from the driveway of
  125 Wells Avenue, northerly 260 feet to a point 20 feet south of the
  driveway of 135 Wells Avenue." — both a length and an end point.
- H Whole-side designation, no segment at all:
  "Cabot School Bridges-to-Parkview Connector Roadway, south side." —
  all segment columns empty.

## Normalization rules

- `-erly` adverbs → compass points: southerly→south, northerly→north,
  westerly→west, easterly→east (columns from_offset_direction,
  extent_direction, to_offset_direction).
- `SIDE side` → `common#side` token: "east side"→east, "odd side"→odd.
- Prime/typographic feet marks → integers: "55’" → 55 (Brookline
  sub-entries). `source_text` keeps the ’ characters verbatim.
- Street-name capitalization normalizes to title case in structured
  columns ("Woodcliff road" → "Woodcliff Road"); no note needed;
  `source_text` stays verbatim.
- Landmark endpoints keep the full noun phrase minus the leading
  preposition: "from the driveway of 125 Wells Avenue" → from_point =
  "the driveway of 125 Wells Avenue".
- `to the intersection of STREET and X` (STREET = the subject street)
  → to_point = X.

## Field placement rules

- For grouped entries (shapes 2 and 3), `street` comes from the parent
  header with any trailing colon dropped ("Brookline Street:" →
  "Brookline Street"); the sub-entry's "(1)"/"a)" marker is never part
  of any structured field.
- `source_text` for grouped sub-entries = parent street header +
  (side sub-header, Brookline only) + the sub-entry paragraph, joined
  with single spaces in document order, e.g.
  "Brookline Street: North side: a) from a point 55’ west of Hartman,
  87’ westerly." This keeps every row self-contained and guarantees
  uniqueness even when sub-entry texts repeat across streets.
- Offsets attach to the point they measure from: `N feet DIR of REF`
  before the extent clause → from_*, after `to a point` → to_*.
- `location_detail` holds only segment qualifiers that genuinely cannot
  be decomposed (see Nevada Street gold row); it never duplicates what
  the structured columns already capture.
- `notes` is reserved for source-text anomalies and ambiguity flags;
  it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | side | from_point | from_off_ft | from_dir | ext_dir | len_ft | to_point | to_off_ft | to_dir | location_detail | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cabot School … Connector Roadway, south side. | Cabot School Bridges-to-Parkview Connector Roadway | south | | | | | | | | | | |
| Brookline St North a) … 55’ west of Hartman, 87’ westerly | Brookline Street | north | Hartman | 55 | west | west | 87 | | | | | source omits street-type suffix for Hartman |
| Nevada St … to a point 190 feet southerly | Nevada Street | west | California Street | 140 | south | | | | | | to a point 190 feet southerly | extent ambiguous: 190 feet of zone or a point 190 feet from California Street; not decomposed |
| Ward St … 50 feet east of West Boulevard Street, westerly 100 feet | Ward Street | north | West Boulevard Street | 50 | east | west | 100 | | | | | source omits 'from a point' before offset |
| Wells Ave, odd side … | Wells Avenue | odd | the driveway of 125 Wells Avenue | | | north | 260 | the driveway of 135 Wells Avenue | 20 | south | | |
| Walnut St … Florence Court to a point 110 feet south of Minot Place | Walnut Street | west | Florence Court | | | | | Minot Place | 110 | south | | |
| Hancock St … 75 feet south of Lasell Street to Lasell Street | Hancock Street | east | Lasell Street | 75 | south | | | Lasell Street | | | | |
| Dedham St (2) … to the intersection of Dedham Street and Walnut Street | Dedham Street | west | Woodcliff Road | 140 | north | north | | Walnut Street | | | | entry wrapped across blank line in source; rejoined |
| Jackson Rd … from Pearl Street 190 feet northerly | Jackson Road | east | Pearl Street | | | north | 190 | | | | | |

## Source-text quirks

- Two entries wrap across blank lines; the fragments start lowercase
  ("and Walnut Street.", "the driveway of 135 Wells Avenue.") and must
  be rejoined into the previous entry's `source_text`. The counting
  rules skip them automatically.
- Brookline Street sub-entries use typographic primes for feet (55’,
  87’, 157’, 140’) and a bare "Hartman" with no street-type suffix.
- "Woodcliff road" (Dedham (1)) has a lowercase 'road' — normalize in
  from_point, verbatim in source_text.
- The "Wheeler Road" header has no trailing colon, unlike every other
  street header.
- The two lettered lists under Brookline Street both start at "a)", so
  the same marker appears under different side sub-headers — the
  source_text prefixing rule keeps the rows unique.
- Stein Circle's entry measures the start "north of Saw Mill Brook
  Parkway" but runs "westerly" — consistent with a curving street, not
  an error; record as written, no note.

## Counting rules (manifest)

```json
{
  "region_start": "until one-half hour after the scheduled end of school\\.",
  "region_end": "\\(c\\) The commissioner",
  "entry_start": "^(\\(\\d+\\) |[a-z]\\) |[A-Z].*\\bside\\b[^:]*$)"
}
```

The region starts after the (b)(2) time clause so the numbered TIME
paragraphs are excluded, and ends before boilerplate (c). `entry_start`
counts: numbered sub-entries `(1) `, lettered sub-entries `a) `, and
capitalized paragraphs containing the word "side" not followed by a
trailing colon (which excludes the `North side:`/`South side:`
sub-headers). Street headers ("Brookline Street:", "Wheeler Road") lack
"side" and are skipped; lowercase wrap fragments fail all three
alternatives. Verified count: 30 (revision 2025-04-11).

## Proposed common vocabulary

`compass_point` — plain compass directions for offset/extent
measurements ("a point 275 feet **south** of Beacon Street",
"**southerly** 275 feet"), distinct from `common#direction`
(travel directions, "-bound") and `common#side` (which mixes in
both/odd/even):

```json
"compass_point": {
  "description": "Plain compass direction for offsets and extents (point X feet south of Y; southerly N feet)",
  "enum": ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
}
```

Inlined in `179_school_drop_off_zones.json` (three columns:
`from_offset_direction`, `extent_direction`, `to_offset_direction`)
because `_common.json` could not be edited during parallel schema
authoring. When promoted, replace the three inline enums with
`{"$ref": "common#compass_point"}`.
