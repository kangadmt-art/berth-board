// ---- NEXT MEETING, berth by berth — at the top of the Priority chart page. SIMPLE VERSION (Mihir, 22 Nov 18:20: "bahut complicated kar diya, simple bana").
// It follows his rule of 18:09 and nothing else:
//   1. Every berthed vessel holds a priority — the one the berthing list prints for her.
//   2. When she leaves, the next vessel of THAT priority comes ("24 ke badle 24").
//   3. If that priority has no vessel, the one after it in the order gets it.
// One more line is shown only when it applies: a HIGHER priority with a place vacant and a vessel waiting for a berth that suits her.
// The names come straight from the list's rank columns. The board's own opinion on whether the berth suits a vessel is only a small tag on her name.
let HPB_CAND=[]; // filled by hpbid(): every HP bidder with the meeting she bids at
const MB_PR={GOV:'Govt',COASTAL:'Coastal',HP:'HP · bid',SAAGAR:'SAAGAR','24H':'24 hrs','8K':'8K',STL:'Steel / Project',BIT:'Bitumen',GEN:'General'};
const MB_HOLD=Object.assign({},MB_PR,{HP:'HP'});
const MB_RK={GOV:'GOV',COASTAL:'CSTL',HP:'HP',SAAGAR:'SGR','24H':'24H','8K':'8K',STL:'STL',BIT:'BIT',GEN:'GEN'};
function meetBoard(){
  const el=document.getElementById('mtgb'); if(!el)return;
  const M=NXM, WE=M-11+24+18, base=n=>n.replace(/ \(.*$/,''), ex=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  const dd=x=>{const d=dt(x);return d.getUTCDate()+' '+MON[d.getUTCMonth()];};
  const lies=(v,B)=>v.b===B.id||(v.p&&Math.min(v.p[1],B.p[1])-Math.max(v.p[0],B.p[0])>2.5); // a vessel lying across into the berth blocks it too (Flag Marina, 254 m, over CJ-7 and CJ-8)
  const ready=w=>w.rdy!=null&&w.rdy<=M+0.01, canUse=(w,b)=>{try{return allowedBerths(w).includes(b);}catch(e){return false;}};
  const ORD=CATS.map(c=>c.k), lineOf=x=>x.slot||x.cat;
  const eff=v=>Math.max(v.T,typeof v.overrun==='number'?v.overrun:0); // a vessel whose work will run past her list ETC is not counted as leaving on it
  const holdAt=(L,t)=>V.filter(v=>v.cat!=='SPACE'&&lineOf(v)===L&&v.F<=t+0.01&&eff(v)>t+0.01&&!(L==='GOV'&&v.via)&&!(L==='HP'&&(v.cat==='GEN'||v.cat==='STL'))); // who holds a line's places at that hour
  const rows=BERTHS.filter(B=>!B.ppp&&!B.mnt&&!B.kict).map(B=>{
    const r={b:B.id}, occ=V.filter(v=>v.cat!=='SPACE'&&v.T>NOW&&lies(v,B)).sort((a,z)=>eff(a)-eff(z)), last=occ[occ.length-1]||null;
    if(!last){r.run=Math.round(slotRun(B.id,NOW)*RUN_TOL);if(!W.some(w=>ready(w)&&canUse(w,B.id)&&(w.loa||0)<=r.run)){r.st='S';return r;}r.st='K';r.t=NOW;r.now=1;}
    else{r.v=last;r.t=(eff(last)<PROG_END&&!PROG_SAIL.has(last.n))?PROG_END:eff(last);r.over=typeof last.overrun==='number'&&last.overrun>last.T; // a sailing the present programme does not print falls to the next window
      r.st=r.t<=WE+0.01?'K':'C';r.est=!!last.est||!!last.dpr;if(r.st==='C')return r;}
    const run=slotRun(B.id,r.t+0.1)*RUN_TOL, suits=w=>canUse(w,B.id)&&(w.loa||0)<=run;
    const pool=HPB_CAND.filter(c=>c.st===0&&c.mt===M&&c.al.includes(B.id)).sort((a,z)=>((a.rank||99)-(z.rank||99))||((a.w.rdy||1e9)-(z.w.rdy||1e9)));
    const queue=L=>L==='HP'?pool.map(c=>c.w):W.filter(w=>ready(w)&&w.rk&&w.rk[L]!=null&&w.rk[L]<98).sort((a,z)=>a.rk[L]-z.rk[L]);
    const X=r.v?lineOf(r.v):null, ix=X?ORD.indexOf(X):-1;
    r.up=[];r.same=null;r.next=null;
    ORD.forEach((L,i)=>{if(ix>=0&&i>=ix)return;const C=CATS[i];                       // a higher priority: a place vacant AND a vessel this berth suits
      if(L!=='HP'&&holdAt(L,r.t).length>=C.max)return;const c=queue(L).filter(suits);if(c.length&&r.up.length<2)r.up.push({L,ws:c.slice(0,2)});});
    if(ix>=0){r.same={L:X,ws:queue(X).slice(0,X==='HP'?6:3)};                                       // the same priority, in list order — whether or not the board thinks the berth suits
      if(!r.same.ws.some(suits))for(let i=ix+1;i<ORD.length;i++){const c=queue(ORD[i]).filter(w=>suits(w)&&!r.same.ws.includes(w));if(c.length){r.next={L:ORD[i],ws:c.slice(0,2)};break;}}}  // the one after it — only when the same priority has no vessel this berth suits
    r.sv=suits;return r;});
  const K=rows.filter(r=>r.st==='K'), C=rows.filter(r=>r.st==='C'), Sm=rows.filter(r=>r.st==='S');
  const isEta=n=>(typeof ETA!=='undefined')&&!!ETA[n], ag=n=>agOf(n)!=='—'?agOf(n):(agOf(base(n))!=='—'?agOf(base(n)):'');
  const rkTxt=w=>ORD.filter(k=>w.rk&&w.rk[k]!=null).map(k=>MB_RK[k]+(w.govAuto&&k==='GOV'?'':' '+(w.rk[k]>=98?'Y':w.rk[k]))).join(' · ');
  const wdet=w=>[ex(w.c),nf.format(w.q)+' '+ex(w.u),ag(w.n)?'agent '+ex(ag(w.n)):'',w.rdy==null?'':isEta(w.n)?'ETA '+dd(w.rdy)+' · abhi pahunchi nahi':'ready '+dd(w.rdy)+' · '+Math.max(0,Math.floor((M-w.rdy)/24))+' din se',w.loa?Math.round(w.loa)+' m':'',w.dr?w.dr+' m draft':''].filter(Boolean).join(' · ');
  const vdet=v=>{const F0=Math.min(...V.filter(x=>base(x.n)===base(v.n)).map(x=>x.F)), d=DPR.rows.find(x=>base(x.n)===base(v.n)&&/^CJ/.test(x.loc||''));
    return [ex(v.c),nf.format(v.q)+' '+ex(v.u),ag(v.n)?'agent '+ex(ag(v.n)):'',(F0<=NOW?'lagi ':'aayegi ')+fmt(F0),d&&d.bal>0?'baaki '+nf.format(d.bal)+' '+ex(v.u)+' (DPR '+DPR.d.slice(0,5)+')':''].filter(Boolean).join(' · ');};
  const holdTxt=v=>{const X=lineOf(v);return (MB_HOLD[X]||X)+(v.slot&&v.cat!==v.slot?' ki jagah mein · '+(MB_HOLD[v.cat]||v.cat)+' vessel':/30k\/25k/i.test(v.via||'')?' · 30K quote':/project/i.test(v.via||'')?' · project':'');};
  const vrow=(w,i,r,nonum)=>{const hc=HPB_CAND.find(c=>c.w===w);return `<div class="mbv${isMine(w.n)?' me':''}"><div class="mbv1">${nonum?'':`<b>${i+1}</b>`}<span>${ex(base(w.n))}</span>${hc&&hc.two?'<em>2 berth chahiye</em>':''}${isEta(w.n)?'<em>ETA</em>':''}${isMine(w.n)?'<em class="mbm">M&amp;Co</em>':''}${r&&r.sv&&!r.sv(w)?'<em class="mbx">board: yeh berth suit nahi</em>':''}<i>${rkTxt(w)}</i></div><div class="mbv2">${wdet(w)}</div></div>`;};
  const grp=(lab,g,r,note)=>`<div class="mbr mbw"><label>${lab} <span class="mbp">${MB_PR[g.L]||g.L}</span>${note?` <small>${note}</small>`:''}</label><div>${g.ws.length?g.ws.map((w,i)=>vrow(w,i,r,g.L==='HP')).join(''):'<span class="mbno">is priority mein abhi koi ready vessel nahi</span>'}</div></div>`;
  const card=r=>{const v=r.v, across=v&&v.b!==r.b;
    const out=r.now?'<span class="mbno">Abhi khali hai</span>':`<span class="mbo">${ex(base(v.n))}</span><span class="mbh">${holdTxt(v)}</span>${across?` <small>· CJ-${v.b} wali vessel, dono berth par</small>`:''}<div class="mbv2">${vdet(v)}</div>`;
    let h=`<div class="mbc"><div class="mbt"><span class="mbn">CJ-${r.b}</span><span class="mbk">KHALI · ${r.now?'abhi':(r.est?'~':'')+fmt(r.t)}</span></div><div class="mbr"><label>Niklegi</label><div>${out}</div></div>`;
    if(r.same)h+=grp('Usi priority ki agli',r.same,r,r.same.L==='HP'?'· jo bid mein hain':'');
    r.up.forEach(g=>{h+=grp(r.same?'Upar ki priority':'Lag sakti hai',g,r,r.same?'· jagah khali, berth ke wait mein':'');});
    if(r.next)h+=grp('Uske baad',r.next,r,r.next.L==='HP'?'· jo bid mein hain':'');
    if(!r.same&&!r.up.length)h+='<div class="mbr mbw"><div class="mbno">abhi koi naam nahi</div></div>';
    return h+'</div>';};
  const crow=r=>`<tr><td>CJ-${r.b}</td><td><b>${ex(base(r.v.n))}</b><span class="mbh">${holdTxt(r.v)}</span>${isMine(r.v.n)?' <small class="mbm">M&amp;Co</small>':''}${r.over?` <small>· list ETC ${fmt(r.v.T)}, par kaam baaki</small>`:''}<div class="mbv2">${vdet(r.v)}</div></td><td>~${dd(r.t)}</td></tr>`;
  const srow=r=>`<tr><td>CJ-${r.b}</td><td class="mbno">Jagah chhoti (~${r.run} m) · koi vessel fit nahi</td><td></td></tr>`;
  const hh=document.getElementById('mbh'), hs=document.getElementById('mbsub');
  if(hh)hh.innerHTML=`${fday(M)} <span>· 11:00</span>`;
  if(hs)hs.innerHTML=(PEND?'<b style="color:var(--warn)">Meeting ho chuki</b> · programme ka intezaar · ':'')+`Jo vessel nikli, uski priority ki agli vessel aati hai · us priority mein koi na ho to uske baad wali · ${fday(WE)} 18:00 tak ki berths`;
  el.innerHTML=`<div class="mbstrip">${rows.map(r=>(r.b==='13'?'<u></u>':'')+`<i class="${r.st==='K'?'k':r.st==='S'?'s':''}">${r.b}</i>`).join('')}</div>`
    +`<div class="mbleg"><span><b style="background:#e0a23a"></b>Khali hogi · ${K.length}</span><span><b style="background:#22303d"></b>Continue · ${C.length}</span>${Sm.length?`<span><b style="background:repeating-linear-gradient(135deg,#1b242d 0 3px,#3a4856 3px 6px)"></b>Chhoti jagah · ${Sm.length}</span>`:''}</div>`
    +(K.length?`<div class="mbgrid">${K.map(card).join('')}</div>`:'<p class="mbno">Is meeting ki window mein koi berth khali nahi ho rahi.</p>')
    +((C.length||Sm.length)?`<div class="mbcont"><h3>Continue · khali nahi hongi</h3><table>${C.map(crow).join('')}${Sm.map(srow).join('')}</table></div>`:'')
    +`<p class="mbfoot">Naam list ke rank ke order mein (daayin taraf rank: SGR = SAAGAR, GEN = General, Y = rank nahi chhapa) · HP mein bid hoti hai, order nahi<br>Yeh board ka andaza hai · port ka programme aane par milaya jayega</p>`;
  const nm=g=>g?{pr:g.L,ch:g.ws.map(w=>base(w.n))}:null;
  window.__MEETB={meet:fday(M)+' 11:00',end:fmt(WE),at:fmt(NOW),rows:rows.map(r=>({b:r.b,st:r.st,out:r.v?base(r.v.n):'',hold:r.v?lineOf(r.v):'',t:r.t!=null?fmt(r.t):'',same:nm(r.same),up:(r.up||[]).map(nm),next:nm(r.next)}))};
}
