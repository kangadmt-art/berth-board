#!/usr/bin/env python3
# apply72 — v276 — Mihir, 25 Nov 23:48: "board mein 16 number par koi non clean cargo vessel lage woh dikhna chahiye us page par aur uska data bhi wahi hove ke kitne vessel hue".
# New section on the Cargo page: "CJ-16 · non-clean cargo" — every coal / coke / iron ore / pellet vessel at CJ-16 (the cargoes Trade Notice 3089 of 15.11.2026 let in),
# the count so far, the MT and the berth time they took, and what is programmed or expected next. Record = const CJ16_LOG (every completed call at CJ-16 since 28 Oct,
# from the data book); a vessel still in V at CJ-16 and the board's projection are read live. tools/trim_board.js appends a CJ-16 vessel to CJ16_LOG before it drops her from V.
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
STAMP = sys.argv[1]
D = json.load(open('/home/claude/berth-board/db/databook.json'))
rows = []
for c in D['calls']:
    if str(c['berth']) != '16' or c['status'] != 'sailed': continue
    f = c['madeFast'][5:]; o = c['out'][5:]
    g = (c.get('gear') or '').lower()
    rows.append((c['madeFast'], " {n:'%s',c:'%s',q:%s,u:'%s',ie:'%s',ag:'%s',cat:'%s',qt:%s,loa:%s,g:'%s',f:'%s',o:'%s'%s}" % (
        q(re.sub(r' \(.*$', '', c['vessel'])), q(c['cargo']), c['qty'], c['unit'], c.get('ie') or '', q(c.get('agent') or ''), c.get('priority') or '', c['norm'] if c.get('norm') else 'null',
        c['loa'] if c.get('loa') else 'null', 'gearless' if g.startswith('gearless') else 'geared' if g.startswith('geared') else '', f, o, ',est:1' if c.get('outIsEstimate') else '')))
rows.sort()
print(len(rows), 'completed calls at CJ-16 on record')
LOG = ("const CJ16_LOG=[ // every completed call at CJ-16 on the board's record, oldest first (from the data book, 25 Nov) — tools/trim_board.js appends a vessel here before it drops her from V. "
       "qt = the MT-a-day she was berthed on (quote or norm). Read by c16() — the CJ-16 non-clean cargo section (Mihir, 25 Nov 23:48).\n" + ",\n".join(r for _, r in rows) + "\n];\n"
       "const NC16=c=>/coal|coke|iron|pellet|\\bore\\b|fines/i.test(c||'')&&!/mill ?scale/i.test(c||''); // \"non-clean\" at CJ-16 = the cargoes Trade Notice 3089 (15.11.2026) let in: coal, coke (petcoke too), iron ore fines, pellets. Aggregates are NOT counted — they lay at CJ-16 before the notice as well (Alasia, 1 Nov).\n"
       "const NC16_FAM=c=>/coal/i.test(c)?'Coal':/coke/i.test(c)?'Coke':/pellet/i.test(c)?'Pellets':'Iron ore';\n")
B.rep("const HP_LOG=[ //", LOG + "const HP_LOG=[ //")

# ---- the section (after "Kab berth milega?", before the meeting preview)
B.rep("  <section class=\"card\" data-sec=\"mpt\" aria-labelledby=\"mp\">",
      "  <section class=\"card\" data-sec=\"c16\" aria-labelledby=\"c16h\">\n"
      "    <div class=\"sechead\"><h2 id=\"c16h\">CJ-16 · non-clean cargo</h2><p id=\"c16sub\"></p></div>\n"
      "    <div class=\"stats\" id=\"c16stats\" style=\"grid-template-columns:repeat(auto-fit,minmax(150px,1fr))\"></div>\n"
      "    <div id=\"c16tbl\"></div>\n"
      "    <details class=\"tdfull\"><summary>Every vessel at CJ-16 since 28 Oct — clean and non-clean</summary><div id=\"c16all\"></div></details>\n"
      "  </section>\n"
      "  <section class=\"card\" data-sec=\"mpt\" aria-labelledby=\"mp\">")
B.rep("const SEC_OPEN_DEFAULT=new Set(['finder','mine','hpb']);", "const SEC_OPEN_DEFAULT=new Set(['finder','mine','hpb','c16']);")

