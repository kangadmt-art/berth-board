#!/usr/bin/env python3
# apply19b — v173 (part 2): HP rule list, Tuna, liquid berths, movement log, timber sheet. Documents as in apply19a.
import shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'pre19b.html')
B = Board(P); q = B.q

def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)

# ================= HP: passed-over vessels =================
a, b = B.line_of("const NOHP=new Set(['Orion']);")
B.s = B.s[:a] + ("const NOHP=new Set(['Orion','Gokova-M','Belmoira']); // the HP place goes to the highest MTPD quote of the day, not to the rank (16 Nov). A ranked vessel passed over for a berth she could use is entered here:"
                 " Gokova-M (HP 1) — CJ-7 went to Meghna Prestige (HP 3) at 42,500 on programme 19.11; Belmoira (HP 4) — CJ-16 went to Ocean Kudos, who arrived two days after her. Rome Trader was on it (16 Nov) and berthed under SAAGAR on 18 Nov.") + B.s[b:]

# ================= TUNA =================
TUNA = {
 'src': 'DPA berthing list 18.11.26 (0700, revised) · DPR 19.11, 18.11 and 17.11 — no Tuna row on programme 18.11 or 19.11, none on the signal sheets · TT-2 and TT-4 vacant',
 'berths': [
  {'b': 'TT-3', 'n': 'Beagle', 'c': 'Coal in bulk', 'q': 77220, 'u': 'MT', 'ie': 'IMP', 'loa': 228.99, 'f': '11-16 19:42', 'ag': 'Dariya Shg',
   'prev': 'Mykonos Wave (coal 83,150 MT) — DPR 17.11: completed 12:00, let go 18:06 on 16 Nov', 'next': 'Marvelous Star (coal 50,000 MT, ready 15 Nov 13:18, "TT-03") waits behind',
   'note': 'DPR 17.11: MADE FAST 19:42, commenced 22:50 on 16 Nov (board est 14:30). DPR 19.11: 27,265 MT in 24 h, 62,695 of 77,220 off, 14,525 left → about 19 Nov 19:45 at this rate. Her sailing and Marvelous Star\'s berthing are not on any sheet in hand'},
  {'b': 'TT-1', 'n': 'Europa Graeca', 'c': 'Sugar in bulk', 'q': 75676.64, 'u': 'MT', 'ie': 'IMP', 'loa': 229, 'f': '11-15 06:18', 'ag': 'Gautham Freight',
   'prev': 'Doukato (sugar 82,650 MT) — completed 14 Nov 22:00, let go 15 Nov 04:42', 'next': 'Blue Ionian (ready 3 Nov, TT-01) waits behind',
   'note': 'DPR 19.11: 11,394 MT in 24 h (12,704 and 13,090 the two days before), 46,388 of 75,677 off, 29,289 left → about 21 Nov 20:30 at this rate. LIST 18.11: TT-1 · made fast 15 Nov 06:18 · no norm or ETC printed'}],
 'wait': [
  {'n': 'Blue Ionian', 'c': 'Sugar in bulk', 'q': 73354.82, 'u': 'MT', 'ie': 'IMP', 'loa': 224.94, 'dr': 13.99, 'rep': '11-02 07:48', 'rdy': 'RDY', 'ag': 'Interocean', 'rem': 'TT-01 · ready 3 Nov 11:00 — behind Europa Graeca (about 21 Nov evening at the DPR pace)'},
  {'n': 'Marvelous Star', 'c': 'Coal in bulk', 'q': 50000, 'u': 'MT', 'ie': 'IMP', 'loa': 229, 'dr': None, 'rep': '11-15 13:18', 'rdy': 'RDY', 'ag': 'Atlantic Shg', 'rem': 'TT-03 · reported / ready 15 Nov 13:18 — behind Beagle (about 19 Nov evening at the DPR pace)'}],
 'eta': [
  {'n': 'Woohyun Dream', 'c': 'RSM in bulk', 'q': 31500, 'u': 'MT', 'ie': 'EXP', 'loa': 183, 'eta': '11-21 00:00', 'ag': 'Taurus', 'rem': 'new on list 18.11'},
  {'n': 'MP Postpanamax 1', 'c': 'Coal in bulk', 'q': 88000, 'u': 'MT', 'ie': 'IMP', 'loa': 234.98, 'eta': '11-24 00:00', 'ag': 'Taurus', 'rem': ''}]}
a = B.s.index("const TUNA={"); e = B.s.index("const LIQ={", a)
B.s = B.s[:a] + ("const TUNA={src:" + js(TUNA['src']) + ",\n berths:[\n  " + ",\n  ".join(js(x) for x in TUNA['berths']) + "\n ],\n wait:[\n  " + ",\n  ".join(js(x) for x in TUNA['wait'])
                 + "\n ],\n eta:[\n  " + ",\n  ".join(js(x) for x in TUNA['eta']) + "\n ]};\n") + B.s[e:]

# ================= LIQ =================
def V_(n, c, qv, ie, loa, f, ag, note, **k):
    d = {'n': n, 'c': c, 'q': qv, 'u': 'MT', 'ie': ie, 'loa': loa, 'f': f}
    if k.get('est'): d['est'] = 1
    if k.get('nm'): d['nm'] = k['nm']
    d['rank'] = k.get('rank', ''); d['ag'] = ag
    if k.get('etc'): d['etc'] = k['etc']
    d['note'] = note; return d
