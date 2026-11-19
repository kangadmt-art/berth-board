#!/usr/bin/env python3
# apply21a — v175 (part 1, data): Daily Berthing List 19.11 (0700) + Programme for 20.11 (TF/SH/2102, dated 19 Nov), received 19 Nov 16:12.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v174.html')
B = Board(P, list_tag='LIST 19.11'); q = B.q
L = "LIST 19.11"; PG = "PROGRAMME 20.11 (TF/SH/2102, dated 19 Nov)"
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
def add(marker, b, n, p, c, qty, u, cat, f, t, note, nm=None, est=False, extra=''):
    B.add_after(marker, " {b:'%s',n:'%s',%sp:[%s,%s],c:'%s',q:%s,u:'%s',cat:'%s',%sf:'%s',t:'%s',%snote:'%s'},\n" % (
        b, q(n), ("nm:%d," % nm) if nm else '', p[0], p[1], q(c), qty, u, cat, extra, f, t, 'est:1,' if est else '', q(note)))

# ================= HEADER =================
B.rep("const NOW=h('11-19 12:29');", "const NOW=h('11-19 16:12');")
a, b = B.line_of("const PROG_END=h('11-19 22:30');")
B.s = B.s[:a] + "const PROG_END=h('11-20 18:00'); // programme 20.11 (meeting of 19 Nov) covers till here — barge windows end here; beyond it no data" + B.s[b:]
B.rep("List <b>18.11 · 0700, revised</b> · DPR <b>19.11</b> · Programme <b>19.11</b> · Signals to <b>19 Nov day sheet (disp 1040)</b>",
      "List <b>19.11 · 0700</b> · DPR <b>19.11</b> · Programme <b>20.11</b> · Signals to <b>19 Nov day sheet (disp 1040)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 19 Nov 16:12: Berthing List 19.11 (0700) and Programme for 20.11 (TF/SH/2102, dated 19 Nov). The afternoon movements of 19 Nov are still as signalled, not confirmed — the evening sheet of 19 Nov and DPR 20.11 are awaited · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='list 19.11 (0700) · programme 20.11 (TF/SH/2102) · ")
B.rep("'Bristol (salt, next call)','HN Doris (salt, next call)','Theometor','Rahma','African Peacock','Enshi','Propel Confidence']);",
      "'Bristol (salt, next call)','HN Doris (salt, next call)','Theometor','Rahma','African Peacock','Enshi','Propel Confidence','Sea Gautham','Saga Viking','Truong Minh Dream','Yara J','ML Egret']);")

# ================= V =================
# CJ-3
M = "{b:'3',n:'Sea Gautham',p:[17.5,22.25]"
pre(M, PG + ": CJ-03 · outward readiness 20 Nov 08:00 (4.9 m) — nobody is named behind her. " + L + ": OTHERS · CJ-3 · 17½–22¼ · \"SPACE A/C\" · made fast 19 Nov 05:40 · no norm or ETC.")
sub(M, "f:'11-19 05:40',t:'11-21 05:40',est:1", "f:'11-19 05:40',t:'11-20 08:00'")
# CJ-4 — Propel out, ML Egret shifted in from CJ-15
M = "{b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75]"
pre(M, PG + ": CJ-04 · outward readiness 20 Nov 15:00 (6.4 m) → ML EGRET shifted in from CJ-15. " + L + ": COASTAL · CJ-4 · 23½–31¾ · norm 21,160 · ETC 20 Nov 11:47.")
sub(M, "f:'11-19 05:00',t:'11-20 11:47'", "f:'11-19 05:00',t:'11-20 15:00',lt:'11-20 11:47'")
M = "{b:'15',n:'ML Egret',nm:3450,p:[143.5,156.75]"
pre(M, PG + ": \"MV ML EGRET · 23–31¾ · SHIFT FROM CJ-15 TO CJ-04. PORT C.\" — she is moved to CJ-4 on the port's account once Propel Confidence has sailed (15:00), and CJ-15 goes to Belmoira. About 16:00 off this berth is the board's estimate. " + L + ": SAAGAR · CJ-15 · norm 4,600 · ETC 28 Nov 07:30.")
sub(M, "f:'11-18 21:45',t:'12-01 09:55',est:1", "f:'11-18 21:45',t:'11-20 16:00',est:1")
sub(M, "nm:3450,p:[143.5,156.75]", "nm:4600,p:[143.5,156.75]")
M = "{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]"
add(M, '15', 'Belmoira', (143.5, 156.75), 'Salt in bulk', 58300, 'MT', 'GOV', '11-20 18:30', '11-22 19:00',
    PG + ": CJ-15 · 143½–156¾ · category \"GOVT(30K)\" · sailing draught 13 m — a Sr No 7 vessel (30,000 MTPD quote) put in a Govt place: Truong Minh Dream leaves hers at 17:45 on the 20th. The berth is made for her by shifting ML Egret to CJ-4 on the port's account. About 18:30 alongside is the board's estimate (after Propel Confidence 15:00 → ML Egret's shift). " + L + ": HP 3 · 8K 11 · GEN 22 · 30K/25K/10K Sr No 7 · reported / ready 16 Nov 17:30 · salt in bulk 58,300 MT EXP. 58,300 MT at 30,000 a day is 47 h of work → about 22 Nov 19:00, the board's estimate.",
    nm=30000, est=True, extra="via:'30k/25k quote (Sr No 7)',")
