#!/usr/bin/env python3
# apply67 — v271: two papers received 25 Nov 13:02, no text —
#   DAILY BERTHING LIST 25.11.2026 (position 0700, xlsx) and DAILY PERFORMANCE REPORT 25.11.2026 (position 0700, xlsx).
# The first list since 23.11. It prints ASIAN SUMMIT under SAAGAR at CJ-7 (norm 16,100) — the open check is answered — and CD GLORY as SGR 1.
# They reached the board two hours AFTER the meeting of 25 Nov sat, so the call of v270 (24 Nov 22:51) is frozen for scoring.
import sys, re, json, subprocess, datetime as DT
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 25.11'); q = B.q
L = 'LIST 25.11'; D = 'DPR 25.11'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)
def pre(marker, text): B.note_prefix(marker, q(text) + " ")
def after(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:b + 1] + text + "\n" + B.s[b + 1:]
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]
def setf(marker, **kw):
    """set / add / drop fields in the head of a V entry (the part before its note). est=False drops est:1; a value of None drops the field."""
    if B.s.count(marker) != 1: B.die('setf marker: ' + marker)
    i = B.s.index(marker); j = B.s.index(",note:'", i); head = B.s[i:j]
    for k, v in kw.items():
        pat = re.compile(r",%s:(?:'(?:[^'\\]|\\.)*'|[\d.]+)" % k)
        if k == 'est':
            head = pat.sub('', head)
            if v: head += ',est:1'
            continue
        new = '' if v is None else ",%s:%s" % (k, js(v))
        if pat.search(head): head = pat.sub(lambda _: new, head, count=1)
        elif new:
            est = ',est:1' if head.endswith(',est:1') else ''
            head = (head[:-6] if est else head) + new + est
    B.s = B.s[:i] + head + B.s[j:]
BASE = DT.datetime(2026, 11, 25, 7, 0)
def eta(bal, l24):
    t = BASE + DT.timedelta(hours=bal / l24 * 24); m = int(round((t.hour * 60 + t.minute) / 5.0) * 5); t = t.replace(hour=0, minute=0) + DT.timedelta(minutes=m)
    return '%d %s %02d:%02d' % (t.day, 'Nov' if t.month == 11 else 'Dec', t.hour, t.minute)

# ================= HEADER =================
B.rep("const NOW=h('11-24 22:51');", "const NOW=h('11-25 13:02');")
B.rep("<i>List</i><b>23.11 · revised after the meeting</b>", "<i>List</i><b>25.11 · 0700</b>")
B.rep("<i>DPR</i><b>24.11</b>", "<i>DPR</i><b>25.11</b>")
B.rep("berthing list 23.11 as revised after the meeting (no list came for 22.11 or, so far, 24.11)", "berthing list 25.11 (position 07:00; no list came for 22.11 or 24.11)")
B.rep("· DPR 24.11 (position 07:00; no list for 24.11 yet) ·", "· DPR 25.11 (position 07:00) ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='list 25.11 (0700) · DPR 25.11 (0700) · ")
a, b = B.line_of("const CALL_FROZEN=null;")
B.s = B.s[:a] + ("const CALL_FROZEN={d:'11-25',at:'11-24 22:51',basis:'list 23.11 (revised) · programme 25.11 · DPR 24.11 · HM signals to the evening sheet of 24 Nov (amended to 19:20)',"
    "call:[['Hai Nam 81','14'],['Meghna Prestige','15A']]}; // the call as it stood before the meeting of 25 Nov — list 25.11 and DPR 25.11 reached the board at 13:02, after it sat. Set back to null when programme 26.11 is entered and the meeting is scored.") + B.s[b:]

# ================= V =================
M = "{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]"
pre(M, D + ": WORK STOPPED 03:05, LEFT THE BERTH 05:15 on 25 Nov — 8,748 MT in her last day on 12 hooks; 27,625 MT loaded, 3,575 MT of her sugar NOT loaded. She sailed short to keep the berth moving (programme readiness 23:43, signal 06:00).")
setf(M, t='11-25 05:15')
M = "{b:'1',n:'Manta Sena',nm:6500,p:[0,7.5]"
pre(M, L + " / " + D + ": \"B'TODAY\" at CJ-1 — not made fast at 0700 · 6.5K / 8K · norm 6,500 · the ETC cell prints a duration, 4 days 17 h 23 min · stevedores printed Trueblue / JKS, 1 hook booked.")
M = "{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]"
pre(M, L + ": ETC 30 NOV 13:50 · under BITUMEN at CJ-2. " + D + ": 3,481 MT in 24 h on 12 hooks (rice 2,850 · flour 332 · sugar 299) — 19,743 loaded, 12,957 left → about " + eta(12957, 3481) + " at this rate.")
setf(M, t='11-30 13:50', est=False)
M = "{b:'3',n:'Horizon Chaser',p:[17.5,21.75]"
pre(M, D + ": commenced 07:18, COMPLETED 21:30 on 24 Nov, LEFT THE BERTH 00:50 on 25 Nov — 3,820 MT of bitumen in 14 hours; seven hours ahead of the programme's 08:00. CJ-3 is vacant on the list.")
setf(M, t='11-25 00:50')
M = "{b:'4',n:'Safi Alfa',nm:3450,p:[23,31.75]"
pre(M, L + ": ETC 28 NOV 00:00 unchanged · panels now 23–31¼ · remark \"32100 – TOTAL\". " + D + ": 3,695 MT in 24 h on 15 hooks (3,890 the day before) — 20,107 loaded, 5,993 left → about " + eta(5993, 3695) + " at this rate.")
M = "{b:'5',n:'Blue Shark',p:[32.25,39.75]"
pre(M, L + ": NORM 4,025 · ETC 30 NOV 13:00 · under GENERAL at CJ-5 · warped (\"W1\") from 32½–40. " + D + ": 2,482 MT in her first full day on 12 hooks (rice 2,133 · flour 349 · sugar none yet) — 2,856 loaded, 20,525 left → about " + eta(20525, 2482) + " at this rate, three days past the list ETC.")
setf(M, t='11-30 13:00', est=False, nm=4025)
M = "{b:'6',n:'Parvraj',nm:14950,p:[40.75,49]"
pre(M, L + ": panels 40¾–49 · \"S1, W1\" (shifted once, warped once) · ETC still printed 24 Nov 08:17. " + D + ": 11,449 MT in 24 h on 12 hooks — 45,549 off, 3,951 left → about " + eta(3951, 11449) + " today.")
M = "{b:'7',n:'Gokova-M',nm:50000,p:[50.5,57]"
pre(M, D + ": 36,500 MT in her last day on 19 hooks — 50,500 MT in all; printed \"COMP 0030 HRS LB 0005 HRS\" on 25 Nov (the two hours are the wrong way round; the signal had OUT 00:01). 25 hours alongside for 50,500 MT.")
setf(M, t='11-25 00:05')
M = "{b:'7',n:'Asian Summit',nm:30000,p:[50,57]"
pre(M, L + ": PRINTED UNDER \"SAAGAR\" at CJ-7 (Sr No 4, with AG Varvara and Uni Blossom) · NORM 16,100 — the petcoke norm, not a 30K quote · MADE FAST 25 Nov 02:48, COMMENCED 04:50 · ETC 28 NOV 22:59. So the port does count her in the SAAGAR places — the check is closed. " + D + ": 3,800 MT in the first two hours on 5 hooks; 56,699 left.")
B.rep(M, "{b:'7',n:'Asian Summit',nm:16100,p:[50,57]")
M = "{b:'7',n:'Asian Summit',nm:16100,p:[50,57]"
setf(M, f='11-25 02:48', t='11-28 22:59', est=False, via='listed under SAAGAR (list 25.11), norm 16,100 · she was HP 4 / SGR 7 on the waiting sheet')
M = "{b:'8',n:'Zheng Hui',p:[58,67.75]"
pre(M, L + ": NORM 14,950 · ETC 28 NOV 16:15 · under GOV at CJ-8. " + D + ": 18,260 MT in her first full day on 10 hooks — 19,260 off, 46,740 left → about " + eta(46740, 18260) + " at this rate, twenty hours inside the list ETC.")
setf(M, t='11-28 16:15', est=False, nm=14950)
M = "{b:'9',n:'Sand Topic',nm:20000,p:[69,77.75]"
pre(M, D + ": COMPLETED 01:30, LEFT THE BERTH 04:00 on 25 Nov — 51,292 MT of petcoke; the last 10,200 on 11 hooks (programme: shifting to OTB 05:00).")
setf(M, t='11-25 04:00')
M = "{b:'9',n:'Pioneer Fortune',nm:6500,p:[69,76.25]"
pre(M, L + " / " + D + ": \"B'TODAY\" at CJ-9 under GFPL — not made fast at 0700 · the waiting sheet still shows her 8K 3 with \"Sr No 07\".")
M = "{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]"
pre(M, D + ": COMPLETED 06:45 on 25 Nov — 34,869 CBM, the last 32,072 pcs / 10,414 CBM on 12 hooks; the let-go hour is not printed (programme readiness 17:30). " + L + ": printed in brackets at [13] — outgoing — with AG Varvara at 13, \"B'TODAY\".")
M = "{b:'13',n:'AG Varvara',nm:4600,p:[112,125]"
pre(M, L + ": \"B'TODAY\" at CJ-13 under SAAGAR · 112–125 · NORM 4,000 CBM a day · 39,112.656 CBM · cargo density 0.136 · Sr No 07.")
B.rep(M, "{b:'13',n:'AG Varvara',nm:4000,p:[112,125]")
M = "{b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]"
pre(M, L + ": ETC 26 NOV 01:36 · COASTAL, \"CSTL(30K)\". " + D + ": 28,030 MT in 24 h on 10 hooks — 49,117 off, 23,516 left → about " + eta(23516, 28030) + " at this rate.")
setf(M, t='11-26 01:36', est=False)
M = "{b:'15',n:'ML Egret',nm:4600,p:[145.75,158.25]"
pre(M, D + ": COMPLETED 18:50, LEFT THE BERTH 22:30 on 24 Nov — 42,885 CBM / 122,980 pcs; the last 4,879 CBM on 5 hooks · stevedore Mihir & Co. Six days and an hour alongside.")
setf(M, t='11-24 22:30')
M = "{b:'15',n:'Xin Hai Tong 71',p:[145.75,158.25]"
pre(M, L + ": printed under \"PROJECT/STEEL\" at CJ-15 (Sr No 7) · MADE FAST 25 Nov 04:06, COMMENCED 06:10 · no ETC printed. " + D + ": 2 packages / 23 MT in the first hour on 1 hook; 1,798 packages / 5,683 MT left. Out about 26 Nov 12:30, est.")
setf(M, f='11-25 04:06', t='11-26 12:30')
M = "{b:'15A',n:'Ocean Kudos',nm:30000,p:[159.25,171.75]"
pre(M, L + ": ETC 26 NOV 11:09 · 24 HRS, \"24HRS (30K)\". " + D + ": 26,000 MT in her first full day on 14 hooks — 30,500 loaded, 39,690 left → about " + eta(39690, 26000) + " at this rate, eight hours past the list ETC.")
setf(M, t='11-26 11:09', est=False)
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, L + ": under HP at CJ-16, remark \"SGR(PROJ)\" · windmill blades / steel pipes & I-beams 11,531.5 MT · no ETC. " + D + ": I-beams and pipes COMPLETED 15:25 on 24 Nov (8,220 MT); WINDMILL BLADES COMMENCED 13:10 — 16 blades / 309 MT by 0700, 38 blades / 729 MT left → about 27 Nov 01:20 at that pace, est.")
setf(M, t='11-27 01:20')

