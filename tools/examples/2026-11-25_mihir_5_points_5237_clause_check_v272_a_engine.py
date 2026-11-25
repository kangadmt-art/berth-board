#!/usr/bin/env python3
# v272 part A — engine: Mihir's word of 25 Nov 14:47 (no HP bid) + circular 5237 point (i) read against the policy papers
import sys; sys.path.insert(0,'/home/claude/berth-board/tools'); from boardpatch import Board
B=Board('/home/claude/work/dpa-berth-board.html'); q=B.q

# 1. nobody is bidding for HP
B.rep("W.forEach(w=>{w.noHP=NOHP.has(w.n);});",
"W.forEach(w=>{w.noHP=NOHP.has(w.n);});\n"
"const HP_NO_BID=true; // Mihir, 25 Nov 14:47: \"NO vessel bid for HP category\". While this is true no waiting vessel is given a berth on an HP bid, whatever her HP number on the list — the list number is seniority, not a bid. A vacant HP place goes down the order (a Project vessel, then General). Set to false when a programme prints an HP berthing or Mihir says a vessel has bid.\n"
"const HP_NO_BID_SRC='Mihir, 25 Nov 14:47';")
B.rep("if(k==='HP'){l=l.filter(w=>!w.noHP&&!(e.b==='5'&&IRON(w.c)));l=hpOrder(l);}",
      "if(k==='HP'){l=l.filter(w=>!w.noHP&&!(HP_NO_BID&&w.only!=='HP')&&!(e.b==='5'&&IRON(w.c)));l=hpOrder(l);}")
B.rep("let q=readyAll.filter(w=>RKG(w,C.k)&&!(C.k==='HP'&&w.noHP))", "let q=readyAll.filter(w=>RKG(w,C.k)&&!(C.k==='HP'&&(w.noHP||HP_NO_BID)))")

# 2. circular 5237 (i): a vacant Govt / Coastal place goes down the order — Coastal, HP bid, SAAGAR — and only then to a 30K / 25K quote
B.rep("{k:'GOV',l:'Govt priority',s:'2 slots · else Project SAAGAR · else 30k/25k (Sr No 7); a Sr No 7 vessel in a Govt slot never blocks a Govt vessel',max:2,fb:'WIND,HPQ'},",
      "{k:'GOV',l:'Govt priority',s:'2 places · with no Govt vessel: a Coastal vessel, then an HP bid, then the SAAGAR line by seniority (circular 5237 (i), from the 23 Nov meeting) · only then a 30k/25k quote; a vessel standing in a Govt place never blocks a Govt vessel',max:2,fb:'WIND,HPQ',fb5:'CSTQ,HPB,SGRQ,HPQ'},")
B.rep("{k:'COASTAL',l:'Coastal',s:'1 berth · else SAAGAR project (windmill / project) · else 30k/25k',max:1,fb:'WIND,HPQ'},",
      "{k:'COASTAL',l:'Coastal',s:'1 place · with no Coastal vessel: an HP bid, then the SAAGAR line by seniority (circular 5237 (i), from the 23 Nov meeting) · only then a 30k/25k quote',max:1,fb:'WIND,HPQ',fb5:'HPB,SGRQ,HPQ'},")
B.rep("const FBL={HPQ:'30k/25k quote (Sr No 7)',WIND:'SAAGAR project',GENQ:'General',K8Q:'6.5K line · vacant Bitumen place'};",
      "const FBL={HPQ:'30k/25k quote (Sr No 7)',WIND:'SAAGAR project',GENQ:'General',K8Q:'6.5K line · vacant Bitumen place',CSTQ:'Coastal vessel · circular 5237 (i)',HPB:'HP bid · circular 5237 (i)',SGRQ:'SAAGAR · circular 5237 (i)'};\n"
      "const FB5={CSTQ:'COASTAL',HPB:'HP',SGRQ:'SAAGAR'}; // the line a vessel comes from when she takes a vacant Govt / Coastal place under circular 5237 (i)")
