#!/usr/bin/env python3
# v272 part B — a berth nobody up the order can use, with an HP place unused: the Sr No 7 quote line takes it (corrigendum 09.07.2026 (iv): Sr No 7 = the berths remaining after Sr No 1 to 6)
import sys; sys.path.insert(0,'/home/claude/berth-board/tools'); from boardpatch import Board
B=Board('/home/claude/work/dpa-berth-board.html')
B.rep("if(g.length)ranked.push({w:g[0],cat:'GEN',via:'General · cross-fill (vacant '+(CL[vac[0]]||vac[0])+' slot)',slot:vac[0]});}}",
      "if(g.length)ranked.push({w:g[0],cat:'GEN',via:'General · cross-fill (vacant '+(CL[vac[0]]||vac[0])+' slot)',slot:vac[0]});}\n"
      "      // Corrigendum of 09.07.2026, para (iv): Sr No 7 — \"any vessel committing higher productivity\" — has the berths REMAINING after Sr No 1 to 6. With no HP bid (Mihir, 25 Nov) and the Govt / Coastal places going\n"
      "      // to SAAGAR under circular 5237 (i), a berth no line up to General can use would lie idle while 30K / 25K vessels wait; the senior quote vessel this berth suits takes it, in the HP place nobody bid for. Board's reading — not yet seen on a programme.\n"
      "      if(!ranked.length&&vac.includes('HP')){const q7=pools.HPQ('HP').filter(w=>onlyOK(w,'HP',FBL.HPQ));if(q7.length)ranked.push({w:q7[0],cat:'HP',via:FBL.HPQ});}}")
B.save(); print('saved B')
