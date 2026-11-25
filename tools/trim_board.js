// node tools/trim_board.js <abs board.html>   — makes the DISPLAY board light (Mihir, 21 Nov 14:18). Run tools/build_db.js FIRST: what is cut here lives on in the data book.
//  1. a vessel that has completed and left is taken out of V (kept: every entry of a vessel still alongside or coming, and the last vessel that left each berth — the projection reads it)
//  2. signal movements: only the rows of the board's own day (MV and LIQ.moves)
//  3. expected-vs-actual checks (LEARN): only the open (pending) ones
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
 // a SALT vessel that leaves V goes into SALT_DONE first (the Salt tab's completed record)
 const sd=[];[...drop].forEach(i=>{const l=lines[i];const g=k=>{const m=l.match(new RegExp("\\b"+k+":'((?:[^'\\\\]|\\\\.)*)'"));return m?m[1]:'';};if(!/salt/i.test(g('c'))||/\best:1/.test(l))return;
  const n=g('n'),bn=n.replace(/ \(.*$/,''),mf=g('f'),qm=l.match(/\bq:([0-9.]+)/);if(s.includes("{n:'"+bn+"',")&&s.slice(s.indexOf('const SALT_DONE=[')).split('\n];')[0].includes("mf:'"+mf+"'"))return;
  const rp=x=>{const m=s.match(new RegExp("'"+x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+"':'(\\d\\d-\\d\\d \\d\\d:\\d\\d)'"));return m?m[1]:null;};const arr=rp(n)||rp(bn);
  const agm=s.match(new RegExp("'"+n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+"':'([A-Z][^']*)'"));
  sd.push(" {n:'"+bn+"',q:"+(qm?qm[1]:0)+",ag:'"+(agm?agm[1]:'')+"',b:'"+g('b')+"',pri:'"+g('cat')+"',arr:"+(arr?"'"+arr+"'":'null')+",mf:'"+mf+"',out:'"+g('t')+"'}");});
 // a vessel of CJ-9 / CJ-10 that leaves V goes into PPP_DONE first (the CJ-9 · 10 tab's record of stay and output)
 const pd=[];[...drop].forEach(i=>{const l=lines[i];const g=k=>{const m=l.match(new RegExp("\\b"+k+":'((?:[^'\\\\]|\\\\.)*)'"));return m?m[1]:'';};if(!/^(9|10)$/.test(g('b')))return;
  const n=g('n'),bn=n.replace(/ \(.*$/,''),mf=g('f'),qm=l.match(/\bq:([0-9.]+)/);const blk=(s.indexOf('const PPP_DONE=[')>0)?s.slice(s.indexOf('const PPP_DONE=[')).split('\n];')[0]:'';if(blk.includes("{n:'"+bn+"',")&&blk.includes("mf:'"+mf+"'"))return;
  const agm=s.match(new RegExp("'"+n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+"':'([A-Z][^']*)'"));
  pd.push(" {n:'"+bn+"',b:'"+g('b')+"',c:'"+g('c')+"',q:"+(qm?qm[1]:0)+",ie:'',ag:'"+(agm?agm[1]:'')+"',mf:'"+mf+"',out:'"+g('t')+"'"+(/\best:1/.test(l)?',est:1':'')+"}");});
 // an HP vessel that leaves V goes into HP_LOG first (the HP bid panel's record of winning quotes — Mihir, 22 Nov)
 const hd=[];[...drop].forEach(i=>{const l=lines[i];const g=k=>{const m=l.match(new RegExp("\\b"+k+":'((?:[^'\\\\]|\\\\.)*)'"));return m?m[1]:'';};if(g('cat')!=='HP'||/\bslot:'/.test(l)||/\bvia:'/.test(l)||/\best:1/.test(l))return;const nm=l.match(/\bnm:(\d+)/);if(!nm)return;
  const n=g('n'),bn=n.replace(/ \(.*$/,''),mf=g('f'),qm=l.match(/\bq:([0-9.]+)/);const blk=(s.indexOf('const HP_LOG=[')>0)?s.slice(s.indexOf('const HP_LOG=[')).split('\n];')[0]:'';if(!blk||(blk.includes("{n:'"+bn+"',")&&blk.includes("f:'"+mf+"'")))return;
  const agm=s.match(new RegExp("'"+n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+"':'([A-Z][^']*)'"));
  hd.push(" {n:'"+bn+"',b:'"+g('b')+"',c:'"+g('c')+"',q:"+(qm?qm[1]:0)+",ag:'"+(agm?agm[1]:'')+"',qt:"+nm[1]+",f:'"+mf+"',o:'"+g('t')+"'}");});
 // a vessel of CJ-16 that leaves V goes into CJ16_LOG first (the CJ-16 non-clean cargo section's record of every call at the berth — Mihir, 25 Nov 23:48)
 const cd=[];[...drop].forEach(i=>{const l=lines[i];const g=k=>{const m=l.match(new RegExp("\\b"+k+":'((?:[^'\\\\]|\\\\.)*)'"));return m?m[1]:'';};if(g('b')!=='16'||g('cat')==='SPACE')return;
  const n=g('n'),bn=n.replace(/ \(.*$/,''),mf=g('f'),qm=l.match(/\bq:([0-9.]+)/),nm=l.match(/\bnm:(\d+)/);const blk=(s.indexOf('const CJ16_LOG=[')>0)?s.slice(s.indexOf('const CJ16_LOG=[')).split('\n];')[0]:'';if(!blk||(blk.includes("{n:'"+bn+"',")&&blk.includes("f:'"+mf+"'")))return;
  const esc=n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');const agm=s.match(new RegExp("'"+esc+"':'([A-Z][^']*)'"));const iem=s.match(new RegExp("'"+esc+"':'(IMP|EXP)'"));const lom=s.match(new RegExp("'"+esc+"':([0-9.]+)[,}]"));
  cd.push(" {n:'"+bn+"',c:'"+g('c')+"',q:"+(qm?qm[1]:0)+",u:'"+(g('u')||'MT')+"',ie:'"+(iem?iem[1]:'')+"',ag:'"+(agm?agm[1]:'')+"',cat:'"+(g('slot')||g('cat'))+"',qt:"+(nm?nm[1]:'null')+",loa:"+(lom?lom[1]:'null')+",g:'',f:'"+mf+"',o:'"+g('t')+"'"+(/\best:1/.test(l)?',est:1':'')+"}");});
 s=s.slice(0,a)+lines.filter((l,i)=>!drop.has(i)).join('\n')+s.slice(e);
 if(pd.length){const x=s.indexOf('const PPP_DONE=['),y=s.indexOf('\n];',x);if(x>0)s=s.slice(0,y)+',\n'+pd.join(',\n')+s.slice(y);console.log('CJ-9/10 record +',pd.length,'— CHECK the I/E, agent and sailing hour of the new line(s) in PPP_DONE');}
 if(hd.length){const x=s.indexOf('const HP_LOG=['),y=s.indexOf('\n];',x);if(x>0)s=s.slice(0,y)+',\n'+hd.join(',\n')+s.slice(y);console.log('HP record +',hd.length,'— CHECK the agent of the new line(s) in HP_LOG');}
 if(cd.length){const x=s.indexOf('const CJ16_LOG=['),y=s.indexOf('\n];',x);if(x>0)s=s.slice(0,y)+',\n'+cd.join(',\n')+s.slice(y);console.log('CJ-16 record +',cd.length,'— CHECK the I/E, agent, LOA, gear and sailing hour of the new line(s) in CJ16_LOG');}
 if(sd.length){const x=s.indexOf('const SALT_DONE=['),y=s.indexOf('\n];',x);if(x>0)s=s.slice(0,y)+',\n'+sd.join(',\n')+s.slice(y);console.log('salt record +',sd.length,'— CHECK the agent and arrival of the new line(s) in SALT_DONE');}
 // ---- 2. MV and LIQ.moves — rows of the board's day only
 const cutMoves=(start,endMark,ind)=>{const a=s.indexOf(start); if(a<0)return [0,0]; const a2=a+start.length, e=s.indexOf(endMark,a2); const arr=Function('return ['+s.slice(a2,e)+'\n]')();
  const out=arr.map(([t,rows])=>[t,rows.filter(r=>String(r[5]||'').slice(0,5)>=day /* today and what is already signalled for tomorrow */)]).filter(x=>x[1].length);
  s=s.slice(0,a2)+out.map(x=>ind+js(x)).join(',\n')+s.slice(e); return [arr.length,out.length];};
 const mv=cutMoves('const MV=[\n','\n];',' '); const la=s.indexOf('const LIQ={'); const lm=s.indexOf(' moves:[\n',la); let lq=[0,0];
 if(lm>0){const a2=lm+' moves:[\n'.length,e=s.indexOf('\n ]',a2);const arr=Function('return ['+s.slice(a2,e)+'\n]')();const out=arr.map(([t,rows])=>[t,rows.filter(r=>String(r[5]||'').slice(0,5)>=day /* today and what is already signalled for tomorrow */)]).filter(x=>x[1].length);s=s.slice(0,a2)+out.map(x=>'  '+js(x)).join(',\n')+s.slice(e);lq=[arr.length,out.length];}
 // ---- 3. LEARN — open only
 const l0=s.indexOf('const LEARN=[\n')+'const LEARN=[\n'.length, l1=s.indexOf('\n];',l0); const L=s.slice(l0,l1).split('\n'); const ent=L.filter(l=>/^ \{d:'/.test(l)); const MON3=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];const nowL=/const NOW=h\(.(\d\d)-(\d\d) /.exec(s);const dKey=(m,d)=>m*100+d;const today=dKey(+nowL[1],+nowL[2]);const recent=l=>{const m=/^ \{d:'(\d{1,2}) ([A-Z][a-z]{2})/.exec(l);if(!m)return false;const k=dKey(MON3.indexOf(m[2])+1,+m[1]);return k===today||k===today-1||(+nowL[2]===1&&k<today&&k>=today-75);}; // Mihir, 21 Nov 21:26: keep the open ones and the last two days; the rest go to the data book
 const open=ent.filter(l=>/st:'open'\},?$/.test(l)); // Mihir, 21 Nov 21:52: ONLY the pending ones stay on the board; a closed check goes to the data book (recent() above is no longer used)
 if(ent.length!==L.filter(l=>l.trim()).length)console.error('note: LEARN has',L.filter(l=>l.trim()).length-ent.length,'lines that are not entries — left out');
 s=s.slice(0,l0)+open.map(l=>l.replace(/,$/,'')).join(',\n')+s.slice(l1);
 fs.writeFileSync(file,s);
 console.log('V: dropped',drop.size,'of',idx.length,'· signal sheets',mv[0],'→',mv[1],'· oil-jetty sheets',lq[0],'→',lq[1],'· checks',ent.length,'→',open.length,'open · file',(size0/1024|0),'→',(s.length/1024|0),'KB');
})();
