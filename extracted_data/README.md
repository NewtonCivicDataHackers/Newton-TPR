# Newton TPR Extracted Data

<!-- GENERATED FILE — do not edit. -->
<!-- Regenerate with: python3 .claude/skills/tpr-extract/scripts/gen_readme.py -->

Structured TSV datasets extracted from the Newton Traffic and Parking Regulations section text in [sections/](../sections/). The extraction contract — schemas, vocabulary, per-section specs, and validation — lives in the `tpr-extract` skill at `.claude/skills/tpr-extract/`.

- **TPR revision**: 2026-01-16
- **Format**: TSV (tab-separated, UTF-8, no quoting); every row carries a verbatim `source_text` provenance column

## Datasets

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

## Planned

Sections with extraction coverage planned but not yet built:

- **83** — Use and operation of heavy commercial vehicles restricted on certain streets → `83_commercial_vehicle_restrictions.tsv`
- **84** — Speed zones designated → `84_speed_limits.tsv`
- **85** — One-way streets → `85_one_way_streets.tsv`
- **86** — U-turns → `86_u_turns_prohibited.tsv`
- **87** — Left turns prohibited → `87_left_turns_prohibited.tsv`
- **88** — Right turn only → `88_right_turn_only.tsv`
- **89** — Right turns prohibited → `89_right_turns_prohibited.tsv`
- **90** — Vehicle Restrictions on Public Ways., the following prohibitions apply: → `90_vehicle_restrictions.tsv`
- **95** — Thruways → `95_thruways.tsv`
- **97** — Left lane must turn left → `97_left_lane_must_turn_left.tsv`
- **98** — Right lane must turn right → `98_right_lane_must_turn_right.tsv`
- **99** — Through travel prohibited → `99_through_travel_prohibited.tsv`
- **145** — Traffic-control signal locations → `145_traffic_control_signals.tsv`
- **146** — Flashing warning light locations → `146_flashing_warning_lights.tsv`
- **147** — Obedience to isolated stop signs → `147_stop_signs.tsv`
- **149** — School zones → `149_school_zones.tsv`
- **150** — Safety Zones → `150_safety_zones.tsv`
- **172** — Loading zones → `172_loading_zones.tsv`
- **176** — Parking regulations pertaining to particular streets.* → `176_street_parking_regulations.tsv`
- **177** — Football game day parking regulations → `177_game_day_parking.tsv`
- **179** — School drop off zones → `179_school_drop_off_zones.tsv`
- **180** — Stopping Prohibited on Particular Streets → `180_stopping_prohibited.tsv`
- **194** — Time limits in municipal off-street parking areas → `194_municipal_parking_time_limits.tsv`
- **199** — Fire Lanes → `199_fire_lanes.tsv`
- **200** — Accessible Parking Spaces → `200_accessible_parking_spaces.tsv`
- **201** — Overnight on-street angle parking areas → `201_overnight_angle_parking.tsv`
- **202** — Resident restricted areas → `202_resident_restricted_areas.tsv`
- **204** — Newton North High School Tiger Parking Permits → `204_tiger_parking_permits.tsv`
- **205** — Newtonville Neighborhood Parking District → `205_newtonville_parking_district.tsv`
- **206** — Auburndale Village Parking District → `206_auburndale_parking_district.tsv`
- **207** — Horace Mann Neighborhood Parking District → `207_horace_mann_parking_district.tsv`
- **208** — Waban Village Parking District → `208_waban_parking_district.tsv`
- **209** — Newton Highlands Parking District → `209_newton_highlands_parking_district.tsv`
- **210** — Newton Corner Parking District → `210_newton_corner_parking_district.tsv`
- **211** — Charlesbank Area Parking District → `211_charlesbank_parking_district.tsv`
- **219** — Parking prohibitions in areas that previously allowed parking → `219_removed_parking_spaces.tsv`
- **220** — Parking prohibitions for tow zones.* → `220_tow_zones.tsv`
- **221** — Signs to be erected → `221_game_day_sign_locations.tsv`

## Not extracted

| Section | Title | Status | Reason |
|---------|-------|--------|--------|
| 168 | Parking limit in municipal off-street parking areas | excluded | Single citywide rule (3-hour limit); no per-location entries to tabulate. |
| 169 | Times parking prohibited in Oak Hill off-street area | excluded | Single rule for one lot; no per-location entries to tabulate. |
| 178 | Reserved | excluded | Reserved. |
| 203 | Reserved | excluded | Reserved. |
| 222 | Reserved | excluded | Reserved. |
| 223 | Reserved | excluded | Reserved. |
| 195 | Reserved | review | Marked Reserved, but sections/195.txt contains stray TPR-196 content (section-splitter artifact in process-tpr.py). |

## Legacy CSV files

The remaining `*.csv` files are one-off extractions from March 2025 (two TPR revisions stale, no provenance, inconsistent schemas). Treat them as deprecated; they are removed as each section's TSV dataset goes active.

