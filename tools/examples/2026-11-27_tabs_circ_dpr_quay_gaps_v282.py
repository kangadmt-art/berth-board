#!/usr/bin/env python3
# apply78 — v282. Mihir, 27 Nov 14:34: (1) circulars in a top tab like Salt / Timber; (2) the berthing detail the Priority tab already gives is not needed
# lower down in the dry-cargo tab; (3) DPR in a tab of its own, out of the cargo tab; (4) Quay by panel number: the free panels between vessels and the free
# space must be easy to see.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'); s = B.s
def cut(start, end):
    global s
    assert s.count(start) == 1, start
    a = s.index(start); b = s.index(end, a) + len(end); blk = s[a:b]; s = s[:a] + s[b:]; return blk
# ---- (2) berthing-detail sections out of the cargo tab → bottom of the Priority tab
mpt = cut('  <section class="card" data-sec="mpt"', '  </section>\n')
hpb = cut('  <section class="card" data-sec="hpb"', '  </section>\n')
spt = cut('  <section class="card" data-sec="spt"', '  </section>\n')
grp = cut('    <section class="card" data-sec="groups">', '    </section>\n')
a = s.index('  <div class="two">\n    <section class="card" data-sec="moves">'); b = s.index('  </div>\n', a)
s = s[:a] + s[a:b].replace('  <div class="two">\n', '').replace('    <section', '  <section').replace('    </section>', '  </section>').replace('      <div', '    <div') + s[b + len('  </div>\n'):]
# ---- (3) DPR and (1) circulars + news out of the cargo tab
dpr = cut('  <section class="card" data-sec="dpr"', '  </section>\n').replace(' data-sec="dpr"', '')
ntc = cut('    <section class="card" data-sec="notices"', '  </section>\n').replace(' data-sec="notices"', '').replace('    <section', '  <section')
nws = cut('  <section class="card" data-sec="news"', '  </section>\n').replace(' data-sec="news"', '')
anchor = '  <div id="pqtab"></div></div>\n'
assert s.count(anchor) == 1
s = s.replace(anchor, '  <div id="pqtab"></div>\n  <p class="morenote">Aur detail · the same berthing picture in other cuts — tap a heading to open it.</p>\n' + mpt + spt + grp.replace('    <section', '  <section').replace('    </section>', '  </section>').replace('      <div', '    <div') + hpb + '  </div>\n'
    + '  <div class="view" data-view="dpr" id="view-dpr">\n' + dpr + '  </div>\n'
    + '  <div class="view" data-view="circ" id="view-circ">\n' + ntc + nws + '  </div>\n')
# ---- nav, names, colours
nav = '    <a href="#salt" data-view="salt">'
a = s.index(nav); b = s.index('\n', a) + 1
s = s[:b] + ('    <a href="#dpr" data-view="dpr"><b>DPR</b><small>Cargo progress · last 24 hours · balance and pace, vessel by vessel</small><span class="vb" id="vb-dpr"></span></a>\n'
             '    <a href="#circ" data-view="circ"><b>Circulars</b><small>DPA circulars &amp; trade notices · number · date · what it means · PDF</small><span class="vb" id="vb-circ"></span></a>\n') + s[b:]
s = s.replace("const VIEWS={cargo:'Deendayal Port · Kandla · Dry cargo jetty',", "const VIEWS={dpr:'Deendayal Port · Kandla · Daily performance report',circ:'Deendayal Port · Kandla · Circulars and trade notices',cargo:'Deendayal Port · Kandla · Dry cargo jetty',", 1)
s = s.replace("const VIEW_NAME={ppp:'CJ-9 · CJ-10',", "const VIEW_NAME={dpr:'DPR',circ:'Circulars',ppp:'CJ-9 · CJ-10',", 1)
css = '.views a[data-view="sawal"]{--sc:var(--warn)}'
assert s.count(css) == 1
s = s.replace(css, '.views a[data-view="dpr"]{--sc:var(--dry)}.views a[data-view="circ"]{--sc:var(--brass)}.morenote{color:var(--muted);font-size:12.5px;margin:14px 2px 6px}\n'
    '.qgw{margin:6px 0 12px}.qgh{font-size:12.5px;margin:10px 0 4px;color:var(--muted)}.qgh b{color:var(--fg)}.qgh .tot{color:var(--ok);font-weight:700}\n'
    '.qg{display:flex;flex-wrap:wrap;gap:6px;align-items:stretch}.qg>div{border:1px solid var(--line);border-radius:8px;padding:6px 9px;font-size:12px;line-height:1.35;background:var(--panel2);min-width:96px}\n'
    '.qg>div b{display:block;font-weight:700}.qg small{display:block;color:var(--muted);font-size:11px}.qg .g{border:1.5px dashed var(--ok);background:transparent}.qg .g b{color:var(--ok)}.qg .g.sm{border-color:var(--line2)}.qg .g.sm b{color:var(--muted)}\n' + css, 1)
