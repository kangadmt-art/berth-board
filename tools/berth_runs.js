const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[2]);await p.waitForTimeout(3000);
const r=await p.evaluate(()=>{const pad=x=>String(x).padStart(2,'0');const iso=t=>{const d=new Date(Date.UTC(2026,9,25,0,0)+t*36e5);return pad(d.getUTCDate())+'/'+pad(d.getUTCMonth()+1)+' '+pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());};
 const D=window.__dbg, NOW=D.h('11-27 10:20'), out=[];
 const all=D.V.filter(v=>v.T>NOW&&v.cat!=='SPACE').map(v=>({b:v.b,n:v.n,F:v.F,T:v.T,cat:v.cat,via:v.via||'',k:'V'})).concat(window.__S.map(s=>({b:s.b,n:s.n,F:s.F,T:s.T,cat:s.cat,via:s.via||'',k:'S'})));
 const bs=[...new Set(all.map(x=>x.b))].sort((a,z)=>parseFloat(a)-parseFloat(z));
 for(const bb of bs){const l=all.filter(x=>x.b===bb).sort((a,z)=>a.F-z.F);out.push('CJ-'+bb+': '+l.map(x=>x.n.replace(/ \(.*$/,'')+' ['+x.cat+(x.via?'*':'')+'] '+iso(Math.max(x.F,NOW))+'→'+iso(x.T)).join('  |  '));}
 return out;});
console.log(r.join('\n'));await b.close();})();
