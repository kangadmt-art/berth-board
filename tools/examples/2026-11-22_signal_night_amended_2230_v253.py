#!/usr/bin/env python3
# apply50 — v253: HM signal 21 Nov NIGHT sheet, re-issued as "AMENDMENT & NEW SIGNAL" (dispatched 22:30, Capt Sandeep). Received 22 Nov 00:26.
# Changes against the 19:00 sheet: Nord Copper OUT and Sanghi Sudarshan IN moved up to the night (o/c behind SG Friendship 23:15 and Hartati);
# tug Sagar 5 + barge IN moved up behind Silver Gertrude (04:00); SG Friendship 23:15 (was 23:48); Silver Gertrude OUT 04:00 (was 02:48);
# Ginga Cheetah IN behind Tan Binh 259 (06:00, mooring buoy 3 — new row); New Bliss OUT / Crystal O IN are NOT on the amended sheet → kept, open check.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='HM SIGNAL 21 Nov night amended'); q = B.q
SG = 'HM SIGNAL 21 Nov night sheet, AMENDED (disp 22:30)'
B.rep("const NOW=h('11-21 20:26');", "const NOW=h('11-22 00:26');")
B.rep("<i>Signals to</i><b>21 Nov night sheet (disp 1900)</b>", "<i>Signals to</i><b>21 Nov night sheet, amended (disp 2230)</b>")
B.rep("night (disp 19:00) · DPR 21.11", "night (disp 19:00) and the night sheet as amended (disp 22:30) · DPR 21.11")
if B.s.count("const BOARD_SRC='") == 1: B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 21 Nov night sheet amended (disp 2230) · ")
M = "{b:'14',n:'Nord Copper',nm:23000,p:[126.5,141.75]"
B.note_prefix(M, q(SG + ": OUT \"o/c\" · Capt Sandeep, behind SG Friendship's shift (23:15) and Hartati's berthing — about 03:15 on 22 Nov, est (her list ETC is 03:03). The 19:00 sheet had RT OUT 11:00.") + " ")
B.sub_entry(M, "t:'11-22 11:00'", "t:'11-22 03:15',est:1")
M = "{b:'14',n:'Sanghi Sundarshan',p:[135,141.75]"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt Sandeep, straight behind Nord Copper's sailing · OTB → 135–141¾ · \"speed 7 kts\" — about 05:15 on 22 Nov, est (the 19:00 sheet: behind New Bliss, about 13:00).") + " ")
B.sub_entry(M, "f:'11-22 13:00',t:'11-23 13:00'", "f:'11-22 05:15',t:'11-23 05:15'")
M = "{b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133]"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt G. Raj, behind Silver Gertrude's RT OUT at 04:00 · OTB → 126½–133 · \"AIS not working BG\" — about 06:00 on 22 Nov, est (the 19:00 sheet: behind Nord Copper's 11:00, about 13:00).") + " ")
B.sub_entry(M, "f:'11-22 13:00',t:'11-23 21:00'", "f:'11-22 06:00',t:'11-23 14:00'")
NR = q(SG + ": her row is NOT on the amended sheet. The 19:00 sheet had %s; Capt Sachin now takes TCI Express out at 10:00. Time kept as the 19:00 sheet and programme 22.11 — the day sheet of 22 Nov will show it (open check).") + " "
B.note_prefix("{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]", NR % "OUT 10:05 (Capt Sachin)")
B.note_prefix("{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]", NR % "IN 10:00 (Capt Madaan)")
# oil jetties
M = "now:{n:'SG Friendship'"
B.note_prefix(M, q(SG + ": SHIFT to OTB 23:15 on 21 Nov (was 23:48) · Capt Sandeep · agent a/c → Hartati in behind her.") + " ")
B.sub_entry(M, "etc:'11-21 23:48'", "etc:'11-21 23:15'")
M = "now:{n:'Silver Gertrude'"
B.note_prefix(M, q(SG + ": RT OUT 04:00 on 22 Nov (was 02:48) · Capt G. Raj → Ginga Cheetah in on the flood behind Tan Binh 259 (06:00, Capt Nanda), about 08:00 est.") + " ")
B.sub_entry(M, "etc:'11-22 02:48'", "etc:'11-22 04:00'")
def js(o):
    if isinstance(o, str): return "'" + q(o) + "'"
    return '[' + ','.join(js(x) for x in o) + ']'
