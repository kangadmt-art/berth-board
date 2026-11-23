#!/usr/bin/env python3
# apply61 — v264: two papers received 23 Nov 14:10, no text —
#   PROGRAMME 24.11 (TF/SH/2102 dt 23 Nov 2026, xlsx) and the DAILY BERTHING LIST 23.11 as REVISED after the meeting (xlsx).
# Cargo jetties: CJ-5 Vishva Bandhan out 18:30 → BLUE SHARK (GEN) · "CJ-07" Flag Marina out 21:00 → ZHENG HUI (GOVT) at 58–67¾ and GOKOVA-M (HP(50K)) at 50½–57,
#   Parvraj shifted to 41¼–49½ (port convenience) · CJ-15A Belmoira out 20:28 → OCEAN KUDOS (24HRS(30K)) · CJ-3 Horizon Chaser (bitumen tanker, space a/c).
# The 23 Nov meeting is scored on the call frozen at 02:16 (Gokova-M → 8 · Blue Shark → 15A · Zheng Hui → 7 · Manta Sena → 1).
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 23.11 (revised)'); q = B.q
P = 'PROGRAMME 24.11'; LR = 'LIST 23.11 (revised after the meeting)'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)
def pre(m, t): B.note_prefix(m, q(t) + " ")
def sub(m, o, n): B.sub_entry(m, o, n)
def after(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:b + 1] + text + "\n" + B.s[b + 1:]
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]

# ================= HEADER =================
B.rep("const NOW=h('11-23 11:06');", "const NOW=h('11-23 14:10');")
B.rep("const PROG_END=h('11-23 18:00'); // programme 23.11 (meeting of 22 Nov) covers till here", "const PROG_END=h('11-24 18:00'); // programme 24.11 (meeting of 23 Nov) covers till here")
B.rep("<i>Programme</i><b>23.11</b>", "<i>Programme</i><b>24.11</b>")
B.rep("<i>List</i><b>23.11 · 0700</b>", "<i>List</i><b>23.11 · revised after the meeting</b>")
B.rep("berthing list 23.11 (position 07:00; no list came for 22.11) · programme 23.11 ·", "berthing list 23.11 as revised after the meeting (no list came for 22.11) · programme 24.11 ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 24.11 (TF/SH/2102 dt 23 Nov) · list 23.11 revised after the meeting · ")
B.rep("const PROG_SAIL=new Set(['Tug Sagar 5 + barge Victoria 250',", "const PROG_SAIL=new Set(['Vishva Bandhan','Flag Marina','Belmoira','Tug Sagar 5 + barge Victoria 250',")
a, b = B.line_of("const CALL_FROZEN={d:'11-23',at:'11-23 02:16'")
B.s = B.s[:a] + "const CALL_FROZEN=null; // {d,at,basis,call} = the meeting call as it stood BEFORE the meeting, when papers written after it reach the board before the programme; null = show the live call" + B.s[b:]

# ================= V — sailings and changes =================
M = "{b:'5',n:'Vishva Bandhan',nm:8050,p:[33.25,41.5]"
pre(M, P + ": CJ-05 · OUT readiness 23 Nov 18:30, 6.7 m, night sailing → MV BLUE SHARK takes the berth (32½–40, GEN, night berthing).")
sub(M, "f:'11-21 11:24',t:'11-23 07:40'", "f:'11-21 11:24',t:'11-23 18:30',lt:'11-23 07:40'")
M = "{b:'7',n:'Flag Marina',nm:42500,p:[56.75,67.25]"
pre(M, P + ": \"CJ-07\" · OUT readiness 23 Nov 21:00, 6.9 m, night sailing → two vessels take her length: MV ZHENG HUI (58–67¾, GOVT) and MV GOKOVA-M (50½–57, HP(50K)).")
sub(M, "f:'11-21 12:45',t:'11-24 01:03'", "f:'11-21 12:45',t:'11-23 21:00',lt:'11-24 01:03'")
M = "{b:'15A',n:'Belmoira',nm:30000,p:[160.5,171.75]"
pre(M, P + ": CJ-15A · OUT readiness 23 Nov 20:28, 13.0 m, night sailing → MV OCEAN KUDOS takes the berth (159¼–171¾, 24HRS(30K)).")
M = "{b:'6',n:'Parvraj',nm:14950,p:[43,51.25]"
pre(M, P + ": CJ-06 · NIGHT SHIFTING AT PANELS to 41¼–49½ (from 43–51¼) · \"PORT C.\" — moved two panels south at the port's convenience to open 50½–57 for Gokova-M. No outward row for her.")
B.rep(M, "{b:'6',n:'Parvraj',nm:14950,p:[41.25,49.5]")
M = "{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]"
pre(M, LR + ": quantity now 15,770 MT (14,321 on the 0700 list) · ETC 24 NOV 23:43 (18:22 before). " + P + ": no outward row for her — she works through the window; Manta Sena (8K 1) waits for the next programme.")
sub(M, "c:'Sugar bags',q:14321,u:'MT',cat:'8K',f:'11-22 11:30',t:'11-24 18:22'", "c:'Sugar bags',q:15770,u:'MT',cat:'8K',f:'11-22 11:30',t:'11-24 23:43'")

