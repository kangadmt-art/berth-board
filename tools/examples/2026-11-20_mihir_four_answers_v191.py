#!/usr/bin/env python3
# apply36 — v191: Mihir's four answers of 20 Nov 15:53.
# (1) Rock phosphate is NOT government cargo. (2) Truong Minh Dream's (Govt priority) sailing was delayed, so Belmoira could not berth; the shifting of
# ML Egret was therefore not required and was cancelled. (3) Uni Blossom is senior in SAAGAR — she berths after Rome Trader sails.
# (4) Timber laytime: the simple rule — 12 hours free from arrival, no further rule.   argv[1] = UPDATED
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='MIHIR (20 Nov 15:53)'); q = B.q
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
B.rep("const NOW=h('11-20 15:13');", "const NOW=h('11-20 15:53');")

# ---- (4) timber laytime: 12 hours free from arrival, nothing else
B.rep("if(q&&nor!=null){const inFree=mf!=null&&mf<nor+DEM.free; ls=inFree?Math.max(nor,mf):nor+DEM.free;\n      lsHow=inFree?(mfA!=null?'at berthing, inside the '+DEM.free+' free hours':'at berthing — expected inside the '+DEM.free+' free hours'):'arrival + '+DEM.free+' h';",
      "if(q&&nor!=null){ls=nor+DEM.free; lsHow='arrival + '+DEM.free+' h'; // Mihir (20 Nov 15:53): the SIMPLE rule — 12 hours free from arrival, NO further rule. The clause of 16 Nov (\"or at berthing, if she is berthed inside those 12 hours\") is withdrawn.")
B.rep("the first 12 hours are free. Laytime starts when they end — or at\n// berthing, if she is berthed inside those 12 hours. Allowed = quantity",
      "the first 12 hours are free. Laytime starts when they end —\n// NO FURTHER RULE (Mihir, 20 Nov 15:53; the 16 Nov clause about berthing inside the 12 hours is withdrawn). Allowed = quantity")
B.rep("laytime starts when they end — or at berthing, if she is berthed inside those ${DEM.free} hours. Allowed time",
      "laytime starts when they end, whenever she berths — no other rule (Mihir, 20 Nov). Allowed time")

# ---- (1) rock phosphate is not government cargo
a, b = B.line_of("(()=>{const l=W.filter(w=>/\\b(urea|mop|npk|dap|tsp|dsp|ssp)\\b|fertil|sulphate|potash|phosphate/i.test(w.c)&&!/bag|acid|rock/i.test(w.c)")
B.s = B.s[:a] + "// Mihir (20 Nov 15:53): ROCK PHOSPHATE IS NOT GOVERNMENT CARGO — the cargo rule below skips it (the board's reading in v189, now confirmed).\n" + B.s[a:]
# ---- (2) ML Egret's shift: cancelled, not required
a, b = B.line_of("const NO_SHIFT=new Set(['ML Egret']);")
B.s = B.s[:a] + "const NO_SHIFT=new Set(['ML Egret']); // vessels the board must NOT move under its port-convenience shift rule. ML Egret — Mihir (20 Nov 15:53): her shift (programme 20.11, to CJ-4) was only to make room for Belmoira; Truong Minh Dream's sailing was delayed, Belmoira could not berth, so the shifting was NOT REQUIRED AND CANCELLED. Take a name out when a programme prints a shift for her again, or when she has sailed. (Without it the engine moves her into CJ-8 under Flag Marina — a shifted V entry has no LOA, so its run check is skipped.)" + B.s[b:]
B.note_prefix("{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]", q("MIHIR (20 Nov 15:53): her shift was only to make room for Belmoira. Truong Minh Dream's sailing was delayed, Belmoira could not berth — so the shifting was not required and is CANCELLED. She stays at CJ-15.") + " ")
B.note_prefix("{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]", q("MIHIR (20 Nov 15:53): senior in SAAGAR — she berths when Rome Trader has sailed.") + " ")
w = B.wrow
w('Belmoira', "she could NOT berth because the sailing of Truong Minh Dream (Govt priority) was delayed — the Govt place she was to take on her 30K quote did not open in time; ML Egret\\'s shift was therefore not required and was cancelled. The place has since gone to Parvraj (GP 1)")
w('Sea Postman', "ROCK PHOSPHATE IS NOT GOVERNMENT CARGO — she stands in General only (GEN 22)")