add(M, '4', 'ML Egret', (23, 31.75), 'JAS pine logs', 42885, 'CBM', 'SAAGAR', '11-20 17:30', '11-28 07:30',
    PG + ": 23–31¾ · \"SHIFT FROM CJ-15 TO CJ-04. PORT C.\" — behind Propel Confidence (out 15:00); about 17:30 alongside is the board's estimate. " + L + ": SAAGAR · norm 4,600 · ETC 28 Nov 07:30 (printed for CJ-15; the shift is on the port's account). She keeps the SAAGAR log place — and takes CJ-4, one of the three berths a log vessel under 6.5K or General could have used.",
    nm=4600, est=True)
# CJ-5
M = "{b:'5',n:'Saga Viking',nm:3450,p:[32.75,41.5]"
pre(M, PG + ": CJ-05 · outward readiness 20 Nov 17:30 (6.4 m) · \"SHIFTING FROM CJ-05 TO OTB. AGENT'S REQ.\" → Ken Ann. " + L + ": GENERAL · CJ-5 · 32¾–41½ · ETC 21 Nov 18:58 — she leaves a day inside it.")
sub(M, "f:'11-17 01:24',t:'11-21 18:58'", "f:'11-17 01:24',t:'11-20 17:30',lt:'11-21 18:58'")
add(M, '5', 'Ken Ann', (33.5, 41.5), 'Steel / general cargo', 5022, 'MT', '24H', '11-20 19:30', '11-21 19:30',
    PG + ": CJ-05 · 33½–41½ · 24HRS — behind Saga Viking (17:30); about 19:30 alongside is the board's estimate. " + L + ": 24H 2 · STL 2 · GEN 23 · reported / ready 16 Nov 23:35 · steel general cargo 5,021.7 MT IMP. A 24-hr berth: out within 24 h of berthing.",
    est=True)
# CJ-6
M = "{b:'6',n:'Truong Minh Dream',nm:17193,p:[42.5,51.25]"
pre(M, PG + ": CJ-06 · outward readiness 20 Nov 17:45 (7.5 m) → Katerina K, \"PROVISIONAL BERTHING\". " + L + ": GOV · CJ-6 · 42½–51¼ · ETC 19 Nov 13:46 — she lies 28 h past it.")
sub(M, "f:'11-17 16:00',t:'11-19 13:46'", "f:'11-17 16:00',t:'11-20 17:45',lt:'11-19 13:46'")
add(M, '6', 'Katerina K', (42.5, 51.25), 'Kaolin / clay / bentonite in J-bags', 29636, 'MT', 'GEN', '11-20 19:45', '11-29 10:00',
    PG + ": CJ-06 · 42½–51¼ · \"PROVISIONAL BERTHING\" — behind Truong Minh Dream (17:45); about 19:45 alongside is the board's estimate. Provisional: she holds the berth until a vessel with a claim on it is ready (CJ-6 is where the Govt fertiliser vessels work). " + L + ": GEN 7 · reported 5 Nov 14:00, ready 16 Nov 11:00 · 27,576 + 2,060 MT EXP, 22,150 MT of it in jumbo bags. No norm printed: 29,636 MT at 3,450 a day → about 29 Nov, the board's estimate.",
    est=True)
