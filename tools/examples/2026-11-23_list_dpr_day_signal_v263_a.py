#!/usr/bin/env python3
# apply60a — v263 (part 1, data): three papers received 23 Nov 11:06, no text —
#   DAILY BERTHING LIST 23.11.2026 (0700) · DAILY PERFORMANCE REPORT 23.11.2026 (0700, xlsx) · HM signal 23 Nov DAY sheet (disp 08:15, Capt Omesh).
# The big change: CJ-14 goes to LILA TOKYO ("CSTL(30K) B'TODAY", signal IN 10:45), not to Hai Nam 81 as programme 23.11 had it (provisional);
# Hai Nam 81 is back on the waiting sheet. ML Egret warped 09:30 to make room. No list had come for 22.11.
# The meeting call of 23 Nov is FROZEN as v262 published it at 02:16 (the papers reached the board after the 11:00 meeting hour).
import re, sys, subprocess
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 23.11'); q = B.q
L = 'LIST 23.11'; D = 'DPR 23.11'; SG = 'HM SIGNAL 23 Nov day sheet (disp 08:15)'
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
B.rep("const NOW=h('11-23 02:16');", "const NOW=h('11-23 11:06');")
B.rep("<i>List</i><b>21.11 · revised after the meeting</b>", "<i>List</i><b>23.11 · 0700</b>")
B.rep("<i>DPR</i><b>22.11</b>", "<i>DPR</i><b>23.11</b>")
B.rep("<i>Signals to</i><b>22 Nov night sheet (disp 2130 / 2155)</b>", "<i>Signals to</i><b>23 Nov day sheet (disp 0815)</b>")
n0 = len(B.s)
B.s, k = re.subn(r"<b>Papers on the board:</b>.*?berthing-policy circular 5237 of 21\.11\.2026\.",
    "<b>Papers on the board:</b> berthing list 23.11 (position 07:00; no list came for 22.11) · programme 23.11 · DPR 23.11 (position 07:00) · HM signal sheets to the day sheet of 23 Nov (disp 08:15) · timber desk sheet 21 Nov 12:00 · berthing-policy circular 5237 of 21.11.2026.", B.s, count=1, flags=re.S)
assert k == 1 and abs(len(B.s) - n0) < 600
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 23 Nov day sheet (disp 0815) · list 23.11 (0700) · DPR 23.11 (0700) · ")
B.rep("const CALL_FROZEN=null;", "const CALL_FROZEN={d:'11-23',at:'11-23 02:16',basis:'list 21.11 (revised) · programme 23.11 · DPR 22.11 · HM signals to the night sheet of 22 Nov (disp 21:30 / 21:55)',call:[['Gokova-M','8'],['Blue Shark','15A'],['Zheng Hui','7'],['Manta Sena','1']]};")

# ================= V — list 23.11 + DPR 23.11 + day signal =================
M = "{b:'5',n:'Vishva Bandhan',nm:9258,p:[33.25,41.5]"
pre(M, D + ": 2,164 MT in 24 h on 6 hooks — 43,114 off, only 884 left → about 23 Nov 17:00 at this rate. " + L + ": GOV · CJ-5 · NORM now printed 8,050 (9,258 before) · ETC 23 NOV 07:40 (22 Nov 14:33 before) — the port has re-stated her permissible time after the shift; \"S1 59½–68\" is her old place. No sailing for her on the day sheet of 23 Nov and none on programme 23.11.")
sub(M, "f:'11-21 11:24',t:'11-23 14:33',lt:'11-22 14:33',est:1", "f:'11-21 11:24',t:'11-23 07:40'")
B.rep(M, "{b:'5',n:'Vishva Bandhan',nm:8050,p:[33.25,41.5]")
pre("{b:'6',n:'Parvraj',nm:14950,p:[43,51.25]", D + ": 11,487 MT in 24 h on 12 hooks (norm 14,950) — 23,998 off, 25,502 left → about 25 Nov 12:15 at this rate, 28 hours past the list ETC. " + L + ": GOV · CJ-6 · ETC 24 NOV 08:17 — unchanged.")
M = "{b:'7',n:'Flag Marina',nm:42500,p:[56.75,67.25]"
pre(M, D + ": 50,175 MT in 24 h on 15 hooks (quote 42,500) — 94,350 off, 8,900 left → done about 11:15 on 23 Nov at this rate. The DPR again prints her at CJ-8 and CJ-7 as vacant — she lies across both. " + L + ": HP · CJ-7 · 56¾–67¼ · norm 42,500 · ETC 24 NOV 01:03 — the first ETC printed for her. No sailing for her on the day sheet of 23 Nov (disp 08:15) and none on programme 23.11.")
sub(M, "f:'11-21 12:45',t:'11-23 23:05',est:1", "f:'11-21 12:45',t:'11-24 01:03'")
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, D + ": 3,340 MT in 24 h on 9 hooks (1,846 and 803 the two days before) — 6,095 loaded, 5,618 left → about 24 Nov 23:20 at this rate (it was 27 Nov on DPR 22.11). " + L + ": printed under HP with \"SGR(PROJ)\" · CJ-16 · no norm or ETC — unchanged.")
sub(M, "t:'11-27 03:30',est:1", "t:'11-24 23:20',est:1")
pre("{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]", D + ": 24,703 pcs / 8,020 CBM in 24 h on 12 hooks (6,998 the day before; norm 4,600) — 15,358 CBM off, 19,511 left → about 25 Nov 17:20 at this rate (26 Nov 05:30 on DPR 22.11). " + L + ": SAAGAR · CJ-13 · ETC 28 NOV 17:58 — unchanged.")
M = "{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]"
pre(M, SG + ": WARP 09:30 on 23 Nov · Capt Deepak · 143½–156¾ → 145¾–158¼ — moved 2¼ panels north to make room for Lila Tokyo (229 m) at CJ-14. " + D + ": 19,543 pcs / 6,811 CBM in 24 h on 12 hooks (6,339 the day before) — 30,181 CBM off, 12,704 left → about 25 Nov 03:45 at this rate (25 Nov 08:50 on DPR 22.11) · stevedore Mihir & Co. " + L + ": SAAGAR · CJ-15 · already printed at 145¾–158¼ with \"W1 143½–156¾\" · ETC 28 NOV 07:30 — unchanged.")
B.rep(M, "{b:'15',n:'ML Egret',nm:4600,p:[145.75,158.25]")
M = "{b:'15A',n:'Belmoira',nm:30000,p:[160.5,171.75]"
pre(M, D + ": 29,491 MT in 24 h on 12 hooks (quote 30,000) — 39,475 loaded, 18,825 left → about 23 Nov 22:20 at this rate. " + L + ": 24 HRS · CJ-15A · \"24HRS(30K)\" · made fast 21 Nov 19:50, commenced 21:50 · norm 30,000 · ETC 23 NOV 20:28 — the first ETC printed for her (the board had about 18:30, counted from the made-fast hour).")
sub(M, "t:'11-23 18:30',est:1", "t:'11-23 20:28'")
M = "{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]"
pre(M, D + ": OTB 09:45, MADE FAST 11:30, RE-COMMENCED 13:25 on 22 Nov — 2,099 MT in her first 17½ h on 12 hooks; the sheet prints 13,530 loaded and 13,670 left (the list counts 14,321 MT for this call). " + L + ": 6.5K / 8K · CJ-1 · 7½–N · norm 6,500 · ETC 24 NOV 18:22 · \"(32700-TOTAL)\". The board had 11:45 for the berthing.")
sub(M, "f:'11-22 11:45',t:'11-24 14:45',est:1", "f:'11-22 11:30',t:'11-24 18:22'")
pre("{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]", D + ": rice bags 2,900 MT (14,727 left) + wheat flour 332 (2,119 left) + sugar bags 475 (3,002 left) — 3,707 MT in 24 h on 10 hooks (2,474 the day before); 19,848 of 32,700 left → about 28 Nov 15:30 at this rate. " + L + ": printed under the BITUMEN heading · CJ-2 · ETC 30 NOV 13:50 — unchanged; no norm printed.")
pre("{b:'4',n:'Safi Alfa',nm:3450,p:[23,31.75]", D + ": 5,154 MT in 24 h on 15 hooks (3,994 the day before; norm 3,450) — 12,522 loaded, 13,578 left → about 25 Nov 22:15 at this rate, two days inside the list ETC. " + L + ": GENERAL · CJ-4 · ETC 28 NOV 00:00 — unchanged.")
M = "{b:'9',n:'Sand Topic',p:[69,77.75]"
pre(M, D + ": MADE FAST 02:45, COMMENCED 04:50 on 23 Nov — 3,095 MT in the first two hours on 5 hooks; 48,197 left. The board had about 01:30. " + L + ": GFPL · CJ-9 · 69–77¾ · petcoke 51,291.7 MT · NORM 20,000 · made fast printed \"22 Nov 02:45\" and ETC 24 Nov 18:18 — the date is a slip: the berth was Yuan Hang Wei Ye's until 00:01 on the 23rd, and the DPR and the signal both say 23 Nov. Counted from 23 Nov her permissible time is 25 Nov 18:18.")
sub(M, "f:'11-23 01:30',t:'11-25 14:45',est:1", "f:'11-23 02:45',t:'11-25 18:18',lt:'11-24 18:18',est:1")
B.rep(M, "{b:'9',n:'Sand Topic',nm:20000,p:[69,77.75]")
M = "{b:'9',n:'Yuan Hang Wei Ye (next call)',p:[69,77.25]"
pre(M, D + ": COMPLETED 18:30 on 22 Nov, LEFT THE BERTH 00:01 on 23 Nov — 50,455 MT, the last 20,455 on 8 hooks (signal: RT OUT 23:30).")
sub(M, "t:'11-22 23:30'", "t:'11-23 00:01'")
M = "{b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133]"
pre(M, SG + ": RT OUT 11:00 on 23 Nov · Capt Yadav · 126½–133 → OTB — six and a half hours ahead of the programme's 17:30; LILA TOKYO takes the berth, not Hai Nam 81. " + D + ": COMMENCED 10:40 on 22 Nov, COMPLETED 03:40 on 23 Nov — 640 pipes / 3,804 MT on 5 hooks. " + L + ": \"[14]\" · norm 2,875 · ETC 23 Nov 15:40.")
sub(M, "f:'11-22 05:55',t:'11-23 17:30'", "f:'11-22 05:55',t:'11-23 11:00'")
pre("{b:'14',n:'Sanghi Sundarshan',p:[135,141.75]", D + ": COMPLETED 20:30, LEFT THE BERTH 23:00 on 22 Nov — 168 coils / 4,004 MT. " + L + ": \"[14A]\" · \"SPACE A/C\".")
M = "{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]"
pre(M, D + ": the sailing box prints NEW BLISS · CJ 1 · 10:15 (22 Nov) — her let-go hour (signal: OUT 10:00).")
sub(M, "t:'11-22 10:00'", "t:'11-22 10:15'")

