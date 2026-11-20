#!/usr/bin/env python3
# apply34c — v189 (part 3, rule): ML Egret is not to be 'shifted' by the board's port-convenience rule.
# The port had programmed her shift (programme 20.11, to CJ-4) and then gave CJ-4 to Safi Alfa on the 12:40 signal sheet of 20 Nov.
# Left alone, the engine re-invents the same shift a day later into CJ-5 (behind Ken Ann) and hangs a whole chain on it
# (Belmoira CJ-15, Manta Sena CJ-15A, CD Glory CJ-1 on 22 Nov). A shift the port has just dropped is not projected again until a programme prints it.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
B.rep("const mov=o.filter(x=>CLEAN.includes(x.b)&&SHIFTABLE(x.c)&&", "const mov=o.filter(x=>!NO_SHIFT.has(x.n)&&CLEAN.includes(x.b)&&SHIFTABLE(x.c)&&")
B.rep("const PROG_SAIL=new Set([", "const NO_SHIFT=new Set(['ML Egret']); // vessels the board must NOT move under its port-convenience shift rule: the port programmed ML Egret's shift (programme 20.11) and then DROPPED it (HM signal 20 Nov 12:40 — Safi Alfa into CJ-4). Take a name out when a programme prints a shift for her again, or when she has sailed.\nconst PROG_SAIL=new Set([")
B.save()
