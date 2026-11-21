#!/usr/bin/env python3
# apply46 — v204: PROGRAMME 22.11 (TF/SH/2102, 21 Nov), LIST 21.11 revised after the meeting, HM signal 21 Nov AMENDED (disp 0746 / 0840 / 1257), timber desk sheet 21 Nov 1200. Received 21 Nov 14:46.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 21.11 (revised)'); q = B.q
P = 'PROGRAMME 22.11'; SG = 'HM SIGNAL 21 Nov amended (disp 12:57)'; LT = 'LIST 21.11 (revised after the meeting)'
def pre(m, t): B.note_prefix(m, q(t) + " ")
def sub(m, o, n): B.sub_entry(m, o, n)
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]
# ---- header
B.rep("const NOW=h('11-21 11:22');", "const NOW=h('11-21 14:46');")
setline("const PROG_END=h('11-21 18:00');", "const PROG_END=h('11-22 18:00'); // programme 22.11 (meeting of 21 Nov) covers till here — barge windows end here;")
B.rep("List <b>21.11 · 0700</b> · DPR <b>21.11</b> · Programme <b>21.11</b> · Signals to <b>21 Nov day sheet (disp 0746)</b>", "List <b>21.11 · revised after the meeting</b> · DPR <b>21.11</b> · Programme <b>22.11</b> · Signals to <b>21 Nov amended sheet (disp 0746 / 0840 / 1257)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>", "<summary>Sources, rules &amp; tide</summary><div>Received 21 Nov 14:46: PROGRAMME 22.11 (Crystal O into CJ-1 under 6.5K; tug Sagar 5 with barge and Sanghi Sundarshan into CJ-14 behind Nord Copper; Sand Topic into CJ-9), the LIST of 21.11 revised after the meeting (Belmoira at CJ-15A under 24 hrs as a 30K quote; 6.5K / 8K ranks renumbered with Crystal O first), the HM signal of 21 Nov amended at 12:57 (Heng Yuan Fa Zhan out 18:45, Belmoira in behind her) and the timber desk sheet of 21 Nov 12:00 · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 22.11 · list 21.11 revised · HM signal 21 Nov amended (disp 1257) · ")
B.rep("const PROG_SAIL=new Set(['Ken Ann',", "const PROG_SAIL=new Set(['New Bliss','Nord Copper','Heng Yuan Fa Zhan','Yuan Hang Wei Ye (next call)','Ken Ann',")
# ---- V: sailings
M = "{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]"
pre(M, SG + ": RT OUT 18:45 · Capt Deepak · 161¾–169 → OTB. " + LT + ": \"[15A]\" — sailing today; Belmoira follows.")
sub(M, "f:'11-19 22:06',t:'11-21 21:30',est:1", "f:'11-19 22:06',t:'11-21 18:45'")
M = "{b:'9',n:'Yuan Hang Wei Ye (next call)',p:[69,77.25]"
pre(M, P + ": OUT readiness 22 Nov 17:45, 12.5 m → MV SAND TOPIC in — a stay of about 28 hours for 50,455 MT (the board had assumed 20,000 a day, to 24 Nov).")
sub(M, "f:'11-21 13:30',t:'11-24 02:00',est:1", "f:'11-21 13:30',t:'11-22 17:45',est:1")
M = "{b:'14',n:'Nord Copper',nm:23000,p:[126.5,141.75]"
pre(M, P + ": OUT readiness 22 Nov 11:00, 11.3 m → tug Sagar 5 with barge Victoria 250 (126½–133, CSTL) and Sanghi Sudharshan (\"CJ-14A\", 135–141¾, space a/c) take her place.")
sub(M, "f:'11-20 02:06',t:'11-22 03:03',", "f:'11-20 02:06',t:'11-22 11:00',lt:'11-22 03:03',")
pre("{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]", P + ": OUT readiness 22 Nov 10:05, 10.4 m → MV CRYSTAL O in, 7½–N, category 6.5K, starboard.")
# ---- V: new berth entries
a, b = B.line_of(" {b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]")
NEWV = [
 " {b:'15A',n:'Belmoira',nm:30000,p:[160.5,171.75],c:'Salt in bulk',q:58300,u:'MT',cat:'24H',via:'30k/25k quote (Sr No 7)',f:'11-21 20:45',t:'11-23 19:25',est:1,note:'" + q(SG + ": IN \"o/c\" · Capt Deepak, after Heng Yuan Fa Zhan's 18:45 · OTB → 160½–171¾ — about 20:45 alongside, est. " + LT + ": printed AT BERTH under 24 HRS · CJ-15A · \"24HRS(30K)\" · salt in bulk 58,300 MT EXP · norm 30,000 — at the norm about 23 Nov 19:25. She had been starred X / \"B'TODAY\" since 19 Nov; the board's v197 had her here, v198 had moved her to CJ-14.") + "'},",
 " {b:'1',n:'Crystal O',nm:6500,p:[0,7.5],c:'Sugar bags',q:14321,u:'MT',cat:'8K',f:'11-22 12:05',t:'11-24 15:00',est:1,note:'" + q(P + ": CJ-01 · IN behind New Bliss (out 22 Nov 10:05) · 7½–N · CATEGORY 6.5K · starboard. " + LT + ": she is now 8K 1 (no 8K rank was printed for her on the morning list) · GEN 3 · sugar bags 31,200 MT · reported 16 Oct · working at midstream — DPR 21.11: 16,879 loaded, 14,321 left (shown here). At the 6,500 norm about 24 Nov 15:00, est.") + "'},",
 " {b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133],c:'Coated steel pipes',q:3804.5,u:'MT',cat:'COASTAL',f:'11-22 13:00',t:'11-23 21:00',est:1,note:'" + q(P + ": CJ-14 · IN behind Nord Copper (out 22 Nov 11:00) · 126½–133 · CSTL. " + LT + ": CSTL 1 · remark \"13-16, 1 CRANE\" · ready 21 Nov 11:00. The board had put her at the empty CJ-3. Stay about a day and a half, est.") + "'},",
 " {b:'14',n:'Sanghi Sundarshan',p:[135,141.75],c:'Steel coil',q:4004,u:'MT',cat:'SPACE',f:'11-22 13:15',t:'11-23 13:15',est:1,note:'" + q(P + ": \"CJ-14A\" · MV SANGHI SUDHARSHAN · 135–141¾ · SPACE A/C — beside the tug-and-barge in Nord Copper's berth. " + LT + ": readiness 21 Nov 11:00 · \"SPACE A/C, BB, CJ-13 TO 16\" · steel coil 4,004 MT IMP · 93 m. Stay about a day, est.") + "'},",
 " {b:'9',n:'Sand Topic',p:[69,77.75],c:'Petcoke',q:51292,u:'MT',cat:'PPP',f:'11-22 19:45',t:'11-25 09:00',est:1,note:'" + q(P + ": CJ-09 · IN behind Yuan Hang Wei Ye (out 22 Nov 17:45) · 69–77¾ · GFPL · ETA 22 Nov 03:00 · arrival draught 12.0 m · port side. " + LT + ": petcoke 51,291.7 MT IMP · readiness 22 Nov 03:00 · \"CJ-09\". No norm — about 20,000 a day assumed.") + "'},",
]
B.s = B.s[:a] + "\n".join(NEWV) + "\n" + B.s[a:]
B.rep("Object.assign(LOA,{'Safi Alfa':189.99,'Flag Marina':254.62,'Parvraj':189.9});", "Object.assign(LOA,{'Safi Alfa':189.99,'Flag Marina':254.62,'Parvraj':189.9,'Belmoira':199.92,'Crystal O':171.59,'Sand Topic':199.9,'Sanghi Sundarshan':93,'Tug Sagar 5 + barge Victoria 250':75});")
for n in ('Belmoira', 'Crystal O', 'Tug Sagar 5 + barge Victoria 250', 'Sanghi Sundarshan', 'Sand Topic'): B.wdel(n)
# ---- W: revised list
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Manta Sena', "8K 2 (was 1) · GEN 4 — Crystal O is now printed 8K 1 and takes CJ-1 on programme 22.11; Manta Sena is the senior of the line once she is alongside", rk="'8K':2,GEN:4")
w('Crystal Land', "8K 3 · GEN 5", rk="'8K':3,GEN:5")
w('Pioneer Fortune', "8K 4 · GEN 8 · Sr No 7", rk="'8K':4,GEN:8")
w('Tan Bin 259', "8K 5 · GEN 14 · PROGRAMME 22.11: out of MRG 3, readiness 22 Nov 15:00", rk="'8K':5,GEN:14")
w('Gokova-M', "HP 1 · 24H 1 · 8K 6 · GEN 15 · remark adds \"50500MT-TOTAL- WHARFAGE PENDING\"", rk="HP:1,'24H':1,'8K':6,GEN:15")
w('Porto Fiscardo', "8K 7 · GEN 18", rk="'8K':7,GEN:18")
w('Captainannis L', "8K 8 · GEN 19", rk="'8K':8,GEN:19")
w('CD Glory', "SGR 3 · 8K 9 (was 8 — Crystal O is put in at the head of the 6.5K / 8K line) · GEN 20 · Sr No 7", rk="SAAGAR:3,'8K':9,GEN:20")
w('Dariya Priya', "SGR 4 · 8K 10 · GEN 21", rk="SAAGAR:4,'8K':10,GEN:21")
w('African Tiger', "SGR 5 · 8K 11 · GEN 25", rk="SAAGAR:5,'8K':11,GEN:25")
w('Ocean Kudos', "HP 3 · 8K 12 · GEN Y — still printed with ranks; held on Mihir's word of 20 Nov", rk="HP:3,'8K':12,GEN:98")
w('Zheng Hui', "ARRIVED — reported / ready 21 Nov 08:12 (ETA sheet, first row after KM Jakarta) · GEN Y", rdy="11-21 08:12")
w('Tai Keystone', "ETA / READINESS now 22 Nov 00:00 (was 21 Nov 00:00) — a day later", rdy="11-22 00:00")
w('Asian Summit', "ETA 22 Nov 10:00 · readiness 22 Nov 08:00 · HP Y · GEN Y · \"30K/25K/10K SR NO.07\" · 13.3 m", rk="HP:98,GEN:98", rdy="11-22 10:00", dr="13.3")
w('Hai Nam 81', "ETA / readiness 22 Nov 15:00 (was 16:00)", rdy="11-22 15:00")
w('Paiwan Ace', "ETA 22 Nov 02:00 (still printed \"PAIWAN ICE\") · the timber desk sheet of 21 Nov gives MV PAIWAN ACE 36,905 CBM, ETA 22 Nov 01:00 — the same vessel")
m = B._row('MSC Magali').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEWW = [
 " ['KM Jakarta','Salt in bulk',55000,'MT',199.98,6.5,null,{HP:98,'8K':98},'" + q(LT + " (ETA sheet): NEW · ETA 21 Nov 00:00 · N/A · HP Y · 8K Y · \"30K/25K/10K SR.NO 07\" · DD 13.00 m · salt in bulk 55,000 MT EXP · agent True Blue") + "'],",
 " ['Erna Oldendorff','Pine logs',34424,'CBM',179.99,10.34,'11-23 00:00',{SAAGAR:98},'" + q(LT + " (ETA sheet): NEW — \"MV ERNA OLDENDROFF\" · Australian pine logs 34,424.173 CBM IMP · ETA / readiness 23 Nov 00:00 · SGR Y · Sr No 7 · agent DBC. Timber desk 21 Nov: ETA 23 Nov 12:00, ETB 8 Dec") + "'],",
 " ['African Pheasant','Pine logs',45282,'CBM',199.98,null,null,{SAAGAR:98,'8K':98},'" + q(LT + " (ETA sheet): NEW · pine logs 45,282 CBM IMP · ETA 24 Nov · N/A · SGR Y · 8K Y · Sr No 7 · agent Synergy. Timber desk 21 Nov: ETA 23 Nov 23:30, ETB 13 Dec") + "'],",
]
B.s = B.s[:e] + "\n".join(NEWW) + "\n" + B.s[e:]
a, b = B.line_of("Object.assign(AG,{'Star New London':")
B.s = B.s[:b] + "\nObject.assign(AG,{'KM Jakarta':'True Blue','Erna Oldendorff':'DBC','African Pheasant':'Synergy'});Object.assign(IE,{'KM Jakarta':'EXP','Erna Oldendorff':'IMP','African Pheasant':'IMP','Crystal O':'EXP','Sand Topic':'IMP','Sanghi Sundarshan':'IMP'}); // list 21.11 revised" + B.s[b:]
setline("const ETA={'Tai Keystone':", "const ETA={'KM Jakarta':'11-21 00:00','Tai Keystone':'11-22 00:00','Paiwan Ace':'11-22 02:00','Asian Summit':'11-22 10:00','Zheng Run':'11-22 12:00','Hai Nam 81':'11-22 15:00','V Pacific':'11-23 00:00','Hai Long 1':'11-23 00:00','Lolo Gate':'11-23 00:00','Outlander':'11-23 00:00','Erna Oldendorff':'11-23 00:00',"
        "'KSS Edmond':'11-24 00:00','Kang Qi Fu Hua':'11-24 00:00','Kerem':'11-24 00:00','Meghna Prestige (salt, next call)':'11-24 00:00','African Pheasant':'11-24 00:00','Princess Manissa':'11-25 00:00','Valentina Sea':'11-26 00:00','Gutian Trust':'11-30 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 21.11 revised after the meeting")
