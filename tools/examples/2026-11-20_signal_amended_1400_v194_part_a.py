#!/usr/bin/env python3
# apply39a — v194 (part 1, data): HM SIGNAL SHEET of 20 Nov, "Amendment Signal", dispatched 12:40 / 13:25 / 14:00 (Capt Pathak) — image sent by Mihir at 20:11, no text.
# It supersedes the 12:40 dispatch applied in v189. What is new: Propel Confidence is "(RT) SHIFT" to OTB on agent's account (was RT OUT); SAFI ALFA's inward row and
# Konrad's outward row are NO LONGER on the sheet; Meghna Prestige goes out "o/c" under Capt Omesh after Rome Trader (00:30) and Uni Blossom; Parvraj's berth is written
# (43–51¼); Heng Yuan Fa Zhan's turn-round is 23:15; Jag Pushpa out 14:45; Eva Richway in 20:45; Bow Endeavour out 22:00; Arrabbiata shift 02:00.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; B = Board(W + 'dpa-berth-board.html'); q = B.q
SG = "HM SIGNAL 20 Nov (amended sheet, disp 14:00)"
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def pre(marker, text): B.note_prefix(marker, q(text) + " ")
def sub(marker, old, new): B.sub_entry(marker, old, new)

B.rep("const NOW=h('11-20 17:13');", "const NOW=h('11-20 20:11');")
B.rep("Signals to <b>20 Nov afternoon sheet (disp 1240)</b>", "Signals to <b>20 Nov evening sheet, amended (disp 1240 / 1325 / 1400)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 20 Nov 20:11: the HM signal sheet of 20 Nov as AMENDED (dispatched 12:40 / 13:25 / 14:00) — Safi Alfa's inward row to CJ-4 is no longer on it; Propel Confidence is shifted to OTB on her agent's account; Meghna Prestige goes out only after Uni Blossom is in (early on the 21st); Parvraj into 43–51¼ · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 20 Nov amended (disp 1400) · ")

# ---------------- V ----------------
M = "{b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75]"
pre(M, SG + ": the row now reads \"(RT) SHIFT\" at 17:00, 23½–31¾ → OTB, marked AGENT'S ACCOUNT · Capt Sud + Dixit — she is moved off the berth to the anchorage on her agent's account, not sailed; her cargo was done (DPR 20.11: 5,818 MT left at 0700). And SAFI ALFA's inward row behind her is NO LONGER on the sheet — CJ-4 is empty from 17:00.")
a, b = B.line_of(" {b:'4',n:'Safi Alfa',nm:3000,p:[23,31.75],")
B.s = B.s[:a] + B.s[b + 1:]
row = open(W + 'safi_row.txt', encoding='utf-8').read()
i = row.index(",{GEN:1},'") + len(",{GEN:1},'")
row = row[:i] + q("HM SIGNAL 20 Nov (amended sheet, disp 12:40 / 13:25 / 14:00): her inward row — IN \"o/c\" at 23–31¾ on the 12:40 dispatch — is NOT on the amended sheet. Programme 21.11 has no CJ-04 row, and the list as revised after the meeting keeps her waiting at GEN 1. She is taken back to the waiting rows until a signal or a programme carries her again — TO CONFIRM WITH MIHIR. She is the senior-most vessel of the General line, and CJ-4 is empty from 17:00 (Propel Confidence shifted to OTB) · ") + row[i:]
a, b = B.line_of(" ['Fortunelit','Rice/sugar bags',")
B.s = B.s[:a] + row + "\n" + B.s[a:]
M = "{b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75]"
pre(M, SG + ": RT OUT \"o/c\" under Capt Omesh — after Rome Trader's 00:30 and Uni Blossom's berthing, so about 04:00 on 21 Nov (est), not 19:39 on the 20th as programme 21.11 printed.")
sub(M, "f:'11-19 07:30',t:'11-20 19:39'", "f:'11-19 07:30',t:'11-21 04:00',lt:'11-20 19:39',est:1")
M = "{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]"
pre(M, SG + ": TURN AROUND now 23:15 (16:00 on the earlier dispatch), 161¾–169, flood to ebb, agent's account · Capt Karan + Nikhil.")
M = "{b:'6',n:'Parvraj',nm:14950,p:[43,51.25]"
pre(M, SG + ": IN \"o/c\" → 43–51¼ — the berth is written now · Capt Karan + Nikhil, after Jeil Crystal's 19:00.")
M = "{b:'13',n:'Rome Trader (salt, next call)',nm:23000,p:[113,125.25]"
pre(M, "MIHIR & COMPANY · " + SG + ": RT OUT 00:30 · Capt Omesh · 113–125¼ → OTB, with Uni Blossom IN \"o/c\" behind her — as programmed.")
M = "{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]"
pre(M, SG + ": IN \"o/c\" · Capt Omesh · OTB → 113–124¾, after Rome Trader's 00:30.")

