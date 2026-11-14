// Export the board's projection (window.__S) as JSON with 'MM-DD HH:MM' times - used to build the PRED snapshot and PREDLOG rows.
// Usage: node tools/dump_projection.js /abs/path/board.html out.json
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const file=path.resolve(process.argv[2]),out=process.argv[3]||'S.json';
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+file);await p.waitForTimeout(2200);
const r=await p.evaluate(()=>{const S=window.__S;const pad=x=>String(x).padStart(2,'0');
 const iso=t=>{const d=new Date(Date.UTC(2026,9,25,0,0)+t*36e5);return pad(d.getUTCMonth()+1)+'-'+pad(d.getUTCDate())+' '+pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());}; // hour 0 = 25 Oct 2026 00:00 IST
 return S.map(x=>({n:x.n,b:x.b,F:iso(x.F),T:iso(x.T),cat:x.cat,via:x.via||'',shifted:!!x.shifted,prev:x.prev||''}));});
fs.writeFileSync(out,JSON.stringify(r,null,1));r.forEach(x=>console.log([x.n,x.b,x.F,x.T,x.cat,x.via].join(' | ')));await b.close();})();
