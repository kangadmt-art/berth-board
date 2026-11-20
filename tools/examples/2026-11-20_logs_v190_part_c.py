#!/usr/bin/env python3
# apply35c — v190 (part 3, logs): UPDATED, meeting-call filter, CD Glory route notes, snapshot, prediction log, own-vessel log, lessons (with the correction of 12:52). argv[1] = UPDATED.
import re, sys, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P); q = B.q
S = json.load(open(W + 'S190.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]

# the meeting call names a vessel only if the projection really berths her around that window
B.rep("  const live=S.filter(x=>x.proj&&!x.shifted&&x.prevAt!=null&&fa(x)<=end).sort((a,z)=>fa(a)-fa(z));",
      "  const live=S.filter(x=>x.proj&&!x.shifted&&x.prevAt!=null&&fa(x)<=end&&x.F<=end+6).sort((a,z)=>fa(a)-fa(z)); // x.F<=end+6 (20 Nov, v190): a berth that frees inside the window but stays blocked (CJ-8 under Flag Marina; CJ-1 while the bag limit is full) must not put a vessel in the call that the projection itself berths days later")

# ================= OPTS notes =================
def note_of(label, text):
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "SAAGAR group — one bulk and one break-bulk place. Revised list 20.11: Uni Blossom (SGR 1), AG Varvara (2), Xin Hai Tong 71 (3 — project cargo), CD Glory (4), Dariya Priya (5), African Tiger (6). Uni Blossom takes Rome Trader's place tonight (programme 21.11: CJ-13, night berthing after 00:30). The next place is ML Egret's — about 24 Nov at the DPR pace, list ETC 28 Nov — and it is AG Varvara's. By this line alone CD Glory waits for Uni Blossom's place: about 27–28 Nov. The timber desk, after the meeting of 20 Nov, writes ETB 26 Nov.")
note_of('6.5K / 8K', "THE BOARD'S PICK — and a close call. 8K 9 on the revised list: Manta Sena 1, Crystal Land 2, Pioneer Fortune 3, Uni Blossom 4 (berthing by SAAGAR), Tan Bin 259 5, Gokova-M 6, Porto Fiscardo 7, Captainannis L 8. The 6.5K place opens when New Bliss leaves CJ-1 — about 21 Nov 22:20 at the DPR pace, list ETC 22 Nov 10:05 — and counts as open through the window of programme 22.11 (from 21 Nov 18:00). Programme 21.11 shifts Vishva Bandhan into CJ-5 on the evening of 21 Nov; at the DPR pace she is finished there about 20:00 (list ETC 22 Nov 14:33). If CJ-5 comes free BEFORE CJ-1 it goes down the 8K line, and none of the eight ahead can lie at CJ-5 — bag vessels load at CJ-1 to 4 or the clean berths, Gokova-M loads too deep — so it is CD Glory's: CJ-5, about 21 Nov 22:00. (Mihir, 11 Nov: the place is never held for a berth that frees later. Drake Well, 8K 10, took the place at CJ-1 on programme 13.11.) If New Bliss is out first, or the meeting of 21 Nov keeps the place for Manta Sena at CJ-1, this line is closed for her. The berth to ask for at that meeting is CJ-5 under 6.5K / 8K.")
note_of('General · by seniority', "The General queue — GEN 20. General berths by seniority with at most three bag vessels alongside (Mihir, 19 Nov); AG Varvara (GEN 16) stands ahead of her for any General berth both can use. By this line alone: CJ-15A about 25 Nov 01:40, against a vacant Higher-productivity place.")

# ================= PRED snapshot =================
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
SG = 'HM signal 20 Nov (12:40 sheet)'; PG = 'programme 21.11'
fixed = [
 ['Jag Pushpa', 'sails', '20 Nov 15:30', SG + ' · RT OUT · OJ-3 → SG Friendship'],
 ['Propel Confidence', 'sails', '20 Nov 17:00', SG + ' · RT OUT · CJ-4 → Safi Alfa'],
 ['Orchids', 'OJ-6', '20 Nov 17:30', SG + ' · IN on arrival · est'],
 ['Truong Minh Dream', 'sails', '20 Nov 18:15', PG + ' · CJ-6 · night sailing → Parvraj'],
 ['Safi Alfa', '4', '20 Nov 19:00', SG + ' · IN o/c at 23–31¾ · General, GEN 1 · est'],
 ['Jeil Crystal', 'sails', '20 Nov 19:00', PG + ' · OJ-2 → Hatnyanawati'],
 ['Meghna Prestige', 'sails', '20 Nov 19:39', PG + ' · CJ-7 · night sailing'],
 ['Hatnyanawati', 'OJ-2', '20 Nov 21:00', PG + ' · night berthing · est'],
 ['Parvraj', '6', '20 Nov 21:30', PG + ' · GOV · 43–51¼ · night berthing · est'],
 ['Woohyun Dream', 'TT-2', '20 Nov 22:30', PG + ' · Tuna · night berthing · est'],
 ['Bow Endeavour', 'sails', '20 Nov 23:30', PG + ' · OJ-4 → Eva Richway'],
 ['Rome Trader (salt, next call)', 'sails', '21 Nov 00:30', PG + ' · 12.9 m · night sailing → Uni Blossom · list ETC 04:40'],
 ['Eva Richway', 'OJ-4', '21 Nov 01:30', PG + ' · night berthing · est'],
 ['Uni Blossom', '13', '21 Nov 02:30', PG + ' · SGR · 113–124¾ · night berthing · est'],
 ['Seacon Monaco', 'sails', '21 Nov 15:00', PG + ' · CJ-9 → Yuan Hang Wei Ye'],
 ['Ken Ann', 'sails', '21 Nov 16:00', PG + ' · CJ-5 → Vishva Bandhan shifted in'],
 ['Yuan Hang Wei Ye (next call)', '9', '21 Nov 17:00', PG + ' · GFPL · 69–77¼ · est'],
 ['Vishva Bandhan', '5', '21 Nov 18:00', PG + ' · SHIFT from CJ-8, port a/c · 33¼–41½ · est'],
 ['Flag Marina', '7', '21 Nov 18:00', PG + ' · HP(42.5K) · 56¾–67¼, across CJ-7 and CJ-8 — after the shift · est'],
 ['Vishva Bandhan', 'sails', '21 Nov 20:00', 'DPR 20.11 pace, from CJ-5 — list ETC 22 Nov 14:33'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — project vessel'],
 ['Europa Graeca', 'sails', '21 Nov 21:45', 'DPR 20.11 pace · Tuna TT-1 → Blue Ionian'],
 ['New Bliss', 'sails', '21 Nov 22:21', 'DPR 20.11 pace — list ETC 22 Nov 10:05'],
 ['Nord Copper', 'sails', '22 Nov 03:03', 'list ETC at the 23,000 norm'],
 ['African Hornbill (blades, next call)', 'sails', '24 Nov 04:00', 'board estimate — no norm printed'],
 ['ML Egret', 'sails', '24 Nov 09:40', 'DPR 20.11 pace — list ETC 28 Nov 07:30 · stays at CJ-15'],
]
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-26 00:00']
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v190) — programme 21.11 and the revised list 20.11 on DPR 20.11 and the signal sheets of 20 Nov; to be read against the evening signal sheet, DPR 21.11, list 21.11 and programme 22.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a_), b_, c_, q(d_)) for a_, b_, c_, d_ in fixed + proj)) + B.s[j:]

