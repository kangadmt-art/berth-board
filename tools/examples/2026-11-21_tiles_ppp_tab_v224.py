#!/usr/bin/env python3
# apply48 — v224 (Mihir, 21 Nov 21:26): Timber + Salt tiles on the main screen; quay-runs block folded and explained simply;
# meeting log and expected-vs-actual show the last two days only; new tab for the PPP berths CJ-9 / CJ-10.
import re, sys
p='/home/claude/work/dpa-berth-board.html'; s=open(p).read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(s.count(o),o[:80]); s=s.replace(o,n)
# ---------- A. tiles
a=s.index("   <div class=\"stat\" data-go=\"timber\" style=\"--sc:var(--tmb)\">"); b=s.index("</div>`;",a)+len("</div>`;")
TILE=r"""   <div class="stat biz" data-go="timber" style="--sc:var(--tmb)"><div class="v">${tqW+tqE}<small> waiting + expected</small></div><div class="l"><b>Timber vessels</b> · <b>${tqB}</b> at berth now</div><div class="comm"><span class="cc" style="--sc:var(--warn)"><b>${tqW}</b><span>waiting</span></span><span class="cc" style="--sc:#7fb2ff"><b>${tqE}</b><span>expected</span></span><span class="cc" style="--sc:var(--bad)"><b>${tmbMoney(tqS/24*DEM.usd)}</b><span>demurrage so far</span></span></div><div class="last">Tap to open the Timber page →</div></div>
   <div class="stat biz" data-go="salt" style="--sc:#dfe7f2"><div class="v">${slW+slE}<small> waiting + expected</small></div><div class="l"><b>Salt vessels</b> · <b>${slB}</b> at berth now</div><div class="comm"><span class="cc" style="--sc:var(--warn)"><b>${slW}</b><span>waiting</span></span><span class="cc" style="--sc:#7fb2ff"><b>${slE}</b><span>expected</span></span><span class="cc" style="--sc:var(--ok)"><b>${Math.round(slQ/1000)}k MT</b><span>to load</span></span></div><div class="last">Tap to open the Salt page →</div></div>`;"""
s=s[:a]+TILE+s[b:]
rep("  const TQ=tmbRows(), tqB=","  const isSl=c=>/salt/i.test(c||''),slB=V.filter(v=>isSl(v.c)&&v.F<=NOW&&v.T>NOW).length,slWl=W.filter(w=>isSl(w.c)&&w.rep!=null&&w.rep<=NOW),slEl=W.filter(w=>isSl(w.c)&&(w.rep==null||w.rep>NOW)),slW=slWl.length,slE=slEl.length,slQ=slWl.concat(slEl).reduce((a,w)=>a+(w.q||0),0);\n  const TQ=tmbRows(), tqB=")
rep("if(k==='liquid'||k==='tuna'||k==='timber'){setView(k,{top:true});}","if(k==='liquid'||k==='tuna'||k==='timber'||k==='salt'){setView(k,{top:true});}")
a=s.index("  {const st=document.getElementById('stats'),all=[...st.children],more="); b=s.index("st.appendChild(d);}}",a)+len("st.appendChild(d);}}")
s=s[:a]+"""  {const st=document.getElementById('stats'),all=[...st.children]; // main screen (Mihir, 21 Nov 21:26): Timber and Salt first — waiting + expected as the big number, at berth beneath — then the all-vessels tile; the other nine fold under "More figures"
   if(all.length===12){const keep=[all[10],all[11],all[0]],more=all.filter(e=>!keep.includes(e));keep.forEach(e=>st.appendChild(e));const d=document.createElement('details');d.className='tdfull';d.style.gridColumn='1/-1';d.innerHTML='<summary>More figures · dry cargo by commodity · import / export · bulk · bagged · break bulk · expected · berths occupied · oil jetties · Tuna</summary><div class="stats" style="margin-top:8px"></div>';const box=d.lastChild;more.forEach(e=>box.appendChild(e));st.appendChild(d);}}"""+s[b:]
