#!/usr/bin/env python3
# apply76a — v280 part 1. 27 Nov 10:19: Mihir's answers to the seven open questions + DAILY BERTHING LIST 27.11.2026 (xlsx, 07:00) + DPR 27.11.2026 (xlsx, 07:00).
# Mihir, in the order of the Open questions tab:
#  1 Xin Bo — "In todays berthing list it will be declared"            2 "Katerina K as 3rd General, the 1st general is Safi Alfa & 2nd general is Blue Shark"
#  3 "Aggregates is not dirty cargo"                                    4 stevedore-only vessels — "No Such vessel"
#  5 "Josco taicang is under steel already mentioned in berthing list and Jumbo Kinetic is under coastal"
#  6 "MSC magali and other 5 vessels bid for HP and most senior MSC MAGALI got movement in HP"          7 team hold v. later list — "Please go through Berthing list"
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 27.11'); q = B.q
L = 'LIST 27.11'; D = 'DPR 27.11'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def pre(m, t): B.note_prefix(m, q(t) + " ")
def setf(marker, **kw):
    if B.s.count(marker) != 1: B.die('setf marker: ' + marker)
    i = B.s.index(marker); j = B.s.index(",note:'", i); head = B.s[i:j]
    for k, v in kw.items():
        pat = re.compile(r",%s:(?:'(?:[^'\\]|\\.)*'|\[[^\]]*\]|[\d.]+)" % k)
        if k == 'est':
            head = pat.sub('', head)
            if v: head += ',est:1'
            continue
        new = ",%s:%s" % (k, js(v))
        if pat.search(head): head = pat.sub(lambda _: new, head, count=1)
        else:
            est = ',est:1' if head.endswith(',est:1') else ''
            head = (head[:-6] if est else head) + new + est
    B.s = B.s[:i] + head + B.s[j:]
def setline(prefix, new): a, b = B.line_of(prefix); B.s = B.s[:a] + new + B.s[b:]

# ================= HEADER =================
B.rep("const NOW=h('11-26 23:10');", "const NOW=h('11-27 10:20');")
B.rep("<i>List</i><b>26.11 · revised after the meeting</b>", "<i>List</i><b>27.11</b>")
B.rep("<i>DPR</i><b>26.11</b>", "<i>DPR</i><b>27.11</b>")
B.rep("berthing list 26.11 as revised after the meeting (no list came for 22.11 or 24.11) · programme 27.11 · DPR 26.11 (position 07:00) ·", "berthing list 27.11 (07:00; no list came for 22.11 or 24.11) · programme 27.11 · DPR 27.11 (position 07:00) ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='list 27.11 (0700) · DPR 27.11 (0700) · Mihir 27 Nov 10:19 (answers to the seven open questions) · ")

# ================= ENGINE — Mihir's answers =================
# 6: the HP column of the list IS the bid line — MSC Magali and five others bid; the senior-most got the HP berth.
a, b = B.line_of("const HP_NO_BID=true;")
B.s = B.s[:a] + ("const HP_NO_BID=false; // Mihir, 27 Nov 10:19: \"MSC magali and other 5 vessels bid for HP and most senior MSC MAGALI got movement in HP\" — the vessels standing in the HP column of the list are the HP bidders, and the place goes to the senior-most of them. "
    "(25 Nov 14:47 he had said no vessel was bidding; from 25 to 27 Nov the board gave no berth on an HP number.) true = no waiting vessel is given a berth on her HP number.") + B.s[b:]
B.rep("const HP_NO_BID_SRC='Mihir, 25 Nov 14:47';", "const HP_NO_BID_SRC='Mihir, 27 Nov 10:19';")
B.rep("{k:'STL',l:'Steel / project',s:'1 slot · no fallback in the regulation',max:1},", "{k:'STL',l:'Steel / project',s:'1 slot · by the STL / PRJ column of the list (Mihir, 27 Nov: Josco Taicang is under Steel as the list prints) · no fallback in the regulation',max:1},")

