#!/usr/bin/env python3
# apply29 — v183: GEAR, the simple formula (Mihir, 20 Nov 00:11): where the details are available show them, where not write that no
# details of gear are available; show it wherever vessels are listed, Tuna too. First online round: 22 vessels searched, 4 found.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v182.html')
B = Board(P)
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % sys.argv[1] + B.s[m.end():]
a = B.s.index("// ---- GEAR — does the vessel carry her own cranes?"); e = B.s.index("const ieTag=k=>k?", a)
B.s = B.s[:a] + r"""// ---- GEAR — does the vessel carry her own cranes? The port's sheets never print it (Mihir, 19 Nov 23:56).
// THE FORMULA (Mihir, 20 Nov 00:11): where the details are available, show them; where not, write that no details of gear are
// available; show it wherever vessels are listed (Cargo, Priority chart, Barge, Timber, Tuna). NO reading from LOA / size / cargo
// (Mihir, 20 Nov 00:05) — only what a source states for THAT vessel.
// GEAR[name] = [G | GL, short, detail, source] — found online by NAME and matched to the list's LOA (same name, other length = other ship).
// GEAR_NONE = searched online, gear not stated anywhere found (kept so she is not searched the same way again; try the owner's fleet
// page or the ship's particulars next). A vessel in neither list has NOT been searched yet — window.__GEAR.todo lists them.
// ROUTINE: every vessel new to the board is searched once when she first appears; the backlog is worked off a few at a time.
const GEAR={
 'Ken Ann':['G','4×36 t','4 cranes × 36 t · 36,644 DWT, built 2019','Shipfix vessel directory · IMO 9846158'],
 'Belmoira':['G','4×30.7 t','4 cranes × 30.7 t · 61,346 DWT, built 2020','Shipfix vessel directory · IMO 9873278'],
 'Meghna Prestige':['G','4×30 t','4 cranes × 30 t · 66,213 DWT, built 2023','Shipfix vessel directory · IMO 9928839'],
 'Tai Keystone':['GL','','gearless · Kamsarmax 84,703 DWT, built 2017','Shipfix vessel directory · IMO 9789843']
};
const GEAR_NONE=['CD Glory','Sea Postman','Xin Hai Tong 71','Katerina K','Nord Copper','Uni Blossom','Rome Trader','DSM London','African Hornbill','Seacon Monaco','Propel Confidence','Vishva Bandhan','Saga Viking','Truong Minh Dream','Yara J','ML Egret','New Bliss','Heng Yuan Fa Zhan'];
const gearName=n=>n.replace(/\s*\((salt, next call|blades, next call|next call|reload|re-berthing|GL|LPG\/C)\)\s*$/,'');
function gearOf(n){const g=GEAR[gearName(n)];return g?{g:g[0],sh:g[1],d:g[2],s:g[3]}:{g:'?',sh:'',d:'no details of gear available'+(GEAR_NONE.includes(gearName(n))?' — searched online, not stated':' — not searched online yet'),s:''};}
const gearTxt=x=>x.g==='G'?'GEARED'+(x.sh?' '+x.sh:''):x.g==='GL'?'GEARLESS':'NO GEAR DETAILS', gearCls=x=>x.g==='G'?'gd':x.g==='GL'?'gl':'gq';
const gearTip=x=>(x.d+(x.s?' ('+x.s+')':'')).replace(/"/g,'&quot;');
const gearChip=n=>{const x=gearOf(n);return ` <span class="ie ${gearCls(x)}" title="${gearTip(x)}">${gearTxt(x)}</span>`;};
""" + B.s[e:]
B.rep("const gm=n=>{const x=gearOf(n);return x.g?`<span class=\"mini ${gearCls(x)}\" title=\"${gearTip(x)}\">${gearTxt(x)} ✓</span>`:'';};",
      "const gm=n=>{const x=gearOf(n);return `<span class=\"mini ${gearCls(x)}\" title=\"${gearTip(x)}\">${gearTxt(x)}</span>`;};")
a = B.s.index(" const gs=root.getElementById('gearsum');if(gs){"); e = B.s.index(" let n=0,grp='';const body=rows.map(w=>{let g='';", a)
B.s = B.s[:a] + """ const gs=root.getElementById('gearsum');if(gs){const all=[...new Set(V.filter(v=>v.T>NOW).map(v=>gearName(v.n)).concat(W.map(w=>gearName(w.n)),(TUNA.berths||[]).concat(TUNA.wait||[],TUNA.eta||[]).filter(x=>x&&x.n).map(x=>gearName(x.n))))];
  const found=all.filter(n=>GEAR[n]),none=all.filter(n=>!GEAR[n]&&GEAR_NONE.includes(n)),todo=all.filter(n=>!GEAR[n]&&!GEAR_NONE.includes(n));window.__GEAR={found,none,todo};
  gs.innerHTML=`Ship's cranes (the port's sheets do not print it) — shown where the vessel's own details were found online: ${found.map(n=>'<b>'+n+'</b> '+(GEAR[n][0]==='G'?'geared '+GEAR[n][1]:'gearless')).join(' · ')}. <b>NO GEAR DETAILS</b> = no details of gear available. Searched online so far: <b>${found.length+none.length}</b> of ${all.length} vessels (${found.length} found); the other ${todo.length} are searched in turn, and every new vessel when she first appears.`;}
""" + B.s[e:]
# ---- Tuna, Barge, Timber (phone line) — the chip beside the vessel's name
n = B.s.count('<td class="pk"><b>${v.n}</b>'); assert n == 3, n
B.s = B.s.replace('<td class="pk"><b>${v.n}</b>', '<td class="pk"><b>${v.n}</b>${gearChip(v.n)}')
B.rep('return `<tr><td class="pk"><b>${r.n}</b>${isMine(r.n)?', 'return `<tr><td class="pk"><b>${r.n}</b>${gearChip(r.n)}${isMine(r.n)?')
B.rep('<div class="s1"><span class="nm">${r.n}${tag(r)}</span>', '<div class="s1"><span class="nm">${r.n}${tag(r)}${gearChip(r.n)}</span>')
B.rep("New 20 Nov 00:05 (Mihir): GEARED ✓ / GEARLESS ✓ only beside a vessel checked online — the reading from LOA / size is removed, no mark = not found online yet",
      "New 20 Nov 00:11 (Mihir): ship's gear beside every vessel on every tab — GEARED with her cranes or GEARLESS where the details were found online, NO GEAR DETAILS where none are available; nothing is read from size")
B.save()
