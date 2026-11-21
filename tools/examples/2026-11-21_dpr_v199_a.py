#!/usr/bin/env python3
# apply44a — v199 (part 1, data): DAILY PERFORMANCE REPORT 21.11.2026 (position 0700 on 21 Nov; PDF, received 21 Nov 11:22, no text).
# Actual hours of 20 Nov and the night (Rome Trader left 23:40, Meghna Prestige 02:45, Seacon Monaco completed 07:30 ...), the 24-hour output and balances,
# midstream work (Sea Postman and Dariya Priya have started), Tuna and oil-jetty rows. The meeting call of 21 Nov is FROZEN as v198 published it at 10:45.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
D = 'DPR 21.11'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)
def pre(marker, text): B.note_prefix(marker, q(text) + " ")
def sub(marker, old, new): B.sub_entry(marker, old, new)
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]

# ================= HEADER =================
B.rep("const NOW=h('11-21 10:21');", "const NOW=h('11-21 11:22');")
B.rep("List <b>21.11 · 0700</b> · DPR <b>20.11</b> · Programme <b>21.11</b>", "List <b>21.11 · 0700</b> · DPR <b>21.11</b> · Programme <b>21.11</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 21 Nov 11:22: the DAILY PERFORMANCE REPORT 21.11 (0700) — Rome Trader completed 20:00 and left 23:40 on 20 Nov; Meghna Prestige left 02:45; Seacon Monaco completed 07:30; ML Egret 6,473 CBM in the day (25,854 left); Sea Postman and Dariya Priya have started at midstream; African Hornbill only 803 MT in the day · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='DPR 21.11 (0700) · ")

# ================= DPR const =================
def R(loc, n, ie, c, l24, upto, bal, g='', hk=0, note='', partial=None, comm=None):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if partial: d['partial'] = 1; d['comm'] = comm
    d['note'] = note; return d