def P_(n, c, qv, ie, ag, out, outBy): return {'n': n, 'c': c, 'q': qv, 'u': 'MT', 'ie': ie, 'ag': ag, 'out': out, 'outBy': outBy}
LB = [
 {'b': 'OJ-1', 'prev': P_('Searay', 'CPO', 29999.06, 'IMP', 'JM Baxi', '11-19 08:30', 'signal 19 Nov: OUT 08:30 (Capt Sud) — DPR 19.11: completed 05:42 on the 19th, 29,999 MT (programme 19.11 readiness was 04:00)'), 'now': None,
  'next': V_('Artigo', 'CPO', 24000, 'IMP', 185, '11-19 19:30', 'GAC Shg', 'signal 19 Nov: IN 17:15 (Capt Verma — the hour he boards) → OJ-1, FLOOD → about 19:30 est · programme 19.11: OJ-01 after Searay · list 18.11: CPO 24,000 MT, 10.5 m, reported 7 Nov 14:36, commercially ready 8 Nov, rank "1E"', est=1, rank='1E')},
 {'b': 'OJ-2', 'prev': P_('Korea Chemi', 'Chemicals', 7144.47, 'IMP', 'GAC Shg', '11-19 11:00', 'signal 19 Nov: OUT 11:00 (Capt Madaan) — DPR 19.11: made fast 12:30, commenced 14:20 on 18 Nov, completed 07:25 on the 19th (programme 19.11 readiness was 12:30)'),
  'now': V_('Jeil Crystal', 'Chemicals / base oil', 6635.14, 'IMP', 117.27, '11-19 12:00', 'Wilhelmsen', 'signal 19 Nov: IN 09:30 (Capt Karan — the hour he boards) → OJ-2, behind Korea Chemi\'s 11:00 sailing → about 12:00 est · list 18.11: chemicals 6,635 MT IMP + base oil 1,985 MT EXP, 8.3 m, reported / ready 17 Nov 19:45, rank "1C", REQ OJ 2, 3, 4 · programme 18.11 had named her or Korea Chemi for OJ-2, "whichever comes first"', est=1, rank='1C')},
 {'b': 'OJ-3', 'prev': P_('Stolt Norland', 'Butyl cellosolve', 997.75, 'IMP', 'JM Baxi', '11-17 11:45', 'DPR 18.11: completed 10:05, LET GO 11:45 on 17 Nov (signal 17 Nov: OUT 11:30, Capt Omesh) — she had berthed at OJ-3, not OJ-2 as programmed: made fast 03:06 on the 17th'),
  'now': V_('Jag Pushpa', 'CDSBO', 44252, 'IMP', 183, '11-18 17:00', 'JM Baxi', 'DPR 19.11: SHIFTED FROM OJ-7 on 18 Nov — work stopped 13:00, let go 15:30, re-made fast OJ-3 17:00, re-commenced 18:24 (programme 18.11: "shifting from OJ-07 to OJ-03, A/C of Atlantic Shg" — she made room at OJ-7 for the LPG carrier). She first made fast at OJ-7 on 17 Nov 06:30 and commenced 09:24. 17,276 MT off at OJ-7 and 9,424 at OJ-3 by 0700 on the 19th — about 17,500 MT left at most', nm='650', etc='11-20 08:34')},
 {'b': 'OJ-4', 'prev': P_('Lujain', 'Caustic soda', 21300, 'EXP', 'Atlantic Shg', '11-17 04:00', 'night signal 16 Nov (disp 2005): OUT 04:00 (Capt Rawat) — DPR 17.11: completed 01:42 on the 17th (the programme had 10:00)'),
  'now': V_('Avyaan', 'HSD', 35000, 'IMP', 183.06, '11-17 09:00', 'Victory Shg', 'DPR 19.11: 16,810 MT in 24 h, 31,545 of 35,000 off, 3,455 left → done about noon on the 19th · DPR 18.11: made fast 09:00, commenced 11:00 on 17 Nov', nm='550', rank='1O', etc='11-20 04:38'),
  'out': '11-19 15:00', 'outBy': 'signal 19 Nov: OUT 15:00 (Capt Karan) · programme 19.11: outward readiness 17:00',
  'next': V_('Bow Endeavour', 'Chemicals', 13047.17, 'IMP', 159.03, '11-19 16:30', 'GAC Shg', 'signal 19 Nov: IN 14:00 (Capt Verma — the hour he boards) → OJ-4, behind Avyaan\'s 15:00 sailing → about 16:30 est · list 18.11 (ETA sheet): chemicals 13,047 MT IMP, 6.0 m, ETA / readiness 18 Nov 14:30', est=1)},
 {'b': 'OJ-5', 'prev': P_('Bochem Ghent', 'Phosphoric acid', 21042.06, 'IMP', 'JM Baxi', '11-15 12:30', 'programme 15.11: outward readiness 15 Nov 12:30 · LIST 18.11: OJ-5 "UNDER MAINTENANCE" · DPR 19.11: vacant'), 'now': None},
 {'b': 'OJ-6', 'prev': P_('Ishaan', 'MS', 29822.97, 'IMP', 'Victory Shg', '11-18 17:55', 'DPR 19.11: completed 12:12, LET GO 17:55 on 18 Nov · programme 18.11: outward readiness 17:30'),
  'now': V_('Kestrel', 'VLSFO', 24000, 'EXP', 182.5, '11-18 19:00', 'Malara Shg', 'DPR 19.11: MADE FAST 19:00, commenced 21:00 on 18 Nov — 7,585 MT loaded by 0700, 16,415 left → about 20 Nov 04:30 at that rate · list 18.11: reported / ready 17 Nov 12:54, "OJ-06 B\'TODAY" · programme 18.11: OJ-06, starboard')},
 {'b': 'OJ-7', 'prev': P_('Jag Pushpa', 'CDSBO', 44252, 'IMP', 'JM Baxi', '11-18 15:30', 'DPR 19.11: work stopped 13:00, LET GO 15:30 on 18 Nov — shifted to OJ-3 with about 27,000 MT still on board'),
  'now': V_('NV Sunshine (LPG/C)', 'Propane & butane', 24000, 'IMP', 226, '11-18 20:30', 'Atlantic Shg', 'DPR 19.11: MADE FAST 20:30, commenced 22:12 on 18 Nov — 10,242 MT off by 0700, 13,758 left → about 19 Nov 19:00 at that rate · list 18.11: reported / ready 17 Nov 11:30, "OJ-07 B\'TODAY" · programme 18.11: OJ-07, starboard')}]
