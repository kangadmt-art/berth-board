# v258 — Meeting page: (1) "Port convenience" is not a priority (Mihir, 22 Nov 17:48) — a berth the engine gives to nobody in the window now
# gets its priority from the count run from the top; (2) every vessel on the page shows her details.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
JS = open('/home/claude/work/mtg/meetboard2.js', encoding='utf-8').read()
CSS = open('/home/claude/work/mtg/meetboard.css', encoding='utf-8').read()
a = s.index('// ---- MEETING page (Mihir, 22 Nov 2026)'); b = s.index('function preview(){\n', a)
s = s[:a] + JS + s[b:]
a = s.index('/* v257 Meeting page'); b = s.index('</style>', a)
s = s[:a] + CSS + s[b:]
assert s.count('function meetBoard(') == 1 and s.count('let HPB_CAND=[]') == 1
assert "Port convenience'" not in s
old = "const UPDATED='22 Nov 2026 · 17:42 IST';"
assert s.count(old) == 1; s = s.replace(old, "const UPDATED='22 Nov 2026 · 17:52 IST';")
open(P, 'w', encoding='utf-8').write(s)
print('meeting page v258 applied', len(s))
