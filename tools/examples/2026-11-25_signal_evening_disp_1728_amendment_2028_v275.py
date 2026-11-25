#!/usr/bin/env python3
# apply71 — v275: two HM signal sheets dated 25/11/2026, both signed Capt Omesh, received 25 Nov 23:39 as images with no text.
#  EVENING SHEET (dispatched 17:28), 13 rows:
#   Omesh  : 20:30 IN SCI Chennai OTB → 98–110 "FLOOD" (container)
#   Verma  : (1) 21:15 IN LPG/C Green Bhavishya OTB → OJ-1 "FLOOD" · (2) 23:45 OUT Parvraj 40¾–49 · (3) 01:36 OUT Lila Tokyo 126–143½
#   Deepak : (1) 22:00 SHIFT LPG/C Bogazici OJ-1 → OTB · (2) o/c IN Tanjong Pagar OTB → 88–95½ "FLOOD" (container) · (3) o/c OUT Sriwangi V OJ-7 · (4) o/c IN Tug Varahi + barge AKG 11 OTB → 128–134¾
#   Yadav  : 21:30 TURN AROUND African Hornbill 173½–188 "Agent A/C" · 00:00 OUT DP World Godavari 87–97½ · o/c IN Peonia OTB → OJ-7 "FLOOD"
#   Sachin : 23:00 OUT Hafnia Ammolite OJ-3 · o/c IN Lumis OTB → OJ-3 · PMS / stand-by: one hour each on completion
#  AMENDMENT (dispatched 20:28), 2 rows — Capt Bali: 08:00 RT OUT Lila Tokyo 126–143½ → OTB · o/c IN Tug Varahi + barge AKG 11 OTB → 128–134¾
#  So Lila Tokyo does not sail at night: 08:00 on 26 Nov, and the tug and barge come in behind her — alongside about noon, est.
# Conventions: an IN hour is the pilot boarding, alongside about 2 h later; "o/c" = about 2 h behind that pilot's previous move. All est.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='HM SIGNAL 25 Nov evening'); q = B.q
SG = 'HM SIGNAL 25 Nov evening sheet (disp 17:28)'; SA = 'HM SIGNAL 25 Nov amendment (disp 20:28)'
STAMP = sys.argv[1]
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def pre(m, t): B.note_prefix(m, q(t) + " ")
B.rep("const NOW=h('11-25 16:11');", "const NOW=h('11-25 23:39');")
B.rep("<i>Signals to</i><b>24 Nov evening sheet (disp 1655, amended to 1920)</b>", "<i>Signals to</i><b>25 Nov evening sheet (disp 1728, amended 2028)</b>")
B.rep("HM signal sheets to the evening sheet of 24 Nov (disp 16:55, amended to 19:20) ·", "HM signal sheets to the evening sheet of 25 Nov (disp 17:28, amended 20:28) ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 25 Nov evening sheet (disp 1728) + amendment (disp 2028) · ")

# ---- cargo berths
M = "{b:'6',n:'Parvraj',nm:14950,p:[40.75,49]"
pre(M, SG + ": OUT 23:45 · Capt Verma · 40¾–49 → OTB — the programme's hour, now with a pilot. Nobody is signalled into CJ-6.")
M = "{b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]"
pre(M, SA + ": RT OUT 08:00 ON 26 NOV · Capt Bali · 126–143½ → OTB — NOT the night sailing: the evening sheet (17:28) had her at 01:36 with Capt Verma, the programme's hour; three hours later the amendment moves her to the morning. The tug and barge follow her in with the same pilot.")
B.sub_entry(M, "t:'11-26 01:36'", "t:'11-26 08:00',lt:'11-26 01:36'")
M = "{b:'14',n:'Tug Varahi + barge AKG 11',p:[128,134.75]"
pre(M, SA + ": IN \"o/c\" · Capt Bali, straight behind Lila Tokyo's 08:00 · OTB → 128–134¾ — alongside about 12:00 on 26 Nov, est (the evening sheet had her behind the 01:36 sailing, Capt Deepak; the board had 03:30). 4,000 MT of coated pipes → about 28 Nov 02:25, est. The Coastal place stays hers till then.".replace('\\"', '"'))
B.sub_entry(M, "f:'11-26 03:30',t:'11-27 17:55',est:1", "f:'11-26 12:00',t:'11-28 02:25',est:1")
M = "{b:'16',n:'African Hornbill (blades, next call)',p:[173.5,188]"
pre(M, SG + ": TURN AROUND 21:30 · Capt Yadav · 173½–188 → 173½–188 · \"Agent A/C\" — an hour after the programme's 20:30. The shift to CJ-15A is not on these sheets (it waits for Ocean Kudos, 26 Nov).".replace('\\"', '"'))

