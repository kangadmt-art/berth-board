#!/usr/bin/env python3
# apply51 — v254: DAILY PERFORMANCE REPORT 22.11.2026 (position 0700, xlsx) + HM signal 22 Nov DAY sheet (Capt Madaan, disp 08:05 / 08:25 / 09:00).
# Received 22 Nov 12:18, AFTER the 11:00 meeting, no text (the amended night sheet of 21 Nov came again with them). No list 22.11 yet.
# The meeting call of 22 Nov is FROZEN as v253 published it at 00:31 (Xin Hai Tong 71 → CJ-14).
import re, sys, subprocess
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
D = 'DPR 22.11'; SG = 'HM SIGNAL 22 Nov day sheet (disp 08:05)'
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

# ================= HEADER =================
B.rep("const NOW=h('11-22 00:26');", "const NOW=h('11-22 12:18');")
B.rep("<i>DPR</i><b>21.11</b>", "<i>DPR</i><b>22.11</b>")
B.rep("<i>Signals to</i><b>21 Nov night sheet, amended (disp 2230)</b>", "<i>Signals to</i><b>22 Nov day sheet (disp 0805 / 0825 / 0900)</b>")
n0 = len(B.s)
B.s, k = re.subn(r"<b>Papers of 21 Nov on the board:</b>.*?berthing-policy circular 5237 of 21\.11\.2026\.",
    "<b>Papers on the board:</b> berthing list 21.11 as revised after the meeting (the list of 22.11 has not come yet) · programme 22.11 · DPR 22.11 (position 07:00) · HM signal sheets to the day sheet of 22 Nov (disp 08:05 / 08:25 / 09:00) · timber desk sheet 21 Nov 12:00 · berthing-policy circular 5237 of 21.11.2026.", B.s, count=1, flags=re.S)
assert k == 1 and abs(len(B.s) - n0) < 600
B.rep("const CALL_FROZEN=null;", "const CALL_FROZEN={d:'11-22',at:'11-22 00:26',basis:'list 21.11 (revised) · HM signal 21 Nov night sheet as amended (disp 22:30) · DPR 21.11 · programme 22.11',call:[['Xin Hai Tong 71','14']]};")

# ================= DPR const =================
def R(loc, n, ie, c, l24, upto, bal, g='', hk=0, note='', partial=None, comm=None):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if partial: d['partial'] = 1; d['comm'] = comm
    d['note'] = note; return d
