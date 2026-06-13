# Section 194 — Time limits in municipal off-street parking areas

## Source shape

A wide **matrix table** on PDF **page 208** (top-left cell "Metered Parking
Lot"). PDF text extraction scrambles it into unusable stacked columns in
`sections/194.txt`, so it is extracted by **reading the PDF page** with a
vision model (see [[pdf-page-vision-for-scrambled-tables]] / SKILL.md
"Pre-normalization" is not enough here — the text is unrecoverable). 11 lots
as of revision 2026-01-16.

Columns: lot name (grouped under village sub-headings — Auburndale, Newton
Centre, Newton Corner, Newton Highlands, Newtonville, West Newton); space
counts by limit (1hr / 2hr / 3hr / 6hr / no-time-limit); accessible; EV;
"reserved by permit or other"; and which enforcement window applies
(8AM-6PM Mon-Sat vs Mon-Fri).

One row per lot. Village sub-heading rows are group labels, not lots.

## Permit-code legend (decodes `reserved_by_permit` and count annotations)

- **A** = reserved for vehicles displaying an Auburndale Business Permit
- **BH** = Brigham House
- **NC** = long-term spaces reserved for Newton Centre employees with permits,
  Mon–Fri 8am–6pm
- **CC** = 15 Cooper Center Employee Permits; time limits do not apply to
  vehicles displaying a CC permit
- **ZC** = ZipCar

`reserved_by_permit` is kept verbatim in `count(code)` form (e.g.
`2(ZC) & 12(NC)` = 2 ZipCar + 12 Newton Centre). Where a time-limit count cell
itself carries a code (Austin St: `69 (CC)` 3hr, `50 (CC)` no-limit), the
integer goes in the count column and the exception is recorded in `notes`.

## Verification

No text multiset is recoverable (text fully scrambled). Verified by **two
independent PDF-page reads** (a Sonnet agent + the orchestrator) agreeing
**11/11 lots, every cell**. Manifest uses
`"counting": {"verified_by": ...}` so `validate.py` skips the regex count.

## Related

TPR-196 ("Time limits in *other* municipal off-street parking areas" — the
no-payment lots) is a separate table, currently merged into `sections/195.txt`
by a `process-tpr.py` splitter bug and not yet extracted. See [[tpr-extract-skill-state]].
