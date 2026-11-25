const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e.stack||e).slice(0,600)));p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text().slice(0,300));});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(2500);console.log(errs.slice(0,4).join('\n---\n')||'no errors');await b.close();})();
