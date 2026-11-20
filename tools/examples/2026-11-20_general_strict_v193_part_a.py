#!/usr/bin/env python3
# apply38a — v193 (part 1, rule): Mihir (20 Nov 17:13) — "AG Varvara General me nahi aa sakta 21st ko, us vessel se kafi vessels senior hai. Tumhara calculation galat hai."
# GENERAL GOES STRICTLY BY SENIORITY: a General berth (and a General cross-fill) is given only to the senior-most ready vessel of the General line. If she cannot use
# the berth, or the three-bag limit keeps her out, the berth is NOT passed down to a junior. Until now the board skipped the capped / unsuited seniors and gave the
# berth to the next vessel that fitted (AG Varvara, GEN 16, over fourteen seniors).
# Also: Uni Blossom's estimated stay is taken at the record average of completed log vessels (5,606 CBM a day), not at the 4,600 norm, until the list prints her ETC.
import sys
sys.path.insert(0,'/home/claude/berth-board/tools')
from boardpatch import Board
B=Board('/home/claude/work/dpa-berth-board.html'); q=B.q
old="    const genQ=()=>baseUse.filter(w=>!(bagsNow>=3&&isBag(w.c))).sort((a,z)=>(a.rk.GEN||900+(a.rep||0)/1e4)-(z.rk.GEN||900+(z.rep||0)/1e4));"
new=("    // Mihir (20 Nov 17:13): \"AG Varvara cannot come in General on the 21st — many vessels are senior to her\". GENERAL IS STRICT SENIORITY (GEN_STRICT): the berth is offered\n"
     "    // only to the senior-most ready vessel still waiting in the General line (any berth). If this berth does not suit her, or the three-bag limit keeps her out, the General\n"
     "    // line takes nothing here — the berth is not passed down to a junior (it stays for the other groups, or empty). A vessel with no berth she could ever use is not counted.\n"
     "    const genKey=w=>(w.rk.GEN||900+(w.rep||0)/1e4);\n"
     "    const genTop=GEN_STRICT?W.filter(w=>!done.has(w.n)&&R(w)!=null&&R(w)<=e.t&&w.rep<=e.t&&meetOK(w,e.t)&&allowedBerths(w).length>0).sort((a,z)=>genKey(a)-genKey(z))[0]:null;\n"
     "    const genQ=()=>{const l=baseUse.filter(w=>!(bagsNow>=3&&isBag(w.c))).sort((a,z)=>genKey(a)-genKey(z));return (genTop&&l.length&&genKey(genTop)<genKey(l[0]))?[]:l;};")
B.rep(old,new)
B.rep("const NO_SHIFT=new Set(['ML Egret']);", "const GEN_STRICT=true; // Mihir (20 Nov 17:13): General goes strictly by seniority — a junior is not given a General berth past a ready senior; see genQ() in simulate()\nconst NO_SHIFT=new Set(['ML Egret']);")
# Uni Blossom: estimate at the record average of completed log vessels
B.sub_entry("{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]", "f:'11-21 02:30',t:'11-28 16:30',est:1", "f:'11-21 02:30',t:'11-27 08:00',est:1")
B.sub_entry("{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]", "norm 4,600 CBM a day assumed (ML Egret\\'s), to about 28 Nov 16:30", "no norm printed for her yet — taken at 5,600 CBM a day, the record average of the completed log vessels (the 4,600 norm would give 28 Nov 16:30; ML Egret is doing 8,070), to about 27 Nov 08:00")
B.rep("const NOW=h('11-20 16:50');", "const NOW=h('11-20 17:13');")
B.save()
