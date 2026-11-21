#!/usr/bin/env python3
# apply43a — v198 (part 1, data): DAILY BERTHING LIST 21.11.2026 (0700) and the HM signal sheet of 21 Nov (day sheet, dispatched 07:46, Capt Pathak).
# Received 21 Nov 10:21, no text. The day's programmed moves are signalled 5–7 hours ahead of programme 21.11:
# Vishva Bandhan SHIFT 10:15 (CJ-8 -> CJ-5, port a/c), Flag Marina IN 09:00, Ken Ann RT OUT 10:30, Seacon Monaco OUT o/c, Yuan Hang Wei Ye IN o/c, TCI Express IN 09:00 (CJ-11).
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P, list_tag='LIST 21.11'); q = B.q
LT = 'LIST 21.11'; SG = 'HM SIGNAL 21 Nov (day sheet, disp 07:46)'
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
def after(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:b + 1] + text + "\n" + B.s[b + 1:]
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]

# ================= HEADER =================
B.rep("const NOW=h('11-20 23:48');", "const NOW=h('11-21 10:21');")
B.rep("List <b>20.11 · revised after the meeting</b> · DPR <b>20.11</b> · Programme <b>21.11</b> · Signals to <b>20 Nov amended sheets, both pages (disp 1240 / 1325 / 1400)</b>",
      "List <b>21.11 · 0700</b> · DPR <b>20.11</b> · Programme <b>21.11</b> · Signals to <b>21 Nov day sheet (disp 0746)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 21 Nov 10:21: the BERTHING LIST 21.11 (0700) and the HM SIGNAL SHEET of 21 Nov (day sheet, disp 07:46) — the day's moves are signalled five to seven hours ahead of programme 21.11: Vishva Bandhan shifted CJ-8 → CJ-5 at 10:15, Flag Marina in (pilot 09:00), Ken Ann out 10:30, Seacon Monaco out and Yuan Hang Wei Ye in \"on completion\". The list gives the night's actual hours (Safi Alfa made fast 20 Nov 17:50, Parvraj 22:50, Uni Blossom 21 Nov 02:00) and the first norms / ETCs for them · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 21 Nov (day sheet, disp 0746) · list 21.11 (0700) · ")

