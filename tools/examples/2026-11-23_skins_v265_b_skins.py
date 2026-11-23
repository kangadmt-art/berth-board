#!/usr/bin/env python3
# apply62b — v265 (part 2): colour themes ("skins") and the chooser in the header.
# A skin is html[data-skin="…"] redefining tokens; nothing else in the page changes. The choice is kept in localStorage('dpaSkin').
# "data-skin", not "data-theme": the artifact host may set data-theme on the root itself.
import re, json
P = '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read(); n0 = len(s)

def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def hx(t): return '#%02x%02x%02x' % tuple(max(0, min(255, round(v))) for v in t)
def mix(a, b, t): A, B = rgb(a), rgb(b); return hx(tuple(A[i] + (B[i] - A[i]) * t for i in range(3)))
def trip(h): return '%d,%d,%d' % rgb(h)

OK, WARN, BAD, NA = '#5fbf7f', '#e2b04a', '#e06464', '#7d87a8'
def dark(d):
    """derive the secondary tokens of a dark skin from its base colours"""
    bg, pn, p2, ln, l2, fg, mu, dm, ac, tn = (d[k] for k in ('bg', 'panel', 'panel2', 'line', 'line2', 'fg', 'muted', 'dim', 'brass', 'tint'))
    o = dict(d); o.pop('tint')
    o.update({
     'hi-a': mix(bg, tn, .20), 'hi-b': mix(bg, tn, .13), 'hi-c': mix(bg, tn, .27), 'hi-d': mix(bg, tn, .12), 'press': mix(bg, tn, .30), 'me-bg': mix(bg, ac, .18),
     'cell': mix(p2, l2, .35), 'cell2': mix(p2, ln, .5), 'hatch-a': mix(pn, p2, .8), 'hatch-b': mix(p2, ln, .7), 'hatch-c': l2,
     'chip': mix(p2, ln, .4), 'rowline': mix(p2, ln, .25), 'cardin': mix(pn, p2, .7),
     'pill-bg': mix(bg, ac, .20), 'pill-line': mix(bg, ac, .48), 'pill-tx': mix(ac, '#ffffff', .25),
     'mute2': mix(mu, dm, .5), 'mute3': mix(mu, dm, .2), 'fg2': mix(fg, mu, .4), 'fg3': mix(fg, mu, .7),
     'tint-ok': mix(bg, OK, .22), 'tint-bad': mix(bg, BAD, .24), 'tint-na': mix(bg, NA, .26), 'tint-warn': mix(bg, WARN, .20),
     'tint-live': mix(bg, BAD, .16), 'line-ok': mix(bg, OK, .35), 'tint-ok2': mix(bg, OK, .12), 'tint-warn2': mix(bg, WARN, .14),
     'quay3': mix(d['quay'], p2, .5), 'tick': mix(l2, mu, .3), 'tick2': mix(dm, mu, .3), 'wave': mix(d['water'], ac, .18),
     'dim2': mix(l2, dm, .35), 'dim3': mix(l2, dm, .6),
     'band-c': bg, 'link': mix(ac, '#ffffff', .2), 'acc-rgb': trip(ac), 'gold-rgb': trip(d['gold']),
    })
    return o

