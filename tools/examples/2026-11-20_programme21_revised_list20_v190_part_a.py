#!/usr/bin/env python3
# apply35a — v190 (part 1, data): PROGRAMME FOR 21.11 (TF/SH/2102 dated 20 Nov, after the meeting) and the REVISED berthing list 20.11
# (a later issue of the same day: ranks renumbered, Belmoira's and Katerina K's at-berth rows taken out, expected sheet restated). Received 20 Nov 15:13, no text.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P, list_tag='LIST 20.11 (revised after the meeting)'); q = B.q
PG = 'PROGRAMME 21.11'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)
def pre(marker, text): B.note_prefix(marker, q(text) + " ")
def sub(marker, old, new): B.sub_entry(marker, old, new)
def vline(d): return " " + js(d) + ","
def after(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:b + 1] + text + "\n" + B.s[b + 1:]
def setline(prefix, text):
    a, b = B.line_of(prefix); B.s = B.s[:a] + text + B.s[b:]

# ================= HEADER =================
B.rep("const NOW=h('11-20 12:52');", "const NOW=h('11-20 15:13');")
setline("const PROG_END=", "const PROG_END=h('11-21 18:00'); // programme 21.11 (meeting of 20 Nov) covers till here — barge windows end here; beyond it no data")
B.rep("List <b>20.11 · 0700</b> · DPR <b>20.11</b> · Programme <b>20.11</b> · Signals to <b>20 Nov afternoon sheet (disp 1240)</b>",
      "List <b>20.11 · revised after the meeting</b> · DPR <b>20.11</b> · Programme <b>21.11</b> · Signals to <b>20 Nov afternoon sheet (disp 1240)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 20 Nov 15:13: the PROGRAMME FOR 21.11 (TF/SH/2102, dated 20 Nov) — Parvraj CJ-6, Flag Marina CJ-7 (HP 42.5K, 56¾–67¼), Uni Blossom CJ-13 behind Rome Trader (out 00:30), Yuan Hang Wei Ye CJ-9, Vishva Bandhan shifted CJ-8 → CJ-5 on the port's account — and the berthing list 20.11 as REVISED after the meeting (ranks renumbered: CD Glory SGR 4 · 8K 9) · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 21.11 · list 20.11 (revised after the meeting) · ")

# ================= V =================
M = "{b:'5',n:'Ken Ann',p:[33.5,41.5]"
pre(M, PG + ": OUT 21 Nov 16:00 (5.63 m) — and VISHVA BANDHAN is shifted into her place from CJ-8.")
sub(M, "f:'11-20 12:30',t:'11-21 12:30',est:1", "f:'11-20 12:30',t:'11-21 16:00',est:1")
M = "{b:'8',n:'Vishva Bandhan',nm:9258,p:[59.5,68]"
pre(M, PG + ": \"SHIFTING FROM CJ-08 TO CJ-05. PORT C.\" — she moves to 33¼–41½ when Ken Ann is out (21 Nov 16:00), on the port's account. The reason is FLAG MARINA: 254.62 m at 56¾–67¼ lies across CJ-7 and CJ-8. About 18:00 is the board's estimate for the move.")
sub(M, "f:'11-17 18:30',t:'11-22 14:33'", "f:'11-17 18:30',t:'11-21 18:00',lt:'11-22 14:33',est:1")
after(" {b:'5',n:'Ken Ann',p:[33.5,41.5],", vline({'b': '5', 'n': 'Vishva Bandhan', 'nm': 9258, 'p': [33.25, 41.5], 'c': 'Granular urea bulk', 'q': 44000, 'u': 'MT', 'cat': 'GOV', 'f': '11-21 18:00', 't': '11-22 14:33', 'est': 1,
    'note': PG + ': SHIFTED IN from CJ-8 on the port\'s account ("PORT C."), 33¼–41½, behind Ken Ann (out 21 Nov 16:00) — about 18:00, est. She keeps her Govt place and finishes here: list ETC 22 Nov 14:33 at the 9,258 norm. At the DPR 20.11 pace she would be done about 21 Nov 17:15 — almost as the shift falls due; DPR 21.11 will show how much is really left · granular urea 44,000 MT IMP · 190 m · agent JM Baxi'}))
