# v260 (display part) — the meeting section shows the priority each berthed vessel holds (as the list prints it) and where her place goes;
# our vessel's log gets the new reading; stamp.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
JS = open('/home/claude/work/mtg/meetboard4.js', encoding='utf-8').read()
CSS = open('/home/claude/work/mtg/meetboard4.css', encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)
a = s.index('// ---- NEXT MEETING, berth by berth'); b = s.index('function preview(){\n', a); s = s[:a] + JS + s[b:]
a = s.index('/* v257 Meeting page'); b = s.index('</style>', a); s = s[:a] + CSS + s[b:]
rep("AG Varvara to CJ-5 on the night of the 24th. Nothing is programmed for CD Glory yet.'}",
    "AG Varvara to CJ-5 on the night of the 24th. Nothing is programmed for CD Glory yet.'},\n"
    "  {d:'22 Nov 18:12 · Mihir — a place is free only when its vessel has sailed',exp:'11-26 07:25',b:'13',slot:'SAAGAR (SGR 3) — CJ-13, 26 Nov about 07:30, behind Uni Blossom',why:'Ten hours later, and CJ-13 instead of CJ-14. Mihir (22 Nov 18:09) withdrew the rule of 1 and 7 Nov under which a place was given out again while its vessel was still alongside. A SAAGAR place now opens only when a SAAGAR vessel has sailed. ML Egret goes about 25 Nov 09:00 — that place is AG Varvara\\'s (SGR 1), CJ-5 about 25 Nov 14:00. Uni Blossom goes about 26 Nov 05:30 — that place is CD Glory\\'s, at the same berth, two hours behind her (SAAGAR for SAAGAR). Both sailings are worked out from the DPR rate; a slow day on Uni Blossom moves CD Glory by the same hours. Nothing is programmed for CD Glory yet.'}")
rep("const UPDATED='22 Nov 2026 · 18:03 IST';", "const UPDATED='22 Nov 2026 · 18:12 IST';")
open(P, 'w', encoding='utf-8').write(s)
print('v260 display applied', len(s))
