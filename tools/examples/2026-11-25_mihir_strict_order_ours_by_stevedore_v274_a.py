#!/usr/bin/env python3
# apply70 — v274 — Mihir, 25 Nov 17:02:
#  1. "Yes gearless vessel of Coal and Iron ore will berth at CJ 16."
#  2. "Berthing allotment shall be made strictly in accordance with the prescribed order of priority, and the vessel shall thereafter be allocated a suitable
#     available berth, considering its LOA, draft, cargo and operational requirements."
#  3. "Jaha stevedoring mein bhi Mihir and Co ho, apna vessel hua to usko uske hisab se consider karne ka" — a vessel is OURS when Mihir & Company is her agent OR her stevedore.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q

# ---- 1. gearless coal / iron ore at CJ-16 — confirmed, and narrowed to what he named
B.rep("A=A.filter(b=>SHORECRANE.includes(b)||(OPEN16&&b==='16'&&(COAL(c)||DIRTY(c)))); // programme 26.11: MSC Magali (gearless, 253 m, coal) is given CJ-16 — a gearless coal / ore vessel keeps CJ-16 beside CJ-7 / 8",
      "A=A.filter(b=>SHORECRANE.includes(b)||(OPEN16&&b==='16'&&(COAL(c)||IRON(c)))); // Mihir (25 Nov 17:02): \"gearless vessel of Coal and Iron ore will berth at CJ 16\" — first seen on programme 26.11 (MSC Magali, 253 m, coal). She keeps CJ-7 / 8 as well.")

# ---- 2. the place goes strictly by the order of priority; the berth is found for the vessel afterwards
a, b = B.line_of("    const WINDOW_HOLD=false;")
B.s = B.s[:a] + ("    const WINDOW_HOLD=true; // Mihir (25 Nov 17:02): \"allotment strictly in accordance with the prescribed order of priority, and the vessel shall thereafter be allocated a suitable available berth, "
    "considering its LOA, draft, cargo and operational requirements\" — the PLACE is the senior vessel's; if THIS berth does not suit her but another berth she can use comes free in the same meeting window on a declared sailing, "
    "the place waits for her there and this berth goes down the order. If no berth of the window suits her, the next vessel in line is taken (policy 24.03.2025, para 1). "
    "This brings back the reading of 9 Nov, which Mihir had withdrawn on 11 Nov (\"no waiting inside the window\"); his word of 25 Nov is the later one.") + B.s[b:]
B.rep("if(WINDOW_HOLD&&cand.length&&['COASTAL','24H','8K','STL'].includes(C.k)&&inUse+1>=C.max){", "if(WINDOW_HOLD&&cand.length&&['GOV','COASTAL','24H','8K','STL'].includes(C.k)&&inUse+1>=C.max){")
B.rep("&&meetOK(w,e.t)&&RK(w,C.k)&&!ranked.some(r=>r.w===w)).sort((a,z)=>rkv(a,C.k)-rkv(z,C.k));\n        const sen=full.filter(x=>rkv(x,C.k)<rkv(cand[0],C.k));\n        const elsewhere=",
      "&&meetOK(w,e.t)&&RKG(w,C.k)&&!ranked.some(r=>r.w===w)).sort((a,z)=>rkv(a,C.k)-rkv(z,C.k));\n        const sen=full.filter(x=>rkv(x,C.k)<rkv(cand[0],C.k));\n        const elsewhere=")
