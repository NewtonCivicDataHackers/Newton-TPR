# Section 199 — Fire Lanes

## Source shape

One intro sentence ("The following locations are hereby designated as Fire
Lanes.") followed by a numbered list `(1)`–`(12)`, then a stray `§` paragraph
and the ordinance-history footer beginning `(TPR-482,`. 12 entries as of
revision 2025-04-11. Every entry keeps its `(N)` list marker verbatim in
`source_text`.

## Entry grammars observed

Two families:

1. **Public-way segment** — the named street itself is the fire lane;
   `lane_type = street`.
   - `STREET, both sides, from FROM_POINT BEARING for approximately N’.`
     — "Elm Road, both sides, from Walnut Street westerly for approximately
     74’." → side = both, from_point = Walnut Street,
     extent_direction = westerly, length_feet = 74.
   - `STREET, both sides, from FROM_POINT to TO_POINT.`
     — "Melrose Avenue, both sides, from Lexington Street to Melrose Street."
   - `STREET, SIDE side.` — "Cabot School Bridges-to-Parkview Connector
     Roadway, south side." (no endpoints at all).

2. **Property entry** — heading names an address and/or property, then a
   body sentence describes the designated driveway/roadway/aisle;
   `lane_type` = the facility noun.
   - `NUMBER STREET. The FACILITY … from FROM_POINT BEARING [for]
     approximately N’.` — "(5) 390-398 Cherry Street. The driveway of
     390-398 Cherry Street from the sidewalk easterly approximately 50’."
   - `NUMBER STREET (PROPERTY). The FACILITY at ADDRESS POSITIONAL.`
     — "(6) 276 Church Street (YMCA). The driveway at 276 Church Street
     between the marked parking areas and immediately in front of the YMCA
     building."
   - `PROPERTY (ALIAS on STREET). The FACILITY POSITIONAL from FROM_POINT …`
     — the Heartland Plaza entry; no street number at all, street comes from
     the parenthetical.
   - `FACILITY of PROPERTY at NUMBER STREET.` — "(4) Center Drive aisle of
     the Crystal Lake Bathhouse Parking Lot at 30 Rogers Street."

## Normalization rules

- Feet are marked with a curly apostrophe: `approximately 60’` →
  `length_feet = 60`. Every length in this section is "approximately"; the
  qualifier is implied by the column and not recorded anywhere else.
- `in a westerly direction` → `extent_direction = westerly` (same as bare
  "westerly").
- `street_number` is the heading's number range, digits and hyphen only:
  "31-49", "390-398", "740". When the body enumerates individual numbers
  ("31,37,43,47, and 49"), the heading range is canonical; the enumeration
  survives in `source_text` only.
- Strip the leading article (and only the article) from
  `from_point`/`to_point`: "from the edge of the sidewalk" → "edge of the
  sidewalk"; "from the sidewalk" → "sidewalk"; "from the Watertown line" →
  "Watertown line".
- `source_text` keeps the `(N)` list marker and all source punctuation
  verbatim (whitespace-collapsed), including "(1)740" with its missing space
  and "31,37,43,47, and 49" with its missing spaces.

## Field placement rules

- **`street` is always a bare street name** — the house number goes to
  `street_number`, never into `street`. A property entry geocodes from
  `street_number` + `street`; a public-way entry from `street` + endpoints.
- **`lane_type = street`** for public-way entries (grammar family 1), even
  when the way's own name contains "Roadway" (the Cabot School connector).
  Otherwise `lane_type` is the facility noun from the body sentence:
  `driveway`, `roadway`, or `drive aisle`.
- **`side` is the side of the designated way**, whichever way that is:
  "both sides" of Elm Road, but also "The east side of the driveway" →
  side = east.
- **`from_point`/`to_point` may be non-street anchors** for property entries
  (sidewalk, rear of the building, Watertown city line). Record them as
  stated; they are extents within a parcel, not geocoding targets.
- **Positional phrases go to `location_detail` whole**, keeping their object
  even when it repeats a captured field: "in front of the Marshall's Mall"
  (property_name already = Marshall's Mall), "against the building in the
  rear of 31,37,43,47, and 49 Boylston Street". Faithfulness beats
  deduplication.
- **`property_name` is verbatim** including parentheticals:
  "Heartland Plaza (Stop & Shop on Watertown Street)" stays whole even
  though its inner street reference also supplies `street`.
- `notes` is reserved for anomalies and interpretation flags; it never
  carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | street_number | property_name | lane_type | side | from_point | to_point | extent_direction | length_feet | location_detail | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (1)740 Beacon Street… | Beacon Street | 740 | | driveway | east | edge of the sidewalk | | southerly | 60 | | |
| (2) 31-49 Boylston Street… | Boylston Street | 31-49 | | roadway | | | | | | against the building in the rear of 31,37,43,47, and 49 Boylston Street | heading range 31-49 is canonical; body enumerates individual numbers |
| (3) Cabot School Bridges-to-Parkview Connector Roadway… | Cabot School Bridges-to-Parkview Connector Roadway | | | street | south | | | | | | |
| (4) Center Drive aisle… | Rogers Street | 30 | Crystal Lake Bathhouse Parking Lot | drive aisle | | | | | | center | 'Center Drive aisle' capitalization ambiguous; read as the central drive aisle of the lot, not a way named Center Drive |
| (8) 2 Hammond Pond Parkway… | Hammond Pond Parkway | 2 | | driveway | | sidewalk | rear of the building | | 200 | to the left of two accessible parking spaces | |
| (9) Heartland Plaza… | Watertown Street | | Heartland Plaza (Stop & Shop on Watertown Street) | roadway | | Watertown line | | westerly | 200 | in front of the Heartland Plaza | from_point is the Watertown city line, not a street |
| (12) 275 Needham Street… | Needham Street | 275 | Marshall's Mall | roadway | | Needham Street | | northerly | 500 | in front of the Marshall's Mall | |

Notes on the settled readings:

- **(8)** "commencing from the sidewalk to the rear of the building
  approximately 200’" parses as from_point = sidewalk, to_point = rear of
  the building, length 200 — a both-endpoints-plus-length extent with no
  bearing stated.
- **(12)** from_point legitimately duplicates `street`: the roadway runs
  from Needham Street northerly.

## Source-text quirks

- **PDF line-wrap splits six entries** — (1), (5), (6), (8), (9), (12) —
  across blank lines; the fragments must be rejoined into the previous
  entry's `source_text`. Unlike other sections, two fragments do **not**
  start lowercase: "50’." starts with a digit and "Watertown line in a
  westerly direction…" starts uppercase. This is why `entry_start` is
  `^\(\d+\)` here, not the usual `^[A-Z]`.
- Entry (1) has no space after its list marker: "(1)740 Beacon Street." —
  reproduce verbatim in `source_text`.
- "31,37,43,47, and 49" has missing spaces after commas — reproduce
  verbatim.
- A stray `§` paragraph sits between the last entry and the ordinance
  footer; it matches neither `entry_start` nor any entry — ignore it.
- Feet use the curly apostrophe U+2019 (’), not a straight quote.

## Counting rules (manifest)

```json
{"region_start": "hereby designated as Fire Lanes", "region_end": "\\(TPR-\\d+,", "entry_start": "^\\(\\d+\\)"}
```

12 entries as of revision 2025-04-11. Verified: every `(N)` paragraph counts,
all six wrap fragments and the `§` paragraph are skipped, and the footer
`(TPR-482, 04-11-19; …)` ends the region.

## Proposed common vocabulary

`bearing` — compass direction of extent in the "-erly" form the TPR uses for
segment measurements ("from Walnut Street westerly for approximately 74’"),
distinct from `direction` (travel direction, "-bound") and `side`:

```json
"bearing": {
  "description": "Compass bearing a segment or measurement extends, in '-erly' form",
  "enum": ["northerly", "southerly", "easterly", "westerly",
           "northeasterly", "northwesterly", "southeasterly", "southwesterly"]
}
```

Defined inline on this schema's `extent_direction` until promoted to
`_common.json` (only the four cardinal values occur in this section, but the
TPR uses intercardinal "-erly" forms elsewhere, so the def proposes all
eight). Other segment-based sections (parking restrictions) will need the
same vocabulary.
