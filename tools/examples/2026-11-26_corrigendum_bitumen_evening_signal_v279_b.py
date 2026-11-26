#!/usr/bin/env python3
# apply75b — v279: CD Glory's reading after the night papers of 26 Nov.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o): return "'" + q(o) + "'"
e = {'d': '26 Nov 23:10 · HM evening signal (disp 18:10, to 21:00) + corrigendum 26.11.2026', 'exp': '11-27 20:00', 'b': '5',
 'slot': 'SAAGAR (SGR 1) — Asian Summit\'s place; CJ-5, 27 Nov about 20:00 · for the meeting of 27 Nov',
 'why': 'Same reading as the afternoon, two hours later on the clock: Asian Summit has no outward row on programme 27.11, so the board lets her go at the end of that window, 18:00 on 27 Nov, and CD Glory is alongside about two hours after. '
        'NOT KNOWN TONIGHT: whether Asian Summit was shifted CJ-7 → CJ-5 this evening. The night signal sheet starts at 23:00 and has none of the four moves programme 27.11 set for the evening (tug Varahi out, Blue Shark to CJ-14, Asian Summit to CJ-5, Jumbo Kinetic in); they would be on the day sheet\'s afternoon rows, which have not come. If the shift did not happen, she is still at CJ-7 — CD Glory then follows her there or wherever the meeting seats the SAAGAR place. '
        'THE CORRIGENDUM OF 26 NOV (Bitumen berth → 6.5K line, break bulk only) does not move her: she is 8K 5, with four bag vessels ahead for that one berth.'}
k = " 'CD Glory':[\n"; a = B.s.index("const MYLOG={"); i = B.s.index(k, a); j = B.s.index("\n ],", i)
B.s = B.s[:j] + ",\n  {" + ",".join(kk + ":" + js(e[kk]) for kk in ('d', 'exp', 'b', 'slot', 'why')) + "}" + B.s[j:]
B.rep("so the board gives CD Glory CJ-5 about 27 Nov 18:00. ", "so the board gives CD Glory CJ-5 on the evening of 27 Nov (about 20:00). ")
B.save()
