#!/usr/bin/env python3
# apply74b — v278 part 2: DPR 26.11 const, Barge tab, movements, oil jetties, Tuna, timber notes.
import sys, re, json, subprocess, datetime as DT
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 26.11 (revised)'); q = B.q
L = 'LIST 26.11 (revised)'; P = 'PROGRAMME 27.11'; D = 'DPR 26.11'; SG = 'HM SIGNAL 26 Nov day sheet'
BASE = DT.datetime(2026, 11, 26, 7, 0)
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

# ---- engine: a DPR row can say "no pace" (the list has re-stated her quantity) or carry a lag (hours lost to a shift)
B.rep("const dprPace=r=>{if(!r||!(r.l24>0))return null;", "const dprPace=r=>{if(!r||!(r.l24>0)||r.noPace)return null;")
B.rep("const dprEtc=r=>(r&&dprRate(r)>0&&r.bal>0)?h(DPR.asOf)+r.bal/dprRate(r)*24:null;", "const dprEtc=r=>(r&&dprRate(r)>0&&r.bal>0&&!r.noPace)?h(DPR.asOf)+r.bal/dprRate(r)*24+(r.lag||0):null; // lag = hours a programmed shift takes out of her work")

# ================= DPR const =================
def R(loc, n, ie, c, l24, upto, bal, g='', hk=0, note='', partial=None, comm=None, **x):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if partial: d['partial'] = 1; d['comm'] = comm
    d.update(x); d['note'] = note; return d
