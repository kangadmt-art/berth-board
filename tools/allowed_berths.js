const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[2]);await p.waitForTimeout(3000);
const names=process.argv.slice(3);
const r=await p.evaluate((names)=>{const D=window.__dbg;return names.map(n=>{const w=D.W.find(x=>x.n===n);return n+': '+(w?JSON.stringify(D.allowedBerths(w))+' loa '+w.loa+' dr '+w.dr+' rk '+JSON.stringify(w.rk):'not in W');});},names);
console.log(r.join('\n'));await b.close();})();
