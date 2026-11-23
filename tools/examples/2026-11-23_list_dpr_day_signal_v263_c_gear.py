#!/usr/bin/env python3
# apply60c — v263 (part 3): gear of the vessels new on list 23.11 (looked up once, 23 Nov).
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
B.rep(" 'Arrabbiata':['G','4×30.5 t','4 cranes × 30.5 t · 40,358 DWT, built 2025','Shipfix vessel directory · IMO 9979515']\n};",
      " 'Arrabbiata':['G','4×30.5 t','4 cranes × 30.5 t · 40,358 DWT, built 2025','Shipfix vessel directory · IMO 9979515'],\n"
      " 'Jumbo Kinetic':['G','2×1,500 t','2 mast cranes × 1,500 t (3,000 t in tandem) · heavy-lift vessel, 14,000 DWT, built 2014','SAL / Jumbo fleet list · Cranepedia · IMO 9634165'],\n"
      " 'Sakizaya Star':['GL','','gearless · Kamsarmax 82,516 DWT, built 2020','The Freight vessel profile · VesselFinder · IMO 9861316']\n};")
B.rep("const GEAR_NONE=['Star New London',", "const GEAR_NONE=['KM Jakarta','Horizon Chaser','Saturn J','RB Leah','Star New London',")
B.save()
