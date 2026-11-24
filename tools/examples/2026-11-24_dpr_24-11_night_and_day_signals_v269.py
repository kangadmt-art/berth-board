#!/usr/bin/env python3
# apply65 — v269: three papers received 24 Nov 10:40, no text (20 minutes before the meeting of 24 Nov) —
#   DAILY PERFORMANCE REPORT 24.11.2026 (position 0700, PDF) ·
#   HM "AMENDMENT & NEW SIGNAL" dated 23/11/26 (disp 21:00 / 01:28, Capt G. Raj) — the night sheet, amending the evening sheet of 16:25 ·
#   HM "DAY SIGNAL" dated 23/11/26 (disp 21:15 / 05:47, Capt Omesh) — the day sheet for 24 Nov.
# No list for 24.11 yet: waiting rows keep their ranks; only the midstream progress is noted on them.
# The DPR gives the ACTUAL hours of the night: Blue Shark made fast 21:00 · Gokova-M 23:05 · Ocean Kudos 01:00 · Horizon Chaser 04:00 · Zheng Hui 04:18 ·
# Lila Tokyo 13:30 on the 23rd · left the berth: Vishva Bandhan 18:35, Flag Marina 20:20, Belmoira 22:53, the tug-and-barge 12:50.
import sys, re, subprocess, datetime as DT
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='DPR 24.11'); q = B.q
D = 'DPR 24.11'; SN = 'HM NIGHT SIGNAL 23 Nov (amendment & new, disp 21:00 / 01:28)'; SD = 'HM DAY SIGNAL 24 Nov (disp 21:15 / 05:47)'
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
BASE = DT.datetime(2026, 11, 24, 7, 0)
def eta(bal, l24):
    t = BASE + DT.timedelta(hours=bal / l24 * 24); m = int(round((t.hour * 60 + t.minute) / 5.0) * 5); t = t.replace(hour=0, minute=0) + DT.timedelta(minutes=m)
    return '%d Nov %02d:%02d' % (t.day, t.hour, t.minute)
def f(n): return format(int(round(n)), ',')

# ================= HEADER =================
B.rep("const NOW=h('11-23 16:41');", "const NOW=h('11-24 10:40');")
B.rep("<i>DPR</i><b>23.11</b>", "<i>DPR</i><b>24.11</b>")
B.rep("<i>Signals to</i><b>23 Nov evening sheet (disp 1625)</b>", "<i>Signals to</i><b>24 Nov day sheet (disp 2115 / 0547)</b>")
B.rep("· DPR 23.11 (position 07:00) · HM signal sheets to the evening sheet of 23 Nov (disp 16:25) · timber desk sheet",
      "· DPR 24.11 (position 07:00; no list for 24.11 yet) · HM signal sheets to the day sheet of 24 Nov (disp 21:15 / 05:47) · timber desk sheet")
B.rep("const BOARD_SRC='", "const BOARD_SRC='DPR 24.11 (0700) · HM day signal 24 Nov (disp 2115 / 0547) · HM night signal 23 Nov (amendment, disp 2100 / 0128) · ")

