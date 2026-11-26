#!/usr/bin/env python3
# apply74d — v278 part 4: open questions, own-vessel readings, CD Glory's options, engine comments.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 26.11 (revised)'); q = B.q
def js(o):
    if o is None: return 'null'
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (int, float)): return repr(o)
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def lrow(dkey):
    a = B.s.index(" {d:'" + dkey); b = B.s.index("\n", a); return a, b
def lset(dkey, field, text, mode='set'):
    a, b = lrow(dkey); ln = B.s[a:b]
    m = re.search(r",%s:'((?:[^'\\]|\\.)*)'" % field, ln)
    if not m: B.die('LEARN field: ' + field)
    new = q(text) + (' ' + m.group(1) if mode == 'pre' else '')
    ln = ln[:m.start(1)] + new + ln[m.end(1):]; B.s = B.s[:a] + ln + B.s[b:]

# ================= LEARN =================
K5 = "21 Nov 20:25 · Circular 5237, point (i)"
lset(K5, 'ask', "Answered on 26 Nov: for a vacant Govt place the port took the senior 30K-quote vessel of the HP column (Hai Nam 81, \"GOV(30K)\") before the SAAGAR line.")
lset(K5, 'act', "PROGRAMME 27.11 (the meeting of 26 Nov): THE TEST CAME, AND WENT THE OTHER WAY. Parvraj's Govt place is given to MV HAI NAM 81 — salt, HP 1 on the list, \"30K/25K/10K Sr No 07\" — printed \"GOV(30K)\" at CJ-15A. CD Glory, SGR 1, was waiting and CJ-15A suits her. So the port reads \"3(A) Higher productivity\" in point (i) as the vessels standing in the HP column of the list on their 30K quotes, by that column's order — not only a vessel bidding 40,000 or more — and SAAGAR, 3(B), comes after them. The wording of the circular holds; the board had read the HP step too narrowly. EARLIER —", 'pre')
lset(K5, 'fix', "CLOSED AGAINST THE BOARD'S READING, 26 Nov (v278), as this row said it would be. In the calculation now: a vacant Govt place goes to a Coastal vessel, then to the senior 30K / 25K quote vessel of the HP column the berth suits, then to the SAAGAR line; a vacant Coastal place to the quote vessel, then SAAGAR. CD Glory goes back to her own line's place. Whether to take this up with the port is Mihir's call — the papers of this row are the material for it. Before 26 Nov:", 'pre')
a, b = lrow(K5); ln = B.s[a:b]; assert ln.rstrip(',').endswith("st:'open'}"); B.s = B.s[:a] + ln.replace(",st:'open'}", ",st:'reference'}") + B.s[b:]
KH = "25 Nov 16:11 · programme 26.11 — MSC Magali"
lset(KH, 'act', "PROGRAMME 27.11 adds a second fact: MV HAI NAM 81, HP 1 on the list, is printed \"GOV(30K)\" — a 30K quote, not a bid, and she is taken from the HP column all the same. So the HP column works on 30K quotes for vacant Govt / Coastal / 24-hour places; a bid of 40,000 or more (MSC Magali, 50K) takes an HP place itself. BEFORE THAT —", 'pre')
NEW = [
 {'d': '26 Nov 15:14 · Xin Bo — our salt vessel on the expected sheet', 'ask': 'Xin Bo (our salt vessel, 50,000 MT, ETA 27 Nov 03:00): under which line do we take her — 30K quote, SAAGAR or 8K — and when will she be declared ready?', 'who': 'Mihir',
  'v': 'The line and the readiness of MV Xin Bo.', 'exp': 'The revised list 26.11 has her on the expected sheet: agent Mihir, HP Y · SGR Y · 8K Y, "30K/25K/10K Sr No 07", readiness N/A.',
  'act': 'A "Y" is willingness, not a place in the line: she gets a number only when she has reported and is declared ready.',
  'why': 'Salt works only at CJ-13 to 16. Tried on the board with her ready on 27 Nov 11:00 and last in the HP column (HP 7): she takes the Govt place Hai Nam 81 leaves — CJ-15A, about 29 Nov 01:00 — on the 30K quote, ahead of the log vessels of the SAAGAR line. Declared a day later, that place has gone to Dariya Priya.',
  'fix': 'Until she is declared ready the board shows no berth for her. OPEN — Mihir to say the line and the readiness.', 'st': 'open'},
 {'d': '26 Nov 15:14 · Katerina K at CJ-6 — General past its two senior vessels', 'ask': 'Katerina K (GEN 3) was given CJ-6 past GEN 1 and GEN 2, whom CJ-6 does not suit. So General goes to the senior vessel the berth suits — is that how you want the board to count it?', 'who': 'Mihir',
  'v': 'How the General line fills a berth its senior-most vessel cannot use.', 'exp': 'Mihir, 20 Nov 17:13: General goes strictly by seniority — a junior is not given a General berth past a ready senior. The board therefore gave General nothing when the berth did not suit GEN 1.',
  'act': 'DPR 26.11 and the revised list: MV KATERINA K — GEN 3, kaolin / bentonite / soya bean meal, 199.99 m — made fast at CJ-6 at 04:12 on 26 Nov, two hours after Parvraj let go, under GENERAL. Fortunelit (GEN 1) and Crystal Land (GEN 2), both bag vessels, were waiting; CJ-6 is not a berth for them. She is on no programme and no signal sheet in hand.',
  'why': 'The port did not leave CJ-6 vacant for want of a berth for GEN 1. It agrees with Mihir\'s word of 22 Nov that no berth is left vacant, and with 25 Nov 17:02 — the place by priority, then a suitable berth.',
  'fix': 'In the calculation from v278: General goes to the senior vessel the berth suits; among vessels the berth suits, strictly by seniority as before. OPEN — Mihir to confirm, since it narrows his word of 20 Nov.', 'st': 'open'},
 {'d': '26 Nov 15:14 · programme 27.11 — the meeting of 26 Nov', 'ask': '', 'who': '',
  'v': 'The berthings of the cargo jetties given at the meeting of 26 Nov.', 'exp': 'The call frozen at 25 Nov 23:39: Star New London → CJ-15 (HP place, 30K quote) · CD Glory → CJ-4 (vacant Govt place, circular 5237) · Fortunelit → CJ-15A (General).',
  'act': 'Programme 27.11: JUMBO KINETIC "CSTL" at CJ-7, 52–57 · HAI NAM 81 "GOV(30K)" at CJ-15A behind African Hornbill · to make room, Asian Summit shifts CJ-7 → CJ-5 and Blue Shark CJ-5 → CJ-14, both "A/C of Gautam Freight", and Safi Alfa warps. None of the three called.',
  'why': '(1) The Govt place went to the 30K quote of the HP column before SAAGAR — see the circular 5237 row. (2) CJ-4 and CJ-15 did not come free: Safi Alfa\'s list ETC moved to 30 Nov with 6,000 MT more declared; Xin Hai Tong 71 works 910 MT a day — the board had reckoned on her norm-less first hour. (3) Star New London went back to the expected sheet. (4) Jumbo Kinetic was held to CJ-13–16 by the board; the port seats a project vessel at CJ-7 and moves two working vessels for her at the agent\'s cost.',
  'fix': 'Coded: the quote line before SAAGAR for a vacant Govt / Coastal place · General to the senior vessel the berth suits · a DPR balance the list has since re-stated gives no finishing time · a programmed shift costs the shifted vessel hours. NOT coded: a shift on an agent\'s account cannot be foreseen — the board will keep missing those.', 'st': 'reference'},
]
ORDER = ('d', 'ask', 'who', 'v', 'exp', 'act', 'why', 'fix', 'st')
B.rep("const LEARN=[\n", "const LEARN=[\n" + "".join(" {" + ",".join(k + ":" + js(r[k]) for k in ORDER) + "},\n" for r in NEW))