def Wt(n, c, qv, loa, dr, rep, rdy, rank, ag, rem, ie='IMP'): return {'n': n, 'c': c, 'q': qv, 'u': 'MT', 'ie': ie, 'loa': loa, 'dr': dr, 'rep': rep, 'rdy': rdy, 'rank': rank, 'ag': ag, 'rem': rem, 'st': ''}
LW = [
 Wt('Artigo', 'CPO', 24000, 185, 10.5, '11-07 14:36', '11-08 11:00', '1E', 'GAC Shg', 'signal 19 Nov: OJ-1 today, IN 17:15 on the flood · the ullage remark is still printed on list 18.11'),
 Wt('Ginga Cheetah', 'CDSBO + CDSFO', 24270, 159.98, 10, '11-08 01:24', None, '', 'Interocean', 'N/A · ullage issue, "commercially ready"'),
 Wt('Silver Gertrude', 'CDSBO', 22500, 183.06, 12.9, '11-08 19:54', '11-15 11:00', '2E', 'Interocean', 'commercially ready 15 Nov · rank "2E" (list 18.11)'),
 Wt('Hafnia Ammolite', 'CDSBO', 30800, 184.06, 10.5, '11-10 07:00', None, '', 'Interocean', 'readiness "18 Nov 11:00 / NR" · ullage issue'),
 Wt('Lumis', 'CPO', 20000, 174.38, 10.7, '11-11 09:00', None, '', 'Atlantic Shg', 'N/A · ullage issue'),
 Wt('Ahinos', 'CPO', 16609.19, 183, 12.65, '11-12 01:30', None, '', 'Marine Links', 'N/A · ullage issue, "commercially ready"'),
 Wt('Peonia', 'CDSBO', 27000, 164.5, 10.4, '11-13 15:42', None, '', 'Interocean', 'readiness "18 Nov 11:00 / NR" · REQ OJ-03, 07 · ullage issue'),
 Wt('Willows', 'MS', 28000, 179.88, 9.1, '11-16 22:36', '11-18 11:00', '1O', 'Atlantic Shg', 'reported 16 Nov 22:36, ready 18 Nov 11:00 · OJ-06 — behind Kestrel'),
 Wt('Sriwangi V', 'CPO', 9999.78, 183.21, 11.6, '11-17 09:18', None, '', 'GAC Shg', 'readiness "18 Nov 11:00 / NR" · ullage issue, "commercially ready"')]
def Et(n, c, qv, loa, dr, eta, ag, rem, ie='IMP'): return {'n': n, 'c': c, 'q': qv, 'u': 'MT', 'ie': ie, 'loa': loa, 'dr': dr, 'eta': eta, 'rdy': None, 'ag': ag, 'rem': rem}
LE = [
 Et('Hatnyanawati', 'Chemicals', 10000, 123.5, 2.7, '11-18 07:12', 'GAC Shg', 'REQ OJ 2, 3, 4', 'EXP'),
 Et('Rasheeda', 'Chemicals', 5000, 114.5, 3.8, '11-18 12:00', 'V Ocean', 'back at OTB since 18 Nov 09:25 (shifted off OJ-2 at her agent\'s request after discharging) — 5,000 MT to load · remark "NOT RESPONDING"', 'EXP'),
 Et('Eva Richway', 'Chemicals', 8627.19, 145.53, 6.43, '11-18 17:00', 'GAC Shg', 'ETA / readiness 18 Nov 17:00'),
 Et('SG Friendship', 'Chemicals', 1999.19, 144.03, None, '11-18 19:00', 'Atlantic Shg', 'new on list 18.11'),
 Et('Hartati', 'Chemicals', 11000, 123.19, 5.7, '11-18 23:00', 'GAC Shg', 'REQ OJ 2, 3, 4', 'EXP'),
 Et('Al Mahboobah', 'Benzene', 9000, 145.53, None, '11-19 00:00', 'Atlantic Shg', 'new on list 18.11', 'EXP'),
 Et('Bow Fortitude', 'Chemicals', 10172.11, 158.93, 8, '11-19 07:00', 'GAC Shg', 'ETA / readiness 19 Nov 07:00'),
 Et('PVT Aurora', 'Chemicals', 5000, 146.19, None, '11-19 12:00', 'Atlantic Shg', ''),
 Et('Ocean Star', 'Chemicals', 5203.21, 145.53, None, '11-21 00:00', 'Atlantic Shg', 'new on list 18.11'),
 Et('Chemroute Pegasus', 'Chemicals', 8708.7, 159.03, None, '11-21 00:00', 'Atlantic Shg', ''),
 Et('Thetis Leona', 'Chemicals', 5000, 146.5, None, '11-21 00:00', 'Wilhelmsen', 'new on list 18.11'),
 Et('SC Draco', 'Methanol', 21336.35, 182.9, 9.9, '11-22 00:00', 'Interocean', ''),
 Et('Chemroad Nexus', 'Chemicals', 5000, 182.99, None, '11-22 00:00', 'Atlantic Shg', ''),
 Et('Bow Tribute', 'Chemicals', 5000, 182.66, 7.1, '11-22 00:00', 'GAC Shg', 'REQ OJ 2, 3, 4 · new on list 18.11'),
 Et('MC Hera', 'Chemicals', 5000, 182.75, None, '11-22 00:00', 'Atlantic Shg', 'new on list 18.11'),
 Et('Ginga Merlin', 'Chemicals', 6000, 147.83, 6, '11-23 00:00', 'GAC Shg', 'REQ OJ 2, 3, 4'),
 Et('Bochem Shangha', 'CPO', 24000, 158.9, 10.2, '11-23 00:00', 'Interocean', 'new on list 18.11'),
 Et('Bogazici (LPG/C)', 'Propane & butane', 24000, 174.2, None, '11-23 18:00', 'Atlantic Shg', 'new on list 18.11'),
 Et('YC Azalea', 'CPO', 20000, 147.83, None, '11-24 02:00', 'Atlantic Shg', 'new on list 18.11'),
 Et('Asian Aurora', 'CPO', 12000, 128, 7.9, '11-24 22:00', 'JM Baxi', ''),
 Et('Rigel', 'CDSBO', 44000, 182.9, 13, '11-26 00:00', 'Interocean', 'OJ-07 · new on list 18.11'),
 Et('Theresa', 'Palm oil', 18399.76, 156.7, None, '11-27 00:00', 'Taurus', 'new on list 18.11'),
 Et('Asia Unity', 'CDSBO', 6930, 177, 7.85, '12-07 00:00', 'Interocean', 'new on list 18.11')]