# ================= V =================
M = "{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]"
pre(M, D + ": 5,347 MT in 24 h on 12 hooks (norm 6,500) — 18,877 loaded, 8,323 left → about " + eta(8323, 5347) + " at this rate, about 20 hours past the list ETC (24 Nov 23:43).")
M = "{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]"
pre(M, D + ": 3,410 MT in 24 h on 12 hooks (rice 3,000 · flour 285 · sugar 125; 3,707 the day before) — 16,262 loaded, 16,438 left → about " + eta(16438, 3410) + " at this rate.")
M = "{b:'3',n:'Horizon Chaser',p:[17.5,21.75]"
pre(M, D + ": MADE FAST 04:00 on 24 Nov, not commenced at 0700 — 3,820 MT of bitumen to discharge. " + SN + ": IN \"o/c\" · Capt Sud (the evening sheet had Capt G. Raj at 21:15), after DP World Godavari — she came five hours later than the board's 23:15. Out about 25 Nov 04:00 on the 24 hours of her last call, est.")
sub(M, "f:'11-23 23:15',t:'11-24 23:15',est:1", "f:'11-24 04:00',t:'11-25 04:00',est:1")
M = "{b:'4',n:'Safi Alfa',nm:3450,p:[23,31.75]"
pre(M, D + ": 3,890 MT in 24 h on 12 hooks (5,154 the day before on 15; norm 3,450) — 16,412 loaded, 9,688 left → about " + eta(9688, 3890) + " at this rate — 20 hours later than yesterday's pace gave (25 Nov 22:15); the list ETC is 28 Nov 00:00.")
M = "{b:'5',n:'Vishva Bandhan',nm:8050,p:[33.25,41.5]"
pre(M, D + ": COMPLETED 15:45, LEFT THE BERTH 18:35 on 23 Nov — 43,998 MT (signal: RT OUT 18:30).")
sub(M, "t:'11-23 18:30'", "t:'11-23 18:35'")
M = "{b:'5',n:'Blue Shark',p:[32.5,40]"
pre(M, D + ": MADE FAST 21:00 on 23 Nov, COMMENCED 01:15 (rice) and 03:30 (flour) on 24 Nov — 374 MT in the first hours on 3 hooks; 23,007 left (rice 11,420 · flour 6,074 · sugar 5,513). The board had about 20:00. Finish about 30 Nov 16:00, est.")
sub(M, "f:'11-23 20:00',t:'11-30 15:00',est:1", "f:'11-23 21:00',t:'11-30 16:00',est:1")
M = "{b:'6',n:'Parvraj',nm:14950,p:[41.25,49.5]"
pre(M, D + ": 10,102 MT in 24 h on 12 hooks (11,487 the day before; norm 14,950) — 34,100 off, 15,400 left → about " + eta(15400, 10102) + " at this rate; her list ETC (24 Nov 08:17) is past. " + SN + ": SHIFT 21:30 · Capt G. Raj · 43–51¼ → 41¼–49½ · \"PORT C\" (the evening sheet had 20:00).")
M = "{b:'7',n:'Gokova-M',nm:50000,p:[50.5,57]"
pre(M, D + ": MADE FAST 23:05, COMMENCED 23:55 on 23 Nov — 14,000 MT in the first 7 hours on 5 hooks (about 47,400 a day; her quote is 50,000); 36,500 left → about 25 Nov 01:30 at this pace, est. The sheet counts 50,500 MT for her (\"ball J bags\"); the list has 42,000. " + SN + ": IN \"o/c\" · Capt Bali · FLOOD, behind Flag Marina (RT OUT 20:00, an hour earlier than the evening sheet).")
sub(M, "f:'11-23 23:00',t:'11-25 01:15',est:1", "f:'11-23 23:05',t:'11-25 01:30',est:1")
M = "{b:'7',n:'Flag Marina',nm:42500,p:[56.75,67.25]"
pre(M, D + ": COMPLETED 16:45, LEFT THE BERTH 20:20 on 23 Nov — 103,250 MT, the last 8,900 on 7 hooks (night signal: RT OUT 20:00; evening sheet 21:00).")
sub(M, "t:'11-23 21:00'", "t:'11-23 20:20'")
M = "{b:'8',n:'Zheng Hui',p:[58,67.75]"
pre(M, D + ": MADE FAST 04:18, COMMENCED 06:25 on 24 Nov — 1,000 MT in the first half hour on 4 hooks; 65,000 left; printed \"(GL)\" — gearless. " + SN + ": IN \"o/c\" · Capt Karan, behind his 01:00 sailing of Al Hadbaa — three hours later than the board's 01:00. At the DAP norm → about 28 Nov 15:20, est.")
sub(M, "f:'11-24 01:00',t:'11-28 15:55',est:1", "f:'11-24 04:18',t:'11-28 15:20',est:1")
M = "{b:'9',n:'Sand Topic',nm:20000,p:[69,77.75]"
pre(M, D + ": 37,997 MT in 24 h on 15 hooks (norm 20,000) — 41,092 off, 10,200 left → about " + eta(10200, 37997) + " at this rate, a day inside her permissible time.")
M = "{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]"
pre(M, D + ": 28,023 pcs / 9,097 CBM in 24 h on 12 hooks (8,020 the day before; norm 4,600) — 24,455 CBM off, 10,414 left → about " + eta(10414, 9097) + " at this rate (25 Nov 17:20 on DPR 23.11).")
M = "{b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]"
pre(M, D + ": MADE FAST 13:30, COMMENCED 14:40 on 23 Nov — 21,087 MT in the first 16 hours on 10 hooks (about 31,000 a day; quote 30,000); 51,546 left → about 25 Nov 22:55 at this pace, est. The board had about 12:45 for the berthing.")
sub(M, "f:'11-23 12:45',t:'11-25 22:50',est:1", "f:'11-23 13:30',t:'11-25 22:55',est:1")
M = "{b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133]"
pre(M, D + ": sailing box — left CJ-14 at 12:50 on 23 Nov (signal: RT OUT 11:00).")
sub(M, "t:'11-23 11:00'", "t:'11-23 12:50'")
M = "{b:'15',n:'ML Egret',nm:4600,p:[145.75,158.25]"
pre(M, D + ": 22,448 pcs / 7,825 CBM in 24 h on 12 hooks (6,811 the day before; norm 4,600) — 38,006 CBM off, 4,879 left → about " + eta(4879, 7825) + " at this rate (25 Nov 03:45 on DPR 23.11) · stevedore Mihir & Co.")
M = "{b:'15A',n:'Belmoira',nm:30000,p:[160.5,171.75]"
pre(M, D + ": COMPLETED 20:15, LEFT THE BERTH 22:53 on 23 Nov — 58,300 MT of salt, the last 18,825 on 10 hooks (night signal: OUT 22:45; evening sheet 23:45).")
sub(M, "t:'11-23 23:45'", "t:'11-23 22:53'")
M = "{b:'15A',n:'Ocean Kudos',nm:30000,p:[159.25,171.75]"
pre(M, D + ": MADE FAST 01:00, COMMENCED 03:00 on 24 Nov — 4,500 MT of salt in the first 4 hours on 5 hooks; 65,690 left → about 26 Nov 11:35 at her 30,000 quote, est. " + SN + ": IN \"o/c\" · Capt G. Raj behind Belmoira (OUT 22:45) — the board had about 01:45.")
sub(M, "f:'11-24 01:45',t:'11-26 11:55',est:1", "f:'11-24 01:00',t:'11-26 11:35',est:1")
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, D + ": 1,770 MT in 24 h on 9 hooks (3,340 the day before) — 7,865 loaded, 3,848 left → about " + eta(3848, 1770) + " at this rate — a day and a half later than yesterday's pace gave (24 Nov 23:20).")
sub(M, "t:'11-24 23:20',est:1", "t:'11-26 11:10',est:1")

