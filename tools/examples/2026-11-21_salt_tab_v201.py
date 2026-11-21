#!/usr/bin/env python3
# apply45 — v201: SALT tab (Mihir, 21 Nov 14:31): every salt vessel — arrived, berthed, sailed and the days; completed vessels stay on show; month-wise figure. No demurrage on this tab.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
B.rep("timber:'Deendayal Port · Kandla · Timber vessels',", "timber:'Deendayal Port · Kandla · Timber vessels',salt:'Deendayal Port · Kandla · Salt vessels',")
B.rep('<span class="vb" id="vb-timber"></span></a>\n', '<span class="vb" id="vb-timber"></span></a>\n    <a href="#salt" data-view="salt"><b>Salt</b><small>Salt vessels · arrived · berthed · sailed · days · record</small><span class="vb" id="vb-salt"></span></a>\n')
B.rep('.views a[data-view="timber"]{--sc:var(--tmb)}', '.views a[data-view="timber"]{--sc:var(--tmb)}.views a[data-view="salt"]{--sc:#dfe7f2}')
B.rep('  <div class="view" data-view="timber" id="view-timber">\n', '''  <div class="view" data-view="salt" id="view-salt">
  <div class="tsum" id="saltstats" aria-label="Salt vessels — summary" style="grid-template-columns:repeat(4,minmax(0,1fr))"></div>
  <section class="card"><div class="sechead"><h2>Salt vessels</h2><p id="saltsub"></p></div><div id="saltlist"></div></section>
  <section class="card"><div class="sechead"><h2>Completed vessels · record</h2><p>Every salt vessel that has loaded and sailed, newest first — kept for good.</p></div><div id="saltdone"></div></section>
  </div>
  <div class="view" data-view="timber" id="view-timber">
''')
SALT = r'''
// ================= SALT tab (Mihir, 21 Nov 14:31) =================
// "Salt wale mae sirf aaya, laga aur nikla — total kitne din huve; completed vessel dikhte rahe aur monthly figure bhi." No demurrage here.
// SALT_DONE = the record of salt vessels that have sailed: n, q (MT), ag, b (berth), pri, arr (reported for the salt call; null = not on record), mf (made fast), out (left the berth).
// tools/trim_board.js adds a salt vessel here when it takes her out of V.
const SALT_DONE=[
 {n:'Agia Fevronia',q:60500,ag:'Gautham Freight',b:'16',pri:'HP',arr:null,mf:'10-28 18:06',out:'10-30 06:00'},
 {n:'Maritime Harmony',q:74850,ag:'Cross Trade',b:'16',pri:'HP',arr:null,mf:'10-30 13:00',out:'11-01 18:00'},
 {n:'Unity Melody',q:54705,ag:'Gautham Freight',b:'15A',pri:'HP',arr:'11-03 14:00',mf:'11-05 10:24',out:'11-06 23:05'},
 {n:'Orion',q:61600,ag:'Cross Trade',b:'16',pri:'24H',arr:'10-27 10:42',mf:'11-05 14:30',out:'11-06 14:30'},
 {n:'Mettle Star',q:79080,ag:'Cross Trade',b:'15A',pri:'24H',arr:'11-01 06:42',mf:'11-07 11:30',out:'11-08 11:30'},
 {n:'Star Fighter',q:58000,ag:'Cross Trade',b:'16',pri:'8K',arr:'11-04 22:48',mf:'11-09 15:54',out:'11-12 01:35'},
 {n:'HN Doris',q:75000,ag:'Cross Trade',b:'16',pri:'HP',arr:'11-14 03:54',mf:'11-17 21:12',out:'11-19 21:20'},
 {n:'Bristol',q:63200,ag:'True Blue',b:'15A',pri:'HP',arr:'11-16 00:00',mf:'11-17 21:30',out:'11-19 20:40'},
 {n:'Rome Trader',q:55275,ag:'Mihir & Company',b:'13',pri:'SAAGAR',arr:'11-14 17:00',mf:'11-18 17:00',out:'11-20 23:40'}
];
function salt(){const el=document.getElementById('saltlist');if(!el)return;
  const isS=c=>/salt/i.test(c||''),base=n=>n.replace(/ \(.*$/,''),mine=x=>/mihir/i.test(x.ag||''),MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const f=x=>Math.round(x).toLocaleString('en-IN'),dd=(a,b)=>(a==null||b==null)?null:(b-a)/24,d1=x=>x==null?'—':x.toFixed(1)+' d',tm=x=>x==null?'not on record':fmt(x);
  const PR={GOV:'Govt',COASTAL:'Coastal',HP:'Higher productivity',SAAGAR:'SAAGAR','24H':'24 hours','8K':'6.5K / 8K',STL:'Steel / Project',BIT:'Bitumen',GEN:'General'};
  const arrOf=n=>REP[n]?h(REP[n]):(REP[base(n)]?h(REP[base(n)]):null);
  const done=SALT_DONE.map(r=>({n:r.n,q:r.q,ag:r.ag,b:r.b,pri:r.pri,arr:r.arr?h(r.arr):null,mf:h(r.mf),out:h(r.out)}));
  V.filter(v=>isS(v.c)&&v.T<=NOW&&!v.est).forEach(v=>{if(!done.some(r=>r.n===base(v.n)&&Math.abs(r.mf-v.F)<1))done.push({n:base(v.n),q:v.q,ag:agOf(v.n),b:v.b,pri:v.cat,arr:arrOf(v.n),mf:v.F,out:v.T});});
  done.sort((a,z)=>z.out-a.out);
  const atB=V.filter(v=>isS(v.c)&&v.F<=NOW&&v.T>NOW),com=V.filter(v=>isS(v.c)&&v.F>NOW);
  const wt=W.filter(w=>isS(w.c)&&w.rep!=null&&w.rep<=NOW),ex=W.filter(w=>isS(w.c)&&(w.rep==null||w.rep>NOW)).sort((a,z)=>(a.rep||1e9)-(z.rep||1e9));
  const tag=x=>mine(x)?' <span class="ie" style="border:1px solid var(--brass);color:var(--brass)">Mihir &amp; Co</span>':'';
  const row=(name,ag,top,l1,l2)=>`<div style="padding:10px 2px;border-bottom:1px solid var(--line)${mine({ag})?';border-left:3px solid var(--brass);padding-left:9px':''}"><div style="display:flex;justify-content:space-between;gap:8px;align-items:baseline;flex-wrap:wrap"><b style="font-size:15px">${name}${tag({ag})}${gearChip(name)}</b><span style="font-size:12px;color:var(--brass)">${top}</span></div><div style="font-size:12.5px;color:var(--muted);margin-top:2px">${l1}</div><div style="font-size:12.5px;margin-top:2px">${l2}</div></div>`;
  const head=t=>`<div style="font-size:11px;letter-spacing:.12em;color:var(--muted);text-transform:uppercase;margin:14px 0 2px;padding:5px 8px;background:rgba(255,255,255,.04)">${t}</div>`;
  let H='';
  if(atB.length){H+=head('Loading at berth');atB.forEach(v=>{const a=arrOf(v.n);H+=row(base(v.n),agOf(v.n),'CJ-'+v.b,`${f(v.q)} MT · ${PR[v.cat]||v.cat} · agent ${agOf(v.n)}`,`arrived <b>${tm(a)}</b> · berthed <b>${fmt(v.F)}</b> · waited ${d1(dd(a,v.F))} · at berth ${d1(dd(v.F,NOW))} so far · out about <b>${fmt(v.T)}</b>`);});}
  if(com.length){H+=head('Coming alongside');com.forEach(v=>{const a=arrOf(v.n);H+=row(base(v.n),agOf(v.n),'CJ-'+v.b,`${f(v.q)} MT · ${PR[v.cat]||v.cat} · agent ${agOf(v.n)}`,`arrived <b>${tm(a)}</b> · berthing about <b>${fmt(v.F)}</b>`);});}
  if(wt.length){H+=head('Arrived · waiting for a berth');wt.forEach(w=>{const p=S.find(x=>x.n===w.n&&x.proj);H+=row(base(w.n),agOf(w.n),'waiting '+d1(dd(w.rep,NOW)),`${f(w.q)} MT · agent ${agOf(w.n)}${w.rdy==null?' · readiness not declared':''}`,`arrived <b>${fmt(w.rep)}</b> · board: ${p?'<b>CJ-'+p.b+' about '+fmt(p.F)+'</b>':'beyond the projection'}`);});}
  if(ex.length){H+=head('Expected · not yet arrived');ex.forEach(w=>{const p=S.find(x=>x.n===w.n&&x.proj);H+=row(base(w.n),agOf(w.n),w.rep!=null?'ETA '+fmt(w.rep).replace(/ \d\d:\d\d$/,''):'ETA not given',`${f(w.q)} MT · agent ${agOf(w.n)}`,p?`board: <b>CJ-${p.b} about ${fmt(p.F)}</b>`:'');});}
  el.innerHTML=H||'<div class="empty">No salt vessel at berth, waiting or expected.</div>';
  // month-wise — by the month she sailed
  const m={};done.forEach(r=>{const d=dt(r.out),k=d.getUTCFullYear()*100+d.getUTCMonth();const o=m[k]=m[k]||{n:0,q:0,st:0,ns:0,lab:MN[d.getUTCMonth()]+' '+d.getUTCFullYear()};o.n++;o.q+=r.q||0;const t=dd(r.mf,r.out);o.st+=t;});
  const ks=Object.keys(m).sort(),T=ks.reduce((s,k)=>({n:s.n+m[k].n,q:s.q+m[k].q,st:s.st+m[k].st}),{n:0,q:0,st:0});
  const mt=`<table style="width:100%;margin-top:8px;border-collapse:collapse;font-size:12.5px;text-align:right"><tr style="color:var(--muted)"><th style="text-align:left;font-weight:600">Salt loaded · by month of sailing</th><th style="font-weight:600">Vessels</th><th style="font-weight:600">MT</th><th style="font-weight:600">Avg days at berth</th></tr>${ks.map(k=>`<tr><td style="text-align:left">${m[k].lab}</td><td>${m[k].n}</td><td>${f(m[k].q)}</td><td>${(m[k].st/m[k].n).toFixed(1)}</td></tr>`).join('')}<tr style="border-top:1px solid var(--line);font-weight:700"><td style="text-align:left">On record</td><td>${T.n}</td><td>${f(T.q)}</td><td>${T.n?(T.st/T.n).toFixed(1):'—'}</td></tr></table>`;
  const sub=document.getElementById('saltsub');if(sub)sub.innerHTML='Arrived, berthed and sailed — and the days each took. No demurrage on this tab. Tonnage is the list quantity.'+mt;
  document.getElementById('saltdone').innerHTML=done.map(r=>row(r.n,r.ag,'CJ-'+r.b+' · total '+d1(dd(r.arr,r.out)),`${f(r.q)} MT · ${PR[r.pri]||r.pri} · agent ${r.ag}`,`arrived <b>${tm(r.arr)}</b> · berthed <b>${fmt(r.mf)}</b> · sailed <b>${fmt(r.out)}</b><br>waited ${d1(dd(r.arr,r.mf))} · at berth <b>${d1(dd(r.mf,r.out))}</b>`)).join('')||'<div class="empty">None yet.</div>';
  const tp=(c,v,l)=>`<div class="tp" style="--sc:${c}"><b>${v}</b><span>${l}</span></div>`;
  document.getElementById('saltstats').innerHTML=tp('var(--ok,#5fbf7a)',atB.length,'at berth')+tp('var(--warn)',wt.length,'waiting')+tp('#7fb2ff',ex.length,'expected')+tp('#dfe7f2',done.length,'completed ↓');
  const vb=document.getElementById('vb-salt');if(vb)vb.innerHTML=`<b>${atB.length}</b> at berth · <b>${wt.length}</b> waiting · <b>${ex.length}</b> expected`;}
'''
a, b = B.line_of("function timber(){")
B.s = B.s[:a] + SALT.lstrip('\n') + B.s[a:]
B.rep("notices();news();learn();", "notices();news();learn();salt();")
B.save()
