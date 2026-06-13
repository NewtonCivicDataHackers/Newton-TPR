# Section 84 — Speed zones designated

The largest and most format-heterogeneous section. Three coexisting source
forms, each extracted and verified by a different method, merged into one
dataset (`entry_type` distinguishes them). 275 rows as of revision 2026-01-16
(170 stanza sub-segments + 100 table rows + 5 one-liners).

## Form 1 — prose stanzas (`entry_type=stanza`)

```
Auburn Street, westbound, beginning at Washington Street, thence westerly on Auburn Street:
    0.84 miles at 25 miles per hour
    0.52 “ “ 30 “ “ “
    ending at Commonwealth Avenue; the total distance being 1.36 miles.
```

- One **row per speed sub-segment**. A directional traversal can have several
  sub-segments at different speeds; interior boundaries are NOT named in the
  source, so only the first segment carries `start_point` and the last carries
  `end_point`. `offset_miles` gives each sub-segment's cumulative start
  distance; `length_miles` its length.
- **Ditto marks** (`“ “ 30 “ “ “`) are expanded first by
  `scripts/expand_dittos.py` (see SKILL.md "Pre-normalization"); the resulting
  fully-explicit text is then decomposed.
- **Verification — distance checksum:** each stanza states "the total distance
  being Z miles"; `sum(sub-segment lengths)` must equal Z. **115 of 116
  stanzas pass exactly.** This is a source-intrinsic verifier no extractor can
  fake — it caught every parser bug during development.

### Parser notes (paragraph-based decomposition)
- Headers wrap across lines ("...thence northerly on \n Waltham Street:") — so
  parse blank-line-separated **paragraphs**, not lines.
- Endings vary: "ending at X", "ending north of X", "the **total** distance"
  vs "the distance", missing separators, and spelled-out totals
  ("...eighty-three hundredths (0.83) miles" → read the parenthetical).
- The ending is sometimes glued into the same paragraph as the speed lines;
  search each paragraph for the ending, don't expect a separate one.

## Form 2 — column tables (`entry_type=table`)

Streets with many zones are printed as 3-column tables
(`Start Point | End Point | Speed Limit`), e.g. "Eastbound Beacon Street:".
PDF **text extraction linearizes these into useless stacked columns** (row
pairing lost). They are extracted by **reading the original PDF page** with a
vision model (see [[pdf-page-vision-for-scrambled-tables]] / SKILL.md), one row
per table row. Endpoints may be GPS coordinates ("42.326424, -71.234588"),
preserved verbatim. 15 streets × 2 directions = 30 tables, 100 rows.

- **Verification — column-multiset reconciliation:** the set of start-points,
  end-points, and the speed multiset from the PDF read must match the
  (scrambled) text's column lists. Pairing is the only thing the PDF adds.
- Completeness: the 30 table headings in the text confirm 30 tables found.

## Form 3 — one-liners (`entry_type=oneliner`)

```
Cummings Road., 25 miles per hour from Homer Street to end. (Ord. No. X-23, 7-8-02)
```
5 inline entries at the end of the section. `start_point`/`end_point` from the
"from X to Y"; no length/offset.

## Known source defects (preserved, flagged in `notes`)
- **Lion Drive and Brandeis Road, westbound**: sub-segments sum to 1.02 mi but
  the stated total is 0.83 mi (its eastbound twin is 0.85). Source
  inconsistency; values kept verbatim, flagged. (the 1 checksum miss.)
- **Watertown Street eastbound**: a coordinate reads "2.359229, -71.203450" —
  missing the leading 4 (cf. westbound "42.359286"); kept verbatim, flagged.
- **Vine Street eastbound**: a source speed line reads "0.18 miles at 25 per
  hour" (missing "miles"); speed/length still recoverable.

## Counting / manifest

`count_entries` cannot verify this section (three forms; table rows are not
recoverable from the scrambled text). Completeness/correctness are instead
established by the **distance checksum** (stanzas) and **multiset
reconciliation** (tables); the manifest records `"counting": {"verified_by":
...}` so `validate.py` skips the regex-count check for this dataset.