# ================= V — the five inward vessels of programme 24.11 =================
NEWV = [
 " {b:'5',n:'Blue Shark',p:[32.5,40],c:'Sugar/rice/wheat bags',q:26500,u:'MT',cat:'GEN',f:'11-23 20:30',t:'11-30 15:30',est:1,note:'" + q(
   P + ": CJ-05 · IN behind Vishva Bandhan (out readiness 23 Nov 18:30) · 32½–40 · CATEGORY GEN · night berthing. About 20:30 alongside, est; 26,500 MT of bags → about 30 Nov 15:30 at the board's bag rate, est — the list will print her norm and ETC. "
   "Waiting sheet: GEN 1 — the senior vessel of the General line; reported 15 Oct 21:30, ready 19 Nov 11:00; 167 m, 5.9 m; agent Interocean. "
   "The board's call had named her for this meeting, at CJ-15A; the port gave her the berth left over at CJ-5 once the Govt vessel had gone to the long berth.") + "'},",
 " {b:'8',n:'Zheng Hui',p:[58,67.75],c:'DAP',q:66000,u:'MT',cat:'GOV',f:'11-23 23:00',t:'11-28 13:55',est:1,note:'" + q(
   P + ": printed \"CJ-07\" · IN behind Flag Marina (out readiness 23 Nov 21:00) · 58–67¾ · CATEGORY GOVT · night berthing. These are the board's CJ-8 panels (the port counts the whole length as CJ-07). About 23:00 alongside, est; 66,000 MT at the DAP norm of 14,950 → about 28 Nov 14:00, est. "
   + LR + ": GP 1 — the first Govt rank printed for her · GEN 26; reported / ready 21 Nov 07:54; 229 m, 12.85 m, gearless; agent Interocean.") + "'},",
 " {b:'7',n:'Gokova-M',nm:50000,p:[50.5,57],c:'Ball clay + J-bags',q:42000,u:'MT',cat:'HP',via:'HP bid · 50,000 a day (\"HP(50K)\")',f:'11-24 01:00',t:'11-25 03:15',est:1,note:'" + q(
   P + ": printed \"CJ-07\" · IN · 50½–57 · CATEGORY HP(50K) · night starboard — no hour printed; she can come only after Flag Marina has sailed (21:00) and Parvraj has shifted two panels south: about 01:00 on 24 Nov, est. "
   "HP on a bid of 50,000 MT a day: the list quantity of 50,500 MT is then one day's work → about 25 Nov 03:15, est (41,650 MT ball clay + 374 MT J-bags by the remark). "
   + LR + ": HP 1 · 24H 1 · 8K 4 · GEN 12; reported / ready 11 Nov 23:40 — twelve days waiting; 190 m, 6.1 m; agent Delta. She had been passed over three times for a 24-hours place at the clean berths (clay).") + "'},",
 " {b:'15A',n:'Ocean Kudos',nm:30000,p:[159.25,171.75],c:'Salt in bulk',q:70190,u:'MT',cat:'24H',via:'30k/25k quote (Sr No 7)',f:'11-23 22:30',t:'11-26 08:40',est:1,note:'" + q(
   P + ": CJ-15A · IN behind Belmoira (out readiness 23 Nov 20:28) · 159¼–171¾ · CATEGORY 24HRS(30K) · sailing draught 14.3 m · night berthing. About 22:30 alongside, est; 70,190 MT at her 30,000 quote → about 26 Nov 08:40, est. "
   + LR + ": HP 2 · 8K 10 · GEN 22 · \"30K/25K/10K SR.NO 07\"; reported / ready 18 Nov 16:06; 225 m, 7.1 m; agent True Blue. "
   "The board had held her as NOT READY on the team's word of 21 Nov 16:19 and so never called her; the list printed her ready throughout. Salt for salt at CJ-15A: Belmoira's 24-hours place goes to the next senior vessel on a 30K quote, as CJ-14 went to Lila Tokyo this forenoon.") + "'},",
 " {b:'3',n:'Horizon Chaser',p:[17.5,21.75],c:'Bitumen (tanker)',q:3820,u:'MT',cat:'SPACE',f:'11-23 22:00',t:'11-24 22:00',est:1,note:'" + q(
   P + ": CJ-03 · IN · 17½–21¾ · ETA 23 Nov 20:00 · NIGHT BERTHING · \"SPACE A/C\" · arrival draught 5.85 m. About 22:00 alongside, est; her last call (31 Oct – 1 Nov, the same berth, 3,902 MT) took 24 hours → out about 24 Nov 22:00, est. "
   + LR + " (ETA sheet): bitumen 3,820.32 MT IMP · ETA / readiness 23 Nov 20:00 · 94.4 m · agent Preetika. On space account — the Bitumen place itself is held by DSM London as General.") + "'},",
]
a, b = B.line_of(" {b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]")
B.s = B.s[:a] + "\n".join(NEWV) + "\n" + B.s[a:]
B.rep("'Hai Nam 81':189.94,'Lila Tokyo':229});", "'Hai Nam 81':189.94,'Lila Tokyo':229,'Blue Shark':167,'Zheng Hui':229});")
after("Object.assign(REP,{'Zheng Hui':'11-21 07:54','KM Jakarta':'11-21 21:48',", "Object.assign(REP,{'Horizon Chaser':'11-23 20:00'}); // this call — her October call had reported 30 Oct 15:24")