SKINS = [
 # id, name, one-line description, tokens
 ('navy', 'Navy & Brass', 'Deep navy, brass fittings', dark({
   'bg': '#0a1220', 'panel': '#101b2e', 'panel2': '#16243b', 'line': '#22334d', 'line2': '#31476b', 'fg': '#f1eadb', 'muted': '#a6aebc', 'dim': '#6c7b92',
   'brass': '#dcb96a', 'brass2': '#a98a45', 'water': '#0c1626', 'quay': '#223049', 'quay2': '#2d3f5d',
   'band-a': '#1b3358', 'band-b': '#0e1c33', 'gold': '#dcb96a', 'gold2': '#f0d79a', 'tint': '#2a5fc0'})),
 ('timber', 'Timber Yard', 'Bark brown, lichen green', dark({
   'bg': '#14100c', 'panel': '#1c1611', 'panel2': '#261e17', 'line': '#3a2d21', 'line2': '#4f3d2d', 'fg': '#f3eadc', 'muted': '#b6a692', 'dim': '#7e6d5b',
   'brass': '#c3d67c', 'brass2': '#8fa052', 'water': '#110e0b', 'quay': '#342a20', 'quay2': '#43362a',
   'band-a': '#3c2b1a', 'band-b': '#1f1711', 'gold': '#dba862', 'gold2': '#f0cf95', 'tint': '#b0702a'})),
 ('creek', 'Creek Tide', 'Sea green, foam', dark({
   'bg': '#08171a', 'panel': '#0e2024', 'panel2': '#142b30', 'line': '#1f3c42', 'line2': '#2d525a', 'fg': '#e6f2f0', 'muted': '#95b1b1', 'dim': '#5f7e80',
   'brass': '#86ecd9', 'brass2': '#46a999', 'water': '#0a1c20', 'quay': '#20393e', 'quay2': '#2a484e',
   'band-a': '#123a41', 'band-b': '#0c2429', 'gold': '#e0cf9f', 'gold2': '#f2e6c0', 'tint': '#1fa59a'})),
 ('dusk', 'Dusk', 'Aubergine, rose', dark({
   'bg': '#16101c', 'panel': '#1e1626', 'panel2': '#281d32', 'line': '#3b2c48', 'line2': '#503c60', 'fg': '#f3e9f0', 'muted': '#b4a4b9', 'dim': '#7c6b83',
   'brass': '#f4a9c0', 'brass2': '#b9728a', 'water': '#140e19', 'quay': '#342740', 'quay2': '#423250',
   'band-a': '#3c2452', 'band-b': '#22172d', 'gold': '#e8bc8c', 'gold2': '#f6d8b8', 'tint': '#9a4fd0'})),
 ('salt', 'Salt Pan', 'Daylight · light', {
   'bg': '#edf1f4', 'panel': '#ffffff', 'panel2': '#f3f6f8', 'line': '#d4dce3', 'line2': '#b7c4ce', 'fg': '#14202e', 'muted': '#4f6078', 'dim': '#8292a2',
   'brass': '#0b6fa4', 'brass2': '#5aa3cc', 'water': '#dde9f0', 'quay': '#c3cdd5', 'quay2': '#b2bec8',
   'dry': '#b8771f', 'brk': '#23917f', 'prj': '#c9523b', 'box': '#3f6fd0', 'ppp': '#6c7686', 'ok': '#2b9454', 'warn': '#b47a0c', 'bad': '#cc4040',
   'band-a': '#17304f', 'band-b': '#10213a', 'band-c': '#0c1a2e', 'gold': '#a5781a', 'gold2': '#8a6212',
   'hi-a': '#e2eef7', 'hi-b': '#f0f6fa', 'hi-c': '#d9e9f5', 'hi-d': '#e9f2f8', 'press': '#d5e6f3', 'me-bg': '#d2e8f6',
   'amber': '#e0a23a', 'amber-tx': '#8a5a06', 'amber-line': '#d9a441', 'amber-ink': '#17100a',
   'pill-line': '#7fb1d6', 'pill-bg': '#dcebf6', 'pill-tx': '#125e97',
   'tx-info': '#1466a8', 'tx-exp': '#3a63c8', 'tx-ok': '#1e7b43', 'tx-warn': '#9a5a06', 'tx-bad': '#c0392b', 'tx-bad2': '#b8442e',
   'tx-out': '#b3562a', 'tx-live': '#c0392b', 'tx-miss': '#c2485a', 'bad2': '#d04450', 'bad3': '#e04a3a', 'mnt-tx': '#946410',
   'tint-ok': '#dff3e6', 'tint-bad': '#f9dfdc', 'tint-na': '#e6e9f0', 'tint-warn': '#f6ecd2', 'tint-live': '#fbe3df',
   'line-ok': '#a9d8b8', 'tint-ok2': '#eaf7ee', 'tint-warn2': '#f8efd6',
   'mute2': '#6c7c8d', 'mute3': '#5d6e80', 'fg2': '#2c3b4d', 'fg3': '#3a4a5c',
   'cell': '#dde4ea', 'cell2': '#dde4ea', 'hatch-a': '#e9eef2', 'hatch-b': '#d2dae1', 'hatch-c': '#c0cad3',
   'chip': '#edf1f5', 'rowline': '#e2e7ec', 'cardin': '#f6f8fa',
   'tab-salt': '#5d6f85', 'tab-ppp': '#8a4fd6', 'tab-pri': '#a5781a', 'tab-barge': '#1f9c90', 'tmb': '#5f8a1f',
   'ink': '#0b1420', 'ink2': '#0e141b', 'quay3': '#cfd6dd', 'tick': '#9aa7b4', 'tick2': '#7f8c9a', 'wave': '#b7d1e2',
   'mnt-a': '#ead7b8', 'mnt-b': '#d4b07a', 'dim2': '#a7b2bd', 'dim3': '#98a4b0',
   'link': '#0b6fa4', 'sel': '#10203a', 'on-acc': '#ffffff', 'hatch-ov': 'rgba(255,255,255,.5)', 'acc-rgb': '11,111,164', 'gold-rgb': '165,120,26', 'ov-rgb': '16,28,48'}),
]
# the default look, for the chooser tile only
DEF = ('', 'Kandla Night', 'Slate, signal blue', {'bg': '#0f1419', 'panel': '#161d24', 'line2': '#334454', 'fg': '#e8eef4', 'brass': '#5cc8ff', 'band-a': '#17293d', 'gold': '#c9a24c'})

