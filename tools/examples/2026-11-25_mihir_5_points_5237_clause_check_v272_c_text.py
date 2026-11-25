#!/usr/bin/env python3
# v272 part C — Mihir, 25 Nov 14:47 (after the meeting of 25 Nov), five points:
#   1. Asian Summit is under SAAGAR, not HP.  2. No vessel bid for the HP category.  3. Berthing goes by the vacant places, by priority, first.
#   4. Lila Tokyo was the senior vessel; the port by mistake allotted the movement to Hai Nam 81.
#   5. No information from the port yet — check "that clause" (circular 5237 (i)) against the policy of 24.03.2025, the circular of 21.05.2026 and the corrigendum of 09.07.2026.
# Part A (apply68a.py) = the engine; part B (apply68b.py) = the Sr No 7 remaining-berth rule; this part = the words: checks, register, own-vessel readings.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def row(prefix):
    a, b = B.line_of(prefix); return a, b, B.s[a:b]
def put(a, b, ln): B.s = B.s[:a] + ln + B.s[b:]
def field(ln, k, new=None, pre=None):
    m = re.search(r"(?<=[{,])" + k + r":'((?:[^'\\]|\\.)*)'", ln)
    if not m: B.die('field ' + k + ' not found')
    val = q(new) if new is not None else q(pre) + m.group(1)
    return ln[:m.start(1)] + val + ln[m.end(1):]

