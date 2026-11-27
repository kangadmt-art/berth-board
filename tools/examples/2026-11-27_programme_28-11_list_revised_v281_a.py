#!/usr/bin/env python3
# apply77 — v281. Papers 27 Nov 13:58 (no text): PROGRAMME FOR 28.11.2026 (TF/SH/2102 dt 27 Nov) — the meeting of 27 Nov — and the list 27.11 REVISED after it.
# The programme gives NO berth at the dry-cargo jetties: only CJ-11 / CJ-12 containers, OJ-2 / 3 / 6 / 7 and TT-2 / TT-3.
# Call frozen from bak_v280 (board as at 27 Nov 10:20): Tug Marigold + barge → 3, Meghna Prestige → 14, Rex → 5, Pacific Apex → 16, Tai Keystone → 7. None given.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 27.11 (revised)'); q = B.q
L = 'LIST 27.11 (revised)'; P = 'PROGRAMME 28.11'
src = open('/home/claude/work/apply74c.py', encoding='utf-8').read()
exec(src[src.index("def js(o):"):src.index("# ---- the wait / eta blocks")])
def pre(m, t): B.note_prefix(m, q(t) + " ")
def setf(marker, **kw):
    i = B.s.index(marker); j = B.s.index(",note:'", i); head = B.s[i:j]
    for k, v in kw.items():
        pat = re.compile(r",%s:(?:'(?:[^'\\]|\\.)*'|\[[^\]]*\]|[\d.]+)" % k); new = ",%s:%s" % (k, js(v))
        head = pat.sub(lambda _: new, head, count=1) if pat.search(head) else head
    B.s = B.s[:i] + head + B.s[j:]
def setline(prefix, new): a, b = B.line_of(prefix); B.s = B.s[:a] + new + B.s[b:]
def setnow(bid, nown, add, **kw):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    for k, v in kw.items(): now[k] = repr(v) if k == 'q' else js(v)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS); bput(a, b, d, tail)
def rem(name, text):
    a, b = B.line_of("  {n:'%s'," % name); i = B.s.index("rem:'", a) + 5; assert i < b; B.s = B.s[:i] + q(text + ' · ') + B.s[i:]

B.rep("const NOW=h('11-27 10:20');", "const NOW=h('11-27 13:58');")
B.rep("const PROG_END=h('11-27 18:00'); // programme 27.11 (meeting of 26 Nov) covers till here", "const PROG_END=h('11-28 18:00'); // programme 28.11 (meeting of 27 Nov) covers till here")
B.rep("<i>List</i><b>27.11</b>", "<i>List</i><b>27.11 · revised after the meeting</b>")
B.rep("<i>Programme</i><b>27.11</b>", "<i>Programme</i><b>28.11</b>")
B.rep("berthing list 27.11 (07:00; no list came for 22.11 or 24.11) · programme 27.11 ·", "berthing list 27.11 as revised after the meeting (no list came for 22.11 or 24.11) · programme 28.11 ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 28.11 (TF/SH/2102 dt 27 Nov — no dry-cargo berthing) · list 27.11 as revised after the meeting · ")

# ---- MEETLOG
ML = ("{d:'11-27',at:'11-27 10:20',basis:'list 27.11 · programme 27.11 · DPR 27.11 · HM signals to the evening sheet of 26 Nov · Mihir 27 Nov 10:19',prog:'28.11',"
      "call:[['Tug Marigold + barge Alaacrity 666','3'],['Meghna Prestige','14'],['Rex','5'],['Pacific Apex','16'],['Tai Keystone','7']],got:[],note:'" + q(
      "THE PORT GAVE NO BERTH AT THE DRY-CARGO JETTIES. Programme 28.11 has only containers (CJ-11, CJ-12), tankers (OJ-2, 3, 6, 7) and Tuna (TT-2, TT-3). The board had called five. "
      "WHY: the programme carries no outward row for any cargo jetty — not even MSC Magali, whose list ETC is 28 Nov 17:18, inside the window. The port programmes a berth only when the vessel on it is DECLARED completing; the board had emptied berths on the DPR pace (DSM London, Asian Summit, Jumbo Kinetic) and on the list ETC (MSC Magali), and had made a shift of its own (Blue Shark out of CJ-14 for Meghna Prestige). "
      "Tug Marigold at CJ-3 was the board seating a Coastal vessel in a vacant berth; the port left CJ-3 empty — her list remark is \"13 TO 16\". "
      "LESSON, now the standing reading: within a meeting's window nothing is called unless the outgoing vessel's completion is declared (an outward row, or a list ETC well inside the window); the DPR pace says when a berth COULD come free, not when the port will give it.") + "'},")
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")

