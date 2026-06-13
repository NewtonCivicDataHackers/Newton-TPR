# Section 86 — U-turns

## Source shape

One boilerplate sentence ("No operator shall make a U-turn on the following
streets:"), then the entry list, until the ordinance-history footer beginning
`(Rev. Ords.`. 18 atomic entries as of revision 2025-04-11.

Two paragraph layouts coexist:

- **Simple entries**: one paragraph per street —
  "Brookline Street, both directions, between Oak Hill Street and Hartman Road."
- **Header + numbered sub-entries**: a street-header paragraph ending in a
  colon ("Beacon Street:", "Centre Street:", "Washington Street:") followed by
  `(1)`, `(2)`, … paragraphs, each an atomic entry on that street. Beacon has
  2, Centre has 2, Washington Street has 4.

Header paragraphs are NOT entries; each numbered sub-entry is one row.

## Entry grammars observed

1. `STREET, both directions, between FROM and TO.` — the dominant segment
   form → street, direction = `all`, from_point, to_point.
   - "Derby Street, both directions, between Cherry Street and Edward Road."
2. `(n) both directions, between FROM and TO.` — same fields; `street` comes
   from the preceding header paragraph.
   - "Beacon Street:" + "(1) both directions, between Centre Street and
     Dalton Street."
3. `STREET, between FROM and TO.` — no direction stated → direction empty.
   - "Wheeler Road, between Meadowbrook Road and Voss Terrace."
4. `(n) for DIRECTIONbound vehicles on STREET at CROSS.` — intersection form
   → direction, cross_street; from/to columns empty.
   - "(3) for northbound vehicles on Washington Street at Centre Street."
5. Offset-point endpoints: "Pine Street, both directions, between a point
   225 feet northeast of Washburn Avenue and a point northeasterly 385 feet."
   → offset columns; see gold rows.
6. Trailing `except …` carve-out (Washington Street (1)) → `exception`.

## Normalization rules

- `both directions` → direction = `all` (a two-way street's both travel
  directions; consistent with 96's all-directions convention).
- `for DIRECTIONbound vehicles` → that direction ("for northbound vehicles"
  → `northbound`).
- No direction stated → direction empty. Do not infer `all`.
- **Endpoint anchors drop the leading article**: "the Watertown line" →
  `Watertown line`; "the westerly turnpike bridge at West Newton" →
  `westerly turnpike bridge at West Newton`. Otherwise verbatim — anchors may
  be streets, municipal lines, driveways, or bridges.
- **Offset points decompose**: "a point 225 feet northeast of Washburn
  Avenue" → from_point = `Washburn Avenue`, from_offset_feet = `225`,
  from_offset_direction = `northeast`. "-erly" bearings normalize to the
  8-point compass token ("northeasterly" → `northeast`).
- **Shared possessives distribute**: "between the Newton-Wellesley Hospital's
  west driveway and east driveway" → from_point = `Newton-Wellesley
  Hospital's west driveway`, to_point = `Newton-Wellesley Hospital's east
  driveway` (syntactic distribution, not a guess).
- `exception` drops the leading "except" and de-hyphenates PDF line-wrap
  ("seventy- five" → "seventy-five"); `source_text` keeps the wrap artifact
  verbatim (see quirks).

## Field placement rules

- For numbered sub-entries, `source_text` = header + clause joined with one
  space: "Beacon Street: (1) both directions, between Centre Street and
  Dalton Street." This keeps provenance self-contained and `source_text`
  unique. `street` = the header street without the colon.
- `at CROSS` (intersection form) fills `cross_street`; segment entries leave
  it empty. A row never has both cross_street and from/to columns filled.
- Endpoint phrases stay whole in `from_point`/`to_point` — "westerly
  turnpike bridge at West Newton" is one anchor; do not peel "at West Newton"
  into `location_detail`.
- `exception` carries carve-out data; `notes` never carries data — it is
  reserved for source-text anomalies and ambiguity flags.
- Offset direction columns are set iff the matching offset_feet column is.

## Gold rows for the awkward entries

These exact field values are the settled interpretation; reproduce them
unless the source text itself changes (then update them here):

| source entry (abbrev.) | street | direction | cross_street | from_point | from_off | to_point | to_off | exception | notes |
|---|---|---|---|---|---|---|---|---|---|
| Pine Street … a point 225 feet northeast of Washburn Avenue and a point northeasterly 385 feet | Pine Street | all | | Washburn Avenue | 225 northeast | | 385 northeast | | to-endpoint anchor unstated in source; reads as 385 feet northeasterly beyond the from-point |
| Washington Street (1) … except seventy- five (75) feet … | Washington Street | all | | Chestnut Street | | westerly turnpike bridge at West Newton | | seventy-five (75) feet in front of police headquarters for police and other emergency vehicles | entry split across a blank line in source; 'seventy-five' hyphen-wrapped |
| Washington Street (3) for northbound vehicles … at Centre Street | Washington Street | northbound | Centre Street | | | | | | |
| Washington Street (4) … Hospital's west driveway and east driveway | Washington Street | all | | Newton-Wellesley Hospital's west driveway | | Newton-Wellesley Hospital's east driveway | | | |
| Cypress Street … between Bow Street, and the Bowen School Bus and the Driveway Loop | Cypress Street | all | | Bow Street | | Bowen School Bus and the Driveway Loop | | | endpoint text likely garbled in source (stray comma after Bow Street; reads as one bus-driveway-loop feature) |
| Centre Street (2) … the Watertown line and Washington Street | Centre Street | all | | Watertown line | | Washington Street | | | |
| Wheeler Road, between Meadowbrook Road and Voss Terrace | Wheeler Road | | | Meadowbrook Road | | Voss Terrace | | | |

(from_off/to_off abbreviate the offset_feet + offset_direction column pairs.)

## Source-text quirks

- **Washington Street (1) splits across a blank line** mid-word: the
  paragraph ends "except seventy-" and the lowercase fragment "five (75)
  feet in front of police headquarters…" follows after a blank line. Rejoin
  with a single space in `source_text` (yielding "seventy- five (75) feet" —
  verbatim whitespace-collapse, no de-hyphenation there); the `exception`
  column gets the clean de-hyphenated reading. The fragment starts lowercase
  so the counting rules skip it.
- **Pine Street wraps without a blank line** ("northeasterly" / "385 feet.");
  split_paragraphs already joins it — one paragraph, one entry.
- **Curly apostrophe** in "Newton-Wellesley Hospital’s" (U+2019): keep it
  verbatim in `source_text` and in the from/to anchors.
- The Cypress Street endpoint text is garbled (see gold row); reproduce it
  verbatim in `source_text` and flag in `notes`.
- Two near-duplicate Watertown Street entries exist (Albemarle–Edinboro with
  "both directions", Hawthorn–Pearl without); both are real entries, not
  artifacts.

## Counting rules (manifest)

```json
{"region_start": "U-turn on the following streets:", "region_end": "\\(Rev\\. Ords\\.", "entry_start": "^(\\(\\d+\\)|[A-Z]).*[^:]$"}
```

`entry_start` counts numbered sub-entries (`(1)`, `(2)`, …) and
uppercase-starting simple entries, while skipping the three street-header
paragraphs (they end with a colon, rejected by `[^:]$`) and the lowercase
"five (75) feet…" continuation fragment. Verified: 18 entries as of
revision 2025-04-11.

## Proposed common vocabulary

`compass_point` — 8-point compass bearing for offset/bearing fields:
`["north", "south", "east", "west", "northeast", "northwest", "southeast",
"southwest"]`. Used here inline by `from_offset_direction` and
`to_offset_direction`. Distinct from `common#direction` (travel-bound
"-bound" tokens) and `common#side` (no intercardinals; includes
both/odd/even). Other sections with "at a point N feet DIRECTION of X"
grammars (e.g. 148, 176, 180) will want the same def — promote to
`_common.json` as `compass_point` when a coordinated edit is possible.