# ================= MYLOG =================
def mylog(name, entry):
    k = " '%s':[\n" % name; a = B.s.index("const MYLOG={"); i = B.s.index(k, a); j = B.s.index("\n ],", i)
    B.s = B.s[:j] + ",\n  {" + ",".join(kk + ":" + js(entry[kk]) for kk in ('d', 'exp', 'b', 'slot', 'why')) + "}" + B.s[j:]
mylog('CD Glory', {'d': '26 Nov 15:14 · programme 27.11 + list 26.11 revised + DPR 26.11', 'exp': '11-27 18:00', 'b': '5',
 'slot': 'SAAGAR (SGR 1) — her line\'s own place when Asian Summit finishes; CJ-5, 27 Nov evening · for the meeting of 27 Nov',
 'why': 'NOT ON PROGRAMME 27.11. The reading of the last two days — a vacant Govt place under circular 5237 (i), CJ-4 on 26 Nov night — did not hold: the port gave Parvraj\'s Govt place to Hai Nam 81 (salt, HP 1) as "GOV(30K)" at CJ-15A, a berth she could have used; and CJ-4 is not free, Safi Alfa\'s ETC is now 30 Nov. So the 30K-quote line stands before SAAGAR for a vacant Govt place, and she is back to her own line. '
        'THAT LINE IS NOW CLOSE: Asian Summit — the SAAGAR bulk place — discharged 26,200 MT in her first full day and had 30,499 left at 07:00 on 26 Nov. She is shifted CJ-7 → CJ-5 tonight (Gautam Freight\'s account); at that pace she finishes about 27 Nov 16:00, shift included. CD Glory is SGR 1 and CJ-5 takes hardwood logs (Lanna Naree, 5–9 Nov), so the board gives her CJ-5 about 27 Nov 18:00 — to be given at the meeting of 27 Nov, which programmes from 18:00. '
        'WHAT CAN MOVE IT: the port programmes on its own ETC — Asian Summit\'s is 28 Nov 22:59; unless her agent declares the earlier completion at the meeting, the place comes a day later, 29 Nov. And petcoke at CJ-5 may not keep the rate it had at CJ-7. ONE MORE: Asian Summit holds the SAAGAR BULK place, and a SAAGAR bulk vessel that is ready takes that place before the logs — New Joyful (petcoke, SGR Y, ETA 28 Nov 05:00, printed "RDY") is the one to watch; if the place frees only on 28 / 29 Nov, she can be ahead of CD Glory for it. Timber desk (24 Nov): ETB 27 Nov.'})
