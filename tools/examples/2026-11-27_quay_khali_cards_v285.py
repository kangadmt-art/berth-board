#!/usr/bin/env python3
# apply81 — v285. Mihir, 27 Nov 18:34: "space" = the empty quay — from which panel to which panel, how many panels are empty, and the distance in metres.
# A short list of ONLY the empty places comes first, in those three figures; the full table (vessels + empty) follows with the same three columns.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); s = B.s
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60]); s = s.replace(a, b)
rep(".qgt{width:100%;", ".kh{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px;margin:6px 0 14px}.kh>div{border:1.5px solid var(--ok);border-radius:10px;padding:10px 12px;background:rgba(95,191,127,.08)}\n"
    ".kh .pp{font-family:var(--f-disp);font-size:22px;font-weight:800;line-height:1.1}.kh .pp small{font-family:var(--f-body);font-size:11px;font-weight:400;color:var(--muted);display:block;letter-spacing:0}\n"
    ".kh .nn{display:flex;gap:14px;margin-top:6px;font-size:13px}.kh .nn b{font-size:17px;color:var(--ok)}.kh .ft{font-size:11.5px;color:var(--muted);margin-top:4px}.kh>div.sm{border-color:var(--line2);background:transparent}.kh>div.sm .nn b{color:var(--fg)}\n"
    ".khcap{font-size:13px;margin:10px 0 2px}.khcap b{font-size:14px}\n.qgt{width:100%;")
a = s.index("function quayGaps(){"); b = s.index("function runs(){", a)
fn = r'''function quayGaps(){
  const el=document.getElementById('qgaps'); if(!el)return;
  const pn=x=>frac(Math.round(x*4)/4);
  const block=seg=>{
    const present=runFleet(seg).filter(v=>v.p&&v.F<=T&&T<v.T).sort((a,z)=>a.p[0]-z.p[0]);
    const R=quayRuns(T,seg); const rows=[], cards=[]; let cur=seg.from, free=0, freeM=0, n=0, lastN='';
    const gap=(a,z,after,before)=>{ if(z-a<0.01)return; const m=gapM(a,z); const r=R.find(x=>Math.abs(x.a-a)<0.01&&Math.abs(x.z-z)<0.01); free+=z-a; freeM+=m; n++;
      const fit=r&&r.maxLoa>=70?'~'+r.maxLoa+' m tak ki vessel lag sakti hai':'vessel ke liye chhoti jagah';
      const where=after&&before?after+' aur '+before+' ke beech':after?after+' ke baad, quay ke aakhir tak':before?'quay ke shuru se '+before+' tak':'poora hissa khali';
      cards.push({m,h:`<div class="${m<RUN_MIN_M?'sm':''}"><div class="pp">Panel ${frac(a)} se ${frac(z)}<small>${where}</small></div><div class="nn"><span><b>${pn(z-a)}</b> panel khali</span><span><b>${Math.round(m)}</b> metre</span></div><div class="ft">${fit}</div></div>`});
      rows.push(`<tr class="g${m<RUN_MIN_M?' sm':''}"><td class="hidem">—</td><td>KHALI<br><small>${fit}</small></td><td class="pn">${frac(a)} se ${frac(z)}</td><td class="num">${pn(z-a)}</td><td class="num">${Math.round(m)} m</td></tr>`); };
    const short=v=>v.n.replace(/\s*\(.*\)\s*$/,'');
    for(const v of present){ gap(cur,v.p[0],lastN,short(v)); const m=gapM(v.p[0],v.p[1]);
      rows.push(`<tr><td class="hidem">CJ-${v.b}</td><td><b>${short(v)}</b><br><small>CJ-${v.b}${LOA[v.n]?' · vessel '+Math.round(LOA[v.n])+' m lambi':''}</small></td><td class="pn">${frac(v.p[0])} se ${frac(v.p[1])}</td><td class="num">${pn(v.p[1]-v.p[0])}</td><td class="num">${Math.round(m)} m</td></tr>`); cur=Math.max(cur,v.p[1]); lastN=short(v); }
    gap(cur,seg.to,lastN,'');
    const big=cards.filter(c=>c.m>=RUN_MIN_M), small=cards.filter(c=>c.m<RUN_MIN_M);
    return {top:`<div class="khcap"><b>${seg.label}</b> · kul khali <b>${pn(free)} panel</b> · <b>${Math.round(freeM)} metre</b> · ${n} jagah</div><div class="kh">${big.concat(small).map(c=>c.h).join('')}</div>`,
      full:`<div class="qgcap">${seg.label} · panel ${seg.from} se ${seg.to}</div><div class="scroll"><table class="qgt"><thead><tr><th class="hidem">Berth</th><th>Vessel / khali jagah</th><th>Panel se panel</th><th class="num">Kitne panel</th><th class="num">Metre</th></tr></thead><tbody>${rows.join('')}
      <tr class="tot"><td class="hidem"></td><td>Kul khali · ${n} jagah</td><td></td><td class="num">${pn(free)}</td><td class="num">${Math.round(freeM)} m</td></tr></tbody></table></div>`}; };
  const bl=SEGS.slice().reverse().map(block);
  el.innerHTML=`<div class="qgcap">Khali jagah · abhi (${fmt(T)})</div><div class="qgh">Har dabba ek khali jagah hai: kis panel se kis panel tak, kitne panel khali, aur metre mein kitni doori. Hara dabba = vessel lag sakti hai.</div>`+bl.map(x=>x.top).join('')
    +`<div class="qgcap" style="margin-top:18px">Poori quay · vessel aur khali jagah, north se south</div><div class="qgh">Safed line = lagi hui vessel aur uske panel number. Hari line = khali jagah.</div>`+bl.map(x=>x.full).join('');
}
'''
s = s[:a] + fn + s[b:]
rep('First a table — every vessel with her panel numbers, and every empty stretch with its length in metres — then the quay drawn to scale. Position as the board stands now. CJ-9 and CJ-10 have their own page.', 'Pehle khali jagah — panel se panel, kitne panel, kitne metre. Phir poori quay ki table, phir naap se bana chitra. CJ-9 aur CJ-10 apne page par hain.')
B.s = s; B.save()
