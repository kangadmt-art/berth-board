#!/usr/bin/env python3
# apply84 — v288. Received 27 Nov 23:31: Mihir's answers (from his experienced man) to the 18 questions of 20:41 + three papers (images):
#   HM SIGNAL 27/11/26 "amendment & new signal" (day), dispatch 11:50 / 15:34 · HM SIGNAL 27/11/2026 evening sheet, dispatch 17:27, 18:01, 22:15 (with day rows for 28 Nov)
#   Traffic dept gang / shore-crane allotment sheet, 27-11-2026 3rd shift.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
src = open('/home/claude/work/apply75.py', encoding='utf-8').read()
exec(src[src.index('def js(o):'):src.index('# ================= HEADER')])
SD = 'HM SIGNAL 27 Nov day sheet, amendment & new signal (disp 11:50 / 15:34)'
SG = 'HM SIGNAL 27 Nov evening sheet (disp 17:27, 18:01, 22:15)'
GS = 'GANG SHEET 27 Nov, 3rd shift'
# ================= HEADER =================
B.rep("const NOW=h('11-27 13:58');", "const NOW=h('11-27 23:33');")
B.rep("const UPDATED='27 Nov 2026 · 14:02 IST';", "const UPDATED='27 Nov 2026 · 23:50 IST';")
B.rep("<i>Signals to</i><b>26 Nov evening sheet (disp 1810, to 2100)</b>", "<i>Signals to</i><b>27 Nov evening sheet (disp 1727, to 2215)</b>")
B.rep("HM signal sheets to the evening sheet of 26 Nov (disp 18:10, extended 21:00) ·", "HM signal sheets to the evening sheet of 27 Nov (disp 17:27, extended 22:15) ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 27 Nov evening sheet (disp 1727, to 2215) + day amendment sheet (disp 1150) · gang sheet 27 Nov 3rd shift · Mihir 27 Nov 2331 (answers to the 18 questions) · ")
# ================= V — the four moves happened on the evening of 27 Nov, not 26 Nov =================
LATE = " THE MOVE WAS ON 27 NOV, NOT 26 NOV: the signals of 27 Nov carry it again with today\\'s hours, and the tug was still at 128–134¾ this afternoon. List 27.11 had printed the berths as programmed, not as they stood. "
M = "{b:'14',n:'Tug Varahi + barge AKG 11',p:[128,134.75]"
pre(M, SD + ": OUT 17:30 · Capt Verma · 128–134¾ → OTB · speed 6 kn, by tug Varahi + AKG 11." + LATE); setf(M, t='11-27 17:30')
M = "{b:'5',n:'Blue Shark',p:[32,39.25]"
pre(M, SG + " (and the day sheet): RT SHIFT 20:00 · Capt Bali · 32–39¼ → 128–141 — she stayed at CJ-5 till 20:00 on 27 Nov." + LATE); setf(M, t='11-27 20:00')
M = "{b:'14',n:'Blue Shark',p:[128,141]"
pre(M, SG + ": RT SHIFT 20:00 · Capt Bali · from 32–39¼ → at CJ-14, 128–141, about 21:00 on 27 Nov, est · " + GS + ": at 14, 4 gangs." + LATE); setf(M, f='11-27 21:00')
M = "{b:'7',n:'Asian Summit',nm:16100,p:[50,57]"
pre(M, SG + " (and the day sheet): RT SHIFT 21:00 · Capt Bali · 50–57 → 30½–39¼ — she worked at CJ-7 till 21:00 on 27 Nov." + LATE); setf(M, t='11-27 21:00')
M = "{b:'5',n:'Asian Summit',nm:16100,p:[30.5,39.25]"
pre(M, SG + ": RT SHIFT 21:00 · Capt Bali · from 50–57 → at CJ-5, 30½–39¼, about 22:00 on 27 Nov, est · " + GS + ": at 5, pet coke, 4 gangs." + LATE); setf(M, f='11-27 22:00')
M = "{b:'7',n:'Jumbo Kinetic',p:[52,57]"
pre(M, SG + ": IN \"o/c\" · Capt Karan · OTB → 52–57 · FLOOD (the day sheet had 22:00, Capt Bali) — behind Asian Summit\\'s 21:00 shift → alongside about 23:30 on 27 Nov, est; 844 MT of cranes and packages → about 28 Nov 13:30, est · " + GS + ": at 7, HMC / packages, 2 gangs.")
setf(M, f='11-27 23:30', t='11-28 13:30')
pre("{b:'4',n:'Safi Alfa',nm:3450,p:[21.25,29.5]", SD + ": WARP 16:30 · Capt Verma · 22¾–31 → 21¼–29½ · \"stbd anchor missing\".")
pre("{b:'8',n:'Zheng Hui',p:[58,67.75]", GS + ": printed \"(GL)\" — gearless; 3 new HMC + derricks.")
# ================= LIQ =================
a, b, d, t = bline('OJ-6'); cu = obj(d['now']); assert 'Culture' in cu['n']; mg = take_wait('Maria Glory')
a, b, d, t = bline('OJ-6')
d['prev'] = as_prev(cu, '11-27 12:00', SD + ': OUT 12:00 · Capt Pathak · OJ-6 → OTB (programme: out readiness 27 Nov 12:00)')
d['now'] = as_now(mg, '11-27 23:30', True, SG + ': IN 23:30 · Capt Bali · OTB → OJ-6 · FLOOD — est until the DPR prints the hour'); bput(a, b, d, t)
a, b, d, t = bline('OJ-2'); mh = obj(d['now']); assert 'MC Hera' in mh['n']; bs = take_wait('Bow Saturn')
a, b, d, t = bline('OJ-2')
d['prev'] = as_prev(mh, '11-27 20:30', SG + ': RT OUT 20:30 (20:00 struck) · Capt Karan · OJ-2 → OTB (programme had 22:30)')
d['now'] = as_now(bs, '11-27 23:30', True, SG + ': IN 23:30 · Capt Karan · OTB → OJ-2 — est until the DPR prints the hour'); bput(a, b, d, t)
for bid, nm_, etc, txt in (('OJ-3', 'Ginga Merlin', '11-28 03:00', SG + ': OUT 03:00 on 28 Nov (03:45 struck) · Capt Omesh · OJ-3 → OTB → SC Draco IN "o/c", Capt Omesh'),
                           ('OJ-7', 'Peonia', '11-28 09:30', SG + ' — day signal rows for 28 Nov: RT OUT 09:30 · Capt Mittal · OJ-7 → OTB (programme had 07:30) → Camelia IN "o/c", FLOOD')):
    a, b, d, t = bline(bid); nw = obj(d['now']); assert nm_ in nw['n']; nw['etc'] = js(etc); nw['note'] = "'" + q(txt + ' · ') + nw['note'][1:]; d['now'] = unobj(nw, NOWKEYS); bput(a, b, d, t)
