# Section 89 — Right turns prohibited

## Source shape

One boilerplate sentence ("No person shall make a right turn with a vehicle
at any of the following intersections.") followed by the entry list, one per
blank-line-separated paragraph, until the ordinance-history footer beginning
`(Rev. Ords.`. **22 entries in 20 paragraphs** as of revision 2026-01-16: two
paragraphs each contain two merged entries (see Source-text quirks). Entries
are alphabetical by first-named street — use that ordering to sanity-check
splits.

Section 87 (left turns prohibited) legitimately lists several of the same
locations (Peirce Elementary School Parking Lot, Ruane Road, North Street at
Albemarle Road) — complementary left/right bans, not duplicates. Do not
"deduplicate" across sections.

## Entry grammars observed

Roughly in frequency order:

1. `STREET onto CROSS.` → street, cross_street
   - "High Street onto Elliot Street."
2. `STREET onto CROSS, [from] TIME to TIME.` → trailing time window; a
   leading "from" before the window is dropped
   - "Auburn Street onto Curve Street, from 7:00 a.m. to 9:00 a.m."
3. `STREET, DIRECTION[,] onto CROSS.` → direction between commas or with the
   comma omitted before "onto"
   - "Linden Street, southbound, onto Cliff Road."
   - "Morseland Avenue, northbound onto Ward Street."
4. `STREET onto CROSS, DAYS, TIME to TIME [and TIME to TIME].` → days +
   one or two time windows
   - "Walnut Street, southbound onto Elm Road, school days, 7:00 a.m. to
     8:30 a.m. and 2:00 p.m. to 3:30 p.m."
5. `STREET onto CROSS, TIME to TIME, DAYS.` → same fields, order reversed
   - "Woodland Road onto Hancock Street, 7:00 a.m. to 4:00 p.m., Weekdays."
6. Trailing `(except bicycles)` → exemption = `bicycles` (Bristol Road,
   Crafts Street, North Street)
7. `STREET, DIRECTION into [the] FACILITY.` → "into" marks a non-street
   target (parking lot, drive); facilities are legal in both `street` and
   `cross_street`
   - "Ruane Road into the Peirce Elementary School Parking Lot."
8. `STREET, from APPROACH onto TARGET.` → approach phrase, see field
   placement rules (Jefferson Street, the only instance)
9. Compound schedule: two paired DAYS+TIMES groups in one entry (Beacon
   Street, the only instance) → semicolon-separated groups, see below

## Normalization rules

- Times convert to 24-hour ranges; "and" between windows → comma:
  "7:00 a.m. to 9:00 a.m. and 4:00 p.m. to 6:00 p.m." → `07:00-09:00,16:00-18:00`.
- A leading "from" before a time window is a filler word — drop it.
- "weekdays" / "Weekdays" (any position, any capitalization) →
  `mon,tue,wed,thu,fri`; plural day names → tokens ("Mondays" → `mon`);
  "school days" → `school_days`.
- **Compound schedules** (multiple DAYS+TIMES pairings in one entry): join
  groups with `;` in source order in both `days` and `times`; the i-th days
  group pairs with the i-th times group. Never flatten the pairing into one
  set. See the Beacon Street gold row.
- "southerly" → direction `southbound` (Grove Street, the only instance);
  no note needed.
- "(except bicycles)" → exemption = `bicycles` (drop "except" and
  parentheses).
- A leading article "the" is dropped from `cross_street` targets:
  "into the Peirce Elementary School Parking Lot" → cross_street =
  "Peirce Elementary School Parking Lot".

## Field placement rules

- **Leg qualifiers split off the target**: "onto Albemarle Road, eastern leg"
  → cross_street = `Albemarle Road`, location_detail = `eastern leg`. (This
  section uses comma-form leg qualifiers; the target street must stay
  geocodable on its own.)
- **Carriageway designations stay in the name**: "Commonwealth Avenue, South
  Drive" / "Commonwealth Avenue, North Drive" are part of the street/target
  name, never split (matches the 148 precedent).
- **`from APPROACH onto TARGET`** (mirrors the 148 rule): `street` = the
  first-named way, the whole approach phrase → `location_detail`, the `onto`
  target → `cross_street`. For Jefferson Street this yields street =
  cross_street = "Jefferson Street" — correct, not an error.
- Facilities and named drives are legal in `street` and `cross_street`
  ("Peirce Elementary School Parking Lot", "Riverside Office Center southerly
  drive").
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | cross_street | days | times | exemption | location_detail | notes |
|---|---|---|---|---|---|---|---|---|
| Beacon Street onto Beethoven Avenue, Mondays, Tuesdays, … | Beacon Street | | Beethoven Avenue | mon,tue,thu,fri,school_days;wed,school_days | 08:00-09:00,14:30-15:30;08:00-09:00,12:00-13:00 | | | |
| Grove Street, southerly into the Riverside Office Center southerly drive. | Grove Street | southbound | Riverside Office Center southerly drive | | | | | |
| Jefferson Street, from driveway of 2 Newton Place … | Jefferson Street | | Jefferson Street | | | | from driveway of 2 Newton Place (255 Washington Street) | |
| Crafts Street, westbound onto Albemarle Road, eastern leg … | Crafts Street | westbound | Albemarle Road | | | bicycles | eastern leg | |
| Lexington Street onto Staniford Street, 7:00 a.m. to 9:00 a.m. | Lexington Street | | Staniford Street | | 07:00-09:00 | | | split from merged source line; see spec |
| Linden Street, southbound, onto Cliff Road. | Linden Street | southbound | Cliff Road | | | | | split from merged source line; see spec |
| North Street, southeastbound onto Albemarle Road, eastern leg … | North Street | southeastbound | Albemarle Road | | | bicycles | eastern leg | split from merged source paragraph; see spec |
| Peirce Elementary School Parking Lot onto Berkeley Street. | Peirce Elementary School Parking Lot | | Berkeley Street | | | | | split from merged source paragraph; see spec |
| Ruane Road into the Peirce Elementary School Parking Lot. | Ruane Road | | Peirce Elementary School Parking Lot | | | | | |
| Woodland Road onto Hancock Street, 7:00 a.m. to 4:00 p.m., Weekdays. | Woodland Road | | Hancock Street | mon,tue,wed,thu,fri | 07:00-16:00 | | | |

## Source-text quirks

Two **merged-entry artifacts**, both already present in the raw pdfminer
output of tpr.pdf (they are not section-splitter bugs):

1. One physical line carries two entries (the city's PDF text layer has them
   on one line):
   `Lexington Street onto Staniford Street, 7:00 a.m. to 9:00 a.m. Linden
   Street, southbound, onto Cliff Road.`
   → split after "9:00 a.m." into two rows; each row's `source_text` is its
   own clause.
2. Two entries separated by a line break but **no blank line** (pdfminer
   line_margin grouping), so they form one paragraph:
   `North Street, southeastbound onto Albemarle Road, eastern leg (except
   bicycles).` + `Peirce Elementary School Parking Lot onto Berkeley
   Street.`
   → split at the sentence boundary into two rows.

Both splits are confirmed by the list's alphabetical ordering (Lexington <
Linden < Morseland; North < Peirce < Ruane). Flag all four resulting rows
with the note "split from merged source …; see spec".

- "Peirce" (not "Pierce") is the source's own spelling — reproduce it.
- "Woodland Road … , Weekdays." has a capitalized day token — normalize, no
  note needed.

## Counting rules (manifest)

```json
{"region_start": "\\A", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```

Verified count: **22**, equal to the true entry count.

**Why the region is anchored at `\A` (top of file):** the validator counts at
most one entry per blank-line paragraph, so it cannot see the two
merged-entry paragraphs (natural rules anchored at "following
intersections\\." count only 20). Anchoring at the top counts the two header
paragraphs (section title + boilerplate sentence), which exactly offsets the
two merged paragraphs and pins the expected row count at 22. This is a
deliberate, temporary workaround for a known source defect, not a loosened
check: any extraction that drops or invents a row still fails (≠ 22).

**Remediation:** if the conversion artifacts are ever fixed (each entry in
its own paragraph — e.g. via process-tpr.py post-processing), these rules
will count 24 and validation will fail loudly. At that point switch
`region_start` to `"following intersections\\."` (count becomes 22 again),
remove the four "split from merged source" notes, and delete this workaround
explanation.

## Proposed common vocabulary

This dataset needs paired multi-group schedules for the Beacon Street entry
(two DAYS×TIMES pairings in one atomic entry). The schema extends
`common#days` and `common#time_ranges` inline with a `;` group separator;
the i-th days group pairs with the i-th times group. Proposed for
`_common.json` (not added here because other agents are editing in
parallel):

- `days_groups`: pattern `DAYS(;DAYS)*` where DAYS is the `common#days`
  pattern — "Semicolon-separated day-set groups; pairs positionally with
  time_ranges_groups".
- `time_ranges_groups`: pattern `TIMES(;TIMES)*` where TIMES is the
  `common#time_ranges` pattern — "Semicolon-separated time-window groups;
  pairs positionally with days_groups".

Plain single-group values remain valid under both patterns, so existing
datasets could migrate `days`/`times` to these defs without data changes.
