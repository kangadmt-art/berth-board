#!/usr/bin/env python3
# apply60b — v263 (part 2): own-vessel options refreshed to list 23.11 (CD Glory) and opened for PAIWAN ACE (SGR 6, ready 22 Nov 11:00 — now in the queue).
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]
setline(" routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:3},", " routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:3},note:'" + q(
    "THE ONLY LINE THAT COUNTS FOR HER NOW. A SAAGAR place opens only when a SAAGAR vessel has sailed (Mihir, 22 Nov). List 23.11: AG Varvara (SGR 1), Xin Hai Tong 71 (2 — project cargo, goes by the project route), CD Glory (3), Dariya Priya (4 — working at midstream), African Tiger (5), Paiwan Ace (6). "
    "Two SAAGAR log vessels are alongside. ML Egret at CJ-15: 12,704 CBM left on DPR 23.11, through about 25 Nov 03:45 — her place is AG Varvara's. Uni Blossom at CJ-13: 19,511 CBM left at 8,020 a day, through about 25 Nov 17:20 — her place is CD Glory's, at the same berth about two hours behind her. "
    "Both dates are DPR rates, not programme hours: a slow day on Uni Blossom moves CD Glory by the same hours (the list's permissible time for Uni Blossom runs to 28 Nov 17:58). Her berthing would be programmed at the meeting of 25 Nov. Timber desk (21 Nov): 26 Nov.") + "'},")
setline("  {label:'6.5K / 8K',only:'8K',rk:{'8K':9},", "  {label:'6.5K / 8K',only:'8K',rk:{'8K':8},note:'" + q(
    "CLOSED. Mihir (20 Nov 16:50): CD Glory cannot berth under the 6.5K priority while other vessels are senior to her in it — the place goes by seniority, whichever berth frees first. She is 8K 8 on list 23.11; Manta Sena 1 (takes CJ-1 behind Crystal O, about 24 Nov), Crystal Land 2, Pioneer Fortune 3, Gokova-M 5, Porto Fiscardo 6 and Captainannis L 7 stand ahead. Nothing by this line inside three weeks.") + "'},")
setline("  {label:'General · by seniority',only:'GEN',rk:{GEN:20},", "  {label:'General · by seniority',only:'GEN',rk:{GEN:17},note:'" + q(
    "CLOSED. Mihir (20 Nov 17:13): General goes strictly by seniority — a junior is not given a berth past the vessels senior to her. She is GEN 17 on list 23.11; Blue Shark (GEN 1) is first, and some fifteen vessels stand ahead of her. Nothing by this line inside three weeks.") + "'}]},\n"
    " 'Paiwan Ace':{fixed:[],\n routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:6},note:'" + q(
    "HER LINE. List 23.11 puts her on the waiting sheet (still printed \"PAIWAN ICE\"): reported 22 Nov 00:06, readiness 22 Nov 11:00, SGR 6 · 8K 12. A SAAGAR place opens only when a SAAGAR vessel has sailed. Ahead of her: AG Varvara (1) and CD Glory (3) take the two places that ML Egret and Uni Blossom leave on 25 Nov; Xin Hai Tong 71 (2) goes by the project route; Dariya Priya (4) is discharging at midstream; African Tiger (5) is the next log vessel in line. "
    "Her place is therefore the SECOND one to open after 25 Nov — when AG Varvara (39,113 CBM) or CD Glory (29,158 CBM) finishes — unless Dariya Priya comes off midstream for a berth. The date below is worked out on the vessels ahead at the pace of the log vessels now alongside; it will move with every DPR. Timber desk (21 Nov): 8 Dec.") + "'},\n"
    "  {label:'6.5K / 8K',only:'8K',rk:{'8K':12},note:'" + q(
    "CLOSED for now. The place goes by seniority (Mihir, 20 Nov): she is 8K 12, the last of the line on list 23.11.") + "'}]}};")
B.save()
