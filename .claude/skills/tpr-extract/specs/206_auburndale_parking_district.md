# Section 206 — Auburndale Village Parking District

Membership list (clause (c)) — which streets/segments belong to the district;
one row per street. Same schema as the other districts (208-211). The actual
per-street parking rules live in TPR-176.

PDF text extraction of this list has column-merge artifacts, so it was
disentangled from the PDF pages (218-219). Two-column layout merged pairs onto single lines ("Williston Road (...) Woodbine Street"); split them and de-duplicate Woodbine Street/Terrace (which also appear standalone). Woodbine Street's a)/b) sub-segments captured in notes. Parentheticals "X to Y" →
from_point/to_point; "including ..."/"except ..." → segment_note.

Verified by direct PDF read; `source_text` unique. Manifest counting =
verified_by (line-separated list with merges defeats regex counting).
