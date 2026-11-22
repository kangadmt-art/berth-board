# v256 — header band: the board's own mark, a line drawing of the quay, and a strip of the berths
# drawn to quay length. Decoration only: no data block, no rule, no projection input is touched.
# Mihir, 22 Nov 16:35 asked for a design / logo at the top (draft first); 16:44 "tumhe acha lage woh kar do" -> draft B.
import re, sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
assert 'class="top band"' not in s, 'already applied'

MARK = '''<svg class="bmark" viewBox="0 0 48 48" aria-hidden="true"><defs><clipPath id="bmc"><circle cx="24" cy="24" r="20.4"/></clipPath></defs><circle cx="24" cy="24" r="22" fill="#111b26" stroke="#c9a24c" stroke-width="1.7"/><circle cx="24" cy="24" r="19" fill="none" stroke="rgba(201,162,76,.5)" stroke-width=".7" stroke-dasharray="1 1.9"/><g clip-path="url(#bmc)"><path d="M29 23.6C34 22.6 38.5 19 43 12.5" fill="none" stroke="#e3c377" stroke-width="1.25" stroke-linecap="round"/><rect x="15.2" y="12.6" width="17.6" height="6.6" rx="3.1" fill="#c9a24c"/><path d="M20.4 19h7.2l1.3 9.2h-9.8z" fill="#c9a24c"/><rect x="12.8" y="27.8" width="22.4" height="3.6" rx="1.3" fill="#c9a24c"/><path d="M19.9 22.3q4.1 1.9 8.2 0M19.6 24.6q4.4 1.9 8.8 0" fill="none" stroke="#111b26" stroke-width="1.05" stroke-linecap="round"/><path d="M9 36.2c2.5-1.7 5-1.7 7.5 0s5 1.7 7.5 0 5-1.7 7.5 0 5 1.7 7.5 0" fill="none" stroke="#5cc8ff" stroke-width="1.5" stroke-linecap="round"/><path d="M13 40c1.8-1.2 3.7-1.2 5.5 0s3.7 1.2 5.5 0 3.7-1.2 5.5 0 3.7 1.2 5.5 0" fill="none" stroke="#5cc8ff" stroke-width="1.25" stroke-linecap="round" opacity=".65"/></g></svg>'''
SCENE = '''<svg class="hscene" viewBox="0 0 460 120" aria-hidden="true" fill="none" stroke="#c9a24c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M0 100H300V114"/><path d="M30 100v-6h6v6M160 100v-6h6v6M282 100v-6h6v6"/><path d="M78 100l8-30h12l8 30M82 86h20M84 70V58h16v12M92 58l58-32M92 58V40l58-14M150 26v26"/><path d="M198 100l8-30h12l8 30M202 86h20M204 70V58h16v12M212 58l56-28M212 58V42l56-12M268 30v30"/><path d="M112 100l22-18 22 18"/><path d="M310 84h142l-12 18H322z"/><path d="M410 84V62h26v22M414 68h18M424 62v-8h8v8M318 84V70"/><path d="M330 84v-5h18v5M354 84v-5h18v5M378 84v-5h18v5"/><path d="M306 110c6-4 12-4 18 0s12 4 18 0 12-4 18 0 12 4 18 0 12-4 18 0 12 4 18 0 12-4 18 0 12 4 18 0"/></svg>'''
# the strip follows the quay panels in BERTHS (CJ-11/12 = KICT, shown hatched)
m = re.search(r"const BERTHS=\[(.*?)\n\];", s, flags=re.S); assert m
pan = {a: (float(b), float(c)) for a, b, c in re.findall(r"\{id:'([^']+)',p:\[([\d.]+),([\d.]+)\]", m.group(1))}
assert len(pan) == 17 and pan['1'][0] == 0 and pan['16'][1] == 189, pan
cells = [(k, pan[k][0], pan[k][1]) for k in ['1','2','3','4','5','6','7','8','9','10']] + [('KICT', pan['11'][0], pan['12'][1])] + [(k, pan[k][0], pan[k][1]) for k in ['13','14','15','15A','16']]
RULE = '<div class="qrule" aria-hidden="true">' + ''.join('<i%s style="width:%.3f%%">%s</i>' % (' class="k"' if n == 'KICT' else '', (b - a) / 189 * 100, n) for n, a, b in cells) + '</div>'

