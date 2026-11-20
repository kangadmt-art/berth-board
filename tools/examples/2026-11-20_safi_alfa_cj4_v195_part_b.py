#!/usr/bin/env python3
# apply40b — v195 (part 2, logs). argv[1] = UPDATED
import re, sys, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; B = Board(W + 'dpa-berth-board.html'); q = B.q
S = json.load(open(W + 'S195.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
B.rep("26 Nov about 22:00; the berth on today\\'s reading is CJ-4, behind whoever takes it now.", "CJ-14, 26 Nov about 22:00.")
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
i = B.s.index("const PRED=["); j = B.s.index("\n];", i); blk = B.s[i:j]
rows = re.findall(r"\['((?:[^'\\]|\\.)*)','([^']*)','([^']*)','((?:[^'\\]|\\.)*)'\]", blk)
fixed = [r for r in rows if not r[3].startswith('board projection')]
assert len(fixed) == 20, len(fixed)
k = [r[0] for r in fixed].index('Woohyun Dream')
fixed.insert(k + 1, (q('Safi Alfa'), '4', '20 Nov 23:00', q('Mihir, 20 Nov 20:22: berths at CJ-4 under General (GEN 1) — the hour is the board\'s estimate')))
proj = [(q(x['n']), x['b'], nice(x['F']), q('board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else ''))) for x in S if x['F'] <= '11-27 00:00']
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v195) — as v194, with Mihir's word of 20:22: Safi Alfa berths at CJ-4 under General; to be read against DPR 21.11, list 21.11 and programme 22.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % r for r in list(fixed) + proj)) + B.s[j:]
b0 = B.s.index("\n];", B.s.index("const PREDLOG=["))
AT = '11-20 20:22'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
R = "20 Nov 20:22 re-run on Mihir's word (Safi Alfa berths at CJ-4 under General) — "
new = [
 " {v:'Safi Alfa',predAt:'%s',pb:'4',pt:'11-20 23:00',ab:'',at:'',src:'prog',note:'%s'}" % (AT, q("Mihir, 20 Nov 20:22 — berths at CJ-4 under General; the hour is the board's estimate; reading, not scored")),
 prow('Manta Sena', R + '6.5K / 8K (8K 1), back to CJ-1 behind New Bliss'),
 prow('Blue Shark', R + 'General (GEN 2, senior-most once Safi Alfa is in), CJ-16 after African Hornbill'),
 prow('CD Glory', R + 'Mihir & Co — SAAGAR (SGR 4), CJ-14 when Uni Blossom\'s place opens. Date unchanged: 26 Nov night'),
 prow('Crystal Land', R + '6.5K / 8K (8K 2), after Manta Sena — CJ-15 after ML Egret'),
]
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]
g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 20:22 · Mihir — Safi Alfa berths at CJ-4 under General',exp:'%s',b:'%s',slot:'SAAGAR — CJ-14, 26 Nov about 22:00, when Uni Blossom\\'s place opens · General and 6.5K / 8K closed · Mihir and the timber desk: 26 Nov',why:'" % (g['F'], g['b']) + q(
 "Mihir confirms that Safi Alfa berths at CJ-4 under General. That puts Manta Sena back at CJ-1 behind New Bliss and the board's berth for CD Glory back at CJ-14. Her date has not moved through either reading: the night of 26 Nov, on Uni Blossom's place in the SAAGAR line.") + "'}") + B.s[i:]
B.save()
