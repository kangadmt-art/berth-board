#!/usr/bin/env python3
"""Compact view of the WAITING LIST and ETA sheets of a parsed berthing list (output of parse_xlsx.py).

Usage:  python3 -I tools/list_summary.py <list.json> [name-regex]
Columns (list 14.11.2026 layout): 0 sr · 1 CJ/OJ/PPP · 3 vessel · 4 arrival draught · 5 LOA · 6 IMP/EXP · 7 cargo · 8 qty · 9 UOM ·
10 reporting (ETA on the ETA sheet) · 11 commercial readiness · 12..19 priority ranks GP, CSTL, HP, SGR, 24H, 8K, STL, GEN · 20 agent · 21 remarks.
A rank cell holds a number (queue place), 'Y' (flag only - no queue place) or 'X' (berthing today).
"""
import sys, json, re
d = json.load(open(sys.argv[1]))
pat = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
K = ['GP', 'CSTL', 'HP', 'SGR', '24H', '8K', 'STL', 'GEN']
for sh in ('WAITING LIST', 'ETA'):
    print('=====', sh)
    for r in d.get(sh, []):
        r = (r + [''] * 23)[:23]
        if not r[3] and not r[0]:
            continue
        if not r[3]:
            print('--', ' | '.join(x for x in r if x)[:120]); continue
        if pat and not pat.search(r[3]):
            continue
        rk = ' '.join(f'{K[i]}:{r[12+i]}' for i in range(8) if r[12 + i])
        t = lambda x: x[5:16] if x[:2] == '20' else x
        print(f"{r[0]:>3}|{r[1]:3}|{r[3][:30]:30}|dr {r[4]:5}|loa {r[5]:7}|{r[6]:3}|{r[7][:34]:34}|{r[8][:14]:14}|rep {t(r[10]):11}|rdy {t(r[11]):11}|{rk:28}|{r[20][:12]:12}|{r[21][:80]}")
