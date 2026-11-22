// Print the next-meeting section as data — one line per berth: status (K = khali, C = continue, S = space too short), who leaves, the priority she
// holds, and the names shown: same priority · a higher priority waiting · the one after.
// Run it on the board as it stood BEFORE the programme was applied (the bak file) to score the section:
// was the vessel that got the berth among the names — and in which group?   Usage: node tools/meeting_board.js /abs/path/board.html
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+path.resolve(process.argv[2]));await p.waitForTimeout(2400);
const m=await p.evaluate(()=>window.__MEETB||null);if(!m){console.log('no meeting section on this board');await b.close();return;}
console.log('// meeting '+m.meet+' · window to '+m.end+' · board as at '+m.at);
const g=(t,x)=>x?t+' '+x.pr+': '+(x.ch.join(', ')||'-'):'';
for(const r of m.rows)console.log(['CJ-'+r.b,r.st,r.out?r.out+' ['+r.hold+']':'-',r.t||'-',g('SAME',r.same),...(r.up||[]).map(x=>g('UP',x)),g('NEXT',r.next)].filter(Boolean).join(' | '));
await b.close();})();
