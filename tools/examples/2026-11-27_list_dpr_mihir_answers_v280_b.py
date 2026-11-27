#!/usr/bin/env python3
# apply76b — v280 part 2: DPR 27.11 const, Barge tab, movements.
import sys, re, json, subprocess, datetime as DT
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 27.11'); q = B.q
BASE = DT.datetime(2026, 11, 27, 7, 0)
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def eta(bal, l24):
    t = BASE + DT.timedelta(hours=bal / l24 * 24); m = int(round((t.hour * 60 + t.minute) / 5.0) * 5); t = t.replace(hour=0, minute=0) + DT.timedelta(minutes=m)
    return '%d %s %02d:%02d' % (t.day, 'Nov' if t.month == 11 else 'Dec', t.hour, t.minute)
def R(loc, n, ie, c, l24, upto, bal, g='', hk=0, note='', partial=None, comm=None, **x):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if partial: d['partial'] = 1; d['comm'] = comm
    d.update(x); d['note'] = note; return d
ROWS = [
 R('CJ-1', 'Manta Sena', 'EXP', 'Rice bags', 3757, 6439, 23731, '4/5/4', 13, '3,757 MT in 24 h on 13 hooks — 6,439 loaded, 23,731 left → about ' + eta(23731, 3757) + ' at this rate; list ETC 30 Nov 04:03 · stevedores Trueblue / JKS / Awad / ACT'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 3989, 28051, 4649, '4/4/4', 12, 'rice 2,625 MT (19,351 loaded, 3,149 left) + flour 142 (2,959 / 1,241) + sugar 1,222 (5,741 / 259) — 3,989 MT in 24 h on 12 hooks; 4,649 left → about ' + eta(4649, 3989) + ' at this rate; list ETC 30 Nov 13:50'),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 2762, 25835, 5265, '3/3/4', 10, '2,762 MT in 24 h on 10 hooks — 25,835 loaded, 5,265 left (the DPR now counts against 31,100; the list says "32100 total") → about ' + eta(5265, 2762) + ' at this rate; list ETC 30 Nov 01:58'),
 R('CJ-14', 'Blue Shark', 'EXP', 'Rice bags + wheat flour + sugar bags', 2649, 8876, 14491, '4/4/4', 12, 'printed on the CJ-5 row — rice 1,924 MT (7,076 loaded, 4,668 left) + flour 300 (1,075 / 5,035) + sugar 425 (725 / 4,788) — 2,649 MT in 24 h on 12 hooks, the shift to CJ-14 inside the day; 14,491 left → about ' + eta(14491, 2649) + ' at this rate; list ETC 30 Nov 13:00'),
 R('CJ-6', 'Katerina K', 'EXP', 'Kaolin + bentonite J-bags + soya bean meal', 2936, 2956, 44017, '3/3/3', 9, 'bentonite 2,190 J-bags / 2,936 MT in her first full day on 9 hooks (norm 3,450); 2,956 loaded · left: kaolin 4,981 MT, bentonite 18,436, soya bean meal 20,600 = 44,017 → about ' + eta(44017, 2936) + ' at this rate · stevedore SAS'),
 R('CJ-5', 'Asian Summit', 'IMP', 'Petcoke', 13600, 43600, 16899, '5/4/4', 13, 'printed on the CJ-7 row — 13,600 MT in 24 h on 13 hooks, HALF of the day before (26,200): the shift to CJ-5 is inside this day. 43,600 off, 16,899 left → about ' + eta(16899, 13600) + ' at this rate; list ETC 28 Nov 22:59 · stevedore RSIPL'),
 R('CJ-8', 'Zheng Hui', 'IMP', 'DAP', 12061, 44161, 21839, '2/3/2', 7, '12,061 MT in 24 h on 7 hooks (12,840 the day before; norm 14,950) — 44,161 off, 21,839 left → about ' + eta(21839, 12061) + ' at this rate; list ETC 28 Nov 16:15 · gearless'),
 R('CJ-9', 'Pioneer Fortune', 'EXP', 'Sugar bags', 3440, 5439, 19641, '4/4/4', 12, '3,440 MT in 24 h on 12 hooks — 5,439 loaded, 19,641 left → about ' + eta(19641, 3440) + ' at this rate · stevedore GFPL'),
 R('CJ-13', 'AG Varvara', 'IMP', 'Pine logs', 4200, 8264, 30848, '4/4/4', 12, '30,885 pcs / 4,200 CBM in 24 h on 12 hooks (norm 4,000) — 60,652 pcs / 8,264 CBM off, 225,861 pcs / 30,848 CBM left → about ' + eta(30848, 4200) + ' at this rate; list ETC 5 Dec 08:52 · stevedore RSIPL'),
 R('CJ-14', 'Tug Varahi + barge AKG 11', 'EXP', 'Steel pipes', 2500, 2500, 1311, '1/1/1', 3, 'MADE FAST 10:40, COMMENCED 12:00 on 26 Nov — 420 pipes / 2,500 MT loaded; 220 pipes / 1,311 MT still counted to load at 07:00, while the list of the same hour brackets her as outgoing · stevedore AML', True, '11-26 12:00'),
 R('CJ-15', 'Xin Hai Tong 71', 'IMP', 'Packaged steel & project cargo', 1767, 2700, 3006, '4/4/4', 12, '381 packages / 1,767 MT in 24 h on 12 hooks (910 the day before) — 464 packages / 2,700 MT off, 1,336 packages / 3,006 MT left → about ' + eta(3006, 1767) + ' at this rate · no ETC on the list'),
 R('CJ-15A', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes + windmill blades', 364, 9258, 0, '2/4/0', 6, 'left CJ-16 13:00, re-made fast at CJ-15A 13:48, resumed 15:25; COMPLETED 21:00 on 26 Nov — 54 blades / 1,038 MT + 8,220 MT of I-beams and pipes; LEFT THE BERTH 03:40 on 27 Nov'),
 R('CJ-15A', 'Hai Nam 81', 'EXP', 'Salt in bulk', 0, 0, 52000, '0/0/4', 4, 'MADE FAST 06:18, COMMENCED 07:15 on 27 Nov — nothing by 07:00; 52,000 MT to load · stevedore GFPL · for Vietnam · list: GOV(30K), norm 30,000, ETC 29 Nov 01:54', True, None),
 R('CJ-16', 'MSC Magali', 'IMP', 'Steam coal', 20927, 20927, 79801, '0/3/3', 6, 'MADE FAST 14:54, COMMENCED 16:35 on 26 Nov — 20,927 MT in her first 14½ hours on 6 hooks; 79,801 left · stevedore SSS · gearless · list: HP, norm 50,000, ETC 28 Nov 17:18', True, '11-26 16:35'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 6500, 48113, 9637, '1/1/1', 3, 'mother vessel — 6,500 MT to Sheng Tai in 24 h (11,876 the day before); 48,113 off, 9,637 left'),
 R('MS', 'Sheng Tai', 'EXP', 'Barite ore', 6000, 44213, 11787, '1/1/1', 3, 'daughter vessel, ship-to-ship from African Loon — 6,000 MT in 24 h; 44,213 loaded, 11,787 left'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 1216, 9435, 35533, '2/2/2', 6, 'at midstream 4,350 pcs / 1,216 CBM in 24 h on 6 hooks — 9,435 CBM off, 35,533 left · and 4,606 pcs / 1,288 CBM landed at the barge area'),
 R('MS', 'Aboudi D', 'EXP', 'Rice + sugar bags', 565, 1415, 6725, '1/1/1', 3, 'at midstream rice 368 MT + sugar 197 MT in 24 h — 1,415 loaded, 6,725 left · through OP 1,200 MT of rice and through IFFCO 800 MT of sugar'),
 R('MS', 'MK Lamis', 'EXP', 'Rice bags', 980, 980, 10520, '1/1/1', 3, 'COMMENCED AT MIDSTREAM 14:00 on 26 Nov — 980 MT; 10,520 left on this row (the IFFCO row: 1,625 loaded, nothing in the day)', True, '11-26 14:00'),
 R('MS', 'True Mariner', 'EXP', 'Rice bags', 0, 0, 25000, '', 0, 'made fast at midstream — no cargo yet; 25,000 MT to load · stevedore RSIPL · for Algeria', True, None),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 0, 7872, 9928, '0/0/1', 1, 'nothing at midstream in the day (7,872 loaded, 9,928 left on this row) · 756 MT came through the CJ row — 10,476 loaded, 7,324 left there'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 0, 7350, 2650, '', 0, 'no work — 2,650 MT of rice left (sugar 12,540 complete)'),
 R('MS', 'Crystal O', 'EXP', 'Sugar bags', 200, 27825, 3375, '0/1/1', 2, '200 MT through OP in the day — 27,825 loaded, 3,375 left (the MS row prints no work)'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no work — 4,470 left'),
 R('MS', 'Yara J', 'IMP', 'Rice bags', 2020, 30000, 0, '', 0, '2,020 MT landed at CJ in the day — 30,000 MT, complete'),
 R('BA', 'Coastal Amigo', 'EXP', 'Steel plates', 1091, 1899, 301, '1/1/1', 3, 'at the barge area — 158 plates / 1,091 MT in 24 h; 275 plates / 1,899 MT loaded, 360 plates / 301 MT left · for Dharamtar'),
 R('OJ-1', 'Green Bhavishya (LPG/C)', 'IMP', 'Propane', 10147, 14000, 0, '', 0, 'COMPLETED 19:30, LEFT THE BERTH 23:15 on 26 Nov — 14,000 MT'),
 R('OJ-1', 'Lumis', 'IMP', 'CPO / PFAD', 9220, 9220, 10780, '', 0, 'began at OJ-3 08:12 on 26 Nov; work stopped 21:06, left OJ-3 23:40; RE-MADE FAST AT OJ-1 00:30, resumed 02:00 on 27 Nov — 9,220 MT off; the DPR counts 10,780 left of 20,000, the list has 30,605 MT and ETC 29 Nov 15:24', noPace=1),
 R('OJ-2', 'Thetis Leona', 'IMP', 'Chemicals', 454, 5000, 0, '', 0, 'COMPLETED 11:00, LEFT THE BERTH 14:20 on 26 Nov — 5,000 MT'),
 R('OJ-2', 'MC Hera', 'IMP', 'Chemicals', 13860, 13860, 6740, '', 0, 'MADE FAST 15:36, COMMENCED 18:06 on 26 Nov (printed "HC Hera") — 13,860 MT in 13 hours; 6,740 left', True, '11-26 18:06'),
 R('OJ-3', 'Ginga Merlin', 'IMP', 'Chemicals', 380, 380, 5620, '', 0, 'MADE FAST 02:42, COMMENCED 05:30 on 27 Nov — 380 MT by 07:00; 5,620 left; list ETC 27 Nov 23:22', True, '11-27 05:30'),
 R('OJ-4', 'Ocean Star', 'IMP', 'Chemicals', 5203, 5203, 0, '', 0, 'MADE FAST 12:06, COMMENCED 14:48 on 26 Nov; COMPLETED 04:48 on 27 Nov — 5,203 MT · signal: RT OUT 09:15'),
 R('OJ-6', 'Culture', 'EXP', 'VLSFO', 15667, 29500, 2000, '', 0, '15,667 MT loaded in 24 h — 29,500 on board, 2,000 left (24,000 on the list) → about ' + eta(2000, 15667) + ' at this rate · the list of 07:00 brackets her as outgoing and prints OJ-6 vacant'),
 R('OJ-7', 'Peonia', 'IMP', 'CDSBO', 19054, 19054, 7947, '', 0, 'commenced 07:42 on 26 Nov — 19,054 MT off, 7,947 left → about ' + eta(7947, 19054) + ' at this rate; list ETC 28 Nov 03:20'),
 R('TT-1', 'Blue Ionian', 'IMP', 'Sugar bulk', 13455, 51655, 21700, '', 0, '13,455 MT in 24 h — 51,655 off, 21,700 left → about ' + eta(21700, 13455) + ' at this rate'),
 R('TT-3', 'MP Postpanamax 1', 'IMP', 'Coal in bulk', 25400, 75500, 12500, '', 0, '25,400 MT in 24 h — 75,500 off, 12,500 left → about ' + eta(12500, 25400) + ' at this rate'),
]
a = B.s.index("const DPR={d:'26.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
old = B.s[a:e].split('\n'); ri = next(i for i, l in enumerate(old) if l.startswith(' rows:['))
keep = old[2:ri]
NEWDPR = ("const DPR={d:'27.11.2026',asOf:'11-27 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 27 Nov (xlsx from Mihir, 27 Nov 10:19)',\n"
 " tot:{dry:83431,dryL:26444,dryU:56987,ms:15261,kict:38819,tuna:38855,oj:73985,vad:263598,all:513949,gangs:'PR 29 · TR 4 · 41 + 6W gangs demanded / 41 + 6W supplied',rakes:'2',wb:936,sail:'Lila Tokyo · CJ-14 · 08:10 · Ocean Kudos · CJ-15 · 13:00 · Chemroad Nexus · OJ-4 · 09:40 · Manta Omer Mecit · MS · 05:40'},\n"
 + "\n".join(keep) + ("\n" if keep else "") + " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]

out = subprocess.run(['python3', '-I', '/home/claude/berth-board/tools/barge_from_dpr.py', '/home/claude/work/in27/d27.txt', '27.11', '11-27 07:00'], capture_output=True, text=True).stdout.rstrip('\n')
assert out.startswith("  {d:'27.11'") and out.endswith("]},"), out[-80:]
out = out.replace("n:'Aboudi',", "n:'Aboudi D',").replace("c:'Fertilizer j/bags'", "c:'Fertiliser in J-bags'").replace("ag:'Jm Baxi'", "ag:'JM Baxi'").replace("n:'Darya Priya'", "n:'Dariya Priya'")
print(out)
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + out + "\n")

MVN = ['DPR 27.11 and list 27.11 — the actual hours of 26 / 27 Nov at the cargo jetties', [
 ['08:10', 'OUT', 'Lila Tokyo', 'CJ-14 → OTB', '—', '11-26 08:10', 'sailing block of the DPR (signal 08:00)'],
 ['10:40', 'IN', 'Tug Varahi + barge AKG 11', 'OTB → CJ-14 · 128–134¾', '—', '11-26 10:40', 'made fast 10:40, commenced 12:00'],
 ['13:00', 'SHIFT', 'African Hornbill', 'CJ-16 → CJ-15A · 157½–166¾', '—', '11-26 13:48', 'left CJ-16 13:00, re-made fast 13:48, resumed 15:25'],
 ['13:00', 'OUT', 'Ocean Kudos', 'CJ-15A → OTB', '—', '11-26 13:00', 'sailing block of the DPR'],
 ['14:58', 'IN', 'MSC Magali', 'OTB → CJ-16 · 169½–188', '—', '11-26 14:58', 'made fast 14:58 (DPR 14:54), commenced 16:35 · HP'],
 ['—', 'SHIFT', 'Blue Shark', 'CJ-5 → CJ-14 · 128–141', '—', '11-26 20:00', 'done by 07:00 on 27 Nov (list) — hour not on any paper; est'],
 ['—', 'SHIFT', 'Asian Summit', 'CJ-7 → CJ-5 · 30½–39¼', '—', '11-26 22:00', 'done by 07:00 on 27 Nov (list, "S1 50–57") — hour not on any paper; est'],
 ['01:00', 'OUT', 'Tanjong Pagar 1', 'CJ-11 → OTB', '—', '11-27 01:00', 'container · completed 22:40, left the berth 01:00'],
 ['03:30', 'IN', 'Hui Fa', 'OTB → CJ-11 · 87–95½', '—', '11-27 03:30', 'container · made fast 03:30, commenced 04:20'],
 ['03:40', 'OUT', 'African Hornbill', 'CJ-15A → OTB', '—', '11-27 03:40', 'completed 21:00 on 26 Nov, left the berth 03:40'],
 ['06:18', 'IN', 'Hai Nam 81', 'OTB → CJ-15A · 157½–166¼', '—', '11-27 06:18', 'made fast 06:18, commenced 07:15 · GOV(30K)']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
B.save(); print('saved 76b')