# ================= W =================
B.wdel('Libra'); B.wdel('Manta Omer Mecit')
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Fortunelit', "GEN 1 · working at MS — the senior vessel of the General line now that Blue Shark is alongside", rk="GEN:1")
w('Crystal Land', "8K 2 · GEN 2 — next of the 6.5K / 8K line (Manta Sena and Pioneer Fortune are printed \"B'TODAY\")", rk="'8K':2,GEN:2")
w('Katerina K', "GEN 3 · remark \"22150 (J BAGS) CJ 1 TO 8, 13 TO 16\"", rk="GEN:3")
w('MK Lamis', "GEN 4 · \"CJ-01 TO 04 · DOC NR\" · DPR 25.11: loading through IFFCO began 14:25 on 24 Nov — 675 MT, 10,825 left", rk="GEN:4")
w('Ariston Bulker', "GEN 5 · working at MS (no work in the last day; 4,470 left)", rk="GEN:5")
w('Aboudi D', "GEN 6 · \"2 SHORE CRANE REQ · WORKING AT MS\" — she began at midstream 02:10 on 25 Nov (110 MT) and through IFFCO (850 MT); 7,290 left", rk="GEN:6")
w('African Loon', "GEN 7 · readiness printed 16 Nov 11:00 · STS transhipment, working at MS — 2,500 MT to Sheng Tai in the last day; 28,013 left", rk="GEN:7")
w('Porto Fiscardo', "8K 4 · GEN 8 · CJ 1–4", rk="'8K':4,GEN:8")
w('Captainannis L', "8K 5 · GEN 9 · quantity now 16,500 · \"DOC NR · WORKING AT MS\" — 1,692 MT in the last day at midstream; 10,308 left", rk="'8K':5,GEN:9", qty="16500")
w('CD Glory', "SGR 1 — THE SENIOR VESSEL OF THE SAAGAR LINE (SGR 3 on list 23.11) · 8K 6 · GEN 10 · Sr No 07 · agent / stevedore MIHIR", rk="SAAGAR:1,'8K':6,GEN:10")
w('Dariya Priya', "SGR 2 · 8K 7 · GEN 11 · Sr No 07 · working at MS — 7,300 pcs / 2,040 CBM at midstream and 4,581 pcs / 1,281 CBM landed at the barge area in the last day; 38,064 CBM left on board", rk="SAAGAR:2,'8K':7,GEN:11")
w('Sea Postman', "GEN 12 · discharge at midstream COMPLETED 07:45 on 25 Nov (28,500 MT) · NEW REMARK: \"EXP CLAY 40000MT AFTER DISCHARGING (TRUE BLUE)\" — she stays in the General line to LOAD 40,000 MT of clay", rk="GEN:12")
w('Sheng Tai', "GEN 13 · readiness printed 18 Nov 11:00 · daughter vessel, working at MS (STS) — 2,500 MT in the last day; 26,263 left", rk="GEN:13")
w('Tug Varahi + barge AKG 11', "RANKED NOW — CSTL 1 · STL 1 · GEN 14 · commercial readiness 25 NOV 11:00 (N/A before)", rk="COASTAL:1,STL:1,GEN:14", rdy="11-25 11:00")
w('African Tiger', "SGR 3 · 8K 8 · GEN 15 · Sr No 07", rk="SAAGAR:3,'8K':8,GEN:15")
w('Tug Marigold + barge Alaacrity 666', "quantity now 2,500 MT · \"700 PIPES\" · still N/A · CSTL Y", qty="2500")
w('Josco Taicang', "STL 2 · GEN 16 (STL kept out of the board)", rk="GEN:16")
w('MSC Magali', "HP 1 · GEN 17 · \"30K/25K/10K\" — the senior vessel of the HP line now", rk="HP:1,GEN:17")
w('Star New London', "RANKED NOW — HP 2 · 8K 9 · GEN 18 · commercial readiness 24 NOV 11:00 · salt 61,150 MT (58,000 before) · \"30K/25K SR.NO:07 DD-13.50\" · agent Gautam Freight — a salt vessel on a 30K quote, senior to Hai Nam 81", rk="HP:2,'8K':9,GEN:18", rdy="11-24 11:00", qty="61150")
w('Paiwan Ace', "MIHIR · SGR 4 · 8K 10 · GEN 19 (printed \"PAIWAN ICE\" again) · Sr No 07", rk="SAAGAR:4,'8K':10,GEN:19")
w('Hai Nam 81', "HP 3 · 8K 11 · GEN 20 · \"30K/25K/10K SR.NO 07 DD-12.60M\"", rk="HP:3,'8K':11,GEN:20")
w('African Pheasant', "SGR 5 · 8K 12 · GEN 21 · Sr No 07", rk="SAAGAR:5,'8K':12,GEN:21")
w('Erna Oldendorff', "RANKED NOW — SGR 6 · GEN 22 · reporting / readiness printed 23 Nov 13:12 (the expected sheet had 11:30) · Sr No 07", rk="SAAGAR:6,GEN:22", rdy="11-23 13:12")
w('Saturn J', "ON THE WAITING SHEET — reported 23 Nov 21:57 · N/A")
w('Kang Qi Fu Hua', "ON THE WAITING SHEET — reported 24 Nov 06:00 · N/A · windmill blades & accessories 3,412.741 MT")
w('Tai Keystone', "ON THE WAITING SHEET — reported / ready 24 Nov 06:30 · GEN 23, no Govt rank printed · urea 47,250 + 22,617 MT transhipment cargo, last port Pakistan", rk="GEN:23")
w('Jumbo Kinetic', "ON THE WAITING SHEET — reported / ready 24 Nov 09:24 · CSTL 2 · GEN 24 · 2 HMC, 19 packages", rk="COASTAL:2,GEN:24", rdy="11-24 09:24")
w('Meghna Prestige (salt, next call)', "ON THE WAITING SHEET — reported / ready 24 Nov 11:30 · HP 4 · GEN 25 · \"30K/25K/10K S.NO 07\"", rk="HP:4,GEN:25", rdy="11-24 11:30")
w('Zheng Run', "ON THE WAITING SHEET — reported / ready 24 Nov 13:24 · HP 5 · GEN 26 · oxide pellets 66,100 MT EXP · transhipment · \"30K/25K/10K SR.NO 07 DD-12.63\"", rk="HP:5,GEN:26", rdy="11-24 13:24")
w('Kerem', "ON THE WAITING SHEET — reported 24 Nov 23:30 · N/A")
w('Rex', "still on the expected sheet · ETA and readiness both printed 23 Nov 23:00 · DD 13.60", rdy="11-23 23:00")
m = B._row('Zheng Run').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Pacific Apex','Aggregates',63700,'MT',199.98,6.63,'11-24 18:18',{HP:6,GEN:27},'" + q(L + ": NEW on the waiting sheet · aggregates 63,700 MT EXP · reported / ready 24 Nov 18:18 · HP 6 · GEN 27 · \"30K/25K/10K SR.NO-07\" · 199.98 m, 6.63 m · departure draught 13.80 m · agent Scorpio Shg") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
m = B._row('Star Unity').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Coastal Amigo','Steel plates',2200,'MT',67.8,2,null,{COASTAL:98},'" + q(L + " (ETA sheet): NEW · steel plates 2,200 MT EXP · ETA 24 Nov · N/A · CSTL Y · STL Y · 67.8 m · \"BB\" · agent Indo Global") + "'],",
 " ['Propel Success','Iron ore pellets',54758,'MT',197,12.4,'11-25 00:00',{COASTAL:98},'" + q(L + " (ETA sheet): NEW · iron ore pellets 54,758 MT IMP · ETA and readiness 25 Nov · CSTL Y · 197 m, 12.4 m · agent Seascape") + "'],",
 " ['Bunun Miracle','Salt in bulk',32000,'MT',179.97,3.8,null,{},'" + q(L + " (ETA sheet): NEW · salt in bulk 32,000 MT EXP · ETA 27 Nov 05:00 · N/A · \"25K/8K SR.NO:07 DD-9.95M\" · 179.97 m · agent Gautham Freight") + "'],",
 " ['Eva Shanghai','Rice bags',52000,'MT',199.99,6.5,null,{},'" + q(L + " (ETA sheet): NEW · rice bags 52,000 MT EXP · ETA 28 Nov · N/A · 199.99 m · agent BS Shg") + "'],",
 " ['Tug Canara Jog + barge RMG 254','Coated pipes',4000,'MT',76.2,3.5,null,{COASTAL:98},'" + q(L + " (ETA sheet): NEW · coated pipes 4,000 MT EXP · ETA 28 Nov 11:00 · N/A · CSTL Y · STL Y · \"SPACE A/C\" · agent JM Baxi") + "'],",
 " ['Kurushima','Steel general cargo',1291.6,'MT',174.43,7.35,null,{},'" + q(L + " (ETA sheet): NEW · steel general cargo 1,291.6 MT IMP · ETA 2 Dec · N/A · STL Y · 174.43 m · agent DBC") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
