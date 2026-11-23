#!/usr/bin/env python3
# apply64 — v268: HEADINGS BOLD. Mihir 23 Nov 17:43: "isko computer mein kholte hain, wahan headings sab bold hone chahiye — ek baar dekh lena sab."
# What was thin: every card / section heading (h2, Big Shoulders 600 — reads light at 24 px on a wide screen), the table column heads
# (500–600; the mono ones asked for 700 but only 400 / 500 of IBM Plex Mono were loaded), the group bands inside tables, the small section labels (400).
# Now: headings 800 · table column heads and group bands 700 · small section labels 600; IBM Plex Mono 600 / 700 are loaded.
# Display only — no data, no projection change. Field labels, status chips and figure captions are left as they are (not headings).
import re
P = '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read(); n0 = len(s)
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:70])
    s = s.replace(a, b)

# 1) the mono face in real 600 / 700
rep("&family=IBM+Plex+Mono:wght@400;500&display=swap", "&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap")

# 2) light DOM — appended last in the main stylesheet so it wins over the rules above it
CSS = """
/* v268 headings bold — headings 800, table column heads and group bands 700, small section labels 600 */
h2,.sechead h2{font-weight:800}
th,.sdt th,.score th,.mt th,.mpt th,.mst th{font-weight:700}
tr.grp td:first-child{font-weight:700}
.eyebrow,.mine .ht,.mbey,.striplabel,.mbcont h3,.why h3,.oklist h3{font-weight:600}
"""
end = s.index('</style>')
s = s[:end] + CSS + s[end:]

# 3) the Priority chart (shadow root has its own stylesheet)
a = "table.pt td.v{min-width:132px;max-width:150px}table.pt{font-size:13px}}\n</style><p class=\"sub\">Port ki"
rep(a, "table.pt td.v{min-width:132px;max-width:150px}table.pt{font-size:13px}}\n/* v268 headings bold */\nh2{font-weight:800}table.pt th,table.rt th{font-weight:700}table.pt th small{font-weight:500}tr.grp td{font-weight:700}\n</style><p class=\"sub\">Port ki")

# 4) Salt page: the band above each table ("Loading at berth · 1") was an inline-styled div at 400
a = "const head=t=>`<div style=\"font-size:11px;letter-spacing:.12em;color:var(--muted);text-transform:uppercase;margin:14px 0 2px;padding:5px 8px;background:rgba(var(--ov-rgb),.04)\">${t}</div>`;"
rep(a, a.replace("font-size:11px;letter-spacing:.12em;", "font-size:11px;font-weight:700;letter-spacing:.12em;"))

# 5) the two small month tables (Timber arrivals, Salt loaded by month): their heads carried an inline 600
n = s.count('<th style="text-align:left;font-weight:600">') + s.count('<th style="font-weight:600">'); assert n >= 8, n
s = s.replace('<th style="text-align:left;font-weight:600">', '<th style="text-align:left;font-weight:700">').replace('<th style="font-weight:600">', '<th style="font-weight:700">')

s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='23 Nov 2026 · 17:50 IST';", s, count=1)
open(P, 'w', encoding='utf-8').write(s); print('saved', n0, '->', len(s))