# ================= V — signal sheet 21 Nov + list 21.11 =================
M = "{b:'8',n:'Vishva Bandhan',nm:9258,p:[59.5,68]"
pre(M, SG + ": SHIFT 10:15 · Capt Pathak · 59½–68 → 33¼–41½, \"PORT C.\" written in red — the shift programme 21.11 had put after Ken Ann's 16:00 is brought forward by about seven hours. " + LT + ": she is already printed at CJ-5, 33¼–41½, with \"S1 59½–68\".")
sub(M, "f:'11-17 18:30',t:'11-21 18:00',lt:'11-22 14:33',est:1", "f:'11-17 18:30',t:'11-21 11:15',lt:'11-22 14:33',est:1")
M = "{b:'5',n:'Vishva Bandhan',nm:9258,p:[33.25,41.5]"
pre(M, SG + ": SHIFT 10:15 · Capt Pathak · on the port's account — into 33¼–41½ as soon as Ken Ann is clear (RT OUT 10:30): about 11:15 alongside, est. " + LT + ": GOV · CJ-5 · 33¼–41½ · norm 9,258 · ETC 22 NOV 14:33 unchanged.")
sub(M, "f:'11-21 18:00',t:'11-22 14:33',est:1", "f:'11-21 11:15',t:'11-22 14:33',est:1")
M = "{b:'5',n:'Ken Ann',p:[33.5,41.5]"
pre(M, SG + ": RT OUT 10:30 · Capt Yadav + Neeraj · 33½–41½ → OTB — five and a half hours ahead of programme 21.11 (16:00). " + LT + ": \"[5]\" · MADE FAST 20 NOV 13:50, commenced 15:40 · ETC 21 Nov 13:50 (her 24 hours) — the board had estimated 12:30 for the berthing.")
sub(M, "f:'11-20 12:30',t:'11-21 16:00',est:1", "f:'11-20 13:50',t:'11-21 10:30',lt:'11-21 13:50'")
M = "{b:'7',n:'Flag Marina',nm:42500,p:[56.75,67.25]"
pre(M, SG + ": IN 09:00 · Capt Deepak · OTB → 56¾–67¼ — the hour is the pilot boarding at OTB; she comes alongside once Vishva Bandhan has left CJ-8 (shift 10:15): about 11:15, est — almost seven hours ahead of the board's 18:00. " + LT + ": HP · CJ-7 · 56¾–67¼ · \"B'TODAY\" · US coal 1,03,250 MT · norm 42,500 — no ETC yet; at the norm about 23 Nov 21:30.")
sub(M, "f:'11-21 18:00',t:'11-24 04:20',est:1", "f:'11-21 11:15',t:'11-23 21:35',est:1")
M = "{b:'9',n:'Seacon Monaco',nm:20000,p:[69,76.75]"
pre(M, SG + ": OUT \"o/c\" (written in red over the hour) · Capt Deepak, after he has put Flag Marina alongside · 69–76¾ → OTB — about 11:45, est; programme 21.11 had 15:00. " + LT + ": \"[9]\" — sailing today.")
sub(M, "f:'11-18 06:36',t:'11-21 15:00',lt:'11-20 09:48'", "f:'11-18 06:36',t:'11-21 11:45',lt:'11-20 09:48',est:1")
M = "{b:'9',n:'Yuan Hang Wei Ye (next call)',p:[69,77.25]"
pre(M, SG + ": IN \"o/c\" · Capt Yadav, after Ken Ann's 10:30 · OTB → 69–77¼ behind Seacon Monaco — about 13:30 alongside, est (17:00 by programme 21.11). " + LT + ": GFPL · CJ-9 · 69–77¼ · \"B'TODAY\" · iron ore pellets 50,455 MT EXP · no norm printed — about 20,000 a day assumed, to about 24 Nov 02:00.")
sub(M, "f:'11-21 17:00',t:'11-24 05:30',est:1", "f:'11-21 13:30',t:'11-24 02:00',est:1")
M = "{b:'6',n:'Parvraj',nm:14950,p:[43,51.25]"
pre(M, LT + ": GOV · CJ-6 · MADE FAST 20 NOV 22:50, COMMENCED 21 Nov 01:05 · DAP 49,500 MT · NORM 14,950 · ETC 24 NOV 08:17 — the first norm and ETC printed for her; the board had about 21:30 for the berthing. The list prints her panels 42–51¼; the signal and programme 21.11 had 43–51¼ (kept).")
sub(M, "f:'11-20 21:30',t:'11-24 05:00',est:1", "f:'11-20 22:50',t:'11-24 08:17'")
M = "{b:'4',n:'Safi Alfa',nm:3000,p:[23,31.75]"
pre(M, LT + ": GENERAL · CJ-4 · MADE FAST 20 NOV 17:50, COMMENCED 20:00 · rice bags 24,750 MT (\"32100 – TOTAL\") · NORM 3,450 · ETC 28 NOV 00:00 — the first norm and ETC printed for her (the board had assumed 3,000 a day, to 29 Nov 01:30, and 19:30 for the berthing: she was alongside fifty minutes after Propel Confidence's shift). Panels printed 23–31¼ (signal: 23–31¾, kept).")
sub(M, "f:'11-20 19:30',t:'11-29 01:30',est:1", "f:'11-20 17:50',t:'11-28 00:00'")
B.rep("{b:'4',n:'Safi Alfa',nm:3000,p:[23,31.75]", "{b:'4',n:'Safi Alfa',nm:3450,p:[23,31.75]")
M = "{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]"
pre(M, LT + ": SAAGAR · CJ-13 · 113–124¾ · MADE FAST 21 NOV 02:00, COMMENCED 03:45 · pine logs 34,880 CBM · NORM 4,600 · ETC 28 NOV 17:58 — the permissible time, printed for the first time. The board keeps its own estimate for the berth: at 5,600 CBM a day (the record average of the completed log vessels) she is through about 27 Nov 09:15; her first DPR day will show the real pace.")
sub(M, "f:'11-21 02:30',t:'11-27 08:00',est:1", "f:'11-21 02:00',t:'11-27 09:15',lt:'11-28 17:58',est:1")
pre("{b:'14',n:'Nord Copper',nm:23000,p:[126.5,141.75]", LT + ": COASTAL · CJ-14 · made fast 20 Nov 02:06 · COMMENCED 20 NOV 12:00 — ten hours after she made fast · norm 23,000 · ETC 22 NOV 03:03 unchanged.")
pre("{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]", LT + ": PROJECT/STEEL · CJ-15A · 161¾–169 · printed without brackets — no sailing is programmed for her inside programme 21.11's window; the board's 21 Nov 21:30 stays an estimate.")
pre("{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]", LT + ": printed under HP with the remark \"SGR(PROJ)\" · CJ-16 · 173½–188 · no norm or ETC — unchanged.")
pre("{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]", LT + ": 6.5K / 8K · CJ-1 · norm 6,500 · ETC 22 NOV 10:05 — unchanged.")
pre("{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]", LT + ": SAAGAR · CJ-15 · 143½–156¾ · norm 4,600 · ETC 28 NOV 07:30 — unchanged; no shift printed.")
pre("{b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75]", LT + ": no longer on the at-berth sheet — she sailed in the night (the hour comes with DPR 21.11). She is back on the EXPECTED sheet for her next call: salt in bulk 65,900 MT EXP, ETA 24 Nov, agent BS Shg.")
pre("{b:'13',n:'Rome Trader (salt, next call)',nm:23000,p:[113,125.25]", "MIHIR & COMPANY · " + LT + ": no longer on the at-berth sheet — sailed; Uni Blossom made fast behind her at 02:00 on 21 Nov. Her let-go hour comes with DPR 21.11.")

