#!/usr/bin/env python3
# apply42 — v197: Mihir (20 Nov 23:48) — "Waiting ya koi bhi vessel ho, waha gear or gearless wala likh do, jo gear and gearless ka rule hai woh hisab se."
# EVERY vessel on every tab now reads GEARED or GEARLESS:
#   1. confirmed online for that vessel (GEAR)                         → GEARED n×t / GEARLESS
#   2. the DPA berthing list prints "(GL)" after her name (GEAR_LIST)  → GEARLESS            (the board had been dropping that mark)
#   3. otherwise by the SIZE RULE (his 215 m): LOA above 215 m → "GEARLESS · BY RULE"; 215 m or less → "GEARED · BY RULE"; a tug with barge → "GEARLESS · BARGE"
#   4. no LOA on the board                                              → NO GEAR DETAILS
# "MAY BE GEARLESS" is gone (it becomes GEARLESS · BY RULE). Rule-based chips are dashed so that a confirmed one can be told apart.   argv[1] = UPDATED
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
B.rep("const NOW=h('11-20 20:26');", "const NOW=h('11-20 23:48');")
# styles
B.rep(".ie.gq{color:var(--muted);border:1px dashed var(--line2)}", ".ie.gq{color:var(--muted);border:1px dashed var(--line2)}.ie.gdr{color:#9be3b0;border:1px dashed rgba(95,191,122,.6)}.ie.glr{color:#ff9d8a;border:1px dashed rgba(229,99,106,.65)}")
B.rep(".mini.gq{border-style:dashed}", ".mini.gq{border-style:dashed}.mini.gdr{border-style:dashed;border-color:rgba(95,191,122,.6);color:#9be3b0}.mini.glr{border-style:dashed;border-color:rgba(229,99,106,.65);color:#ff9d8a}")
# code
B.rep("// Mihir, 20 Nov 00:26: a vessel NOT confirmed online whose LOA is above 215 m is marked \"MAY BE GEARLESS\" (the only reading from size that is allowed).\n",
      "// THE GEAR RULE (Mihir, 20 Nov 23:48 — \"waiting ya koi bhi vessel ho, waha gear or gearless likh do, jo rule hai us hisab se\"): EVERY vessel reads GEARED or GEARLESS.\n"
      "//   1. confirmed online for THAT vessel (GEAR)                          → GEARED n×t / GEARLESS (solid chip)\n"
      "//   2. the DPA berthing list prints \"(GL)\" after her name (GEAR_LIST)   → GEARLESS (solid chip) — the port's own mark; gearName() strips it from the name\n"
      "//   3. otherwise BY THE SIZE RULE (his 215 m of 20 Nov 00:26)            → LOA above 215 m: GEARLESS · BY RULE; 215 m or less: GEARED · BY RULE; a tug with barge: GEARLESS · BARGE (dashed chip)\n"
      "//   4. no LOA anywhere on the board                                      → NO GEAR DETAILS\n"
      "// It replaces \"MAY BE GEARLESS\" (00:26) and the earlier \"nothing from size\" (00:05). When a new list prints (GL) for a vessel, add her to GEAR_LIST.\n"
      "const GEAR_LIST={'Europa Graeca':'list 20.11','Lila Tokyo':'list 20.11','Cretansea':'list 20.11','MSC Magali':'list 20.11'}; // \"(GL)\" printed after the name on the DPA berthing list\n")
B.rep("function gearLoa(n){if(!_gearLoa){_gearLoa={};V.concat(W,TUNA.berths||[],TUNA.wait||[],TUNA.eta||[]).forEach(x=>{if(x&&x.n&&+x.loa)_gearLoa[gearName(x.n)]=+x.loa;});}return _gearLoa[gearName(n)]||0;}",
      "function gearLoa(n){if(!_gearLoa){_gearLoa={};Object.keys(LOA).forEach(k=>{if(+LOA[k])_gearLoa[gearName(k)]=+LOA[k];});V.concat(W,TUNA.berths||[],TUNA.wait||[],TUNA.eta||[]).forEach(x=>{if(x&&x.n&&+x.loa)_gearLoa[gearName(x.n)]=+x.loa;});}return _gearLoa[gearName(n)]||0;}")
B.rep("  const loa=gearLoa(n),why=GEAR_NONE.includes(k)?'searched online, not stated':'not searched online yet';\n"
      "  if(loa>215)return {g:'M',sh:'',d:'may be gearless — LOA '+loa+' m is above 215 m; not confirmed ('+why+')',s:''};\n"
      "  return {g:'?',sh:'',d:'no details of gear available — '+why,s:''};}",
      "  if(GEAR_LIST[k])return {g:'GL',sh:'',d:'gearless — the DPA berthing list prints (GL) after her name',s:'DPA '+GEAR_LIST[k]};\n"
      "  const loa=gearLoa(n),why=GEAR_NONE.includes(k)?'searched online, not stated':'not searched online yet';\n"
      "  if(/^tug\\b|\\bbarge\\b|\\bBG\\b/i.test(k))return {g:'GLr',sh:'BARGE',d:'gearless — a tug with barge has no cargo gear of her own',s:''};\n"
      "  if(loa>215)return {g:'GLr',sh:'BY RULE',d:'gearless by the size rule — LOA '+loa+' m is above 215 m; not confirmed for this vessel ('+why+')',s:''};\n"
      "  if(loa>0)return {g:'Gr',sh:'BY RULE',d:'geared by the size rule — LOA '+loa+' m is not above 215 m; not confirmed for this vessel ('+why+')',s:''};\n"
      "  return {g:'?',sh:'',d:'no details of gear available — '+why+'; no LOA on the board for the size rule',s:''};}")