setline("const ETA={'Erna Oldendorff':", "const ETA={'Rex':'11-23 23:00','Coastal Amigo':'11-24 00:00','Princess Manissa':'11-25 00:00','Star Unity':'11-25 00:00','Propel Success':'11-25 00:00','V Pacific':'11-26 00:00','Lolo Gate':'11-26 00:00',"
        "'Outlander':'11-26 00:00','Valentina Sea':'11-26 00:00','Hai Long 1':'11-27 00:00','Bunun Miracle':'11-27 05:00','Eva Shanghai':'11-28 00:00','Tug Canara Jog + barge RMG 254':'11-28 11:00','KSS Edmond':'11-30 00:00',"
        "'Gutian Trust':'11-30 00:00','Kurushima':'12-02 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 25.11 — Rex is still printed on it with her readiness")
after("Object.assign(REP,{'Horizon Chaser':'11-23 20:00'});",
      "Object.assign(REP,{'Erna Oldendorff':'11-23 13:12','Saturn J':'11-23 21:57','Kang Qi Fu Hua':'11-24 06:00','Tai Keystone':'11-24 06:30','Jumbo Kinetic':'11-24 09:24','Meghna Prestige (salt, next call)':'11-24 11:30','Zheng Run':'11-24 13:24','Pacific Apex':'11-24 18:18','Kerem':'11-24 23:30'}); // list 25.11 — reporting hours as printed on the waiting sheet (placed last so that it wins)")
after("Object.assign(AG,{'Rex':'OTA Kandla','Star Unity':'Excel Infra'});",
      "Object.assign(AG,{'Pacific Apex':'Scorpio Shg','Coastal Amigo':'Indo Global','Propel Success':'Seascape','Bunun Miracle':'Gautham Freight','Eva Shanghai':'BS Shg','Tug Canara Jog + barge RMG 254':'JM Baxi','Kurushima':'DBC'});"
      "Object.assign(IE,{'Pacific Apex':'EXP','Coastal Amigo':'EXP','Propel Success':'IMP','Bunun Miracle':'EXP','Eva Shanghai':'EXP','Tug Canara Jog + barge RMG 254':'EXP','Kurushima':'IMP'});"
      " // list 25.11")
B.rep("Object.assign(SAILDR,{'Hai Nam 81':12.6,'Zheng Run':12.63,'KM Jakarta':13.0,'Rex':13.6});", "Object.assign(SAILDR,{'Hai Nam 81':12.6,'Zheng Run':12.63,'KM Jakarta':13.0,'Rex':13.6,'Pacific Apex':13.8,'Star New London':13.5,'Bunun Miracle':9.95});")

# ================= DPR const =================
def R(loc, n, ie, c, l24, upto, bal, g='', hk=0, note='', partial=None, comm=None):
    d = {'loc': loc, 'n': n, 'ie': ie, 'c': c, 'l24': l24, 'upto': upto, 'bal': bal, 'g': g, 'hk': hk}
    if partial: d['partial'] = 1; d['comm'] = comm
    d['note'] = note; return d