# ================= name maps / constants =================
B.rep("Object.assign(REP,{'MSC Magali':'11-20 07:30'}); // revised list 20.11 — placed last so that it wins",
      "Object.assign(REP,{'MSC Magali':'11-20 07:30'}); // revised list 20.11 — placed last so that it wins\n"
      "Object.assign(REP,{'Manta Omer Mecit':'11-20 17:30','Sanghi Sundarshan':'11-21 01:12','Star New London':'11-21 03:06','Arrabbiata':'11-21 04:40'}); // list 21.11 — reporting hours of the vessels that came onto the waiting sheet")
after("Object.assign(AG,{'V Pacific':'Excel Infra','Kerem':'BS Shg'});",
      "Object.assign(AG,{'Star New London':'Gautham Freight','Arrabbiata':'BS Shg','Paiwan Ace':'Mihir & Company','Meghna Prestige (salt, next call)':'BS Shg'});"
      "Object.assign(IE,{'Star New London':'EXP','Arrabbiata':'EXP','Paiwan Ace':'IMP','Meghna Prestige (salt, next call)':'EXP'}); // list 21.11 — Paiwan Ace is printed \"PAIWAN ICE\" on the expected sheet, agent MIHIR")
setline("const ETA={'Manta Omer Mecit':", "const ETA={'Tai Keystone':'11-21 00:00','Zheng Hui':'11-21 10:00','Valentina Sea':'11-22 00:00','Princess Manissa':'11-22 00:00','V Pacific':'11-22 00:00','Paiwan Ace':'11-22 00:00',"
        "'Sand Topic':'11-22 03:00','Asian Summit':'11-22 08:00','Zheng Run':'11-22 12:00','Hai Nam 81':'11-22 16:00','Gutian Trust':'11-23 00:00','Hai Long 1':'11-23 00:00','Lolo Gate':'11-23 00:00','Outlander':'11-23 00:00',"
        "'KSS Edmond':'11-24 00:00','Kang Qi Fu Hua':'11-24 00:00','Kerem':'11-24 00:00','Meghna Prestige (salt, next call)':'11-24 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 21.11 (0700) — Tai Keystone and Zheng Hui are still printed on it")
a, b = B.line_of("const SAILDR={"); ln = B.s[a:b]
B.s = B.s[:b] + "\nObject.assign(SAILDR,{'Hai Nam 81':12.6,'Zheng Run':12.63}); // list 21.11 remarks: \"DD-12.60M.\" / \"DD- 12.63\"" + B.s[b:]