LM = [
 ['Day signal · 19 Nov (disp 0745 / 1040, Capt Madaan) — oil-jetty rows', [
  ['08:30', 'OUT', 'Searay', 'OJ-1 → OTB', 'Sud', '11-19 08:30', 'CPO complete 05:42 (DPR 19.11)'],
  ['09:30', 'IN', 'Jeil Crystal', 'OTB → OJ-2', 'Karan', '11-19 12:00', 'the hour is the pilot boarding — alongside once Korea Chemi is clear, est'],
  ['11:00', 'OUT', 'Korea Chemi', 'OJ-2 → OTB', 'Madaan', '11-19 11:00', 'completed 07:25 (DPR 19.11)'],
  ['14:00', 'IN', 'Bow Endeavour', 'OTB → OJ-4', 'Verma', '11-19 16:30', 'behind Avyaan — est'],
  ['15:00', 'OUT', 'Avyaan', 'OJ-4 → OTB', 'Karan', '11-19 15:00', 'programme readiness 17:00'],
  ['17:15', 'IN', 'Artigo', 'OTB → OJ-1', 'Verma', '11-19 19:30', 'FLOOD · CPO 24,000 IMP — est']]],
 ['Programme for 19.11 — TF/SH/2102 (issued after the 18 Nov meeting; its header misprints "16-NOV-2026 / movement for 17.11") — oil-jetty rows', [
  ['04:00', 'OUT', 'Searay', 'OJ-1 → OTB', '—', '11-19 08:30', '→ Artigo · signal: 08:30'],
  ['12:30', 'OUT', 'Korea Chemi', 'OJ-2 → OTB', '—', '11-19 11:00', '→ Jeil Crystal · signal: 11:00'],
  ['17:00', 'OUT', 'Avyaan', 'OJ-4 → OTB', '—', '11-19 15:00', '→ Bow Endeavour · signal: 15:00']]],
 ['DPR 19.11 and signal of 18 Nov (disp 2130 on the 17th, amended to 0933) — actual times at the oil jetties, 18 Nov', [
  ['09:25', 'SHIFT', 'Rasheeda', 'OJ-2 → OTB', 'Sandeep', '11-18 09:25', 'completed 08:18 · signal: SHIFT 09:30 "Agent Req" (06:30 struck) — she waits at OTB to load 5,000 MT'],
  ['12:30', 'IN', 'Korea Chemi', 'OTB → OJ-2', 'Sandeep', '11-18 12:30', 'made fast · commenced 14:20 — she, not Jeil Crystal, came first'],
  ['15:30', 'SHIFT', 'Jag Pushpa', 'OJ-7 → OJ-3', '—', '11-18 15:30', 'work stopped 13:00, let go 15:30, re-made fast OJ-3 17:00, re-commenced 18:24 · A/C of Atlantic Shg'],
  ['17:55', 'OUT', 'Ishaan', 'OJ-6 → OTB', '—', '11-18 17:55', 'completed 12:12 · programme readiness 17:30'],
  ['19:00', 'IN', 'Kestrel', 'OTB → OJ-6', '—', '11-18 19:00', 'made fast · commenced 21:00 · VLSFO 24,000 EXP'],
  ['20:30', 'IN', 'NV Sunshine (LPG/C)', 'OTB → OJ-7', '—', '11-18 20:30', 'made fast · commenced 22:12 · propane & butane 24,000 IMP']]],
 ['Programme for 18.11 — TF/SH/2102 (dated 17 Nov) — oil-jetty rows', [
  ['08:10', 'OUT', 'Rasheeda', 'OJ-2 → OTB', '—', '11-18 09:25', '→ Jeil Crystal (ETA 17 Nov 22:30) or Korea Chemi (ETA 20:00), "whichever comes first" · arrival draught 8.30 / 8.70'],
  ['17:30', 'OUT', 'Ishaan', 'OJ-6 → OTB', '—', '11-18 17:55', '→ Kestrel (ETA 17 Nov 15:00), starboard'],
  ['—', 'SHIFT', 'Jag Pushpa', 'OJ-7 → OJ-3', '—', '11-18 15:30', '"SHIFTING FROM OJ-07 TO OJ-03, A/C OF ATLANTIC SHG"'],
  ['—', 'IN', 'NV Sunshine (LPG/C)', 'OTB → OJ-7', '—', '11-18 20:30', 'starboard']]],
 ['Night signal 16 Nov — RE-ISSUE (disp 2005, Capt G Raj), signal 17 Nov, DPR 17.11 / 18.11 — actual times at the oil jetties, 16–17 Nov', [
  ['23:50', 'RT OUT', 'CS Rotterdam', 'OJ-7 → OTB', 'Karan', '11-16 23:50', 'signal 23:34 · completed 21:24'],
  ['01:45', 'RT OUT', 'Maple Castor', 'OJ-3 → OTB', 'Yadav', '11-17 01:45', 'signal 01:30 · completed 21:18 on the 16th — 7½ h before the programme readiness (09:12)'],
  ['02:50', 'OUT', 'Haein Hope', 'OJ-2 → OTB', '—', '11-17 02:50', 'completed 23:00 on the 16th — 4 h before the programme readiness (06:42)'],
  ['03:06', 'IN', 'Stolt Norland', 'OTB → OJ-3', 'Rawat', '11-17 03:06', 'made fast · the programme had OJ-2; the re-issued night sheet sent her to OJ-3'],
  ['04:00', 'OUT', 'Lujain', 'OJ-4 → OTB', 'Rawat', '11-17 04:00', 'completed 01:42 · programme readiness 10:00'],
  ['06:30', 'IN', 'Jag Pushpa', 'OTB → OJ-7', 'Karan', '11-17 06:30', 'signal: IN 02:30, FLOOD · made fast 06:30, commenced 09:24 · CDSBO 44,252 IMP — not on programme 17.11'],
  ['09:00', 'IN', 'Avyaan', 'OTB → OJ-4', 'Yadav', '11-17 09:00', 'made fast · commenced 11:00'],
  ['11:06', 'IN', 'Rasheeda', 'OTB → OJ-2', '—', '11-17 11:06', 'made fast · commenced 13:24 · the programme had OJ-3'],
  ['11:45', 'OUT', 'Stolt Norland', 'OJ-3 → OTB', 'Omesh', '11-17 11:45', 'signal 11:30 · completed 10:05']]]]
