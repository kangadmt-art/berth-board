// usage: node heads.js <abs board> [width] — every heading-like element on every tab: tag/class, computed weight, size, family, whether the display face is really loaded
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const f=process.argv[2];const w=+(process.argv[3]||1280);
const ctx=await b.newContext({viewport:{width:w,height:900}});const p=await ctx.newPage();
const all={};
for(const tab of ['cargo','priority','barge','timber','salt','ppp','tuna','liquid']){
  await p.goto('file://'+f+'#'+tab);await p.waitForTimeout(2300);
  await p.evaluate(()=>{document.querySelectorAll('button').forEach(x=>{if(/^open all$/i.test(x.textContent.trim())&&x.offsetParent)x.click();});});await p.waitForTimeout(500);
  const r=await p.evaluate(()=>{const out={};const fonts=[...document.fonts].map(x=>x.family+' '+x.weight+' '+x.status);
    const walk=(root,pre)=>{root.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)walk(e.shadowRoot,'shadow ');
      const cs=getComputedStyle(e);const isH=/^H[1-6]$/.test(e.tagName)||/Big Shoulders/.test(cs.fontFamily)&&e.childElementCount<4&&(e.textContent||'').trim().length>0&&(e.textContent||'').trim().length<70;
      if(!isH)return;const r=e.getBoundingClientRect();if(r.width===0)return;
      // skip if parent has same family+weight+size (inherited run)
      const ps=e.parentElement?getComputedStyle(e.parentElement):null;if(ps&&!/^H[1-6]$/.test(e.tagName)&&ps.fontFamily===cs.fontFamily&&ps.fontWeight===cs.fontWeight&&ps.fontSize===cs.fontSize)return;
      const key=pre+e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).join('.'):'')+' | '+cs.fontWeight+' | '+Math.round(parseFloat(cs.fontSize))+'px | '+cs.fontFamily.split(',')[0].replace(/"/g,'');
      if(!out[key])out[key]={n:0,eg:(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,38)};out[key].n++;});};
    walk(document,'');return {out,fonts:[...new Set(fonts)].filter(x=>/Big/.test(x))};});
  all[tab]=r;}
const merged={};for(const t in all)for(const k in all[t].out){merged[k]=merged[k]||{n:0,eg:all[t].out[k].eg,tabs:[]};merged[k].n+=all[t].out[k].n;merged[k].tabs.push(t);}
console.log('fonts',JSON.stringify(all.cargo.fonts));
Object.keys(merged).sort((a,b)=>{const wa=+a.split(' | ')[1],wb=+b.split(' | ')[1];return wa-wb||a.localeCompare(b);}).forEach(k=>console.log(k,'| ×'+merged[k].n,'| '+merged[k].tabs.join(','),'| "'+merged[k].eg+'"'));
await b.close();})();
