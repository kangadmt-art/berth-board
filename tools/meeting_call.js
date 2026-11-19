// Freeze the board's MEETING CALL — the vessels its meeting preview names for the meeting still to come — as a MEETLOG entry.
// Run it on the board as it stands BEFORE a new programme is applied; paste the printed entry at the TOP of MEETLOG and then
// fill prog / got / note from that programme (see handover/HANDOVER.md, "Accuracy — meeting call vs programme").
// Usage: node tools/meeting_call.js /abs/path/board.html ['basis text']
//        node tools/meeting_call.js /abs/path/old_board.html 'basis' 'MM-DD HH:MM'   (an older version without window.__CALL: give the window end)
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+path.resolve(process.argv[2]));await p.waitForTimeout(2400);
const end=process.argv[4]||'';
const c=await p.evaluate(end=>{if(window.__CALL&&!end)return window.__CALL;
  const S=window.__S,pad=x=>String(x).padStart(2,'0'),iso=t=>{if(t==null)return '';const d=new Date(Date.UTC(2026,9,25,0,0)+t*36e5);return pad(d.getUTCMonth()+1)+'-'+pad(d.getUTCDate())+' '+pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());}; // hour 0 = 25 Oct 2026 00:00 IST
  const fa=x=>x.freeAt!=null?x.freeAt:x.prevAt;
  return {d:'??-??',at:'',end,call:S.filter(x=>!x.shifted&&fa(x)!=null&&iso(fa(x))<=end).map(x=>[x.n.replace(/\s*\(.*\)\s*$/,''),String(x.b)])};},end);
const q=s=>s.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
console.log("// meeting "+c.d+" · window to "+c.end+" · "+c.call.length+" vessel(s)"+(c.pend?' · meeting held, programme awaited':''));
console.log(" {d:'"+c.d+"',at:'"+c.at+"',basis:'"+q(process.argv[3]||'')+"',prog:'',\n  call:["+c.call.map(x=>"['"+q(x[0])+"','"+x[1]+"']").join(',')+"],\n  got:[],\n  note:''},");
await b.close();})();