# two more tokens (defaults = the old fixed values): text on an accent fill, and the hatch drawn over an estimated bar
a = 'color-scheme:dark;'
assert s.count(a) >= 1
s = s.replace(a, 'color-scheme:dark; --on-acc:#0b1420; --hatch-ov:rgba(9,19,31,.6);', 1)
for old, new in [
  ("'font-size':9.5,fill:'var(--ink)'},svg,fmt(T));", "'font-size':9.5,fill:'var(--on-acc)'},svg,fmt(T));"),
  ("const tc=v.proj?'var(--fg)':'var(--ink)';", "const tc=v.proj?'var(--fg)':(me?'var(--on-acc)':'var(--ink)');"),
  ("fill:v.proj?(me?'var(--brass)':'var(--fg)'):'var(--ink)'},g,fit(v.n,w-8,6.1));", "fill:v.proj?(me?'var(--brass)':'var(--fg)'):(me?'var(--on-acc)':'var(--ink)')},g,fit(v.n,w-8,6.1));"),
  ("el('rect',{width:1.6,height:5,fill:'rgba(9,19,31,.6)'},pat);", "el('rect',{width:1.6,height:5,fill:'var(--hatch-ov)'},pat);"),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)

css = ["\n/* v265 colour themes — each block only redefines tokens; the default (no data-skin) is Kandla Night */"]
for sid, name, sub, t in SKINS:
    body = ";".join("--%s:%s" % (k, v) for k, v in t.items())
    css.append(":root[data-skin=\"%s\"]{color-scheme:%s;%s}" % (sid, 'light' if sid == 'salt' else 'dark', body))
# Salt Pan keeps a dark masthead: the dark token set is scoped to the header band
css.append(":root[data-skin=\"salt\"] header.top.band{--bg:#0c1a2e;--panel:#152742;--panel2:#1b3050;--line:#2a3b55;--line2:#3a4f6d;--fg:#eef3f8;--muted:#a9b9cb;--dim:#7b8ca0;"
           "--brass:#7cc8ff;--brass2:#4a9bd0;--link:#9fd4ff;--mute2:#7d8c9b;--gold:#dcb96a;--gold2:#f0d79a;--acc-rgb:124,200,255;--gold-rgb:201,162,76;--ov-rgb:255,255,255;border-color:#10213a}")
