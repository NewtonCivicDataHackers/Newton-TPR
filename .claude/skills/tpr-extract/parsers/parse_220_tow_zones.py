#!/usr/bin/env python3
"""Deterministic re-derivation of TPR-220 (tow zones) from sections/220.txt —
an INDEPENDENT SANITY CHECK, not the authoritative data. See parsers/README.md.
Authoritative data is extracted_data/220_tow_zones.tsv.

    python3 parse_220_tow_zones.py    # print the re-derived TSV
"""
import csv, re, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
COLS = ["street", "restriction", "side", "from_point", "to_point",
        "segment_detail", "schedule", "source_text", "notes"]

DASH = re.compile(r'\s*[—–\-─]\s*')  # em / en / hyphen / box-drawing
SIDE = re.compile(r'\b((?:north|south|east|west)(?:\s+and\s+(?:north|south|east|west))?\s+sides?|both\s+sides?)\b', re.I)

def _paras(s):
    out, cur = [], []
    for l in s.split('\n'):
        if l.strip(): cur.append(l.strip())
        elif cur: out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out

def _restriction(body):
    b = body.lower()
    if 'parking prohibited' in b: return 'parking prohibited'
    return 'tow-away zone'

def _side(body):
    m = SIDE.search(body)
    return re.sub(r'\s+sides?$', '', m.group(1).strip(), flags=re.I).lower() if m else ''

def _seg_sched(body):
    frm = to = seg = ''
    m = re.search(r'from (.+?) to (.+?)(?:\.|$)', body)
    if m: frm, to = m.group(1).strip(), m.group(2).strip()
    else:
        m = re.search(r'between (.+?) and (.+?)(?:\.|$)', body)
        if m: frm, to = m.group(1).strip(), m.group(2).strip()
        else:
            m = re.search(r'(from .+?|entire length)(?:\.|$)', body)
            if m: seg = m.group(1).strip()
    tm = re.findall(r'\d{1,2}:\d{2}\s*[ap]\.m\.\s*(?:to|–|-)\s*\d{1,2}:\d{2}\s*[ap]\.m\.', body)
    days = [d for d in ['Monday through Saturday', 'Saturdays included', 'on school days',
                        'school days', 'including Sundays and Holidays'] if d.lower() in body.lower()]
    return frm, to, seg, '; '.join(dict.fromkeys(days + tm))

def parse():
    txt = (REPO_ROOT / 'sections/220.txt').read_text(encoding='utf-8')
    start = re.search(r'In any bus stop at any time\.', txt).end()
    foot = re.search(r'\(Rev\. Ords\. 1973, § 13-183', txt)
    region = txt[start:foot.start()]
    blanket = [m.strip() for m in re.findall(
        r'((?:Any vehicle parked in violation|In any fire lane|In any bus stop)[^\n]*\.)', txt[:start])]

    rows = [dict(street='', restriction='blanket prohibition', side='', from_point='', to_point='',
                 segment_detail='', schedule='', source_text=re.sub(r'\s+', ' ', b).strip(),
                 notes='applies city-wide (tow-away)') for b in blanket]

    cur = None
    for p in _paras(region):
        p = re.sub(r'\s+', ' ', p).strip()
        m = re.match(r'^\((\d+)\)\s*(.*)', p)
        if m and cur:
            body = m.group(2)
            frm, to, seg, sched = _seg_sched(body)
            rows.append(dict(street=cur, restriction=_restriction(body), side=_side(body),
                from_point=frm, to_point=to, segment_detail=seg, schedule=sched,
                source_text=f"{cur} ({m.group(1)}) {body}",
                notes=f'sub-clause ({m.group(1)})' + (' [source: "Tow-way" typo]' if 'tow-way' in body.lower() else '')))
            continue
        parts = DASH.split(p, maxsplit=1)
        if len(parts) == 2 and ('tow' in parts[1].lower() or 'parking prohibited' in parts[1].lower()):
            street, body = parts[0].strip(), parts[1].strip()
            frm, to, seg, sched = _seg_sched(body)
            rows.append(dict(street=street, restriction=_restriction(body), side=_side(body),
                from_point=frm, to_point=to, segment_detail=seg, schedule=sched, source_text=p, notes=''))
            cur = None
        elif re.match(r'^[A-Z]', p) and 'tow' not in p.lower() and len(p.split()) <= 4:
            cur = p.strip()
    return COLS, rows

if __name__ == '__main__':
    cols, rows = parse()
    w = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    w.writerow(cols)
    for r in rows: w.writerow([str(r.get(c, '')) for c in cols])
