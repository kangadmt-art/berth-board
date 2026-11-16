// Dump every waiting / expected vessel as the projection sees her: Sr No 7 flag, ranks, readiness, reporting time, ALLOWED BERTHS, HP status.
// Run it after editing waiting rows - a berth word in a note can change a vessel's allowed berths (handover §6, "Waiting-row notes are parsed").
// Usage: node tools/waiting_dump.js /abs/path/board.html
const {chromium}=require('playwright');const path=require('path');
const file=path.resolve(process.argv[2]);
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+file);await p.waitForTimeout(2200);
const r=await p.evaluate(()=>{const f=window.__fmt;const {W,allowedBerths}=window.__dbg;const Q=w=>!!w.q7||/30\s*K\s*[\/.]\s*25\s*K/i.test(w.x||'');
 return W.map(w=>[w.n,Q(w)?'Q7':'',JSON.stringify(w.rk),w.rdy!=null?f(w.rdy):'N/A',w.rep!=null?f(w.rep):'-','['+allowedBerths(w).join(',')+']',w.noHP?'noHP':''].join(' | '));});
r.forEach(x=>console.log(x));await b.close();})();
