#!/usr/bin/env python3
"""Build the stand-alone Tuna and Liquid boards from the main DPA Berth Board HTML.

Usage: build_pages.py <main board html> <output dir>
Writes <out>/tuna.html and <out>/liquid.html. Everything (style, data, render code) is copied
from the main board so the three pages never drift: the data lives between /*@@TLDATA@@*/ and
/*@@/TLDATA@@*/, the render functions between /*@@TLCODE@@*/ and /*@@/TLCODE@@*/.
"""
import re, sys, os, html

src_path, out_dir = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()

def between(a, b, text=s):
    i = text.index(a); j = text.index(b, i)
    return text[i:j + len(b)]

style = between('<style>', '</style>')
links = '\n'.join(re.findall(r'<link rel="[^"]*"[^>]*>', s)[:3])
tldata = between('/*@@TLDATA@@*/', '/*@@/TLDATA@@*/')
tlcode = between('/*@@TLCODE@@*/', '/*@@/TLCODE@@*/')
updated = re.search(r"const UPDATED='([^']*)'", s).group(1)
now_s = re.search(r"const NOW=h\('([^']*)'\)", s).group(1)
page_urls = re.search(r"const PAGE_URLS=\{[^}]*\}", s).group(0)
main_url = 'https://claude.ai/artifact/AWVRBbjBx4EJGBctgGPRS3'
helpers = '\n'.join([
    re.search(r"^const BASE=.*$", s, re.M).group(0),
    re.search(r"^function h\(s\).*$", s, re.M).group(0),
    re.search(r"^const MON=.*$", s, re.M).group(0),
    re.search(r"^function dt\(x\).*$", s, re.M).group(0),
    re.search(r"^function fmt\(x.*$", s, re.M).group(0),
    re.search(r"^function fday\(x\).*$", s, re.M).group(0),
    re.search(r"^const nf=.*$", s, re.M).group(0),
    re.search(r"^const NS=.*$", s, re.M).group(0),
    re.search(r"^function el\(tag.*$", s, re.M).group(0),
    re.search(r"^function fit\(s.*$", s, re.M).group(0),
    re.search(r"^const FB=.*$", s, re.M).group(0),
])

extra_css = """
.sechead{cursor:default}
.back{font-family:var(--f-mono);font-size:11.5px;color:var(--brass);text-decoration:none;border:1px solid var(--brass2);border-radius:20px;padding:4px 12px;display:inline-block}
.back:hover{color:var(--fg)}
.note{font-size:12.5px;color:var(--muted);border-left:3px solid var(--brass2);padding:4px 0 4px 12px}
"""