# ---------- checks (LEARN) ----------
# (a) CJ-14 / Lila Tokyo — answered
a, b, ln = row(" {d:'23 Nov 11:06 · list 23.11 + HM signal 23 Nov (disp 08:15) — CJ-14 went to Lila Tokyo, not Hai Nam 81'")
assert ln.count("st:'open'") == 1
ln = field(ln, 'fix', pre="ANSWERED — Mihir, 25 Nov 14:47: Lila Tokyo was the senior vessel; the port had by mistake allotted the movement to Hai Nam 81 on programme 23.11 and put it right. A place taken on a quote goes to the SENIOR quote vessel — the board's quote line already runs by seniority. ")
put(a, b, ln.replace("st:'open'", "st:'ok'"))
# (b) meeting of 23 Nov — change (1) confirmed, (2) answered, (3) still with Mihir
a, b, ln = row(" {d:'23 Nov 14:10 · programme 24.11 — the meeting of 23 Nov'")
assert ln.count("st:'open'") == 1
ln = field(ln, 'fix', pre="MIHIR, 25 Nov 14:47 — (1) CONFIRMED: berthing goes by the vacant places, in order of priority, first; the vessel then takes the free berth that suits her. (2) ANSWERED by his word on Lila Tokyo: a quote place goes to the senior quote vessel. Only (3) is still open. EARLIER TEXT: ")
put(a, b, ln)
# (c) meeting of 24 Nov — re-read with Mihir's two facts; closed
a, b, ln = row(" {d:'24 Nov 22:51 · programme 25.11 — the meeting of 24 Nov'")
assert ln.count("st:'open'") == 1
ln = field(ln, 'why', pre="MIHIR, 25 Nov 14:47: Asian Summit berthed under SAAGAR, not HP, and no vessel bid for HP. Read that way the meeting gave every vacant PLACE to its own line and each vessel the berth that suits her: two SAAGAR places fell vacant (ML Egret, Uni Blossom) and two SAAGAR vessels came in — Asian Summit (bulk) at CJ-7, the petcoke berth, and AG Varvara (logs) at CJ-13; the 6.5K place went to Manta Sena; the project vessel Xin Hai Tong 71 took CJ-15; the HP place Gokova-M left went to nobody — there was no bid. EARLIER READING: ")
ln = field(ln, 'fix', pre="CLOSED 25 Nov: (a) is settled — no berth is given on an HP bid while nobody bids. (b) stays on the list for the engine review. ")
put(a, b, ln.replace("st:'open'", "st:'ok'"))
# (d) circular 5237 (i) — read against the three papers
a, b, ln = row(" {d:'21 Nov 20:25 · Circular 5237, point (i) — vacant Govt / Coastal places'")
assert ln.count("st:'open'") == 1
ln = field(ln, 'exp', new="Board till 25 Nov: a vacant Govt or Coastal place went to SAAGAR project cargo, else to a vessel that quoted 30K / 25K (Sr No 7).")
ln = field(ln, 'act', new="The port has said nothing yet (Mihir, 25 Nov 14:47); he asked for the clause to be read against the three papers it names. WHAT THE PAPERS SAY — (1) Policy of 24.03.2025, on allocation: the vacant berths are assessed in the Order of Allotment, a vessel of a higher category ahead of a lower one. (2) Circular of 21.05.2026, the table in force: Sr 1 Govt (2 berths) · Sr 2 Coastal (1) · 3(A) Higher productivity (2) · 3(B) SAAGAR (2) · 3(C) 24 hours (1) · 3(E) 8,000 / 6,500 (1). With no Govt or Coastal vessel, the place went to the 30,000 / 25,000 / 10,000 quotes, by seniority. (3) Corrigendum of 09.07.2026: the 48-hour wait for a Govt vessel is withdrawn; a vessel standing in a Govt place moves to Sr No 7 when a Govt vessel comes; HP ceiling 50,000; Sr No 7 is created for the berths remaining after Sr 1 to 6. (4) Circular 5237 (i): with no suitable Govt / Coastal vessel, allotment goes down the order up to and including Sr. No. 3(B).")
ln = field(ln, 'why', new="RESULT ON PAPER: a vacant Govt place goes to a Coastal vessel, then to an HP bid, then to the SAAGAR line by seniority; a vacant Coastal place to an HP bid, then SAAGAR. The 30K / 25K quote comes only after these. With no vessel bidding for HP (Mihir, 25 Nov), a vacant Govt or Coastal place goes straight to SAAGAR — and CD Glory is SGR 1. TWO WEAK POINTS: (a) the corrigendum of 09.07.2026 calls the 24-hour category \"Sr. No. 3(B)\" in a heading, though the table of 21.05.2026 has SAAGAR at 3(B) and 24 hours at 3(C). Circular 5237 itself calls the 6,500 line \"3(E)\" and Bitumen \"Sr. No. 5\" — the numbering of the 21.05.2026 table — so its 3(B) is SAAGAR; but the port could point to that heading. (b) 5237 does not strike out the 30K / 25K quote in words; it says the rest stays in force. The board reads the quote as what is left when no Coastal, HP or SAAGAR vessel can use the berth. NOT YET SEEN AT A MEETING: the one Govt place given since 23 Nov went to a Govt vessel (Zheng Hui). First test: the Govt place Parvraj leaves and the Coastal place behind Lila Tokyo — programmes 26.11 and 27.11.")
assert ",fix:'" not in ln and ln.count(",st:'open'") == 1
ln = ln.replace(",st:'open'", ",fix:'',st:'open'")
ln = field(ln, 'fix', new="IN THE CALCULATION from 25 Nov 15:00 (v272), on the paper reading. If a programme prints a 30K quote in a Govt or Coastal place while a SAAGAR vessel the berth suits is waiting, the board goes back to the quote and this check is closed against the reading.")
put(a, b, ln)
# (e) new row — Mihir's word of 25 Nov
NEW = {'d': '25 Nov 14:47 · Mihir — after the meeting of 25 Nov',
       'v': 'How the berths are given — four points from Mihir.',
       'exp': "Board till now: Meghna Prestige and Pacific Apex were given berths on an HP bid, by their HP numbers; Star New London and Hai Nam 81 took the vacant Coastal and Govt places on 30K quotes; CD Glory waited for Asian Summit's SAAGAR place (about 29 Nov).",
       'act': "Mihir: (1) Asian Summit is under SAAGAR, not HP. (2) No vessel bid for the HP category. (3) Berthing goes by the vacant places, in order of priority, first. (4) Lila Tokyo was the senior vessel; the port had by mistake allotted the movement to Hai Nam 81.",
       'why': "The HP numbers on the list are the seniority of vessels that declared for it — they are not bids. With no bid the two HP places stand unused, and under circular 5237 (i) a vacant Govt or Coastal place passes HP and reaches SAAGAR.",
       'fix': "(1) Already entered as printed. (2) No berth is given on an HP bid until a programme prints one. (3) Confirmed — each vacant place is taken in order of priority and the vessel gets the berth that suits her. (4) The check of 23 Nov is closed. TWO THINGS OF THE BOARD'S OWN: a berth no line up to General can use, with an HP place unused, goes to the senior 30K / 25K vessel it suits (Sr No 7 = the berths remaining after Sr 1 to 6, corrigendum of 09.07.2026; \"no berth is left vacant\", Mihir 22 Nov) — not yet seen on a programme; and Xin Hai Tong 71 is counted in the Project / Steel place, as list 25.11 prints her (the board had her in a Govt place).",
       'st': 'ok'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(NEW) + ",\n")

# ---------- circular register: what 5237 (i) does on the board ----------
B.rep("(i) OPEN — Mihir, 21 Nov 20:25: it needs the port\\'s confirmation; he will tell after the berthing meeting of Monday 23 Nov. Till then the board keeps the old way for vacant Govt / Coastal places (SAAGAR project cargo, else a 30K / 25K quote vessel).",
      q("(i) ON THE BOARD from v272 (25 Nov 15:00): read, at Mihir's asking, against the policy of 24.03.2025, the circular of 21.05.2026 and the corrigendum of 09.07.2026 — a vacant Govt place goes to a Coastal vessel, then an HP bid, then the SAAGAR line by seniority; a vacant Coastal place to an HP bid, then SAAGAR; a 30K / 25K quote only after that. The port has not yet given a place this way — the check stays open till a programme shows it."))