# the same test, for the lines a vacant Govt / Coastal place goes down to under circular 5237 (i)
a, b = B.line_of("        const elsewhere=x=>{const A=allowedBerths(x);"); body = B.s[a:b].strip()
assert body.startswith("const elsewhere=x=>{") and body.endswith(";")
a2, b2 = B.line_of("      const SL=x=>x.slot||x.cat;")
B.s = B.s[:b2] + "\n      " + body.replace("const elsewhere=x=>{", "const elseW=x=>{", 1) + " // can she be served at ANOTHER berth that comes free inside this window on a declared sailing?" + B.s[b2:]
B.rep("const fc=pools[f](C.k).filter(w=>!ranked.some(r=>r.w===w)&&onlyOK(w,C.k,FBL[f]));if(fc.length){ranked.push({w:fc[0],cat:C.k,via:FBL[f],v5:FB5[f]||null});break;}}}",
      "const fc=pools[f](C.k).filter(w=>!ranked.some(r=>r.w===w)&&onlyOK(w,C.k,FBL[f]));\n"
      "        // strict order (Mihir, 25 Nov 17:02): the place belongs to the senior vessel of the line it comes down to; if this berth does not suit her but another berth of the window does, the place waits for her — no junior, and no later line, takes it here\n"
      "        const L5=FB5[f];if(WINDOW_HOLD&&L5&&inUse+1>=C.max&&!(f==='CSTQ'&&!o.some(x=>(x.slot||x.cat)==='COASTAL'))&&!(f==='HPB'&&HP_NO_BID)){\n"
      "          const all5=W.filter(w=>!done.has(w.n)&&R(w)!=null&&R(w)<=e.t&&w.rep<=e.t&&meetOK(w,e.t)&&RKG(w,L5)&&!ranked.some(r=>r.w===w)&&onlyOK(w,C.k,FBL[f])&&allowedBerths(w).length>0).sort((a,z)=>rkv(a,L5)-rkv(z,L5));\n"
      "          const s5=all5.filter(x=>!fc.length||rkv(x,L5)<rkv(fc[0],L5)).find(elseW);\n"
      "          if(s5){held.push({k:C.k,n:s5.n,r:rkv(s5,L5),skip:fc.length?fc[0].n:'the next line'});break;}}\n"
      "        if(fc.length){ranked.push({w:fc[0],cat:C.k,via:FBL[f],v5:FB5[f]||null});break;}}}")

# ---- 3. ours = agent OR stevedore Mihir & Company
B.rep("const stvOf=(n,t,te)=>{const r=STV[stvKey(n)];if(!r||!r.length)return '';",
      "const STV_SAID={}; // Mihir's word: a vessel for which Mihir & Company is the stevedore though another firm is her agent, before any DPR prints it — {'Vessel name':'Mihir & Co'}\n"
      "const stvOf=(n,t,te)=>{if(STV_SAID[n])return STV_SAID[n];const r=STV[stvKey(n)];if(!r||!r.length)return '';")
B.rep("const isMine=n=>/mihir/i.test(agOf(n)); // our vessels = agent Mihir & Company",
      "const isMine=n=>/mihir/i.test(agOf(n))||/mihir/i.test(stvOf(n)); // our vessels = Mihir & Company is the agent OR the stevedore (Mihir, 25 Nov 17:02: \"jaha stevedoring mein bhi Mihir and Co ho, apna vessel hua\")")
B.rep("mine=x=>/mihir/i.test(x.ag||''),MN=[", "mine=x=>/mihir/i.test(x.ag||'')||(!!x.n&&isMine(x.n)),MN=[")
B.rep("trO=n=>`<tr${mine({ag:agOf(n)})?' class=\"our\"':''}>`", "trO=n=>`<tr${mine({ag:agOf(n),n})?' class=\"our\"':''}>`")
B.rep("const ag=tr.ag||(AG[n]||''), mine=/mihir/i.test(ag);", "const ag=tr.ag||(AG[n]||''), mine=/mihir/i.test(ag)||isMine(n);")
B.rep("<p>Every vessel in the berthing list with agent Mihir &amp; Company, with where it stands today and when it berths.</p>", "<p>Every vessel in the berthing list for which Mihir &amp; Company is the agent or the stevedore, with where it stands today and when it berths.</p>")
B.rep("No vessel with agent Mihir &amp; Company in today\\'s berthing list", "No vessel with Mihir &amp; Company as agent or stevedore in today\\'s berthing list")
B.save(); print('saved 70')