def page(kind):
    if kind == 'tuna':
        title = 'Tuna Board'; eyebrow = 'Deendayal Port · Kandla · Tuna Tekra terminal (Adani PPP)'
        aria = 'Tuna terminal berths'
        section = """
  <section class="card" data-sec="tuna" aria-labelledby="tth">
    <div class="sechead"><h2 id="tth">Tuna · TT-1 to TT-4</h2><p id="ttsub"></p></div>
    <div class="scroll"><svg class="tmap" id="tmap" role="img" aria-label="Tuna terminal berths"></svg></div>
    <div class="scroll"><table class="mpt lqt" id="tuna"></table></div>
  </section>
  <section class="card"><div class="sechead"><h2>How to read this page</h2></div>
    <div class="note">Tuna Tekra is a PPP terminal run by Adani inside Deendayal Port. Its berths are <b>not</b> in the DPA berthing-policy queue, so the board makes no projection here — the order of berthing is whatever the list's remarks say ("TT-03 followed by …"). The DPA list prints no discharge norm or ETC for TT vessels; "days alongside" is counted from the list's MADE FAST time. TT movements do not appear on the Harbour Master's cargo-jetty signals, so a berthing taken from a B'TODAY remark stays marked as not confirmed until a list prints it.</div>
  </section>"""
        tiles_js = """
  const occ=TUNA.berths.length, est=TUNA.berths.filter(b=>b.est).length;
  const days=TUNA.berths.map(b=>Math.round((NOW-h(b.f))/24*10)/10);
  const tiles=[
   ['var(--brk)',occ+'<small>/4</small>','<b>Tuna berths occupied</b>'+(est?' · '+est+' berthing not yet confirmed':''),TUNA.berths.map(b=>`<span class="cc" style="--sc:var(--brk)"><b>${b.b}</b><span>${b.n}<small> · ${b.c}</small></span></span>`).join('')],
   ['var(--brass)',TUNA.wait.length,'<b>Waiting for a Tuna berth</b> · reported, not yet berthed',TUNA.wait.map(w=>`<span class="cc" style="--sc:var(--brass)"><b>${w.n}</b><span>${w.c}<small> · ${w.rem||''}</small></span></span>`).join('')],
   ['var(--box)',TUNA.eta.length,'<b>Expected</b> · ETA given, not yet reported',TUNA.eta.slice().sort((a,b)=>h(a.eta)-h(b.eta)).map(w=>`<span class="cc" style="--sc:var(--box)"><b>${fday(h(w.eta)).slice(4)}</b><span>${w.n}<small> · ${w.c}</small></span></span>`).join('')],
   ['var(--line2)',Math.max(...days)+'<small> d</small>','<b>Longest stay alongside</b> · '+TUNA.berths[days.indexOf(Math.max(...days))].n+' at '+TUNA.berths[days.indexOf(Math.max(...days))].b,'']
  ];"""
        render_call = 'tuna();'
    else:
        title = 'Liquid Board'; eyebrow = 'Deendayal Port · Kandla · Oil jetties OJ-1 to OJ-7'
        aria = 'Oil jetties'
        section = """
  <section class="card" data-sec="liquid" aria-labelledby="lqh">
    <div class="sechead"><h2 id="lqh">Liquid berths · OJ-1 to OJ-7</h2><p id="lqsub"></p></div>
    <div class="scroll"><svg class="tmap" id="lmap" role="img" aria-label="Oil jetties"></svg></div>
    <div class="scroll"><table class="mpt lqt" id="liquid"></table></div>
    <div class="striplabel" style="margin-top:6px">Waiting liquid vessels · queue letters as printed in the list (E = edible oils, C = chemicals, O = POL)</div>
    <div class="scroll"><table class="mpt lqt" id="liqwait"></table></div>
    <div class="striplabel" style="margin-top:6px">Expected liquid vessels (ETA sheet)</div>
    <div class="scroll"><table class="mpt lqt" id="liqeta"></table></div>
    <div class="striplabel" style="margin-top:6px">Oil-jetty movements · HM signals</div>
    <div id="liqmoves"></div>
  </section>
  <section class="card"><div class="sechead"><h2>How to read this page</h2></div>
    <div class="note">The board has no berthing rules for liquid cargo, so nothing here is projected: occupancy is the DPA list plus the Harbour Master's signals, and the queue is shown exactly as the list prints it — the letter after the rank is the list's own category (<b>E</b> edible oils such as CDSBO / CPO, <b>C</b> chemicals, <b>O</b> POL such as HSD / MS / VLSFO); "REQ OJ 2, 3, 4" is the agent's berth requirement from the list remarks. IFFCO's ammonia and phosphoric-acid vessels appear under OJ in the list. "Made fast" times derived from an "o/c" (on completion) signal are estimates until a list prints them. The jetty map is a schematic row in OJ order, not the geographic layout.</div>
  </section>"""
        tiles_js = """
  const occ=LIQ.berths.filter(b=>b.now).length, vac=LIQ.berths.filter(b=>!b.now).map(b=>b.b);
  const W=LIQ.wait.filter(w=>!/at OJ|berthed/.test(w.st||''));
  const grp=r=>/E$/.test(r.rank||'')?'E':/C$/.test(r.rank||'')?'C':/O$/.test(r.rank||'')?'O':'Z';
  const cnt=k=>W.filter(w=>grp(w)===k).length;
  const mv=LIQ.berths.filter(b=>b.out&&h(b.out)>NOW), inn=LIQ.berths.filter(b=>b.next);
  const tiles=[
   ['var(--dry)',occ+'<small>/'+LIQ.berths.length+'</small>','<b>Oil jetties occupied</b>'+(vac.length?' · vacant: '+vac.join(', '):''),LIQ.berths.map(b=>`<span class="cc" style="--sc:${b.now?'var(--dry)':'var(--line2)'}"><b>${b.b}</b><span>${b.now?b.now.n+'<small> · '+b.now.c+'</small>':'<small>vacant</small>'}</span></span>`).join('')],
   ['var(--brass)',W.length,'<b>Waiting</b> · reported, not yet berthed · by the list\\'s queue letter',[['E','Edible oils'],['C','Chemicals'],['O','POL'],['Z','no letter']].filter(([k])=>cnt(k)).map(([k,l])=>`<span class="cc" style="--sc:var(--brass)"><b>${cnt(k)}</b><span>${l}<small> (${k})</small></span></span>`).join('')],
   ['var(--box)',LIQ.eta.length,'<b>Expected</b> · ETA given, not yet reported',(()=>{const d={};LIQ.eta.forEach(e=>{const k=fday(h(e.eta)).slice(4);d[k]=(d[k]||0)+1;});return Object.entries(d).map(([k,n])=>`<span class="cc" style="--sc:var(--box)"><b>${n}</b><span>${k}</span></span>`).join('');})()],
   ['var(--warn)',mv.length,'<b>Sailings signalled</b> after '+fmt(NOW)+' · '+inn.length+' berthings to follow',mv.map(b=>`<span class="cc" style="--sc:var(--warn)"><b>${fmt(h(b.out),false)}</b><span>${b.now?b.now.n:''} out of ${b.b}${b.next?'<small> → '+b.next.n+'</small>':''}</span></span>`).join('')]
  ];"""
        render_call = 'liquid();'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DPA {title}</title>
{links}
{style}
<style>{extra_css}</style>
</head><body>
<div class="wrap">
  <header class="top">
    <div>
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title.split()[0]} <span>Board</span><span class="draft" id="chip"></span></h1>
    </div>
    <div class="asof"><span class="upd" id="upd"></span><br><span id="srcline"></span><br><a class="back" id="back" href="#">← Main berth board (dry cargo)</a></div>
  </header>
  <div class="stats" id="stats"></div>
{section}
  <footer><span id="updf"></span> · status only — no berthing projection for these berths · generated from the main DPA Berth Board</footer>