# ================= W — list 21.11 =================
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Blue Shark', "GEN 1 — the senior vessel of the General line now that Safi Alfa is alongside", rk="GEN:1")
w('Fortunelit', "GEN 2 · working at MS", rk="GEN:2")
w('Crystal O', "GEN 3 · working at MS", rk="GEN:3")
w('Manta Sena', "8K 1 · GEN 4", rk="'8K':1,GEN:4")
w('Crystal Land', "8K 2 · GEN 5", rk="'8K':2,GEN:5")
w('Libra', "GEN 6 · working at MS", rk="GEN:6")
w('Pioneer Fortune', "8K 3 · GEN 8 · Sr No 7 — unchanged (no GEN 7 is printed: the column is renumbered only down to Libra)")
w('Tan Bin 259', "8K 4 · GEN 14 · Sr No 7 · working at MRG 3", rk="'8K':4,GEN:14")
w('Gokova-M', "HP 1 · 24H 1 · 8K 5 · GEN 15", rk="HP:1,'24H':1,'8K':5,GEN:15")
w('AG Varvara', "SGR 1 · GEN 16 · Sr No 7 — the senior vessel of the SAAGAR line now that Uni Blossom is alongside", rk="SAAGAR:1,GEN:16")
w('Xin Hai Tong 71', "SGR 2 · STL 1 · GEN 17 (STL kept out — Mihir, 15 Nov)", rk="SAAGAR:2,GEN:17")
w('Tug Sagar 5 + barge Victoria 250', "READINESS DECLARED 21 Nov 11:00 (was N/A) · CSTL 1 · STL 2 (both were Y) · 3,804.5 MT (4,000 before) · VCN now printed · the remark \"NR\" still stands beside it", rk="COASTAL:1,STL:2", rdy="11-21 11:00", qty="3804.5")
w('Porto Fiscardo', "8K 6 · GEN 18", rk="'8K':6,GEN:18")
w('Captainannis L', "8K 7 · GEN 19 · DOC NR · working at MS", rk="'8K':7,GEN:19")
w('CD Glory', "SGR 3 · 8K 8 · GEN 20 · Sr No 7 — up one place in SAAGAR and in 6.5K / 8K: Uni Blossom is alongside. Ahead of her in SAAGAR: AG Varvara (1) and Xin Hai Tong 71 (2)", rk="SAAGAR:3,'8K':8,GEN:20")
w('Dariya Priya', "SGR 4 · 8K 9 · GEN 21 · Sr No 7 · remark now \"WORKING AT MS\" — the at-berth sheet prints her under MS, COMMENCED 20 Nov 11:40: she has started discharging her logs at midstream", rk="SAAGAR:4,'8K':9,GEN:21")
w('Sea Postman', "GEN 22 · remark now \"WORKING AT MS\" — the at-berth sheet prints her under MS, COMMENCED 20 Nov 10:50: the rock phosphate is being discharged at midstream")
w('African Tiger', "SGR 5 · 8K 10 · GEN 25 · Sr No 7", rk="SAAGAR:5,'8K':10,GEN:25")
w('Ocean Kudos', "the sheet prints her with RANKS again — HP 3 · 8K 11 · GEN Y — readiness still 18 Nov 16:06, and the \"B'TODAY\" is gone. Mihir (20 Nov 11:24) said she is NOT ready: STILL HELD on his word until he says her holds are passed", rk="HP:3,'8K':11,GEN:98")
w('Lila Tokyo', "HP 2 · GEN 24 · \"(GL)\" · 30K/25K/10K · CJ 7 & 8 or the clean berths — unchanged")
w('MSC Magali', "NOW ON THE WAITING SHEET · HP 4 (was Y) · \"(GL)\" · 30K/25K/10K", rk="HP:4")
w('Belmoira', "unchanged — starred, ranks X, \"B'TODAY\" still printed; she is not on the at-berth sheet and was not on programme 21.11")
w('Katerina K', "unchanged — starred, GEN X, \"B'TODAY\" still printed; she is not on the at-berth sheet and was not on programme 21.11")
w('Josco Taicang', "READINESS 21 Nov 11:00 (was N/A) — declared for today's meeting · VCN now printed · no group rank printed yet", rdy="11-21 11:00")
w('Manta Omer Mecit', "NOW ON THE WAITING SHEET · reported / ready 20 Nov 17:30 · 9.75 m · no group rank printed", rdy="11-20 17:30", dr="9.75")
w('Sanghi Sundarshan', "NOW ON THE WAITING SHEET · reported 21 Nov 01:12 · N/A · \"SPACE A/C\"")
w('Tai Keystone', "still on the EXPECTED sheet at 0700 on 21 Nov — ETA / readiness 21 Nov 00:00, no group rank printed")
w('Zheng Hui', "still on the expected sheet — ETA / readiness 21 Nov 10:00 · GEN Y")
w('Zheng Run', "ETA / READINESS 22 Nov 12:00 (was N/A) · HP Y · cargo now printed \"OXIDE PELLETS\" · transhipment · 30K/25K/10K Sr No 7 · DD 12.63 m · VCN printed", rk="HP:98", rdy="11-22 12:00", cargo="Oxide pellets")
B.wdel('North Gate (re-berthing)')
m = B._row('MSC Magali').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Star New London','Salt in bulk',58000,'MT',199.99,null,null,{'8K':98},'" + q(LT + ": NEW · reported 21 Nov 03:06 · N/A · 8K Y · \"30K/25K SR.NO:07\" · salt in bulk 58,000 MT EXP · 199.99 m · agent Gautham Freight") + "'],",
 " ['Arrabbiata','Rice in bags',34150,'MT',179.9,null,null,{},'" + q(LT + ": NEW ON THE WAITING SHEET · reported 21 Nov 04:40 · N/A · rice in bags 34,150 MT EXP · 179.9 m · agent BS Shg — she lay at CJ-11 until the night (programme 21.11: out 20 Nov 22:40; signal: RT SHIFT 02:00)") + "'],",
 " ['Paiwan Ace','Pine logs',36905,'CBM',182.93,11,null,{},'" + q("MIHIR & COMPANY · " + LT + " (ETA sheet): NEW — printed \"MV PAIWAN ICE\" · pine logs 36,904.588 (unit printed MT) IMP · ETA 22 Nov 00:00 · N/A · AGENT MIHIR · 182.93 m, 11.0 m. Read as the PAIWAN ACE of the timber desk sheet (Uruguay, ETA 22 Nov 01:00): same length, same day") + "'],",
 " ['Meghna Prestige (salt, next call)','Salt in bulk',65900,'MT',199.95,6.5,null,{},'" + q(LT + " (ETA sheet): NEW — her next call, to load · ETA 24 Nov · N/A · salt in bulk 65,900 MT EXP · agent BS Shg (her coal call at CJ-7 ended in the night of 20–21 Nov)") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
