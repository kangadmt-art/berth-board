#!/usr/bin/env python3
# apply32a — v187 (part 1, data): Daily Berthing List 20.11 (0700) + DPR 20.11 (position 0700), received 20 Nov 10:36. No programme in this batch.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P, list_tag='LIST 20.11'); q = B.q
L = "LIST 20.11"; D = "DPR 20.11"
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
B.rep("const NOW=h('11-19 22:32');", "const NOW=h('11-20 10:36');")
B.rep("List <b>19.11 · 0700</b> · DPR <b>19.11</b> · Programme <b>20.11</b> · Signals to <b>19 Nov evening sheet (disp 1640, amended 1940)</b>",
      "List <b>20.11 · 0700</b> · DPR <b>20.11</b> · Programme <b>20.11</b> · Signals to <b>19 Nov evening sheet (disp 1640, amended 1940)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 20 Nov 10:36: Berthing List 20.11 (0700) and DPR 20.11 (position 0700). The night movements of 19 Nov now carry their actual hours from the DPR; today's programmed berthings (Belmoira, Ken Ann, Katerina K, ML Egret's shift) are still estimates — the signal sheets of 20 Nov and programme 21.11 are awaited · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='list 20.11 (0700) · DPR 20.11 (0700) · ")

# ================= V — actual hours (DPR 20.11) and the list's norms / ETCs =================
M = "{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]"
pre(M, D + ": MADE FAST 12:50, COMMENCED 17:45 on 19 Nov — rice bags 1,325 MT and wheat flour 500 MT by 0700 (21,175 + 3,700 left; the sugar-bag row is nil). " + L + ": BITUMEN · CJ-2 · 8½–16½ · rice / sugar bags 32,700 MT · no norm printed · ETC 30 NOV 13:50 (about 3,000 a day from commencement).")
sub(M, "f:'11-19 12:30',t:'11-28 10:00',est:1", "f:'11-19 12:50',t:'11-30 13:50'")
M = "{b:'2',n:'North Gate',nm:3000,p:[8.75,16.5]"
pre(M, D + ": 187 MT on the morning of 19 Nov, work stopped 09:00, LET GO 09:50, at OTB 12:05 — she left with 2,873 MT of her 27,000 still to load. " + L + ": back on the waiting sheet (\"REANCHORED AT OTB 1215/19.11.2026\", no rank) and printed under MS, working at midstream.")
sub(M, "t:'11-19 10:00'", "t:'11-19 09:50'")
M = "{b:'3',n:'Sea Gautham',p:[17.5,22.25]"
pre(M, D + ": COMMENCED 10:15 on 19 Nov, COMPLETED 02:30 on the 20th — 7,000 MT on 6 hooks. " + L + ": \"[3]\" — sailing today (programme 20.11: out 08:00).")
M = "{b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75]"
pre(M, D + ": 20,000 MT in 24 h on 15 hooks — 49,100 off, 5,818 left → cargo done about 14:00, an hour before her programmed sailing (15:00). " + L + ": \"[4]\" — sailing today.")
M = "{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]"
pre(M, D + ": 22,561 pcs / 7,863 CBM in 24 h on 12 hooks (norm 4,600) — 10,558 CBM off, 32,327 left. " + L + " already prints her at CJ-4 (23–31¾, \"S1\" from 143½–156¾) — today's shift, printed ahead.")
M = "{b:'4',n:'ML Egret',nm:4600,p:[23,31.75]"
pre(M, L + ": SAAGAR · CJ-4 · 23–31¾ · norm 4,600 · ETC 28 Nov 07:30 — printed at CJ-4 before the shift. At the " + D + " pace (7,863 CBM a day) her 32,327 CBM are done about 24 Nov, four days inside the ETC, less whatever the shift costs.")
M = "{b:'5',n:'Saga Viking',nm:3450,p:[32.75,41.5]"
pre(M, D + ": 2,031 units / 4,062 MT in 24 h — 15,542 off, only 496 MT left → cargo done in the morning; she shifts to OTB at 17:30 at her agent's request (programme 20.11). " + L + ": \"[5]\" · W1 33–41¾.")
M = "{b:'6',n:'Truong Minh Dream',nm:17193,p:[42.5,51.25]"
pre(M, D + ": 11,675 MT in 24 h — 54,400 off, 1,200 left → done about 09:30; programmed out 17:45. " + L + ": \"[6]\" — sailing today.")
M = "{b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75]"
pre(M, D + ": COMMENCED 08:40 on 19 Nov — 39,450 MT in her first 22⅓ h on 17 hooks (about 42,400 a day; the quote is 42,500); 21,050 left → about 19:00 on the 20th, on her list ETC (19:39).")
M = "{b:'8',n:'Vishva Bandhan',nm:9258,p:[59.5,68]"
pre(M, D + ": 10,860 MT in 24 h (norm 9,258) — 28,510 off, 15,488 left → about 21 Nov 17:15 at this rate; list ETC 22 Nov 14:33.")
M = "{b:'9',n:'Seacon Monaco',nm:20000,p:[69,76.75]"
pre(M, D + ": 14,169 MT in 24 h on 15 hooks against a norm of 20,000 — 27,054 off, 13,946 left → about 21 Nov 06:30 at this rate, 21 h past the list ETC (20 Nov 09:48). No outward row on programme 20.11.")
M = "{b:'13',n:'Rome Trader (salt, next call)',nm:26000,p:[113,125.25]"
pre(M, "MIHIR & COMPANY · " + L + ": SAAGAR · CJ-13 · 113–125¼ · NORM NOW 23,000 (26,000 on list 19.11) · ETC NOW 21 NOV 04:40 (was 20 Nov 22:01). " + D + ": 25,320 MT in 24 h on 12 hooks — 35,644 loaded, 19,631 left at 0700 on the 20th → about 21 Nov 01:30 at this rate, three hours inside the new ETC.")
sub(M, "f:'11-18 17:00',t:'11-20 22:01'", "f:'11-18 17:00',t:'11-21 04:40'")
sub(M, "nm:26000,p:[113,125.25]", "nm:23000,p:[113,125.25]")
M = "{b:'14',n:'Yara J',p:[126.5,141.75]"
pre(M, D + ": 5,517 MT on two shifts, work stopped 20:00 on 19 Nov, LET GO 01:00 on the 20th and SHIFTED TO OTB — 26,600 of 30,000 MT off, 3,400 MT still on board. Her 24 hours ended at 20:30. She is not on list 20.11.")
sub(M, "t:'11-19 23:30',lt:'11-19 20:30',x24:1", "t:'11-20 01:00',lt:'11-19 20:30',x24:1")
M = "{b:'14',n:'Nord Copper',p:[126.5,141.75]"
pre(M, L + ": COASTAL · CJ-14 · 126½–141¾ · MADE FAST 20 NOV 02:06 · NORM 23,000 · ETC 22 NOV 03:03. " + D + ": made fast 02:06, not commenced at 0700 (4 gangs on the third shift).")
sub(M, "f:'11-20 01:00',t:'11-21 21:00',est:1", "f:'11-20 02:06',t:'11-22 03:03'")
sub(M, "n:'Nord Copper',p:[126.5,141.75]", "n:'Nord Copper',nm:23000,p:[126.5,141.75]")
M = "{b:'15A',n:'Bristol (salt, next call)',nm:46000,p:[158.75,169]"
pre(M, D + ": COMPLETED 19:15, LET GO 20:40 on 19 Nov — 63,200 MT (12,978 on the last day).")
sub(M, "t:'11-19 20:30',lt:'11-19 08:28'", "t:'11-19 20:40',lt:'11-19 08:28'")
M = "{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]"
pre(M, D + ": MADE FAST 22:06 on 19 Nov, COMMENCED 01:10 on the 20th — 10 units / 332 MT by 0700, 46 units / 1,563 MT left. " + L + ": PROJECT/STEEL · CJ-15A · 161¾–169 · no norm or ETC. About 21 Nov evening is the board's estimate.")
sub(M, "f:'11-19 21:30',t:'11-21 21:30',est:1", "f:'11-19 22:06',t:'11-21 21:30',est:1")
M = "{b:'16',n:'HN Doris (salt, next call)',nm:46000,p:[171.25,188]"
pre(M, D + ": COMPLETED 15:30, LET GO 21:20 on 19 Nov — 39,633 MT on her last day; the sheet's total is 72,775 MT, balance nil.")
sub(M, "t:'11-19 21:00',lt:'11-19 14:19'", "t:'11-19 21:20',lt:'11-19 14:19'")
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[175,188]"
pre(M, L + ": printed under SAAGAR with the remark \"SGR(PROJ)\" · CJ-16 · 173½–188 · MADE FAST 20 NOV 00:30, COMMENCED 04:45 · no norm or ETC. " + D + ": I-beams / steel pipes 106 MT by 0700, 11,607 left. (Mihir, 19 Nov: Project priority in the absence of an HP vessel — the list's word for it is SGR(PROJ).)")
sub(M, "f:'11-19 23:30',t:'11-24 04:00',est:1", "f:'11-20 00:30',t:'11-24 04:00',est:1")
sub(M, "via:'Project priority · in the vacant Higher productivity place'", "via:'Project priority (list: SGR(PROJ)) · in the vacant Higher productivity place'")
sub(M, "p:[175,188]", "p:[173.5,188]")
M = "{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]"
pre(M, D + ": 7,619 MT in 24 h on 12 hooks (norm 6,500) — 21,506 loaded, 12,494 left → about 21 Nov 22:30 at this rate, 11½ h inside the list ETC (22 Nov 10:05).")
M = "{b:'15',n:'Belmoira',nm:30000,p:[143.5,156.75]"
pre(M, L + ": GOV row · CJ-15 · 143½–156¾ · norm 30,000 · \"GOVT(30K) B'TODAY\".")
M = "{b:'5',n:'Ken Ann',p:[33.5,41.5]"
pre(M, L + ": 24 HRS · CJ-5 · 33½–41½ · \"B'TODAY\".")
M = "{b:'6',n:'Katerina K',p:[42.5,51.25]"
pre(M, L + ": GENERAL · CJ-6 · 42½–51¼ · \"B'TODAY\" · the quantity is printed 27576.288/20600.")

