# Section 99 — Through travel prohibited

## Source shape

No boilerplate and no "following locations:" lead-in: the section title line
("Sec. TPR-99. Through travel prohibited") is followed directly by the
entries, one per blank-line-separated paragraph, until the ordinance-history
footer beginning `(TPR-42,`. After the footer comes a separate
"Sec. TPR-100—TPR-144. Reserved." paragraph (outside the counting region).
11 entries as of revision 2026-01-16.

Each entry prohibits a through movement: traffic on `street` may not cross
`cross_street` and/or continue onto `onto_street`. The `onto` target is very
often the same street name as the approach — that repetition IS the through
movement; record both.

## Entry grammars observed

1. `STREET, LEG, crossing CROSS, continuing onto ONTO, DIRECTION (except X).`
   - "Albemarle Road, eastern leg, crossing Crafts Street, continuing onto
     Albemarle Road, northbound (except bicycles)."
2. `STREET onto ONTO, SCHEDULE[, SCHEDULE_2].` — schedule-only, no cross
   street
   - "Beacon Street onto Beethoven Avenue, Mondays, Tuesdays, Thursdays,
     Fridays, school days, 8:00 a.m. to 9:00 a.m. and 2:30 p.m. to 3:30 p.m.,
     Wednesdays, school days, 8:00 a.m. to 9:00 a.m. and 12:00 p.m. to
     1:00 p.m."
3. `STREET DIRECTION at CROSS, onto ONTO, SCHEDULE.`
   - "Capital Street eastbound at Washburn Street, onto Capital Street,
     school days, 8:00 a.m. to 8:45 a.m."
4. `STREET, at CROSS, DIRECTION (except X).` — no onto target
   - "Commonwealth Avenue, North Drive, at Bristol Road, eastbound (except
     bicycles)."
5. `STREET, crossing CROSS onto ONTO, TIMES, DAYS.` — schedule order flipped
   - "Hancock Street, crossing Woodland Road onto Hancock Street,
     7:00 a.m.to 4:00 p.m., Weekdays."
6. `STREET[, DIRECTION,] [at CROSS,] onto ONTO.` — bare movement, no
   schedule, no exception
   - "Lowell Avenue, southbound, at Walnut Street, onto Lowell Avenue."
   - "Trowbridge Avenue, onto Tiger Drive." / "Tiger Drive onto Trowbridge
     Avenue."

## Normalization rules

- Plural day names → tokens: "Mondays" → `mon`; "Weekdays" →
  `mon,tue,wed,thu,fri`; "school days" → `school_days`.
- A day list followed by "school days" is one day set — keep source order
  and comma-join: "Mondays, Tuesdays, Thursdays, Fridays, school days" →
  `mon,tue,thu,fri,school_days`.
- Times convert to 24-hour ranges; "and"-joined windows comma-join:
  "8:00 a.m. to 9:00 a.m. and 2:30 p.m. to 3:30 p.m." →
  `08:00-09:00,14:30-15:30`. A leading "from" ("from 7:00 a.m. to
  9:00 a.m.") is dropped: `07:00-09:00`.
- Exceptions drop parentheses and the word "except", lowercase:
  "(except bicycles)" → `bicycles`.
- Directions normalize to the common vocabulary whether comma-set-off
  ("…, southbound, at…") or run-on ("Capital Street eastbound at…").

## Field placement rules

- **Leg qualifiers go in `location_detail`**, keeping `street` geocodable:
  "Albemarle Road, eastern leg, crossing…" → street = `Albemarle Road`,
  location_detail = `eastern leg`. But **named carriageways stay whole in
  `street`** per the 148/96 precedent: "Commonwealth Avenue, North Drive"
  is the street name, not a qualifier.
- **`crossing X` and `at X` both fill `cross_street`.** They are the street
  at which the prohibition operates.
- **`onto X` / `continuing onto X` fills `onto_street`**, even when X is the
  same name as `street` (Capital, Hancock, Lowell, both Albemarle entries).
  Never collapse it into notes or drop it as redundant.
- **Two schedules in one entry** (Beacon Street, Evelyn Road): the source
  states a second day set with its own times ("…, Wednesdays, school days,
  8:00 a.m. to 9:00 a.m. and 12:00 p.m. to 1:00 p.m."). First schedule →
  `days`/`times`, second → `days_2`/`times_2`, in source order. Never merge
  the two day sets into one `days` value — the times differ by day.
- Empty `days` + `times` means the prohibition applies at all times.
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | cross_street | onto_street | location_detail | exception | days | times | days_2 | times_2 |
|---|---|---|---|---|---|---|---|---|---|---|
| Albemarle Road, eastern leg, crossing Crafts Street… | Albemarle Road | northbound | Crafts Street | Albemarle Road | eastern leg | bicycles | | | | |
| Beacon Street onto Beethoven Avenue, Mondays… | Beacon Street | | | Beethoven Avenue | | | mon,tue,thu,fri,school_days | 08:00-09:00,14:30-15:30 | wed,school_days | 08:00-09:00,12:00-13:00 |
| Capital Street eastbound at Washburn Street… | Capital Street | eastbound | Washburn Street | Capital Street | | | school_days | 08:00-08:45 | | |
| Commonwealth Avenue, North Drive, at Bristol Road… | Commonwealth Avenue, North Drive | eastbound | Bristol Road | | | bicycles | | | | |
| Gilbert Street onto Curve Street, from 7:00 a.m.… | Gilbert Street | | | Curve Street | | | | 07:00-09:00 | | |
| Hancock Street, crossing Woodland Road onto Hancock Street… | Hancock Street | | Woodland Road | Hancock Street | | | mon,tue,wed,thu,fri | 07:00-16:00 | | |

## Source-text quirks

- Several entries begin with a leading space in the source (PDF artifact);
  the validator's paragraph splitter strips lines, and whitespace-collapsing
  `source_text` removes it anyway.
- The Hancock Street entry has a missing space — "7:00 a.m.to 4:00 p.m." —
  reproduce it verbatim in `source_text`; the normalized `times` value is
  unaffected. No note needed.
- Two entry pairs wrap across physical lines mid-clause ("(except /
  bicycles).", and the Beacon/Evelyn schedules) but never across a blank
  line at this revision, so no lowercase continuation fragments to rejoin —
  watch for them in future revisions regardless.
- The footer "(TPR-42, 01-08-10; …)" itself wraps across two lines; the
  `region_end` regex matches its opening token so this never affects
  counting.

## Counting rules (manifest)

```json
{"region_start": "Through travel prohibited", "region_end": "\\(TPR-\\d+,", "entry_start": "^[A-Z]"}
```

`region_start` is the section title (there is no "following locations:"
lead-in). `region_end` matches the ordinance-history footer's first token
`(TPR-42,` and is written generically so renumbering the first ordinance
reference survives. Verified: 11 entries at revision 2026-01-16.
