# Section 150 — Safety Zones

## Source shape

One preamble sentence ("The following are hereby established as safety
zones:"), then one entry per blank-line-separated paragraph — except one
paragraph that holds TWO entries (see quirks) — until the ordinance-history
footer beginning `(TPR-752`. After the footer come `Sec. TPR-151—TPR-167.
Reserved.` and an `ARTICLE III` heading; both are outside the counting
region. 17 entries as of revision 2025-04-11.

Every entry is a street segment (or a whole street) — there are no
directions, sides, days, or times in this section.

## Entry grammars observed

1. `STREET between A and B.` → segment with plain endpoints
   - "Albemarle Road between Watertown Street and Crafts Street."
2. `STREET[,] from A to B.` → identical semantics to `between A and B`
   - "Homer Street, from Commonwealth Avenue to Walnut Street."
3. Either endpoint may be an offset point:
   `a point N feet DIR of X` → point = X, offset_feet = N,
   offset_direction = DIR
   - "Allen Avenue from a point 775 feet south of Beacon Street to a point
     330 feet north of Woodward Street." (both endpoints offset)
   - "Chestnut Street, from a point 375 feet north of Pennsylvania Avenue to
     Oak Street." (only the from endpoint offset)
   - "Walnut Street between Austin Street and a point 250 feet south of Mill
     Street." (`between` with an offset endpoint — grammars 1 and 3 combine)
4. `STREET.` → the entire street is the safety zone
   - "East Side Parkway." / "Ellis Street."

## Normalization rules

- `between A and B` and `from A to B` are the same thing: `from_point` = A,
  `to_point` = B. Preserve source order — do not reorder endpoints.
- `a point N feet DIR of X` decomposes to point = X, offset_feet = N
  (bare integer, no commas or units), offset_direction = DIR lowercase.
- An offset direction never appears without its feet value and vice versa:
  fill `*_offset_feet` and `*_offset_direction` together or not at all.
- A bare street name entry → `extent` = `entire_street`, all six endpoint
  columns empty. Any entry with endpoints → `extent` = `segment`,
  `from_point` and `to_point` both non-empty (the validator cannot enforce
  this conditional; the extractor must).
- Comma before `from` varies ("Crafts Street, from …" vs "Allen Avenue
  from …"); it is noise — same grammar, no note needed.

## Field placement rules

- Offset endpoints are data, fully decomposed: never leave "a point 775 feet
  south of Beacon Street" as a phrase in any column. `from_point`/`to_point`
  hold only the named street or way.
- `location_detail` exists for future qualifiers that do not decompose into
  the endpoint columns; as of revision 2025-04-11 it is empty in every row.
- `notes` is reserved for source-text anomalies (e.g. the merged-paragraph
  artifact); it never carries data.
- A row should geocode from `street` + `from_point`/`to_point` alone, with
  the offsets refining the endpoints.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | extent | from_point | from_offset_feet | from_offset_direction | to_point | to_offset_feet | to_offset_direction | notes |
|---|---|---|---|---|---|---|---|---|---|
| Allen Avenue from a point 775 feet south… | Allen Avenue | segment | Beacon Street | 775 | south | Woodward Street | 330 | north | |
| Beethoven Avenue from a point 970 feet… | Beethoven Avenue | segment | Beacon Street | 970 | south | Woodward Street | 385 | north | shares a source paragraph with the Brandeis Road entry; see spec |
| Brandeis Road between Adeline Road and Lion Drive. | Brandeis Road | segment | Adeline Road | | | Lion Drive | | | shares a source paragraph with the Beethoven Avenue entry; see spec |
| Chestnut Street, from a point 375 feet north… | Chestnut Street | segment | Pennsylvania Avenue | 375 | north | Oak Street | | | |
| East Side Parkway. | East Side Parkway | entire_street | | | | | | | |
| Walnut Street between Austin Street and a point 250 feet south… | Walnut Street | segment | Austin Street | | | Mill Street | 250 | south | |

## Proposed common vocabulary

`from_offset_direction`/`to_offset_direction` need a plain compass point
(`north|south|east|west`). `common#side` contains those values but also
`both|odd|even`, which are nonsense as bearings, and its meaning ("side of
street a regulation applies to") is wrong here. Proposal for `_common.json`
(not added here — defined inline in the dataset schema instead, per the
parallel-edit rule):

```json
"compass_point": {
  "description": "Plain compass point, e.g. the bearing of an offset from a reference street",
  "enum": ["north", "south", "east", "west"]
}
```

The `a point N feet DIR of X` grammar recurs across many TPR sections
(school zones, parking, stopping), so this def — and the offset triple
(`*_point`, `*_offset_feet`, `*_offset_direction`) as a pattern — should be
promoted once it is safe to edit `_common.json`. Then swap this schema's two
inline enums for `{"$ref": "common#compass_point"}`.

## Source-text quirks

- **Merged paragraph (inverse of the usual line-wrap split):** the Beethoven
  Avenue and Brandeis Road entries share one paragraph — no blank line
  between them in `sections/150.txt`. They are unambiguously two distinct
  safety zones (the list is alphabetical). Emit TWO rows; each row's
  `source_text` is its own sentence only, and each carries a note ("shares a
  source paragraph with the … entry; see spec"). The counting rules
  compensate — see below.
- "Crafts Street, …" and "Waverley Avenue, …" lines begin with a stray
  leading space; whitespace-collapsing `source_text` removes it.
- The ordinance-history footer spans three wrapped lines beginning
  `(TPR-752,`; it is excluded by `region_end`.

## Counting rules (manifest)

```json
{"region_start": "Sec\\. TPR-150\\. Safety Zones\\.", "region_end": "\\(TPR-752", "entry_start": "^[A-Z]"}
```

Verified count: **17**, equal to the true number of safety zones.

**Why region_start is the section header, not the preamble colon:** the
validator counts at most one entry per blank-line paragraph, and the
Beethoven/Brandeis merged paragraph holds two entries — so the natural
region (after "established as safety zones:") counts 16 for 17 real zones,
and no `entry_start` regex can recover the difference. Starting the region
at the section header makes the preamble paragraph ("The following are
hereby established as safety zones:") count as one entry, deliberately
offsetting the one merged paragraph: 1 + 16 = 17 = the true entry count.

This offset is calibrated to exactly one merged paragraph. If a future
revision restores the blank line (count becomes 18 vs 17 rows — validation
fails loudly), switch `region_start` to `"established as safety zones:"`,
which then counts entries naturally, and delete this workaround from the
spec. If another merged paragraph ever appears, the count drops and
validation fails loudly again — recount by hand before touching the rules.
