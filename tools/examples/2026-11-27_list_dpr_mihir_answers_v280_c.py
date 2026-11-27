#!/usr/bin/env python3
# apply76c — v280 part 3: oil jetties, Tuna, timber notes — list 27.11, DPR 27.11. Helpers and the wait/eta rebuild are taken from apply74c.py.
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 27.11'); q = B.q
L = 'LIST 27.11'; D = 'DPR 27.11'; SG = 'HM SIGNAL 26 Nov evening sheet'
src = open('/home/claude/work/apply74c.py', encoding='utf-8').read()
h0 = src.index("def js(o):"); h1 = src.index("# ---- the wait / eta blocks")
exec(src[h0:h1])
def setnow(bid, nown, add, **kw):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    for k, v in kw.items():
        if k == 'est':
            if v: now['est'] = '1'
            else: now.pop('est', None)
        elif k == 'q': now['q'] = repr(v)
        else: now[k] = js(v)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS); bput(a, b, d, tail)
def setprev(bid, name, out, add):
    a, b, d, tail = bline(bid); pv = obj(d['prev']); assert name in pv['n'], (name, pv['n'])
    pv['out'] = js(out); pv['outBy'] = "'" + q(add + ' · ') + pv['outBy'][1:]; d['prev'] = unobj(pv, PREVKEYS); bput(a, b, d, tail)

setprev('OJ-1', 'Green Bhavishya', '11-26 23:15', D + ': COMPLETED 19:30, LEFT THE BERTH 23:15 on 26 Nov — 14,000 MT')
setnow('OJ-1', 'Lumis', D + ' + ' + L + ': work stopped at OJ-3 21:06, left 23:40; RE-MADE FAST AT OJ-1 00:30, resumed 02:00 on 27 Nov · 9,220 MT off by 07:00 · list: norm 450, ETC 29 NOV 15:24 (28 Nov 08:47 before), 30,605.68 MT', f='11-27 00:30', est=False, nm='450', etc='11-29 15:24')
setprev('OJ-2', 'Thetis Leona', '11-26 14:20', D + ': COMPLETED 11:00, LEFT THE BERTH 14:20 on 26 Nov — 5,000 MT')
setnow('OJ-2', 'MC Hera', D + ' + ' + L + ': MADE FAST 15:36, COMMENCED 18:06 on 26 Nov · norm 475 · 13,860 MT off by 07:00, 6,740 left → about 27 Nov 18:40 at this rate · no ETC printed', f='11-26 15:36', est=False)
setprev('OJ-3', 'Lumis', '11-26 23:40', D + ': work stopped 21:06, left OJ-3 23:40 for OJ-1')
setnow('OJ-3', 'Ginga Merlin', D + ' + ' + L + ': MADE FAST 02:42, COMMENCED 05:30 on 27 Nov · norm 360 · 6,000 MT · ETC 27 NOV 23:22', f='11-27 02:42', est=False, nm='360', etc='11-27 23:22')
turn('OJ-4', 'Ocean Star', '11-27 09:15', D + ': made fast 12:06, commenced 14:48 on 26 Nov; COMPLETED 04:48 on 27 Nov — 5,203 MT · ' + SG + ': RT OUT 09:15 · Capt Yadav — taken as sailed 09:15 · ' + L + ': in brackets at [4] — outgoing',
     'Chemroad Quest', '11-27 11:15', True, L + ': at OJ-4, "B\'TODAY" — behind Ocean Star (out 09:15) → alongside about 11:15 on 27 Nov, est; not on a signal in hand')
setnow('OJ-5', 'Volga', L + ': printed at OJ-5, "B\'TODAY" — the list confirms the berth is back in use (the DPR of the same morning still carries "under maintenance from 16.11")')
setnow('OJ-6', 'Culture', D + ': 15,667 MT loaded in 24 h — 29,500 on board, 2,000 left (24,000 on the list) · ' + L + ': in brackets at [6] — outgoing — and OJ-6 printed VACANT, nobody named for it', q=31500)
setnow('OJ-7', 'Peonia', D + ': 19,054 MT off by 07:00, 7,947 left → about 27 Nov 17:00 at this rate; list ETC 28 Nov 03:20')

