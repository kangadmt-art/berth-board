// usage: node shots.js <board.html> <outPrefix> [skin] — screenshots of the main tabs at phone and desktop width
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const [,, file, out, skin]=process.argv;const b=await chromium.launch();const errs=[];
for(const [tag,w,h] of [['m',390,844],['d',1280,900]]){
  const ctx=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:tag==='m'?2:1});
  if(skin) await ctx.addInitScript(s=>{try{localStorage.setItem('dpaSkin',s);}catch(e){}},skin);
  const p=await ctx.newPage();p.on('pageerror',e=>errs.push(String(e)));
  for(const v of (process.env.TABS||'cargo,priority,salt,timber,liquid,tuna,barge,ppp').split(',')){
    await p.goto('file://'+file+'#'+v);await p.waitForTimeout(v==='cargo'?2600:1900);
    await p.screenshot({path:`${out}_${tag}_${v}.png`,fullPage:false});
    if(process.env.FULL) await p.screenshot({path:`${out}_${tag}_${v}_full.png`,fullPage:true});
  }
  await ctx.close();}
console.log('errs',errs.length,errs.slice(0,3));await b.close();})();