B.rep("{b:'6',n:'Truong Minh Dream',nm:17193,p:[42.5,51.25]", "{b:'6',n:'Truong Minh Dream',nm:14950,p:[42.5,51.25]")
M = "{b:'6',n:'Truong Minh Dream',nm:14950,p:[42.5,51.25]"
pre(M, PG + ": OUT 20 Nov 18:15 (7.5 m), NIGHT SAILING → PARVRAJ. Revised list 20.11: norm restated 14,950 (17,193 in the morning issue), ETC 20 Nov 01:25.")
sub(M, "t:'11-20 18:15',lt:'11-19 13:46'", "t:'11-20 18:15',lt:'11-20 01:25'")
after(" {b:'6',n:'Truong Minh Dream',nm:14950,p:[42.5,51.25],", vline({'b': '6', 'n': 'Parvraj', 'nm': 14950, 'p': [43, 51.25], 'c': 'DAP', 'q': 49500, 'u': 'MT', 'cat': 'GOV', 'f': '11-20 21:30', 't': '11-24 05:00', 'est': 1,
    'note': PG + ': CJ-06 · 43–51¼ · GOV · "NIGHT SAILING. NIGHT BERTHING." behind Truong Minh Dream (out 18:15) — the berth that was "pending" on the 12:40 signal sheet. About 21:30 alongside, est (pilots Karan + Nikhil, after Jeil Crystal\'s 19:00). Revised list 20.11: GP 1 · GEN 28 · reported / ready 20 Nov 01:56 — berthed the day she arrived. DAP 49,500 MT IMP · 189.9 m · 11.66 m · no norm printed for her yet — 14,950 a day assumed (Truong Minh Dream\'s on the revised list), to about 24 Nov 05:00 · agent Interocean'}))
B.wdel('Parvraj')
M = "{b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75]"
pre(M, PG + ": OUT 20 Nov 19:39 (7.0 m), NIGHT SAILING → FLAG MARINA at 56¾–67¼ — not a night berthing: she comes in on 21 Nov once Vishva Bandhan has left CJ-8.")
after(" {b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75],", vline({'b': '7', 'n': 'Flag Marina', 'nm': 42500, 'p': [56.75, 67.25], 'c': 'US coal in bulk', 'q': 103250, 'u': 'MT', 'cat': 'HP', 'f': '11-21 18:00', 't': '11-24 04:20', 'est': 1,
    'note': PG + ': CJ-07 · 56¾–67¼ · HP(42.5K) — behind Meghna Prestige (out 20 Nov 19:39). At 254.62 m she lies ACROSS CJ-7 AND CJ-8, so she cannot come in until Vishva Bandhan has been shifted out of CJ-8 (after Ken Ann leaves CJ-5 at 16:00 on 21 Nov): the evening of 21 Nov — 18:00 on the board, est; CJ-7 lies empty for about a day until then, and CJ-8 is not free for anyone while she is alongside. Revised list 20.11: HP 3 · SGR 7 · 24H 2 · GEN 26 — taken on a 42,500 MTPD quote ahead of Gokova-M (HP 1) and Lila Tokyo (HP 2). US coal 103,250 MT IMP · 13.37 m · at 42,500 a day to about 24 Nov 04:20 · agent Benline'}))
B.wdel('Flag Marina')
M = "{b:'9',n:'Seacon Monaco',nm:20000,p:[69,76.75]"
pre(M, PG + ": OUT 21 Nov 15:00 (6.5 m) → YUAN HANG WEI YE.")
sub(M, "f:'11-18 06:36',t:'11-20 09:48'", "f:'11-18 06:36',t:'11-21 15:00',lt:'11-20 09:48'")
after(" {b:'9',n:'Seacon Monaco',nm:20000,p:[69,76.75],", vline({'b': '9', 'n': 'Yuan Hang Wei Ye (next call)', 'p': [69, 77.25], 'c': 'Iron ore pellets', 'q': 50455, 'u': 'MT', 'cat': 'PPP', 'f': '11-21 17:00', 't': '11-24 05:30', 'est': 1,
    'note': PG + ': CJ-09 · 69–77¼ · GFPL — behind Seacon Monaco (out 21 Nov 15:00); sailing draught 12.47 m. About 17:00 alongside, est. Revised list 20.11: now printed EXP (transhipment pellets 50,455 MT, loading) · HP 4 · 8K 12 · GEN 27. No norm printed — about 20,000 a day assumed (the GFPL berth\'s last vessel), to about 24 Nov 05:30 · 190 m · agent Genesis'}))