CSS = '''/* v256 header band — the board's own mark, a quay line drawing and a strip of the berths to quay length. Decoration only. */
header.top.band{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:14px;padding:16px 18px 38px;background:linear-gradient(135deg,#17293d 0%,#111b26 58%,#0f1419 100%)}
.brandrow{display:flex;gap:14px;align-items:center;position:relative;z-index:1}.bmark{width:58px;height:58px;flex:none}
.indep{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.05em;color:var(--muted);opacity:.85;margin-top:5px}
header.top.band .asof{position:relative;z-index:1}
.hscene{position:absolute;right:14px;top:12px;width:min(420px,36%);opacity:.26;pointer-events:none}
.qrule{position:absolute;left:0;right:0;bottom:0;height:22px;display:flex;border-top:1px solid rgba(201,162,76,.5);background:rgba(0,0,0,.28);font-family:var(--f-mono);font-size:9.5px;color:#c9a24c;pointer-events:none}
.qrule i{font-style:normal;flex:0 0 auto;box-sizing:border-box;border-right:1px solid rgba(201,162,76,.35);display:flex;align-items:center;justify-content:center;overflow:hidden;white-space:nowrap}.qrule i:last-child{border-right:0}
.qrule i.k{color:#7d8c9b;background:repeating-linear-gradient(135deg,transparent 0 4px,rgba(255,255,255,.045) 4px 8px)}
@media (max-width:900px){.hscene{opacity:.14}}
@media (max-width:640px){header.top.band{padding:13px 14px 34px;margin:0 -10px}header.top.band .eyebrow{letter-spacing:.08em;margin-bottom:3px}
.brandrow{display:grid;grid-template-columns:auto 1fr;column-gap:11px;row-gap:0}.brandrow>div{display:contents}.brandrow .eyebrow{grid-column:1/-1;grid-row:1}.bmark{grid-column:1;grid-row:2/span 2;width:46px;height:46px}.brandrow h1{grid-column:2;grid-row:2}.brandrow .owner{grid-column:2;grid-row:3}.brandrow .indep{grid-column:1/-1;grid-row:4}.indep .lg{display:none}
.hscene{top:auto;bottom:24px;right:8px;width:150px;opacity:.3}.qrule{font-size:8.5px;height:20px}
body[data-view="timber"] .hscene,header.top.band:has(.srcmore[open]) .hscene{display:none}body[data-view="timber"] header.top.band{padding-bottom:42px}}
@media (max-width:380px){header.top.band{padding:13px 12px 34px}.brandrow{column-gap:9px}.bmark{width:40px;height:40px}header.top.band h1{font-size:31px}header.top.band .eyebrow{letter-spacing:.05em}}
'''
a = '@media (max-width:640px){.owner{justify-content:space-between}}\n</style>'
assert s.count(a) == 1
s = s.replace(a, '@media (max-width:640px){.owner{justify-content:space-between}}\n' + CSS + '</style>', 1)

a = '  <header class="top">\n    <div>\n      <div class="eyebrow"'
assert s.count(a) == 1
s = s.replace(a, '  <header class="top band">' + SCENE + RULE + '\n    <div class="brandrow">' + MARK + '<div>\n      <div class="eyebrow"', 1)
m = re.search(r'(<div class="owner">.*?</div>)\n    </div>\n    <div class="asof">', s, flags=re.S); assert m
s = s[:m.start()] + m.group(1) + '\n      <div class="indep">Independent board<span class="lg"> · built from DPA&rsquo;s daily papers</span> · not an official DPA page</div>\n    </div></div>\n    <div class="asof">' + s[m.end():]
open(P, 'w', encoding='utf-8').write(s)
print('header band applied', len(s))