# ---- oil jetties
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
PREVKEYS = ('n', 'c', 'q', 'u', 'ie', 'ag', 'out', 'outBy')
def bline(bid):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]; tail = ',' if ln.endswith(',') else ''
    core = ln[:-1] if tail else ln; d = dict(split_top(core[3:-1]))
    if set(d) - {'b', 'prev', 'now'}: B.die('berth extra keys: ' + bid + str(list(d)))
    return a, b, d, tail
def bput(a, b, d, tail): B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in ('b', 'prev', 'now')) + '}' + tail + B.s[b:]
def berth(bid, nown, add, f=None, nm=None, etc=None, qty=None, est=None, out=None, outBy=None):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    if f is not None: now['f'] = js(f)
    if est is False: now.pop('est', None)
    if nm is not None: now['nm'] = js(nm)
    if etc is not None: now['etc'] = js(etc)
    if qty is not None: now['q'] = repr(qty)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS)
    if out is not None:
        pv = obj(d['prev']); pv['out'] = js(out); pv['outBy'] = "'" + q(outBy + ' · ') + pv['outBy'][1:]; d['prev'] = unobj(pv, PREVKEYS)
    bput(a, b, d, tail)

berth('OJ-1', 'Bogazici', SG + ': SHIFT 22:00 · Capt Deepak · OJ-1 → OTB (programme: 20:00) → LPG/C GREEN BHAVISHYA IN 21:15 · Capt Verma · "FLOOD" — alongside about 23:15, est', etc='11-25 22:00')
berth('OJ-3', 'Hafnia Ammolite', SG + ': OUT 23:00 · Capt Sachin · OJ-3 → OTB — the programme\'s hour → LUMIS IN "o/c" with the same pilot — alongside about 03:00 on 26 Nov, est', etc='11-25 23:00')
berth('OJ-7', 'Sriwangi V', SG + ': OUT "o/c" · Capt Deepak, his third move, after the 22:00 shift at OJ-1 and Tanjong Pagar in — about 02:00 on 26 Nov, est (programme readiness 18:35) → PEONIA IN "o/c" · Capt Yadav · "FLOOD" — alongside about 04:00, est', etc='11-26 02:00')
def rem(name, text):
    a, b = B.line_of("  {n:'%s'," % name); i = B.s.index("rem:'", a) + 5; assert i < b; B.s = B.s[:i] + q(text + ' · ') + B.s[i:]
rem('Green Bhavishya (LPG/C)', SG + ': IN 21:15 · Capt Verma · OTB → OJ-1 · "FLOOD" — behind Bogazici, who shifts out at 22:00 → alongside about 23:15 on 25 Nov, est')
rem('Lumis', SG + ': IN "o/c" · Capt Sachin, behind his 23:00 sailing of Hafnia Ammolite · OTB → OJ-3 → alongside about 03:00 on 26 Nov, est')
rem('Peonia', SG + ': IN "o/c" · Capt Yadav, after his 00:00 sailing of DP World Godavari · OTB → OJ-7 · "FLOOD" → alongside about 04:00 on 26 Nov, est (Sriwangi V leaves about 02:00)')
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-25 16:11',",
    lambda m: "const LIQ={prog:'" + q("HM SIGNAL 25 Nov evening (disp 17:28) — OJ-1 LPG/C Bogazici SHIFTS OUT 22:00 → LPG/C Green Bhavishya in, about 23:15 est · OJ-3 Hafnia Ammolite OUT 23:00 → Lumis in, about 03:00 on 26 Nov est · OJ-7 Sriwangi V OUT about 02:00 on 26 Nov est → Peonia in, about 04:00 est · ") + m.group(1)
    + "',src:'DPA berthing list 25.11.26 as revised after the meeting · DPR 25.11 · programme 26.11 · signals to the evening sheet of 25 Nov (disp 1728, amended 2028)',asOf:'11-25 23:39',", B.s, count=1)