# ---------- CD Glory: her card (OPTS) and the log of readings (MYLOG) ----------
i = B.s.index("routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:1},note:'") + len("routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:1},note:'")
j = B.s.index("'},\n  {label:'6.5K / 8K'", i)
B.s = B.s[:i] + q("SHE IS SGR 1 — FIRST OF THE SAAGAR LINE (list 25.11). There are two ways in. (A) HER LINE'S OWN TWO PLACES: both taken — AG Varvara at CJ-13 into December, Asian Summit at CJ-7 with a list ETC of 28 Nov 22:59 (sooner if she keeps her pace). (B) A VACANT GOVT OR COASTAL PLACE, under circular 5237 (i): with no Govt / Coastal vessel the place goes down the order — Coastal, HP bid, SAAGAR. Mihir (25 Nov): no vessel is bidding for HP — so the place reaches the SAAGAR line, and she is its senior vessel. The Coastal place opens when Jumbo Kinetic (two cranes, a 14-hour call the board expects at CJ-14 tonight) is gone, on the evening of 26 Nov; the board puts CD Glory there about 26 Nov 19:30 — a matter for the meeting of 26 Nov. THIS RESTS ON THE CIRCULAR AS WRITTEN: the port has not yet given a Govt or Coastal place this way. If it keeps to the 30K / 25K quote, she is back on (A): the night of 27 Nov to early 29 Nov. Timber desk (24 Nov): ETB 27 Nov.") + B.s[j:]

def mylog(name, rd):
    i = B.s.index("'" + name + "':[", B.s.index('const MYLOG')); j = B.s.index("\n ],", i)
    assert B.s[j - 1] == '}', B.s[j - 30:j]
    B.s = B.s[:j] + ",\n  " + js(rd) + B.s[j:]
mylog('CD Glory', {'d': '25 Nov 15:00 · Mihir — no HP bid · circular 5237 (i) read against the policy papers', 'exp': '11-26 19:36', 'b': '14',
  'slot': "A vacant Coastal place under circular 5237 (i) — she is SGR 1 · CJ-14 behind Jumbo Kinetic, 26 Nov about 19:30 · on the circular as written, not yet seen at a meeting",
  'why': "Two days earlier than this morning, and by a different door. Mihir (14:47): no vessel bid for the HP category, and berthing goes by the vacant places, in order of priority. He asked for circular 5237 (i) to be read against the policy of 24.03.2025, the circular of 21.05.2026 and the corrigendum of 09.07.2026. On those papers a vacant Govt or Coastal place, with no vessel of its own, goes down the order: Coastal, then an HP bid, then SAAGAR — 3(B) in the table of 21.05.2026 — and only after that to a 30K / 25K quote. With no HP bid it reaches SAAGAR, and CD Glory is SGR 1. Places in sight: the Govt place Parvraj leaves today, and the Coastal place behind Lila Tokyo (out about 26 Nov 01:36). The coastal vessels come first — the tug Varahi with her barge, and Jumbo Kinetic, a 14-hour call at CJ-14 — and CD Glory follows Jumbo Kinetic into CJ-14 on the evening of 26 Nov; it is for the meeting of 26 Nov to give. WHAT IT RESTS ON: the wording of the circular. The port has not yet filled a Govt or Coastal place under it, and the timber desk's ETB (27 Nov) does not count on it. Weak points: the corrigendum of 09.07.2026 calls the 24-hour category \"3(B)\" in one heading, and 5237 does not strike out the 30K quote in words. If the port gives these places to 30K quotes as before, her date is this morning's: Asian Summit's SAAGAR place, the night of 27 Nov to early 29 Nov. RANGE: evening of 26 Nov to early 29 Nov."})
mylog('Paiwan Ace', {'d': '25 Nov 15:00 · Mihir — no HP bid · circular 5237 (i) read against the policy papers', 'exp': '11-29 03:55', 'b': '15',
  'slot': "SAAGAR (SGR 4) — her line's own place when Asian Summit sails, about 29 Nov · ONLY IF the three log vessels ahead of her go in on vacant Govt / Coastal places under circular 5237 (i) · the earliest, not the date",
  'why': "The same reading that brings CD Glory forward. On the circular as written the vacant Coastal and Govt places go to the SAAGAR line while nobody bids for HP: CD Glory (SGR 1) on 26 Nov, Dariya Priya (2) on 27 Nov, African Tiger (3) on 28 Nov. That leaves the SAAGAR place Asian Summit vacates — list ETC 28 Nov 22:59 — to Paiwan Ace: a free bulk place may be given to a log vessel when no SAAGAR bulk vessel is waiting. Four berthings must fall this way before hers, and the port has not yet given one Govt or Coastal place under the circular. If it keeps to the 30K quote, she is back on the desk's dates: 7 Dec under SAAGAR, 2 Dec under 6.5K. Treat 29 Nov as the EARLIEST."})

B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='25 Nov 2026 · 15:10 IST';", B.s, count=1)
B.save(); print('saved C')
