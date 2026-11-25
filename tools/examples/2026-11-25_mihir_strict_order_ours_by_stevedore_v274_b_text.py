#!/usr/bin/env python3
# apply70b — v274 part 2: the record of Mihir's word of 25 Nov 17:02 in the checks and in CD Glory's readings; stamp. Run: python3 apply70b.py '25 Nov 2026 · HH:MM IST'
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o):
    if isinstance(o, str): return "'" + q(o) + "'"
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def field(ln, k, pre):
    m = re.search(r"(?<=[{,])" + k + r":'((?:[^'\\]|\\.)*)'", ln)
    if not m: B.die('field ' + k)
    return ln[:m.start(1)] + q(pre) + m.group(1) + ln[m.end(1):]
a, b = B.line_of(" {d:'23 Nov 14:10 · programme 24.11 — the meeting of 23 Nov'"); ln = B.s[a:b]
ln = field(ln, 'fix', "MIHIR, 25 Nov 17:02 — (1) is now IN THE CALCULATION, in his words: allotment strictly in the prescribed order of priority, then a suitable available berth by LOA, draft, cargo and working needs. The place is the senior vessel's; if the berth in hand does not suit her but another berth of the same meeting window does, the place waits for her there. ")
B.s = B.s[:a] + ln + B.s[b:]
a, b = B.line_of(" {d:'25 Nov 16:11 · programme 26.11 — MSC Magali \"HP(50K)\" at CJ-16'"); ln = B.s[a:b]
ln = field(ln, 'fix', "MIHIR, 25 Nov 17:02: confirmed — a gearless vessel of coal or iron ore berths at CJ-16 (coded for coal and iron ore / pellets; she keeps CJ-7 / 8 too). The question on HP bids is still open. ")
B.s = B.s[:a] + ln + B.s[b:]
NEW = {'d': '25 Nov 17:02 · Mihir — order of priority, then the berth · our vessels',
       'v': 'How a berth is given, and which vessels are ours.',
       'exp': "Board till now: each berth, as it came free, went to the first vessel in the order of priority that the berth suited — so a junior could take a place because the berth in hand did not suit her senior. Our vessels = agent Mihir & Company only.",
       'act': "Mihir: (1) a gearless vessel of coal or iron ore berths at CJ-16. (2) Berthing allotment shall be made strictly in accordance with the prescribed order of priority, and the vessel shall thereafter be allocated a suitable available berth, considering its LOA, draft, cargo and operational requirements. (3) Where Mihir & Company is the stevedore too, the vessel is ours and is to be treated as ours.",
       'why': "The allotment and the berth are two steps: who berths is settled by the order of priority; which berth she gets is settled afterwards by what suits her.",
       'fix': "(1) Coded. (2) The place now waits for the senior vessel when a berth she can use comes free in the same meeting window on a declared sailing; only if no berth of the window suits her does the next vessel take it — for the Govt, Coastal, 24-hrs, 6.5K and Project places and for the lines a vacant Govt / Coastal place goes down to under circular 5237 (i). General was already strict. (This is the 9 Nov reading, withdrawn on 11 Nov and now back by the later word.) The projection of today does not move. (3) A vessel is ours when Mihir & Company is her agent OR her stevedore — the DPR's stevedore column, or Mihir's word for a vessel not yet on a DPR.",
       'st': 'ok'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(NEW) + ",\n")
i = B.s.index("'CD Glory':[", B.s.index('const MYLOG')); j = B.s.index("\n ],", i); assert B.s[j - 1] == '}'
RD = {'d': '25 Nov 17:02 · Mihir — strictly by the order of priority, then a suitable berth', 'exp': '11-26 23:55', 'b': '4',
      'slot': "Unchanged — a vacant Govt place under circular 5237 (i), CJ-4 behind Safi Alfa, 26 Nov about midnight · for the meeting of 26 Nov",
      'why': "The rule Mihir gave is now in the calculation: the place goes strictly by the order of priority and the berth is found for the vessel afterwards. For Parvraj's Govt place the order under the circular is: a coastal vessel first (Jumbo Kinetic — the Coastal place itself is taken by the tug), then an HP bid, then SAAGAR (CD Glory). Jumbo Kinetic can lie only at CJ-13 to 16, and none of those has a DECLARED sailing inside the 26 Nov window — CJ-15 (Xin Hai Tong 71, project cargo, no ETC), CJ-15A (African Hornbill, the same) and CJ-14 (the tug, no norm) are all the board's estimates — so the board does not hold the place for her and it comes to CD Glory at CJ-4. IF THE AGENTS DECLARE THOSE SAILINGS AT THE MEETING, Jumbo Kinetic takes the Govt place at one of them and CD Glory waits for the next place: the Coastal place behind the tug or Zheng Hui's Govt place, both about the evening of 27 Nov — the timber desk's date. The other weak links stand as written at 16:11: the circular not yet applied by any meeting; a possible HP bid; Safi Alfa's list ETC of 28 Nov. RANGE: midnight of 26 Nov to the evening of 29 Nov; 27 Nov evening is the likeliest if the circular is applied."}
B.s = B.s[:j] + ",\n  " + js(RD) + B.s[j:]
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='" + sys.argv[1] + "';", B.s, count=1)
B.save(); print('saved 70b')
