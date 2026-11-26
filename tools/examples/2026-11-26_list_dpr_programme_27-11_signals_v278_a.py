#!/usr/bin/env python3
# apply74a — v278 part 1. Papers received 26 Nov 15:14, no text:
#   DAILY BERTHING LIST 26.11.2026 (xlsx) and the same list REVISED after the meeting (xlsx, "_2") · DPR 26.11.2026 (xlsx, position 07:00)
#   PROGRAMME FOR 27.11.2026 (TF/SH/2102 dt 26 Nov, xlsx) — the meeting of 26 Nov
#   HM SIGNAL day sheet for 26 Nov, two copies (image): the 20:28 sheet of 25 Nov re-dated 26/11 and extended at 08:15 (5 rows) and 09:10 (10 rows), Capt Pathak / Capt Omesh
# The call frozen from v277 (board as at 25 Nov 23:39): Star New London → 15, CD Glory → 4, Fortunelit → 15A. The meeting gave: Jumbo Kinetic → 7 "CSTL", Hai Nam 81 → 15A "GOV(30K)". None right.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 26.11 (revised)'); q = B.q
L = 'LIST 26.11 (revised)'; P = 'PROGRAMME 27.11'; D = 'DPR 26.11'; SG = 'HM SIGNAL 26 Nov day sheet'
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
        new = '' if v is None else ",%s:%s" % (k, v if k == 'p' else js(v))
        if pat.search(head): head = pat.sub(lambda _: new, head, count=1)
        elif new:
            est = ',est:1' if head.endswith(',est:1') else ''
            head = (head[:-6] if est else head) + new + est
    B.s = B.s[:i] + head + B.s[j:]
def setline(prefix, new): a, b = B.line_of(prefix); B.s = B.s[:a] + new + B.s[b:]

# ================= HEADER =================
B.rep("const NOW=h('11-25 23:39');", "const NOW=h('11-26 15:14');")
B.rep("const PROG_END=h('11-26 18:00'); // programme 26.11 (meeting of 25 Nov) covers till here", "const PROG_END=h('11-27 18:00'); // programme 27.11 (meeting of 26 Nov) covers till here")
B.rep("<i>List</i><b>25.11 · revised after the meeting</b>", "<i>List</i><b>26.11 · revised after the meeting</b>")
B.rep("<i>Programme</i><b>26.11</b>", "<i>Programme</i><b>27.11</b>")
B.rep("<i>DPR</i><b>25.11</b>", "<i>DPR</i><b>26.11</b>")
B.rep("<i>Signals to</i><b>25 Nov evening sheet (disp 1728, amended 2028)</b>", "<i>Signals to</i><b>26 Nov day sheet (to 0910)</b>")
B.rep("berthing list 25.11 as revised after the meeting (no list came for 22.11 or 24.11) · programme 26.11 · DPR 25.11 (position 07:00) · HM signal sheets to the evening sheet of 25 Nov (disp 17:28, amended 20:28) ·",
      "berthing list 26.11 as revised after the meeting (no list came for 22.11 or 24.11) · programme 27.11 · DPR 26.11 (position 07:00) · HM signal sheets to the day sheet of 26 Nov (extended to 09:10) ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 27.11 (TF/SH/2102 dt 26 Nov) · list 26.11 (0700) and as revised after the meeting · DPR 26.11 (0700) · HM signal 26 Nov day sheet (disp 2028 / 0815 / 0910) · ")
B.rep("const PROG_SAIL=new Set(['Parvraj','Lila Tokyo','Ocean Kudos',", "const PROG_SAIL=new Set(['Tug Varahi + barge AKG 11','African Hornbill (blades, next call)','Parvraj','Lila Tokyo','Ocean Kudos',")
B.rep("const HZ=h('12-02 00:00');", "const HZ=h('12-04 00:00');")