a = B.s.index("const LIQ={"); e = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = (B.s[:a] + "const LIQ={src:'DPA berthing list 18.11.26 (0700, revised) · programme 19.11 and 18.11 (TF/SH/2102) · signals to the day sheet of 19 Nov (disp 1040) · DPR 19.11 / 18.11 / 17.11',asOf:'11-19 12:29',\n berths:[\n  "
       + ",\n  ".join(js(x) for x in LB) + "\n ],\n wait:[\n  " + ",\n  ".join(js(x) for x in LW) + "\n ],\n eta:[\n  " + ",\n  ".join(js(x) for x in LE) + "\n ],\n moves:[\n"
       + "".join("  " + js(g) + ",\n" for g in LM) + B.s[e:])

# ================= MV — cargo-jetty movement log =================
MVN = [
 ['Day signal · 19 Nov (disp 0745 / 1040, Capt Madaan)', [
  ['10:00', 'OUT', 'North Gate', 'CJ-2 · 8¾–16½ → OTB', 'Sandeep', '11-19 10:00', 'programme 19.11 had 18:00 on the 18th · 3,060 MT still on the DPR at 0700'],
  ['o/c', 'IN', 'DSM London', 'OTB → CJ-2 · 8½–16½', 'Sandeep', '11-19 12:30', 'BIT(GEN) · rice bags + wheat flour 26,700 EXP · after North Gate — est'],
  ['12:00', 'OUT', 'Senator', '101–109 (KICT) → OTB', 'Karan', '11-19 12:00', 'container, not tracked'],
  ['18:45', 'IN', 'Heng Yuan Fa Zhan', 'OTB → CJ-15A · 161¾–169', 'Deepak', '11-19 21:30', 'PROJ · windmill blades 1,895 IMP · the hour is the pilot boarding; alongside once Bristol is out — est'],
  ['o/c', 'RT OUT', 'HN Doris (salt, next call)', 'CJ-16 · 171¼–188 → OTB', 'Deepak', '11-19 22:00', 'after he berths Heng Yuan Fa Zhan — est · 41,858 MT still to load at 0700'],
  ['20:30', 'RT OUT', 'Bristol (salt, next call)', 'CJ-15A · 158¾–169 → OTB', 'Yadav', '11-19 20:30', 'list ETC / programme readiness 08:28 · 13.3 m'],
  ['o/c', 'IN', 'Ocean Kudos', 'OTB → CJ-16 · 171½–188', 'Yadav', '11-20 00:30', 'HP(42.5K) · salt 70,190 EXP · after HN Doris — est'],
  ['—', '—', 'PMS / standby', 'Capt Sud: on completion 1 hour · Capt Karan 13:30–14:30 · Capt Verma: on completion 1 hour', '—', '11-19 13:30', ''],
  ['—', '—', 'Not on the sheet', 'Truong Minh Dream (list ETC 13:46) and Yara J (24-hr berth, 24 h up at 20:30) — no outward row · no berthing at CJ-3, CJ-4 or CJ-7 (done before 07:30)', '—', '11-19 13:46', '']]],
 ['Programme for 19.11 — TF/SH/2102 (issued after the 18 Nov meeting; received 19 Nov 12:29; its header misprints "DATE: 16-NOV-2026 / MOVEMENT FOR 17.11.2026") — cargo-jetty rows', [
  ['18:00', 'OUT', 'North Gate', 'CJ-2 · 9.5 m', '—', '11-19 10:00', 'NIGHT SAILING · signal: 10:00 on the 19th'],
  ['—', 'IN', 'DSM London', 'OTB → CJ-2 · 8½–16½ · BIT(GEN)', '—', '11-19 12:30', 'NIGHT BERTHING — est'],
  ['03:37', 'OUT', 'Rahma', 'CJ-3 · 8.2 m', '—', '11-19 03:35', 'let go 03:35 (DPR)'],
  ['—', 'WARP', 'Saga Viking', 'CJ-5 · 33–41¾ → 32¾–41½', '—', '11-19 04:00', '"NIGHT WARPING AT PANELS" — est'],
  ['—', 'WARP', 'Truong Minh Dream', 'CJ-6 · 42¾–51½ → 42½–51¼', '—', '11-19 04:00', '"NIGHT WARPING AT PANELS" — est'],
  ['—', 'SHIFT', 'Propel Confidence', 'CJ-7 → 23½–31¾ (CJ-3 / CJ-4)', '—', '11-19 03:40', '"NIGHT SHIFTING FROM CJ-07 TO CJ-03. PORT C." · let go 03:40, re-made fast 05:00 (DPR)'],
  ['—', 'IN', 'Sea Gautham', 'OTB → CJ-3 · 17½–22¼ · SPACE A/C', '—', '11-19 05:40', 'NIGHT BERTHING · made fast 05:40 (DPR)'],
  ['—', 'IN', 'Meghna Prestige', 'OTB → CJ-7 · 52¼–58¾ · HP(42.5K)', '—', '11-19 07:30', '42,500 MTPD · made fast 07:30 (DPR)'],
  ['20:00', 'OUT', 'Feng Hai 98', 'CJ-12 (KICT)', '—', '11-18 20:35', '→ Senator 101–109½ (ETA 18 Nov 19:00) · container, not tracked'],
  ['08:28', 'OUT', 'Bristol (salt, next call)', 'CJ-15A · 13.3 m', '—', '11-19 20:30', 'signal: RT OUT 20:30'],
  ['—', 'IN', 'Heng Yuan Fa Zhan', 'OTB → CJ-15A · 161¾–169 · PROJ', '—', '11-19 21:30', 'est'],
  ['14:19', 'OUT', 'HN Doris (salt, next call)', 'CJ-16 · 14.0 m', '—', '11-19 22:00', 'signal: RT OUT o/c — est'],
  ['—', 'IN', 'Ocean Kudos', 'OTB → CJ-16 · 171½–188 · HP(42.5K)', '—', '11-20 00:30', 'sailing draught 14.1 m — est'],
  ['—', 'IN', 'Bon Voyage', 'OTB → barge berth, north side', '—', '11-18 21:00', 'NIGHT BERTHING · steel slab · made fast 21:00 (DPR)']]],
 ['DPR 19.11 — actual times, 0700 on 18 Nov to 0700 on 19 Nov (no evening signal sheet of 18 Nov in hand)', [
  ['11:10', 'OUT', 'Theometor', 'CJ-14 → OTB', 'Pankaj', '11-18 11:10', 'sailed (DPR sailing list) · signal 11:00 · programme 18.11 readiness 17:00'],
  ['14:45', 'OUT', 'African Peacock', 'CJ-13 · 112½–124½ → OTB', 'Pankaj', '11-18 14:45', 'completed 12:00 · signal 15:00 · list ETC 19 Nov 18:34'],
  ['17:00', 'IN', 'Rome Trader (salt, next call)', 'OTB → CJ-13 · 113–125¼', 'Pankaj', '11-18 17:00', 'MADE FAST · commenced 19:25 · SAAGAR · Mihir & Co'],
  ['19:30', 'OUT', 'Enshi', 'CJ-15 · 142–154¾ → OTB', '—', '11-18 19:30', 'completed 14:30 · programme readiness 17:30 · list ETC 19 Nov 09:34'],
  ['20:30', 'IN', 'Yara J', 'midstream → CJ-14 · 126½–141¾', '—', '11-18 20:30', 'left OTB 16:25 · re-made fast 20:30, re-commenced 21:50 · 24 HRS'],
  ['20:35', 'OUT', 'Feng Hai 98', '102–109½ (KICT) → OTB', '—', '11-18 20:35', 'container, not tracked · Senator made fast 22:35'],
  ['21:45', 'IN', 'ML Egret', 'OTB → CJ-15 · 143½–156¾', '—', '11-18 21:45', 'MADE FAST · commenced 23:35 · SAAGAR'],
  ['03:35', 'OUT', 'Rahma', 'CJ-3 · 17½–25½ → OTB', '—', '11-19 03:35', 'completed 16:15 on the 18th'],
  ['03:40', 'SHIFT', 'Propel Confidence', 'CJ-7 · 52½–58¾ → 23½–31¾', '—', '11-19 03:40', 'work stopped 02:30, let go 03:40 · re-made fast 05:00, re-commenced 06:40 · port convenience'],
  ['05:40', 'IN', 'Sea Gautham', 'OTB → CJ-3 · 17½–22¼', '—', '11-19 05:40', 'MADE FAST · space a/c'],
  ['07:30', 'IN', 'Meghna Prestige', 'OTB → CJ-7 · 52¼–58¾', '—', '11-19 07:30', 'MADE FAST · HP(42.5K)']]],
 ['Signal dated 18/11 (disp 2130 on 17 Nov; amended 0003 Capt Sachin, 0314, 0327, 0919 / 0933 Capt Sandeep)', [
  ['03:00', 'SHIFT', 'Vira 1', '87–95 (KICT) → OTB', 'Sachin', '11-18 03:50', 'container, not tracked · let go 03:50 (DPR)'],
  ['03:00', 'RT OUT', 'Honor Star', 'CJ-9 · 69¼–79¼ → OTB', 'Deepak', '11-18 03:20', '08:30 struck → 03:00 · let go 03:20 (DPR) · coal complete 23:15 on the 17th'],
  ['o/c', 'IN', 'Seacon Monaco', 'OTB → CJ-9 · 69–76¾', 'Deepak', '11-18 06:36', 'GFPL · made fast 06:36 (list 18.11)'],
  ['11:00', 'RT OUT', 'Theometor', 'CJ-14 · 125–139½ → OTB', 'Pankaj', '11-18 11:10', 'sailed 11:10 (DPR)'],
  ['15:00', 'OUT', 'African Peacock', 'CJ-13 · 112–124½ → OTB', 'Pankaj', '11-18 14:45', 'let go 14:45 (DPR)'],
  ['o/c', 'IN', 'Rome Trader (salt, next call)', 'OTB → CJ-13 · 113–125¼', 'Pankaj', '11-18 17:00', 'added by amendment · made fast 17:00 (DPR) · programme 18.11 had named CJ-15']]],
 ['Programme for 18.11 — TF/SH/2102 (dated 17 Nov, after the 11:00 meeting; received 19 Nov 12:29) — cargo-jetty rows', [
  ['08:30', 'OUT', 'Honor Star', 'CJ-9 · 10.8 m', '—', '11-18 03:20', 'signal: 03:00'],
  ['—', 'IN', 'Seacon Monaco', 'OTB → CJ-9 · 69–76¾ · GFPL', '—', '11-18 06:36', ''],
  ['—', 'IN', 'Pioneer Fortune', 'OTB → CJ-10 · 77¾–85¾ · GFPL', '—', '11-18 18:00', 'sugar bags 25,080 EXP — list 18.11 still prints "B\'TODAY"; DPR 19.11 shows CJ-10 VACANT and no signal names her: not berthed by 0700 on the 19th'],
  ['17:00', 'OUT', 'Theometor', 'CJ-14 · 11.3 m', '—', '11-18 11:10', 'signal: 11:00'],
  ['—', 'IN', 'Yara J', 'OTB → CJ-14 · 127–142½ · 24 HRS', '—', '11-18 20:30', 'made fast 20:30 (DPR)'],
  ['17:30', 'OUT', 'Enshi', 'CJ-15 · 6.29 m', '—', '11-18 19:30', 'let go 19:30 (DPR)'],
  ['—', 'IN', 'Rome Trader (salt, next call)', 'OTB → CJ-15 · 145½–157¾ · SGR', '—', '11-18 17:00', 'the 18 Nov signal put her at CJ-13 instead, behind African Peacock; ML Egret took CJ-15']]],
 ['DPR 18.11 and signal of 17 Nov (disp 1250; amended 1345 / 1458 / 1517 / 1750, Capt Madaan) — actual times, 17 Nov', [
  ['08:00', 'IN', 'Honor Star', 'OTB → CJ-9 · 69¼–79¼', 'Rawat', '11-17 08:00', 'made fast · commenced 10:30 · completed 23:15'],
  ['13:07', 'SHIFT', 'North Gate', 'CJ-15A · 156½–164¾ → CJ-2 · 8¾–16½', 'Omesh', '11-17 13:07', 'signal 12:30 · work stopped 11:30, let go 13:07 · re-made fast 14:05, re-commenced 15:50'],
  ['15:30', 'RT OUT', 'Phoenix Coral', 'CJ-4 · 26½–32 → OTB', 'Madaan', '11-17 15:30', 'completed 13:00 — the 24-hr vessel was out in 15½ h'],
  ['15:30', 'SHIFT', 'Truong Minh Dream', 'CJ-6 · 46¾–54½ → 42¾–51½', 'Pathak', '11-17 15:30', 'port convenience'],
  ['16:35', 'RT OUT', 'Cape Venture', 'CJ-7 / CJ-8 · 55¾–67½ → OTB', 'Bali', '11-17 16:35', 'signal 16:30 (17:00 → 16:00 → 16:30) · completed 12:30'],
  ['18:30', 'IN', 'Vishva Bandhan', 'OTB → CJ-8 · 59½–68', 'Madaan', '11-17 18:30', 'made fast · commenced 20:45 · GOV'],
  ['19:15', 'SHIFT', 'Evangelia D', 'CJ-16 · 173½–188 → OTB', 'G. Raj', '11-17 19:15', 'RT OUT 17:15 struck: "(OUT IDLE) VSL NOT READY FOR SAILING" · work stopped 18:00, let go 19:15 with 7,716 MT left'],
  ['19:30', 'IN', 'Propel Confidence', 'OTB → CJ-7 · 52½–58¾', 'Bali', '11-17 19:30', 'made fast · commenced 21:15 · COASTAL'],
  ['20:15', 'OUT', 'Tug Chandra Sun + barge Victoria 251', '15B · 166½–171¾ → OTB', 'G. Raj', '11-17 20:15', 'signal 20:00 · completed 19:00'],
  ['21:12', 'IN', 'HN Doris (salt, next call)', 'OTB → CJ-16 · 171¼–188', 'Verma', '11-17 21:12', 'made fast · commenced 00:30 on the 18th · HP(46K)'],
  ['21:30', 'IN', 'Bristol (salt, next call)', 'OTB → CJ-15A · 158¾–169', 'Bali', '11-17 21:30', 'made fast · commenced 22:30 · HP(46K)'],
  ['—', '—', 'KICT (not tracked)', 'DP World Thamirabarani OUT 18:25 · Feng Hai 98 IN → 102–109½ (made fast 19:45) · Vira 1 OUT 18:30 struck — "postponed due to delay in cargo operation"', '—', '11-17 18:25', '']]],
 ['Night signal · 16 Nov — RE-ISSUE (disp 2005, Capt G Raj; it replaces the 1710 sheet) with the DPR 17.11 times', [
  ['22:00', 'SHIFT', 'African Hornbill', 'CJ-4 · 27¼–36 → OTB', 'G. Raj', '11-16 22:00', 'work stopped 20:20, let go 22:00 · 10,500 MT of ball clay left'],
  ['o/c', 'IN', 'Phoenix Coral', 'OTB → CJ-4 · 26½–32', 'G. Raj', '11-17 00:06', 'made fast 00:06, commenced 02:00'],
  ['22:30', 'OUT', 'Princess Joanna', 'CJ-5 · 37–45¾ → OTB', 'Verma', '11-16 22:40', 'NEW on the re-issue (programme: 08:00 on the 17th) · completed 18:30, let go 22:40'],
  ['o/c', 'IN', 'Saga Viking', 'OTB → CJ-5 · 33–41¾', 'Verma', '11-17 01:24', 'marked "FBB" · made fast 01:24, commenced 04:05'],
  ['24:00', 'RT OUT', 'Bomustafao O', 'CJ-2 · 9–16 → OTB', 'Rawat', '11-17 00:01', 'completed 21:50, let go 00:01'],
  ['01:00', 'OUT', 'Drake Well', 'CJ-1 · 7¼–N → OTB', 'Verma', '11-17 01:40', 'NEW on the re-issue (programme: 07:00) · completed 20:00 on the 16th, let go 01:40 · Mihir & Co'],
  ['o/c', 'IN', 'New Bliss', 'OTB → CJ-1 · 7½–N', 'Karan', '11-17 02:33', 'FLOOD · made fast 02:33, commenced 04:40 · 6.5K'],
  ['05:00', 'RT OUT', 'Leya', 'CJ-9 · 69¼–79½ → OTB', 'Yadav', '11-17 05:20', 'let go 05:20'],
  ['o/c', 'IN', 'Honor Star', 'OTB → CJ-9 · 69¼–79¼', 'Rawat', '11-17 08:00', 'marked "FBB" · made fast 08:00']]]]
