# Section 205 — Newtonville Parking District

Membership list (clause (c)) — which streets/segments belong to the district;
one row per street. Same schema as the other districts (208-211). The actual
per-street parking rules live in TPR-176.

PDF text extraction of this list has column-merge artifacts, so it was
disentangled from the PDF pages (216-217). Splits the PDF-merged line "Pulsifer Street Russell Court" into two streets. Parentheticals "X to Y" →
from_point/to_point; "including ..."/"except ..." → segment_note.

Verified by direct PDF read; `source_text` unique. Manifest counting =
verified_by (line-separated list with merges defeats regex counting).
