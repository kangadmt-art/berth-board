#!/usr/bin/env python3
"""barge_from_dpr.py <dpr.txt from parse_xlsx.py> <DD.MM> <asOf 'MM-DD HH:MM'>  →  prints one BARGE.days entry (JS) for the board.
Midstream / barge work as the DPR prints it: ship-side rows (MS, MRG n) per vessel, the shore points where the barges load or land
(CJ, CJ/OP, OP/CJ, OP, IFFCO, BA), and ship-to-ship pairs — rows marked (MV)/(DV) — which are NOT barge work.
IMP = discharge into barges, EXP = loading from barges. Run with python3 -I."""
import re, sys
NAMES = {'TAN BINH 259': 'Tan Bin 259', 'CAPTAINANNIS L': 'Captainannis L', 'CRYSTAL O': 'Crystal O', 'MAK 1': 'Mak 1', 'ARISTON BULKER': 'Ariston Bulker', 'YARA J': 'Yara J', 'AFRICAN LOON': 'African Loon', 'SHENG TAI': 'Sheng Tai'}
def num(x):
    try: return float(str(x).replace(',', ''))
    except Exception: return 0.0
def name(v):
    v = re.sub(r'^M\.?[VT]\.?\s*-?\s*', '', v.strip()); v = re.sub(r'\(\s*(MV|DV|GL)\s*\)', '', v); v = re.sub(r'\s+', ' ', v).strip().upper()
    return NAMES.get(v, v.title())
def cargo(c): return re.sub(r'\s+', ' ', c.strip()).capitalize().replace(' j bags', ' J-bags').replace('j bags', 'J-bags').replace('Npk', 'NPK')
def agent(a): a = a.strip(); return a.upper() if len(a) <= 4 else a.title()
def q(s): return s.replace('\\', '\\\\').replace("'", "\\'")
def main(path, d, asof):
    ship = {}; shore = {}; sts = []; atb = set()
    for ln in open(path, encoding='utf-8'):
        p = [x.strip() for x in ln.rstrip('\n').split(' | ')]
        if len(p) < 13: continue
        loc = p[0].upper(); raw = p[1]
        if re.match(r'^CJ-?\s*\d', loc): atb.add(name(raw)); continue
        if re.match(r'^(MS|MRG)', loc):
            if re.search(r'\(\s*(MV|DV)\s*\)', raw):
                if num(p[6]) > 0: sts.append("%s %s MT" % (name(raw), format(int(round(num(p[6]))), ',')))
                continue
            r = ship.setdefault(name(raw), {'ie': p[2].upper(), 'c': [], 'loc': 'MRG 3' if loc.startswith('MRG') else 'MS', 'l24': 0, 'upto': 0, 'bal': 0, 'ag': p[17] if len(p) > 17 else '', 'st': p[18] if len(p) > 18 else ''})
            r['c'].append(cargo(p[3])); r['l24'] += num(p[6]); r['upto'] += num(p[9]); r['bal'] += num(p[12])
        elif re.match(r'^(CJ$|CJ/OP|OP/CJ|OP$|IFFCO|BA$)', loc) and num(p[6]) > 0:
            shore.setdefault(name(raw), []).append("%s %s" % (p[0].upper().replace('BA', 'Bunder area'), format(int(round(num(p[6]))), ',')))
    rows = []
    for n, r in ship.items():
        if r['l24'] <= 0 and (r['bal'] <= 0 or n in atb): continue        # finished, or gone alongside
        rows.append("   {n:'%s',ie:'%s',c:'%s',loc:'%s',l24:%d,upto:%d,bal:%d,shore:'%s',ag:'%s',st:'%s'}" % (q(n), r['ie'], q(' + '.join(x if i == 0 else x[:1].lower() + x[1:] for i, x in enumerate(dict.fromkeys(r['c'])))), r['loc'], round(r['l24']), round(r['upto']), round(r['bal']), q(' · '.join(shore.get(n, []))), q(agent(r['ag'])), q(r['st'])))
    rows.sort(key=lambda s: -int(re.search(r'l24:(\d+)', s).group(1)))
    print("  {d:'%s',asOf:'%s',sts:'%s',rows:[\n%s\n  ]}," % (d, asof, q(' → '.join(sts)), ",\n".join(rows)))
if __name__ == '__main__': main(*sys.argv[1:4])
