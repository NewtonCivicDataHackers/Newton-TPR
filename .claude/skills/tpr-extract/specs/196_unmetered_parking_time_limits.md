# Section 196 — Time limits in other (unmetered) municipal off-street parking areas

Same wide matrix as TPR-194 but for lots that do NOT require payment.
Heading "Unmetered Parking Lot"; on PDF page 209. 2 lots (both Nonantum):
Adams St and Chapel St (each 23 three-hour spaces).

**Splitter caveat:** `process-tpr.py` merges TPR-196 into `sections/195.txt`
(195 is "Reserved"); there is no `sections/196.txt`, and 196 is absent from
`index.json`. Only the 196 intro is in the text; the table is PDF-derived
(page 209). This dataset's manifest entry was added manually with
`source: sections/195.txt`. A proper fix is to correct the splitter in
`process-tpr.py` so 196 gets its own section — see [[tpr-extract-skill-state]].

Verified by two independent PDF reads (Sonnet earlier + orchestrator) of the
identical-to-194 layout. Manifest counting = verified_by.