ROWS = [
 R('CJ-1', 'Crystal O', 'EXP', 'Sugar bags', 8748, 27625, 3575, '4/4/4', 12, 'WORK STOPPED 03:05, LEFT THE BERTH 05:15 on 25 Nov — 8,748 MT in her last day on 12 hooks; 27,625 loaded, 3,575 MT NOT loaded'),
 R('CJ-1', 'Manta Sena', 'EXP', 'Rice bags', 0, 0, 30170, '0/0/1', 1, '"BERTHING TODAY" — 30,170 MT to load · stevedores Trueblue / JKS', True, None),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour + sugar bags', 3481, 19743, 12957, '4/4/4', 12, 'rice bags 2,850 MT (13,623 loaded, 8,877 left) + wheat flour 332 (2,698 / 1,502) + sugar bags 299 (3,422 / 2,578) — 3,481 MT in 24 h on 12 hooks; 12,957 left → about ' + eta(12957, 3481) + ' at this rate'),
 R('CJ-3', 'Horizon Chaser', 'IMP', 'Bitumen', 3820, 3820, 0, '', 0, 'commenced 07:18, COMPLETED 21:30 on 24 Nov, LEFT THE BERTH 00:50 on 25 Nov — 3,820 MT'),
 R('CJ-4', 'Safi Alfa', 'EXP', 'Rice bags', 3695, 20107, 5993, '4/6/5', 15, '3,695 MT in 24 h on 15 hooks (3,890 the day before; norm 3,450) — 20,107 loaded, 5,993 left → about ' + eta(5993, 3695) + ' at this rate; list ETC 28 Nov 00:00'),
 R('CJ-5', 'Blue Shark', 'EXP', 'Rice bags + wheat flour + sugar bags', 2482, 2856, 20525, '4/4/4', 12, 'rice 2,133 MT (2,457 loaded, 9,287 left) + flour 349 (399 / 5,725) + sugar none yet (5,513 left) — 2,482 MT in her first full day on 12 hooks (norm 4,025); 20,525 left → about ' + eta(20525, 2482) + ' at this rate; list ETC 30 Nov 13:00'),
 R('CJ-6', 'Parvraj', 'IMP', 'DAP', 11449, 45549, 3951, '4/4/4', 12, '11,449 MT in 24 h on 12 hooks (norm 14,950) — 45,549 off, 3,951 left → about ' + eta(3951, 11449) + ' today'),
 R('CJ-7', 'Gokova-M', 'EXP', 'Ball clay in J-bags', 36500, 50500, 0, '5/7/7', 19, '36,500 MT in her last day on 19 hooks — 50,500 MT in all · printed "COMP 0030 HRS LB 0005 HRS" on 25 Nov'),
 R('CJ-7', 'Asian Summit', 'IMP', 'Petcoke', 3800, 3800, 56699, '0/0/5', 5, 'MADE FAST 02:48, COMMENCED 04:50 on 25 Nov — 3,800 MT in the first two hours on 5 hooks; 56,699 left · list: under SAAGAR, norm 16,100, ETC 28 Nov 22:59', True, '11-25 04:50'),
 R('CJ-8', 'Zheng Hui', 'IMP', 'DAP', 18260, 19260, 46740, '4/3/3', 10, '18,260 MT in her first full day on 10 hooks (norm 14,950) — 19,260 off, 46,740 left → about ' + eta(46740, 18260) + ' at this rate; list ETC 28 Nov 16:15 · gearless'),
 R('CJ-9', 'Sand Topic', 'IMP', 'Petcoke', 10200, 51292, 0, '5/4/2', 11, 'COMPLETED 01:30, LEFT THE BERTH 04:00 on 25 Nov — 51,292 MT'),
 R('CJ-9', 'Pioneer Fortune', 'EXP', 'Sugar bags', 0, 0, 25080, '', 0, '"BERTHING TODAY" — 25,080 MT to load · stevedore GFPL', True, None),
 R('CJ-13', 'Uni Blossom', 'IMP', 'Pine logs', 10414, 34869, 0, '4/4/4', 12, 'COMPLETED 06:45 on 25 Nov — 107,405 pcs / 34,869 CBM; the last 32,072 pcs / 10,414 CBM on 12 hooks; let-go hour not printed'),
 R('CJ-14', 'Lila Tokyo', 'IMP', 'Gypsum in bulk', 28030, 49117, 23516, '4/3/3', 10, '28,030 MT in 24 h on 10 hooks (quote 30,000) — 49,117 off, 23,516 left → about ' + eta(23516, 28030) + ' at this rate; list ETC 26 Nov 01:36 · gearless'),
 R('CJ-15', 'ML Egret', 'IMP', 'Pine logs', 4879, 42885, 0, '3/2/0', 5, 'COMPLETED 18:50, LEFT THE BERTH 22:30 on 24 Nov — 122,980 pcs / 42,885 CBM; the last 4,879 CBM on 5 hooks · stevedore Mihir & Co'),
 R('CJ-15', 'Xin Hai Tong 71', 'IMP', 'Packaged steel & project cargo', 23, 23, 5683, '0/0/1', 1, 'MADE FAST 04:06, COMMENCED 06:10 on 25 Nov — 2 packages / 23 MT in the first hour; 1,798 packages / 5,683 MT left', True, '11-25 06:10'),
 R('CJ-15A', 'Ocean Kudos', 'EXP', 'Salt in bulk', 26000, 30500, 39690, '4/5/5', 14, '26,000 MT in her first full day on 14 hooks (quote 30,000) — 30,500 loaded, 39,690 left → about ' + eta(39690, 26000) + ' at this rate; list ETC 26 Nov 11:09 · destination printed: Karachi'),
 R('CJ-16', 'African Hornbill (blades, next call)', 'EXP', 'I-beams / steel pipes + windmill blades', 664, 8529, 729, '3/3/2', 8, 'I-beams and pipes COMPLETED 15:25 on 24 Nov (355 MT in the day; 8,220 in all) · WINDMILL BLADES COMMENCED 13:10 — 16 blades / 309 MT by 0700, 38 blades / 729 MT left → about 27 Nov 01:20 at that pace', True, '11-24 13:10'),
 R('MS', 'Dariya Priya', 'IMP', 'Pine logs', 2040, 6904, 38064, '2/2/2', 6, 'at midstream 7,300 pcs / 2,040 CBM in 24 h on 6 hooks (1,202 the day before) — 6,904 CBM off, 38,064 left · and 4,581 pcs / 1,281 CBM landed at the barge area'),
 R('MS', 'Sheng Tai', 'EXP', 'Barite ore', 2500, 29737, 26263, '1/1/1', 3, 'daughter vessel, ship-to-ship from African Loon — 2,500 MT in 24 h; 29,737 loaded, 26,263 left'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 2500, 29737, 28013, '1/1/1', 3, 'mother vessel — 2,500 MT to Sheng Tai in 24 h; 29,737 off, 28,013 left'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 1692, 7492, 10308, '2/2/1', 5, '1,692 MT in 24 h on 5 hooks (nothing through CJ/OP) — 7,492 loaded, 10,308 left'),
 R('MS', 'Manta Omer Mecit', 'IMP', 'Fertiliser in J-bags', 1347, 2615, 1124, '1/1/1', 3, '1,347 MT into barges in 24 h on 3 hooks — 2,615 off, 1,124 left (1,268 landed at OP)'),
 R('MS', 'Yara J', 'IMP', 'Rice bags', 1200, 29433, 567, '1/1/1', 3, '1,200 MT into barges in 24 h (900 landed at CJ) — 29,433 off, 567 left'),
 R('MS', 'North Gate', 'EXP', 'Chick peas / rice J-bags', 1004, 25825, 0, '1/1/1', 3, 'COMPLETED 02:00, LEFT 06:15 on 25 Nov — 25,825 MT'),
 R('MS', 'Aboudi D', 'EXP', 'Rice + sugar bags', 110, 110, 8030, '2/2/2', 6, 'COMMENCED at midstream 02:10 on 25 Nov — rice 100 MT, sugar 10 MT; 8,030 left (850 MT more through IFFCO)', True, '11-25 02:10'),
 R('MS', 'Sea Postman', 'IMP', 'Rock phosphate', 100, 28500, 0, '1/0/0', 1, 'COMPLETED 07:45 on 25 Nov — 28,500 MT · the list has her next for 40,000 MT of clay, export'),
 R('MS', 'Fortunelit', 'EXP', 'Rice bags', 0, 7000, 3000, '', 0, 'no work for the third day — 3,000 left'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 0, 3530, 4470, '', 0, 'no work — 4,470 left'),
 R('OJ-1', 'Bogazici (LPG/C)', 'IMP', 'Propane + butane', 16166, 16166, 3688, '', 0, 'MADE FAST 10:48 on 24 Nov, commenced 13:00 / 14:00 — propane 8,213 MT (3,242 left) + butane 7,953 (446 left); list ETC 25 Nov 18:25', True, '11-24 13:00'),
 R('OJ-2', 'Chemroute Pegasus', 'IMP', 'Chemicals', 6797, 6797, 1912, '', 0, 'MADE FAST 07:55, COMMENCED 11:25 on 24 Nov — 6,797 MT; 1,912 left; list ETC 25 Nov 08:54', True, '11-24 11:25'),
 R('OJ-3', 'Hafnia Ammolite', 'IMP', 'CDSBO', 11914, 24900, 5900, '', 0, '11,914 MT in 24 h — 24,900 off, 5,900 left → about ' + eta(5900, 11914) + ' at this rate; list ETC 26 Nov 22:40'),
 R('OJ-4', 'Al Mahboobah', 'EXP', 'Benzene', 1638, 9336, 0, '', 0, 'COMPLETED 16:30, LEFT THE BERTH 21:30 on 24 Nov — 9,336 MT'),
 R('OJ-4', 'Chemroad Nexus', 'IMP', 'Chemicals', 1231, 1231, 9719, '', 0, 'MADE FAST 00:20, COMMENCED 02:50 on 25 Nov — 1,231 MT; 9,719 left; list ETC 26 Nov 01:11', True, '11-25 02:50'),
 R('OJ-6', 'Willows', 'IMP', 'MS', 9723, 28000, 0, '', 0, 'COMPLETED 03:12 on 25 Nov — 28,000 MT; let-go hour not printed (signal: RT OUT 08:00)'),
 R('OJ-6', 'Culture', 'EXP', 'VLSFO', 0, 0, 24000, '', 0, '"BERTHING TODAY" — 24,000 MT to load', True, None),
 R('OJ-7', 'Ginga Cheetah', 'IMP', 'CDSBO + CSFO', 31, 24270, 0, '', 0, 'COMPLETED 08:00, LEFT THE BERTH 10:05 on 24 Nov — 24,270 MT'),
 R('OJ-7', 'Sriwangi V', 'IMP', 'CPO', 6907, 6907, 3093, '', 0, 'MADE FAST 12:30, COMMENCED 15:06 on 24 Nov — 6,907 MT; 3,093 left; list ETC 25 Nov 18:35', True, '11-24 15:06'),
 R('TT-1', 'Blue Ionian', 'IMP', 'Sugar bulk', 12979, 25400, 47955, '', 0, '12,979 MT in 24 h — 25,400 off, 47,955 left → about ' + eta(47955, 12979) + ' at this rate'),
 R('TT-2', 'Woohyun Dream', 'EXP', 'RSM in bulk', 1230, 31500, 0, '', 0, 'COMPLETED 16:00, LEFT THE BERTH 19:30 on 24 Nov — 31,500 MT · TT-2 vacant'),
 R('TT-3', 'MP Postpanamax 1', 'IMP', 'Coal in bulk', 25386, 26900, 61100, '', 0, '25,386 MT in her first full day — 26,900 off, 61,100 left → about ' + eta(61100, 25386) + ' at this rate'),
]
a = B.s.index("const DPR={d:'24.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};")
old = B.s[a:e].split('\n'); ri = next(i for i, l in enumerate(old) if l.startswith(' rows:['))
keep = old[2:ri]
NEWDPR = ("const DPR={d:'25.11.2026',asOf:'11-25 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 25 Nov (xlsx from Mihir, 25 Nov 13:02)',\n"
 " tot:{dry:177419,dryL:83095,dryU:94324,ms:12493,kict:31275,tuna:39595,oj:54407,vad:324789,all:639978,gangs:'PR 19 · TR 5 · 40 + 6 W gangs demanded / 40 + 6 W supplied',rakes:'2',wb:971,sail:'MAK 1 · midstream · 04:45 · LPG/C Gas Hong Kong and LPG/C Crystal River · anchorage · 07:42'},\n"
 + "\n".join(keep) + ("\n" if keep else "") + " rows:[\n  " + ",\n  ".join(js(r) for r in ROWS) + "\n ]};")
