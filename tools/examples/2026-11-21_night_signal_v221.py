#!/usr/bin/env python3
# apply47 — v221: HM signal 21 Nov NIGHT sheet (dispatched 19:00, Capt Sandeep) — movements for the night 21/22 Nov and the morning of 22 Nov. Received 21 Nov 20:26.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='HM SIGNAL 21 Nov night'); q = B.q
SG = 'HM SIGNAL 21 Nov night sheet (disp 19:00)'
B.rep("const NOW=h('11-21 16:19');", "const NOW=h('11-21 20:26');")
B.rep("Signals to <b>21 Nov amended sheet (disp 0746 / 0840 / 1257)</b>", "Signals to <b>21 Nov night sheet (disp 1900)</b>")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 21 Nov night sheet (disp 1900) · ")
M = "{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]"
B.note_prefix(M, q(SG + ": IN 10:00 on 22 Nov · Capt Madaan · OTB → 7½–N · FLOOD — about 12:00 alongside. New Bliss leaves the berth at 10:05 (Capt Sachin).") + " ")
B.sub_entry(M, "f:'11-22 12:05'", "f:'11-22 12:00'")
M = "{b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133]"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt Nanda, after Nord Copper's RT OUT at 11:00 on 22 Nov · OTB → 126½–133 · remark \"AIS not working BG\".") + " ")
M = "{b:'14',n:'Sanghi Sundarshan',p:[135,141.75]"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt Sachin, after New Bliss · OTB → 135–141¾ · \"speed 7 kts\". Nord Copper holds these panels till 11:00, so about 13:00 alongside, est.") + " ")
B.sub_entry(M, "f:'11-22 13:15',t:'11-23 13:15'", "f:'11-22 13:00',t:'11-23 13:00'")
B.note_prefix("{b:'14',n:'Nord Copper',nm:23000,p:[126.5,141.75]", q(SG + ": RT OUT 11:00 on 22 Nov · Capt Nanda · 126½–141¾ → OTB — as the programme.") + " ")
B.note_prefix("{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]", q(SG + ": OUT 10:05 on 22 Nov · Capt Sachin · 7½–N → OTB — as the programme.") + " ")
def js(o):
    if isinstance(o, str): return "'" + q(o) + "'"
    return '[' + ','.join(js(x) for x in o) + ']'
MVN = ['HM signal 21 Nov — NIGHT sheet (dispatched 19:00) · Capt Sandeep · received 21 Nov 20:26 · cargo berths', [
 ['10:00', 'SHIFT', 'Flexi 2', 'CJ-12 · 100–109½ → OTB', 'G. Raj', '11-22 10:00', 'agent a/c · container'],
 ['o/c', 'IN', 'TCI Anand', 'OTB → CJ-12 · 101–109½', 'G. Raj', '11-22 12:00', 'FLOOD · "ETA" · container — est'],
 ['10:00', 'OUT', 'TCI Express', 'CJ-11 · 87–95 → OTB', 'Sud', '11-22 10:00', 'container'],
 ['10:05', 'OUT', 'New Bliss', 'CJ-1 · 7½–N → OTB', 'Sachin', '11-22 10:05', 'as programme 22.11'],
 ['o/c', 'IN', 'Sanghi Sundarshan', 'OTB → CJ-14 · 135–141¾', 'Sachin', '11-22 13:00', '"speed 7 kts" · after Nord Copper clears — est'],
 ['10:00', 'IN', 'Crystal O', 'OTB → CJ-1 · 7½–N', 'Madaan', '11-22 12:00', 'FLOOD · 6.5K'],
 ['11:00', 'OUT', 'Nord Copper', 'CJ-14 · 126½–141¾ → OTB', 'Nanda', '11-22 11:00', 'RT OUT'],
 ['o/c', 'IN', 'Tug Sagar 5 + barge Victoria 250', 'OTB → CJ-14 · 126½–133', 'Nanda', '11-22 13:00', '"AIS not working BG" — est']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
LQN = ['HM signal 21 Nov — NIGHT sheet (dispatched 19:00) · Capt Sandeep · oil-jetty rows', [
 ['23:48', 'SHIFT', 'SG Friendship', 'OJ-3 → OTB', 'Sandeep', '11-21 23:48', 'agent a/c'],
 ['o/c', 'IN', 'Hartati', 'OTB → OJ-3', 'Sandeep', '11-22 01:45', 'est'],
 ['02:48', 'OUT', 'Silver Gertrude', 'OJ-7 → OTB', 'Sandeep', '11-22 02:48', 'RT OUT'],
 ['02:30', 'OUT', 'Eva Richway', 'OJ-4 → OTB', 'Bali', '11-22 02:30', 'RT OUT'],
 ['o/c', 'IN', 'Bow Fortitude', 'OTB → OJ-4', 'Bali', '11-22 04:30', 'est'],
 ['05:00', 'OUT', 'Hatnyanawati', 'OJ-2 → OTB', 'Bali', '11-22 05:00', 'RT OUT'],
 ['o/c', 'IN', 'PVT Aurora', 'OTB → OJ-2', 'Bali', '11-22 07:00', 'est'],
 ['06:15', 'IN', 'Ginga Cheetah', 'OTB → OJ-7', 'G. Raj', '11-22 08:15', 'FLOOD'],
 ['07:20', 'OUT', 'Artigo', 'OJ-1 → OTB', 'Sud', '11-22 07:20', ''],
 ['o/c', 'IN', 'Hafnia Ammolite', 'OTB → OJ-1', 'Sud', '11-22 09:20', 'FLOOD · est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n")
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='21 Nov 2026 · 20:30 IST';", B.s, 1)
B.save()