# ---- CJ-14: Hai Nam 81's programmed entry comes out, Lila Tokyo goes in
a, b = B.line_of(" {b:'14',n:'Hai Nam 81',nm:30000,p:[126.5,141]")
NEWV = (" {b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5],c:'Gypsum in bulk',q:72633,u:'MT',cat:'COASTAL',via:'30k/25k quote (Sr No 7)',f:'11-23 12:45',t:'11-25 22:50',est:1,note:'"
    + q(SG + ": IN 10:45 on 23 Nov · Capt Omesh · OTB → 126–143½ — the hour is the pilot boarding at OTB; she comes alongside on the flood (high water 13:02) behind the tug-and-barge (RT OUT 11:00): about 12:45, est. "
        + L + ": printed under COASTAL · CJ-14 · 126–143½ · \"(GL)\" · gypsum in bulk 72,633 MT IMP · NORM 30,000 · remark \"CSTL(30K) B'TODAY\" · no ETC yet — 72,633 MT at her 30,000 quote → about 25 Nov 22:50, est. "
        "Waiting sheet: starred, HP X · GEN X, \"30K/25K/10K … CJ 7 & 8, 13-16 B'TODAY\" — reported / ready 17 Nov 19:05, HP 2 until now. "
        "PROGRAMME 23.11 had named HAI NAM 81 for this place (\"provisional berthing\", in about 19:30 this evening). The port has berthed Lila Tokyo instead, in the forenoon — the senior ready vessel on a 30K quote; ML Egret was warped at 09:30 to make her room. Hai Nam 81 is back on the waiting sheet. Why the vessel was changed is not on the papers (check log, open).") + "'},")
B.s = B.s[:a] + NEWV + B.s[b:]
B.rep("'Hai Nam 81':189.94});", "'Hai Nam 81':189.94,'Lila Tokyo':229});")

# ================= name maps / constants =================
after("Object.assign(REP,{'Zheng Hui':'11-21 08:12','Manta Omer Mecit':'11-20 17:30',",
      "Object.assign(REP,{'Zheng Hui':'11-21 07:54','KM Jakarta':'11-21 21:48','Paiwan Ace':'11-22 00:06','Asian Summit':'11-22 10:00','Hai Nam 81':'11-22 19:15','African Pheasant':'11-23 04:24','Tug Marigold + barge Alaacrity 666':'11-19 10:24'}); // list 23.11 — reporting hours as printed on the waiting sheet (placed last so that it wins)")
after("Object.assign(AG,{'KM Jakarta':'True Blue','Erna Oldendorff':'DBC','African Pheasant':'Synergy'});",
      "Object.assign(AG,{'Horizon Chaser':'Preetika','Saturn J':'DBC','Jumbo Kinetic':'Gautham Freight'});Object.assign(IE,{'Horizon Chaser':'IMP','Saturn J':'EXP','Jumbo Kinetic':'IMP','Hai Nam 81':'EXP','Asian Summit':'IMP'}); // list 23.11")
setline("const ETA={'KM Jakarta':", "const ETA={'Tai Keystone':'11-22 00:00','Zheng Run':'11-22 12:00','V Pacific':'11-23 00:00','Hai Long 1':'11-23 00:00','Lolo Gate':'11-23 00:00','Outlander':'11-23 00:00','Erna Oldendorff':'11-23 00:00',"
        "'Horizon Chaser':'11-23 00:00','Saturn J':'11-23 00:00','KSS Edmond':'11-24 00:00','Kang Qi Fu Hua':'11-24 00:00','Kerem':'11-24 00:00','Meghna Prestige (salt, next call)':'11-24 00:00','Jumbo Kinetic':'11-24 00:00',"
        "'Princess Manissa':'11-25 00:00','Valentina Sea':'11-26 00:00','Gutian Trust':'11-30 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 23.11 (0700) — Tai Keystone and Zheng Run are STILL printed on it; KM Jakarta, Paiwan Ace, Asian Summit, Hai Nam 81 and African Pheasant have reported")
B.rep("Object.assign(SAILDR,{'Hai Nam 81':12.6,'Zheng Run':12.63});", "Object.assign(SAILDR,{'Hai Nam 81':12.6,'Zheng Run':12.63,'KM Jakarta':13.0});")