# ---- MEETLOG 19 Nov: the two programmed vessels that did not berth come out of the count
B.rep("  got:[['Belmoira','15'],['Ken Ann','5'],['Katerina K','6'],['Nord Copper','14'],['African Hornbill','16','signal']],\n  note:'Belmoira took a Govt place on her 30K quote and Katerina K a provisional berth; African Hornbill came in by the evening signal after Ocean Kudos\\' holds were rejected. The two General vessels the board named were passed over.'},",
      "  got:[['Ken Ann','5'],['Nord Copper','14'],['African Hornbill','16','signal']],\n  note:'" + q("Programmed but NOT berthed, so out of the count: Belmoira (a Govt place on her 30K quote, CJ-15) — Truong Minh Dream's sailing was delayed and the place did not open (Mihir, 20 Nov) — and Katerina K (provisional berthing, CJ-6), cancelled by Traffic. African Hornbill came in by the evening signal after Ocean Kudos' holds were rejected. The two General vessels the board named were passed over.") + "'},")

# ---- LEARN
B.rep("The port preferred the senior General vessel (Safi Alfa, waiting since 19 Oct) to its own programmed shift of ML Egret, so Belmoira\\'s clean berth did not open",
      "[CORRECTED by Mihir, 20 Nov 15:53: it was the other way round — Truong Minh Dream\\'s sailing was delayed, so Belmoira could not take the Govt place; ML Egret\\'s shift was then not required and was cancelled, which left CJ-4 for Safi Alfa.] The board had read: the port preferred the senior General vessel (Safi Alfa, waiting since 19 Oct) to its own programmed shift of ML Egret, so Belmoira\\'s clean berth did not open")
B.rep("RULES — (a) the automatic Govt rank by cargo no longer covers ROCK phosphate; (b) NO_SHIFT: a shift the port has dropped (ML Egret) is not projected again until a programme prints it;",
      "RULES — (a) the automatic Govt rank by cargo no longer covers ROCK phosphate [CONFIRMED by Mihir, 20 Nov 15:53: rock phosphate is not government cargo]; (b) NO_SHIFT: a shift the port has dropped (ML Egret) is not projected again until a programme prints it [Mihir, 20 Nov 15:53: the shifting was not required and cancelled];")
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 15:53 · Mihir — four answers",
 "(1) Rock phosphate is NOT government cargo. (2) The sailing of Truong Minh Dream (Govt priority) was delayed; because of that Belmoira could not berth, so the shifting of ML Egret was not required and was cancelled. (3) Uni Blossom is senior in SAAGAR, so she berths after Rome Trader sails. (4) Timber laytime — apply the simple rule: 12 hours free from arrival, no further rule.",
 "Board: (1) since v189 rock phosphate gets no automatic Govt rank — its own reading. (2) v189 had read the cancelled shift as the port preferring Safi Alfa (GEN 1) for CJ-4. (3) Uni Blossom at CJ-13 behind Rome Trader — read from the desk sheet, then printed on programme 21.11. (4) Laytime started 12 hours after arrival, OR at berthing if she berthed inside those 12 hours (16 Nov).",
 "Mihir's word, 20 Nov 15:53.",
 "(2) is the point the board had wrong. Belmoira was to berth as GOVT(30K) — a 30K quote against the Govt place that Truong Minh Dream was to vacate. Truong Minh Dream (list ETC 19 Nov 13:46) was still alongside through the window of programme 20.11 and sails only at 18:15 on 20 Nov, so the place never opened for Belmoira; with no Belmoira there was nothing to clear CJ-15 for, and ML Egret stayed. CJ-4 was then simply free — Safi Alfa. A quote vessel's berthing against a priority place stands or falls with the sailing of the vessel that holds the place.",
 "v191: (1) confirmed — no code change; the cargo rule already skips rock phosphate (Sea Postman, Princess Manissa). (2) notes on ML Egret and Belmoira corrected; ML Egret stays in NO_SHIFT (cancelled); in the 19 Nov meeting record Belmoira and Katerina K are taken out of the berthed count — they were programmed but did not berth. (3) confirmed, nothing to change. (4) CODE: laytime now starts at arrival + 12 h in every case — the clause about berthing inside the 12 hours is removed from the calculation and from the rule text on the Timber tab. No vessel on the sheet had berthed inside her 12 hours, so no figure moves (CD Glory: laytime from 15 Nov 18:42, ends 23 Nov 01:38).", "adopted"))
B.save()
