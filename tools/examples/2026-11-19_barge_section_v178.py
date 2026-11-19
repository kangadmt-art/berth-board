#!/usr/bin/env python3
# apply24 — v178: MIDSTREAM · BARGE WORK section (Mihir, 19 Nov 22:49: "vessel working with barge" and "daily barge discharge and loading"), from the DPR. argv[1] = UPDATED.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v177.html')
B = Board(P)
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % sys.argv[1] + B.s[m.end():]
days = open(W + 'barge_days.txt', encoding='utf-8').read().rstrip().rstrip(',')
B.rep("""    <div class="scroll"><table class="mpt dprt" id="dpr"></table></div>
  </section>
""", """    <div class="scroll"><table class="mpt dprt" id="dpr"></table></div>
  </section>

  <section class="card" data-sec="msb" aria-labelledby="bgh">
    <div class="sechead"><h2 id="bgh">Midstream · barge work</h2><p id="bgsub"></p></div>
    <div class="stats" id="bgstats" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))"></div>
    <div class="scroll"><table class="mpt" id="bgday" style="min-width:560px"></table></div>
    <div class="scroll" style="margin-top:14px"><table class="mpt" id="bgves" style="min-width:700px"></table></div>
  </section>
""")
B.rep("// ---- DPR: DPA Traffic Dept \"Daily Performance Report\"",
"""// ---- MIDSTREAM · BARGE WORK (since v178; Mihir, 19 Nov 22:49: "vessel working with barge" and "daily barge discharge and loading").
// One entry a DPR, NEWEST FIRST. Each row is a vessel worked by barges, as the DPR prints her ship-side row (MS / MRG n): ie IMP = discharge into barges,
// EXP = loading from barges; l24 / upto / bal in MT; shore = the shore points where her barges loaded that day; sts = ship-to-ship pairs, which are not barge work.
// Make the entry with:  python3 -I tools/barge_from_dpr.py <dpr.txt> DD.MM 'MM-DD 07:00'   and paste it at the top of days.
const MSWORK={days:[
""" + days + """
]};
// ---- DPR: DPA Traffic Dept "Daily Performance Report\"""")
B.rep("function dpr(){\n", r"""function msWork(){
  const sub=document.getElementById('bgsub'),st=document.getElementById('bgstats'),td=document.getElementById('bgday'),tv=document.getElementById('bgves');if(!td||!MSWORK.days.length)return;
  const sum=(d,ie)=>d.rows.filter(r=>r.ie===ie).reduce((a,r)=>a+r.l24,0);
  const D=MSWORK.days.map(d=>({d,dis:sum(d,'IMP'),load:sum(d,'EXP'),n:d.rows.filter(r=>r.l24>0).length})), mx=Math.max(...D.map(x=>x.dis+x.load),1);
  const tile=(c,v,l)=>`<div class="stat" style="--sc:${c};cursor:default"><div class="v" style="font-size:26px">${v}</div><div class="l">${l}</div></div>`;
  let cur=0;
  const draw=()=>{const d=D[cur].d, L=D[0];
    sub.innerHTML=`Vessels worked by barges at midstream and the moorings, and what the barges moved each day — from the DPA <b>Daily Performance Report</b>. Latest, DPR <b>${L.d.d}</b> (24 h to 0700): <b>${L.n}</b> vessels worked · discharge <b>${nf.format(L.dis)}</b> MT · loading <b>${nf.format(L.load)}</b> MT. Tap a day for its vessels.`;
    st.innerHTML=tile('var(--brass)',L.n,'<b>Vessels working by barge</b> · DPR '+L.d.d)+tile('var(--warn)',nf.format(L.dis)+'<small> MT</small>','<b>Barge discharge</b> · import, ship → barge')+tile('var(--ok)',nf.format(L.load)+'<small> MT</small>','<b>Barge loading</b> · export, barge → ship')+tile('var(--line2)',nf.format(L.dis+L.load)+'<small> MT</small>','<b>Total by barge</b> · 24 h to 0700');
    td.innerHTML=`<tr><th style="width:19%">DPR · 24 h to 0700</th><th style="width:10%">Vessels</th><th style="width:16%">Discharge · MT</th><th style="width:16%">Loading · MT</th><th style="width:14%">Total · MT</th><th>Discharge / loading</th></tr>`
      +D.map((y,i)=>`<tr data-i="${i}" style="cursor:pointer${i===cur?';background:rgba(92,200,255,.08)':''}"><td class="pk"><b>${y.d.d}</b>${i===cur?' <span style="color:var(--brass);font-size:11px">shown below</span>':''}</td><td>${y.n}</td><td><b>${nf.format(y.dis)}</b></td><td><b>${nf.format(y.load)}</b></td><td><b>${nf.format(y.dis+y.load)}</b></td><td><div style="display:flex;height:10px;border-radius:3px;overflow:hidden;background:var(--panel2);width:${Math.max(4,Math.round((y.dis+y.load)/mx*100))}%"><span style="width:${(y.dis/(y.dis+y.load||1)*100).toFixed(1)}%;background:var(--warn)"></span><span style="flex:1;background:var(--ok)"></span></div></td></tr>`).join('');
    td.querySelectorAll('tr[data-i]').forEach(r=>r.onclick=()=>{cur=+r.dataset.i;draw();});
    tv.innerHTML=`<tr><th style="width:19%">Vessel · DPR ${d.d}</th><th style="width:17%">Cargo</th><th style="width:10%">Work</th><th style="width:11%">Last 24 h · MT</th><th style="width:11%">Up to date</th><th style="width:13%">Balance</th><th>Barges loaded at · agent / stevedore</th></tr>`
      +d.rows.map(r=>{const dy=r.l24>0&&r.bal>0?r.bal/r.l24:null;return `<tr><td class="pk"><b>${r.n}</b>${isMine(r.n)?' <span style="color:var(--brass);font-size:11px">Mihir &amp; Co</span>':''}<br><span style="color:var(--muted)">${r.loc==='MS'?'midstream':'mooring '+r.loc}</span></td><td>${r.c}</td><td style="color:${r.ie==='IMP'?'var(--warn)':'var(--ok)'}">${r.ie==='IMP'?'Discharge':'Loading'}</td><td><b>${r.l24?nf.format(r.l24):'—'}</b>${r.l24?'':'<br><span style="color:var(--muted)">no work</span>'}</td><td>${nf.format(r.upto)}</td><td><b>${nf.format(r.bal)}</b>${dy!=null?`<br><span style="color:var(--muted)">${dy<1?'under a day':'~'+dy.toFixed(1)+' d'} at this rate</span>`:''}</td><td class="w">${r.shore?'<b>'+r.shore+' MT</b>':''}${r.ag}${r.st?' · '+r.st:''}</td></tr>`;}).join('')
      +(d.sts?`<tr><td colspan="7" class="w">Ship-to-ship, not barge work: ${d.sts}</td></tr>`:'')
      +`<tr><td colspan="7" class="w">Ship-side figures as the DPR prints them (cargo over the ship's rail in the 24 h). The DPR gives no figure barge by barge, and none for import cargo landed at the shore.</td></tr>`;
  };
  draw();
}
function dpr(){
""")
B.rep("learn();dpr();", "learn();dpr();msWork();")
B.rep("const SEC_OPEN_DEFAULT=new Set(['finder','mine']);", "const SEC_OPEN_DEFAULT=new Set(['finder','mine','msb']);")
B.rep("<summary>Sources, rules &amp; tide</summary><div>", "<summary>Sources, rules &amp; tide</summary><div>New 19 Nov 22:49 (Mihir): a section \"Midstream · barge work\" — vessels working by barge and the daily barge discharge / loading, from DPR 17.11, 18.11 and 19.11 · ")
B.save()