B.rep(" // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 20.11 (0700) and its issue revised after the meeting of 20 Nov",
      " // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 21.11 (0700)")

# ================= CD Glory options — ranks of list 21.11 =================
B.rep("routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:4},note:'THE ONLY LINE THAT COUNTS FOR HER NOW.", "routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:3},note:'THE ONLY LINE THAT COUNTS FOR HER NOW.")
B.rep("{label:'6.5K / 8K',only:'8K',rk:{'8K':9},note:'CLOSED.", "{label:'6.5K / 8K',only:'8K',rk:{'8K':8},note:'CLOSED.")

# ================= MV =================
MV1 = ['HM signal 21 Nov — day sheet (dispatched 07:46) · Capt Pathak · received 21 Nov 10:21', [
  ['10:15', 'SHIFT', 'Vishva Bandhan', 'CJ-8 · 59½–68 → CJ-5 · 33¼–41½', 'Pathak', '11-21 10:15', '"PORT C." in red — on the port\'s account · programme 21.11 had it after Ken Ann\'s 16:00'],
  ['09:00', 'IN', 'Flag Marina', 'OTB → CJ-7 / CJ-8 · 56¾–67¼', 'Deepak', '11-21 11:15', 'the hour is the pilot boarding — alongside once Vishva Bandhan has left CJ-8, about 11:15 est · the board had 18:00'],
  ['o/c', 'OUT', 'Seacon Monaco', 'CJ-9 · 69–76¾ → OTB', 'Deepak', '11-21 11:45', '"o/c" in red over the hour — after Flag Marina is in · programme 21.11: 15:00 · est'],
  ['10:30', 'OUT', 'Ken Ann', 'CJ-5 · 33½–41½ → OTB', 'Yadav + Neeraj', '11-21 10:30', 'RT OUT · programme 21.11: 16:00'],
  ['o/c', 'IN', 'Yuan Hang Wei Ye', 'OTB → CJ-9 · 69–77¼', 'Yadav', '11-21 13:30', 'behind Seacon Monaco — est · programme 21.11: about 17:00'],
  ['09:00', 'IN', 'TCI Express', 'OTB → CJ-11 · 87–95', 'Sachin', '11-21 11:00', 'FLOOD · container — list 21.11 and programme 21.11 print TCI ANAND for this berth (her ETA is now 22 Nov 06:00); the HM brings TCI Express, arrived 06:17 · est'],
  ['—', '—', 'PMS / stand-by duty', 'Capt Sachin 11:30–12:30 · Capt Yadav from 13:30 (the last words are not clear on the photo)', '—', '11-21 11:30', '']]]
MV2 = ['List 21.11 (0700) — actual hours of 20 Nov and the night', [
  ['13:50', 'IN', 'Ken Ann', 'OTB → CJ-5 · 33½–41½', '—', '11-20 13:50', 'made fast · commenced 15:40 (board est 12:30)'],
  ['17:50', 'IN', 'Safi Alfa', 'OTB → CJ-4 · 23–31¼', '—', '11-20 17:50', 'made fast · commenced 20:00 (board est 19:30) · norm 3,450 · ETC 28 Nov 00:00'],
  ['18:50', 'IN', 'Flexi 2', 'OTB → CJ-12 · 100–109½', '—', '11-20 18:50', 'made fast · commenced 20:59 · container'],
  ['22:50', 'IN', 'Parvraj', 'OTB → CJ-6 · 42–51¼', '—', '11-20 22:50', 'made fast · commenced 01:05 on the 21st (board est 21:30) · norm 14,950 · ETC 24 Nov 08:17'],
  ['02:00', 'IN', 'Uni Blossom', 'OTB → CJ-13 · 113–124¾', '—', '11-21 02:00', 'made fast · commenced 03:45 (board est 02:30) · norm 4,600 · ETC 28 Nov 17:58'],
  ['—', 'OUT', 'Rome Trader · Meghna Prestige · Truong Minh Dream', 'no longer on the at-berth sheet', '—', '11-21 07:00', 'sailed before 0700 — the let-go hours come with DPR 21.11']]]
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
def berth(bid, fn):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]
    tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln
    d = dict(split_top(core[3:-1]))
    if set(d) - {'b', 'prev', 'now', 'out', 'outBy', 'next'}: B.die('berth extra keys: ' + bid)
    d = fn(d)
    B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in ('b', 'prev', 'now', 'out', 'outBy', 'next') if k in d) + '}' + tail + B.s[b:]