# ================= ENGINE — two things the port's papers of 26 Nov show =================
# (1) Programme 27.11 gives Parvraj's vacant Govt place to HAI NAM 81 as "GOV(30K)" at CJ-15A — a berth CD Glory (SGR 1) can use. Hai Nam 81 is HP 1 on the list.
#     So in the port's hands the "3(A) Higher productivity" step of circular 5237 (i) is the 30K / 25K quote line, and SAAGAR comes after it: Coastal → quote → SAAGAR.
B.rep("fb:'WIND,HPQ',fb5:'CSTQ,HPB,SGRQ,HPQ'},", "fb:'WIND,HPQ',fb5:'CSTQ,HPQ,SGRQ'},")
B.rep("fb:'WIND,HPQ',fb5:'HPB,SGRQ,HPQ'},", "fb:'WIND,HPQ',fb5:'HPQ,SGRQ'},")
B.rep("s:'2 places · with no Govt vessel: a Coastal vessel, then an HP bid, then the SAAGAR line by seniority (circular 5237 (i), from the 23 Nov meeting) · only then a 30k/25k quote; a vessel standing in a Govt place never blocks a Govt vessel'",
      "s:'2 places · with no Govt vessel: a Coastal vessel, then the senior 30k/25k quote vessel of the HP line (programme 27.11: Hai Nam 81, GOV(30K)), then the SAAGAR line — circular 5237 (i) as the port applies it; a vessel standing in a Govt place never blocks a Govt vessel'")
B.rep("s:'1 place · with no Coastal vessel: an HP bid, then the SAAGAR line by seniority (circular 5237 (i), from the 23 Nov meeting) · only then a 30k/25k quote'",
      "s:'1 place · with no Coastal vessel: the senior 30k/25k quote vessel of the HP line, then the SAAGAR line — circular 5237 (i) as the port applies it'")
B.rep("{k:'GOV',l:'Govt priority',p:'2 places · fertiliser / Govt cargo, by seniority · if vacant: Coastal, HP bid, SAAGAR (circular 5237)',max:2},", "{k:'GOV',l:'Govt priority',p:'2 places · fertiliser / Govt cargo, by seniority · if vacant: Coastal, 30K quote (HP line), then SAAGAR',max:2},")
B.rep("{k:'COASTAL',l:'Coastal',p:'1 place · if vacant: HP bid, then SAAGAR (circular 5237)',max:1},", "{k:'COASTAL',l:'Coastal',p:'1 place · if vacant: 30K quote (HP line), then SAAGAR',max:1},")
B.rep("p:'no place of its own — takes a vacant 24-hr place; a vacant Govt or Coastal place only when no Coastal, HP or SAAGAR vessel can use it (circular 5237)',max:0}];",
      "p:'no place of its own — takes a vacant Govt, Coastal or 24-hr place, by the seniority of the HP line (Hai Nam 81, GOV(30K), programme 27.11)',max:0}];")
# the next-meeting section: the same order
B.rep("        if(!c.length&&!HP_NO_BID){c=queue('HP').filter(suits);if(c.length)v5='HP';}\n        if(!c.length){c=queue('SAAGAR').filter(suits);if(c.length)v5='SAAGAR';}}",
      "        if(!c.length){c=W.filter(w=>Q7(w)&&RK(w,'HP')&&ready(w)).sort((a,z)=>rkv(a,'HP')-rkv(z,'HP')).filter(suits);if(c.length)v5='Q7';} // the 30K / 25K quote line, by its HP number (programme 27.11)\n"
      "        if(!c.length){c=queue('SAAGAR').filter(suits);if(c.length)v5='SAAGAR';}}")
B.rep("g.v5?'· jagah khali · circular 5237 se '+(MB_PR[g.v5]||g.v5)+' line ko':", "g.v5?'· jagah khali · '+(g.v5==='Q7'?'30K quote (HP line) ko':(MB_PR[g.v5]||g.v5)+' line ko'):")
# (2) CJ-6 went to KATERINA K — GEN 3 — while GEN 1 and GEN 2, whom the berth does not suit, waited. General goes to the senior vessel THE BERTH SUITS; a berth is not left vacant.
B.rep("const GEN_STRICT=true; // Mihir (20 Nov 17:13): General goes strictly by seniority — a junior is not given a General berth past a ready senior; see genQ() in simulate()",
      "const GEN_STRICT=false; // 26 Nov: the port berthed KATERINA K (GEN 3) at CJ-6 at 04:12 while Fortunelit (GEN 1) and Crystal Land (GEN 2) waited — CJ-6 does not suit them. So General goes to the senior vessel THE BERTH SUITS, and no berth is left vacant (Mihir, 22 Nov). "
      "The strict reading of 20 Nov (\"a junior is not given a General berth past a ready senior\") holds only among vessels the berth suits. true = General takes nothing when the berth does not suit its senior-most vessel; see genQ() in simulate()")
