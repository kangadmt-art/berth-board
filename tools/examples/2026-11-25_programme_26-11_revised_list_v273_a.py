#!/usr/bin/env python3
# apply69 — v273: two papers received 25 Nov 16:11, no text —
#   PROGRAMME FOR 26.11.2026 (TF/SH/2102 dt 25 Nov, xlsx) — the meeting of 25 Nov — and the DAILY BERTHING LIST 25.11.2026 as revised after it (xlsx).
# Programme: CJ-6 Parvraj out 25 Nov 23:45, nobody in · CJ-14 Lila Tokyo out 26 Nov 01:36 → tug Varahi + barge AKG 11 "CSTL" · CJ-15A Ocean Kudos out 26 Nov 11:09 →
# African Hornbill shifted there from CJ-16 (port convenience) · CJ-16 → MSC MAGALI "HP(50K)" · Xin Hai Tong 71 shifted at panels.
# Scores the meeting of 25 Nov on CALL_FROZEN (Hai Nam 81 → 14, Meghna Prestige → 15A): neither.
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 25.11 (revised)'); q = B.q
L = 'LIST 25.11 (revised)'; P = 'PROGRAMME 26.11'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)
def pre(m, t): B.note_prefix(m, q(t) + " ")
def setf(marker, **kw):
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
def setline(prefix, new): a, b = B.line_of(prefix); B.s = B.s[:a] + new + B.s[b:]
def after(anchor, text):
    if B.s.count(anchor) != 1: B.die('after anchor: ' + anchor[:80])
    B.s = B.s.replace(anchor, anchor + text)

# ================= HEADER =================
B.rep("const NOW=h('11-25 13:02');", "const NOW=h('11-25 16:11');")
B.rep("const PROG_END=h('11-25 18:00'); // programme 25.11 (meeting of 24 Nov) covers till here", "const PROG_END=h('11-26 18:00'); // programme 26.11 (meeting of 25 Nov) covers till here")
B.rep("<i>List</i><b>25.11 · 0700</b>", "<i>List</i><b>25.11 · revised after the meeting</b>")
B.rep("<i>Programme</i><b>25.11</b>", "<i>Programme</i><b>26.11</b>")
B.rep("berthing list 25.11 (position 07:00; no list came for 22.11 or 24.11) · programme 25.11 ·", "berthing list 25.11 as revised after the meeting (no list came for 22.11 or 24.11) · programme 26.11 ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 26.11 (TF/SH/2102 dt 25 Nov) · list 25.11 revised after the meeting · ")
B.rep("const PROG_SAIL=new Set(['Crystal O',", "const PROG_SAIL=new Set(['Parvraj','Lila Tokyo','Ocean Kudos','Crystal O',")
a, b = B.line_of("const CALL_FROZEN={d:'11-25',"); B.s = B.s[:a] + "const CALL_FROZEN=null;" + B.s[b:]

