#!/usr/bin/env python3
# apply74e — v278 part 5 (after the trim): next-meeting section — a Govt place held by a 30K-quote vessel is open to a GOVT vessel
# (she never blocks one) but is NOT a vacant place for another quote / SAAGAR vessel under circular 5237 (i). Seen with Hai Nam 81 "GOV(30K)".
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html')
B.rep("&&!(L==='HP'&&(v.cat==='GEN'||v.cat==='STL'))); // who holds a line's places at that hour",
      "&&!(L==='HP'&&(v.cat==='GEN'||v.cat==='STL'))); // who holds a line's places at that hour\n"
      "  const holdAll=(L,t)=>V.filter(v=>v.cat!=='SPACE'&&lineOf(v)===L&&v.F<=t+0.01&&eff(v)>t+0.01); // the same, counting a quote vessel standing in a Govt place — for the lines BELOW Govt that place is taken")
B.rep("if(!c.length&&(L==='GOV'||L==='COASTAL')&&!r.up.some(g=>g.v5)){", "if(!c.length&&(L==='GOV'||L==='COASTAL')&&holdAll(L,r.t).length<C.max&&!r.up.some(g=>g.v5)){")
B.save()