# ================= W — list 23.11 =================
def w(name, text, **k): B.list_tag = L; B.wrow(name, q(text), **k)
w('Blue Shark', "GEN 1 — unchanged")
w('Fortunelit', "GEN 2 · working at MS · " + D + ": no work on the ship in the 24 h (1,051 MT moved at CJ/IFFCO) — 7,000 loaded, 3,000 left")
w('Manta Sena', "8K 1 · GEN 3 — back at the head of the 6.5K / 8K line now that Crystal O is alongside (made fast 22 Nov 11:30)", rk="'8K':1,GEN:3")
w('Crystal Land', "8K 2 · GEN 4", rk="'8K':2,GEN:4")
w('Libra', "GEN 5 · working at MS · " + D + ": 2,682 MT in 24 h at midstream (1,530 through IFFCO) — 20,698 loaded, 2,302 left → done about 24 Nov 03:30 without a berth", rk="GEN:5")
w('Pioneer Fortune', "8K 3 · GEN 6 · Sr No 7", rk="'8K':3,GEN:6")
w('Katerina K', "PRINTED WITH A RANK AGAIN — GEN 6, the same number as Pioneer Fortune (who reported an hour and a half before her): carried as 6.5 · the star and \"B'TODAY\" are gone · remark as before", rk="GEN:6.5")
w('MK Lamis', "GEN 7 · remark unchanged · " + D + ": a shore row is opened for her at IFFCO — 11,500 MT to load, nothing moved yet", rk="GEN:7")
w('Ariston Bulker', "GEN 8 · working at MS · " + D + ": no work — 3,530 loaded, 4,470 left", rk="GEN:8")
w('Aboudi D', "GEN 9 · 2 shore cranes required", rk="GEN:9")
w('African Loon', "GEN 10 printed · STS transhipment, working at MS — still held · " + D + ": no work on her sheet in the 24 h — 25,820 off, 31,930 left", rk="GEN:10")
w('Gokova-M', "HP 1 · 24H 1 · 8K 5 · GEN 12", rk="HP:1,'24H':1,'8K':5,GEN:12")
w('AG Varvara', "SGR 1 · GEN 13 · Sr No 7 — still the senior vessel of the SAAGAR line", rk="SAAGAR:1,GEN:13")
w('Xin Hai Tong 71', "SGR 2 · STL 1 · GEN 14 (STL kept out — Mihir, 15 Nov)", rk="SAAGAR:2,GEN:14")
w('Porto Fiscardo', "8K 6 · GEN 15", rk="'8K':6,GEN:15")
w('Captainannis L', "8K 7 · GEN 16 · DOC NR · working at MS · " + D + ": 650 MT in 24 h — 5,061 loaded, 12,739 left", rk="'8K':7,GEN:16")
w('CD Glory', "SGR 3 · 8K 8 · GEN 17 · Sr No 7 — her SAAGAR place is unchanged: AG Varvara (1) and Xin Hai Tong 71 (2) ahead; Paiwan Ace is now SGR 6 behind her", rk="SAAGAR:3,'8K':8,GEN:17")
w('Dariya Priya', "SGR 4 · 8K 9 · GEN 18 · Sr No 7 · working at MS · " + D + ": at midstream 4,700 pcs / 1,314 CBM in 24 h on 6 hooks — 3,662 CBM off, 41,306 left", rk="SAAGAR:4,'8K':9,GEN:18")
w('Sea Postman', "GEN 19 · working at MS · " + D + ": 7,583 MT into barges in 24 h on 6 hooks — 21,204 off, 7,296 left → done about 24 Nov 06:00 at midstream, without a berth", rk="GEN:19")
w('Sheng Tai', "GEN 20 printed · daughter vessel, working at MS (STS) — still held · " + D + ": 2,217 MT in 24 h — 25,237 loaded, 30,763 left", rk="GEN:20")
w('African Tiger', "SGR 5 · 8K 10 · GEN 22 · Sr No 7", rk="SAAGAR:5,'8K':10,GEN:22")
w('Ocean Kudos', "HP 3 · 8K 11 · GEN 23 — still printed with ranks and readiness 18 Nov 16:06; held on the team's word of 21 Nov (not ready)", rk="HP:3,'8K':11,GEN:23")
w('Josco Taicang', "GEN 24 — the first rank printed for her", rk="GEN:24")
w('MSC Magali', "HP 4 · GEN 25 · \"(GL)\" · 30K/25K/10K", rk="HP:4,GEN:25")
w('Manta Omer Mecit', "GEN 26 — the first rank printed for her", rk="GEN:26")
w('Zheng Hui', "GEN 27 (was Y) · reported / ready now printed 21 Nov 07:54 (08:12 on the revised list of 21.11) · still no GP rank printed (DAP — Govt by the cargo rule)", rk="GEN:27", rdy="11-21 07:54")
w('KM Jakarta', "NOW ON THE WAITING SHEET · reported 21 Nov 21:48 · N/A · HP Y · 8K Y · \"30K/25K/10K SR.NO 07\" · DD 13.00 m · 6.4 m", dr="6.4")
w('Star New London', "unchanged — N/A · 8K Y · \"30K/25K SR.NO:07\"")
w('Paiwan Ace', "MIHIR & COMPANY · NOW ON THE WAITING SHEET (still printed \"PAIWAN ICE\") · reported 22 Nov 00:06 · READINESS 22 Nov 11:00 · SGR 6 · 8K 12 · Sr No 7 · 10.83 m — she is in the SAAGAR line from today, behind African Tiger (SGR 5)", rk="SAAGAR:6,'8K':12", rdy="11-22 11:00", dr="10.83")
w('Asian Summit', "NOW ON THE WAITING SHEET · reported / ready 22 Nov 10:00 · HP Y · SGR Y · GEN Y · \"30K/25K/10K SR NO.07\" · 13.35 m", rk="HP:98,SAAGAR:98,GEN:98", dr="13.35")
w('African Pheasant', "NOW ON THE WAITING SHEET · reported 23 Nov 04:24 · READINESS 23 Nov 11:00 — declared for today's meeting · SGR Y · 8K Y · Sr No 7 · 10.98 m", rdy="11-23 11:00", dr="10.98")
w('Erna Oldendorff', "still on the expected sheet — ETA / readiness 23 Nov 00:00 · SGR Y · Sr No 7")
w('Tai Keystone', "STILL ON THE EXPECTED SHEET at 0700 on 23 Nov with the ETA / readiness of 22 Nov 00:00 — she has not reported; no rank printed")
w('Zheng Run', "still on the expected sheet — ETA / readiness 22 Nov 12:00 · HP Y")
w('Tug Marigold + barge Alaacrity 666', "reporting now printed 19 Nov 10:24 (12:25 before) · N/A · 700 pipes")
B.wdel('Lila Tokyo')
m = B._row('Asian Summit').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Hai Nam 81','Salt in bulk',52000,'MT',189.94,6.2,'11-22 19:15',{HP:98,'8K':98},'" + q(L + ": BACK ON THE WAITING SHEET — reported / ready 22 Nov 19:15 · HP Y · 8K Y · \"30K/25K/10K SR.NO 07\" · DD 12.60 m · 6.2 m. Programme 23.11 had given her the tug-and-barge's place for the evening of 23 Nov as a provisional berthing; list 23.11 and the HM signal of 23 Nov give that place to Lila Tokyo, who berths this forenoon. Hai Nam 81 waits · LIST 21.11 (revised): ETA / readiness 22 Nov 15:00 (was 16:00) · LIST 20.11 (revised after the meeting): ETA / readiness moved to 22 Nov 16:00 · 52,000 MT · HP Y · 8K Y · LIST 19.11 (ETA sheet): NEW · ETA 20 Nov 20:00 · N/A · HP Y · 8K Y · 30K/25K/10K Sr No 7 · departure draught 12.60 m · agent Gautham Freight") + "'],",
 " ['Horizon Chaser','Bitumen',3820,'MT',94.4,5.9,null,{},'" + q(L + " (ETA sheet): NEW · MT HORIZON CHASER · bitumen 3,820.32 MT IMP · ETA 23 Nov · N/A · 94.4 m, 5.9 m · remark \"16 1/2 PANELS\" · agent Preetika — the first bitumen tanker on the list since the board began; the Bitumen place is held by DSM London as General") + "'],",
 " ['Saturn J','Rice bags',31000,'MT',179.5,3.6,null,{},'" + q(L + " (ETA sheet): NEW · rice bags 31,000 MT EXP · ETA 23 Nov · N/A · 179.5 m · agent DBC") + "'],",
 " ['Jumbo Kinetic','2 harbour mobile cranes + 19 packages (project)',844,'MT',152.6,8.6,null,{COASTAL:98},'" + q(L + " (ETA sheet): NEW · \"2 HMC, 19 PKGS\" 843.8 MT IMP · ETA 24 Nov · N/A · CSTL Y · 152.6 m, 8.6 m · agent Gautham Freight") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
