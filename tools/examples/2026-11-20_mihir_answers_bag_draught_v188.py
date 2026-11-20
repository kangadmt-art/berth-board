#!/usr/bin/env python3
# apply33 — v188: Mihir's three answers of 20 Nov 11:24 (Ocean Kudos not ready — list typo; Manta Sena most senior in 6.5K / 8K; laytime starts after 12 hours)
# + the board's own correction found while checking them: the 11.2 m loaded-draught step for BAG loaders starts at 35,000 MT, not 30,000. argv[1] = UPDATED.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P, list_tag='MIHIR (20 Nov 11:24)'); q = B.q
UPD = sys.argv[1]
B.rep("const NOW=h('11-20 10:36');", "const NOW=h('11-20 11:24');")
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
B.rep("<summary>Sources, rules &amp; tide</summary><div>", "<summary>Sources, rules &amp; tide</summary><div>20 Nov 11:24 — Mihir: Ocean Kudos is NOT ready (the \"B'TODAY\" on list 20.11 is a typing error); Manta Sena is now the most senior in 6.5K / 8K; timber laytime starts 12 hours after arrival. Board correction: a bag loader of up to 35,000 MT can lie at CJ-1 to 4 (New Bliss, 34,000 MT, is loading at CJ-1) · ")

# ---- the board's own step, corrected from the port's berthings
B.rep("const q=+w.q||0;return q>=40000?12.5:q>=30000?11.2:(w.dr||0);};",
      "const q=+w.q||0,st=isBag(w.c||'')?35000:30000;return q>=40000?12.5:q>=st?11.2:(w.dr||0);}; // 20 Nov: for BAG loaders the 11.2 m step starts at 35,000 MT — the port has New Bliss (sugar bags 34,000 MT) loading at CJ-1 and DSM London (32,700 MT) at CJ-2, both 10.5 m berths; North Gate left CJ-2 at 9.5 m with 24,000 MT on board. The 30,000 step had kept Manta Sena (30,170 MT) and Crystal Land (31,700 MT) off CJ-1 to 4;")

# ---- waiting rows
w = B.wrow
w('Ocean Kudos', "SHE IS NOT READY — the \"B\\'TODAY\" printed on list 20.11 is a typing error. Still held out of the projection")
w('Manta Sena', "she is now the MOST SENIOR vessel in 6.5K / 8K. Board (20 Nov): rice bags 30,170 MT can load at CJ-1 to 4 as well as at the clean berths")
w('Crystal Land', "Manta Sena stands ahead of her in 6.5K / 8K — the second \"8K 1\" on the sheet is her old, unrenumbered rank")

# ---- OPTS notes (CD Glory)
def note_of(label, text):
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('6.5K / 8K', "8K 8 on list 20.11 — the board's pick, but the WEAKER of her two routes now. Mihir (20 Nov 11:24): MANTA SENA is the most senior vessel in 6.5K / 8K. New Bliss leaves the 6.5K place inside the window of 21 → 22 Nov (DPR 20.11 pace 21 Nov 22:20, list ETC 22 Nov 10:05). By the rule of 11 Nov each berth, as it frees, goes to the senior vessel of the line that it suits: CJ-5 frees first (Ken Ann's 24 hours, about 19:30 on the 21st) and no vessel ahead of CD Glory can lie there — Manta Sena, Crystal Land and Pioneer Fortune load bags (CJ-1 to 4 or the clean berths), Uni Blossom goes by SAAGAR, Tan Bin 259 is working at MRG 3, Gokova-M needs CJ-7 / 8, Porto Fiscardo CJ-1 to 4. If the port instead keeps the place for Manta Sena — at CJ-1 behind New Bliss, the way Drake Well and New Bliss each followed the 6.5K vessel before them, or at CJ-15A — CD Glory goes by the General line, about three hours later.")
note_of('General · by seniority', "The General queue — GEN 20 on list 20.11. General berths by seniority with at most three bag vessels alongside (Mihir, 19 Nov). If the 6.5K place goes to Manta Sena, AG Varvara (GEN 16) takes CJ-5 and CD Glory takes CJ-1 when New Bliss leaves — about 22 Nov 00:20 at the DPR 20.11 pace (list ETC 22 Nov 10:05). This holds only while three bag vessels are alongside (DSM London, Katerina K and Aboudi D, if she gets CJ-3 today): with fewer, Blue Shark (GEN 2) or another bag vessel that fits CJ-1 goes ahead of her.")

