#!/usr/bin/env python3
# apply26 — v180: accuracy made simple (Mihir, 19 Nov 23:08): before the berthing meeting the board names the vessels it expects to get a berth;
# when the programme comes, how many of them did. One card a meeting. The earlier berth-and-time table stays behind a "Detail" fold. argv[1] = UPDATED.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v179.html')
B = Board(P)
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % sys.argv[1] + B.s[m.end():]

# ---- styles
B.rep(".score-sum{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:10px}",
 ".mc-sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:2px 0 12px}.mc-sum div{background:var(--panel2,rgba(255,255,255,.04));border:1px solid var(--line2);border-top:3px solid var(--sc,var(--line2));border-radius:8px;padding:10px 12px}.mc-sum b{display:block;font-family:var(--f-disp);font-size:30px;line-height:1.05}.mc-sum b small{font-size:15px;color:var(--muted);font-weight:400}.mc-sum span{display:block;color:var(--muted);font-size:12px;margin-top:3px}"
 ".mc-day{border:1px solid var(--line2);border-radius:8px;padding:10px 12px 11px;margin-top:8px;background:var(--panel2,rgba(255,255,255,.04))}.mc-day.open{border-color:var(--brass);background:rgba(217,178,95,.06)}.mc-day.nocall{opacity:.75}"
 ".mc-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px}.mc-head b{font-family:var(--f-disp);font-size:18px;text-transform:uppercase;letter-spacing:.02em}.mc-head small{color:var(--muted);font-size:11.5px}.mc-score{font-family:var(--f-disp);font-size:24px;white-space:nowrap}.mc-score small{font-size:13px;color:var(--muted)}"
 ".mc-row{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:8px}.mc-row>i{font-style:normal;color:var(--muted);font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;flex:0 0 100%}"
 ".mc-chip{display:inline-flex;gap:5px;align-items:baseline;border:1px solid var(--line2);border-radius:999px;padding:3px 10px;font-size:13px;white-space:nowrap}.mc-chip small{color:var(--muted);font-size:11px}.mc-chip.y{border-color:rgba(95,191,122,.6);background:rgba(95,191,122,.13);color:#9be3b0}.mc-chip.n{border-color:rgba(229,99,106,.5);background:rgba(229,99,106,.09);color:#f3a7ab}.mc-chip.x{color:var(--muted)}.mc-chip.me{box-shadow:0 0 0 1px var(--brass)}.mc-note{color:var(--muted);font-size:12px;margin-top:8px;line-height:1.45}"
 ".score-sum{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:10px}")

# ---- section markup: the simple card on top, the earlier measure folded under it
a, b = B.line_of('    <div class="sechead"><h2 id="sch">Accuracy · berthing predictions</h2>')
old = B.s[a:b]
m2 = re.search(r"<p>(<b>Mihir's measure \(13 Nov\):</b>.*)</p></div>$", old); assert m2, 'old intro'
B.s = B.s[:a] + ('    <div class="sechead"><h2 id="sch">Accuracy · meeting call vs programme</h2><p><b>Mihir\'s measure (19 Nov):</b> before each day\'s berthing meeting the board names the vessels it expects to get a berth. When the programme comes, every name gets a <b style="color:#9be3b0">✓</b> or a <b style="color:#f3a7ab">✗</b> — that is the score.</p></div>\n'
  '    <div id="mscore"></div>\n'
  '    <details style="margin-top:14px"><summary style="cursor:pointer;color:var(--muted);font-size:12.5px">Detail · berth and time of every single prediction (the earlier measure)</summary><p style="color:var(--muted);font-size:12.5px;margin:8px 0 10px">' + m2.group(1).replace("<b>Mihir's measure (13 Nov):</b>", "<b>Earlier measure (13 Nov):</b>") + '</p>') + B.s[b:]
B.rep('    <div id="score"></div>\n  </section>', '    <div id="score"></div></details>\n  </section>')