# ================= W — revised list 23.11 =================
for n in ('Blue Shark', 'Zheng Hui', 'Gokova-M', 'Ocean Kudos', 'Horizon Chaser'): B.wdel(n)
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Katerina K', "GEN 7 — the double number is put right (Pioneer Fortune stays GEN 6)", rk="GEN:7")
w('MK Lamis', "GEN 8", rk="GEN:8")
w('Ariston Bulker', "GEN 9", rk="GEN:9")
w('Aboudi D', "GEN 10 · 2 shore cranes required — the berth standing vacant beside her line went to the bitumen tanker on space account", rk="GEN:10")
w('African Loon', "GEN 11 printed · still held (STS at MS)", rk="GEN:11")
w('Marina L', "remark adds \"(6000MT - PENDING)\" · N/A · DOC NR")
w('Porto Fiscardo', "8K 5 · GEN 15", rk="'8K':5,GEN:15")
w('Captainannis L', "8K 6 · GEN 16", rk="'8K':6,GEN:16")
w('CD Glory', "SGR 3 · 8K 7 · GEN 17 — SAAGAR place unchanged; no SAAGAR vessel left in this programme, so none came in", rk="SAAGAR:3,'8K':7,GEN:17")
w('Dariya Priya', "SGR 4 · 8K 8 · GEN 18", rk="SAAGAR:4,'8K':8,GEN:18")
w('African Tiger', "SGR 5 · 8K 9 · GEN 21", rk="SAAGAR:5,'8K':9,GEN:21")
w('Tug Marigold + barge Alaacrity 666', "CSTL Y now printed · N/A", rk="COASTAL:98")
w('Josco Taicang', "STL 2 · GEN 23 (STL kept out of the board, as for Xin Hai Tong 71)", rk="GEN:23")
w('MSC Magali', "HP 3 · GEN 24", rk="HP:3,GEN:24")
w('Manta Omer Mecit', "GEN 25", rk="GEN:25")
w('Paiwan Ace', "MIHIR & COMPANY · SGR 6 · 8K 11 · GEN 27 — a General rank now printed too", rk="SAAGAR:6,'8K':11,GEN:27")
w('Asian Summit', "RANKED NOW — HP 4 · SGR 7 · GEN 28 (Y before)", rk="HP:4,SAAGAR:7,GEN:28")
w('Hai Nam 81', "RANKED NOW — HP 5 · 8K 12 · GEN 29 (Y before) · still waiting: the 24-hours place behind Belmoira went to Ocean Kudos, who reported four days before her", rk="HP:5,'8K':12,GEN:29")
w('African Pheasant', "RANKED NOW — SGR 8 · 8K 13 · GEN 30 (Y before) · quantity now 45,299.5 CBM", rk="SAAGAR:8,'8K':13,GEN:30", qty="45300")
w('Erna Oldendorff', "ARRIVED — ETA / readiness now printed 23 Nov 11:30 (expected sheet, first row) · SGR Y · Sr No 7", rdy="11-23 11:30")
w('Tai Keystone', "ETA / readiness moved to 24 Nov 06:30 (22 Nov 00:00 before) — still not arrived; no rank", rdy="11-24 06:30")
w('Zheng Run', "ETA / readiness moved to 24 Nov 18:00 (22 Nov 12:00 before) · now printed EXP · HP Y", rdy="11-24 18:00")
w('Meghna Prestige (salt, next call)', "ETA / readiness 24 Nov 12:00 — readiness declared in advance · HP Y · \"30K/25K/10K S.NO 07\"", rk="HP:98", rdy="11-24 12:00")
w('Saturn J', "ETA 23 Nov 21:00 · N/A")
w('Jumbo Kinetic', "ETA 24 Nov 08:00 · N/A · CSTL Y")
w('Kang Qi Fu Hua', "ETA 24 Nov 08:00 · N/A")
w('Kerem', "ETA 24 Nov 16:00 · N/A")
w('V Pacific', "ETA moved to 26 Nov (23 Nov before) · N/A")
w('Lolo Gate', "ETA moved to 26 Nov (23 Nov before) · N/A")
w('Outlander', "ETA moved to 26 Nov (23 Nov before) · N/A")
w('Hai Long 1', "ETA moved to 27 Nov (23 Nov before) · N/A")
w('KSS Edmond', "ETA moved to 30 Nov (24 Nov before) · N/A")
m = B._row('Saturn J').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Rex','Ball clay',63785,'MT',199.99,4.5,null,{},'" + q(LR + " (ETA sheet): NEW · ball clay 63,785 MT EXP · ETA 23 Nov 23:00 · N/A · 199.99 m, 4.5 m · departure draught 13.60 m · agent OTA Kandla") + "'],",
 " ['Star Unity','Rice bags',42000,'MT',189.9,5.9,null,{},'" + q(LR + " (ETA sheet): NEW · rice in bags 42,000 MT EXP · ETA 25 Nov · N/A · 189.9 m · agent Excel Infra") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
