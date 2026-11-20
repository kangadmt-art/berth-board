#!/usr/bin/env python3
# apply38b — v193 (part 2, logs): UPDATED, CD Glory route notes, snapshot, prediction log, own-vessel log, lesson. argv[1] = UPDATED
import re, sys, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; B = Board(W + 'dpa-berth-board.html'); q = B.q
S = json.load(open(W + 'S193.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
def note_of(label, text):
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "THE ONLY LINE THAT COUNTS FOR HER NOW. SAAGAR group — one bulk and one break-bulk place. Revised list 20.11: Uni Blossom (SGR 1), AG Varvara (2), Xin Hai Tong 71 (3 — project cargo, goes by the project route), CD Glory (4), Dariya Priya (5), African Tiger (6). Uni Blossom takes Rome Trader's place tonight. ML Egret's place — about 24 Nov at the DPR pace, list ETC 28 Nov — is AG Varvara's. Uni Blossom's place is CD Glory's: taken at 5,600 CBM a day (the record average of the completed log vessels; no norm is printed for her yet) Uni Blossom is through about 27 Nov 08:00, and the board counts the place from the evening of the 26th — CJ-14, 26 Nov 22:00. Mihir's own reckoning (20 Nov 17:13) and the timber desk: 26 Nov.")
note_of('General · by seniority', "CLOSED. Mihir (20 Nov 17:13): General goes strictly by seniority — a junior is not given a berth past the vessels senior to her. She is GEN 20; Blue Shark (GEN 2) is first, and some eighteen vessels stand ahead of her. Nothing by this line inside three weeks.")

MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
i = B.s.index("const PRED=["); j = B.s.index("\n];", i); blk = B.s[i:j]
rows = re.findall(r"\['((?:[^'\\]|\\.)*)','([^']*)','([^']*)','((?:[^'\\]|\\.)*)'\]", blk)
fixed = [r for r in rows if not r[3].startswith('board projection') and r[0] != 'Propel Confidence']      # Propel Confidence sailed at 17:00
assert 18 < len(fixed) < 30, len(fixed)
proj = [(q(x['n']), x['b'], nice(x['F']), q('board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else ''))) for x in S if x['F'] <= '11-27 00:00']
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v193) — programme 21.11 and the revised list 20.11, with Mihir's rulings of 16:50 and 17:13 (6.5K / 8K and General strictly by seniority); to be read against the evening signal sheet, DPR 21.11, list 21.11 and programme 22.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % r for r in list(fixed) + proj)) + B.s[j:]

b0 = B.s.index("\n];", B.s.index("const PREDLOG=["))
AT = '11-20 17:13'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
R = "20 Nov 17:13 re-run on Mihir's word — General strictly by seniority — "
new = [
 prow('AG Varvara', R + 'not by General (GEN 16): SAAGAR (SGR 2), CJ-5 when ML Egret\'s place opens at the DPR pace — desk 26 Nov'),
 prow('Blue Shark', R + 'General (GEN 2, the senior-most waiting), CJ-16 after African Hornbill'),
 prow('Zheng Hui', R + 'Govt (DAP — no GP printed yet), CJ-8 after Flag Marina clears'),
 prow('CD Glory', R + 'Mihir & Co — SAAGAR (SGR 4), CJ-14 when Uni Blossom\'s place opens (Uni Blossom taken at 5,600 CBM a day). General and 6.5K / 8K closed by seniority. Mihir\'s reckoning and the desk: 26 Nov'),
 prow('Crystal Land', R + '6.5K / 8K (8K 2), next after Manta Sena — CJ-15 after ML Egret'),
]
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]

g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 17:13 · Mihir — General is by seniority too; his reckoning for her is 26 Nov',exp:'%s',b:'%s',slot:'SAAGAR — CJ-14 about 26 Nov night, when Uni Blossom\\'s place opens · General and 6.5K / 8K CLOSED (seniors ahead in both) · Mihir and the timber desk: 26 Nov',why:'" % (g['F'], g['b']) + q(
 "Mihir (20 Nov 17:13): AG Varvara cannot come in by General on the 21st — many vessels are senior to her; the board's calculation was wrong. And by his reckoning CD Glory berths on the 26th. The board had been letting a junior take a General berth whenever the seniors were bag vessels shut out by the three-bag limit or by the berth — that put AG Varvara (GEN 16) into CJ-5 on the 21st, and with her out of the SAAGAR line CD Glory moved up to 24 Nov. Corrected: General goes strictly by seniority, as 6.5K / 8K does. So AG Varvara waits in the SAAGAR line (SGR 2) and takes ML Egret's place — about 23–24 Nov at the DPR pace, 26 Nov by the desk — and CD Glory (SGR 4; Xin Hai Tong 71, SGR 3, goes by the project route) takes the next one, Uni Blossom's. Uni Blossom berths on the night of 20–21 Nov; taken at 5,600 CBM a day (the record average of the completed log vessels — the list has printed no norm for her yet) she is through about 27 Nov 08:00, and the board counts the place from the evening of the 26th: CJ-14, 26 Nov 22:00, done about 5 Dec. That is Mihir's 26th. Only the SAAGAR line counts for her now: General (GEN 20) and 6.5K / 8K (8K 9) are both closed by seniority. What can still move the date: Uni Blossom's real rate (at ML Egret's 8,000 a day she is through on the 25th, at the 4,600 norm on the 28th), and whether Xin Hai Tong 71 really goes by the project route. Laytime runs out 23 Nov 01:38 — nearly four days on demurrage before she berths. This is the fifth reading today; the last two corrections are Mihir's, and they corrected the board's rules, not the facts.") + "'}") + B.s[i:]

def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 17:13 · Mihir — General is strictly by seniority; CD Glory is the 26th by his reckoning",
 "(1) AG Varvara cannot come in General on the 21st — many vessels are senior to her; the board's calculation is wrong. (2) Laytime — noted. (3) CD Glory comes to the 26th by his reckoning.",
 "Board (v192): CJ-5, free on the night of 21 Nov, goes by General to AG Varvara (GEN 16), because the seniors are bag vessels shut out by the three-bag limit or by the berth; CD Glory then moves up the SAAGAR line to CJ-16 on 24 Nov.",
 "Mihir's word, 20 Nov 17:13. The record agrees with him: the board's General picks have failed for days — AG Varvara for CJ-5 and Safi Alfa for CJ-4 on programmes 19.11 and 20.11, Aboudi D for CJ-3 on programme 21.11 (that berth has stood empty since the morning of the 20th) — while Safi Alfa, GEN 1, waited 32 days for her berth.",
 "The board read \"General by seniority, at most three bag vessels alongside\" (19 Nov) as: skip the seniors that cannot come in and give the berth to the next vessel that fits. The port does not do that — in General a junior does not pass a senior; the berth waits, or goes to another group.",
 "v193: GEN_STRICT — a General berth, and a General cross-fill, is offered only to the senior-most ready vessel still waiting in the General line; if the berth does not suit her or the bag limit keeps her out, General takes nothing there. Result: no General berthing in the window of the 21 Nov meeting (CJ-3 and CJ-5 stand empty in the projection) · Blue Shark (GEN 2) CJ-16 24 Nov · AG Varvara CJ-5 23 Nov 22:00 by SAAGAR (ML Egret's place) · CD GLORY CJ-14 26 Nov 22:00 by SAAGAR (Uni Blossom's place) — Mihir's 26th. Uni Blossom's stay is estimated at the record average of the completed log vessels (5,600 CBM a day) until the list prints her ETC. With the 16:50 ruling, a junior no longer passes a senior in General or in 6.5K / 8K.", "adopted"))
B.save()
