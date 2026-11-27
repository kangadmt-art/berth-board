#!/usr/bin/env python3
# apply77c — v281: readings for CD Glory / Paiwan Ace after programme 28.11 and the revised list; one open question; stamp.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o): return "'" + q(o) + "'"
def mylog(name, e):
    k = " '%s':[\n" % name; a = B.s.index("const MYLOG={"); i = B.s.index(k, a); j = B.s.index("\n ],", i)
    B.s = B.s[:j] + ",\n  {" + ",".join(kk + ":" + js(e[kk]) for kk in ('d', 'exp', 'b', 'slot', 'why')) + "}" + B.s[j:]
mylog('CD Glory', {'d': '27 Nov 13:58 · programme 28.11 + list 27.11 revised', 'exp': '11-30 06:03', 'b': '1',
 'slot': 'no longer Asian Summit\'s place if KM Jakarta is counted as the SAAGAR bulk vessel — then a vacant Coastal place, CJ-1 behind Manta Sena, about 30 Nov · if the port gives Asian Summit\'s place to the senior SAAGAR vessel regardless of bulk, CJ-15A about 29 Nov 04:00',
 'why': 'NOT ON PROGRAMME 28.11 — nobody is: the port gave no dry-cargo berth at the meeting of 27 Nov, and printed no outward row for Asian Summit, MSC Magali or DSM London. Every berth now waits for the meeting of 28 Nov. '
        'THE NEW RISK IS KM JAKARTA: on the list revised after the meeting she is ready (27 Nov 11:00) and ranked HP 6 · SGR 7 — salt in bulk, agent True Blue. Asian Summit holds the SAAGAR BULK place; by the rule Mihir confirmed on 14 Nov (bulk and break bulk are separate priorities; logs hold the bulk place only while no SAAGAR bulk vessel waits) that place goes to KM Jakarta, the only ready SAAGAR bulk vessel, ahead of CD Glory. '
        'The board follows that rule: KM Jakarta takes the SAAGAR place at CJ-15A when Hai Nam 81 is out (about 29 Nov 04:00), and CD Glory waits for a vacant Coastal place under circular 5237 — CJ-1 after Manta Sena, about 30 Nov 06:00 — or for AG Varvara\'s break-bulk place, about 4–5 Dec. '
        'IF THE PORT INSTEAD GOES BY THE SGR NUMBER ALONE (CD Glory 1, KM Jakarta 7), she gets CJ-15A about 29 Nov 04:00. This is the point to settle at the meeting of 28 Nov — OPEN QUESTION to Mihir.'})
mylog('Paiwan Ace', {'d': '27 Nov 13:58 · programme 28.11 + list 27.11 revised', 'exp': '12-04 01:22', 'b': '16',
 'slot': 'a General place (GEN 18) at CJ-16 behind the HP vessels, about 4 Dec · the earliest, not the date',
 'why': 'A day later than this morning: nothing was given at the meeting of 27 Nov, so every berth moves to the meeting of 28 Nov; and the HP line is now seated senior-first — Meghna Prestige, Zheng Run, Pacific Apex one after another at CJ-16 — before she can have that berth. SGR 4 · 8K 8 · GEN 18, unchanged.'})
a = B.s.index("  \"SHE IS SGR 1") if False else None
B.rep("THE BERTH: CJ-5 itself if no HP bidder takes it (Rex, HP 5, is the one CJ-5 suits) — otherwise CJ-15 behind Xin Hai Tong 71, about 29 Nov 02:00. For the meeting of 28 Nov; for today\\'s only if Asian Summit\\'s early completion is declared. New Joyful (petcoke, SGR Y, ETA 28 Nov 05:00) is the SAAGAR bulk vessel that could come in ahead for the bulk place.",
      q("PROGRAMME 28.11 gave no dry-cargo berth; the place is for the meeting of 28 Nov. KM JAKARTA (salt, SGR 7, ready 27 Nov) is now a ready SAAGAR BULK vessel — by the rule of 14 Nov the bulk place Asian Summit holds goes to her first; the board then gives CD Glory a vacant Coastal place, CJ-1 about 30 Nov. If the port goes by the SGR number alone, CD Glory gets CJ-15A about 29 Nov 04:00 behind Hai Nam 81. New Joyful (petcoke, SGR Y, ETA 28 Nov 04:00) is the next bulk vessel."))
NEW = {'d': '27 Nov 13:58 · KM Jakarta ranked SGR 7 — the SAAGAR bulk place', 'ask': 'KM Jakarta (salt, SGR 7, ready) — will Asian Summit\'s SAAGAR place go to her as the bulk vessel, or to CD Glory as SGR 1?', 'who': 'Mihir',
 'v': 'Who takes the SAAGAR place Asian Summit leaves.', 'exp': 'Mihir, 14 Nov 18:00: SAAGAR bulk and break bulk are separate priorities — with no bulk vessel waiting, a break-bulk vessel takes the bulk place. On that rule a ready SAAGAR bulk vessel comes first for the bulk place.',
 'act': 'List 27.11 revised after the meeting: KM Jakarta — salt in bulk 60,000 MT, True Blue — is ready from 27 Nov 11:00 and ranked HP 6 · SGR 7. CD Glory is SGR 1. Asian Summit (petcoke) holds the bulk place; AG Varvara (logs) the break-bulk place, till about 4–5 Dec.',
 'why': 'It decides CD Glory\'s date: about 29 Nov if the SGR number alone counts, about 30 Nov or later if the bulk vessel goes first. Xin Bo, once declared under SAAGAR, would stand in the same bulk line.',
 'fix': 'The board follows the rule of 14 Nov — bulk vessel first — until Mihir or programme 29.11 says otherwise. OPEN.', 'st': 'open'}
B.rep("const LEARN=[\n", "const LEARN=[\n {" + ",".join(k + ":" + js(NEW[k]) for k in ('d', 'ask', 'who', 'v', 'exp', 'act', 'why', 'fix', 'st')) + "},\n")
B.s, k = re.subn(r"const UPDATED='[^']*';", "const UPDATED='27 Nov 2026 · 14:02 IST';", B.s, count=1); assert k == 1
B.save()