setline("const ETA={'Tai Keystone':", "const ETA={'Erna Oldendorff':'11-23 11:30','Saturn J':'11-23 21:00','Rex':'11-23 23:00','Tai Keystone':'11-24 06:30','Kang Qi Fu Hua':'11-24 08:00','Jumbo Kinetic':'11-24 08:00',"
        "'Meghna Prestige (salt, next call)':'11-24 12:00','Kerem':'11-24 16:00','Zheng Run':'11-24 18:00','Princess Manissa':'11-25 00:00','Star Unity':'11-25 00:00','V Pacific':'11-26 00:00','Lolo Gate':'11-26 00:00',"
        "'Outlander':'11-26 00:00','Valentina Sea':'11-26 00:00','Hai Long 1':'11-27 00:00','KSS Edmond':'11-30 00:00','Gutian Trust':'11-30 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 23.11 as revised after the meeting — Tai Keystone and Zheng Run are STILL printed on it")
after("Object.assign(AG,{'Horizon Chaser':'Preetika','Saturn J':'DBC','Jumbo Kinetic':'Gautham Freight'});", "Object.assign(AG,{'Rex':'OTA Kandla','Star Unity':'Excel Infra'});Object.assign(IE,{'Rex':'EXP','Star Unity':'EXP','Zheng Run':'EXP'}); // revised list 23.11")
B.rep("Object.assign(SAILDR,{'Hai Nam 81':12.6,'Zheng Run':12.63,'KM Jakarta':13.0});", "Object.assign(SAILDR,{'Hai Nam 81':12.6,'Zheng Run':12.63,'KM Jakarta':13.0,'Rex':13.6});")
B.rep("const GEAR_NONE=['KM Jakarta','Horizon Chaser','Saturn J','RB Leah',", "const GEAR_NONE=['Rex','Star Unity','KM Jakarta','Horizon Chaser','Saturn J','RB Leah',")

