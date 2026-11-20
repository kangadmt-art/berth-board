#!/usr/bin/env python3
# apply34a — v189 (part 1, data): HM signal sheet of 20 Nov, day sheet, "amendment" (dispatched 10:25 / 10:35 / 10:55) — photo from Mihir, 20 Nov 12:46.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P, list_tag='HM SIGNAL 20 Nov'); q = B.q
SG = "HM SIGNAL 20 Nov (day sheet, amended)"
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

B.rep("const NOW=h('11-20 11:24');", "const NOW=h('11-20 12:46');")
B.rep("Signals to <b>19 Nov evening sheet (disp 1640, amended 1940)</b>", "Signals to <b>20 Nov day sheet (amended, disp 1025 / 1035 / 1055)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 20 Nov 12:46: HM signal sheet of 20 Nov, day sheet with amendments (dispatched 10:25 / 10:35 / 10:55) — Saga Viking shifted out at 11:00 and Ken Ann in behind her, Propel Confidence out 17:00, Katerina K's berthing struck out (\"cancelled by Traffic\"), Orchids into OJ-6 · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 20 Nov (day sheet, amended) · ")

# ---------------- V ----------------
M = "{b:'5',n:'Saga Viking',nm:3450,p:[32.75,41.5]"
pre(M, SG + ": SHIFT 11:00 · Capt Madaan · 32¾–41½ → OTB — six and a half hours ahead of programme 20.11 (17:30).")
sub(M, "t:'11-20 17:30',lt:'11-21 18:58'", "t:'11-20 11:00',lt:'11-21 18:58'")
M = "{b:'5',n:'Ken Ann',p:[33.5,41.5]"
pre(M, SG + ": IN \"o/c\" — on completion of Saga Viking's shift (11:00) · Capt Madaan · OTB → 33½–41½. About 13:00 alongside is the board's estimate; her 24 hours then end about 13:00 on 21 Nov, INSIDE the window of programme 21.11 (not the next one).")
sub(M, "f:'11-20 19:30',t:'11-21 19:30',est:1", "f:'11-20 13:00',t:'11-21 13:00',est:1")
M = "{b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75]"
pre(M, SG + ": RT OUT 17:00 (15:15 struck out) · Capt Sud + Udit · 23½–31¾ → OTB — programme 20.11 had 15:00.")
sub(M, "t:'11-20 15:00',lt:'11-20 11:47'", "t:'11-20 17:00',lt:'11-20 11:47'")
M = "{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]"
pre(M, "Her shift is not on the day signal of 20 Nov. CJ-4 frees only at 17:00 (Propel Confidence RT OUT), so the shift is moved to about 17:30 — est.")
sub(M, "t:'11-20 16:00',est:1", "t:'11-20 17:30',est:1")
M = "{b:'4',n:'ML Egret',nm:4600,p:[23,31.75]"
pre(M, "Not on the day signal of 20 Nov — Propel Confidence leaves CJ-4 at 17:00 (signal), so about 19:00 alongside is the board's estimate.")
sub(M, "f:'11-20 17:30',t:'11-28 07:30',est:1", "f:'11-20 19:00',t:'11-28 07:30',est:1")
M = "{b:'15',n:'Belmoira',nm:30000,p:[143.5,156.75]"
pre(M, "Not on the day signal of 20 Nov — she follows ML Egret's shift, which waits for CJ-4 (free 17:00): about 20:00, est.")
sub(M, "f:'11-20 18:30',t:'11-22 19:00',est:1", "f:'11-20 20:00',t:'11-22 20:30',est:1")
M = "{b:'6',n:'Truong Minh Dream',nm:17193,p:[42.5,51.25]"
pre(M, SG + ": OUT 17:45 · Capt Karan + Nirmal — as programmed. Katerina K's berthing behind her is STRUCK OUT (\"cancelled by Traffic\"): nobody is named for CJ-6.")
M = "{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]"
pre(M, SG + ": TURN AROUND 16:00 at 161¾–169, flood to ebb · Capt Karan — she is turned round at the berth, not leaving.")
# Katerina K — her berthing is cancelled: the berth entry goes, she returns to the waiting rows
a, b = B.line_of(" {b:'6',n:'Katerina K',p:[42.5,51.25],")
B.s = B.s[:a] + B.s[b + 1:]
m = B._row('Pioneer Fortune').search(B.s); e = B.s.index("],\n", m.start()) + 3
ROW = (" ['Katerina K','Kaolin / clay J-bags + soya bean meal',29636,'MT',199.99,6.61,'11-16 11:00',{GEN:8.5},'" + q(
  "HM SIGNAL 20 Nov (day sheet, amended): her berthing at CJ-6 — IN \"o/c\", 42½–51¼ — is STRUCK OUT with the remark \"cancelled by Traffic\". She is back in the waiting rows. List 20.11 had printed her starred (\"B'TODAY\", ranks X) between Pioneer Fortune (GEN 8) and MK Lamis (GEN 9): carried as GEN 8.5 until a list prints her rank again. Programme 20.11 had given her CJ-6 as a provisional berthing (GENERAL) behind Truong Minh Dream · list 20.11 quantity 27576.288/20600 · LIST 18.11: GEN 8 · LIST 16.11: READINESS DECLARED 16 Nov 11:00 · remark \"22150 (J BAGS) CJ 1 TO 8 , 13 TO 16\" · Reported 5 Nov 14:00 · agent Ambica") + "'],\n")