ROWS = [
 R('CJ-1', 'Manta Sena', 'EXP', 'Rice bags', 1536, 1536, 28634, '3/5/5', 13, 'MADE FAST 10:40, COMMENCED 15:10 on 25 Nov — 1,536 MT in her first 16 hours on 13 hooks; 28,634 left · stevedores Trueblue / JKS · list ETC 30 Nov 04:03', True, '11-25 15:10'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 4319, 24062, 8638, '4/4/4', 12, 'rice bags 3,103 MT (16,726 loaded, 5,774 left) + wheat flour 119 (2,817 / 1,383) + sugar bags 1,097 (4,519 / 1,481) — 4,319 MT in 24 h on 12 hooks (3,481 the day before); 8,638 left → about ' + eta(8638, 4319) + ' at this rate; list ETC 30 Nov 13:50'),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 2966, 23073, 3027, '4/4/4', 12, '2,966 MT in 24 h on 12 hooks (3,695 the day before) — 23,073 loaded; the DPR prints 3,027 left, against 26,100 — THE REVISED LIST NOW SAYS "32100 TOTAL" and ETC 30 Nov 01:58, i.e. 9,027 left: no finishing time is taken from this balance', noPace=1),
 R('CJ-5', 'Blue Shark', 'EXP', 'Rice bags + wheat flour + sugar bags', 3071, 5927, 17440, '5/5/5', 15, 'rice 2,695 MT (5,152 loaded, 6,592 left) + flour 376 (775 / 5,335) + sugar none yet (5,513 left) — 3,071 MT in 24 h on 15 hooks (2,482 the day before; norm 4,025); 17,440 left → about ' + eta(17440, 3071) + ' at this rate, plus about 3 h for tonight\'s shift to CJ-14; list ETC 30 Nov 13:00', lag=3),
 R('CJ-6', 'Parvraj', 'IMP', 'DAP', 3951, 49500, 0, '3/2/0', 5, 'COMPLETED 20:45 on 25 Nov, LEFT THE BERTH 02:15 on 26 Nov — 49,500 MT'),
 R('CJ-6', 'Katerina K', 'EXP', 'Kaolin + bentonite J-bags + soya bean meal', 20, 20, 48157, '0/0/3', 3, 'MADE FAST 04:12, COMMENCED 06:40 on 26 Nov — 20 MT of bentonite in the first 20 minutes; kaolin 26,000 + bentonite 1,557 + soya bean meal 20,600 MT left · agent Ambica · stevedore SAS · for the Netherlands', True, '11-26 06:40'),
 R('CJ-7', 'Asian Summit', 'IMP', 'Petcoke', 26200, 30000, 30499, '5/5/5', 15, '26,200 MT IN HER FIRST FULL DAY on 15 hooks (norm 16,100) — 30,000 off, 30,499 left → about ' + eta(30499, 26200) + ' at this rate, plus about 5 h for tonight\'s shift to CJ-5; list ETC 28 Nov 22:59 · stevedore RSIPL', lag=5),
 R('CJ-8', 'Zheng Hui', 'IMP', 'DAP', 12840, 32100, 33900, '3/2/2', 7, '12,840 MT in 24 h on 7 hooks (18,260 the day before; norm 14,950) — 32,100 off, 33,900 left → about ' + eta(33900, 12840) + ' at this rate; list ETC 28 Nov 16:15 · gearless'),
 R('CJ-9', 'Pioneer Fortune', 'EXP', 'Sugar bags', 1999, 1999, 23081, '4/4/4', 12, 'MADE FAST 07:20, COMMENCED 13:35 on 25 Nov — 1,999 MT in her first 17 hours on 12 hooks; 23,081 left · stevedore GFPL', True, '11-25 13:35'),
 R('CJ-13', 'AG Varvara', 'IMP', 'Pine logs', 4064, 4064, 35048, '0/4/4', 8, 'MADE FAST 12:12, COMMENCED 15:15 on 25 Nov — 29,767 pcs / 4,064 CBM in her first 16 hours on 8 hooks (norm 4,000 a day); 256,746 pcs / 35,048 CBM left · stevedore RSIPL · list ETC 5 Dec 08:52', True, '11-25 15:15'),
 R('CJ-14', 'Lila Tokyo', 'IMP', 'Gypsum in bulk', 23516, 72633, 0, '3/3/3', 9, 'COMPLETED 06:30 on 26 Nov — 72,633 MT; the last 23,516 on 9 hooks · signal: RT OUT 08:00'),
 R('CJ-14', 'Tug Varahi + barge AKG 11', 'EXP', 'Steel pipes', 0, 0, 3811, '', 0, 'not alongside at 07:00 (printed "BG AKJ 11") — 640 pipes / 3,811 MT to load · agent JM Baxi · stevedore AML · programme 27.11: out readiness 26 Nov 17:30', True, None),
 R('CJ-15', 'Xin Hai Tong 71', 'IMP', 'Packaged steel & project cargo', 910, 933, 4773, '4/4/4', 12, '81 packages / 910 MT in her first full day on 12 hooks — 83 packages / 933 MT off, 1,717 packages / 4,773 MT left → about ' + eta(4773, 910) + ' at this rate · no ETC on the list'),
 R('CJ-15A', 'Ocean Kudos', 'EXP', 'Salt in bulk', 39690, 70190, 0, '5/5/5', 15, 'COMPLETED 05:00 on 26 Nov — 70,190 MT; THE LAST 39,690 MT IN 22 HOURS on 15 hooks · stevedore Trueblue · for Karachi · signal: OUT 13:00'),
 R('CJ-16', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes + windmill blades', 365, 8894, 364, '2/2/2', 6, 'windmill blades 19 / 365 MT in 24 h on 6 hooks — 35 blades / 674 MT loaded, 19 blades / 364 MT left → about ' + eta(364, 365) + ' at this rate (I-beams and pipes, 8,220 MT, done on 24 Nov) · signal: shifts to CJ-15A at 13:00'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 11876, 41613, 16137, '1/1/1', 3, 'mother vessel — 11,876 MT to Sheng Tai in 24 h (2,500 the day before); 41,613 off, 16,137 left'),
 R('MS', 'Sheng Tai', 'EXP', 'Barite ore', 8476, 38213, 17787, '1/1/1', 3, 'daughter vessel, ship-to-ship from African Loon — 8,476 MT in 24 h; 38,213 loaded, 17,787 left'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 1315, 8219, 36749, '2/2/2', 6, 'at midstream 4,700 pcs / 1,315 CBM in 24 h on 6 hooks (2,040 the day before) — 8,219 CBM off, 36,749 left · and 4,839 pcs / 1,354 CBM landed at the barge area'),
 R('MS', 'Aboudi D', 'EXP', 'Rice + sugar bags', 740, 850, 7290, '2/2/2', 6, 'at midstream rice 180 MT + sugar 560 MT in 24 h on 6 hooks — 850 loaded, 7,290 left · 200 MT of rice came through OP'),
 R('MS', 'Yara J', 'IMP', 'Rice bags', 567, 30000, 0, '1/0/0', 1, 'COMPLETED 11:30 on 25 Nov — 30,000 MT (1,500 landed at CJ) · the list has her next for 30,000 MT of rice and sugar bags, export'),
 R('MS', 'Manta Omer Mecit', 'IMP', 'Fertiliser in J-bags', 1124, 3739, 0, '1/1/1', 3, 'COMPLETED 18:00 on 25 Nov — 3,739 MT (1,347 landed at OP)'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 380, 7872, 9928, '2/1/1', 4, '380 MT in 24 h on 4 hooks (1,692 the day before) — 7,872 loaded, 9,928 left · 1,400 MT came through CJ/OP'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 350, 7350, 2650, '1/1/1', 3, '350 MT in 24 h — her first work in four days; 7,350 loaded, 2,650 left (sugar 12,540 MT complete)'),
 R('MS', 'Crystal O', 'EXP', 'Sugar bags', 0, 27625, 3575, '', 0, 'at midstream since she left CJ-1 on 25 Nov — no work; 3,575 MT left'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no work — 4,470 left'),
 R('IFFCO', 'MK Lamis', 'EXP', 'Rice bags', 950, 1625, 9875, '', 0, '950 MT through the IFFCO jetty in 24 h — 1,625 loaded, 9,875 left'),
 R('BA', 'Coastal Amigo', 'EXP', 'Steel plates', 808, 808, 1392, '0/1/1', 2, 'at the barge area — MADE FAST 15:30, COMMENCED 17:45 on 25 Nov; 117 plates / 808 MT loaded, 518 plates / 1,392 MT left · for Dharamtar', True, '11-25 17:45'),
 R('OJ-1', 'Bogazici (LPG/C)', 'IMP', 'Propane + butane', 3688, 19854, 0, '', 0, 'butane completed 08:18, propane 19:30; LEFT THE BERTH 22:30 on 25 Nov — 19,854 MT'),
 R('OJ-1', 'Green Bhavishya (LPG/C)', 'IMP', 'Propane', 3853, 3853, 10147, '', 0, 'MADE FAST 23:32 on 25 Nov, COMMENCED 01:36 on 26 Nov — 3,853 MT in 5½ hours; 10,147 left; list ETC 27 Nov 09:32', True, '11-26 01:36'),
 R('OJ-2', 'Chemroute Pegasus', 'IMP', 'Chemicals', 1312, 8109, 600, '', 0, 'WORK STOPPED 13:00, LEFT THE BERTH 13:30, shifted to OTB 16:45 on 25 Nov — 8,109 MT off, 600 MT STILL ON BOARD (she is back on the waiting sheet, 8C)'),
 R('OJ-2', 'Thetis Leona', 'IMP', 'Chemicals', 4546, 4546, 454, '', 0, 'MADE FAST 16:00, COMMENCED 18:18 on 25 Nov — 4,546 MT; 454 left; list ETC 26 Nov 18:13 · signal: RT OUT 14:00', True, '11-25 18:18'),
 R('OJ-3', 'Hafnia Ammolite', 'IMP', 'CDSBO', 5900, 30800, 0, '', 0, 'COMPLETED 21:30 on 25 Nov, LEFT THE BERTH 00:30 on 26 Nov — 30,800 MT'),
 R('OJ-3', 'Lumis', 'IMP', 'CPO / PFAD', 0, 0, 20000, '', 0, 'MADE FAST 03:42, COMMENCED 08:12 on 26 Nov — nothing by 07:00; the DPR prints 20,000 MT to discharge, the list 30,605', True, None),
 R('OJ-4', 'Chemroad Nexus', 'IMP', 'Chemicals', 9719, 10950, 0, '', 0, 'COMPLETED 05:55 on 26 Nov — 10,950 MT · signal: RT OUT 09:30'),
 R('OJ-6', 'Culture', 'EXP', 'VLSFO', 13833, 13833, 10167, '', 0, 'MADE FAST 10:53, COMMENCED 13:06 on 25 Nov — 13,833 MT loaded in 18 hours; 10,167 left · coastal · programme 27.11: out readiness 27 Nov 12:00', True, '11-25 13:06'),
 R('OJ-7', 'Sriwangi V', 'IMP', 'CPO', 3093, 10000, 0, '', 0, 'COMPLETED 22:24 on 25 Nov, LEFT THE BERTH 02:15 on 26 Nov — 10,000 MT'),
 R('OJ-7', 'Peonia', 'IMP', 'CDSBO', 0, 0, 27001, '', 0, 'MADE FAST 03:48, COMMENCED 07:42 on 26 Nov — nothing by 07:00; 27,001 MT to discharge; list ETC 28 Nov 03:20', True, None),
 R('TT-1', 'Blue Ionian', 'IMP', 'Sugar bulk', 12800, 38200, 35155, '', 0, '12,800 MT in 24 h — 38,200 off, 35,155 left → about ' + eta(35155, 12800) + ' at this rate'),
 R('TT-3', 'MP Postpanamax 1', 'IMP', 'Coal in bulk', 23200, 50100, 37900, '', 0, '23,200 MT in 24 h — 50,100 off, 37,900 left → about ' + eta(37900, 23200) + ' at this rate'),
]
a = B.s.index("const DPR={d:'25.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
old = B.s[a:e].split('\n'); ri = next(i for i, l in enumerate(old) if l.startswith(' rows:['))
keep = old[2:ri]
NEWDPR = ("const DPR={d:'26.11.2026',asOf:'11-26 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 26 Nov (xlsx from Mihir, 26 Nov 15:14)',\n"
 " tot:{dry:133006,dryL:57324,dryU:75682,ms:24828,kict:24991,tuna:36000,oj:45944,vad:415803,all:680572,gangs:'PR 27 · TR 5 · 38 gangs demanded / 38 supplied',rakes:'2',wb:941,sail:'Uni Blossom · CJ-13 · 10:35 · Willows · OJ-6 · 08:15 · Crystal O · CJ-1 · 08:30'},\n"
 + "\n".join(keep) + ("\n" if keep else "") + " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]

# ================= MSWORK (Barge tab) =================
out = subprocess.run(['python3', '-I', '/home/claude/berth-board/tools/barge_from_dpr.py', '/home/claude/work/in26/d26.txt', '26.11', '11-26 07:00'], capture_output=True, text=True).stdout.rstrip('\n')
assert out.startswith("  {d:'26.11'") and out.endswith("]},"), out[-80:]
out = out.replace("n:'Aboudi',", "n:'Aboudi D',").replace("c:'Fertilizer j/bags'", "c:'Fertiliser in J-bags'").replace("ag:'Jm Baxi'", "ag:'JM Baxi'")
print(out)
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + out + "\n")

# ================= MV =================
MVS = ['HM signal 26 Nov — day sheet (the 20:28 sheet re-dated 26/11, extended at 08:15 and 09:10) · Capt Pathak / Capt Omesh · received 26 Nov 15:14 · cargo berths', [
 ['08:00', 'OUT', 'Lila Tokyo', 'CJ-14 · 126–143½ → OTB', 'Bali', '11-26 08:00', 'RT OUT'],
 ['o/c', 'IN', 'Tug Varahi + barge AKG 11', 'OTB → CJ-14 · 128–134¾', 'Bali', '11-26 12:00', 'behind Lila Tokyo — est · programme 27.11 has her out again at 17:30'],
 ['10:00', 'SHIFT', 'Xin Hai Tong 71', 'CJ-15 · 145¾–158¼ → 143–156¼', 'Pathak', '11-26 10:00', 'as programme 26.11'],
 ['13:00', 'SHIFT', 'African Hornbill', 'CJ-16 · 173½–188 → CJ-15A · 157½–166¾', 'Pathak', '11-26 13:00', 'as programme 26.11 — behind Ocean Kudos'],
 ['13:00', 'OUT', 'Ocean Kudos', 'CJ-15A · 159¼–171¾ → OTB', 'Karan', '11-26 13:00', 'completed 05:00'],
 ['13:00', 'IN', 'MSC Magali', 'OTB → CJ-16 · 169½–188', 'Bali', '11-26 15:00', 'pilot boards 13:00 · alongside about 15:00, est · HP (50K)'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Bali 11:30–12:30 · Capt Karan on completion', '—', '11-26 12:30', '']]]
MVN = ['DPR 26.11 and list 26.11 — the actual hours of 25 / 26 Nov at the cargo jetties', [
 ['07:20', 'IN', 'Pioneer Fortune', 'OTB → CJ-9', '—', '11-25 07:20', 'made fast 07:20, commenced 13:35'],
 ['10:35', 'OUT', 'Uni Blossom', 'CJ-13 → OTB', '—', '11-25 10:35', 'sailing block of the DPR — the programme had 17:30'],
 ['10:40', 'IN', 'Manta Sena', 'OTB → CJ-1', '—', '11-25 10:40', 'made fast 10:40, commenced 15:10'],
 ['12:12', 'IN', 'AG Varvara', 'OTB → CJ-13 · 112–125', '—', '11-25 12:12', 'made fast 12:12, commenced 15:15 — the board had ~19:30'],
 ['13:42', 'OUT', 'Hong Da Xing 768', 'CJ-12 → OTB', '—', '11-25 13:42', 'container · completed 11:36, left the berth 13:42'],
 ['00:20', 'OUT', 'DP World Godavari', 'CJ-11 → OTB', '—', '11-26 00:20', 'container · completed 19:42, left the berth 00:20'],
 ['01:25', 'IN', 'Tanjong Pagar 1', 'OTB → CJ-11', '—', '11-26 01:25', 'container · made fast 01:25, commenced 02:39'],
 ['01:50', 'IN', 'SCI Chennai', 'OTB → CJ-12', '—', '11-26 01:50', 'container · made fast 01:50, commenced 03:16'],
 ['02:15', 'OUT', 'Parvraj', 'CJ-6 → OTB', '—', '11-26 02:15', 'completed 20:45 on 25 Nov, left the berth 02:15 (signal: 23:45)'],
 ['04:12', 'IN', 'Katerina K', 'OTB → CJ-6 · 40¼–49', '—', '11-26 04:12', 'made fast 04:12, commenced 06:40 — GEN 3, on no programme and no signal sheet in hand'],
 ['05:00', '—', 'Ocean Kudos', 'CJ-15A', '—', '11-26 05:00', 'completed 05:00 — 70,190 MT'],
 ['06:30', '—', 'Lila Tokyo', 'CJ-14', '—', '11-26 06:30', 'completed 06:30 — 72,633 MT']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVS) + ",\n " + js(MVN) + ",\n")
B.save(); print('saved 74b')
