// Print the MEETING page as data — one line per berth: status (K = khali, C = continue, S = space too short), who leaves and when,
// the priority the board expects there, the chance names, the HP bid pool and the possible shift.
// Run it on the board as it stood BEFORE the programme was applied (the bak file) to score the page:
// was the vessel that got the berth in the chance list / the HP pool?   Usage: node tools/meeting_board.js /abs/path/board.html
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+path.resolve(process.argv[2]));await p.waitForTimeout(2400);
const m=await p.evaluate(()=>window.__MEETB||null);if(!m){console.log('no meeting page on this board');await b.close();return;}
console.log('// meeting '+m.meet+' · window to '+m.end+' · board as at '+m.at);
for(const r of m.rows)console.log(['CJ-'+r.b,r.st,r.out||'-',r.t||'-',r.pr+(r.via?' ('+r.via+')':''),'chance: '+(r.ch.join(', ')||'-'),r.hp.length?'HP pool: '+r.hp.join(', '):'',r.sh.length?'shift: '+r.sh.join(' / '):'',r.cond?'ONLY IF '+r.cond:'',r.alt?'else '+r.alt.pr+': '+r.alt.ch.join(', '):'',r.back?'or '+r.back.pr+': '+r.back.ch.join(', '):''].filter(Boolean).join(' | '));
await b.close();})();
