# v252 — HP bid panel (Mihir, 22 Nov 00:07: "HP mein bidding hoti hai … jo vessel bidding ke liye ho woh dikhne chahiye")
# The HP berth is decided by a bid at the meeting, so the board shows WHO IS IN THE BID and the quotes that won so far,
# instead of naming one vessel. No change to the engine / projection.
import sys
p=sys.argv[1]
s=open(p,encoding='utf-8').read()
def rep1(a,b):
    global s
    assert s.count(a)==1,(a[:70],s.count(a)); s=s.replace(a,b)

# 1. record of past HP berths (from the data book); trim_board.js appends to it
hplog=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'2026-11-22_hp_log_rows.txt'),encoding='utf-8').read()
rep1("const SALT_DONE=[\n","const HP_LOG=[ // every berth given under HP since 28 Oct with the quote the programme printed (from the data book, 22 Nov) — trim_board.js appends an HP vessel here before it drops her from V. x:1 = quantity not worked at this berth alone (shift / top-up), no rate shown\n"+hplog+"\n];\nconst SALT_DONE=[\n")

# 2. section in the cargo tab, right after the meeting preview
sec='''  <section class="card" data-sec="hpb" aria-labelledby="hpbh">
    <div class="sechead"><h2 id="hpbh">HP berth · who is in the bid</h2><p id="hpbsub"></p></div>
    <div id="hpbpool"></div>
    <div class="sdh">Quotes that won an HP berth so far</div>
    <p id="hpbsum" style="font-size:12.5px;line-height:1.7;margin:8px 2px 10px"></p>
    <details class="tdfull"><summary>Every HP berth given so far — quote, stay, and what was done against the quote</summary><div id="hpblog"></div></details>
  </section>
'''
rep1('  <section class="card" data-sec="spt" aria-labelledby="sp">',sec+'  <section class="card" data-sec="spt" aria-labelledby="sp">')

