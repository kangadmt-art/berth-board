#!/usr/bin/env python3
# apply23b — v177 (part 2): snapshot, logs, own-vessel option notes after Mihir's four answers. argv[1] = UPDATED.
import re, sys, json, shutil
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'pre23b.html')
B = Board(P); q = B.q
S = json.load(open(W + 'S177.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
# ---- PRED (the v176 list of fixed rows; HN Doris and African Hornbill now with Mihir's word)
s22 = open(W + 'apply22b.py', encoding='utf-8').read(); ns = {'W': W, 'open': open}
exec(s22[s22.index("src = open(W + 'apply21b.py'"):s22.index("MON = {")], ns); fixed = ns['fixed']
for r in fixed:
    if r[0] == 'HN Doris (salt, next call)': r[3] = 'evening signal 19 Nov: RT OUT 21:00 — full quantity loaded (Mihir, 19 Nov 22:32)'
    if r[0] == 'African Hornbill (blades, next call)': r[3] = 'evening signal 19 Nov: IN 21:30 → 175–188 · Project priority in the absence of an HP vessel (Mihir) · est'
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-25 12:00']
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v177) — Mihir's four answers of 19 Nov 22:32 applied on the evening signal, list 19.11 and programme 20.11; to be read against DPR 20.11, list 20.11 and programme 21.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a), b, c, q(d)) for a, b, c, d in fixed + proj)) + B.s[j:]
# ---- PREDLOG
AT = '11-19 22:32'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
R = "19 Nov 22:32 re-run after Mihir's answers (Ocean Kudos cancelled — holds rejected) — "
new = [
 prow('Uni Blossom', R + 'SAAGAR (SGR 1), CJ-13 when Rome Trader is through on her list ETC — back to the reading of 16:12'),
 prow('CD Glory', R + 'Mihir & Co — 6.5K / 8K (8K 8), CJ-5 when Ken Ann\'s 24 hours are up: New Bliss leaves the 6.5K place inside the 21 → 22 Nov window and none of the seven ahead of her can lie at CJ-5. Turns on about two hours: a clean berth freeing first gives the place to Crystal Land (8K 1). Otherwise General at CJ-1 about 22 Nov 05:00'),
 prow('AG Varvara', R + 'General (GEN 16), CJ-15A after Heng Yuan Fa Zhan'),
 prow('Libra', R + 'General against a vacant HP place, CJ-1 a day after New Bliss leaves'),
 prow('Crystal Land', R + '6.5K / 8K (8K 1), CJ-16 after African Hornbill — only once CD Glory is through with the place'),
]
a0 = B.s.index("const PREDLOG=["); b0 = B.s.index("\n];", a0)
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]
# ---- OPTS notes
def note_of(label, text):
    global B
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "SAAGAR group — one bulk and one break-bulk place. List 19.11: Uni Blossom (SGR 1), African Hornbill (2 — berthed at CJ-16 on the 19th under Project priority), AG Varvara (3), Xin Hai Tong 71 (4 — project cargo), CD Glory (5). Rome Trader's place frees at her ETC (20 Nov 22:01) and goes to Uni Blossom at CJ-13 — Ocean Kudos, whom the board had there for a few hours, is out of the line (holds rejected). ML Egret keeps the log place, at CJ-4 from the 20th, till about 28 Nov. By this line CD Glory's turn is the place ML Egret leaves — about 27–28 Nov.")
note_of('6.5K / 8K', "8K 8 on list 19.11 — THE BOARD'S PICK NOW. New Bliss leaves the 6.5K place inside the window of 21 → 22 Nov (DPR pace 22 Nov 03:00, list ETC 10:05), so the place is given out for that window. Mihir's rule of 11 Nov: each berth, as it frees, goes to the senior vessel of the line that the berth suits — nobody is kept waiting inside the window. CJ-5 frees when Ken Ann's 24 hours are up (about 21 Nov 19:30), and none of the seven ahead of CD Glory can lie there: Crystal Land needs a clean berth, Pioneer Fortune and Porto Fiscardo work the bag berths, Tan Bin 259 is finishing at the mooring, Gokova-M is clay (CJ-7 / CJ-8), Uni Blossom berths under SAAGAR and Nord Copper under Coastal. So CJ-5 comes to her under 6.5K. It turns on about two hours of estimates: if a clean berth frees before CJ-5 does (CJ-14 behind Nord Copper, CJ-15A behind Heng Yuan Fa Zhan), Crystal Land takes the place there and this route is gone till the end of the month.")
note_of('General · by seniority', "The General queue — GEN 20 on list 19.11. Mihir (19 Nov): General berths by seniority, with at most three bag vessels alongside at a time — confirmed. If the 6.5K place goes to Crystal Land instead: CJ-5 on the evening of the 21st falls to AG Varvara (GEN 16), who is senior; CJ-1 frees when New Bliss leaves (about 22 Nov), and with three bag vessels already alongside (DSM London, Katerina K and, on the board, Aboudi D) the bag vessels senior to her — Safi Alfa, Pioneer Fortune — are stopped by the limit, so she is next: about 22 Nov 05:00. If one of those three is not alongside by then, a senior bag vessel takes CJ-1 first. The timber desk says 25 Nov.")
# ---- MYLOG
g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'19 Nov 22:32 · evening signal + Mihir (bag limit confirmed, Ocean Kudos cancelled)',exp:'%s',b:'%s',slot:'6.5K / 8K — CJ-5 when Ken Ann leaves · turns on about two hours · else General, CJ-1 ~22 Nov 05:00 · SAAGAR line ~27–28 Nov · desk 25 Nov',why:'" % (g['F'], g['b']) + q(
 "The board's pick moves from CJ-1 (22 Nov morning, General) to CJ-5 on the evening of 21 Nov, under 6.5K / 8K. What changed: (1) the evening signal put African Hornbill on CJ-16 till about the 24th, and Mihir says Ocean Kudos is cancelled (holds rejected) — so no clean berth frees for Crystal Land (8K 1) before the 21st night; (2) Uni Blossom takes the SAAGAR place Rome Trader leaves, so AG Varvara no longer comes to CJ-5 under SAAGAR. That leaves CJ-5, when Ken Ann's 24 hours are up (about 21 Nov 19:30), to the 6.5K line — New Bliss gives the place up inside that window — and by Mihir's rule of 11 Nov the berth goes to the senior vessel of the line that it suits: none of the seven ahead of CD Glory can lie at CJ-5. The weak point is timing: CJ-14 and CJ-15A, clean berths Crystal Land can use, free about two hours after CJ-5 on the board's estimates; if one of them frees first, the 6.5K place goes to her and CD Glory falls back on General — CJ-1 about 22 Nov 05:00, firmer now that Mihir has confirmed the limit of three bag vessels. Either way 21–22 Nov; laytime ends 23 Nov 01:38, so she would berth just inside it.") + "'}") + B.s[i:]