B.s = B.s[:a] + NEWDPR + B.s[e:]

# ================= MSWORK (Barge tab) =================
out = subprocess.run(['python3', '-I', '/home/claude/berth-board/tools/barge_from_dpr.py', '/home/claude/work/in25a/dpr25.txt', '25.11', '11-25 07:00'], capture_output=True, text=True).stdout.rstrip('\n')
assert out.startswith("  {d:'25.11'") and out.endswith("]},"), out[-60:]
out = out.replace("n:'Aboudi',", "n:'Aboudi D',").replace("c:'Fertilizer j/bags'", "c:'Fertiliser in J-bags'").replace("ag:'Jm Baxi'", "ag:'JM Baxi'")
B.rep("const MSWORK={days:[\n", "const MSWORK={days:[\n" + out + "\n")

# ================= MV =================
MVN = ['DPR 25.11 and list 25.11 — the actual hours of the night of 24 / 25 Nov at the cargo jetties', [
 ['22:30', 'OUT', 'ML Egret', 'CJ-15 → OTB', '—', '11-24 22:30', 'completed 18:50, left the berth 22:30 (signal: OUT 22:00)'],
 ['00:05', 'OUT', 'Gokova-M', 'CJ-7 → OTB', '—', '11-25 00:05', 'printed "COMP 0030 LB 0005" (signal: OUT 00:01)'],
 ['00:50', 'OUT', 'Horizon Chaser', 'CJ-3 → OTB', '—', '11-25 00:50', 'completed 21:30 on 24 Nov, left the berth 00:50 (programme and signal: 08:00)'],
 ['01:37', 'OUT', 'Shebelle', 'CJ-12 → OTB', '—', '11-25 01:37', 'container · completed 01:22, left the berth 01:37'],
 ['02:48', 'IN', 'Asian Summit', 'OTB → CJ-7 · 50–57', '—', '11-25 02:48', 'made fast 02:48, commenced 04:50 — board had ~02:00'],
 ['03:50', 'IN', 'Hong Da Xing 768', 'OTB → CJ-12 · 100–109', '—', '11-25 03:50', 'container · made fast 03:50, commenced 04:49'],
 ['04:00', 'OUT', 'Sand Topic', 'CJ-9 → OTB', '—', '11-25 04:00', 'completed 01:30, left the berth 04:00 (signal: SHIFT 05:00)'],
 ['04:06', 'IN', 'Xin Hai Tong 71', 'OTB → CJ-15 · 145¾–158¼', '—', '11-25 04:06', 'made fast 04:06, commenced 06:10 — board had ~03:30'],
 ['05:15', 'OUT', 'Crystal O', 'CJ-1 → OTB', '—', '11-25 05:15', 'work stopped 03:05, left the berth 05:15 — 3,575 MT not loaded (signal: OUT 06:00)'],
 ['06:45', '—', 'Uni Blossom', 'CJ-13', '—', '11-25 06:45', 'completed 06:45; let-go hour not printed (programme readiness 17:30)']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")

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
def berth(bid, nown, add, f=None, nm=None, etc=None, qty=None, est=None, out=None, outBy=None):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    if f is not None: now['f'] = js(f)
    if est is False: now.pop('est', None)
    if nm is not None: now['nm'] = js(nm)
    if etc is not None: now['etc'] = js(etc)
    if qty is not None: now['q'] = repr(qty)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS)
    if out is not None:
        pv = obj(d['prev']); pv['out'] = js(out); pv['outBy'] = "'" + q(outBy + ' · ') + pv['outBy'][1:]; d['prev'] = unobj(pv, PREVKEYS)
    bput(a, b, d, tail)
def turn(bid, oldn, out, outBy, newn, f, est, add, nm=None, etc=None):
    wa, wb = B.line_of("  {n:'%s'," % newn); wl = B.s[wa:wb].strip().rstrip(','); wv = obj(wl); assert 'n' in wv and 'c' in wv
    B.s = B.s[:wa] + B.s[wb + 1:]
    a, b, d, tail = bline(bid); now = obj(d['now']); assert oldn in now['n'], (oldn, now['n'])
    pv = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}; pv['out'] = js(out); pv['outBy'] = js(outBy)
    nw = {k: wv[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'rank', 'ag') if k in wv}; nw['f'] = js(f)
    if est: nw['est'] = '1'
    if nm is not None: nw['nm'] = js(nm)
    if etc is not None: nw['etc'] = js(etc)
    nw['note'] = "'" + q(add + ' · ') + wv.get('rem', "''")[1:]
    d['prev'] = unobj(pv, PREVKEYS); d['now'] = unobj(nw, NOWKEYS); bput(a, b, d, tail)
