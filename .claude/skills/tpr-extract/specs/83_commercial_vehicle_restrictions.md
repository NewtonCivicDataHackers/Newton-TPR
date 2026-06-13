# Section 83 — Heavy commercial vehicle restrictions

Street-keyed truck-exclusion entries ("Street. Commercial vehicles in excess
of N tons ... from X to Y ..."). 33 rows.

## Two lists (distinguished by `status`)
- **in_effect** (22): the main (a) list of streets where the exclusion is in
  force. NOTE: two `Cross references—` / `State law references—` paragraphs
  interrupt this list mid-way (between Dudley Road and Grove Street) — they are
  NOT entries; skip them.
- **pending_state_approval** (11): the "Note to Sec TPR-83" list — additional
  exclusions the board passed but the Commonwealth had not approved as of the
  2007 recodification. Albemarle Road and Winchester Street appear in both
  lists (different segments/status).

## Fields
`weight_limit_tons` normalizes "five (5) tons"→5, "2½"/"2-1/2"→2.5. `times`,
`from_point`/`to_point`, `alternate_route`, `locality` as stated. Editor's-note
markers (* / **) preserved in `notes`.

## Verification
Hand-extracted from the text (regex counting is confounded by the interleaved
cross-reference paragraphs and the two separate lists); `source_text` unique.
