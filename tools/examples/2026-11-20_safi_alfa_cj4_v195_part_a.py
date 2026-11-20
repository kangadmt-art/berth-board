#!/usr/bin/env python3
# apply40a — v195 (part 1): Mihir (20 Nov 20:22) — "Yes, CJ-4 pe Safi Alfa General me berth hoga." Safi Alfa goes back to CJ-4 as a fixed berth entry (General, GEN 1).
# The hour is on no paper: entered as the night of 20–21 Nov, about 23:00, est. Lesson: a row that is merely ABSENT from an amended signal sheet is not cancelled.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
B.rep("const NOW=h('11-20 20:11');", "const NOW=h('11-20 20:22');")
B.wdel('Safi Alfa')
a, b = B.line_of(" {b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75],")
B.s = B.s[:b + 1] + " " + js({'b': '4', 'n': 'Safi Alfa', 'nm': 3000, 'p': [23, 31.75], 'c': 'Rice bags', 'q': 24750, 'u': 'MT', 'cat': 'GEN', 'f': '11-20 23:00', 't': '11-29 05:00', 'est': 1,
    'note': 'MIHIR (20 Nov 20:22): "Yes — CJ-4 pe Safi Alfa General me berth hoga." She berths at CJ-4 under GENERAL (GEN 1, the senior vessel of the line) behind Propel Confidence, which was shifted to OTB at 17:00. The HOUR is on no paper — the 12:40 dispatch had her IN "o/c" at 23–31¾ (Capt G. Raj), the sheet as amended at 14:00 does not carry the row, programme 21.11 has no CJ-04 row — so the night of 20–21 Nov, about 23:00, is the board\'s estimate; DPR 21.11 will give the made-fast hour. Rice bags, 24,750 MT still to load of 32,100 · 189.99 m · no norm printed yet — about 3,000 a day assumed, to about 29 Nov · agent ACT Infraport'}) + ",\n" + B.s[b + 1:]
B.note_prefix("{b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75]", q("MIHIR (20 Nov 20:22): Safi Alfa DOES berth at CJ-4 behind her, under General — the missing row on the amended sheet was not a cancellation.") + " ")
B.rep("  got:[['Parvraj','6'],['Flag Marina','7'],['Yuan Hang Wei Ye','9'],['Uni Blossom','13']],", "  got:[['Parvraj','6'],['Flag Marina','7'],['Yuan Hang Wei Ye','9'],['Uni Blossom','13'],['Safi Alfa','4','signal']],")
B.rep("Nobody was sent to CJ-3. Safi Alfa (GEN 1) was signalled into CJ-4 at 12:40, but the row is gone from the sheet as amended at 14:00 — not counted.'},",
      "Nobody was sent to CJ-3. Safi Alfa (GEN 1) goes into CJ-4 under General — signalled at 12:40, absent from the sheet as amended at 14:00, confirmed by Mihir at 20:22.'},")
B.rep("['—','—','No longer on the sheet','Safi Alfa IN at 23–31¾ · Konrad OUT from 101–109 (both on the 12:40 dispatch, Capt G. Raj)','—','11-20 20:11','']",
      "['—','—','Not on this sheet','Safi Alfa IN at 23–31¾ · Konrad OUT from 101–109 (both on the 12:40 dispatch, Capt G. Raj)','—','11-20 20:11','" + q("Mihir, 20:22: Safi Alfa WILL berth at CJ-4 under General — a row missing from an amended sheet is not a cancellation") + "']")
# LEARN — the question is answered
B.rep("If Mihir says Safi Alfa is for CJ-4, Manta Sena goes back to CJ-1 behind New Bliss. CD Glory\\'s date does not move (26 Nov night).',st:'open'},",
      "If Mihir says Safi Alfa is for CJ-4, Manta Sena goes back to CJ-1 behind New Bliss. CD Glory\\'s date does not move (26 Nov night). ANSWERED (Mihir, 20 Nov 20:22): YES — Safi Alfa berths at CJ-4 under General. v195: she is back at CJ-4 as a fixed entry (hour estimated, about 23:00 on the 20th) and in the 20 Nov meeting count; Manta Sena returns to CJ-1 behind New Bliss. LESSON: a row that is merely ABSENT from an amended signal sheet is not cancelled — Konrad\\'s outward row was absent too, and Flexi-2 took her berth at 16:45. Only a struck-out row is a cancellation; when the papers fall silent on a berthing, ask before taking it off.',st:'closed'},")
B.save()
