// usage: node labels.js <abs board> [width] — table headers and small upper-case labels on every tab, with computed weight
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const f=process.argv[2];const w=+(process.argv[3]||1280);
const ctx=await b.newContext({viewport:{width:w,height:900}});const p=await ctx.newPage();const merged={};
for(const tab of ['cargo','priority','barge','timber','salt','ppp','tuna','liquid']){
  await p.goto('file://'+f+'#'+tab);await p.waitForTimeout(2300);
  await p.evaluate(()=>{document.querySelectorAll('button').forEach(x=>{if(/^open all$/i.test(x.textContent.trim())&&x.offsetParent)x.click();});document.querySelectorAll('details').forEach(d=>{if(!d.closest('header'))d.open=true;});});await p.waitForTimeout(600);
  const r=await p.evaluate(()=>{const out={};
    const walk=(root,pre)=>{root.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)walk(e.shadowRoot,'shadow ');
      const cs=getComputedStyle(e);const r=e.getBoundingClientRect();if(r.width===0||e.closest('header'))return;
      const own=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim().length>1);
      const isTh=e.tagName==='TH';const isLab=own&&cs.textTransform==='uppercase'&&parseFloat(cs.fontSize)<=14&&!/^(H1|H2|BUTTON|A)$/.test(e.tagName)&&!e.closest('button,a,nav,svg');
      if(!isTh&&!isLab)return;
      let par=e.parentElement,pc='';while(par&&!pc){if(par.className&&typeof par.className==='string'&&par.className.trim())pc=par.className.trim().split(/\s+/)[0];par=par.parentElement;}
      const key=pre+(isTh?'TH':'LAB')+' '+e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).join('.'):'')+' in .'+pc+' | '+cs.fontWeight+' | '+Math.round(parseFloat(cs.fontSize)*10)/10+'px | '+cs.fontFamily.split(',')[0].replace(/"/g,'')+' | '+cs.color;
      if(!out[key])out[key]={n:0,eg:(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,34)};out[key].n++;});};
    walk(document,'');return out;});
  for(const k in r){merged[k]=merged[k]||{n:0,eg:r[k].eg,tabs:[]};merged[k].n+=r[k].n;merged[k].tabs.push(tab);}}
Object.keys(merged).sort().forEach(k=>console.log(k,'| ×'+merged[k].n,'|',merged[k].tabs.join(','),'| "'+merged[k].eg+'"'));
await b.close();})();
