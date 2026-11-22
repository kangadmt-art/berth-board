#!/usr/bin/env python3
# apply59 — v262: HM signal 22 Nov NIGHT sheet, "AMENDMENT & NEW SIGNAL" (dispatched 21:30 / 21:55, Capt Sandeep). Received 23 Nov 02:16, no text.
# Cargo side: Sanghi Sudarshan RT OUT 23:00 (first written 22:20, struck) from 135–141¾; Yuan Hang Wei Ye RT OUT 23:30 from CJ-9; Sand Topic IN o/c on the ebb to 69–77¾.
# Oil side: PVT Aurora RT OUT 02:30 from OJ-2, Rasheeda IN o/c; Bow Fortitude OUT 07:00 from OJ-4, Al Mahbooba IN o/c. DCI Dredge XVII IN 07:00 to mooring buoy 2.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='HM SIGNAL 22 Nov night'); q = B.q
SG = 'HM SIGNAL 22 Nov night sheet, "Amendment & new signal" (disp 21:30 / 21:55)'
B.rep("const NOW=h('11-22 15:39');", "const NOW=h('11-23 02:16');")
B.rep("<i>Signals to</i><b>22 Nov day sheet (disp 0805 / 0825 / 0900)</b>", "<i>Signals to</i><b>22 Nov night sheet (disp 2130 / 2155)</b>")
if B.s.count("const BOARD_SRC='") == 1: B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 22 Nov night sheet, amendment & new signal (disp 2130 / 2155) · ")
# cargo berths
M = "{b:'14',n:'Sanghi Sundarshan',p:[135,141.75]"
B.note_prefix(M, q(SG + ": RT OUT 23:00 on 22 Nov · Capt Sandeep · 135–141¾ → OTB · \"speed 7.0 kts\" (first written 22:20, struck). Four hours ahead of the programme's 03:00 readiness — she lay 19 hours for 4,004 MT of coil.") + " ")
B.sub_entry(M, "t:'11-23 03:00'", "t:'11-22 23:00'")
M = "{b:'9',n:'Yuan Hang Wei Ye (next call)',p:[69,77.25]"
B.note_prefix(M, q(SG + ": RT OUT 23:30 on 22 Nov · Capt Verma · 69–77¼ → OTB. The programme had 17:45; she lay about 34½ hours for 50,455 MT.") + " ")
B.sub_entry(M, "t:'11-22 17:45',est:1", "t:'11-22 23:30'")
M = "{b:'9',n:'Sand Topic',p:[69,77.75]"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt Verma, straight behind Yuan Hang Wei Ye's 23:30 sailing · OTB → 69–77¾ · \"EBB\" — about 01:30 on 23 Nov, est (programme 22.11 had her in behind a 17:45 sailing). Her finish moves by the same hours: about 25 Nov 14:45 at the 20,000 a day assumed.") + " ")
B.sub_entry(M, "f:'11-22 19:45',t:'11-25 09:00'", "f:'11-23 01:30',t:'11-25 14:45'")
# oil jetties
M = "now:{n:'PVT Aurora'"
B.note_prefix(M, q(SG + ": RT OUT 02:30 on 23 Nov · Capt Verma (programme 23.11 had 07:00) → Rasheeda in \"o/c\" behind her, \"speed 6.5 kts\" — about 04:30, est.") + " ")
B.sub_entry(M, "etc:'11-23 07:00'", "etc:'11-23 02:30'")
M = "now:{n:'Bow Fortitude'"
B.note_prefix(M, q(SG + ": OUT 07:00 on 23 Nov · Capt Yadav — as the programme → Al Mahbooba in \"o/c\" behind her, about 09:00, est.") + " ")
M = "{n:'Rasheeda',c:'Chemicals'"
B.sub_entry(M, "rem:'", "rem:'" + q(SG + ": IN \"o/c\" to OJ-2 · Capt Verma, behind PVT Aurora's RT OUT at 02:30 on 23 Nov · \"speed 6.5 kts\" — about 04:30, est. ") )
M = "{n:'Al Mahboobah',c:'Benzene'"
B.sub_entry(M, "rem:'", "rem:'" + q(SG + ": IN \"o/c\" to OJ-4 · Capt Yadav, behind Bow Fortitude's 07:00 on 23 Nov — about 09:00, est. ") )
B.rep("PROGRAMME 23.11 — OJ-2 PVT Aurora out 23 Nov 07:00 (6.5 m) → Rasheeda · OJ-4 Bow Fortitude out 23 Nov 07:00 (7.0 m) → Al Mahboobah · no other oil-jetty move printed',src:'DPA berthing list 21.11.26 (revised) · DPR 22.11 · programme 22.11 · signals to the day sheet of 22 Nov (disp 0805 / 0825 / 0900)',asOf:'11-22 12:18',",
      "HM SIGNAL 22 Nov night (disp 21:30 / 21:55) — OJ-2 PVT Aurora RT OUT 02:30 on 23 Nov → Rasheeda in about 04:30 est · OJ-4 Bow Fortitude out 07:00 → Al Mahboobah in about 09:00 est · PROGRAMME 23.11 prints no other oil-jetty move',src:'DPA berthing list 21.11.26 (revised) · DPR 22.11 · programme 23.11 · signals to the night sheet of 22 Nov (disp 2130 / 2155)',asOf:'11-23 02:16',")
def js(o):
    if isinstance(o, str): return "'" + q(o) + "'"
    return '[' + ','.join(js(x) for x in o) + ']'
MVN = ['HM signal 22 Nov — NIGHT sheet ("Amendment & new signal", dispatched 21:30 / 21:55) · Capt Sandeep · received 23 Nov 02:16 · cargo berths', [
 ['23:00', 'OUT', 'Sanghi Sundarshan', 'CJ-14 · 135–141¾ → OTB', 'Sandeep', '11-22 23:00', 'RT OUT · "speed 7.0 kts" · first written 22:20, struck · programme had 03:00'],
 ['23:30', 'OUT', 'Yuan Hang Wei Ye', 'CJ-9 · 69–77¼ → OTB', 'Verma', '11-22 23:30', 'RT OUT · Gautam Freight berth · programme had 17:45'],
 ['o/c', 'IN', 'Sand Topic', 'OTB → CJ-9 · 69–77¾', 'Verma', '11-23 01:30', 'EBB · behind Yuan Hang Wei Ye — est'],
 ['07:00', 'IN', 'DCI Dredge XVII', 'OTB → Mooring buoy 2', 'Deepak', '11-23 07:00', 'dredger']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
LQN = ['HM signal 22 Nov — NIGHT sheet (dispatched 21:30 / 21:55) · Capt Sandeep · oil-jetty rows', [
 ['02:30', 'OUT', 'PVT Aurora', 'OJ-2 → OTB', 'Verma', '11-23 02:30', 'RT OUT · programme had 07:00'],
 ['o/c', 'IN', 'Rasheeda', 'OTB → OJ-2', 'Verma', '11-23 04:30', '"speed 6.5 kts" — est'],
 ['07:00', 'OUT', 'Bow Fortitude', 'OJ-4 → OTB', 'Yadav', '11-23 07:00', ''],
 ['o/c', 'IN', 'Al Mahboobah', 'OTB → OJ-4', 'Yadav', '11-23 09:00', 'est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n")
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='23 Nov 2026 · 02:19 IST';", B.s, 1)
B.save()