# ================= MEETLOG — the 23 Nov meeting, scored on the call frozen at 02:16 =================
ML = ("{d:'11-23',at:'11-23 02:16',basis:'list 21.11 (revised) · programme 23.11 · DPR 22.11 · HM signals to the night sheet of 22 Nov (disp 21:30 / 21:55)',prog:'24.11',"
      "call:[['Gokova-M','8'],['Blue Shark','15A'],['Zheng Hui','7'],['Manta Sena','1']],got:[['Horizon Chaser','3'],['Blue Shark','5'],['Gokova-M','7'],['Zheng Hui','8'],['Ocean Kudos','15A']],note:'" + q(
      "Three of the four vessels named, none on the berth the board gave her. Zheng Hui (GOVT) and Gokova-M (HP on a 50K bid) do take Flag Marina's length — the port prints both at \"CJ-07\": Gokova-M at 50½–57, Zheng Hui at 58–67¾ — so the two vessels and the two berths were right, each on the other's side. "
      "Blue Shark (GEN 1) came in, but at CJ-5 behind Vishva Bandhan, not at the clean berth. CJ-15A went to OCEAN KUDOS on a 30K quote under 24 hrs — salt for salt behind Belmoira; the board had held her as not ready on the team's word of 21 Nov. "
      "Nothing at CJ-1: Crystal O's ETC is now 24 Nov 23:43, so Manta Sena waits. CJ-3 went to the bitumen tanker Horizon Chaser on space account. "
      "What it shows: the port first counts which priority has a place vacant (Govt, HP, 24 hrs — one each — and one berth to spare for General rank 1), then puts each vessel on the berth that suits her; the vessel does not follow the berth her place-holder is leaving. "
      "The berth-wise meeting section of v262 had the right group for two of these four (Zheng Hui and Gokova-M at CJ-7 / 8) and missed Blue Shark at CJ-5 and Ocean Kudos at CJ-15A.") + "'},")
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")

# ================= LEARN =================
L1 = {'d': '23 Nov 14:10 · programme 24.11 — the meeting of 23 Nov',
      'v': "The four berthings of the cargo jetties given at the meeting of 23 Nov.",
      'exp': "The call frozen at 02:16: Gokova-M → CJ-8 (24 hrs quote) · Blue Shark → CJ-15A (General) · Zheng Hui → CJ-7 (Govt) · Manta Sena → CJ-1 (8K).",
      'act': "Programme 24.11: Zheng Hui GOVT at \"CJ-07\" 58–67¾ and Gokova-M HP(50K) at \"CJ-07\" 50½–57, both behind Flag Marina (Parvraj shifted two panels south, port convenience) · Blue Shark GEN at CJ-5 behind Vishva Bandhan · OCEAN KUDOS 24HRS(30K) at CJ-15A behind Belmoira · Horizon Chaser (bitumen tanker) at CJ-3 on space account · nothing at CJ-1 (Crystal O's ETC now 24 Nov 23:43).",
      'why': "Each vessel came into a place her own priority had vacant — the one rule held: Govt (Vishva Bandhan out) → Zheng Hui, GP 1; HP (Flag Marina out) → Gokova-M, HP 1, on a bid of 50,000 a day; 24 hrs (Belmoira out) → Ocean Kudos on a 30K quote, the senior ready quote vessel once Lila Tokyo had gone to CJ-14; and the berth to spare (Flag Marina had lain across two) → Blue Shark, GEN 1 — nothing is left vacant. The BERTH was then chosen to suit the vessel, not taken from the vessel leaving: Zheng Hui (229 m, gearless) to the long berth, Blue Shark to CJ-5. The board named three of the four but tied each to the berth her place-holder was leaving; it missed Ocean Kudos because it held her not ready on the team's word of 21 Nov, two days old.",
      'fix': "Entered from the programme. Three changes are proposed for the calculation and NOT made yet — Mihir to say yes: (1) count the vacant PLACES by priority first, then give each vessel the free berth that suits her; (2) a vacant Govt / Coastal / 24-hrs place taken on a 30K quote goes to the senior ready 30K-quote vessel whose cargo suits the berth (Belmoira 21 Nov, Lila Tokyo and Ocean Kudos 23 Nov); (3) a hold placed on a vessel on the team's word lapses when a later list still prints her ready and ranked.",
      'st': 'open'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(L1) + ",\n")

