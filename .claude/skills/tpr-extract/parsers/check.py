#!/usr/bin/env python3
"""Triangulation harness: run each deterministic parser and diff its re-derived
rows against the AUTHORITATIVE committed TSV in extracted_data/.

This is a sanity check, NOT a regenerator — it never writes data. See
parsers/README.md. Agreement = strong evidence those sections didn't drift on a
new revision; divergence (or a parser checksum failure) = a signal for human
review, because the TPR is human-edited and a frozen parser will break on novel
formats. Exit 0 = all agree; non-zero = divergence(s) printed for review.
"""
import csv, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))

import parse_84_speed_zones, parse_177_game_day, parse_220_tow_zones  # noqa: E402

def load_tsv(path):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter='\t'))

def run_parser(mod):
    out = mod.parse()
    cols, rows = out[0], out[1]
    fails = out[2] if len(out) > 2 else []
    return cols, [dict(zip(cols, [str(r.get(c, '')) for c in cols])) for r in rows], fails

CHECKS = [
    ('84 speed zones (stanzas+one-liners)', parse_84_speed_zones,
     'extracted_data/84_speed_limits.tsv', lambda r: r['entry_type'] in ('stanza', 'oneliner')),
    ('177 game-day parking', parse_177_game_day,
     'extracted_data/177_game_day_parking.tsv', None),
    ('220 tow zones', parse_220_tow_zones,
     'extracted_data/220_tow_zones.tsv', None),
]

def main():
    from collections import Counter
    any_divergence = False
    for label, mod, tsv, row_filter in CHECKS:
        cols, parser_rows, fails = run_parser(mod)
        committed = load_tsv(REPO_ROOT / tsv)
        if row_filter:
            committed = [r for r in committed if row_filter(r)]
        # Compare full rows as a multiset (source_text alone is not unique:
        # multi-segment stanzas share it). Agreement on the multiset is the
        # real triangulation signal.
        p_ms = Counter(tuple(r.get(c, '') for c in cols) for r in parser_rows)
        c_ms = Counter(tuple(r.get(c, '') for c in cols) for r in committed)
        only_p = list((p_ms - c_ms).elements())
        only_c = list((c_ms - p_ms).elements())
        si = cols.index('source_text')
        ok = not (only_p or only_c)
        print(f"[{'AGREE' if ok else 'DIVERGE'}] {label}: parser={len(parser_rows)} "
              f"committed={len(committed)} matched={sum((p_ms & c_ms).values())}")
        # Checksum flags are INFORMATIONAL (the parser's own quality signal);
        # a flag that's also reflected in the committed data is a known anomaly,
        # not a drift. Only parser-vs-committed divergence fails the harness.
        for f in fails:
            print(f"    info: parser checksum flag (known if also in committed): "
                  f"{f[0]} {f[1]} sum={f[2]} total={f[3]}")
        for row in only_p[:10]:
            print(f"    only in PARSER:    {row[si][:80]}")
        for row in only_c[:10]:
            print(f"    only in COMMITTED: {row[si][:80]}")
        if not ok:
            any_divergence = True
    if any_divergence:
        print("\nDIVERGENCE — review the rows above (format drift or a wrong row).")
        return 1
    print("\nOK: all deterministic parsers agree with the committed data.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