# a DPR row whose balance the list has since re-stated (more cargo declared) gives no pace
B.rep("V.forEach(v=>{const r=dprOf(v.n);if(!r||r.partial||!/^CJ/.test(r.loc))return;", "V.forEach(v=>{const r=dprOf(v.n);if(!r||r.partial||r.noPace||!/^CJ/.test(r.loc))return; // noPace: the list has re-stated her quantity since — the DPR balance is out of date and gives no finishing time\n ")

# ================= V =================
M = "{b:'6',n:'Parvraj',nm:14950,p:[40.75,49]"
pre(M, D + ": COMPLETED 20:45 on 25 Nov, LEFT THE BERTH 02:15 on 26 Nov — 49,500 MT (signal: OUT 23:45).")
setf(M, t='11-26 02:15')
M = "{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]"
pre(M, D + " (sailing block): SAILED 10:35 on 25 Nov.")
setf(M, t='11-25 10:35')
M = "{b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]"
pre(M, D + ": COMPLETED 06:30 on 26 Nov — 72,633 MT, the last 23,516 on 9 hooks · " + SG + ": RT OUT 08:00, Capt Bali — taken as sailed 08:00.")
M = "{b:'14',n:'Tug Varahi + barge AKG 11',p:[128,134.75]"
pre(M, P + ": CJ-14 · OUT readiness 26 NOV 17:30, 4.0 m — she comes in about noon and is to be out the same evening → MV BLUE SHARK shifted in from CJ-5. " + D + " (07:00): not alongside yet — 640 pipes / 3,811 MT to load; stevedore AML. " + L + ": at CJ-14 under COASTAL, \"B'TODAY\".")
setf(M, t='11-26 17:30')
M = "{b:'5',n:'Blue Shark',p:[32.25,39.75]"
pre(M, P + ": SHIFTING FROM CJ-05 TO CJ-14, to 128–141, \"A/C OF GAUTAM FREIGHT\" — behind the tug and barge (out readiness 26 Nov 17:30) → about 19:30 on 26 Nov, est. " + D + ": rice bags 2,695 MT + wheat flour 376 — 3,071 MT in 24 h on 15 hooks; 5,927 loaded, 17,440 left. " + L + ": panels 32–39¼, norm 4,025, ETC 30 Nov 13:00.")
setf(M, t='11-26 19:30', est=True, p='[32,39.25]')
M = "{b:'4',n:'Safi Alfa',nm:3450,p:[23,31.75]"
pre(M, L + ": ETC NOW 30 NOV 01:58 (28 Nov 00:00 before) · remark \"32100- TOTAL\" — more cargo declared: 32,100 MT in all against 26,100 on the DPR. " + P + ": WARPING AT PANELS to 21¼–29½ (room for Asian Summit at CJ-5). " + D + ": 2,966 MT in 24 h on 12 hooks; 23,073 loaded — the DPR's balance of 3,027 is against the old figure; against 32,100 it is 9,027.")
setf(M, t='11-30 01:58', p='[21.25,29.5]')
M = "{b:'7',n:'Asian Summit',nm:16100,p:[50,57]"
pre(M, P + ": SHIFTING FROM CJ-07 TO CJ-05, to 30½–39¼, \"A/C OF GAUTAM FREIGHT\" — once Blue Shark has left CJ-5 and Safi Alfa has warped → about 21:30 on 26 Nov, est; JUMBO KINETIC then takes 52–57. " + D + ": 26,200 MT IN HER FIRST FULL DAY on 15 hooks (norm 16,100) — 30,000 off, 30,499 left → about 27 Nov 11:00 at this rate; list ETC 28 Nov 22:59.")
setf(M, t='11-26 21:30', est=True)
M = "{b:'15',n:'Xin Hai Tong 71',p:[143,156.25]"
pre(M, SG + ": SHIFT 10:00 · Capt Pathak · 145¾–158¼ → 143–156¼ — done as programmed. " + D + ": 81 packages / 910 MT in her first full day on 12 hooks; 933 MT off, 1,717 packages / 4,773 MT left → about 1 Dec 13:00 at this rate — NOT 26 Nov as the board had reckoned. No ETC on the list.")
setf(M, t='12-01 13:00', est=True)
M = "{b:'15A',n:'Ocean Kudos',nm:30000,p:[159.25,171.75]"
pre(M, D + ": COMPLETED 05:00 on 26 Nov — 70,190 MT, 39,690 in her last day on 15 hooks · " + SG + ": OUT 13:00 · Capt Karan — taken as sailed 13:00.")
setf(M, t='11-26 13:00')
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, SG + ": SHIFT 13:00 · Capt Pathak · 173½–188 → 157½–166¾ — as programmed.")
setf(M, t='11-26 13:00', est=False)
M = "{b:'15A',n:'African Hornbill (blades, next call)',p:[157.5,166.75]"
pre(M, P + ": CJ-15A · OUT readiness printed \"26 Nov 03:30\" — read as 27 NOV 03:30 (night sailing), 10.0 m → MV HAI NAM 81 in, \"GOV(30K)\", night berthing. " + L + ": at 15A, 157½–166¾, \"SGR(PROJ)\", shifted from 173½–188. " + D + ": 19 blades / 365 MT in 24 h; 19 blades / 364 MT left.")
setf(M, f='11-26 14:00', t='11-27 03:30')
M = "{b:'16',n:'MSC Magali',nm:50000,p:[169.5,188]"
pre(M, SG + ": IN 13:00 · Capt Bali · OTB → 169½–188 — alongside about 15:00 on 26 Nov, est. " + L + ": at CJ-16 under HP, norm 50,000, \"B'TODAY\".")
M = "{b:'1',n:'Manta Sena',nm:6500,p:[0,7.5]"
pre(M, D + ": MADE FAST 10:40, COMMENCED 15:10 on 25 Nov — 1,536 MT by 07:00 on 13 hooks; 28,634 left · stevedores Trueblue / JKS. " + L + ": ETC 30 Nov 04:03.")
setf(M, f='11-25 10:40', t='11-30 04:03', est=False)
M = "{b:'9',n:'Pioneer Fortune',nm:6500,p:[69,76.25]"
pre(M, D + ": MADE FAST 07:20, COMMENCED 13:35 on 25 Nov — 1,999 MT by 07:00 on 12 hooks; 23,081 left · stevedore GFPL.")
setf(M, f='11-25 07:20')
M = "{b:'13',n:'AG Varvara',nm:4000,p:[112,125]"
pre(M, D + ": MADE FAST 12:12, COMMENCED 15:15 on 25 Nov (the board had ~19:30) — 29,767 pcs / 4,064 CBM in her first 16 hours on 8 hooks; 35,048 CBM left · stevedore RSIPL. " + L + ": norm 4,000, ETC 5 Dec 08:52.")
setf(M, f='11-25 12:12', t='12-05 08:52', est=False)
M = "{b:'8',n:'Zheng Hui',p:[58,67.75]"
pre(M, D + ": 12,840 MT in 24 h on 7 hooks (18,260 the day before; norm 14,950) — 32,100 off, 33,900 left → about 28 Nov 22:20 at this rate; list ETC 28 Nov 16:15.")
M = "{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]"
pre(M, D + ": 4,319 MT in 24 h on 12 hooks — 24,062 loaded, 8,638 left → about 28 Nov 07:00 at this rate; list ETC 30 Nov 13:50.")
NEWV = [
 " {b:'6',n:'Katerina K',nm:3450,p:[40.25,49],c:'Kaolin / bentonite J-bags / soya bean meal',q:48177,u:'MT',cat:'GEN',f:'11-26 04:12',t:'12-10 06:00',est:1,note:'" + q(
   D + " + " + L + ": MADE FAST 04:12, COMMENCED 06:40 on 26 Nov at CJ-6, 40¼–49 — two hours after Parvraj let go · listed under GENERAL, norm 3,450 · kaolin 26,000 MT + bentonite in J-bags 1,577 + soya bean meal 20,600 = 48,177 MT; 20 MT loaded by 07:00 · agent Ambica, stevedore SAS · for the Netherlands. No ETC printed; at the norm about 10 Dec, est. "
   "SHE WAS GEN 3 — NOT ON PROGRAMME 26.11 and on no signal sheet in hand: the port filled CJ-6 after the programme was issued. GEN 1 (Fortunelit) and GEN 2 (Crystal Land) are bag vessels the berth does not suit; General went to the senior vessel it does suit.") + "'},",
 " {b:'14',n:'Blue Shark',p:[128,141],c:'Sugar/rice/wheat bags',q:26500,u:'MT',cat:'GEN',f:'11-26 20:00',t:'11-30 13:00',nm:4025,est:1,note:'" + q(
   P + ": SHIFTING FROM CJ-05 TO CJ-14 · 128–141 · \"A/C OF GAUTAM FREIGHT\" — behind the tug Varahi and her barge (out readiness 26 Nov 17:30) → about 20:00 on 26 Nov, est. She keeps her General place; list ETC 30 Nov 13:00, norm 4,025. "
   "A bag vessel moved to a clean berth at Gautam Freight's cost: it frees CJ-5 for Asian Summit, which frees 52–57 for Gautam Freight's own vessel, Jumbo Kinetic.") + "'},",
 " {b:'5',n:'Asian Summit',nm:16100,p:[30.5,39.25],c:'Petcoke',q:60499,u:'MT',cat:'SAAGAR',via:'listed under SAAGAR (list 25.11), norm 16,100 · she was HP 4 / SGR 7 on the waiting sheet',f:'11-26 22:00',t:'11-28 22:59',est:1,note:'" + q(
   P + ": SHIFTING FROM CJ-07 TO CJ-05 · 30½–39¼ · \"A/C OF GAUTAM FREIGHT\" — after Blue Shark has left CJ-5 → about 22:00 on 26 Nov, est. She keeps her SAAGAR place. List ETC 28 Nov 22:59 (norm 16,100); at the pace of DPR 26.11 — 26,200 MT a day, 30,499 left — about 27 Nov 11:00, if the shift and the smaller berth do not slow her. "
   "THE SAAGAR PLACE CD GLORY IS WAITING FOR IS THIS ONE.") + "'},",
 " {b:'7',n:'Jumbo Kinetic',p:[52,57],c:'2 harbour mobile cranes + 19 packages',q:844,u:'MT',cat:'COASTAL',f:'11-26 23:30',t:'11-27 13:30',est:1,note:'" + q(
   P + ": CJ-07 · IN · 52–57 · CATEGORY \"CSTL\" · starboard side — no outward vessel on her row: she comes in when Asian Summit has been shifted to CJ-5 → about 23:30 on 26 Nov, est. Two harbour mobile cranes and 19 packages, 843.8 MT; no norm — 14 hours taken, est. "
   "Revised list: CSTL 1 · STL 3 · GEN 24; reported / ready 24 Nov 09:24; 152.36 m, 7.0 m; agent Gautam Freight. The Coastal place is free once the tug Varahi sails (17:30). THE BOARD HAD HELD HER TO CJ-13–16 — the port puts her at CJ-7, and shifts two vessels at Gautam Freight's cost to do it.") + "'},",
 " {b:'15A',n:'Hai Nam 81',nm:30000,p:[157.5,166.25],c:'Salt in bulk',q:52000,u:'MT',cat:'GOV',via:'30k/25k quote (Sr No 7)',f:'11-27 05:30',t:'11-28 23:05',est:1,note:'" + q(
   P + ": CJ-15A · IN behind African Hornbill (out readiness 27 Nov 03:30, night sailing) · 157½–166¼ · CATEGORY \"GOV(30K)\" · night berthing · sailing draught 12.6 m → about 05:30 on 27 Nov, est. 52,000 MT of salt at 30,000 a day → about 28 Nov 23:05, est. "
   "Revised list: HP 1 · 8K 9 · GEN 18 · \"30K/25K/10K SR.NO 07\"; reported / ready 22 Nov 19:15; 190 m; agent Gautam Freight. "
   "SHE TAKES THE GOVT PLACE PARVRAJ LEFT, ON A 30K QUOTE — the place and the berth the board had read as CD Glory's under circular 5237 (i). The port put the 30K-quote line (she is its No. 1) ahead of SAAGAR.") + "'},",
]
a, b = B.line_of(" {b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]")
B.s = B.s[:a] + "\n".join(NEWV) + "\n" + B.s[a:]
B.rep("'Tug Varahi + barge AKG 11':77,'MSC Magali':253.54});", "'Tug Varahi + barge AKG 11':77,'MSC Magali':253.54,'Katerina K':199.99,'Jumbo Kinetic':152.36,'Hai Nam 81':190});")