# ---------- B. quay runs: folded, plain words
a=s.index("  el.innerHTML=`<div class=\"bh\"><h3>Free quay runs · panel-wise · CJ-13 to CJ-16 and CJ-1 to CJ-8</h3><small>"); b=s.index("</small></div>${SEGS.map(block).join('')}`;",a)+len("</small></div>${SEGS.map(block).join('')}`;")
s=s[:a]+"""  el.innerHTML=`<details class="tdfull"><summary><b>Free space on the quay</b> · where a waiting vessel could fit, each time a vessel sails or berths</summary><div class="bh"><h3>Free space on the quay · CJ-13 to 16 and CJ-1 to 8</h3><small><b>How to read it.</b> Each card is one moment when the quay changes — a vessel sails or berths. <b>Panels 156¾–173½</b> = the empty stretch of quay at that moment, by panel number (the scale in the picture above). <b>~254 m</b> = how long that stretch is. <b>– clearance</b> = one panel is kept free beside each neighbouring vessel, so the usable length is shorter. <b>vessel up to ~246 m</b> = the longest vessel that fits. <b>fits, in slot order</b> = the ready vessels that are short enough and are allowed at those berths, in the order of priority. "taken by …" means the programme or signal has already given that space. It only shows where there is room — the board's berthing dates are in the tables above, not here.</small></div>${SEGS.map(block).join('')}</details>`;"""+s[b:]
# ---------- C. meeting log: last two meetings; expected vs actual: open + last two days
rep("  ${openCard}${rows.map(card).join('')}`;","  ${openCard}${rows.slice(0,2).map(card).join('')}${rows.length>2?`<div class=\"empty\" style=\"margin-top:8px\">The last two meetings are shown. ${rows.length-2} earlier meetings are kept in the data book; the totals above count all of them.</div>`:''}`;")
old208=open('/home/claude/work/bak_v208.html').read().split("\n"); old204=open('/home/claude/work/bak_v204.html').read().split("\n")
keep=[l for l in old208 if l.startswith(" {d:'21 Nov 16:19 · Mihir\\'s team — HP is a bid'") or l.startswith(" {d:'21 Nov 10:21 · list 21.11 (0700) + HM signal 21 Nov (disp 07:46)'")]
keep+= [l for l in old204 if l.startswith(" {d:'21 Nov 14:46 · programme 22.11 + list 21.11 revised")]
assert len(keep)==3,len(keep)
keep.sort(key=lambda l:l[5:17],reverse=True)
a=s.index("const LEARN=[\n")+len("const LEARN=[\n"); e=s.index("\n",a)+1   # after the first (open) entry
s=s[:e]+"\n".join(keep)+"\n"+s[e:]
# ---------- D. PPP tab
rep('<span class="vb" id="vb-salt"></span></a>\n','<span class="vb" id="vb-salt"></span></a>\n    <a href="#ppp" data-view="ppp"><b>CJ-9 · 10</b><small>PPP berths · Gautam Freight · what is alongside and what is next</small><span class="vb" id="vb-ppp"></span></a>\n')
rep("salt:'Deendayal Port · Kandla · Salt vessels',","salt:'Deendayal Port · Kandla · Salt vessels',ppp:'Deendayal Port · Kandla · CJ-9 and CJ-10 (PPP)',")
rep("const VIEW_NAME={cargo:'Cargo jetties',","const VIEW_NAME={ppp:'CJ-9 · CJ-10',salt:'Salt',cargo:'Cargo jetties',")
rep('.views a[data-view="salt"]{--sc:#dfe7f2}','.views a[data-view="salt"]{--sc:#dfe7f2}.views a[data-view="ppp"]{--sc:#c58bff}')
rep('  <div class="view" data-view="timber" id="view-timber">\n','''  <div class="view" data-view="ppp" id="view-ppp">
  <div class="tsum" id="pppstats" style="grid-template-columns:repeat(2,minmax(0,1fr))"></div>
  <section class="card"><div class="sechead"><h2>CJ-9 and CJ-10 · PPP berths</h2><p id="pppsub"></p></div><div id="ppplist"></div></section>
  <section class="card"><div class="sechead"><h2>Circulars on these berths</h2><p>Every DPA paper on the operation of CJ-9 and CJ-10 that is on the register.</p></div><div id="pppcirc"></div></section>
  </div>
  <div class="view" data-view="timber" id="view-timber">
''')
PPP=r"""
// ================= CJ-9 / CJ-10 tab (Mihir, 21 Nov 21:26) =================
// "PPP wale 9 and 10 berth ka bhi page alag bana de to pata chale udhar kya chal raha hai." Status only — these berths are run by Gautam Freight (O&M) and are outside the berthing-policy queue.
function ppp(){
  const el=document.getElementById('ppplist'); if(!el)return;
  const MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],s2=t=>{if(t==null)return '—';const d=dt(t);return String(d.getUTCDate()).padStart(2,'0')+' '+MN[d.getUTCMonth()]+' '+String(d.getUTCHours()).padStart(2,'0')+':'+String(d.getUTCMinutes()).padStart(2,'0');},f=x=>x==null?'—':Math.round(x).toLocaleString('en-IN'),base=n=>n.replace(/ \(.*$/,'');
  const P=V.filter(v=>v.b==='9'||v.b==='10').sort((a,z)=>a.F-z.F),now=P.filter(v=>v.F<=NOW&&v.T>NOW),next=P.filter(v=>v.F>NOW),past=P.filter(v=>v.T<=NOW).sort((a,z)=>z.T-a.T);
  const dprOf=n=>DPR.rows.find(r=>base(r.n)===base(n)&&/^CJ-(9|10)$/.test(r.loc||''));
  const wq=W.filter(w=>/CJ-?0?9\b|CJ-?10\b|GFPL/i.test(w.x||'')&&!P.some(v=>base(v.n)===base(w.n)));
  const tbl=(th,rows)=>`<div class="sdwrap"><table class="sdt"><tr>${th.map((x,i)=>`<th${(i===0||i===th.length-1)?' class="l"':''}>${x}</th>`).join('')}</tr>${rows.join('')}</table></div>`,head=t=>`<div class="sdh">${t}</div>`;
  const row=(v,st)=>{const r=dprOf(v.n);return `<tr><td class="l"><b>${base(v.n)}</b>${gearChip(v.n)}</td><td>CJ-${v.b}</td><td>${st}</td><td>${v.c||'—'}</td><td>${f(v.q)} ${v.u||''}</td><td>${(typeof IE!=='undefined'&&IE[base(v.n)])||'—'}</td><td>${s2(v.F)}</td><td><b>${s2(v.T)}</b>${v.est?' est':''}</td><td>${r&&r.upto>0?f(r.upto):'—'}</td><td>${r&&r.upto>0?f(r.bal):'—'}</td><td class="l">${(typeof AG!=='undefined'&&AG[base(v.n)])||'—'}</td></tr>`;};
  const TH=['Vessel','Berth','Status','Cargo','Quantity','I/E','Berthed','Out about','Done (DPR)','Left (DPR)','Agent'];
  let H='';
  H+=head('At berth now · '+now.length)+(now.length?tbl(TH,now.map(v=>row(v,'working'))):'<div class="empty">No vessel alongside CJ-9 or CJ-10 at this hour.</div>');
  H+=head('Coming next · '+next.length)+(next.length?tbl(TH,next.map(v=>row(v,'programmed'))):'<div class="empty">No next vessel named on the programme or signal.</div>');
  if(wq.length)H+=head('Waiting / expected for these berths (list remark) · '+wq.length)+tbl(['Vessel','Cargo','Quantity','Reported / ETA','Ready','List remark'],wq.map(w=>`<tr><td class="l"><b>${w.n}</b>${gearChip(w.n)}</td><td>${w.c}</td><td>${f(w.q)} ${w.u}</td><td>${s2(w.rep)}</td><td>${w.rdy!=null?s2(w.rdy):'N/A'}</td><td class="l" style="white-space:normal;min-width:220px">${String(w.x||'').slice(0,140)}</td></tr>`));
  if(past.length)H+=head('Last vessel out · '+past.length)+tbl(TH,past.map(v=>row(v,'sailed')));
  el.innerHTML=H;
  const tp=(c,v,l)=>`<div class="tp" style="--sc:${c}"><b>${v}</b><span>${l}</span></div>`;
  const b9=now.find(v=>v.b==='9'),b10=now.find(v=>v.b==='10'),n9=next.find(v=>v.b==='9');
  document.getElementById('pppstats').innerHTML=tp('#c58bff',b9?base(b9.n):'vacant','CJ-9 · '+(b9?(b9.c+' · out about '+s2(b9.T)):'no vessel')+(n9?' · next: '+base(n9.n)+', '+s2(n9.F):''))+tp('var(--muted)',b10?base(b10.n):'no vessel','CJ-10 · '+(b10?b10.c:'shown as under maintenance on the board — nothing on the list, programme or signal'));
  document.getElementById('pppsub').innerHTML='CJ-9 and CJ-10 are operated by M/s Gautam Freight Pvt Ltd (O&amp;M). They are <b>outside the DPA berthing queue</b>, so the board does not project them — this page only shows what the list, programme, HM signal and DPR say: who is alongside, when she leaves, who is named next. Every past call at these berths is kept in the data book.';
  const circ=NOTICES.filter(n=>/\b0?9\s*(&|and|,|\/)\s*10\b|Gautam|GFPL|OMCJ910/i.test((n.t||'')+' '+(n.ref||''))).sort((a,z)=>String(z.iso).localeCompare(String(a.iso)));
  document.getElementById('pppcirc').innerHTML=circ.length?tbl(['Date','Circular','Ref','PDF'],circ.map(n=>`<tr><td class="l">${n.rd||''}</td><td style="text-align:left;white-space:normal;min-width:240px"><b>${n.t}</b></td><td style="text-align:left;white-space:normal">${n.ref||''}</td><td class="l">${n.file?`<a class="plink" href="${n.file}" target="_blank" rel="noopener">open</a>`:'—'}</td></tr>`)):'<div class="empty">None on the register.</div>';
  const vb=document.getElementById('vb-ppp');if(vb)vb.innerHTML=(b9?'<b>'+base(b9.n)+'</b>':'CJ-9 vacant')+(n9?' · next '+base(n9.n):'');
}
"""
rep("function timber(){","PPPMARK\nfunction timber(){")
s=s.replace("PPPMARK\n",PPP.lstrip("\n"),1)
rep("notices();news();learn();salt();","notices();news();learn();salt();ppp();")
s=re.sub(r"const UPDATED='[^']*';","const UPDATED='21 Nov 2026 · 21:45 IST';",s,count=1)
open(p,'w').write(s)