# ================= V — the programme =================
M = "{b:'6',n:'Parvraj',nm:14950,p:[40.75,49]"
pre(M, P + ": CJ-06 · OUT readiness 25 Nov 23:45, 6.4 m, night sailing — NO inward vessel is printed for the berth, and her Govt place is given to nobody.")
setf(M, t='11-25 23:45', lt='11-24 08:17')
M = "{b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]"
pre(M, P + ": CJ-14 · OUT readiness 26 Nov 01:36 (her list ETC), 7.0 m, night sailing → TUG VARAHI WITH BARGE AKG 11 takes 128–134¾ as \"CSTL\", night berthing — the Coastal place goes to a coastal vessel.")
M = "{b:'15A',n:'Ocean Kudos',nm:30000,p:[159.25,171.75]"
pre(M, P + ": CJ-15A · OUT readiness 26 Nov 11:09 (her list ETC), 14.1 m → AFRICAN HORNBILL is shifted here from CJ-16 (port convenience); no new vessel takes her 24-hrs place. DPR 25.11 pace: about 19:40 — if she is late, the shift and MSC Magali behind it are late too.")
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, P + ": TWO ROWS — (1) NIGHT TURNAROUND at 173½–188 at 20:30 on 25 Nov, agent's request, draft 9.50 m; (2) SHIFTING FROM CJ-16 TO CJ-15A, to 157½–166¾, port convenience, once Ocean Kudos is out (readiness 26 Nov 11:09) → about 13:00 on 26 Nov, est — CJ-16 is then given to MSC MAGALI, \"HP(50K)\".")
setf(M, t='11-26 13:00', est=True)
M = "{b:'15',n:'Xin Hai Tong 71',p:[145.75,158.25]"
pre(M, P + ": SHIFTING AT PANELS to 143–156¼, port convenience — 2¾ panels south, into the room Lila Tokyo leaves (the tug and barge take only 128–134¾).")
B.rep(M, "{b:'15',n:'Xin Hai Tong 71',p:[143,156.25]")
NEWV = [
 " {b:'14',n:'Tug Varahi + barge AKG 11',p:[128,134.75],c:'Coated pipes',q:4000,u:'MT',cat:'COASTAL',f:'11-26 03:30',t:'11-27 17:55',est:1,note:'" + q(
   P + ": CJ-14 · IN behind Lila Tokyo (out readiness 26 Nov 01:36) · 128–134¾ · CATEGORY \"CSTL\" · night berthing → about 03:30 on 26 Nov, est. 4,000 MT of coated pipes → about 27 Nov 17:55, est (the board's reckoning; no norm printed). "
   "Waiting sheet: CSTL 1 · STL 1 · GEN 15; reported 18 Nov 06:24, commercial readiness 25 Nov 11:00 — she declared ready at the meeting that berthed her; agent JM Baxi. THE COASTAL PLACE WENT TO A COASTAL VESSEL. The board's call (24 Nov 22:51) had Hai Nam 81 here on a 30K quote — the tug was not ready then.") + "'},",
 " {b:'15A',n:'African Hornbill (blades, next call)',p:[157.5,166.75],c:'Windmill blades / steel pipes / I-beams',q:11532,u:'MT',cat:'STL',slot:'HP',via:'Project priority (list: SGR(PROJ)) · in the vacant Higher productivity place',f:'11-26 13:30',t:'11-27 03:20',est:1,note:'" + q(
   P + ": SHIFTING FROM CJ-16 TO CJ-15A · 157½–166¾ · PORT CONVENIENCE — behind Ocean Kudos (out readiness 26 Nov 11:09) → about 13:30 on 26 Nov, est. The panels are entered as printed (9¼ panels). She has 38 blades / 729 MT left on DPR 25.11 → about 27 Nov 03:20 with the shift, est. "
   "The port moves the project vessel to make CJ-16's length free for MSC Magali (253 m), the HP bid.") + "'},",
 " {b:'16',n:'MSC Magali',nm:50000,p:[169.5,188],c:'Steam coal',q:100728,u:'MT',cat:'HP',f:'11-26 15:00',t:'11-28 15:20',est:1,note:'" + q(
   P + ": CJ-16 · IN · 169½–188 · CATEGORY \"HP(50K)\" — an HP bid at the ceiling of 50,000 MT a day. No outward vessel is printed on her row: she comes in when African Hornbill has been shifted to CJ-15A, which waits for Ocean Kudos (out readiness 26 Nov 11:09) → about 15:00 on 26 Nov, est. "
   "100,728 MT of steam coal at 50,000 a day → about 28 Nov 15:20, est. Waiting sheet: HP 1 · GEN 18 · \"30K/25K/10K\" · gearless; reported / ready 20 Nov 07:30; 253.54 m, 13.38 m; agent Genesis. Coal on the clean side goes only to CJ-16 (Trade Notice 3089). "
   "MIHIR (25 Nov 14:47) had said no vessel bid for the HP category — the programme prints this one; see the checks. The board's call had Meghna Prestige (HP 4) for the HP place, at CJ-15A.") + "'},",
]
a, b = B.line_of(" {b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]")
B.s = B.s[:a] + "\n".join(NEWV) + "\n" + B.s[a:]
B.rep("'AG Varvara':199.99,'Xin Hai Tong 71':199.9});", "'AG Varvara':199.99,'Xin Hai Tong 71':199.9,'Tug Varahi + barge AKG 11':77,'MSC Magali':253.54});")

