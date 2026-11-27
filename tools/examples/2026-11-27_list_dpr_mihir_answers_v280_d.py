#!/usr/bin/env python3
# apply76d — v280 part 4: the seven questions closed with Mihir's answers (27 Nov 10:19), own-vessel readings, CD Glory's options.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
def js(o): return "'" + q(o) + "'"
def lrow(dkey): a = B.s.index(" {d:'" + dkey); b = B.s.index("\n", a); return a, b
def close(dkey, ans):
    a, b = lrow(dkey); ln = B.s[a:b]
    m = re.search(r",fix:'((?:[^'\\]|\\.)*)'", ln); assert m, dkey
    ln = ln[:m.start(1)] + q("MIHIR, 27 Nov 10:19 — " + ans + " ANSWERED AND CLOSED. Before:") + ' ' + m.group(1) + ln[m.end(1):]
    assert ",st:'open'}" in ln, dkey; ln = ln.replace(",st:'open'}", ",st:'reference'}"); B.s = B.s[:a] + ln + B.s[b:]
close("26 Nov 15:14 · Xin Bo — our salt vessel on the expected sheet", "\"In today's berthing list it will be declared.\" The board waits for the list revised after the meeting of 27 Nov and takes her line and readiness from it.")
close("26 Nov 15:14 · Katerina K at CJ-6 — General past its two senior vessels", "\"Katerina K as 3rd General, the 1st General is Safi Alfa and the 2nd General is Blue Shark.\" She took the third General place; DSM London at CJ-2 is in the Bitumen place. The calculation stays as the port acted: General goes to the senior vessel the berth suits.")
close("25 Nov 23:52 · CJ-16 non-clean cargo", "\"Aggregates is not dirty cargo.\" They are not counted on the CJ-16 tab — as it already stood.")
close("25 Nov 17:06 · our vessels by stevedore", "\"No such vessel.\" No waiting or expected vessel is ours as stevedore only; ours are the vessels with agent Mihir.")
close("25 Nov 16:33 · revised list 25.11 — Steel / Project ranks", "\"Josco Taicang is under Steel, already mentioned in the berthing list, and Jumbo Kinetic is under Coastal.\" The STL / PRJ column now counts on the board: Josco Taicang STL 1, Kang Qi Fu Hua STL 2.")
close("25 Nov 16:11 · programme 26.11 — MSC Magali", "\"MSC Magali and other 5 vessels bid for HP and most senior MSC Magali got movement in HP.\" The vessels of the HP column are the bidders; a vacant HP place goes to the senior-most of them the berth suits (HP_NO_BID is off from v280).")
close("23 Nov 14:10 · programme 24.11 — the meeting of 23 Nov", "\"Please go through the berthing list.\" The list decides: a vessel the later list prints ready and ranked is counted so, whatever hold the team had reported.")

def mylog(name, e):
    k = " '%s':[\n" % name; a = B.s.index("const MYLOG={"); i = B.s.index(k, a); j = B.s.index("\n ],", i)
    B.s = B.s[:j] + ",\n  {" + ",".join(kk + ":" + js(e[kk]) for kk in ('d', 'exp', 'b', 'slot', 'why')) + "}" + B.s[j:]
mylog('CD Glory', {'d': '27 Nov 10:19 · list 27.11 + DPR 27.11 + Mihir on HP bids and Steel', 'exp': '11-29 01:50', 'b': '15',
 'slot': 'SAAGAR (SGR 1) — Asian Summit\'s place; berth CJ-15 behind Xin Hai Tong 71, 29 Nov about 02:00 — or CJ-5 on 28 Nov afternoon if no HP bidder takes that berth',
 'why': 'A day later than last night, for two reasons. (1) ASIAN SUMMIT LOST HALF A DAY TO HER SHIFT: 13,600 MT in the day against 26,200 the day before; 16,899 left at 07:00 on 27 Nov → about 28 Nov 12:50 at that rate. The list has her at CJ-5 with ETC 28 Nov 22:59 — so her place is outside what today\'s meeting can see on the port\'s own ETC, unless her agent declares the earlier finish. '
        '(2) MIHIR, 27 Nov: the HP column vessels are bidders. The second HP place is vacant, and HP stands above SAAGAR — when CJ-5 frees, the board gives the BERTH to Rex (HP 5, ball clay; the HP vessels senior to her cannot use CJ-5) and CD Glory, who has the SAAGAR place, takes the next berth that suits her: CJ-15, when Xin Hai Tong 71 is done — 1,767 MT a day now, 3,006 left → about 28 Nov 23:50. '
        'So: 28 Nov afternoon at CJ-5 if Rex is not seated there; otherwise CJ-15 about 29 Nov 02:00. Either way it is for the meeting of 28 Nov, not today\'s, unless Asian Summit\'s early completion is declared today. New Joyful (petcoke, SGR Y, ETA 28 Nov 05:00) is still the SAAGAR bulk vessel to watch.'})
