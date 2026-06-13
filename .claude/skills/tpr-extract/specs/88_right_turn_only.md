# Section 88 — Right turn only

## Source shape

One boilerplate sentence — "A right turn only shall be made by a person with
a vehicle at any of the following intersections:" — then a flat entry list,
one entry per blank-line-separated paragraph, until the ordinance-history
footer beginning `(Rev. Ords.`. 13 entries as of revision 2026-01-16.

Every entry names an approach way and an `onto` target; the regulated
movement (right turn only) is constant for the whole section, so there is no
`turn` column. An intersection row geocodes from `street` + `cross_street`.

## Entry grammars observed

Roughly in frequency order:

1. `STREET onto CROSS.` — no direction stated.
   - "Elm Street onto Washington Street." → street, cross_street,
     direction empty.
2. `STREET, DIRECTION, onto CROSS.` — direction set off by commas after the
   approach street.
   - "Newtonville Avenue, westbound, onto Walnut Street."
3. `STREET onto CROSS, DIRECTION.` — trailing direction.
   - "Commonwealth Avenue Carriage Way onto Lowell Avenue, westbound."
   - "Summer Street onto Willow Street, southbound."
4. `STREET, at LANDMARK, onto CROSS.` — positional qualifier between street
   and target.
   - "Commonwealth Avenue North Drive, at 629 Commonwealth Avenue, onto
     Commonwealth Avenue South Drive."
5. `AREA, from WAY onto CROSS.` — approach described by a `from` phrase.
   - "Newton Centre parking area, from municipal parking area onto Beacon
     Street."
6. Stray comma before `onto` with no direction: "Tiger Drive, onto Walnut
   Street." — treat as grammar 1; no note needed.

## Normalization rules

- Directions are already lowercase compass-bound tokens in this section; if a
  future revision capitalizes or hyphenates one ("Southbound",
  "south-bound"), normalize to the `common#direction` vocabulary, no note
  needed (same rule as section 96).
- **Trailing direction binds to the approach street** (grammar 3):
  "Summer Street onto Willow Street, southbound." → street = Summer Street,
  direction = southbound. This follows the settled convention from sections
  148 and 96 (`STREET at CROSS, DIRECTION.` → direction governs the approach
  traffic). The Carriage Way entry confirms it: Lowell Avenue runs
  north–south, so "westbound" can only describe travel on the Carriage Way.
  Do not add a note for these — the rule is settled here.

## Field placement rules

- `street` = the way the turning traffic approaches on, exactly as written
  (whitespace-collapsed, not beautified). Compound carriageway names stay
  whole: "Commonwealth Avenue Carriage Way", "Commonwealth Avenue North
  Drive".
- `cross_street` = the `onto` target, always present in this section, so the
  field is required. It holds only the named way; qualifiers stay out of it.
- **Positional qualifiers go in `location_detail`** ("at 629 Commonwealth
  Avenue") — never in `notes`. Street-number landmarks are positions, not
  streets.
- **`from X onto Y`** (grammar 5): X describes the approach →
  `location_detail`; Y is what's entered → `cross_street` (same rule as
  section 148). "Newton Centre parking area, from municipal parking area onto
  Beacon Street." → street = Newton Centre parking area, location_detail =
  from municipal parking area, cross_street = Beacon Street.
- `notes` is reserved for source-text anomalies and ambiguity flags; it never
  carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | cross_street | location_detail | notes |
|---|---|---|---|---|---|
| Comm Ave Carriage Way onto Lowell Avenue, westbound | Commonwealth Avenue Carriage Way | westbound | Lowell Avenue | | |
| Comm Ave North Drive, at 629 …, onto … South Drive | Commonwealth Avenue North Drive | | Commonwealth Avenue South Drive | at 629 Commonwealth Avenue | |
| Newton Centre parking area, from municipal parking area onto Beacon Street | Newton Centre parking area | | Beacon Street | from municipal parking area | street is a parking area, not a public way |
| Summer Street onto Willow Street, southbound | Summer Street | southbound | Willow Street | | |
| Tiger Drive, onto Walnut Street | Tiger Drive | | Walnut Street | | |

## Source-text quirks

- **Near-duplicate pairs are real**: "Elm Street onto Washington Street." and
  "Elm Street, southbound, onto Washington Street." are both in the source
  (likewise "Waltham Street onto Washington Street." / "Waltham Street,
  southbound, onto Washington Street."), almost certainly an amendment adding
  the directioned version without repealing the generic one. **Keep all four
  rows** — one row per source entry; their `source_text` values differ, so
  the uniqueness constraint is satisfied. Do not deduplicate or merge.
- Most entry lines carry a leading space (PDF artifact); the validator strips
  it, and `source_text` is whitespace-collapsed anyway.
- No lowercase line-wrap continuation fragments in this section as of
  revision 2026-01-16; if one appears in a future revision, rejoin it into
  the previous entry's `source_text` (it will not be counted by
  `entry_start`).
- "Tiger Drive, onto Walnut Street." has a stray comma before `onto`;
  reproduce verbatim in `source_text`, no note needed.

## Counting rules (manifest)

```json
{"region_start": "following intersections:", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```

Verified against revision 2026-01-16: 13 entries.