def rem(name, text):
    a, b = B.line_of("  {n:'%s'," % name); i = B.s.index("rem:'", a) + 5; assert i < b; B.s = B.s[:i] + q(text + ' · ') + B.s[i:]
rem('SC Draco', SG + ': IN "o/c" · Capt Omesh · OTB → OJ-3, behind Ginga Merlin\'s 03:00 sailing on 28 Nov → about 05:00, est')
rem('Camelia', SG + ' — day rows for 28 Nov: IN "o/c" · Capt Mittal · OTB → OJ-7 · FLOOD, behind Peonia\'s 09:30 sailing → about 11:30 on 28 Nov, est')
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-27 13:58',",
    lambda m: "const LIQ={prog:'" + q("HM SIGNALS 27 Nov — OJ-6 Culture OUT 12:00 → MARIA GLORY IN 23:30 · OJ-2 MC Hera RT OUT 20:30 → BOW SATURN IN 23:30 · 28 Nov: OJ-3 Ginga Merlin OUT 03:00 → SC Draco o/c · OJ-7 Peonia RT OUT 09:30 → Camelia o/c · ") + m.group(1)
    + "',src:'DPA berthing list 27.11.26 as revised after the meeting · DPR 27.11 · programme 28.11 · signals to the evening sheet of 27 Nov (disp 1727, to 2215)',asOf:'11-27 23:33',", B.s, count=1)