mylog('Paiwan Ace', {'d': '27 Nov 10:19 · list 27.11 + DPR 27.11 + Mihir on HP bids and Steel', 'exp': '12-02 22:37', 'b': '16',
 'slot': 'a General place (GEN 18) at CJ-16, about 2 Dec night — the earliest, not the date',
 'why': 'About a day earlier than yesterday\'s reading and by a different door: with the HP column counted as bidders (Mihir, 27 Nov) the salt and clay vessels clear through the HP places, and the log vessels ahead of her go faster — CD Glory about 29 Nov, Dariya Priya a vacant Coastal place at CJ-14 about 1 Dec, African Tiger CJ-15A about 2 Dec. '
        'She then gets CJ-16 behind Kang Qi Fu Hua (Steel, a one-day call) about 2 Dec 22:30 — in a General place, before a SAAGAR place comes round to her (SGR 4). Revised ranks: SGR 4 · 8K 8 · GEN 18 (the list prints "Paiwan Ice"). Every step is an estimate on an estimate.'})
a = B.s.index("const OPTS={'CD Glory':{fixed:[],"); b = B.s.index("\nconst OPTRES=", a)
B.s = B.s[:a] + ("const OPTS={'CD Glory':{fixed:[],\n routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:1},note:'" + q(
  "SHE IS SGR 1 — FIRST OF THE SAAGAR LINE (list 27.11). Her way in is her line's own place, which Asian Summit holds: shifted to CJ-5, 16,899 MT left at 07:00 on 27 Nov, about 28 Nov 12:50 at the pace of the shift day; list ETC 28 Nov 22:59. "
  "THE BERTH: CJ-5 itself if no HP bidder takes it (Rex, HP 5, is the one CJ-5 suits) — otherwise CJ-15 behind Xin Hai Tong 71, about 29 Nov 02:00. For the meeting of 28 Nov; for today's only if Asian Summit's early completion is declared. "
  "New Joyful (petcoke, SGR Y, ETA 28 Nov 05:00) is the SAAGAR bulk vessel that could come in ahead for the bulk place.") + "'},\n"
  "  {label:'6.5K / 8K',only:'8K',rk:{'8K':5},note:'" + q("CLOSED. Mihir (20 Nov 16:50): she cannot berth under the 6.5K priority while others are senior in it. She is 8K 5 (list 27.11); Crystal Land 1, Glimlit 2, Porto Fiscardo 3 and Captainannis L 4 stand ahead — for Manta Sena's place (about 30 Nov) and for the Bitumen berth, CJ-2, which now goes to this line for break bulk only (corrigendum 26.11.2026).") + "'},\n"
  "  {label:'General · by seniority',only:'GEN',rk:{GEN:10},note:'" + q("NOT HER WAY IN. She is GEN 10 (list 27.11); General's three places are Safi Alfa, Blue Shark and Katerina K (Mihir, 27 Nov). The SAAGAR place comes first in any case.") + "'}]}};") + B.s[b:]
# Shree Krishna IX is a Bunder-basin vessel: readiness kept off so the cargo-jetty lines do not seat her
B.rep(" ['Shree Krishna IX','Steel slabs',2242,'MT',76,3.4,'11-27 05:30',{},", " ['Shree Krishna IX','Steel slabs',2242,'MT',76,3.4,null,{},")
B.save(); print('saved 76d')