B.rep("const MV=[\n", "const MV=[\n" + "".join(" " + js(g) + ",\n" for g in MVN))

# ================= TIMBER =================
B.rep("asOf:'11-16 18:00',etaFromDesk:true,waiting:null,", "asOf:'11-16 18:00',etaFromDesk:false,waiting:null,")
for pfx in (" {n:'African Peacock',cbm:36926,from:'Australia',c:'Pine logs',eta:", " {n:'Enshi',cbm:33134,from:'Australia',c:'Pine logs',eta:", " {n:'Drake Well',cbm:26112,from:'Argentina',c:'Pine logs',eta:"):
    a, b = B.line_of(pfx); B.s = B.s[:a] + B.s[b + 1:]
def T(pfx, d): B.set_line(pfx, " " + js(d) + ",")
T(" {n:'ML Egret',cbm:42886,", {'n': 'ML Egret', 'cbm': 42886, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-06 14:24', 'etb': '11-18', 'comm': '11-18 23:35',
   'note': 'berthed 18 Nov 21:45 at CJ-15 under SAAGAR — on the day the desk gave · DPR 19.11: 2,695 CBM / 7,734 pcs in her first 7½ h · 12.11 m'})
T(" {n:'Uni Blossom',cbm:34870,", {'n': 'Uni Blossom', 'cbm': 34870, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-09 11:36', 'etb': '11-19',
   'note': 'SGR 1 · 8K 3 on list 18.11 — next in the SAAGAR line now that ML Egret has berthed · the desk had 19 Nov · 10.8 m'})