# chooser
css.append("""
.skbtn{display:inline-flex;align-items:center;gap:7px;font-family:var(--f-mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg);background:rgba(var(--ov-rgb),.05);border:1px solid var(--line2);border-radius:999px;padding:5px 12px 5px 8px;cursor:pointer;-webkit-tap-highlight-color:transparent;position:relative;z-index:2}
.skbtn:hover{border-color:var(--brass)}
.skbtn i{width:15px;height:15px;border-radius:50%;flex:none;background:conic-gradient(var(--brass) 0 33%,var(--gold) 0 66%,var(--panel2) 0);border:1.5px solid var(--fg)}
.skpop{position:fixed;z-index:60;width:min(430px,calc(100vw - 24px));background:var(--panel);border:1px solid var(--line2);border-radius:14px;padding:14px;box-shadow:0 18px 50px rgba(0,0,0,.45)}
.skpop[hidden]{display:none}
.skpop h3{font-family:var(--f-disp);font-weight:800;font-size:22px;line-height:1;text-transform:uppercase;letter-spacing:.02em;color:var(--fg);margin:0 0 3px}
.skpop p{font-size:12.5px;color:var(--muted);margin:0 0 11px}
.skdone{float:right;font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--fg);background:none;border:1px solid var(--line2);border-radius:999px;padding:5px 12px;margin:-2px 0 0 10px;cursor:pointer}
.skdone:hover{border-color:var(--brass)}
.skgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}
.sktile{display:block;text-align:left;font:inherit;color:var(--fg);background:none;border:1.5px solid var(--line);border-radius:10px;padding:5px 5px 7px;cursor:pointer;-webkit-tap-highlight-color:transparent}
.sktile:hover{border-color:var(--line2)}
.sktile[aria-pressed="true"]{border-color:var(--brass);box-shadow:0 0 0 2px rgba(var(--acc-rgb),.28)}
.sktile .sw{display:block;height:58px;border-radius:6px;position:relative;overflow:hidden;background:var(--t-bg);border:1px solid rgba(128,128,128,.35)}
.sktile .sw::before{content:"";position:absolute;left:0;right:0;top:0;height:19px;background:var(--t-band);border-bottom:2px solid var(--t-gold)}
.sktile .sw::after{content:"";position:absolute;left:7px;right:7px;top:27px;bottom:7px;border-radius:4px;background:var(--t-panel);border:1px solid var(--t-line);border-top:3px solid var(--t-acc)}
.sktile .sw b{position:absolute;left:13px;bottom:13px;z-index:1;height:4px;width:44%;border-radius:2px;background:var(--t-fg);opacity:.9}
.sktile .nm{display:flex;align-items:center;gap:5px;font-family:var(--f-body);font-weight:700;font-size:13px;line-height:1.15;margin:7px 2px 1px}
.sktile .nm::after{content:"";width:8px;height:8px;border-radius:50%;margin-left:auto;flex:none;border:1.5px solid var(--line2)}
.sktile[aria-pressed="true"] .nm::after{background:var(--brass);border-color:var(--brass)}
.sktile small{display:block;font-size:11.5px;line-height:1.25;color:var(--muted);margin:0 2px}
@media (max-width:640px){.skpop{left:12px!important;right:12px;top:auto!important;bottom:12px;width:auto}.skgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.skbtn{padding:5px 10px 5px 7px}}
""")
end = s.index('</style>')
s = s[:end] + "\n".join(css) + s[end:]

# markup: the button sits in the owner row of the header
a = '<span class="vcount" id="viewcount" style="display:none"></span></div>'
assert s.count(a) == 1
s = s.replace(a, '<span class="vcount" id="viewcount" style="display:none"></span><button type="button" class="skbtn" id="skbtn" aria-haspopup="dialog" aria-expanded="false" aria-controls="skpop"><i aria-hidden="true"></i>Theme</button></div>')

# early: apply the saved skin before first paint
h = s.index('<style>')   # the page is a fragment (no head / body tags): the early script goes just before the stylesheet
s = s[:h] + "<script>try{var k=localStorage.getItem('dpaSkin');if(k)document.documentElement.setAttribute('data-skin',k);}catch(e){}</script>\n" + s[h:]