berth('OJ-1', 'Bogazici', L + ': printed in brackets at [1] — outgoing; OJ-1 itself "VACANT" (nobody named behind her) · MADE FAST 24 Nov 10:48, COMMENCED 14:00 · norm 775 · quantity 19,854 MT · ETC 25 NOV 18:25 · ' + D + ': propane 8,213 MT (3,242 left) + butane 7,953 (446 left) · the board had about 09:00 for the berthing', f='11-24 10:48', est=False, nm='775', etc='11-25 18:25', qty=19854.03)
berth('OJ-2', 'Chemroute Pegasus', L + ': printed in brackets at [2] — outgoing; THETIS LEONA "B\'TODAY" at OJ-2 · MADE FAST 24 Nov 07:55, COMMENCED 11:25 · norm 415 · ETC 25 NOV 08:54 (programme readiness 17:30) · ' + D + ': 6,797 MT off, 1,912 left · the board had about 07:30 for the berthing', f='11-24 07:55', est=False, nm='415')
berth('OJ-3', 'Hafnia Ammolite', L + ': remark "SHIFT FROM OJ-01 23(2048)" · ETC 26 Nov 22:40 · ' + D + ': 11,914 MT in 24 h — 24,900 off, 5,900 left → about ' + eta(5900, 11914) + ' at this rate')
berth('OJ-4', 'Chemroad Nexus', L + ': MADE FAST 25 Nov 00:20, COMMENCED 02:50 · norm 525 · ETC 26 NOV 01:11 · ' + D + ': 1,231 MT off, 9,719 left · the board had about 23:00 on the 24th', f='11-25 00:20', est=False, nm='525', etc='11-26 01:11',
      out='11-24 21:30', outBy=D + ': completed 16:30, LEFT THE BERTH 21:30 on 24 Nov — 9,336 MT')
berth('OJ-7', 'Sriwangi V', L + ': MADE FAST 24 Nov 12:30, COMMENCED 15:06 · norm 415 · ETC 25 NOV 18:35 · ' + D + ': 6,907 MT off, 3,093 left · the board had about 11:45', f='11-24 12:30', est=False, nm='415', etc='11-25 18:35',
      out='11-24 10:05', outBy=D + ': completed 08:00, LEFT THE BERTH 10:05 on 24 Nov — 24,270 MT')
turn('OJ-6', 'Willows', '11-25 08:00', D + ': COMPLETED 03:12 on 25 Nov — 28,000 MT; let-go hour not printed · HM evening signal 24 Nov: RT OUT 08:00, Capt Karan · ' + L + ': printed in brackets at [6] — outgoing',
     'Culture', '11-25 10:00', True, L + ': "B\'TODAY" at OJ-6 · now on the waiting sheet — reported 23 Nov 17:00, ready 24 Nov 11:00 · VLSFO 24,000 MT EXP · HM evening signal 24 Nov: IN "o/c", Capt Sud, on the flood → about 10:00 on 25 Nov, est')
# ---- waiting and expected tankers: rebuilt from the two sheets; a vessel already on the board keeps her line and her history
LJ = json.load(open('/home/claude/work/in25a/l25.json'))
def nrm(x):
    x = x.upper(); x = re.sub(r"\(LPG/C\)", '', x); x = re.sub(r"^(LPG/C\.?|M\.?T\.?)\s*[.]?\s*", '', x.strip()); return re.sub(r'[^A-Z0-9]', '', x)
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
have = {}
for ln in B.s[w0 + 8:e0].split('\n') + B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n'):
    ln = ln.strip().rstrip(',')
    if ln.startswith('{n:'): d = obj(ln); have[nrm(d['n'][1:-1])] = d
DISP = {'GREENBHAVISHYA': 'Green Bhavishya (LPG/C)', 'VOLGA': 'Volga', 'NOBLER': 'Nobler', 'INSPIRE': 'Inspire', 'STOLTLIND': 'Stolt Lind', 'OCEANPIONEER': 'Ocean Pioneer', 'SAEHANMARINA': 'Saehan Marina'}
AGD = {'ATLANTIC SHG': 'Atlantic Shg', 'SCORPIO SHG': 'Scorpio Shg', 'NEXWAVE': 'Nexwave', 'INTEROCEAN': 'Interocean', 'JM BAXI': 'JM Baxi', 'WILHELMSEN': 'Wilhelmsen', 'ADMIRAL': 'Admiral', 'GAC SHG': 'GAC Shg'}
CGD = {'CHEMICALS': 'Chemicals', 'PROPANE': 'Propane', 'CDSBO': 'CDSBO', 'PHOSPHORIC ACID': 'Phosphoric acid', 'CPO': 'CPO'}
def dm(x):
    m = re.match(r'(\d{4})-(\d\d)-(\d\d)[ T](\d\d):(\d\d)', x or ''); return '%s-%s %s:%s' % (m.group(2), m.group(3), m.group(4), m.group(5)) if m else None
def say(t):
    d_, hm = t.split(' '); return '%d %s %s' % (int(d_[3:]), 'Nov' if d_[:2] == '11' else 'Dec', hm)
def num(x):
    try: v = round(float(x), 2); return repr(int(v)) if v == int(v) else repr(v)
    except Exception: return None
def tank_rows(sheet):
    out, sec = [], None
    for r in LJ[sheet]:
        r = [('' if x is None else str(x).strip()) for x in r] + [''] * 25
        if r[3] in ('CARGO JETTY VESSELS', 'OIL TANKERS', 'CONTAINERS', 'TUNA VESSELS', 'VADINAR'): sec = r[3]; continue
        if sec == 'OIL TANKERS' and r[1] == 'OJ': out.append(r)
    return out