# ================= PREDLOG =================
b0 = B.s.index("\n];", B.s.index("const PREDLOG=["))
AT = '11-20 15:13'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
def grow(n, b, t, note): return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',src:'prog',note:'%s'}" % (q(n), AT, b, t, q(note))
R = "20 Nov 15:13 re-run on programme 21.11 + the revised list 20.11 — "
new = [
 grow('Parvraj', '6', '11-20 21:30', 'programme 21.11 — GOV, 43–51¼, night berthing behind Truong Minh Dream (18:15); reading, not scored'),
 grow('Uni Blossom', '13', '11-21 02:30', 'programme 21.11 — SGR, 113–124¾, night berthing behind Rome Trader (00:30); reading, not scored'),
 grow('Yuan Hang Wei Ye (next call)', '9', '11-21 17:00', 'programme 21.11 — GFPL, 69–77¼, behind Seacon Monaco (15:00); reading, not scored'),
 grow('Flag Marina', '7', '11-21 18:00', 'programme 21.11 — HP(42.5K), 56¾–67¼ across CJ-7 and CJ-8, after Vishva Bandhan is shifted to CJ-5; reading, not scored'),
 prow('Aboudi D', R + 'General (GEN 12), CJ-3 — empty since Sea Gautham and not on programme 21.11, so not before its window ends'),
 prow('CD Glory', R + 'Mihir & Co — 6.5K / 8K (8K 9), CJ-5 when Vishva Bandhan, shifted in on the 21st, is done at the DPR pace — IF CJ-5 clears before New Bliss leaves CJ-1; none of the eight ahead in the line can lie at CJ-5. Else General about 25 Nov or SAAGAR about 27–28 Nov. Desk: 26 Nov'),
 prow('Belmoira', R + 'Sr No 7 quote against the Coastal place, CJ-15A after Heng Yuan Fa Zhan — no longer treated as HP'),
 prow('Hai Nam 81', R + 'Sr No 7 quote against a Govt place, CJ-14 after Xin Hai Tong 71 — she is due 22 Nov 16:00'),
 prow('AG Varvara', R + 'SAAGAR (SGR 2), CJ-16 after African Hornbill, when ML Egret\'s place opens at the DPR pace — CJ-5 is no longer hers: it goes to the 6.5K / 8K line'),
 prow('Tai Keystone', R + 'Govt (bulk urea), CJ-7 after Flag Marina — she needs CJ-7 / 8 and Flag Marina lies across both till about 24 Nov'),
 prow('Blue Shark', R + 'General (GEN 2), CJ-1 — first bag place to open, when Aboudi D is out'),
 prow('Sea Postman', R + 'General (GEN 22), CJ-6 after Parvraj'),
 prow('Dariya Priya', R + 'General against a vacant HP place, CJ-15 after ML Egret'),
 prow('Manta Sena', R + '6.5K / 8K (8K 1), CJ-14 — only because the place is taken by CD Glory at CJ-5 on the 21st; if the port keeps the place for her she goes to CJ-1 behind New Bliss about 22 Nov 00:20'),
]
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]