tiles = [DEF] + SKINS
TJS = json.dumps([{'id': sid, 'n': name, 's': sub, 'bg': t['bg'], 'pn': t['panel'], 'ln': t['line2'], 'fg': t['fg'], 'ac': t['brass'],
                   'bd': t['band-a'], 'gd': '#dcb96a' if sid == 'salt' else t['gold']} for sid, name, sub, t in tiles], ensure_ascii=False)
script = """
<div class="skpop" id="skpop" role="dialog" aria-label="Colour theme" hidden></div>
<script>
/* v265 colour themes — the chooser. A skin only sets html[data-skin]; the choice stays on this device (localStorage 'dpaSkin'). */
(function(){
  var SK=%s, root=document.documentElement, btn=document.getElementById('skbtn'), pop=document.getElementById('skpop');
  if(!btn||!pop)return;
  function cur(){return root.getAttribute('data-skin')||'';}
  function set(id){ if(id)root.setAttribute('data-skin',id); else root.removeAttribute('data-skin');
    try{ if(id)localStorage.setItem('dpaSkin',id); else localStorage.removeItem('dpaSkin'); }catch(e){}
    pop.querySelectorAll('.sktile').forEach(function(t){ t.setAttribute('aria-pressed',String(t.getAttribute('data-skin-id')===id)); }); }
  function draw(){ var c=cur();
    pop.innerHTML='<button type="button" class="skdone" id="skdone">Done</button><h3>Colour theme</h3><p>Pick one — it stays on this phone or computer.</p><div class="skgrid">'+SK.map(function(k){
      return '<button type="button" class="sktile" data-skin-id="'+k.id+'" aria-pressed="'+(k.id===c)+'" style="--t-bg:'+k.bg+';--t-panel:'+k.pn+';--t-line:'+k.ln+';--t-fg:'+k.fg+';--t-acc:'+k.ac+';--t-band:'+k.bd+';--t-gold:'+k.gd+'"><span class="sw"><b></b></span><span class="nm">'+k.n+'</span><small>'+k.s+'</small></button>';
    }).join('')+'</div>'; }
  function place(){ var r=btn.getBoundingClientRect(), w=pop.offsetWidth||430, x=Math.max(12,Math.min(window.innerWidth-w-12,r.left));
    pop.style.left=x+'px'; pop.style.top=Math.min(window.innerHeight-pop.offsetHeight-12,r.bottom+8)+'px'; }
  function open(){ draw(); pop.hidden=false; place(); btn.setAttribute('aria-expanded','true'); var on=pop.querySelector('[aria-pressed="true"]'); if(on)on.focus({preventScroll:true}); }
  function close(){ if(pop.hidden)return; pop.hidden=true; btn.setAttribute('aria-expanded','false'); }
  btn.addEventListener('click',function(e){ e.stopPropagation(); if(pop.hidden)open(); else close(); });
  pop.addEventListener('click',function(e){ e.stopPropagation(); if(e.target.closest('.skdone')){close();btn.focus();return;} var t=e.target.closest('.sktile'); if(t)set(t.getAttribute('data-skin-id')||''); });
  document.addEventListener('click',function(e){ if(!pop.hidden&&!pop.contains(e.target)&&e.target!==btn)close(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!pop.hidden){close();btn.focus();} });
  window.addEventListener('resize',function(){ if(!pop.hidden)place(); });
  window.addEventListener('scroll',function(){ if(window.innerWidth>640)close(); },{passive:true});
  if(cur()&&!SK.some(function(k){return k.id===cur();}))set('');
}());
</script>
""" % TJS
# the chooser goes BEFORE the board's own script: tools/build_db.js takes the last '})();' of the file as the end of the board's code
b = s.index('<script>\n(function(){\nconst BASE=')
s = s[:b] + script.lstrip('\n') + s[b:]
a = "UPDATED='23 Nov 2026 · 14:22 IST'"
assert s.count(a) == 1
s = s.replace(a, "UPDATED='23 Nov 2026 · 15:56 IST'")   # display-only version; NOW and every paper stay as in v264
open(P, 'w', encoding='utf-8').write(s); print('saved', n0, '->', len(s))
