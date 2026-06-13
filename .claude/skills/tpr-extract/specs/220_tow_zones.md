# Section 220 — Parking prohibitions for tow zones

176-class mixed-format section. 62 rows.

## Forms
- **3 blanket prohibitions** (preamble): tow-away applies to any vehicle in
  violation of TPR-177 (game-day), in any fire lane, or in any bus stop —
  `restriction='blanket prohibition'`, `street` empty.
- **Em-dash inline entries**: "STREET — Tow-away zone, SIDE side, [schedule,]
  [segment]." The dash char varies in the source (— / – / ─ / -); normalized.
- **Heading + numbered sub-clauses**: "STREET" then "(1) Tow-away zone, ..."
  → one row per sub-clause (street-prefixed source_text).

`restriction` normalized to 'tow-away zone' (incl. the "Tow-way" typo, flagged
in notes) / 'parking prohibited' (Essex Road) / 'blanket prohibition'.
from/to from "from X to Y"/"between X and Y"; other location phrasing →
`segment_detail`; times/day phrases → `schedule`. source_text authoritative.

## Verification
Deterministic parse → 62 rows, matching the independent count both Sonnet and
Opus produced in an earlier double-extraction. source_text unique. Manifest
counting = verified_by.
