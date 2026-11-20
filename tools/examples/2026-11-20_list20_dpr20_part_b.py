#!/usr/bin/env python3
# apply32b — v187 (part 2): liquid rows from list 20.11 + DPR 20.11, gear, own-vessel option notes, snapshot, logs. argv[1] = UPDATED.
import re, sys, json, shutil
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'pre32b.html')
B = Board(P); q = B.q
S = json.load(open(W + 'S187a.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]

# ================= LIQ — berth lines =================
def split_top(body):
    """body = text between the outer braces of one berth line -> ordered list of (key, raw value)"""
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
    if keys[0] != 'b': B.die('berth keys: ' + bid + ' ' + str(keys))
    if set(keys) - {'b', 'prev', 'now', 'out', 'outBy', 'next'}: B.die('berth extra keys: ' + bid + ' ' + str(keys))
    d = fn(dict(d))
    order = [k for k in ('b', 'prev', 'now', 'out', 'outBy', 'next') if k in d]
    B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in order) + '}' + tail + B.s[b:]
def note_pre(raw, text):
    i = raw.index("note:'") + 6; return raw[:i] + q(text) + raw[i:]
def oj1(d):
    d['now'] = js({'n': 'Artigo', 'c': 'CPO', 'q': 24000, 'u': 'MT', 'ie': 'IMP', 'loa': 185, 'f': '11-19 20:06', 'nm': '450', 'rank': '1E', 'ag': 'GAC Shg', 'etc': '11-22 07:26',
        'note': 'DPR 20.11: MADE FAST 20:06, commenced 23:06 on 19 Nov — 3,611 MT off by 0700, 20,389 left · list 20.11: OJ-1 · norm 450 MT/h · ETC 22 Nov 07:26 · evening signal 19 Nov: IN 17:30'})
    d.pop('next', None); d.pop('out', None); d.pop('outBy', None); return d
def oj2(d):
    d['now'] = js({'n': 'Jeil Crystal', 'c': 'Chemicals / base oil', 'q': 6635.14, 'u': 'MT', 'ie': 'IMP', 'loa': 117.27, 'f': '11-19 12:00', 'nm': '225', 'rank': '1C', 'ag': 'Wilhelmsen', 'etc': '11-20 21:29',
        'note': 'DPR 20.11: MADE FAST 12:00, commenced 14:10 on 19 Nov — chemicals 6,100 MT off, 535 left; base oil 1,986 MT still to load · list 20.11: norm 225 MT/h (chemicals) and 250 (base oil) · ETC 20 Nov 21:29'})
    d.pop('next', None); return d
def oj3(d):
    d['now'] = note_pre(d['now'], 'DPR 20.11: 13,400 MT in 24 h — 40,100 off, 4,155 left → done about 14:30 on the 20th · list 20.11: "[3]" — sailing today · ')
    d['next'] = note_pre(d['next'], 'list 20.11: OJ-3 "B\'TODAY" · norm 650 MT/h · ')
    return d
def oj4(d):
    d['prev'] = js({'n': 'Avyaan', 'c': 'HSD', 'q': 35000, 'u': 'MT', 'ie': 'IMP', 'ag': 'Victory Shg', 'out': '11-19 14:20', 'outBy': 'DPR 20.11: completed 12:06, LET GO 14:20 on 19 Nov — 35,000 MT (signal: OUT 15:00)'})
    d['now'] = js({'n': 'Bow Endeavour', 'c': 'Chemicals', 'q': 13047.17, 'u': 'MT', 'ie': 'IMP', 'loa': 159.73, 'f': '11-19 16:42', 'nm': '475', 'rank': '', 'ag': 'GAC Shg', 'etc': '11-21 00:10',
        'note': 'DPR 20.11: MADE FAST 16:42, commenced 19:18 on 19 Nov — 5,385 MT off by 0700, 7,662 left · list 20.11: norm 475 MT/h · ETC 21 Nov 00:10'})
    d.pop('next', None); return d
def oj6(d):
    d['now'] = note_pre(d['now'], 'DPR 20.11: 15,415 MT loaded in 24 h — 23,000 on board, 1,000 left · list 20.11: "[6]" — sailing today · ')
    d['next'] = note_pre(d['next'], 'LIST 20.11 PRINTS MT ORCHIDS (VLSFO 8,000 MT, ETA 20 Nov 16:00) AS "B\'TODAY" AT OJ-6 and leaves Willows on the waiting sheet (rank "1O", OJ-06) — the list and programme 20.11 disagree; the programme is followed here until a signal sheet shows who berths · ')
    return d
def oj7(d):
    d['prev'] = js({'n': 'NV Sunshine (LPG/C)', 'c': 'Propane & butane', 'q': 24000, 'u': 'MT', 'ie': 'IMP', 'ag': 'Atlantic Shg', 'out': '11-20 02:35', 'outBy': 'DPR 20.11: completed 22:48 on 19 Nov, LET GO 02:35 on the 20th — 24,000 MT (programme / signal: 01:00)'})
    d['now'] = js({'n': 'Silver Gertrude', 'c': 'CDSBO', 'q': 22500, 'u': 'MT', 'ie': 'IMP', 'loa': 183.06, 'f': '11-20 05:00', 'est': 1, 'rank': '1E', 'ag': 'Interocean',
        'note': 'DPR 20.11: "UNDER BERTHING" at 0700 on 20 Nov — about 05:00 alongside is the board\'s estimate · list 20.11: OJ-7 "B\'TODAY", CDSBO 22,500 MT · programme 20.11: OJ-07 behind NV Sunshine, night, starboard'})
    for k in ('out', 'outBy', 'next'): d.pop(k, None)
    return d
for bid, fn in (('OJ-1', oj1), ('OJ-2', oj2), ('OJ-3', oj3), ('OJ-4', oj4), ('OJ-6', oj6), ('OJ-7', oj7)): berth(bid, fn)

# ================= LIQ — waiting and expected rows =================
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
wait = [r.rstrip(',') for r in B.s[w0 + len(" wait:[\n"):e0].split('\n')]
eta = [r.rstrip(',') for r in B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n')]
def nm(r): return re.match(r"  \{n:'((?:[^'\\]|\\.)*)'", r).group(1)
def setf(r, key, val):
    rx = re.compile(key + r":'(?:[^'\\]|\\.)*'"); assert len(rx.findall(r)) == 1, (key, r[:80]); return rx.sub(lambda _: key + ":'" + q(val) + "'", r)
W2 = []
for r in wait:
    n = nm(r)
    if n == 'Silver Gertrude': continue                      # under berthing at OJ-7
    if n == 'Willows': r = setf(r, 'rem', 'rank "1O" · OJ-06 · PROGRAMME 20.11: OJ-6 behind Kestrel (out 20 Nov 11:00) — but LIST 20.11 prints Orchids as B\'TODAY at OJ-6 and keeps Willows on the waiting sheet')
    if n == 'SG Friendship': r = setf(r, 'rem', 'rank "1C" · REQ OJ 2, 3, 4 · LIST 20.11: B\'TODAY — OJ-3 behind Jag Pushpa (programme 20.11: out 13:00)')
    if n == 'Eva Richway': r = setf(setf(r, 'rank', '1C'), 'rem', 'rank "1C" on list 20.11 (2C the day before)')
    if n == 'Bow Fortitude': r = setf(setf(r, 'rank', '2C'), 'rem', 'rank "2C" on list 20.11')
    W2.append(r)
assert len(W2) == len(wait) - 1
W2 += ["  " + js({'n': 'PVT Aurora', 'c': 'Chemicals', 'q': 5000, 'u': 'MT', 'ie': 'IMP', 'loa': 146.19, 'dr': 8.15, 'rep': '11-19 11:06', 'rdy': '11-19 11:06', 'rank': '3C', 'ag': 'Atlantic Shg', 'rem': 'reported / ready 19 Nov 11:06 · rank "3C" · REQ OJ 2, 3, 4', 'st': ''}),
       "  " + js({'n': 'Al Mahboobah', 'c': 'Benzene', 'q': 9336.42, 'u': 'MT', 'ie': 'EXP', 'loa': 145.53, 'dr': 6, 'rep': '11-19 21:00', 'rdy': '11-19 21:00', 'rank': '4C', 'ag': 'Atlantic Shg', 'rem': 'reported / ready 19 Nov 21:00 · rank "4C" · REQ OJ 2, 3, 4', 'st': ''})]
E2 = []
for r in eta:
    n = nm(r)
    if n in ('PVT Aurora', 'Al Mahboobah'): continue
    if n == 'Orchids':
        r = "  " + js({'n': 'Orchids', 'c': 'VLSFO', 'q': 8600, 'u': 'MT', 'ie': 'IMP', 'loa': 128.6, 'dr': None, 'eta': '11-20 16:00', 'rdy': None, 'ag': 'Atlantic Shg',
                       'rem': 'LIST 20.11: ETA / readiness 20 Nov 16:00 · printed "B\'TODAY" at OJ-6 (8,000 MT on the at-berth sheet, 8,600 on the ETA sheet) — programme 20.11 gave OJ-6 to Willows'})
    E2.append(r)
    if n == 'Rigel': E2.append("  " + js({'n': 'Seaconger', 'c': 'CPO', 'q': 29999.69, 'u': 'MT', 'ie': 'IMP', 'loa': 178, 'dr': 11, 'eta': '11-26 00:00', 'rdy': None, 'ag': 'James Mackintosh', 'rem': 'new on list 20.11'}))
assert len(E2) == len(eta) - 2 + 1
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(W2) + "\n ],\n eta:[\n" + ",\n".join(E2) + B.s[m0:]
B.rep("const LIQ={src:'DPA berthing list 19.11.26 (0700) · programme 20.11, 19.11 and 18.11 (TF/SH/2102) · signals to the day sheet of 19 Nov (disp 1040) · DPR 19.11 / 18.11 / 17.11',asOf:'11-19 19:51',",
      "const LIQ={src:'DPA berthing list 20.11.26 (0700) · DPR 20.11 · programme 20.11 (TF/SH/2102) · signals to the evening sheet of 19 Nov',asOf:'11-20 10:36',")
LMN = ['DPR 20.11 — actual hours at the oil jetties, 19 Nov and the night', [
  ['14:20', 'OUT', 'Avyaan', 'OJ-4 → OTB', '—', '11-19 14:20', 'completed 12:06, let go 14:20 (signal: 15:00)'],
  ['16:42', 'IN', 'Bow Endeavour', 'OTB → OJ-4', '—', '11-19 16:42', 'made fast 16:42, commenced 19:18'],
  ['20:06', 'IN', 'Artigo', 'OTB → OJ-1', '—', '11-19 20:06', 'made fast 20:06, commenced 23:06'],
  ['02:35', 'OUT', 'NV Sunshine (LPG/C)', 'OJ-7 → OTB', '—', '11-20 02:35', 'completed 22:48 on the 19th, let go 02:35 (programme: 01:00)'],
  ['—', 'IN', 'Silver Gertrude', 'OTB → OJ-7', '—', '11-20 05:00', '"under berthing" at 0700 — est']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LMN) + ",\n" + B.s[mm:]

# ================= GEAR =================
B.rep("const GEAR_NONE=['CD Glory',", "const GEAR_NONE=['North Gate','CD Glory',")

# ================= OPTS notes =================
def note_of(label, text):
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "SAAGAR group — one bulk and one break-bulk place. List 20.11: Uni Blossom (SGR 1), AG Varvara (3), Xin Hai Tong 71 (4 — project cargo), CD Glory (5), Dariya Priya (6), African Tiger (7), Flag Marina (8). Rome Trader's place frees in the night of 20–21 Nov and goes to Uni Blossom. The other place is ML Egret's: at the DPR 20.11 pace she is through about 24 Nov, four days inside her list ETC — so by this line alone CD Glory would berth about 23 Nov night, at the clean berth that frees in that window.")
note_of('6.5K / 8K', "8K 8 on list 20.11 — THE BOARD'S PICK. New Bliss leaves the 6.5K place inside the window of 21 → 22 Nov (DPR 20.11 pace 21 Nov 22:20, list ETC 22 Nov 10:05), so the place is open to the berths that free in that window. CJ-5 frees first (Ken Ann's 24 hours — she berths this evening) and none of the vessels ahead of her can lie there: MANTA SENA (8K 1 — ready from today's meeting, clean berths only), Crystal Land (also printed 8K 1 — clean berths only), Pioneer Fortune (2 — CJ-1 to 4 or the clean berths), Uni Blossom (3 — SAAGAR takes her first), Tan Bin 259 (4 — working at MRG 3), Gokova-M (5 — CJ-7 / 8), Porto Fiscardo (6 — CJ-1 to 4). It turns on about two hours of estimates: if CJ-15A (Heng Yuan Fa Zhan, about 21:30 on the 21st) frees inside the window before CJ-5 does, Manta Sena takes the place there and CD Glory falls to the General line.")
note_of('General · by seniority', "The General queue — GEN 20 on list 20.11. General berths by seniority with at most three bag vessels alongside (Mihir, 19 Nov). With DSM London, Katerina K and Aboudi D alongside, the bag vessels ahead of her are held back, and CJ-1 falls to her when New Bliss leaves — about 22 Nov 00:20 at the DPR 20.11 pace (list ETC 22 Nov 10:05). This is where she goes if the 6.5K place is taken elsewhere — only a few hours later than the 6.5K pick.")

# ================= PRED snapshot =================
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
PGs = 'programme 20.11'
fixed = [
 ['Sea Gautham', 'sails', '20 Nov 08:00', PGs + ' — completed 02:30 (DPR 20.11)'],
 ['Kestrel', 'sails', '20 Nov 11:00', PGs + ' · OJ-6 → Willows (list 20.11 prints Orchids there)'],
 ['Jag Pushpa', 'sails', '20 Nov 13:00', PGs + ' · OJ-3 → SG Friendship'],
 ['Propel Confidence', 'sails', '20 Nov 15:00', PGs + ' — DPR 20.11: cargo done about 14:00'],
 ['ML Egret', '4', '20 Nov 17:30', PGs + ' · SHIFT from CJ-15, port account · est'],
 ['Saga Viking', 'sails', '20 Nov 17:30', PGs + ' · shifts to OTB at her agent\'s request'],
 ['Truong Minh Dream', 'sails', '20 Nov 17:45', PGs],
 ['Belmoira', '15', '20 Nov 18:30', PGs + ' · GOVT(30K) · list 20.11: B\'TODAY · est'],
 ['Ken Ann', '5', '20 Nov 19:30', PGs + ' · 24HRS · list 20.11: B\'TODAY · est'],
 ['Meghna Prestige', 'sails', '20 Nov 19:39', 'list ETC (HP 42,500) — DPR 20.11 pace about 19:00'],
 ['Katerina K', '6', '20 Nov 19:45', PGs + ' · provisional berthing · list 20.11: B\'TODAY · est'],
 ['Rome Trader (salt, next call)', 'sails', '21 Nov 04:40', 'list ETC at the 23,000 norm — DPR 20.11 pace about 01:30'],
 ['Seacon Monaco', 'sails', '21 Nov 06:37', 'DPR 20.11 pace — her list ETC (20 Nov 09:48) is past'],
 ['Vishva Bandhan', 'sails', '21 Nov 17:13', 'DPR 20.11 pace — list ETC 22 Nov 14:33'],
 ['Ken Ann', 'sails', '21 Nov 19:30', '24-hr berth'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — project vessel'],
 ['Europa Graeca', 'sails', '21 Nov 21:45', 'DPR 20.11 pace · Tuna TT-1 → Blue Ionian'],
 ['New Bliss', 'sails', '21 Nov 22:21', 'DPR 20.11 pace — list ETC 22 Nov 10:05'],
 ['Nord Copper', 'sails', '22 Nov 03:03', 'list ETC at the 23,000 norm'],
 ['Belmoira', 'sails', '22 Nov 19:00', 'board estimate — 58,300 MT at 30,000 a day'],
 ['African Hornbill (blades, next call)', 'sails', '24 Nov 04:00', 'board estimate — no norm printed'],
 ['ML Egret', 'sails', '24 Nov 09:40', 'DPR 20.11 pace — list ETC 28 Nov 07:30'],
]
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-25 12:00']
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v187) — list 20.11 + DPR 20.11 applied on programme 20.11; to be read against the signal sheets of 20 Nov, programme 21.11, DPR 21.11 and list 21.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a_), b_, c_, q(d_)) for a_, b_, c_, d_ in fixed + proj)) + B.s[j:]