# ---- V
M = "{b:'7',n:'Jumbo Kinetic',p:[52,57]"
pre(M, L + ": STILL \"B'TODAY\" at CJ-7, 52–57, on the list revised after the meeting of 27 Nov — not yet alongside; taken as about 16:00 on 27 Nov, est. " + P + ": no row for CJ-7.")
setf(M, f='11-27 16:00', t='11-28 06:00')
for m_ in ("{b:'5',n:'Asian Summit',nm:16100,p:[30.5,39.25]", "{b:'16',n:'MSC Magali',nm:50000,p:[169.5,188]", "{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]", "{b:'15',n:'Xin Hai Tong 71',p:[143,156.25]"):
    pre(m_, P + ": NO OUTWARD ROW for her berth — the port has not programmed her out before 18:00 on 28 Nov; the berth is for the meeting of 28 Nov.")

# ---- W
def w(name, text, **k): B.wrow(name, q(text), **k)
w('Marina L', "READY NOW — commercial readiness 27 Nov 11:00 · no rank printed yet · \"LP: Karachi - Pakistan\"", rdy="11-27 11:00")
w('Star Unity', "RANKED — 24 HRS 1 · commercial readiness 27 Nov 11:00 · rice in bags 42,000 MT · remark \"1 TO 5\" · agent Excel Infra", rk="'24H':1", rdy="11-27 11:00")
w('KM Jakarta', "RANKED — HP 6 · SGR 7 · commercial readiness 27 Nov 11:00 · salt 60,000 MT · \"30K/25K/10K SR.NO 07 DD-13.30 M\" · agent True Blue", rk="HP:6,SAAGAR:7", rdy="11-27 11:00")
w('True Mariner', "printed at \"MRG 03\" under OTHERS, \"B'TODAY\" — and still GEN 16 on the waiting sheet")
w('Tug Marigold + barge Alaacrity 666', "CSTL 1 · GEN 15 · ready 27 Nov 11:00 · remark now \"694 PIPES 13 TO 16\" · " + P + ": not on it")
w('Shree Krishna IX', "at the Bunder basin (\"BB\"), \"B'TODAY\" — marked X on the waiting sheet")
w('Xin Bo', "STILL ON THE EXPECTED SHEET after the meeting of 27 Nov — ETA 27 Nov 03:00, the readiness column printing the same hour · HP Y · SGR Y · 8K Y, NO NUMBER in any line · \"30K/25K/10K SR.NO 07 DD-12.25M LP: Bin Qasim\". She is not declared on this list")
w('Bunun Miracle', "(ETA sheet) ETA 27 Nov 16:00 · HP Y · 24H Y · \"25K/8K SR.NO 07 DD-9.95M\"", rk="HP:98,'24H':98")
w('Paiwan Wisdom', "(ETA sheet) ETA 27 Nov 02:00 — still on the expected sheet · SGR Y · 8K Y")
w('Jiaxin', "(ETA sheet) ETA 27 Nov 23:30 (28 Nov before)")
w('New Joyful', "(ETA sheet) ETA 28 Nov 04:00 · SGR Y")
w('El Matador', "(ETA sheet) ETA 28 Nov 22:00 (29 Nov before)")
w('Agia Fotini', P + ": TT-02 · IN · night berthing — SHE GOES TO TUNA, not to the cargo jetties", tag=False) if False else w('Agia Fotini', "PROGRAMME 28.11: TT-02 · IN · night berthing — she goes to Tuna, not to the cargo jetties")
w('CD Glory', "MIHIR · SGR 1 · 8K 5 · GEN 10 — unchanged · PROGRAMME 28.11: no dry-cargo berth given to anyone; Asian Summit has no outward row")
w('Paiwan Ace', "MIHIR · SGR 4 · 8K 8 · GEN 18 — unchanged · PROGRAMME 28.11: no dry-cargo berth given")
m = B._row('Star Unity').search(B.s); e = B.s.index("],\n", m.start()) + 3
B.s = B.s[:e] + " ['Prince Khaled','Rice bags',7800,'MT',125.96,2.95,null,{},'" + q(L + " (ETA sheet): NEW · rice bags 7,800 MT EXP · ETA 28 Nov 09:00 · N/A · 125.96 m · agent DBC") + "'],\n" + B.s[e:]
a, b = B.line_of("const ETA={'Xin Bo':"); ln = B.s[a:b]
for k, v in (("'Jiaxin':'11-28 00:00'", "'Jiaxin':'11-27 23:30'"), ("'New Joyful':'11-28 05:00'", "'New Joyful':'11-28 04:00'"), ("'El Matador':'11-29 00:00'", "'El Matador':'11-28 22:00'"), ("'Tug Canara Jog + barge RMG 254':'11-28 11:00'", "'Tug Canara Jog + barge RMG 254':'11-29 00:00'"), ("'Paiwan Wisdom':'11-28 00:00'", "'Paiwan Wisdom':'11-27 02:00'"), ("'Hasoonlit':", "'Prince Khaled':'11-28 09:00','Hasoonlit':")):
    assert k in ln, k; ln = ln.replace(k, v)