# ================= W =================
for n in ('Katerina K', 'Hai Nam 81', 'Jumbo Kinetic', 'Coastal Amigo'): B.wdel(n)      # Coastal Amigo is working at the Bunder basin ("OTHERS · BB", made fast 25 Nov 15:30)
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Crystal Land', "8K 1 · GEN 2", rk="'8K':1,GEN:2")
w('MK Lamis', "GEN 3 · remark \"CJ-01 TO 04 DOC NR\" · " + D + ": 950 MT through IFFCO, 1,625 loaded", rk="GEN:3")
w('Ariston Bulker', "GEN 4 · working at MS", rk="GEN:4")
w('Aboudi D', "GEN 5 · 2 shore cranes required · working at MS", rk="GEN:5")
w('African Loon', "GEN 6 · STS transhipment, working at MS", rk="GEN:6")
w('Glimlit', "RANKED NOW — 8K 2 · GEN 7 · commercial readiness 26 NOV 11:00 (N/A before) · rice in bags 24,560 + lentils in bags 3,000 · Sr No 07", rk="'8K':2,GEN:7", rdy="11-26 11:00")
w('Porto Fiscardo', "8K 3 · GEN 8", rk="'8K':3,GEN:8")
w('Captainannis L', "8K 4 · GEN 9 · DOC NR · working at MS", rk="'8K':4,GEN:9")
w('CD Glory', "MIHIR · SGR 1 · 8K 5 · GEN 10 · Sr No 07 · PROGRAMME 27.11: not on it — the Govt place the board had read as hers went to a salt vessel on a 30K quote", rk="SAAGAR:1,'8K':5,GEN:10")
B.rep("['CD Glory','Hardwood logs'", "['CD Glory','Hardwood logs'") if False else None
w('Dariya Priya', "SGR 2 · 8K 6 · GEN 12 · Sr No 07 · working at MS", rk="SAAGAR:2,'8K':6,GEN:12")
w('Sheng Tai', "GEN 13 · daughter vessel, working at MS (STS)", rk="GEN:13")
w('African Tiger', "SGR 3 · 8K 7 · GEN 14 · Sr No 07", rk="SAAGAR:3,'8K':7,GEN:14")
w('True Mariner', "RANKED NOW — GEN 15 · commercial readiness 26 NOV 11:00 (N/A before) · rice bags 25,125 MT", rk="GEN:15", rdy="11-26 11:00", qty=25125)
w('Josco Taicang', "STL 1 · GEN 16 (STL kept out of the board — open question)", rk="GEN:16")
w('Paiwan Ace', "MIHIR · SGR 4 · 8K 8 · GEN 17 · Sr No 07", rk="SAAGAR:4,'8K':8,GEN:17")
w('African Pheasant', "SGR 5 · 8K 10 · GEN 19 · Sr No 07", rk="SAAGAR:5,'8K':10,GEN:19")
w('Erna Oldendorff', "SGR 6 · GEN 20 · Sr No 07", rk="SAAGAR:6,GEN:20")
w('Kang Qi Fu Hua', "RANKED NOW — STL 2 (kept out of the board, like Josco Taicang — open question) · GEN 21 · commercial readiness 26 NOV 11:00 · remark \"2 HMC, STBD\"", rk="GEN:21", rdy="11-26 11:00")
w('Tai Keystone', "GEN 22, no Govt rank printed · urea 47,250 + 22,617 MT of transhipment cargo", rk="GEN:22")
w('Sea Postman', "HER NEXT CALL — clay 40,015 MT EXP · reported 24 Nov 07:45 · commercial readiness 26 NOV 11:00 · HP 2 · GEN 23 · \"30K/25K/10K S.NO 07\" · agent True Blue (the rock phosphate, 28,500 MT, was finished at midstream on 25 Nov)", rk="HP:2,GEN:23", rdy="11-26 11:00", cargo='Clay', qty=40015)
w('Meghna Prestige (salt, next call)', "HP 3 · GEN 25 · \"30K/25K/10K S.NO 07\" · PROGRAMME 27.11: not on it — the Govt place went to Hai Nam 81 (HP 1) on a 30K quote", rk="HP:3,GEN:25")
w('Zheng Run', "HP 4 · GEN 26", rk="HP:4,GEN:26")
w('Pacific Apex', "HP 5 · GEN 27", rk="HP:5,GEN:27")
w('Rex', "ON THE WAITING SHEET — reported / ready 25 Nov 10:00 · HP 6 · 8K 11 · GEN 28 · \"30K/25K/ SR.NO 07 DD- 13.60\"", rk="HP:6,'8K':11,GEN:28", rdy="11-25 10:00")
w('Yara J (next call)', "ON THE WAITING SHEET — reported 25 Nov 11:30 · N/A · rice and sugar bags 30,000 MT EXP · agent DBC")
w('Star Unity', "ON THE WAITING SHEET — reported 25 Nov 13:42 · N/A · remark \"1 TO 5\"")
w('Propel Success', "ON THE WAITING SHEET — reported / ready 25 Nov 14:18 · CSTL 2 · GEN 29 · iron ore pellets 54,758 MT IMP · 197 m, 12.37 m · agent Seascape", rk="COASTAL:2,GEN:29", rdy="11-25 14:18")
w('Lolo Gate', "ON THE WAITING SHEET — reported 25 Nov 19:25 · N/A")
w('Princess Manissa', "(ETA sheet) ETA and readiness 26 Nov 09:15 · remark \"3 HMC 7 TO 8\" · agent Alap Carrier", rdy="11-26 09:15")
w('Star New London', "BACK ON THE EXPECTED SHEET — ETA 27 Nov 12:00 · N/A · HP Y · \"30K/25K/10K SR.NO 07 DD-13.50 M\". The morning sheet of 26 Nov still had her waiting, HP 2, ready 24 Nov 11:00; the revised sheet takes her rank and readiness away", rk="HP:98", rdy="")
w('Feng Shou Hai', "(ETA sheet) ETA 27 Nov 01:00 · N/A")
w('Tomkar', "(ETA sheet) ETA 27 Nov 12:00 · N/A")
w('Bunun Miracle', "(ETA sheet) ETA 27 Nov 16:00 · N/A")
w('Outlander', "(ETA sheet) ETA 28 Nov · N/A")
w('JSW Manikgad', "(ETA sheet) ETA 29 Nov (27 Nov before) · N/A")
m = B._row('Star Unity').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Xin Bo','Salt in bulk',50000,'MT',189.99,6.5,null,{HP:98,SAAGAR:98,'8K':98},'" + q(L + " (ETA sheet): NEW — MIHIR · salt in bulk 50,000 MT EXP · ETA 27 Nov 03:00 · N/A · HP Y · SGR Y · 8K Y · \"30K/25K/10K SR.NO 07\" · 189.99 m, 6.5 m · agent Mihir & Company") + "'],",
 " ['KM Jakarta','Salt in bulk',60000,'MT',199.98,6.5,null,{SAAGAR:98},'" + q(L + " (ETA sheet): BACK ON THE LIST as expected — salt in bulk 60,000 MT EXP (55,000 before) · ETA 27 Nov · N/A · SGR Y · \"30K/25K/10K SR.NO 07 DD-13.30 M\" · agent True Blue. She was off both sheets of the revised list 25.11") + "'],",
 " ['Agia Fotini','Lentils in bulk',16193,'MT',184.75,8.02,null,{},'" + q(L + " (ETA sheet): NEW · lentils in bulk 16,193 MT IMP · ETA 27 Nov 12:00 · N/A · 184.75 m, 8.02 m · agent Interocean") + "'],",
 " ['New Joyful','Petcoke',53011,'MT',199.95,11.87,null,{SAAGAR:98},'" + q(L + " (ETA sheet): NEW · petcoke 53,010.95 MT IMP · ETA 28 Nov 05:00 · readiness printed \"RDY\" · SGR Y · 199.95 m, 11.87 m · agent Benline") + "'],",
 " ['Team Bravo','Pine logs',20722,'CBM',179.99,null,null,{SAAGAR:98,'8K':98},'" + q(L + " (ETA sheet): NEW · pine logs 20,722 CBM IMP · ETA 29 Nov · N/A · SGR Y · 8K Y · \"SR.NO 07\" · 179.99 m · agent Synergy") + "'],",
 " ['El Matador','Rice bags',52000,'MT',199.9,null,null,{},'" + q(L + " (ETA sheet): NEW · rice in bags 52,000 MT EXP · ETA 29 Nov · N/A · 199.9 m · agent DBC") + "'],",
 " ['Patmos John','Salt in bulk',56000,'MT',189.99,null,null,{SAAGAR:98},'" + q(L + " (ETA sheet): NEW · salt in bulk 56,000 MT EXP · ETA 30 Nov · N/A · SGR Y · \"30K/25K/10K SR.NO 07\" · 189.99 m · agent Cross Trade") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
