# Section 95 — Thruways

## Source shape

One boilerplate sentence ("The following streets or ways or parts thereof are
hereby designated "thruways" under and by virtue of section 9 of chapter 89 of
the General Laws:") — itself split across a blank line by PDF wrap, ending in
the fragment paragraph `chapter 89 of the General Laws:`. Entries follow, one
per blank-line-separated paragraph, until the ordinance-history footer
beginning `(Rev. Ords.`. 4 entries as of revision 2026-01-16 (Boylston Street,
Centre Street, Commonwealth Avenue, Washington Street). One row per entry —
even the Commonwealth Avenue entry with an interior gap stays a single row
(see below).

## Entry grammars observed

1. `STREET, from POINT to POINT.` — the base segment grammar; endpoints are
   either cross streets or municipal boundary lines.
   - "Centre Street, from Winchester Street to Newton-Watertown line."
   - "Washington Street, from Newton-Wellesley line to Newton-Boston line."
2. `STREET, from POINT to POINT. TRAILING-SENTENCE.` — a second sentence
   qualifies the designation; it is data, not an anomaly.
   - "Boylston Street, from the Newton-Boston line to the Newton-Wellesley
     line. This street being a state highway is covered by state highway
     regulations." → `remark` = "This street being a state highway is covered
     by state highway regulations."
3. `STREET, from POINT to the junction of CROSS not including the
   intersection, then, beginning again at the DIRECTION limits of such
   intersection to POINT.` — a segment with an interior gap at one
   intersection. Model as ONE row: `from_point` and `to_point` are the overall
   extremes, `excluded_intersection` = CROSS. The resumption phrasing
   ("westerly limits of such intersection") stays in `source_text` only — the
   excluded portion is, by definition, the intersection itself.
   - "Commonwealth Avenue, from the Newton-Boston line to the junction of
     Washington Street not including the intersection, then, beginning again
     at the westerly limits of such intersection to the Newton-Weston line."

## Normalization rules

- **Article-strip endpoints**: "the Newton-Boston line" → `Newton-Boston
  line`. The source is inconsistent (Boylston/Commonwealth use "the",
  Centre/Washington don't); the columns are uniform without the article.
- **Municipal boundaries** keep the source's hyphenated form `Newton-<Town>
  line` (Newton-Boston line, Newton-Wellesley line, Newton-Watertown line,
  Newton-Weston line). They are geocodable as the point where `street`
  crosses the city limit toward `<Town>`.
- **Endpoints stay in source order** — do not reorder to west-to-east or
  alphabetically. Washington Street runs "from Newton-Wellesley line to
  Newton-Boston line" and the row says exactly that.
- `source_text` is the full rejoined entry, including any trailing sentence
  and any line-wrap continuation fragment, whitespace-collapsed.

## Field placement rules

- **`from_point`/`to_point` hold only the endpoint name** (cross street or
  boundary line) — no "the junction of", no "the westerly limits of".
- **`excluded_intersection` holds only the named cross street** of a carved-
  out intersection; everything else about the gap lives in `source_text`.
- **`remark` carries source content**: trailing sentences that qualify the
  designation (the state-highway jurisdiction sentence), verbatim and
  whitespace-collapsed. It is NOT a place for extractor commentary.
- **`notes` is reserved for source-text anomalies** and ambiguity flags; it
  never carries data. (No entry currently needs one.)

## Gold rows (the complete extraction)

The section is small enough to gold-plate entirely; reproduce these exact
field values unless the source text itself changes (then update them here):

| street | from_point | to_point | excluded_intersection | remark | notes |
|---|---|---|---|---|---|
| Boylston Street | Newton-Boston line | Newton-Wellesley line | | This street being a state highway is covered by state highway regulations. | |
| Centre Street | Winchester Street | Newton-Watertown line | | | |
| Commonwealth Avenue | Newton-Boston line | Newton-Weston line | Washington Street | | |
| Washington Street | Newton-Wellesley line | Newton-Boston line | | | |

## Source-text quirks

- PDF line-wrap splits two entries across blank lines; the fragments start
  lowercase ("covered by state highway regulations.", "intersection, then,
  beginning again at the westerly limits of such intersection to the
  Newton-Weston line.") and must be rejoined into the previous entry's
  `source_text`. The counting rule's `entry_start: ^[A-Z]` already excludes
  them from the count.
- The boilerplate is also wrap-split; its second fragment `chapter 89 of the
  General Laws:` carries the `region_start` match, so entries begin cleanly
  after it.
- Entry lines are indented with a single leading space in `sections/95.txt`;
  the validator's paragraph splitter strips it, so `^[A-Z]` still matches.

## Counting rules (manifest)

```json
{"region_start": "General Laws:", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```

Verified against revision 2026-01-16: 4 entries, with the two lowercase
continuation fragments correctly rejected.
