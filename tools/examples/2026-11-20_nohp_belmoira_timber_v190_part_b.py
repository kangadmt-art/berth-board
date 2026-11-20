#!/usr/bin/env python3
# apply35b — v190 (part 2): Belmoira is a Sr No 7 quote vessel, not an HP vessel (NOHP) — so the board does not invent a shift of Uni Blossom to seat her;
# timber rows refreshed from programme 21.11 and the revised list 20.11.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
B.rep("const NOHP=new Set(['Orion','Gokova-M','Lila Tokyo']);", "const NOHP=new Set(['Orion','Gokova-M','Lila Tokyo','Belmoira']);")
a, b = B.line_of("const NOHP=new Set([")
B.s = B.s[:b] + " Belmoira (20 Nov, v190): back on the list — her programmed berth (CJ-15 as GOVT(30K)) was not vacated and her at-berth row is taken out of the revised list 20.11; she is a Sr No 7 quote vessel placed against a vacant Govt / Coastal / 24-hr place, not an HP vessel — left as HP the engine shifted Uni Blossom out of CJ-13 for her the day after she berths." + B.s[b:]
def T(pfx, d): B.set_line(pfx, " " + js(d) + ",")
T(" {n:'Uni Blossom',cbm:34870,", {'n': 'Uni Blossom', 'cbm': 34870, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-09 11:36', 'etb': '11-20',
   'note': 'desk 20 Nov, after the meeting: will berth 20 Nov 23:00 under Saagar · PROGRAMME 21.11: CJ-13, 113–124¾, NIGHT BERTHING behind Rome Trader (out 21 Nov 00:30) — about 02:30 on 21 Nov · revised list 20.11: SGR 1 · 8K 4 · 10.8 m'})
T(" {n:'AG Varvara',cbm:39113,", {'n': 'AG Varvara', 'cbm': 39113, 'from': 'Australia', 'c': 'Pine logs', 'eta': '11-12 07:06', 'etb': '11-26', 'note': 'desk ETB 26 Nov (24 Nov on the sheet of 16 Nov) · revised list 20.11: SGR 2 · GEN 16 — next in the SAAGAR line · 199.99 m, 9.0 m'})
T(" {n:'CD Glory',cbm:29158,", {'n': 'CD Glory', 'cbm': 29158, 'from': 'Malaysia', 'c': 'Hardwood logs', 'eta': '11-15 06:42', 'etb': '11-26',
   'note': 'desk ETB 26 Nov (25 Nov on the sheet of 16 Nov) · revised list 20.11: SGR 4 · 8K 9 · GEN 20 · 179.9 m, 10.4 m — fits CJ-1, CJ-4, CJ-5'})
T(" {n:'Dariya Priya',cbm:44968,", {'n': 'Dariya Priya', 'cbm': 44968, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-16 09:00', 'etb': '11-30',
   'note': '"Darya Priya" on the desk sheet · desk ETB 30 Nov (29 Nov before) · revised list 20.11: SGR 5 · 8K 10 · GEN 21 · 11.0 m'})
T(" {n:'African Tiger',cbm:36328,", {'n': 'African Tiger', 'cbm': 36328, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-18 06:30', 'etb': '12-03',
   'note': 'desk: arrived 18 Nov 11:00, ETB 3 Dec · revised list 20.11: SGR 6 · 8K 11 · GEN 25 · reported 18 Nov 06:30 · 180 m, 10.8 m'})
B.save()
