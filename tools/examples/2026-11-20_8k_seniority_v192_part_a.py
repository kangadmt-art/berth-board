#!/usr/bin/env python3
# apply37a — v192 (part 1, rule): Mihir (20 Nov 16:50) — "MV CD Glory can not berth at CJ-5 in 6.5K priority as other vessels are senior than her in 6.5K priority".
# In the 6.5K / 8K line the place goes by SENIORITY: a junior does not take it at a berth her seniors cannot use (SENIOR_ONLY=['8K']). OPTS ranks brought to the revised list.
# (The first two replacements were applied by hand before this file was written; kept here as the record.)
import sys
sys.path.insert(0,'/home/claude/berth-board/tools')
from boardpatch import Board
B=Board('/home/claude/work/dpa-berth-board.html')
if "const SENIOR_ONLY=['8K'];" not in B.s:
    old="      if(cand.length){ranked.push({w:cand[0],cat:C.k,via:null});if(cand[1])ranked.push({w:cand[1],cat:C.k,via:null,same:1});continue;}"
    new=("      // Mihir (20 Nov 16:50): \"CD Glory can not berth at CJ-5 in 6.5K priority as other vessels are senior than her in 6.5K priority\" — in the 6.5K / 8K line the place goes\n"
         "      // by SENIORITY: a junior does not take it at a berth her seniors cannot use. The berth then goes down the order to the other groups and the place waits for the\n"
         "      // senior vessel's berth. (For this line it replaces the 11 Nov reading \"the place is never held\". A senior with no berth she could ever use is not counted.)\n"
         "      if(SENIOR_ONLY.includes(C.k)&&cand.length){\n"
         "        const fullS=W.filter(w=>!done.has(w.n)&&R(w)!=null&&R(w)<=e.t&&w.rep<=e.t&&meetOK(w,e.t)&&RK(w,C.k)&&!ranked.some(r=>r.w===w)&&allowedBerths(w).length>0).sort((a,z)=>rkv(a,C.k)-rkv(z,C.k));\n"
         "        const senS=fullS.filter(x=>rkv(x,C.k)<rkv(cand[0],C.k));\n"
         "        if(senS.length){held.push({k:C.k,n:senS[0].n,r:rkv(senS[0],C.k),skip:cand[0].n});continue;}\n"
         "      }\n")
    B.rep(old,new+old)
    B.rep("    const WINDOW_HOLD=false;", "    const SENIOR_ONLY=['8K']; // lines in which a junior never jumps a ready senior (Mihir, 20 Nov 16:50 — the 6.5K / 8K place)\n    const WINDOW_HOLD=false;")
B.rep("routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:5},", "routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:4},")
B.rep("{label:'6.5K / 8K',only:'8K',rk:{'8K':8},", "{label:'6.5K / 8K',only:'8K',rk:{'8K':9},")
B.rep("const NOW=h('11-20 15:53');", "const NOW=h('11-20 16:50');")
B.save()
