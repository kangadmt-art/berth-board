#!/usr/bin/env python3
# apply77b — v281: the HP line goes senior-first (Mihir, 27 Nov 10:19: "most senior MSC MAGALI got movement in HP"); the junior-first swap of 1 Nov is switched off.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
B.rep("const HP_NO_BID_SRC='Mihir, 27 Nov 10:19';", "const HP_NO_BID_SRC='Mihir, 27 Nov 10:19';\nconst HP_SENIOR_FIRST=true; // Mihir, 27 Nov 10:19: of the HP bidders the senior-most got the HP berth. The 1 Nov swap (junior commits 50k under HP, senior takes the comfortable 30k slot) is off; false brings it back.")
B.rep("    const hpOrder=list=>{ hpJunior=false; if(list.length<2)return list;\n      const sen=list.slice().sort((a,z)=>rkv(a,'HP')-rkv(z,'HP'));\n",
      "    const hpOrder=list=>{ hpJunior=false; if(list.length<2)return list;\n      const sen=list.slice().sort((a,z)=>rkv(a,'HP')-rkv(z,'HP'));\n      if(HP_SENIOR_FIRST)return sen;\n")
B.save()
