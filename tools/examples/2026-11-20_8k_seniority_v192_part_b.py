#!/usr/bin/env python3
# apply37b — v192 (part 2, logs): UPDATED, CD Glory route notes, snapshot, prediction log, own-vessel log, lessons. argv[1] = UPDATED
import re, sys, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; B = Board(W + 'dpa-berth-board.html'); q = B.q
S = json.load(open(W + 'S192.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
def note_of(label, text):
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "THE BOARD'S PICK. SAAGAR group — one bulk and one break-bulk place. Revised list 20.11: Uni Blossom (SGR 1), AG Varvara (2), Xin Hai Tong 71 (3 — project cargo), CD Glory (4), Dariya Priya (5), African Tiger (6). Uni Blossom takes Rome Trader's place tonight. AG Varvara is projected into CJ-5 by General on 21 Nov and Xin Hai Tong 71 into CJ-14 by the project route — which leaves CD Glory next for ML Egret's place: about 24 Nov at the DPR pace (list ETC 28 Nov). Board: CJ-16 behind African Hornbill, 24 Nov 06:00. If AG Varvara does not berth by General she takes this place first, and CD Glory waits for Uni Blossom's — about 28 Nov. Timber desk, after the meeting of 20 Nov: 26 Nov.")
note_of('6.5K / 8K', "CLOSED. Mihir (20 Nov 16:50): CD Glory cannot berth under the 6.5K priority while other vessels are senior to her in it — the place goes by seniority, whichever berth frees first. She is 8K 9; Manta Sena 1 (takes CJ-1 behind New Bliss, about 22 Nov), Crystal Land 2, Pioneer Fortune 3, Tan Bin 259 5, Gokova-M 6, Porto Fiscardo 7 and Captainannis L 8 stand ahead. Nothing by this line inside three weeks.")

# ---- PRED
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
i = B.s.index("const PRED=["); j = B.s.index("\n];", i); blk = B.s[i:j]
rows = re.findall(r"\['((?:[^'\\]|\\.)*)','([^']*)','([^']*)','((?:[^'\\]|\\.)*)'\]", blk)
fixed = [r for r in rows if not r[3].startswith('board projection') and r[0] != 'Jag Pushpa']          # the programmed / signalled moves stand; Jag Pushpa has sailed
assert 20 < len(fixed) < 30, len(fixed)
proj = [(q(x['n']), x['b'], nice(x['F']), q('board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else ''))) for x in S if x['F'] <= '11-26 00:00']
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v192) — programme 21.11 and the revised list 20.11, with Mihir's word of 16:50 (6.5K / 8K by seniority); to be read against the evening signal sheet, DPR 21.11, list 21.11 and programme 22.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % r for r in list(fixed) + proj)) + B.s[j:]

# ---- PREDLOG
b0 = B.s.index("\n];", B.s.index("const PREDLOG=["))
AT = '11-20 16:50'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
R = "20 Nov 16:50 re-run on Mihir's word — the 6.5K / 8K place goes by seniority — "
new = [
 prow('AG Varvara', R + 'General (GEN 16), CJ-5 when Vishva Bandhan has finished there — the 6.5K line no longer takes that berth'),
 prow('Manta Sena', R + '6.5K / 8K (8K 1), CJ-1 behind New Bliss'),
 prow('CD Glory', R + 'Mihir & Co — SAAGAR (SGR 4), CJ-16 behind African Hornbill when ML Egret\'s place opens at the DPR pace; AG Varvara (SGR 2) is taken by General, Xin Hai Tong 71 (SGR 3) by the project route. 6.5K / 8K closed — eight seniors. General: CJ-15A about 25 Nov. Desk: 26 Nov'),
 prow('Blue Shark', R + 'General against a vacant HP place, CJ-15 after ML Egret'),
 prow('Dariya Priya', R + 'General against a vacant HP place, CJ-15A after Belmoira'),
 prow('Crystal Land', R + '6.5K / 8K (8K 2), next after Manta Sena — CJ-14 after Hai Nam 81'),
]
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]

# ---- MYLOG
g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 16:50 · Mihir — she cannot take the 6.5K place ahead of her seniors',exp:'%s',b:'%s',slot:'SAAGAR — CJ-16 about 24 Nov 06:00, when ML Egret\\'s place opens · General — CJ-15A about 25 Nov · 6.5K / 8K CLOSED (eight vessels senior to her) · timber desk 26 Nov',why:'" % (g['F'], g['b']) + q(
 "Mihir (20 Nov 16:50): CD Glory cannot berth at CJ-5 under the 6.5K priority, because other vessels are senior to her in that line. The board had given her CJ-5 on the night of the 21st on its 11 Nov reading — that the place passes down the line when the berth does not suit the seniors. For 6.5K / 8K that reading is withdrawn: the place goes by seniority, and she is 8K 9. So Manta Sena (8K 1) takes the place at CJ-1 behind New Bliss, about 22 Nov 00:20, and CJ-5, when Vishva Bandhan has finished there, goes to General — AG Varvara (GEN 16), the senior vessel that does not load bags. That last point helps CD Glory: with AG Varvara (SGR 2) berthed by General and Xin Hai Tong 71 (SGR 3) taken by the project route, she is next in the SAAGAR line for ML Egret's place — about 24 Nov at the DPR pace (list ETC 28 Nov) — and the board seats her at CJ-16 behind African Hornbill: 24 Nov 06:00, done about 2 Dec 21:50. Weak points: AG Varvara must indeed get CJ-5 by General (if she does not, the SAAGAR place is hers first and CD Glory waits for Uni Blossom's, about 28 Nov); ML Egret must keep her pace; African Hornbill's sailing (24 Nov 04:00) is the board's own estimate. The timber desk says 26 Nov. Laytime (arrival + 12 hours) runs out 23 Nov 01:38. This is her fourth date today — 21 Nov night, 23 Nov night, 21 Nov night, 24 Nov morning; the last move rests on Mihir's word, not on a document.") + "'}") + B.s[i:]