B.wdel('Yuan Hang Wei Ye (next call)')
M = "{b:'13',n:'Rome Trader (salt, next call)',nm:23000,p:[113,125.25]"
pre(M, "MIHIR & COMPANY · " + PG + ": OUT 21 Nov 00:30 at 12.9 m, NIGHT SAILING → UNI BLOSSOM, night berthing. Printed now — four hours inside her list ETC (04:40); it replaces the board's 21:00 estimate of this afternoon.")
sub(M, "f:'11-18 17:00',t:'11-20 21:00',lt:'11-21 04:40',est:1", "f:'11-18 17:00',t:'11-21 00:30',lt:'11-21 04:40'")
setline(" {b:'13',n:'Uni Blossom',", vline({'b': '13', 'n': 'Uni Blossom', 'nm': 4600, 'p': [113, 124.75], 'c': 'Pine logs', 'q': 34870, 'u': 'CBM', 'cat': 'SAAGAR', 'f': '11-21 02:30', 't': '11-28 16:30', 'est': 1,
    'note': PG + ': CJ-13 · 113–124¾ · SGR · "NIGHT SAILING. NIGHT BERTHING." behind Rome Trader (out 21 Nov 00:30) — about 02:30 alongside, est. The berth the board had read from the timber desk sheet; the desk\'s hour (20 Nov 23:00) moves by about three and a half hours. Revised list 20.11: SGR 1 · 8K 4 · GEN 10. Pine logs 34,870 CBM from Uruguay · arrived 9 Nov 11:36 · 179.97 m, 10.8 m · norm 4,600 CBM a day assumed (ML Egret\'s), to about 28 Nov 16:30 · agent Synergy'}))

# ================= name maps / constants =================
setline("const PROG_SAIL=new Set([", B.s[slice(*B.line_of("const PROG_SAIL=new Set(["))].replace("const PROG_SAIL=new Set([", "const PROG_SAIL=new Set(['Ken Ann','Meghna Prestige','Seacon Monaco',", 1))
a, b = B.line_of("const NOHP=new Set(["); ln = B.s[a:b]
assert ln.startswith("const NOHP=new Set(['Orion','Gokova-M']);")
B.s = B.s[:a] + ln.replace("const NOHP=new Set(['Orion','Gokova-M']);", "const NOHP=new Set(['Orion','Gokova-M','Lila Tokyo']);", 1) + " Lila Tokyo (HP 2, \"CJ 7 & 8, 13-16\") — CJ-7 / 8 went to Flag Marina (HP 3) at 42,500 on programme 21.11." + B.s[b:]
setline("const CALL_FROZEN=", "const CALL_FROZEN=null; // {d,at,basis,call} = the meeting call as it stood BEFORE the meeting, when papers written after the meeting reach the board before the programme (20 Nov: v189). null = show the live call. The 20 Nov call went into MEETLOG with programme 21.11.")
B.rep("W.forEach(w=>{w.rep=REP[w.n]?h(REP[w.n]):w.rdy;});",
      "Object.assign(REP,{'MSC Magali':'11-20 07:30'}); // revised list 20.11 — placed last so that it wins\nW.forEach(w=>{w.rep=REP[w.n]?h(REP[w.n]):w.rdy;});")
