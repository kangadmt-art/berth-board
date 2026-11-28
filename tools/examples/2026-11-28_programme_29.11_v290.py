#!/usr/bin/env python3
# apply86 — v290. Papers 28 Nov 14:24 (no text): PROGRAMME FOR 29.11.2026 (file "20261127_PROGRAM FOR 29.11.2026.xlsx"; its heading still reads "MOVEMENT FOR 28.11.2026 · TF/SH/2102 · 27-NOV-2026",
# but every row is of the meeting of 28 Nov) + list 28.11 REVISED after the meeting (+ the morning list again).
# Frozen call (v288): Crystal Land 2 · Rex 5 · Meghna Prestige 16 · KM Jakarta 15A · Tai Keystone 8 · Star Unity 13 · Tug Marigold 3 · Sea Postman 7 · Josco Taicang 15.
# The meeting gave: Meghna Prestige → 13 "GOVT(30K)" · Zheng Run → 8 "HP(50K)" · Pacific Apex → 15A "HP(50K)" · Xin Bo → 16 "SGR" · and AG Varvara shifted 13 → 5 (port convenience).
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 28.11 (revised)'); q = B.q
L = 'LIST 28.11 (revised)'; P = 'PROGRAMME 29.11'
src = open('/home/claude/work/apply77.py', encoding='utf-8').read()
exec(src[src.index("src = open('/home/claude/work/apply74c.py'"):src.index("B.rep(\"const NOW=h('11-27 10:20');\"")])
B.rep("const NOW=h('11-28 11:12');", "const NOW=h('11-28 14:24');")
B.rep("const UPDATED='28 Nov 2026 · 11:20 IST';", "const UPDATED='28 Nov 2026 · 14:26 IST';")
B.rep("const PROG_END=h('11-28 18:00'); // programme 28.11 (meeting of 27 Nov) covers till here", "const PROG_END=h('11-29 18:00'); // programme 29.11 (meeting of 28 Nov) covers till here")
B.rep("<i>List</i><b>28.11</b>", "<i>List</i><b>28.11 · revised after the meeting</b>")
B.rep("<i>Programme</i><b>28.11</b>", "<i>Programme</i><b>29.11</b>")
B.rep("berthing list 28.11 (07:00; no list came for 22.11 or 24.11) · programme 28.11 ·", "berthing list 28.11 as revised after the meeting (no list came for 22.11 or 24.11) · programme 29.11 ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 29.11 (meeting of 28 Nov; the sheet is still headed \"movement for 28.11.2026\") · list 28.11 as revised after the meeting · ")
setline("const CALL_FROZEN={d:'11-28',", "const CALL_FROZEN=null; // {d,at,basis,call} = the meeting call as it stood BEFORE the meeting, when papers written after it reach the board before the programme; null = show the live call")
ML = ("{d:'11-28',at:'11-27 23:33',basis:'board v288 — list 27.11 (revised) · DPR 27.11 · HM signals to the evening sheet of 27 Nov',prog:'29.11',"
      "call:[['Crystal Land','2'],['Rex','5'],['Meghna Prestige','16'],['KM Jakarta','15A'],['Tai Keystone','8'],['Star Unity','13'],['Tug Marigold + barge Alaacrity 666','3'],['Sea Postman','7'],['Josco Taicang','15']],"
      "got:[['Meghna Prestige','13'],['Zheng Run','8'],['Pacific Apex','15A'],['Xin Bo','16']],note:'" + q(
      "FOUR BERTHS GIVEN, NONE CALLED RIGHT — one vessel right at the wrong berth and in the wrong line (Meghna Prestige). The port also shifts AG Varvara from CJ-13 to CJ-5 on its own account; the board of the morning (v289) had that shift. "
      "(1) HP: both places went at \"HP(50K)\" to ZHENG RUN (pellets, HP 3) at CJ-8 and PACIFIC APEX (aggregates, HP 4) at CJ-15A. Sea Postman (ball clay, HP 1) and Meghna Prestige (salt, HP 2) are senior in the column and did not get HP — the bid is at 50,000 and only cargo that can do 50,000 a day takes it. The board had seated the seniors of the column. "
      "(2) MEGHNA PRESTIGE took the vacant Govt place as \"GOVT(30K)\" at CJ-13 — the berth AG Varvara is shifted out of. The board had her under HP at CJ-16. Tai Keystone (Govt, urea) got nothing though Zheng Hui leaves CJ-8. "
      "(3) XIN BO took the SAAGAR bulk place Asian Summit leaves — \"SGR\" at CJ-16 behind MSC Magali. The revised list has her SGR 7 and KM Jakarta with no SAAGAR rank any more; the board had KM Jakarta. Xin Bo was not on the waiting sheet when the call was frozen. "
      "(4) The outgoing vessels WERE declared this time: Asian Summit 28 Nov 20:00, Zheng Hui 23:30, Hai Nam 81 29 Nov 01:54, MSC Magali 05:00. DSM London and Safi Alfa — about 2,300 and 3,000 MT left at 07:00 — were NOT declared, so Crystal Land, Tug Marigold and the General vessels got nothing. Jumbo Kinetic and Xin Hai Tong 71 not declared either (Sea Postman, Josco Taicang, Star Unity). "
      "LESSONS: HP(50K) goes to pellets / aggregates / coal, not to salt or clay; a salt vessel of the HP column takes a vacant Govt place at 30K; the port moved a log vessel to CJ-5 to open a clean berth for salt.") + "'},")
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")
# ================= V =================
M = "{b:'5',n:'Asian Summit',nm:16100,p:[30.5,39.25]"
pre(M, P + ": OUT readiness 28 NOV 20:00 · 7.08 m · night sailing → AG VARVARA shifts in from CJ-13."); setf(M, t='11-28 20:00')
M = "{b:'13',n:'AG Varvara',nm:4000,p:[112,125]"
pre(M, P + ": NIGHT SHIFTING FROM CJ-13 TO CJ-05 · 30½–39¼ · \"PORT C.\" — port convenience — behind Asian Summit (out 28 Nov 20:00) → she leaves CJ-13 about 22:00 on 28 Nov, est. CJ-13 then goes to Meghna Prestige (salt)."); setf(M, t='11-28 22:00')
M = "{b:'8',n:'Zheng Hui',p:[58,67.75]"
pre(M, P + ": OUT readiness 28 NOV 23:30 · 7.1 m · night sailing → ZHENG RUN in, HP(50K)."); setf(M, t='11-28 23:30')
M = "{b:'15A',n:'Hai Nam 81',nm:30000,p:[157.5,166.25]"
pre(M, P + ": OUT readiness 29 NOV 01:54 · 12.6 m · night sailing → PACIFIC APEX in, HP(50K)."); setf(M, t='11-29 01:54')
M = "{b:'16',n:'MSC Magali',nm:50000,p:[169.5,188]"
pre(M, P + ": OUT readiness 29 NOV 05:00 · 7.7 m · night sailing → XIN BO in, SGR."); setf(M, t='11-29 05:00')
for m_ in ("{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]", "{b:'4',n:'Safi Alfa',nm:3450,p:[21.25,29.5]", "{b:'7',n:'Jumbo Kinetic',p:[52,57]", "{b:'15',n:'Xin Hai Tong 71',p:[143,156.25]"):
    pre(m_, P + ": NO OUTWARD ROW for her berth — her completion was not declared at the meeting of 28 Nov; the berth is for the meeting of 29 Nov.")
