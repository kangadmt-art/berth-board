#!/usr/bin/env python3
# apply85c — v289 part 3: oil jetties, Tuna, timber notes — list 28.11, DPR 28.11, HM signal 28 Nov day sheet.
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 28.11'); q = B.q
L = 'LIST 28.11'; D = 'DPR 28.11'; SG = 'HM SIGNAL 28 Nov day sheet (disp 10:45)'
src = open('/home/claude/work/apply74c.py', encoding='utf-8').read()
exec(src[src.index("def js(o):"):src.index("# ---- the wait / eta blocks")])
s76 = open('/home/claude/work/apply76c.py', encoding='utf-8').read()
exec(s76[s76.index("def setnow("):s76.index("setprev('OJ-1'")])
setnow('OJ-1', 'Lumis', D + ' + ' + L + ': 9,223 MT in 24 h — 18,443 off · list ETC 29 NOV 15:24')
setprev('OJ-2', 'MC Hera', '11-27 20:50', D + ': COMPLETED 16:42, LEFT THE BERTH 20:50 on 27 Nov — 20,600 MT')
setnow('OJ-2', 'Bow Saturn', D + ' + ' + L + ': MADE FAST 02:42, COMMENCED 05:42 on 28 Nov (the signal had IN 23:30) · norm 360 · ETC 29 NOV 05:28', f='11-28 02:42', est=False, nm='360', etc='11-29 05:28')
turn('OJ-3', 'Ginga Merlin', '11-28 03:05', D + ': COMPLETED 00:06, LEFT THE BERTH 03:05 on 28 Nov — 7,813 MT (signal: OUT 03:00)',
     'SC Draco', '11-28 06:00', False, D + ' + ' + L + ': MADE FAST 06:00 on 28 Nov, not commenced by 07:00 · norm 550 · ETC 30 NOV 00:47', nm='550', etc='11-30 00:47')
setnow('OJ-4', 'Chemroad Quest', D + ' + ' + L + ': MADE FAST 15:20, COMMENCED 17:40 on 27 Nov · norm 225 · 2,300 MT off by 07:00, 2,656 left · ETC 28 NOV 17:21', f='11-27 15:20', est=False, nm='225', etc='11-28 17:21')
setnow('OJ-5', 'Volga', D + ' + ' + L + ': MADE FAST 12:55, COMMENCED 16:15 on 27 Nov · norm 200 · 5,190 MT off by 07:00, 2,287 left · ETC 29 NOV 06:18', f='11-27 12:55', est=False, nm='200', etc='11-29 06:18')
setprev('OJ-6', 'Culture', '11-27 12:15', D + ': COMPLETED 09:10, LEFT THE BERTH 12:15 on 27 Nov — 31,542 MT')
setnow('OJ-6', 'Maria Glory', D + ' + ' + L + ': MADE FAST 02:30, COMMENCED 05:30 on 28 Nov (the signal had IN 23:30) · 850 MT off by 07:00 · no ETC printed', f='11-28 02:30', est=False)
turn('OJ-7', 'Peonia', '11-28 09:30', D + ': COMPLETED 05:00 on 28 Nov — 27,001 MT · ' + SG + ': OUT 09:30 · Capt Mittal · ' + L + ': in brackets at [7] — outgoing',
     'Camelia', '11-28 11:30', True, SG + ': IN "o/c" · Capt Mittal · OTB → OJ-7 · FLOOD, behind Peonia\'s 09:30 sailing → alongside about 11:30 on 28 Nov, est · ' + L + ': at OJ-7, "B\'TODAY", norm 525', nm='525')
