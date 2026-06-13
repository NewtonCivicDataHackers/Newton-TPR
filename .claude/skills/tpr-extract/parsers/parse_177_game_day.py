#!/usr/bin/env python3
"""Deterministic re-derivation of TPR-177 (football game-day parking) from
sections/177.txt — an INDEPENDENT SANITY CHECK, not the authoritative data.
See parsers/README.md. Authoritative data is extracted_data/177_game_day_parking.tsv.

Run via parsers/check.py, or standalone to print the re-derived TSV:
    python3 parse_177_game_day.py
"""
import csv, re, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
COLS = ["street", "side", "from_point", "to_point", "segment_detail",
        "enforcement_window", "source_text", "notes"]

SIDE = re.compile(r'\b(both|north|south|east|west)\s+sides?\b', re.I)

def _paras(s):
    out, cur = [], []
    for l in s.split('\n'):
        if l.strip(): cur.append(l.strip())
        elif cur: out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out

def _seg(text):
    m = re.search(r'from (.+?) to (.+?)(?:\.|$)', text)
    if m: return m.group(1).strip(), m.group(2).strip(), ''
    m = re.search(r'from (.+?)(?:\.|$)', text)
    if m: return '', '', m.group(1).strip()
    m = re.search(r'\bto (.+?)(?:\.|$)', text)
    if m: return '', m.group(1).strip(), ''
    return '', '', ''

def parse():
    txt = (REPO_ROOT / 'sections/177.txt').read_text(encoding='utf-8')
    d0 = re.search(r'two hours after the scheduled time of game commencement:', txt).end()
    e_hdr = re.search(r'\(e\) The following is a list', txt)
    foot = re.search(r'\(Ord\. No\. T-278', txt)
    rows = []

    def emit(street, body, window, note, source_text):
        s = SIDE.search(body)
        side = s.group(1).lower() if s else ''
        after = body[s.end():] if s else body
        frm, to, seg = _seg(after)
        rows.append(dict(street=street.strip(), side=side, from_point=frm, to_point=to,
                         segment_detail=seg, enforcement_window=window,
                         source_text=source_text, notes=note))

    def process(region, window):
        cur = None
        for p in _paras(region):
            if p.startswith('(e)'): continue
            m = re.match(r'^\((\d+)\)\s*(.*)', p)
            if m and cur:
                emit(cur, m.group(2), window, f'sub-clause ({m.group(1)}) of {cur}',
                     f"{cur} ({m.group(1)}) {m.group(2)}")
                continue
            if re.match(r'^[A-Z]', p):
                if p.rstrip().endswith(':'):
                    cur = p.rstrip().rstrip(':').strip(); continue
                cur = None
                emit(p.split(',')[0].strip(), p, window, '', p)

    process(txt[d0:e_hdr.start()], '2h before to 2h after')
    process(txt[e_hdr.end():foot.start()], '7:00 a.m. to 5h after')
    return COLS, rows

if __name__ == '__main__':
    cols, rows = parse()
    w = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    w.writerow(cols)
    for r in rows: w.writerow([str(r.get(c, '')) for c in cols])
