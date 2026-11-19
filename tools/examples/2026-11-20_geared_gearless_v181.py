#!/usr/bin/env python3
# apply27 — v181: GEARED / GEARLESS on every vessel (Mihir, 19 Nov 23:56 — the port's sheets never print it).
# A vessel checked online is listed in GEAR and shown with "✓"; every other vessel is read from her size and shown with "~". argv[1] = UPDATED.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v180.html')
B = Board(P)
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % sys.argv[1] + B.s[m.end():]

# ---- styles: cargo tab chip, priority-chart chip
B.rep(".ie.ix{color:var(--muted);border:1px solid var(--line2)}",
      ".ie.ix{color:var(--muted);border:1px solid var(--line2)}.ie.gd{color:#9be3b0;border:1px solid rgba(95,191,122,.5);background:rgba(95,191,122,.10)}.ie.gl{color:#ff9d8a;border:1px solid rgba(229,99,106,.55);background:rgba(229,99,106,.10)}.ie.gq{color:var(--muted);border:1px dashed var(--line2)}")
B.rep(".mini.m{border-color:var(--brass2);color:var(--brass)}", ".mini.m{border-color:var(--brass2);color:var(--brass)}.mini.gd{border-color:rgba(95,191,122,.5);color:#9be3b0}.mini.gl{border-color:rgba(229,99,106,.55);color:#ff9d8a}.mini.gq{border-style:dashed}.gsum{color:var(--muted);font-size:12.5px;margin:6px 0 2px}.gsum b{color:var(--fg)}")

# ---- data + helpers (before the IMP/EXP chip helpers)
B.rep("const ieTag=k=>k?", r"""// ---- GEAR — does the vessel carry her own cranes? The port's sheets never print it (Mihir, 19 Nov 23:56: "tell from the vessel's
// name whether she is gearless — you will find the vessel's details online").
// GEAR[name] = [G | GL, detail, source]: looked up online by NAME and matched to the list's LOA — the same name with a different
// length is a different ship, so never enter a vessel on the name alone. Shown with "✓".
// GEAR_ID[name] = found online (size class, IMO) but the page does not state her cranes — the size reading stands, the detail is shown.
// Every other vessel is read from her size, shown with "~": tug-and-barge → gearless · LOA ≥ 215 m (Panamax and larger) → gearless ·
// log cargo → geared · LOA 150–215 m (Handysize / Supramax / Ultramax) → geared · smaller, or a small blade / deck carrier → not known.
// DISPLAY ONLY: the projection does not use it (an HMC / shore-crane rule needs Mihir's word first).
const GEAR={
 'Ken Ann':['G','4 cranes × 36 t · Handysize 36,644 DWT, built 2019','Shipfix vessel directory · IMO 9846158'],
 'Tai Keystone':['GL','Kamsarmax 84,703 DWT, built 2017','Shipfix vessel directory · IMO 9789843'],
 'Belmoira':['G','Ultramax 61,346 DWT, built 2020 · her owner Belships describes its Ultramaxes as crane-fitted','Belships · IMO 9873278']
};
const GEAR_ID={
 'CD Glory':'Handysize 32,451 DWT, built 2011 · IMO 9611498',
 'Sea Postman':'Supramax · IMO 1124786',
 'Xin Hai Tong 71':'bulk carrier · IMO 9663128'
};
const gearName=n=>n.replace(/\s*\((salt, next call|blades, next call|next call|reload|re-berthing|GL)\)\s*$/,'');
let _gearLoa=null;
function gearOf(n,loa,c){
  const k=gearName(n);
  if(!_gearLoa){_gearLoa={};V.concat(W).forEach(x=>{if(x.loa)_gearLoa[gearName(x.n)]={loa:+x.loa,c:x.c||''};});}
  const m=_gearLoa[k]||{}; loa=+loa||m.loa||0; c=c||m.c||'';
  if(GEAR[k])return {g:GEAR[k][0],sure:true,d:GEAR[k][1],s:GEAR[k][2]};
  const id=GEAR_ID[k]?GEAR_ID[k]+' (found online, cranes not stated there) · ':'';
  if(/\btug\b|barge/i.test(n))return {g:'GL',sure:false,d:'tug and barge',s:'by type'};
  if(/tanker/i.test(c))return {g:'',sure:false,d:'',s:''};
  if(loa>=215)return {g:'GL',sure:false,d:id+'LOA '+loa+' m — Panamax size or larger, these carry no cranes',s:'by size'};
  if(/\blogs?\b/i.test(c))return {g:'G',sure:false,d:id+'log carrier — logs are worked with the ship\'s cranes',s:'by cargo'};
  if(/blade/i.test(c)&&loa<170)return {g:'?',sure:false,d:(loa?'LOA '+loa+' m — ':'')+'small blade / deck carrier, could be either',s:'not checked'};
  if(loa>=150)return {g:'G',sure:false,d:id+'LOA '+loa+' m — '+(loa>=185?'Supramax / Ultramax':'Handysize')+' size, normally 4 cranes',s:'by size'};
  return {g:'?',sure:false,d:(loa?'LOA '+loa+' m — ':'')+'small vessel, could be either',s:'not checked'};
}
const gearTxt=x=>x.g==='G'?'GEARED':x.g==='GL'?'GEARLESS':'GEAR ?', gearCls=x=>x.g==='G'?'gd':x.g==='GL'?'gl':'gq';
const gearTip=x=>(gearTxt(x).toLowerCase()+' — '+x.d+' ('+x.s+')').replace(/"/g,'&quot;');
const gearChip=(n,loa,c)=>{const x=gearOf(n,loa,c);return x.g?` <span class="ie ${gearCls(x)}" title="${gearTip(x)}">${gearTxt(x)}${x.g==='?'?'':x.sure?' ✓':' ~'}</span>`:'';};
const ieTag=k=>k?""")
B.rep("const cg=o=>(o.c||'')+ieChip(o.n);                       // commodity + IMP/EXP chip (HTML)",
      "const cg=o=>(o.c||'')+ieChip(o.n)+gearChip(o.n,o.loa,o.c); // commodity + IMP/EXP chip + GEARED / GEARLESS chip (HTML)")

