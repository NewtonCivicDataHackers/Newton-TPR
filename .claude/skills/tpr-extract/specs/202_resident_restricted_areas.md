# Section 202 — Resident restricted areas

## Source shape

Prose intro, then blank-line-separated street entries until the ordinance
footer `(Ord. No. S-227`. 28 entries as of revision 2026-01-16.

## Entry grammars observed

1. `STREET[, LOCALITY][:|,] SIDE side, entire length.` →
   "Abbott Street, Newton Upper Falls: both sides, entire length." /
   "Lawrence Avenue, west side, entire length."
2. `STREET[:|,] SIDE side, from A to B.` (range) →
   "Allerton Road, south side, from Hyde Street to Centre Street."
3. Offset endpoints: "from a point N feet DIR of X" →
   from_point=X, from_offset_feet=N, from_offset_direction=DIR (same for `to`).
4. Street **header** (bare name or name ending in `:`) followed by numbered
   sub-clauses `(1) … (2) …` — Gibbs Street, Waban Park. The header is NOT an
   entry; each sub-clause is a row with `street` = the header street.

## Field placement rules

- `side`: both / north / south / east / west (common#side).
- `locality`: village qualifier ("Newton Upper Falls", "Newton Highlands",
  "Waban") when the source names one; else empty.
- `extent` = "entire length" only when the whole street is covered (no
  from/to). Use `to_point` = "end" for "to end".
- Drive/reservation qualifiers ("north side of the north drive along the
  reservation") → `side` + `notes`, since they are not a mappable cross-street.
- An administrative sub-clause that is not a single mappable segment
  (Peabody Street's visitor-permit `(1)` paragraph) → one row, `street` set,
  the provision summarized in `notes`; segment columns empty.

## Counting rules (manifest)

```json
{"region_start": "otherwise noted\\.", "region_end": "\\(Ord\\. No\\. S-227", "entry_start": "^(\\(\\d+\\)|[A-Z][^:]*,|[A-Z].*:\\s*\\S)"}
```

`entry_start` matches numbered sub-clauses, capitalized lines containing a
comma, or capitalized lines with content after a colon — but NOT bare headers
ending in `:` (e.g. "Waban Park:") or PDF-wrapped continuation fragments.
