// node tools/build_db.js <abs board.html> [out dir]   ->  db/databook.json  (the DATA BOOK: every record the board holds, as plain data)
// It opens the board in a headless browser, exposes the board's own data blocks and writes them out with dates as 'YYYY-MM-DD HH:MM'.
const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs'),path=require('path'),os=require('os');
(async()=>{
 const src=process.argv[2], out=process.argv[3]||path.join(__dirname,'..','db');
 let s=fs.readFileSync(src,'utf8');
 const mark="window.__dbg={slotRun,V,W,allowedBerths,h,PM,gearOf,gearTxt};"; if(!s.includes(mark)){console.error('marker not found');process.exit(1);}
  // exposed at the END of the script (some blocks are declared after the projection runs); each name on its own so one missing block does not stop the rest
 const names=['V','W','AG','IE','LOA','REP','ETA','DPR','MSWORK','TUNA','TUNA_OCC','LIQ','TIMBER','MV','MEETLOG','PREDLOG','MYLOG','LEARN','NOTICES','NOW','UPDATED','agOf'];
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
  return {missing:D.__miss||'',builtFrom:D.UPDATED,asOf:iso(D.NOW),calls,waiting,dpr:D.DPR,barge:D.MSWORK,tuna:D.TUNA,tunaDays:D.TUNA_OCC,liquid:D.LIQ,timber:D.TIMBER,moves:D.MV,meetings:D.MEETLOG,predictions:D.PREDLOG,ourLog:D.MYLOG,learn:D.LEARN,circulars:D.NOTICES||[]};
 });
 await b.close(); fs.unlinkSync(tmp);
 if(errs.length){console.error('PAGE ERRORS',errs);process.exit(1);}
 // blocks declared inside a function of the board (not visible at the end of the script): read as plain literals from the source
 const lit=name=>{const a=s.indexOf('const '+name+'=[');if(a<0)return [];const e=s.indexOf('\n];',a);try{return Function('return '+s.slice(a+('const '+name+'=').length,e+2))();}catch(err){console.error(name+' not read: '+err.message);return [];}};
 if(!db.meetings)db.meetings=lit('MEETLOG'); if(!db.predictions)db.predictions=lit('PREDLOG'); db.missing='';
 // THE DATA BOOK KEEPS EVERYTHING: the display board drops sailed vessels, old signal sheets and closed checks — what is no longer on the board stays here from the earlier build.
 const file=path.join(out,'databook.json');
 if(fs.existsSync(file)){const old=JSON.parse(fs.readFileSync(file,'utf8'));
  const merge=(now,was,key,onKeep)=>{const k=new Set((now||[]).map(key));const kept=(was||[]).filter(x=>!k.has(key(x)));if(onKeep)kept.forEach(onKeep);return (now||[]).concat(kept);};
  // A call that was still 'coming' when it left the board never happened as entered — its hour was revised (the new entry is on the board) or the vessel was
  // taken off the programme. It is NOT kept. (Till 23 Nov such forecasts stayed in the book as 'sailed' calls: 14 old versions and one berthing that never took place.)
  db.calls=merge(db.calls,(old.calls||[]).filter(c=>c.status!=='coming'),c=>c.vessel+'|'+c.berth+'|'+c.madeFast,c=>{c.status='sailed';c.outIsEstimate=false;});
  // Older versions of a stay: the same vessel on the same berth with an overlapping stay further down the array. The array is newest-first by construction
  // (board entries, then what the last build had, then what the build before had …), so the first one met is the latest word and the later ones go.
  const VOID=new Set(['Hai Nam 81|14|2026-11-23 19:30']); // entered from programme 23.11 as provisional; CJ-14 went to Lila Tokyo — she never berthed there
  const T=x=>x?Date.parse(x.replace(' ','T')+':00Z'):NaN, keep=[], gone=[], odd=[];
  db.calls.forEach(c=>{const k=c.vessel+'|'+c.berth+'|'+c.madeFast;
   if(VOID.has(k)){gone.push(k+' (never berthed)');return;}
   const ov=y=>y.vessel===c.vessel&&T(c.madeFast)<T(y.out)&&T(y.madeFast)<T(c.out);
   const dup=keep.find(y=>y.berth===c.berth&&ov(y)); if(dup){gone.push(k+' (older version of '+dup.madeFast+')');return;}
   const two=keep.find(y=>y.berth!==c.berth&&ov(y)&&!(y.madeFast===c.madeFast&&y.out===c.out)); if(two)odd.push(k+' overlaps CJ-'+two.berth+' '+two.madeFast); // one vessel lying across two berths has the same hours on both rows — that is not odd
   keep.push(c);});
  if(gone.length)console.log('calls not kept:',gone.length,'—',gone.join(' · '));
  if(odd.length)console.log('LOOK: the same vessel on two berths at once —',odd.join(' · '));
  db.calls=keep;
  db.moves=merge(db.moves,old.moves,m=>m[0]);
  // a sheet still on the board may have been cut to today's rows: keep the fuller copy
  db.moves=db.moves.map(m=>{const o=(old.moves||[]).find(x=>x[0]===m[0]);return (o&&o[1].length>m[1].length)?o:m;});
  db.learn=merge(db.learn,old.learn,l=>l.d); db.meetings=merge(db.meetings,old.meetings,m=>m.d); db.predictions=merge(db.predictions,old.predictions,x=>x.v+'|'+x.predAt+'|'+x.pb+'|'+x.pt);
  db.barge.days=merge(db.barge.days,old.barge&&old.barge.days,d=>d.d); db.tunaDays=merge(db.tunaDays,old.tunaDays,d=>d.d); db.circulars=merge(db.circulars,old.circulars,c=>c.ref+'|'+c.t);
  if(old.liquid&&old.liquid.moves){db.liquid.moves=merge(db.liquid.moves,old.liquid.moves,m=>m[0]).map(m=>{const o=old.liquid.moves.find(x=>x[0]===m[0]);return (o&&o[1].length>m[1].length)?o:m;});}
  db.dprDays=merge([{d:db.dpr.d,asOf:db.dpr.asOf,tot:db.dpr.tot,rows:db.dpr.rows}],old.dprDays,d=>d.d);
 } else db.dprDays=[{d:db.dpr.d,asOf:db.dpr.asOf,tot:db.dpr.tot,rows:db.dpr.rows}];
 fs.mkdirSync(out,{recursive:true}); fs.writeFileSync(file,JSON.stringify(db));
 const st=x=>db.calls.filter(c=>c.status===x).length;
 console.log('databook.json',(JSON.stringify(db).length/1024|0)+' KB · calls',db.calls.length,'(sailed',st('sailed'),'· alongside',st('alongside'),'· coming',st('coming')+') · waiting rows',db.waiting.length,'· moves sheets',db.moves.length,'· barge days',db.barge.days.length,'· meetings',db.meetings.length,'· predictions',db.predictions.length);
})();
