# TPR Geocoding — Build Plan

Geocode the 40 `extracted_data/*.tsv` TPR datasets to Newton geography. This
plan is the durable record of decisions made while designing it (written to
survive context compaction). Nothing here is built/committed yet except this
plan; the extraction project (the `tpr-extract` skill, 40 datasets) is done.

Sibling discipline carries over from `tpr-extract`: deterministic core +
independent verification + **triangulate-and-flag** (never a silent guess),
provenance on every record, human review of the residual. Tooling: **`uv run`
+ PEP 723** inline deps (see memory `use-uv-and-pep723`).

## Status / what's proven

- **147 intersection pilot: 97% (963/989) of rows resolve both street names**
  deterministically; **0 geocoded points outside Newton bounds.**
- Centerline + OSM fetched to `/tmp/tpr_geo/` (EPHEMERAL — re-fetch, see below).
- Google geocoder tested: works WITH an acceptance gate; unreliable for
  intersections.

## Data sources (tiered)

1. **Primary — Newton GIS street centerlines.** ArcGIS Hub item
   `52aa85d9b7cd4a05b9018e9db8012c10_15` ("Street_Center_Lines"). Fetch:
   `curl -sL "https://opendata.arcgis.com/datasets/52aa85d9b7cd4a05b9018e9db8012c10_15.geojson"`
   4780 LineStrings, 1476 names, WGS84 [lon,lat]. Key fields: `NAME`
   (UPPERCASE/abbreviated, e.g. "WASHINGTON ST"), **`FROM_ST`/`TO_ST`**
   (cross-streets at each segment's endpoints = intersection topology),
   `LF/LT/RF/RT` (address ranges), `ONEWAY`, `TRUCK_EXCL`, `Segment_ID`.
2. **Secondary — OpenStreetMap (osmnx).** Fills centerline gaps (e.g. Corey St).
   `ox.graph_from_place("Newton, Massachusetts, USA", network_type="drive")` →
   `ox.graph_to_gdfs(G, nodes=False)`. ~8500 edges, 1383 names.
3. **Tertiary fallback — Google geocoder (connected MCP) OR MassGIS.**
   For streets/addresses/POIs absent from both. Google is wired and works but
   has ToS limits on STORING coords → tag `source: google_geocode` + note;
   prefer **MassGIS** (open license) for anything redistributed. POIs
   (driveways, school lots) only Google can place → low-confidence.

## Location types → method

| Type | Method | Datasets |
|---|---|---|
| Intersection (street × cross) | centerline FROM_ST/TO_ST endpoint match; geometric crossing fallback. **NOT Google** (unreliable for intersections) ✓ proven | 147, 96, 145, 146, 148, 88, 97, 98, 99, 221 |
| Offset point ("N ft DIR of X") | resolve X, linear-reference N ft along the route | within 176, 84, 202, 147(some) |
| Segment (from→to) | linear-referenced interval along the route | 176, 84, 85, 83 |
| Address ("740 Beacon St") | centerline LF/LT/RF/RT ranges; Google address geocode (gated) | 199, 200, 219 |
| POI / landmark | Google places → low-confidence, human-confirm | residual in several |
| Inline GPS (lat,lon already present) | use directly — **also the validation set** | 84, 194, 196 |

## Name resolution (deterministic; NO auto-fuzzy)

Normalizer: uppercase; strip "."; abbreviate ALL suffix tokens
(STREET→ST, ROAD→RD, AVENUE→AVE, TERRACE→TER, PLACE→PL, CIRCLE→CIR, DRIVE→DR,
COURT→CT, LANE→LN, PARKWAY→PKWY, BOULEVARD→BLVD, SQUARE→SQ, EXTENSION→EXT,
WEST/EAST/NORTH/SOUTH→W/E/N/S); strip "(...)"; take first of "X and Y" / "X/Y";
collapse divided-road "COMMONWEALTH AVE, N/S DR"→"COMMONWEALTH AVE". Match:
exact → space-insensitive exact → curated alias table. **No fuzzy auto-match**
(Carver≠Carter, Aspen≠Spencer, Lion≠Lind — proven dangerous). Fuzzy only as a
SUGGESTION in the review queue.

**Paired-street disambiguator** (stronger than string distance): when a name is
ambiguous/absent, the right candidate is the one whose centerline actually
intersects the *paired* street. (Meadow Rd → Meadowbrook Rd, because only
Meadowbrook intersects Country Club Rd, the cross-street in that §147 row.)

## Representation (the crux — decided)

**Store linear references, NOT geometry.** A regulation =
`(street/route, side, from_anchor, from_offset_ft, to_anchor, to_offset_ft,
type, value, source_text, method, confidence, source)`. Anchor to
**cross-streets + offsets (semantic, stable)**, NOT `Segment_ID` (geometric,
churns between GIS releases).

- **Geometry is DERIVED on demand** (compute Point/LineString by measuring
  offsets along the *current* centerline). Optionally materialized as a
  **regenerable** GeoJSON export (`--render`), marked derived — never truth.
  (Same principle as the extraction: source_text/offsets are truth, geometry
  computed downstream; a TPR edit or a GIS-release edit each re-resolve without
  re-authoring the other.)
- **GIS segment = spatial backbone + join key.** Routes assembled by chaining
  segments on FROM_ST/TO_ST adjacency; offsets measured along the route.
- **Coarse regs (speed/one-way/truck/thruway): one value per segment holds** →
  clean per-segment rollup. **Parking (176/220/180): side-specific +
  offset-delimited, many per block-face** → linear-referenced intervals;
  optional DERIVED "homogeneous re-segmentation" if a one-value-per-piece layer
  is wanted (build product, not the model).
- Point features (signs) → Points at intersections.

## Outputs & registers (formats)

- **`geo/`** — vendored centerline + OSM reference data, with provenance &
  licensing (Newton GIS attribution; OSM ODbL; note Google ToS / MassGIS).
- **Truth layer**: linear-reference records per regulation → **JSONL** keyed by
  `source_text`, with a committed **JSON Schema** (validate via `jsonschema`).
- **`geocoded/review_queue.jsonl`** — unresolved/inferred items: JSONL +
  JSON Schema; fields `tpr_value, section, paired_street, suggestion, evidence,
  candidates[], confidence, status(open/confirmed/rejected)`. Nested → JSON.
- **`geo/street_aliases.jsonl`** — curated, auto-applied corrections only;
  JSONL + JSON Schema; `tpr_value, resolved_to, evidence, sources, verified_by`.
- **Geometry** → GeoJSON (derived export). **Flat per-row join table** →
  optional TSV keyed by `source_text`.
- **Provenance on every record**: `method` (centerline_endpoint /
  centerline_geometric / osm / google_geocode / alias / manual), `confidence`,
  `source`. **Do NOT reformat the 40 published extraction TSVs** (stay TSV,
  enforced by `tpr-extract/scripts/validate.py`).

## Verification (triangulate-and-flag)

- **Inline GPS coords** (84/194/196) cross-check the centerline geocoder.
- Plausibility: in-Newton-bounds; point lies on the named street.
- **ONEWAY** field cross-checks dataset 85; **TRUCK_EXCL** cross-checks 83.
- **Google acceptance gate**: accept only if `formatted_address` corroborates
  the query (Google silently degrades — Lion Dr→"154 Wells Ave", Institution
  Ave→city centroid). Else → review queue.
- Everything inferential/low-confidence → review queue with evidence + status.

## Build phases

- **Phase 0 — Foundation.** Create `tpr-geocode` skill (SKILL.md = this policy);
  vendor `geo/` centerline+OSM w/ provenance; JSON Schemas for the two registers;
  seed `street_aliases.jsonl` + `review_queue.jsonl` with the exceptions below;
  normalizer/resolver module (`uv`/PEP 723: shapely, osmnx, pyproj, jsonschema).
- **Phase 1 — Intersections + points** (proven path): geocode 147, 96, 145,
  146, 148, 88, 97–99, 221 → Points + provenance/confidence; unresolved →
  review queue; validate (bounds, on-street).
- **Phase 2 — Route assembly + linear-referencing core.** Chain segments into
  per-street routes; offset-resolver (feet along route from a cross-street).
  Empirical check: speed-zone→segment alignment rate; 176 clauses-per-blockface.
- **Phase 3 — Offsets + segments.** 84 (speed), 176 (parking), 85, 83, 202,
  180, 220 as linear-referenced intervals.
- **Phase 4 — Addresses + POIs.** 199, 200, 219 via LF/LT ranges / Google
  (gated); landmarks via Google places (human-confirm).
- **Phase 5 — Verification + outputs.** Inline-GPS + ONEWAY/TRUCK cross-checks;
  `--render` GeoJSON; per-segment rollup (coarse) + optional homogeneous layer
  (parking); coverage report.

## Seed exceptions (found in the 147 pilot — preload the registers)

**Aliases (safe, auto-apply):** Carver Street→CARVER RD; Aspen Street→ASPEN AVE
(§206 confirms); Wendall Rd→WENDELL RD; Ossippee Rd→OSSIPEE RD; Woodchester
Rd→WOODCHESTER DR; Wolcott Street Extension→WOLCOTT ST; space-insensitive:
Brae Burn, Gray Cliff, Saw Mill Brook, Longmeadow.

**Review queue (do NOT auto-resolve):**
- Institution Avenue → suggest **Braeland Ave × Langley Rd** (only un-stop-signed
  Braeland node; historical "Newton Theological Institution" on Herrick Rd);
  status open. Absent from city GIS, OSM, and Google.
- Lion Drive — absent from city GIS + OSM (real per §176); needs source.
- Corey Street — absent from city GIS, present in OSM → resolve via OSM.
- Philip Bram Way — absent both GIS layers; Google matched (gated) → low conf.
- Meadow Road → **Meadowbrook Rd** (paired-street: only "…Meadow…" intersecting
  Country Club Rd); status open.
- Landmarks/ramps (not streets): Marriott Hotel Driveway, YMCA Driveway, Peirce
  Elementary parking lot, Route 9 ramps, I-95 North → Google places / flag.

## Key principles (don't regress)

1. Anchor regs to cross-streets + offsets (semantic), not Segment_IDs.
2. Geometry is derived/regenerable, never stored as truth.
3. No auto-fuzzy name matching; fuzzy is a review-queue suggestion only.
4. Google results pass the formatted_address acceptance gate or go to review.
5. Provenance + confidence on every geocoded record; inferential → review queue.
6. `uv run` + PEP 723 for every script with deps.
