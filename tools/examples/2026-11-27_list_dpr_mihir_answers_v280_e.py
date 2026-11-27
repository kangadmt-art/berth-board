#!/usr/bin/env python3
# apply76e — v280 (after the trim): the Open questions tab when nothing is open.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html')
B.rep("if(!LEARN.length){el.innerHTML='<div class=\"empty\">No variance recorded yet.</div>';return;}",
      "if(!LEARN.length){el.innerHTML='<div class=\"empty\">Koi sawal khula nahi — no open question. Every question so far is answered and in the rule book; the full record is in the data book.</div>';const vb0=document.getElementById('vb-sawal');if(vb0)vb0.textContent='0 open · all answered';return;}")
B.save()
