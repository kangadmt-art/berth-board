#!/usr/bin/env python3
# apply28 — v182: the size reading of GEARED / GEARLESS is REMOVED (Mihir, 20 Nov 00:05: "take the LOA rule out — enter a vessel only
# after checking her online, so there is no confusion"). A mark now appears ONLY for a vessel whose own gear is stated by an online source.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v181.html')
B = Board(P)
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % sys.argv[1] + B.s[m.end():]
a = B.s.index("// ---- GEAR — does the vessel carry her own cranes?"); e = B.s.index("const ieTag=k=>k?", a)
B.s = B.s[:a] + r"""// ---- GEAR — does the vessel carry her own cranes? The port's sheets never print it (Mihir, 19 Nov 23:56: "tell from the vessel's
// name whether she is gearless — you will find the vessel's details online").
// RULE (Mihir, 20 Nov 00:05): NO reading from LOA / size / cargo — a mark is shown ONLY for a vessel checked online. No entry = no mark.
// GEAR[name] = [G | GL, detail, source]: an online source that states THIS vessel's own gear ("Gear: C:4x36", "Gearless"), found by
// her NAME and matched to the list's LOA — the same name with another length is another ship. A statement about a class or a fleet
// ("Ultramaxes carry cranes") is NOT enough.
// GEAR_ID[name] = found online (IMO, size class) but the page does not state her cranes — NOT shown; kept so she is not searched twice
// the same way (try the owner's fleet page / ship's particulars next).
const GEAR={
 'Ken Ann':['G','4 cranes × 36 t · 36,644 DWT, built 2019','Shipfix vessel directory · IMO 9846158'],
 'Tai Keystone':['GL','Kamsarmax 84,703 DWT, built 2017','Shipfix vessel directory · IMO 9789843']
};
const GEAR_ID={
 'CD Glory':'Handysize 32,451 DWT, built 2011 · IMO 9611498',
 'Sea Postman':'Supramax · IMO 1124786',
 'Xin Hai Tong 71':'bulk carrier · IMO 9663128',
 'Belmoira':'Ultramax 61,346 DWT, built 2020 · IMO 9873278 (owner Belships)',
 'Katerina K':'bulk carrier 63,878 DWT · IMO 9801718',
 'Nord Copper':'Ultramax 60,396 DWT, built 2018 · IMO 9805647',
 'Uni Blossom':'Handysize 37,634 DWT, built 2018 · IMO 9816567'
};
const gearName=n=>n.replace(/\s*\((salt, next call|blades, next call|next call|reload|re-berthing|GL)\)\s*$/,'');
function gearOf(n){const g=GEAR[gearName(n)];return g?{g:g[0],sure:true,d:g[1],s:g[2]}:{g:'',sure:false,d:'',s:''};}
const gearTxt=x=>x.g==='G'?'GEARED':'GEARLESS', gearCls=x=>x.g==='G'?'gd':'gl';
const gearTip=x=>(gearTxt(x).toLowerCase()+' — '+x.d+' ('+x.s+')').replace(/"/g,'&quot;');
const gearChip=n=>{const x=gearOf(n);return x.g?` <span class="ie ${gearCls(x)}" title="${gearTip(x)}">${gearTxt(x)} ✓</span>`:'';};
""" + B.s[e:]
B.rep("const cg=o=>(o.c||'')+ieChip(o.n)+gearChip(o.n,o.loa,o.c); // commodity + IMP/EXP chip + GEARED / GEARLESS chip (HTML)",
      "const cg=o=>(o.c||'')+ieChip(o.n)+gearChip(o.n);           // commodity + IMP/EXP chip + GEARED / GEARLESS chip, only if checked online (HTML)")
B.rep("const gm=(n,c)=>{const x=gearOf(n,0,c);return x.g?`<span class=\"mini ${gearCls(x)}\" title=\"${gearTip(x)}\">${gearTxt(x)}${x.g==='?'?'':x.sure?' ✓':' ~'}</span>`:'';};",
      "const gm=n=>{const x=gearOf(n);return x.g?`<span class=\"mini ${gearCls(x)}\" title=\"${gearTip(x)}\">${gearTxt(x)} ✓</span>`:'';};")
a = B.s.index(" const gs=root.getElementById('gearsum');if(gs){"); e = B.s.index(" let n=0,grp='';const body=rows.map(w=>{let g='';", a)
B.s = B.s[:a] + """ const gs=root.getElementById('gearsum');if(gs){const k=Object.keys(GEAR),tot=new Set(V.filter(v=>v.T>NOW).map(v=>gearName(v.n)).concat(W.map(w=>gearName(w.n)))).size;
  gs.innerHTML=`Ship's cranes — a <b>GEARED ✓</b> / <b>GEARLESS ✓</b> mark is shown only for a vessel checked online (the port's sheets do not print it). Checked so far: ${k.map(n=>'<b>'+n+'</b> '+(GEAR[n][0]==='G'?'geared':'gearless')+' ('+GEAR[n][1].split(' · ')[0]+')').join(' · ')}. No mark = not found online yet — ${k.length} of ${tot} vessels done; nothing is guessed from size.`;}
""" + B.s[e:]
B.rep("New 19 Nov 23:56 (Mihir): GEARED / GEARLESS beside every vessel — ✓ = checked online, ~ = read from her size (the port's sheets do not print it)",
      "New 20 Nov 00:05 (Mihir): GEARED ✓ / GEARLESS ✓ only beside a vessel checked online — the reading from LOA / size is removed, no mark = not found online yet")
B.save()
