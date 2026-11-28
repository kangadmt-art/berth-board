#!/usr/bin/env python3
# apply93 — v297. 29 Nov 00:34, no text: the team's reply on the cargo list PDF (Kandla_Dry_Cargo_Handled…_1.pdf) —
# for each of the 35 cargoes they wrote the berths a vessel of that cargo CAN berth at, geared and gearless. This is now the board's cargo → berth rule.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
B.rep("function allowedBerths(w){\n  const c=w.c||''; let A=POOL.slice();\n  if(LIST_ASK[w.n])A=A.filter(b=>LIST_ASK[w.n].includes(b));\n",
"""// ---- CARGO → BERTH, as Mihir's team wrote it on the cargo list (29 Nov 00:34). "CJ 13 to 16" includes 15A. Where the team left a cargo blank (barite, manganese ore, bentonite in bulk, bitumen) teamBerths() returns null and the older rules below still decide.
// Gearless = confirmed gearless (online or "(GL)" on the list); confirmed geared = geared; not known → taken as gearless above 200 m.
const isGearless=w=>{const g=gearOf(w.n).g;return g==='GL'?true:g==='G'?false:(w.loa||LOA[w.n]||0)>200;};
function teamBerths(w){
  const x=(w.c||'').toLowerCase(), GL=isGearless(w), C=CLEAN, R=(a,z)=>POOL.filter(b=>!C.includes(b)&&+b>=a&&+b<=z);
  if(/windmill/.test(x))return C.slice();
  if(/pipe/.test(x))return C.slice();
  if(/salt/.test(x))return C.slice();
  if(JUMBO(x))return R(1,6).concat(C);                                   // bentonite / soda ash / manganese sulphate jumbo bags
  if(/clay|feldspar|kaolin/.test(x)&&!/bentonite/.test(x))return GL?['7','8'].concat(C):['4','5','7','8'].concat(C);
  if(/bag/.test(x))return R(1,5).concat(C);                              // rice, sugar, chick peas, lentils, mixed bags
  if(/log|timber/.test(x))return ['1','4','5','7','8'].concat(C);
  if(/coal|coke/.test(x))return GL?['7','8','16']:['5','7','8','16'].concat(RK(w,'SAAGAR')||w.cat==='SAAGAR'?['6']:[]); // CJ-6 only when she is under SAAGAR
  if(/pellet feed|fines/.test(x))return GL?['7','8','16']:['5','7','8','16'];
  if(/pellet/.test(x))return GL?['7','8','16']:['3','4','5','7','8','16'];
  if(/iron ore/.test(x))return GL?['7','8','16']:['5','7','8','16'];
  if(/aggregate/.test(x))return GL?['7','8'].concat(C):['4','5','7','8'].concat(C);
  if(/gypsum/.test(x))return GL?['7','8'].concat(C):['5','7','8'].concat(C);
  if(/soda ash/.test(x))return R(1,5).concat(['7','8']);
  if(/rock phosphate/.test(x))return GL?['7','8']:['4','5'];
  if(/urea|\\bdap\\b|\\btsp\\b|\\bmop\\b|potash|npk|ammonium|polyhalite|fertili/.test(x))return GL?['7','8']:R(1,8);
  if(/pulp/.test(x))return R(1,8);
  if(/wheat|rice|sugar|soya|maize|corn|grain/.test(x))return R(1,5).concat(C); // agri cargo in bulk, as the team wrote for rice in bulk
  if(/steel|coil|slab|plate|project|package|crane|general cargo/.test(x))return R(1,8).concat(C);
  return null;
}
function allowedBerths(w){
  const T=teamBerths(w);
  if(T){ // the team's table decides; a berth named in the list remark replaces it ("keeps her to those berths only")
    let A=POOL.filter(b=>T.includes(b));
    const rq=LIST_ASK[w.n]||reqOf(w); if(rq){const I=POOL.filter(b=>rq.includes(b)); if(I.length)A=I;}
    else if(/2\\s*(shore ?crane|s\\.?c\\.?\\b)/i.test(w.x||'')){const SCB=isBag(w.c||'')?['2','3']:['6','7','8','13','14','15','15A','16'];const A1=A.filter(b=>SCB.includes(b));if(A1.length)A=A1;}
    if((w.ie||IE[w.n])==='EXP'){const L=loadedDr(w);const deep=A.filter(b=>berthDepth(b)>=L);if(deep.length&&deep.length<A.length)A=deep;}
    return A;
  }
  const c=w.c||''; let A=POOL.slice();
  if(LIST_ASK[w.n])A=A.filter(b=>LIST_ASK[w.n].includes(b));
""")
B.save(); print('saved 93')
