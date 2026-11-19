#!/usr/bin/env python3
# apply22b — v176 (part 2): snapshot, logs, own-vessel option notes. argv[1] = UPDATED.
import re, sys, json, shutil
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'pre22b.html')
B = Board(P); q = B.q
S = json.load(open(W + 'S176.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
# ---- PRED: the list written for v175, corrected by the evening sheet
src = open(W + 'apply21b.py', encoding='utf-8').read(); ns = {}
exec(src[src.index("PGs = 'programme 20.11'"):src.index("proj = [")], ns); fixed = ns['fixed']
fixed = [r for r in fixed if r[0] != 'Ocean Kudos']
for r in fixed:
    if r[0] == 'HN Doris (salt, next call)': r[2] = '19 Nov 21:00'; r[3] = 'evening signal 19 Nov: RT OUT 21:00 (Capt Omesh)'
    if r[0] == 'Bristol (salt, next call)': r[3] = 'evening signal 19 Nov: RT OUT 20:30 (Capt Verma)'
    if r[0] == 'Heng Yuan Fa Zhan' and r[1] == '15A': r[3] = 'evening signal 19 Nov: IN 18:45 (Capt Deepak), alongside once Bristol is out · est'
    if r[0] == 'Yara J': r[3] = 'programme 20.11 + evening signal 19 Nov: RT OUT 23:30 (Capt Deepak)'
    if r[0] == 'Nord Copper' and r[1] == '14': r[2] = '20 Nov 01:00'; r[3] = 'evening signal 19 Nov: IN 22:30 (Capt Yadav), alongside once Yara J is out · CSTL · est'
    if r[0] == 'Beagle': r[3] = 'programme 20.11 · Tuna TT-3, night sailing → Marvelous Star — not on the evening signal sheet'
i0 = next(i for i, r in enumerate(fixed) if r[0] == 'Yara J')
fixed.insert(i0, ['African Hornbill (blades, next call)', '16', '19 Nov 23:30', 'evening signal 19 Nov: IN 21:30 (Capt Deepak) → 175–188, alongside once HN Doris is out · est'])
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-25 12:00']
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v176) — evening signal of 19 Nov applied on list 19.11 + programme 20.11; to be read against DPR 20.11, list 20.11 and programme 21.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a), b, c, q(d)) for a, b, c, d in fixed + proj)) + B.s[j:]
# ---- PREDLOG
AT = '11-19 19:51'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
R = "19 Nov 19:51 re-run on the evening signal — "
new = [
 " {v:'African Hornbill (blades, next call)',predAt:'%s',pb:'16',pt:'11-19 23:30',ab:'',at:'',src:'prog',note:'%s'}" % (AT, q('evening signal 19 Nov — IN 21:30 (Capt Deepak) → 175–188, behind HN Doris (21:00); reading, not scored. The board had her at CJ-14 on 21 Nov')),
 prow('Ocean Kudos', R + 'Higher productivity (she holds the 42,500 allotment), CJ-13 when Rome Trader is through on her list ETC — the berth programmed for her went to African Hornbill tonight'),
 prow('AG Varvara', R + 'SAAGAR (SGR 3), CJ-5 after Ken Ann\'s 24 hours — Uni Blossom (SGR 1) is too deep for CJ-5'),
 prow('Xin Hai Tong 71', R + 'SAAGAR project parcel against the Coastal place, CJ-14 after Nord Copper'),
 prow('Crystal Land', R + '6.5K / 8K (8K 1), CJ-15A after Heng Yuan Fa Zhan'),
 prow('CD Glory', R + 'Mihir & Co — General, CJ-1 when New Bliss leaves; unchanged and still a weak pick (see 19 Nov 16:12)'),
 prow('Uni Blossom', R + 'General, CJ-13 after Ocean Kudos — pushed back two days by Ocean Kudos coming back into the line'),
]
a0 = B.s.index("const PREDLOG=["); b0 = B.s.index("\n];", a0)
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]
# ---- OPTS: SAAGAR note
a = B.s.index("{label:'SAAGAR',", B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
B.s = B.s[:n0] + q("SAAGAR group — one bulk and one break-bulk place. List 19.11: Uni Blossom (SGR 1), African Hornbill (2 — windmill blades; she berths at CJ-16 tonight on the evening signal), AG Varvara (3), Xin Hai Tong 71 (4 — project cargo), CD Glory (5). Rome Trader's place frees at her ETC (20 Nov 22:01); her berth CJ-13 is wanted first by Ocean Kudos (HP), so the SAAGAR place goes to a log vessel at another berth — on the board AG Varvara at CJ-5 on the 21st, Uni Blossom being too deep for it. ML Egret keeps the other place at CJ-4 till about 28 Nov (list ETC 28 Nov 07:30). By this line CD Glory's turn is the place ML Egret leaves — about 27–28 Nov.") + B.s[n1:]
# ---- LEARN
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("19 Nov 19:51 · evening signal 19 Nov (disp 1640, amended 1940)",
 "AFRICAN HORNBILL (windmill blades, SGR 2) is sent to 175–188 — CJ-16 — tonight behind HN Doris; OCEAN KUDOS, given that berth under HP(42.5K) on programme 19.11 and printed \"B'TODAY\" on list 19.11, is not on the sheet. Neither the programme of the day nor the board had this.",
 "Board (19 Nov 16:25): Ocean Kudos CJ-16 20 Nov 00:30 (programme 19.11 + morning signal) · African Hornbill CJ-14 21 Nov 23:00 (SAAGAR project parcel in the Coastal place).",
 "Evening signal: HN Doris RT OUT 21:00 (Capt Omesh) · African Hornbill IN 21:30 (Capt Deepak) → 175–188 · Bristol RT OUT 20:30 (Capt Verma) · Heng Yuan Fa Zhan IN 18:45 → 161¾–169 · Yara J RT OUT 23:30 · Nord Copper IN 22:30 → 126½–141¾ · Artigo IN 17:30 → OJ-1 · NV Sunshine RT OUT 01:00. No row for Ocean Kudos, none for Beagle / Marvelous Star at Tuna.",
 "Why Ocean Kudos lost the berth is not on any sheet (vessel or cargo not ready is the usual reason). A windmill parcel is a short job the port slips into a berth that would otherwise lie idle.",
 "v176: African Hornbill entered at CJ-16 on the signal, counted against no priority place until a list prints hers; Ocean Kudos is back in the line holding her HP allotment — the board seats her at the next clean berth, CJ-13 behind Rome Trader, which pushes Uni Blossom back two days. To check on list 20.11 / programme 21.11: African Hornbill's priority, Ocean Kudos's new berth.", "ok"))
B.save()
