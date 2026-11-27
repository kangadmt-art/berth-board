#!/usr/bin/env python3
# apply79c — v283: the long note under "Quay by panel number" folds into a "how to read" line; one short sentence stays.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); s = B.s
a = s.index('<p class="qhelp">'); b = s.index('</p>', a) + 4; long = s[a + len('<p class="qhelp">'):b - 4]
c = s.index('</div>', b) + len('</div>')          # end of the section head
s = s[:a] + '<p class="qhelp">North (CJ-1) on the left, south (CJ-16) on the right. First the free space between vessels, then the quay drawn to scale. Move the slider to see another hour.</p>' + s[b:c] \
    + '\n    <details class="tdfull" style="margin:0 0 8px"><summary>How this picture is drawn · berth lengths, panel marks, draught</summary><p class="qhelp" style="margin-top:8px">' + long + '</p></details>' + s[c:]
B.s = s; B.save()