# ================= V =================
pre("{b:'1',n:'Manta Sena',nm:6500,p:[0,7.5]", D + ": 3,757 MT in 24 h on 13 hooks; 6,439 loaded, 23,731 left → about 3 Dec 14:35 at this rate; list ETC 30 Nov 04:03.")
pre("{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]", D + ": 3,989 MT in 24 h on 12 hooks — 28,051 loaded, 4,649 left → about 28 Nov 11:00 at this rate; list ETC 30 Nov 13:50.")
pre("{b:'4',n:'Safi Alfa',nm:3450,p:[21.25,29.5]", D + ": 2,762 MT in 24 h on 10 hooks — 25,835 loaded, 5,265 left (the DPR now counts against 31,100) → about 29 Nov 04:45 at this rate; list ETC 30 Nov 01:58, \"32100 total\".")
M = "{b:'5',n:'Blue Shark',p:[32,39.25]"
pre(M, L + ": she is printed at CJ-14, 128–141, at 07:00 on 27 Nov, with \"W1, W2, S1 32–39¼\" in the remarks — THE SHIFT IS DONE; its hour is not on any paper in hand (kept as estimated).")
M = "{b:'14',n:'Blue Shark',p:[128,141]"
pre(M, L + ": AT CJ-14, 128–141, at 07:00 on 27 Nov — shifted as programmed; hour not known. " + D + ": rice 1,924 + wheat flour 300 + sugar 425 = 2,649 MT in 24 h on 12 hooks (the shift is inside this day); 8,876 loaded, 14,491 left → about 2 Dec 18:15 at this rate; list ETC 30 Nov 13:00.")
M = "{b:'14',n:'Tug Varahi + barge AKG 11',p:[128,134.75]"
pre(M, D + " + " + L + ": MADE FAST 10:40, COMMENCED 12:00 on 26 Nov — 420 pipes / 2,500 MT loaded; the DPR still counts 220 pipes / 1,311 MT to load at 07:00 on 27 Nov, while the list of the same hour prints her in brackets — outgoing — and Blue Shark on 128–141. Her sailing hour is not on any paper in hand.")
setf(M, f='11-26 10:40')
M = "{b:'7',n:'Asian Summit',nm:16100,p:[50,57]"
pre(M, L + ": printed at CJ-5, 30½–39¼, at 07:00 on 27 Nov, remark \"S1 50–57\" — THE SHIFT IS DONE; its hour is not on any paper in hand (kept as estimated).")
M = "{b:'5',n:'Asian Summit',nm:16100,p:[30.5,39.25]"
pre(M, L + ": AT CJ-5, 30½–39¼, at 07:00 on 27 Nov (\"S1 50–57\") — shifted; ETC still 28 NOV 22:59. " + D + ": 13,600 MT in 24 h on 13 hooks — HALF OF THE DAY BEFORE (26,200): the shift is inside this day. 43,600 off, 16,899 left → about 28 Nov 12:50 at this rate; at the first day's rate, 27 Nov 22:30.")
M = "{b:'7',n:'Jumbo Kinetic',p:[52,57]"
pre(M, L + ": at CJ-7, 52–57, under COASTAL, \"B'TODAY\" — NOT YET ALONGSIDE at 07:00 on 27 Nov, though Asian Summit has left 50–57. Taken as about 12:00 on 27 Nov, est; 14 hours' work → about 28 Nov 02:00, est. MIHIR, 27 Nov: she is under Coastal.")
setf(M, f='11-27 12:00', t='11-28 02:00')
pre("{b:'6',n:'Katerina K',nm:3450,p:[40.25,49]", D + ": bentonite in J-bags 2,190 bags / 2,936 MT in her first full day on 9 hooks (norm 3,450); 2,956 loaded; left: kaolin 4,981 MT + bentonite 18,436 + soya bean meal 20,600 = 44,017 MT → about 12 Dec at this rate. No ETC on the list. MIHIR, 27 Nov: she holds the 3RD GENERAL PLACE — Safi Alfa the 1st, Blue Shark the 2nd.")
pre("{b:'8',n:'Zheng Hui',p:[58,67.75]", D + ": 12,061 MT in 24 h on 7 hooks — 44,161 off, 21,839 left → about 29 Nov 02:25 at this rate; list ETC 28 Nov 16:15.")
pre("{b:'9',n:'Pioneer Fortune',nm:6500,p:[69,76.25]", D + ": 3,440 MT in 24 h on 12 hooks — 5,439 loaded, 19,641 left → about 3 Dec at this rate.")
pre("{b:'13',n:'AG Varvara',nm:4000,p:[112,125]", D + ": 30,885 pcs / 4,200 CBM in 24 h on 12 hooks (norm 4,000) — 8,264 CBM off, 30,848 left → about 4 Dec 15:15 at this rate; list ETC 5 Dec 08:52.")
M = "{b:'15',n:'Xin Hai Tong 71',p:[143,156.25]"
pre(M, D + ": 381 packages / 1,767 MT in 24 h on 12 hooks — TWICE the day before (910): 2,700 MT off, 1,336 packages / 3,006 MT left → about 28 Nov 23:50 at this rate, not 1 Dec. No ETC on the list.")
setf(M, t='11-28 23:50')
M = "{b:'15A',n:'African Hornbill (blades, next call)',p:[157.5,166.75]"
pre(M, D + ": re-made fast at CJ-15A 13:48, resumed 15:25, COMPLETED 21:00 on 26 Nov — 54 blades / 1,038 MT + 8,220 MT of I-beams and pipes; LEFT THE BERTH 03:40 on 27 Nov.")
setf(M, f='11-26 13:48', t='11-27 03:40')
M = "{b:'15A',n:'Hai Nam 81',nm:30000,p:[157.5,166.25]"
pre(M, D + " + " + L + ": MADE FAST 06:18, COMMENCED 07:15 on 27 Nov at CJ-15A, 157½–166¼ · listed under GOV, remark \"GOV(30K)\" · norm 30,000 · ETC 29 NOV 01:54 · stevedore GFPL.")
setf(M, f='11-27 06:18', t='11-29 01:54', est=False)
M = "{b:'16',n:'MSC Magali',nm:50000,p:[169.5,188]"
pre(M, D + " + " + L + ": MADE FAST 14:58 (DPR 14:54), COMMENCED 16:35 on 26 Nov · norm 50,000 · ETC 28 NOV 17:18 · 20,927 MT in her first 14½ hours on 6 hooks; 79,801 left → at that rate about 29 Nov 05:45 · stevedore SSS. MIHIR, 27 Nov: she and five other vessels bid for HP; she, the senior-most, got the HP berth.")
setf(M, f='11-26 14:58', t='11-28 17:18', est=False)

