// usage: node opt.js <abs board> — the board's own "options by priority" for our vessels (window.__OPT), with times
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[2]);await p.waitForTimeout(3000);
const r=await p.evaluate(()=>{const pad=x=>String(x).padStart(2,'0');const iso=t=>{const d=new Date(Date.UTC(2026,9,25,0,0)+t*36e5);return pad(d.getUTCDate())+' '+['','','','','','','','','','Oct','Nov','Dec'][d.getUTCMonth()]+' '+pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());};
 const O=window.__OPT||{};const out={};for(const n in O){out[n]=(O[n]||[]).map(o=>o.label+' → '+(o.r?('CJ-'+o.r.b+' '+iso(o.r.F)+' ['+o.r.cat+']'):'none within the run')+(o.note?' ('+String(o.note).slice(0,60)+')':''));}return out;});
console.log(JSON.stringify(r,null,1));await b.close();})();