setline("const ETA={'Coastal Amigo':", "const ETA={'Princess Manissa':'11-26 09:15','KM Jakarta':'11-27 00:00','Feng Shou Hai':'11-27 01:00','Xin Bo':'11-27 03:00','Tomkar':'11-27 12:00','Star New London':'11-27 12:00','Agia Fotini':'11-27 12:00','Bunun Miracle':'11-27 16:00',"
        "'Outlander':'11-28 00:00','Paiwan Wisdom':'11-28 00:00','New Joyful':'11-28 05:00','New Faith':'11-28 08:00','Tug Canara Jog + barge RMG 254':'11-28 11:00','V Pacific':'11-29 00:00','Hai Long 1':'11-29 00:00','JSW Manikgad':'11-29 00:00','Team Bravo':'11-29 00:00','El Matador':'11-29 00:00',"
        "'Eva Shanghai':'11-30 00:00','KSS Edmond':'11-30 00:00','Gutian Trust':'11-30 00:00','Patmos John':'11-30 00:00','Hasoonlit':'12-01 00:00','Valentina Sea':'12-02 00:00','Kurushima':'12-02 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 26.11 as revised after the meeting")
a, b = B.line_of("Object.assign(REP,{'Erna Oldendorff':'11-23 13:12',")
B.s = B.s[:b] + ("\nObject.assign(REP,{'Sea Postman':'11-24 07:45','Rex':'11-25 10:00','Yara J (next call)':'11-25 11:30','Star Unity':'11-25 13:42','Propel Success':'11-25 14:18','Lolo Gate':'11-25 19:25'}); // list 26.11 (revised) — Sea Postman: her new call's reporting"
    "\ndelete REP['Star New London'];delete REP['KM Jakarta']; // list 26.11 (revised): both are on the EXPECTED sheet again — their earlier reporting hours no longer stand") + B.s[b:]