# 3. renderer
fn=r'''// ---- HP bid (Mihir, 22 Nov 00:07). HP is a bid at the meeting — 40,000 to 50,000 MT a day, the highest bid takes the berth, at 50,000 each the senior one.
// The board cannot see the bids, so it names no winner: it shows who bids at which meeting (the meeting that programmes the first berth she can use),
// by list seniority, and the quotes that won so far (the programme prints the winner's quote).
const hpFam=c=>/salt/i.test(c)?'Salt':/coal|coke/i.test(c)?'Coal / coke':/aggregate/i.test(c)?'Aggregates':/pellet|iron|\bore\b|fines/i.test(c)?'Ore / pellets':/clay|feldspar/i.test(c)?'Clay':/gypsum/i.test(c)?'Gypsum':'Other';
function hpRecs(){
  const base=n=>n.replace(/ \(.*$/,'');
  const rec=HP_LOG.map(r=>({n:r.n,b:r.b,c:r.c,q:r.q,ag:r.ag,qt:r.qt,F:h(r.f),T:h(r.o),est:!!r.est,x:!!r.x}));
  const byN={};V.filter(v=>v.cat==='HP'&&!v.slot&&!v.via&&v.nm).forEach(v=>{const n=base(v.n);const a=byN[n];if(!a)byN[n]={n,b:v.b,c:v.c,q:v.q,ag:agOf(v.n)!=='—'?agOf(v.n):agOf(n),qt:v.nm,F:v.F,T:v.T,est:!!v.est||v.T>NOW,x:false};else{a.F=Math.min(a.F,v.F);if(v.T>a.T){a.T=v.T;a.est=!!v.est||v.T>NOW;}}});
  Object.values(byN).forEach(v=>{if(!rec.some(r=>r.n===v.n&&Math.abs(r.F-v.F)<1))rec.push(v);});
  return rec.sort((a,z)=>z.F-a.F);
}
function hpbid(){
  const el=document.getElementById('hpbpool'); if(!el)return;
  const sub=document.getElementById('hpbsub'), lg=document.getElementById('hpblog'), sm=document.getElementById('hpbsum');
  const rec=hpRecs(), K=x=>(Math.round(x/100)/10)+'K', base=n=>n.replace(/ \(.*$/,''), dd=x=>{const d=dt(x);return d.getUTCDate()+' '+MON[d.getUTCMonth()];};
  const tbl=(th,rows)=>`<div class="sdwrap"><table class="sdt"><tr>${th.map((x,i)=>`<th${(i===0||i===th.length-1)?' class="l"':''}>${x}</th>`).join('')}</tr>${rows.join('')}</table></div>`;
  // the HP places now — a General or Project vessel standing in a vacant HP place does not block an HP vessel (12 Nov, 14 Nov)
  const live={};V.filter(v=>v.cat==='HP'&&!v.slot&&!v.via&&v.T>NOW).forEach(v=>{const n=base(v.n);if(!live[n]||v.T>live[n].T)live[n]=v;});
  const use=Object.values(live).sort((a,z)=>a.T-z.T), MAXHP=2, vac=Math.max(0,MAXHP-use.length);
  const guest=V.filter(v=>v.slot==='HP'&&v.cat!=='HP'&&v.T>NOW);
  const M=NXM;
  // when a berth is next clear: after the last vessel alongside or programmed there — and after any vessel lying across into it (Flag Marina, 254 m, lies over CJ-7 and CJ-8)
  const firstFree=b=>{const B=BERTHS.find(x=>x.id===b);if(!B)return null;const bl=V.filter(v=>v.cat!=='SPACE'&&v.T>NOW&&(v.b===b||(v.p&&Math.min(v.p[1],B.p[1])-Math.max(v.p[0],B.p[0])>2.5)));return bl.length?Math.max(...bl.map(v=>v.T)):NOW;};
  // the meeting of day D (11:00) programmes D 18:00 → D+1 18:00
  const winMeet=t=>{const d=dt(t);const hod=d.getUTCHours()+d.getUTCMinutes()/60;const day0=t-hod;return hod>=18?day0+11:day0-24+11;};
  const cand=W.filter(w=>w.rk&&w.rk.HP).map(w=>{
    const rank=w.rk.HP<98?w.rk.HP:null, two=(w.loa||0)>235, al=allowedBerths(w).filter(b=>{const B=BERTHS.find(x=>x.id===b);return !(B&&B.dr&&w.dr&&w.dr-(B.dr+(B.tide||0))>1);}) /* a berth more than 1 m short of her draft, tide allowance counted, is left out: petcoke at 13.3 m is not for CJ-5 (10.5 m); Lila Tokyo at 14.04 m still counts for CJ-7 / 8 (12 + 1.5 m, after lighterage) */, exp=(typeof ETA!=='undefined')&&!!ETA[w.n];
    const last=rec.find(r=>hpFam(r.c)===hpFam(w.c)), pj=S.find(x=>x.n===w.n&&x.proj);
    let opt=null, mt=null;
    if(w.rdy!=null){al.map(b=>({b,t:firstFree(b)})).filter(o=>o.t!=null).forEach(o=>{const go=Math.max(o.t,w.rdy);if(!opt||go<opt.go)opt={b:o.b,t:o.t,go};});
      if(opt){mt=Math.max(M,winMeet(opt.go));for(let k=0;k<3&&w.rep!=null&&w.rep>mt&&w.rep>firstHW(mt);k++)mt+=24;}}
    return {w,rank,two,al,exp,last,pj,opt,mt,st:w.rdy==null?3:opt?0:2};
  }).sort((a,z)=>a.st-z.st||((a.mt||1e9)-(z.mt||1e9))||((a.rank||99)-(z.rank||99))||((a.w.rdy||1e9)-(z.w.rdy||1e9)));
  const stTxt=c=>{const w=c.w;const t=[c.st===0?`<b class="des">${fday(c.mt)} meeting</b> · CJ-${c.opt.b} frees ~${fmt(c.opt.t)}`:c.st===2?'<span style="color:var(--muted)">ready, no berth of hers in sight</span>':'<span style="color:var(--muted)">not ready</span>'];
    if(c.st===0&&c.exp)t.push('if she arrives on her ETA');if(c.two)t.push('two berths ('+Math.round(w.loa)+' m)');if(w.noHP)t.push('passed over before');return t.join(' · ');};
  const grp={};cand.filter(c=>c.st===0).forEach(c=>{(grp[c.mt]=grp[c.mt]||[]).push(c);});const mts=Object.keys(grp).map(Number).sort((a,z)=>a-z);
  if(sub)sub.innerHTML=`HP is a <b>bid at the meeting</b> — 40,000 to 50,000 MT a day. The highest bid takes the berth; at 50,000 each, the senior vessel takes it. The board cannot see the bids, so it names no winner: it shows who bids at which meeting.`;
  const places=`<p style="font-size:13px;line-height:1.7;margin:4px 2px 8px"><b>HP places: ${MAXHP}</b> · ${use.length?use.map(v=>`CJ-${v.b} ${base(v.n)} (${K(v.nm)}) till ~${fmt(v.T)}${v.est?' est':''}`).join(' · '):'none in use'}${vac?` · <b style="color:var(--ok)">${vac} open</b>`:''}`+
    mts.slice(0,3).map(m=>{const g=grp[m], byB={};g.forEach(c=>{(byB[c.opt.b]=byB[c.opt.b]||[]).push(c);});const sen=g.filter(c=>c.rank)[0];
      return `<br><b>${fday(m)} meeting</b> · ${g.length} in the bid — ${Object.keys(byB).map(b=>`CJ-${b}: ${byB[b].map(c=>`${c.w.n} (${c.rank?'HP '+c.rank:'Y'})`).join(', ')}`).join(' · ')}${sen&&g.length>1?` · at 50,000 each the senior takes it: <b>${sen.w.n}</b>`:''}`;}).join('')+
    (mts.length&&mts[0]>M+0.01?`<br><span style="color:var(--muted)">${fday(M)} meeting: no berth comes free for an HP vessel in its window — no HP bid expected.</span>`:'')+
    (guest.length?`<br><span style="color:var(--muted)">${guest.map(v=>`CJ-${v.b} ${base(v.n)} (project) stands in a vacant HP place and does not block an HP vessel`).join(' · ')}.</span>`:'')+`</p>`;
  el.innerHTML=places+(cand.length?tbl(['HP no.','Vessel','Bids at','Last HP quote · same cargo','Cargo','MT','Ready / ETA','Agent','Berths she can use','Board expects her at'],cand.map(c=>{const w=c.w;
    return `<tr${isMine(w.n)?' class="our"':''}><td class="l"><b title="${c.rank?'her HP seniority on the list':'the list prints Y: listed for HP, not numbered yet'}">${c.rank?'HP '+c.rank:'HP Y'}</b></td><td class="l"><b>${w.n}</b>${isMine(w.n)?' <span class="tag">Mihir &amp; Co</span>':''}</td><td class="l">${stTxt(c)}</td><td class="l">${c.last?'<b>'+K(c.last.qt)+'</b> · '+dd(c.last.F)+' · '+c.last.n:'none on record'}</td><td class="l">${w.c}</td><td>${nf.format(Math.round(w.q))}</td><td class="l">${w.rdy==null?'N/A':fmt(w.rdy)}</td><td class="l">${agOf(w.n)}</td><td class="l">${c.al.length?'CJ-'+c.al.join(' · '):'—'}</td><td class="l">${c.pj?`CJ-${c.pj.b} · ${fmt(c.pj.F)} · ${CL[c.pj.cat]||c.pj.cat}${c.pj.via?' as '+c.pj.via:''}`:'—'}</td></tr>`;}))
    +`<p style="font-size:12.5px;color:var(--muted);margin:2px 2px 8px">"Bids at" = the meeting that programmes the first berth she can use once it is clear (sailing times marked est are the board's estimate). A vessel that runs past her quoted time is taken off the berth.</p>`
    :'<p style="font-size:12.5px;color:var(--muted)">No vessel on the list carries an HP rank.</p>');
  // quotes that won so far, cargo-wise, oldest → newest
  const fam={};rec.slice().reverse().forEach(r=>{(fam[hpFam(r.c)]=fam[hpFam(r.c)]||[]).push(r);});
  if(sm)sm.innerHTML=Object.keys(fam).sort((a,z)=>fam[z].length-fam[a].length).map(k=>`<b>${k}</b> · ${fam[k].map(r=>K(r.qt)).join(' → ')} <span style="color:var(--muted)">(latest ${dd(fam[k][fam[k].length-1].F)})</span>`).join('<br>')+`<br><span style="color:var(--muted)">${rec.length} HP berths on record since ${dd(rec[rec.length-1].F)} · 40K means nobody bid against her.</span>`;
  if(lg)lg.innerHTML=tbl(['Vessel','Quote','Cargo','MT','Berth','Berthed','Sailed','Days at berth','MT a day over the whole stay','Whole stay vs quote','Agent'],rec.map(r=>{const days=(r.T-r.F)/24, live=r.est, rate=(!r.x&&!live&&days>0)?r.q/days:null;
    return `<tr${/mihir/i.test(r.ag||'')?' class="our"':''}><td class="l"><b>${r.n}</b></td><td><b>${K(r.qt)}</b></td><td class="l">${r.c}</td><td>${nf.format(Math.round(r.q))}</td><td>CJ-${r.b}</td><td class="l">${fmt(r.F)}</td><td class="l">${live?'~'+fmt(r.T)+' est':fmt(r.T)}</td><td>${live?'at berth':days.toFixed(1)}</td><td>${rate?nf.format(Math.round(rate)):(r.x?'shift / top-up':'—')}</td><td>${rate?Math.round(rate/r.qt*100)+' %':'—'}</td><td class="l">${r.ag||'—'}</td></tr>`;}))+'<p style="font-size:12px;color:var(--muted);margin:2px 2px 8px">Whole stay vs quote = cargo ÷ days from made fast to sailing, against the quote. The stay counts the hours before commencement and the wait for the tide after completion, so it reads lower than the working rate — a vessel can meet her quote and still show 80 %.</p>';
}
'''
rep1("function preview(){\n",fn+"function preview(){\n")
rep1("tideLine();preview();","tideLine();preview();hpbid();")

# 4. meeting preview: an HP pick is only the board's guess of the bid
rep1("""<td class="pk"><b>${x.n}</b>${isMine(x.n)?'<span class="tag">Mihir &amp; Co</span>':''}""","""<td class="pk"><b>${x.n}</b>${isMine(x.n)?'<span class="tag">Mihir &amp; Co</span>':''}${x.cat==='HP'&&!x.via?'<span class="tag" title="HP is decided by the bid at the meeting — see the HP bid table below">HP · decided by bid</span>':''}""")

# 5. the HP panel is open by default
rep1("const SEC_OPEN_DEFAULT=new Set(['finder','mine']);","const SEC_OPEN_DEFAULT=new Set(['finder','mine','hpb']);")
open(p,'w',encoding='utf-8').write(s)
print('patched',len(s))