ROWS = [
 R('CJ-1', 'New Bliss', 'EXP', 'Sugar bags', 6072, 34000, 0, '4/4/4', 12, 'COMPLETED 07:00 on 22 Nov — 34,000 MT, the last 6,072 on 12 hooks; let-go hour blank (day signal: OUT 10:00)'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 2474, 9145, 23555, '4/4/4', 12, 'rice bags 1,349 MT (4,873 loaded, 17,627 left) + wheat flour 375 (1,749 / 2,451) + sugar bags 750 (2,523 / 3,477) — only 2,474 MT in 24 h on 12 hooks (4,846 the day before; norm 3,000); 23,555 left → about 1 Dec at this rate'),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 3994, 7368, 18732, '4/4/4', 12, '3,994 MT in 24 h on 12 hooks (norm 3,450) — 7,368 loaded, 18,732 left → about 26 Nov 23:30 at this rate. The row now adds to 26,100 MT (32,100 on DPR 21.11)'),
 R('CJ-5', 'Ken Ann', 'IMP', 'Steel / general cargo', 82, 5021, 0, '1/0/0', 1, 'COMPLETED 07:45, LEFT THE BERTH 10:30 on 21 Nov — 559 units / 5,021 MT'),
 R('CJ-5', 'Vishva Bandhan', 'IMP', 'Granular urea bulk', 2037, 40950, 3048, '0/3/3', 6, 'from CJ-8: RE-MADE FAST 11:24, RE-COMMENCED 12:20 on 21 Nov — 2,037 MT in the 24 h on 6 hooks; 40,950 off, 3,048 left → about 23 Nov 11:00 at the rate since she re-commenced', True, '11-21 12:20'),
 R('CJ-6', 'Parvraj', 'IMP', 'DAP', 10434, 12511, 36989, '4/4/4', 12, '10,434 MT in 24 h on 12 hooks (norm 14,950) — 12,511 off, 36,989 left → about 25 Nov 20:00 at this rate, a day and a half past the list ETC (24 Nov 08:17)'),
 R('CJ-8', 'Flag Marina', 'IMP', 'US coal in bulk', 44175, 44175, 59075, '0/5/5', 10, 'MADE FAST 12:45, COMMENCED 14:30 on 21 Nov — 44,175 MT in her first 16½ h on 10 hooks (about 64,000 a day; quote 42,500); 59,075 left. The DPR prints her at CJ-8 and CJ-7 as VACANT — she is 254 m and lies across both', True, '11-21 14:30'),
 R('CJ-9', 'Yuan Hang Wei Ye (next call)', 'EXP', 'Iron ore pellets', 30000, 30000, 20455, '5/2/2', 9, 'MADE FAST 13:06, COMMENCED 14:45 on 21 Nov — 30,000 MT in 16¼ h on 9 hooks (about 44,000 a day); 20,455 left → about 18:00 on 22 Nov', True, '11-21 14:45'),
 R('CJ-13', 'Uni Blossom', 'IMP', 'Pine logs', 6998, 7338, 27531, '4/4/4', 12, '21,557 pcs / 6,998 CBM in 24 h on 12 hooks (norm 4,600) — 7,338 CBM off, 27,531 left → about 26 Nov 05:30 at this rate, two and a half days inside the list ETC (28 Nov 17:58)'),
 R('CJ-14', 'Nord Copper', 'EXP', 'Salt in bulk', 24010, 45010, 0, '4/4/4', 12, 'COMPLETED 00:30, LEFT THE BERTH 02:25 on 22 Nov — 45,010 MT, the last 24,010 in 17½ h on 12 hooks'),
 R('CJ-14', 'Tug Sagar 5 + barge Victoria 250', 'EXP', 'Coated steel pipes', 0, 0, 3804, '0/0/0', 0, 'MADE FAST 05:55 on 22 Nov, not commenced at 0700 — 640 pipes / 3,804 MT to load', True, None),
 R('CJ-14', 'Sanghi Sundarshan', 'IMP', 'Steel coil', 95, 95, 3909, '0/0/0', 0, 'printed as "CJ-14A" · MADE FAST 04:00, COMMENCED 06:10 on 22 Nov — 4 coils / 95 MT in the first 50 minutes; 164 coils / 3,909 MT left', True, '11-22 06:10'),
 R('CJ-15', 'ML Egret', 'IMP', 'Pine logs', 6339, 23370, 19515, '4/4/4', 12, '18,189 pcs / 6,339 CBM in 24 h on 12 hooks (6,473 the day before; norm 4,600) — 23,370 CBM off, 19,515 left → about 25 Nov 08:50 at this rate · stevedore Mihir & Co'),
 R('CJ-15A', 'Heng Yuan Fa Zhan', 'IMP', 'Windmill blades & accessories', 582, 1895, 0, '2/1/0', 3, 'COMPLETED 16:45, LEFT THE BERTH 18:45 on 21 Nov — 56 units / 1,895 MT'),
 R('CJ-15A', 'Belmoira', 'EXP', 'Salt in bulk', 9984, 9984, 48316, '0/4/4', 8, 'MADE FAST 19:50, COMMENCED 21:50 on 21 Nov — 9,984 MT in her first 9 h on 8 hooks (about 26,000 a day; quote 30,000); 48,316 left · destination printed: Karachi', True, '11-21 21:50'),
 R('CJ-16', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes', 1846, 2755, 8958, '3/3/3', 9, '1,846 MT in 24 h on 9 hooks (803 the day before) — 2,755 loaded, 8,958 left → about 27 Nov 03:30 at this rate'),
 R('MS', 'Sea Postman', 'IMP', 'Rock phosphate', 5137, 13621, 14879, '2/2/2', 6, '5,137 MT into barges in 24 h on 6 hooks (8,484 in her first 20 h) — 13,621 off, 14,879 left → about 25 Nov 04:30 at this rate'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 1705, 2348, 42620, '2/2/2', 6, 'at midstream 6,100 pcs / 1,705 CBM in 24 h on 6 hooks — 2,348 CBM off, 42,620 left'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 10620, 25820, 31930, '1/1/1', 3, 'mother vessel — ship-to-ship to Sheng Tai (daughter; 9,720 MT on her sheet): 10,620 MT in 24 h, 31,930 left'),
 R('MS', 'Libra', 'EXP', 'Rice bags', 2210, 17957, 5043, '1/1/1', 3, '2,210 MT in 24 h (3,432 through IFFCO) — 17,957 loaded, 5,043 left → about 24 Nov 14:00 at this rate'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 0, 4411, 13389, '2/2/2', 6, 'no work on the ship in the 24 h (695 MT moved at CJ/OP) — 13,389 left'),
 R('MS', 'Crystal O', 'EXP', 'Sugar bags', 0, 16879, 14321, '', 0, 'no work — 14,321 left; she berths at CJ-1 today (day signal: IN 09:45)'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 650, 7000, 3000, '1/1/1', 3, '650 MT rice in 24 h — 7,000 loaded, 3,000 left; her sugar bags (12,500 MT through IFFCO) are complete'),
 R('MS', 'MAK 1', 'EXP', 'Rice in J-bags', 0, 21088, 800, '', 0, 'no work for the fourth day — 800 MT left'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no work — 4,470 left'),
 R('MS', 'North Gate', 'EXP', 'Chick peas / rice J-bags', 0, 23940, 3060, '', 0, 'no work — 3,060 left'),
 R('MRG-3', 'Tan Bin 259', 'EXP', 'NPK in jumbo bags', 1312, 12337, 0, '2/2/0', 4, 'COMPLETED 22:30 on 21 Nov — 12,337 MT; let-go hour blank (signal: OUT 06:00 on 22 Nov from mooring buoy 3)'),
 R('OJ-1', 'Artigo', 'IMP', 'CPO', 8877, 24000, 0, '', 0, 'COMPLETED 06:06 on 22 Nov — 24,000 MT; let-go hour blank (signal: OUT 07:20)'),
 R('OJ-2', 'Hatnyanawati', 'EXP', 'Chemicals', 7020, 10000, 0, '', 0, 'COMPLETED 03:00, LEFT THE BERTH 05:15 on 22 Nov — 10,000 MT'),
 R('OJ-2', 'PVT Aurora', 'IMP', 'Chemicals', 0, 0, 5000, '', 0, 'MADE FAST 08:18 on 22 Nov', True, None),
 R('OJ-3', 'SG Friendship', 'IMP', 'Chemicals', 3260, 8172, 0, '', 0, 'COMPLETED 20:00, LEFT THE BERTH 23:15 on 21 Nov — 8,172 MT'),
 R('OJ-3', 'Hartati', 'EXP', 'Chemicals', 500, 500, 10500, '', 0, 'MADE FAST 01:54, COMMENCED 04:54 on 22 Nov — 500 MT in two hours; 10,500 left', True, '11-22 04:54'),
 R('OJ-4', 'Eva Richway', 'IMP', 'Chemicals', 5877, 8627, 0, '', 0, 'COMPLETED 22:00 on 21 Nov, LEFT THE BERTH 02:40 on the 22nd — 8,627 MT'),
 R('OJ-4', 'Bow Fortitude', 'IMP', 'Chemicals', 0, 0, 10172, '', 0, 'MADE FAST 05:48 on 22 Nov, not commenced at 0700', True, None),
 R('OJ-6', 'Orchids', 'IMP', 'VLSFO', 559, 757, 7843, '', 0, '559 MT in 24 h — 757 off, 7,843 left (day signal: RT OUT 16:00 on 22 Nov)'),
 R('OJ-7', 'Silver Gertrude', 'IMP', 'CDSBO', 9359, 22500, 0, '', 0, 'COMPLETED 02:24, LEFT THE BERTH 03:50 on 22 Nov — 22,500 MT'),
 R('OJ-7', 'Ginga Cheetah', 'IMP', 'CDSBO + CSFO', 0, 0, 24270, '', 0, '"under berthing" at 0700 on 22 Nov', True, None),
 R('TT-1', 'Europa Graeca', 'IMP', 'Sugar bulk', 4867, 72546, 3131, '', 0, '4,867 MT in 24 h (10,095 the day before) — 72,546 off, 3,131 left → about 22 Nov 22:30 at this rate'),
 R('TT-2', 'Woohyun Dream', 'EXP', 'RSM in bulk', 10050, 10400, 21100, '', 0, '10,050 MT in 24 h — 10,400 loaded, 21,100 left → about 24 Nov 09:30 at this rate'),
 R('TT-3', 'Marvelous Star', 'IMP', 'Coal in bulk', 25235, 57000, 19844, '', 0, '25,235 MT in 24 h — 57,000 off, 19,844 left → about 23 Nov 02:00 at this rate. The sheet adds to 76,844 MT (the list has 50,000)'),
]
a = B.s.index("const DPR={d:'21.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
old = B.s[a:e].split('\n'); ri = next(i for i, l in enumerate(old) if l.startswith(' rows:['))
keep = old[2:ri]
NEWDPR = ("const DPR={d:'22.11.2026',asOf:'11-22 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 22 Nov (xlsx from Mihir, 22 Nov 12:18)',\n"
 " tot:{dry:175812,dryL:93250,dryU:82562,ms:12414,kict:39675,tuna:40152,oj:35452,vad:274027,all:577532,gangs:'PR 25 · TR 0 · 36 + 6 W gangs demanded / 36 + 6 W supplied',rakes:'2',wb:423,sail:'Seacon Monaco · CJ-9 · 11:50'},\n"
 + "\n".join(keep) + ("\n" if keep else "") + " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]

# ================= MSWORK (Barge tab) =================
out = subprocess.run(['python3', '-I', '/home/claude/berth-board/tools/barge_from_dpr.py', '/home/claude/work/in22a/dpr22.txt', '22.11', '11-22 07:00'], capture_output=True, text=True).stdout.rstrip('\n')
assert out.startswith("  {d:'22.11'") and out.endswith("]},"), out[-40:]
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + out + "\n")

# ================= V — hours and notes =================
M = "{b:'14',n:'Nord Copper',nm:23000,p:[126.5,141.75]"
pre(M, D + ": COMPLETED 00:30, LEFT THE BERTH 02:25 on 22 Nov — 45,010 MT, the last 24,010 in 17½ h on 12 hooks. The board had about 03:15 from the amended night sheet.")
sub(M, "t:'11-22 03:15',est:1", "t:'11-22 02:25'")
M = "{b:'14',n:'Sanghi Sundarshan',p:[135,141.75]"
pre(M, D + ": printed as \"CJ-14A\" · MADE FAST 04:00, COMMENCED 06:10 on 22 Nov — 4 coils / 95 MT by 0700; 164 coils / 3,909 MT left. The board had about 05:15.")
sub(M, "f:'11-22 05:15',t:'11-23 05:15'", "f:'11-22 04:00',t:'11-23 04:00'")
M = "{b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133]"
pre(M, D + ": MADE FAST 05:55 on 22 Nov, not commenced at 0700 — 640 pipes / 3,804 MT to load. The board had about 06:00.")
sub(M, "f:'11-22 06:00'", "f:'11-22 05:55'")
M = "{b:'7',n:'Flag Marina',nm:42500,p:[56.75,67.25]"
pre(M, D + ": MADE FAST 12:45, COMMENCED 14:30 on 21 Nov — 44,175 MT in her first 16½ h on 10 hooks (about 64,000 a day against the 42,500 quote); 59,075 left. At that rate she would finish about 05:00 on 23 Nov, but coal vessels on HP have ended at 70–80 % of the quote over the whole stay (Meghna Prestige, Xanadu, Andreas Petrakis), so the board keeps the quote time from her made-fast hour — about 23 Nov 23:05, est — until the list prints her ETC. The DPR prints her at CJ-8 and CJ-7 as VACANT; she is 254 m and lies across both.")
sub(M, "f:'11-21 11:15',t:'11-23 21:35'", "f:'11-21 12:45',t:'11-23 23:05'")
M = "{b:'15A',n:'Belmoira',nm:30000,p:[160.5,171.75]"
pre(M, D + ": MADE FAST 19:50, COMMENCED 21:50 on 21 Nov — 9,984 MT in her first 9 h on 8 hooks (about 26,000 a day; quote 30,000); 48,316 of 58,300 left. Quote time from the made-fast hour: about 23 Nov 18:30, est.")
sub(M, "f:'11-21 20:45',t:'11-23 19:25'", "f:'11-21 19:50',t:'11-23 18:30'")
M = "{b:'9',n:'Yuan Hang Wei Ye (next call)',p:[69,77.25]"
pre(M, D + ": MADE FAST 13:06, COMMENCED 14:45 on 21 Nov — 30,000 MT in 16¼ h on 9 hooks (about 44,000 a day); 20,455 left → about 18:00 on 22 Nov.")
sub(M, "f:'11-21 13:30'", "f:'11-21 13:06'")
M = "{b:'9',n:'Seacon Monaco',nm:20000,p:[69,76.75]"
pre(M, D + ": the sailing box prints SEACON MONACO · CJ-9 · 11:50 (21 Nov) — her let-go hour, which DPR 21.11 had left blank.")
sub(M, "t:'11-21 11:45',lt:'11-20 09:48',est:1", "t:'11-21 11:50',lt:'11-20 09:48'")
B.rep("mf:'11-18 06:36',out:'11-21 11:45',est:1}", "mf:'11-18 06:36',out:'11-21 11:50'}")
M = "{b:'5',n:'Vishva Bandhan',nm:9258,p:[33.25,41.5]"
pre(M, D + ": RE-MADE FAST at CJ-5 11:24, RE-COMMENCED 12:20 on 21 Nov — 2,037 MT in the 24 h on 6 hooks; 40,950 off, 3,048 left → about 23 Nov 11:00 at the rate since she re-commenced. The team was right that she does not sail on the 22nd.")
sub(M, "f:'11-21 11:15'", "f:'11-21 11:24'")
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, D + ": 1,846 MT in 24 h on 9 hooks (803 the day before) — 2,755 loaded, 8,958 left → about 27 Nov 03:30 at this rate (it was 4 Dec on DPR 21.11).")
sub(M, "t:'12-04 18:00',est:1", "t:'11-27 03:30',est:1")
M = "{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]"
pre(M, SG + ": OUT 10:00 on 22 Nov · Capt Sachin · 7½–N → OTB. " + D + ": COMPLETED 07:00 on 22 Nov — 34,000 MT, the last 6,072 on 12 hooks.")
sub(M, "t:'11-22 10:05'", "t:'11-22 10:00'")
M = "{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]"
pre(M, SG + ": IN 09:45 on 22 Nov · Capt Madaan · OTB → 7½–N · FLOOD — about 11:45 alongside. " + D + ": no work at midstream in the 24 h; 14,321 MT left to load.")
sub(M, "f:'11-22 12:00',t:'11-24 15:00'", "f:'11-22 11:45',t:'11-24 14:45'")
pre("{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]", D + ": rice bags 1,349 MT (17,627 left) + wheat flour 375 (2,451 left) + sugar bags 750 (3,477 left) — only 2,474 MT in 24 h on 12 hooks (4,846 the day before; norm 3,000); 23,555 of 32,700 left → about 1 Dec at this rate.")
pre("{b:'4',n:'Safi Alfa',nm:3450,p:[23,31.75]", D + ": 3,994 MT in 24 h on 12 hooks (norm 3,450) — 7,368 loaded, 18,732 left → about 26 Nov 23:30 at this rate. The row now adds to 26,100 MT (32,100 on DPR 21.11).")
pre("{b:'6',n:'Parvraj',nm:14950,p:[43,51.25]", D + ": 10,434 MT in 24 h on 12 hooks (norm 14,950) — 12,511 off, 36,989 left → about 25 Nov 20:00 at this rate, a day and a half past the list ETC.")
pre("{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]", D + ": 21,557 pcs / 6,998 CBM in 24 h on 12 hooks (norm 4,600) — 7,338 CBM off, 27,531 left → about 26 Nov 05:30 at this rate.")
pre("{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]", D + ": 18,189 pcs / 6,339 CBM in 24 h on 12 hooks (6,473 the day before) — 23,370 CBM off, 19,515 left → about 25 Nov 08:50 at this rate (it was 25 Nov 06:50 on DPR 21.11).")
pre("{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]", D + ": COMPLETED 16:45, LEFT THE BERTH 18:45 on 21 Nov — 56 units / 1,895 MT.")
pre("{b:'5',n:'Ken Ann',p:[33.5,41.5]", D + ": COMPLETED 07:45, LEFT THE BERTH 10:30 on 21 Nov — 559 units / 5,021 MT.")

# ================= W =================
def w(name, text, **k):
    B.list_tag = D; B.wrow(name, q(text), **k)
w('Sea Postman', "5,137 MT into barges in 24 h on 6 hooks — 13,621 off, 14,879 left → done about 25 Nov 04:30 at midstream, without a berth")
w('Dariya Priya', "at midstream 6,100 pcs / 1,705 CBM in 24 h on 6 hooks — 2,348 CBM off, 42,620 left")
w('Libra', "2,210 MT in 24 h at midstream (3,432 through IFFCO) — 17,957 loaded, 5,043 left → done about 24 Nov 14:00 without a berth")
w('Captainannis L', "no work on the ship in the 24 h (695 MT moved at CJ/OP) — 4,411 loaded, 13,389 left")
w('Fortunelit', "650 MT rice in 24 h at midstream — 7,000 loaded, 3,000 left; her sugar bags (12,500 MT through IFFCO) are complete")
B.wdel('Tan Bin 259')   # completed 22:30 on 21 Nov at mooring buoy 3, signal OUT 06:00 on 22 Nov — sailed without a berth call

# ================= TIMBER notes =================
def tnote(name, text):
    k = "{n:'%s',cbm:" % name
    if B.s.count(k) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(D + ": " + text + " · ") + B.s[i:]
tnote('ML Egret', "18,189 pcs / 6,339 CBM in 24 h on 12 hooks — 23,370 off, 19,515 left → about 25 Nov 08:50 at this rate")
tnote('Uni Blossom', "21,557 pcs / 6,998 CBM in 24 h on 12 hooks — 7,338 off, 27,531 left → about 26 Nov 05:30 at this rate")
tnote('Dariya Priya', "at midstream 6,100 pcs / 1,705 CBM in 24 h on 6 hooks — 2,348 off, 42,620 left")

# ================= MV =================
MV1 = ['HM signal 22 Nov — day sheet (dispatched 08:05 / 08:25 / 09:00) · Capt Madaan · received 22 Nov 12:18 · cargo berths', [
 ['10:00', 'OUT', 'New Bliss', 'CJ-1 · 7½–N → OTB', 'Sachin', '11-22 10:00', 'DPR 22.11: completed 07:00'],
 ['09:45', 'IN', 'Crystal O', 'OTB → CJ-1 · 7½–N', 'Madaan', '11-22 11:45', 'FLOOD · 6.5K'],
 ['10:00', 'SHIFT', 'Flexi 2', 'CJ-12 · 100–109½ → OTB', 'Sud', '11-22 10:00', 'container'],
 ['o/c', 'IN', 'TCI Anand', 'OTB → CJ-12 · 101–109½', 'Sud', '11-22 12:00', 'FLOOD · container — est'],
 ['13:00', 'OUT', 'TCI Express', 'CJ-11 · 87–95 → OTB', 'Sachin', '11-22 13:00', 'RT OUT · container · was 10:00']]]
MV2 = ['DPR 22.11 — actual hours at the cargo jetties, 21 Nov and the night', [
 ['10:30', 'OUT', 'Ken Ann', 'CJ-5 → OTB', '—', '11-21 10:30', 'completed 07:45, left the berth 10:30'],
 ['11:24', 'SHIFT', 'Vishva Bandhan', 'CJ-8 → CJ-5', '—', '11-21 11:24', 're-made fast 11:24, re-commenced 12:20'],
 ['11:50', 'OUT', 'Seacon Monaco', 'CJ-9 → OTB', '—', '11-21 11:50', 'sailing box: 11:50'],
 ['12:45', 'IN', 'Flag Marina', 'OTB → CJ-7 / CJ-8', '—', '11-21 12:45', 'made fast 12:45, commenced 14:30 — DPR prints her at CJ-8'],
 ['13:06', 'IN', 'Yuan Hang Wei Ye', 'OTB → CJ-9', '—', '11-21 13:06', 'made fast 13:06, commenced 14:45'],
 ['18:45', 'OUT', 'Heng Yuan Fa Zhan', 'CJ-15A → OTB', '—', '11-21 18:45', 'completed 16:45, left the berth 18:45'],
 ['19:50', 'IN', 'Belmoira', 'OTB → CJ-15A', '—', '11-21 19:50', 'made fast 19:50, commenced 21:50'],
 ['02:25', 'OUT', 'Nord Copper', 'CJ-14 → OTB', '—', '11-22 02:25', 'completed 00:30, left the berth 02:25 — board had ~03:15'],
 ['04:00', 'IN', 'Sanghi Sundarshan', 'OTB → CJ-14 · 135–141¾', '—', '11-22 04:00', 'made fast 04:00, commenced 06:10 — board had ~05:15'],
 ['05:55', 'IN', 'Tug Sagar 5 + barge Victoria 250', 'OTB → CJ-14 · 126½–133', '—', '11-22 05:55', 'made fast 05:55, not commenced at 0700 — board had ~06:00']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MV1) + ",\n " + js(MV2) + ",\n")

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
def bline(bid):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]; tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln; d = dict(split_top(core[3:-1]))
    if set(d) - {'b', 'prev', 'now'}: B.die('berth extra keys: ' + bid + str(list(d)))
    return a, b, d, tail