NEWV = [
 " {b:'5',n:'AG Varvara',nm:4000,p:[30.5,39.25],c:'JAS pine logs',q:39113,u:'CBM',cat:'SAAGAR',f:'11-28 23:00',t:'12-05 08:52',est:1,note:'" + q(
   P + ": NIGHT SHIFTING FROM CJ-13 TO CJ-05 · 30½–39¼ · \"PORT C.\" (port convenience) — behind Asian Summit, out readiness 28 Nov 20:00 → alongside CJ-5 about 23:00 on 28 Nov, est. She keeps her SAAGAR break-bulk place. 26,617 CBM left at 07:00 on 28 Nov; list ETC 5 Dec 08:52. THE PORT MOVES THE LOG VESSEL OFF THE CLEAN BERTH to berth a salt vessel (Meghna Prestige) at CJ-13.") + "'},",
 " {b:'13',n:'Meghna Prestige (salt, next call)',nm:30000,p:[113,125.25],c:'Salt in bulk',q:65900,u:'MT',cat:'GOV',via:'30k/25k quote (Sr No 7)',f:'11-29 00:30',t:'12-01 05:15',est:1,note:'" + q(
   P + ": CJ-13 · IN · 113–125¼ · CATEGORY \"GOVT(30K)\" · night berthing · sailing draught 12.5 m — the berth AG Varvara is shifted out of → about 00:30 on 29 Nov, est. 65,900 MT of salt at 30,000 a day → about 1 Dec 05:15, est. "
   "Revised list: HP 2 · GEN 27 · \"30K/25K/10K S.NO 07\"; reported / ready 24 Nov 11:30; 199.95 m. SHE TAKES THE VACANT GOVT PLACE ON A 30K QUOTE — Zheng Hui (Govt) leaves and Tai Keystone was not berthed.") + "'},",
 " {b:'8',n:'Zheng Run',nm:50000,p:[58,67.75],c:'Oxide pellets',q:66100,u:'MT',cat:'HP',f:'11-29 02:00',t:'11-30 09:45',est:1,note:'" + q(
   P + ": CJ-08 · IN behind Zheng Hui (out readiness 28 Nov 23:30) · 58–67¾ · CATEGORY \"HP(50K)\" · night berthing · sailing draught 12.7 m → about 02:00 on 29 Nov, est. 66,100 MT of pellets at 50,000 a day → about 30 Nov 09:45, est. "
   "Revised list: HP 3 · GEN 28 · \"TRANSHIPMENT 30K/25K/10K SR.NO 07\"; reported / ready 24 Nov 13:24; 229 m, gearless.") + "'},",
 " {b:'15A',n:'Pacific Apex',nm:50000,p:[161,172.5],c:'Aggregates',q:63700,u:'MT',cat:'HP',f:'11-29 04:30',t:'11-30 11:05',est:1,note:'" + q(
   P + ": CJ-15A · IN behind Hai Nam 81 (out readiness 29 Nov 01:54) · 161–172½ · CATEGORY \"HP(50K)\" · night berthing · sailing draught 13.81 m → about 04:30 on 29 Nov, est. 63,700 MT of aggregates at 50,000 a day → about 30 Nov 11:05, est. "
   "Revised list: HP 4 · GEN 29; reported / ready 24 Nov 18:18; 199.98 m. AGGREGATES AT A CLEAN BERTH — as Mihir said on 27 Nov, aggregates are not dirty cargo.") + "'},",
 " {b:'16',n:'Xin Bo',p:[174.5,188],c:'Salt in bulk',q:50000,u:'MT',cat:'SAAGAR',via:'SAAGAR bulk place — behind Asian Summit',f:'11-29 07:30',t:'12-01 09:30',est:1,note:'" + q(
   P + ": CJ-16 · IN behind MSC Magali (out readiness 29 Nov 05:00, night sailing) · 174½–188 · CATEGORY \"SGR\" · night berthing · sailing draught 12.25 m → about 07:30 on 29 Nov, est. 50,000 MT of salt — no norm printed; at about 24,000 a day (Hai Nam 81\'s pace) → about 1 Dec 09:30, est. "
   "MIHIR & COMPANY. Revised list: HP 8 · SGR 7 · 8K 11 · GEN 36 · \"30K/25K/10K SR.NO 07 DD-12.25M LP: Bin Qasim\"; reported / ready 27 Nov 08:45; 189.99 m. SHE TAKES THE SAAGAR BULK PLACE ASIAN SUMMIT LEAVES — KM Jakarta, who stood ahead of her, has no SAAGAR rank on the revised list.") + "'},",
]
a, b = B.line_of(" {b:'13',n:'AG Varvara',nm:4000,p:[112,125]")
B.s = B.s[:a] + "\n".join(NEWV) + "\n" + B.s[a:]
a, b = B.line_of("Object.assign(LOA,{'Safi Alfa':189.99,")
B.s = B.s[:b] + "\nObject.assign(LOA,{'Meghna Prestige (salt, next call)':199.95,'Zheng Run':229,'Pacific Apex':199.98,'Xin Bo':189.99}); // programme 29.11" + B.s[b:]
for n in ('Meghna Prestige (salt, next call)', 'Zheng Run', 'Pacific Apex', 'Xin Bo'): B.wdel(n)
# ================= W — the revised list =================
s85 = open('/home/claude/work/apply85a.py', encoding='utf-8').read()
blk = s85[s85.index("board = {}\na = B.s.index('const WRAW=[')"):s85.index("ETAROWS = cj('ETA')")]
blk = blk.replace("/home/claude/work/in28/l28.json", "/home/claude/work/in28p/l28r.json").replace("SKIP = {'Shree Krishna IX'}", "SKIP = {'Shree Krishna IX', 'African Loon', 'Sheng Tai'}")
blk = blk.replace("b in ('Xin Bo', 'Bunun Miracle', 'Tomkar', 'Jiaxin', 'Star New London', 'Paiwan Wisdom', 'Propel Fortune', 'New Faith', 'New Joyful', 'Tug Canara Jog + barge RMG 254')", "False")
exec(blk)
def w(name, text, **k): B.wrow(name, q(text), **k)
w('KM Jakarta', "HER SAAGAR RANK IS GONE — only HP 6 · GEN 34 now (she was SGR 7 this morning) · " + P + ": the SAAGAR bulk place went to Xin Bo")
w('Tai Keystone', P + ": NOT ON IT — Zheng Hui (Govt) leaves CJ-8 on 28 Nov 23:30 and the berth goes to Zheng Run under HP(50K); the vacant Govt place goes to Meghna Prestige at 30K")
w('Sea Postman', P + ": NOT ON IT though HP 1 — both HP places went at 50K to Zheng Run and Pacific Apex")
w('CD Glory', "MIHIR · SGR 1 · 8K 5 · GEN 13 · " + P + ": not on it — the SAAGAR place given was the BULK place (to Xin Bo); AG Varvara keeps the break-bulk place, at CJ-5 now")
w('Paiwan Ace', "MIHIR · SGR 4 · 8K 8 · GEN 21 · " + P + ": not on it")
m = B._row('Star Unity').search(B.s); e = B.s.index("],\n", m.start()) + 3
B.s = B.s[:e] + " ['Kadhim','Rice bags',2800,'MT',79.99,null,null,{},'" + q(L + " (ETA sheet): NEW · rice in bags 2,800 MT EXP · ETA 29 Nov 08:00 · N/A · 79.99 m · agent Nexwave") + "'],\n" + B.s[e:]
w('Jaador', "(ETA sheet) HP Y · \"30K/25K/10K SR.NO 07 LP: Bin Qasim, Pakistan\"", rk="HP:98")
a, b = B.line_of("const ETA={"); ln = B.s[a:b]
for k, v in (("'Team Bravo':'11-29 00:00'", "'Team Bravo':'11-29 00:30','Kadhim':'11-29 08:00'"),):
    assert k in ln, k; ln = ln.replace(k, v)