B.rep("const gearTxt=x=>x.g==='G'?'GEARED'+(x.sh?' '+x.sh:''):x.g==='GL'?'GEARLESS':x.g==='M'?'MAY BE GEARLESS':'NO GEAR DETAILS', gearCls=x=>x.g==='G'?'gd':x.g==='GL'?'gl':x.g==='M'?'gy':'gq';",
      "const gearTxt=x=>x.g==='G'?'GEARED'+(x.sh?' '+x.sh:''):x.g==='GL'?'GEARLESS':x.g==='Gr'?'GEARED · '+x.sh:x.g==='GLr'?'GEARLESS · '+x.sh:'NO GEAR DETAILS', gearCls=x=>x.g==='G'?'gd':x.g==='GL'?'gl':x.g==='Gr'?'gdr':x.g==='GLr'?'glr':'gq';")
B.rep("window.__dbg={slotRun,V,W,allowedBerths,h,PM};", "window.__dbg={slotRun,V,W,allowedBerths,h,PM,gearOf,gearTxt};")
# legend on the Priority chart tab
B.rep("  gs.innerHTML=`Ship's cranes (the port's sheets do not print it) — shown where the vessel's own details were found online: ${found.map(n=>'<b>'+n+'</b> '+(GEAR[n][0]==='G'?'geared '+GEAR[n][1]:'gearless')).join(' · ')}. <b>MAY BE GEARLESS</b> = not confirmed online, but her LOA is above 215 m. <b>NO GEAR DETAILS</b> = no details of gear available. Searched online so far: <b>${found.length+none.length}</b> of ${all.length} vessels (${found.length} found); the other ${todo.length} are searched in turn, and every new vessel when she first appears.`;}",
      "  gs.innerHTML=`Ship's cranes — every vessel reads GEARED or GEARLESS. A <b>solid</b> chip is confirmed for that vessel: found online (${found.map(n=>'<b>'+n+'</b> '+(GEAR[n][0]==='G'?'geared '+GEAR[n][1]:'gearless')).join(' · ')}) or printed <b>(GL)</b> on the DPA berthing list (${Object.keys(GEAR_LIST).join(' · ')}). A <b>dashed</b> chip marked <b>BY RULE</b> is not confirmed — it is written by the size rule: LOA above 215 m gearless, 215 m or less geared; a tug with barge is gearless. Searched online so far: <b>${found.length+none.length}</b> of ${all.length} vessels (${found.length} found); every new vessel is searched when she first appears.`;}")
# lesson
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 23:48 · Mihir — geared or gearless against every vessel, by the rule",
 "\"Waiting ya koi bhi vessel ho, waha gear or gearless wala likh do, jo gear and gearless ka rule hai woh hisab se\" — with a screenshot of the Tuna tab showing MAY BE GEARLESS and NO GEAR DETAILS.",
 "Board: GEARED / GEARLESS only where found online for that vessel (8 of 82); MAY BE GEARLESS above 215 m; NO GEAR DETAILS for all the rest — 74 vessels.",
 "A chip that says \"no details\" on nine vessels in ten tells him nothing. And the board had been throwing away the port's own mark: the berthing list prints \"(GL)\" after the name of some gearless vessels (Europa Graeca, Lila Tokyo, MSC Magali, Cretansea on list 20.11) — the name cleaner stripped it.",
 "The 00:05 instruction (nothing from size) was kept too long once he had himself given a size line at 00:26; what he wants on the board is an answer against every vessel.",
 "v197: every vessel reads GEARED or GEARLESS — (1) found online → solid chip with the cranes; (2) \"(GL)\" on the DPA list → GEARLESS, solid; (3) otherwise by the size rule — above 215 m GEARLESS · BY RULE, 215 m or less GEARED · BY RULE, tug with barge GEARLESS · BARGE — dashed chip, so a confirmed one can be told from a rule one; (4) NO GEAR DETAILS only where the board has no LOA. LOA for vessels at berth now comes from the LOA table. The reading of the rule (215 m both ways) is the board's — told to Mihir.", "adopted"))
B.save()

# --- applied by hand after the script (same version): LOA table entries and one found vessel ---
# Object.assign(LOA,{'Safi Alfa':189.99,'Flag Marina':254.62,'Parvraj':189.9});
# Object.assign(LOA,{'Paiwan Ace':182.93,'Paiwan Wisdom':175,'Erna Oldendorff':179.99,'African Pheasant':199,'Stalo':229,'Mak 1':186});  # looked up online
# GEAR['Paiwan Ace']=['G','4×30.7 t','4 cranes × 30.7 t · 40,236 DWT, built 2024','Shipfix vessel directory · IMO 9984405']
# GEAR_NONE += 'Paiwan Wisdom','Erna Oldendorff','African Pheasant','Stalo','Mak 1'
