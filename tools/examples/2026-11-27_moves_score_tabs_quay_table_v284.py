#!/usr/bin/env python3
# apply80 — v284. Mihir, 27 Nov 15:03: signal movements and accuracy in pages of their own · Quay by panel number: the free space in metres and the panel
# numbers of the berthed vessels must read clearly · CJ-9 / CJ-10 detail not needed here (it is on the CJ-9·10 page) · the 10-day view is not needed on
# the page — the projection itself goes on being worked out.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'); s = B.s
def cut(start, end):
    global s
    assert s.count(start) == 1, start
    a = s.index(start); b = s.index(end, a) + len(end); blk = s[a:b]; s = s[:a] + s[b:]; return blk
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
mv = cut('  <section class="card" data-sec="moves">', '  </section>\n').replace(' data-sec="moves"', '')
sc = cut('  <section class="card" data-sec="score" aria-labelledby="sch">', '  </section>\n').replace(' data-sec="score"', '')
rep('  <div class="view" data-view="priority" id="view-priority">\n', '  <div class="view" data-view="moves" id="view-moves">\n' + mv + '  </div>\n  <div class="view" data-view="score" id="view-score">\n' + sc + '  </div>\n  <div class="view" data-view="priority" id="view-priority">\n')
rep('    <a href="#barge" data-view="barge">', '    <a href="#moves" data-view="moves"><b>Movements</b><small>Harbour Master\'s signal sheets · in · out · shift · cargo berths</small><span class="vb" id="vb-moves"></span></a>\n    <a href="#barge" data-view="barge">')
rep('    <a href="#cj16" data-view="cj16">', '    <a href="#score" data-view="score"><b>Accuracy</b><small>Board\'s meeting call against the port\'s programme · day by day</small><span class="vb" id="vb-score"></span></a>\n    <a href="#cj16" data-view="cj16">')
rep("const VIEWS={mine:", "const VIEWS={moves:'Deendayal Port · Kandla · Signal movements',score:'Deendayal Port · Kandla · Accuracy of the board',mine:")
rep("const VIEW_NAME={mine:'Mihir & Co',", "const VIEW_NAME={moves:'Movements',score:'Accuracy',mine:'Mihir & Co',")
rep('.views a[data-view="mine"]{--sc:var(--brass)}', '.views a[data-view="moves"]{--sc:var(--dry)}.views a[data-view="score"]{--sc:var(--ok)}\n'
    '.qgt{width:100%;border-collapse:collapse;font-size:13px;margin:4px 0 14px}.qgt th{font-family:var(--f-mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);text-align:left;padding:6px 8px;border-bottom:1px solid var(--line2)}\n'
    '.qgt td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:middle}.qgt td.num,.qgt th.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}.qgt td.pn{white-space:nowrap;font-weight:700}\n'
    '.qgt tr.g td{background:rgba(95,191,127,.10);color:var(--ok);font-weight:700}.qgt tr.g.sm td{background:transparent;color:var(--muted);font-weight:400}.qgt tr.g td small{color:var(--muted);font-weight:400}.qgt td small{color:var(--muted)}\n'
    '.qgt tr.tot td{border-top:2px solid var(--line2);border-bottom:0;font-weight:700}.qgcap{font-family:var(--f-disp);font-size:17px;font-weight:800;text-transform:uppercase;letter-spacing:.02em;margin:10px 0 2px}\n'
    '@media (max-width:640px){.qgt{font-size:12px}.qgt td,.qgt th{padding:6px 5px}.qgt .hidem{display:none}}\n'
    '.views a[data-view="mine"]{--sc:var(--brass)}')