ROWS = [
 R('CJ-1', 'New Bliss', 'EXP', 'Sugar bags', 6422, 27928, 6072, '4/4/4', 12, '6,422 MT in 24 h on 12 hooks (7,619 the day before; norm 6,500) — 27,928 loaded, 6,072 left → ~22 Nov 05:40 at this rate, 4½ h inside the list ETC (22 Nov 10:05)'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 4846, 6671, 26029, '4/4/4', 12, 'rice bags 2,199 MT (3,524 loaded, 18,976 left) + wheat flour 874 (1,374 / 2,826) + sugar bags 1,773 (their first day; 4,227 left) — 4,846 MT in 24 h on 12 hooks; 26,029 of 32,700 left → ~26 Nov 16:00 at this rate, four days inside the list ETC (30 Nov 13:50)'),
 R('CJ-4', 'Propel Confidence', 'IMP', 'Iron ore pellets', 5818, 54918, 0, '3/0/0', 3, 'COMPLETED 13:00, LEFT THE BERTH 17:00 on 20 Nov — 54,918 MT'),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 2125, 3525, 28575, '0/3/3', 6, 'at OTB 16:35, MADE FAST 17:50, RE-COMMENCED 20:00 on 20 Nov — 2,125 MT in 11 h on 6 hooks (about 4,600 a day; norm 3,450). The berth row counts 3,525 loaded and 28,575 left of 32,100; the LIST counts 24,750 to load from this berthing (ETC 28 Nov 00:00) — by the list about 22,625 are left', 1, '11-20 20:00'),
 R('CJ-5', 'Saga Viking', 'IMP', 'Kraft pulp', 496, 16038, 0, '1/0/0', 1, 'COMPLETED 08:45, LEFT THE BERTH 11:10 on 20 Nov — 16,038 MT / 7,958 units'),
 R('CJ-5', 'Ken Ann', 'IMP', 'Steel / general cargo', 4939, 4939, 82, '0/3/2', 5, 'MADE FAST 13:50, COMMENCED 15:40 on 20 Nov — 551 units / 4,939 MT by 0700; 8 units / 82 MT left (signalled out 10:30 on the 21st)', 1, '11-20 15:40'),
 R('CJ-6', 'Truong Minh Dream', 'IMP', 'DAP / TSP bulk', 1200, 55600, 0, '1/1/0', 2, 'COMPLETED 15:15, LEFT THE BERTH 18:15 on 20 Nov — 55,600 MT'),
 R('CJ-6', 'Parvraj', 'IMP', 'DAP bulk', 2077, 2077, 47423, '0/0/4', 4, 'MADE FAST 22:50 on 20 Nov, COMMENCED 01:05 on the 21st — 2,077 MT in 6 h on 4 hooks; 47,423 left (norm 14,950, list ETC 24 Nov 08:17)', 1, '11-21 01:05'),
 R('CJ-7', 'Meghna Prestige', 'IMP', 'Coal in bulk', 21050, 60500, 0, '6/6/3', 15, 'COMPLETED 23:30 on 20 Nov, LEFT THE BERTH 02:45 on the 21st — 60,500 MT'),
 R('CJ-8', 'Vishva Bandhan', 'IMP', 'Urea bulk', 10403, 38913, 5085, '4/3/4', 11, '10,403 MT in 24 h (norm 9,258) — 38,913 off, 5,085 left → ~21 Nov 18:45 at this rate, before the hours lost on the shift to CJ-5 (list ETC 22 Nov 14:33)'),
 R('CJ-9', 'Seacon Monaco', 'IMP', 'Soda ash in bulk', 13946, 41000, 0, '6/6/6', 18, 'COMPLETED 07:30 on 21 Nov — 41,000 MT; the let-go hour is left blank (signalled out "on completion" this morning)'),
 R('CJ-13', 'Rome Trader (salt, next call)', 'EXP', 'Salt in bulk', 19631, 55275, 0, '5/5/0', 10, 'COMPLETED 20:00, LEFT THE BERTH 23:40 on 20 Nov — 55,275 MT, the last 19,631 on 10 hooks in two shifts · agent and stevedore Mihir'),
 R('CJ-13', 'Uni Blossom', 'IMP', 'Pine logs', 340, 340, 34529, '0/0/4', 4, 'MADE FAST 02:00, COMMENCED 03:45 on 21 Nov — 1,050 pcs / 340 CBM in her first three hours on 4 hooks; 106,355 pcs / 34,529 CBM left', 1, '11-21 03:45'),
 R('CJ-14', 'Nord Copper', 'EXP', 'Salt in bulk', 21000, 21000, 24010, '4/4/4', 12, 'COMMENCED 12:00 on 20 Nov — 21,000 MT in 19 h on 12 hooks (about 26,500 a day; norm 23,000); 24,010 left → ~22 Nov 04:45 at this rate (list ETC 22 Nov 03:03)', 1, '11-20 12:00'),
 R('CJ-15', 'ML Egret', 'IMP', 'Pine logs', 6473, 17031, 25854, '4/4/4', 12, '18,572 pcs / 6,473 CBM in 24 h on 12 hooks (7,863 the day before; norm 4,600) — 17,031 CBM off, 25,854 left → ~25 Nov 06:50 at this rate, three days inside the list ETC (28 Nov 07:30) · stevedore Mihir'),
 R('CJ-15A', 'Heng Yuan Fa Zhan', 'IMP', 'Windmill blades & accessories', 981, 1313, 582, '2/2/2', 6, '29 units / 981 MT in 24 h on 6 hooks — 39 units / 1,313 MT off, 17 units / 582 MT left → ~21 Nov 21:00 at this rate'),
 R('CJ-16', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes', 803, 909, 10804, '3/3/3', 9, '803 MT in 24 h on 9 hooks — 909 MT loaded in two days, 10,804 left → about 4 Dec at this rate; no norm is printed for her'),
 R('MS', 'Sea Postman', 'IMP', 'Rock phosphate', 8484, 8484, 20016, '1/2/2', 5, 'at OTB since 17 Nov 02:18; COMMENCED AT MIDSTREAM 10:50 on 20 Nov — 8,484 MT into barges in 20 h on 5 hooks (about 10,000 a day); 20,016 left → about 23 Nov morning at this rate, without a berth', 1, '11-20 10:50'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 643, 643, 44325, '1/2/2', 5, 'at OTB since 16 Nov 09:00; COMMENCED AT MIDSTREAM 11:40 on 20 Nov — 2,300 pcs / 643 CBM in 19 h on 5 hooks; 158,548 pcs / 44,325 CBM left · stevedore RSIPL', 1, '11-20 11:40'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 9985, 15200, 42550, '1/1/1', 3, 'mother vessel — ship-to-ship to Sheng Tai (daughter; 10,085 MT on her own row): 9,985 MT in the 24 h, 42,550 left'),
 R('MS', 'Libra', 'EXP', 'Rice bags', 2150, 15747, 7253, '1/1/1', 3, '2,150 MT in 24 h (2,250 into barges at IFFCO) — 7,253 left'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 1260, 4411, 13389, '1/1/2', 4, '1,260 MT in 24 h (1,654 into barges at CJ/OP) — 13,389 left'),
 R('MS', 'Crystal O', 'EXP', 'Sugar bags', 647, 16879, 14321, '1/0/0', 1, '647 MT in 24 h on one gang — 14,321 left'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 0, 6350, 3650, '', 0, 'no work at the ship in the 24 h — rice 6,350 MT done, 3,650 left; 1,177 MT of rice went into barges at CJ/OP; sugar 11,650 of 12,500 at IFFCO'),
 R('MS', 'MAK 1', 'EXP', 'Rice in J-bags', 0, 21088, 800, '', 0, 'no work for the third day — 800 MT left'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no cargo in the 24 h — 4,470 left'),
 R('MS', 'North Gate', 'EXP', 'Chick peas / rice J-bags', 0, 23940, 3060, '', 0, 'no work — 3,060 MT left'),
 R('MRG-3', 'Tan Bin 259', 'EXP', 'NPK in jumbo bags', 2655, 11025, 1312, '2/2/2', 6, '2,655 MT in 24 h — 1,312 left → done about 19:00 on 21 Nov'),
 R('OJ-1', 'Artigo', 'IMP', 'CPO', 11512, 15123, 8877, '', 0, '11,512 MT in 24 h — 15,123 off, 8,877 left → ~22 Nov 01:30 at this rate (list ETC 22 Nov 07:26)'),
 R('OJ-2', 'Jeil Crystal', 'IMP', 'Chemicals / base oil', 2521, 8621, 0, '', 0, 'chemicals COMPLETED 09:45 (6,635 MT); base oil 1,986 MT loaded 10:00–18:45; LEFT THE BERTH 20:00 on 20 Nov'),
 R('OJ-2', 'Hatnyanawati', 'EXP', 'Chemicals', 2980, 2980, 7020, '', 0, 'MADE FAST 21:20, commenced 23:40 on 20 Nov — 2,980 MT loaded in 7⅓ h; 7,020 left', 1, '11-20 23:40'),
 R('OJ-3', 'Jag Pushpa', 'IMP', 'CDSBO', 4155, 44255, 0, '', 0, 'COMPLETED 15:24, LEFT THE BERTH 17:55 on 20 Nov — 44,255 MT'),
 R('OJ-3', 'SG Friendship', 'IMP', 'Chemicals', 4912, 4912, 3260, '', 0, 'MADE FAST 21:06, commenced 23:24 on 20 Nov — 4,912 MT in 7½ h; 3,260 left → about midday on the 21st', 1, '11-20 23:24'),
 R('OJ-4', 'Bow Endeavour', 'IMP', 'Chemicals', 7662, 13047, 0, '', 0, 'COMPLETED 20:54, LEFT THE BERTH 22:00 on 20 Nov — 13,047 MT'),
 R('OJ-4', 'Eva Richway', 'IMP', 'Chemicals', 2750, 2750, 5877, '', 0, 'MADE FAST 23:00 on 20 Nov, commenced 01:24 on the 21st — 2,750 MT in 5½ h; 5,877 left → about 19:00 on the 21st', 1, '11-21 01:24'),
 R('OJ-6', 'Kestrel', 'EXP', 'VLSFO', 1000, 24000, 0, '', 0, 'COMPLETED 08:30, LEFT THE BERTH 10:30 on 20 Nov — 24,000 MT'),
 R('OJ-6', 'Orchids', 'IMP', 'VLSFO', 198, 198, 8402, '', 0, 'MADE FAST 19:48 on 20 Nov, commenced 06:18 on the 21st — 198 MT by 0700; 8,402 left (8,600 MT in all; the list prints 8,000)', 1, '11-21 06:18'),
 R('OJ-7', 'Silver Gertrude', 'IMP', 'CDSBO', 13141, 13141, 9359, '', 0, 'MADE FAST 10:12, commenced 13:30 on 20 Nov — 13,141 MT in 17½ h; 9,359 left → about 19:30 on the 21st (list ETC 22 Nov 02:48)', 1, '11-20 13:30'),
 R('TT-1', 'Europa Graeca', 'IMP', 'Sugar bulk', 10095, 67679, 7998, '', 0, '10,095 MT in 24 h — 67,679 off, 7,998 left → ~22 Nov 02:00 at this rate'),
 R('TT-2', 'Woohyun Dream', 'EXP', 'RSM in bulk', 350, 350, 31150, '', 0, 'MADE FAST 23:35 on 20 Nov, COMMENCED 06:30 on the 21st — 350 MT in the first half hour; 31,150 left', 1, '11-21 06:30'),
 R('TT-3', 'Marvelous Star', 'IMP', 'Coal in bulk', 25260, 31765, 45079, '', 0, '25,260 MT in 24 h — 31,765 off, 45,079 left (76,844 MT in all; the list prints 50,000) → ~23 Nov 02:00 at this rate'),
]
a = B.s.index("const DPR={d:'20.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
NEWDPR = ("const DPR={d:'21.11.2026',asOf:'11-21 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 21 Nov (PDF from Mihir, 21 Nov 11:22)',\n"
 " tot:{dry:147917,dryL:69993,dryU:77924,ms:18494,kict:7350,tuna:35705,oj:50831,vad:327114,all:587411,gangs:'PR 27 · TR 1 · 43 + 6 W gangs demanded / 43 + 6 W supplied',rakes:'3',wb:841,sail:'Sea Gautam · CJ-3 · 08:40 · Eco Oceano CA · SBM-II · 09:30'},\n"
 " // partial:1 = the vessel worked only part of the 24 h — the 24-hour figure is not a day's rate, the projection does not use it; comm = commencement inside the window (dprPace() counts her rate from it once she has six hours of work)\n"
 " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]
# rate actually worked — for the status lines and the Timber tab (the projection rule is unchanged: it skips partial rows)
B.rep("const dprEtc=r=>", "const dprPace=r=>{if(!r||!(r.l24>0))return null;if(r.partial&&r.comm){const hrs=h(DPR.asOf)-h(r.comm);return hrs>=6?r.l24/hrs:null;}return r.l24/24;}; // units per HOUR actually worked; a start-up of under six hours gives no rate (21 Nov, v199: Uni Blossom's first three hours, Woohyun Dream's first half hour)\nconst dprEtc=r=>")
B.rep("function dprLine(n){const r=dprOf(n);if(!r)return '';const e=dprEtc(r);", "function dprLine(n){const r=dprOf(n);if(!r)return '';const pc=dprPace(r),e=(pc&&r.bal>0)?h(DPR.asOf)+r.bal/pc:null;")
B.rep("${e?' · at this rate ~'+fmt(e)+(r.partial?' (partial day, understated)':''):(r.bal===0?' · completed':'')}</small>`;}",
      "${e?' · at this rate ~'+fmt(e)+(r.partial?' (rate counted from her commencement)':''):(r.bal===0?' · completed':(r.partial?' · just commenced — no rate yet':''))}</small>`;}")
B.rep("const eDpr=(dr&&dr.bal>0&&dr.l24>0)?h(DPR.asOf)+dr.bal/(dr.partial&&dr.comm?dr.l24/Math.max(1,h(DPR.asOf)-h(dr.comm)):dr.l24/24):null;",
      "const eDpr=(dr&&dr.bal>0&&dprPace(dr))?h(DPR.asOf)+dr.bal/dprPace(dr):null; // no pace from a start-up of under six hours (dprPace)")

# ================= MSWORK (Barge tab) =================
MS = [
 {'n': 'Sea Postman', 'ie': 'IMP', 'c': 'Rock phosphate', 'loc': 'MS', 'l24': 8484, 'upto': 8484, 'bal': 20016, 'shore': '', 'ag': 'DBC', 'st': 'RSIPL'},
 {'n': 'Tan Bin 259', 'ie': 'EXP', 'c': 'NPK in jumbo bags', 'loc': 'MRG 3', 'l24': 2655, 'upto': 11025, 'bal': 1312, 'shore': 'Bunder area 2,655', 'ag': 'DBC', 'st': 'RSIPL'},
 {'n': 'Libra', 'ie': 'EXP', 'c': 'Rice bags', 'loc': 'MS', 'l24': 2150, 'upto': 15747, 'bal': 7253, 'shore': 'IFFCO 2,250', 'ag': 'DBC', 'st': 'TRS'},
 {'n': 'Captainannis L', 'ie': 'EXP', 'c': 'Rice bags', 'loc': 'MS', 'l24': 1260, 'upto': 4411, 'bal': 13389, 'shore': 'CJ/OP 1,654', 'ag': 'Act Infraport', 'st': 'TRUEBLUE/TSAS'},
 {'n': 'Crystal O', 'ie': 'EXP', 'c': 'Sugar bags', 'loc': 'MS', 'l24': 647, 'upto': 16879, 'bal': 14321, 'shore': '', 'ag': 'DBC', 'st': 'RSIPL/GFPL'},
 {'n': 'Dariya Priya', 'ie': 'IMP', 'c': 'Pine logs (CBM)', 'loc': 'MS', 'l24': 643, 'upto': 643, 'bal': 44325, 'shore': '', 'ag': 'DBC', 'st': 'RSIPL'},
 {'n': 'Fortunelit', 'ie': 'EXP', 'c': 'Rice bags', 'loc': 'MS', 'l24': 0, 'upto': 6350, 'bal': 3650, 'shore': 'CJ/OP 1,177', 'ag': 'An Line', 'st': 'TSAS'},
 {'n': 'Ariston Bulker', 'ie': 'EXP', 'c': 'Bentonite J-bags', 'loc': 'MS', 'l24': 0, 'upto': 3530, 'bal': 4470, 'shore': '', 'ag': 'Ambica', 'st': 'INAYAT'},
 {'n': 'Mak 1', 'ie': 'EXP', 'c': 'Rice in J-bags', 'loc': 'MS', 'l24': 0, 'upto': 21088, 'bal': 800, 'shore': '', 'ag': 'Samsara', 'st': 'INAYAT'},
 {'n': 'North Gate', 'ie': 'EXP', 'c': 'Chick peas / rice J-bags', 'loc': 'MS', 'l24': 0, 'upto': 23940, 'bal': 3060, 'shore': '', 'ag': 'J M Baxi', 'st': 'J M BAXI'},
]
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n  {d:'21.11',asOf:'11-21 07:00',sts:'African Loon 9,985 MT → Sheng Tai 10,085 MT',rows:[\n   " + ",\n   ".join(js(r) for r in MS) + "\n  ]},\n")

# ================= V — hours and notes =================
M = "{b:'13',n:'Rome Trader (salt, next call)',nm:23000,p:[113,125.25]"
pre(M, "MIHIR & COMPANY · " + D + ": COMPLETED 20:00, LEFT THE BERTH 23:40 on 20 Nov — 55,275 MT, the last 19,631 MT on 10 hooks in two shifts; fifty minutes ahead of the programmed 00:30 and five hours inside her list ETC (04:40).")
sub(M, "f:'11-18 17:00',t:'11-21 00:30',lt:'11-21 04:40'", "f:'11-18 17:00',t:'11-20 23:40',lt:'11-21 04:40'")
M = "{b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75]"
pre(M, D + ": COMPLETED 23:30 on 20 Nov, LEFT THE BERTH 02:45 on the 21st — 60,500 MT (21,050 on the last day, 15 hooks). The board had estimated 04:00.")
sub(M, "t:'11-21 04:00',lt:'11-20 19:39',est:1", "t:'11-21 02:45',lt:'11-20 19:39'")
M = "{b:'5',n:'Saga Viking',nm:3450,p:[32.75,41.5]"
pre(M, D + ": COMPLETED 08:45, LEFT THE BERTH 11:10 on 20 Nov — 16,038 MT / 7,958 units.")
sub(M, "f:'11-17 01:24',t:'11-20 11:00',lt:'11-21 18:58'", "f:'11-17 01:24',t:'11-20 11:10',lt:'11-21 18:58'")
pre("{b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75]", D + ": COMPLETED 13:00, LEFT THE BERTH 17:00 on 20 Nov — 54,918 MT in all.")
pre("{b:'6',n:'Truong Minh Dream',nm:14950,p:[42.5,51.25]", D + ": COMPLETED 15:15, LEFT THE BERTH 18:15 on 20 Nov — 55,600 MT.")
pre("{b:'9',n:'Seacon Monaco',nm:20000,p:[69,76.75]", D + ": COMPLETED 07:30 on 21 Nov — 13,946 MT on the last day (18 hooks), 41,000 MT in all; the let-go hour is left blank.")
pre("{b:'5',n:'Ken Ann',p:[33.5,41.5]", D + ": 551 units / 4,939 MT by 0700 on 21 Nov — only 8 units / 82 MT left; made fast 13:50, commenced 15:40 on the 20th.")
pre("{b:'4',n:'Safi Alfa',nm:3450,p:[23,31.75]", D + ": at OTB 16:35, MADE FAST 17:50, RE-COMMENCED 20:00 on 20 Nov — 2,125 MT in 11 h on 6 hooks (about 4,600 a day against the 3,450 norm). The DPR's berth row counts 28,575 MT left of 32,100; the list counts 24,750 to load from this berthing — by the list about 22,625 are left.")
pre("{b:'6',n:'Parvraj',nm:14950,p:[43,51.25]", D + ": 2,077 MT in her first 6 h on 4 hooks (commenced 01:05); 47,423 left.")
pre("{b:'8',n:'Vishva Bandhan',nm:9258,p:[59.5,68]", D + ": 10,403 MT in 24 h on 11 hooks (norm 9,258) — 38,913 off, 5,085 left at 0700 on 21 Nov.")
pre("{b:'5',n:'Vishva Bandhan',nm:9258,p:[33.25,41.5]", D + ": 5,085 MT left at 0700 — about 18:45 on 21 Nov at the day's rate (10,403), plus the hours lost on the shift; list ETC 22 Nov 14:33.")
pre("{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]", D + ": 1,050 pcs / 340 CBM in her first three hours on 4 hooks (third shift); 106,355 pcs / 34,529 CBM left — too early for a rate.")
pre("{b:'14',n:'Nord Copper',nm:23000,p:[126.5,141.75]", D + ": 21,000 MT in 19 h on 12 hooks since she commenced at 12:00 on 20 Nov (about 26,500 a day; norm 23,000) — 24,010 left → about 22 Nov 04:45, close to the list ETC (03:03).")
pre("{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]", D + ": 18,572 pcs / 6,473 CBM in 24 h on 12 hooks (7,863 the day before) — 17,031 CBM off, 25,854 left → about 25 Nov 06:50 at this rate (it was 24 Nov 09:40 on DPR 20.11); list ETC 28 Nov 07:30 · stevedore Mihir.")
pre("{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]", D + ": 29 units / 981 MT in 24 h on 6 hooks — 39 units / 1,313 MT off, 17 units / 582 MT left → about 21 Nov 21:00 at this rate: the board's 21:30 holds.")
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, D + ": only 803 MT in the full 24 h on 9 hooks — 909 MT loaded in two days, 10,804 left. At this rate she is alongside until about 4 DEC (no norm is printed, so there is no permissible time to cut her short). The board's 24 Nov was a guess made before her first full day; it now carries the DPR pace, to be re-read with every DPR.")
sub(M, "f:'11-20 00:30',t:'11-24 04:00',est:1", "f:'11-20 00:30',t:'12-04 18:00',est:1")
M = "{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]"
pre(M, D + ": rice bags 2,199 MT (18,976 left) + wheat flour 874 (2,826 left) + SUGAR BAGS 1,773 on their first day (4,227 left) — 4,846 MT in 24 h on 12 hooks; 26,029 of 32,700 left → about 26 Nov 16:00 at this rate, four days inside the list ETC (30 Nov 13:50).")
sub(M, "c:'Rice bags + wheat flour',q:26700,u:'MT'", "c:'Rice bags + wheat flour + sugar bags',q:32700,u:'MT'")
pre("{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]", D + ": 6,422 MT in 24 h on 12 hooks (7,619 the day before) — 27,928 loaded, 6,072 left → about 22 Nov 05:40 at this rate; list ETC 22 Nov 10:05.")
pre("{b:'14',n:'Yara J',p:[126.5,141.75]", D + ": a row is printed for her without a berth number (\"CJ\") — rice bags 216 MT in the 24 h, 12,168 / 17,832 on the sheet. It does not agree with DPR 20.11 (26,600 off, 3,400 left when she left CJ-14); read as barge work landed at the cargo jetty. She is not on list 21.11.")

# ================= W notes =================
def w(name, text, **k):
    B.list_tag = D; B.wrow(name, q(text), **k)
w('Sea Postman', "DISCHARGING AT MIDSTREAM since 10:50 on 20 Nov — 8,484 MT into barges in 20 h on 5 hooks (about 10,000 a day); 20,016 left → done about 23 Nov morning WITHOUT a berth; the clay (40,000 MT, True Blue) is to load after that")
w('Dariya Priya', "AT MIDSTREAM since 11:40 on 20 Nov — 2,300 pcs / 643 CBM in 19 h on 5 hooks; 44,325 CBM left. At that rate the midstream work hardly shortens her stay at a berth")
w('Tan Bin 259', "2,655 MT in 24 h at MRG 3 — 1,312 left → done about 19:00 on 21 Nov")
w('Libra', "2,150 MT in 24 h at midstream — 7,253 left")
w('Captainannis L', "1,260 MT in 24 h at midstream — 13,389 left")
w('Crystal O', "647 MT in 24 h at midstream — 14,321 left")

# ================= TIMBER notes =================
B.rep("{n:'ML Egret',cbm:42886,from:'New Zealand',c:'Pine logs',eta:'11-06 14:24',etb:'11-18',comm:'11-18 23:35',note:'",
      "{n:'ML Egret',cbm:42886,from:'New Zealand',c:'Pine logs',eta:'11-06 14:24',etb:'11-18',comm:'11-18 23:35',note:'" + q(D + ": 18,572 pcs / 6,473 CBM in 24 h on 12 hooks (7,863 the day before) — 17,031 off, 25,854 left → about 25 Nov 06:50 · stevedore Mihir · "))
B.rep("etb:'11-20',comm:'11-21 03:45',note:'", "etb:'11-20',comm:'11-21 03:45',note:'" + q(D + ": 1,050 pcs / 340 CBM in her first three hours on 4 hooks; 34,529 left — no rate yet · "))
B.rep("{n:'Dariya Priya',cbm:44968,from:'New Zealand',c:'Pine logs',eta:'11-16 09:00',etb:'11-30',note:'", "{n:'Dariya Priya',cbm:44968,from:'New Zealand',c:'Pine logs',eta:'11-16 09:00',etb:'11-30',note:'" + q(D + ": at midstream 2,300 pcs / 643 CBM in 19 h on 5 hooks (stevedore RSIPL) — 44,325 CBM left · "))

# ================= MV =================
MVN = ['DPR 21.11 — actual hours at the cargo jetties, 20 Nov and the night', [
  ['11:10', 'OUT', 'Saga Viking', 'CJ-5 → OTB', '—', '11-20 11:10', 'completed 08:45, left the berth 11:10 (signal: 11:00)'],
  ['17:00', 'OUT', 'Propel Confidence', 'CJ-4 → OTB', '—', '11-20 17:00', 'completed 13:00, left the berth 17:00'],
  ['17:50', 'IN', 'Safi Alfa', 'OTB → CJ-4', '—', '11-20 17:50', 'at OTB 16:35, made fast 17:50, re-commenced 20:00'],
  ['18:15', 'OUT', 'Truong Minh Dream', 'CJ-6 → OTB', '—', '11-20 18:15', 'completed 15:15, left the berth 18:15'],
  ['23:40', 'OUT', 'Rome Trader', 'CJ-13 → OTB', '—', '11-20 23:40', 'completed 20:00, left the berth 23:40 — programme 21.11: 00:30 · Mihir & Co'],
  ['02:45', 'OUT', 'Meghna Prestige', 'CJ-7 → OTB', '—', '11-21 02:45', 'completed 23:30 on the 20th, left the berth 02:45 (board est 04:00)'],
  ['01:50', 'OUT', 'Arrabbiata', 'CJ-11 → OTB', '—', '11-21 01:50', 'containers complete 19:51 on the 20th, left the berth 01:50'],
  ['07:30', '—', 'Seacon Monaco', 'CJ-9 · cargo complete', '—', '11-21 07:30', 'completed 07:30 — let-go hour blank on the sheet']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")

# ================= LIQ =================
def split_top(body):
    parts, depth, instr, esc, cur = [], 0, False, False, ''
    for ch in body:
        if instr:
            cur += ch
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == "'": instr = False
            continue
        if ch == "'": instr = True; cur += ch; continue
        if ch in '{[': depth += 1
        elif ch in '}]': depth -= 1
        if ch == ',' and depth == 0: parts.append(cur); cur = ''
        else: cur += ch
    if cur: parts.append(cur)
    return [[p[:p.index(':')], p[p.index(':') + 1:]] for p in parts]
def obj(text): return dict(split_top(text[1:-1]))
def unobj(d, order): return '{' + ','.join(k + ':' + d[k] for k in order if k in d) + '}'
NOWKEYS = ('n', 'c', 'q', 'u', 'ie', 'loa', 'f', 'est', 'nm', 'rank', 'ag', 'etc', 'note')
def berth(bid, nown, add, prevn=None, out=None, outBy=None, q_=None):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]
    tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln
    d = dict(split_top(core[3:-1]))
    if set(d) - {'b', 'prev', 'now'}: B.die('berth extra keys: ' + bid + str(list(d)))
    now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    now['note'] = "'" + q(D + ': ' + add + ' · ') + now['note'][1:]
    if q_ is not None: now['q'] = repr(q_)
    d['now'] = unobj(now, NOWKEYS)
    if prevn:
        pv = obj(d['prev']); assert prevn in pv['n'], (prevn, pv['n'])
        pv['out'] = js(out); pv['outBy'] = js(outBy)
        d['prev'] = unobj(pv, ('n', 'c', 'q', 'u', 'ie', 'ag', 'out', 'outBy'))
    B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in ('b', 'prev', 'now')) + '}' + tail + B.s[b:]
berth('OJ-1', 'Artigo', '11,512 MT in 24 h — 15,123 off, 8,877 left → about 22 Nov 01:30 at this rate (list ETC 07:26)')
berth('OJ-2', 'Hatnyanawati', '2,980 MT loaded by 0700 (commenced 23:40), 7,020 left', 'Jeil Crystal', '11-20 20:00', 'DPR 21.11: chemicals completed 09:45 (6,635 MT), base oil 1,986 MT loaded 10:00–18:45, LEFT THE BERTH 20:00 on 20 Nov (signal: RT OUT 19:00)')
berth('OJ-3', 'SG Friendship', '4,912 MT off in 7½ h, 3,260 left → about midday on 21 Nov, half a day inside the list ETC', 'Jag Pushpa', '11-20 17:55', 'DPR 21.11: completed 15:24, LEFT THE BERTH 17:55 on 20 Nov — 44,255 MT (signal: OUT 17:45)')
berth('OJ-4', 'Eva Richway', '2,750 MT off in 5½ h, 5,877 left → about 19:00 on 21 Nov', 'Bow Endeavour', '11-20 22:00', 'DPR 21.11: completed 20:54, LEFT THE BERTH 22:00 on 20 Nov — 13,047 MT (signal: RT OUT 22:00)')
berth('OJ-6', 'Orchids', 'MADE FAST 19:48 on 20 Nov — the DPR confirms the date · commenced 06:18 on the 21st, 198 MT by 0700, 8,402 left (8,600 MT in all)', 'Kestrel', '11-20 10:30', 'DPR 21.11: completed 08:30, LEFT THE BERTH 10:30 on 20 Nov — 24,000 MT (programme 20.11: 11:00)', q_=8600)
berth('OJ-7', 'Silver Gertrude', '13,141 MT off in 17½ h, 9,359 left → about 19:30 on 21 Nov, well inside the list ETC')
LMN = ['DPR 21.11 — actual hours at the oil jetties, 20 Nov', [
  ['10:30', 'OUT', 'Kestrel', 'OJ-6 → OTB', '—', '11-20 10:30', 'completed 08:30, left the berth 10:30 (programme 20.11: 11:00)'],
  ['17:55', 'OUT', 'Jag Pushpa', 'OJ-3 → OTB', '—', '11-20 17:55', 'completed 15:24, left the berth 17:55 (signal: 17:45)'],
  ['20:00', 'OUT', 'Jeil Crystal', 'OJ-2 → OTB', '—', '11-20 20:00', 'chemicals complete 09:45, base oil loaded 10:00–18:45, left the berth 20:00 (signal: 19:00)'],
  ['22:00', 'OUT', 'Bow Endeavour', 'OJ-4 → OTB', '—', '11-20 22:00', 'completed 20:54, left the berth 22:00 (signal: 22:00)']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LMN) + ",\n" + B.s[mm:]
B.rep("const LIQ={src:'DPA berthing list 21.11.26 (0700) · DPR 20.11 · programme 21.11 (TF/SH/2102) · signals to the day sheet of 21 Nov (disp 0746 — no oil-jetty row on it)',asOf:'11-21 10:21',",
      "const LIQ={src:'DPA berthing list 21.11.26 (0700) · DPR 21.11 · programme 21.11 (TF/SH/2102) · signals to the day sheet of 21 Nov (disp 0746 — no oil-jetty row on it)',asOf:'11-21 11:22',")

# ================= TUNA =================
B.rep("next:'Blue Ionian (ready 3 Nov, TT-01) waits behind',note:'", "next:'Blue Ionian (ready 3 Nov, TT-01) waits behind',note:'" + q(D + ": 10,095 MT in 24 h, 67,679 of 75,677 off, 7,998 left → about 22 Nov 02:00 at this rate. "))
B.rep("next:'nobody named — MP Postpanamax 1 (coal 88,000 MT) is expected on 22 Nov 17:30',note:'", "next:'nobody named — MP Postpanamax 1 (coal 88,000 MT) is expected on 22 Nov 17:30',note:'" + q(D + ": 25,260 MT in 24 h — 31,765 off, 45,079 left (76,844 MT in all) → about 23 Nov 02:00 at this rate. "))
B.rep("prev:'vacant on every list since 10 Nov',next:'nobody named',note:'", "prev:'vacant on every list since 10 Nov',next:'nobody named',note:'" + q(D + ": 350 MT loaded by 0700 (commenced 06:30) — 31,150 left. "))
B.rep("rem:'TT-01 · ready 3 Nov 11:00 — behind Europa Graeca (about 21 Nov night at the DPR 20.11 pace)'", "rem:'TT-01 · ready 3 Nov 11:00 — behind Europa Graeca (about 22 Nov 02:00 at the DPR 21.11 pace)'")
B.rep("const TUNA={src:'DPA berthing list 21.11.26 (0700) · DPR 20.11 · programme 21.11 · TT-2 Woohyun Dream made fast 20 Nov 23:35 · TT-4 vacant'",
      "const TUNA={src:'DPA berthing list 21.11.26 (0700) · DPR 21.11 · programme 21.11 · TT-2 Woohyun Dream made fast 20 Nov 23:35 · TT-4 vacant'")

# ================= the 21 Nov meeting call — frozen as published before the meeting (v198, 10:45) =================
setline("const CALL_FROZEN=null;", "const CALL_FROZEN={d:'11-21',at:'11-21 10:21',basis:'list 21.11 · HM signal 21 Nov (disp 07:46) · DPR 20.11',call:[['Blue Shark','15A'],['Manta Sena','1'],['Xin Hai Tong 71','14']]}; // {d,at,basis,call} = the meeting call as it stood BEFORE the meeting. 21 Nov: v198 was published at 10:45, before the 11:00 meeting; DPR 21.11 reached the board at 11:22, after it — the call is not rebuilt. Use this call for the MEETLOG entry when programme 22.11 comes, then set it back to null (= show the live call).")
B.save()