# ================= LIQ — programme 24.11 + revised list =================
def split_top(body):
    parts, depth, instr, esc, cur = [], 0, False, False, ''
    for ch in body:
        if instr:
            cur += ch
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == "'": instr = False
            continue
        if ch == "'": instr = True; cur += ch; continue
        if ch in '{[': depth += 1
        elif ch in '}]': depth -= 1
        if ch == ',' and depth == 0: parts.append(cur); cur = ''
        else: cur += ch
    if cur: parts.append(cur)
    return [[p[:p.index(':')], p[p.index(':') + 1:]] for p in parts]
def obj(text): return dict(split_top(text[1:-1]))
def unobj(d, order): return '{' + ','.join(k + ':' + d[k] for k in order if k in d) + '}'
NOWKEYS = ('n', 'c', 'q', 'u', 'ie', 'loa', 'f', 'est', 'nm', 'rank', 'ag', 'etc', 'note')
def berth(bid, nown, add, etc=None, qty=None):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]; tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln; d = dict(split_top(core[3:-1])); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    if etc is not None: now['etc'] = js(etc)
    if qty is not None: now['q'] = repr(qty)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS)
    B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in ('b', 'prev', 'now')) + '}' + tail + B.s[b:]
berth('OJ-1', 'Hafnia Ammolite', P + ': NIGHT SHIFTING from OJ-01 to OJ-03 behind Hartati (out readiness 23 Nov 23:00) · "A/C OF ATLANTIC" → LPG/C BOGAZICI then takes OJ-01 (night starboard, "PRIO")')
berth('OJ-2', 'Rasheeda', P + ': OUT readiness 24 Nov 07:00, 5.4 m → MT CHEMROUTE PEGASUS in · ' + LR + ': quantity 4,356.023 MT (3,156 on the 0700 list) · ETC 24 NOV 06:13', etc='11-24 07:00', qty=4356.02)
berth('OJ-3', 'Hartati', P + ': OUT readiness 23 Nov 23:00, 9.4 m, night sailing → MT HAFNIA AMMOLITE shifts in from OJ-01', etc='11-23 23:00')
berth('OJ-7', 'Ginga Cheetah', P + ': OUT readiness 24 Nov 05:14, 6.1 m, night sailing → MT SRIWANGI V in (night starboard) · ' + LR + ': ETC 24 NOV 05:14 (03:14 before)', etc='11-24 05:14')
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
wait = [r.rstrip(',') for r in B.s[w0 + len(" wait:[\n"):e0].split('\n')]
eta = [r.rstrip(',') for r in B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n')]
def nm_(r): return re.match(r"  \{n:'((?:[^'\\]|\\.)*)'", r).group(1)
def setf(r, key, val):
    rx = re.compile(r"\b" + key + r":(?:'(?:[^'\\]|\\.)*'|null|[0-9.]+)"); assert len(rx.findall(r)) == 1, (key, r[:90])
    return rx.sub(lambda _: key + ":" + (js(val)), r)
def remp(r, text):
    i = r.index("rem:'") + 5; return r[:i] + q(text) + (" · " if r[i] != "'" else "") + r[i:]
WCH = {
 'Chemroute Pegasus': lambda r: remp(r, P + ': OJ-02 — IN behind Rasheeda (out readiness 24 Nov 07:00)'),
 'Sriwangi V': lambda r: remp(r, P + ': OJ-07 — IN behind Ginga Cheetah (out readiness 24 Nov 05:14), night starboard'),
}
seen = set(); W2 = []
for r in wait:
    if nm_(r) in WCH: r = WCH[nm_(r)](r); seen.add(nm_(r))
    W2.append(r)
assert seen == set(WCH), set(WCH) - seen
TG = 'revised list 23.11: '
ECH = {
 'Bogazici (LPG/C)': lambda r: remp(setf(r, 'eta', '11-24 08:00'), P + ': OJ-01 — IN, night starboard, "PRIO", once Hafnia Ammolite has shifted to OJ-03 · ' + TG + 'ETA 24 Nov 08:00 (23 Nov 18:00 before)'),
 'Ginga Merlin': lambda r: remp(setf(setf(r, 'eta', '11-23 10:06'), 'rdy', '11-23 10:06'), TG + 'ARRIVED — reported / ready 23 Nov 10:06 (still printed on the expected sheet)'),
 'Culture': lambda r: remp(setf(r, 'eta', '11-23 19:00'), TG + 'ETA 23 Nov 19:00'),
 'YC Azalea': lambda r: remp(setf(r, 'eta', '11-23 22:00'), TG + 'ETA 23 Nov 22:00 (24 Nov 02:00 before)'),
 'Stolt Endurance': lambda r: remp(setf(r, 'eta', '11-24 08:00'), TG + 'ETA 24 Nov 08:00'),
 'SC Draco': lambda r: remp(setf(r, 'eta', '11-24 12:00'), TG + 'ETA 24 Nov 12:00'),
 'Camelia': lambda r: remp(setf(r, 'eta', '11-24 19:00'), TG + 'ETA 24 Nov 19:00 (25 Nov 04:00 before)'),
 'Western Carnation': lambda r: remp(setf(r, 'eta', '11-24 20:00'), TG + 'ETA 24 Nov 20:00'),
 'Bow Saturn': lambda r: remp(setf(setf(r, 'rdy', '11-25 00:00'), 'q', 8198.96), TG + 'readiness declared for 25 Nov 00:00 · chemicals 8,198.957 MT (6,600 before) · 9.0 m'),
 'No 5 Ocean Pioneer': lambda r: remp(setf(r, 'eta', '11-25 00:00'), TG + 'printed twice — 25 Nov (Atlantic Shg) and 26 Nov (Admiral)'),
 'Asian Aurora': lambda r: remp(setf(r, 'eta', '11-25 14:00'), TG + 'ETA 25 Nov 14:00 (24 Nov 22:00 before)'),
 'Chase Ocean': lambda r: remp(setf(r, 'eta', '11-26 00:01'), TG + 'ETA 26 Nov (24 Nov before)'),
}
names = [nm_(r) for r in eta]
def find(key):
    c = [n for n in names if n == key or n.startswith(key)]
    assert len(c) == 1, (key, c, names); return c[0]
ECH2 = {find(k): v for k, v in ECH.items()}
gs = find('Green Sanvi')
E2 = [ECH2[nm_(r)](r) if nm_(r) in ECH2 else r for r in eta if nm_(r) != gs]
for d in (
 {'n': 'Jag Vikram (LPG/C)', 'c': 'Propane & butane', 'q': 20000, 'u': 'MT', 'ie': 'IMP', 'loa': 174.2, 'dr': None, 'eta': '11-25 00:00', 'rdy': None, 'ag': 'Atlantic Shg', 'rem': 'new on the revised list 23.11'},
 {'n': 'Maria Glory', 'c': 'Naphtha', 'q': 30000, 'u': 'MT', 'ie': 'IMP', 'loa': 183.21, 'dr': None, 'eta': '11-26 00:00', 'rdy': None, 'ag': 'Atlantic Shg', 'rem': 'new on the revised list 23.11'},
 {'n': 'GC Argon', 'c': 'Chemicals', 'q': 5000, 'u': 'MT', 'ie': 'IMP', 'loa': 144.09, 'dr': 6, 'eta': '11-28 00:00', 'rdy': None, 'ag': 'GAC Shg', 'rem': 'new on the revised list 23.11'}):
    E2.append("  " + js(d))
E2.sort(key=lambda r: re.search(r"eta:'([^']*)'", r).group(1))
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(W2) + "\n ],\n eta:[\n" + ",\n".join(E2) + B.s[m0:]
B.s, k = re.subn(r"const LIQ=\{prog:'(?:[^'\\]|\\.)*',src:'(?:[^'\\]|\\.)*',asOf:'11-23 11:06',",
    lambda _: "const LIQ={prog:'" + q("PROGRAMME 24.11 — OJ-3 Hartati out 23 Nov 23:00 (9.4 m) → Hafnia Ammolite SHIFTS in from OJ-1 (night, a/c of Atlantic) → OJ-1 LPG/C Bogazici in (night starboard, PRIO) · OJ-7 Ginga Cheetah out 24 Nov 05:14 (6.1 m) → Sriwangi V · OJ-2 Rasheeda out 24 Nov 07:00 (5.4 m) → Chemroute Pegasus · revised list 23.11: LPG/C Green Sanvi CANCELLED")
    + "',src:'DPA berthing list 23.11.26 as revised after the meeting · DPR 23.11 · programme 24.11 · signals to the day sheet of 23 Nov (disp 0815 — no oil-jetty row on it)',asOf:'11-23 14:10',", B.s, count=1)
assert k == 1

# ================= TUNA =================
def tuna(bid, text):
    a, b = B.line_of("  {b:'%s',n:" % bid); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(text + " ") + B.s[i:]
tuna('TT-2', P + ": TT-02 · OUT readiness 24 Nov 17:45, 9.0 m — no inward vessel named for her berth.")
a, b = B.line_of("  {n:'RB Leah',"); i = B.s.index("rem:'", a) + 5; assert i < b
B.s = B.s[:i] + q("revised list 23.11: remark \"TT-03\" — she is meant for TT-3 · ") + B.s[i:]
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda _: "const TUNA={src:'" + q("DPA berthing list 23.11.26 as revised after the meeting · DPR 23.11 · programme 24.11 · TT-2 Woohyun Dream out 24 Nov 17:45 · TT-3 MP Postpanamax 1 berthing today behind Marvelous Star · TT-4 vacant") + "',", B.s, count=1)
assert k == 1