NOWKEYS = ('n', 'c', 'q', 'u', 'ie', 'loa', 'f', 'est', 'nm', 'rank', 'ag', 'etc', 'note')
def rotate(name, f, nm, etc, add, q_=None):
    """the vessel that was 'next' is alongside: prev <- now (with its out / outBy), now <- next with the list's actual hours."""
    def fn(d):
        now = obj(d['now']); nx = obj(d['next'])
        assert name in nx['n'], (name, nx['n'])
        prev = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}
        prev['out'] = d['out']; prev['outBy'] = d['outBy']
        nx.pop('est', None); nx['f'] = js(f)
        if nm is not None: nx['nm'] = js(nm)
        if etc is not None: nx['etc'] = js(etc)
        if q_ is not None: nx['q'] = repr(q_)
        nx['note'] = "'" + q(add + " · ") + nx['note'][1:]
        d2 = {'b': d['b'], 'prev': unobj(prev, ('n', 'c', 'q', 'u', 'ie', 'ag', 'out', 'outBy')), 'now': unobj(nx, NOWKEYS)}
        return d2
    return fn
berth('OJ-2', rotate('Hatnyanawati', '11-20 21:20', '360', '11-22 05:06', LT + ': OJ-2 · MADE FAST 20 NOV 21:20, commenced 23:40 · chemicals 10,000 MT EXP · norm 360 MT/h · ETC 22 NOV 05:06 (board est 21:00)'))
berth('OJ-3', rotate('SG Friendship', '11-20 21:06', '360', '11-21 23:48', LT + ': OJ-3 · MADE FAST 20 NOV 21:06, commenced 23:24 · chemicals 8,172.93 MT IMP · norm 360 MT/h · ETC 21 NOV 23:48 (board est 19:30 — an hour and a half early)'))
berth('OJ-4', rotate('Eva Richway', '11-20 23:00', '360', '11-22 02:57', LT + ': OJ-4 · MADE FAST 20 NOV 23:00, commenced 01:24 on the 21st · chemicals 8,627.19 MT IMP · norm 360 MT/h · ETC 22 NOV 02:57 (board est 23:00)'))
berth('OJ-6', rotate('Orchids', '11-20 19:48', None, None, LT + ': OJ-6 · VLSFO 8,000 MT IMP · made fast printed "21 Nov 19:48" — a slip for 20 Nov 19:48 (it is after the 0700 position; the board had about 19:30) · commenced 21 Nov 06:18 · no norm or ETC'))
def oj7(d):
    now = obj(d['now']); assert 'Silver Gertrude' in now['n']
    now.pop('est', None); now['f'] = js('11-20 10:12'); now['nm'] = js('650'); now['etc'] = js('11-22 02:48')
    now['note'] = "'" + q(LT + ': OJ-7 · MADE FAST 20 NOV 10:12, commenced 13:30 · CDSBO 22,500 MT · norm 650 MT/h · ETC 22 NOV 02:48 (the board had about 05:00 — she was "under berthing" on DPR 20.11) · ') + now['note'][1:]
    d['now'] = unobj(now, NOWKEYS); return d
berth('OJ-7', oj7)
def oj1(d):
    now = obj(d['now']); assert 'Artigo' in now['n']
    now['note'] = "'" + q(LT + ': OJ-1 · norm 450 MT/h · ETC 22 NOV 07:26 — unchanged · ') + now['note'][1:]
    d['now'] = unobj(now, NOWKEYS); return d