# ================= PREDLOG =================
a0 = B.s.index("const PREDLOG=["); b0 = B.s.index("\n];", a0)
blk = B.s[a0:b0]
def actual(v, predAt, pb, ab, at):
    global blk
    key = " {v:'%s',predAt:'%s',pb:'%s'," % (q(v), predAt, pb)
    if blk.count(key) != 1: B.die('PREDLOG row: ' + key)
    i = blk.index(key); e = blk.index("\n", i) if "\n" in blk[i:] else len(blk); row = blk[i:e]
    if row.count("ab:'',at:''") != 1: B.die('PREDLOG row already filled: ' + key)
    blk = blk[:i] + row.replace("ab:'',at:''", "ab:'%s',at:'%s'" % (ab, at)) + blk[e:]
actual('DSM London', '11-19 12:29', '2', '2', '11-19 12:50')
actual('Heng Yuan Fa Zhan', '11-19 12:29', '15A', '15A', '11-19 22:06')
actual('African Hornbill (blades, next call)', '11-19 12:29', '14', '16', '11-20 00:30')
actual('African Hornbill (blades, next call)', '11-19 16:12', '14', '16', '11-20 00:30')
actual('African Hornbill (blades, next call)', '11-19 19:51', '16', '16', '11-20 00:30')
actual('Nord Copper', '11-19 12:29', '16', '14', '11-20 02:06')
actual('Nord Copper', '11-19 16:12', '14', '14', '11-20 02:06')
AT = '11-20 10:36'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
R = "20 Nov daily run on DPR 20.11 + list 20.11 (programme 20.11 in hand) — "
new = [
 prow('Aboudi D', R + 'General, CJ-3 from the next window — Sea Gautham has completed and nobody is named behind her; bags, two shore cranes'),
 prow('Tai Keystone', R + 'Govt (bulk urea), CJ-7 after Meghna Prestige — if she reports as declared (20 Nov 12:00)'),
 prow('Uni Blossom', R + 'SAAGAR (SGR 1), CJ-13 when Rome Trader is through — list ETC 21 Nov 04:40, DPR pace about 01:30'),
 prow('Sea Postman', R + 'Govt (rock phosphate in bulk), CJ-8 after Vishva Bandhan'),
 prow('CD Glory', R + 'Mihir & Co — 6.5K / 8K, CJ-5 when Ken Ann\'s 24 hours are up; turns on about two hours (Manta Sena, 8K 1 from today, takes the place if a clean berth frees first). Fallback General, CJ-1 about 22 Nov 00:20. SAAGAR line about 23 Nov night; desk 25 Nov'),
 prow('AG Varvara', R + 'General, CJ-15A after Heng Yuan Fa Zhan — the bag vessels ahead of her are held by the limit of three'),
 prow('Xin Hai Tong 71', R + 'SAAGAR project parcel against the Coastal place, CJ-14 after Nord Copper'),
 prow('Dariya Priya', R + 'General, CJ-15 after Belmoira'),
 prow('Blue Shark', R + 'General (GEN 2 from today) against a vacant HP place, CJ-1 once a bag vessel has left'),
 prow('African Tiger', R + 'SAAGAR, CJ-14 — ML Egret\'s place frees about 24 Nov at the DPR pace'),
 prow('Yuan Hang Wei Ye (next call)', R + 'Sr No 7 quote against the Coastal place, CJ-16 after African Hornbill (pellets only at CJ-16)'),
]
B.s = B.s[:a0] + blk + ",\n" + ",\n".join(new) + B.s[b0:]