if k != 1: B.die('LIQ head not found')
LQN = ['HM signal 27 Nov — day amendment sheet (disp 11:50) and evening sheet (disp 17:27, 18:01, 22:15) · oil-jetty rows', [
 ['12:00', 'OUT', 'Culture', 'OJ-6 → OTB', 'Pathak', '11-27 12:00', ''],
 ['o/c', 'IN', 'Chemroad Quest', 'OTB → OJ-4', 'Pathak', '11-27 13:30', 'behind Culture — est'],
 ['20:30', 'OUT', 'MC Hera', 'OJ-2 → OTB', 'Karan', '11-27 20:30', 'RT OUT · 20:00 struck'],
 ['23:30', 'IN', 'Maria Glory', 'OTB → OJ-6', 'Bali', '11-27 23:30', 'FLOOD'],
 ['23:30', 'IN', 'Bow Saturn', 'OTB → OJ-2', 'Karan', '11-27 23:30', ''],
 ['03:00', 'OUT', 'Ginga Merlin', 'OJ-3 → OTB', 'Omesh', '11-28 03:00', '03:45 struck'],
 ['o/c', 'IN', 'SC Draco', 'OTB → OJ-3', 'Omesh', '11-28 05:00', 'behind Ginga Merlin — est'],
 ['09:30', 'OUT', 'Peonia', 'OJ-7 → OTB', 'Mittal', '11-28 09:30', 'RT OUT · day signal row for 28 Nov'],
 ['o/c', 'IN', 'Camelia', 'OTB → OJ-7', 'Mittal', '11-28 11:30', 'FLOOD · behind Peonia — est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n")
# ================= MV =================
MVS = ['HM signal 27 Nov — day amendment sheet (disp 11:50 / 15:34) and evening sheet (disp 17:27, 18:01, 22:15) · received 27 Nov 23:31 · cargo berths', [
 ['14:00', 'IN', 'True Mariner', 'OTB → mooring buoy 3', 'Yadav', '11-27 14:00', 'rice bags, midstream'],
 ['14:00', 'IN', 'DP World Thamira', 'OTB → CJ-11 · 88–94½', 'Madaan', '11-27 14:00', 'container · FLOOD · "Bharani" struck out'],
 ['15:00', 'OUT', 'Hui Fa', 'CJ-11 · 87½–95¾ → OTB', 'Verma', '11-27 15:00', 'container'],
 ['15:30', 'OUT', 'Coastal Amigo', 'Barge basin → OTB', 'Pathak', '11-27 15:30', ''],
 ['o/c', 'IN', 'Shree Krishna IX', 'OTB → Barge basin, north side', 'Pathak', '11-27 17:00', 'steel slabs — est'],
 ['16:30', 'WARP', 'Safi Alfa', 'CJ-4 · 22¾–31 → 21¼–29½', 'Verma', '11-27 16:30', 'stbd anchor missing'],
 ['17:30', 'OUT', 'Tug Varahi + AKG 11', 'CJ-14 · 128–134¾ → OTB', 'Verma', '11-27 17:30', 'speed 6 kn'],
 ['20:00', 'SHIFT', 'Blue Shark', 'CJ-5 · 32–39¼ → CJ-14 · 128–141', 'Bali', '11-27 20:00', 'RT'],
 ['21:00', 'SHIFT', 'Asian Summit', 'CJ-7 · 50–57 → CJ-5 · 30½–39¼', 'Bali', '11-27 21:00', 'RT'],
 ['o/c', 'IN', 'Jumbo Kinetic', 'OTB → CJ-7 · 52–57', 'Karan', '11-27 23:30', 'FLOOD · day sheet had 22:00 — est'],
 ['01:30', 'IN', 'Zyra', 'OTB → CJ-12 · 100–109', 'Omesh', '11-28 01:30', 'container · CANCELLED'],
 ['03:00', 'OUT', 'SCI Chennai', 'CJ-12 · 98–110 → OTB', 'Mittal', '11-28 03:00', 'container · CANCELLED — delay in cargo operation']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVS) + ",\n")
# ================= ENGINE — answers of 27 Nov 23:31 =================
B.rep("const BAGB=['1','2','3','4'].concat(CLEAN);      // bags: only CJ-1–4 and CJ-13–16",
      "const BAGB=['1','2','3','4','5'].concat(CLEAN);  // bags: not at CJ-6, 7, 8 (Mihir, 27 Nov 23:31) — so CJ-1 to 5 and CJ-13 to 16; jumbo bags may also work at CJ-6\n"
      "const JUMBO=c=>/jumbo|j[- ]?bag/i.test(c||'');\n"
      "const AGRI=c=>/wheat|rice|sugar|soya|maize|corn|pulses|peas|grain|barley|sorghum|meal\\b/i.test(c||''); // agri cargo: not at CJ-6, 7, 8 (Mihir, 27 Nov 23:31)")
B.rep("  if(!FERT(c))A=A.filter(b=>b!=='6');\n", "  if(!FERT(c)&&!JUMBO(c))A=A.filter(b=>b!=='6'); // jumbo bags can work at CJ-6 (Mihir, 27 Nov 23:31; Katerina K, bentonite J-bags, 26 Nov)\n  if(AGRI(c))A=A.filter(b=>!['6','7','8'].includes(b)||(b==='6'&&JUMBO(c)));\n")
B.rep("if(isBag(c)){const A1=A.filter(b=>BAGB.includes(b));", "if(isBag(c)){const A1=A.filter(b=>BAGB.includes(b)||(b==='6'&&JUMBO(c)));")
B.rep("if(k==='HP'){l=l.filter(w=>!w.noHP", "if(k==='HP'){l=l.filter(w=>(+w.q||0)>=40000) /* only a parcel of 40,000 MT or more qualifies for HP (sequence note + Mihir, 27 Nov 23:31) */.filter(w=>!w.noHP")
# open question answered
B.rep("fix:'The board follows the sequence note (the latest word). OPEN — say if a SAAGAR log or bulk vessel can also stand in a vacant Govt / Coastal place.',st:'open'}",
      "fix:'ANSWERED — Mihir, 27 Nov 23:31: a vacant Govt or Coastal place takes only a SAAGAR PROJECT vessel, or a 30K / 25K / 10K vessel. SAAGAR logs or bulk cannot. A vacant HP place takes only a SAAGAR project vessel — no 30K / 25K / 10K there. (African Hornbill had berthed as SAAGAR (Project) against a vacant Govt place.) The board already runs this way since v287.',st:'adopted'}")
B.save(); print('saved 84')
