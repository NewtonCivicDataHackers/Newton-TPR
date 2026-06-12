# Section 148 — Obedience to yield signs

## Source shape

Boilerplate paragraphs (a)–(c) end with "…is authorized at the following
locations:". Entries follow, one per blank-line-separated paragraph, until the
ordinance-history footer beginning `(Rev. Ords.`. 32 entries as of revision
2026-01-16.

## Entry grammars observed

Several variants, roughly in frequency order:

1. `STREET, DIRECTION at CROSS.` → street, direction, yields_to
   - "Alderwood Road, eastbound at Burrage Road."
2. `STREET at CROSS, DIRECTION.` → same fields, direction trailing
   - "College Road at Beacon Street, southwestbound."
3. `STREET, DIRECTION[,] from LANE onto TARGET.` → the lane goes in
   `location_detail`, the `onto` target is `yields_to`
   - "Brookline Street, westbound, from right turn lane onto Dedham Street."
4. `STREET, DIRECTION at the channelized traffic island at CROSS.` →
   `location_detail` = "at the channelized traffic island", yields_to = CROSS
   - "Collins Road, westbound at the channelized traffic island at Waban Avenue."
5. No direction at all: "Islington Oval Road at Islington Road." → direction
   empty.

## Field placement rules

- **Positional qualifiers always go in `location_detail`** ("just west of
  Oldham Road", "at a point 240 feet south of Crafts Street", "at merge") —
  never in `notes`. `notes` is reserved for source-text anomalies and
  ambiguity flags; it never carries data.
- **`at CROSS` always yields `yields_to = CROSS`**, even when no direction is
  stated ("Islington Oval Road at Islington Road." → yields_to = Islington
  Road, direction empty, no note needed).
- **Ways named "X to Y"** ("Grove Street to Route 16 Collector-Distributor
  Road") are ramp designations: keep the full phrase as `street`.

## Judgment calls (keep these consistent)

- **`from X onto Y`**: X describes the approach (lane/way) → `location_detail`;
  Y is what's entered → `yields_to`.
- **`from STREET` with no `onto`** (e.g. "Commonwealth Avenue, North Drive,
  from Commonwealth Avenue, South Drive, opposite Central Street,
  northbound."): the movement is ambiguous — which way carries the sign is not
  parseable from the grammar. Keep `street` = the first-named way, put the
  whole `from …` phrase in `location_detail`, leave `yields_to` empty, and
  note the ambiguity.
- **Highway-direction-in-name**: "I-95/Massachusetts-128 Northbound" — the
  "Northbound" is the carriageway designation; record street =
  "I-95/Massachusetts-128", direction = northbound.
- **Parenthetical portion qualifiers**: "Waban Avenue (one-way southbound
  portion)" — keep the parenthetical in `street`; its "southbound" also
  supplies `direction`.
- **Island position without a target street** ("…at the channelized traffic
  island south of Commonwealth Avenue."): position is relative, not an entered
  street → whole phrase in `location_detail`, `yields_to` empty.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | yields_to | location_detail | notes |
|---|---|---|---|---|---|
| Comm Ave North Drive, from … South Drive | Commonwealth Avenue, North Drive | northbound | | from Commonwealth Avenue, South Drive, opposite Central Street | movement ambiguous in source; see spec |
| Comm Ave North Drive, westbound onto … | Commonwealth Avenue, North Drive | westbound | Commonwealth Avenue | just west of Oldham Road | |
| Grove Street to Route 16 … | Grove Street to Route 16 Collector-Distributor Road | | Washington Street | from the right turn lane | |
| Islington Oval Road at Islington Road | Islington Oval Road | | Islington Road | | |
| Waban Avenue (one-way southbound portion) … | Waban Avenue (one-way southbound portion) | southbound | Waban Avenue (two-way portion) | approximately 150 feet northeast of Annawan Road | unclosed parenthesis in source |
| Waltham Street … (western leg) … | Waltham Street | southbound | Waltham Street (western leg) | at a point 240 feet south of Crafts Street | |
| Washington Street … Beacon Street merge | Washington Street | eastbound | Beacon Street | at merge | |
| Highland Street … connector … | Highland Street | eastbound | Highland Street | at the connector between Chestnut Street and Highland Street | |

## Source-text quirks

- PDF line-wrap can split an entry across a blank line; the fragment starts
  lowercase ("northeast of Annawan Road.") and must be rejoined to the
  previous entry. The validator's `entry_start: ^[A-Z]` rule handles counting;
  the extractor must rejoin the text in `source_text`.
- The Waban Avenue entry has an unclosed parenthesis in the source — note it,
  reproduce it verbatim in `source_text`.

## Counting rules (manifest)

```json
{"region_start": "following locations:", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```