# ---- (4) free space between vessels, drawn right under the time slider
leg = '    <div class="legend" id="legend"></div>\n'
assert s.count(leg) == 1
s = s.replace(leg, '    <div class="qgw" id="qgaps"></div>\n' + leg, 1)
fn = r'''function quayGaps(){
  const el=document.getElementById('qgaps'); if(!el)return;
  const pn=x=>{const r=Math.round(x*4)/4;return frac(r);};
  const block=seg=>{
    const present=runFleet(seg).filter(v=>v.p&&v.F<=T&&T<v.T).sort((a,z)=>a.p[0]-z.p[0]);
    const R=quayRuns(T,seg); const items=[]; let cur=seg.from, free=0, freeM=0, n=0, best=null;
    const gap=(a,z)=>{ if(z-a<0.01)return; const m=gapM(a,z); const r=R.find(x=>Math.abs(x.a-a)<0.01&&Math.abs(x.z-z)<0.01); free+=z-a; freeM+=m; n++; if(!best||m>best.m)best={a,z,m};
      items.push(`<div class="g${m<RUN_MIN_M?' sm':''}"><b>KHALI · ${pn(z-a)} panel${z-a===1?'':'s'}</b>${pr([a,z])} · ~${Math.round(m)} m<small>${r&&r.maxLoa>=70?'vessel up to ~'+r.maxLoa+' m fits':m<RUN_MIN_M?'too short for a vessel':'short'}</small></div>`); };
    for(const v of present){ gap(cur,v.p[0]); items.push(`<div><b>${v.n.replace(/\s*\(.*\)\s*$/,'')}</b>${pr(v.p)}<small>CJ-${v.b}${LOA[v.n]?' · '+Math.round(LOA[v.n])+' m':''}</small></div>`); cur=Math.max(cur,v.p[1]); }
    gap(cur,seg.to);
    return `<div class="qgh"><b>${seg.label}</b> · panels ${seg.from}–${seg.to} · <span class="tot">khali ${pn(free)} panels · ~${Math.round(freeM)} m</span> in ${n} place${n===1?'':'s'}${best?' · longest ~'+Math.round(best.m)+' m ('+pr([best.a,best.z])+')':''}</div><div class="qg">${items.join('')}</div>`; };
  el.innerHTML=`<div class="qgh"><b>Khali jagah · free space between vessels</b> at ${fmt(T)} — north to south. Solid box = a vessel with her panels; dashed green = empty quay. Vessels the board only projects (dotted hulls) are not counted.</div>`+SEGS.slice().reverse().map(block).join('');
}
'''
s = s.replace("function runs(){\n  const el=document.getElementById('runs'); if(!el)return;", fn + "function runs(){\n  const el=document.getElementById('runs'); if(!el)return;", 1)
assert "strip(document.getElementById('stripB'),110,189);runs();" in s
s = s.replace("strip(document.getElementById('stripB'),110,189);runs();", "strip(document.getElementById('stripB'),110,189);quayGaps();runs();", 1)
# ---- badges for the two new tabs
sm = "  setSum('notices',"
assert s.count(sm) == 1
s = s.replace(sm, "  {const vb=document.getElementById('vb-circ');if(vb){const L=NOTICES.slice().sort((a,z)=>(z.iso||'').localeCompare(a.iso||''))[0];vb.innerHTML=`<b>${NOTICES.length}</b> papers${L?' · latest '+L.rd:''}`;}\n"
    "   const vd=document.getElementById('vb-dpr');if(vd)vd.innerHTML=`<b>${DPR.d.slice(0,5)}</b> · ${Math.round(DPR.tot.all).toLocaleString('en-IN')} MT in 24 h`;}\n" + sm, 1)
B.s = s; B.save()