B.s = B.s[:a] + ln + B.s[b:]
a, b = B.line_of("Object.assign(AG,{'Shree Krishna IX':'Indoglobal',")
B.s = B.s[:b] + "\nObject.assign(AG,{'Prince Khaled':'DBC','Star Unity':'Excel Infra'});IE['Prince Khaled']='EXP'; // list 27.11 (revised)" + B.s[b:]

# ---- LIQ / TUNA from the programme and the revised list
setnow('OJ-2', 'MC Hera', P + ': OUT readiness 27 NOV 22:30, 7.7 m, night sailing → MT BOW SATURN in, night berthing · ' + L + ': ETC 28 Nov 14:58', etc='11-27 22:30')
setnow('OJ-3', 'Ginga Merlin', P + ': OUT readiness 28 NOV 03:45, 6.2 m → MT SC DRACO in, night berthing · ' + L + ': quantity 7,812.6 MT (6,000 before), ETC 28 Nov 04:24', etc='11-28 03:45', q=7812.61)
setnow('OJ-7', 'Peonia', P + ': OUT readiness 28 NOV 07:30, 7.3 m → MT CAMELIA in, starboard', etc='11-28 07:30')
setnow('OJ-6', 'Culture', P + ': OJ-06 — no outward vessel printed (she is taken as gone) → MT MARIA GLORY IN, night, starboard')
rem('Bow Saturn', P + ': OJ-02 — IN behind MC Hera (out readiness 27 Nov 22:30) → about 00:30 on 28 Nov, est')
rem('SC Draco', P + ': OJ-03 — IN behind Ginga Merlin (out readiness 28 Nov 03:45) → about 05:45 on 28 Nov, est')
rem('Maria Glory', P + ': OJ-06 — IN, night, starboard; the berth is printed vacant')
rem('Camelia', P + ': OJ-07 — IN behind Peonia (out readiness 28 Nov 07:30) → about 09:30 on 28 Nov, est')
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-27 10:20',",
    lambda m: "const LIQ={prog:'" + q("PROGRAMME 28.11 — OJ-2 MC Hera out 27 Nov 22:30 → Bow Saturn · OJ-3 Ginga Merlin out 28 Nov 03:45 → SC Draco · OJ-6 → Maria Glory · OJ-7 Peonia out 28 Nov 07:30 → Camelia · ") + m.group(1)
    + "',src:'DPA berthing list 27.11.26 as revised after the meeting · DPR 27.11 · programme 28.11 · signals to the evening sheet of 26 Nov',asOf:'11-27 13:58',", B.s, count=1)
assert k == 1
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda m: "const TUNA={src:'" + q("DPA berthing list 27.11.26 (revised) · DPR 27.11 · PROGRAMME 28.11: TT-3 MP Postpanamax 1 out 28 Nov 02:30 → Sakizaya Star in (night) · TT-2 → Agia Fotini in (night; lentils in bulk) · TT-1 Blue Ionian working · TT-4 vacant") + "',", B.s, count=1)
assert k == 1
B.save(); print('saved 77')