def bput(a, b, d, tail): B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in ('b', 'prev', 'now')) + '}' + tail + B.s[b:]
def berth(bid, nown, add):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    now['note'] = "'" + q(D + ': ' + add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS); bput(a, b, d, tail)
def turn(bid, oldn, out, outBy, newn, f, est, add):
    wa, wb = B.line_of("  {n:'%s'," % newn); wl = B.s[wa:wb].strip().rstrip(','); wv = obj(wl); assert 'n' in wv and 'c' in wv, list(wv)[:4]
    B.s = B.s[:wa] + B.s[wb + 1:]
    a, b, d, tail = bline(bid); now = obj(d['now']); assert oldn in now['n'], (oldn, now['n'])
    pv = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}; pv['out'] = js(out); pv['outBy'] = js(outBy)
    nw = {k: wv[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'rank', 'ag') if k in wv}; nw['f'] = js(f)
    if est: nw['est'] = '1'
    nw['note'] = "'" + q(D + ': ' + add + ' · ') + wv.get('rem', "''")[1:]
    d['prev'] = unobj(pv, ('n', 'c', 'q', 'u', 'ie', 'ag', 'out', 'outBy')); d['now'] = unobj(nw, NOWKEYS); bput(a, b, d, tail)
turn('OJ-1', 'Artigo', '11-22 07:20', 'DPR 22.11: completed 06:06 on 22 Nov — 24,000 MT, let-go hour blank · HM signal: OUT 07:20', 'Hafnia Ammolite', '11-22 09:20', True, 'not on the DPR at 0700 — signal: IN "o/c" behind Artigo on the flood, about 09:20, est')
turn('OJ-2', 'Hatnyanawati', '11-22 05:15', 'DPR 22.11: completed 03:00, LEFT THE BERTH 05:15 on 22 Nov — 10,000 MT (signal: RT OUT 05:00)', 'PVT Aurora', '11-22 08:18', False, 'MADE FAST 08:18 on 22 Nov — 5,000 MT to discharge')
turn('OJ-3', 'SG Friendship', '11-21 23:15', 'DPR 22.11: completed 20:00, LEFT THE BERTH 23:15 on 21 Nov — 8,172 MT (signal: SHIFT 23:15, agent a/c)', 'Hartati', '11-22 01:54', False, 'MADE FAST 01:54, COMMENCED 04:54 on 22 Nov — 500 MT loaded by 0700, 10,500 left')
turn('OJ-4', 'Eva Richway', '11-22 02:40', 'DPR 22.11: completed 22:00 on 21 Nov, LEFT THE BERTH 02:40 on the 22nd — 8,627 MT (signal: RT OUT 02:30)', 'Bow Fortitude', '11-22 05:48', False, 'MADE FAST 05:48 on 22 Nov, not commenced at 0700 — 10,172 MT to discharge')
turn('OJ-7', 'Silver Gertrude', '11-22 03:50', 'DPR 22.11: completed 02:24, LEFT THE BERTH 03:50 on 22 Nov — 22,500 MT (signal: RT OUT 04:00)', 'Ginga Cheetah', '11-22 08:00', True, '"UNDER BERTHING" on the DPR at 0700 — signal: IN o/c on the flood behind Tan Binh 259 (06:00), about 08:00, est')
berth('OJ-6', 'Orchids', '559 MT in 24 h — 757 off, 7,843 left · HM day signal 22 Nov: RT OUT 16:00 (Capt Sud)')
LM1 = ['HM signal 22 Nov — day sheet (dispatched 08:05 / 08:25 / 09:00) · Capt Madaan · oil-jetty rows', [['16:00', 'OUT', 'Orchids', 'OJ-6 → OTB', 'Sud', '11-22 16:00', 'RT OUT']]]
LM2 = ['DPR 22.11 — actual hours at the oil jetties, 21 Nov and the night', [
 ['23:15', 'OUT', 'SG Friendship', 'OJ-3 → OTB', '—', '11-21 23:15', 'completed 20:00, left the berth 23:15'],
 ['01:54', 'IN', 'Hartati', 'OTB → OJ-3', '—', '11-22 01:54', 'made fast 01:54, commenced 04:54 — board had ~01:15'],
 ['02:40', 'OUT', 'Eva Richway', 'OJ-4 → OTB', '—', '11-22 02:40', 'completed 22:00, left the berth 02:40 (signal 02:30)'],
 ['03:50', 'OUT', 'Silver Gertrude', 'OJ-7 → OTB', '—', '11-22 03:50', 'completed 02:24, left the berth 03:50 (signal 04:00)'],
 ['05:15', 'OUT', 'Hatnyanawati', 'OJ-2 → OTB', '—', '11-22 05:15', 'completed 03:00, left the berth 05:15 (signal 05:00)'],
 ['05:48', 'IN', 'Bow Fortitude', 'OTB → OJ-4', '—', '11-22 05:48', 'made fast 05:48, not commenced at 0700 — board had ~04:30'],
 ['08:18', 'IN', 'PVT Aurora', 'OTB → OJ-2', '—', '11-22 08:18', 'made fast 08:18 — board had ~07:00']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LM1) + ",\n  " + js(LM2) + ",\n" + B.s[mm:]
B.s, k = re.subn(r"src:'DPA berthing list 21\.11\.26 \(0700\) · DPR 21\.11 · programme 21\.11 \(TF/SH/2102\)[^']*',asOf:'11-21 11:22'",
    "src:'DPA berthing list 21.11.26 (revised) · DPR 22.11 · programme 22.11 · signals to the day sheet of 22 Nov (disp 0805 / 0825 / 0900)',asOf:'11-22 12:18'", B.s, count=1)
assert k == 1

# ================= TUNA =================
def tuna(bid, text):
    a, b = B.line_of("  {b:'%s',n:" % bid); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(D + ": " + text + " ") + B.s[i:]
tuna('TT-1', "4,867 MT in 24 h (10,095 the day before) — 72,546 off, 3,131 left → about 22 Nov 22:30 at this rate.")
tuna('TT-2', "10,050 MT in 24 h — 10,400 loaded, 21,100 left → about 24 Nov 09:30 at this rate.")
tuna('TT-3', "25,235 MT in 24 h — 57,000 off, 19,844 left → about 23 Nov 02:00 at this rate; the sheet adds to 76,844 MT.")
B.rep("const TUNA={src:'DPA berthing list 21.11.26 (0700) · DPR 21.11", "const TUNA={src:'DPA berthing list 21.11.26 (0700) · DPR 22.11")

# ================= the open check of the night is settled =================
M = " {d:'22 Nov 00:26 · New Bliss out / Crystal O in at CJ-1"
sub(M, "act:'Not known yet — the day sheet of 22 Nov will show it.'", "act:'" + q("Day sheet 22 Nov (disp 08:05): New Bliss OUT 10:00 (Capt Sachin), Crystal O IN 09:45 on the flood (Capt Madaan) — the two moves had only been left for the day sheet. DPR 22.11: New Bliss completed 07:00.") + "'")
sub(M, "st:'open'", "st:'ok'")
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='22 Nov 2026 · 12:40 IST';", B.s, count=1)
B.save()

# ---- part 2 (same version): our vessel's reading, after the projection was read
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
a = B.s.index(" 'CD Glory':["); e = B.s.index("\n ]", a)
ent = "  {d:'22 Nov 12:18 · DPR 22.11 + day signal of 22 Nov',exp:'11-25 21:06',b:'15A',slot:'" + q("SAAGAR (SGR 3) — CJ-15A, 25 Nov about 21:00, behind Hai Nam 81 · rests on two estimates from quotes") + "',why:'" + q("A day earlier on the board, and CJ-15A instead of CJ-15. DPR 22.11: ML Egret did 6,339 CBM (19,515 left → about 25 Nov 08:50) and Uni Blossom 6,998 CBM on her first full day (27,531 left → about 26 Nov 05:30; it was 27 Nov) — so the SAAGAR line opens on the 25th, not the 26th. The clean berth the board finds first is CJ-15A: Belmoira (salt, made fast 21 Nov 19:50, 30K quote) is reckoned out about 18:30 on 23 Nov, Hai Nam 81 (salt, 30K quote) follows her for two days, and CD Glory takes the berth behind her about 21:00 on the 25th. Both of those are estimates from quotes, not declared times — Belmoira did about 26,000 a day in her first nine hours, under her quote. If either runs a day over, CD Glory is back on the 26th at CJ-15 behind ML Egret, as before. Ahead of her in SAAGAR: AG Varvara (CJ-5, 24 Nov night, behind Vishva Bandhan). Nothing is programmed yet, and the port's answer on circular 5237 point (i) can still move it.") + "'}"
B.s = B.s[:e] + ("" if B.s[e - 1] == ',' else ",") + "\n" + ent + B.s[e:]
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='22 Nov 2026 · 12:31 IST';", B.s, count=1)
B.save()
