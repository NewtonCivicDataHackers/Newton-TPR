# Section 149 — School zones

## Source shape

One sentence of boilerplate ("The following are hereby established as school
zones:"), then entries until the ordinance-history footer beginning
`(Rev. Ords.`. 32 entries as of revision 2026-01-16.

Entries take two forms:

- **Inline**: `SCHOOL: STREET, …` in a single paragraph
  ("Angier School: Beacon Street, from a point 25 feet east of Manitoba Road,
  easterly 575 feet.").
- **Grouped**: a header-only paragraph `SCHOOL:` (ends at the colon, no row)
  followed by numbered paragraphs `(1) STREET, …`, `(2) STREET, …` — one row
  each, inheriting `school` from the header. Eight groups in the current
  revision; Brimmer-May has a single numbered entry.
- **Hybrid**: Horace Mann School's header paragraph carries its own inline
  segment AND is followed by two numbered entries (3 rows total).

Two separate inline entries share `school` = "Burr School" (two different
streets) — two rows, same school value.

## Entry grammars observed

1. Two endpoints, either bare or offset:
   `STREET, from [a point N feet DIR of] FROM to [a point M feet DIR of] TO[, both directions].`
   - "(1) Park Street, from a point 112 feet south of Arlington Street to a
     point 68 feet south of Elmwood Street, both directions."
   - "(2) Tremont Street, from Park Street to a point 85 feet east of Hibbard
     Road, both directions."
2. Extent grammar — start point plus heading and length, no end point:
   `STREET, from a point N feet DIR of FROM, DIRECTIONerly L feet.`
   - "Angier School: Beacon Street, from a point 25 feet east of Manitoba
     Road, easterly 575 feet." → extent_direction = east,
     extent_length_feet = 575, to_* empty.
3. Whole street: `SCHOOL: STREET.` — "Brown Middle School: Meadowbrook Road."
   → street only, all segment fields empty.
4. Bare endpoints without the `from` keyword:
   "Newton Montessori School: Crescent Avenue, Centre Street to Norwood
   Avenue." → from_point = Centre Street, to_point = Norwood Avenue.
5. Offset without "a point": "Education Center: Walnut Street, from Watertown
   Street to 100 feet south of Linwood Avenue." → decomposes exactly like
   grammar 1 (to_offset_feet = 100, to_offset_direction = south); no note
   needed.
6. Landmark endpoints: "to the Brookline town line", "to the street’s end"
   → the phrase after the `to` keyword goes in to_point as written (article
   and curly apostrophe included), offsets empty.

## Normalization rules

- Offset and heading words normalize to compass_point tokens
  (north/south/east/west/northeast/northwest/southeast/southwest):
  "east of" → east; "easterly of" → east ("a point 500 feet easterly of Park
  Street"); "northeasterly 385 feet" → extent_direction = northeast;
  capitalized "South of" → south (no note needed).
- "both directions" → `directions` = `all` (common#direction_set vocabulary:
  a linear zone's two travel directions are all of them). Empty when the
  source states nothing.
- Endpoint phrases are not beautified: keep "the Brookline town line",
  "the street’s end" (curly apostrophe as in source).

## Field placement rules

- **Offsets are always decomposed** into `*_offset_feet` + `*_offset_direction`;
  `from_point`/`to_point` hold only the reference street or landmark, never
  the offset phrase. A segment row geocodes from `street` + the two endpoint
  columns; offsets refine the endpoints.
- `school` is the full name(s) exactly as written, including slash compounds
  ("Oak Hill Middle School/Brown Middle School") — do not split.
- One row per counted entry paragraph; header-only paragraphs yield no row.
- `source_text` is the entry paragraph verbatim (whitespace-collapsed,
  continuation fragments rejoined). Numbered entries keep their `(n)` prefix
  and do NOT prepend the group-header school name — the school lives in the
  `school` column. Inline entries naturally include the `SCHOOL:` prefix.
- `location_detail` exists for qualifiers that fit no structured column; the
  current revision has none, so it should be empty everywhere.
- `notes` is reserved for source-text anomalies; it never carries data.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | from_point | from_off | to_point | to_off | extent | directions | notes |
|---|---|---|---|---|---|---|---|---|
| Angier School: Beacon Street … easterly 575 feet | Beacon Street | Manitoba Road | 25/east | | | east/575 | | |
| (3) Vernon Street … 500 feet easterly of Park Street | Vernon Street | Eldredge Street | | Park Street | 500/east | | all | |
| Brown Middle School: Meadowbrook Road | Meadowbrook Road | | | | | | | |
| (1) Middlesex Road … to the Brookline town line | Middlesex Road | Dunster Road | | the Brookline town line | | | | |
| Education Center: Walnut Street … to 100 feet south of Linwood Avenue | Walnut Street | Watertown Street | | Linwood Avenue | 100/south | | | |
| Horace Mann School: Nevada Street from California Street to Linwood Avenue | Nevada Street | California Street | | Linwood Avenue | | | | |
| (2) Linwood Avenue from Nevada Street to Crafts Street (Horace Mann) | Linwood Avenue | Nevada Street | | Crafts Street | | | | duplicate of (1) in source |
| (2) Prospect Street … to the street’s end | Prospect Street | Washington Street | 50/east | the street’s end | | | | |
| Newton Montessori School: Crescent Avenue, Centre Street to Norwood Avenue | Crescent Avenue | Centre Street | | Norwood Avenue | | | | |
| (1) Grove Street … a point 255 south of Woodland Road | Grove Street | Hancock Street | 80/north | Woodland Road | 255/south | | | unit missing in source ('255 south'); feet per section grammar |
| (2) Beacon Street … west of Beethoven Road a point 150 feet east of Amy Circle | Beacon Street | Beethoven Road | 180/west | Amy Circle | 150/east | | | missing 'to' between endpoints in source; 'Beethoven Road' as written (cf. Beethoven Avenue in (1)) |

(`from_off`/`to_off` abbreviate offset_feet/offset_direction; `extent`
abbreviates extent_direction/extent_length_feet.)

## Source-text quirks

- PDF line-wrap splits several entries across a blank line, and unlike other
  sections the fragments can start **uppercase**: "Parkway.", "Street.",
  "Tyler Terrace." as well as lowercase "directions.", "of Oak Hill Street."
  The colon-aware `entry_start` regex below handles counting (fragments
  contain no colon and no `(n)` prefix); the extractor must rejoin the text
  into the previous entry's `source_text`.
- Horace Mann's numbered entries (1) and (2) are **verbatim duplicates**
  ("Linwood Avenue from Nevada Street to Crafts Street."). Extract both rows
  — the count says 32 and the `(n)` prefix in `source_text` keeps the unique
  constraint satisfied. Flag the duplication in (2)'s `notes`.
- Some entries end with `;` instead of `.` (Little People's (1), Zervas (1))
  — reproduce verbatim in `source_text`.
- "to a point 200 feet South of Prospect Street" — capitalized direction
  mid-sentence; normalize, no note needed.
- The ordinance-history footer is interleaved with stray page-header junk
  ("§", "Zones.", "19-02; …") after the first `(Rev. Ords.` line; region_end
  excludes all of it.

## Proposed common vocabulary

`compass_point` — currently defined inline in `149_school_zones.json` for
`from_offset_direction`, `to_offset_direction`, and `extent_direction`;
should move to `_common.json` when convenient (other segment-based sections —
84, 176, 180 — will need it for the same "a point N feet DIR of X" grammar):

```json
"compass_point": {
  "description": "Compass point for offsets and headings relative to a reference point",
  "enum": ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
}
```

`common#side` does not cover this: it lacks the intercardinals ("225 feet
northeast of Washburn Avenue") and carries parking-only values (odd/even).

## Counting rules (manifest)

```json
{
  "region_start": "established as school zones:",
  "region_end": "\\(Rev\\. Ords\\.",
  "entry_start": "^(\\(\\d+\\)|[A-Z][^:]*:\\s*\\S)"
}
```

An entry is either a numbered paragraph `(n) …` or a `Name: content`
paragraph with text after the colon. Header-only group paragraphs end at the
colon (no trailing content once stripped) and are skipped; continuation
fragments — even capitalized ones — contain no colon and are skipped. The
plain `^[A-Z]` rule used by other sections over-counts here (capitalized
wrap fragments) and under-counts nothing; do not fall back to it.
Verified count: 32 (13 inline + 19 numbered).
