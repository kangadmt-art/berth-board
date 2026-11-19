// extract.js <board.html> <out.json> — pulls what the priority-wise page needs out of the board (read-only)
const fs=require('fs');const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const file=process.argv[2];const html=fs.readFileSync(file,'utf8');
const m1=html.match(/const NOW=h\('([^']+)'\)/),m2=html.match(/const UPDATED='([^']+)'/),m3=html.match(/const HZ=h\('([^']+)'\)/);
const hdr=(html.match(/<br>(List <b>[^\n]*?)<br><details class="srcmore">/)||[])[1]||'';
const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+file);await p.waitForTimeout(2500);
const r=await p.evaluate(([now,hz])=>{const f=window.__fmt,{V,W,allowedBerths,h}=window.__dbg,S=window.__S,NOW=h(now);
 const mine=x=>/MIHIR & COMPANY/.test(x||'');const q7=w=>/30\s*K\s*[\/.]\s*25\s*K/i.test(w.x||'');
 const berth=V.filter(v=>v.T>NOW&&!v.span).map(v=>({slot:v.slot||v.cat,cat:v.cat,via:v.via||'',b:v.b,n:v.n,c:v.c,q:v.q,u:v.u,F:v.F,T:v.T,Ft:f(v.F),Tt:f(v.T),est:!!v.est,lt:(v.listT&&Math.abs(v.listT-v.T)>0.5)?f(v.listT):'',future:v.F>NOW,mine:mine(v.note),dpr:!!v.dpr,noOut:!!v.noOut,over:!!v.overstay}));
 const proj={};S.filter(x=>x.proj).forEach(x=>{proj[x.n]={b:x.b,F:x.F,Ft:f(x.F),Tt:f(x.T),cat:x.cat,via:x.via||''};});
 const wait=W.map(w=>{const x=w.x||'';const tags=[];
   if(/FINISHING AT MIDSTREAM/i.test(x.slice(0,400)))tags.push('finishing at midstream');else if(/working at (MS|MRG|midstream)/i.test(x.slice(0,260)))tags.push('working at midstream');
   if(/HELD|held out|still held|no berth; held/i.test(x.slice(0,400)))tags.push('held');
   return {n:w.n,c:w.c,q:w.q,u:w.u,loa:w.loa,dr:w.dr,rdy:w.rdy,rdyT:w.rdy!=null?f(w.rdy):'',rep:w.rep,repT:w.rep!=null?f(w.rep):'',rk:w.rk,govAuto:!!w.govAuto,q7:q7(w),noHP:!!w.noHP,allowed:allowedBerths(w),tags,mine:mine(x),proj:proj[w.n]||null,first:x.slice(0,200)};});
 return {berth,wait,opt:window.__OPT,nowT:f(NOW),NOW,HZ:h(hz)};},[m1[1],m3[1]]);
r.updated=m2[1];r.hz=m3[1];r.hdr=hdr.replace(/<[^>]+>/g,'');
fs.writeFileSync(process.argv[3],JSON.stringify(r));console.log('berth',r.berth.length,'wait',r.wait.length,'bytes',JSON.stringify(r).length);
console.log(r.hdr,'|',r.nowT,'|',r.updated,'| hz',r.hz);

await b.close();})();