# ================= W =================
for n in ('MSC Magali', 'Tug Varahi + barge AKG 11', 'KM Jakarta'): B.wdel(n)      # KM Jakarta (salt 55,000, True Blue) is on neither sheet of the revised list
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Marsal', "RANKED NOW — GEN 11 · commercial readiness 25 NOV 11:00 (N/A before) · remark \"2 SHORE CRANE REQ\" — every General rank below her moves down one", rk="GEN:11", rdy="11-25 11:00")
w('Dariya Priya', "SGR 2 · 8K 7 · GEN 12 · Sr No 07 · working at MS", rk="SAAGAR:2,'8K':7,GEN:12")
w('Sea Postman', "GEN 13 · ALSO ON THE EXPECTED SHEET for her next call: clay in bulk 40,000 MT EXP, ETA 26 Nov, agent True Blue", rk="GEN:13")
w('Sheng Tai', "GEN 14", rk="GEN:14")
w('African Tiger', "SGR 3 · 8K 8 · GEN 16 · Sr No 07", rk="SAAGAR:3,'8K':8,GEN:16")
w('Josco Taicang', "STL 2 · GEN 17 (STL kept out of the board)", rk="GEN:17")
w('Star New London', "HP 2 · 8K 9 · GEN 19 · \"30K/25K SR.NO:07 DD-13.50\"", rk="HP:2,'8K':9,GEN:19")
w('Paiwan Ace', "MIHIR · SGR 4 · 8K 10 · GEN 20 · Sr No 07", rk="SAAGAR:4,'8K':10,GEN:20")
w('Hai Nam 81', "HP 3 · 8K 11 · GEN 21 · PROGRAMME 26.11: not on it — CJ-14, where the board's call had her on a 30K quote, went to the coastal tug and barge", rk="HP:3,'8K':11,GEN:21")
w('African Pheasant', "SGR 5 · 8K 12 · GEN 22 · Sr No 07", rk="SAAGAR:5,'8K':12,GEN:22")
w('Erna Oldendorff', "SGR 6 · GEN 23 · Sr No 07", rk="SAAGAR:6,GEN:23")
w('Tai Keystone', "GEN 24, no Govt rank printed · PROGRAMME 26.11: not on it — Parvraj's Govt place and CJ-6 are given to nobody", rk="GEN:24")
w('Jumbo Kinetic', "CSTL 2 · STL 3 (new; kept out of the board, as for Josco Taicang) · GEN 25 · PROGRAMME 26.11: not on it — the Coastal place went to the tug Varahi and her barge (CSTL 1)", rk="COASTAL:2,GEN:25")
w('Meghna Prestige (salt, next call)', "HP 4 · GEN 26 · PROGRAMME 26.11: not on it — the HP berth went to MSC Magali (HP 1) on a 50K bid, at CJ-16", rk="HP:4,GEN:26")
w('Zheng Run', "HP 5 · GEN 27", rk="HP:5,GEN:27")
w('Pacific Apex', "HP 6 · GEN 28", rk="HP:6,GEN:28")
w('CD Glory', "SGR 1 · 8K 6 · GEN 10 — unchanged · PROGRAMME 26.11: not on it. No timber berth came free in this window: the tug and barge took the head of the fourteenth berth, the fifteenth-A went to a shift")
w('Rex', "STILL ON THE EXPECTED SHEET · ETA and readiness now 25 Nov 10:00 (23 Nov 23:00 before) · HP Y · 8K Y · \"30K/25K/ SR.NO 07 DD-13.60\" · agent OTA Kandla", rk="HP:98,'8K':98", rdy="11-25 10:00")
w('Coastal Amigo', "(ETA sheet) ETA 25 Nov (24 Nov before) · N/A")
w('Star Unity', "(ETA sheet) ETA 25 Nov 16:00 · N/A")
w('Propel Success', "(ETA sheet) ETA and readiness 25 Nov 16:00 (00:00 before) · CSTL Y", rdy="11-25 16:00")
w('Lolo Gate', "(ETA sheet) ETA 26 Nov 10:00 · N/A")
w('Princess Manissa', "(ETA sheet) ETA 26 Nov 11:00 (25 Nov before) · N/A")
w('Outlander', "(ETA sheet) ETA 27 Nov (26 Nov before) · N/A")
w('Valentina Sea', "(ETA sheet) ETA 2 Dec (26 Nov before) · N/A")
m = B._row('Star Unity').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Yara J (next call)','Rice & sugar bags',30000,'MT',199.99,4,null,{},'" + q(L + " (ETA sheet): NEW · rice and sugar bags 30,000 MT EXP · ETA 25 Nov 11:35 · N/A · 199.99 m, 4.0 m · agent DBC") + "'],",
 " ['Tomkar','Ball clay',33500,'MT',199.9,7,null,{},'" + q(L + " (ETA sheet): NEW · ball clay 33,500 MT EXP · ETA 27 Nov · N/A · 199.9 m, 7.0 m · departure draught 10.67 m · agent True Blue") + "'],",
 " ['Feng Shou Hai','Aggregates',60500,'MT',199.9,6.5,null,{},'" + q(L + " (ETA sheet): NEW · aggregates 60,500 MT EXP · ETA 27 Nov · N/A · 199.9 m, 6.5 m · agent BS Shg") + "'],",
 " ['JSW Manikgad','Bentonite',7800,'MT',122,null,null,{},'" + q(L + " (ETA sheet): NEW · bentonite 7,800 MT EXP · ETA 27 Nov · N/A · 122 m · agent Atlantic Shg") + "'],",
 " ['Paiwan Wisdom','Pine logs',19320,'CBM',175.53,null,null,{SAAGAR:98,'8K':98},'" + q(L + " (ETA sheet): FIRST TIME ON THE PORT LIST · pine logs 19,320 CBM IMP · ETA 28 Nov · N/A · SGR Y · 8K Y · \"SR.NO 07\" · 175.53 m · agent Synergy") + "'],",
 " ['New Faith','Sugar in bags',29300,'MT',170,5.2,null,{},'" + q(L + " (ETA sheet): NEW · sugar in bags 29,300 MT EXP · ETA 28 Nov 08:00 · N/A · 170 m, 5.2 m · agent Anline") + "'],",
 " ['Hasoonlit','Sugar in bags',34500,'MT',180,6.7,null,{},'" + q(L + " (ETA sheet): NEW · sugar in bags 34,500 MT EXP · ETA 1 Dec · N/A · 180 m, 6.7 m · agent GAC Shg") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
