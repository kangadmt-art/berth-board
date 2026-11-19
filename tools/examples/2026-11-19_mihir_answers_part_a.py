#!/usr/bin/env python3
# apply23a — v177 (part 1): Mihir's four answers, 19 Nov 22:32 —
#  1. General berths by seniority; at most three bag vessels at a time (CONFIRMED).
#  2. African Hornbill berths under PROJECT priority, in the absence of an HP vessel.
#  3. Ocean Kudos: her holds were rejected, so her movement was cancelled.
#  4. HN Doris loaded her full quantity.
import shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v176.html')
B = Board(P, list_tag='MIHIR 19 Nov 22:32'); q = B.q
MI = "MIHIR (19 Nov 22:32)"
B.rep("const NOW=h('11-19 19:51');", "const NOW=h('11-19 22:32');")
B.rep("<summary>Sources, rules &amp; tide</summary><div>", "<summary>Sources, rules &amp; tide</summary><div>Mihir, 19 Nov 22:32: General berths by seniority with at most three bag vessels at a time (confirmed) · African Hornbill takes CJ-16 under Project priority in the absence of an HP vessel · Ocean Kudos's holds were rejected and her movement cancelled · HN Doris loaded her full quantity · ")
# ---- African Hornbill: Project priority, in the vacant HP place
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[175,188]"
B.note_prefix(M, q(MI + ": she berths under PROJECT priority, in the absence of an HP vessel — Ocean Kudos, who had the berth under HP, was cancelled when her holds were rejected. The board counts her against the vacant HP place; like a General cross-fill she does not keep a real HP vessel out.") + " ")
B.sub_entry(M, "cat:'SAAGAR',slot:'SPJ',via:'SAAGAR project parcel · category not printed yet',", "cat:'STL',slot:'HP',via:'Project priority · in the vacant Higher productivity place',")
# ---- HN Doris: full quantity
M = "{b:'16',n:'HN Doris (salt, next call)',nm:46000,p:[171.25,188]"
B.note_prefix(M, q(MI + ": SHE LOADED HER FULL QUANTITY (75,000 MT) — she did not leave short. DPR 19.11 had 41,858 MT still to load at 0700, so the last day ran far above the 17,542 MT of the day before.") + " ")
# ---- Ocean Kudos: holds rejected — held
a, b = B.line_of(" ['Ocean Kudos','Salt in bulk',70190,'MT',225,7.1,'11-18 16:06',{HP:0.5},")
B.s = B.s[:a] + (" ['Ocean Kudos','Salt in bulk',70190,'MT',225,7.1,null,{HP:98},'" + q(MI + ": HER HOLDS WERE REJECTED, so her movement was cancelled — that is why the evening signal of 19 Nov sent African Hornbill to the berth programme 19.11 had given her under HP(42.5K). HELD out of the projection until her holds are passed and she is ready again · salt in bulk 70,190 MT EXP · 225 m · reported 18 Nov 16:06 · 30K/25K/10K Sr No 7 · agent True Blue") + "'],") + B.s[b:]
# ---- rule code: a Project-priority vessel takes a berth against a vacant HP place before a General cross-fill does (Mihir, 19 Nov)
B.rep("!(C.k==='GOV'&&x.via)&&!(C.k==='HP'&&x.cat==='GEN')&&", "!(C.k==='GOV'&&x.via)&&!(C.k==='HP'&&(x.cat==='GEN'||x.cat==='STL'))&&")
B.rep("      if(vac.length){const g=genQ().filter(w=>onlyOK(w,'GEN','General · cross-fill'));",
      "      // Mihir (19 Nov): \"African Hornbill project priority mein lagega, in absence of HP\" — with no HP vessel for the berth, a Project-priority vessel takes it against the vacant HP place, even with the one project place in use (Heng Yuan Fa Zhan was alongside under PROJECT/STEEL the same night). She comes before the General cross-fill.\n"
      "      if(vac.includes('HP')){const pj=rkQ('STL').concat(pools.WIND()).filter((w,i,a)=>a.indexOf(w)===i&&onlyOK(w,'STL','Project · cross-fill'));if(pj.length)ranked.push({w:pj[0],cat:'STL',via:'Project priority · in the vacant Higher productivity place',slot:'HP'});}\n"
      "      if(!ranked.length&&vac.length){const g=genQ().filter(w=>onlyOK(w,'GEN','General · cross-fill'));")
B.rep("s:'2 berths · highest MTPD quote · no fallback in the regulation (Mihir, 1 Nov / 7 Nov): if nobody participates the berth goes down the order — SAAGAR, 24-hrs (else 30k/25k), 8K … lastly General'",
      "s:'2 berths · highest MTPD quote · no fallback in the regulation (Mihir, 1 Nov / 7 Nov): if nobody participates the berth goes down the order — SAAGAR, 24-hrs (else 30k/25k), 8K, a Project-priority vessel (19 Nov) … lastly General'")
# ---- priority chart: show how a vessel holds her place when it is not by her own rank
B.rep("${v.future?'<span class=\"mini w\">coming</span>':''}</td><td class=\"l\">${esc(v.c)}", "${v.future?'<span class=\"mini w\">coming</span>':''}${v.via?'<small>'+esc(v.via)+'</small>':''}</td><td class=\"l\">${esc(v.c)}")
B.save()