# ================= W =================
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Tug Marigold + barge Alaacrity 666', "RANKED NOW — CSTL 1 · GEN 15 · commercial readiness 27 NOV 11:00 · Jindal coated steel pipes 1,750 MT, \"694 pipes\" · agent Chandra", rk="COASTAL:1,GEN:15", rdy="11-27 11:00")
w('True Mariner', "GEN 16 · working at MS", rk="GEN:16")
w('Josco Taicang', "STL 1 · GEN 17 — MIHIR, 27 Nov 10:19: she is under Steel as the list prints; her STL rank is now counted", rk="STL:1,GEN:17")
w('Paiwan Ace', "MIHIR · SGR 4 · 8K 8 · GEN 18 (printed \"PAIWAN ICE\") · Sr No 07", rk="SAAGAR:4,'8K':8,GEN:18")
w('African Pheasant', "SGR 5 · 8K 9 · GEN 19", rk="SAAGAR:5,'8K':9,GEN:19")
w('Kang Qi Fu Hua', "STL 2 · GEN 21 — her STL rank is now counted, as for Josco Taicang (Mihir, 27 Nov)", rk="STL:2,GEN:21")
w('Sea Postman', "HP 1 · GEN 23 — first of the HP bid line now that Hai Nam 81 has berthed", rk="HP:1,GEN:23")
w('Meghna Prestige (salt, next call)', "HP 2 · GEN 24", rk="HP:2,GEN:24")
w('Zheng Run', "HP 3 · GEN 25", rk="HP:3,GEN:25")
w('Pacific Apex', "HP 4 · GEN 26", rk="HP:4,GEN:26")
w('Rex', "HP 5 · 8K 10 · GEN 27", rk="HP:5,'8K':10,GEN:27")
w('Propel Success', "CSTL 2 · GEN 28 (Tug Marigold + barge is now CSTL 1)", rk="COASTAL:2,GEN:28")
w('Princess Manissa', "ON THE WAITING SHEET — reported / ready 26 Nov 09:15 · GEN 29 · \"3 HMC 7 TO 8\"", rk="GEN:29")
w('KM Jakarta', "ON THE WAITING SHEET — reported 26 Nov 18:48 · readiness N/A · SGR Y · \"30K/25K/10K SR.NO 07 DD-13.30 M\"")
w('Feng Shou Hai', "ON THE WAITING SHEET — reported 27 Nov 00:15 · readiness N/A · \"LP: Karachi, Pakistan\"")
w('Star New London', "(ETA sheet) ETA 27 Nov 23:30, readiness printed the same hour · HP Y")
w('Xin Bo', "(ETA sheet) still expected at 07:00 — ETA 27 Nov 03:00 · N/A · HP Y · SGR Y · 8K Y. MIHIR, 27 Nov 10:19: she will be declared in today's berthing list")
w('CD Glory', "MIHIR · SGR 1 · 8K 5 · GEN 10 — unchanged · the SAAGAR place she waits for: Asian Summit, now at CJ-5, ETC 28 Nov 22:59; 16,899 MT left at 07:00")
m = B._row('Star Unity').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Shree Krishna IX','Steel slabs',2242,'MT',76,3.4,'11-27 05:30',{},'" + q(L + ": NEW · steel slab 2,241.877 MT IMP · reported / ready 27 Nov 05:30 · CSTL 3 · GEN 30 · remark \"BB\" — she is for the Bunder basin, like Coastal Amigo; kept out of the cargo-jetty lines · 76 m · agent Indoglobal") + "'],",
 " ['Propel Fortune','Iron ore pellets',54866,'MT',189.99,12.8,null,{COASTAL:98,HP:98},'" + q(L + " (ETA sheet): NEW · iron ore pellets 54,866 MT IMP · ETA 28 Nov · N/A · CSTL Y · HP Y · \"30K/25K/10K SR.NO 07\" · 189.99 m, 12.8 m · agent Genesis") + "'],",
 " ['Jiaxin','Salt in bulk',54800,'MT',189.99,4.5,null,{HP:98},'" + q(L + " (ETA sheet): NEW · salt in bulk 54,800 MT EXP · ETA 28 Nov · N/A · HP Y · \"30K/25K/10K SR.NO 07 DD-12.80M\" · 189.99 m · agent Gautam Freight") + "'],",
 " ['Boa','Salt in bulk',58000,'MT',189.99,null,null,{HP:98},'" + q(L + " (ETA sheet): NEW · salt in bulk 58,000 MT EXP · ETA 30 Nov · N/A · HP Y · \"30K/25K/10K SR.NO 07\" · 189.99 m · agent Cross Trade") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
