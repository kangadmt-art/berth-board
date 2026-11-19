#!/usr/bin/env python3
# apply31 — v186: Tuna tab — vacant berths day by day, on a sketch of the pier (Mihir, 20 Nov 00:33–00:40).
import re, shutil
P='/home/claude/work/dpa-berth-board.html'; shutil.copy(P,'/home/claude/work/bak_v185.html'); s=open(P,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]); s=s.replace(a,b)
rep('''  <section class="card"><div class="sechead"><h2>How to read this board</h2></div>
    <div class="note">Tuna Tekra is a PPP terminal run by Adani''','''  <section class="card" aria-labelledby="tvh"><div class="sechead"><h2 id="tvh">Tuna · vacant berths, day by day</h2><p id="tvsub"></p></div>
    <div class="scroll"><svg class="tmap" id="tvmap" role="img" aria-label="Tuna pier — sea side and inner side, days vacant"></svg></div>
    <div class="scroll"><table class="mst" id="tvgrid" style="min-width:720px"></table></div>
    <div class="note" id="tvnote" style="margin-top:8px"></div>
  </section>
  <section class="card"><div class="sechead"><h2>How to read this board</h2></div>
    <div class="note">Tuna Tekra is a PPP terminal run by Adani''')
rep("function tuna(){\n", r"""// ---- TUNA · vacant berths, day by day (Mihir, 20 Nov 00:33–00:40: "do we have data on when the four Tuna berths had no vessel").
// TUNA_OCC: one entry a daily berthing list, OLDEST FIRST — the vessel alongside each berth at 0700 ('' = vacant); b:null = no list that day.
// WITH EVERY NEW LIST add an entry at the END. Lists are kept from 10 Nov 2026; nothing earlier is archived.
// HIS RULE (20 Nov 00:37): a berth is VACANT for a day only if it is vacant that morning AND still vacant on the next list — vacant at
// 0700 but occupied by the next list counts as OCCUPIED (it may have filled within the hour). The latest day waits for the next list.
// TUNA_SIDE (Mihir, 20 Nov 00:40): shore cranes stand only at the sea-side berths (west face, TT-1 / TT-3); the inner berths
// (east face, TT-2 / TT-4) have none — his reading of why they stay vacant, not from a port document.
const TUNA_SIDE={'TT-1':'sea','TT-3':'sea','TT-2':'inner','TT-4':'inner'};
const TUNA_OCC=[
 {d:'11-10',b:{'TT-1':'Doukato','TT-2':'','TT-3':'Navios Felicity I','TT-4':''}},
 {d:'11-11',b:{'TT-1':'Doukato','TT-2':'','TT-3':'','TT-4':''}},
 {d:'11-12',b:{'TT-1':'Doukato','TT-2':'','TT-3':'','TT-4':''}},
 {d:'11-13',b:{'TT-1':'Doukato','TT-2':'','TT-3':'Mykonos Wave','TT-4':'Bos Anjil'}},
 {d:'11-14',b:{'TT-1':'Doukato','TT-2':'','TT-3':'Mykonos Wave','TT-4':'Bos Anjil'}},
 {d:'11-15',b:null},
 {d:'11-16',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Mykonos Wave','TT-4':'Bos Anjil'}},
 {d:'11-17',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Beagle','TT-4':''}},
 {d:'11-18',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Beagle','TT-4':''}},
 {d:'11-19',b:{'TT-1':'Europa Graeca','TT-2':'','TT-3':'Beagle','TT-4':''}}
];
function tunaVac(){
  const g=id=>document.getElementById(id), tb=g('tvgrid'), svg=g('tvmap'); if(!tb||!svg)return;
  const B=['TT-1','TT-3','TT-2','TT-4'], D=TUNA_OCC, n=D.length, FMo='var(--f-mono)';
  const nextL=i=>{for(let j=i+1;j<n;j++)if(D[j].b)return D[j];return null;}, prevL=i=>{for(let j=i-1;j>=0;j--)if(D[j].b)return D[j];return null;};
  const st=(i,k)=>{const d=D[i];
    if(!d.b){const p=prevL(i),x=nextL(i);if(!p||!x)return {s:'unk',v:''};return (!p.b[k]&&!x.b[k])?{s:'vac',v:'',inf:1}:{s:'occ',v:x.b[k]||p.b[k],inf:1};}
    if(d.b[k])return {s:'occ',v:d.b[k]};
    const x=nextL(i);return !x?{s:'pend',v:''}:x.b[k]?{s:'fill',v:x.b[k]}:{s:'vac',v:''};};
  const cnt=k=>{let v=0,t=0;D.forEach((d,i)=>{const z=st(i,k).s;if(z==='vac'){v++;t++;}else if(z==='occ'||z==='fill')t++;});return {v,t};};
  const side=sd=>B.filter(k=>TUNA_SIDE[k]===sd).reduce((a,k)=>{const c=cnt(k);return {v:a.v+c.v,t:a.t+c.t};},{v:0,t:0});
  const lab=d=>{const x=dt(h(d+' 12:00'));return x.getUTCDate()+' '+MON[x.getUTCMonth()];}, S=side('sea'), I=side('inner');
  const scored=D.filter((d,i)=>['occ','vac','fill'].includes(st(i,'TT-1').s)), first=lab(D[0].d), lastS=lab(scored[scored.length-1].d);
  g('tvsub').innerHTML=`From the daily berthing lists (position at 0700), kept from <b>${first}</b>. A berth counts as vacant for a day only if it is vacant that morning <b>and</b> still vacant on the next list. ${first} to ${lastS}: sea side (TT-1, TT-3) vacant <b>${S.v} of ${S.t}</b> berth-days · inner side (TT-2, TT-4) vacant <b>${I.v} of ${I.t}</b> berth-days.`;
  // the pier — Mihir's sketch: TT-1 / TT-3 on the west (sea) face, TT-2 / TT-4 on the east (inner) face, trestle to the shore on the east
  svg.innerHTML='';svg.setAttribute('viewBox','0 0 760 300');
  el2('rect',{x:300,y:24,width:60,height:252,rx:4,fill:'#1f2b36',stroke:'var(--line2)'},svg);
  el2('text',{x:338,y:154,'text-anchor':'middle','font-family':FMo,'font-size':10,fill:'var(--dim)','letter-spacing':'.1em',transform:'rotate(-90 338 154)'},svg,'TUNA TEKRA PIER');
  el2('rect',{x:360,y:140,width:390,height:22,fill:'#1f2b36',stroke:'var(--line2)'},svg);
  el2('text',{x:555,y:155,'text-anchor':'middle','font-family':FMo,'font-size':10,fill:'var(--dim)','letter-spacing':'.1em'},svg,'APPROACH TRESTLE · TO SHORE →');
  el2('text',{x:100,y:17,'font-family':FMo,'font-size':10.5,fill:'#8fd0ff','letter-spacing':'.08em'},svg,'← SEA SIDE · SHORE CRANES');
  el2('text',{x:364,y:17,'font-family':FMo,'font-size':10.5,fill:'var(--muted)','letter-spacing':'.08em'},svg,'INNER SIDE · NO SHORE CRANE');
  const crane=y=>el2('path',{d:`M314 ${y} v-24 l-22 -5 M314 ${y-24} l9 7 M309 ${y} h10`,stroke:'#8fd0ff','stroke-width':2,fill:'none','stroke-linecap':'round','stroke-linejoin':'round'},svg);
  const box=(x,y,k)=>{const c=cnt(k),sh=c.t?c.v/c.t:0,now=D[n-1].b?D[n-1].b[k]:'';
    el2('rect',{x,y,width:196,height:100,rx:6,fill:c.v?`rgba(229,99,106,${(0.07+0.33*sh).toFixed(2)})`:'rgba(95,191,122,.10)',stroke:sh>=0.5?'#e5636a':c.v?'rgba(229,99,106,.5)':'rgba(95,191,122,.5)','stroke-width':1.4},svg);
    el2('text',{x:x+10,y:y+20,'font-family':FMo,'font-size':11,fill:'var(--brass)','letter-spacing':'.08em'},svg,k);
    el2('text',{x:x+10,y:y+50,'font-family':'var(--f-disp)','font-size':21,'font-weight':800,fill:c.v?'#ff9d8a':'#9be3b0'},svg,c.v?`VACANT ${c.v} OF ${c.t} DAYS`:'NEVER VACANT');
    el2('text',{x:x+10,y:y+72,'font-family':FMo,'font-size':10.5,fill:'var(--muted)'},svg,'latest list: '+(now||'vacant'));};
  box(100,30,'TT-1');box(100,170,'TT-3');box(364,30,'TT-2');box(364,170,'TT-4');[78,118,218,258].forEach(crane);
  // the grid
  const cell=(i,k)=>{const x=st(i,k),nm=x.v?x.v.split(' ').slice(0,2).join(' '):'',q=x.inf?'*':'';
    if(x.s==='occ')return `<td style="background:rgba(95,191,122,.10)">${nm}${q}</td>`;
    if(x.s==='vac')return `<td style="background:rgba(229,99,106,.24);color:#ff9d8a;font-weight:700">VACANT${q}</td>`;
    if(x.s==='fill')return `<td style="background:rgba(207,143,63,.13);color:#f3b86a">vacant 0700<br><small>then ${nm}</small></td>`;
    if(x.s==='pend')return `<td style="color:var(--muted)">vacant 0700<br><small>next list awaited</small></td>`;
    return '<td style="color:var(--muted)">—</td>';};
  const row=k=>{const c=cnt(k);return `<tr><td class="pk nw"><b>${k}</b></td>${D.map((d,i)=>cell(i,k)).join('')}<td class="nw"><b style="color:${c.v?'#ff9d8a':'#9be3b0'}">${c.v} of ${c.t}</b></td></tr>`;};
  const grp=(t,c)=>`<tr><td colspan="${n+2}" style="background:var(--panel2);padding:6px 8px;font-family:var(--f-mono);font-size:10.5px;letter-spacing:.08em;color:${c}">${t}</td></tr>`;
  tb.innerHTML=`<tr><th>Berth</th>${D.map(d=>`<th>${lab(d.d)}${d.b?'':'*'}</th>`).join('')}<th>Vacant days</th></tr>`
    +grp('SEA SIDE · SHORE CRANES','#8fd0ff')+row('TT-1')+row('TT-3')+grp('INNER SIDE · NO SHORE CRANE','var(--muted)')+row('TT-2')+row('TT-4');
  g('tvnote').innerHTML=`<b>How it is counted.</b> Red = vacant that morning and still vacant on the next list. Amber = vacant at 0700 but a vessel was alongside by the next list — counted as occupied. * = no berthing list was received that day; the day is read from the lists on either side. The latest day is settled when the next list comes. Shore cranes only at the sea-side berths is Mihir's information (20 Nov), not printed on any port sheet.`;
}
function tuna(){
""")
rep("  tunaTiles();\n", "  tunaTiles();tunaVac();\n")
rep("<div>New 20 Nov 00:26 (Mihir):", "<div>New 20 Nov 00:40 (Mihir): Tuna tab — vacant berths day by day on a sketch of the pier (sea side with shore cranes, inner side without), from the lists kept since 10 Nov · New 20 Nov 00:26 (Mihir):")
m=re.search(r"const UPDATED='[^']*';",s); s=s[:m.start()]+"const UPDATED='20 Nov 2026 · 01:00 IST';"+s[m.end():]
open(P,'w',encoding='utf-8').write(s); print('patched')