B.rep(",GENQ:genQ,K8Q:()=>{", ",GENQ:genQ,CSTQ:()=>o.some(x=>(x.slot||x.cat)==='COASTAL')?rkQ('COASTAL'):[] /* a Coastal vessel takes a vacant Govt place only when the Coastal place itself is taken — else she takes her own */,HPB:()=>rkQ('HP'),SGRQ:()=>baseUse.filter(w=>RKG(w,'SAAGAR')).sort((a,z)=>rkv(a,'SAAGAR')-rkv(z,'SAAGAR')) /* the whole SAAGAR line by seniority — bulk, break bulk and project alike; the one-bulk / one-break-bulk split is for SAAGAR's own two places */,K8Q:()=>{")
B.rep("for(const f of ((C.k==='BIT'&&e.t>=POL2111)?'K8Q':C.fb).split(',')){const fc=pools[f](C.k).filter(w=>!ranked.some(r=>r.w===w)&&onlyOK(w,C.k,FBL[f]));if(fc.length){ranked.push({w:fc[0],cat:C.k,via:FBL[f]});break;}}}",
      "for(const f of ((C.k==='BIT'&&e.t>=POL2111)?'K8Q':(C.fb5&&e.t>=POL2111)?C.fb5:C.fb).split(',')){const fc=pools[f](C.k).filter(w=>!ranked.some(r=>r.w===w)&&onlyOK(w,C.k,FBL[f]));if(fc.length){ranked.push({w:fc[0],cat:C.k,via:FBL[f],v5:FB5[f]||null});break;}}}")
# among the picks for one berth such a vessel stands where her OWN line stands (a Coastal vessel for her own place comes before a SAAGAR vessel for a Govt place)
B.rep("    // Mihir (2 Nov): a vacant HP slot sends the berth down the order, \"lastly to General\"",
      "    // Circular 5237 (i): a vessel that takes a vacant Govt / Coastal place from further down the order stands, among the picks for THIS berth, where her own line stands —\n"
      "    // a Coastal vessel for the Coastal place comes before a SAAGAR vessel for a Govt place. (A 30k/25k quote keeps the turn of the place it fills, as before.)\n"
      "    if(ranked.some(r=>r.v5)){const own=r=>CATS.findIndex(c=>c.k===(r.v5||r.cat));const srt=ranked.map((r,i)=>({r,i})).sort((a,z)=>(own(a.r)-own(z.r))||(a.i-z.i));srt.forEach((x,i)=>{ranked[i]=x.r;});}\n"
      "    // Mihir (2 Nov): a vacant HP slot sends the berth down the order, \"lastly to General\"")
# options run: the vessel's own line also covers the place she takes under 5237 (i)
B.rep("on==='Q7'?/30k\\/25k/i.test(via||''):(cat===on&&!via));};", "on==='Q7'?/30k\\/25k/i.test(via||''):((cat===on&&!via)||(!!via&&via===FBL[{SAAGAR:'SGRQ',COASTAL:'CSTQ',HP:'HPB'}[on]])));};")
B.rep("on==='Q7'?/30k\\/25k/i.test(r.via||''):(r.cat===on&&!r.via)))ranked.splice(i,1);}", "on==='Q7'?/30k\\/25k/i.test(r.via||''):((r.cat===on&&!r.via)||(!!r.via&&r.via===FBL[{SAAGAR:'SGRQ',COASTAL:'CSTQ',HP:'HPB'}[on]]))))ranked.splice(i,1);}")

# 3. words on the board
B.rep("/30k\\/25k/i.test(v.via||'')?' · 30K quote':/project/i.test(v.via||'')?' · project':'');};",
      "/30k\\/25k/i.test(v.via||'')?' · 30K quote':/^SAAGAR ·/.test(v.via||'')?' ki jagah mein · SAAGAR vessel':/^Coastal vessel/.test(v.via||'')?' ki jagah mein · Coastal vessel':/project/i.test(v.via||'')?' · project':'');};")
