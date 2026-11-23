// usage: node full.js <board.html> <outPrefix> <skin|-> <tab> [width] — full-page shot with every section opened
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const [,, file, out, skin, tab, w0]=process.argv;const w=+(w0||390);const b=await chromium.launch();const errs=[];
  const ctx=await b.newContext({viewport:{width:w,height:900},deviceScaleFactor:1});
  if(skin&&skin!=='-') await ctx.addInitScript(s=>{try{localStorage.setItem('dpaSkin',s);}catch(e){}},skin);
  const p=await ctx.newPage();p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+file+'#'+tab);await p.waitForTimeout(2600);
  const n=await p.evaluate(()=>{let k=0;document.querySelectorAll('button').forEach(x=>{if(/^open all$/i.test(x.textContent.trim())&&x.offsetParent){x.click();k++;}});document.querySelectorAll('details').forEach(d=>{ if(d.offsetParent&&!d.open&&d.closest('header')==null&&k<1){} });return k;});
  await p.waitForTimeout(900);
  await p.screenshot({path:`${out}.png`,fullPage:true});
  console.log('openall',n,'errs',errs.length,errs.slice(0,3));await b.close();})();