# ================= MYLOG =================
# correct the 12:52 entry for CD Glory — the misread note was not the cause
B.rep("(1) A BOARD ERROR: the date shown since 11:24 (CJ-5, 21 Nov 21:30 under 6.5K / 8K) stood on a note the board had misread, which kept Manta Sena to CJ-1 to 4. Corrected: she is the senior 8K vessel wherever she can lie, and the 6.5K place — CJ-1 behind New Bliss, about 22 Nov 00:20 — is hers.",
      "(1) [CORRECTED 20 Nov 15:13 — this entry first blamed a misread note about Manta Sena; a re-run shows that note changed nothing for CD Glory.] Ken Ann came in at 11:00 instead of 19:30, so CJ-5 was due to come free at midday on 21 Nov — inside programme 21.11's window, before the 6.5K place opens (New Bliss leaves on the night of the 21st). CJ-5 then falls to General, and the 6.5K place, when it opens, to Manta Sena at CJ-1.".replace("'", "\\'"))
g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 15:13 · programme 21.11 + list 20.11 revised after the meeting',exp:'%s',b:'%s',slot:'6.5K / 8K — CJ-5 about 21 Nov 22:00, IF CJ-5 (Vishva Bandhan, shifted in) clears before CJ-1 (New Bliss) · else General about 25 Nov / SAAGAR about 27–28 Nov · timber desk 26 Nov · revised list: SGR 4 · 8K 9 · GEN 20',why:'" % (g['F'], g['b']) + q(
 "Programme 21.11 does not name her — nothing she can use frees in its window. But it changes her prospect again, and this entry also CORRECTS the last one. (a) CORRECTION: at 12:52 the board said its earlier date (CJ-5, night of 21 Nov, 6.5K / 8K) had rested on a misread note about Manta Sena. A re-run shows that note changed nothing for CD Glory. What had moved her was the clock: Ken Ann came in at 11:00, so CJ-5 was due to come free at midday on the 21st — inside programme 21.11's window, before the 6.5K place opens. (b) Programme 21.11 now puts VISHVA BANDHAN into CJ-5 behind Ken Ann (out 16:00) — shifted from CJ-8 on the port's account, because Flag Marina (254 m) needs CJ-7 and CJ-8 together — and she finishes there: about 20:00 on the 21st at the DPR pace (15,488 MT left at 0700 on the 20th, at 10,860 a day), 22 Nov 14:33 by her list ETC. So CJ-5 comes free in the NEXT window, in which the 6.5K place is open (New Bliss leaves CJ-1 about 21 Nov 22:20 at her pace; list ETC 22 Nov 10:05). (c) The rule (Mihir, 11 Nov): each berth, as it frees, goes to the senior vessel of the line that the berth suits; the place is not held for a berth that frees later. None of the eight vessels ahead of her in 6.5K / 8K can lie at CJ-5 — the bag vessels load at CJ-1 to 4 or the clean berths, Gokova-M loads too deep, Uni Blossom berths tonight by SAAGAR. If CJ-5 clears first it is hers: about 21 Nov 22:00, done about 26 Nov 14:40. (d) It is a close call — the two berths are some two hours apart on yesterday's rates. If New Bliss is out first, or the meeting of 21 Nov keeps the place for Manta Sena at CJ-1, CD Glory is back to General (CJ-15A, about 25 Nov) or the SAAGAR line (about 27–28 Nov; SGR 4 now, behind AG Varvara and Xin Hai Tong 71). The desk says 26 Nov. The meeting of 21 Nov (11:00) decides it — the berth to ask for is CJ-5 under 6.5K / 8K. Laytime runs out 23 Nov 01:38.") + "'}") + B.s[i:]
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); e = B.s.index("\n ]\n};", a)
B.s = B.s[:e] + (",\n  {d:'20 Nov 15:13 · programme 21.11 — out 21 Nov 00:30',exp:'11-18 17:00',b:'13',slot:'alongside CJ-13 · SAAGAR · PROGRAMMED OUT 21 Nov 00:30 at 12.9 m, night sailing · list ETC 21 Nov 04:40 · DPR pace about 01:30',why:'" + q(
 "Programme 21.11 prints her outward readiness: 21 Nov 00:30, draught 12.9 m, NIGHT SAILING — with Uni Blossom into 113–124¾ behind her, night berthing. That is four hours inside her list ETC and an hour ahead of the DPR 20.11 pace: the 19,631 MT left at 0700 have to be on board by about 23:00, some 29,500 a day against 25,320 on the 19th. The board's 21:00 of this afternoon was read off the timber desk's hour for Uni Blossom (23:00) and was three and a half hours early; the berth reading (CJ-13) was right. Her let-go hour comes with DPR 21.11; after that she leaves this card.") + "'}") + B.s[e:]

