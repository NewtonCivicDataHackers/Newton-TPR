# Section 176 — Parking regulations pertaining to particular streets

The largest section (~190KB, PDF pp. 95–199). Prose, not tables, so extracted
from the **text** (chunked) rather than PDF pages. ~526 streets, ~1283
numbered clauses.

## Source shape

Intro (a) construction rules / (b) / (c) "On the following streets ... parking
of vehicles is restricted as stated below:", then per-street blocks:

```
Adams Street
 (1) Prohibited, all times, Washington Street to a point 100 feet northerly, east side.
 (2) Two-hour limit, except Saturdays, Sundays and Holidays, 7:00 a.m. – 7:00 p.m., from a
     point 100 feet north of Washington Street to Wiltshire Road, east side.
 ...
```

- A **street heading** is a bare capitalized line (no clause marker) followed
  by `(1)`.
- Each **numbered clause** `(n)` is one parking regulation.

## Grain & rules

- **One row per numbered clause.** clause = n.
- **Lettered sub-clauses** (`a) … b) … c) …` under a numbered clause — usually
  day/time windows for the same location, as in TPR-180's Hartman Road) are
  NOT separate rows; fold them into the parent clause's `schedule`, joined with
  `; `. Note their presence in `notes`.
- **Wrapped lines:** PDF inserts blank lines mid-clause; a clause's continuation
  starts lowercase ("of Washington Street to ..."). Rejoin into one clause /
  one `source_text` (whitespace-collapsed).
- `restriction` = the leading phrase, lowercased: prohibited / two-hour limit /
  one-hour limit / 15-minute limit / parking meter zone / resident permit only /
  loading zone / no stopping / etc.
- `side` from common#side (east/west/both/north/south/odd/even).
- Segment: when the clause reads "FROM to TO", fill `from_point`/`to_point`
  (strip "a point", "the junction of"); "entire length" → `extent`; if the
  segment is too complex for a clean pair, leave from/to empty (the full text
  remains in `source_text`).
- `schedule`: the day/time content (times, "except Saturdays, Sundays and
  Holidays", "School Days", "including Saturdays", etc.).
- `source_text`: prefix with the street name so each clause is unique
  ("Adams Street (2) Two-hour limit ...").
- Cross-references like "except by Resident Permit as listed in TPR-202" →
  keep in `source_text`, summarize in `notes`.

## Extraction method (as built)

11 Sonnet agents, each reading a street-aligned line range of `sections/176.txt`
(disjoint, boundaries on street headings → no splits). 1295 clauses extracted.

Agents hand-wrote TSV and inconsistently dropped trailing empty cells
(`extent`, `notes`), so the files had ragged column counts. Recovery
(`/tmp/tpr_fanout/salvage_176.py`): fields 0–5 are reliably positioned
(verified — `clause` 100% integer, field 3 always a side value/variant), and
`source_text` is identifiable as the street-prefixed field containing the
clause marker. So street/clause/restriction/side/from_point/to_point and
source_text/notes are salvaged directly; `extent` is re-derived from
source_text ("entire length"); `schedule` is a best-effort regex pull of time
ranges + day phrases from source_text (source_text remains authoritative).
Lesson for future big sections: have agents emit **JSON** (all keys explicit),
not hand-aligned TSV.

## Verification

Cross-method reconciliation: a deterministic numbered-clause count (1288) vs the
salvaged rows (1295) differed on only 6 streets — all traced to the
deterministic detector's own heading errors (it missed real streets Elm Road/
Studio Road/Greenwood Street and invented phantom headings), confirmed by grep.
Sonnet's extraction was the more accurate of the two. `source_text` is unique
across all 1295 rows. Manifest uses `"counting": {"verified_by": ...}`.

## Pilot

Lines 26–659 (Aberdeen → Bennington, 44 streets) = 115 numbered clauses.
