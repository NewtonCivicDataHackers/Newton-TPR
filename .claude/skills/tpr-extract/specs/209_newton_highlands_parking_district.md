# Section 209 — Newton Highlands Parking District

## Source shape

Administrative prose (a)–(b), then clause (c) lists the streets composing the
district's geographic boundary, then clause (d) onward (restriction menus,
permit caps) which are NOT per-street assignments. Only the (c) membership
list is extracted: one row per street/segment.

## Entry grammar

`STREET [(PARENTHETICAL)]` — one per entry.
- Parenthetical `X to Y` → `from_point`=X, `to_point`=Y
  ("Beacon Street (M.B.T.A. Bridge to Locke Road/Irvington Road)").
- Trailing `, including <addresses>` inside the parenthetical → `segment_note`.
- Non-range parenthetical that disambiguates locality ("(Newton Corner)") →
  `segment_note`; from/to stay empty.
- Bare street name → whole street; from/to/segment_note empty.

`district` is constant ("Newton Highlands").

## Counting rules (manifest)

The (c) list ends at clause (d) ("(d) The public streets ...").
Entries are blank-line separated (paragraph counting).