# CJ-7
M = "{b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75]"
pre(M, L + ": HP · CJ-7 · 52¼–58¾ · made fast 19 Nov 07:30 · norm 42,500 · ETC 20 Nov 19:39. No outward row on programme 20.11 — the ETC falls after its window.")
sub(M, "f:'11-19 07:30',t:'11-20 19:30',est:1", "f:'11-19 07:30',t:'11-20 19:39'")
# CJ-13 — Rome Trader: norm and ETC are printed now
M = "{b:'13',n:'Rome Trader (salt, next call)',p:[113,125.25]"
pre(M, "MIHIR & COMPANY · " + L + ": SAAGAR · CJ-13 · 113–125¼ · made fast 18 Nov 17:00, commenced 19:25 · NORM 26,000 · ETC 20 NOV 22:01 — the permissible time is printed now. Her first night ran at about 21,400 MT a day (DPR 19.11: 10,324 MT by 0700, 44,951 left): at that rate she is through about 21 Nov 09:30, some 11 h past the ETC; to make 22:01 on the 20th she needs about 27,700 MT a day from 0700 on the 19th. No outward row on programme 20.11 — the ETC falls after its window.")
sub(M, "f:'11-18 17:00',t:'11-21 09:30',est:1", "f:'11-18 17:00',t:'11-20 22:01'")
sub(M, "n:'Rome Trader (salt, next call)',p:[113,125.25]", "n:'Rome Trader (salt, next call)',nm:26000,p:[113,125.25]")
# CJ-14
M = "{b:'14',n:'Yara J',p:[126.5,141.75]"
pre(M, PG + ": CJ-14 · outward readiness 19 Nov 23:30 (6.7 m) · NIGHT SAILING → Nord Copper. " + L + ": 24 HRS · ETC 19 Nov 20:30 — the 24 hours; she is given three more.")
sub(M, "f:'11-18 20:30',t:'11-19 20:30',est:1", "f:'11-18 20:30',t:'11-19 23:30',lt:'11-19 20:30',x24:1")
add(M, '14', 'Nord Copper', (126.5, 141.75), 'Salt in bulk', 45000, 'MT', 'COASTAL', '11-20 01:30', '11-21 21:00',
    PG + ": CJ-14 · 126½–141¾ · CSTL · sailing draught 12 m · NIGHT BERTHING — behind Yara J (23:30); about 01:30 on the 20th alongside is the board's estimate. " + L + ": CSTL 1 · 8K 7 · GEN 19 · 30K/25K/10K Sr No 7 · reported 14 Nov 15:42, ready 16 Nov 11:00 · salt in bulk 45,000 MT EXP. She takes the Coastal place while Propel Confidence still holds it till 15:00. No norm printed: 45,000 MT at the 26,000 a day Rome Trader was given → about 21 Nov 21:00, the board's estimate.",
    est=True)
M = "{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]"
pre(M, L + ": BITUMEN row · CJ-2 · 8½–16½ · \"B'TODAY\" · rice / sugar bags 32,700 MT — no norm or ETC yet.")

