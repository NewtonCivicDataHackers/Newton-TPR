# Section 87 — Left turns prohibited

## Source shape

One boilerplate sentence — "No person shall make a left turn with a vehicle
at any of the following intersections:" — then entries, one per
blank-line-separated paragraph, until the ordinance-history footer beginning
`(Rev. Ords.`. 40 entries as of revision 2026-01-16. Every entry is a single
prohibited left-turn movement; there are no sub-lists or header paragraphs
inside the region.

## Entry grammars observed

Roughly in frequency order:

1. `STREET[, DIRECTION] onto CROSS.` → street, direction, cross_street
   - "Morseland Avenue, southbound onto Ward Street."
   - "Davis Street onto Highland Street." (no direction)
2. `STREET[, DIRECTION,] onto CROSS DIRECTION2.` → DIRECTION2 modifies the
   receiving street → `cross_street_direction`
   - "Grove Street, southbound, onto Central Street eastbound."
   - "Bridge Street southbound onto Watertown Street eastbound between
     4 p.m. and 6 p.m."
3. `STREET onto CROSS, DIRECTION2.` → trailing direction after the target
   also attaches to the receiving street → `cross_street_direction`
   - "Forest Street onto Walnut Street, northbound."
4. `STREET[, DIRECTION] into DESTINATION.` → turn into a driveway or parking
   facility → `destination`, `cross_street` empty
   - "Beacon Street, eastbound, into Newton Centre municipal parking area."
   - "Ruane Road into the Peirce Elementary School Parking Lot."
5. Restatement grammar: `STREET, for DIRECTIONbound vehicles on STREET at
   CROSS.` → direction = DIRECTIONbound, cross_street = CROSS (the first
   STREET is repeated after "on"; no data in the repetition)
   - "Park Street, for northbound vehicles on Park Street at Centre Street."
6. Schedule tails: ", from 7:00 a.m. to 9:00 a.m.", "between 4 p.m. and
   6 p.m.", ", school days, 8:00 a.m. to 9:30 a.m. and 3:00 p.m. to
   4:30 p.m.", ", 7:00 a.m. to 4:00 p.m.., weekdays.", plus one compound
   multi-day schedule (Beacon Street onto Beethoven Avenue — see gold row).
7. Exception tails: "(except bicycles)" → exceptions = `bicycles` (3 entries).

## Normalization rules

- `easterly`/`northerly`/`southerly`/`westerly` → eastbound/northbound/
  southbound/westbound ("Cypress Street, easterly onto Centre Street." →
  direction = eastbound).
- `for Xbound vehicles on STREET` → direction = Xbound.
- Times convert to 24-hour ranges; "from X to Y" and "between X and Y" both
  → one range ("between 4 p.m. and 6 p.m." → `16:00-18:00`); "X and Y"
  joining two windows → comma-joined (`08:00-09:30,15:00-16:30`).
- Day words expand/normalize: "weekdays" → `mon,tue,wed,thu,fri`;
  "school days" → `school_days`; "Mondays, Tuesdays, Thursdays, Fridays" →
  `mon,tue,thu,fri`.
- Exceptions drop "except" and parentheses, lowercase: "(except bicycles)"
  → `bicycles`.
- `destination` drops a leading article: "into the Riverside Office Center
  northerly drive" → `Riverside Office Center northerly drive`.

## Field placement rules