# ================= W — midstream progress only (no list today) =================
def w(name, text): B.wrow(name, q(text))
w('Sea Postman', "7,196 MT into barges in 24 h on 6 hooks — 28,400 off, ONLY 100 MT LEFT at 0700 on 24 Nov: she finishes at midstream this morning and will not need a berth")
w('Libra', "2,310 MT in 24 h at midstream (15 through IFFCO, completed there 08:00) — 22,943 loaded, 57 MT left: done at midstream, no berth needed")
w('Manta Omer Mecit', "NOW WORKING AT MIDSTREAM — OTB 17:30, made fast 20:00, commenced 21:45 on 23 Nov · 1,268 MT into barges on 2 hooks, 2,471 left")
w('Captainannis L', "739 MT in 24 h at midstream on 6 hooks (1,520 through CJ/OP) — 5,800 loaded, 12,000 left")
w('Dariya Priya', "at midstream 4,300 pcs / 1,202 CBM in 24 h on 6 hooks — 4,864 CBM off, 40,104 left")
w('Fortunelit', "no work for the second day — 7,000 loaded at midstream, 3,000 left (949 at CJ/IFFCO)")

# ================= DPR const =================
def R(loc, n, ie, c, l24, upto, bal, g='', hk=0, note='', partial=None, comm=None):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if partial: d['partial'] = 1; d['comm'] = comm
    d['note'] = note; return d