a, b = B.line_of("Object.assign(AG,{'Yara J (next call)':'DBC',")
B.s = B.s[:b] + ("\nObject.assign(AG,{'Xin Bo':'Mihir & Company','KM Jakarta':'True Blue','Agia Fotini':'Interocean','New Joyful':'Benline','Team Bravo':'Synergy','El Matador':'DBC','Patmos John':'Cross Trade','Propel Success':'Seascape','Princess Manissa':'Alap Carrier'});"
    "Object.assign(IE,{'Xin Bo':'EXP','KM Jakarta':'EXP','Agia Fotini':'IMP','New Joyful':'IMP','Team Bravo':'IMP','El Matador':'EXP','Patmos John':'EXP','Sea Postman':'EXP','Katerina K':'EXP'}); // list 26.11 (revised)") + B.s[b:]
B.rep("'Star New London':13.5,'Bunun Miracle':9.95,'Tomkar':10.67});", "'Star New London':13.5,'Bunun Miracle':9.95,'Tomkar':10.67,'KM Jakarta':13.3,'Hai Nam 81':12.6});")

# ================= MEETLOG — the meeting of 26 Nov, scored on the call frozen from v277 (board as at 25 Nov 23:39) =================
ML = ("{d:'11-26',at:'11-25 23:39',basis:'list 25.11 (revised) · programme 26.11 · DPR 25.11 · HM signals to the evening sheet of 25 Nov (amended 20:28)',prog:'27.11',"
      "call:[['Star New London','15'],['CD Glory','4'],['Fortunelit','15A']],got:[['Jumbo Kinetic','7'],['Hai Nam 81','15A']],note:'" + q(
      "None of the three. (1) CD GLORY at CJ-4: the board had given her Parvraj's vacant Govt place under circular 5237 (i). The port gave that place to HAI NAM 81 — HP 1 on the list — as \"GOV(30K)\", at CJ-15A, a berth CD Glory could have used: the 30K-quote line stands before SAAGAR. And CJ-4 did not come free — Safi Alfa's list ETC moved to 30 Nov with more cargo declared. "
      "(2) FORTUNELIT at CJ-15A: the berth went to Hai Nam 81. (3) STAR NEW LONDON at CJ-15: Xin Hai Tong 71 is still there — 910 MT a day, about 1 Dec — and Star New London herself is back on the expected sheet. "
      "What the port did instead: the Coastal place the tug Varahi leaves (out 17:30) → JUMBO KINETIC, \"CSTL\", at CJ-7 — the board had held her to CJ-13–16 — and to seat her it shifts Asian Summit CJ-7 → CJ-5 and Blue Shark CJ-5 → CJ-14, both on Gautam Freight's account, and warps Safi Alfa. "
      "Also, outside any programme: CJ-6 went to KATERINA K (GEN 3) at 04:12 on 26 Nov, past GEN 1 and GEN 2 whom the berth does not suit. "
      "Same priority first held where it was tested: Coastal → Coastal. Changes made: the quote line before SAAGAR for a vacant Govt / Coastal place; General to the senior vessel the berth suits.") + "'},")
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")
B.save(); print('saved 74a')
