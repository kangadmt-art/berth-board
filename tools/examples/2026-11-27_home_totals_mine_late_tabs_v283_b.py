#!/usr/bin/env python3
# apply79b — v283: the totals tile ends in one plain line (the page icons sit right under it).
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
a = B.s.index("every page has its icon below:"); b = B.s.index("</div></div>`;", a)
B.s = B.s[:a] + "every page has its icon below." + B.s[b:]
B.save()