r0 = src.index("LJ = json.load("); r1 = src.index("print('tankers no longer on either sheet")
chunk = src[r0:r1]
chunk = chunk.replace("/home/claude/work/in26/l26r.json", "/home/claude/work/in28/l28.json")
chunk = chunk.replace("DISP = {", "DISP = {'SANMARSANTOOR': 'Sanmar Santoor', ")
chunk = chunk.replace("DISP = {", "DISP = {'LOYALTYGALAXY': 'Loyalty Galaxy', ")
chunk = chunk.replace("DISP = {", "DISP = {'KATSUYAMA': 'Katsuyama', ")
chunk = chunk.replace("DISP = {", "DISP = {'EVABERGEN': 'Eva Bergen', ")
chunk = chunk.replace("peg = dict(peg); peg['rem'] = \"''\"; peg['q'] = '600'; have['CHEMROUTEPEGASUS'] = peg\n", "")
chunk = chunk.replace("if k in ('OCEANSTAR', 'MCHERA'): continue", "if k in ('CAMELIA', 'SCDRACO', 'BOWSATURN', 'MARIAGLORY', 'CHEMROADQUEST', 'VOLGA'): continue")
chunk = chunk.replace("elif k == 'CHEMROUTEPEGASUS': bits.append('BACK ON THE WAITING SHEET — shifted out of OJ-2 on 25 Nov 16:45 with 600 MT still on board')\n", "elif False: pass\n")
assert "l28.json" in chunk and "'CAMELIA'" in chunk
import builtins
_die = B.die; missing = []
try:
    exec(chunk)
except SystemExit:
    raise
print('\n'.join(chg)); print('dropped:', [have[k]['n'] for k in have if k not in used])
B.s = B.s[:w0 + 8] + ",\n".join(WAIT) + B.s[e0:]
e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
B.s = B.s[:e0 + len("\n ],\n eta:[\n")] + ",\n".join(ETAS) + B.s[m0:]
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-27 23:33',",
    lambda m: "const LIQ={prog:'" + q("LIST 28.11 + DPR 28.11 + SIGNAL 28 Nov — OJ-2 Bow Saturn made fast 02:42, ETC 29 Nov 05:28 · OJ-3 Ginga Merlin left 03:05 → SC DRACO made fast 06:00, ETC 30 Nov 00:47 · OJ-4 Chemroad Quest ETC 28 Nov 17:21 · OJ-5 Volga ETC 29 Nov 06:18 · OJ-6 Maria Glory made fast 02:30 · OJ-7 Peonia completed 05:00, OUT 09:30 → CAMELIA in, about 11:30 est · OJ-1 Lumis ETC 29 Nov 15:24 · ") + m.group(1)
    + "',src:'DPA berthing list 28.11.26 (0700) · DPR 28.11 · programme 28.11 · signals to the day sheet of 28 Nov (disp 1045)',asOf:'11-28 11:12',", B.s, count=1)