- **Direction placement is positional.** A direction token attached to the
  first street (before `onto`/`into`) is the approach `direction`; a
  direction token after the onto-target — inline ("onto Dedham Street
  northbound") or trailing (", northbound." / ", eastbound.") — is
  `cross_street_direction`. Both can appear in one entry (grammar 2).
- **`onto X` vs `into X`**: `onto` targets are named streets/ways →
  `cross_street`; `into` targets are driveways/parking facilities →
  `destination`. `cross_street` holds only named streets/ways; `destination`
  holds only non-street facilities. Never fill both.
- **Facilities can be the origin too**: "Peirce Elementary School Parking
  Lot onto Berkeley Street." → street = Peirce Elementary School Parking
  Lot, cross_street = Berkeley Street.
- **Carriageway designations stay in the street column**: "onto Commonwealth
  Avenue, North Drive" → cross_street = `Commonwealth Avenue, North Drive`.
- **Leg qualifiers go in `location_detail`**: "onto Albemarle Road, eastern
  leg" → cross_street = Albemarle Road, location_detail = `eastern leg`.
- **`at CROSS` in the restatement grammar (5) → cross_street = CROSS** when
  CROSS is a named street. When it is not ("at the entrance to the
  Massachusetts Turnpike"), the whole `at …` phrase goes in
  `location_detail` and cross_street stays empty.
- **Compound schedules** (different times on different days) go in
  `schedule_detail` as semicolon-joined `DAYS TIMES` clauses (common day
  tokens, 24-hour ranges); `days` and `times` stay empty for that row.
  Simple schedules always use `days`/`times`, never `schedule_detail`.
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | cross_street | cross_street_direction | destination | days | times | schedule_detail | location_detail | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Auburn Street, eastbound into driveway of 1900 Commonwealth Avenue. | Auburn Street | eastbound | | | driveway of 1900 Commonwealth Avenue | | | | | |
| Beacon Street onto Beethoven Avenue, Mondays, Tuesdays… | Beacon Street | | Beethoven Avenue | | | | | mon,tue,thu,fri,school_days 08:00-09:00,14:30-15:30; wed,school_days 08:00-09:00,12:00-13:00 | | |
| Forest Street onto Walnut Street, northbound. | Forest Street | | Walnut Street | northbound | | | | | | |
| Nahanton Street, eastbound, onto Dedham Street northbound at the southernmost intersection… | Nahanton Street | eastbound | Dedham Street | northbound | | | | | at the southernmost intersection of Nahanton Street and Dedham Street | source entry wraps across a blank line; rejoined |
| North Street, northwestbound onto Albemarle Road, eastern leg (except bicycles). | North Street | northwestbound | Albemarle Road | | | | | | eastern leg | |
| Washington Street onto Waltham Street, eastbound. | Washington Street | | Waltham Street | eastbound | | | | | | near-duplicate of the adjacent 'Washington Street, eastbound, onto Waltham Street.' entry |
| Washington Street, eastbound, onto Waltham Street. | Washington Street | eastbound | Waltham Street | | | | | | | near-duplicate of the adjacent 'Washington Street onto Waltham Street, eastbound.' entry |
| Washington Street, westbound, onto Washington Street (opposite Elm Street). | Washington Street | westbound | Washington Street | | | | | | opposite Elm Street | |
| Washington Street, for westbound vehicles on Washington Street at the entrance to the Massachusetts Turnpike. | Washington Street | westbound | | | | | | | at the entrance to the Massachusetts Turnpike | |
| Williams School driveway, Grove Street, onto Grove Street northbound. | Williams School driveway | | Grove Street | northbound | | | | | | appositive 'Grove Street' after the driveway name locates the driveway; redundant with cross_street |
| Woodland Road onto Hancock Street, 7:00 a.m. to 4:00 p.m.., weekdays. | Woodland Road | | Hancock Street | | | mon,tue,wed,thu,fri | 07:00-16:00 | | | double period after 'p.m.' in source |

The two Washington→Waltham entries are distinct source entries (almost
certainly the same restriction enacted twice); extract both as written —
`source_text` differs, so uniqueness holds.

## Source-text quirks

- **PDF line-wrap split**: the Nahanton Street entry wraps across a blank
  line; the fragment "and Dedham Street." starts lowercase and must be
  rejoined into the previous entry's `source_text`. The counting rules skip
  it automatically.
- **Two-line paragraph, no blank line**: the Beacon Street onto Beethoven
  Avenue entry spans two source lines with no blank line between them — one
  paragraph, one entry; whitespace-collapse into one `source_text`.
- **Double period**: "7:00 a.m. to 4:00 p.m.., weekdays." — reproduce
  verbatim in `source_text`, normalize the time normally, note it.
- **Self-referencing turn**: "Washington Street, westbound, onto Washington
  Street (opposite Elm Street)." is a continuation movement at the Elm
  Street junction (same shape as section 96's); keep both street columns as
  Washington Street and the parenthetical in `location_detail`.

## Proposed common vocabulary

`schedule_clauses` — compound day/time schedule: semicolon-joined clauses of
`DAYS TIMES`, where DAYS matches `common#days` and TIMES matches
`common#time_ranges` (e.g. `mon,tue,thu,fri,school_days 08:00-09:00,14:30-15:30;
wed,school_days 08:00-09:00,12:00-13:00`). Defined inline as the
`schedule_detail` pattern in this dataset's schema because `_common.json`
could not be edited at authoring time; worth promoting to `_common.json` —
other turn-restriction sections (88, 89) and parking sections are likely to
hit the same different-times-on-different-days shape.

## Counting rules (manifest)

```json
{"region_start": "following intersections:", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^[A-Z]"}
```

40 entries as of revision 2026-01-16; the lone lowercase fragment
"and Dedham Street." is skipped as a continuation, and the two-line Beethoven
Avenue paragraph counts once. Verified with
`validate.count_entries` against `sections/87.txt`.
