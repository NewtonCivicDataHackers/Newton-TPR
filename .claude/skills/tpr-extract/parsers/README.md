# Deterministic parsers — an independent SANITY CHECK, not the source of truth

**Read this before assuming these scripts are authoritative. They are not.**

## What these are

Pure-Python parsers that re-derive a few datasets *directly from* the section
text in `sections/*.txt`, with no LLM and no network. Each one is a second,
independent way to produce rows that were originally produced by the main
extraction process.

## What is actually authoritative

The committed TSVs in `extracted_data/*.tsv`. Those are the source of truth.
They were produced by the full extraction process (LLM double-extraction,
PDF-page vision reads for scrambled tables, and careful hand extraction),
each gated by `scripts/validate.py`. **The parsers here did not produce the
authoritative data and are not trusted to be correct.**

## The role: a tripwire, not an authority

The TPR is a **human-edited legal document**. Every revision can introduce a
new phrasing, a new structural form, a typo, or an internal inconsistency that
a parser frozen against today's formats will not handle — and may mis-handle
*silently*. So a deterministic parser is **not** a stable, trustworthy
extractor. Its value is exactly the opposite of authority:

> Run `check.py` after a new TPR revision. Each parser re-derives its rows from
> the new section text and is diffed against the committed TSV.
> - **Agreement** (and the parser's own checksum/counts hold) → strong evidence
>   that nothing in those sections drifted.
> - **Divergence, or a parser failure/checksum mismatch** → a SIGNAL that the
>   format changed or a row is wrong. This goes to a **human for review**, never
>   to automatic correction. The parser being "broken" by a revision is the
>   alarm doing its job, not a defect.

This is one leg of a triangulation: LLM extraction (format-robust) +
deterministic parser (cheap, independent) + the method-independent verifiers in
`validate.py` (checksums, completeness counts, multiset reconciliation). Where
all three agree, confidence is high; where they disagree is precisely what a
person should look at.

## Coverage (deliberately partial — this is informative)

A parser exists ONLY for sections with a regular-enough grammar to re-derive:

| Section | Parser | Re-derivable subset | Independent check |
|---|---|---|---|
| 84 speed zones | `parse_84_speed_zones.py` | prose **stanzas + one-liners** only | per-stanza distance **checksum** |
| 177 game-day parking | `parse_177_game_day.py` | all rows | row count |
| 220 tow zones | `parse_220_tow_zones.py` | all rows | row count |

Everything NOT listed here has **no deterministic parser** — the ~30 LLM
double-extracted sections, the PDF-vision tables (194, 196, and 84's *table*
rows), and the hand-extracted sections (83, 180, 201, 202, 204, 205, 206,
208–211). On a new revision those have no cheap deterministic cross-check and
must be re-extracted and reviewed directly. The absence of a parser is itself
useful: it tells you which sections carry the most review burden.

## Run

```
python3 .claude/skills/tpr-extract/parsers/check.py
```
Exit 0 = every parser agrees with the committed TSV. Non-zero = divergence to
review (the script prints exactly which rows/cells differ).
