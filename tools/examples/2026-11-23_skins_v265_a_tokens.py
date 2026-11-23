#!/usr/bin/env python3
# apply62a — v265 (part 1): every fixed colour in the stylesheet, markup and scripts becomes a named token whose default
# in :root is the colour it replaces. The default look ("Kandla Night") must come out pixel-identical; skins then only redefine tokens.
import re, sys
P = '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read(); n0 = len(s)

# 1) fallbacks that never fire (the token is defined) or that stand in for an undefined token
for a, b in (("var(--brass,#c9a24c)", "var(--brass)"), ("var(--warn,#e0a040)", "var(--warn)"), ("var(--ok,#5fbf7a)", "var(--ok)"),
             ("var(--bg,#0f1c2e)", "var(--bg)"), ("var(--text,#e8edf2)", "var(--fg)"), ("var(--accent,#7cc4ff)", "var(--link)")):
    assert s.count(a) >= 1, a
    s = s.replace(a, b)

# 2) literal -> token
MAP = {
 '#c9a24c': 'gold', '#e3c377': 'gold2', '#17293d': 'band-a', '#111b26': 'band-b',
 '#132339': 'hi-a', '#0f1c2e': 'hi-b', '#1a2740': 'hi-c', '#14212d': 'hi-d', '#1c2a3e': 'press', '#17303f': 'me-bg',
 '#e0a23a': 'amber', '#f0bd60': 'amber-tx', '#8a6a2a': 'amber-line', '#17100a': 'amber-ink',
 '#2f6f9c': 'pill-line', '#12314a': 'pill-bg', '#8fd6ff': 'pill-tx',
 '#8fd0ff': 'tx-info', '#7fb2ff': 'tx-exp', '#9be3b0': 'tx-ok', '#f3b86a': 'tx-warn', '#ff9d8a': 'tx-bad', '#f09a82': 'tx-bad2',
 '#e9a07a': 'tx-out', '#ff8a7a': 'tx-live', '#f3a7ab': 'tx-miss', '#e5636a': 'bad2', '#ff6a5a': 'bad3', '#f0c070': 'mnt-tx',
 '#18352a': 'tint-ok', '#3d2020': 'tint-bad', '#2a2f3f': 'tint-na', '#3a3220': 'tint-warn', '#2e1818': 'tint-live',
 '#234a35': 'line-ok', '#0f2219': 'tint-ok2', '#2c2616': 'tint-warn2',
 '#7d8c9b': 'mute2', '#8fa1b3': 'mute3', '#c5d0da': 'fg2', '#aab4c2': 'fg3',
 '#22303d': 'cell', '#1f2b36': 'cell2', '#1b242d': 'hatch-a', '#232e39': 'hatch-b', '#3a4856': 'hatch-c',
 '#1f2a35': 'chip', '#1d2731': 'rowline', '#1a2530': 'cardin',
 '#dfe7f2': 'tab-salt', '#c58bff': 'tab-ppp', '#d9b25f': 'tab-pri', '#4fd1c5': 'tab-barge',
 '#0b1420': 'ink', '#0e141b': 'ink2', '#2a3240': 'quay3', '#46566c': 'tick', '#6b7b90': 'tick2', '#12304b': 'wave',
 '#3a2a1a': 'mnt-a', '#5a4020': 'mnt-b', '#3d4c5a': 'dim2', '#4a5a69': 'dim3',
}
DIRECT = {'#0f1419': 'bg', '#161d24': 'panel', '#5cc8ff': 'brass'}   # literals that repeat an existing token
RGBA = {'92,200,255': 'acc-rgb', '201,162,76': 'gold-rgb', '255,255,255': 'ov-rgb'}

a = s.index(':root{'); b = s.index('}', a) + 1; root = s[a:b]
assert '--bg:#0f1419' in root and '--f-mono' in root
head, tail = s[:a], s[b:]
def tok(text):
    cnt = {}
    def r(m):
        h = m.group(0).lower()
        if h in MAP: cnt[h] = cnt.get(h, 0) + 1; return 'var(--%s)' % MAP[h]
        if h in DIRECT: cnt[h] = cnt.get(h, 0) + 1; return 'var(--%s)' % DIRECT[h]
        return m.group(0)
    text = re.sub(r'#[0-9a-fA-F]{6}\b', r, text)
    text = re.sub(r'#fff\b', lambda m: (cnt.__setitem__('#fff', cnt.get('#fff', 0) + 1), 'var(--sel)')[1], text)
    for k, v in RGBA.items():
        n = len(re.findall(r'rgba\(\s*' + k.replace(',', r'\s*,\s*') + r'\s*,', text))
        text = re.sub(r'rgba\(\s*' + k.replace(',', r'\s*,\s*') + r'\s*,', 'rgba(var(--%s),' % v, text); cnt[k] = n
    return text, cnt
head2, c1 = tok(head); tail2, c2 = tok(tail)
used = {}
for c in (c1, c2):
    for k, v in c.items(): used[k] = used.get(k, 0) + v
missing = [k for k in list(MAP) + list(DIRECT) + list(RGBA) if not used.get(k)]
assert not missing, missing
left = sorted(set(x.lower() for x in re.findall(r'#[0-9a-fA-F]{6}\b', head2 + tail2)))
print('literals still fixed:', left)

# 3) defaults — exactly the colours replaced
defaults = "\n  /* v265 — every fixed colour is a token; a skin (html[data-skin]) redefines tokens and nothing else */\n  " + \
    " ".join("--%s:%s;" % (v, k) for k, v in MAP.items()) + \
    "\n  --band-c:#0f1419; --link:#7cc4ff; --sel:#fff; --acc-rgb:92,200,255; --gold-rgb:201,162,76; --ov-rgb:255,255,255;\n}"
root2 = root[:-1].rstrip() + defaults
s = head2 + root2 + tail2

# the header band ends on its own token (a light skin keeps a dark masthead)
g = "background:linear-gradient(135deg,var(--band-a) 0%,var(--band-b) 58%,var(--bg) 100%)"
assert s.count(g) == 1, s.count(g)
s = s.replace(g, "background:linear-gradient(135deg,var(--band-a) 0%,var(--band-b) 58%,var(--band-c) 100%);color:var(--fg)")
open(P, 'w', encoding='utf-8').write(s); print('saved', n0, '->', len(s), '| replaced', sum(used.values()))
