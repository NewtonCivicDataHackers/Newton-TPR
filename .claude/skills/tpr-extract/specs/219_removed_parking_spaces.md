# Section 219 — Parking prohibitions in areas that previously allowed parking

## Source shape

The shortest covered section. A title line, then a single intro paragraph —
"The following parking spaces were removed in compliance with Sec. 19-166
(p):" — then the entries, one per blank-line-separated paragraph. There is
**no ordinance-history footer** as of revision 2026-01-16; the section simply
ends after the last entry. 2 entries as of revision 2026-01-16.

This is an accumulating list: the city appends an entry each time a parking
space is removed under Sec. 19-166(p) (spaces removed near crosswalks /
daylighting). Expect the entry count to grow across revisions, and expect new
grammar variants — see "Schema headroom" below.

## Entry grammars observed

One grammar so far, both entries:

1. `STREET, SIDE side, within N feet of a marked crosswalk near ADDRESS,
   previously marked as meter #NNNN.`
   - "Lincoln Street, south side, within 25 feet of a marked crosswalk near
     26 Lincoln Street, previously marked as meter #5029."
   → street = Lincoln Street, side = south, within_feet = 25,
     reference_point = marked crosswalk, near_address = 26 Lincoln Street,
     meter_number = 5029

## Normalization rules

- `SIDE side` → bare side token: "south side" → `south`, "north side" →
  `north`.
- `within N feet of X` → `within_feet` = N (integer, no units in the cell —
  units live in the column name), `reference_point` = X with the leading
  article dropped and lowercased: "a marked crosswalk" → `marked crosswalk`.
  Keep the adjective ("marked") — it distinguishes marked from unmarked
  crosswalks.
- `near ADDRESS` → `near_address` = the address exactly as written, including
  unit-letter suffixes: "39A Lincoln Street" stays `39A Lincoln Street`.
  This is the geocodable anchor: `near_address` alone (plus ", Newton MA")
  resolves to a house-number-level point; `street` + `side` then place the
  space.
- `previously marked as meter #NNNN` → `meter_number` = the digits only:
  "meter #5029" → `5029`. Strip the "#"; do not zero-pad or reformat.

## Field placement rules

- **The address goes in `near_address`, never in `street`.** `street` is the
  street the regulation applies to ("Lincoln Street"), even though the
  address in these entries happens to be on the same street.
- **`reference_point` holds only the measured-from feature** (crosswalk,
  hydrant, etc.); the address qualifying it goes in `near_address`. Splitting
  "a marked crosswalk near 26 Lincoln Street" across the two columns is the
  settled interpretation.
- Any positional phrase that does not fit the structured columns goes in
  `location_detail` — never in `notes`. `notes` is reserved for source-text
  anomalies and ambiguity flags; it never carries data.
- If a future entry omits the meter clause, leave `meter_number` empty — do
  not infer one.

## Gold rows (currently the entire dataset)

| street | side | within_feet | reference_point | near_address | meter_number |
|---|---|---|---|---|---|
| Lincoln Street | south | 25 | marked crosswalk | 26 Lincoln Street | 5029 |
| Lincoln Street | north | 25 | marked crosswalk | 39A Lincoln Street | 5011 |

`location_detail` and `notes` are empty for both rows.

## Schema headroom

Removal entries elsewhere in the TPR sometimes describe segments
("from X to Y") rather than crosswalk-radius points. If a future revision
adds such a grammar here, extend the schema with `from_point`/`to_point`
(and `cross_street` if intersections appear) rather than stuffing endpoints
into `location_detail` — update this spec when that happens.

## Source-text quirks

- Both entries line-wrap mid-clause in the PDF text just before
  "meter #NNNN."; the wrapped fragment is on the **next physical line of the
  same paragraph** (no intervening blank line), so paragraph splitting joins
  it automatically. Collapse the wrap to a single space in `source_text`.
- No ordinance-history footer. The `region_end` pattern below intentionally
  matches nothing today; the validator treats a non-matching `region_end` as
  end-of-text, and the pattern is in place for the day the city appends a
  `(Rev. Ords.` footer.
- The intro cites "Sec. 19-166 (p)" — that citation is section-wide
  boilerplate, not per-entry data; it gets no column.

## Counting rules (manifest)

```json
{"region_start": "parking spaces were removed in compliance with Sec\\. 19-166 \\(p\\):", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```

Verified against revision 2026-01-16: counts 2. The intro paragraph is
consumed by `region_start` (it matches through the trailing colon), and any
lowercase line-wrap fragments are absorbed into their entry's paragraph
before counting.