B.rep(" // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 21.11 (0700)", " // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 23.11 (0700)")

# ================= DPR const =================
def R(loc, n, ie, c, l24, upto, bal, g='', hk=0, note='', partial=None, comm=None):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if partial: d['partial'] = 1; d['comm'] = comm
    d['note'] = note; return d
ROWS = [
 R('CJ-1', 'Crystal O', 'EXP', 'Sugar bags', 2099, 13530, 13670, '4/4/4', 12, 'OTB 09:45, MADE FAST 11:30, RE-COMMENCED 13:25 on 22 Nov — 2,099 MT in her first 17½ h on 12 hooks; the sheet prints 13,530 loaded and 13,670 left (the list counts 14,321 MT for this call)', True, '11-22 13:25'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 3707, 12852, 19848, '4/3/3', 10, 'rice bags 2,900 MT (7,773 loaded, 14,727 left) + wheat flour 332 (2,081 / 2,119) + sugar bags 475 (2,998 / 3,002) — 3,707 MT in 24 h on 10 hooks (2,474 the day before); 19,848 left → about 28 Nov 15:30 at this rate'),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 5154, 12522, 13578, '5/5/5', 15, '5,154 MT in 24 h on 15 hooks (3,994 the day before; norm 3,450) — 12,522 loaded, 13,578 left → about 25 Nov 22:15 at this rate, two days inside the list ETC (28 Nov 00:00)'),
 R('CJ-5', 'Vishva Bandhan', 'IMP', 'Granular urea bulk', 2164, 43114, 884, '2/2/2', 6, '2,164 MT in 24 h on 6 hooks — 43,114 off, only 884 left → about 23 Nov 17:00 at this rate; her permissible time (list ETC 23 Nov 07:40) is over'),
 R('CJ-6', 'Parvraj', 'IMP', 'DAP', 11487, 23998, 25502, '4/4/4', 12, '11,487 MT in 24 h on 12 hooks (norm 14,950) — 23,998 off, 25,502 left → about 25 Nov 12:15 at this rate, 28 hours past the list ETC (24 Nov 08:17)'),
 R('CJ-8', 'Flag Marina', 'IMP', 'US coal in bulk', 50175, 94350, 8900, '5/5/5', 15, '50,175 MT in 24 h on 15 hooks (quote 42,500) — 94,350 off, 8,900 left → done about 11:15 on 23 Nov at this rate. The DPR prints her at CJ-8 and CJ-7 as VACANT — she is 254 m and lies across both'),
 R('CJ-9', 'Yuan Hang Wei Ye (next call)', 'EXP', 'Iron ore pellets', 20455, 50455, 0, '5/3/0', 8, 'COMPLETED 18:30 on 22 Nov, LEFT THE BERTH 00:01 on 23 Nov — 50,455 MT, the last 20,455 on 8 hooks'),
 R('CJ-9', 'Sand Topic', 'IMP', 'Petcoke', 3095, 3095, 48197, '0/0/5', 5, 'MADE FAST 02:45, COMMENCED 04:50 on 23 Nov — 3,095 MT in the first two hours on 5 hooks; 48,197 left', True, '11-23 04:50'),
 R('CJ-13', 'Uni Blossom', 'IMP', 'Pine logs', 8020, 15358, 19511, '4/4/4', 12, '24,703 pcs / 8,020 CBM in 24 h on 12 hooks (6,998 the day before; norm 4,600) — 15,358 CBM off, 19,511 left → about 25 Nov 17:20 at this rate, three days inside the list ETC (28 Nov 17:58)'),
 R('CJ-14', 'Tug Sagar 5 + barge Victoria 250', 'EXP', 'Coated steel pipes', 3804, 3804, 0, '1/2/2', 5, 'COMMENCED 10:40 on 22 Nov, COMPLETED 03:40 on 23 Nov — 640 pipes / 3,804 MT on 5 hooks; let-go hour blank (day signal: RT OUT 11:00)'),
 R('CJ-14', 'Sanghi Sundarshan', 'IMP', 'Steel coil', 3909, 4004, 0, '1/1/0', 2, 'printed as "CJ-14A" · COMPLETED 20:30, LEFT THE BERTH 23:00 on 22 Nov — 168 coils / 4,004 MT'),
 R('CJ-15', 'ML Egret', 'IMP', 'Pine logs', 6811, 30181, 12704, '4/4/4', 12, '19,543 pcs / 6,811 CBM in 24 h on 12 hooks (6,339 the day before; norm 4,600) — 30,181 CBM off, 12,704 left → about 25 Nov 03:45 at this rate · stevedore Mihir & Co'),
 R('CJ-15A', 'Belmoira', 'EXP', 'Salt in bulk', 29491, 39475, 18825, '4/4/4', 12, '29,491 MT in 24 h on 12 hooks (quote 30,000) — 39,475 loaded, 18,825 left → about 23 Nov 22:20 at this rate · destination printed: Karachi'),
 R('CJ-16', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes', 3340, 6095, 5618, '3/3/3', 9, '3,340 MT in 24 h on 9 hooks (1,846 and 803 the two days before) — 6,095 loaded, 5,618 left → about 24 Nov 23:20 at this rate'),
 R('MS', 'Sea Postman', 'IMP', 'Rock phosphate', 7583, 21204, 7296, '2/2/2', 6, '7,583 MT into barges in 24 h on 6 hooks (5,137 the day before) — 21,204 off, 7,296 left → about 24 Nov 06:00 at this rate'),
 R('MS', 'Libra', 'EXP', 'Rice bags', 2682, 20698, 2302, '1/1/1', 3, '2,682 MT in 24 h (1,530 through IFFCO) — 20,698 loaded, 2,302 left → about 24 Nov 03:30 at this rate'),
 R('MS', 'Sheng Tai', 'EXP', 'Barite ore', 2217, 25237, 30763, '1/1/1', 3, 'daughter vessel, ship-to-ship from African Loon — 2,217 MT in 24 h; 25,237 loaded, 30,763 left'),
 R('MS', 'Yara J', 'IMP', 'Rice bags', 1857, 27357, 2643, '1/1/1', 3, '1,857 MT into barges in 24 h — 27,357 off, 2,643 left'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 1314, 3662, 41306, '2/2/2', 6, 'at midstream 4,700 pcs / 1,314 CBM in 24 h on 6 hooks (1,705 the day before) — 3,662 CBM off, 41,306 left'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 650, 5061, 12739, '2/2/2', 6, '650 MT in 24 h on 6 hooks — 5,061 loaded, 12,739 left'),
 R('MS', 'MAK 1', 'EXP', 'Rice in J-bags', 180, 21268, 620, '0/1/1', 2, '180 MT in 24 h — the first work in five days; 620 MT left'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 0, 25820, 31930, '1/1/1', 3, 'mother vessel — nothing on her own sheet in the 24 h; 25,820 off, 31,930 left'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 0, 7000, 3000, '', 0, 'no work on the ship in the 24 h (1,051 MT moved at CJ/IFFCO) — 3,000 left'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no work — 4,470 left'),
 R('MS', 'North Gate', 'EXP', 'Chick peas / rice J-bags', 0, 23940, 3060, '', 0, 'no work on the ship (1,382 MT moved at OP/CJ) — 3,060 left'),
 R('OJ-1', 'Hafnia Ammolite', 'IMP', 'CDSBO', 6970, 6970, 23830, '', 0, 'MADE FAST 10:00, COMMENCED 13:06 on 22 Nov — 6,970 MT in 18 h; 23,830 left', True, '11-22 13:06'),
 R('OJ-2', 'PVT Aurora', 'IMP', 'Chemicals', 5000, 5000, 0, '', 0, 'made fast 08:18, commenced 10:25 on 22 Nov, COMPLETED 22:40, LEFT THE BERTH 02:40 on 23 Nov — 5,000 MT'),
 R('OJ-2', 'Rasheeda', 'EXP', 'Chemicals', 0, 0, 3156, '', 0, 'MADE FAST 06:48 on 23 Nov, not commenced at 0700 — 3,156 MT to load', True, None),
 R('OJ-3', 'Hartati', 'EXP', 'Chemicals', 9590, 10090, 910, '', 0, '9,590 MT in 24 h — 10,090 loaded, 910 left → done about 09:15 on 23 Nov'),
 R('OJ-4', 'Bow Fortitude', 'IMP', 'Chemicals', 10172, 10172, 0, '', 0, 'COMMENCED 08:12 on 22 Nov, COMPLETED 03:00, LEFT THE BERTH 06:25 on 23 Nov — 10,172 MT'),
 R('OJ-4', 'Al Mahboobah', 'EXP', 'Benzene', 0, 0, 9336, '', 0, '"BERTHING TODAY" at 0700 on 23 Nov — 9,336 MT to load', True, None),
 R('OJ-6', 'Orchids', 'IMP', 'VLSFO', 757, 8600, 0, '', 0, 'COMPLETED 12:48, LEFT THE BERTH 16:20 on 22 Nov — 8,600 MT'),
 R('OJ-6', 'Willows', 'IMP', 'MS', 4073, 4073, 23927, '', 0, 'MADE FAST 23:42 on 22 Nov, COMMENCED 01:42 on 23 Nov — 4,073 MT in the first 5¼ h; 23,927 left', True, '11-23 01:42'),
 R('OJ-7', 'Ginga Cheetah', 'IMP', 'CDSBO + CSFO', 14780, 14780, 9490, '', 0, 'MADE FAST 09:54, COMMENCED 12:35 on 22 Nov — 14,780 MT in 18½ h; 9,490 left → about 19:00 on 23 Nov', True, '11-22 12:35'),
 R('TT-1', 'Europa Graeca', 'IMP', 'Sugar bulk', 3131, 75677, 0, '', 0, 'COMPLETED 18:30, LEFT THE BERTH 22:36 on 22 Nov — 75,677 MT'),
 R('TT-1', 'Blue Ionian', 'IMP', 'Sugar bulk', 270, 270, 73085, '', 0, 'MADE FAST 01:00, COMMENCED 06:30 on 23 Nov — 270 MT in the first half hour; 73,085 left', True, '11-23 06:30'),
 R('TT-2', 'Woohyun Dream', 'EXP', 'RSM in bulk', 11860, 22260, 9240, '', 0, '11,860 MT in 24 h — 22,260 loaded, 9,240 left → about 24 Nov 01:45 at this rate'),
 R('TT-3', 'Marvelous Star', 'IMP', 'Coal in bulk', 17517, 74517, 2327, '', 0, '17,517 MT in 24 h — 74,517 off, 2,327 left → done about 10:15 on 23 Nov; MP Postpanamax 1 is "B\'TODAY" behind her'),
]
a = B.s.index("const DPR={d:'22.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
old = B.s[a:e].split('\n'); ri = next(i for i, l in enumerate(old) if l.startswith(' rows:['))
keep = old[2:ri]
NEWDPR = ("const DPR={d:'23.11.2026',asOf:'11-23 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 23 Nov (xlsx from Mihir, 23 Nov 11:06)',\n"
 " tot:{dry:159891,dryL:74230,dryU:85661,ms:14266,kict:35446,tuna:32778,oj:51342,vad:523018,all:816741,gangs:'PR 27 · TR 0 · 42 + 6 W gangs demanded / 42 + 6 W supplied',rakes:'3',wb:785,sail:'New Bliss · CJ-1 · 10:15 · Artigo · OJ-1 · 07:30 · Flexi 2 · KICT-12 · 10:00'},\n"
 + "\n".join(keep) + ("\n" if keep else "") + " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]

# ================= MSWORK (Barge tab) =================
out = subprocess.run(['python3', '-I', '/home/claude/berth-board/tools/barge_from_dpr.py', '/home/claude/work/in23b/dpr23.txt', '23.11', '11-23 07:00'], capture_output=True, text=True).stdout.rstrip('\n')
assert out.startswith("  {d:'23.11'") and out.endswith("]},"), out[-40:]
fo = "{n:'Fortunelit',ie:'EXP',c:'Rice bags',loc:'MS',l24:0,upto:7000,bal:3000,shore:''"
assert out.count(fo) == 1; out = out.replace(fo, fo[:-2] + "'CJ/IFFCO 1,051'")   # the tool does not read the "CJ/IFFCO" shore row
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + out + "\n")

# ================= MV =================
MV1 = ['HM signal 23 Nov — day sheet (dispatched 08:15) · Capt Omesh · received 23 Nov 11:06 · cargo berths', [
 ['09:30', 'WARP', 'ML Egret', 'CJ-15 · 143½–156¾ → 145¾–158¼', 'Deepak', '11-23 09:30', '2¼ panels north — room for Lila Tokyo at CJ-14'],
 ['11:00', 'OUT', 'Tug Sagar 5 + barge Victoria 250', 'CJ-14 · 126½–133 → OTB', 'Yadav', '11-23 11:00', 'RT OUT · programme had 17:30'],
 ['10:45', 'IN', 'Lila Tokyo', 'OTB → CJ-14 · 126–143½', 'Omesh', '11-23 12:45', 'pilot boards 10:45 · alongside about 12:45 on the flood, est · CSTL(30K) — programme 23.11 had Hai Nam 81 here'],
 ['12:00', 'OUT', 'TCI Anand', 'CJ-12 · 101–109½ → OTB', 'Madaan', '11-23 12:00', 'container'],
 ['10:45', 'IN', 'Enzo 2', 'OTB → CJ-12 · 100–109', 'Deepak', '11-23 13:00', 'FLOOD · container · behind TCI Anand — est'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Yadav and Capt Deepak — one hour PMS on completion', '—', '11-23 13:00', '']]]
MV2 = ['DPR 23.11 and list 23.11 — actual hours at the cargo jetties, 22 Nov and the night', [
 ['10:15', 'OUT', 'New Bliss', 'CJ-1 → OTB', '—', '11-22 10:15', 'sailing box: 10:15 (signal 10:00)'],
 ['11:30', 'IN', 'Crystal O', 'OTB → CJ-1', '—', '11-22 11:30', 'OTB 09:45, made fast 11:30, re-commenced 13:25 — board had ~11:45'],
 ['13:20', 'OUT', 'TCI Express', 'CJ-11 → OTB', '—', '11-22 13:20', 'container · completed 12:44, left the berth 13:20 (signal 13:00)'],
 ['20:45', 'IN', 'Al Hadbaa', 'OTB → CJ-11 · 88–94½', '—', '11-22 20:45', 'container · made fast 20:45, commenced 21:44'],
 ['20:45', 'IN', 'TCI Anand', 'OTB → CJ-12 · 101–109½', '—', '11-22 20:45', 'container · made fast 20:45, commenced 21:45'],
 ['23:00', 'OUT', 'Sanghi Sundarshan', 'CJ-14 · 135–141¾ → OTB', '—', '11-22 23:00', 'completed 20:30, left the berth 23:00'],
 ['00:01', 'OUT', 'Yuan Hang Wei Ye', 'CJ-9 → OTB', '—', '11-23 00:01', 'completed 18:30 on 22 Nov, left the berth 00:01 (signal 23:30)'],
 ['02:45', 'IN', 'Sand Topic', 'OTB → CJ-9', '—', '11-23 02:45', 'made fast 02:45, commenced 04:50 — board had ~01:30 · the list prints the date as 22 Nov']]]
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
def berth(bid, nown, add, f=None, nm=None, etc=None, qty=None, est=None, prevout=None):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    if f is not None: now['f'] = js(f)
    if est is False: now.pop('est', None)
    if nm is not None: now['nm'] = js(nm)
    if etc is not None: now['etc'] = js(etc)
    if qty is not None: now['q'] = repr(qty)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS)
    if prevout:
        pv = obj(d['prev']); pv['out'] = js(prevout[0]); pv['outBy'] = "'" + q(prevout[1] + ' · ') + pv['outBy'][1:]
        d['prev'] = unobj(pv, ('n', 'c', 'q', 'u', 'ie', 'ag', 'out', 'outBy'))
    bput(a, b, d, tail)
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
    d['prev'] = unobj(pv, ('n', 'c', 'q', 'u', 'ie', 'ag', 'out', 'outBy')); d['now'] = unobj(nw, NOWKEYS); bput(a, b, d, tail)
berth('OJ-1', 'Hafnia Ammolite', L + ' / ' + D + ': OJ-1 · MADE FAST 22 Nov 10:00, COMMENCED 13:06 · CDSBO 30,800 MT IMP · norm 300 MT/h · ETC 26 NOV 22:40 · 6,970 MT by 0700 on 23 Nov, 23,830 left (the board had about 09:20)',
      f='11-22 10:00', est=False, nm='300', etc='11-26 22:40', prevout=('11-22 07:30', 'DPR 23.11 sailing box: ARTIGO · OJ 1 · 07:30'))
turn('OJ-2', 'PVT Aurora', '11-23 02:40', 'DPR 23.11: commenced 10:25 on 22 Nov, completed 22:40, LEFT THE BERTH 02:40 on 23 Nov — 5,000 MT (signal: RT OUT 02:30) · list 23.11: "[2]" · norm 225 MT/h · ETC 23 Nov 10:31',
     'Rasheeda', '11-23 06:48', False, L + ' / ' + D + ': OJ-2 · MADE FAST 23 Nov 06:48, not commenced at 0700 · chemicals 3,156.023 MT EXP (5,000 on the earlier lists) · norm 250 MT/h · no ETC yet (the board had about 04:30)', nm='250', qty=3156.02)
berth('OJ-3', 'Hartati', L + ' / ' + D + ': norm 250 MT/h · ETC 24 NOV 01:54 · 9,590 MT in 24 h — 10,090 loaded, 910 left → done about 09:15 on 23 Nov', nm='250', etc='11-24 01:54')
turn('OJ-4', 'Bow Fortitude', '11-23 06:25', 'DPR 23.11: commenced 08:12 on 22 Nov, completed 03:00, LEFT THE BERTH 06:25 on 23 Nov — 10,172 MT (signal: OUT 07:00) · list 23.11: "[4]" · norm 360 MT/h · ETC 23 Nov 14:03',
     'Al Mahboobah', '11-23 08:25', True, L + ' / ' + D + ': OJ-4 · "B\'TODAY" / "BERTHING TODAY" · benzene 9,336.421 MT EXP · norm 360 MT/h · no dated ETC yet — in behind Bow Fortitude (left 06:25): about 08:25, est', nm='360')
turn('OJ-6', 'Orchids', '11-22 16:20', 'DPR 23.11: completed 12:48, LEFT THE BERTH 16:20 on 22 Nov — 8,600 MT (signal: RT OUT 16:00)',
     'Willows', '11-22 23:42', False, L + ' / ' + D + ': OJ-6 · MADE FAST 22 Nov 23:42, COMMENCED 23 Nov 01:42 · MS 28,000 MT IMP · no norm ("-") or ETC · 4,073 MT by 0700, 23,927 left')
berth('OJ-7', 'Ginga Cheetah', L + ' / ' + D + ': OJ-7 · MADE FAST 22 Nov 09:54, COMMENCED 12:35 · norm 650 MT/h · ETC 24 NOV 03:14 · 14,780 MT by 0700 on 23 Nov, 9,490 left → about 19:00 on 23 Nov (the board had about 08:00)',
      f='11-22 09:54', est=False, nm='650', etc='11-24 03:14')
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
wait = [r.rstrip(',') for r in B.s[w0 + len(" wait:[\n"):e0].split('\n')]
eta = [r.rstrip(',') for r in B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n')]
def nm_(r): return re.match(r"  \{n:'((?:[^'\\]|\\.)*)'", r).group(1)
def setf(r, key, val):
    rx = re.compile(r"\b" + key + r":(?:'(?:[^'\\]|\\.)*'|null)"); assert len(rx.findall(r)) == 1, (key, r[:80]); return rx.sub(lambda _: key + ":" + ("'" + q(val) + "'" if val is not None else 'null'), r)
def remp(r, text):
    i = r.index("rem:'") + 5; return r[:i] + q(text) + (" · " if r[i] != "'" else "") + r[i:]
TG = 'LIST 23.11: '
assert [nm_(r) for r in wait] == ['Lumis', 'Ahinos', 'Peonia', 'Sriwangi V', 'Chemroute Pegasus', 'Chemroad Nexus', 'Thetis Leona'], [nm_(r) for r in wait]
WCH = {
 'Sriwangi V': lambda r: remp(setf(r, 'rank', '1E'), TG + 'rank "1E" (was 3E) — first of the edible-oil line now · "commercially ready"'),
 'Chemroute Pegasus': lambda r: remp(setf(r, 'rank', '1C'), TG + 'rank "1C" — first of the chemical line now'),
 'Chemroad Nexus': lambda r: remp(setf(r, 'rank', '2C'), TG + 'rank "2C"'),
 'Thetis Leona': lambda r: remp(setf(r, 'rank', '3C'), TG + 'rank "3C"'),
}
W2 = [WCH[nm_(r)](r) if nm_(r) in WCH else r for r in wait]
for d in (
 {'n': 'Ocean Star', 'c': 'Chemicals', 'q': 5203.21, 'u': 'MT', 'ie': 'IMP', 'loa': 145.53, 'dr': 7.2, 'rep': '11-21 17:15', 'rdy': '11-21 17:15', 'rank': '4C', 'ag': 'Atlantic Shg', 'rem': TG + 'ARRIVED — reported / ready 21 Nov 17:15 · rank "4C" · REQ OJ 2, 3, 4 · 7.2 m', 'st': ''},
 {'n': 'MC Hera', 'c': 'Chemicals', 'q': 20599.67, 'u': 'MT', 'ie': 'IMP', 'loa': 182.75, 'dr': 8.7, 'rep': '11-21 23:18', 'rdy': '11-21 23:18', 'rank': '5C', 'ag': 'Atlantic Shg', 'rem': TG + 'ARRIVED — reported / ready 21 Nov 23:18 · rank "5C" · REQ OJ 2, 3, 4 · chemicals 20,599.671 MT (5,000 on the expected sheet before) · 8.7 m', 'st': ''},
 {'n': 'Bochem Shanghai', 'c': 'CPO', 'q': 24000, 'u': 'MT', 'ie': 'IMP', 'loa': 158.9, 'dr': 10.5, 'rep': '11-22 22:42', 'rdy': None, 'rank': '', 'ag': 'Interocean', 'rem': TG + 'ARRIVED — reported 22 Nov 22:42 · N/A · CPO 24,000 MT · 10.5 m', 'st': ''},
 {'n': 'Chemroad Quest', 'c': 'Chemicals', 'q': 4956.47, 'u': 'MT', 'ie': 'IMP', 'loa': 174.43, 'dr': 10.6, 'rep': '11-22 23:45', 'rdy': '11-22 23:45', 'rank': '6C', 'ag': 'JM Baxi', 'rem': TG + 'ARRIVED — reported / ready 22 Nov 23:45 · rank "6C" · REQ OJ 3, 4 · 10.6 m', 'st': ''}):
    W2.append("  " + js(d))
GONE = ('Ocean Star', 'MC Hera', 'Chemroad Quest', 'Bochem Shangha')
E2 = [r for r in eta if nm_(r) not in GONE]; assert len(E2) == len(eta) - 4, [nm_(r) for r in eta]
ECH = {
 'SC Draco': lambda r: remp(setf(r, 'eta', '11-24 00:00'), TG + 'ETA 24 Nov (22 Nov before)'),
 'Bow Tribute': lambda r: remp(setf(r, 'eta', '11-25 00:00'), TG + 'ETA 25 Nov (22 Nov before)'),
 'Green Sanvi (LPG/C)': lambda r: remp(setf(r, 'eta', '11-23 00:00'), TG + 'ETA 23 Nov (22 Nov before) · 9.2 m'),
 'Ginga Merlin': lambda r: remp(setf(r, 'rdy', '11-23 00:00'), TG + 'ETA / readiness 23 Nov 00:00'),
}
seen = set()
for i, r in enumerate(E2):
    if nm_(r) in ECH: E2[i] = ECH[nm_(r)](r); seen.add(nm_(r))
assert seen == set(ECH), set(ECH) - seen
have = {nm_(r) for r in E2}
for d in (
 {'n': 'Culture', 'c': 'VLSFO', 'q': 24000, 'u': 'MT', 'ie': 'EXP', 'loa': 179.99, 'dr': 5.8, 'eta': '11-23 00:00', 'rdy': None, 'ag': 'Malara Shg', 'rem': 'new on list 23.11'},
 {'n': 'Elora 1', 'c': 'CPO', 'q': 20000, 'u': 'MT', 'ie': 'IMP', 'loa': 176, 'dr': None, 'eta': '11-26 21:00', 'rdy': None, 'ag': 'Atlantic Shg', 'rem': 'new on list 23.11'}):
    if d['n'] not in have: E2.append("  " + js(d))
E2.sort(key=lambda r: re.search(r"eta:'([^']*)'", r).group(1))
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(W2) + "\n ],\n eta:[\n" + ",\n".join(E2) + B.s[m0:]
LM = ['DPR 23.11 and list 23.11 — actual hours at the oil jetties, 22 Nov and the night (no oil-jetty row on the day signal of 23 Nov, disp 08:15)', [
 ['07:30', 'OUT', 'Artigo', 'OJ-1 → OTB', '—', '11-22 07:30', 'sailing box: 07:30 (signal 07:20)'],
 ['09:54', 'IN', 'Ginga Cheetah', 'OTB → OJ-7', '—', '11-22 09:54', 'made fast 09:54, commenced 12:35 — board had ~08:00'],
 ['10:00', 'IN', 'Hafnia Ammolite', 'OTB → OJ-1', '—', '11-22 10:00', 'made fast 10:00, commenced 13:06 — board had ~09:20'],
 ['16:20', 'OUT', 'Orchids', 'OJ-6 → OTB', '—', '11-22 16:20', 'completed 12:48, left the berth 16:20 (signal 16:00)'],
 ['23:42', 'IN', 'Willows', 'OTB → OJ-6', '—', '11-22 23:42', 'made fast 23:42, commenced 01:42 on the 23rd'],
 ['02:40', 'OUT', 'PVT Aurora', 'OJ-2 → OTB', '—', '11-23 02:40', 'completed 22:40 on 22 Nov, left the berth 02:40 (signal 02:30)'],
 ['06:25', 'OUT', 'Bow Fortitude', 'OJ-4 → OTB', '—', '11-23 06:25', 'completed 03:00, left the berth 06:25 (signal 07:00)'],
 ['06:48', 'IN', 'Rasheeda', 'OTB → OJ-2', '—', '11-23 06:48', 'made fast 06:48 — board had ~04:30'],
 ['—', 'IN', 'Al Mahboobah', 'OTB → OJ-4', '—', '11-23 08:25', '"berthing today" on the list and the DPR — behind Bow Fortitude, about 08:25 est']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LM) + ",\n" + B.s[mm:]
B.s, k = re.subn(r"const LIQ=\{prog:'(?:[^'\\]|\\.)*',src:'(?:[^'\\]|\\.)*',asOf:'11-23 02:16',",
    lambda _: "const LIQ={prog:'" + q("LIST 23.11 / DPR 23.11 — OJ-2 Rasheeda made fast 23 Nov 06:48 behind PVT Aurora (left 02:40) · OJ-4 Al Mahboobah berthing today behind Bow Fortitude (left 06:25) · OJ-6 Willows made fast 22 Nov 23:42 · OJ-5 under maintenance · no oil-jetty row on the day signal of 23 Nov (disp 08:15)")
    + "',src:'DPA berthing list 23.11.26 (0700) · DPR 23.11 · programme 23.11 · signals to the day sheet of 23 Nov (disp 0815 — no oil-jetty row on it)',asOf:'11-23 11:06',", B.s, count=1)
assert k == 1

# ================= TUNA =================
def tuna(bid, text):
    a, b = B.line_of("  {b:'%s',n:" % bid); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(text + " ") + B.s[i:]
tuna('TT-3', D + ": 17,517 MT in 24 h — 74,517 off, 2,327 left → done about 10:15 on 23 Nov. " + L + ": \"[3]\" — sailing today; MP Postpanamax 1 is \"B'TODAY\" at TT-3 behind her.")
tuna('TT-2', D + ": 11,860 MT in 24 h — 22,260 loaded, 9,240 left → about 24 Nov 01:45 at this rate.")
a, b = B.line_of("  {b:'TT-1',n:'Europa Graeca'"); tail = ',' if B.s[a:b].endswith(',') else ''
B.s = B.s[:a] + "  " + js({'b': 'TT-1', 'n': 'Blue Ionian', 'c': 'Sugar in bulk', 'q': 73354.82, 'u': 'MT', 'ie': 'IMP', 'loa': 224.94, 'f': '11-23 01:00', 'ag': 'Interocean',
    'prev': 'Europa Graeca (sugar 75,677 MT) — DPR 23.11: completed 18:30, left the berth 22:36 on 22 Nov', 'next': 'nobody named',
    'note': D + ": MADE FAST 01:00, COMMENCED 06:30 on 23 Nov — 270 MT in the first half hour; 73,085 left. " + L + ": TT-1 · made fast 23 Nov 01:00 · no norm or ETC. She had waited since 2 Nov (ready 3 Nov 11:00). PROGRAMME 22.11: TT-01 — IN behind Europa Graeca."}) + tail + B.s[b:]
a = B.s.index("const TUNA={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); z0 = B.s.index("\n ]};", e0)
TW = ["  " + js({'n': 'MP Postpanamax 1', 'c': 'Coal in bulk', 'q': 88000, 'u': 'MT', 'ie': 'IMP', 'loa': 235, 'dr': 14.41, 'rep': '11-22 20:00', 'rdy': 'RDY', 'ag': 'Taurus', 'rem': L + ": reported / ready 22 Nov 20:00 · \"B'TODAY\" at TT-3 behind Marvelous Star (2,327 MT left at 0700) · 235 m, 14.41 m · PROGRAMME 23.11: TT-03 — IN, night berthing"}),
      "  " + js({'n': 'Sakizaya Star', 'c': 'US coal in bulk', 'q': 80010, 'u': 'MT', 'ie': 'IMP', 'loa': 229, 'dr': 14.46, 'rep': '11-23 03:42', 'rdy': 'RDY', 'ag': 'Benline', 'rem': L + ': NEW · reported / ready 23 Nov 03:42 · US coal 80,010 MT · 229 m, 14.46 m'})]
TE = ["  " + js({'n': 'RB Leah', 'c': 'Coal in bulk', 'q': 78263.1, 'u': 'MT', 'ie': 'IMP', 'loa': 229, 'eta': '11-24 23:00', 'ag': 'Atlantic Shg', 'rem': L + ' (ETA sheet): NEW · ETA 24 Nov 23:00 · N/A'})]
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(TW) + "\n ],\n eta:[\n" + ",\n".join(TE) + B.s[z0:]
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda _: "const TUNA={src:'" + q("DPA berthing list 23.11.26 (0700) · DPR 23.11 · programme 23.11 · TT-1 Blue Ionian made fast 23 Nov 01:00 · TT-3 MP Postpanamax 1 berthing today behind Marvelous Star · TT-4 vacant") + "',", B.s, count=1)
assert k == 1
B.rep(" {d:'11-21',b:{'TT-1':'Europa Graeca','TT-2':'Woohyun Dream','TT-3':'Marvelous Star','TT-4':''}}\n];",
      " {d:'11-21',b:{'TT-1':'Europa Graeca','TT-2':'Woohyun Dream','TT-3':'Marvelous Star','TT-4':''}},\n {d:'11-22',b:{'TT-1':'Europa Graeca','TT-2':'Woohyun Dream','TT-3':'Marvelous Star','TT-4':''}},\n {d:'11-23',b:{'TT-1':'Blue Ionian','TT-2':'Woohyun Dream','TT-3':'Marvelous Star','TT-4':''}}\n];")

# ================= TIMBER =================
def tnote(name, text, tag=D):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('ML Egret', "19,543 pcs / 6,811 CBM in 24 h on 12 hooks — 30,181 off, 12,704 left → about 25 Nov 03:45 at this rate · warped 2¼ panels north at 09:30 on 23 Nov (signal) to make room for Lila Tokyo at CJ-14")
tnote('Uni Blossom', "24,703 pcs / 8,020 CBM in 24 h on 12 hooks — 15,358 off, 19,511 left → about 25 Nov 17:20 at this rate")
tnote('Dariya Priya', "at midstream 4,700 pcs / 1,314 CBM in 24 h on 6 hooks — 3,662 off, 41,306 left · LIST 23.11: SGR 4 · 8K 9 · GEN 18")
tnote('AG Varvara', "SGR 1 · GEN 13 — still the senior vessel of the SAAGAR line", L)
tnote('CD Glory', "SGR 3 · 8K 8 · GEN 17", L)
tnote('African Tiger', "SGR 5 · 8K 10 · GEN 22", L)
tnote('Paiwan Ace', "ON THE WAITING SHEET (still printed \"PAIWAN ICE\") — reported 22 Nov 00:06, READINESS 22 Nov 11:00 · SGR 6 · 8K 12 · Sr No 7", L)
tnote('Erna Oldendorff', "still on the expected sheet — ETA / readiness 23 Nov 00:00 · SGR Y", L)
tnote('African Pheasant', "ON THE WAITING SHEET — reported 23 Nov 04:24, READINESS 23 Nov 11:00 · SGR Y · 8K Y", L)
B.rep("{n:'Paiwan Ace',cbm:36905,from:'Uruguay',c:'Pine logs',eta:'11-22 02:00',", "{n:'Paiwan Ace',cbm:36905,from:'Uruguay',c:'Pine logs',eta:'11-22 00:06',")
B.rep("{n:'African Pheasant',cbm:45282,from:'New Zealand',c:'Pine logs',eta:'11-24 00:00',", "{n:'African Pheasant',cbm:45282,from:'New Zealand',c:'Pine logs',eta:'11-23 04:24',")

# ================= MEETLOG — the 22 Nov meeting: the berth went to Lila Tokyo in the end =================
B.rep("call:[['Xin Hai Tong 71','14']],got:[['Hai Nam 81','14']],note:'Right berth, wrong vessel.",
      "call:[['Xin Hai Tong 71','14']],got:[['Lila Tokyo','14','signal']],note:'" + q("23 NOV: the programme's Hai Nam 81 did not berth — list 23.11 and the day signal of 23 Nov put LILA TOKYO (CSTL(30K), in 10:45) into CJ-14 and Hai Nam 81 back on the waiting sheet; the board's call was wrong either way. AS WRITTEN ON 22 NOV: ") + "Right berth, wrong vessel.")

# ================= LEARN =================
L1 = {'d': '23 Nov 11:06 · list 23.11 + HM signal 23 Nov (disp 08:15) — CJ-14 went to Lila Tokyo, not Hai Nam 81',
      'v': "The Coastal place at CJ-14 behind the tug Sagar 5 with barge.",
      'exp': "Programme 23.11 (meeting of 22 Nov): HAI NAM 81 — salt, 30K quote, \"CSTL(30K)\", provisional berthing — in about 19:30 on 23 Nov. The board followed the programme.",
      'act': "List 23.11 prints MV LILA TOKYO (GL) under COASTAL at CJ-14, 126–143½, \"CSTL(30K) B'TODAY\" (gypsum 72,633 MT, norm 30,000). Day signal of 23 Nov: Lila Tokyo IN 10:45 (Capt Omesh), the tug-and-barge RT OUT 11:00, ML Egret warped at 09:30 to make room. Hai Nam 81 is back on the waiting sheet — reported / ready 22 Nov 19:15, HP Y · 8K Y.",
      'why': "Not on the papers. Two readings: (1) Hai Nam 81's berthing was provisional because she had not arrived when the meeting sat (she reported 19:15, after it), and the place then went to the senior ready vessel on a 30K quote — Lila Tokyo, ready since 17 Nov, HP 2; (2) the port chose by seniority among the 30K quotes once Lila Tokyo asked for a clean berth. Either way the list remark naming her berths (\"CJ 7 & 8, 13-16\") was honoured — the board had held her to CJ-7 / 8. OPEN — Mihir to say why the vessel was changed.",
      'fix': "Lila Tokyo entered at CJ-14 from the signal; Hai Nam 81 returned to the waiting rows as printed. Not changed in the calculation yet: how firmly a \"provisional\" programme row is to be taken, and whether a list remark naming berths opens those berths to the vessel.",
      'st': 'open'}
L2 = {'d': '23 Nov 11:06 · list 23.11 — Sand Topic at CJ-9, a date slip',
      'v': "Sand Topic at CJ-9 (Gautam Freight berth).",
      'exp': "Night signal of 22 Nov: in \"o/c\" behind Yuan Hang Wei Ye (RT OUT 23:30) — about 01:30 on 23 Nov.",
      'act': "DPR 23.11: MADE FAST 02:45, COMMENCED 04:50 on 23 Nov; Yuan Hang Wei Ye left the berth 00:01. List 23.11 prints the same hours with the date 22 Nov and counts her ETC from it — 24 Nov 18:18.",
      'why': "A date slip on the list: at 02:45 on 22 Nov the berth was held by Yuan Hang Wei Ye. The DPR and the signal sheet agree on 23 Nov.",
      'fix': "Entered as 23 Nov 02:45; at the 20,000 norm her permissible time is then 25 Nov 18:18 — the list's 24 Nov 18:18 is a day early. No effect on the DPA queue.",
      'st': 'ok'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(L1) + ",\n " + js(L2) + ",\n")

B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='23 Nov 2026 · 11:20 IST';", B.s, count=1)
B.save()
