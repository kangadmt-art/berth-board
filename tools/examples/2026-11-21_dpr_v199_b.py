#!/usr/bin/env python3
# apply44b — v199 (part 2, logs): PRED snapshot, PREDLOG rows, Rome Trader's last log entry, LEARN — after DPR 21.11 and the three projection fixes
# (shifted vessel must fit her new berth; free run cut at the ends of the berth's own quay; no shift for a junior in a seniority line).
import re, sys, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o):
    if o is None: return 'null'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'

# ---- MYLOG: Rome Trader — the record closes
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n"); e = B.s.index("\n ]", a + 5)
ENT = {'d': '21 Nov 11:22 · DPR 21.11 — completed and sailed', 'exp': '11-18 17:00', 'b': '13',
       'slot': 'SAILED · completed 20 Nov 20:00, left the berth 23:40 · 55,275 MT',
       'why': "DPR 21.11: COMPLETED 20:00 and LEFT THE BERTH 23:40 on 20 Nov — 55,275 MT loaded in 2 d 0½ h from commencement (18 Nov 19:25), about 27,300 MT a day; the last 19,631 MT went on board on 10 hooks in two shifts. She left fifty minutes ahead of the programmed 00:30 and five hours inside her permissible time (list ETC 21 Nov 04:40). Uni Blossom made fast behind her at 02:00. She leaves this card."}
B.s = B.s[:e] + ",\n  " + js(ENT) + B.s[e:]

# ---- LEARN
L = {'d': '21 Nov 11:22 · DPR 21.11 (0700)',
     'v': "The day of 20 Nov and the night, against the DPR of 21 Nov — and three faults the DPR brought out in the board's own projection.",
     'exp': "Board (v198): Rome Trader out 00:30 on 21 Nov (programme / signal) · Meghna Prestige out about 04:00 (est) · Jeil Crystal out 19:00, Jag Pushpa 17:45, Kestrel 11:00 (signals / programme) · ML Egret done about 24 Nov 09:40 (DPR 20.11 pace, 7,863 CBM a day) · New Bliss done about 21 Nov 22:20 · African Hornbill out about 24 Nov (a guess — no norm) · AG Varvara into CJ-5 on 23 Nov, Manta Sena into CJ-1 at 00:21 on 22 Nov.",
     'act': "DPR 21.11: Rome Trader COMPLETED 20:00, LEFT 23:40 on 20 Nov · Meghna Prestige completed 23:30, left 02:45 · Jeil Crystal left 20:00 · Jag Pushpa 17:55 · Kestrel 10:30 · Saga Viking 11:10 · Seacon Monaco completed 07:30 on the 21st. ML Egret 6,473 CBM in the day (25,854 left → about 25 Nov 06:50) · New Bliss 6,422 MT (6,072 left → about 22 Nov 05:40, so her list ETC 10:05 stands) · African Hornbill only 803 MT in a full day (10,804 left → about 4 Dec at that rate) · DSM London 4,846 MT with sugar bags started (→ about 26 Nov 16:00) · Sea Postman 8,484 MT and Dariya Priya 643 CBM at midstream.",
     'why': "Sailing hours were within an hour of the signals, mostly a little late; Rome Trader a little early. The moves in the projection come from two paces: ML Egret slowed by 1,400 CBM a day, which puts her place — AG Varvara's — a day later (CJ-5, 24 Nov evening); New Bliss slowed too, so Manta Sena waits for her list ETC (CJ-1, 22 Nov about noon). African Hornbill's 24 Nov was the board's guess before she had worked a full day; at 803 MT a day she holds CJ-16 for about two weeks, and the salt vessels that need a clean berth lose it. THREE FAULTS OF THE BOARD, found because CJ-16 closed: with that berth gone the engine 'shifted' Uni Blossom off CJ-13 — first into CJ-8, which lies under Flag Marina, then into CJ-5 — for Belmoira's 6.5K / 8K place, which she cannot take past Manta Sena. (1) the shift never checked that the shifted vessel fits the berth she is moved to; (2) the free run was measured on across CJ-9 to CJ-12, which the pool does not hold; (3) the shift ignored the seniority rule of the 6.5K / 8K line.",
     'fix': "All three corrected in the code (v199): the shifted vessel must fit her new berth beside its neighbours; the free run is cut at the ends of the berth's own quay (CJ-1 to CJ-8, CJ-13 to CJ-16); a line that goes by seniority makes no shift for a junior. No shift of Uni Blossom is projected now. Also: a status line no longer gives a completion date from a start-up of under six hours (Uni Blossom's first three hours, Woohyun Dream's first half hour) — the rate is counted from the commencement once she has six hours of work. African Hornbill is carried at the DPR pace, to be re-read with every DPR. The 21 Nov meeting call stays as published at 10:45, before the meeting (Blue Shark 15A · Manta Sena 1 · Xin Hai Tong 71 14) — the DPR came after the meeting hour and does not change it. CD Glory: unchanged, CJ-14 on 26 Nov night. STILL TO WATCH: by the strict General rule nobody is given CJ-5 between Vishva Bandhan (out tonight) and AG Varvara (24 Nov) — the list still prints Katerina K \"B'TODAY\"; programme 22.11 will show whether the port fills it.",
     'st': 'adopted'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(L) + ",\n")

