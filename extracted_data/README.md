# Newton TPR Extracted Data

<!-- GENERATED FILE — do not edit. -->
<!-- Regenerate with: python3 .claude/skills/tpr-extract/scripts/gen_readme.py -->

Structured TSV datasets extracted from the Newton Traffic and Parking Regulations section text in [sections/](../sections/). The extraction contract — schemas, vocabulary, per-section specs, and validation — lives in the `tpr-extract` skill at `.claude/skills/tpr-extract/`.

- **TPR revision**: 2026-01-16
- **Format**: TSV (tab-separated, UTF-8, no quoting); every row carries a verbatim `source_text` provenance column

## Datasets

### 85 — One-way streets

[85_one_way_streets.tsv](85_one_way_streets.tsv) — 110 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way the one-way restriction applies to; for numbered sub-entries, the street named in the group-header paragraph (required) |
| `roadway` | Carriageway or portion designator from the source (e.g. 'North Drive', 'Southern roadway', 'east roadway', 'loop portion', 'north fork', 'crossover'); empty when the restriction covers the whole street |
| `direction` | Direction(s) of travel, only when the source states one explicitly ('-erly' adverbs normalize to '-bound'; 'counterclockwise direction' to 'counterclockwise'; 'X and Y' to a comma-joined set); empty when the from/to order alone carries the direction — never inferred from street geography. Inline pattern is common#direction_set plus 'counterclockwise' (see spec, Proposed common vocabulary) |
| `from_point` | Named street, municipal line, or feature where the one-way segment begins (leading articles dropped); when the source says 'a point N feet DIR of X', the anchor X alone — the offset goes in from_offset_feet/from_offset_direction. Qualifier words like 'near' or 'opposite' stay in the cell verbatim. Empty when the entry names no start point |
| `from_offset_feet` | Distance in feet from from_point to the actual segment start, when the source gives 'a point N feet DIR of X'; numerals win over spelled-out numbers |
| `from_offset_direction` | Compass bearing of the offset from from_point (the DIR in 'a point N feet DIR of X'). Inline enum; proposed for _common.json as compass_point (see spec) (vocabulary: `compass_point`) |
| `to_point` | Named street, municipal line, or feature where the one-way segment ends, same conventions as from_point; empty when the entry names no end point (e.g. an extent given as a length, or a whole-street entry) |
| `to_offset_feet` | Distance in feet from to_point to the actual segment end, when the source gives 'a point N feet DIR of X' |
| `to_offset_direction` | Compass bearing of the offset from to_point. Same inline enum as from_offset_direction (vocabulary: `compass_point`) |
| `length_feet` | Stated length of the one-way segment in feet, when the source gives an extent instead of (or in addition to) a second endpoint (e.g. 'two hundred fifteen (215) feet westerly', 'continuing 50 feet') |
| `exception` | Vehicles exempted from the one-way restriction, without the leading 'except' (e.g. 'non-motorized vehicles'); empty when the restriction applies to all vehicular traffic |
| `location_detail` | Positional or portion qualifier from the source that is not a segment endpoint (e.g. 'at Kenrick Park', 'on the southwest leg', 'on that part of Centre Street known as Centre Green', 'Ward 3', 'bridge over Turnpike', 'at triangle') |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 86 — U-turns

[86_u_turns_prohibited.tsv](86_u_turns_prohibited.tsv) — 18 rows

| Column | Description |
|--------|-------------|
| `street` | Street on which U-turns are prohibited; for numbered sub-entries, the street named in the header paragraph (required) |
| `direction` | Direction(s) of travel the prohibition applies to; 'all' for 'both directions'; empty when the source states none (vocabulary: `direction_set`) |
| `cross_street` | Intersecting street for at-intersection prohibitions ('on STREET at CROSS'); empty for segment entries |
| `from_point` | Segment start anchor: street, municipal line, driveway, bridge, or other named feature as written, leading article dropped; empty for intersection entries or when the source leaves the anchor unstated |
| `from_offset_feet` | Distance in feet from from_point to the actual segment start, when the source defines the start as an offset point; empty when the start is at from_point itself |
| `from_offset_direction` | Compass bearing of the from-offset, 8-point compass ('northeasterly' normalizes to northeast); empty unless from_offset_feet is set (vocabulary: `compass_point`) |
| `to_point` | Segment end anchor, same form as from_point; empty for intersection entries or when the source leaves the anchor unstated |
| `to_offset_feet` | Distance in feet from to_point (or, when to_point is empty, from the segment start) to the actual segment end |
| `to_offset_direction` | Compass bearing of the to-offset, 8-point compass ('northeasterly' normalizes to northeast); empty unless to_offset_feet is set (vocabulary: `compass_point`) |
| `exception` | Carve-out clause without the leading 'except', whitespace-collapsed and de-hyphenated (e.g. 'seventy-five (75) feet in front of police headquarters for police and other emergency vehicles') |
| `location_detail` | Positional qualifier attached to the street itself that fits no other column; endpoint phrases stay whole in from_point/to_point and never go here |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 87 — Left turns prohibited