berth('OJ-1', oj1)
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
wait = [r.rstrip(',') for r in B.s[w0 + len(" wait:[\n"):e0].split('\n')]
eta = [r.rstrip(',') for r in B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n')]
def nm_(r): return re.match(r"  \{n:'((?:[^'\\]|\\.)*)'", r).group(1)
def setf(r, key, val):
    rx = re.compile(r"\b" + key + r":(?:'(?:[^'\\]|\\.)*'|null)"); assert len(rx.findall(r)) == 1, (key, r[:80]); return rx.sub(lambda _: key + ":" + ("'" + q(val) + "'" if val is not None else 'null'), r)
def remp(r, text):
    i = r.index("rem:'") + 5; return r[:i] + q(text) + (" · " if r[i] != "'" else "") + r[i:]
TG = 'LIST 21.11: '
WCH = {
 'Hartati': lambda r: remp(setf(r, 'rank', '1C'), TG + 'rank "1C" — first of the chemical line now'),
 'Bow Fortitude': lambda r: remp(setf(r, 'rank', '2C'), TG + 'rank "2C"'),
 'PVT Aurora': lambda r: remp(setf(r, 'rank', '3C'), TG + 'rank "3C"'),
 'Al Mahboobah': lambda r: remp(setf(r, 'rank', '4C'), TG + 'rank "4C"'),
}
seen = set(); W2 = []
for r in wait:
    n = nm_(r)
    if n == 'SG Friendship': seen.add(n); continue
    if n in WCH: r = WCH[n](r); seen.add(n)
    W2.append(r)
assert seen == set(WCH) | {'SG Friendship'}, (set(WCH) | {'SG Friendship'}) - seen
for d in (
 {'n': 'Chemroute Pegasus', 'c': 'Chemicals', 'q': 8708.7, 'u': 'MT', 'ie': 'IMP', 'loa': 159.03, 'dr': 8.5, 'rep': '11-20 20:30', 'rdy': '11-20 20:30', 'rank': '5C', 'ag': 'Atlantic Shg', 'rem': TG + 'ARRIVED — reported / ready 20 Nov 20:30 · rank "5C" · REQ OJ 2, 3, 4 · 8.5 m', 'st': ''},
 {'n': 'Chemroad Nexus', 'c': 'Chemicals', 'q': 10949.31, 'u': 'MT', 'ie': 'IMP', 'loa': 183, 'dr': 8.99, 'rep': '11-20 22:30', 'rdy': '11-20 22:30', 'rank': '6C', 'ag': 'Atlantic Shg', 'rem': TG + 'ARRIVED — reported / ready 20 Nov 22:30 · rank "6C" · REQ OJ 2, 3, 4 · 8.99 m', 'st': ''},
 {'n': 'Thetis Leona', 'c': 'Chemicals', 'q': 5000, 'u': 'MT', 'ie': 'IMP', 'loa': 146.5, 'dr': 10, 'rep': '11-21 04:40', 'rdy': '11-21 04:40', 'rank': '7C', 'ag': 'Wilhelmsen', 'rem': TG + 'ARRIVED — reported / ready 21 Nov 04:40 · rank "7C" · REQ OJ 2, 3, 4 · 10 m', 'st': ''}):
    W2.append("  " + js(d))
E2 = [r for r in eta if nm_(r) not in ('Thetis Leona', 'Chemroute Pegasus', 'Chemroad Nexus')]
assert len(E2) == len(eta) - 3
E2.append("  " + js({'n': 'Southern Anoa', 'c': 'CPO', 'q': 17998.97, 'u': 'MT', 'ie': 'IMP', 'loa': 145.53, 'dr': 9.6, 'eta': '11-25 00:00', 'rdy': None, 'ag': 'Interocean', 'rem': 'new on list 21.11'}))
E2.sort(key=lambda r: re.search(r"eta:'([^']*)'", r).group(1))
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(W2) + "\n ],\n eta:[\n" + ",\n".join(E2) + B.s[m0:]
LMN = ['List 21.11 (0700) — actual hours at the oil jetties, 20 Nov and the night (no oil-jetty row on the signal sheet of 21 Nov, disp 07:46)', [
  ['10:12', 'IN', 'Silver Gertrude', 'OTB → OJ-7', '—', '11-20 10:12', 'made fast · commenced 13:30 (the board had about 05:00) · ETC 22 Nov 02:48'],
  ['19:48', 'IN', 'Orchids', 'OTB → OJ-6', '—', '11-20 19:48', 'made fast — the list prints "21 Nov 19:48", a slip · commenced 21 Nov 06:18 (board est 19:30)'],
  ['21:06', 'IN', 'SG Friendship', 'OTB → OJ-3', '—', '11-20 21:06', 'made fast · commenced 23:24 (board est 19:30) · ETC 21 Nov 23:48'],
  ['21:20', 'IN', 'Hatnyanawati', 'OTB → OJ-2', '—', '11-20 21:20', 'made fast · commenced 23:40 (board est 21:00) · ETC 22 Nov 05:06'],
  ['23:00', 'IN', 'Eva Richway', 'OTB → OJ-4', '—', '11-20 23:00', 'made fast · commenced 01:24 on the 21st (board est 23:00) · ETC 22 Nov 02:57']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LMN) + ",\n" + B.s[mm:]
B.rep("const LIQ={src:'DPA berthing list 20.11.26 (revised after the meeting) · DPR 20.11 · programme 21.11 (TF/SH/2102) · signals to the amended sheets of 20 Nov, both pages (disp 1400)',asOf:'11-20 20:26',",
      "const LIQ={src:'DPA berthing list 21.11.26 (0700) · DPR 20.11 · programme 21.11 (TF/SH/2102) · signals to the day sheet of 21 Nov (disp 0746 — no oil-jetty row on it)',asOf:'11-21 10:21',")

# ================= TUNA =================
B.rep("ie:'EXP',loa:183,f:'11-20 22:30',est:1,ag:'Taurus',prev:'vacant on every list since 10 Nov',next:'nobody named',note:'PROGRAMME 21.11: TT-02, NIGHT BERTHING.",
      "ie:'EXP',loa:183,f:'11-20 23:35',ag:'Taurus',prev:'vacant on every list since 10 Nov',next:'nobody named',note:'" + q(LT + ": TT-2 · MADE FAST 20 NOV 23:35, COMMENCED 21 Nov 06:30 (board est 22:30) · rapeseed meal 31,500 MT EXP · no norm or ETC. ") + "PROGRAMME 21.11: TT-02, NIGHT BERTHING.")
B.rep("next:'Blue Ionian (ready 3 Nov, TT-01) waits behind',note:'", "next:'Blue Ionian (ready 3 Nov, TT-01) waits behind',note:'" + q(LT + ": TT-1 · \"(GL)\" · still alongside at 0700 on 21 Nov — no norm or ETC printed. "))
B.rep("const TUNA={src:'DPA berthing list 20.11.26 (revised after the meeting) · DPR 20.11 · programme 21.11 (TT-02: Woohyun Dream in, night berthing) · TT-4 vacant'",
      "const TUNA={src:'DPA berthing list 21.11.26 (0700) · DPR 20.11 · programme 21.11 · TT-2 Woohyun Dream made fast 20 Nov 23:35 · TT-4 vacant'")
B.rep(" {d:'11-20',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Marvelous Star','TT-4':''}}\n];",
      " {d:'11-20',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Marvelous Star','TT-4':''}},\n {d:'11-21',b:{'TT-1':'Europa Graeca','TT-2':'Woohyun Dream','TT-3':'Marvelous Star','TT-4':''}}\n];")

# ================= TIMBER =================
B.rep("asOf:'11-20 12:00',etaFromDesk:true,waiting:43,", "asOf:'11-20 12:00',etaFromDesk:false,waiting:43,")
B.rep("{n:'Uni Blossom',cbm:34870,from:'Uruguay',c:'Pine logs',eta:'11-09 11:36',etb:'11-20',note:'",
      "{n:'Uni Blossom',cbm:34870,from:'Uruguay',c:'Pine logs',eta:'11-09 11:36',etb:'11-20',comm:'11-21 03:45',note:'" + q(LT + ": berthed 21 Nov 02:00 at CJ-13 under SAAGAR, COMMENCED 03:45 · norm 4,600 CBM · ETC 28 Nov 17:58 (the list counts 34,880 CBM) · "))
B.rep("{n:'AG Varvara',cbm:39113,from:'Australia',c:'Pine logs',eta:'11-12 07:06',etb:'11-26',note:'", "{n:'AG Varvara',cbm:39113,from:'Australia',c:'Pine logs',eta:'11-12 07:06',etb:'11-26',note:'" + q(LT + ": SGR 1 · GEN 16 — the senior vessel of the SAAGAR line · "))
B.rep("{n:'CD Glory',cbm:29158,from:'Malaysia',c:'Hardwood logs',eta:'11-15 06:42',etb:'11-26',note:'", "{n:'CD Glory',cbm:29158,from:'Malaysia',c:'Hardwood logs',eta:'11-15 06:42',etb:'11-26',note:'" + q(LT + ": SGR 3 · 8K 8 · GEN 20 · "))
B.rep("{n:'Dariya Priya',cbm:44968,from:'New Zealand',c:'Pine logs',eta:'11-16 09:00',etb:'11-30',note:'", "{n:'Dariya Priya',cbm:44968,from:'New Zealand',c:'Pine logs',eta:'11-16 09:00',etb:'11-30',note:'" + q(LT + ": \"WORKING AT MS\" — commenced at midstream 20 Nov 11:40 · SGR 4 · 8K 9 · GEN 21 · "))
B.rep("{n:'African Tiger',cbm:36328,from:'Uruguay',c:'Pine logs',eta:'11-18 06:30',etb:'12-03',note:'", "{n:'African Tiger',cbm:36328,from:'Uruguay',c:'Pine logs',eta:'11-18 06:30',etb:'12-03',note:'" + q(LT + ": SGR 5 · 8K 10 · GEN 25 · "))
B.rep("{n:'Paiwan Ace',cbm:null,from:'Uruguay',c:'Pine logs',eta:'11-22 01:00',etb:'12-08',note:'",
      "{n:'Paiwan Ace',cbm:36905,from:'Uruguay',c:'Pine logs',eta:'11-22 01:00',etb:'12-08',note:'" + q("MIHIR & COMPANY · " + LT + " prints her \"PAIWAN ICE\" on the expected sheet — pine logs 36,904.588 (unit printed MT) · ETA 22 Nov 00:00 · N/A · agent MIHIR · 182.93 m, 11.0 m. The CBM here is the list's figure — the desk sheet has not given one · "))
B.save()
