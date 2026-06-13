# Section 98 — Right lane must turn right

## Source shape

One boilerplate sentence ("A right turn only shall be made by a person with a
vehicle in the right lane at the following intersections:"), then entries, one
per blank-line-separated paragraph, until the ordinance-history footer
beginning `(Ord. No. S-65`. A trailing `ARTICLE. II.` page-header line follows
the footer and is outside the region. 25 entries as of revision 2026-01-16.

Every entry is the same regulation (mandatory right turn from the right lane),
so there is no `turn` or `lane` column — the dataset title carries it. Every
entry names exactly one approach street, one direction, and one turn target.

## Entry grammars observed

Roughly in frequency order:

1. `STREET, DIRECTION onto CROSS.` → street, direction, cross_street
   - "Beacon Street, eastbound onto Hammond Pond Parkway."
2. `STREET, DIRECTION, onto CROSS.` — extra comma before `onto`; identical
   meaning. The comma is punctuation noise; ignore it for parsing.
   - "Chestnut Street, northbound, onto Washington Street."
3. `STREET, DIRECTION, at CROSS.` — `at` works like `onto` (one entry)
   - "Collins Road, northbound, at Beacon Street." → cross_street = Beacon
     Street
4. `STREET, DIRECTION onto CROSS DIRECTION2 at POSITION.` → DIRECTION2 is the
   receiving direction of travel on the cross street → `onto_direction`; the
   `at …` position phrase → `location_detail`
   - "Dedham Street, southbound onto Nahanton Street westbound at the
     southernmost intersection of Nahanton Street and Dedham Street."
5. Compound target: `onto X and Y.` — one sign at one location where both
   ways join the approach street
   - "Commonwealth Avenue, eastbound, onto Day Street and Fuller Street."
6. Continuation movement with parenthetical position
   - "Washington Street, north-eastbound, continuing onto Washington Street
     (opposite Elm Street)."

## Normalization rules

- Hyphenated directions normalize to the vocabulary: "north-eastbound" →
  northeastbound.
- Parenthetical positional qualifiers drop their parentheses in
  `location_detail`: "(opposite Elm Street)" → `opposite Elm Street`
  (matches section 96's handling).

## Field placement rules

- `onto X` / `at X` always yields `cross_street = X`.
- **Compound targets stay whole**: "onto Day Street and Fuller Street" →
  `cross_street = Day Street and Fuller Street`, verbatim with the
  conjunction. Do NOT split into two rows — the source counts it as one entry
  (one sign where both streets meet Commonwealth Avenue).
- **Named non-street ways are still cross streets**: "Woodland MBTA driveway"
  is a named way → `cross_street`, not `location_detail`.
- A direction word immediately after the cross street ("onto Nahanton Street
  westbound") is the receiving direction → `onto_direction`; it is never part
  of the `cross_street` value.
- Positional qualifiers ("at the southernmost intersection of Nahanton Street
  and Dedham Street", "opposite Elm Street") go in `location_detail` — never
  in `notes`.
- **Movement qualifiers are data** (same rule as section 96): "continuing
  onto X" → `cross_street = X` and the phrase "continuing onto X" goes in
  `location_detail`. Join multiple distinct qualifiers with `; ` in source
  order.
- `notes` is reserved for source-text anomalies and ambiguity flags; it never
  carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | cross_street | onto_direction | location_detail | notes |
|---|---|---|---|---|---|---|
| Commonwealth Avenue … onto Day Street and Fuller Street | Commonwealth Avenue | eastbound | Day Street and Fuller Street | | | |
| Dedham Street, southbound onto Nahanton Street. | Dedham Street | southbound | Nahanton Street | | | |
| Dedham Street … southernmost intersection … | Dedham Street | southbound | Nahanton Street | westbound | at the southernmost intersection of Nahanton Street and Dedham Street | |
| Washington Street, north-eastbound, continuing onto Washington Street (opposite Elm Street). | Washington Street | northeastbound | Washington Street | | continuing onto Washington Street; opposite Elm Street | |
| Washington Street … onto Woodland MBTA driveway | Washington Street | eastbound | Woodland MBTA driveway | | | |

## Source-text quirks

- PDF line-wrap splits the disambiguated Dedham/Nahanton entry across a blank
  line; the fragment "and Dedham Street." starts lowercase and must be
  rejoined into the previous entry's `source_text` (the validator's
  `entry_start: ^[A-Z]` rule already skips it for counting).
- **Near-duplicate pair**: the source lists both a generic "Dedham Street,
  southbound onto Nahanton Street." and a disambiguated entry pinning the
  southernmost of the two Dedham/Nahanton intersections. Both are kept as
  separate rows, one per source entry, with empty `notes` — the overlap is
  documented here, not in the data.
- The disambiguated Dedham/Nahanton entry's first paragraph has no trailing
  period before the line wrap; the period arrives with the rejoined fragment.

## Counting rules (manifest)

```json
{"region_start": "at the following intersections:", "region_end": "\\(Ord\\. No\\. S-65", "entry_start": "^[A-Z]"}
```

Verified against revision 2026-01-16: 26 paragraphs in the region, 1 lowercase
continuation skipped → 25 entries.