# ---- data + renderer
B.rep("function renderPredlog(){", r"""// ===== MEETING CALL vs PROGRAMME — Mihir's accuracy measure (19 Nov 23:08) =====
// "Before the berthing meeting we say: today these 5 vessels will berth. Against that — how many did, once the programme has come."
// One entry a berthing meeting, NEWEST FIRST.
//  at / basis = the board's data time and sheets behind the call · prog = the programme that answers it
//  call = the vessels the board's meeting preview named BEFORE that programme reached the board — [vessel, berth the board said]
//         (projection rows whose berth frees by 18:00 of the day after the meeting; port-convenience shifts are not calls).
//         null = the board was not updated between the two programmes, so there was no call and the day is not scored.
//  got  = the vessels that got a berth in that meeting's window — the INWARD column of the programme at the dry-cargo berths
//         (no shifts / warps, no container berths CJ-11 / CJ-12, no tug-and-barge), plus a berthing given by a signal inside the
//         window: [vessel, berth, 'signal']. A programmed vessel later known NOT to have berthed is taken out and named in the note.
// The call of the meeting still to come is not stored here: it is read live from the projection (see renderMeetlog) and frozen
// into this list with `node tools/meeting_call.js <board.html>` BEFORE the next programme is applied.
const MEETLOG=[
 {d:'11-19',at:'11-19 12:29',basis:'DPR 19.11 · list 18.11 · programme 19.11',prog:'20.11',
  call:[['Ken Ann','14'],['AG Varvara','5'],['Safi Alfa','4'],['Sea Postman','6']],
  got:[['Belmoira','15'],['Ken Ann','5'],['Katerina K','6'],['Nord Copper','14'],['African Hornbill','16','signal']],
  note:'Belmoira took a Govt place on her 30K quote and Katerina K a provisional berth; African Hornbill came in by the evening signal after Ocean Kudos\' holds were rejected. The two General vessels the board named were passed over.'},
 {d:'11-18',at:null,basis:'',prog:'19.11',call:null,
  got:[['DSM London','2'],['Meghna Prestige','7'],['Sea Gautham','3'],['Heng Yuan Fa Zhan','15A']],
  note:'No call — no sheets reached the board on 17 or 18 Nov, so this day is not scored. Ocean Kudos was programmed for CJ-16 and did not berth (holds rejected).'},
 {d:'11-17',at:'11-16 18:17',basis:'list 16.11 · programme 17.11 — made the evening before, no sheets on 17 Nov',prog:'18.11',
  call:[['Safi Alfa','14'],['AG Varvara','4'],['Yara J','2'],['Aboudi D','3']],
  got:[['Seacon Monaco','9'],['Yara J','14'],['Rome Trader','13'],['ML Egret','15','signal']],
  note:'The programme printed Rome Trader at CJ-15 and Pioneer Fortune at CJ-10: Rome Trader berthed at CJ-13, ML Egret took CJ-15 by signal, Pioneer Fortune did not berth.'},
 {d:'11-16',at:'11-15 20:54',basis:'night signal 15 Nov · programme 16.11 — no DPR or list of 16 Nov before the programme',prog:'17.11',
  call:[['Pioneer Fortune','4'],['Saga Viking','1'],['Vishva Bandhan','7'],['Gokova-M','8'],['Rome Trader','14'],['HN Doris','13'],['Propel Confidence','16']],
  got:[['New Bliss','1'],['Bristol','15A'],['Phoenix Coral','4'],['Saga Viking','5'],['Propel Confidence','7'],['Vishva Bandhan','8'],['HN Doris','16']],
  note:'Four of the seven named got a berth — each at a different berth from the one the board gave. New Bliss (6.5K), Bristol (HP quote) and Phoenix Coral (24 hrs) were not named.'},
 {d:'11-15',at:'11-15 10:50',basis:'DPR 15.11 · list 14.11',prog:'16.11',
  call:[['Evangelia D','16'],['Rahma','14'],['Deniz ID','2'],['Saga Viking','5']],
  got:[['Rahma','15A'],['Honor Star','9'],['Evangelia D','16']],
  note:'The two General vessels named (Deniz ID, Saga Viking) did not get a berth; Honor Star went to the GFPL berth.'},
 {d:'11-14',at:'11-14 10:15',basis:'DPR 14.11 · list 13.11',prog:'15.11',
  call:[['Sea Gautham','5'],['Xin Hai Tong 71','15'],['Rahma','14']],
  got:[['Truong Minh Dream','6'],['African Hornbill','4']],
  note:'The port gave CJ-6 to Truong Minh Dream (Govt) and CJ-4 to African Hornbill (24 hrs); none of the three named berthed.'},
 {d:'11-13',at:'11-13 09:30',basis:'DPR 13.11 · list 12.11',prog:'14.11',
  call:[['Rahma','15'],['Gokova-M','7'],['CD Cherry','5'],['Saga Viking','2']],
  got:[['Princess Joanna','6'],['Cape Venture','7'],['CD Cherry','15','signal']],
  note:'The programme printed CD Glory at CJ-15 under 24 hrs; CD Cherry berthed there by the night-sheet amendment.'},
 {d:'11-12',at:'11-12 11:00',basis:'DPR 12.11 · list 11.11',prog:'13.11',
  call:[['Drake Well','15'],['Heng Yuan Fa Zhan','15A'],['Gokova-M','8'],['Saga Viking','7'],['CD Cherry','5'],['Rahma','15A']],
  got:[['Drake Well','1'],['Chang Hang','7'],['Merchia','8'],['Karpathos Dawn','15']],
  note:'Chang Hang (HP), Merchia (Coastal) and Karpathos Dawn (24 hrs) took the berths the board had given to General and Steel vessels.'},
 {d:'11-11',at:'11-11 12:00',basis:'DPR 11.11 · list 11.11',prog:'12.11',
  call:[['Drake Well','16']],
  got:[['Leya','9'],['Cape Diversity','16']],
  note:'CJ-16 went to Cape Diversity (pellets, HP) instead of Drake Well; Leya went to the GFPL berth.'}
];
function renderMeetlog(){
  const el=document.getElementById('mscore'); if(!el) return;
  const bl=b=>b?(/^OJ|^TT/.test(b)?b:'CJ-'+b):'', clean=n=>n.replace(/\s*\(.*\)\s*$/,''), dayOf=d=>fday(h(d+' 12:00'));
  const pad=x=>String(x).padStart(2,'0'), iso=t=>{const d=dt(t);return pad(d.getUTCMonth()+1)+'-'+pad(d.getUTCDate())+' '+pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());};
  const rows=MEETLOG.map(m=>{const got=new Map(m.got.map(g=>[g[0],g])), named=new Set((m.call||[]).map(c=>c[0]));
    const call=m.call?m.call.map(c=>({n:c[0],b:c[1],g:got.get(c[0])||null})):null;
    return {...m,callR:call,hit:call?call.filter(c=>c.g).length:0,extra:m.got.filter(g=>!named.has(g[0]))};});
  const sc=rows.filter(r=>r.callR), C=sc.reduce((a,r)=>a+r.callR.length,0), H=sc.reduce((a,r)=>a+r.hit,0), K=sc.reduce((a,r)=>a+r.got.length,0);
  const BR=sc.reduce((a,r)=>a+r.callR.filter(c=>c.g&&c.g[1]===c.b).length,0), pc=(a,b)=>b?Math.round(100*a/b)+'%':'—';
  // the call for the meeting still to come — the same rows as the meeting preview, read live from the projection
  const fa=x=>x.freeAt!=null?x.freeAt:x.prevAt, end=NXM-11+24+18;
  const live=S.filter(x=>x.proj&&!x.shifted&&x.prevAt!=null&&fa(x)<=end).sort((a,z)=>fa(a)-fa(z));
  window.__CALL={d:iso(NXM).slice(0,5),at:iso(NOW),end:iso(end),pend:PEND,call:live.map(x=>[clean(x.n),String(x.b)])};
  const chip=(cls,mark,n,sm)=>`<span class="mc-chip ${cls}${isMine(n)?' me':''}">${mark?'<b>'+mark+'</b>':''}${n}${sm?' <small>'+sm+'</small>':''}</span>`;
  const openCard=`<div class="mc-day open"><div class="mc-head"><div><b>${fday(NXM)} meeting</b> <small>· ${PEND?'held — programme awaited':'still to come'} · window to ${fday(end)} 18:00</small></div><div class="mc-score"><small>open</small></div></div>
    <div class="mc-row"><i>Board says these ${live.length||''} will get a berth</i>${live.length?live.map(x=>chip('',' ',clean(x.n),bl(x.b))).join(''):'<span class="mc-chip x">no berth frees for a waiting vessel in this window</span>'}</div>
    <div class="mc-note">Scored when the next programme comes. The call can still change if a new DPR, list or signal reaches the board before that.</div></div>`;
  const card=r=>`<div class="mc-day${r.callR?'':' nocall'}"><div class="mc-head"><div><b>${dayOf(r.d)} meeting</b> <small>· programme ${r.prog}</small></div><div class="mc-score">${r.callR?`<b style="color:${r.hit*2>=r.callR.length?'#9be3b0':'#f3a7ab'}">${r.hit}</b> <small>of ${r.callR.length} berthed</small>`:'<small>no call</small>'}</div></div>
    ${r.callR?`<div class="mc-row"><i>Board said these ${r.callR.length} will berth</i>${r.callR.map(c=>c.g?chip('y','✓',c.n,bl(c.g[1])+(c.g[1]!==c.b?' · board said '+bl(c.b):'')+(c.g[2]?' · by signal':'')):chip('n','✗',c.n,'')).join('')}</div>`:''}
    <div class="mc-row"><i>${r.callR?'Port also berthed — not named by the board':'Port berthed'}</i>${r.extra.length?r.extra.map(g=>chip('x','',g[0],bl(g[1])+(g[2]?' · by signal':''))).join(''):'<span class="mc-chip x">none</span>'}</div>
    <div class="mc-note">${r.at?'Call made '+fmt(h(r.at))+' · '+r.basis+'. ':''}${r.note}</div></div>`;
  el.innerHTML=`<div class="mc-sum">
    <div style="--sc:${H*2>=C?'var(--ok,#5fbf7a)':'#e5636a'}"><b>${H} <small>of ${C}</small></b><span><b style="display:inline;font:inherit;color:var(--text,#e8edf2)">${pc(H,C)}</b> · vessels the board named that got a berth</span></div>
    <div><b>${H} <small>of ${K}</small></b><span><b style="display:inline;font:inherit;color:var(--text,#e8edf2)">${pc(H,K)}</b> · vessels the port berthed that the board had named</span></div>
    <div><b>${BR} <small>of ${H}</small></b><span>of those, at the berth the board said</span></div>
    <div><b>${sc.length}</b><span>meetings scored · ${fday(h(sc[sc.length-1].d+' 12:00')).replace(/^\S+ /,'')} to ${fday(h(sc[0].d+' 12:00')).replace(/^\S+ /,'')}</span></div></div>
  ${openCard}${rows.map(card).join('')}`;
}
function renderPredlog(){""")
B.rep("\nrenderPredlog();renderScore();\n", "\nrenderPredlog();renderScore();renderMeetlog(); // these three sit inside learn(), which runs after the projection S exists\n")
B.rep("<div>New 19 Nov 22:55 (Mihir): a BARGE tab", "<div>New 19 Nov 23:08 (Mihir): Accuracy made simple — before each meeting the board names the vessels it expects to berth; when the programme comes, how many did (one card a meeting, 11–19 Nov backfilled from the board's own saved versions) · New 19 Nov 22:55 (Mihir): a BARGE tab")
B.save()