# ================= MYLOG =================
g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 10:36 · list 20.11 + DPR 20.11',exp:'%s',b:'%s',slot:'6.5K / 8K — CJ-5 when Ken Ann leaves · or General — CJ-1 when New Bliss leaves, about 22 Nov 00:20 · SAAGAR line about 23 Nov night · desk 25 Nov',why:'" % (g['F'], g['b']) + q(
 "List 20.11: SGR 5 · 8K 8 · GEN 20 — her ranks are unchanged and so is the board's date, the night of 21 Nov. What changed around her: (1) MANTA SENA declared readiness for today's meeting and is printed 8K 1 (Crystal Land is printed 8K 1 as well — the sheet was not renumbered), so one more vessel stands ahead of her in the 6.5K line; like Crystal Land she can lie only at a clean berth, so CJ-5 still falls to CD Glory if it is the first berth to free once the 6.5K place opens (Ken Ann's 24 hours, about 19:30 on the 21st). If CJ-15A frees first, Manta Sena takes the place. (2) The General fallback moved a few hours EARLIER: New Bliss did 7,619 MT (DPR 20.11) and is through about 21 Nov 22:20, so CJ-1 is hers about 22 Nov 00:20 by seniority — the three-bag limit holds back the bag vessels ahead of her. (3) The SAAGAR line moved from the end of the month to about 23 Nov: ML Egret did 7,863 CBM in the day and frees her place about 24 Nov. Either way the board has her alongside between the night of 21 Nov and the early hours of 22 Nov, at CJ-5 or CJ-1. Laytime ends 23 Nov 01:38.") + "'}") + B.s[i:]
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); e = B.s.index("\n ]\n};", a)
B.s = B.s[:e] + (",\n  {d:'20 Nov 10:36 · list 20.11 + DPR 20.11 — norm 23,000, ETC 21 Nov 04:40',exp:'11-18 17:00',b:'13',slot:'alongside CJ-13 · SAAGAR · norm now 23,000 · list ETC 21 Nov 04:40 · DPR pace about 21 Nov 01:30',why:'" + q(
 "List 20.11 restates her NORM as 23,000 MT a day (26,000 on list 19.11) and her ETC as 21 Nov 04:40 (was 20 Nov 22:01) — Nord Copper, the other salt vessel, is printed at 23,000 too. DPR 20.11: 25,320 MT in the 24 hours on 12 hooks (her first night had run at about 21,400 a day); 35,644 MT loaded, 19,631 left at 0700 on the 20th → cargo done about 21 Nov 01:30 at this rate, three hours inside the permissible time. She is not on programme 20.11 (her ETC is after its window); her outward row should come on programme 21.11.") + "'}") + B.s[e:]

