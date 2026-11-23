#!/usr/bin/env python3
# apply63 — v267: HM signal 23 Nov EVENING sheet (dispatched 16:25, Capt Madaan). Received 23 Nov 16:41, an image with no text.
# 14 rows — the night's moves that programme 24.11 had printed without hours, now with a pilot and an hour each:
#   Sachin : 18:00 IN Blue Shark OTB → 32½–40
#   Bali   : 18:30 RT OUT Vishva Bandhan 33¼–41½ · 21:00 RT OUT Flag Marina 56¾–67¼ · o/c IN Gokova-M → 50½–57 "FLOOD" · o/c SHIFT Hafnia Ammolite OJ-1 → OJ-3 (red remark)
#   G. Raj : 20:00 SHIFT Parvraj 43–51¼ → 41¼–49½ "PORT C" · 21:15 IN Horizon Chaser ("ETA") → 17½–21¾ · 23:45 OUT Belmoira 160½–171¾ · o/c IN Ocean Kudos → 159¼–171¾
#   Sud    : 23:00 OUT Al Hadbaa 88–94½ (container) · o/c IN DP World Godavari ("ETA") → 87–97½ "FLOOD"
#   Karan  : 23:00 RT OUT Hartati OJ-3 · o/c IN Zheng Hui → 58–67¾ · 05:14 RT OUT Ginga Cheetah OJ-7
# The board's conventions: an IN hour is the pilot boarding, alongside about 2 h later; "o/c" = about 2 h behind that pilot's previous move. All est.
# What changes against programme 24.11 as entered at v264: Gokova-M comes BEFORE Zheng Hui (23:00 / 01:00 — the board had them the other way round),
# Belmoira leaves 23:45 (programme readiness 20:28) so Ocean Kudos is alongside about 01:45 on the 24th (board had 22:30), Horizon Chaser about 23:15 (22:00),
# Blue Shark about 20:00 (20:30).
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='HM SIGNAL 23 Nov evening'); q = B.q
SG = 'HM SIGNAL 23 Nov evening sheet (disp 16:25)'
B.rep("const NOW=h('11-23 14:10');", "const NOW=h('11-23 16:41');")
B.rep("<i>Signals to</i><b>23 Nov day sheet (disp 0815)</b>", "<i>Signals to</i><b>23 Nov evening sheet (disp 1625)</b>")
B.rep("HM signal sheets to the day sheet of 23 Nov (disp 08:15) · timber desk sheet", "HM signal sheets to the evening sheet of 23 Nov (disp 16:25) · timber desk sheet")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 23 Nov evening sheet (disp 1625) · ")