B.s = B.s[:a] + ln + B.s[b:]
a, b = B.line_of("Object.assign(AG,{'Shree Krishna IX':'Indoglobal',")
B.s = B.s[:b] + "\nObject.assign(AG,{'Kadhim':'Nexwave'});IE['Kadhim']='EXP'; // list 28.11 (revised)" + B.s[b:]
# ================= LIQ / TUNA =================
setnow('OJ-1', 'Lumis', P + ': OUT readiness 29 NOV 15:30, 7.2 m → LPG/C KRUIBEKE in (ETA 29 Nov 12:30, starboard, priority, arrival draught 9.60 m)', etc='11-29 15:30')
setnow('OJ-2', 'Bow Saturn', P + ': OUT readiness 29 NOV 05:00, 6.5 m, night sailing → MT BOW TRIBUTE in, night berthing', etc='11-29 05:00')
setnow('OJ-3', 'SC Draco', P + ': NIGHT SHIFTING FROM OJ-03 TO OJ-04 behind Chemroad Quest (out 28 Nov 18:30) · "A/C ATLANTIC" → OJ-3 then takes MT YC AZALEA, night berthing')
setnow('OJ-4', 'Chemroad Quest', P + ': OUT readiness 28 NOV 18:30, 8.0 m, night sailing → MT SC DRACO shifts in from OJ-3', etc='11-28 18:30')
setnow('OJ-5', 'Volga', P + ': OUT readiness 29 NOV 05:00, 5.5 m, night sailing → MT STOLT LIND in (ETA 29 Nov 15:30, starboard, arrival draught 10.50 m)', etc='11-29 05:00')
for nm_, tx in (('Kruibeke', 'OJ-01 · IN behind Lumis (out 29 Nov 15:30) · priority · starboard'), ('Bow Tribute', 'OJ-02 · IN behind Bow Saturn (out 29 Nov 05:00) · night berthing'), ('YC Azalea', 'OJ-03 · IN when SC Draco has shifted to OJ-4 · night berthing'), ('Stolt Lind', 'OJ-05 · IN behind Volga (out 29 Nov 05:00) · ETA 29 Nov 15:30 · starboard')):
    if B.s.count("  {n:'%s'," % nm_) == 1: rem(nm_, P + ': ' + tx)
    else: print('no liquid wait row for', nm_)
