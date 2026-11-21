// node tools/build_db.js <abs board.html> [out dir]   ->  db/databook.json  (the DATA BOOK: every record the board holds, as plain data)
// It opens the board in a headless browser, exposes the board's own data blocks and writes them out with dates as 'YYYY-MM-DD HH:MM'.
const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs'),path=require('path'),os=require('os');
(async()=>{
 const src=process.argv[2], out=process.argv[3]||path.join(__dirname,'..','db');
 let s=fs.readFileSync(src,'utf8');
 const mark="window.__dbg={slotRun,V,W,allowedBerths,h,PM,gearOf,gearTxt};"; if(!s.includes(mark)){console.error('marker not found');process.exit(1);}
  // exposed at the END of the script (some blocks are declared after the projection runs); each name on its own so one missing block does not stop the rest
 const names=['V','W','AG','IE','LOA','REP','ETA','DPR','MSWORK','TUNA','TUNA_OCC','LIQ','TIMBER','MV','MEETLOG','PREDLOG','MYLOG','LEARN','NOW','UPDATED','agOf'];
 const expose="\n;window.__db={};"+names.map(n=>"try{window.__db."+n+"="+n+";}catch(e){window.__db.__miss=(window.__db.__miss||'')+' "+n+"';}").join('')+"\n";
 const k=s.lastIndexOf('})();'); if(k<0){console.error('end of the board script not found');process.exit(1);} s=s.slice(0,k)+expose+s.slice(k); // the board's code is one function: the names are only visible inside it
 const tmp=path.join(os.tmpdir(),'board_db_'+process.pid+'.html'); fs.writeFileSync(tmp,s);
 const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file://'+tmp);await p.waitForTimeout(2500);
 const db=await p.evaluate(()=>{
  const D=window.__db; if(D.__miss)console.warn('missing blocks:'+D.__miss); const pad=x=>String(x).padStart(2,'0');
  const iso=t=>{if(t==null||isNaN(t))return null;const d=new Date(Date.UTC(2026,9,25,0,0)+t*36e5);return d.getUTCFullYear()+'-'+pad(d.getUTCMonth()+1)+'-'+pad(d.getUTCDate())+' '+pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());};
  const md=x=>x?('2026-'+x):null; // 'MM-DD HH:MM' -> '2026-MM-DD HH:MM'
  const ag=n=>{try{return D.agOf?D.agOf(n):(D.AG[n]||'');}catch(e){return D.AG[n]||'';}};
  const g=n=>{const x=window.__dbg.gearOf(n);return window.__dbg.gearTxt(x);};
  const S=window.__S||[];
  const calls=D.V.map(v=>({vessel:v.n,berth:v.b,panels:v.p||null,cargo:v.c||'',qty:v.q||null,unit:v.u||'',ie:D.IE[v.n]||'',agent:ag(v.n),loa:v.loa||D.LOA[v.n]||null,gear:g(v.n),
    priority:v.cat||'',slot:v.slot||'',via:v.via||'',norm:v.nm||null,madeFast:iso(v.F),out:iso(v.T),outIsEstimate:!!(v.est||v.T>D.NOW),listETC:v.lt?iso(D.V===null?null:window.__dbg.h(v.lt)):null,
    status:v.T<=D.NOW?'sailed':(v.F<=D.NOW?'alongside':'coming'),note:v.note||v.x||''}));
  const proj={};S.filter(x=>x.proj).forEach(x=>{proj[x.n]={berth:x.b,at:iso(x.F),out:iso(x.T),by:x.cat,via:x.via||''};});
  const waiting=D.W.map(w=>({vessel:w.n,cargo:w.c,qty:w.q,unit:w.u,ie:D.IE[w.n]||'',agent:ag(w.n),loa:w.loa||null,draught:w.dr||null,gear:g(w.n),reported:iso(w.rep),ready:iso(w.rdy),
    ranks:w.rk||{},status:(w.rep!=null&&w.rep>D.NOW)?'expected':'waiting',berthsAllowed:window.__dbg.allowedBerths(w),projection:proj[w.n]||null,note:w.x||''}));
  return {missing:D.__miss||'',builtFrom:D.UPDATED,asOf:iso(D.NOW),calls,waiting,dpr:D.DPR,barge:D.MSWORK,tuna:D.TUNA,tunaDays:D.TUNA_OCC,liquid:D.LIQ,timber:D.TIMBER,moves:D.MV,meetings:D.MEETLOG,predictions:D.PREDLOG,ourLog:D.MYLOG,learn:D.LEARN};
 });
 await b.close(); fs.unlinkSync(tmp);
 if(errs.length){console.error('PAGE ERRORS',errs);process.exit(1);}
 // blocks declared inside a function of the board (not visible at the end of the script): read as plain literals from the source
 const lit=name=>{const a=s.indexOf('const '+name+'=[');if(a<0)return [];const e=s.indexOf('\n];',a);try{return Function('return '+s.slice(a+('const '+name+'=').length,e+2))();}catch(err){console.error(name+' not read: '+err.message);return [];}};
 if(!db.meetings)db.meetings=lit('MEETLOG'); if(!db.predictions)db.predictions=lit('PREDLOG'); db.missing='';
 fs.mkdirSync(out,{recursive:true}); fs.writeFileSync(path.join(out,'databook.json'),JSON.stringify(db));
 const st=x=>db.calls.filter(c=>c.status===x).length;
 console.log('databook.json',(JSON.stringify(db).length/1024|0)+' KB · calls',db.calls.length,'(sailed',st('sailed'),'· alongside',st('alongside'),'· coming',st('coming')+') · waiting rows',db.waiting.length,'· moves sheets',db.moves.length,'· barge days',db.barge.days.length,'· meetings',db.meetings.length,'· predictions',db.predictions.length);
})();