# ---- cargo berths
M = "{b:'5',n:'Blue Shark',p:[32.5,40]"
B.note_prefix(M, q(SG + ": IN 18:00 · Capt Sachin · OTB → 32½–40 — the pilot boards at 18:00, half an hour before Vishva Bandhan's ready time; alongside about 20:00, est (the board had 20:30). Her finish moves with it: about 30 Nov 15:00, est.") + " ")
B.sub_entry(M, "f:'11-23 20:30',t:'11-30 15:30',est:1", "f:'11-23 20:00',t:'11-30 15:00',est:1")
M = "{b:'5',n:'Vishva Bandhan',nm:8050"
B.note_prefix(M, q(SG + ": RT OUT 18:30 · Capt Bali · 33¼–41½ → OTB — the programme's hour, now with a pilot.") + " ")
M = "{b:'7',n:'Flag Marina',nm:42500"
B.note_prefix(M, q(SG + ": RT OUT 21:00 · Capt Bali · 56¾–67¼ → OTB — the programme's hour. Behind her the same pilot brings Gokova-M in (\"o/c\", on the flood); Zheng Hui follows with Capt Karan.") + " ")
M = "{b:'7',n:'Gokova-M',nm:50000"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt Bali, straight behind Flag Marina's 21:00 · OTB → 50½–57 · \"FLOOD\" (high water 02:00 on 24 Nov) — about 23:00 on 23 Nov, est. She comes BEFORE Zheng Hui; the board had put her second, about 01:00. Her finish moves two hours earlier: about 25 Nov 01:15, est.") + " ")
B.sub_entry(M, "f:'11-24 01:00',t:'11-25 03:15',est:1", "f:'11-23 23:00',t:'11-25 01:15',est:1")
M = "{b:'6',n:'Parvraj',nm:14950,p:[41.25,49.5]"
B.note_prefix(M, q(SG + ": SHIFT 20:00 · Capt G. Raj · 43–51¼ → 41¼–49½ · \"PORT C\" — the night shifting of the programme, an hour before Flag Marina sails.") + " ")
M = "{b:'3',n:'Horizon Chaser',p:[17.5,21.75]"
B.note_prefix(M, q(SG + ": IN 21:15 · Capt G. Raj · \"ETA\" · OTB → 17½–21¾ — the pilot boards at 21:15; alongside about 23:15, est (the board had 22:00 from the programme's ETA of 20:00). Out about 24 Nov 23:15 on the 24 hours of her last call, est.") + " ")
B.sub_entry(M, "f:'11-23 22:00',t:'11-24 22:00',est:1", "f:'11-23 23:15',t:'11-24 23:15',est:1")
M = "{b:'15A',n:'Belmoira',nm:30000"
B.note_prefix(M, q(SG + ": OUT 23:45 · Capt G. Raj · 160½–171¾ → OTB — three and a quarter hours after the programme's readiness of 20:28 (the DPR rate gave about 22:20 for the last of her salt). Ocean Kudos comes in behind her with the same pilot.") + " ")
B.sub_entry(M, "t:'11-23 20:28'", "t:'11-23 23:45',lt:'11-23 20:28'")
M = "{b:'15A',n:'Ocean Kudos',nm:30000"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt G. Raj, straight behind Belmoira's 23:45 · OTB → 159¼–171¾ — about 01:45 on 24 Nov, est (the board had 22:30 on the 23rd). 70,190 MT at her 30,000 quote → about 26 Nov 11:55, est.") + " ")
B.sub_entry(M, "f:'11-23 22:30',t:'11-26 08:40',est:1", "f:'11-24 01:45',t:'11-26 11:55',est:1")
M = "{b:'8',n:'Zheng Hui',p:[58,67.75]"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt Karan, behind his 23:00 sailing of Hartati from OJ-3 · OTB → 58–67¾ — about 01:00 on 24 Nov, est (the board had 23:00 on the 23rd). She comes AFTER Gokova-M. 66,000 MT at the DAP norm → about 28 Nov 16:00, est.") + " ")
B.sub_entry(M, "f:'11-23 23:00',t:'11-28 13:55',est:1", "f:'11-24 01:00',t:'11-28 15:55',est:1")

# ---- oil jetties
M = "now:{n:'Hartati'"
B.note_prefix(M, q(SG + ": RT OUT 23:00 · Capt Karan · OJ-3 → OTB — the programme's hour.") + " · ")
M = "now:{n:'Hafnia Ammolite'"
B.note_prefix(M, q(SG + ": SHIFT \"o/c\" · Capt Bali · OJ-1 → OJ-3, after he has berthed Gokova-M — about 01:00 on 24 Nov, est (Hartati clears OJ-3 at 23:00). A red remark over the row, hard to read — it looks like \"agent attendance\".") + " · ")
M = "now:{n:'Ginga Cheetah'"
B.note_prefix(M, q(SG + ": RT OUT 05:14 on 24 Nov · Capt Karan · OJ-7 → OTB — the programme's hour.") + " · ")
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-23 14:10',",
    lambda m: "const LIQ={prog:'" + q("HM SIGNAL 23 Nov evening (disp 16:25) — OJ-3 Hartati RT OUT 23:00 → Hafnia Ammolite SHIFTS OJ-1 → OJ-3 \"o/c\", about 01:00 on 24 Nov est · OJ-7 Ginga Cheetah RT OUT 24 Nov 05:14 · no row yet for Bogazici, Sriwangi V or Rasheeda · ") + m.group(1)
    + "',src:'DPA berthing list 23.11.26 as revised after the meeting · DPR 23.11 · programme 24.11 · signals to the evening sheet of 23 Nov (disp 1625)',asOf:'11-23 16:41',", B.s, count=1)