T(" {n:'AG Varvara',cbm:39113,", {'n': 'AG Varvara', 'cbm': 39113, 'from': 'Australia', 'c': 'Pine logs', 'eta': '11-12 07:06', 'etb': '11-24', 'note': 'SGR 3 · GEN 17 on list 18.11 · 199.99 m, 9.0 m'})
T(" {n:'CD Glory',cbm:29158,", {'n': 'CD Glory', 'cbm': 29158, 'from': 'Malaysia', 'c': 'Hardwood logs', 'eta': '11-15 06:42', 'etb': '11-25',
   'note': 'list 18.11 (sheet revised after the 18 Nov meeting): SGR 5 · 8K 8 · GEN 22 — the 6.5K / 8K rank is printed now · 179.9 m, 10.4 m — fits CJ-1, CJ-4, CJ-5'})
T(" {n:'Dariya Priya',cbm:44968,", {'n': 'Dariya Priya', 'cbm': 44968, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-16 09:00', 'etb': '11-29',
   'note': '"Darya Priya" on the desk sheet · list 18.11: reported / ready 16 Nov 09:00 · SGR 7 · 8K 11 · GEN 25 · 11.0 m'})
T(" {n:'African Tiger',cbm:36328,", {'n': 'African Tiger', 'cbm': 36328, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-18 06:30', 'etb': '12-03',
   'note': 'list 18.11: reported 18 Nov 06:30, readiness 18 Nov 11:00 · SGR Y · 8K Y — not ranked yet · 180 m, 10.8 m'})
