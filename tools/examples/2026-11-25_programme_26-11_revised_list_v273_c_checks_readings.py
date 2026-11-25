#!/usr/bin/env python3
# apply69c — v273 part 3: the checks, CD Glory's card, the own-vessel readings. Run with the stamp: python3 apply69c.py '25 Nov 2026 · HH:MM IST'
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
STAMP = sys.argv[1]
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def field(ln, k, pre):
    m = re.search(r"(?<=[{,])" + k + r":'((?:[^'\\]|\\.)*)'", ln)
    if not m: B.die('field ' + k)
    return ln[:m.start(1)] + q(pre) + m.group(1) + ln[m.end(1):]

# ---------- checks ----------
a, b = B.line_of(" {d:'21 Nov 20:25 · Circular 5237, point (i) — vacant Govt / Coastal places'"); ln = B.s[a:b]
ln = field(ln, 'act', "PROGRAMME 26.11 (the meeting of 25 Nov): NOT PUT TO THE TEST. Parvraj's Govt place is given to nobody — CJ-6 gets no inward vessel — and the Coastal place behind Lila Tokyo goes to a coastal vessel, the tug Varahi with her barge. No SAAGAR vessel and no 30K quote is printed in a Govt or Coastal place: no timber or clean berth was left over for either. The Govt place stands vacant from 25 Nov 23:45 — the meeting of 26 Nov is the test. EARLIER: ")
B.s = B.s[:a] + ln + B.s[b:]
NEW = {'d': '25 Nov 16:11 · programme 26.11 — MSC Magali "HP(50K)" at CJ-16',
       'v': 'Whether vessels are bidding for the HP places.',
       'exp': "Mihir, 25 Nov 14:47: no vessel bid for the HP category. The board stopped giving any berth on an HP bid.",
       'act': "Programme 26.11, from the same meeting, prints MV MSC MAGALI at CJ-16, 169½–188, category \"HP(50K)\" — and shifts African Hornbill to CJ-15A on port convenience to make room for her.",
       'why': "Not on the papers. Either the bid came after Mihir's word, or his word was about the other vessels of the HP column — the salt, pellet and aggregate vessels standing there on 30K / 25K quotes. It matters for circular 5237 (i): an HP bid stands BEFORE the SAAGAR line for a vacant Govt or Coastal place. If one of those vessels bids 40,000 or more, she takes that place ahead of CD Glory.",
       'fix': "MSC Magali entered as printed, under HP. For the vessels still waiting the board keeps Mihir's word — no berth on a bid it cannot see. OPEN — Mihir to say whether any waiting vessel is bidding. Also learnt from this row: a gearless coal vessel is given CJ-16 (the board had held every vessel over 200 m to CJ-7 / 8) — a gearless coal / ore vessel now keeps CJ-16 too.",
       'st': 'open'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(NEW) + ",\n")

# ---------- CD Glory's card ----------
i = B.s.index("routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:1},note:'") + len("routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:1},note:'")
j = B.s.index("'},\n  {label:'6.5K / 8K'", i)
B.s = B.s[:i] + q("SHE IS SGR 1 — FIRST OF THE SAAGAR LINE (revised list 25.11). Two ways in. (A) A VACANT GOVT PLACE, under circular 5237 (i): Parvraj sails tonight (25 Nov 23:45) and programme 26.11 gives her Govt place to nobody. With no Govt or Coastal vessel for it and no HP bid, the place comes down to the SAAGAR line — to her. The first berth she can use after that is CJ-4, behind Safi Alfa, who finishes about 26 Nov 21:55 at her DPR pace; so the board says about midnight on 26 Nov. It is for the meeting of 26 Nov to give. IT RESTS ON THREE THINGS: the circular as written — the port has not yet given a Govt or Coastal place this way; no other vessel bidding for HP — MSC Magali did, at 50K, and an HP bid stands before SAAGAR; and Safi Alfa finishing at her pace — her list ETC is 28 Nov 00:00, and the port programmes on its own ETC. (B) HER LINE'S OWN PLACE, when Asian Summit sails (list ETC 28 Nov 22:59): run without the circular, the board gives the evening of 29 Nov — sooner if Asian Summit keeps her pace; DPR 26.11 will show. Timber desk (24 Nov): ETB 27 Nov.") + B.s[j:]

