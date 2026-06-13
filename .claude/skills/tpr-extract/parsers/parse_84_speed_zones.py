#!/usr/bin/env python3
"""Deterministic re-derivation of TPR-84 speed-zone STANZAS + ONE-LINERS from
sections/84.txt — an INDEPENDENT SANITY CHECK, not the authoritative data.
See parsers/README.md. Authoritative data is extracted_data/84_speed_limits.tsv.

This covers ONLY the prose forms (entry_type 'stanza' and 'oneliner'). The
section's column TABLES (entry_type 'table') are scrambled by PDF text
extraction and were read from the PDF pages by a vision model — they are NOT
re-derivable here, so check.py compares only the stanza+oneliner rows.

Built-in independent check: each stanza states a total distance; the sum of its
sub-segment lengths must equal it. parse() reports any checksum mismatch.

    python3 parse_84_speed_zones.py     # print the re-derived stanza/oneliner TSV
"""
import csv, re, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / '.claude/skills/tpr-extract/scripts'))
from expand_dittos import expand_dittos  # noqa: E402

COLS = ["street", "direction", "entry_type", "start_point", "end_point",
        "length_miles", "offset_miles", "speed_mph", "source_text", "notes"]

DIRS = r'(north|south|east|west|northeast|northwest|southeast|southwest)bound'
HEADER = re.compile(r'^(.+?),\s*(' + DIRS + r'),\s*.*\bbeginning\b', re.I)
HDR_FROM = re.compile(r'\bbeginning(?:\s+at)?\s+(.+?),?\s+thence\b', re.I)
SPEED = re.compile(r'(\d+(?:\.\d+)?)\s+miles at\s+(\d+)\s+(?:miles\s+)?per hour')
ENDING = re.compile(r'ending\b(.*?)\s*(?:;|,)?\s*the (?:total )?distance being\s+(.+?)\s+miles?\.', re.I | re.S)
ONELINER = re.compile(r'^(.+?),\s*(\d+) miles per hour,?\s+from (.+?) to (.+?)\.\s*\(', re.I)

def _clean(pt):
    pt = re.sub(r'^\s*(?:at\s+)?(?:the junction of\s+)?', '', pt.strip(), flags=re.I)
    return re.sub(r'\s+', ' ', pt).strip()

def _paragraphs(text):
    paras, cur = [], []
    for ln in text.split('\n'):
        if ln.strip(): cur.append(ln.strip())
        elif cur: paras.append(cur); cur = []
    if cur: paras.append(cur)
    return paras

def parse():
    raw = (REPO_ROOT / 'sections/84.txt').read_text(encoding='utf-8')
    exp, _, _ = expand_dittos(raw)
    region = exp[re.search(r'the areas described:', exp).end():]
    paras = _paragraphs(region)
    rows, checksum_fail = [], []

    i = 0
    while i < len(paras):
        joined = ' '.join(paras[i])
        h = HEADER.match(joined)
        if not h:
            i += 1; continue
        street = re.sub(r'\s+', ' ', h.group(1)).strip()
        direction = h.group(2).lower()
        fm = HDR_FROM.search(joined)
        frm = _clean(fm.group(1)) if fm else ''
        segs = []
        j = i + 1
        speed_src = to = total = end_src = ''
        while j < len(paras):
            pj = ' '.join(paras[j])
            if HEADER.match(pj): break
            if 'miles at' in pj:
                segs.extend([(float(a), int(b)) for a, b in SPEED.findall(pj)])
                speed_src = (speed_src + ' ' + pj).strip()
            em = ENDING.search(pj)
            if em:
                to = _clean(em.group(1)); total = em.group(2); end_src = pj
                break
            j += 1
        if not segs:
            i = j + 1 if j > i else i + 1; continue
        next_i = (j + 1) if end_src else j
        src = (joined + ' ' + speed_src + ' ' + end_src).strip()
        pm = re.search(r'\(([\d.]+)\)', total)
        try:
            tnum = float(pm.group(1)) if pm else float(re.findall(r'[\d.]+', total)[0])
        except Exception:
            tnum = None
        csum_note = ''
        if tnum is not None:
            s = round(sum(l for l, _ in segs), 3)
            if abs(s - tnum) > 0.02:
                checksum_fail.append((street, direction, s, tnum))
                csum_note = f'source total {tnum} mi disagrees with segment sum {s} mi'
        off = 0.0
        for k, (length, mph) in enumerate(segs):
            note = csum_note or ('' if len(segs) == 1 else f'segment {k+1} of {len(segs)}')
            rows.append(dict(street=street, direction=direction, entry_type='stanza',
                start_point=frm if k == 0 else '', end_point=to if k == len(segs)-1 else '',
                length_miles=length, offset_miles=round(off, 3), speed_mph=mph,
                source_text=src, notes=note))
            off += length
        i = next_i

    for ln in region.split('\n'):
        o = ONELINER.match(ln.strip())
        if o:
            rows.append(dict(street=o.group(1).strip(), direction='', entry_type='oneliner',
                start_point=_clean(o.group(3)), end_point=_clean(o.group(4)),
                length_miles='', offset_miles='', speed_mph=int(o.group(2)),
                source_text=re.sub(r'\s+', ' ', ln.strip()), notes=''))

    return COLS, rows, checksum_fail

if __name__ == '__main__':
    cols, rows, fails = parse()
    w = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    w.writerow(cols)
    for r in rows: w.writerow([str(r.get(c, '')) for c in cols])
    for f in fails:
        print(f"# checksum mismatch: {f[0]} {f[1]} sum={f[2]} total={f[3]}", file=sys.stderr)