mylog('Paiwan Ace', {'d': '26 Nov 15:14 · programme 27.11 + list 26.11 revised + DPR 26.11', 'exp': '12-03 16:56', 'b': '16',
 'slot': 'SAAGAR (SGR 4) — the place CD Glory leaves; CJ-16, about 3 Dec evening · the earliest, not the date',
 'why': 'Three and a half days later than yesterday\'s reading, because the short cut is gone: the port gives a vacant Govt / Coastal place to the 30K-quote line before SAAGAR (Hai Nam 81, programme 27.11), so the log vessels ahead of her no longer clear through those places as fast. Revised list: SGR 4 · 8K 8 · GEN 17. '
        'How the board gets there: CD Glory takes Asian Summit\'s SAAGAR place about 27 Nov; Dariya Priya (SGR 2) a Govt place at CJ-15A about 29 Nov once the quote line has nobody for that berth; African Tiger (SGR 3) CJ-15 about 1 Dec when Xin Hai Tong 71 is done; then she is first of the line, and the next SAAGAR place is CD Glory\'s, about 3 Dec. '
        'Each of those steps is an estimate on an estimate. If Xin Bo is declared ready on 27 Nov she takes the 29 Nov Govt place at CJ-15A instead of Dariya Priya, and everything behind moves about two days.'})
