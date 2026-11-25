#!/usr/bin/env python3
# apply69d — v273 part 4: the next-meeting section follows circular 5237 (i) in the row it already has ("Upar ki priority · jagah khali"):
# a vacant Govt / Coastal place with no vessel of its own for this berth names the line the place goes down to — Coastal, HP bid, SAAGAR. No new row type.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
B.rep("if(L!=='HP'&&holdAt(L,r.t).length>=C.max)return;const c=queue(L).filter(suits);if(c.length&&r.up.length<2)r.up.push({L,ws:c.slice(0,2)});});",
      "if(L!=='HP'&&holdAt(L,r.t).length>=C.max)return;let c=queue(L).filter(suits),v5=null;\n"
      "      if(!c.length&&(L==='GOV'||L==='COASTAL')&&!r.up.some(g=>g.v5)){ // circular 5237 (i): the vacant place goes down the order — a Coastal vessel (when the Coastal place is taken), an HP bid, the SAAGAR line\n"
      "        if(L==='GOV'&&holdAt('COASTAL',r.t).length>=1){c=queue('COASTAL').filter(suits);if(c.length)v5='COASTAL';}\n"
      "        if(!c.length&&!HP_NO_BID){c=queue('HP').filter(suits);if(c.length)v5='HP';}\n"
      "        if(!c.length){c=queue('SAAGAR').filter(suits);if(c.length)v5='SAAGAR';}}\n"
      "      if(c.length&&r.up.length<2)r.up.push({L,ws:c.slice(0,2),v5});});")
B.rep("r.up.forEach(g=>{h+=grp(r.same?'Upar ki priority':'Lag sakti hai',g,r,r.same?'· jagah khali, berth ke wait mein':'');});",
      "r.up.forEach(g=>{h+=grp(r.same?'Upar ki priority':'Lag sakti hai',g,r,g.v5?'· jagah khali · circular 5237 se '+(MB_PR[g.v5]||g.v5)+' line ko':r.same?'· jagah khali, berth ke wait mein':'');});")
B.save(); print('saved 69d')
