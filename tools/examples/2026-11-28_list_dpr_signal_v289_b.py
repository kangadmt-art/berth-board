#!/usr/bin/env python3
# apply85b — v289 part 2: DPR 28.11 const, Barge tab, movements, stevedores.
import sys, re, json, subprocess, datetime as DT
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 28.11'); q = B.q
BASE = DT.datetime(2026, 11, 28, 7, 0)
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
 R('CJ-1', 'Manta Sena', 'EXP', 'Rice bags', 4461, 10900, 19270, '5/5/5', 15, '4,461 MT in 24 h on 15 hooks (3,757 the day before) — 10,900 loaded, 19,270 left → about ' + eta(19270, 4461) + ' at this rate; list ETC 30 Nov 04:03 · stevedores Trueblue / JKS / Awad / ACT'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 2301, 30352, 2348, '4/4/4', 12, 'rice 1,900 MT (21,251 loaded, 1,249 left) + flour 142 (3,101 / 1,099) + sugar 259 (6,000, complete) — 2,301 MT in 24 h on 12 hooks; 2,348 left → about ' + eta(2348, 2301) + ' at this rate; list ETC 30 Nov 13:50'),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 3301, 29136, 2964, '4/4/4', 12, '3,301 MT in 24 h on 12 hooks — 29,136 loaded, 2,964 left → about ' + eta(2964, 3301) + ' at this rate; list ETC 30 Nov 01:58'),
 R('CJ-14', 'Blue Shark', 'EXP', 'Rice bags + wheat flour + sugar bags', 1803, 10679, 15803, '2+1+1 a shift', 12, 'THE DAY OF THE SHIFT — work stopped at CJ-5 19:35, left 20:25; re-made fast at CJ-14 21:15 on 27 Nov, resumed 02:40 on 28 Nov. Rice 855 MT + flour 773 + sugar 175 = 1,803 MT; 10,679 loaded, 15,803 left → at the earlier 2,650 a day about ' + eta(15803, 2650) + '; list ETC 30 Nov 13:00', noPace=1),
 R('CJ-5', 'Asian Summit', 'IMP', 'Petcoke', 14700, 58300, 2199, '4/5/4', 13, 'THE DAY OF THE SHIFT — work stopped at CJ-7 20:00, left 22:00; re-made fast at CJ-5 22:54, resumed 23:30 on 27 Nov. 14,700 MT in 24 h on 13 hooks — 58,300 off, ONLY 2,199 LEFT → about ' + eta(2199, 14700) + ' at this rate; list ETC 28 Nov 22:59 · stevedore RSIPL'),
 R('CJ-6', 'Katerina K', 'EXP', 'Kaolin + bentonite J-bags + soya bean meal', 3450, 6406, 40567, '3/3/3', 9, 'bentonite 2,760 J-bags / 3,450 MT in 24 h on 9 hooks (norm 3,450) — 6,406 MT loaded · left: kaolin 4,981 MT, bentonite 14,986, soya bean meal 20,600 = 40,567 → about ' + eta(40567, 3450) + ' at this rate · stevedore SAS'),
 R('CJ-7', 'Jumbo Kinetic', 'IMP', '2 harbour mobile cranes + 19 packages', 0, 0, 843, '0/0/2', 2, 'MADE FAST 23:25 on 27 Nov — NOT COMMENCED: "project cargo, can unlash and discharge — work only in daylight" · 19 units / 843 MT · from Kakinada · stevedore GFPL', True, None),
 R('CJ-8', 'Zheng Hui', 'IMP', 'DAP', 16330, 61950, 4050, '2/3/4', 9, '16,330 MT in 24 h on 9 hooks (12,061 the day before; norm 14,950) — 61,950 off, 4,050 left → about ' + eta(4050, 16330) + ' at this rate; list ETC 28 Nov 16:15 · gearless'),
 R('CJ-9', 'Pioneer Fortune', 'EXP', 'Sugar bags', 3754, 9193, 15887, '4/4/4', 12, '3,754 MT in 24 h on 12 hooks — 9,193 loaded, 15,887 left → about ' + eta(15887, 3754) + ' at this rate · stevedore GFPL'),
 R('CJ-13', 'AG Varvara', 'IMP', 'Pine logs', 4231, 12495, 26617, '4/4/4', 12, '31,115 pcs / 4,231 CBM in 24 h on 12 hooks (norm 4,000) — 91,767 pcs / 12,495 CBM off, 194,746 pcs / 26,617 CBM left → about ' + eta(26617, 4231) + ' at this rate; list ETC 5 Dec 08:52 · stevedore RSIPL'),
 R('CJ-14', 'Tug Varahi + barge AKG 11', 'EXP', 'Steel pipes', 1311, 3811, 0, '1/0/0', 1, 'COMPLETED 14:00, LEFT THE BERTH 16:20 on 27 Nov — 640 pipes / 3,811 MT · for Mumbai · stevedore AML'),
 R('CJ-15', 'Xin Hai Tong 71', 'IMP', 'Packaged steel & project cargo', 381, 3081, 2625, '4/4/3', 11, 'only 282 packages / 381 MT in 24 h on 11 hooks (1,767 the day before) — 746 packages / 3,081 MT off, 1,054 packages / 2,625 MT left → at the two-day average about ' + eta(2625, 1074) + ' · no ETC on the list', noPace=1),
 R('CJ-15A', 'Hai Nam 81', 'EXP', 'Salt in bulk', 24455, 24455, 27545, '4/4/4', 12, 'commenced 07:15 on 27 Nov — 24,455 MT in her first 23¾ hours on 12 hooks (norm 30,000); 27,545 left → about ' + eta(27545, 24455 * 24 / 23.75) + ' at this rate; list ETC 29 Nov 01:54 · stevedore GFPL · for Vietnam'),
 R('CJ-16', 'MSC Magali', 'IMP', 'Steam coal', 46879, 67806, 32922, '3/4/4', 11, '46,879 MT in 24 h on 11 hooks (norm 50,000) — 67,806 off, 32,922 left → about ' + eta(32922, 46879) + ' at this rate; list ETC 28 Nov 17:18 · stevedore SSS · gearless'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 1418, 49531, 8219, '1/1/1', 3, 'mother vessel — only 1,418 MT to Sheng Tai in 24 h (6,500 the day before); 49,531 off, 8,219 left'),
 R('MS', 'Sheng Tai', 'EXP', 'Barite ore', 2987, 47200, 8800, '1/1/1', 3, 'daughter vessel, ship-to-ship from African Loon — 2,987 MT in 24 h; 47,200 loaded, 8,800 left'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 1314, 10749, 34219, '2/2/2', 6, 'at midstream 4,700 pcs / 1,314 CBM in 24 h on 6 hooks — 10,749 CBM off, 34,219 left · and 7,541 pcs / 2,108 CBM landed at the barge area (10,071 CBM landed so far)'),
 R('MS', 'Aboudi D', 'EXP', 'Rice + sugar bags', 1380, 2795, 5345, '1/1/1', 3, 'at midstream rice 770 MT + sugar 610 MT in 24 h — 2,795 loaded, 5,345 left'),
 R('MS', 'MK Lamis', 'EXP', 'Rice bags', 730, 1710, 9790, '1/1/0', 2, '730 MT at midstream in 24 h — 1,710 loaded, 9,790 left · 500 MT came through IFFCO'),
 R('MS', 'Lolo Gate', 'EXP', 'Rice bags', 0, 0, 26000, '0/1/1', 2, 'nothing loaded at midstream yet — 26,000 MT to load; 1,300 MT came through IFFCO in the day · stevedore Trueblue', True, None),
 R('MS', 'Lanna Naree', 'EXP', 'Rice bags + project cargo', 100, 100, 24900, '0/1/1', 2, 'first 100 MT at midstream; 24,900 left · 600 MT came through IFFCO · stevedore ACT', True, None),
 R('MS', 'True Mariner', 'EXP', 'Rice bags', 0, 0, 25000, '', 0, 'at mooring buoy 3 — OTB 13:07, MADE FAST 16:45 on 27 Nov; no cargo yet, 25,000 MT to load (360 MT came through IFFCO) · stevedore RSIPL · for Algeria', True, None),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 500, 8372, 9428, '1/1/1', 3, '500 MT at midstream in 24 h — 8,372 loaded, 9,428 left on this row · 478 MT through the CJ row (10,954 loaded, 6,846 left there)'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 0, 7350, 2650, '', 0, 'no work — 2,650 MT of rice left (sugar 12,540 complete)'),
 R('MS', 'Crystal O', 'EXP', 'Sugar bags', 1550, 29175, 2025, '', 0, '1,550 MT at midstream in 24 h — 29,175 loaded, 2,025 left (the OP row: 1,750 in the day, 1,625 left)'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no work — 4,470 left'),
 R('BA', 'Coastal Amigo', 'EXP', 'Steel plates', 301, 2200, 0, '1/1/0', 2, 'COMPLETED 15:00, LEFT 15:40 on 27 Nov — 635 plates / 2,200 MT · for Dharamtar'),
 R('BA', 'Shree Krishna IX', 'IMP', 'Steel slabs', 1389, 1389, 853, '0/1/1', 2, 'MADE FAST 16:45, COMMENCED 17:00 on 27 Nov at the barge area — 57 slabs / 1,389 MT; 35 slabs / 853 MT left · from Dharamtar · stevedore GSI', True, '11-27 17:00'),
 R('OJ-1', 'Lumis', 'IMP', 'CPO / PFAD', 9223, 18443, 1557, '', 0, '9,223 MT in 24 h — 18,443 off; the DPR counts 1,557 left of 20,000, the list has 30,605 MT and ETC 29 Nov 15:24', noPace=1),
 R('OJ-2', 'MC Hera', 'IMP', 'Chemicals', 6740, 20600, 0, '', 0, 'COMPLETED 16:42, LEFT THE BERTH 20:50 on 27 Nov — 20,600 MT'),
 R('OJ-2', 'Bow Saturn', 'IMP', 'Chemicals', 199, 199, 8000, '', 0, 'MADE FAST 02:42, COMMENCED 05:42 on 28 Nov — 199 MT by 07:00; 8,000 left; list ETC 29 Nov 05:28', True, '11-28 05:42'),
 R('OJ-3', 'Ginga Merlin', 'IMP', 'Chemicals', 7433, 7813, 0, '', 0, 'COMPLETED 00:06, LEFT THE BERTH 03:05 on 28 Nov — 7,813 MT'),
 R('OJ-3', 'SC Draco', 'IMP', 'Methanol', 0, 0, 21336, '', 0, 'MADE FAST 06:00 on 28 Nov — not commenced by 07:00; 21,336 MT; list ETC 30 Nov 00:47', True, None),
 R('OJ-4', 'Chemroad Quest', 'IMP', 'Chemicals', 2300, 2300, 2656, '', 0, 'MADE FAST 15:20, COMMENCED 17:40 on 27 Nov — 2,300 MT in 13 hours; 2,656 left; list ETC 28 Nov 17:21', True, '11-27 17:40'),
 R('OJ-5', 'Volga', 'IMP', 'Chemicals', 5190, 5190, 2287, '', 0, 'MADE FAST 12:55, COMMENCED 16:15 on 27 Nov — 5,190 MT in 15 hours; 2,287 left; list ETC 29 Nov 06:18', True, '11-27 16:15'),
 R('OJ-6', 'Culture', 'EXP', 'VLSFO', 2042, 31542, 0, '', 0, 'COMPLETED 09:10, LEFT THE BERTH 12:15 on 27 Nov — 31,542 MT'),
 R('OJ-6', 'Maria Glory', 'IMP', 'Naphtha', 850, 850, 29248, '', 0, 'MADE FAST 02:30, COMMENCED 05:30 on 28 Nov — 850 MT by 07:00; 29,248 left', True, '11-28 05:30'),
 R('OJ-7', 'Peonia', 'IMP', 'CDSBO', 7947, 27001, 0, '', 0, 'COMPLETED 05:00 on 28 Nov — 27,001 MT; still alongside at 07:00 · signal: OUT 09:30'),
 R('TT-1', 'Blue Ionian', 'IMP', 'Sugar bulk', 10700, 62355, 11000, '', 0, '10,700 MT in 24 h — 62,355 off, 11,000 left → about ' + eta(11000, 10700) + ' at this rate'),
 R('TT-3', 'MP Postpanamax 1', 'IMP', 'Coal in bulk', 12500, 88000, 0, '', 0, 'COMPLETED 19:00 on 27 Nov, LEFT THE BERTH 02:30 on 28 Nov — 88,000 MT'),
 R('TT-3', 'Sakizaya Star', 'IMP', 'Coal in bulk', 0, 0, 80010, '', 0, 'MADE FAST 05:00 on 28 Nov — not commenced by 07:00; 80,010 MT', True, None),
]
a = B.s.index("const DPR={d:'27.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
old = B.s[a:e].split('\n'); ri = next(i for i, l in enumerate(old) if l.startswith(' rows:['))
keep = old[2:ri]
NEWDPR = ("const DPR={d:'28.11.2026',asOf:'11-28 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 28 Nov (xlsx from Mihir, 28 Nov 11:12)',\n"
 " tot:{dry:136143,dryL:50125,dryU:86018,ms:9979,kict:35509,tuna:23200,oj:41924,vad:254703,all:501458,gangs:'PR 29 · TR 5 · 42 + 6W gangs demanded / 42 + 6W supplied',rakes:'2',wb:928,sail:'Ocean Star · OJ-4 · 09:30'},\n"
 + "\n".join(keep) + ("\n" if keep else "") + " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]
out = subprocess.run(['python3', '-I', '/home/claude/berth-board/tools/barge_from_dpr.py', '/home/claude/work/in28/d28.txt', '28.11', '11-28 07:00'], capture_output=True, text=True).stdout.rstrip('\n')
assert out.startswith("  {d:'28.11'") and out.endswith("]},"), out[-200:]
out = out.replace("n:'Aboudi',", "n:'Aboudi D',").replace("ag:'Jm Baxi'", "ag:'JM Baxi'").replace("n:'Darya Priya'", "n:'Dariya Priya'")
print(out[:1500])
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + out + "\n")
MVN = ['DPR 28.11, list 28.11 and HM signal 28 Nov day sheet (disp 10:45) — the actual hours of 27 / 28 Nov at the cargo jetties', [
 ['15:22', 'OUT', 'Hui Fa', 'CJ-11 → OTB', '—', '11-27 15:22', 'container · completed 14:19, left the berth 15:22'],
 ['15:40', 'OUT', 'Coastal Amigo', 'Barge area → OTB', '—', '11-27 15:40', 'completed 15:00'],
 ['16:05', 'IN', 'DP World Thamirabarani', 'OTB → CJ-11 · 88–94½', '—', '11-27 16:05', 'container · made fast 16:05, commenced 16:46'],
 ['16:20', 'OUT', 'Tug Varahi + AKG 11', 'CJ-14 → OTB', '—', '11-27 16:20', 'completed 14:00, left the berth 16:20 — signal had 17:30'],
 ['16:45', 'IN', 'Shree Krishna IX', 'OTB → Barge area', '—', '11-27 16:45', 'made fast 16:45, commenced 17:00'],
 ['16:45', 'IN', 'True Mariner', 'OTB → mooring buoy 3', '—', '11-27 16:45', 'OTB 13:07, made fast 16:45'],
 ['20:25', 'SHIFT', 'Blue Shark', 'CJ-5 → CJ-14 · 128–141', '—', '11-27 21:15', 'work stopped 19:35, left 20:25, re-made fast 21:15, resumed 02:40'],
 ['22:00', 'SHIFT', 'Asian Summit', 'CJ-7 → CJ-5 · 30½–39¼', '—', '11-27 22:54', 'work stopped 20:00, left 22:00, re-made fast 22:54, resumed 23:30'],
 ['23:25', 'IN', 'Jumbo Kinetic', 'OTB → CJ-7 · 52–57', '—', '11-27 23:25', 'made fast 23:25 — not commenced, works in daylight only · COASTAL'],
 ['13:30', 'IN', 'Zyra', 'OTB → CJ-12 · 100–109', 'Mittal', '11-28 13:30', 'container · FLOOD · signal 28 Nov'],
 ['14:15', 'OUT', 'SCI Chennai', 'CJ-12 · 98–110 → OTB', 'Deepak', '11-28 14:15', 'container · signal 28 Nov'],
 ['o/c', 'IN', 'Sepelu', 'OTB → CJ-11 · 87–94½', 'Deepak', '11-28 17:00', 'container · FLOOD · behind DP World Thamirabarani — est'],
 ['15:00', 'OUT', 'DP World Thamirabarani', 'CJ-11 · 88–94½ → OTB', 'Sachin', '11-28 15:00', 'container · signal 28 Nov'],
 ['—', '—', 'No cargo-jetty move', 'CJ-1 to 8 and CJ-13 to 16', '—', '11-28 10:45', 'the day sheet of 28 Nov (disp 10:45) carries no dry-cargo berth move — as programme 28.11 had it']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
B.save(); print('saved 85b')