# ---- LEARN
B.rep("told to Mihir together with the correction.',st:'open'},", "told to Mihir together with the correction. ANSWERED (Mihir, 20 Nov 16:50): she cannot take the 6.5K place — her seniors in that line come first; see the entry of 16:50.',st:'closed'},")
B.rep("The slot is never held for a berth that frees later. (CJ-5 itself goes to the Govt priority first.)", "The slot is never held for a berth that frees later. (CJ-5 itself goes to the Govt priority first.) [20 Nov 16:50, Mihir: in the 6.5K / 8K line seniority comes first — a junior does not take the place past her seniors; see that entry.]")
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 16:50 · Mihir — the 6.5K / 8K place goes by seniority",
 "CD Glory cannot berth at CJ-5 under the 6.5K priority, as other vessels are senior to her in that priority. (His second point: the note on laytime was not clear to him — explained again in the chat; no rule changed.)",
 "Board (v190 / v191): CJ-5, when Vishva Bandhan has finished there on the night of 21 Nov, goes down the 6.5K / 8K line to CD Glory (8K 9), because none of the eight ahead of her can lie at CJ-5 — the 11 Nov reading, \"the place is never held for a berth that frees later\".",
 "Mihir's word, 20 Nov 16:50 — in answer to the board's question whether the port would give her CJ-5 or keep the place for Manta Sena.",
 "In 6.5K / 8K seniority decides, not which berth frees first. The 11 Nov answer (\"if no suitable berth is available for the senior, the berth goes to the next senior that fits\") does not carry a junior past eight ready seniors — the more so when a berth that suits the senior-most (CJ-1, behind New Bliss) frees the same night.",
 "v192: SENIOR_ONLY=['8K'] in the projection — in the 6.5K / 8K line a junior is not a candidate while a ready senior of the line is still waiting (a senior with no berth she could ever use is not counted); the berth goes down the order to the other groups. Result: Manta Sena CJ-1 about 22 Nov 00:20 (8K) · AG Varvara CJ-5 21 Nov 22:00 (General) · CD Glory CJ-16 24 Nov 06:00 by SAAGAR. The other single-place lines (Coastal, 24 hrs, Steel / Project) still follow the 11 Nov reading — Mihir spoke of 6.5K only. OPTS ranks brought to the revised list (SGR 4, 8K 9).", "adopted"))
B.save()
