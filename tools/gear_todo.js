// GEAR backlog: which vessels on the board have their gear found online, which were searched without a result, and which are still to be searched.
// Usage: node tools/gear_todo.js /abs/path/board.html
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+path.resolve(process.argv[2])+'#priority');await p.waitForTimeout(2600);
const g=await p.evaluate(()=>window.__GEAR);console.log('found ('+g.found.length+'):',g.found.join(' · '));console.log('searched, not stated ('+g.none.length+'):',g.none.join(' · '));console.log('TO SEARCH ('+g.todo.length+'):',g.todo.join(' · '));await b.close();})();