r0 = src.index("LJ = json.load("); r1 = src.index("print('tankers no longer on either sheet")
chunk = src[r0:r1]
chunk = chunk.replace("/home/claude/work/in26/l26r.json", "/home/claude/work/in27/l27.json")
chunk = chunk.replace("peg = dict(peg); peg['rem'] = \"''\"; peg['q'] = '600'; have['CHEMROUTEPEGASUS'] = peg\n", "")
chunk = chunk.replace("if k in ('OCEANSTAR', 'MCHERA'): continue", "if k in ('CHEMROADQUEST', 'GINGAMERLIN', 'VOLGA'): continue")
chunk = chunk.replace("elif k == 'CHEMROUTEPEGASUS': bits.append('BACK ON THE WAITING SHEET — shifted out of OJ-2 on 25 Nov 16:45 with 600 MT still on board')\n", "elif False: pass\n")
chunk = chunk.replace("DISP = {", "DISP = {'AHINOS': 'Ahinos', ")
assert "l27.json" in chunk and "CHEMROADQUEST" in chunk
exec(chunk)
print('\n'.join(chg)); print('dropped:', [have[k]['n'] for k in have if k not in used])
B.s = B.s[:w0 + 8] + ",\n".join(WAIT) + B.s[e0:]
e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
B.s = B.s[:e0 + len("\n ],\n eta:[\n")] + ",\n".join(ETAS) + B.s[m0:]
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-26 23:10',",
    lambda m: "const LIQ={prog:'" + q("LIST 27.11 + DPR 27.11 — OJ-1 Lumis re-made fast 00:30 (from OJ-3), ETC 29 Nov 15:24 · OJ-2 MC Hera made fast 15:36 on 26 Nov · OJ-3 Ginga Merlin made fast 02:42, ETC 27 Nov 23:22 · OJ-4 Ocean Star completed 04:48, out 09:15 → Chemroad Quest \"B'TODAY\" · OJ-5 Volga \"B'TODAY\" · OJ-6 Culture outgoing, berth printed vacant · ") + m.group(1)
    + "',src:'DPA berthing list 27.11.26 (0700) · DPR 27.11 · programme 27.11 · signals to the evening sheet of 26 Nov (disp 1810, extended 2100)',asOf:'11-27 10:20',", B.s, count=1)
if k != 1: B.die('LIQ head')
LQD = ['DPR 27.11 and list 27.11 — actual hours at the oil jetties, 26 / 27 Nov', [
 ['09:40', 'OUT', 'Chemroad Nexus', 'OJ-4 → OTB', '—', '11-26 09:40', 'sailing block of the DPR'],
 ['12:06', 'IN', 'Ocean Star', 'OTB → OJ-4', '—', '11-26 12:06', 'made fast 12:06, commenced 14:48; completed 04:48 on 27 Nov'],
 ['14:20', 'OUT', 'Thetis Leona', 'OJ-2 → OTB', '—', '11-26 14:20', 'completed 11:00, left the berth 14:20'],
 ['15:36', 'IN', 'MC Hera', 'OTB → OJ-2', '—', '11-26 15:36', 'made fast 15:36, commenced 18:06 — board had ~17:00'],
 ['23:15', 'OUT', 'Green Bhavishya (LPG/C)', 'OJ-1 → OTB', '—', '11-26 23:15', 'completed 19:30, left the berth 23:15'],
 ['23:40', 'SHIFT', 'Lumis', 'OJ-3 → OJ-1', '—', '11-27 00:30', 'left OJ-3 23:40, re-made fast 00:30, resumed 02:00'],
 ['02:42', 'IN', 'Ginga Merlin', 'OTB → OJ-3', '—', '11-27 02:42', 'made fast 02:42, commenced 05:30 — board had ~03:00']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQD) + ",\n")

# ================= TUNA =================
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda m: "const TUNA={src:'" + q("DPA berthing list 27.11.26 · DPR 27.11 · TT-1 Blue Ionian and TT-3 MP Postpanamax 1 working · TT-2 and TT-4 vacant") + "',", B.s, count=1)
if k != 1: B.die('TUNA head')
def tnote_tt(bid, text):
    a, b = B.line_of("  {b:'%s',n:" % bid); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(text + ' ') + B.s[i:]
tnote_tt('TT-3', D + ': 25,400 MT in 24 h — 75,500 off, 12,500 left → about 27 Nov 18:50 at this rate.')
tnote_tt('TT-1', D + ': 13,455 MT in 24 h — 51,655 off, 21,700 left → about 28 Nov 21:40 at this rate.')

# ================= TIMBER =================
def tnote(name, text, tag=L):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('AG Varvara', "30,885 pcs / 4,200 CBM in 24 h on 12 hooks — 8,264 CBM off, 30,848 left → about 4 Dec 15:15 at this rate; list ETC 5 Dec 08:52", tag=D)
tnote('CD Glory', "SGR 1 · 8K 5 · GEN 10 — unchanged · the SAAGAR place she waits for: Asian Summit, shifted to CJ-5; 13,600 MT in the day of the shift, 16,899 left at 07:00 on 27 Nov → about 28 Nov 12:50 at that rate; list ETC 28 Nov 22:59")
tnote('Paiwan Ace', "SGR 4 · 8K 8 · GEN 18 (printed \"Paiwan Ice\")")
tnote('Dariya Priya', "SGR 2 · 8K 6 · GEN 12 · " + D + ": 1,216 CBM at midstream + 1,288 CBM landed at the barge area in 24 h — 9,435 CBM off, 35,533 left")
tnote('African Pheasant', "SGR 5 · 8K 9 · GEN 19")
B.save(); print('saved 76c')