# ---- MYLOG (CD Glory)
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 11:24 · Mihir — Manta Sena is the most senior in 6.5K / 8K',exp:'11-21 21:30',b:'5',slot:'6.5K / 8K — CJ-5, only if the place is not kept for Manta Sena · else General — CJ-1 about 22 Nov 00:20 · SAAGAR line about 23 Nov night · desk 25 Nov',why:'" + q(
 "Mihir (20 Nov 11:24): Manta Sena is now the most senior vessel in 6.5K / 8K, and Ocean Kudos is not ready (the B'TODAY on the list is a typing error). The date on the board does not move, but which route gives it matters. Checking Manta Sena, the board found its own draught step wrong for bag loaders: it had kept every bag vessel of 30,000 MT and more off CJ-1 to 4, yet New Bliss (34,000 MT) is loading at CJ-1 and DSM London (32,700 MT) at CJ-2 — corrected to 35,000 MT, so Manta Sena (30,170 MT) can lie at CJ-1 to 4 or a clean berth. By the as-it-frees rule CJ-5 still falls to CD Glory under 6.5K (it frees first and suits none of the seven ahead of her). If the port keeps the place for Manta Sena instead — the last two 6.5K vessels each took the berth of the one before — the re-run puts AG Varvara at CJ-5 (General) and CD GLORY AT CJ-1 ABOUT 22 NOV 00:20 by General, three hours later. That fallback needs three bag vessels alongside (DSM London, Katerina K, Aboudi D); if Aboudi D does not get CJ-3 today, a bag vessel senior to her (Blue Shark, GEN 2) can take CJ-1 first. So: the night of 21 Nov to the early hours of 22 Nov, CJ-5 or CJ-1. Laytime (arrival 15 Nov 06:42 + 12 hours, then 29,158 CBM at 4,000 a day) ends 23 Nov 01:38.") + "'}") + B.s[i:]

# ---- LEARN: the open entry answered + the draught-step correction
old_v = "TO CONFIRM WITH MIHIR: (1) Ocean Kudos is still printed \"B\\'TODAY\" on the waiting sheet — have her holds been passed, and for which berth? (2) 8K 1 is printed twice (Manta Sena and Crystal Land) — the board takes Manta Sena first, by reporting."
B.rep(old_v, "ANSWERED BY MIHIR (20 Nov 11:24): (1) Ocean Kudos is NOT ready — the \"B\\'TODAY\" on the list is a typing error. (2) Manta Sena is now the most senior in 6.5K / 8K. (3) Laytime starts after 12 hours — as the timber sheet counts it.")
old_f = "No rule changed. OPEN (1) Ocean Kudos — holds passed, which berth? OPEN (2) 8K 1 printed twice.',st:'open'},"
B.rep(old_f, "No rule changed. ANSWERED (Mihir, 20 Nov 11:24): (1) Ocean Kudos is not ready, the list has a typing error — she stays held. (2) Manta Sena is the most senior in 6.5K / 8K — as the board had her. (3) Laytime starts after 12 hours — the sheet already counts arrival + 12 h (CD Glory: from 15 Nov 18:42, ends 23 Nov 01:38); if he means 12 hours after BERTHING, the rule in §7 has to change.',st:'ok'},")
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 11:24 · board correction — where a bag loader of 30,000 MT and more can lie",
 "Found while checking Mihir's word that Manta Sena is the most senior in 6.5K / 8K: the board allowed her only the clean berths.",
 "Board's step (14 Nov): an export vessel of 30,000 MT or more loads to about 11.2 m, so she is kept off CJ-1 to 5 (10.5 m) — Manta Sena (30,170 MT) and Crystal Land (31,700 MT) could lie only at CJ-13 to 16.",
 "Port: New Bliss (sugar bags 34,000 MT) was berthed at CJ-1 under 6.5K (programme 17.11) and DSM London (rice / sugar bags 32,700 MT) at CJ-2 (programme 19.11); North Gate left CJ-2 at an outward draught of 9.5 m with 24,000 MT loaded; Porto Fiscardo (rice bags 50,000 MT) herself asks for CJ 1 – 4 on the list.",
 "The step was the board's own estimate, set from bulk loaders. Bag vessels of this size do load at CJ-1 to 4 — what they cannot take at the berth is finished at midstream.",
 "v188: for bag cargo the 11.2 m step starts at 35,000 MT (bulk stays at 30,000). Manta Sena and Crystal Land can now be seated at CJ-1 to 4 as well. The main run does not change for the coming window (CD Glory CJ-5, 21 Nov night); further out Manta Sena, not Pioneer Fortune, takes the next 6.5K berth. Mihir to say if a 30–35,000 MT bag loader is in fact kept off CJ-1 to 4.", "adopted"))
B.save()