if k != 1: B.die('LIQ head not found')

MVA = ['HM signal 25 Nov — amendment (dispatched 20:28) · Capt Omesh · received 25 Nov 23:39', [
 ['08:00', 'OUT', 'Lila Tokyo', 'CJ-14 · 126–143½ → OTB', 'Bali', '11-26 08:00', 'RT OUT on 26 Nov · replaces the 01:36 night sailing of the evening sheet'],
 ['o/c', 'IN', 'Tug Varahi + barge AKG 11', 'OTB → CJ-14 · 128–134¾', 'Bali', '11-26 12:00', 'behind Lila Tokyo — est · CSTL']]]
MVN = ['HM signal 25 Nov — evening sheet (dispatched 17:28) · Capt Omesh · received 25 Nov 23:39 · cargo berths', [
 ['20:30', 'IN', 'SCI Chennai', 'OTB → CJ-12 · 98–110', 'Omesh', '11-25 22:30', 'FLOOD · container · pilot boards 20:30 · alongside about 22:30, est'],
 ['21:30', 'TURN', 'African Hornbill', 'CJ-16 · 173½–188 → 173½–188', 'Yadav', '11-25 21:30', 'turn around · "Agent A/C" · programme had 20:30'],
 ['23:45', 'OUT', 'Parvraj', 'CJ-6 · 40¾–49 → OTB', 'Verma', '11-25 23:45', 'as the programme · nobody signalled in behind her'],
 ['00:00', 'OUT', 'DP World Godavari', 'CJ-11 · 87–97½ → OTB', 'Yadav', '11-26 00:00', 'container'],
 ['o/c', 'IN', 'Tanjong Pagar', 'OTB → CJ-11 · 88–95½', 'Deepak', '11-26 02:00', 'FLOOD · container · behind DP World Godavari — est'],
 ['01:36', 'OUT', 'Lila Tokyo', 'CJ-14 · 126–143½ → OTB', 'Verma', '11-26 08:00', 'SUPERSEDED by the 20:28 amendment: 08:00 on 26 Nov, Capt Bali'],
 ['o/c', 'IN', 'Tug Varahi + barge AKG 11', 'OTB → CJ-14 · 128–134¾', 'Deepak', '11-26 12:00', 'SUPERSEDED by the 20:28 amendment: behind the 08:00 sailing, Capt Bali — about noon, est'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Verma, Capt Yadav, Capt Deepak, Capt Sachin — one hour each on completion', '—', '11-26 05:00', '']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVA) + ",\n " + js(MVN) + ",\n")
LQN = ['HM signal 25 Nov — evening sheet (dispatched 17:28) · Capt Omesh · oil-jetty rows', [
 ['21:15', 'IN', 'Green Bhavishya (LPG/C)', 'OTB → OJ-1', 'Verma', '11-25 23:15', 'FLOOD · behind Bogazici — est'],
 ['22:00', 'SHIFT', 'Bogazici (LPG/C)', 'OJ-1 → OTB', 'Deepak', '11-25 22:00', 'programme had 20:00'],
 ['23:00', 'OUT', 'Hafnia Ammolite', 'OJ-3 → OTB', 'Sachin', '11-25 23:00', 'as the programme'],
 ['o/c', 'IN', 'Lumis', 'OTB → OJ-3', 'Sachin', '11-26 03:00', 'behind Hafnia Ammolite — est'],
 ['o/c', 'OUT', 'Sriwangi V', 'OJ-7 → OTB', 'Deepak', '11-26 02:00', 'his third move — est · programme readiness 18:35'],
 ['o/c', 'IN', 'Peonia', 'OTB → OJ-7', 'Yadav', '11-26 04:00', 'FLOOD · behind Sriwangi V — est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n")
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='" + STAMP + "';", B.s, count=1)
B.save(); print('saved 71')