after("Object.assign(IE,{'Belmoira':'EXP',", "Object.assign(AG,{'V Pacific':'Excel Infra','Kerem':'BS Shg'});Object.assign(IE,{'V Pacific':'EXP','Kerem':'EXP','Yuan Hang Wei Ye (next call)':'EXP'}); // revised list 20.11 — Yuan Hang Wei Ye is printed EXP now (transhipment pellets, loading)")
B.rep("const GEAR_NONE=['North Gate',", "const GEAR_NONE=['V Pacific','Kerem','North Gate',")
setline("const ETA={'Tai Keystone':", "const ETA={'Manta Omer Mecit':'11-20 17:00','Tai Keystone':'11-21 00:00','Sanghi Sundarshan':'11-21 02:00','Zheng Hui':'11-21 10:00','Valentina Sea':'11-22 00:00','Princess Manissa':'11-22 00:00','V Pacific':'11-22 00:00',"
        "'Sand Topic':'11-22 03:00','Asian Summit':'11-22 08:00','Zheng Run':'11-22 12:00','Hai Nam 81':'11-22 16:00','Gutian Trust':'11-23 00:00','Hai Long 1':'11-23 00:00','Lolo Gate':'11-23 00:00','Outlander':'11-23 00:00',"
        "'KSS Edmond':'11-24 00:00','Kang Qi Fu Hua':'11-24 00:00','Kerem':'11-24 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 20.11 as revised after the meeting — MSC Magali reported 20 Nov 07:30")

# ================= W — revised list 20.11 =================
w = B.wrow
w('Crystal Land', "8K 2 · GEN 6 — the 8K column is renumbered: Manta Sena 1, Crystal Land 2", rk="'8K':2,GEN:6")
w('Libra', "GEN 7 · remark now only \"working at MS\" (the docs remark is gone)")
w('Pioneer Fortune', "8K 3 · GEN 8 · Sr No 7", rk="'8K':3,GEN:8")
w('Tan Bin 259', "8K 5 · GEN 14 · Sr No 7 · working at MRG 3", rk="'8K':5,GEN:14")
w('Gokova-M', "HP 1 · 24H 1 · 8K 6 · GEN 15 — passed again: CJ-7 / 8 to Flag Marina (HP 3) on a 42.5K quote", rk="HP:1,'24H':1,'8K':6,GEN:15")
w('AG Varvara', "SGR 2 · GEN 16 · Sr No 7 — next in the SAAGAR line once Uni Blossom is in", rk="SAAGAR:2,GEN:16")
w('Xin Hai Tong 71', "SGR 3 · STL 1 · GEN 17 (STL kept out — Mihir, 15 Nov)", rk="SAAGAR:3,GEN:17")
w('Porto Fiscardo', "8K 7 · GEN 18", rk="'8K':7,GEN:18")
w('Captainannis L', "8K 8 (was Y) · GEN 19 · DOC NR · working at MS", rk="'8K':8,GEN:19")
w('CD Glory', "SGR 4 · 8K 9 · GEN 20 · Sr No 7 — up one place in SAAGAR (Uni Blossom, AG Varvara and Xin Hai Tong 71 ahead); down one in 6.5K / 8K, where Captainannis L is now numbered ahead of her", rk="SAAGAR:4,'8K':9,GEN:20")
w('Dariya Priya', "SGR 5 · 8K 10 · GEN 21 · Sr No 7", rk="SAAGAR:5,'8K':10,GEN:21")
w('Sea Postman', "still NO Govt rank · GEN 22 · now printed IMP/EXP — \"EXP CLAY 40000MT AFTER DISCHARGING (TRUE BLUE)\": she loads clay after the rock phosphate is out")
w('Lila Tokyo', "HP 2 · GEN 24 · 30K/25K/10K Sr No 7 · CJ 7 & 8 or the clean berths — passed over: CJ-7 / 8 goes to Flag Marina (HP 3) at 42,500 on programme 21.11 (NOHP)", rk="HP:2,GEN:24")
w('African Tiger', "SGR 6 · 8K 11 · GEN 25 · Sr No 7", rk="SAAGAR:6,'8K':11,GEN:25")
w('Tai Keystone', "ETA / readiness moved to 21 Nov 00:00 (20 Nov 12:00 in the morning issue) — she had not arrived for the meeting of 20 Nov", rdy="11-21 00:00")
w('MSC Magali', "REPORTED / READY 20 Nov 07:30 (still printed on the expected sheet) · HP Y · 30K/25K/10K", rdy="11-20 07:30")
w('Manta Omer Mecit', "ETA / readiness 20 Nov 17:00", rdy="11-20 17:00")
w('Zheng Hui', "ETA / readiness 21 Nov 10:00 · GEN Y — no GP printed", rk="GEN:98", rdy="11-21 10:00")
w('Hai Nam 81', "ETA / readiness moved to 22 Nov 16:00 · 52,000 MT · HP Y · 8K Y", rdy="11-22 16:00", qty=52000)
w('Asian Summit', "ETA / readiness moved to 22 Nov 08:00", rdy="11-22 08:00")
w('Sand Topic', "ETA 22 Nov 03:00 · N/A")
w('Zheng Run', "ETA 22 Nov 12:00 · N/A")
w('Gutian Trust', "ETA 23 Nov · N/A")
w('Hai Long 1', "ETA 23 Nov · N/A")
w('Lolo Gate', "ETA 23 Nov · N/A")
w('Sanghi Sundarshan', "ETA 21 Nov 02:00 · N/A · \"SPACE A/C\"")
w('North Gate (re-berthing)', "remark now \"(2873MT – BALANCE)\" — as the DPR had it")
w('Belmoira', "her at-berth row (CJ-15, GOVT(30K)) is TAKEN OUT of the revised issue; the waiting sheet still shows her starred with X ranks. Not on programme 21.11")
w('Katerina K', "her at-berth row (CJ-6, B\\'TODAY) is TAKEN OUT of the revised issue; the waiting sheet still shows her starred, GEN X. Not on programme 21.11 — CJ-6 is Parvraj\\'s")
m = B._row('Princess Manissa').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['V Pacific','Rice in bags',42000,'MT',189.9,5.8,null,{},'" + q("LIST 20.11 (revised after the meeting; ETA sheet): NEW · ETA 22 Nov · N/A · rice in bags 42,000 MT EXP · agent Excel Infra") + "'],",
 " ['Kerem','Manganese ore',29950,'MT',171.45,6,null,{},'" + q("LIST 20.11 (revised after the meeting; ETA sheet): NEW · ETA 24 Nov · N/A · manganese ore 29,950 MT EXP · agent BS Shg") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
