#!/usr/bin/env python3
# apply43b — v198 (part 2, logs): meeting-call filter (no tug-and-barge), CD Glory's options and log entry, LEARN, PRED snapshot, PREDLOG rows and actual hours.
# Run after apply43a.py and after the horizon / gear lines (HZ 28 Nov; Arrabbiata found geared 4 x 30.5 t; Star New London searched, not stated).
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
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]

# ---- meeting call: a tug-and-barge is not counted among the berthed vessels (MEETLOG `got`), so it is not named in the call either
B.rep("const live=S.filter(x=>x.proj&&!x.shifted&&x.prevAt!=null&&fa(x)<=end&&x.F<=end+6)", "const live=S.filter(x=>x.proj&&!x.shifted&&x.prevAt!=null&&fa(x)<=end&&x.F<=end+6&&!/^tug\\b|\\bbarge\\b/i.test(x.n))")
B.rep(" // x.F<=end+6 (20 Nov, v190):", " // no tug-and-barge (21 Nov, v198): `got` does not count them, so the call does not name them · x.F<=end+6 (20 Nov, v190):")
B.rep("'Stalo':229,'Mak 1':186});", "'Stalo':229,'Mak 1':186.5}); // Mak 1: 186.5 as list 21.11 prints her under MS (186 online)")

# ---- CD Glory options
setline(" routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:3},", " routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:3},note:'" + q(
    "THE ONLY LINE THAT COUNTS FOR HER NOW. SAAGAR group — one bulk and one break-bulk place. List 21.11: AG Varvara (SGR 1), Xin Hai Tong 71 (2 — project cargo, goes by the project route), CD Glory (3), Dariya Priya (4 — now working at midstream), African Tiger (5). "
    "Uni Blossom made fast at CJ-13 on 21 Nov 02:00 and commenced 03:45. ML Egret's place — about 24 Nov at the DPR pace, list ETC 28 Nov — is AG Varvara's. Uni Blossom's place is CD Glory's. "
    "The list now prints Uni Blossom's permissible time: ETC 28 Nov 17:58 at the 4,600 norm. The board reckons her at 5,600 CBM a day (the record average of the completed log vessels) — through about 27 Nov 09:15 — and her place is then given at the meeting of 26 Nov: CJ-14, 26 Nov about 21:00. "
    "THE CONDITION: Uni Blossom must be clear by 18:00 on 27 Nov, which needs about 5,300–5,400 CBM a day from her. If she runs longer, CJ-14 goes to Crystal Land on the 26th and CD Glory berths about a day later (27 Nov night, CJ-1 on the board). Mihir's own reckoning (20 Nov 17:13) and the timber desk: 26 Nov.") + "'},")
setline("  {label:'6.5K / 8K',only:'8K',rk:{'8K':8},", "  {label:'6.5K / 8K',only:'8K',rk:{'8K':8},note:'" + q(
    "CLOSED. Mihir (20 Nov 16:50): CD Glory cannot berth under the 6.5K priority while other vessels are senior to her in it — the place goes by seniority, whichever berth frees first. She is 8K 8 on list 21.11; Manta Sena 1 (takes CJ-1 behind New Bliss, about 22 Nov), Crystal Land 2, Pioneer Fortune 3, Tan Bin 259 4, Gokova-M 5, Porto Fiscardo 6 and Captainannis L 7 stand ahead. Nothing by this line inside three weeks.") + "'},")
setline("  {label:'General · by seniority',only:'GEN',rk:{GEN:20},", "  {label:'General · by seniority',only:'GEN',rk:{GEN:20},note:'" + q(
    "CLOSED. Mihir (20 Nov 17:13): General goes strictly by seniority — a junior is not given a berth past the vessels senior to her. She is GEN 20; Blue Shark (GEN 1) is first, and some seventeen vessels stand ahead of her. Nothing by this line inside three weeks.") + "'}]}};")