# ================= name maps =================
B.rep("W.forEach(w=>{w.rep=REP[w.n]?h(REP[w.n]):w.rdy;});",
      "Object.assign(REP,{'True Mariner':'11-19 17:00','Josco Taicang':'11-20 00:00','Parvraj':'11-20 01:56','North Gate (re-berthing)':'10-10 07:15'}); // list 20.11 — placed last so that it wins\nW.forEach(w=>{w.rep=REP[w.n]?h(REP[w.n]):w.rdy;});")
B.rep("Object.assign(AG,{'African Hornbill':", "Object.assign(AG,{'North Gate (re-berthing)':'JM Baxi'});Object.assign(IE,{'North Gate (re-berthing)':'EXP'}); // list 20.11\nObject.assign(AG,{'African Hornbill':")
a, b = B.line_of("const ETA={'Parvraj':'11-20 03:00',")
B.s = B.s[:a] + ("const ETA={'Tai Keystone':'11-20 12:00','MSC Magali':'11-20 12:00','Manta Omer Mecit':'11-20 18:00','Hai Nam 81':'11-20 20:00','Gutian Trust':'11-21 00:00','Zheng Hui':'11-21 00:00',"
                 "'Hai Long 1':'11-21 00:00','Zheng Run':'11-21 00:00','Asian Summit':'11-21 04:00','Sanghi Sundarshan':'11-21 11:00','Sand Topic':'11-21 23:00','Lolo Gate':'11-22 00:00','Valentina Sea':'11-22 00:00','Princess Manissa':'11-22 00:00',"
                 "'Outlander':'11-23 00:00','KSS Edmond':'11-24 00:00','Kang Qi Fu Hua':'11-24 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 20.11 — Parvraj, Josco Taicang and True Mariner have reported") + B.s[b:]

