#!/usr/bin/env python3
# apply62c — v266: the "… ki jagah mein · … vessel" chip (.mbh) on the Priority page was nowrap and ran past the card on a phone,
# which made the whole page scroll sideways (page 413 px wide on a 390 px screen; there since the chip came in, v260). It may wrap now. Display only.
P = '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
a = ".mbh{display:inline-block;font-family:var(--f-mono);font-size:11px;color:var(--pill-tx);border:1px solid var(--pill-line);border-radius:4px;padding:0 6px;margin-left:7px;vertical-align:1px;white-space:nowrap;font-weight:400}"
assert s.count(a) == 1
s = s.replace(a, a + "\n@media (max-width:640px){.mbh{white-space:normal;max-width:calc(100% - 8px)}}")
a = "UPDATED='23 Nov 2026 · 15:56 IST'"
assert s.count(a) == 1
s = s.replace(a, "UPDATED='23 Nov 2026 · 16:01 IST'")
open(P, 'w', encoding='utf-8').write(s); print('saved')
