// node tools/trim_board.js <abs board.html>   — makes the DISPLAY board light (Mihir, 21 Nov 14:18). Run tools/build_db.js FIRST: what is cut here lives on in the data book.
//  1. a vessel that has completed and left is taken out of V (kept: every entry of a vessel still alongside or coming, and the last vessel that left each berth — the projection reads it)
//  2. signal movements: only the rows of the board's own day (MV and LIQ.moves)
//  3. expected-vs-actual checks (LEARN): only the open ones
// The projection must be identical before and after — check with tools/dump_projection.js.
const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const q=s=>String(s).replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/\n/g,'\\n');
const js=o=>o===null||o===undefined?'null':typeof o==='number'?String(o):typeof o==='string'?"'"+q(o)+"'":Array.isArray(o)?'['+o.map(js).join(',')+']':'{'+Object.keys(o).map(k=>k+':'+js(o[k])).join(',')+'}';
(async()=>{
 const file=process.argv[2]; let s=fs.readFileSync(file,'utf8'); const size0=s.length;
 const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+file);await p.waitForTimeout(2500);
 const info=await p.evaluate(()=>{const d=window.__dbg,pad=x=>String(x).padStart(2,'0');const now=Math.max(...d.V.map(v=>v.F).filter(f=>f<1e6));return {V:d.V.map(v=>({n:v.n,b:v.b,F:v.F,T:v.T}))};});
 const nowM=s.match(/const NOW=h\('(\d\d-\d\d) (\d\d):(\d\d)'\);/); const day=nowM[1];
 const NOW=await p.evaluate(x=>window.__dbg.h(x),nowM[0].slice(13,24)); await b.close();
 // ---- 1. V
 const a=s.indexOf('const V=[\n')+'const V=[\n'.length, e=s.indexOf('\n];',a); const lines=s.slice(a,e).replace(/\},\s*\{b:'/g,"},\n {b:'").split('\n'); // one entry a line
 const idx=lines.map((l,i)=>/^ \{b:'/.test(l)?i:-1).filter(i=>i>=0); if(idx.length!==info.V.length){console.error('V lines',idx.length,'≠ V entries',info.V.length);process.exit(1);}
 const live=new Set(info.V.filter(v=>v.T>NOW).map(v=>v.n)); const lastAt={};
 info.V.forEach((v,i)=>{if(v.T<=NOW&&(!lastAt[v.b]||info.V[lastAt[v.b].i].T<v.T))lastAt[v.b]={i};});
 const keepLast=new Set(Object.values(lastAt).map(x=>x.i)); const drop=new Set(); 
 info.V.forEach((v,i)=>{if(v.T<=NOW&&!live.has(v.n)&&!keepLast.has(i))drop.add(idx[i]);});
 s=s.slice(0,a)+lines.filter((l,i)=>!drop.has(i)).join('\n')+s.slice(e);
 // ---- 2. MV and LIQ.moves — rows of the board's day only
 const cutMoves=(start,endMark,ind)=>{const a=s.indexOf(start); if(a<0)return [0,0]; const a2=a+start.length, e=s.indexOf(endMark,a2); const arr=Function('return ['+s.slice(a2,e)+'\n]')();
  const out=arr.map(([t,rows])=>[t,rows.filter(r=>String(r[5]||'').startsWith(day))]).filter(x=>x[1].length);
  s=s.slice(0,a2)+out.map(x=>ind+js(x)).join(',\n')+s.slice(e); return [arr.length,out.length];};
 const mv=cutMoves('const MV=[\n','\n];',' '); const la=s.indexOf('const LIQ={'); const lm=s.indexOf(' moves:[\n',la); let lq=[0,0];
 if(lm>0){const a2=lm+' moves:[\n'.length,e=s.indexOf('\n ]',a2);const arr=Function('return ['+s.slice(a2,e)+'\n]')();const out=arr.map(([t,rows])=>[t,rows.filter(r=>String(r[5]||'').startsWith(day))]).filter(x=>x[1].length);s=s.slice(0,a2)+out.map(x=>'  '+js(x)).join(',\n')+s.slice(e);lq=[arr.length,out.length];}
 // ---- 3. LEARN — open only
 const l0=s.indexOf('const LEARN=[\n')+'const LEARN=[\n'.length, l1=s.indexOf('\n];',l0); const L=s.slice(l0,l1).split('\n'); const ent=L.filter(l=>/^ \{d:'/.test(l)); const open=ent.filter(l=>/st:'open'\},?$/.test(l));
 if(ent.length!==L.filter(l=>l.trim()).length)console.error('note: LEARN has',L.filter(l=>l.trim()).length-ent.length,'lines that are not entries — left out');
 s=s.slice(0,l0)+open.map(l=>l.replace(/,$/,'')).join(',\n')+s.slice(l1);
 fs.writeFileSync(file,s);
 console.log('V: dropped',drop.size,'of',idx.length,'· signal sheets',mv[0],'→',mv[1],'· oil-jetty sheets',lq[0],'→',lq[1],'· checks',ent.length,'→',open.length,'open · file',(size0/1024|0),'→',(s.length/1024|0),'KB');
})();