# ---- MYLOG: CD Glory
a = B.s.index("\n 'CD Glory':[\n"); e = B.s.index("\n ]", a + 5)
ENT = {'d': '21 Nov 10:21 · list 21.11 + HM signal of 21 Nov', 'exp': '11-26 21:04', 'b': '14',
       'slot': "SAAGAR (SGR 3 now) — CJ-14, 26 Nov about 21:00, on Uni Blossom's place · holds only if Uni Blossom is clear by 18:00 on 27 Nov",
       'why': "List 21.11: she moves up to SGR 3 and 8K 8 — Uni Blossom is alongside (CJ-13, made fast 21 Nov 02:00, commenced 03:45). Her date does not move: the night of 26 Nov at CJ-14 (an hour earlier on the board only because the vessel before her at CJ-14 is now Belmoira, not Hai Nam 81). "
              "What is new is the list's permissible time for Uni Blossom: ETC 28 Nov 17:58 at the 4,600 norm. The board reckons Uni Blossom at 5,600 CBM a day — the record average — through about 27 Nov 09:15, and her place is then given at the meeting of 26 Nov. "
              "If Uni Blossom is not clear by 18:00 on 27 Nov (she needs about 5,300–5,400 CBM a day for that), CJ-14 goes to Crystal Land on the 26th and CD Glory berths about a day later. "
              "Ahead of her in SAAGAR: AG Varvara (takes ML Egret's place, about 23 Nov) and Xin Hai Tong 71 (project cargo — by the project route, CJ-14 on 22 Nov). Dariya Priya (SGR 4, behind her) has started discharging at midstream."}
B.s = B.s[:e] + ",\n  " + js(ENT) + B.s[e:]

# ---- LEARN
L = {'d': '21 Nov 10:21 · list 21.11 (0700) + HM signal 21 Nov (disp 07:46)',
     'v': "The night of 20–21 Nov and the day of 21 Nov, against the list of 21 Nov and the morning signal sheet.",
     'exp': "Board (v196 / v197): Safi Alfa into CJ-4 about 19:30 on 20 Nov, at 3,000 MT a day; Parvraj CJ-6 about 21:30; Uni Blossom CJ-13 about 02:30 on 21 Nov; and by programme 21.11 — Seacon Monaco out 15:00, Ken Ann out 16:00, Yuan Hang Wei Ye in 17:00, Vishva Bandhan shifted and Flag Marina in about 18:00. Next on the Coastal place: Belmoira (30K / 25K quote), CJ-15A on 22 Nov.",
     'act': "List 21.11: Safi Alfa MADE FAST 17:50 (norm 3,450, ETC 28 Nov 00:00) · Parvraj 22:50 (norm 14,950, ETC 24 Nov 08:17) · Uni Blossom 02:00, commenced 03:45 (norm 4,600, ETC 28 Nov 17:58) · Ken Ann had berthed 13:50 on the 20th. Signal 21 Nov (disp 07:46): Flag Marina IN 09:00, Vishva Bandhan SHIFT 10:15 (\"PORT C.\"), Ken Ann RT OUT 10:30, Seacon Monaco OUT and Yuan Hang Wei Ye IN \"o/c\" — the whole day's programme five to seven hours early; TCI Express (not TCI Anand) into CJ-11. Waiting sheet: tug Sagar 5 with barge Victoria 250 declared ready for today's meeting with CSTL 1 · Ocean Kudos printed with ranks again (HP 3 · 8K 11) · Dariya Priya and Sea Postman \"working at MS\" · the expected sheet prints \"PAIWAN ICE\", agent Mihir.",
     'why': "The berthing hours came within about an hour and a half of the board's estimates. The day moves ran early because a programme's hours are outward READINESS times: once the outgoing vessel is finished and the tide serves, the harbour master moves her (Ken Ann's 24 hours ran only to 13:50). On the Coastal place: a tug-and-barge with a printed CSTL 1 is a real coastal call and stands ahead of a 30K / 25K quote — so the board now gives the Coastal place to the tug (CJ-3, the empty short berth) and carries Belmoira on the next Govt place instead (CJ-14, 23 Nov).",
     'fix': "Hours corrected from the list; norms and ETCs entered as printed. Uni Blossom keeps the board's own estimate for the berth (5,600 CBM a day → about 27 Nov 09:15) with the list ETC shown beside it — CD Glory's 26 Nov depends on it. A tug-and-barge is no longer named in the meeting call (it is not counted among the berthed vessels either). Horizon moved to 28 Nov. OPEN (1): OCEAN KUDOS — list 21.11 prints her with ranks again (HP 3 · 8K 11 · GEN Y, readiness 18 Nov 16:06) and without \"B'TODAY\". Mihir said on 20 Nov that she is not ready; she is still HELD out of the projection on his word — is she ready now? OPEN (2): \"PAIWAN ICE\" on the expected sheet (pine logs 36,904.588, 182.93 m, ETA 22 Nov, agent Mihir) is read as the PAIWAN ACE of the timber desk sheet — to confirm.",
     'st': 'open'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(L) + ",\n")