# ================= LEARN =================
B.rep("And the board\\'s own date for CD Glory stood on a note it had misread (Manta Sena kept to CJ-1 to 4).",
      "[CORRECTED 20 Nov 15:13: the board also said here that its own date for CD Glory had stood on a misread note about Manta Sena. It had not — see the entry of 15:13. Ken Ann\\'s early berthing was the cause.]")
B.rep("OPEN (1) Uni Blossom\\'s berth and Rome Trader\\'s hour. OPEN (2) Parvraj\\'s berth.',st:'open'},",
      "ANSWERED by programme 21.11 (20 Nov 15:13): (1) Uni Blossom — CJ-13, 113–124¾, behind Rome Trader, as read; Rome Trader out 21 Nov 00:30, not 21:00. (2) Parvraj — CJ-6, 43–51¼, GOV.',st:'closed'},")
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 15:13 · programme 21.11 + list 20.11 revised after the meeting",
 "Programme 21.11 against the board — and a correction to what the board said at 12:52 about CD Glory. TO WATCH at the meeting of 21 Nov: does the 6.5K place go to CD Glory at CJ-5, or wait for Manta Sena at CJ-1?",
 "Board before the meeting (v187 / v188 — the frozen call): Aboudi D CJ-3 · Tai Keystone CJ-7 · Uni Blossom CJ-13 · Sea Postman CJ-8. After the signal sheets and the desk sheet (v189): Parvraj CJ-6 · Flag Marina CJ-7 that night · Uni Blossom CJ-13 at 23:00 with Rome Trader out about 21:00 · Aboudi D CJ-3 · AG Varvara CJ-5 by General when Ken Ann left.",
 "Programme 21.11: Parvraj CJ-6 (GOV, night berthing) · Flag Marina CJ-7 as HP(42.5K) at 56¾–67¼ — across CJ-7 and CJ-8, so VISHVA BANDHAN is shifted CJ-8 → CJ-5 on the port's account once Ken Ann is out (21 Nov 16:00), and Flag Marina comes in after that, not tonight · Uni Blossom CJ-13 behind Rome Trader, out 00:30 on 21 Nov · Yuan Hang Wei Ye CJ-9 (GFPL) · nothing for CJ-3 · no shift for ML Egret · Belmoira and Katerina K not on it (their at-berth rows are out of the revised list). Revised list: 8K renumbered (Manta Sena 1 … Captainannis L 8, CD Glory 9) · SGR (AG Varvara 2, Xin Hai Tong 71 3, CD Glory 4) · HP (Lila Tokyo 2, Flag Marina 3) · Parvraj GP 1 · Tai Keystone's readiness moved to 21 Nov 00:00 · MSC Magali reported 07:30.",
 "Meeting call 1 of 4 (Uni Blossom, berth too). The Govt place went to the vessel that reported that morning with GP printed, not to rock phosphate; Tai Keystone was still at sea; the HP place went by quote to a 254 m vessel that needs two berths, and the port made the room by shifting a working Govt vessel — a move the board does not foresee; CJ-3 stays empty though Aboudi D fits it. CORRECTION: at 12:52 the board told Mihir that its earlier date for CD Glory (CJ-5, night of 21 Nov) had rested on a misread note about Manta Sena. A re-run of v188 with the note corrected gives the same date — the note was not the cause. The cause was Ken Ann berthing eight hours early, which put CJ-5's freeing inside programme 21.11's window, before the 6.5K place opens.",
 "v190: programme and revised list entered — Parvraj, Flag Marina, Yuan Hang Wei Ye and Uni Blossom are fixed berth entries; Vishva Bandhan is carried at CJ-8 to about 18:00 on 21 Nov and then at CJ-5. Flag Marina is entered from the moment Vishva Bandhan leaves CJ-8: a vessel lying across two berths has to start when the neighbour berth empties, or the engine offers that berth to someone else. NOHP + Lila Tokyo (passed over for CJ-7 / 8) and + Belmoira (a Sr No 7 quote vessel, not HP — as HP she made the engine shift Uni Blossom out of CJ-13 the day after she berths). The meeting call names a vessel only if the projection berths her within six hours of the window's end. CD Glory: back to CJ-5 about 21 Nov 22:00 under 6.5K / 8K, if CJ-5 clears before CJ-1 — told to Mihir together with the correction.", "open"))
B.save()