setline("const ETA={'Rex':", "const ETA={'Coastal Amigo':'11-25 00:00','Rex':'11-25 10:00','Yara J (next call)':'11-25 11:35','Star Unity':'11-25 16:00','Propel Success':'11-25 16:00','V Pacific':'11-26 00:00','Lolo Gate':'11-26 10:00','Princess Manissa':'11-26 11:00',"
        "'Outlander':'11-27 00:00','Tomkar':'11-27 00:00','Hai Long 1':'11-27 00:00','Feng Shou Hai':'11-27 00:00','JSW Manikgad':'11-27 00:00','Bunun Miracle':'11-27 05:00','Eva Shanghai':'11-28 00:00','Paiwan Wisdom':'11-28 00:00','New Faith':'11-28 08:00',"
        "'Tug Canara Jog + barge RMG 254':'11-28 11:00','KSS Edmond':'11-30 00:00','Gutian Trust':'11-30 00:00','Hasoonlit':'12-01 00:00','Valentina Sea':'12-02 00:00','Kurushima':'12-02 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 25.11 as revised after the meeting")
a, b = B.line_of("Object.assign(AG,{'Pacific Apex':'Scorpio Shg',")
B.s = B.s[:b] + ("\nObject.assign(AG,{'Yara J (next call)':'DBC','Tomkar':'True Blue','Feng Shou Hai':'BS Shg','JSW Manikgad':'Atlantic Shg','Paiwan Wisdom':'Synergy','New Faith':'Anline','Hasoonlit':'GAC Shg'});"
    "Object.assign(IE,{'Yara J (next call)':'EXP','Tomkar':'EXP','Feng Shou Hai':'EXP','JSW Manikgad':'EXP','Paiwan Wisdom':'IMP','New Faith':'EXP','Hasoonlit':'EXP'}); // list 25.11 (revised)") + B.s[b:]