WAIT, ETAS, used = [], [], set()
for r in tank_rows('WAITING LIST'):
    k = nrm(r[3])
    if k == 'CULTURE': continue                                   # turned over into OJ-6 above
    d = dict(have.get(k) or {}); used.add(k); was_eta = 'eta' in d
    if not d: B.die('new tanker on the waiting sheet, give her a line: ' + r[3])
    rep, rdy = dm(r[10]), dm(r[11]); rank = next((x for x in r[12:20] if x and x != 'X'), '')
    if r[12:20].count('X'): rank = d.get('rank', "''")[1:-1]      # berthing today: keep the rank she had
    d.pop('eta', None); d['rep'] = js(rep); d['rdy'] = js(rdy) if rdy else 'null'; d['rank'] = js(rank)
    if num(r[8]): d['q'] = num(r[8])
    if num(r[4]): d['dr'] = num(r[4])
    bits = [('ON THE WAITING SHEET — reported ' if was_eta else 'reported ') + say(rep), ('ready ' + say(rdy)) if rdy else ('not ready (' + r[11] + ')' if r[11] not in ('', 'N/A') else 'N/A')]
    if rank: bits.append('rank ' + rank)
    if r[21]: bits.append('"' + r[21] + '"')
    d['rem'] = "'" + q(L + ': ' + ' · '.join(bits) + ' · ') + d.get('rem', "''")[1:]
    WAIT.append('  ' + unobj(d, ('n', 'c', 'q', 'u', 'ie', 'loa', 'dr', 'rep', 'rdy', 'rank', 'ag', 'rem')))
seen5 = 0
for r in tank_rows('ETA'):
    k = nrm(r[3]); et = dm(r[10])
    if k == 'NO5OCEANPIONEER':
        seen5 += 1
        if r[20].upper() != 'ADMIRAL': k = 'NO5OCEANPIONEERATL'
    d = dict(have.get(k) or {}); used.add(k)
    if not d:
        nm_ = 'No 5 Ocean Pioneer (Atlantic Shg)' if k == 'NO5OCEANPIONEERATL' else DISP.get(k)
        if not nm_: B.die('new expected tanker, give her a display name: ' + r[3])
        d = {'n': js(nm_), 'c': js(CGD.get(r[7].upper(), r[7].capitalize())), 'q': num(r[8]) or '0', 'u': "'MT'", 'ie': js(r[6]), 'loa': num(r[5]) or 'null', 'dr': num(r[4]) or 'null', 'ag': js(AGD.get(r[20].upper(), r[20].title())), 'rem': "''"}
        bits = ['NEW', 'ETA ' + say(et), 'N/A']
    else:
        old = d.get('eta', "''")[1:-1]; bits = ['ETA ' + say(et) + ('' if old == et or not old else ' (' + say(old) + ' before)'), 'N/A']
    if r[21]: bits.append('"' + r[21] + '"')
    d['eta'] = js(et); d['rdy'] = 'null'; d.pop('rep', None); d.pop('rank', None)
    d['rem'] = "'" + q(L + ' (ETA sheet): ' + ' · '.join(bits) + ' · ') + d.get('rem', "''")[1:]
    ETAS.append('  ' + unobj(d, ('n', 'c', 'q', 'u', 'ie', 'loa', 'dr', 'eta', 'rdy', 'ag', 'rem')))
gone = [have[k]['n'] for k in have if k not in used]
print('tankers no longer on either sheet (dropped):', gone)
B.s = B.s[:w0 + 8] + ",\n".join(WAIT) + B.s[e0:]
e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
B.s = B.s[:e0 + len("\n ],\n eta:[\n")] + ",\n".join(ETAS) + B.s[m0:]
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-24 22:51',",
    lambda m: "const LIQ={prog:'" + q("LIST 25.11 — Thetis Leona \"B'TODAY\" at OJ-2 and Culture at OJ-6; OJ-1 printed VACANT behind LPG/C Bogazici (ETC 25 Nov 18:25) · ") + m.group(1)
    + "',src:'DPA berthing list 25.11.26 (0700) · DPR 25.11 · programme 25.11 · signals to the evening sheet of 24 Nov (disp 1655, amended to 1920)',asOf:'11-25 13:02',", B.s, count=1)
if k != 1: B.die('LIQ head not found')
LQ = ['DPR 25.11 and list 25.11 — actual hours at the oil jetties, 24 / 25 Nov', [
 ['07:55', 'IN', 'Chemroute Pegasus', 'OTB → OJ-2', '—', '11-24 07:55', 'made fast 07:55, commenced 11:25 — board had ~07:30'],
 ['10:05', 'OUT', 'Ginga Cheetah', 'OJ-7 → OTB', '—', '11-24 10:05', 'completed 08:00, left the berth 10:05 (signal: OUT 10:00)'],
 ['10:48', 'IN', 'Bogazici (LPG/C)', 'OTB → OJ-1', '—', '11-24 10:48', 'made fast 10:48, commenced 13:00 / 14:00 — board had ~09:00'],
 ['12:30', 'IN', 'Sriwangi V', 'OTB → OJ-7', '—', '11-24 12:30', 'made fast 12:30, commenced 15:06 — board had ~11:45'],
 ['21:30', 'OUT', 'Al Mahboobah', 'OJ-4 → OTB', '—', '11-24 21:30', 'completed 16:30, left the berth 21:30 (signal: OUT 21:00)'],
 ['00:20', 'IN', 'Chemroad Nexus', 'OTB → OJ-4', '—', '11-25 00:20', 'made fast 00:20, commenced 02:50 — board had ~23:00'],
 ['03:12', '—', 'Willows', 'OJ-6', '—', '11-25 03:12', 'completed 03:12; let-go hour not printed (signal: RT OUT 08:00)']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQ) + ",\n")

# ================= TUNA =================
def tuna(bid, text):
    a, b = B.line_of("  {b:'%s',n:" % bid); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(text + " ") + B.s[i:]
tuna('TT-1', D + ": 12,979 MT in 24 h — 25,400 off, 47,955 left → about " + eta(47955, 12979) + " at this rate.")
tuna('TT-3', D + ": 25,386 MT in her first full day — 26,900 off, 61,100 left → about " + eta(61100, 25386) + " at this rate. " + L + ": made fast 23 Nov 15:14, commenced 24 Nov 05:00; no ETC.")
a, b = B.line_of("  {b:'TT-2',n:'Woohyun Dream'"); B.s = B.s[:a] + B.s[b + 1:]          # TT-2 is vacant on the list
a, b = B.line_of("  {n:'RB Leah',"); B.s = B.s[:a] + B.s[b + 1:]
a, b = B.line_of("  {n:'Sakizaya Star',"); ln = B.s[a:b].rstrip(',')
B.s = B.s[:a] + ln + ",\n  {n:'RB Leah',c:'Coal in bulk',q:78263.1,u:'MT',ie:'IMP',loa:229,dr:14.5,rep:'11-24 19:00',rdy:null,ag:'Atlantic Shg',rem:'" + q(L + ": ON THE WAITING SHEET — reported 24 Nov 19:00 · N/A · remark \"TT-03\" · 229 m, 14.5 m · revised list 23.11: ETA 24 Nov 23:00") + "'}" + B.s[b:]
i = B.s.index("rem:'", B.s.index("  {n:'Sakizaya Star',")) + 5; B.s = B.s[:i] + q(L + ": unchanged — reported / ready 23 Nov 03:42 · ") + B.s[i:]
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda _: "const TUNA={src:'" + q("DPA berthing list 25.11.26 (0700) · DPR 25.11 · TT-2 VACANT — Woohyun Dream (RSM 31,500 MT) completed 16:00, left 19:30 on 24 Nov · TT-4 vacant · waiting: Sakizaya Star (ready), RB Leah (arrived 24 Nov 19:00, marked TT-03)") + "',", B.s, count=1)
assert k == 1
B.rep(" {d:'11-24',b:{'TT-1':'Blue Ionian','TT-2':'Woohyun Dream','TT-3':'MP Postpanamax 1','TT-4':''}}\n];",
      " {d:'11-24',b:{'TT-1':'Blue Ionian','TT-2':'Woohyun Dream','TT-3':'MP Postpanamax 1','TT-4':''}},\n {d:'11-25',b:{'TT-1':'Blue Ionian','TT-2':'','TT-3':'MP Postpanamax 1','TT-4':''}}\n];")