# ================= name maps =================
B.rep("Object.assign(LOA,{'DSM London':180,", "Object.assign(LOA,{'Belmoira':199.92,'Ken Ann':179.99,'Katerina K':199.99,'Nord Copper':199.9}); // programme 20.11\nObject.assign(LOA,{'DSM London':180,")
B.rep("Object.assign(AG,{'Ocean Kudos':'True Blue',", "Object.assign(AG,{'Ken Ann':'DBC','Katerina K':'Ambica','Nord Copper':'Cross Trade','Belmoira':'Cross Trade','Pioneer Fortune':'Marine Links','Hai Nam 81':'Gautham Freight','Sanghi Sundarshan':'Samsara','Kang Qi Fu Hua':'JM Baxi'});Object.assign(IE,{'Ken Ann':'IMP','Katerina K':'EXP','Nord Copper':'EXP','Belmoira':'EXP','Pioneer Fortune':'EXP','Hai Nam 81':'EXP','Sanghi Sundarshan':'IMP','Kang Qi Fu Hua':'IMP'}); // list 19.11 / programme 20.11\nObject.assign(AG,{'Ocean Kudos':'True Blue',")
B.rep("Object.assign(REP,{'DSM London':'10-12 23:05',", "Object.assign(REP,{'Pioneer Fortune':'11-05 12:30','Tug Varahi + barge AKG 11':'11-18 06:24','Flag Marina':'11-18 07:45','Haj Ali':'11-19 07:00','Yuan Hang Wei Ye (next call)':'11-19 08:42','Tug Marigold + barge Alaacrity 666':'11-19 12:25'}); // list 19.11\nObject.assign(REP,{'DSM London':'10-12 23:05',")
a, b = B.line_of("const ETA={'Tug Varahi + barge AKG 11':'11-18 06:30',")
B.s = B.s[:a] + ("const ETA={'Parvraj':'11-20 03:00','Tai Keystone':'11-20 12:00','MSC Magali':'11-20 12:00','Josco Taicang':'11-20 14:00','Manta Omer Mecit':'11-20 18:00','Hai Nam 81':'11-20 20:00','Gutian Trust':'11-21 00:00','Zheng Hui':'11-21 00:00',"
                 "'Hai Long 1':'11-21 00:00','Zheng Run':'11-21 00:00','Asian Summit':'11-21 04:00','Sanghi Sundarshan':'11-21 11:00','Sand Topic':'11-21 23:00','True Mariner':'11-22 00:00','Lolo Gate':'11-22 00:00','Valentina Sea':'11-22 00:00','Princess Manissa':'11-22 00:00',"
                 "'Outlander':'11-23 00:00','KSS Edmond':'11-24 00:00','Kang Qi Fu Hua':'11-24 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 19.11") + B.s[b:]
a, b = B.line_of("const NOHP=new Set(['Orion','Gokova-M','Belmoira']);")
B.s = B.s[:a] + ("const NOHP=new Set(['Orion','Gokova-M']); // the HP place goes to the highest MTPD quote of the day, not to the rank (16 Nov). A ranked vessel passed over for a berth she could use is entered here:"
                 " Gokova-M (HP 1) — CJ-7 went to Meghna Prestige (HP 3) at 42,500 on programme 19.11. Belmoira was on it (19 Nov) and is programmed for CJ-15 as GOVT(30K) on 20 Nov; Rome Trader (16 Nov) berthed under SAAGAR.") + B.s[b:]