# ---- LEARN
a = B.s.index(" {d:'19 Nov 16:12 · list 19.11 + programme 20.11',v:'", B.s.index("const LEARN=[")); e = B.s.index("},\n", a); ent = B.s[a:e]
if ent.count("st:'open'") != 1: B.die('16:12 entry st')
B.s = B.s[:a] + ent.replace("st:'open'", "st:'closed'") + B.s[e:]
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("19 Nov 22:32 · Mihir — four answers",
 "(1) GENERAL berths by seniority, and at most THREE BAG VESSELS are alongside at a time — confirmed. (2) AFRICAN HORNBILL berths under PROJECT priority, in the absence of an HP vessel. (3) OCEAN KUDOS: her holds were rejected, so her movement was cancelled. (4) HN DORIS loaded her full quantity.",
 "Board (19 Nov 20:00): the bag limit used but marked unconfirmed · African Hornbill at CJ-16 counted against no priority place · Ocean Kudos back in the line with her HP allotment, seated at CJ-13 behind Rome Trader · HN Doris possibly leaving short (41,858 MT to load at 0700 on DPR 19.11).",
 "Mihir, as above.",
 "The board had the bag limit right. Its guess that Ocean Kudos would be re-berthed at once was wrong — a vessel whose holds are rejected is out until they pass. HN Doris: the DPR's second-day figure (17,542 MT) did not show what she could load on the last day.",
 "v177: (1) the bag-limit note is no longer marked unconfirmed. (2) New rule in the projection: with no HP vessel for a berth, a Project-priority vessel takes it against the vacant HP place — before a General cross-fill, and without keeping a real HP vessel out; African Hornbill is entered so (Steel / project, in the vacant HP place). (3) Ocean Kudos is held out of the projection till she is ready again; Uni Blossom is back behind Rome Trader at CJ-13. (4) HN Doris's note corrected. CD Glory's pick moves to CJ-5, 21 Nov evening, under 6.5K / 8K.", "closed"))
B.save()