[87_left_turns_prohibited.tsv](87_left_turns_prohibited.tsv) — 40 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way the turning traffic is on; may be a named driveway or parking-lot way (e.g. 'Peirce Elementary School Parking Lot', 'Williams School driveway') (required) |
| `direction` | Approach direction of travel on `street`; empty when the source states none. Normalize 'easterly'/'northerly' etc. to the vocabulary; 'for Xbound vehicles' supplies X (vocabulary: `direction`) |
| `cross_street` | Named street or way the prohibited left turn would enter ('onto X'), or the street at which the turn is prohibited in the restatement grammar ('at X'). Named streets/ways only — driveways and parking facilities go in `destination`. Carriageway designations stay intact (e.g. 'Commonwealth Avenue, North Drive') |
| `cross_street_direction` | Direction of travel onto the receiving street when the source states one, whether inline ('onto Watertown Street eastbound') or trailing ('onto Waltham Street, eastbound.'); empty when not stated (vocabulary: `direction`) |
| `destination` | Non-street destination the prohibited turn would enter ('into X'): a driveway, parking area, or parking lot, as named in the source with leading article dropped (e.g. 'driveway of 1900 Commonwealth Avenue', 'Newton Centre municipal parking area'); empty when the turn target is a named street |
| `days` | Days the prohibition applies; empty means at all times (or see schedule_detail) (vocabulary: `days`) |
| `times` | Time window(s) the prohibition applies; empty means at all times (or see schedule_detail) (vocabulary: `time_ranges`) |
| `schedule_detail` | Compound schedule with different times on different days, which one days+times pair cannot express. Semicolon-joined clauses of 'DAYS TIMES' using the common day tokens and 24-hour ranges. When used, days and times stay empty |
| `exceptions` | Vehicles exempt from the prohibition, lowercase without parentheses (e.g. 'bicycles' from '(except bicycles)') |
| `location_detail` | Positional qualifier from the source (e.g. 'opposite Elm Street', 'eastern leg', 'at the entrance to the Massachusetts Turnpike', 'at the southernmost intersection of Nahanton Street and Dedham Street') |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 88 — Right turn only

[88_right_turn_only.tsv](88_right_turn_only.tsv) — 13 rows

| Column | Description |
|--------|-------------|
| `street` | Street, drive, or way the turning traffic approaches on; the intersection geocodes from street + cross_street (required) |
| `direction` | Direction of travel on street that must turn right; empty when the source states none (vocabulary: `direction`) |
| `cross_street` | Street or way onto which the right turn must be made (the 'onto' target) (required) |
| `location_detail` | Positional or approach qualifier from the source (e.g. 'at 629 Commonwealth Avenue', 'from municipal parking area') |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 89 — Right turns prohibited

[89_right_turns_prohibited.tsv](89_right_turns_prohibited.tsv) — 22 rows

| Column | Description |
|--------|-------------|
| `street` | Street, way, or facility the restricted traffic is on; the first-named way exactly as listed (whitespace-collapsed, not beautified); carriageway designations like ', South Drive' stay in the name (required) |
| `direction` | Direction of travel the prohibition applies to; 'southerly' normalizes to southbound (see spec); empty when the source states none (vocabulary: `direction`) |
| `cross_street` | Street, way, or facility onto/into which the right turn is prohibited; leading article 'the' dropped; leg qualifiers (e.g. 'eastern leg') go to location_detail. Every entry as of revision 2026-01-16 names a target, so an empty cell signals a parse problem |
| `days` | Days the prohibition applies; empty means every day. Semicolon separates paired schedule groups: the i-th days group pairs with the i-th times group (see spec, Beacon Street gold row) (vocabulary: `days`) |
| `times` | Time window(s) the prohibition applies; empty means at all times. Semicolon separates paired schedule groups: the i-th times group pairs with the i-th days group (see spec, Beacon Street gold row) (vocabulary: `time_ranges`) |
| `exemption` | Vehicle class exempt from the prohibition, lowercase without 'except' or parentheses (e.g. 'bicycles'); empty when none |
| `location_detail` | Approach or leg qualifier from the source (e.g. 'eastern leg', 'from driveway of 2 Newton Place (255 Washington Street)') |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 90 — Vehicle Restrictions on Public Ways., the following prohibitions apply:

[90_vehicle_restrictions.tsv](90_vehicle_restrictions.tsv) — 5 rows