</div>
<script>
(function(){{
{helpers}
const NOW=h('{now_s}');
const UPDATED='{updated}';
{page_urls}
const MAIN_URL='{main_url}';
const pageHref=k=>/github\\.io$/.test(location.hostname)?k+'.html':(PAGE_URLS[k]||'#'+k);
{tldata}
{tlcode}
document.getElementById('upd').innerHTML='<span style="letter-spacing:.1em">LAST UPDATED</span> <b>'+UPDATED+'</b>';
document.getElementById('updf').textContent='Updated '+UPDATED;
document.getElementById('chip').textContent=fday(NOW).slice(4).toUpperCase()+' 2026';
document.getElementById('srcline').innerHTML='Source: '+({'{'}tuna:TUNA.src,liquid:LIQ.src{'}'})['{kind}'];
document.getElementById('back').href=/github\\.io$/.test(location.hostname)?'index.html':MAIN_URL;
{tiles_js}
document.getElementById('stats').innerHTML=tiles.map(([c,v,l,ch])=>`<div class="stat" style="--sc:${{c}}"><div class="v">${{v}}</div><div class="l">${{l}}</div>${{ch?`<div class="comm">${{ch}}</div>`:''}}</div>`).join('');
{render_call}
}})();
</script>
</body></html>
"""

os.makedirs(out_dir, exist_ok=True)
for kind in ('tuna', 'liquid'):
    out = os.path.join(out_dir, kind + '.html')
    open(out, 'w', encoding='utf-8').write(page(kind))
    print('wrote', out)