if k != 1: B.die('LIQ head')
LQD = ['DPR 28.11, list 28.11 and HM signal 28 Nov day sheet (disp 10:45) — actual hours at the oil jetties, 27 / 28 Nov', [
 ['12:15', 'OUT', 'Culture', 'OJ-6 → OTB', '—', '11-27 12:15', 'completed 09:10, left the berth 12:15'],
 ['12:55', 'IN', 'Volga', 'OTB → OJ-5', '—', '11-27 12:55', 'made fast 12:55, commenced 16:15'],
 ['15:20', 'IN', 'Chemroad Quest', 'OTB → OJ-4', '—', '11-27 15:20', 'made fast 15:20, commenced 17:40'],
 ['20:50', 'OUT', 'MC Hera', 'OJ-2 → OTB', '—', '11-27 20:50', 'completed 16:42, left the berth 20:50'],
 ['02:30', 'IN', 'Maria Glory', 'OTB → OJ-6', '—', '11-28 02:30', 'made fast 02:30, commenced 05:30 — signal had 23:30'],
 ['02:42', 'IN', 'Bow Saturn', 'OTB → OJ-2', '—', '11-28 02:42', 'made fast 02:42, commenced 05:42 — signal had 23:30'],
 ['03:05', 'OUT', 'Ginga Merlin', 'OJ-3 → OTB', '—', '11-28 03:05', 'completed 00:06, left the berth 03:05'],
 ['06:00', 'IN', 'SC Draco', 'OTB → OJ-3', '—', '11-28 06:00', 'made fast 06:00'],
 ['09:30', 'OUT', 'Peonia', 'OJ-7 → OTB', 'Mittal', '11-28 09:30', 'completed 05:00 · signal 28 Nov'],
 ['o/c', 'IN', 'Camelia', 'OTB → OJ-7', 'Mittal', '11-28 11:30', 'FLOOD · behind Peonia — est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQD) + ",\n")
# ================= TUNA =================
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda m: "const TUNA={src:'" + q("DPA berthing list 28.11.26 · DPR 28.11 · TT-3 MP Postpanamax 1 left 02:30 on 28 Nov → Sakizaya Star made fast 05:00 · TT-1 Blue Ionian working, 11,000 MT left · TT-2 and TT-4 vacant · waiting: RB Leah (for TT-3), Agia Fotini (for TT-2)") + "',", B.s, count=1)
if k != 1: B.die('TUNA head')
a, b = B.line_of("  {b:'TT-3',n:'MP Postpanamax 1'")
B.s = B.s[:a] + "  {b:'TT-3',n:'Sakizaya Star',c:'US coal in bulk',q:80010,u:'MT',ie:'IMP',loa:229,f:'11-28 05:00',ag:'Benline',prev:'" + q("MP Postpanamax 1 (coal 88,000 MT) — DPR 28.11: completed 19:00 on 27 Nov, left the berth 02:30 on 28 Nov") + "',next:'" + q("RB Leah (coal 78,263 MT) is marked \"TT-03\" on the waiting sheet") + "',note:'" + q(D + " + " + L + ": MADE FAST 05:00 on 28 Nov — not commenced by 07:00; 80,010 MT of US coal · reported / ready 23 Nov 03:42.") + "'}," + B.s[b:]
a, b = B.line_of("  {n:'Sakizaya Star',c:'US coal in bulk'")
B.s = B.s[:a] + "  {n:'Agia Fotini',c:'Lentils in bulk',q:16193,u:'MT',ie:'IMP',loa:184.75,dr:8.02,rep:'11-26 08:25',rdy:'11-26 08:25',ag:'Interocean',rem:'" + q(L + ": on the Tuna waiting sheet — reported / ready 26 Nov 08:25 · remark \"TT-02\" · lentils in bulk 16,193 MT · 184.75 m, 8.02 m (programme 28.11 had her going into TT-2 at night; TT-2 is still printed vacant at 07:00)") + "'}," + B.s[b:]
def tnote_tt(bid, text):
    a, b = B.line_of("  {b:'%s',n:" % bid); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(text + ' ') + B.s[i:]
tnote_tt('TT-1', D + ': 10,700 MT in 24 h — 62,355 off, 11,000 left → about 29 Nov 07:40 at this rate.')
B.wdel('Agia Fotini')
# ================= TIMBER =================
def tnote(name, text, tag=L):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('AG Varvara', "31,115 pcs / 4,231 CBM in 24 h on 12 hooks — 12,495 CBM off, 26,617 left → about 4 Dec 14:00 at this rate; list ETC 5 Dec 08:52", tag=D)
tnote('CD Glory', "SGR 1 · 8K 5 · GEN 11 · \"SR.NO 07\"")
tnote('Dariya Priya', "SGR 2 · 8K 6 · GEN 13 · working at midstream · " + D + ": 1,314 CBM at midstream + 2,108 CBM landed at the barge area in 24 h — 10,749 CBM off, 34,219 left")
tnote('African Tiger', "SGR 3 · 8K 7 · GEN 15")
tnote('Paiwan Ace', "SGR 4 · 8K 8 · GEN 19")
tnote('African Pheasant', "SGR 5 · 8K 9 · GEN 20")
tnote('Erna Oldendorff', "SGR 6 · GEN 21")
tnote('Paiwan Wisdom', "ON THE WAITING SHEET — reported / ready 28 Nov 01:54 · SGR 9 · 8K 12 · GEN 39 · \"SR.NO 07\"")
B.rep("{n:'Paiwan Wisdom',cbm:19320,from:'USA',lp:'Pascagoula',lpn:'last calls shown: Palm Beach, Pascagoula (USA), then Ponce (Puerto Rico) 13–17 Oct · public AIS port calls (Maritime Optima), read 27 Nov',c:'Pine logs',eta:'11-28',", "{n:'Paiwan Wisdom',cbm:19320,from:'USA',lp:'Pascagoula',lpn:'last calls shown: Palm Beach, Pascagoula (USA), then Ponce (Puerto Rico) 13–17 Oct · public AIS port calls (Maritime Optima), read 27 Nov',c:'Pine logs',eta:'11-28 01:54',")
B.save(); print('saved 85c')