a = B.s.index("const MYLOG={"); k = " 'Rome Trader (salt, next call)':[\n"; i = B.s.index(k, a)
B.s = B.s[:i] + " 'Xin Bo':[\n  {" + ",".join(kk + ":" + js(v) for kk, v in (
  ('d', '26 Nov 15:14 · list 26.11 revised (ETA sheet) — first reading'), ('exp', '11-29 01:05'), ('b', '15A'),
  ('slot', 'a vacant Govt place on the 30K quote, behind Hai Nam 81 — CJ-15A, about 29 Nov 01:00 · ONLY IF she is declared ready on 27 Nov and the port ranks her in the HP column'),
  ('why', 'Salt in bulk 50,000 MT EXP, 189.99 m, 6.5 m on arrival, ETA 27 Nov 03:00, agent Mihir; HP Y · SGR Y · 8K Y, "30K/25K/10K Sr No 07", readiness N/A. Salt works only at CJ-13 to 16. '
          'The port has just shown how a salt vessel gets in: Hai Nam 81, first of the HP column on a 30K quote, takes a vacant Govt place at CJ-15A on 27 Nov and is done about 28 Nov 23:00. Ahead of Xin Bo in that column are Sea Postman (clay — CJ-7/8), Meghna Prestige (salt — she takes CJ-16 behind MSC Magali about 28 Nov evening), Zheng Run, Pacific Apex and Rex, none of whom can use CJ-15A. '
          'So, tried on the board with her ready 27 Nov 11:00 and last of the column: CJ-15A about 29 Nov 01:00, out about 30 Nov 22:00 at 30,000 a day. Under SAAGAR alone the board gives the same berth and hour — she still goes in on the quote. NOT in the live projection: with readiness N/A the board gives her no berth.'))) + "}\n ],\n" + B.s[i:]

# ================= OPTS — CD Glory =================
a = B.s.index("const OPTS={'CD Glory':{fixed:[],"); b = B.s.index("\nconst OPTRES=", a)
B.s = B.s[:a] + ("const OPTS={'CD Glory':{fixed:[],\n routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:1},note:'" + q(
  "SHE IS SGR 1 — FIRST OF THE SAAGAR LINE (revised list 26.11). Her way in is her line's own place: Asian Summit (petcoke) holds it, did 26,200 MT in her first full day and had 30,499 left at 07:00 on 26 Nov — about 27 Nov 16:00 at that pace, tonight's shift to CJ-5 included. CJ-5 takes hardwood logs, so the board gives CD Glory CJ-5 about 27 Nov 18:00. "
  "It is for the meeting of 27 Nov. THE RISK: the port's own ETC for Asian Summit is 28 Nov 22:59 — if her completion is not declared earlier at the meeting, the place comes on 29 Nov, and by then New Joyful (petcoke, SGR Y, ETA 28 Nov 05:00) may be ready — a SAAGAR bulk vessel takes the bulk place before the logs. "
  "THE SHORT CUT IS CLOSED: a vacant Govt place under circular 5237 (i) went to Hai Nam 81 on a 30K quote (programme 27.11) — the quote line stands before SAAGAR. Timber desk (24 Nov): ETB 27 Nov.") + "'},\n"
  "  {label:'6.5K / 8K',only:'8K',rk:{'8K':5},note:'" + q("CLOSED. Mihir (20 Nov 16:50): CD Glory cannot berth under the 6.5K priority while other vessels are senior to her in it — the place goes by seniority, whichever berth frees first. She is 8K 5 on the revised list 26.11; Crystal Land 1, Glimlit 2, Porto Fiscardo 3 and Captainannis L 4 stand ahead, and Manta Sena holds the place till about 30 Nov.") + "'},\n"
  "  {label:'General · by seniority',only:'GEN',rk:{GEN:10},note:'" + q("NOT HER WAY IN. General goes by seniority among the vessels a berth suits (Mihir, 20 Nov; Katerina K, 26 Nov). She is GEN 10 on the revised list 26.11 — nine vessels stand ahead, though several of them are bag vessels that cannot use a timber berth. The SAAGAR place comes first in any case.") + "'}]}};") + B.s[b:]

# ================= engine comments =================
B.rep("{ // circular 5237 (i): the vacant place goes down the order — a Coastal vessel (when the Coastal place is taken), an HP bid, the SAAGAR line", "{ // circular 5237 (i) as the port applies it (programme 27.11): the vacant place goes down the order — a Coastal vessel (when the Coastal place is taken), the 30K / 25K quote vessels of the HP column, the SAAGAR line")
B.rep("the senior quote vessel this berth suits takes it, in the HP place nobody bid for. Board's reading — not yet seen on a programme.", "the senior quote vessel this berth suits takes it, in the HP place nobody bid for. Board's reading. (Programme 27.11 shows the port going further: Hai Nam 81, HP 1 on a 30K quote, in a vacant GOVT place ahead of SAAGAR — see CATS.GOV fb5.)")
B.save(); print('saved 74d')