if k != 1: B.die('LIQ head not found')

def js(o):
    if isinstance(o, str): return "'" + q(o) + "'"
    return '[' + ','.join(js(x) for x in o) + ']'
MVN = ['HM signal 23 Nov — evening sheet (dispatched 16:25) · Capt Madaan · received 23 Nov 16:41 · cargo berths', [
 ['18:00', 'IN', 'Blue Shark', 'OTB → CJ-5 · 32½–40', 'Sachin', '11-23 20:00', 'pilot boards 18:00 · alongside about 20:00, est · behind Vishva Bandhan'],
 ['18:30', 'OUT', 'Vishva Bandhan', 'CJ-5 · 33¼–41½ → OTB', 'Bali', '11-23 18:30', 'RT OUT · as the programme'],
 ['20:00', 'SHIFT', 'Parvraj', 'CJ-6 · 43–51¼ → 41¼–49½', 'G. Raj', '11-23 20:00', '"PORT C" · room for Gokova-M at 50½–57'],
 ['21:00', 'OUT', 'Flag Marina', 'CJ-7 / 8 · 56¾–67¼ → OTB', 'Bali', '11-23 21:00', 'RT OUT · as the programme'],
 ['21:15', 'IN', 'Horizon Chaser', 'OTB → CJ-3 · 17½–21¾', 'G. Raj', '11-23 23:15', '"ETA" · pilot boards 21:15 · alongside about 23:15, est · bitumen, space account'],
 ['o/c', 'IN', 'Gokova-M', 'OTB → CJ-7 · 50½–57', 'Bali', '11-23 23:00', 'FLOOD · behind Flag Marina — est · HP(50K)'],
 ['23:45', 'OUT', 'Belmoira', 'CJ-15A · 160½–171¾ → OTB', 'G. Raj', '11-23 23:45', 'programme had 20:28'],
 ['o/c', 'IN', 'Zheng Hui', 'OTB → CJ-8 · 58–67¾', 'Karan', '11-24 01:00', 'behind his 23:00 from OJ-3 — est · Govt'],
 ['o/c', 'IN', 'Ocean Kudos', 'OTB → CJ-15A · 159¼–171¾', 'G. Raj', '11-24 01:45', 'behind Belmoira — est · 24HRS(30K)'],
 ['23:00', 'OUT', 'Al Hadbaa', 'CJ-11 · 88–94½ → OTB', 'Sud', '11-23 23:00', 'container'],
 ['o/c', 'IN', 'DP World Godavari', 'OTB → CJ-11 · 87–97½', 'Sud', '11-24 01:00', '"ETA" · FLOOD · container · behind Al Hadbaa — est'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Sachin 16:30–17:30 · Capt Sud 21:30–22:30 · Capt Karan 03:30–04:30', '—', '11-24 04:30', '']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
LQN = ['HM signal 23 Nov — evening sheet (dispatched 16:25) · Capt Madaan · oil-jetty rows', [
 ['23:00', 'OUT', 'Hartati', 'OJ-3 → OTB', 'Karan', '11-23 23:00', 'RT OUT · as the programme'],
 ['o/c', 'SHIFT', 'Hafnia Ammolite', 'OJ-1 → OJ-3', 'Bali', '11-24 01:00', 'after Gokova-M — est · red remark, hard to read ("agent attendance"?)'],
 ['05:14', 'OUT', 'Ginga Cheetah', 'OJ-7 → OTB', 'Karan', '11-24 05:14', 'RT OUT · as the programme']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n")
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='23 Nov 2026 · 16:45 IST';", B.s, count=1)
B.save()