B.rep("Object.assign(REP,{'Manta Omer Mecit':'11-20 17:30',", "Object.assign(REP,{'Zheng Hui':'11-21 08:12','Manta Omer Mecit':'11-20 17:30',")
# CD Glory options — 8K rank
B.rep("{label:'6.5K / 8K',only:'8K',rk:{'8K':8},note:'", "{label:'6.5K / 8K',only:'8K',rk:{'8K':9},note:'" + q("Revised list 21.11: she is 8K 9 — Crystal O was put in at the head of the line and took CJ-1. ") )
# ---- MV: the amended sheet (today's rows)
def js(o):
    if isinstance(o, str): return "'" + q(o) + "'"
    return '[' + ','.join(js(x) for x in o) + ']'
MVN = ['HM signal 21 Nov — AMENDED (dispatched 07:46 / 08:40 / 12:57) · Capt Pathak · received 21 Nov 14:46', [
 ['10:15', 'SHIFT', 'Vishva Bandhan', 'CJ-8 · 59½–68 → CJ-5 · 33¼–41½', 'Nanda (was Pathak)', '11-21 10:15', 'pilot changed in red · "PORT C."'],
 ['09:00', 'IN', 'Flag Marina', 'OTB → CJ-7 / CJ-8 · 56¾–67¼', 'Deepak + Neeraj', '11-21 11:15', 'unchanged'],
 ['o/c', 'OUT', 'Seacon Monaco', 'CJ-9 · 69–76¾ → OTB', 'Nanda', '11-21 11:45', 'pilot changed in red'],
 ['10:30', 'OUT', 'Ken Ann', 'CJ-5 · 33½–41½ → OTB', 'Yadav + Ashish', '11-21 10:30', 'RT OUT'],
 ['o/c', 'IN', 'Yuan Hang Wei Ye', 'OTB → CJ-9 · 69–77¼', 'Yadav', '11-21 13:30', 'unchanged'],
 ['09:00', 'IN', 'TCI Express', 'OTB → CJ-11 · 87–95', 'Sachin', '11-21 11:00', 'FLOOD · container'],
 ['18:45', 'OUT', 'Heng Yuan Fa Zhan', 'CJ-15A · 161¾–169 → OTB', 'Deepak', '11-21 18:45', 'NEW ROW · RT OUT'],
 ['o/c', 'IN', 'Belmoira', 'OTB → CJ-15A · 160½–171¾', 'Deepak', '11-21 20:45', 'NEW ROW · behind Heng Yuan Fa Zhan — est']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
# ---- meeting of 21 Nov: scored on the call frozen before the meeting
ML = "{d:'11-21',at:'11-21 10:21',basis:'list 21.11 · HM signal 21 Nov (disp 07:46) · DPR 20.11',prog:'22.11',call:[['Blue Shark','15A'],['Manta Sena','1'],['Xin Hai Tong 71','14']],got:[['Crystal O','1'],['Sand Topic','9'],['Sanghi Sundarshan','14'],['Belmoira','15A','signal']],note:'" + q("None of the three. CJ-1 went to Crystal O under 6.5K — the revised list prints her 8K 1, a rank the morning list did not carry; Manta Sena is now 8K 2. CJ-15A went to Belmoira under 24 hrs as a 30K quote (amended signal, in tonight) — she had been starred \"B'TODAY\" for three days and the board's v197 had her there; v198 moved her and gave the berth to Blue Shark by General. CJ-14 went to the tug-and-barge (CSTL) and Sanghi Sundarshan (space a/c) side by side — not to Xin Hai Tong 71. Sand Topic is the GFPL berth's own vessel.") + "'},"
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")
setline("const CALL_FROZEN=", "const CALL_FROZEN=null; // {d,at,basis,call} = the meeting call as it stood BEFORE the meeting, when papers written after it reach the board before the programme; null = show the live call")
# ---- TUNA / LIQ: programme 22.11 in one line each
B.rep("rem:'TT-01 · ready 3 Nov 11:00 — behind Europa Graeca (about 22 Nov 02:00 at the DPR 21.11 pace)'", "rem:'PROGRAMME 22.11: TT-01 — IN behind Europa Graeca (out readiness 22 Nov 09:30, 7.3 m) · ready 3 Nov 11:00'")
B.rep("const LIQ={src:'", "const LIQ={prog:'PROGRAMME 22.11 — OJ-1 Artigo out 22 Nov 07:20 → Hafnia Ammolite · OJ-2 Hatnyanawati out 05:00 → PVT Aurora (night) · OJ-3 SG Friendship shifts to OTB 21 Nov 23:48, agent\\'s request → Hartati (night) · OJ-4 Eva Richway out 02:30 → Bow Fortitude (night) · OJ-7 Silver Gertrude out 02:48 → Ginga Cheetah (night). Revised list: Hatnyanawati norm 250 MT/h, ETC 22 Nov 17:20.',src:'")
# ---- TIMBER desk sheet 21 Nov 1200
B.rep("d:'20 Nov 1200',upto:'21 Nov 1800, after the berthing meeting of 20 Nov',", "d:'21 Nov 1200',upto:'22 Nov 1800, after the berthing meeting of 21 Nov',")
B.rep("asOf:'11-20 12:00',etaFromDesk:false,waiting:43,", "asOf:'11-21 12:00',etaFromDesk:false,waiting:44,")
B.rep("{n:'Erna Oldendorff',cbm:null,from:'Australia',c:'Pine logs',eta:'11-23 20:00',etb:'12-08',note:'", "{n:'Erna Oldendorff',cbm:34424,from:'Australia',c:'Pine logs',eta:'11-23 12:00',etb:'12-08',note:'" + q("desk 21 Nov: ETA 23 Nov 12:00 (20:00 before), CBM not given — 34,424 is the DPA list figure (revised list 21.11: SGR Y, readiness 23 Nov 00:00, agent DBC) · "))
B.rep("{n:'African Pheasant',cbm:null,from:'New Zealand',c:'Logs',eta:'11-23 16:30',etb:'12-13',note:'", "{n:'African Pheasant',cbm:45282,from:'New Zealand',c:'Pine logs',eta:'11-23 23:30',etb:'12-13',note:'" + q("desk 21 Nov: ETA 23 Nov 23:30 (16:30 before), CBM not given — 45,282 is the DPA list figure (revised list 21.11: ETA 24 Nov, SGR Y · 8K Y, agent Synergy)"))
B.rep("etb:'11-20',comm:'11-21 03:45',note:'", "etb:'11-20',comm:'11-21 03:45',note:'" + q("desk 21 Nov: berthed 21 Nov 02:05 under SAAGAR (the list and the DPR say 02:00) · "))
a = B.s.index("{n:'Paiwan Ace',cbm:36905,"); i = B.s.index("note:'", a) + 6
B.s = B.s[:i] + q("DESK 21 Nov: MV PAIWAN ACE — 36,905 CBM, Uruguay, ETA 22 Nov 01:00, ETB 8 Dec: the desk now gives the same figure the list prints for \"PAIWAN ICE\" — one vessel, confirmed · ") + B.s[i:]
B.rep('OPEN (2): "PAIWAN ICE" on the expected sheet', '(2) ANSWERED by the timber desk sheet of 21 Nov 12:00 — MV PAIWAN ACE, 36,905 CBM: the same vessel. Was: "PAIWAN ICE" on the expected sheet')
B.save()
# (engine) gapAt(): a free gap is clipped to the berth's own quay — see the python block in tools/examples notes; applied by hand after this script.