B.rep(" // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 20.11 (0700)", " // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 20.11 (0700) and its issue revised after the meeting of 20 Nov")

# ================= MV =================
MVN = ['Programme for 21.11 — TF/SH/2102 (dated 20 Nov, after the 11:00 meeting; received 20 Nov 15:13; window 20 Nov 18:00 → 21 Nov 18:00) — cargo-jetty rows', [
  ['18:15', 'OUT', 'Truong Minh Dream', 'CJ-6 → OTB · 7.5 m', '—', '11-20 18:15', 'NIGHT SAILING → Parvraj'],
  ['—', 'IN', 'Parvraj', 'OTB → CJ-6 · 43–51¼', '—', '11-20 21:30', 'GOV · NIGHT BERTHING — est'],
  ['19:39', 'OUT', 'Meghna Prestige', 'CJ-7 → OTB · 7.0 m', '—', '11-20 19:39', 'NIGHT SAILING → Flag Marina (day berthing, after the CJ-8 shift)'],
  ['22:40', 'OUT', 'Arrabbiata', 'CJ-11 → OTB · 6.8 m', '—', '11-20 22:40', 'NIGHT SAILING → TCI Anand'],
  ['00:30', 'OUT', 'Rome Trader', 'CJ-13 → OTB · 12.9 m', '—', '11-21 00:30', 'NIGHT SAILING → Uni Blossom · list ETC 04:40'],
  ['—', 'IN', 'Uni Blossom', 'OTB → CJ-13 · 113–124¾', '—', '11-21 02:30', 'SGR · NIGHT BERTHING — est'],
  ['09:30', 'IN', 'TCI Anand', 'OTB → CJ-11 · 87–95', '—', '11-21 11:30', 'ETA 21 Nov 09:30 · starboard · arrival draught 6.90 m · container — est'],
  ['15:00', 'OUT', 'Seacon Monaco', 'CJ-9 → OTB · 6.5 m', '—', '11-21 15:00', '→ Yuan Hang Wei Ye'],
  ['—', 'IN', 'Yuan Hang Wei Ye', 'OTB → CJ-9 · 69–77¼', '—', '11-21 17:00', 'GFPL · sailing draught 12.47 m — est'],
  ['16:00', 'OUT', 'Ken Ann', 'CJ-5 → OTB · 5.63 m', '—', '11-21 16:00', '→ Vishva Bandhan shifted in'],
  ['—', 'SHIFT', 'Vishva Bandhan', 'CJ-8 · 59½–68 → CJ-5 · 33¼–41½', '—', '11-21 18:00', '"SHIFTING FROM CJ-08 TO CJ-05. PORT C." — est'],
  ['—', 'IN', 'Flag Marina', 'OTB → CJ-7 / CJ-8 · 56¾–67¼', '—', '11-21 18:00', 'HP(42.5K) · 254.62 m, across both berths — after the shift, est'],
  ['—', '—', 'Not on the programme', 'CJ-3 (empty since Sea Gautham) · CJ-4 Safi Alfa (by the 12:40 signal) · ML Egret (no shift) · Belmoira · Katerina K · Aboudi D', '—', '11-21 18:00', '']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")

# ================= MEETLOG — the 20 Nov meeting, scored on the call frozen before it =================
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n {d:'11-20',at:'11-20 10:36',basis:'DPR 20.11 · list 20.11 · programme 20.11',prog:'21.11',\n"
      "  call:[['Aboudi D','3'],['Tai Keystone','7'],['Uni Blossom','13'],['Sea Postman','8']],\n"
      "  got:[['Parvraj','6'],['Flag Marina','7'],['Yuan Hang Wei Ye','9'],['Uni Blossom','13'],['Safi Alfa','4','signal']],\n"
      "  note:'" + q("Uni Blossom was right, berth too. Parvraj — reported that same morning, GP 1 — took the Govt place the board had given to Sea Postman's rock phosphate. Flag Marina took CJ-7 on a 42.5K quote; she lies across CJ-8 as well, so Vishva Bandhan is shifted to CJ-5. Tai Keystone had not arrived (readiness moved to 21 Nov). Nobody was sent to CJ-3. Safi Alfa (GEN 1) came into CJ-4 by signal.") + "'},\n")

# ================= LIQ =================
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
def berth(bid, fn):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]
    tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln
    d = split_top(core[3:-1]); keys = [k for k, _ in d]
    if set(keys) - {'b', 'prev', 'now', 'out', 'outBy', 'next'}: B.die('berth extra keys: ' + bid + ' ' + str(keys))
    d = fn(dict(d))
    order = [k for k in ('b', 'prev', 'now', 'out', 'outBy', 'next') if k in d]
    B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in order) + '}' + tail + B.s[b:]
