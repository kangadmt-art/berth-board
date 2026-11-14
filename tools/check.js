// Validate a board file before publishing.
// Usage: node tools/check.js /abs/path/board.html [--mine] [--demur] [--meeting] [--all]
// Prints: script syntax, "},," count, page errors, undefined/NaN tokens on the three tabs (every section opened),
// DPR / overrun flags, the projection S, the own-vessel options, and optionally the Mihir & Co card, demurrage table, meeting preview.
// Exit code 1 if anything is wrong. Needs playwright (preinstalled under /opt/npm-tools in this environment).
const fs=require('fs'),vm=require('vm'),path=require('path');
const file=path.resolve(process.argv[2]||'index.html');const want=f=>process.argv.includes(f)||process.argv.includes('--all');
let bad=0;
const html=fs.readFileSync(file,'utf8');
{const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,i=0;while((m=re.exec(html))){i++;try{new vm.Script(m[1]);}catch(e){bad++;console.log('SCRIPT',i,'SYNTAX ERROR:',e.message);}}
 const dc=(html.match(/\},,/g)||[]).length;if(dc){bad++;}console.log('scripts:',i,'| "},," occurrences:',dc);}
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1100}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+file);await p.waitForTimeout(2500);
const oa=await p.$('text=Open all');if(oa){await oa.click();await p.waitForTimeout(900);}
const scan=()=>p.evaluate(()=>{const t=document.body.innerText;const out=[];const re=/undefined|NaN|\[object/g;let m;while((m=re.exec(t)))out.push(t.slice(Math.max(0,m.index-140),m.index+40).replace(/\n/g,' ⏎ '));return out;});
const main=await scan();
const r=await p.evaluate(()=>{const S=window.__S||[];const f=window.__fmt;const V=(window.__dbg||{}).V||[];const g=id=>(document.getElementById(id)||{}).innerText||'';
 const flags=V.filter(v=>v.dpr||v.overrun||v.overstay).map(v=>v.n+' CJ-'+v.b+(v.dpr?' DPR→'+f(v.T):'')+(v.overrun?' OVERRUN→'+f(v.overrun):'')+(v.overstay?' OVERSTAY':''));
 const sp=S.map(x=>[x.n,'CJ-'+x.b,f(x.F),f(x.T),x.cat,x.via||'',x.shifted?'SHIFTED':''].join(' | '));
 const opt={};for(const n in (window.__OPT||{}))opt[n]=window.__OPT[n].map(o=>o.label+' → '+(o.r?'CJ-'+o.r.b+' '+f(o.r.F)+' to '+f(o.r.T)+' ['+o.r.cat+(o.r.via?' via '+o.r.via:'')+']':'none'));
 return {flags,sp,opt,upd:(document.querySelector('.upd')||{}).innerText||'',mine:g('mine'),demur:g('demur'),mpsub:g('mpsub'),mpt:g('mpt')};});
const tabs={};for(const v of ['liquid','tuna']){const a=await p.$(`a[data-view="${v}"]`);if(a){await a.click();await p.waitForTimeout(700);tabs[v]=await scan();}}
console.log('page errors:',JSON.stringify(errs));console.log(r.upd.replace(/\n/g,' '));
console.log('bad tokens — cargo tab:',main.length,'| liquid:',(tabs.liquid||[]).length,'| tuna:',(tabs.tuna||[]).length);
[...main,...(tabs.liquid||[]),...(tabs.tuna||[])].forEach(x=>console.log('  BAD: …'+x+'…'));
console.log('--- flags');r.flags.forEach(x=>console.log(' ',x));
console.log('--- projection S (vessel | berth | alongside | completes | group | via)');r.sp.forEach(x=>console.log(' ',x));
console.log('--- own-vessel options');console.log(JSON.stringify(r.opt,null,1));
if(want('--mine')){console.log('--- Mihir & Co card');console.log(r.mine);}
if(want('--demur')){console.log('--- timber demurrage');console.log(r.demur.replace(/\n\s+/g,' | '));}
if(want('--meeting')){console.log('--- meeting preview');console.log(r.mpsub);console.log(r.mpt.replace(/\n\s*\n/g,'\n'));}
await b.close();
if(errs.length||main.length||(tabs.liquid||[]).length||(tabs.tuna||[]).length)bad++;
if(bad){console.log('\nNOT OK — fix before publishing');process.exit(1);}console.log('\nOK');})();