# ---------------- MV ----------------
MVN = ['HM signal 20 Nov — evening sheet, AMENDED (dispatched 12:40 / 13:25 / 14:00) · Capt Pathak · received 20 Nov 20:11', [
  ['14:45', 'OUT', 'Jag Pushpa', 'OJ-3 → OTB', 'Sandeep', '11-20 14:45', '15:30 on the 12:40 dispatch'],
  ['o/c', 'IN', 'SG Friendship', 'OTB → OJ-3', 'Sandeep', '11-20 17:00', 'est'],
  ['16:45', 'IN', 'Flexi-2', 'OTB → CJ-12 · 100–109½', 'Karan + Nikhil', '11-20 16:45', 'flood · 17:00 before · Konrad\'s outward row is no longer on the sheet'],
  ['17:00', 'SHIFT', 'Propel Confidence', 'CJ-4 · 23½–31¾ → OTB', 'Sud + Dixit', '11-20 17:00', '"(RT) SHIFT", agent\'s account — RT OUT on the 12:40 dispatch'],
  ['o/c', 'IN', 'Orchids', 'OTB → OJ-6', 'Sud + Dixit', '11-20 19:30', 'on arrival (ETA) · flood · est'],
  ['18:15', 'OUT', 'Truong Minh Dream', 'CJ-6 · 42½–51¼ → OTB', 'Verma', '11-20 18:15', ''],
  ['19:00', 'OUT', 'Jeil Crystal', 'OJ-2 → OTB', 'Karan + Nikhil', '11-20 19:00', 'RT OUT'],
  ['o/c', 'IN', 'Parvraj', 'OTB → CJ-6 · 43–51¼', 'Karan + Nikhil', '11-20 21:30', 'the berth is written now ("pending" at 12:40) · est'],
  ['o/c', 'IN', 'Hatnyanawati', 'OTB → OJ-2', 'Verma', '11-20 21:00', 'est'],
  ['20:45', 'IN', 'Eva Richway', 'OTB → OJ-4', 'Sud + Dixit', '11-20 23:00', 'behind Bow Endeavour · est'],
  ['22:00', 'OUT', 'Bow Endeavour', 'OJ-4 → OTB', 'Verma', '11-20 22:00', 'RT OUT · programme 21.11: 23:30'],
  ['23:15', '—', 'Heng Yuan Fa Zhan', 'CJ-15A · 161¾–169 · turned round at the berth', 'Karan + Nikhil', '11-20 23:15', 'TURN AROUND · flood to ebb · agent\'s account · 16:00 before'],
  ['00:30', 'OUT', 'Rome Trader', 'CJ-13 · 113–125¼ → OTB', 'Omesh', '11-21 00:30', 'RT OUT'],
  ['o/c', 'IN', 'Uni Blossom', 'OTB → CJ-13 · 113–124¾', 'Omesh', '11-21 02:30', 'est'],
  ['o/c', 'OUT', 'Meghna Prestige', 'CJ-7 · 52¼–58¾ → OTB', 'Omesh', '11-21 04:00', 'RT OUT, after Uni Blossom is in — programme 21.11 had 20 Nov 19:39 · est'],
  ['02:00', 'SHIFT', 'Arrabbiata', 'CJ-11 · 87–95 → OTB', 'Verma', '11-21 02:00', '"(RT) SHIFT" · programme 21.11: out 20 Nov 22:40'],
  ['—', '—', 'No longer on the sheet', 'Safi Alfa IN at 23–31¾ · Konrad OUT from 101–109 (both on the 12:40 dispatch, Capt G. Raj)', '—', '11-20 20:11', '']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")

# ---------------- MEETLOG 20 Nov: Safi Alfa's signal row was withdrawn ----------------
B.rep("  got:[['Parvraj','6'],['Flag Marina','7'],['Yuan Hang Wei Ye','9'],['Uni Blossom','13'],['Safi Alfa','4','signal']],",
      "  got:[['Parvraj','6'],['Flag Marina','7'],['Yuan Hang Wei Ye','9'],['Uni Blossom','13']],")
B.rep("Nobody was sent to CJ-3. Safi Alfa (GEN 1) came into CJ-4 by signal.'},", "Nobody was sent to CJ-3. Safi Alfa (GEN 1) was signalled into CJ-4 at 12:40, but the row is gone from the sheet as amended at 14:00 — not counted.'},")

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
def setf(txt, key, val):
    rx = re.compile(r"\b" + key + r":'[^']*'"); assert len(rx.findall(txt)) == 1, (key, txt[:90]); return rx.sub(key + ":'" + val + "'", txt)
def oj3(d):
    d['out'] = "'11-20 14:45'"
    d['outBy'] = js(SG + ': Jag Pushpa OUT 14:45 · Capt Sandeep (15:30 on the 12:40 dispatch) — SG Friendship IN "o/c" behind her')
    return d
berth('OJ-3', oj3)
def oj4(d):
    d['out'] = "'11-20 22:00'"
    d['outBy'] = js(SG + ': Bow Endeavour RT OUT 22:00 · Capt Verma — programme 21.11 had 23:30 · list ETC 21 Nov 00:10')
    assert "Eva Richway" in d['next']; d['next'] = setf(d['next'], 'f', '11-20 23:00')
    i = d['next'].index("note:'") + 6; d['next'] = d['next'][:i] + q(SG + ": IN 20:45 · Capt Sud + Dixit — about 23:00 alongside, behind Bow Endeavour (out 22:00), est · ") + d['next'][i:]
    return d
berth('OJ-4', oj4)
def oj6(d):
    assert "Orchids" in d['next']; d['next'] = setf(d['next'], 'f', '11-20 19:30')
    i = d['next'].index("note:'") + 6; d['next'] = d['next'][:i] + q(SG + ": IN \"o/c\" on arrival · Capt Sud + Dixit, after Propel Confidence's 17:00 shift — about 19:30, est · ") + d['next'][i:]
    return d
berth('OJ-6', oj6)
LMN = ['HM signal 20 Nov — evening sheet, AMENDED (dispatched 12:40 / 13:25 / 14:00)', [
  ['14:45', 'OUT', 'Jag Pushpa', 'OJ-3 → OTB', 'Sandeep', '11-20 14:45', ''],
  ['o/c', 'IN', 'SG Friendship', 'OTB → OJ-3', 'Sandeep', '11-20 17:00', 'est'],
  ['o/c', 'IN', 'Orchids', 'OTB → OJ-6', 'Sud + Dixit', '11-20 19:30', 'on arrival · flood · est'],
  ['19:00', 'OUT', 'Jeil Crystal', 'OJ-2 → OTB', 'Karan + Nikhil', '11-20 19:00', 'RT OUT'],
  ['o/c', 'IN', 'Hatnyanawati', 'OTB → OJ-2', 'Verma', '11-20 21:00', 'est'],
  ['20:45', 'IN', 'Eva Richway', 'OTB → OJ-4', 'Sud + Dixit', '11-20 23:00', 'est'],
  ['22:00', 'OUT', 'Bow Endeavour', 'OJ-4 → OTB', 'Verma', '11-20 22:00', 'RT OUT']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LMN) + ",\n" + B.s[mm:]
B.rep("signals to the afternoon sheet of 20 Nov (disp 1240)',asOf:'11-20 15:13',", "signals to the evening sheet of 20 Nov as amended (disp 1400)',asOf:'11-20 20:11',")
B.save()