B.rep("'Star New London':13.5,'Bunun Miracle':9.95});", "'Star New London':13.5,'Bunun Miracle':9.95,'Tomkar':10.67});")

# ================= HP — one bid is now on a programme =================
B.rep("const HP_NO_BID_SRC='Mihir, 25 Nov 14:47';", "const HP_NO_BID_SRC='Mihir, 25 Nov 14:47';\nconst HP_NO_BID_NOTE='Programme 26.11 then printed MSC Magali at CJ-16 as HP(50K) — she is entered as printed. The board assumes no OTHER vessel bids, till Mihir says.';")
B.rep("(${HP_NO_BID_SRC}). The board gives no berth on an HP bid until a programme prints one; the list's HP numbers below are seniority only. A vacant HP place goes down the order.`:'');",
      "(${HP_NO_BID_SRC}). ${HP_NO_BID_NOTE} The list's HP numbers below are seniority only; the board gives no berth on a bid it cannot see. A vacant HP place goes down the order.`:'');")
B.rep("' — abhi HP mein kisi ne bid nahi ki ('+HP_NO_BID_SRC+')'", "' — '+HP_NO_BID_SRC+': HP mein bid nahi; par programme 26.11 mein MSC Magali HP(50K) chhapi hai'")
B.rep("no vessel is bidding at present (Mihir, 25 Nov)',max:2},", "Mihir (25 Nov): no vessel is bidding — but programme 26.11 prints MSC Magali as HP(50K)',max:2},")

# ================= MEETLOG — the meeting of 25 Nov, scored on the call frozen at 24 Nov 22:51 =================
ML = ("{d:'11-25',at:'11-24 22:51',basis:'list 23.11 (revised) · programme 25.11 · DPR 24.11 · HM signals to the evening sheet of 24 Nov (amended to 19:20)',prog:'26.11',"
      "call:[['Hai Nam 81','14'],['Meghna Prestige','15A']],got:[['Tug Varahi + barge AKG 11','14'],['MSC Magali','16']],note:'" + q(
      "Neither. CJ-14 — the Coastal place behind Lila Tokyo — went to a COASTAL vessel, the tug Varahi with barge AKG 11 (CSTL 1): she declared ready at 11:00 on the day of the meeting, after the call was frozen; the board had filled the place with Hai Nam 81 on a 30K quote. "
      "The HP berth went to MSC MAGALI (HP 1) on a 50,000 bid, at CJ-16 — the board had named Meghna Prestige (HP 4) at CJ-15A, by a rank that does not decide HP. To give MSC Magali her 253 m the port shifts African Hornbill from CJ-16 to CJ-15A behind Ocean Kudos, on port convenience; so CJ-15A takes no new vessel and the 24-hrs place Ocean Kudos leaves is given to nobody. "
      "CJ-6 (Parvraj out 23:45, a Govt place) and CJ-3: nobody. Xin Hai Tong 71 is moved 2¾ panels south. "
      "Same priority first held where there was a vessel: Coastal → Coastal. The meeting section of v270 had no Coastal name for CJ-14 (none was ready) and put the HP names under it — Hai Nam 81, Meghna Prestige; MSC Magali was left out of its HP names because the board held her to CJ-7 / 8. Lesson: coal can lie at CJ-16, and the port will shift a vessel to fit an HP bid in. "
      "Circular 5237 (i) was not put to the test: no clean berth was left over for a SAAGAR or a quote vessel.") + "'},")
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")

B.save(); print('saved 69 part 1')