# ---- PRED snapshot
S = json.load(open('/home/claude/work/S198.json'))
def dm(t):
    mon = {'11': 'Nov', '12': 'Dec'}[t[:2]]; return str(int(t[3:5])) + ' ' + mon + ' ' + t[6:]
SIG = 'HM signal 21 Nov (disp 07:46)'
FIX = [
 ['Ken Ann', 'sails', '21 Nov 10:30', SIG + ' · RT OUT · Capt Yadav + Neeraj'],
 ['Vishva Bandhan', '5', '21 Nov 11:15', SIG + ' · SHIFT 10:15 from CJ-8, port a/c · 33¼–41½ · est'],
 ['Flag Marina', '7', '21 Nov 11:15', SIG + ' · IN 09:00 (pilot) · HP · 56¾–67¼, across CJ-7 and CJ-8 · est'],
 ['Seacon Monaco', 'sails', '21 Nov 11:45', SIG + ' · OUT o/c, after Flag Marina is in · est'],
 ['Yuan Hang Wei Ye (next call)', '9', '21 Nov 13:30', SIG + ' · IN o/c behind Seacon Monaco · GFPL · est'],
 ['Vishva Bandhan', 'sails', '21 Nov 17:13', 'DPR 20.11 pace, from CJ-5 — list ETC 22 Nov 14:33'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — project vessel; list 21.11 prints no sailing for her'],
 ['Europa Graeca', 'sails', '21 Nov 21:45', 'DPR 20.11 pace · Tuna TT-1 → Blue Ionian'],
 ['New Bliss', 'sails', '21 Nov 22:21', 'DPR 20.11 pace — list ETC 22 Nov 10:05'],
 ['SG Friendship', 'sails', '21 Nov 23:48', 'list ETC · OJ-3'],
 ['Silver Gertrude', 'sails', '22 Nov 02:48', 'list ETC · OJ-7'],
 ['Eva Richway', 'sails', '22 Nov 02:57', 'list ETC · OJ-4'],
 ['Nord Copper', 'sails', '22 Nov 03:03', 'list ETC at the 23,000 norm'],
 ['Hatnyanawati', 'sails', '22 Nov 05:06', 'list ETC · OJ-2'],
 ['Artigo', 'sails', '22 Nov 07:26', 'list ETC · OJ-1'],
 ['Flag Marina', 'sails', '23 Nov 21:35', 'board estimate at the 42,500 norm'],
 ['Yuan Hang Wei Ye (next call)', 'sails', '24 Nov 02:00', 'board estimate — about 20,000 a day assumed'],
 ['African Hornbill (blades, next call)', 'sails', '24 Nov 04:00', 'board estimate — no norm printed'],
 ['Parvraj', 'sails', '24 Nov 08:17', 'list ETC at the 14,950 norm'],
 ['ML Egret', 'sails', '24 Nov 09:40', 'DPR 20.11 pace — list ETC 28 Nov 07:30'],
 ['Uni Blossom', 'sails', '27 Nov 09:15', 'board estimate at 5,600 CBM a day — list ETC 28 Nov 17:58'],
 ['Safi Alfa', 'sails', '28 Nov 00:00', 'list ETC at the 3,450 norm'],
]
PN = {'Tug Sagar 5 + barge Victoria 250': 'Coastal (CSTL 1, ready 21 Nov 11:00) · the empty CJ-3',
      'Manta Sena': '6.5K / 8K (8K 1) · after New Bliss',
      'Xin Hai Tong 71': 'Govt slot as SAAGAR project · after Nord Copper',
      'Blue Shark': 'General (GEN 1) · after Heng Yuan Fa Zhan',
      'Belmoira': 'Govt slot as 30k/25k quote (Sr No 7) · after Xin Hai Tong 71',
      'AG Varvara': "SAAGAR (SGR 1) · ML Egret's place · CJ-5 after Vishva Bandhan",
      'Tai Keystone': 'Govt · after Flag Marina',
      'Gokova-M': 'Coastal slot as 30k/25k quote (Sr No 7) · after Flag Marina',
      'Hai Nam 81': '24-hrs slot as 30k/25k quote (Sr No 7) · after African Hornbill',
      'Zheng Hui': 'Govt · after Gokova-M',
      'CD Glory': "SAAGAR (SGR 3) · Uni Blossom's place · after Belmoira",
      'Crystal Land': '6.5K / 8K (8K 2) · after ML Egret',
      'Fortunelit': 'General (GEN 2) · after Safi Alfa'}
assert set(x['n'] for x in S) == set(PN), set(x['n'] for x in S) ^ set(PN)
PRJ = [[x['n'], x['b'], dm(x['F']), 'board projection — ' + PN[x['n']]] for x in S]
a = B.s.index("const PRED=["); e = B.s.index("\n];", a)
B.s = B.s[:a] + "const PRED=[ // snapshot 21 Nov (v198) — list 21.11 + HM signal 21 Nov (disp 07:46); to be read against DPR 21.11, programme 22.11 and the next signal sheets\n " + ",".join(js(r) for r in FIX + PRJ) + B.s[e:]

# ---- PREDLOG: actual hours from list 21.11 (and two older ones never filled), then the new rows
ACT = {'Safi Alfa': ('4', '11-20 17:50'), 'Parvraj': ('6', '11-20 22:50'), 'Uni Blossom': ('13', '11-21 02:00'), 'Ken Ann': ('5', '11-20 13:50'),
       'Nord Copper': ('14', '11-20 02:06'), 'Heng Yuan Fa Zhan': ('15A', '11-19 22:06')}
a = B.s.index("const PREDLOG=["); e = B.s.index("\n];", a); blk = B.s[a:e]; n_f = 0
out = []
for ln in blk.split('\n'):
    m = re.match(r" \{v:'((?:[^'\\]|\\.)*)',predAt:'[^']*',pb:(?:null|'[^']*'),pt:(?:null|'[^']*'),ab:'',at:''", ln)
    if m and m.group(1) in ACT:
        ab, at = ACT[m.group(1)]; ln = ln.replace(",ab:'',at:''", ",ab:'%s',at:'%s'" % (ab, at), 1); n_f += 1
    out.append(ln)
blk = '\n'.join(out); print('PREDLOG rows filled:', n_f)
TAG = '21 Nov 10:21 — list 21.11 + HM signal 21 Nov: '
NEWR = [
 {'v': 'Flag Marina', 'predAt': '11-21 10:21', 'pb': '7', 'pt': '11-21 11:15', 'ab': '', 'at': '', 'src': 'prog', 'note': 'HM signal 21 Nov (disp 07:46) — IN 09:00 (pilot), alongside once Vishva Bandhan has left CJ-8; reading, not scored'},
 {'v': 'Tug Sagar 5 + barge Victoria 250', 'predAt': '11-21 10:21', 'pb': '3', 'pt': '11-21 18:00', 'ab': '', 'at': '', 'note': TAG + 'Coastal (CSTL 1, declared ready for the 21 Nov meeting) — the empty CJ-3'},
 {'v': 'Blue Shark', 'predAt': '11-21 10:21', 'pb': '15A', 'pt': '11-22 20:00', 'ab': '', 'at': '', 'note': TAG + 'General (GEN 1) — CJ-15A after Heng Yuan Fa Zhan; the Coastal place the board had given Belmoira there goes to the tug-and-barge'},
 {'v': 'Belmoira', 'predAt': '11-21 10:21', 'pb': '14', 'pt': '11-23 15:26', 'ab': '', 'at': '', 'note': TAG + 'Govt place as 30K / 25K quote — CJ-14 after Xin Hai Tong 71 (was CJ-15A on the Coastal place, 22 Nov)'},
 {'v': 'AG Varvara', 'predAt': '11-21 10:21', 'pb': '5', 'pt': '11-23 20:00', 'ab': '', 'at': '', 'note': TAG + "SAAGAR (SGR 1) — ML Egret's place, CJ-5"},
 {'v': 'Tai Keystone', 'predAt': '11-21 10:21', 'pb': '7', 'pt': '11-23 23:35', 'ab': '', 'at': '', 'note': TAG + 'Govt — CJ-7 after Flag Marina, who is in seven hours early'},
 {'v': 'Gokova-M', 'predAt': '11-21 10:21', 'pb': '8', 'pt': '11-24 02:00', 'ab': '', 'at': '', 'note': TAG + 'Coastal place as 30K / 25K quote — CJ-8 after Flag Marina'},
 {'v': 'Hai Nam 81', 'predAt': '11-21 10:21', 'pb': '16', 'pt': '11-24 06:00', 'ab': '', 'at': '', 'note': TAG + '24-hrs place as 30K / 25K quote — CJ-16 after African Hornbill (was CJ-14, 23 Nov)'},
 {'v': 'Zheng Hui', 'predAt': '11-21 10:21', 'pb': '8', 'pt': '11-25 18:36', 'ab': '', 'at': '', 'note': TAG + 'Govt — CJ-8 after Gokova-M; both Govt places are taken until Belmoira leaves'},
 {'v': 'CD Glory', 'predAt': '11-21 10:21', 'pb': '14', 'pt': '11-26 21:04', 'ab': '', 'at': '', 'note': TAG + "Mihir & Co — SAAGAR (SGR 3), CJ-14 on Uni Blossom's place. Date unchanged: 26 Nov night — if Uni Blossom is clear by 18:00 on 27 Nov"},
 {'v': 'Fortunelit', 'predAt': '11-21 10:21', 'pb': '4', 'pt': '11-28 02:00', 'ab': '', 'at': '', 'note': TAG + 'General (GEN 2) — CJ-4 after Safi Alfa (list ETC 28 Nov 00:00); new inside the horizon'},
]
blk += ",\n " + ",\n ".join(js(r) for r in NEWR)
B.s = B.s[:a] + blk + B.s[e:]
B.save()

# --- applied by hand between part a and part b / after part b (same version) ---
# const HZ=h('11-28 00:00'); OPT_HZ=h('12-12 00:00')
# GEAR['Arrabbiata']=['G','4×30.5 t','4 cranes × 30.5 t · 40,358 DWT, built 2025','Shipfix vessel directory · IMO 9979515'];  GEAR_NONE += 'Star New London'
# after `const ETA={...}`:  W.forEach(w=>{if(ETA[w.n])w.rep=h(ETA[w.n]);});   // expected vessels take their ETA as reporting hour
