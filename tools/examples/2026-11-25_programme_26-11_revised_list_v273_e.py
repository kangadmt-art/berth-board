#!/usr/bin/env python3
# apply69e — v273 part 5: one more weak link named in CD Glory's reading (the coastal vessel ahead of SAAGAR for the Govt place); final stamp.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
B.rep(q("and the next timber berths are CJ-15 (Xin Hai Tong 71, no ETC) and CJ-14 behind the tug, 27 Nov evening. If the circular is not applied at all:"),
      q("and the next timber berths are CJ-15 (Xin Hai Tong 71, no ETC) and CJ-14 behind the tug, 27 Nov evening; (4) Jumbo Kinetic, a coastal vessel with the Coastal place taken, stands before SAAGAR for this same Govt place — she can lie only at CJ-13 to 16, so the board lets CJ-4 pass her by; if the port holds the place for her, CD Glory waits for the next one (the Coastal place behind the tug, or Zheng Hui's Govt place, both 27 Nov evening). If the circular is not applied at all:"))
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='" + sys.argv[1] + "';", B.s, count=1)
B.save(); print('saved 69e')
