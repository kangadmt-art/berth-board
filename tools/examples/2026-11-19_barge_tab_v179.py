#!/usr/bin/env python3
# apply25 — v179: BARGE becomes its own tab at the top, with the work shown commodity-wise (Mihir, 19 Nov 22:55). argv[1] = UPDATED.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v178.html')
B = Board(P)
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % sys.argv[1] + B.s[m.end():]
# ---- the section leaves the Cargo tab
a = B.s.index('\n  <section class="card" data-sec="msb" aria-labelledby="bgh">'); e = B.s.index("</section>\n", a) + len("</section>\n")
B.s = B.s[:a] + B.s[e:]
B.rep("const SEC_OPEN_DEFAULT=new Set(['finder','mine','msb']);", "const SEC_OPEN_DEFAULT=new Set(['finder','mine']);")
# ---- tab + view
B.rep('.views a[data-view="priority"]{--sc:#d9b25f}', '.views a[data-view="priority"]{--sc:#d9b25f}.views a[data-view="barge"]{--sc:#4fd1c5}')
B.rep("@media (max-width:640px){.views{gap:6px}.views a{flex:1 1 0;padding:8px 9px 7px}", "@media (max-width:640px){.views{gap:6px;flex-wrap:wrap}.views a{flex:1 1 30%;padding:8px 9px 7px}")
a, b = B.line_of('    <a href="#priority" data-view="priority">')
B.s = B.s[:b + 1] + '    <a href="#barge" data-view="barge"><b>Barge</b><small>Midstream · vessels working by barge · daily discharge / loading · commodity-wise</small><span class="vb" id="vb-barge"></span></a>\n' + B.s[b + 1:]
B.rep('  <div class="view" data-view="timber" id="view-timber">', '''  <div class="view" data-view="barge" id="view-barge">
  <section class="card" aria-labelledby="bgh"><div class="sechead"><h2 id="bgh">Barge work · midstream</h2><p id="bgsub"></p></div>
    <div class="stats" id="bgstats" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))"></div></section>
  <section class="card" aria-labelledby="bgh2"><div class="sechead"><h2 id="bgh2">Daily barge discharge &amp; loading</h2><p>Each DPR covers the 24 hours to 0700. Tap a day — its commodities and vessels show below.</p></div>
    <div class="scroll"><table class="mst" id="bgday"></table></div></section>
  <section class="card" aria-labelledby="bgh3"><div class="sechead"><h2 id="bgh3">Commodity-wise</h2><p id="bgcsub"></p></div>
    <div class="scroll"><table class="mst" id="bgcom"></table></div></section>
  <section class="card" aria-labelledby="bgh4"><div class="sechead"><h2 id="bgh4">Vessel operations · commodity-wise</h2><p id="bgvsub"></p></div>
    <div class="scroll"><table class="mst" id="bgves" style="min-width:620px"></table></div></section>
  </div>
  <div class="view" data-view="timber" id="view-timber">''')
B.rep("priority:'Deendayal Port · Kandla · Priority chart',", "priority:'Deendayal Port · Kandla · Priority chart',barge:'Deendayal Port · Kandla · Barge work',")
B.rep("const VIEW_NAME={cargo:'Cargo jetties',priority:'Priority chart',", "const VIEW_NAME={cargo:'Cargo jetties',priority:'Priority chart',barge:'Barge',")
B.rep("// tabs: Cargo jetties · Priority chart · Timber · Tuna · Liquid — same page, hash remembers the open board (#cargo / #priority / #timber / #tuna / #liquid)",
      "// tabs: Cargo jetties · Priority chart · Barge · Timber · Tuna · Liquid — same page, hash remembers the open board (#cargo / #priority / #barge / #timber / #tuna / #liquid)")
B.rep("New 19 Nov 22:49 (Mihir): a section \"Midstream · barge work\" — vessels working by barge and the daily barge discharge / loading, from DPR 17.11, 18.11 and 19.11 · ",
      "New 19 Nov 22:55 (Mihir): a BARGE tab — vessels working by barge, the daily barge discharge / loading and the work commodity-wise, from DPR 17.11, 18.11 and 19.11 · ")
