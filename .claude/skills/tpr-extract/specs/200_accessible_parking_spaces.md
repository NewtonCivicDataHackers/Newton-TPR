# Section 200 — Accessible Parking Spaces

## Source shape

One header paragraph ("The following accessible parking spaces are hereby
designated … of Newton Revised Ordinances, 2017.") followed by an
alphabetical-by-street list of space designations, one per blank-line-separated
paragraph, until the ordinance-history footer beginning `(TPR-275,`.

**87 entries as of revision 2025-04-11** — but only 85 capital-initial
paragraphs, because the PDF text flow merged two pairs of entries into single
paragraphs (see Source-text quirks). Each merged paragraph yields TWO rows.

## Entry grammars observed

Roughly in frequency order:

1. Offset + extent: `STREET: SIDE side, [from a point] N feet DIR of CROSS,
   EXTENTDIRerly M feet.` (or `M feet EXTENTDIRerly`, or `M’ EXTENTDIRerly`)
   → street, side, cross_street, offset_feet, offset_direction, length_feet,
   extent_direction
   - "Aspen Avenue: north side, 130 feet west of Forest Avenue, westerly 28 feet."
   - "Chestnut Street, north side, from a point 290’ east of Oak Street, 20’ easterly."
2. Two-point segment: `… from a point N feet DIR of CROSS to a point M feet
   DIR of CROSS [(K spaces)].` → offset_feet = N, to_offset_feet = M
   (same cross_street and offset_direction for both points in every instance)
   - "Albemarle Road: eastern roadway, east side, from a point 185 feet north
     of Watertown Street to a point 390 feet north of Watertown Street (6 spaces)."
3. Point-only (no extent): "Armory Street: west side, 300 feet north of
   Washington Street." → length_feet and extent_direction empty.
4. Frontage: `STREET: in front of [#]N [STREET] [(LANDMARK)].` →
   address_number = N; the landmark gloss goes to location_detail.
   - "Beech Street: in front of 16 Beech Street." → address_number = 16
   - "Lincoln Road: in front of #68." → address_number = 68
5. Landmark-only: "Ash Street: north side, opposite Auburndale Brach library."
   → whole phrase in location_detail; cross_street empty.
6. Corner: "Union Street: Corner of Union Street and Herrick Road." →
   cross_street = Herrick Road, location_detail = "corner".
7. Trailing side: "Washington Street: from a point 290’ west of Armory Street,
   20’ westerly, north side." → side = north; field order in the source does
   not matter.

## Normalization rules

- `-erly` extent adverbs map to compass points: westerly → west, easterly →
  east, southerly → south, northerly → north. Likewise side phrases:
  "southeast side" → southeast, "northeast side" → northeast, "South Side" →
  south (capitalization is a source artifact, no note needed).
- The curly apostrophe `’` is the PDF's feet symbol: "290’" → offset_feet 290,
  "20’ easterly" → length_feet 20, extent_direction east.
- Space counts normalize to integers wherever stated: "(6 spaces)" → 6,
  "Two spaces" → 2, "Three (3) accessible parking spaces" → 3, "one accessible
  space" → 1. When no count is stated, `spaces` stays EMPTY — do not record an
  implied 1.
- `#N` house numbers drop the `#`: "in front of #212 Plymouth Road" →
  address_number = 212. Ranges and alternatives keep their source form minus
  `#`: "18-20", "38 or 42".
- `N feet from CROSS` with no bearing (Adams Street) → offset_direction EMPTY;
  the grammar simply omits it, no note needed.

## Field placement rules

- **`street` is the designation header** before the colon (or first comma when
  the entry uses comma punctuation), as written: keep parenthetical village
  qualifiers ("North Street (Newtonville)") and header carriageway
  designations ("Commonwealth Avenue, South Drive") in `street`.
- **Carriageway/roadway qualifiers in the body go to `location_detail`**:
  "eastern roadway" (Albemarle Road), "south Drive" (the colon-form
  Commonwealth Avenue entry). Only header-position carriageway names stay in
  `street`.
- **`cross_street` holds only named streets/ways, as written.** Landmark
  reference points ("the ramp", "the crosswalk", a church) go to
  `location_detail` and `cross_street` stays empty — except when the landmark
  phrase itself names a street as offset origin or corner partner.
- **Open-ended extents**: "northerly to end" → extent_direction = north,
  length_feet empty, location_detail = "to end".
- **`address_number` only for numbers on `street` itself.** "Nevada Street: in
  front of the ramp leading to #538 California Street." → address_number
  EMPTY; the whole phrase goes to location_detail (the number belongs to
  California Street).
- Multiple distinct qualifiers join with `; ` in source order
  ("east side of Walnut Street; immediately north of the crosswalk").
- `notes` is reserved for source-text anomalies (typos, stray characters,
  ambiguity flags); it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them unless
the source text itself changes (then update them here):

| source entry (abbrev.) | street | side | cross_street | offset/to/len | spaces | address_number | location_detail | notes |
|---|---|---|---|---|---|---|---|---|
| Adams Street: … 220 feet from Centre Street, westerly 20 feet | Adams Street | north | Centre Street | 220 / / 20 (offset_direction empty, extent west) | | | | |
| Albemarle Road: eastern roadway … 185 … to … 390 … (6 spaces) | Albemarle Road | east | Watertown Street | 185 / 390 / (dir north) | 6 | | eastern roadway | |
| Armory Street: … 230 feet north of Washington Street, northerly to end | Armory Street | west | Washington Street | 230 / / (dir north, extent north) | | | to end | |
| Ash Street: … opposite Auburndale Brach library | Ash Street | north | | | | | opposite Auburndale Brach library | 'Brach' sic in source (Branch) |
| Commonwealth Avenue: On either side of the front pathway… | Commonwealth Avenue | | | | | | on either side of the front pathway to Street Ignatius Church | 'Street Ignatius' sic in source (St. Ignatius) |
| Commonwealth Avenue: south side, south Drive, 231 feet east of Melrose… | Commonwealth Avenue | south | Melrose Street | 231 / / 22 (dir east, extent east) | | | south Drive | |
| Commonwealth Avenue, South Drive, South Side, … 125 feet east of Chestnut Terrace… | Commonwealth Avenue, South Drive | south | Chestnut Terrace | 125 / / 20 (dir east, extent east) | | | | |
| Curve Street: Two spaces in front of #21 Curve Street (Myrtle Baptist Church) | Curve Street | | | | 2 | 21 | Myrtle Baptist Church | |
| Hull Street: Three (3) accessible parking spaces, north side, Hull Street, just to the west of the ramp | Hull Street | north | | | 3 | | just to the west of the ramp | street name repeated mid-entry in source |
| Lincoln Street: opposite the hp ramp at the Newton Highlands Congregational Church… | Lincoln Street | | | | | | opposite the hp ramp at the Newton Highlands Congregational Church | 'hp' sic in source (handicap) |
| Madison Avenue: east side of Walnut Street, immediately north of the crosswalk | Madison Avenue | | Walnut Street | | | | east side of Walnut Street; immediately north of the crosswalk | 'east side' modifies Walnut Street, not Madison Avenue — side left empty |
| Nevada Street: in front of the ramp leading to #538 California Street | Nevada Street | | | | | | in front of the ramp leading to #538 California Street | |
| Temple Street: one accessible space, near the entrance to the Temple Shalom Parking Lot | Temple Street | | | | 1 | | near the entrance to the Temple Shalom Parking Lot | |
| Union Street: Corner of Union Street and Herrick Road | Union Street | | Herrick Road | | | | corner | street name repeated mid-entry in source |
| Watertown Street: in front of #468. . | Watertown Street | | | | | 468 | | stray period artifact in source; paragraph merged with the 851 Watertown Street entry |
| West Street: in front of #38 or #42 | West Street | | | | | 38 or 42 | | source offers alternative house numbers |
| Windsor Road: NW corner of Beacon/Windsor | Windsor Road | | Beacon | | | | NW corner | cross street written as 'Beacon/Windsor' shorthand |

## Source-text quirks

- **Merged entries (2 rows from 1 paragraph), twice:**
  1. The Homer Street paragraph runs two designations together with a
     line-wrap inside the second: "Homer Street: north side, 40 feet west of
     Centre Street, westerly 40 feet. Homer Street: north side, 40 feet west"
     + fragment "of City Hall Drive, westerly 20 feet." → split into two rows;
     rejoin the fragment into the second row's `source_text`.
  2. "Watertown Street: in front of #468." is followed by a stray "." line and
     then "Watertown Street: in front of 851 Watertown Street." with NO blank
     line between — one paragraph, two rows. Keep the stray period in the
     first row's `source_text` ("…#468. .") and note it.
- PDF line-wrap splits the four Albemarle Road entries across blank lines; the
  fragments start lowercase ("of Watertown Street (6 spaces).", "north of
  Watertown Street (3 spaces).") and must be rejoined into the entry's
  `source_text`.
- Header punctuation is inconsistent: most entries use `STREET:` but several
  use `STREET,` (Beacon, Chapel, Chestnut, the comma-form Commonwealth Avenue,
  two Curve Street, Elm, Langley, Mechanic, two Washington Street, one Wyman).
  No note needed.
- Typos to reproduce verbatim in `source_text` and flag in `notes`:
  "Auburndale Brach library" (Branch), "Street Ignatius Church"
  (St. Ignatius), "the hp ramp" (handicap).
- Mixed feet notation: spelled-out "feet" and curly-apostrophe "’" both occur,
  sometimes within one entry ("north side, 180’ west of Central Avenue,
  easterly 20 feet").

## Counting rules (manifest)

```json
{
  "region_start": "Newton Revised Ordinances, 2017\\.",
  "region_end": "\\(TPR-275,",
  "entry_start": "^[A-Z]|^of City Hall Drive|^of Watertown Street \\(6 spaces\\)"
}
```

Yields 87. The region has 85 capital-initial paragraphs but 87 atomic entries
because of the two merged paragraphs above. The two extra `entry_start`
branches are deliberate, artifact-specific stand-ins that make the heuristic
total equal the atomic entry count: `^of City Hall Drive` counts the wrap
fragment that IS the tail of the second Homer Street entry; `^of Watertown
Street \(6 spaces\)` counts one Albemarle continuation fragment as a stand-in
for the second entry inside the merged Watertown #468/#851 paragraph (which
has no fragment of its own to count). If a future revision changes the PDF
line flow, re-derive these branches — they are tied to this revision's exact
wrap points.

## Proposed common vocabulary

Not added to `_common.json` (parallel agents); defined inline in the dataset
schema for now:

1. **Extend `common#side`** with intercardinal values `northeast`,
   `northwest`, `southeast`, `southwest`. This section uses "southeast side"
   (two Washington Street entries) and "northeast side" (one Wyman Street
   entry).
2. **New def `compass_point`**: enum `north, south, east, west, northeast,
   northwest, southeast, southwest` — a compass bearing for offset and extent
   directions ("185 feet north of Watertown Street", "westerly 20 feet").
   Distinct from `common#direction`, whose `-bound` values denote travel
   direction, not bearing. Used here by `offset_direction` and
   `extent_direction`; any section with metes-and-bounds location grammar
   will need it.
