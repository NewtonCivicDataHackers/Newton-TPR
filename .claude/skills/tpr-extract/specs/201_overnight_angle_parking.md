# Section 201 — Overnight on-street angle parking areas

## Source shape

Short prose intro, then a single entry list. As of revision 2026-01-16 there
is exactly **1 entry**, ending before the ordinance footer `(TPR-265`.

## Entry grammar

`STREET: between A and B, up to N spaces.`
- "Chestnut Street: between Oak Street and Linden Street, up to 25 spaces." →
  street=Chestnut Street, from_point=Oak Street, to_point=Linden Street,
  spaces=25.

`spaces` records the maximum ("up to N").

## Counting rules (manifest)

```json
{"region_start": "Newton Revised Ordinances, 2012\\.", "region_end": "\\(TPR-265", "entry_start": "^[A-Z]"}
```