# ================= LEARN =================
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 10:36 · list 20.11 + DPR 20.11",
 "The night of 19 Nov against the board, and what list 20.11 changes. TO CONFIRM WITH MIHIR: (1) Ocean Kudos is still printed \"B'TODAY\" on the waiting sheet — have her holds been passed, and for which berth? (2) 8K 1 is printed twice (Manta Sena and Crystal Land) — the board takes Manta Sena first, by reporting.",
 "Board (v177–v186): Yara J out 23:30 as programmed · North Gate out 10:00 on the 19th · Nord Copper alongside about 01:00 · African Hornbill about 23:30 at 175–188 · Heng Yuan Fa Zhan about 21:30 · Rome Trader on norm 26,000, ETC 20 Nov 22:01 · Willows into OJ-6 behind Kestrel.",
 "DPR 20.11 / list 20.11: YARA J let go 01:00 on the 20th and was SHIFTED TO OTB with 3,400 MT still on board (her 24 hours ended 20:30) · NORTH GATE let go 09:50 on the 19th with 2,873 MT not loaded — re-anchored at OTB, back on the waiting sheet with no rank, working at midstream · Nord Copper made fast 02:06 (norm 23,000, ETC 22 Nov 03:03) · African Hornbill made fast 00:30 at 173½–188, printed \"SGR(PROJ)\" · Heng Yuan Fa Zhan 22:06 · HN Doris let go 21:20, 72,775 MT on the sheet · ROME TRADER: norm 23,000, ETC 21 Nov 04:40, 25,320 MT in the day · Manta Sena ready, 8K 1 · Blue Shark GEN 2 · Parvraj reported, GP Y · Ocean Kudos still printed B'TODAY · oil: the list prints Orchids \"B'TODAY\" at OJ-6 where programme 20.11 has Willows · Tuna: Marvelous Star's quantity is 50,000 MT on the list and 76,844 MT on the DPR.",
 "Two more vessels left a berth unfinished when their time was up — Yara J (24-hr berth) and North Gate (list ETC 18 Nov 01:20) — after Evangelia D on 17 Nov: the permissible time is being enforced, and the balance is worked at midstream. The salt norm was restated at 23,000 for Rome Trader and Nord Copper alike. African Hornbill's berthing is called SAAGAR project on the list, which fits Mihir's \"project priority in the absence of HP\". The other points are differences between the port's own sheets, not rules.",
 "v187: actual hours entered; Rome Trader and Nord Copper on norm 23,000 with the printed ETCs; North Gate back in the waiting rows, held while she has no rank; Manta Sena ready under 8K 1, ahead of Crystal Land by reporting; Ocean Kudos stays held; OJ-6 follows the programme (Willows) with the list's Orchids noted. No rule changed. OPEN (1) Ocean Kudos — holds passed, which berth? OPEN (2) 8K 1 printed twice.", "open"))
B.save()