# ================= TIMBER =================
def tnote(name, text, tag=LR):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('CD Glory', "SGR 3 · 8K 7 · GEN 17")
tnote('Dariya Priya', "SGR 4 · 8K 8 · GEN 18")
tnote('African Tiger', "SGR 5 · 8K 9 · GEN 21")
tnote('Paiwan Ace', "SGR 6 · 8K 11 · GEN 27")
tnote('African Pheasant', "RANKED — SGR 8 · 8K 13 · GEN 30 · 45,299.5 CBM")
tnote('Erna Oldendorff', "ARRIVED — ETA / readiness printed 23 Nov 11:30 (expected sheet) · SGR Y")
B.rep("{n:'Erna Oldendorff',cbm:34424,from:'Australia',c:'Pine logs',eta:'11-23 12:00',", "{n:'Erna Oldendorff',cbm:34424,from:'Australia',c:'Pine logs',eta:'11-23 11:30',")

# ================= OPTS — CD Glory's 8K rank =================
a, b = B.line_of("  {label:'6.5K / 8K',only:'8K',rk:{'8K':8},"); ln = B.s[a:b]
assert ln.count("She is 8K 8 on list 23.11") == 1 and ln.count("Porto Fiscardo 6 and Captainannis L 7") == 1
ln = ln.replace("rk:{'8K':8}", "rk:{'8K':7}").replace("She is 8K 8 on list 23.11", "She is 8K 7 on the revised list 23.11").replace("Gokova-M 5, Porto Fiscardo 6 and Captainannis L 7", "Porto Fiscardo 5 and Captainannis L 6")
B.s = B.s[:a] + ln + B.s[b:]

B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='23 Nov 2026 · 14:20 IST';", B.s, count=1)
B.save()
