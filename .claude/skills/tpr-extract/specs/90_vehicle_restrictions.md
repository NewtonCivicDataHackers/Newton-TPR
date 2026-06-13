# Section 90 — Vehicle Restrictions on Public Ways

## Source shape

A single mangled header line — "Sec. TPR-90. Vehicle Restrictions on Public
Ways., the following prohibitions apply:" (the splitter fused the section
title and the lead-in clause; the doubled punctuation `Ways.,` is verbatim).
Entries follow, one per blank-line-separated paragraph, each opening with a
street-name label (`STREET: No vehicle of any description, except …`), until
the ordinance-history footer beginning `(TPR-360`. 5 entries as of revision
2026-01-16.

## Entry grammars observed

1. **Timed school-day exclusion** (4 of 5 entries):
   `STREET: No vehicle of any description, except those of EXEMPT, shall go
   upon STREET between TIME and TIME [school-day condition].`
   - "Kimball Terrace: No vehicle of any description, except those of
     resident and permit holders and service vehicles, shall go upon Kimball
     Terrace between 8:00 a.m. and 5:00 p.m. when public schools of the city
     are in session." → street = Kimball Terrace, restriction = travel,
     exemptions = "resident and permit holders and service vehicles",
     days = school_days, times = 08:00-17:00.
2. **Directional entry prohibition on a segment** (Norwood Avenue):
   `STREET: No vehicle of any description, except those of EXEMPT, shall
   enter STREET in the DIRECTIONerly direction, to the DIRECTION of POINT.`
   → restriction = entry, direction from "in the easterly direction",
   from_point = POINT, location_detail = "east of Bridges Avenue".

The leading label always repeats the street named after "shall go
upon"/"shall enter"; record it once in `street`.

## Normalization rules

- `restriction`: "shall go upon" → `travel`; "shall enter" → `entry`.
- `vehicle_type`: "No vehicle of any description" → `all`. Every current
  entry restricts all vehicles; if a future revision names a class (e.g.
  commercial vehicles over a weight), record the class phrase instead.
- `exemptions`: copy the "except those of …" clause verbatim, minus the
  leading "those of" and the trailing comma before "shall". Internal commas
  stay ("property owners whose access is Minot Place, and service vehicles").
- `days`: "school days", "when public schools of the city are in session",
  and "on any day when the public schools of the city are in session" all
  normalize to `school_days`. No stated days → empty (every day).
- `times`: "between 8:00 a.m. and 5:00 p.m." → `08:00-17:00`; no stated
  window → empty (at all times).
- `direction`: "in the easterly direction" → `eastbound` (likewise
  westerly/northerly/southerly → the matching `common#direction` value).

## Field placement rules

- **Whole-way restrictions** (the four school-day entries): `from_point`,
  `to_point`, and `location_detail` all empty — the restriction covers the
  entire named way.
- **Open-ended segment qualifiers** ("to the east of Bridges Avenue"):
  `from_point` = the reference point (Bridges Avenue), `to_point` empty
  (open-ended), and the relational phrase minus the leading "to the" goes in
  `location_detail` ("east of Bridges Avenue") so the side of `from_point`
  is preserved. The deliberate redundancy mirrors 148's portion
  parentheticals: the atom is normalized AND the relation is kept.
- **Exemption street names stay in `exemptions`.** Minot Place and the
  Norwood/Parkview abutter clauses name streets, but those identify exempt
  parties, not restricted locations — never promote them to location
  columns.
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | from_point | restriction | exemptions | days | times | location_detail |
|---|---|---|---|---|---|---|---|---|
| Blithedale Street … 8:00 a.m. and 5:00 p.m. school days | Blithedale Street | | | travel | resident and permit holders and service vehicles | school_days | 08:00-17:00 | |
| Minot Place … property owners whose access is Minot Place | Minot Place | | | travel | property owners whose access is Minot Place, and service vehicles | school_days | 07:45-16:00 | |
| Norwood Avenue … easterly direction, to the east of Bridges Avenue | Norwood Avenue | eastbound | Bridges Avenue | entry | property owners whose properties abut Norwood Avenue or Parkview Avenue | | | east of Bridges Avenue |

(`to_point`, `notes` empty in all three; `vehicle_type` = `all` throughout.)

## Source-text quirks

- PDF line-wrap splits two entries across blank lines; the fragments start
  lowercase ("shall go upon Blithedale Street…", "go upon Lasell Street…")
  and must be rejoined into the previous entry's `source_text`. The
  validator's `entry_start: ^[A-Z]` rule keeps the count right; the
  extractor must rejoin the text.
- The Blithedale entry says "school days" bare where the others spell out
  "when public schools of the city are in session" — same meaning, same
  `school_days` token, no note needed.
- The header's "Ways., the following prohibitions apply:" is a splitter
  artifact of the fused title/lead-in; it is not an entry.
- The footer `(TPR-360, 09-14-17; TPR-755, 07-22-21; TPR-823, 06-16-22)` and
  the trailing "Secs. TPR-91 – 94. Reserved." line are outside the entry
  region.

## Counting rules (manifest)

```json
{"region_start": "the following prohibitions apply:", "region_end": "\\(TPR-360", "entry_start": "^[A-Z]"}
```

Verified: 5 entries; the two lowercase continuation fragments are skipped.