B.s, k = re.subn(r"const LIQ=\{prog:'", lambda m: "const LIQ={prog:'" + q("PROGRAMME 29.11 — OJ-4 Chemroad Quest OUT 28 Nov 18:30 → SC DRACO shifts from OJ-3 → OJ-3 YC AZALEA in · OJ-2 Bow Saturn OUT 29 Nov 05:00 → BOW TRIBUTE · OJ-5 Volga OUT 29 Nov 05:00 → STOLT LIND (ETA 15:30) · OJ-1 Lumis OUT 29 Nov 15:30 → LPG/C KRUIBEKE · "), B.s, count=1)
B.rep("asOf:'11-28 11:12',", "asOf:'11-28 14:24',")
a, b = B.line_of("  {b:'TT-1',n:"); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(P + ": OUT readiness 29 NOV 11:00, 7.5 m — no inward vessel printed. ") + B.s[i:]
# ================= ENGINE — what the meeting of 28 Nov showed =================
B.rep("if(k==='HP'){l=l.filter(w=>(+w.q||0)>=40000)", "if(k==='HP'){l=l.filter(w=>(+w.q||0)>=40000&&!/salt|clay/i.test(w.c||'')) /* meeting of 28 Nov: the bid is at 50,000 a day — pellets and aggregates took both places over the salt and clay vessels senior to them in the column; salt takes a vacant Govt / Coastal place at 30K instead */")
B.save(); print('saved 86')
B.rep("const PROG_SAIL=new Set(['Tug Varahi + barge AKG 11',","const PROG_SAIL=new Set(['Asian Summit','Zheng Hui','Hai Nam 81','MSC Magali','Tug Varahi + barge AKG 11',") # outward rows of programme 29.11 (applied after save in v290)