B.s = B.s[:e] + ROW + B.s[e:]

# ---------------- MV ----------------
MVN = ['HM signal 20 Nov — day sheet, amended (dispatched 10:25 / 10:35 / 10:55) · pilot launch 11:35 / 12:35', [
  ['11:00', 'SHIFT', 'Saga Viking', 'CJ-5 · 32¾–41½ → OTB', 'Madaan', '11-20 11:00', 'programme 20.11: 17:30'],
  ['o/c', 'IN', 'Ken Ann', 'OTB → CJ-5 · 33½–41½', 'Madaan', '11-20 13:00', 'on completion of Saga Viking — about 13:00, est · 24 HRS'],
  ['15:15', 'OUT', 'Konrad', 'CJ-12 · 101–109 → OTB', 'G. Raj', '11-20 15:15', 'RT OUT · container'],
  ['17:00', 'OUT', 'Propel Confidence', 'CJ-4 · 23½–31¾ → OTB', 'Sud + Udit', '11-20 17:00', 'RT OUT · 15:15 struck out, 17:00 written · programme: 15:00'],
  ['o/c', 'IN', 'Katerina K', 'OTB → CJ-6 · 42½–51¼', '—', '11-20 17:45', 'STRUCK OUT — "cancelled by Traffic"'],
  ['17:45', 'OUT', 'Truong Minh Dream', 'CJ-6 · 42½–51¼ → OTB', 'Karan + Nirmal', '11-20 17:45', 'as programmed'],
  ['o/c', 'IN', 'Flexi-2', 'OTB → CJ-12 · 100–109½', 'Karan', '11-20 18:00', 'container · flood · est'],
  ['16:00', '—', 'Heng Yuan Fa Zhan', 'CJ-15A · 161¾–169 · turned round at the berth', 'Karan', '11-20 16:00', 'TURN AROUND · flood to ebb']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")

# ---------------- LIQ ----------------
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
    out = []
    for p in parts:
        i = p.index(':'); out.append([p[:i], p[i + 1:]])
    return out
def berth(bid, fn):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]
    tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln
    if not (core.startswith('  {') and core.endswith('}')): B.die('berth line shape: ' + bid)
    d = split_top(core[3:-1]); keys = [k for k, _ in d]
    if set(keys) - {'b', 'prev', 'now', 'out', 'outBy', 'next'}: B.die('berth extra keys: ' + bid + ' ' + str(keys))
    d = fn(dict(d))
    order = [k for k in ('b', 'prev', 'now', 'out', 'outBy', 'next') if k in d]
    B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in order) + '}' + tail + B.s[b:]
