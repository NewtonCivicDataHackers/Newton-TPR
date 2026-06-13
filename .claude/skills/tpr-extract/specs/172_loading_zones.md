# Section 172 — Loading zones

## Source shape

TWO entry lists in one dataset, distinguished by the `time_limit_minutes`
column:

- (a) "The following locations are designated as loading zones which have a
  thirty minute time limit:" → entries with `time_limit_minutes = 30`
  (18 entries as of revision 2026-01-16)
- (b) "The following locations are designated as loading zones which shall
  have a ten minute time limit:" → entries with `time_limit_minutes = 10`
  (1 entry: Lake Avenue)

Entries end at the ordinance-history footer beginning `(Ord. No. Z-19`.
The `(b)` header paragraph starts with `(` so the counting rules skip it
automatically. The section is followed by "Sec. TPR-173—TPR-175 Reserved.",
which lies past `region_end` and is never extracted.

## Entry grammars observed

Every entry is a street segment anchored on a named cross street. Variants,
roughly in frequency order:

1. `STREET, SIDE side, from a point N feet DIR of CROSS, EXTENTerly M feet.`
   → street, side, from_point = CROSS, from_offset_feet = N,
   from_offset_direction = DIR, extent_direction = EXTENT, length_feet = M
   - "Border Street, north side from a point 211 feet west of Elm Street,
     westerly 20 feet." (comma after "side" and before the extent clause is
     inconsistently present — same parse either way)
2. No side stated: `STREET, from a point N feet DIR of CROSS, EXTENTerly M
   feet.` → side empty
   - "Columbus Street, from a point 150 feet north of Lincoln Street,
     northerly 80 feet."
3. Anchor without offset: `STREET, SIDE side[,] from CROSS, EXTENTerly M
   feet.` → from_offset_feet and from_offset_direction empty
   - "Sumner Street, west side, from Langley Road, northerly 50 feet."
4. Endpoint-to-endpoint: `STREET, SIDE side, from X to Y.` → from_point = X,
   to_point = Y; offsets, extent_direction, and length_feet all empty
   - "Elm Road, south side, from Lowell Avenue to Blithdale Street."
5. Reordered qualifiers: side or length may trail the extent clause
   - "Highland Avenue, from a point 40 feet west of Walnut Street, 40 feet
     westerly, north side." (length precedes direction; side trails)
   - "Jackson Road, from Pearl Street northeasterly 130 feet on southeasterly
     side." (side trails in '-erly' form)

## Normalization rules

- `-erly` adverbs normalize to compass points: southerly → south,
  westerly → west, northeasterly → northeast, southeasterly → southeast.
  Applies to `extent_direction` and to trailing side phrases
  ("on southeasterly side" → side = southeast).
- Spelled-out numbers with parenthesized digits reduce to the digits:
  "one hundred forty (140) feet" → 140, "three hundred forty (340) feet"
  → 340. The verbatim wording stays in `source_text` only.
- Distances are always feet in this section; they land in `from_offset_feet`
  / `length_feet` as bare integers.
- `time_limit_minutes` comes from which header list the entry falls under,
  never from the entry text: 30 for list (a), 10 for list (b).

## Field placement rules

- `from_point` holds only the named anchor street ("from a point 140 feet
  south of Beacon Street" → from_point = Beacon Street); the offset goes in
  `from_offset_feet` + `from_offset_direction`, never in the name.
- `to_point` is used only for grammar 4 (`from X to Y`); a
  direction-and-length extent never fills `to_point`.
- Positional qualifiers beyond the segment atoms go in `location_detail`
  ("at the existing crosswalk" on the Herrick Road entry) — never in
  `notes`. `notes` is reserved for source-text anomalies; it never carries
  data.
- Side phrases attached to something other than the street itself still fill
  `side`, with the attachment in `location_detail` (see Walnut Park gold
  row).

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | side | from_point | from_offset_feet | from_offset_direction | extent_direction | length_feet | location_detail |
|---|---|---|---|---|---|---|---|---|
| Beethoven Avenue, east side, from a point one hundred forty (140) feet… | Beethoven Avenue | east | Beacon Street | 140 | south | south | 340 | |
| Highland Avenue, … 40 feet westerly, north side. | Highland Avenue | north | Walnut Street | 40 | west | west | 40 | |
| Jackson Road, from Pearl Street northeasterly 130 feet on southeasterly side. | Jackson Road | southeast | Pearl Street | | | northeast | 130 | |
| Herrick Road, … northerly 15 feet at the existing crosswalk. | Herrick Road | | Braeland Road | 210 | north | north | 15 | at the existing crosswalk |
| Walnut Park, west side of west drive of the Walnut Hill School from a point 600 feet north of Washington Street, northerly 80 feet. | Walnut Park | west | Washington Street | 600 | north | north | 80 | west drive of the Walnut Hill School |

Walnut Park: the "west side" grammatically qualifies the school's west
drive, not Walnut Park itself; record side = west and keep the drive
designation in `location_detail` so the row still geocodes from street +
from_point + offset.

## Source-text quirks

- A stray `§` paragraph (PDF artifact) sits between the Sumner Street and
  Union Street entries. It is skipped by `entry_start: ^[A-Z]` and must
  never be extracted.
- The Beethoven Avenue and Walnut Park entries wrap across two source lines
  within one paragraph; collapse to a single line in `source_text`.
- The comma after "SIDE side" and before the extent clause is inconsistently
  present (compare Border Street vs. Charlesbank Road); this is punctuation
  noise, not a grammar difference.
- The (b) list has exactly one entry as of revision 2026-01-16; do not
  assume it stays that way.

## Proposed common vocabulary

- **Extend `common#side`** with the intercardinal values `northeast`,
  `northwest`, `southeast`, `southwest` — this section has streets running
  diagonally ("Gardner Street, northwest side", "Pearl Street, northeast
  side", "on southeasterly side"). Defined inline in this schema (as a local
  `enum` override on the `common#side` $ref) pending addition to
  `_common.json`.
- **New def `common#compass_point`**: enum `north, south, east, west,
  northeast, northwest, southeast, southwest` — a static compass bearing,
  distinct from `common#direction`'s travel-flow "-bound" values. Used here
  for `from_offset_direction` ("140 feet south of Beacon Street") and
  `extent_direction` ("southerly 340 feet"); any section measuring offsets
  from intersections will need it. Defined inline in this schema pending
  addition to `_common.json`.

## Counting rules (manifest)

```json
{"region_start": "designated as loading zones which have a thirty minute time limit:", "region_end": "\\(Ord\\. No\\. Z-19", "entry_start": "^[A-Z]"}
```

Counts both the (a) and (b) lists (19 as of revision 2026-01-16); the `(b)`
header paragraph and the stray `§` artifact are skipped by `entry_start`.
