const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const f=process.argv[2];
for(const tab of (process.argv[3]||'priority').split(',')){
  const ctx=await b.newContext({viewport:{width:390,height:844}});const p=await ctx.newPage();
  await p.goto('file://'+f+'#'+tab);await p.waitForTimeout(2200);
  const r=await p.evaluate(()=>{const W=innerWidth;const out=[];const walk=(root,pre)=>{root.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)walk(e.shadowRoot,pre+'#shadow ');const r=e.getBoundingClientRect();if(r.width>0&&r.right>W+1&&getComputedStyle(e).position!=='fixed'){let clipped=false;let a=e.parentElement||(e.getRootNode().host);while(a&&a!==document.documentElement){const o=getComputedStyle(a);if(/(auto|scroll|hidden|clip)/.test(o.overflowX)){clipped=true;break;}a=a.parentElement||(a.getRootNode&&a.getRootNode().host);}if(!clipped)out.push(pre+e.tagName+'.'+String(e.className).slice(0,30)+' r='+Math.round(r.right)+' w='+Math.round(r.width)+' "'+(e.textContent||'').trim().slice(0,40)+'"');}});};walk(document,'');return {sw:document.documentElement.scrollWidth,n:out.length,out:out.slice(0,10)};});
  console.log(tab,JSON.stringify(r,null,1));await ctx.close();}
await b.close();})();
