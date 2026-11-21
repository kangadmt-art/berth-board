#!/usr/bin/env python3
# python3 tools/build_books.py [out.html]  ->  the BOOKS page: Data book (searchable record of every vessel) · Rule book · Process book.
# Reads db/databook.json (made by tools/build_db.js) and book/RULE_BOOK.md, book/PROCESS_BOOK.md.
import json, re, sys, html, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(R, 'books.html')
db = json.load(open(os.path.join(R, 'db', 'databook.json'), encoding='utf-8'))
def md(path):
    o, inl = [], False
    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t); t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t); t = re.sub(r'`(.+?)`', r'<code>\1</code>', t); return t
    for ln in open(path, encoding='utf-8').read().split('\n'):
        if ln.startswith('- '):
            if not inl: o.append('<ul>'); inl = True
            o.append('<li>' + inline(ln[2:]) + '</li>'); continue
        if inl: o.append('</ul>'); inl = False
        if ln.startswith('# '): continue
        if ln.startswith('## '): o.append('<h3>' + inline(ln[3:]) + '</h3>')
        elif ln.strip(): o.append('<p>' + inline(ln) + '</p>')
    if inl: o.append('</ul>')
    return '\n'.join(o)
DATA = {'circ': db.get('circulars', []), 'asOf': db['asOf'], 'calls': db['calls'], 'waiting': db['waiting'], 'timberDone': db['timber'].get('done', [])}
blob = json.dumps(DATA, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
PAGE = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DPA Data Book</title>
<style>
:root{--bg:#0b1524;--card:#12203a;--card2:#16294a;--line:#263a5e;--ink:#e9eef7;--mut:#9fb0cc;--brass:#d4a94e;--brass2:#f0cf86;--ok:#5fd0a0;--warn:#f0a35e;--blue:#7fb2ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:14px 12px 60px}
header{display:flex;align-items:baseline;justify-content:space-between;gap:10px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:10px}
h1{font-size:20px;margin:0;letter-spacing:.3px}h1 b{color:var(--brass)}.asof{color:var(--mut);font-size:12.5px}
nav{display:flex;gap:6px;margin:12px 0;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5}
nav button{flex:1;background:var(--card);color:var(--mut);border:1px solid var(--line);border-radius:10px;padding:10px 6px;font:600 14px system-ui;cursor:pointer}
nav button.on{background:linear-gradient(180deg,#1b3158,#14264a);color:var(--brass2);border-color:var(--brass)}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:6px 0 12px}.tile{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px}
.tile b{display:block;font-size:22px;color:var(--brass2)}.tile span{color:var(--mut);font-size:12px}
input[type=search],select{width:100%;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:11px 12px;font:15px system-ui}
.row2{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:8px}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.chip{background:var(--card);border:1px solid var(--line);color:var(--mut);border-radius:999px;padding:6px 12px;font-size:13px;cursor:pointer}
.chip.on{color:#0b1524;background:var(--brass);border-color:var(--brass);font-weight:700}
.count{color:var(--mut);font-size:12.5px;margin:4px 2px 8px}
.v{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 12px;margin-bottom:8px;cursor:pointer}
.v.ours{border-left:3px solid var(--brass)}.vt{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.vn{font-weight:700;font-size:15.5px}.tag{font-size:11px;border-radius:6px;padding:2px 7px;font-weight:700;white-space:nowrap}
.t-sailed{background:#22324f;color:#b7c4dc}.t-alongside{background:#123f33;color:var(--ok)}.t-coming{background:#3d3214;color:var(--brass2)}.t-waiting{background:#3f2a14;color:var(--warn)}.t-expected{background:#17305a;color:var(--blue)}
.vs{color:var(--mut);font-size:13.5px;margin-top:2px}.vd{display:none;margin-top:9px;border-top:1px dashed var(--line);padding-top:9px;font-size:13.5px}
.v.open .vd{display:block}.kv{display:grid;grid-template-columns:118px 1fr;gap:3px 10px}.kv span{color:var(--mut)}.note{color:#c6d2e8;margin-top:8px;font-size:13px;white-space:pre-wrap}
h2{font-size:15px;color:var(--brass2);margin:22px 0 8px;letter-spacing:.4px;text-transform:uppercase}
table{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--card);border-radius:12px;overflow:hidden}th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:right}th:first-child,td:first-child{text-align:left}th{color:var(--mut);font-weight:600;font-size:12px}
.book{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:6px 16px 16px}.book h3{color:var(--brass2);font-size:16px;margin:20px 0 6px;border-bottom:1px solid var(--line);padding-bottom:5px}
.book li{margin:6px 0}.book ul{padding-left:20px;margin:6px 0}.book i{color:var(--mut)}.book code{background:#0b1524;border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:12.5px}.book p{color:#c6d2e8}
.more{display:block;width:100%;background:var(--card2);color:var(--brass2);border:1px solid var(--line);border-radius:10px;padding:10px;font:600 14px system-ui;cursor:pointer}
.hide{display:none}
@media(max-width:560px){.tiles{grid-template-columns:repeat(2,1fr)}.row2{grid-template-columns:1fr 1fr}.kv{grid-template-columns:100px 1fr}}
</style></head><body><div class="wrap">
<header><h1><b>DPA</b> Data Book</h1><div class="asof" id="asof"></div></header>
<nav><button data-t="data" class="on">Data book</button><button data-t="rules">Rule book</button><button data-t="process">Process book</button></nav>
<section id="t-data">
 <div class="tiles" id="tiles"></div>
 <input type="search" id="q" placeholder="Search a vessel, cargo or agent">
 <div class="row2"><select id="fb"></select><select id="fp"></select><select id="fc"></select></div>
 <div class="chips" id="chips"></div><div class="count" id="count"></div><div id="list"></div><button class="more hide" id="more">Show more</button>
 <h2>Days alongside by cargo · vessels that have sailed (a shift counts as one stay)</h2><table id="tc"></table>
 <h2>Calls by berth · days per call at that berth</h2><table id="tb"></table>
</section>
<section id="t-rules" class="hide"><div class="book">__RULES__</div><h2>Circulars and trade notices on record</h2><div class="count" id="ccount"></div><div id="circ"></div></section>
<section id="t-process" class="hide"><div class="book">__PROCESS__</div></section>
</div>
<script>
const D=__DATA__;
const $=id=>document.getElementById(id),esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const dt=s=>s?(+s.slice(8,10))+' '+MON[+s.slice(5,7)-1]+' '+s.slice(11):'—', ms=s=>s?Date.parse(s.replace(' ','T')+':00Z'):null;
const days=(a,b)=>(a&&b)?(ms(b)-ms(a))/864e5:null, f1=x=>x==null?'—':x.toFixed(1), num=x=>x==null?'—':Number(x).toLocaleString('en-IN');
const grp=c=>{c=(c||'').toLowerCase();if(/log|timber/.test(c))return 'Timber logs';if(/salt/.test(c))return 'Salt';if(/coal|coke/.test(c))return 'Coal / coke';if(/urea|dap|mop|npk|tsp|fert|phosph|sulphur/.test(c))return 'Fertiliser';if(/pellet|iron ore/.test(c))return 'Iron ore / pellets';if(/bag|rice|sugar|flour/.test(c))return 'Bag cargo';if(/steel|project|windmill|blade|pipe|coil|beam/.test(c))return 'Steel / project';if(/clay|bentonite|gypsum|bauxite|barite|ore|mineral/.test(c))return 'Minerals';return 'Other';};
const PRI={GOV:'Government',COASTAL:'Coastal',HP:'Higher productivity',SAAGAR:'SAAGAR','24H':'24 hours','8K':'6.5K / 8K',STL:'Steel / Project',BIT:'Bitumen',GEN:'General',SPACE:'Space a/c',PPP:'PPP berth'};
const ours=r=>/mihir/i.test(r.agent||'');
const REC=[].concat(D.calls.map(c=>Object.assign({kind:'call',st:c.status,g:grp(c.cargo),stay:c.status==='sailed'?days(c.madeFast,c.out):null,key:c.madeFast},c)),
  D.waiting.map(w=>Object.assign({kind:'wait',st:w.status,g:grp(w.cargo),berth:'',priority:'',key:w.reported||'9999'},w)));
REC.sort((a,z)=>{const o={alongside:0,coming:1,waiting:2,expected:3,sailed:4};return (o[a.st]-o[z.st])||(a.st==='sailed'?(z.key>a.key?1:-1):(a.key>z.key?1:-1));});
$('asof').textContent='The data starts at the end of October 2026 (earliest berthing on record 25 Oct; CJ-9 from 28 Oct) — nothing earlier is on record · as of '+dt(D.asOf);
const cnt=s=>REC.filter(r=>r.st===s).length;
$('tiles').innerHTML=[[D.calls.length,'berth calls on record'],[cnt('alongside'),'alongside now'],[cnt('waiting'),'waiting'],[cnt('expected'),'expected']].map(t=>'<div class="tile"><b>'+t[0]+'</b><span>'+t[1]+'</span></div>').join('');
const opt=(id,label,vals,nm)=>{$(id).innerHTML='<option value="">'+label+'</option>'+vals.map(v=>'<option value="'+esc(v)+'">'+esc(nm?nm(v):v)+'</option>').join('');};
const bo=['1','2','3','4','5','6','7','8','9','13','14','15','15A','16'];
opt('fb','All berths',bo.filter(b=>D.calls.some(c=>c.berth===b)),v=>'CJ-'+v);
opt('fp','All priorities',Object.keys(PRI).filter(k=>D.calls.some(c=>c.priority===k)),v=>PRI[v]);
opt('fc','All cargo',[...new Set(REC.map(r=>r.g))].sort());
let F='all',LIM=40;
const CH=[['all','All'],['alongside','Alongside'],['waiting','Waiting'],['expected','Expected'],['sailed','Sailed'],['ours','Mihir & Co']];
function chips(){$('chips').innerHTML=CH.map(c=>'<span class="chip'+(F===c[0]?' on':'')+'" data-f="'+c[0]+'">'+c[1]+'</span>').join('');}
const rk=r=>Object.keys(r.ranks||{}).filter(k=>r.ranks[k]<90&&Number.isInteger(r.ranks[k])).map(k=>(PRI[k]||k)+' '+r.ranks[k]).join(' · ');
function line(r){
 if(r.kind==='call'){const a='CJ-'+r.berth+(r.priority?' · '+(PRI[r.priority]||r.priority):'');
  if(r.st==='sailed')return a+' · '+dt(r.madeFast)+' → '+dt(r.out)+' · '+f1(r.stay)+' d';
  if(r.st==='alongside')return a+' · since '+dt(r.madeFast)+' · out about '+dt(r.out);
  return a+' · coming '+dt(r.madeFast);}
 const p=r.projection?' · board: CJ-'+r.projection.berth+' about '+dt(r.projection.at):'';
 return r.st==='expected'?'ETA '+dt(r.reported)+p:'waiting since '+dt(r.reported)+(rk(r)?' · '+rk(r):'')+p;}
function detail(r){const kv=[];const add=(k,v)=>{if(v!==''&&v!=null&&v!=='—')kv.push('<span>'+k+'</span><div>'+esc(v)+'</div>');};
 add('Cargo',r.cargo+(r.qty?' · '+num(r.qty)+' '+(r.unit||''):''));add('Import / export',r.ie);add('Agent',r.agent);add('Length',r.loa?r.loa+' m':'');add('Draught',r.draught?r.draught+' m':'');add('Gear',r.gear);
 if(r.kind==='call'){add('Berth','CJ-'+r.berth+(r.panels?' · panels '+r.panels.join(' – '):''));add('Priority',(PRI[r.priority]||r.priority)+(r.via?' · '+r.via:''));add('Norm',r.norm?num(r.norm)+' a day':'');add('Made fast',dt(r.madeFast));add(r.st==='sailed'?'Left the berth':'Out (estimate)',dt(r.out));add('List ETC',r.listETC?dt(r.listETC):'');add('Stay',r.stay!=null?f1(r.stay)+' days':'');}
 else{add('Reported',dt(r.reported));add('Ready',r.ready?dt(r.ready):'not declared');add('Ranks',rk(r));add('Berths she can use',(r.berthsAllowed||[]).map(b=>'CJ-'+b).join(', '));if(r.projection)add('Board projection','CJ-'+r.projection.berth+' · '+dt(r.projection.at)+' · by '+(PRI[r.projection.by]||r.projection.by));}
 return '<div class="kv">'+kv.join('')+'</div>'+(r.note?'<div class="note">'+esc(r.note)+'</div>':'');}
function draw(){const q=$('q').value.trim().toLowerCase(),b=$('fb').value,p=$('fp').value,c=$('fc').value;
 const L=REC.filter(r=>(F==='all'||(F==='ours'?ours(r):r.st===F))&&(!b||r.berth===b)&&(!p||r.priority===p||(r.ranks&&r.ranks[p]<90))&&(!c||r.g===c)&&(!q||(r.vessel+' '+r.cargo+' '+r.agent).toLowerCase().includes(q)));
 $('count').textContent=L.length+' record'+(L.length===1?'':'s');
 $('list').innerHTML=L.slice(0,LIM).map((r,i)=>'<div class="v'+(ours(r)?' ours':'')+'" data-i="'+REC.indexOf(r)+'"><div class="vt"><span class="vn">'+esc(r.vessel)+'</span><span class="tag t-'+r.st+'">'+r.st.toUpperCase()+'</span></div><div class="vs">'+esc(r.cargo)+(r.qty?' · '+num(r.qty)+' '+(r.unit||''):'')+'</div><div class="vs">'+esc(line(r))+'</div><div class="vd"></div></div>').join('')||'<div class="count">Nothing matches.</div>';
 $('more').classList.toggle('hide',L.length<=LIM);}
$('list').addEventListener('click',e=>{const v=e.target.closest('.v');if(!v)return;const d=v.querySelector('.vd');if(!d.innerHTML)d.innerHTML=detail(REC[+v.dataset.i]);v.classList.toggle('open');});
$('chips').addEventListener('click',e=>{const c=e.target.closest('.chip');if(!c)return;F=c.dataset.f;LIM=40;chips();draw();});
['q','fb','fp','fc'].forEach(id=>$(id).addEventListener('input',()=>{LIM=40;draw();}));
$('more').addEventListener('click',()=>{LIM+=60;draw();});
document.querySelector('nav').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x===b));['data','rules','process'].forEach(t=>$('t-'+t).classList.toggle('hide',t!==b.dataset.t));window.scrollTo(0,0);});
const sailed=REC.filter(r=>r.kind==='call'&&r.st==='sailed'&&r.stay>0.2&&r.priority!=='SPACE');
// one VISIT = a vessel's calls joined across a shift (next berth within 8 hours of leaving the last one)
const VIS=[];{const by={};D.calls.filter(c=>c.priority!=='SPACE').forEach(c=>{(by[c.vessel]=by[c.vessel]||[]).push(c);});Object.values(by).forEach(a=>{a.sort((x,y)=>x.madeFast>y.madeFast?1:-1);let cur=null;a.forEach(c=>{if(cur&&days(cur.out,c.madeFast)<8/24){cur.out=c.out;cur.st=c.status;}else{cur={g:grp(c.cargo),f:c.madeFast,out:c.out,st:c.status};VIS.push(cur);}});});}
const G={};VIS.filter(v=>v.st==='sailed').forEach(v=>{const d=days(v.f,v.out);if(d>0.2)(G[v.g]=G[v.g]||[]).push(d);});
$('tc').innerHTML='<tr><th>Cargo</th><th>Vessels</th><th>Average days</th><th>Shortest</th><th>Longest</th></tr>'+Object.keys(G).sort((a,z)=>G[z].length-G[a].length).map(k=>{const a=G[k];return '<tr><td>'+k+'</td><td>'+a.length+'</td><td>'+f1(a.reduce((s,x)=>s+x,0)/a.length)+'</td><td>'+f1(Math.min(...a))+'</td><td>'+f1(Math.max(...a))+'</td></tr>';}).join('');
$('tb').innerHTML='<tr><th>Berth</th><th>Calls</th><th>Average days</th><th>Now</th></tr>'+bo.filter(b=>D.calls.some(c=>c.berth===b)).map(b=>{const a=sailed.filter(r=>r.berth===b).map(r=>r.stay),n=D.calls.filter(c=>c.berth===b),now=n.find(c=>c.status==='alongside');return '<tr><td>CJ-'+b+'</td><td>'+n.length+'</td><td>'+(a.length?f1(a.reduce((s,x)=>s+x,0)/a.length):'—')+'</td><td>'+(now?esc(now.vessel):'—')+'</td></tr>';}).join('');
// circulars — newest first; in force before the rest
{const C=(D.circ||[]).slice().sort((a,z)=>((a.st==='in force'?0:1)-(z.st==='in force'?0:1))||(z.iso>a.iso?1:-1));
 $('ccount').textContent=C.length+' on record · '+C.filter(c=>c.st==='in force').length+' in force · tap one for the gist and the PDF';
 $('circ').innerHTML=C.map(c=>'<div class="v"><div class="vt"><span class="vn">'+esc(c.t)+'</span><span class="tag '+(c.st==='in force'?'t-alongside':'t-sailed')+'">'+esc((c.st||'').toUpperCase())+'</span></div><div class="vs">'+esc(c.kind||'')+' · dated '+esc(c.rd||'')+'</div><div class="vd"><div class="kv"><span>Reference</span><div>'+esc(c.ref||'')+'</div><span>Received</span><div>'+esc(c.d||'')+' · '+esc(c.src||'')+'</div></div><div class="note"><b>What it says:</b> '+esc(c.s||'')+'</div>'+(c.eff?'<div class="note"><b>Bearing on berthing:</b> '+esc(c.eff)+'</div>':'')+(c.file?'<div class="note"><a href="'+esc(c.file)+'" target="_blank" rel="noopener" style="color:var(--brass2)">Open the PDF'+(c.pg?' · '+c.pg+' page'+(c.pg>1?'s':''):'')+'</a></div>':'')+'</div></div>').join('');
 $('circ').addEventListener('click',e=>{if(e.target.closest('a'))return;const v=e.target.closest('.v');if(v)v.classList.toggle('open');});}
chips();draw();
</script></body></html>'''
page = PAGE.replace('__RULES__', md(os.path.join(R, 'book', 'RULE_BOOK.md'))).replace('__PROCESS__', md(os.path.join(R, 'book', 'PROCESS_BOOK.md'))).replace('__DATA__', blob)
open(out, 'w', encoding='utf-8').write(page); print(out, len(page) // 1024, 'KB')
