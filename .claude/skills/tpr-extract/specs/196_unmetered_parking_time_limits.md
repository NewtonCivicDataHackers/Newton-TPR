# Section 196 — Time limits in other (unmetered) municipal off-street parking areas

Same wide matrix as TPR-194 but for lots that do NOT require payment.
Heading "Unmetered Parking Lot"; on PDF page 209. 2 lots (both Nonantum):
Adams St and Chapel St (each 23 three-hour spaces).

`sections/196.txt` now exists and 196 is in `index.json` (the `process-tpr.py`
splitter was fixed: its boundary regex required a period after the section
number, but the "Sec. TPR-196 Time limits..." heading has none, so 196 had
been merged into 195.txt). The text holds only the 196 intro; the table
itself is PDF-derived (page 209).

Verified by two independent PDF reads (Sonnet earlier + orchestrator) of the
identical-to-194 layout. Manifest counting = verified_by.