ROWS = [
 R('CJ-1', 'Crystal O', 'EXP', 'Sugar bags', 5347, 18877, 8323, '4/4/4', 12, '5,347 MT in 24 h on 12 hooks (norm 6,500) — 18,877 loaded, 8,323 left → about ' + eta(8323, 5347) + ' at this rate'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 3410, 16262, 16438, '4/4/4', 12, 'rice bags 3,000 MT (10,773 loaded, 11,727 left) + wheat flour 285 (2,366 / 1,834) + sugar bags 125 (3,123 / 2,877) — 3,410 MT in 24 h on 12 hooks (3,707 the day before); 16,438 left → about ' + eta(16438, 3410) + ' at this rate'),
 R('CJ-3', 'Horizon Chaser', 'IMP', 'Bitumen', 0, 0, 3820, '', 0, 'MADE FAST 04:00 on 24 Nov, not commenced at 0700 — 3,820 MT to discharge', True, None),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 3890, 16412, 9688, '4/4/4', 12, '3,890 MT in 24 h on 12 hooks (5,154 the day before on 15; norm 3,450) — 16,412 loaded, 9,688 left → about ' + eta(9688, 3890) + ' at this rate (25 Nov 22:15 on DPR 23.11); list ETC 28 Nov 00:00'),
 R('CJ-5', 'Vishva Bandhan', 'IMP', 'Granular urea bulk', 884, 43998, 0, '2/1/0', 3, 'COMPLETED 15:45, LEFT THE BERTH 18:35 on 23 Nov — 43,998 MT'),
 R('CJ-5', 'Blue Shark', 'EXP', 'Rice bags + wheat flour + sugar bags', 374, 374, 23007, '0/0/3', 3, 'MADE FAST 21:00 on 23 Nov, COMMENCED 01:15 (rice) and 03:30 (flour) on 24 Nov — 374 MT in the first hours on 3 hooks; 23,007 left (rice 11,420 · flour 6,074 · sugar 5,513)', True, '11-24 01:15'),
 R('CJ-6', 'Parvraj', 'IMP', 'DAP', 10102, 34100, 15400, '4/4/4', 12, '10,102 MT in 24 h on 12 hooks (11,487 the day before; norm 14,950) — 34,100 off, 15,400 left → about ' + eta(15400, 10102) + ' at this rate; list ETC 24 Nov 08:17 is past'),
 R('CJ-7', 'Gokova-M', 'EXP', 'Ball clay in J-bags', 14000, 14000, 36500, '0/0/5', 5, 'MADE FAST 23:05, COMMENCED 23:55 on 23 Nov — 14,000 MT in the first 7 hours on 5 hooks (about 47,400 a day; quote 50,000); 36,500 left → about 25 Nov 01:30 at this pace. The sheet counts 50,500 MT for her; the list has 42,000', True, '11-23 23:55'),
 R('CJ-8', 'Flag Marina', 'IMP', 'US coal in bulk', 8900, 103250, 0, '5/2/0', 7, 'COMPLETED 16:45, LEFT THE BERTH 20:20 on 23 Nov — 103,250 MT, the last 8,900 on 7 hooks'),
 R('CJ-8', 'Zheng Hui', 'IMP', 'DAP', 1000, 1000, 65000, '0/0/4', 4, 'MADE FAST 04:18, COMMENCED 06:25 on 24 Nov — 1,000 MT in the first half hour on 4 hooks; 65,000 left · printed "(GL)", gearless', True, '11-24 06:25'),
 R('CJ-9', 'Sand Topic', 'IMP', 'Petcoke', 37997, 41092, 10200, '5/5/5', 15, '37,997 MT in 24 h on 15 hooks (norm 20,000) — 41,092 off, 10,200 left → about ' + eta(10200, 37997) + ' at this rate'),
 R('CJ-13', 'Uni Blossom', 'IMP', 'Pine logs', 9097, 24455, 10414, '4/4/4', 12, '28,023 pcs / 9,097 CBM in 24 h on 12 hooks (8,020 the day before; norm 4,600) — 24,455 CBM off, 10,414 left → about ' + eta(10414, 9097) + ' at this rate'),
 R('CJ-14', 'Lila Tokyo', 'IMP', 'Gypsum in bulk', 21087, 21087, 51546, '3/4/3', 10, 'MADE FAST 13:30, COMMENCED 14:40 on 23 Nov — 21,087 MT in the first 16 hours on 10 hooks (about 31,000 a day; quote 30,000); 51,546 left → about 25 Nov 22:55 at this pace · printed "(GL)", gearless', True, '11-23 14:40'),
 R('CJ-15', 'ML Egret', 'IMP', 'Pine logs', 7825, 38006, 4879, '4/4/4', 12, '22,448 pcs / 7,825 CBM in 24 h on 12 hooks (6,811 the day before; norm 4,600) — 38,006 CBM off, 4,879 left → about ' + eta(4879, 7825) + ' at this rate · stevedore Mihir & Co'),
 R('CJ-15A', 'Belmoira', 'EXP', 'Salt in bulk', 18825, 58300, 0, '5/5/0', 10, 'COMPLETED 20:15, LEFT THE BERTH 22:53 on 23 Nov — 58,300 MT of salt, the last 18,825 on 10 hooks · destination printed: Karachi'),
 R('CJ-15A', 'Ocean Kudos', 'EXP', 'Salt in bulk', 4500, 4500, 65690, '0/0/5', 5, 'MADE FAST 01:00, COMMENCED 03:00 on 24 Nov — 4,500 MT in the first 4 hours on 5 hooks; 65,690 left → about 26 Nov 11:35 at her 30,000 quote · destination printed: Karachi', True, '11-24 03:00'),
 R('CJ-16', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes', 1770, 7865, 3848, '3/3/3', 9, '1,770 MT in 24 h on 9 hooks (3,340 the day before) — 7,865 loaded, 3,848 left → about ' + eta(3848, 1770) + ' at this rate'),
 R('MS', 'Sea Postman', 'IMP', 'Rock phosphate', 7196, 28400, 100, '2/2/2', 6, '7,196 MT into barges in 24 h on 6 hooks — 28,400 off, only 100 left: she finishes at midstream this morning'),
 R('MS', 'Libra', 'EXP', 'Rice bags', 2310, 22943, 57, '1/1/1', 3, '2,310 MT in 24 h (15 through IFFCO, completed there 08:00) — 22,943 loaded, 57 left'),
 R('MS', 'Sheng Tai', 'EXP', 'Barite ore', 2000, 27237, 28763, '1/1/1', 3, 'daughter vessel, ship-to-ship from African Loon — 2,000 MT in 24 h; 27,237 loaded, 28,763 left'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 2000, 27237, 30513, '1/1/1', 3, 'mother vessel — 2,000 MT to Sheng Tai in 24 h; 27,237 off, 30,513 left'),
 R('MS', 'Manta Omer Mecit', 'IMP', 'Fertiliser in J-bags', 1268, 1268, 2471, '0/1/1', 2, 'OTB 17:30, MADE FAST 20:00, COMMENCED 21:45 on 23 Nov — 1,268 MT into barges on 2 hooks; 2,471 left', True, '11-23 21:45'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 1202, 4864, 40104, '2/2/2', 6, 'at midstream 4,300 pcs / 1,202 CBM in 24 h on 6 hooks (1,314 the day before) — 4,864 CBM off, 40,104 left'),
 R('MS', 'Yara J', 'IMP', 'Rice bags', 876, 28233, 1767, '2/2/2', 6, '876 MT into barges in 24 h on 6 hooks (80 landed at CJ) — 28,233 off, 1,767 left'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 739, 5800, 12000, '2/2/2', 6, '739 MT in 24 h on 6 hooks (1,520 through CJ/OP) — 5,800 loaded, 12,000 left'),
 R('MS', 'North Gate', 'EXP', 'Chick peas / rice J-bags', 694, 24821, 886, '0/1/1', 2, '694 MT in 24 h on 2 hooks (500 through OP/CJ) — 24,821 loaded, 886 left'),
 R('MS', 'MAK 1', 'EXP', 'Rice in J-bags', 620, 21888, 0, '1/1/1', 3, 'COMPLETED 19:30 on 23 Nov — 21,888 MT; the last 620 on 3 hooks'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 0, 7000, 3000, '', 0, 'no work for the second day — 3,000 left (949 at CJ/IFFCO)'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no work — 4,470 left'),
 R('OJ-1', 'Bogazici (LPG/C)', 'IMP', 'Propane / butane', 0, 0, 24000, '', 0, '"TODAY BERTHING" at 0700 on 24 Nov — 24,000 MT to discharge (day signal: IN o/c, Capt Verma, flood)', True, None),
 R('OJ-2', 'Rasheeda', 'EXP', 'Chemicals', 4356, 4356, 0, '', 0, 'COMMENCED 10:50 on 23 Nov, COMPLETED 04:55, LEFT THE BERTH 07:00 on 24 Nov — 4,356 MT'),
 R('OJ-3', 'Hartati', 'EXP', 'Chemicals', 910, 11000, 0, '', 0, 'COMPLETED 21:30, LEFT THE BERTH 23:20 on 23 Nov — 11,000 MT'),
 R('OJ-3', 'Hafnia Ammolite', 'IMP', 'CDSBO', 6016, 12986, 17814, '', 0, 'work stopped 20:48, let go OJ-1 23:45 on 23 Nov — SHIFTED to OJ-3: re-made fast 01:00, re-commenced 01:42 on 24 Nov · 6,016 MT in the 24 h; 12,986 off, 17,814 left'),
 R('OJ-4', 'Al Mahboobah', 'EXP', 'Benzene', 7698, 7698, 1638, '', 0, 'MADE FAST 09:24, COMMENCED 12:30 on 23 Nov — 7,698 MT in 18½ h; 1,638 left → about 11:00 on 24 Nov', True, '11-23 12:30'),
 R('OJ-6', 'Willows', 'IMP', 'MS', 14204, 18277, 9723, '', 0, '14,204 MT in 24 h — 18,277 off, 9,723 left → about ' + eta(9723, 14204) + ' at this rate'),
 R('OJ-7', 'Ginga Cheetah', 'IMP', 'CDSBO + CSFO', 9459, 24239, 31, '', 0, '9,459 MT in 24 h — 24,239 off, 31 left; her 05:14 sailing was struck off the night sheet ("postponed due to delay in cargo operation") — day signal: OUT 10:00'),
 R('TT-1', 'Blue Ionian', 'IMP', 'Sugar bulk', 12151, 12421, 60934, '', 0, '12,151 MT in her first full day — 12,421 off, 60,934 left → about ' + eta(60934, 12151) + ' at this rate'),
 R('TT-2', 'Woohyun Dream', 'EXP', 'RSM in bulk', 8010, 30270, 1230, '', 0, '8,010 MT in 24 h — 30,270 loaded, 1,230 left → done about ' + eta(1230, 8010)[-5:] + ' on 24 Nov'),
 R('TT-3', 'Marvelous Star', 'IMP', 'Coal in bulk', 2327, 76844, 0, '', 0, 'COMPLETED 10:30, LEFT THE BERTH 18:54 on 23 Nov — 76,844 MT'),
 R('TT-3', 'MP Postpanamax 1', 'IMP', 'Coal in bulk', 1514, 1514, 86486, '', 0, 'MADE FAST 15:14 on 23 Nov, COMMENCED 05:00 on 24 Nov — 1,514 MT in the first two hours; 86,486 left', True, '11-24 05:00'),
]
a = B.s.index("const DPR={d:'23.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
old = B.s[a:e].split('\n'); ri = next(i for i, l in enumerate(old) if l.startswith(' rows:['))
keep = old[2:ri]
NEWDPR = ("const DPR={d:'24.11.2026',asOf:'11-24 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 24 Nov (PDF from Mihir, 24 Nov 10:40)',\n"
 " tot:{dry:155926,dryL:56954,dryU:98972,ms:14905,kict:30464,tuna:28411,oj:42643,vad:232969,all:505318,gangs:'PR 28 · TR 0 · 46 + 6 W gangs demanded / 46 + 6 W supplied',rakes:'3',wb:456,sail:'Tug Sagar 5 + barge Victoria 250 · CJ-14 · 12:50 · LPG/C Indonesia Energy and LPG/C Jenggala Bango · anchorage · 12:12'},\n"
 + "\n".join(keep) + ("\n" if keep else "") + " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]

# ================= MSWORK (Barge tab) — the DPR came as a PDF: its midstream and shore rows were keyed into the tool's pipe format by hand =================
out = subprocess.run(['python3', '-I', '/home/claude/berth-board/tools/barge_from_dpr.py', '/home/claude/work/in24a/dpr24_pipe.txt', '24.11', '11-24 07:00'], capture_output=True, text=True).stdout.rstrip('\n')
assert out.startswith("  {d:'24.11'") and out.endswith("]},"), out[-60:]
out = out.replace("c:'Fertilizer j/bags'", "c:'Fertiliser in J-bags'").replace("ag:'Jm Baxi'", "ag:'JM Baxi'")
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + out + "\n")

# ================= MV =================
MV1 = ['HM day signal 24 Nov (sheet dated 23/11, dispatched 21:15 / 05:47) · Capt Omesh · received 24 Nov 10:40 · cargo berths', [
 ['11:30', 'IN', 'Shebelle', 'OTB → CJ-12 · 101–109', 'Verma', '11-24 13:30', 'FLOOD · container · pilot boards 11:30, behind Enzo 2 — est'],
 ['12:30', 'SHIFT', 'Enzo 2', 'CJ-12 · 100–109 → OTB', 'Pathak', '11-24 12:30', 'container · written as a shift to OTB'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Verma — one hour PMS on completion (Capt Yadav struck off the sheet)', '—', '11-24 13:30', '']]]
MV2 = ['HM night signal 23 Nov — "amendment & new signal" (dispatched 21:00 / 01:28) · Capt G. Raj · with the hours DPR 24.11 prints · cargo berths', [
 ['20:00', 'OUT', 'Flag Marina', 'CJ-7 / 8 · 56¾–67¼ → OTB', 'Bali', '11-23 20:20', 'RT OUT (evening sheet 21:00) · DPR: completed 16:45, left the berth 20:20'],
 ['21:30', 'SHIFT', 'Parvraj', 'CJ-6 · 43–51¼ → 41¼–49½', 'G. Raj', '11-23 21:30', '"PORT C" (evening sheet 20:00)'],
 ['22:45', 'OUT', 'Belmoira', 'CJ-15A · 160½–171¾ → OTB', 'G. Raj', '11-23 22:53', 'evening sheet 23:45 · DPR: completed 20:15, left the berth 22:53'],
 ['o/c', 'IN', 'Gokova-M', 'OTB → CJ-7 · 50½–57', 'Bali', '11-23 23:05', 'FLOOD · DPR: made fast 23:05, commenced 23:55 — board had ~23:00'],
 ['o/c', 'IN', 'Ocean Kudos', 'OTB → CJ-15A · 159¼–171¾', 'G. Raj', '11-24 01:00', 'DPR: made fast 01:00, commenced 03:00 — board had ~01:45'],
 ['01:00', 'OUT', 'Al Hadbaa', 'CJ-11 · 88–94½ → OTB', 'Karan', '11-24 01:05', 'container (evening sheet: Sud 23:00) · DPR: completed 00:01, left the berth 01:05'],
 ['o/c', 'IN', 'DP World Godavari', 'OTB → CJ-11 · 87–97½', 'Sud', '11-24 01:55', '"ETA" · FLOOD · container · DPR: made fast 01:55'],
 ['o/c', 'IN', 'Horizon Chaser', 'OTB → CJ-3 · 17½–21¾', 'Sud', '11-24 04:00', '"ETA" (evening sheet: G. Raj 21:15) · DPR: made fast 04:00, not commenced at 0700 — board had ~23:15'],
 ['o/c', 'IN', 'Zheng Hui', 'OTB → CJ-8 · 58–67¾', 'Karan', '11-24 04:18', 'behind his 01:00 · DPR: made fast 04:18, commenced 06:25 — board had ~01:00'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Sud 22:15–22:45 · Capt Karan 04:00–05:00', '—', '11-24 05:00', '']]]
MV3 = ['DPR 24.11 — actual hours at the cargo jetties on 23 Nov (day and evening)', [
 ['12:02', 'OUT', 'TCI Anand', 'CJ-12 → OTB', '—', '11-23 12:02', 'container · completed 11:19, left the berth 12:02 (signal 12:00)'],
 ['12:50', 'OUT', 'Tug Sagar 5 + barge Victoria 250', 'CJ-14 → OTB', '—', '11-23 12:50', 'sailing box: 12:50 (signal RT OUT 11:00)'],
 ['13:20', 'IN', 'Enzo 2', 'OTB → CJ-12', '—', '11-23 13:20', 'container · made fast 13:20, commenced 14:10'],
 ['13:30', 'IN', 'Lila Tokyo', 'OTB → CJ-14', '—', '11-23 13:30', 'made fast 13:30, commenced 14:40 — board had ~12:45'],
 ['18:35', 'OUT', 'Vishva Bandhan', 'CJ-5 → OTB', '—', '11-23 18:35', 'completed 15:45, left the berth 18:35 (signal RT OUT 18:30)'],
 ['21:00', 'IN', 'Blue Shark', 'OTB → CJ-5', '—', '11-23 21:00', 'made fast 21:00, commenced 01:15 on the 24th — board had ~20:00']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MV1) + ",\n " + js(MV2) + ",\n " + js(MV3) + ",\n")

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
PREVKEYS = ('n', 'c', 'q', 'u', 'ie', 'ag', 'out', 'outBy')
def bline(bid):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]; tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln; d = dict(split_top(core[3:-1]))
    if set(d) - {'b', 'prev', 'now'}: B.die('berth extra keys: ' + bid + str(list(d)))
    return a, b, d, tail
def bput(a, b, d, tail): B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in ('b', 'prev', 'now')) + '}' + tail + B.s[b:]
def berth(bid, nown, add, f=None, nm=None, etc=None, qty=None, est=None):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    if f is not None: now['f'] = js(f)
    if est is False: now.pop('est', None)
    if nm is not None: now['nm'] = js(nm)
    if etc is not None: now['etc'] = js(etc)
    if qty is not None: now['q'] = repr(qty)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS); bput(a, b, d, tail)
def turn(bid, oldn, out, outBy, newn, f, est, add, nm=None, etc=None, qty=None):
    wa, wb = B.line_of("  {n:'%s'," % newn); wl = B.s[wa:wb].strip().rstrip(','); wv = obj(wl); assert 'n' in wv and 'c' in wv, list(wv)[:4]
    B.s = B.s[:wa] + B.s[wb + 1:]
    a, b, d, tail = bline(bid); now = obj(d['now']); assert oldn in now['n'], (oldn, now['n'])
    pv = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}; pv['out'] = js(out); pv['outBy'] = js(outBy)
    nw = {k: wv[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'rank', 'ag') if k in wv}; nw['f'] = js(f)
    if est: nw['est'] = '1'
    if nm is not None: nw['nm'] = js(nm)
    if etc is not None: nw['etc'] = js(etc)
    if qty is not None: nw['q'] = repr(qty)
    nw['note'] = "'" + q(add + ' · ') + wv.get('rem', "''")[1:]
    d['prev'] = unobj(pv, PREVKEYS); d['now'] = unobj(nw, NOWKEYS); bput(a, b, d, tail)
# OJ-3: Hartati out, Hafnia Ammolite across from OJ-1 (the vessel object is copied before OJ-1 is turned over)
a1, b1, d1, t1 = bline('OJ-1'); haf = obj(d1['now']); assert 'Hafnia Ammolite' in haf['n']
a3, b3, d3, t3 = bline('OJ-3'); har = obj(d3['now']); assert 'Hartati' in har['n']
pv = {k: har[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in har}; pv['out'] = js('11-23 23:20')
pv['outBy'] = js('DPR 24.11: completed 21:30, LEFT THE BERTH 23:20 on 23 Nov — 11,000 MT (night signal: OUT 23:00, Capt Sud)')
nw = dict(haf); nw['f'] = js('11-24 01:00'); nw.pop('est', None)
nw['note'] = "'" + q(D + ": SHIFTED FROM OJ-1 — work stopped 20:48, let go 23:45 on 23 Nov; RE-MADE FAST at OJ-3 01:00, re-commenced 01:42 on 24 Nov · 6,016 MT in the 24 h; 12,986 off, 17,814 left · " + SN + ": SHIFT \"o/c\" · Capt Bali · red remark \"agent attendance\" (hard to read) · she first made fast at OJ-1 on 22 Nov 10:00" + ' · ') + haf['note'][1:]
d3['prev'] = unobj(pv, PREVKEYS); d3['now'] = unobj(nw, NOWKEYS); bput(a3, b3, d3, t3)
turn('OJ-1', 'Hafnia Ammolite', '11-23 23:45', 'DPR 24.11: work stopped 20:48, let go 23:45 on 23 Nov — SHIFTED to OJ-3 (re-made fast 01:00 on 24 Nov), not sailed',
     'Bogazici (LPG/C)', '11-24 09:00', True, SD + ': IN "o/c" · Capt Verma (Capt Yadav struck off) · "ETA" · OTB → OJ-1 · FLOOD · marked ② — his second move after Rasheeda\'s 07:00 → about 09:00, est · DPR 24.11: "TODAY BERTHING" · propane / butane 24,000 MT')
turn('OJ-2', 'Rasheeda', '11-24 07:00', 'DPR 24.11: commenced 10:50 on 23 Nov, completed 04:55, LEFT THE BERTH 07:00 on 24 Nov — 4,356 MT (day signal: OUT 07:00, Capt Verma, "speed 6.5 kts")',
     'Chemroute Pegasus', '11-24 07:30', True, SN + ': IN 05:30 · Capt Karan · OTB → OJ-2 — added on the night sheet; the day sheet had her and struck the row, "preponed in night" · the pilot boards 05:30, Rasheeda let go 07:00 → alongside about 07:30, est · not yet on DPR 24.11 (position 0700)')
turn('OJ-7', 'Ginga Cheetah', '11-24 10:00', SD + ': OUT 10:00 · Capt Madaan — her 05:14 sailing was struck off the night sheet, "postponed due to delay in cargo operation" · DPR 24.11: 24,239 MT off, 31 left at 0700',
     'Sriwangi V', '11-24 11:45', True, SD + ': IN 09:45 · Capt Omesh · OTB → OJ-7 · FLOOD — the pilot boards 09:45, Ginga Cheetah sails at 10:00 → alongside about 11:45, est')
berth('OJ-4', 'Al Mahboobah', D + ': MADE FAST 23 Nov 09:24, COMMENCED 12:30 — 7,698 MT by 0700 on 24 Nov, 1,638 left → about 11:00 on 24 Nov (the board had about 08:25 for the berthing)', f='11-23 09:24', est=False)
berth('OJ-6', 'Willows', D + ': 14,204 MT in 24 h — 18,277 off, 9,723 left → about ' + eta(9723, 14204) + ' at this rate')
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-23 16:41',",
    lambda m: "const LIQ={prog:'" + q("DPR 24.11 + SIGNALS (night sheet 23 Nov, day sheet 24 Nov) — OJ-1 Hafnia Ammolite shifted to OJ-3 (re-made fast 01:00) → LPG/C Bogazici in on the flood, about 09:00 est · OJ-2 Rasheeda left 07:00 → Chemroute Pegasus in, about 07:30 est · OJ-3 Hartati left 23:20 on 23 Nov · OJ-7 Ginga Cheetah out 10:00 → Sriwangi V in, about 11:45 est · EARLIER: ") + m.group(1)
    + "',src:'DPA berthing list 23.11.26 as revised after the meeting · DPR 24.11 · programme 24.11 · signals to the day sheet of 24 Nov (disp 2115 / 0547)',asOf:'11-24 10:40',", B.s, count=1)
if k != 1: B.die('LIQ head not found')
LQ1 = ['HM day signal 24 Nov (sheet dated 23/11, dispatched 21:15 / 05:47) · Capt Omesh · oil-jetty rows', [
 ['07:00', 'OUT', 'Rasheeda', 'OJ-2 → OTB', 'Verma', '11-24 07:00', '① · "speed 6.5 kts" · DPR: completed 04:55, left the berth 07:00'],
 ['o/c', 'IN', 'Bogazici (LPG/C)', 'OTB → OJ-1', 'Verma', '11-24 09:00', '② · "ETA" · FLOOD · Capt Yadav struck off — est'],
 ['09:45', 'IN', 'Sriwangi V', 'OTB → OJ-7', 'Omesh', '11-24 11:45', 'FLOOD · pilot boards 09:45, behind Ginga Cheetah — est'],
 ['10:00', 'OUT', 'Ginga Cheetah', 'OJ-7 → OTB', 'Madaan', '11-24 10:00', 'her night sailing (05:14) was postponed'],
 ['—', 'IN', 'Chemroute Pegasus', 'OTB → OJ-2', '—', '11-24 07:30', 'row struck: "preponed in night" — see the night sheet']]]
LQ2 = ['HM night signal 23 Nov — "amendment & new signal" (dispatched 21:00 / 01:28) · Capt G. Raj · with the hours DPR 24.11 prints · oil-jetty rows', [
 ['23:00', 'OUT', 'Hartati', 'OJ-3 → OTB', 'Sud', '11-23 23:20', 'evening sheet: Capt Karan · DPR: completed 21:30, left the berth 23:20'],
 ['o/c', 'SHIFT', 'Hafnia Ammolite', 'OJ-1 → OJ-3', 'Bali', '11-24 01:00', 'red remark "agent attendance" · DPR: let go OJ-1 23:45, re-made fast OJ-3 01:00, re-commenced 01:42'],
 ['05:14', 'OUT', 'Ginga Cheetah', 'OJ-7 → OTB', 'Karan', '11-24 10:00', 'ROW STRUCK — "postponed due to delay in cargo operation" · day signal: OUT 10:00'],
 ['05:30', 'IN', 'Chemroute Pegasus', 'OTB → OJ-2', 'Karan', '11-24 07:30', 'new row · pilot boards 05:30, behind Rasheeda (left 07:00) — est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQ1) + ",\n  " + js(LQ2) + ",\n")

# ================= TUNA =================
def tuna(bid, text):
    a, b = B.line_of("  {b:'%s',n:" % bid); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(text + " ") + B.s[i:]
tuna('TT-1', D + ": 12,151 MT in her first full day — 12,421 off, 60,934 left → about " + eta(60934, 12151) + " at this rate.")
tuna('TT-2', D + ": 8,010 MT in 24 h — 30,270 loaded, 1,230 left → done about " + eta(1230, 8010)[-5:] + " on 24 Nov.")
a, b = B.line_of("  {b:'TT-3',n:'Marvelous Star'"); tail = ',' if B.s[a:b].endswith(',') else ''
B.s = B.s[:a] + "  " + js({'b': 'TT-3', 'n': 'MP Postpanamax 1', 'c': 'Coal in bulk', 'q': 88000, 'u': 'MT', 'ie': 'IMP', 'loa': 235, 'f': '11-23 15:14', 'ag': 'Taurus',
    'prev': 'Marvelous Star (coal 76,844 MT) — DPR 24.11: completed 10:30, left the berth 18:54 on 23 Nov', 'next': 'nobody named — RB Leah (coal, ETA 24 Nov 23:00) is marked "TT-03" on the revised list',
    'note': D + ": MADE FAST 15:14 on 23 Nov, COMMENCED 05:00 on 24 Nov — 1,514 MT in the first two hours; 86,486 left. The DPR prints her made fast before Marvelous Star's let-go hour (18:54) — one of the two hours is off. LIST 23.11: reported / ready 22 Nov 20:00 · 235 m, 14.41 m."}) + tail + B.s[b:]
a, b = B.line_of("  {n:'MP Postpanamax 1',"); B.s = B.s[:a] + B.s[b + 1:]
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda _: "const TUNA={src:'" + q("DPA berthing list 23.11.26 as revised after the meeting · DPR 24.11 · programme 24.11 · TT-3 MP Postpanamax 1 made fast 23 Nov 15:14 behind Marvelous Star · TT-2 Woohyun Dream nearly done, out 24 Nov 17:45 · TT-4 vacant") + "',", B.s, count=1)
assert k == 1
B.rep(" {d:'11-23',b:{'TT-1':'Blue Ionian','TT-2':'Woohyun Dream','TT-3':'Marvelous Star','TT-4':''}}\n];",
      " {d:'11-23',b:{'TT-1':'Blue Ionian','TT-2':'Woohyun Dream','TT-3':'Marvelous Star','TT-4':''}},\n {d:'11-24',b:{'TT-1':'Blue Ionian','TT-2':'Woohyun Dream','TT-3':'MP Postpanamax 1','TT-4':''}}\n];")

# ================= TIMBER =================
def tnote(name, text, tag=D):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('ML Egret', "22,448 pcs / 7,825 CBM in 24 h on 12 hooks — 38,006 off, 4,879 left → about " + eta(4879, 7825) + " at this rate")
tnote('Uni Blossom', "28,023 pcs / 9,097 CBM in 24 h on 12 hooks — 24,455 off, 10,414 left → about " + eta(10414, 9097) + " at this rate")
tnote('Dariya Priya', "at midstream 4,300 pcs / 1,202 CBM in 24 h on 6 hooks — 4,864 off, 40,104 left")

# ================= MYLOG — CD Glory: the board's reading moved from CJ-4 (26 Nov 00:13) to CJ-1 (25 Nov 22:20) =================
RD = {'d': '24 Nov 10:40 · DPR 24.11 + night and day signals', 'exp': '11-25 22:21', 'b': '1',
      'slot': "SAAGAR (SGR 3) · CJ-1 behind Crystal O is the board's reading · two SAAGAR berths come up at today's meeting — CJ-15 tonight, CJ-13 tomorrow midday",
      'why': "DPR 24.11 changed three paces. (1) SAFI ALFA slowed — 3,890 MT in 24 h against 5,154 the day before; CJ-4 now clears about 26 Nov 18:45, not 25 Nov 22:15, so CJ-4 is no longer her earliest berth. (2) CRYSTAL O at CJ-1 clears about 25 Nov 20:20 at 5,347 MT a day — the board now puts CD Glory there about 22:20 on 25 Nov. (3) The two timber berths clear sooner: ML EGRET about 22:00 tonight (4,879 CBM left), UNI BLOSSOM about 10:30 on 25 Nov (10,414 left). Both are SAAGAR places and the SAAGAR line is AG Varvara (SGR 1), Xin Hai Tong 71 (SGR 2), CD Glory (SGR 3). The board gives CJ-15 to Hai Nam 81 on her HP quote and CJ-13 to AG Varvara. BEST CASE: the port keeps both places for the SAAGAR line and counts Xin Hai Tong 71 by the project route — then CD Glory is on today's programme for CJ-13, about midday 25 Nov. MIDDLE: CJ-1, 25 Nov about 22:20. LATE: Crystal O slips or the 8K line (Manta Sena) takes CJ-1 — then CJ-4 behind Safi Alfa, about 26 Nov 20:45."}
i = B.s.index("'CD Glory':[", B.s.index('const MYLOG')); j = B.s.index("\n ],", i)
assert B.s[j - 1] == '}', B.s[j - 30:j]
B.s = B.s[:j] + ",\n  " + js(RD) + B.s[j:]

B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='24 Nov 2026 · 10:50 IST';", B.s, count=1)
B.save()
print({k: eta(*v) for k, v in {'Crystal O': (8323, 5347), 'DSM': (16438, 3410), 'Safi Alfa': (9688, 3890), 'Parvraj': (15400, 10102), 'Sand Topic': (10200, 37997), 'Uni Blossom': (10414, 9097), 'ML Egret': (4879, 7825), 'Hornbill': (3848, 1770), 'Willows': (9723, 14204), 'Blue Ionian': (60934, 12151), 'Woohyun': (1230, 8010)}.items()})
