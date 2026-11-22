// ---- MEETING page (Mihir, 22 Nov 2026): the next berthing meeting, berth by berth. For every DPA berth: who is on it, CONTINUE or KHALI,
// which priority operates there and who has a chance — each vessel with her details (cargo, quantity, agent, ready since, length, list ranks).
// The chance names are the engine's own pick and its next in line (so berth fit, draught and seniority are already counted); a berth HP vessels
// can use shows the bid pool first. A berth the engine gives to nobody in this window is never shown as staying vacant (Mihir, 22 Nov 17:28) and
// never under a made-up priority (Mihir, 17:48: "port convenience" is not a priority): the count is run from the top of the order — the first line
// with a vacant place and a ready vessel that can use the berth is the priority, its vessels are the chance, and the shift that would let that
// line's senior vessel in is shown beside it.
let HPB_CAND=[]; // filled by hpbid(): every HP bidder with the meeting she bids at
const MB_PR={GOV:'Govt',COASTAL:'Coastal',HP:'HP · bid',SAAGAR:'SAAGAR','24H':'24 hrs','8K':'8K',STL:'Steel / Project',BIT:'Bitumen',GEN:'General'};
const MB_RK={GOV:'GOV',COASTAL:'CSTL',HP:'HP',SAAGAR:'SGR','24H':'24H','8K':'8K',STL:'STL',BIT:'BIT',GEN:'GEN'};
function meetBoard(){
  const el=document.getElementById('mtgb'); if(!el)return;
  const M=NXM, WE=M-11+24+18, base=n=>n.replace(/ \(.*$/,''), ex=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  const fa=x=>x.freeAt!=null?x.freeAt:x.prevAt, dd=x=>{const d=dt(x);return d.getUTCDate()+' '+MON[d.getUTCMonth()];};
  const lies=(v,B)=>v.b===B.id||(v.p&&Math.min(v.p[1],B.p[1])-Math.max(v.p[0],B.p[0])>2.5); // a vessel lying across into the berth blocks it too (Flag Marina, 254 m, over CJ-7 and CJ-8)
  const ready=w=>w.rdy!=null&&w.rdy<=M+0.01, canUse=(w,b)=>{try{return allowedBerths(w).includes(b);}catch(e){return false;}};
  const inWin=x=>x.proj&&!x.shifted&&x.prevAt!=null&&fa(x)<=WE+0.01, firmIn=x=>inWin(x)&&!x.softWait&&x.prevAt<WE-0.01; // firm = her place is open inside this meeting's window
  const placed={};S.filter(firmIn).forEach(x=>{placed[x.n]=String(x.b);});
  const ORD=CATS.map(c=>c.k), below=L=>ORD.indexOf(L)>ORD.indexOf('HP');
  const eff=v=>Math.max(v.T,typeof v.overrun==='number'?v.overrun:0); // a vessel whose work will run past her list ETC is not counted as leaving on it (Parvraj, 22 Nov: 36 h of cargo beyond the ETC)
  const lineOf=x=>x.slot||x.cat;
  const occN=L=>V.filter(v=>v.cat!=='SPACE'&&v.T>NOW&&eff(v)>WE&&lineOf(v)===L).length+S.filter(x=>firmIn(x)&&lineOf(x)===L).length; // places of a line held through this window
  const rows=BERTHS.filter(B=>!B.ppp&&!B.mnt&&!B.kict).map(B=>{
    const r={b:B.id}, occ=V.filter(v=>v.cat!=='SPACE'&&v.T>NOW&&lies(v,B)).sort((a,z)=>eff(a)-eff(z)), last=occ[occ.length-1]||null;
    if(!last){r.run=Math.round(slotRun(B.id,NOW)*RUN_TOL);if(!W.some(w=>ready(w)&&canUse(w,B.id)&&(w.loa||0)<=r.run)){r.st='S';return r;}r.st='K';r.t=NOW;r.now=1;}
    else{r.v=last;r.t=(eff(last)<PROG_END&&!PROG_SAIL.has(last.n))?PROG_END:eff(last);r.over=typeof last.overrun==='number'&&last.overrun>last.T; // a sailing the present programme does not print falls to the next window
      r.st=r.t<=WE+0.01?'K':'C';r.coming=last.F>NOW;r.est=!!last.est||!!last.dpr;if(r.st==='C')return r;}
    const pk=S.filter(x=>inWin(x)&&String(x.b)===B.id).sort((a,z)=>a.F-z.F)[0]||null;
    if(pk&&!r.now&&fa(pk)>r.t&&fa(pk)<=WE)r.t=fa(pk);
    if(pk&&firmIn(pk)){r.pr=lineOf(pk);r.via=(pk.via||'').replace(/ \(Sr No 7\)/,'');r.ch=[pk.n].concat(pk.alt&&pk.alt.n&&pk.alt.n!==pk.n?[pk.alt.n]:[]);}
    else{ // the count from the top: the first line with a vacant place and a ready vessel the berth suits
      const run=slotRun(B.id,r.t+0.1)*RUN_TOL, fits=w=>ready(w)&&!placed[w.n]&&canUse(w,B.id)&&(w.loa||0)<=run;
      r.pr='';r.ch=[];
      for(const C of CATS){if(C.k==='HP'||occN(C.k)>=C.max)continue;const line=W.filter(w=>ready(w)&&!placed[w.n]&&w.rk&&w.rk[C.k]!=null&&w.rk[C.k]<98).sort((a,z)=>a.rk[C.k]-z.rk[C.k]);
        const c=line.filter(fits);if(!c.length)continue;
        r.pr=C.k;r.vac=C.max-occN(C.k);r.ch=c.slice(0,3).map(w=>w.n);r.sen=(line.find(w=>w.rk[C.k]<c[0].rk[C.k]&&!fits(w))||{}).n||'';break;}
      if(!r.pr)r.ch=W.filter(fits).sort((a,z)=>((((a.rk||{}).GEN)||99)-(((z.rk||{}).GEN)||99))||(a.rdy-z.rdy)).slice(0,3).map(w=>w.n);
      r.sh=V.filter(v=>v.F<=NOW&&v.T>WE&&/\blogs?\b/i.test(v.c)&&(BERTHS.find(x=>x.id===v.b)||{}).clean&&canUse({n:v.n,c:v.c,q:v.q,u:v.u,loa:v.loa,dr:v.dr||0,g:v.g,rk:{},x:''},B.id)).map(v=>({n:base(v.n),b:v.b}));
      if(r.sen){const sw=W.find(w=>w.n===r.sen);if(!(sw&&r.sh.some(x=>canUse(sw,x.b))))r.sen='';}}
    const pool=HPB_CAND.filter(c=>c.st===0&&c.mt===M&&c.al.includes(B.id)).sort((a,z)=>((a.rank||99)-(z.rank||99))||((a.w.rdy||1e9)-(z.w.rdy||1e9)));
    if(pool.length&&(r.pr==='HP'||!r.pr||below(r.pr))){const hp=pool.filter(c=>r.pr==='HP'||!pk||!firmIn(pk)||c.w.n!==pk.n);if(hp.length)r.hp=hp;}
    return r;});
  const K=rows.filter(r=>r.st==='K'), C=rows.filter(r=>r.st==='C'), Sm=rows.filter(r=>r.st==='S');
  const isEta=n=>(typeof ETA!=='undefined')&&!!ETA[n], ag=n=>agOf(n)!=='—'?agOf(n):(agOf(base(n))!=='—'?agOf(base(n)):'');
  const rkTxt=w=>ORD.filter(k=>w.rk&&w.rk[k]!=null).map(k=>MB_RK[k]+(w.govAuto&&k==='GOV'?'':' '+(w.rk[k]>=98?'Y':w.rk[k]))).join(' · ');
  const wdet=w=>[ex(w.c),nf.format(w.q)+' '+ex(w.u),ag(w.n)?'agent '+ex(ag(w.n)):'',w.rdy==null?'':isEta(w.n)?'ETA '+dd(w.rdy)+' · abhi pahunchi nahi':'ready '+dd(w.rdy)+' · '+Math.max(0,Math.floor((M-w.rdy)/24))+' din se',w.loa?Math.round(w.loa)+' m':'',w.dr?w.dr+' m draft':''].filter(Boolean).join(' · ');
  const vdet=v=>{const F0=Math.min(...V.filter(x=>base(x.n)===base(v.n)).map(x=>x.F)), d=DPR.rows.find(x=>base(x.n)===base(v.n)&&/^CJ/.test(x.loc||''));
    return [ex(v.c),nf.format(v.q)+' '+ex(v.u),ag(v.n)?'agent '+ex(ag(v.n)):'',(F0<=NOW?'lagi ':'aayegi ')+fmt(F0),d&&d.bal>0?'baaki '+nf.format(d.bal)+' '+ex(v.u)+' (DPR '+DPR.d.slice(0,5)+')':''].filter(Boolean).join(' · ');};
  const vrow=(n,i,x)=>{const w=W.find(y=>y.n===n)||{n,c:'',q:0,u:'',rk:{}};return `<div class="mbv${isMine(n)?' me':''}"><div class="mbv1">${i!=null?`<b>${i+1}</b>`:''}<span>${ex(base(n))}</span>${x&&x.two?'<em>2 berth chahiye</em>':''}${isEta(n)?'<em>ETA</em>':''}${isMine(n)?'<em class="mbm">M&amp;Co</em>':''}<i>${rkTxt(w)}</i></div><div class="mbv2">${wdet(w)}</div></div>`;};
  const prl=r=>MB_PR[r.pr]||r.pr;
  const card=r=>{const v=r.v, across=v&&v.b!==r.b;
    const out=r.now?'<span class="mbno">Abhi khali hai</span>':`<span class="mbo">${ex(base(v.n))}</span>${across?` <small>· CJ-${v.b} wali vessel, dono berth par</small>`:''}<div class="mbv2">${vdet(v)}</div>`;
    let h=`<div class="mbc"><div class="mbt"><span class="mbn">CJ-${r.b}</span><span class="mbk">KHALI · ${r.now?'abhi':(r.est?'~':'')+fmt(r.t)}</span></div><div class="mbr"><label>Niklegi</label><div>${out}</div></div>`;
    const pri=r.pr?`<span class="mbp">${prl(r)}</span>${r.via?` <small>· ${ex(r.via)}</small>`:''}${r.vac?` <small>· ${r.vac} jagah khali</small>`:''}`:'<span class="mbno">ginti mein koi line khali nahi · jo lag sakti hain:</span>';
    if(r.hp){h+=`<div class="mbr"><label>Priority</label><div><span class="mbp">HP · bid</span></div></div><div class="mbr mbw"><label>Chance · bid mein</label><div>${r.hp.map(c=>vrow(c.w.n,null,c)).join('')}</div></div>`;
      if(r.pr!=='HP'&&r.ch.length)h+=`<div class="mbr"><label>Bid na ho</label><div>${pri}</div></div><div class="mbr mbw"><div>${r.ch.map((n,i)=>vrow(n,i)).join('')}</div></div>`;}
    else h+=`<div class="mbr"><label>Priority</label><div>${pri}</div></div><div class="mbr mbw"><label>Chance</label><div>${r.ch.length?r.ch.map((n,i)=>vrow(n,i)).join(''):'<span class="mbno">abhi koi naam nahi</span>'}</div></div>`;
    if(r.sh&&r.sh.length)h+=`<div class="mbr mbw"><label>Shifting se</label><div><small class="mbs">${r.sen?`${prl(r)} ki senior <b>${ex(base(r.sen))}</b> is berth par nahi lag sakti. `:''}${r.sh.map(x=>ex(x.n)).join(' ya ')} (logs) yahan shift ho, to ${r.sh.length>1?'unki':'uski'} clean berth ${r.sen?ex(base(r.sen))+' ko':'doosri vessel ko'}.</small></div></div>`;
    return h+'</div>';};
  const crow=r=>`<tr><td>CJ-${r.b}</td><td><b>${ex(base(r.v.n))}</b>${isMine(r.v.n)?' <small class="mbm">M&amp;Co</small>':''}${r.over?` <small>· list ETC ${fmt(r.v.T)}, par kaam baaki</small>`:''}<div class="mbv2">${vdet(r.v)}</div></td><td>~${dd(r.t)}</td></tr>`;
  const srow=r=>`<tr><td>CJ-${r.b}</td><td class="mbno">Jagah chhoti (~${r.run} m) · koi vessel fit nahi</td><td></td></tr>`;
  const hh=document.getElementById('mbh'), hs=document.getElementById('mbsub');
  if(hh)hh.innerHTML=`${fday(M)} <span>· 11:00</span>`;
  if(hs)hs.innerHTML=(PEND?'<b style="color:var(--warn)">Meeting ho chuki</b> · programme ka intezaar · ':'')+`Kaunsi berth khali hogi, aur kisko mil sakti hai · ${fday(WE)} 18:00 tak ki berths`;
  el.innerHTML=`<div class="mbstrip">${rows.map(r=>(r.b==='13'?'<u></u>':'')+`<i class="${r.st==='K'?'k':r.st==='S'?'s':''}">${r.b}</i>`).join('')}</div>`
    +`<div class="mbleg"><span><b style="background:#e0a23a"></b>Khali hogi · ${K.length}</span><span><b style="background:#22303d"></b>Continue · ${C.length}</span>${Sm.length?`<span><b style="background:repeating-linear-gradient(135deg,#1b242d 0 3px,#3a4856 3px 6px)"></b>Chhoti jagah · ${Sm.length}</span>`:''}</div>`
    +(K.length?`<div class="mbgrid">${K.map(card).join('')}</div>`:'<p class="mbno">Is meeting ki window mein koi berth khali nahi ho rahi.</p>')
    +((C.length||Sm.length)?`<div class="mbcont"><h3>Continue · khali nahi hongi</h3><table>${C.map(crow).join('')}${Sm.map(srow).join('')}</table></div>`:'')
    +`<p class="mbfoot">Chance mein naam us line ki seniority ke order mein · HP mein bid hoti hai, order nahi · daayin taraf list ke rank (SGR = SAAGAR, GEN = General, Y = rank nahi chhapa)<br>Yeh board ka andaza hai · port ka programme aane par milaya jayega</p>`;
  const vb=document.getElementById('vb-meeting');if(vb)vb.innerHTML=`<b>${K.length}</b> khali · ${fday(M)}`;
  window.__MEETB={meet:fday(M)+' 11:00',end:fmt(WE),at:fmt(NOW),rows:rows.map(r=>({b:r.b,st:r.st,out:r.v?base(r.v.n):'',t:r.t!=null?fmt(r.t):'',pr:r.pr||'',via:r.via||'',ch:(r.ch||[]).map(base),hp:(r.hp||[]).map(c=>base(c.w.n)),sh:(r.sh||[]).map(x=>x.n),sen:r.sen?base(r.sen):''}))};
}
