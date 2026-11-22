# v261 — the meeting section, SIMPLE VERSION (Mihir, 22 Nov 18:20). One rule: the vessel that leaves is replaced by the next vessel of her own
# priority; if that priority has none, by the one after it. Shown per berth, names straight from the list's rank columns.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
JS = open('/home/claude/work/mtg/meetboard5.js', encoding='utf-8').read()
CSS = open('/home/claude/work/mtg/meetboard5.css', encoding='utf-8').read()
a = s.index('// ---- NEXT MEETING, berth by berth'); b = s.index('function preview(){\n', a); s = s[:a] + JS + s[b:]
a = s.index('/* v257 Meeting page'); b = s.index('</style>', a); s = s[:a] + CSS + s[b:]
assert s.count('function meetBoard(') == 1 and s.count('let HPB_CAND=[]') == 1
old="const UPDATED='22 Nov 2026 · 18:12 IST';"; assert s.count(old)==1; s=s.replace(old,"const UPDATED='22 Nov 2026 · 18:27 IST';")
open(P, 'w', encoding='utf-8').write(s)
print('v261 simple section applied', len(s))