# ---- data: one row a vessel and cargo
days = open(W + 'barge_days.txt', encoding='utf-8').read().rstrip().rstrip(',')
a = B.s.index("const MSWORK={days:[\n") + len("const MSWORK={days:[\n"); e = B.s.index("\n]};", a)
B.s = B.s[:a] + days + B.s[e:]
B.rep("// ---- MIDSTREAM · BARGE WORK (since v178; Mihir, 19 Nov 22:49: \"vessel working with barge\" and \"daily barge discharge and loading\").\n// One entry a DPR, NEWEST FIRST. Each row is a vessel worked by barges,",
      "// ---- BARGE tab — midstream / barge work (v178 as a section, v179 its own tab; Mihir, 19 Nov 22:49 and 22:55: \"vessel working with barge\", \"daily barge discharge and loading\", \"commodity wise\").\n// One entry a DPR, NEWEST FIRST. Each row is a vessel AND cargo worked by barges,")
# ---- renderer
a = B.s.index("function msWork(){"); e = B.s.index("\nfunction dpr(){\n", a)
B.s = B.s[:a] + r"""function msWork(){
  const g=id=>document.getElementById(id), sub=g('bgsub'),st=g('bgstats'),td=g('bgday'),tc=g('bgcom'),tv=g('bgves');if(!td||!MSWORK.days.length)return;
  // commodity of a cargo line — first match wins; an unknown cargo stands under its own name
  const COMM=[[/coal|coke/i,'Coal'],[/rice/i,'Rice'],[/sugar/i,'Sugar'],[/npk|urea|dap|mop|fertili|sulphate|phosph/i,'Fertiliser'],[/bentonite|clay|kaolin/i,'Bentonite / clay'],[/salt/i,'Salt'],[/steel|pipe|coil|slab/i,'Steel'],[/wheat|maize|pulses|soya|meal|rsm/i,'Foodgrain / meal'],[/barite|ore|gypsum/i,'Ore / minerals']];
  const commOf=c=>{const m=COMM.find(x=>x[0].test(c));return m?m[1]:c;};
  const sum=(rows,ie)=>rows.filter(r=>r.ie===ie).reduce((a,r)=>a+r.l24,0), uniq=rows=>[...new Set(rows.map(r=>r.n))];
  const D=MSWORK.days.map(d=>({d,dis:sum(d.rows,'IMP'),load:sum(d.rows,'EXP'),n:uniq(d.rows.filter(r=>r.l24>0)).length})), mx=Math.max(...D.map(x=>x.dis+x.load),1);
  const tile=(c,v,l)=>`<div class="stat" style="--sc:${c};cursor:default"><div class="v" style="font-size:26px">${v}</div><div class="l">${l}</div></div>`;
  const wk=ie=>ie==='IMP'?'<span style="color:var(--warn)">Discharge</span>':'<span style="color:var(--ok)">Loading</span>';
  const L=D[0], vb=g('vb-barge'); if(vb)vb.innerHTML=`<b>${nf.format(L.dis+L.load)}</b> MT · ${L.n} vessels · DPR ${L.d.d}`;
  let cur=0;
  const draw=()=>{const x=D[cur], d=x.d, G={};
    d.rows.forEach(r=>{const k=commOf(r.c)+'|'+r.ie;(G[k]=G[k]||{k:commOf(r.c),ie:r.ie,rows:[]}).rows.push(r);});
    const groups=Object.values(G).map(q=>Object.assign(q,{l24:q.rows.reduce((a,r)=>a+r.l24,0),upto:q.rows.reduce((a,r)=>a+r.upto,0),bal:q.rows.reduce((a,r)=>a+r.bal,0),ves:uniq(q.rows)})).sort((a,z)=>z.l24-a.l24||z.bal-a.bal);
    sub.innerHTML=`Vessels worked by barges at midstream and the moorings, from the DPA <b>Daily Performance Report</b>. Latest, DPR <b>${L.d.d}</b> (24 h to 0700): <b>${L.n}</b> vessels worked · discharge <b>${nf.format(L.dis)}</b> MT · loading <b>${nf.format(L.load)}</b> MT. All figures in MT.`;
    st.innerHTML=tile('var(--brass)',L.n,'<b>Vessels working by barge</b> · DPR '+L.d.d)+tile('var(--warn)',nf.format(L.dis)+'<small> MT</small>','<b>Barge discharge</b> · import, ship → barge')+tile('var(--ok)',nf.format(L.load)+'<small> MT</small>','<b>Barge loading</b> · export, barge → ship')+tile('var(--line2)',nf.format(L.dis+L.load)+'<small> MT</small>','<b>Total by barge</b> · 24 h to 0700');
    td.innerHTML=`<tr><th>DPR</th><th>Vessels</th><th>Discharge</th><th>Loading</th><th>Total</th><th style="width:26%"></th></tr>`
      +D.map((y,i)=>`<tr data-i="${i}" style="cursor:pointer${i===cur?';background:rgba(92,200,255,.08)':''}"><td class="pk nw"><b>${y.d.d}</b>${i===cur?' <span style="color:var(--brass);font-size:11px">▾</span>':''}</td><td>${y.n}</td><td><b>${nf.format(y.dis)}</b></td><td><b>${nf.format(y.load)}</b></td><td><b>${nf.format(y.dis+y.load)}</b></td><td><div style="display:flex;height:10px;border-radius:3px;overflow:hidden;background:var(--panel2);width:${Math.max(4,Math.round((y.dis+y.load)/mx*100))}%"><span style="width:${(y.dis/(y.dis+y.load||1)*100).toFixed(1)}%;background:var(--warn)"></span><span style="flex:1;background:var(--ok)"></span></div></td></tr>`).join('');
    td.querySelectorAll('tr[data-i]').forEach(r=>r.onclick=()=>{cur=+r.dataset.i;draw();});
    g('bgcsub').innerHTML=`DPR <b>${d.d}</b> — what the barges moved in the 24 hours, commodity by commodity.`;
    tc.innerHTML=`<tr><th>Commodity</th><th>Work</th><th>Last 24 h</th><th>Up to date</th><th>Balance</th><th>Vessels</th></tr>`
      +groups.map(q=>`<tr><td class="pk nw"><b>${q.k}</b></td><td>${wk(q.ie)}</td><td><b>${q.l24?nf.format(q.l24):'—'}</b></td><td>${nf.format(q.upto)}</td><td><b>${nf.format(q.bal)}</b></td><td>${q.ves.length} · <span style="color:var(--muted)">${q.ves.join(', ')}</span></td></tr>`).join('')
      +`<tr><td class="pk nw"><b>All</b></td><td style="color:var(--muted)">${nf.format(x.dis)} dis · ${nf.format(x.load)} load</td><td><b>${nf.format(x.dis+x.load)}</b></td><td></td><td></td><td>${x.n} working</td></tr>`;
    g('bgvsub').innerHTML=`DPR <b>${d.d}</b> — each vessel under her commodity: cargo over the ship's rail in the 24 hours, the total so far, what is left and how long at this rate.`;
    tv.innerHTML=`<tr><th>Vessel</th><th>Cargo</th><th>Last 24 h</th><th>Up to date</th><th>Balance</th><th>Barges loaded at · agent / stevedore</th></tr>`
      +groups.map(q=>`<tr><td colspan="6" style="background:var(--panel2);padding:7px 8px"><b style="font-family:var(--f-disp);font-size:16px;text-transform:uppercase;letter-spacing:.02em">${q.k}</b> &nbsp;${wk(q.ie)} · <b>${nf.format(q.l24)}</b> MT in 24 h · ${q.ves.length} vessel${q.ves.length>1?'s':''} · balance ${nf.format(q.bal)} MT</td></tr>`
        +q.rows.map(r=>{const dy=r.l24>0&&r.bal>0?r.bal/r.l24:null;return `<tr><td class="pk"><b>${r.n}</b>${isMine(r.n)?' <span style="color:var(--brass);font-size:11px">Mihir &amp; Co</span>':''}<br><span style="color:var(--muted)">${r.loc==='MS'?'midstream':'mooring '+r.loc}</span></td><td>${r.c}</td><td><b>${r.l24?nf.format(r.l24):'—'}</b>${r.l24?'':'<br><span style="color:var(--muted)">no work</span>'}</td><td>${nf.format(r.upto)}</td><td><b>${r.bal?nf.format(r.bal):'done'}</b>${dy!=null?`<br><span style="color:var(--muted)">${dy<1?'under a day':'~'+dy.toFixed(1)+' d'} at this rate</span>`:''}</td><td class="w">${r.shore?'<b>'+r.shore+' MT</b>':''}${r.ag}${r.st?' · '+r.st:''}</td></tr>`;}).join('')).join('')
      +(d.sts?`<tr><td colspan="6" class="w">Ship-to-ship, not barge work: ${d.sts}</td></tr>`:'')
      +`<tr><td colspan="6" class="w">Ship-side figures as the DPR prints them. The DPR gives no figure barge by barge, and none for import cargo landed at the shore.</td></tr>`;
  };
  draw();
}""" + B.s[e:]
B.save()