MVN = ['HM signal 21 Nov — NIGHT sheet AMENDED ("Amendment & new signal", dispatched 22:30) · Capt Sandeep · received 22 Nov 00:26 · cargo berths', [
 ['o/c', 'OUT', 'Nord Copper', 'CJ-14 · 126½–141¾ → OTB', 'Sandeep', '11-22 03:15', 'behind SG Friendship (23:15) and Hartati · was RT OUT 11:00 — est'],
 ['o/c', 'IN', 'Sanghi Sundarshan', 'OTB → CJ-14 · 135–141¾', 'Sandeep', '11-22 05:15', '"speed 7 kts" · behind Nord Copper — est'],
 ['o/c', 'IN', 'Tug Sagar 5 + barge Victoria 250', 'OTB → CJ-14 · 126½–133', 'G. Raj', '11-22 06:00', '"AIS not working BG" · behind Silver Gertrude 04:00 — est'],
 ['06:00', 'OUT', 'Tan Binh 259', 'Mooring buoy 3 → OTB', 'Nanda', '11-22 06:00', 'new on this sheet'],
 ['10:00', 'SHIFT', 'Flexi 2', 'CJ-12 · 100–109½ → OTB', 'Sud', '11-22 10:00', 'agent a/c · container'],
 ['o/c', 'IN', 'TCI Anand', 'OTB → CJ-12 · 101–109½', 'Sud', '11-22 12:00', 'FLOOD · "ETA" · container — est'],
 ['10:00', 'OUT', 'TCI Express', 'CJ-11 · 87–95 → OTB', 'Sachin', '11-22 10:00', 'container']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
LQN = ['HM signal 21 Nov — NIGHT sheet AMENDED (dispatched 22:30) · Capt Sandeep · oil-jetty rows', [
 ['23:15', 'SHIFT', 'SG Friendship', 'OJ-3 → OTB', 'Sandeep', '11-21 23:15', 'agent a/c · was 23:48'],
 ['o/c', 'IN', 'Hartati', 'OTB → OJ-3', 'Sandeep', '11-22 01:15', 'est'],
 ['02:30', 'OUT', 'Eva Richway', 'OJ-4 → OTB', 'Bali', '11-22 02:30', 'RT OUT'],
 ['o/c', 'IN', 'Bow Fortitude', 'OTB → OJ-4', 'Bali', '11-22 04:30', 'est'],
 ['04:00', 'OUT', 'Silver Gertrude', 'OJ-7 → OTB', 'G. Raj', '11-22 04:00', 'RT OUT · was 02:48'],
 ['05:00', 'OUT', 'Hatnyanawati', 'OJ-2 → OTB', 'Bali', '11-22 05:00', 'RT OUT'],
 ['o/c', 'IN', 'PVT Aurora', 'OTB → OJ-2', 'Bali', '11-22 07:00', 'est'],
 ['07:20', 'OUT', 'Artigo', 'OJ-1 → OTB', 'G. Raj', '11-22 07:20', ''],
 ['o/c', 'IN', 'Ginga Cheetah', 'OTB → OJ-7', 'Nanda', '11-22 08:00', 'FLOOD · behind Tan Binh 259 (06:00) — est'],
 ['o/c', 'IN', 'Hafnia Ammolite', 'OTB → OJ-1', 'G. Raj', '11-22 09:20', 'FLOOD · est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n")
LRN = " {d:'22 Nov 00:26 · New Bliss out / Crystal O in at CJ-1 — not on the amended night sheet',v:'" + q("The 19:00 sheet had New Bliss OUT 10:05 (Capt Sachin) and Crystal O IN 10:00 (Capt Madaan) on 22 Nov. The sheet re-issued at 22:30 (\"Amendment & new signal\") carries neither row; Capt Sachin now has TCI Express at 10:00.") + "',exp:'" + q("Board keeps both as the 19:00 sheet and programme 22.11: New Bliss out 22 Nov 10:05, Crystal O alongside about 12:00.") + "',act:'" + q("Not known yet — the day sheet of 22 Nov will show it.") + "',why:'" + q("Either the two moves were left for the day sheet, or New Bliss is not finishing by 10:05 (DPR 21.11: 6,072 MT left at 0700 on the 21st — about 05:40 on the 22nd at that pace). If she is late, Crystal O is late by the same hours.") + "',st:'open'},\n"
B.rep("const LEARN=[\n", "const LEARN=[\n" + LRN)
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='22 Nov 2026 · 00:35 IST';", B.s, 1)
B.save()