B.rep("const queue=L=>L==='HP'?pool.map(c=>c.w):", "const queue=L=>L==='HP'?(HP_NO_BID?[]:pool.map(c=>c.w)):")
B.rep("HP mein bid hoti hai, order nahi<br>", "HP mein bid hoti hai, order nahi${HP_NO_BID?' — abhi HP mein kisi ne bid nahi ki ('+HP_NO_BID_SRC+')':''}<br>")
B.rep("if(w.noHP)t.push('passed over before');return t.join(' · ');};", "if(w.noHP)t.push('passed over before');if(HP_NO_BID)t.unshift('<b style=\"color:var(--warn)\">no bid at present</b>');return t.join(' · ');};")
B.rep("The board cannot see the bids, so it names no winner: it shows who bids at which meeting.`;",
      "The board cannot see the bids, so it names no winner: it shows who bids at which meeting.`+(HP_NO_BID?`<br><b style=\"color:var(--warn)\">No vessel is bidding for HP at present</b> (${HP_NO_BID_SRC}). The board gives no berth on an HP bid until a programme prints one; the list's HP numbers below are seniority only. A vacant HP place goes down the order.`:'');")
# Priority chart (its own copy of the helpers)
B.rep("const lineOf=p=>/^General/.test(p.via)?'GEN':/30k\\/25k/i.test(p.via)?'Q7':/SAAGAR project/.test(p.via)?'SAAGAR':p.cat;",
      "const lineOf=p=>/^General/.test(p.via)?'GEN':/30k\\/25k/i.test(p.via)?'Q7':/^SAAGAR (project|·)/.test(p.via)?'SAAGAR':/^Coastal vessel/.test(p.via)?'COASTAL':p.cat;")
B.rep("if(/SAAGAR project/.test(v))return 'SAAGAR project · in a vacant '+CL[p.cat]+' place';",
      "if(/SAAGAR project/.test(v))return 'SAAGAR project · in a vacant '+CL[p.cat]+' place';if(/^SAAGAR ·/.test(v))return 'SAAGAR · in a vacant '+CL[p.cat]+' place (circular 5237)';if(/^Coastal vessel/.test(v))return 'Coastal · in a vacant '+CL[p.cat]+' place (circular 5237)';")
B.rep("{k:'BIT',l:'Bitumen',p:'1 place · if no bitumen vessel, a General vessel takes it',max:1},", "{k:'BIT',l:'Bitumen',p:'1 place · if no bitumen vessel, the senior vessel of the 6.5K line takes it (circular 5237)',max:1},")
B.rep("{k:'Q7',l:'Sr No 7 · 30K / 25K quote',p:'no place of its own — takes a vacant Govt, Coastal or 24-hr place',max:0}];",
      "{k:'Q7',l:'Sr No 7 · 30K / 25K quote',p:'no place of its own — takes a vacant 24-hr place; a vacant Govt or Coastal place only when no Coastal, HP or SAAGAR vessel can use it (circular 5237)',max:0}];")
B.rep("{k:'GOV',l:'Govt priority',p:'2 places · fertiliser / Govt cargo, by seniority',max:2},", "{k:'GOV',l:'Govt priority',p:'2 places · fertiliser / Govt cargo, by seniority · if vacant: Coastal, HP bid, SAAGAR (circular 5237)',max:2},")
B.rep("{k:'COASTAL',l:'Coastal',p:'1 place',max:1},", "{k:'COASTAL',l:'Coastal',p:'1 place · if vacant: HP bid, then SAAGAR (circular 5237)',max:1},")
B.rep("{k:'HP',l:'Higher productivity',p:'2 places · goes to the highest MTPD quote of the day, not to the rank',max:2},", "{k:'HP',l:'Higher productivity',p:'2 places · goes to the highest MTPD quote of the day, not to the rank · no vessel is bidding at present (Mihir, 25 Nov)',max:2},")

# 4. as printed: list 25.11 has Xin Hai Tong 71 under PROJECT/STEEL, and two Govt vessels (Parvraj, Zheng Hui)
B.sub_entry("{b:'15',n:'Xin Hai Tong 71',p:[145.75,158.25]", "cat:'GOV',via:'printed \"PROJ\" — project cargo (SGR 2 on the list)'", "cat:'STL',via:'printed \"PROJ\" — project cargo (SGR 2 on the list)'")
B.save(); print('saved A')