# ---- priority chart (shadow root): chip beside the vessel name in both tables + a count line
B.rep("""<td class="l"><b>${esc(short(v.n))}</b>${v.mine?'<span class="mini m">Mihir</span>':''}${v.future?'<span class="mini w">coming</span>':''}""",
      """<td class="l"><b>${esc(short(v.n))}</b>${v.mine?'<span class="mini m">Mihir</span>':''}${v.future?'<span class="mini w">coming</span>':''}${gm(v.n,v.c)}""")
B.rep("""<td class="v"><b>${esc(short(w.n))}</b>${w.mine?'<span class="mini m">Mihir</span>':''}${w.noHP?'<span class="mini w" title="passed over for HP">HP ✕</span>':''}""",
      """<td class="v"><b>${esc(short(w.n))}</b>${w.mine?'<span class="mini m">Mihir</span>':''}${w.noHP?'<span class="mini w" title="passed over for HP">HP ✕</span>':''}${gm(w.n,w.c)}""")
B.rep(""" let n=0,grp='';const body=rows.map(w=>{let g='';""",
      """ const gs=root.getElementById('gearsum');if(gs){const a=W.map(w=>gearOf(w.n,0,w.c)).filter(x=>x.g),cnt=k=>a.filter(x=>x.g===k).length;
  gs.innerHTML=`Ship's cranes — <b>${cnt('G')}</b> geared · <b>${cnt('GL')}</b> gearless · <b>${cnt('?')}</b> not known. <b>✓</b> = checked online (${a.filter(x=>x.sure).length}) · <b>~</b> = read from her size (LOA 215 m and above gearless · 150–215 m and log carriers geared). The port's sheets do not print it.`;}
 let n=0,grp='';const body=rows.map(w=>{let g='';""")
B.rep("""<div class="bar"><span class="lb2">Line dekho</span><span id="sorts"></span></div>""",
      """<div class="bar"><span class="lb2">Line dekho</span><span id="sorts"></span></div>\n<p class="gsum" id="gearsum"></p>""")
# gm() — the chip in the chart's own style; defined beside the chart's other helpers
B.rep("const short=n=>n.replace(/ \\((salt, next call|blades, next call|next call|reload)\\)/,'');",
      "const short=n=>n.replace(/ \\((salt, next call|blades, next call|next call|reload)\\)/,'');\nconst gm=(n,c)=>{const x=gearOf(n,0,c);return x.g?`<span class=\"mini ${gearCls(x)}\" title=\"${gearTip(x)}\">${gearTxt(x)}${x.g==='?'?'':x.sure?' ✓':' ~'}</span>`:'';};")
B.rep("<div>New 19 Nov 23:08 (Mihir): Accuracy made simple", "<div>New 19 Nov 23:56 (Mihir): GEARED / GEARLESS beside every vessel — ✓ = checked online, ~ = read from her size (the port's sheets do not print it) · New 19 Nov 23:08 (Mihir): Accuracy made simple")
B.save()
