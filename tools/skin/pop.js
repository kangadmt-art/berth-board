// usage: node pop.js <board.html> <outPrefix> [skin] — the theme chooser open, at phone and desktop width; then picks a theme and reloads to prove it is remembered
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const [,, file, out, skin]=process.argv;const b=await chromium.launch();const errs=[];
for(const [tag,w,h] of [['m',390,844],['s',360,740],['d',1280,900]]){
  const ctx=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:tag==='d'?1:2,hasTouch:tag!=='d'});
  if(skin) await ctx.addInitScript(s=>{try{if(!localStorage.getItem('dpaSkin'))localStorage.setItem('dpaSkin',s);}catch(e){}},skin);
  const p=await ctx.newPage();p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+file+'#cargo');await p.waitForTimeout(2600);
  await p.click('#skbtn');await p.waitForTimeout(350);
  await p.screenshot({path:`${out}_${tag}.png`});
  const info=await p.evaluate(()=>{const r=document.getElementById('skpop').getBoundingClientRect();const bt=document.getElementById('skbtn').getBoundingClientRect();return {pop:[r.left,r.top,r.right,r.bottom].map(Math.round),btn:[bt.left,bt.top,bt.width,bt.height].map(Math.round),vw:innerWidth,vh:innerHeight,sw:document.documentElement.scrollWidth,tiles:document.querySelectorAll('.sktile').length,pressed:document.querySelector('.sktile[aria-pressed="true"]')?.textContent};});
  if(tag==='m'){ // pick Dusk, check it applies, reload, check it stays; then Esc closes
    await p.click('.sktile[data-skin-id="dusk"]');await p.waitForTimeout(200);
    const a1=await p.evaluate(()=>[document.documentElement.getAttribute('data-skin'),localStorage.getItem('dpaSkin'),getComputedStyle(document.body).backgroundColor,document.getElementById('skpop').hidden]);
    await p.keyboard.press('Escape');await p.waitForTimeout(100);
    const hid=await p.evaluate(()=>document.getElementById('skpop').hidden);
    await p.reload();await p.waitForTimeout(1500);
    const a2=await p.evaluate(()=>[document.documentElement.getAttribute('data-skin'),getComputedStyle(document.body).backgroundColor]);
    await p.click('#skbtn');await p.waitForTimeout(200);await p.click('.sktile[data-skin-id=""]');await p.waitForTimeout(200);
    const a3=await p.evaluate(()=>[document.documentElement.getAttribute('data-skin'),localStorage.getItem('dpaSkin'),getComputedStyle(document.body).backgroundColor]);
    console.log('pick dusk',JSON.stringify(a1),'esc closes',hid,'after reload',JSON.stringify(a2),'back to default',JSON.stringify(a3));
  }
  console.log(tag,JSON.stringify(info));
  await ctx.close();}
console.log('errs',errs.length,errs.slice(0,3));await b.close();})();