DONE = [
 {'n': 'African Peacock', 'cbm': 36926, 'pcs': 282103, 'from': 'Australia', 'c': 'Pine logs', 'ag': 'DBC', 'berth': '13', 'pri': 'SAAGAR', 'nor': '10-31 02:06', 'mf': '11-08 23:42', 'comm': '11-09 02:30', 'done': '11-18 12:00', 'out': '11-18 14:45',
  'note': 'stevedore RSIPL · 30½ h inside her list ETC (19 Nov 18:34)'},
 {'n': 'Enshi', 'cbm': 33134, 'pcs': 230822, 'from': 'Australia', 'c': 'Pine logs', 'ag': 'DBC', 'berth': '15', 'pri': 'SAAGAR', 'nor': '11-05 00:18', 'mf': '11-09 17:05', 'comm': '11-09 22:15', 'done': '11-18 14:30', 'out': '11-18 19:30',
  'note': '"Enishi" on the sheets · stevedore RSIPL · began at CJ-4, moved to CJ-15 on 15 Nov · 19 h inside her list ETC (19 Nov 09:34)'},
 {'n': 'Drake Well', 'cbm': 26112, 'from': 'Argentina', 'c': 'Pine logs', 'ag': 'Mihir & Company', 'berth': '1', 'pri': '6.5K', 'nor': '11-05 15:00', 'mf': '11-13 14:00', 'comm': '11-13 15:35', 'done': '11-16 20:00', 'out': '11-17 01:40',
  'note': 'stevedore Mihir · DPA out-turn 26,111 CBM · berthed under the 6,500 CBM priority · best day 7,882 (DPR 15.11) · 20 h inside the list ETC (17 Nov 16:24)'}]
B.rep(" done:[\n", " done:[\n" + "".join(" " + js(d) + ",\n" for d in DONE))
B.rep("const TIMBER={src:\"Kandla Timber Vessel's Position · Mihir & Co timber desk\",d:'16 Nov 1200',upto:'16 Nov 1800, after the berthing meeting (the sheet prints 17.11.26 — a slip)',",
      "const TIMBER={src:\"Kandla Timber Vessel's Position · Mihir & Co timber desk\",d:'16 Nov 1200',upto:'16 Nov 1800, after the berthing meeting (the sheet prints 17.11.26 — a slip) — no desk sheet since; arrivals, ranks and berthing times below are from DPA list 18.11 and DPR 17.11 / 18.11 / 19.11',")
B.save()