| Column | Description |
|--------|-------------|
| `street` | Public way the restriction applies to (the entry's leading label, which matches the street named after 'shall go upon'/'shall enter') (required) |
| `direction` | Direction of prohibited travel or entry ('in the easterly direction' -> eastbound); empty when the source states none (vocabulary: `direction`) |
| `from_point` | Cross street or landmark where the restricted segment begins; empty when the restriction covers the entire way |
| `to_point` | Cross street or landmark where the restricted segment ends; empty when the segment is open-ended or the restriction covers the entire way |
| `restriction` | Prohibited act: 'travel' when the source says 'shall go upon' (no traveling on the way), 'entry' when it says 'shall enter' (no entering the way) (required) |
| `vehicle_type` | Class of vehicle restricted; 'all' for 'No vehicle of any description' (currently every entry) (required) |
| `exemptions` | Exempt parties from the 'except those of ...' clause, verbatim minus the leading 'those of' and the trailing comma; empty when the prohibition is unconditional |
| `days` | Days the restriction applies; 'school days' and 'when public schools of the city are in session' both normalize to school_days; empty means every day (vocabulary: `days`) |
| `times` | Time window(s) the restriction applies; empty means at all times (vocabulary: `time_ranges`) |
| `location_detail` | Relational segment qualifier from the source (e.g. 'east of Bridges Avenue'), preserving which side of from_point the restriction covers |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 95 — Thruways

[95_thruways.tsv](95_thruways.tsv) — 4 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way designated a thruway under M.G.L. c. 89 s. 9 (required) |
| `from_point` | Segment start point: a cross street or municipal boundary line, article-stripped (e.g. 'Newton-Boston line', 'Winchester Street'); kept in source order, never reordered (required) |
| `to_point` | Segment end point: a cross street or municipal boundary line, article-stripped (e.g. 'Newton-Wellesley line'); kept in source order, never reordered (required) |
| `excluded_intersection` | Cross street whose intersection is carved out of the designation ('... not including the intersection, then, beginning again at the ... limits of such intersection ...'); empty when the segment is continuous |
| `remark` | Trailing source sentence(s) qualifying the designation (e.g. the state-highway jurisdiction note), verbatim and whitespace-collapsed; source content only, never extractor commentary |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 96 — No Turn on Red signs

[96_no_turn_on_red.tsv](96_no_turn_on_red.tsv) — 76 rows

| Column | Description |
|--------|-------------|
| `street` | Street or approach the restricted traffic is on; for intersection-wide entries, the full multi-street designation as written (whitespace-collapsed, not beautified) (required) |
| `direction` | Direction(s) of travel the restriction applies to; 'all' for all-directions/all-approaches entries; empty when the source states none (vocabulary: `direction_set`) |
| `cross_street` | Street at/onto/towards which the turn is prohibited; empty for intersection-wide entries or when not stated |
| `turn` | Which turn is prohibited on red (required) |
| `lane_detail` | Lane qualifier from the source (e.g. 'left two lanes', 'far left two lanes', 'left and center lane') |
| `condition` | Operating condition of the sign, lowercase without parentheses (e.g. 'when illuminated') |
| `days` | Days the restriction applies; empty means at all times (vocabulary: `days`) |
| `times` | Time window(s) the restriction applies; empty means at all times (vocabulary: `time_ranges`) |
| `location_detail` | Positional qualifier from the source (e.g. 'at exit 125', 'opposite Elm Street', 'in Newton Corner') |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 97 — Left lane must turn left

[97_left_lane_must_turn_left.tsv](97_left_lane_must_turn_left.tsv) — 79 rows

| Column | Description |
|--------|-------------|
| `street` | Street or approach the left-lane traffic is on; for multi-street designations, the full phrase as written (whitespace-collapsed, not beautified, e.g. 'Winchester and Centre Streets', 'Commonwealth Avenue, North Drive') (required) |
| `direction` | Direction(s) of travel the requirement applies to; 'all' for all-directions entries; empty when the source states none (every entry as of 2025-04-11 states one) (vocabulary: `direction_set`) |
| `cross_street` | Named street or way (street, avenue, parkway, on-ramp, named driveway) onto/at which the left turn is made; multi-target entries keep the conjunction verbatim ('Wachusett Road or Hammond Street'); empty when the target is a property/lot/address (see destination) |
| `cross_street_direction` | Carriageway direction of the target street when the source states a bare direction immediately after the cross street name ('onto Winchester Street southbound'); directions embedded in ramp designations stay in cross_street ('Route 9 eastbound on-ramp') (vocabulary: `direction`) |
| `destination` | Non-way turn target: property address, parking lot, or driveway-of-address introduced by 'into', or a street address following 'at' (e.g. '267-287 Grove Street', 'Trio Parking Lot', 'Driveway of 2150 Washington Street', '233 Needham Street'); empty when the target is a named street/way (see cross_street) |
| `lane_detail` | Lane qualifier from the source (e.g. '2 left lanes', 'two lanes'); empty when only the section-wide left lane(s) rule applies |
| `location_detail` | Positional or movement qualifier from the source (e.g. 'opposite Elm Street', 'on Washington Street Bridge over Mass. Turnpike', 'between Washington St and Foster St', 'continuing onto Washington Street'); multiple distinct qualifiers joined with '; ' in source order |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 98 — Right lane must turn right

[98_right_lane_must_turn_right.tsv](98_right_lane_must_turn_right.tsv) — 25 rows

| Column | Description |
|--------|-------------|
| `street` | Street the right-lane traffic is on (the approach street) (required) |
| `direction` | Direction of travel on the approach street; every entry in this section states exactly one (required; vocabulary: `direction`) |
| `cross_street` | Street or way onto/at which the right turn must be made; compound targets keep the conjunction as written ('Day Street and Fuller Street') (required) |
| `onto_direction` | Direction of travel on the cross street after the turn, when the source states one (e.g. 'onto Nahanton Street westbound'); empty otherwise (vocabulary: `direction`) |
| `location_detail` | Positional or movement qualifier from the source (e.g. 'at the southernmost intersection of Nahanton Street and Dedham Street', 'continuing onto Washington Street; opposite Elm Street'); multiple qualifiers joined with '; ' in source order |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 99 — Through travel prohibited

[99_through_travel_prohibited.tsv](99_through_travel_prohibited.tsv) — 11 rows

| Column | Description |
|--------|-------------|
| `street` | Street the restricted traffic approaches on, name only — leg/drive qualifiers like 'eastern leg' go in location_detail, but named carriageways ('Commonwealth Avenue, North Drive') stay whole (required) |
| `direction` | Direction of travel the prohibition applies to; empty when the source states none (vocabulary: `direction`) |
| `cross_street` | Street being crossed or at which the prohibition applies ('crossing X', 'at X'); empty when the source states none |
| `onto_street` | Street the prohibited through movement would continue onto ('onto X', 'continuing onto X'); often the same name as street — keep it anyway, that repetition is the through movement; empty when the source states none |
| `location_detail` | Leg or positional qualifier from the source (e.g. 'eastern leg') |
| `exception` | Exempted traffic, lowercase, without parentheses or the word 'except' (e.g. 'bicycles'); empty when no exemption |
| `days` | Days of the first (or only) schedule; empty (with times empty) means at all times (vocabulary: `days`) |
| `times` | Time window(s) of the first (or only) schedule; empty means at all times (vocabulary: `time_ranges`) |
| `days_2` | Days of a second schedule when the source states a distinct day set with its own times; empty otherwise (vocabulary: `days`) |
| `times_2` | Time window(s) paired with days_2; empty when there is no second schedule (vocabulary: `time_ranges`) |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 145 — Traffic-control signal locations

[145_traffic_control_signals.tsv](145_traffic_control_signals.tsv) — 124 rows

| Column | Description |
|--------|-------------|
| `street` | First-named street or way of the signalized location, exactly as written (whitespace-collapsed); ramp and carriageway designations stay whole (e.g. 'Boylston Street (Route 9) eastbound onramp and offramp') (required) |
| `cross_street` | Second-named street or way of the intersection; named driveways and ramp designations count as ways; empty for midblock, segment, and landmark entries |
| `additional_streets` | Third and subsequent streets/ways of a multi-leg intersection, joined with '; ' in source order (semicolon because way names may contain commas); empty when the intersection has only two legs |
| `signal_type` | Kind of device: subsections (a) and (c) are traffic_signal, subsection (b) is pedestrian_hybrid_beacon (required) |
| `direction` | Direction of travel the signal installation is designated for, when the entry states one as a standalone qualifier (e.g. 'Washington Street at Centre Avenue, eastbound.'); NOT filled from direction words embedded in ramp/carriageway names (vocabulary: `direction`) |
| `from_point` | Reference street for proximity and offset entries ('near X', 'N feet DIRECTION of X') or segment start for 'between X and Y' entries; empty for plain intersection entries |
| `to_point` | Segment end for 'between X and Y' entries; empty otherwise |
| `offset_feet` | Distance in feet from from_point when the source gives one (e.g. '70 feet east of Lawrence Avenue'); empty for 'near' entries with no stated distance |
| `offset_direction` | Compass direction of the offset from from_point (proposed common vocabulary: compass_point) (vocabulary: `compass_point`) |
| `owner` | Owning/operating jurisdiction when the source states one: 'state' for subsection (c) entries, 'shared with City of Boston' for the Commonwealth Avenue/Fr. Herlihy/Lake Street parenthetical; empty means not stated (city-maintained by default) |
| `location_detail` | Landmark or positional qualifier from the source that is not a named way (e.g. 'at Burr School', 'at the Fire Department Headquarters', 'at the staircase to the Waban train station') |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed, line-wrap fragments rejoined; the two subsection (c) entries that duplicate subsection (a) entries verbatim are prefixed '(c) ' to keep this column unique (see spec) (required; vocabulary: `source_text`) |

### 146 — Flashing warning light locations

[146_flashing_warning_lights.tsv](146_flashing_warning_lights.tsv) — 63 rows

| Column | Description |
|--------|-------------|
| `street` | Street on which the flashing warning light is located, as written in the source (suspected typos kept verbatim and flagged in notes) (required) |
| `direction` | Direction of travel the light governs; empty when the source states none (most entries) (vocabulary: `direction`) |
| `cross_street` | Named public street/way locating the light: the 'at'/'and' street for intersection entries, or the reference way for offset entries; slash-joined dual designations kept as written; empty when the reference is a landmark |
| `landmark` | Non-street reference feature anchoring the location (park, greenway, driveway, parking area, town line), leading article 'the' dropped; empty when the reference is a named street |
| `offset_feet` | Distance in feet from the reference point, for 'N feet DIRECTION of REF' entries; empty for plain intersection entries |
| `offset_direction` | Compass bearing of the offset from the reference point; set iff offset_feet is set (vocabulary: `compass_point`) |
| `signal_type` | Type of flashing device from the trailing descriptor: rrfb (rectangular rapid flashing beacon), flashing_yellow, or flashing_red; empty when the source states none |
| `pedestrian_activated` | 'yes' when the source says the device is pedestrian activated; empty when activation is not stated |
| `location_detail` | Positional qualifier from the source not captured by the other columns (e.g. 'eastern leg', 'between the entrance and exit'); never carries the signal descriptor |
| `notes` | Extractor remarks about anomalies in the source text (suspected typos, missing signal type); never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 147 — Obedience to isolated stop signs

[147_stop_signs.tsv](147_stop_signs.tsv) — 989 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way carrying the stop-controlled traffic (the first-named street); for intersection-wide multi-street entries, the full multi-street designation as written (whitespace-collapsed, not beautified) (required) |
| `direction` | Direction(s) of travel that must stop; 'all' for all-directions entries; empty when the source states none (vocabulary: `direction_set`) |
| `cross_street` | Street or way being entered (the second-named street, including named ramps and carriageways); empty for intersection-wide entries, unnamed targets (connector spurs, triangles), or midblock point designations |
| `offset_feet` | Distance in feet of the stop point from offset_from, when the source locates the sign by a measured offset; filled together with offset_direction and offset_from |
| `offset_direction` | Compass point of the offset measured from offset_from (proposed common#compass_point; defined inline pending adoption in _common.json) (vocabulary: `compass_point`) |
| `offset_from` | Street the offset is measured from; may differ from cross_street (e.g. '97 feet east of Centre Street'); filled together with offset_feet and offset_direction |
| `location_detail` | Lane, ramp, island, roadway, approach, ward, or position qualifier from the source (e.g. 'from right turn lane', 'southern roadway', 'Ward 5', 'northern intersection', 'east end'); multiple qualifiers joined with '; ' in source order |
| `notes` | Extractor remarks about anomalies in the source text (merged paragraphs, unclosed parentheses, nonstandard wording); never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 148 — Obedience to yield signs

[148_yield_signs.tsv](148_yield_signs.tsv) — 32 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way on which traffic must yield (required) |
| `direction` | Direction of travel governed by the sign; empty when the source does not state one (vocabulary: `direction`) |
| `yields_to` | Street or way being entered; empty when the source text does not state it unambiguously |
| `location_detail` | Lane, island, or position qualifier from the source (e.g. 'from right turn lane', 'at the channelized traffic island') |
| `notes` | Extractor remarks about anomalies in the source text |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 149 — School zones

[149_school_zones.tsv](149_school_zones.tsv) — 32 rows

| Column | Description |
|--------|-------------|
| `school` | School(s) the zone serves, exactly as written including slash compounds (e.g. 'Bigelow Middle School/Underwood School'); numbered entries inherit it from their group-header paragraph (required) |
| `street` | Street the school zone lies on (required) |
| `from_point` | Reference street or landmark designating the segment start, as written after 'from' minus any offset phrase (e.g. 'Park Street', 'the Brookline town line'); empty for whole-street zones |
| `from_offset_feet` | Offset in feet from from_point to the actual segment start ('a point 112 feet south of Arlington Street' -> 112); empty when the segment starts at from_point itself |
| `from_offset_direction` | Compass point of the start offset relative to from_point ('25 feet east of Manitoba Road' -> east); normalized per spec ('easterly' -> east) (vocabulary: `compass_point`) |
| `to_point` | Reference street or landmark designating the segment end, as written after 'to' minus any offset phrase (e.g. 'Elmwood Street', 'the street’s end'); empty for whole-street zones and extent-grammar entries |
| `to_offset_feet` | Offset in feet from to_point to the actual segment end; empty when the segment ends at to_point itself |
| `to_offset_direction` | Compass point of the end offset relative to to_point; normalized per spec (vocabulary: `compass_point`) |
| `extent_direction` | Heading along the street for extent-grammar entries ('easterly 575 feet' -> east, 'northeasterly' -> northeast); empty for endpoint-to-endpoint segments (vocabulary: `compass_point`) |
| `extent_length_feet` | Zone length in feet for extent-grammar entries ('easterly 575 feet' -> 575); empty for endpoint-to-endpoint segments |
| `directions` | Travel directions the zone applies to; 'both directions' normalizes to 'all'; empty when the source states none (vocabulary: `direction_set`) |
| `location_detail` | Positional qualifier that fits no structured column; empty in the current revision — never carries data a structured column provides |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim entry paragraph, whitespace-collapsed, continuation fragments rejoined; numbered entries keep their '(n)' prefix and do NOT prepend the group-header school name (required; vocabulary: `source_text`) |

### 150 — Safety Zones

[150_safety_zones.tsv](150_safety_zones.tsv) — 17 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way on which the safety zone lies (required) |
| `extent` | 'entire_street' when the entry is a bare street name with no endpoints; 'segment' when the zone is bounded (required) |
| `from_point` | Street or way at (or measured from) which the segment begins; empty only for entire_street rows |
| `from_offset_feet` | Offset in feet from from_point to the actual segment start, from 'a point N feet DIR of X'; empty when the segment begins at from_point itself |
| `from_offset_direction` | Compass bearing of the offset from from_point; present iff from_offset_feet is present. Inline enum pending a common#compass_point def (see spec, Proposed common vocabulary) |
| `to_point` | Street or way at (or measured from) which the segment ends; empty only for entire_street rows |
| `to_offset_feet` | Offset in feet from to_point to the actual segment end, from 'a point N feet DIR of Y'; empty when the segment ends at to_point itself |
| `to_offset_direction` | Compass bearing of the offset from to_point; present iff to_offset_feet is present. Inline enum pending a common#compass_point def (see spec, Proposed common vocabulary) |
| `location_detail` | Positional qualifier from the source that does not decompose into the endpoint columns; empty for every entry as of revision 2025-04-11 |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 172 — Loading zones

[172_loading_zones.tsv](172_loading_zones.tsv) — 19 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way on which the loading zone lies (required) |
| `side` | Side of street the zone occupies; '-erly' source forms normalize to compass points ('southeasterly side' -> southeast); empty when the source states none. Extends common#side with intercardinal values pending their addition to _common.json (vocabulary: `side`) |
| `from_point` | Named street or way anchoring the start of the zone (the X in 'from X' or 'from a point N feet DIR of X'); holds only the street name, never offset text (required) |
| `from_offset_feet` | Distance in feet from from_point to where the zone begins; empty when the zone begins at from_point itself |
| `from_offset_direction` | Compass direction from from_point to the zone's start ('140 feet south of Beacon Street' -> south); empty when there is no offset. Proposed common#compass_point vocabulary, defined inline pending its addition to _common.json (vocabulary: `compass_point`) |
| `extent_direction` | Compass direction the zone runs from its start point; '-erly' source forms normalize ('southerly' -> south, 'northeasterly' -> northeast); empty for from/to endpoint entries. Proposed common#compass_point vocabulary, defined inline pending its addition to _common.json (vocabulary: `compass_point`) |
| `length_feet` | Length of the zone in feet along extent_direction; empty for from/to endpoint entries |
| `to_point` | Named street or way ending the zone, only for 'from X to Y' entries; empty when the extent is given as direction + length |
| `time_limit_minutes` | Loading time limit in minutes: 30 for entries under paragraph (a), 10 for entries under paragraph (b) (required) |
| `location_detail` | Positional qualifier from the source not captured by the segment atoms (e.g. 'at the existing crosswalk', 'west drive of the Walnut Hill School') |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 179 — School drop off zones

[179_school_drop_off_zones.tsv](179_school_drop_off_zones.tsv) — 30 rows

| Column | Description |
|--------|-------------|
| `street` | Street or way the drop off zone is on; for grouped entries, taken from the parent street-header paragraph (required) |
| `side` | Side of the street the zone occupies; every entry in this section states one (required; vocabulary: `side`) |
| `from_point` | Cross street, way, or landmark from which the zone's start is measured or at which it begins (e.g. 'Beacon Street', 'Pearl Street', 'the driveway of 125 Wells Avenue'); empty for whole-side designations |
| `from_offset_feet` | Distance in feet from from_point to the zone's start, measured along from_offset_direction; empty when the zone begins at from_point itself |
| `from_offset_direction` | Compass direction from from_point to the zone's start ('a point 275 feet south of Beacon Street' -> south). Proposed for _common.json as compass_point; inlined here because _common.json may not be edited concurrently (vocabulary: `compass_point`) |
| `extent_direction` | Compass direction the zone runs from its start point; '-erly' adverbs normalize to compass points ('southerly 275 feet' -> south). Same proposed compass_point vocabulary as from_offset_direction (vocabulary: `compass_point`) |
| `length_feet` | Running length of the zone in feet, when the source states the extent as a distance; empty when the extent is given only as an endpoint |
| `to_point` | Cross street, way, or landmark at or near which the zone ends ('to Fellsmere Road' -> 'Fellsmere Road'; 'to the intersection of Dedham Street and Walnut Street' -> 'Walnut Street'); empty when the extent is given only as a length |
| `to_offset_feet` | Distance in feet from to_point to the zone's end, measured along to_offset_direction; empty when the zone ends at to_point itself |
| `to_offset_direction` | Compass direction from to_point to the zone's end ('to a point 110 feet south of Minot Place' -> south). Same proposed compass_point vocabulary as from_offset_direction (vocabulary: `compass_point`) |
| `location_detail` | Segment or position qualifier that cannot be decomposed into the structured columns (e.g. Nevada Street's 'to a point 190 feet southerly'); never invented, never duplicated from structured columns |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; for grouped sub-entries, prefixed with the parent street header (and side sub-header, if any) in document order; wrapped fragments rejoined (required; vocabulary: `source_text`) |

### 199 — Fire Lanes

[199_fire_lanes.tsv](199_fire_lanes.tsv) — 12 rows

| Column | Description |
|--------|-------------|
| `street` | Public street the fire lane is on or that the host property fronts on; always a bare street name, never with a house number (required) |
| `street_number` | House number or number range from the entry heading, digits and hyphen only (e.g. '740', '31-49'); empty for entries on public ways or properties identified only by name |
| `property_name` | Named property, business, or facility hosting the fire lane, verbatim as written including parentheticals (e.g. 'Crystal Lake Bathhouse Parking Lot', 'Heartland Plaza (Stop & Shop on Watertown Street)'); empty when the entry names only an address or public way |
| `lane_type` | Kind of way designated: 'street' when the fire lane is the named public way itself; otherwise the facility noun from the source (required) |
| `side` | Side of the designated way the fire lane occupies — street side for public-way entries ('both sides'), or side of a driveway ('The east side of the driveway') (vocabulary: `side`) |
| `from_point` | Segment start point as stated, leading article stripped; a street name for public-way entries, possibly a non-street anchor (sidewalk, city line) for property entries |
| `to_point` | Segment end point as stated, leading article stripped; empty when the extent is given as direction + length instead |
| `extent_direction` | Compass bearing the segment extends from from_point, in '-erly' form; proposed common#bearing (see spec) |
| `length_feet` | Stated segment length in feet (source marks feet with a curly apostrophe, e.g. 60’); all lengths in this section are prefixed 'approximately' — the qualifier is implied and not recorded |
| `location_detail` | Positional qualifier from the source, kept whole even when its object repeats a captured field (e.g. 'in front of the Marshall's Mall', 'between the marked parking areas and immediately in front of the YMCA building', 'to the left of two accessible parking spaces') |
| `notes` | Extractor remarks about anomalies or interpretation flags in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 200 — Accessible Parking Spaces

[200_accessible_parking_spaces.tsv](200_accessible_parking_spaces.tsv) — 87 rows

| Column | Description |
|--------|-------------|
| `street` | Street the space is on — the designation header before the colon/comma, as written (including parenthetical village qualifiers like 'North Street (Newtonville)' and carriageway designations like 'Commonwealth Avenue, South Drive') (required) |
| `side` | Side of street the space is on; inline enum extends common#side with intercardinal values ('southeast side', 'northeast side' appear in this section) — see spec's Proposed common vocabulary |
| `cross_street` | Reference street or way from which offsets are measured, or the cross street of a corner entry; only named streets/ways, as written; empty for frontage and landmark-only entries |
| `offset_feet` | Distance in feet from cross_street to the (start) point of the space ('220 feet from Centre Street', 'from a point 290’ east of Oak Street'); feet symbol ’ normalizes to the bare integer |
| `offset_direction` | Compass bearing from cross_street to the measured point(s) ('185 feet north of Watertown Street' → north); empty when the source gives none ('220 feet from Centre Street'); inline compass-point enum — see spec's Proposed common vocabulary (vocabulary: `compass_point`) |
| `to_offset_feet` | End-point offset in feet for two-point segments ('from a point 185 feet north of Watertown Street to a point 390 feet north of Watertown Street'); shares cross_street and offset_direction with offset_feet; empty for single-point entries |
| `length_feet` | Stated linear extent of the space(s) in feet ('westerly 20 feet', '20 feet easterly', '20’ easterly'); empty for two-point segments, point-only entries, and 'to end' extents |
| `extent_direction` | Compass bearing the space extends from the start point ('westerly' → west, 'northerly to end' → north); same inline compass-point enum as offset_direction (vocabulary: `compass_point`) |
| `spaces` | Number of designated spaces when the source states one ('(6 spaces)' → 6, 'Two spaces' → 2, 'Three (3) accessible parking spaces' → 3, 'one accessible space' → 1); empty when unstated (a single space is implied but never recorded) |
| `address_number` | House number(s) the space fronts, digits as written without the '#' ('16', '18-20', '38 or 42'); only when the address is on the same street as `street` — numbers on other streets stay in location_detail |
| `location_detail` | Positional qualifiers that are not offsets: carriageway ('eastern roadway', 'south Drive'), landmark phrases ('opposite Auburndale Brach library', 'just to the west of the ramp'), corner designations ('NW corner'), open-ended extents ('to end'); multiple distinct qualifiers joined with '; ' in source order |
| `notes` | Extractor remarks about anomalies in the source text (typos, stray characters, ambiguity flags); never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 201 — Overnight on-street angle parking areas

[201_overnight_angle_parking.tsv](201_overnight_angle_parking.tsv) — 1 rows

| Column | Description |
|--------|-------------|
| `street` | Street with the designated angle-parking area (required) |
| `from_point` | Start of the segment |
| `to_point` | End of the segment |
| `spaces` | Maximum number of designated spaces |
| `notes` | Extractor remarks about source anomalies; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 202 — Resident restricted areas

[202_resident_restricted_areas.tsv](202_resident_restricted_areas.tsv) — 28 rows

| Column | Description |
|--------|-------------|
| `street` | Street (or slash-joined street pair) the resident restriction applies to (required) |
| `locality` | Village/neighborhood qualifier given in the source (e.g. 'Newton Upper Falls', 'Waban'); empty if none |
| `side` | Side of street; empty when not stated (vocabulary: `side`) |
| `from_point` | Reference street/landmark at the start of the segment |
| `from_offset_feet` | Distance from from_point, in feet |
| `from_offset_direction` | Compass direction of the from_point offset (vocabulary: `compass_point`) |
| `to_point` | Reference street/landmark at the end of the segment; 'end' for the street's end |
| `to_offset_feet` | Distance from to_point, in feet |
| `to_offset_direction` | Compass direction of the to_point offset (vocabulary: `compass_point`) |
| `extent` | 'entire length' when the restriction covers the whole street; empty otherwise |
| `times` | Time window when the restriction applies; empty means at all times (vocabulary: `time_range`) |
| `notes` | Sub-clause detail (e.g. drive/reservation qualifiers) or administrative provisions that are not a single mappable segment |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 219 — Parking prohibitions in areas that previously allowed parking

[219_removed_parking_spaces.tsv](219_removed_parking_spaces.tsv) — 2 rows

| Column | Description |
|--------|-------------|
| `street` | Street on which the removed parking space was located (required) |
| `side` | Side of the street the space was on; empty when the source does not state one (vocabulary: `side`) |
| `within_feet` | Distance in feet of the prohibition zone around the reference point, from 'within N feet of ...'; empty when the source gives no distance |
| `reference_point` | Physical feature the distance is measured from, lowercase without leading article (e.g. 'marked crosswalk'); empty when none stated |
| `near_address` | Street address anchoring the reference point, exactly as written (e.g. '26 Lincoln Street', '39A Lincoln Street'); the geocodable anchor for the row |
| `meter_number` | Former parking meter number, digits only with the '#' stripped; empty when the space was not described as metered |
| `location_detail` | Positional qualifier from the source that does not fit the structured columns; empty for all current entries |
| `notes` | Extractor remarks about anomalies in the source text; never carries data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

### 221 — Signs to be erected

[221_game_day_sign_locations.tsv](221_game_day_sign_locations.tsv) — 7 rows

| Column | Description |
|--------|-------------|
| `street` | Street on which the temporary game-time sign is placed (required) |
| `cross_street` | Named street at which the sign is placed; empty when the reference point is a municipal boundary (see city_line). A row geocodes from street + cross_street or street + city_line |
| `city_line` | Adjacent municipality whose Newton boundary line is the sign's reference point ('at the Boston line' -> boston); lowercase token; empty when the reference point is a named street. Proposed shared vocabulary (municipal_boundary) defined inline pending adoption into _common.json |
| `street_2` | Second sign location's street, used ONLY when a PDF line-wrap jams two 'STREET, at TARGET.' sign locations into one blank-line paragraph; empty otherwise. Lets one paragraph-row carry both geocodable sign locations without dropping either |
| `cross_street_2` | Second merged sign location's named cross street; empty when that location's reference point is a municipal boundary (see city_line_2) or when there is no second location |
| `city_line_2` | Second merged sign location's municipal boundary token (same vocabulary as city_line); empty when that location's reference point is a named street or when there is no second location |
| `notes` | Extractor remarks about anomalies in the source text (e.g. the PDF merge of two sign locations into one paragraph); never carries geocodable data |
| `source_text` | Verbatim source clause, whitespace-collapsed; the row's provenance (required; vocabulary: `source_text`) |

## Planned

Sections with extraction coverage planned but not yet built:

- **83** — Use and operation of heavy commercial vehicles restricted on certain streets → `83_commercial_vehicle_restrictions.tsv`
- **84** — Speed zones designated → `84_speed_limits.tsv`
- **176** — Parking regulations pertaining to particular streets.* → `176_street_parking_regulations.tsv`
- **177** — Football game day parking regulations → `177_game_day_parking.tsv`
- **180** — Stopping Prohibited on Particular Streets → `180_stopping_prohibited.tsv`
- **194** — Time limits in municipal off-street parking areas → `194_municipal_parking_time_limits.tsv`
- **204** — Newton North High School Tiger Parking Permits → `204_tiger_parking_permits.tsv`
- **205** — Newtonville Neighborhood Parking District → `205_newtonville_parking_district.tsv`
- **206** — Auburndale Village Parking District → `206_auburndale_parking_district.tsv`
- **208** — Waban Village Parking District → `208_waban_parking_district.tsv`
- **209** — Newton Highlands Parking District → `209_newton_highlands_parking_district.tsv`
- **210** — Newton Corner Parking District → `210_newton_corner_parking_district.tsv`
- **211** — Charlesbank Area Parking District → `211_charlesbank_parking_district.tsv`

## Not extracted

| Section | Title | Status | Reason |
|---------|-------|--------|--------|
| 168 | Parking limit in municipal off-street parking areas | excluded | Single citywide rule (3-hour limit); no per-location entries to tabulate. |
| 169 | Times parking prohibited in Oak Hill off-street area | excluded | Single rule for one lot; no per-location entries to tabulate. |
| 178 | Reserved | excluded | Reserved. |
| 203 | Reserved | excluded | Reserved. |
| 207 | Horace Mann Neighborhood Parking District | excluded | Header and ordinance history only; no parking-district streets enumerated in the source. |
| 222 | Reserved | excluded | Reserved. |
| 223 | Reserved | excluded | Reserved. |
| 195 | Reserved | review | Marked Reserved, but sections/195.txt contains stray TPR-196 content (section-splitter artifact in process-tpr.py). |
| 220 | Parking prohibitions for tow zones.* | review | 176-class section: blanket preamble entries + street headers with numbered sub-clauses + em-dash inline forms. Both models produced malformed rows (inconsistent column counts); needs careful single-section pass. |

## Legacy CSV files

The remaining `*.csv` files are one-off extractions from March 2025 (two TPR revisions stale, no provenance, inconsistent schemas). Treat them as deprecated; they are removed as each section's TSV dataset goes active.