def oj4(d):
    d['out'] = "'11-20 23:30'"
    d['outBy'] = js('PROGRAMME 21.11: Bow Endeavour outward readiness 20 Nov 23:30 (6.5 m), NIGHT SAILING — list ETC 21 Nov 00:10')
    d['next'] = js({'n': 'Eva Richway', 'c': 'Chemicals', 'q': 8627.19, 'u': 'MT', 'ie': 'IMP', 'loa': 145.53, 'f': '11-21 01:30', 'est': 1, 'rank': '2C', 'ag': 'GAC Shg',
        'note': 'PROGRAMME 21.11: OJ-04 behind Bow Endeavour (out 20 Nov 23:30), NIGHT BERTHING — about 01:30 on 21 Nov, est · revised list 20.11: rank 2C · reported / ready 18 Nov 15:48'})
    return d
berth('OJ-4', oj4)
def oj2(d):
    assert "Hatnyanawati" in d['next']
    d['outBy'] = js('PROGRAMME 21.11: Jeil Crystal outward readiness 20 Nov 19:00 (6.2 m), NIGHT SAILING · HM SIGNAL 20 Nov (12:40 sheet): RT OUT 19:00 · Capt Karan + Nikhil — list ETC 20 Nov 21:29')
    i = d['next'].index("note:'") + 6; d['next'] = d['next'][:i] + q("PROGRAMME 21.11: OJ-02 behind Jeil Crystal, NIGHT BERTHING · revised list 20.11: readiness 20 Nov 11:00, rank 1C · ") + d['next'][i:]
    return d