def mylog(name, rd):
    i = B.s.index("'" + name + "':[", B.s.index('const MYLOG')); j = B.s.index("\n ],", i)
    assert B.s[j - 1] == '}', B.s[j - 30:j]
    B.s = B.s[:j] + ",\n  " + js(rd) + B.s[j:]
mylog('CD Glory', {'d': '25 Nov 16:11 · programme 26.11 + list 25.11 revised after the meeting', 'exp': '11-26 23:55', 'b': '4',
  'slot': "A vacant Govt place under circular 5237 (i) — she is SGR 1 · CJ-4 behind Safi Alfa, 26 Nov about midnight · for the meeting of 26 Nov · on the circular as written, not yet seen",
  'why': "Programme 26.11 does not name her — and could not have: no timber berth came free in its window. The head of CJ-14 goes to the tug Varahi and her barge (the Coastal place, to a coastal vessel), CJ-15A to the shift of African Hornbill, CJ-16 to MSC Magali on an HP bid of 50K. What the programme does show: Parvraj sails at 23:45 tonight and her GOVT PLACE is given to nobody. On circular 5237 (i) that place, with no Govt or Coastal vessel for it and no HP bid, comes to the SAAGAR line, and CD Glory is SGR 1. The 3 pm reading had her in the Coastal place at CJ-14 behind Jumbo Kinetic; the Coastal place has now gone to the tug till about 27 Nov 18:00, so it is the Govt place and CJ-4, where Safi Alfa finishes about 26 Nov 21:55 at her DPR pace. THE WEAK LINKS: (1) the port has still not given a Govt or Coastal place under the circular — the 26 Nov meeting is the first real test; (2) MSC Magali's bid shows vessels DO bid for HP, and an HP bid stands before SAAGAR for this place; (3) Safi Alfa's list ETC is 28 Nov 00:00 — if the port goes by it, CJ-4 is not in the 26 Nov window, and the next timber berths are CJ-15 (Xin Hai Tong 71, no ETC) and CJ-14 behind the tug, 27 Nov evening. If the circular is not applied at all: Asian Summit's SAAGAR place, about the evening of 29 Nov on her list ETC. RANGE: midnight of 26 Nov to the evening of 29 Nov."})
mylog('Paiwan Ace', {'d': '25 Nov 16:11 · programme 26.11 + list 25.11 revised after the meeting', 'exp': '11-30 03:55', 'b': '15A',
  'slot': "SAAGAR (SGR 4) — her line's own place when Asian Summit sails; CJ-15A behind Star New London, 30 Nov early · ONLY IF the three log vessels ahead of her go in on vacant Govt / Coastal places under circular 5237 (i) · the earliest, not the date",
  'why': "A day later than the 3 pm reading. Programme 26.11 gives the Coastal place to the tug Varahi till about 27 Nov 18:00 and CJ-16 to MSC Magali till about 28 Nov 15:20, so the timber vessels ahead of her go in later: CD Glory 26 Nov night (Govt place), Dariya Priya 27 Nov night (Govt place), African Tiger 28 Nov midday (Coastal place). Asian Summit's SAAGAR place (list ETC 28 Nov 22:59) is then hers, at the first berth she can use — CJ-15A on 30 Nov. Every step before hers rests on the circular being applied as written, which no meeting has yet done. If it is not: the desk's dates — 7 Dec under SAAGAR, 2 Dec under 6.5K. Revised list: SGR 4 · 8K 10 · GEN 20."})

B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='" + STAMP + "';", B.s, count=1)
B.save(); print('saved 69c')