FN = r"""
// ---- CJ-16 · non-clean cargo (Mihir, 25 Nov 23:48): every coal / coke / iron ore / pellet vessel at CJ-16, how many so far, and the berth time they took
function c16(){
  const sub=document.getElementById('c16sub'),st=document.getElementById('c16stats'),tb=document.getElementById('c16tbl'),al=document.getElementById('c16all'); if(!tb)return;
  const base=n=>n.replace(/ \(.*$/,''),K=x=>x?(x>=1000?(Math.round(x/100)/10+'K').replace('.0K','K'):x):'—';
  const tbl=(th,rows)=>`<div class="sdwrap"><table class="sdt"><tr>${th.map((x,i)=>`<th${(i===0||i===th.length-1)?' class="l"':''}>${x}</th>`).join('')}</tr>${rows.join('')}</table></div>`;
  const rows=CJ16_LOG.map(r=>({n:r.n,c:r.c,q:r.q,u:r.u||'MT',ie:r.ie,ag:r.ag,cat:r.cat,qt:r.qt,loa:r.loa,g:r.g,F:h(r.f),T:h(r.o),est:!!r.est,st:'sailed'}));
  const seen=r=>rows.some(x=>x.n===base(r.n)&&Math.abs(x.F-r.F)<24);
  V.filter(v=>v.b==='16'&&v.cat!=='SPACE').forEach(v=>{if(seen(v))return;const gr=gearOf(v.n);rows.push({n:base(v.n),full:v.n,c:v.c,q:v.q,u:v.u||'MT',ie:(typeof IE!=='undefined'&&IE[v.n])||'',ag:agOf(v.n),cat:v.slot||v.cat,via:v.via,qt:v.nm||null,loa:(typeof LOA!=='undefined'&&LOA[v.n])||null,g:gr?(gr.g==='GL'?'gearless':gr.g==='G'?'geared':gr.g==='M'?'may be gearless':''):'',F:v.F,T:v.T,est:!!v.est,st:v.T<=NOW?'sailed':v.F<=NOW?'alongside':'programmed'});});
  (typeof S!=='undefined'?S:[]).filter(s=>s.b==='16').forEach(s=>{const w=s.w||{};rows.push({n:base(s.n),full:s.n,c:s.c||w.c,q:s.q||w.q,u:s.u||w.u||'MT',ie:(typeof IE!=='undefined'&&IE[s.n])||'',ag:agOf(s.n),cat:s.cat,via:s.via,qt:null,loa:w.loa||null,g:(gr=>gr?(gr.g==='GL'?'gearless':gr.g==='G'?'geared':gr.g==='M'?'may be gearless':''):'')(gearOf(s.n)),F:s.F,T:s.T,est:true,st:'expected'});});
  rows.sort((a,z)=>a.F-z.F);
  const nc=rows.filter(r=>NC16(r.c)), been=nc.filter(r=>r.st==='sailed'||r.st==='alongside'), next=nc.filter(r=>r.st==='programmed'||r.st==='expected');
  const hrs=r=>Math.max(0,Math.min(r.T,NOW)-r.F), d1=x=>(x/24).toFixed(1);
  const first=nc.length?nc[0].F:null, span=first!=null?Math.max(1,NOW-first):0, used=been.reduce((a,r)=>a+hrs(r),0), mt=been.reduce((a,r)=>a+(r.u==='MT'?r.q:0),0);
  const since=first!=null?rows.filter(r=>r.F>=first&&r.F<=NOW):[];
  const famOf=r=>NC16(r.c)?'non-clean':/salt/i.test(r.c)?'salt':/blade|windmill|project|steel/i.test(r.c)?'project / steel':/rice|sugar|wheat|bag/i.test(r.c)?'food cargo':/aggregate/i.test(r.c)?'aggregates':'other';
  const mix={};since.forEach(r=>{mix[famOf(r)]=(mix[famOf(r)]||0)+1;});
  const stTxt=r=>r.st==='sailed'?'sailed':r.st==='alongside'?'<b style="color:var(--warn)">at berth now</b>':r.st==='programmed'?'<b style="color:var(--gold)">on the programme</b>':'<span style="color:var(--muted)">board expects</span>';
  const under=r=>(CL[r.cat]||r.cat||'—')+(r.qt&&/^(HP|24H|GOV|COASTAL)$/.test(r.cat||'')?' · '+K(r.qt):'')+(r.via&&/30k\/25k/i.test(r.via)?' · quote':'');
  const tile=(c,v,l)=>`<div class="stat" style="--sc:${c};cursor:default"><div class="v" style="font-size:26px">${v}</div><div class="l">${l}</div></div>`;
  if(sub)sub.innerHTML=`Coal, coke, iron ore and pellet vessels berthed at CJ-16 — cargoes kept off the clean berths until this month (pellets let in from 11 Nov; Trade Notice 3089 of 15 Nov: coal, coke, iron ore fines and pellets at CJ-16). `+
    (nc.length?`<b>${been.length} vessel${been.length===1?'':'s'} so far</b>${first!=null?' · the first on '+fmt(first).replace(/ \d\d:\d\d$/,''):''}${next.length?` · <b>${next.length} more</b> ${next.some(r=>r.st==='programmed')?'programmed / expected':'expected by the board'}`:''}.`:'None on the board\'s record yet.')+
    ` <span style="color:var(--muted)">Aggregates are not counted — they lay at CJ-16 before the notice too.</span>`;
  if(st)st.innerHTML=nc.length?[
    tile('var(--warn)',been.length,`<b>non-clean vessels so far</b> · ${Object.entries(been.reduce((a,r)=>{const k=NC16_FAM(r.c);a[k]=(a[k]||0)+1;return a;},{})).map(([k,n])=>n+' '+k.toLowerCase()).join(' · ')||'—'}`),
    tile('var(--gold)',next.length,`<b>coming</b> · ${next.length?next.map(r=>r.n+' ~'+fmt(r.F).replace(/ \d\d:\d\d$/,'')).join(' · '):'none in sight'}`),
    tile('var(--dry)',nf.format(Math.round(mt)),'<b>MT</b> of non-clean cargo over CJ-16 so far'),
    tile('var(--brk)',d1(used),`<b>berth-days</b> taken · ${Math.round(used/span*100)} % of CJ-16's time since ${first!=null?fmt(first).replace(/ \d\d:\d\d$/,''):'—'}`),
    tile('var(--tmb,var(--brass))',since.length,`<b>vessels at CJ-16</b> since then · ${Object.entries(mix).sort((a,z)=>z[1]-a[1]).map(([k,n])=>n+' '+k).join(' · ')}`)].join(''):'';
  const TH=['Vessel','Cargo','MT','I / E','Berthed under','Made fast','Left','Days at berth','LOA · gear','Status','Agent · stevedore'];
  const tr=(r,mark)=>`<tr${isMine(r.full||r.n)?' class="our"':''}${mark&&NC16(r.c)?' style="background:rgba(var(--ov-rgb),.06)"':''}><td class="l"><b>${r.n}</b>${mark&&NC16(r.c)?' <span class="chip" style="margin-left:4px;color:var(--warn);border-color:var(--warn)">non-clean</span>':''}</td><td class="l">${r.c}</td><td>${nf.format(Math.round(r.q))}${r.u!=='MT'?' '+r.u:''}</td><td>${r.ie||'—'}</td><td class="l">${under(r)}</td>`+
    `<td class="l">${(r.st==='programmed'||r.st==='expected')?'~'+fmt(r.F)+' est':fmt(r.F)}</td><td class="l">${r.st==='sailed'&&!r.est?fmt(r.T):'~'+fmt(r.T)+' est'}</td><td>${r.st==='sailed'?d1(r.T-r.F):r.st==='alongside'?d1(NOW-r.F)+' so far':'~'+d1(r.T-r.F)}</td><td class="l">${r.loa?Math.round(r.loa)+' m':'—'}${r.g?' · '+r.g:''}</td><td class="l">${stTxt(r)}</td><td class="l">${r.ag||'—'}${stvS(r.full||r.n,r.F,r.T)}</td></tr>`;
  tb.innerHTML=nc.length?tbl(TH,nc.slice().reverse().map(r=>tr(r,false))):'<div class="empty">No coal, coke, iron ore or pellet vessel has been berthed at CJ-16 on the board\'s record.</div>';
  if(al)al.innerHTML=tbl(TH,rows.slice().reverse().map(r=>tr(r,true)))+`<p style="font-size:12px;color:var(--muted);margin:2px 2px 8px">${rows.filter(r=>r.st==='sailed').length} completed calls on record since ${fmt(rows[0].F).replace(/ \d\d:\d\d$/,'')}. "Board expects" rows are the board's own projection, not a programme.</p>`;
}
"""
B.rep("function hpRecs(){", FN.strip("\n") + "\nfunction hpRecs(){")
B.rep("preview();hpbid();meetBoard();", "preview();hpbid();c16();meetBoard();")
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='" + STAMP + "';", B.s, count=1)
B.save(); print('saved 72')