# quay: no time slider, no CJ-9 / 10 block (both kept in the page, hidden, because the drawing code reads them)
rep('    <div class="controls">', '    <div class="controls" hidden style="display:none">')
rep('    <div class="striplabel">Outside the DPA queue · CJ-9 (PPP) and CJ-10 (maintenance)</div>\n    <div class="side" id="side"></div>', '    <div hidden style="display:none"><div class="side" id="side"></div></div>')
rep('First the free space between vessels, then the quay drawn to scale. Move the slider to see another hour.', 'First a table — every vessel with her panel numbers, and every empty stretch with its length in metres — then the quay drawn to scale. Position as the board stands now. CJ-9 and CJ-10 have their own page.')
# the free-space strip becomes a plain table
a = s.index("function quayGaps(){"); b = s.index("function runs(){", a)
fn = r'''function quayGaps(){
  const el=document.getElementById('qgaps'); if(!el)return;
  const pn=x=>frac(Math.round(x*4)/4);
  const block=seg=>{
    const present=runFleet(seg).filter(v=>v.p&&v.F<=T&&T<v.T).sort((a,z)=>a.p[0]-z.p[0]);
    const R=quayRuns(T,seg); const rows=[]; let cur=seg.from, free=0, freeM=0, n=0, usedM=0;
    const gap=(a,z)=>{ if(z-a<0.01)return; const m=gapM(a,z); const r=R.find(x=>Math.abs(x.a-a)<0.01&&Math.abs(x.z-z)<0.01); free+=z-a; freeM+=m; n++;
      const fit=r&&r.maxLoa>=70?'a vessel up to ~'+r.maxLoa+' m can berth':'too short for a vessel';
      rows.push(`<tr class="g${m<RUN_MIN_M?' sm':''}"><td class="hidem">—</td><td>KHALI · empty<br><small>${fit}</small></td><td class="pn">${frac(a)} – ${frac(z)}</td><td class="num">${pn(z-a)}</td><td class="num">${Math.round(m)} m</td></tr>`); };
    for(const v of present){ gap(cur,v.p[0]); const m=gapM(v.p[0],v.p[1]); usedM+=m;
      rows.push(`<tr><td class="hidem">CJ-${v.b}</td><td><b>${v.n.replace(/\s*\(.*\)\s*$/,'')}</b><br><small><span class="showm">CJ-${v.b} · </span>${LOA[v.n]?'vessel length '+Math.round(LOA[v.n])+' m':''}</small></td><td class="pn">${frac(v.p[0])} – ${frac(v.p[1])}</td><td class="num">${pn(v.p[1]-v.p[0])}</td><td class="num">${Math.round(m)} m</td></tr>`); cur=Math.max(cur,v.p[1]); }
    gap(cur,seg.to);
    return `<div class="qgcap">${seg.label} · panels ${seg.from} to ${seg.to}</div><div class="scroll"><table class="qgt"><thead><tr><th class="hidem">Berth</th><th>Vessel / empty space</th><th>Panel no. · from – to</th><th class="num">Panels</th><th class="num">Length</th></tr></thead><tbody>${rows.join('')}
      <tr class="tot"><td class="hidem"></td><td>Total empty · ${n} place${n===1?'':'s'}</td><td></td><td class="num">${pn(free)}</td><td class="num">${Math.round(freeM)} m</td></tr></tbody></table></div>`; };
  el.innerHTML=`<div class="qgh"><b>Kaun kahan lagi hai aur kitni jagah khali hai</b> · ${fmt(T)} · north to south. Green rows = empty quay. "Length" = metres of quay between the two panel numbers.</div>`+SEGS.slice().reverse().map(block).join('');
}
'''
s = s[:a] + fn + s[b:]
# badges
rep("  setSum('moves',", "  {const vb=document.getElementById('vb-moves');if(vb)vb.innerHTML=`<b>${mvN}</b> moves · latest ${MV[0][0].replace(/\\s*[·(—].*$/,'').replace(/^HM signal /,'')}`;\n"
    "   const vs=document.getElementById('vb-score');if(vs){const L=MEETLOG[0];if(L){const got=(L.got||[]).map(x=>x[0]+'|'+x[1]),hit=(L.call||[]).filter(x=>got.includes(x[0]+'|'+x[1])).length;vs.innerHTML=`last meeting <b>${hit}</b> of ${(L.call||[]).length} right`;}}}\n  setSum('moves',")
rep("const SEC_OPEN_DEFAULT=new Set(['finder','quay','hpb']);", "const SEC_OPEN_DEFAULT=new Set(['finder','quay','hpb']); // the cargo tab is now two sections — both open")
B.s = s; B.save()
