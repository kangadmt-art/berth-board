#!/usr/bin/env python3
# apply19o — v173: own-vessel options (CD Glory only — Rome Trader has berthed)
import sys, shutil
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
P = '/home/claude/work/dpa-berth-board.html'; shutil.copy(P, '/home/claude/work/pre19o.html')
B = Board(P); q = B.q
a = B.s.index("const OPTS={'CD Glory':{fixed:[],"); e = B.s.index("const OPTRES=", a)
N1 = "SAAGAR group — one bulk and one break-bulk place. Both changed hands on 18 Nov: Rome Trader (bulk) took CJ-13 and ML Egret (logs) CJ-15, where she stays about twelve days at the norm. List 18.11 prints the line: Uni Blossom (SGR 1), African Hornbill (2 — windmill blades, a project parcel), AG Varvara (3), Xin Hai Tong 71 (4 — project cargo), CD Glory (5), Dariya Priya (7). No bulk vessel is ranked in SAAGAR now, so when Rome Trader finishes, her place goes to the first log vessel — Uni Blossom. CD Glory's turn by this line comes only after the log vessels ahead of her have each had a berth: the end of the month at the earliest."
N2 = "PRINTED NOW — 8K 8, on the list revised after the 18 Nov meeting. One berth at a time: New Bliss has it at CJ-1 till about 22 Nov (list ETC 22 Nov 10:05). Ahead of her in this line: Crystal Land (8K 1 — loads too deep for CJ-1 to CJ-5, she needs a clean berth), Uni Blossom (3 — SAAGAR is likely to take her first), Tan Bin 259 (4 — finishing at the mooring), Gokova-M (5 — clay, CJ-7 / CJ-8 only), Porto Fiscardo (6 — rice bags, 190 m, asks for CJ-1 to CJ-4) and Nord Copper (7 — salt, clean berths only). Whichever of them is given the place when New Bliss leaves holds it for days; CD Glory then waits for the turn after that."
N3 = "The General queue — GEN 22 on list 18.11. CJ-1 suits few of the vessels ahead of her: bag vessels are held by the limit of three at a time, and the deep-loading ones cannot use it. That is how the board comes to seat her at CJ-1 when New Bliss leaves — a soft date: it holds only if no priority vessel is given the berth and New Bliss is out by her list ETC. The timber desk says 25 Nov."
new = ("const OPTS={'CD Glory':{fixed:[],\n routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:5},note:'" + q(N1) + "'},\n"
       "  {label:'6.5K / 8K',only:'8K',rk:{'8K':8},note:'" + q(N2) + "'},\n"
       "  {label:'General · by seniority',only:'GEN',rk:{GEN:22},note:'" + q(N3) + "'}]}};\n")
B.s = B.s[:a] + new + B.s[e:]
B.save()