# ---- PRED snapshot
S = json.load(open('/home/claude/work/S199.json'))
def dm(t):
    mon = {'11': 'Nov', '12': 'Dec'}[t[:2]]; return str(int(t[3:5])) + ' ' + mon + ' ' + t[6:]
SIG = 'HM signal 21 Nov (disp 07:46)'; DP = 'DPR 21.11 pace'
FIX = [
 ['Ken Ann', 'sails', '21 Nov 10:30', SIG + ' · RT OUT · Capt Yadav + Neeraj — DPR 21.11: 82 MT left at 0700'],
 ['Vishva Bandhan', '5', '21 Nov 11:15', SIG + ' · SHIFT 10:15 from CJ-8, port a/c · 33¼–41½ · est'],
 ['Flag Marina', '7', '21 Nov 11:15', SIG + ' · IN 09:00 (pilot) · HP · 56¾–67¼, across CJ-7 and CJ-8 · est'],
 ['Seacon Monaco', 'sails', '21 Nov 11:45', SIG + ' · OUT o/c — DPR 21.11: completed 07:30 · est'],
 ['SG Friendship', 'sails', '21 Nov 12:00', DP + ' · OJ-3 — list ETC 21 Nov 23:48'],
 ['Yuan Hang Wei Ye (next call)', '9', '21 Nov 13:30', SIG + ' · IN o/c behind Seacon Monaco · GFPL · est'],
 ['Vishva Bandhan', 'sails', '21 Nov 18:44', DP + ', from CJ-5 (before the hours lost on the shift) — list ETC 22 Nov 14:33'],
 ['Eva Richway', 'sails', '21 Nov 19:00', DP + ' · OJ-4 — list ETC 22 Nov 02:57'],
 ['Silver Gertrude', 'sails', '21 Nov 19:30', DP + ' · OJ-7 — list ETC 22 Nov 02:48'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — ' + DP + ' says about 21:00 (17 units left)'],
 ['Hatnyanawati', 'sails', '22 Nov 00:15', DP + ' · OJ-2 — list ETC 22 Nov 05:06'],
 ['Artigo', 'sails', '22 Nov 01:30', DP + ' · OJ-1 — list ETC 22 Nov 07:26'],
 ['Europa Graeca', 'sails', '22 Nov 02:00', DP + ' · Tuna TT-1 → Blue Ionian'],
 ['Nord Copper', 'sails', '22 Nov 03:03', 'list ETC at the 23,000 norm — ' + DP + ' about 04:45'],
 ['New Bliss', 'sails', '22 Nov 10:05', 'list ETC — ' + DP + ' about 05:40'],
 ['Marvelous Star', 'sails', '23 Nov 02:00', DP + ' · Tuna TT-3'],
 ['Flag Marina', 'sails', '23 Nov 21:35', 'board estimate at the 42,500 norm'],
 ['Yuan Hang Wei Ye (next call)', 'sails', '24 Nov 02:00', 'board estimate — about 20,000 a day assumed'],
 ['Parvraj', 'sails', '24 Nov 08:17', 'list ETC at the 14,950 norm'],
 ['ML Egret', 'sails', '25 Nov 06:51', DP + ' (6,473 CBM a day) — list ETC 28 Nov 07:30'],
 ['DSM London', 'sails', '26 Nov 15:54', DP + ' (4,846 MT a day) — list ETC 30 Nov 13:50'],
 ['Uni Blossom', 'sails', '27 Nov 09:15', 'board estimate at 5,600 CBM a day — list ETC 28 Nov 17:58'],
 ['Safi Alfa', 'sails', '28 Nov 00:00', 'list ETC at the 3,450 norm'],
 ['African Hornbill (blades, next call)', 'sails', '4 Dec 18:00', DP + ' (803 MT a day) — no norm printed'],
]
PN = {'Tug Sagar 5 + barge Victoria 250': 'Coastal (CSTL 1, ready 21 Nov 11:00) · the empty CJ-3',
      'Xin Hai Tong 71': 'Govt slot as SAAGAR project · after Nord Copper',
      'Manta Sena': '6.5K / 8K (8K 1) · after New Bliss (list ETC 10:05)',
      'Blue Shark': 'General (GEN 1) · after Heng Yuan Fa Zhan',
      'Belmoira': 'Govt slot as 30k/25k quote (Sr No 7) · after Xin Hai Tong 71',
      'Tai Keystone': 'Govt · after Flag Marina',
      'Gokova-M': 'Coastal slot as 30k/25k quote (Sr No 7) · after Flag Marina',
      'AG Varvara': "SAAGAR (SGR 1) · ML Egret's place · CJ-5 after Vishva Bandhan",
      'Hai Nam 81': '24-hrs slot as 30k/25k quote (Sr No 7) · after ML Egret (CJ-16 is held by African Hornbill)',
      'Zheng Hui': 'Govt · after Gokova-M',
      'Fortunelit': 'Bitumen slot as General (GEN 2) · after DSM London',
      'CD Glory': "SAAGAR (SGR 3) · Uni Blossom's place · after Belmoira",
      'Crystal Land': '6.5K / 8K (8K 2) · after Hai Nam 81',
      'Crystal O': 'General (GEN 3) · after Safi Alfa'}
assert set(x['n'] for x in S) == set(PN), set(x['n'] for x in S) ^ set(PN)
PRJ = [[x['n'], x['b'], dm(x['F']), 'board projection — ' + PN[x['n']]] for x in S]
a = B.s.index("const PRED=["); e = B.s.index("\n];", a)
B.s = B.s[:a] + "const PRED=[ // snapshot 21 Nov (v199) — list 21.11 + HM signal 21 Nov (disp 07:46) + DPR 21.11; to be read against programme 22.11, the next signal sheets and DPR 22.11\n " + ",".join(js(r) for r in FIX + PRJ) + B.s[e:]

# ---- PREDLOG: rows for the picks that moved with DPR 21.11
TAG = '21 Nov 11:22 — DPR 21.11: '
NEWR = [
 {'v': 'Manta Sena', 'predAt': '11-21 11:22', 'pb': '1', 'pt': '11-22 12:05', 'ab': '', 'at': '', 'note': TAG + '6.5K / 8K (8K 1) — CJ-1 behind New Bliss, whose pace slowed (6,422 MT, done about 05:40): her list ETC 10:05 stands. Was 22 Nov 00:21'},
 {'v': 'AG Varvara', 'predAt': '11-21 11:22', 'pb': '5', 'pt': '11-24 20:43', 'ab': '', 'at': '', 'note': TAG + "SAAGAR (SGR 1) — ML Egret's place, a day later: ML Egret did 6,473 CBM (7,863 the day before), done about 25 Nov 06:50. Was 23 Nov 20:00"},
 {'v': 'Hai Nam 81', 'predAt': '11-21 11:22', 'pb': '15', 'pt': '11-25 08:51', 'ab': '', 'at': '', 'note': TAG + '24-hrs place as 30K / 25K quote — CJ-15 after ML Egret; CJ-16 is held by African Hornbill (803 MT a day). Was CJ-16, 24 Nov 06:00'},
 {'v': 'Fortunelit', 'predAt': '11-21 11:22', 'pb': '2', 'pt': '11-26 17:54', 'ab': '', 'at': '', 'note': TAG + 'General (GEN 2) in the Bitumen slot — CJ-2 after DSM London (4,846 MT a day, done about 26 Nov 16:00). Was CJ-4, 28 Nov 02:00'},
 {'v': 'Crystal Land', 'predAt': '11-21 11:22', 'pb': '15', 'pt': '11-27 09:27', 'ab': '', 'at': '', 'note': TAG + '6.5K / 8K (8K 2) — after Manta Sena, who berths 12 h later; CJ-15 after Hai Nam 81. Was 26 Nov 23:40'},
 {'v': 'Crystal O', 'predAt': '11-21 11:22', 'pb': '4', 'pt': '11-28 02:00', 'ab': '', 'at': '', 'note': TAG + 'General (GEN 3) — CJ-4 after Safi Alfa (list ETC 28 Nov 00:00); new inside the horizon'},
 {'v': 'CD Glory', 'predAt': '11-21 11:22', 'pb': '14', 'pt': '11-26 21:04', 'ab': '', 'at': '', 'note': TAG + "Mihir & Co — unchanged: SAAGAR (SGR 3), CJ-14 on Uni Blossom's place, 26 Nov night. Uni Blossom has only three hours of work on the sheet — no rate yet"},
]
a = B.s.index("const PREDLOG=["); e = B.s.index("\n];", a)
B.s = B.s[:e] + ",\n " + ",\n ".join(js(r) for r in NEWR) + B.s[e:]
B.save()

# --- applied by hand between part a and part b (same version): three fixes in simulate() ---
# 1. `mov` filter of the port-convenience shift:  ... &&runFor(need.w,x.b,e.t+0.5,x.n)&&runFor({loa:x.loa||LOA[x.n]||180},e.b,e.t+0.5,x.n)
# 2. runFor(): const seg=CLEAN.includes(b)?[110,189]:[0,68];  gaps cut to seg before the best run is chosen
# 3. const SENIOR_ONLY=['8K'] moved to the top level (after GEN_STRICT); in the shift block, before `if(cl){need=...}`:
#    if(cl&&SENIOR_ONLY.includes(C.k)&&q.some(x=>x!==cl&&rkv(x,C.k)<rkv(cl,C.k)&&allowedBerths(x).length>0))continue;