# ================= TIMBER =================
def tnote(name, text, tag=L):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('ML Egret', "COMPLETED 18:50, LEFT THE BERTH 22:30 on 24 Nov — 122,980 pcs / 42,885 CBM · stevedore Mihir & Co", D)
tnote('Uni Blossom', "COMPLETED 06:45 on 25 Nov — 107,405 pcs / 34,869 CBM; let-go hour not printed (programme readiness 17:30)", D)
tnote('AG Varvara', "\"B'TODAY\" at CJ-13 under SAAGAR · 112–125 · norm 4,000 CBM a day · cargo density 0.136")
tnote('CD Glory', "SGR 1 — the senior vessel of the SAAGAR line · 8K 6 · GEN 10 · Sr No 07")
tnote('Dariya Priya', "SGR 2 · 8K 7 · GEN 11 · working at MS — DPR 25.11: 2,040 CBM at midstream + 1,281 CBM landed at the barge area in 24 h; 38,064 CBM left on board")
tnote('African Tiger', "SGR 3 · 8K 8 · GEN 15")
tnote('Paiwan Ace', "SGR 4 · 8K 10 · GEN 19 (printed \"PAIWAN ICE\")")
tnote('African Pheasant', "SGR 5 · 8K 12 · GEN 21")
tnote('Erna Oldendorff', "SGR 6 · GEN 22 — ranked now · reporting / readiness printed 23 Nov 13:12")
B.rep("{n:'Erna Oldendorff',cbm:34424,from:'Australia',c:'Pine logs',eta:'11-23 11:30',", "{n:'Erna Oldendorff',cbm:34424,from:'Australia',c:'Pine logs',eta:'11-23 13:12',")

# ================= LEARN — the Asian Summit check is answered by the list =================
a, b = B.line_of(" {d:'24 Nov 22:51 · programme 25.11 — Asian Summit printed \"SGR\" at CJ-7'".replace('"', '\\"') if False else " {d:'24 Nov 22:51 · programme 25.11 — Asian Summit printed")
ln = B.s[a:b]; assert ln.count("st:'open'") == 1 and ln.count("fix:'") == 1
ln = ln.replace("st:'open'", "st:'ok'").replace("fix:'", "fix:'" + q("ANSWERED by list 25.11 (25 Nov 13:02): the at-berth sheet prints her under SAAGAR at CJ-7 with the petcoke norm of 16,100 — the port counts her in the SAAGAR places; reading 2 it is, and as-printed was the right entry. "))
B.s = B.s[:a] + ln + B.s[b:]

# ================= ENGINE — one condition, to match the rule already written beside it =================
# "only a vessel actually alongside now; a programmed vessel not yet berthed is never 'shifted'" — the test looked at the hour of the event, not at NOW,
# so AG Varvara (programmed for CJ-13 tonight) was being shifted off to CJ-4 a day after berthing. Now she must be alongside at NOW.
B.rep("CLEAN.includes(x.b)&&SHIFTABLE(x.c)&&x.F<=e.t-24&&x.T>e.t+SHIFT_MIN_LEFT", "CLEAN.includes(x.b)&&SHIFTABLE(x.c)&&x.F<=NOW&&x.F<=e.t-24&&x.T>e.t+SHIFT_MIN_LEFT")

# ================= OPTS — CD Glory's routes carried the ranks of list 23.11 (SGR 3 · 8K 7 · GEN 17); the horizon stood at 28 Nov =================
i = B.s.index("const OPTS={'CD Glory':{fixed:[],"); j = B.s.index("const OPTRES=", i)
OPT = ("const OPTS={'CD Glory':{fixed:[],\n routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:1},note:'" + q(
   "THE ONLY LINE THAT COUNTS FOR HER — AND SHE IS FIRST IN IT. List 25.11: CD Glory SGR 1, Dariya Priya 2 (working at midstream), African Tiger 3, Paiwan Ace 4, African Pheasant 5, Erna Oldendorff 6. "
   "A SAAGAR place opens only when a SAAGAR vessel has sailed (Mihir, 22 Nov). The list shows two SAAGAR places, both taken: AG VARVARA at CJ-13 (in tonight, 39,113 CBM — into December) and ASIAN SUMMIT at CJ-7 (petcoke 60,499 MT, made fast 25 Nov 02:48). So CD Glory's turn hangs on Asian Summit. "
   "Her list ETC is 28 Nov 22:59, at the norm of 16,100 a day; but she discharged 3,800 MT in her first two hours, and Sand Topic took 47 hours for 51,292 MT of the same cargo at the next berth — at that pace she is done about midday on 27 Nov. The timber desk has ETB 27 Nov. "
   "The board runs on the list ETC until a full day of her work is on a DPR; the date here will come forward if she keeps her pace.") + "'},\n"
   "  {label:'6.5K / 8K',only:'8K',rk:{'8K':6},note:'" + q("CLOSED. Mihir (20 Nov 16:50): CD Glory cannot berth under the 6.5K priority while other vessels are senior to her in it — the place goes by seniority, whichever berth frees first. She is 8K 6 on list 25.11; Crystal Land 2, Porto Fiscardo 4 and Captainannis L 5 stand ahead, and Manta Sena holds the place till about 30 Nov.") + "'},\n"
   "  {label:'General · by seniority',only:'GEN',rk:{GEN:10},note:'" + q("CLOSED. Mihir (20 Nov 17:13): General goes strictly by seniority — a junior is not given a berth past the vessels senior to her. She is GEN 10 on list 25.11; Fortunelit (GEN 1) is first and nine vessels stand ahead of her.") + "'}]}};\n")
B.s = B.s[:i] + OPT + B.s[j:]
B.rep("const HZ=h('11-28 00:00'); let HZRUN=HZ;", "const HZ=h('12-02 00:00'); let HZRUN=HZ;")

# ================= MYLOG — CD Glory =================
RD = {'d': '25 Nov 13:02 · list 25.11 + DPR 25.11', 'exp': '11-29 02:18', 'b': '16',
      'slot': "SAAGAR — SGR 1 on list 25.11, first of her line · both SAAGAR places are taken: AG Varvara (CJ-13) and Asian Summit (CJ-7) · her turn hangs on Asian Summit",
      'why': "List 25.11 settles yesterday's doubt: it prints ASIAN SUMMIT under SAAGAR at CJ-7 — the port counts her in the SAAGAR places — and CD GLORY as SGR 1. The SAAGAR line has two places; AG Varvara takes CJ-13 tonight for nine days, so the place that opens for CD Glory is Asian Summit's. The list gives Asian Summit an ETC of 28 Nov 22:59, worked at the petcoke NORM of 16,100 MT a day (yesterday the board had reckoned her at a 30K quote, 27 Nov 04:25 — that is where the 27 Nov 08:00 came from). On that ETC CD Glory comes in about 29 Nov 02:20, at CJ-16 — CJ-7 itself goes to Tai Keystone (Govt, can lie only at CJ-7 / 8). BUT the norm is a floor: Asian Summit landed 3,800 MT in her first two hours on 5 hooks, and Sand Topic finished 51,292 MT of the same cargo in 47 hours at the next berth. At that pace Asian Summit is done about midday on 27 Nov and CD Glory follows the same night, about 22:30 — the timber desk's ETB of 27 Nov. The board keeps the list ETC till a full day of her work is on a DPR (tomorrow's). RANGE: night of 27 Nov to early 29 Nov. Also from this list: Star New London (salt, HP 2) and Pacific Apex (HP 6) are new in the HP line; they do not touch the SAAGAR place."}
i = B.s.index("'CD Glory':[", B.s.index('const MYLOG')); j = B.s.index("\n ],", i)
assert B.s[j - 1] == '}', B.s[j - 30:j]
B.s = B.s[:j] + ",\n  " + js(RD) + B.s[j:]

B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='25 Nov 2026 · 13:20 IST';", B.s, count=1)
B.save()