# ================= W — list 19.11 =================
w = B.wrow
for n in ('Ken Ann', 'Katerina K', 'Nord Copper', 'Belmoira', 'Mak 1', 'Stalo'): B.wdel(n)
w('Safi Alfa', "GEN 1", rk="GEN:1")
w('Fortunelit', "GEN 2 · working at MS", rk="GEN:2")
w('Crystal O', "GEN 3 · working at MS", rk="GEN:3")
w('Crystal Land', "8K 1 · GEN 4", rk="'8K':1,GEN:4")
w('Libra', "GEN 5 · working at MS", rk="GEN:5")
w('Blue Shark', "READINESS DECLARED 19 Nov 11:00 (\"cargo not arrived 18,000 MT\") — no group rank printed yet on the 0700 sheet", rdy="11-19 11:00")
w('MK Lamis', "READINESS DECLARED 19 Nov 11:00 · GEN 8 · remark \"CJ-01 TO 04 DOC NR\"", rk="GEN:8", rdy="11-19 11:00")
w('Uni Blossom', "SGR 1 · 8K 3 · GEN 9 · Sr No 7", rk="SAAGAR:1,'8K':3,GEN:9")
w('Ariston Bulker', "GEN 10 · working at MS", rk="GEN:10")
w('African Hornbill (blades, next call)', "SGR 2 · GEN 11", rk="SAAGAR:2,GEN:11")
w('Aboudi D', "GEN 12", rk="GEN:12")
w('African Loon', "GEN 13 printed · STS at midstream — still held", rk="GEN:13", rdy="")
w('Tan Bin 259', "8K 4 · GEN 14 · Sr No 7 · working at MRG 3", rk="'8K':4,GEN:14")
w('Gokova-M', "HP 1 · 24H 1 · 8K 5 · GEN 15 — the 24-hr place of 20 Nov goes to Ken Ann (24H 2)", rk="HP:1,'24H':1,'8K':5,GEN:15")
w('AG Varvara', "SGR 3 · GEN 16 · Sr No 7", rk="SAAGAR:3,GEN:16")
w('Xin Hai Tong 71', "SGR 4 · STL 1 · GEN 17", rk="SAAGAR:4,GEN:17")
w('Porto Fiscardo', "8K 6 · GEN 18", rk="'8K':6,GEN:18")
w('Captainannis L', "READINESS 19 Nov 11:00 · 8K Y · DOC NR · working at MS", rk="'8K':98", rdy="11-19 11:00")
w('CD Glory', "SGR 5 · 8K 8 · GEN 20 · Sr No 7", rk="SAAGAR:5,'8K':8,GEN:20")
w('Dariya Priya', "SGR 6 · 8K 10 · GEN 21 · Sr No 7", rk="SAAGAR:6,'8K':10,GEN:21")
w('Sea Postman', "GEN 24 (no Govt rank printed)", rk="GEN:24")
w('Sheng Tai', "GEN 25 printed · daughter vessel, working at MS (STS) — still held", rk="GEN:25", rdy="")
w('Lila Tokyo', "HP 4 · GEN 26", rk="HP:4,GEN:26")
w('African Tiger', "RANKED NOW — SGR 7 · 8K 12 · GEN 27 · Sr No 7", rk="SAAGAR:7,'8K':12,GEN:27")
w('Flag Marina', "REPORTED / READY 18 Nov 07:45 · HP 5 · SGR 8 · 24H 3 · GEN 28 · 30K/25K/10K Sr No 7 · remark: CJ 7 & 8 or the clean berths", rk="HP:5,SAAGAR:8,'24H':3,GEN:28", rdy="11-18 07:45")
w('Tug Varahi + barge AKG 11', "reported 18 Nov 06:24 · N/A · CSTL Y · STL Y")
w('Haj Ali', "REPORTED 19 Nov 07:00 · N/A")
w('Yuan Hang Wei Ye (next call)', "REPORTED / READY 19 Nov 08:42 · HP Y · 8K Y · 30K/25K/10K Sr No 7 · \"TRANSHIPMENT\"", rk="HP:98,'8K':98", rdy="11-19 08:42")
w('Tug Marigold + barge Alaacrity 666', "REPORTED 19 Nov 12:25 · N/A · 700 pipes")
w('Parvraj', "ETA / readiness 20 Nov 03:00 · GP Y", rdy="11-20 03:00")
w('Tai Keystone', "ETA / readiness 20 Nov 12:00 · urea 47,250 MT + 22,617 MT transhipment cargo", rdy="11-20 12:00")
w('MSC Magali', "ETA / readiness 20 Nov 12:00 · HP Y", rk="HP:98", rdy="11-20 12:00")
for n, t in (('Josco Taicang', 'ETA 20 Nov 14:00 · N/A'), ('Manta Omer Mecit', 'ETA 20 Nov 18:00 · N/A'), ('Gutian Trust', 'ETA 21 Nov · N/A'), ('Zheng Hui', 'ETA 21 Nov · N/A'),
             ('True Mariner', 'ETA 22 Nov · N/A'), ('Lolo Gate', 'ETA 22 Nov · N/A'), ('Outlander', 'ETA 23 Nov · N/A')):
    w(n, t)