def note_pre(raw, text):
    i = raw.index("note:'") + 6; return raw[:i] + q(text) + raw[i:]
def oj3(d):
    assert d['out'] == "'11-20 13:00'", d['out']
    d['out'] = "'11-20 15:30'"
    d['outBy'] = js('HM SIGNAL 20 Nov (day sheet, amended): Jag Pushpa RT OUT 15:30 · Capt Sandeep — programme 20.11 had 13:00')
    assert d['next'].count("f:'11-20 15:00',est:1") == 1
    d['next'] = note_pre(d['next'].replace("f:'11-20 15:00',est:1", "f:'11-20 17:00',est:1"), 'HM SIGNAL 20 Nov (day sheet, amended): IN 15:15 (the "o/c" struck out) · Capt Sud · OTB → OJ-3 — about 17:00 alongside, est · ')
    return d
def oj6(d):
    d['next'] = js({'n': 'Orchids', 'c': 'VLSFO', 'q': 8000, 'u': 'MT', 'ie': 'IMP', 'loa': 128.6, 'f': '11-20 17:30', 'est': 1, 'rank': '', 'ag': 'Atlantic Shg',
        'note': 'HM SIGNAL 20 Nov (day sheet, amended): ORCHIDS IN "o/c" at OJ-6 on arrival (ETA 16:00), on the flood · Capt Sandeep — about 17:30 alongside, est · list 20.11: OJ-6 "B\'TODAY", VLSFO 8,000 MT. The signal follows the list; programme 20.11 had put WILLOWS here, and she stays on the waiting sheet'})
    return d
berth('OJ-3', oj3); berth('OJ-6', oj6)
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
wait = [r.rstrip(',') for r in B.s[w0 + len(" wait:[\n"):e0].split('\n')]
eta = [r.rstrip(',') for r in B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n')]
def nm(r): return re.match(r"  \{n:'((?:[^'\\]|\\.)*)'", r).group(1)
def setf(r, key, val):
    rx = re.compile(key + r":'(?:[^'\\]|\\.)*'"); assert len(rx.findall(r)) == 1, (key, r[:80]); return rx.sub(lambda _: key + ":'" + q(val) + "'", r)
W2 = [setf(r, 'rem', 'rank "1O" · OJ-06 · programme 20.11 had her at OJ-6 behind Kestrel, but list 20.11 and the HM signal of 20 Nov give OJ-6 to Orchids — Willows waits') if nm(r) == 'Willows' else r for r in wait]
E2 = [r for r in eta if nm(r) != 'Orchids']
assert len(E2) == len(eta) - 1
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(W2) + "\n ],\n eta:[\n" + ",\n".join(E2) + B.s[m0:]
LMN = ['HM signal 20 Nov — day sheet, amended (dispatched 10:25 / 10:35 / 10:55)', [
  ['15:15', 'IN', 'SG Friendship', 'OTB → OJ-3', 'Sud', '11-20 15:15', '"o/c" struck out, 15:15 written — about 17:00 alongside, est'],
  ['15:30', 'OUT', 'Jag Pushpa', 'OJ-3 → OTB', 'Sandeep', '11-20 15:30', 'RT OUT · programme 20.11: 13:00'],
  ['o/c', 'IN', 'Orchids', 'OTB → OJ-6', 'Sandeep', '11-20 17:30', 'on arrival (ETA 16:00) · flood · est — programme 20.11 had Willows here']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LMN) + ",\n" + B.s[mm:]
B.rep("const LIQ={src:'DPA berthing list 20.11.26 (0700) · DPR 20.11 · programme 20.11 (TF/SH/2102) · signals to the evening sheet of 19 Nov',asOf:'11-20 10:36',",
      "const LIQ={src:'DPA berthing list 20.11.26 (0700) · DPR 20.11 · programme 20.11 (TF/SH/2102) · signals to the day sheet of 20 Nov (amended, disp 1055)',asOf:'11-20 12:46',")
B.save()