# ================= W — list 20.11 =================
w = B.wrow
w('Safi Alfa', "GEN 1 · remark \"(24750 – balance) 32100 MT – total\"", rk="GEN:1", qty=24750)
w('Blue Shark', "RANKED NOW — GEN 2 · ready 19 Nov 11:00 · 26,500 MT", rk="GEN:2", qty=26500)
w('Fortunelit', "GEN 3 · working at MS", rk="GEN:3")
w('Crystal O', "GEN 4 · working at MS", rk="GEN:4")
w('Manta Sena', "READINESS DECLARED 20 Nov 11:00 · 8K 1 · GEN 5", rk="'8K':1,GEN:5", rdy="11-20 11:00")
w('Crystal Land', "8K 1 printed again (Manta Sena, senior by reporting, is also printed 8K 1 — the sheet was not renumbered) · GEN 6", rk="'8K':1,GEN:6")
w('Libra', "GEN 7 · DOCS NR (3,000 MT pending) · working at MS", rk="GEN:7")
w('Pioneer Fortune', "8K 2 · GEN 8 · Sr No 7", rk="'8K':2,GEN:8")
w('MK Lamis', "GEN 9 · CJ-01 TO 04 · DOC NR · 11,500 MT", rk="GEN:9", qty=11500)
w('Uni Blossom', "SGR 1 · 8K 3 · GEN 10 · Sr No 7", rk="SAAGAR:1,'8K':3,GEN:10")
w('Ariston Bulker', "GEN 11 · working at MS", rk="GEN:11")
w('Aboudi D', "GEN 12 · 2 SHORE CRANE REQ", rk="GEN:12")
w('African Loon', "GEN 13 printed · STS transhipment, working at MS — still held", rk="GEN:13", rdy="")
w('Tan Bin 259', "8K 4 · GEN 14 · Sr No 7 · working at MRG 3", rk="'8K':4,GEN:14")
w('Gokova-M', "HP 1 · 24H 1 · 8K 5 · GEN 15", rk="HP:1,'24H':1,'8K':5,GEN:15")
w('AG Varvara', "SGR 3 · GEN 16 · Sr No 7", rk="SAAGAR:3,GEN:16")
w('Xin Hai Tong 71', "SGR 4 · STL 1 · GEN 17 (STL kept out — Mihir, 15 Nov)", rk="SAAGAR:4,GEN:17")
w('Porto Fiscardo', "8K 6 · GEN 18", rk="'8K':6,GEN:18")
w('Captainannis L', "8K Y · GEN 19 — ranked in General now · DOC NR · working at MS", rk="'8K':98,GEN:19")
w('CD Glory', "SGR 5 · 8K 8 · GEN 20 · Sr No 7 — unchanged; one more vessel stands ahead of her in the 6.5K / 8K line (Manta Sena, ready today)", rk="SAAGAR:5,'8K':8,GEN:20")
w('Dariya Priya', "SGR 6 · 8K 10 · GEN 21 · Sr No 7", rk="SAAGAR:6,'8K':10,GEN:21")
w('Sea Postman', "GEN 22 (no Govt rank printed)", rk="GEN:22")
w('Sheng Tai', "GEN 23 printed · daughter vessel, working at MS (STS) — still held", rk="GEN:23", rdy="")
w('Lila Tokyo', "HP 4 · GEN 24 · 30K/25K/10K Sr No 7 · remark now: CJ 7 & 8 or the clean berths", rk="HP:4,GEN:24")
w('African Tiger', "SGR 7 · 8K 12 · GEN 25 · Sr No 7", rk="SAAGAR:7,'8K':12,GEN:25")
w('Flag Marina', "HP 5 · SGR 8 · 24H 3 · GEN 26", rk="HP:5,SAAGAR:8,'24H':3,GEN:26")
w('Ocean Kudos', "the sheet still prints HP X · 8K X · GEN X and \"B\\'TODAY\" — the print of her cancelled movement (programme 19.11, CJ-16); no clean berth is free for her today. STILL HELD until Mihir or a signal says her holds are passed")
w('Yuan Hang Wei Ye (next call)', "HP Y · 8K Y · GEN 27 — ranked in General now · 30K/25K/10K Sr No 7 · transhipment", rk="HP:98,'8K':98,GEN:27")
w('True Mariner', "REPORTED 19 Nov 17:00 · N/A")
w('Josco Taicang', "REPORTED 20 Nov 00:00 · N/A · project cargo 1,969 MT (389 pkg) + CR steel coils 13,455 MT (1,061 pkg) · 11.6 m", dr=11.6)
w('Parvraj', "REPORTED / READY 20 Nov 01:56 · GP Y · GEN 28", rk="GEN:28", rdy="11-20 01:56")
m = B._row('Parvraj').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['North Gate (re-berthing)','Chick peas & rice in jumbo bags',2873,'MT',177.13,6.2,null,{},'" + q("LIST 20.11: BACK ON THE WAITING SHEET — \"REANCHORED AT OTB 1215/19.11.2026\" · readiness 7 Nov 11:00 printed, NO group rank · also printed under MS, working at midstream. DPR 20.11: at CJ-2 she loaded 187 MT on 19 Nov, work stopped 09:00, let go 09:50 — 2,873 MT of 27,000 still to load. HELD out of the projection while no rank is printed (she is finishing by barge) · agent JM Baxi") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
B.rep(" // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 19.11 (0700)", " // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 20.11 (0700)")

# ================= DPR block =================
def R(loc, n, ie, c, l24, upto, bal, g, hk, note, comm=None):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if comm: d['partial'] = 1; d['comm'] = comm
    d['note'] = note; return d
ROWS = [
 R('CJ-1', 'New Bliss', 'EXP', 'Sugar bags', 7619, 21506, 12494, '4/4/4', 12, '7,619 MT in 24 h on 12 hooks (norm 6,500) — 12,494 left → ~21 Nov 22:30 at this rate, 11½ h inside the list ETC (22 Nov 10:05)'),
 R('CJ-2', 'North Gate', 'EXP', 'Chick peas / rice J-bags', 187, 24127, 2873, '2/0/0', 2, '187 MT, work stopped 09:00, LET GO 09:50 on 19 Nov, at OTB 12:05 — 2,873 MT not loaded; the sheet also carries her under MS (no work, 3,060 left there)'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour', 1825, 1825, 24875, '1/3/3', 7, 'MADE FAST 12:50, COMMENCED 17:45 on 19 Nov — rice bags 1,325 MT + wheat flour 500 MT by 0700; 21,175 + 3,700 left (the sugar-bag row is nil; the list counts 32,700 MT in all)', comm='11-19 17:45'),
 R('CJ-3', 'Sea Gautham', 'EXP', 'Ammonium sulphate', 7000, 7000, 0, '2/2/2', 6, 'COMMENCED 10:15 on 19 Nov, COMPLETED 02:30 on the 20th — 7,000 MT'),
 R('CJ-4', 'Propel Confidence', 'IMP', 'Iron ore pellets', 20000, 49100, 5818, '5/5/5', 15, '20,000 MT in 24 h — 5,818 left → ~14:00 on the 20th at this rate (programmed out 15:00)'),
 R('CJ-5', 'Saga Viking', 'IMP', 'Kraft pulp', 4062, 15542, 496, '2/2/2', 6, '4,062 MT / 2,031 units in 24 h — 496 MT left → done in the morning; to OTB at 17:30 (programme 20.11)'),
 R('CJ-6', 'Truong Minh Dream', 'IMP', 'DAP / TSP bulk', 11675, 54400, 1200, '4/4/4', 12, '11,675 MT in 24 h — 1,200 left → ~09:30 on the 20th (programmed out 17:45)'),
 R('CJ-7', 'Meghna Prestige', 'IMP', 'Coal in bulk', 39450, 39450, 21050, '5/6/6', 17, 'COMMENCED 08:40 on 19 Nov — 39,450 MT in 22⅓ h on 17 hooks (about 42,400 a day; quote 42,500); 21,050 left → ~19:00 on the 20th (list ETC 19:39)', comm='11-19 08:40'),
 R('CJ-8', 'Vishva Bandhan', 'IMP', 'Urea bulk', 10860, 28510, 15488, '4/4/4', 12, '10,860 MT in 24 h (norm 9,258) — 15,488 left → ~21 Nov 17:15 at this rate (list ETC 22 Nov 14:33)'),
 R('CJ-9', 'Seacon Monaco', 'IMP', 'Soda ash in bulk', 14169, 27054, 13946, '5/5/5', 15, '14,169 MT in 24 h against a norm of 20,000 — 13,946 left → ~21 Nov 06:30 at this rate (list ETC 20 Nov 09:48)'),
 R('CJ-13', 'Rome Trader (salt, next call)', 'EXP', 'Salt in bulk', 25320, 35644, 19631, '4/4/4', 12, '25,320 MT in 24 h on 12 hooks (list norm now 23,000) — 35,644 loaded, 19,631 left → ~21 Nov 01:30 at this rate, 3 h inside the list ETC (21 Nov 04:40) · agent and stevedore Mihir'),
 R('CJ-14', 'Yara J', 'IMP', 'Rice bags', 5517, 26600, 3400, '3/3/0', 6, '5,517 MT on two shifts, work stopped 20:00 on 19 Nov, LET GO 01:00 on the 20th — shifted to OTB with 3,400 of 30,000 MT still on board'),
 R('CJ-14', 'Nord Copper', 'EXP', 'Salt in bulk', 0, 0, 45000, '0/0/4', 4, 'MADE FAST 02:06 on 20 Nov, not commenced at 0700'),
 R('CJ-15', 'ML Egret', 'IMP', 'Pine logs', 7863, 10558, 32327, '4/4/4', 12, '22,561 pcs / 7,863 CBM in 24 h on 12 hooks (norm 4,600) — 10,558 CBM off, 32,327 left → ~24 Nov 09:30 at this rate; she is shifted to CJ-4 today'),
 R('CJ-15A', 'Bristol (salt, next call)', 'EXP', 'Salt bulk', 12978, 63200, 0, '5/5/0', 10, 'COMPLETED 19:15, LET GO 20:40 on 19 Nov — 63,200 MT'),
 R('CJ-15A', 'Heng Yuan Fa Zhan', 'IMP', 'Windmill blades & accessories', 332, 332, 1563, '0/0/2', 2, 'MADE FAST 22:06 on 19 Nov, COMMENCED 01:10 on the 20th — 10 units / 332 MT; 46 units / 1,563 MT left', comm='11-20 01:10'),
 R('CJ-16', 'HN Doris (salt, next call)', 'EXP', 'Salt bulk', 39633, 72775, 0, '3/1/0', 4, 'COMPLETED 15:30, LET GO 21:20 on 19 Nov — 39,633 MT on the last day; 72,775 MT in all on the sheet'),
 R('CJ-16', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes', 106, 106, 11607, '0/0/3', 3, 'MADE FAST 00:30, COMMENCED 04:45 on 20 Nov — 106 MT by 0700; 11,607 left', comm='11-20 04:45'),
 R('MS', 'Stalo', 'IMP', 'Coal in bulk', 3886, 43400, 0, '', 0, 'COMPLETED 17:10 on 19 Nov at midstream — 43,400 MT; let go'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 2000, 5215, 52535, '1/1/1', 3, 'mother vessel — ship-to-ship to Sheng Tai (daughter) at anchorage: 2,000 MT in the 24 h, 52,535 left'),
 R('MS', 'Libra', 'EXP', 'Rice bags', 1400, 13597, 9403, '1/1/0', 2, '1,400 MT in 24 h (another 2,170 at IFFCO) — 9,403 left'),
 R('MS', 'Crystal O', 'EXP', 'Sugar bags', 847, 16232, 14968, '1/1/1', 3, '847 MT in 24 h — 14,968 left'),
 R('MS', 'Fortunelit', 'EXP', 'Sugar / rice bags', 0, 18850, 3650, '', 0, 'no work in the 24 h — rice 6,350 MT done, 3,650 left; sugar complete (12,500 MT)'),
 R('MS', 'MAK 1', 'EXP', 'Rice in J-bags', 0, 21088, 800, '', 0, 'no work for the second day — 800 MT left'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 1403, 3151, 14649, '1/1/1', 3, '1,403 MT in 24 h — 14,649 left'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '1/0/0', 1, 'no cargo in the 24 h (one gang on the first shift) — 4,470 left'),
 R('MRG-3', 'Tan Bin 259', 'EXP', 'NPK in jumbo bags', 1428, 8370, 3967, '2/2/2', 6, '1,428 MT in 24 h — 3,967 left → ~3 days'),
 R('BA', 'Bon Voyage', 'IMP', 'Steel slab', 839, 2173, 0, '1/0/0', 1, 'COMPLETED 12:45 on 19 Nov at the barge berth — 88 slabs / 2,173 MT; let go'),
 R('OJ-1', 'Artigo', 'IMP', 'CPO', 3611, 3611, 20389, '', 0, 'MADE FAST 20:06, commenced 23:06 on 19 Nov — 3,611 MT in 8 h; 20,389 left', comm='11-19 23:06'),
 R('OJ-2', 'Jeil Crystal', 'IMP', 'Chemicals', 6100, 6100, 535, '', 0, 'MADE FAST 12:00, commenced 14:10 on 19 Nov — chemicals 6,100 MT off, 535 left; base oil 1,986 MT still to load', comm='11-19 14:10'),
 R('OJ-3', 'Jag Pushpa', 'IMP', 'CDSBO', 13400, 40100, 4155, '', 0, '13,400 MT in 24 h — 40,100 off, 4,155 left → ~14:30 on the 20th (programmed out 13:00)'),
 R('OJ-4', 'Avyaan', 'IMP', 'HSD', 3455, 35000, 0, '', 0, 'COMPLETED 12:06, LET GO 14:20 on 19 Nov — 35,000 MT'),
 R('OJ-4', 'Bow Endeavour', 'IMP', 'Chemicals', 5385, 5385, 7662, '', 0, 'MADE FAST 16:42, commenced 19:18 on 19 Nov — 5,385 MT in 11¾ h; 7,662 left', comm='11-19 19:18'),
 R('OJ-6', 'Kestrel', 'EXP', 'VLSFO', 15415, 23000, 1000, '', 0, '15,415 MT loaded in 24 h — 1,000 left; programmed out 11:00 on the 20th'),
 R('OJ-7', 'NV Sunshine', 'IMP', 'Propane', 13758, 24000, 0, '', 0, 'COMPLETED 22:48 on 19 Nov, LET GO 02:35 on the 20th — 24,000 MT'),
 R('OJ-7', 'Silver Gertrude', 'IMP', 'CDSBO', 0, 0, 22500, '', 0, '"UNDER BERTHING" at 0700 on 20 Nov'),
 R('TT-1', 'Europa Graeca', 'IMP', 'Sugar bulk', 11196, 57584, 18093, '', 0, '11,196 MT in 24 h — 18,093 left → ~21 Nov 21:45 at this rate'),
 R('TT-3', 'Beagle', 'IMP', 'Coal in bulk', 14525, 77220, 0, '', 0, 'COMPLETED 18:00, LET GO 20:40 on 19 Nov — 77,220 MT'),
 R('TT-3', 'Marvelous Star', 'IMP', 'Coal in bulk', 6505, 6505, 70339, '', 0, 'MADE FAST 22:36 on 19 Nov, commenced 01:40 on the 20th — 6,505 MT by 0700; the DPR balance is 70,339 MT (76,844 in all) though the list prints 50,000', comm='11-20 01:40'),
]
a = B.s.index("const DPR={d:'19.11.2026'"); b = B.s.index("\n ]};", a) + len("\n ]};")
B.s = B.s[:a] + ("const DPR={d:'20.11.2026',asOf:'11-20 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 20 Nov (xlsx from Mihir, 20 Nov 10:36)',\n"
 " tot:{dry:215133,dryL:98366,dryU:116767,ms:10392,kict:2084,tuna:32226,oj:61124,vad:85496,all:406455,gangs:'PR 20 · 37 + 12 W gangs demanded / 37 + 12 W supplied',rakes:'3',wb:651,sail:'Searay · OJ-1 · 08:35 · Korea Chemi · OJ-2 · 11:00'},\n"
 " // partial:1 = the vessel worked only part of the 24 h — the rate is understated, the projection does not use it; comm = commencement inside the window\n"
 " rows:[\n  " + ",\n  ".join(js(x) for x in ROWS) + "\n ]};") + B.s[b:]

# ================= MSWORK — barge day from DPR 20.11 =================
day = open(W + 'in20/mswork20.txt', encoding='utf-8').read().rstrip('\n')
tail = "st:'INAYAT'}\n  ]},"
assert day.endswith(tail), day[-60:]
day = day[:-len("\n  ]},")] + ",\n   {n:'North Gate',ie:'EXP',c:'Chick peas / rice J-bags',loc:'MS',l24:0,upto:23940,bal:3060,shore:'',ag:'J M Baxi',st:'J M BAXI'}\n  ]},"
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + day + "\n")

# ================= TUNA =================
a, b = B.line_of("  {b:'TT-3',n:'Beagle',c:'Coal in bulk',q:77220,")
B.s = B.s[:a] + "  " + js({'b': 'TT-3', 'n': 'Marvelous Star', 'c': 'Coal in bulk', 'q': 50000, 'u': 'MT', 'ie': 'IMP', 'loa': 229, 'f': '11-19 22:36', 'ag': 'Atlantic Shg',
    'prev': 'Beagle (coal 77,220 MT) — DPR 20.11: completed 18:00, let go 20:40 on 19 Nov',
    'next': 'nobody named — MP Postpanamax 1 (coal 88,000 MT) is expected on 24 Nov',
    'note': 'DPR 20.11: MADE FAST 22:36 on 19 Nov, commenced 01:40 on the 20th — 6,505 MT by 0700. The DPR balance is 70,339 MT (76,844 MT in all); list 20.11 prints 50,000 MT — the two sheets differ. LIST 20.11: TT-3 · made fast 19 Nov 22:36 · no norm or ETC. Programme 20.11: night berthing behind Beagle.'}) + "," + B.s[b:]
B.rep("note:'DPR 19.11: 11,394 MT in 24 h (12,704 and 13,090 the two days before), 46,388 of 75,677 off, 29,289 left → about 21 Nov 20:30 at this rate.",
      "note:'DPR 20.11: 11,196 MT in 24 h, 57,584 of 75,677 off, 18,093 left → about 21 Nov 21:45 at this rate. DPR 19.11: 11,394 MT in 24 h (12,704 and 13,090 the two days before), 29,289 left.")
a, b = B.line_of("  {n:'Marvelous Star',c:'Coal in bulk',q:50000,u:'MT',ie:'IMP',loa:229,dr:null,rep:'11-15 13:18',")
B.s = B.s[:a - 1] + B.s[b:]          # drop the row and the line break before it
B.rep("rem:'TT-01 · ready 3 Nov 11:00 — behind Europa Graeca (about 21 Nov evening at the DPR pace)'},\n ],", "rem:'TT-01 · ready 3 Nov 11:00 — behind Europa Graeca (about 21 Nov night at the DPR 20.11 pace)'}\n ],")
B.rep("eta:'11-21 00:00',ag:'Taurus',rem:'new on list 18.11'}", "eta:'11-21 00:00',ag:'Taurus',rem:'list 20.11: ETA / readiness 21 Nov'}")
B.rep("const TUNA={src:'DPA berthing list 19.11.26 (0700) · programme 20.11 (TT-03: Beagle out, Marvelous Star in) · DPR 19.11 · TT-2 and TT-4 vacant'",
      "const TUNA={src:'DPA berthing list 20.11.26 (0700) · DPR 20.11 · programme 20.11 (TT-03: Beagle out, Marvelous Star in) · TT-2 and TT-4 vacant'")
B.rep(" {d:'11-19',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Beagle','TT-4':''}}\n];",
      " {d:'11-19',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Beagle','TT-4':''}},\n {d:'11-20',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Marvelous Star','TT-4':''}}\n];")

# ================= TIMBER =================
def T(pfx, d): B.set_line(pfx, " " + js(d) + ",")
T(" {n:'ML Egret',cbm:42886,", {'n': 'ML Egret', 'cbm': 42886, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-06 14:24', 'etb': '11-18', 'comm': '11-18 23:35',
   'note': 'berthed 18 Nov 21:45 at CJ-15 under SAAGAR · DPR 20.11: 22,561 pcs / 7,863 CBM in 24 h — 10,558 off, 32,327 left · list 20.11: norm 4,600 CBM, ETC 28 Nov 07:30, already printed at CJ-4 (23–31¾) — she is SHIFTED there today on the port\'s account (programme 20.11) · 12.11 m'})
T(" {n:'Uni Blossom',cbm:34870,", {'n': 'Uni Blossom', 'cbm': 34870, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-09 11:36', 'etb': '11-19',
   'note': 'SGR 1 · 8K 3 · GEN 10 on list 20.11 — next for a SAAGAR place when Rome Trader is through (list ETC now 21 Nov 04:40; DPR pace about 01:30) · the desk had 19 Nov · 10.8 m'})
T(" {n:'AG Varvara',cbm:39113,", {'n': 'AG Varvara', 'cbm': 39113, 'from': 'Australia', 'c': 'Pine logs', 'eta': '11-12 07:06', 'etb': '11-24', 'note': 'SGR 3 · GEN 16 on list 20.11 · 199.99 m, 9.0 m'})
T(" {n:'CD Glory',cbm:29158,", {'n': 'CD Glory', 'cbm': 29158, 'from': 'Malaysia', 'c': 'Hardwood logs', 'eta': '11-15 06:42', 'etb': '11-25',
   'note': 'list 20.11: SGR 5 · 8K 8 · GEN 20 — unchanged · 179.9 m, 10.4 m — fits CJ-1, CJ-4, CJ-5; CJ-4 goes to ML Egret today'})
T(" {n:'Dariya Priya',cbm:44968,", {'n': 'Dariya Priya', 'cbm': 44968, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-16 09:00', 'etb': '11-29',
   'note': '"Darya Priya" on the desk sheet · list 20.11: SGR 6 · 8K 10 · GEN 21 · 11.0 m'})
T(" {n:'African Tiger',cbm:36328,", {'n': 'African Tiger', 'cbm': 36328, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-18 06:30', 'etb': '12-03',
   'note': 'list 20.11: SGR 7 · 8K 12 · GEN 25 · reported 18 Nov 06:30 · 180 m, 10.8 m'})

# ================= MV — actual hours from DPR 20.11 =================
MVN = ['DPR 20.11 (position 0700, 20 Nov) and list 20.11 — actual hours of 19 Nov and the night, cargo jetties', [
  ['09:50', 'OUT', 'North Gate', 'CJ-2 → OTB', '—', '11-19 09:50', 'work stopped 09:00, let go 09:50, at OTB 12:05 — 2,873 MT not loaded (signal: OUT 10:00)'],
  ['12:50', 'IN', 'DSM London', 'OTB → CJ-2 · 8½–16½', '—', '11-19 12:50', 'made fast 12:50, commenced 17:45'],
  ['20:40', 'OUT', 'Bristol (salt, next call)', 'CJ-15A', '—', '11-19 20:40', 'completed 19:15, let go 20:40 (signal: RT OUT 20:30)'],
  ['21:20', 'OUT', 'HN Doris (salt, next call)', 'CJ-16', '—', '11-19 21:20', 'completed 15:30, let go 21:20 — 72,775 MT on the sheet (signal: RT OUT o/c)'],
  ['22:06', 'IN', 'Heng Yuan Fa Zhan', 'OTB → CJ-15A · 161¾–169', '—', '11-19 22:06', 'made fast 22:06, commenced 01:10 on the 20th (signal: IN 18:45)'],
  ['00:30', 'IN', 'African Hornbill (blades, next call)', 'OTB → CJ-16 · 173½–188', '—', '11-20 00:30', 'made fast 00:30, commenced 04:45 (signal: IN 21:30) — list: SGR(PROJ)'],
  ['01:00', 'SHIFT', 'Yara J', 'CJ-14 → OTB', '—', '11-20 01:00', 'work stopped 20:00 on the 19th, let go 01:00 — 3,400 MT still on board (programme: out 23:30)'],
  ['02:06', 'IN', 'Nord Copper', 'OTB → CJ-14 · 126½–141¾ · CSTL', '—', '11-20 02:06', 'made fast 02:06, not commenced at 0700 (signal: IN 22:30)'],
  ['02:30', '—', 'Sea Gautham', 'CJ-3 · completed', '—', '11-20 02:30', 'commenced 10:15 on the 19th, completed 02:30 — 7,000 MT; programmed out 08:00']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
B.save()