berth('OJ-2', oj2)
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
wait = [r.rstrip(',') for r in B.s[w0 + len(" wait:[\n"):e0].split('\n')]
eta = [r.rstrip(',') for r in B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n')]
def nm(r): return re.match(r"  \{n:'((?:[^'\\]|\\.)*)'", r).group(1)
def setf(r, key, val):                      # string field
    rx = re.compile(r"\b" + key + r":(?:'(?:[^'\\]|\\.)*'|null)"); assert len(rx.findall(r)) == 1, (key, r[:80]); return rx.sub(lambda _: key + ":" + ("'" + q(val) + "'" if val is not None else 'null'), r)
def setn(r, key, val):                      # numeric field
    rx = re.compile(r"\b" + key + r":(?:[0-9.]+|null)"); assert len(rx.findall(r)) == 1, (key, r[:80]); return rx.sub(lambda _: key + ":" + repr(val), r)
def remp(r, text):                          # prefix the remark
    i = r.index("rem:'") + 5; return r[:i] + q(text) + (" · " if r[i] != "'" else "") + r[i:]
TG = 'REVISED LIST 20.11: '
WCH = {
 'Ginga Cheetah': lambda r: remp(setf(setf(setf(r, 'rdy', '11-20 11:00'), 'rank', '1E'), 'c', 'CDSBO + CSFO'), TG + 'READINESS 20 Nov 11:00 · rank "1E" · "commercially ready" (the ullage remark is gone)'),
 'Hafnia Ammolite': lambda r: remp(setn(setf(setf(r, 'rdy', '11-20 11:00'), 'rank', '2E'), 'dr', 10.6), TG + 'READINESS 20 Nov 11:00 · rank "2E" · OJ-03 & 7 · 10.6 m'),
 'Lumis': lambda r: remp(setf(r, 'c', 'CPO / PFAD'), TG + 'CPO / PFAD · "OJ-03 ullage issue" · still N/A'),
 'Sriwangi V': lambda r: remp(setf(setf(r, 'rdy', '11-20 11:00'), 'rank', '3E'), TG + 'READINESS 20 Nov 11:00 · rank "3E" · "commercially ready"'),
 'Hartati': lambda r: remp(setf(setf(r, 'rdy', '11-20 11:00'), 'rank', '3C'), TG + 'READINESS 20 Nov 11:00 · rank "3C"'),
 'Bow Fortitude': lambda r: remp(setf(r, 'rank', '4C'), TG + 'rank "4C"'),
 'PVT Aurora': lambda r: remp(setf(r, 'rank', '5C'), TG + 'rank "5C"'),
 'Al Mahboobah': lambda r: remp(setf(r, 'rank', '6C'), TG + 'rank "6C"'),
}
seen = set(); W2 = []
for r in wait:
    n = nm(r)
    if n == 'Eva Richway': seen.add(n); continue
    if n in WCH: r = WCH[n](r); seen.add(n)
    W2.append(r)
assert seen == set(WCH) | {'Eva Richway'}, set(WCH) - seen
ECH = {
 'Thetis Leona': lambda r: remp(setn(r, 'dr', 10), TG + 'REQ OJ 2, 3, 4 · 10 m'),
 'Ocean Star': lambda r: remp(setf(setf(r, 'eta', '11-21 15:00'), 'rdy', '11-21 15:00'), TG + 'ETA / readiness 21 Nov 15:00 · REQ OJ 2, 3, 4'),
 'Chemroute Pegasus': lambda r: remp(setf(setf(r, 'eta', '11-21 21:00'), 'rdy', '11-21 21:00'), TG + 'ETA / readiness 21 Nov 21:00 · REQ OJ 2, 3, 4'),
 'Chemroad Nexus': lambda r: remp(setn(setn(setf(setf(r, 'eta', '11-22 00:30'), 'rdy', '11-22 00:30'), 'q', 10949.31), 'dr', 9.42), TG + 'ETA / readiness 22 Nov 00:30 · 10,949 MT (5,000 before) · 9.42 m · REQ OJ 2, 3, 4'),
 'Chemroad Quest': lambda r: remp(setf(r, 'eta', '11-22 08:00'), TG + 'ETA 22 Nov 08:00'),
}
seen = set(); E2 = []
for r in eta:
    n = nm(r)
    if n in ECH: r = ECH[n](r); seen.add(n)
    E2.append(r)
    if n == 'MC Hera':
        E2.append("  " + js({'n': 'Green Sanvi (LPG/C)', 'c': 'Propane & butane', 'q': 20000, 'u': 'MT', 'ie': 'IMP', 'loa': 225.28, 'dr': None, 'eta': '11-22 00:00', 'rdy': None, 'ag': 'Atlantic Shg', 'rem': 'new on the revised list 20.11'}))
assert seen == set(ECH), set(ECH) - seen
E2.sort(key=lambda r: re.search(r"eta:'([^']*)'", r).group(1))
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(W2) + "\n ],\n eta:[\n" + ",\n".join(E2) + B.s[m0:]
LMN = ['Programme for 21.11 — TF/SH/2102 (dated 20 Nov) — oil-jetty rows', [
  ['19:00', 'OUT', 'Jeil Crystal', 'OJ-2 → OTB · 6.2 m', '—', '11-20 19:00', 'NIGHT SAILING → Hatnyanawati, NIGHT BERTHING'],
  ['—', 'IN', 'Hatnyanawati', 'OTB → OJ-2', '—', '11-20 21:00', 'chemicals 10,000 EXP · est'],
  ['23:30', 'OUT', 'Bow Endeavour', 'OJ-4 → OTB · 6.5 m', '—', '11-20 23:30', 'NIGHT SAILING → Eva Richway, NIGHT BERTHING'],
  ['—', 'IN', 'Eva Richway', 'OTB → OJ-4', '—', '11-21 01:30', 'chemicals 8,627 IMP · rank 2C · est']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LMN) + ",\n" + B.s[mm:]
B.rep("const LIQ={src:'DPA berthing list 20.11.26 (0700) · DPR 20.11 · programme 20.11 (TF/SH/2102) · signals to the afternoon sheet of 20 Nov (disp 1240)',asOf:'11-20 12:52',",
      "const LIQ={src:'DPA berthing list 20.11.26 (revised after the meeting) · DPR 20.11 · programme 21.11 (TF/SH/2102) · signals to the afternoon sheet of 20 Nov (disp 1240)',asOf:'11-20 15:13',")

# ================= TUNA =================
a, b = B.line_of("  {b:'TT-1',n:'Europa Graeca',")
ln = B.s[a:b]
if not ln.endswith(','): ln += ','
B.s = B.s[:a] + ln + "\n  " + js({'b': 'TT-2', 'n': 'Woohyun Dream', 'c': 'RSM in bulk', 'q': 31500, 'u': 'MT', 'ie': 'EXP', 'loa': 183, 'f': '11-20 22:30', 'est': 1, 'ag': 'Taurus',
    'prev': 'vacant on every list since 10 Nov', 'next': 'nobody named',
    'note': 'PROGRAMME 21.11: TT-02, NIGHT BERTHING. Revised list 20.11: ETA / readiness 20 Nov 20:30, remark "TT-02" — about 22:30 alongside, est. Rapeseed meal 31,500 MT to load.'}) + B.s[b:]
a = B.s.index("const TUNA={"); e1 = B.s.index(" eta:[\n", a); e2 = B.s.index("\n ]};", e1)
rows = [r.rstrip(',') for r in B.s[e1 + len(" eta:[\n"):e2].split('\n')]
rows2 = []
for r in rows:
    if r.startswith("  {n:'Woohyun Dream',"): continue
    if r.startswith("  {n:'MP Postpanamax 1',"):
        assert r.count("eta:'11-24 00:00'") == 1; r = r.replace("eta:'11-24 00:00'", "eta:'11-22 17:30'"); i = r.index("rem:'") + 5; r = r[:i] + q("revised list 20.11: ETA / readiness 22 Nov 17:30 (24 Nov before)") + r[i:]
    rows2.append(r)
assert len(rows2) == len(rows) - 1
B.s = B.s[:e1] + " eta:[\n" + ",\n".join(rows2) + B.s[e2:]
B.rep("next:'nobody named — MP Postpanamax 1 (coal 88,000 MT) is expected on 24 Nov'", "next:'nobody named — MP Postpanamax 1 (coal 88,000 MT) is expected on 22 Nov 17:30'")
B.rep("const TUNA={src:'DPA berthing list 20.11.26 (0700) · DPR 20.11 · programme 20.11 (TT-03: Beagle out, Marvelous Star in) · TT-2 and TT-4 vacant'",
      "const TUNA={src:'DPA berthing list 20.11.26 (revised after the meeting) · DPR 20.11 · programme 21.11 (TT-02: Woohyun Dream in, night berthing) · TT-4 vacant'")
B.save()