m = B._row('Manta Omer Mecit').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Pioneer Fortune','Sugar bags',25080,'MT',169.26,5.68,'11-13 11:00',{'8K':2,GEN:6},'LIST 19.11: BACK ON THE WAITING LIST — 8K 2 · GEN 6 · Sr No 7 · reported 5 Nov 12:30, ready 13 Nov 11:00. Programme 18.11 had given her the GFPL berth (77¾–85¾) and list 18.11 printed \"B\\'TODAY\", but she never berthed (DPR 19.11: vacant) · agent Marine Links'],",
 " ['Hai Nam 81','Salt in bulk',51000,'MT',189.94,3.5,null,{HP:98,'8K':98},'LIST 19.11 (ETA sheet): NEW · ETA 20 Nov 20:00 · N/A · HP Y · 8K Y · 30K/25K/10K Sr No 7 · departure draught 12.60 m · agent Gautham Freight'],",
 " ['Sanghi Sundarshan','Steel coil',4004,'MT',93,4.7,null,{},'LIST 19.11 (ETA sheet): NEW · ETA 21 Nov 11:00 · N/A · agent Samsara'],",
 " ['Kang Qi Fu Hua','Windmill blades & accessories',3413,'MT',153.8,4.3,null,{},'LIST 19.11 (ETA sheet): NEW · ETA 24 Nov · N/A · agent JM Baxi'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
B.rep(" // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 18.11 (0700, the issue revised after the meeting)", " // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 19.11 (0700)")

# ================= OPTS (ranks) =================
B.rep("{label:'General · by seniority',only:'GEN',rk:{GEN:22},", "{label:'General · by seniority',only:'GEN',rk:{GEN:20},")

# ================= MV — programme 20.11 =================
MVN = ['Programme for 20.11 — TF/SH/2102 (dated 19 Nov, after the 11:00 meeting; received 19 Nov 16:12) — cargo-jetty rows', [
  ['23:30', 'OUT', 'Yara J', 'CJ-14 · 6.7 m', '—', '11-19 23:30', 'NIGHT SAILING · the 24 hours were up at 20:30'],
  ['—', 'IN', 'Nord Copper', 'OTB → CJ-14 · 126½–141¾ · CSTL', '—', '11-20 01:30', 'NIGHT BERTHING · sailing draught 12 m — est'],
  ['08:00', 'OUT', 'Sea Gautham', 'CJ-3 · 4.9 m', '—', '11-20 08:00', 'nobody named behind her'],
  ['15:00', 'OUT', 'Propel Confidence', 'CJ-4 · 6.4 m', '—', '11-20 15:00', 'list ETC 11:47'],
  ['—', 'SHIFT', 'ML Egret', 'CJ-15 → CJ-4 · 23–31¾', '—', '11-20 16:00', '"SHIFT FROM CJ-15 TO CJ-04. PORT C." — est'],
  ['—', 'IN', 'Belmoira', 'OTB → CJ-15 · 143½–156¾ · GOVT(30K)', '—', '11-20 18:30', 'sailing draught 13 m — est'],
  ['17:30', 'SHIFT', 'Saga Viking', 'CJ-5 → OTB · 6.4 m', '—', '11-20 17:30', '"SHIFTING FROM CJ-05 TO OTB. AGENT\'S REQ."'],
  ['—', 'IN', 'Ken Ann', 'OTB → CJ-5 · 33½–41½ · 24HRS', '—', '11-20 19:30', 'est'],
  ['17:45', 'OUT', 'Truong Minh Dream', 'CJ-6 · 7.5 m', '—', '11-20 17:45', 'list ETC 19 Nov 13:46'],
  ['—', 'IN', 'Katerina K', 'OTB → CJ-6 · 42½–51¼', '—', '11-20 19:45', '"PROVISIONAL BERTHING." — est'],
  ['—', 'IN', 'KICT (not tracked)', 'Arrabbiata → 87–95 (ETA 19 Nov 19:00, night, starboard) · Konrad → 101–109 (ETA 19 Nov 23:30)', '—', '11-19 19:00', ''],
  ['22:00', 'SHIFT', 'Bon Voyage', 'barge berth → OTB · 2 m', '—', '11-19 22:00', 'NIGHT SHIFTING · agent\'s request'],
  ['—', '—', 'No row for', 'New Bliss · DSM London · Meghna Prestige (ETC 20 Nov 19:39) · Vishva Bandhan · Seacon Monaco (ETC 20 Nov 09:48) · ROME TRADER (ETC 20 Nov 22:01) · Heng Yuan Fa Zhan · Ocean Kudos — none of them moves before 18:00 on the 20th', '—', '11-20 18:00', '']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
B.save()