setline("const ETA={'Princess Manissa':", "const ETA={'Xin Bo':'11-27 03:00','Tomkar':'11-27 12:00','Agia Fotini':'11-27 12:00','Bunun Miracle':'11-27 16:00','Star New London':'11-27 23:30',"
        "'Outlander':'11-28 00:00','Paiwan Wisdom':'11-28 00:00','Propel Fortune':'11-28 00:00','Jiaxin':'11-28 00:00','New Joyful':'11-28 05:00','New Faith':'11-28 08:00','Tug Canara Jog + barge RMG 254':'11-28 11:00','V Pacific':'11-29 00:00','Hai Long 1':'11-29 00:00','JSW Manikgad':'11-29 00:00','Team Bravo':'11-29 00:00','El Matador':'11-29 00:00',"
        "'Eva Shanghai':'11-30 00:00','KSS Edmond':'11-30 00:00','Gutian Trust':'11-30 00:00','Patmos John':'11-30 00:00','Boa':'11-30 00:00','Hasoonlit':'12-01 00:00','Valentina Sea':'12-02 00:00','Kurushima':'12-02 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 27.11")
a, b = B.line_of("delete REP['Star New London'];delete REP['KM Jakarta'];")
B.s = B.s[:b] + "\nObject.assign(REP,{'Princess Manissa':'11-26 09:15','KM Jakarta':'11-26 18:48','Feng Shou Hai':'11-27 00:15','Shree Krishna IX':'11-27 05:30'}); // list 27.11 — now on the waiting sheet" + B.s[b:]
a, b = B.line_of("Object.assign(AG,{'Xin Bo':'Mihir & Company',")
B.s = B.s[:b] + "\nObject.assign(AG,{'Shree Krishna IX':'Indoglobal','Propel Fortune':'Genesis','Jiaxin':'Gautam Freight','Boa':'Cross Trade','Tug Marigold + barge Alaacrity 666':'Chandra'});Object.assign(IE,{'Shree Krishna IX':'IMP','Propel Fortune':'IMP','Jiaxin':'EXP','Boa':'EXP'}); // list 27.11" + B.s[b:]
B.rep("'KM Jakarta':13.3,'Hai Nam 81':12.6});", "'KM Jakarta':13.3,'Hai Nam 81':12.6,'Jiaxin':12.8});")
B.save(); print('saved 76a')
