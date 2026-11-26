#!/usr/bin/env python3
# apply74c — v278 part 3: oil jetties (LIQ), Tuna, timber notes — list 26.11 (revised), DPR 26.11, programme 27.11, HM day signal 26 Nov.
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 26.11 (revised)'); q = B.q
L = 'LIST 26.11 (revised)'; P = 'PROGRAMME 27.11'; D = 'DPR 26.11'; SG = 'HM SIGNAL 26 Nov day sheet'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
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
def berth(bid, nown, add, f=None, nm=None, etc=None, qty=None, est=None):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    if f is not None: now['f'] = js(f)
    if est is False: now.pop('est', None)
    if nm is not None: now['nm'] = js(nm)
    if etc is not None: now['etc'] = js(etc)
    if qty is not None: now['q'] = repr(qty)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS); bput(a, b, d, tail)
def turn(bid, oldn, out, outBy, newn, f, est, add, nm=None, etc=None, qty=None):
    wa, wb = B.line_of("  {n:'%s'," % newn); wl = B.s[wa:wb].strip().rstrip(','); wv = obj(wl); assert 'n' in wv and 'c' in wv
    B.s = B.s[:wa] + B.s[wb + 1:]
    a, b, d, tail = bline(bid); now = obj(d['now']); assert oldn in now['n'], (oldn, now['n'])
    pv = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}; pv['out'] = js(out); pv['outBy'] = js(outBy)
    nw = {k: wv[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'rank', 'ag') if k in wv}; nw['f'] = js(f)
    if est: nw['est'] = '1'
    if nm is not None: nw['nm'] = js(nm)
    if etc is not None: nw['etc'] = js(etc)
    if qty is not None: nw['q'] = repr(qty)
    nw['note'] = "'" + q(add + ' · ') + wv.get('rem', "''")[1:]
    d['prev'] = unobj(pv, PREVKEYS); d['now'] = unobj(nw, NOWKEYS); bput(a, b, d, tail)
    return {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'ag') if k in now}

# ---- the wait / eta blocks must not end with a dangling comma after a line is taken out: normalise at the end (rebuilt below anyway)
turn('OJ-1', 'Bogazici', '11-25 22:30', D + ': butane completed 08:18, propane 19:30; LEFT THE BERTH 22:30 on 25 Nov — 19,854 MT (signal: SHIFT 22:00)',
     'Green Bhavishya (LPG/C)', '11-25 23:32', False, D + ' + ' + L + ': MADE FAST 23:32 on 25 Nov, COMMENCED 01:36 on 26 Nov · norm 500 · ETC 27 NOV 09:32 · 3,853 MT off by 07:00, 10,147 left · ' + P + ': OUT readiness 27 Nov 03:00, 6.6 m — nobody named behind her',
     nm='500', etc='11-27 03:00')
peg = turn('OJ-2', 'Chemroute Pegasus', '11-25 13:30', D + ': WORK STOPPED 13:00, LEFT THE BERTH 13:30, shifted to OTB 16:45 on 25 Nov — 8,109 MT off, 600 MT still on board; back on the waiting sheet as 8C',
     'Thetis Leona', '11-25 16:00', False, D + ' + ' + L + ': MADE FAST 16:00, COMMENCED 18:18 on 25 Nov · norm 225 · ETC 26 Nov 18:13 · 4,546 MT off by 07:00, 454 left',
     nm='225', etc='11-26 14:00')
turn('OJ-2', 'Thetis Leona', '11-26 14:00', SG + ': RT OUT 14:00 · Capt Pathak · ' + L + ': printed in brackets at [2] — outgoing; ETC 26 Nov 18:13 · ' + D + ': 4,546 MT off, 454 left at 07:00',
     'MC Hera', '11-26 17:00', True, SG + ': IN "o/c" · Capt Karan, behind his 13:00 sailing of Ocean Kudos — alongside about 17:00 on 26 Nov, est · ' + L + ': "B\'TODAY" at OJ-2 · norm 475 · 20,599.67 MT → about 28 Nov 14:00 at the norm, est',
     nm='475')
turn('OJ-3', 'Hafnia Ammolite', '11-26 00:30', D + ': COMPLETED 21:30 on 25 Nov, LEFT THE BERTH 00:30 on 26 Nov — 30,800 MT (signal: OUT 23:00)',
     'Lumis', '11-26 03:42', False, D + ' + ' + L + ': MADE FAST 03:42, COMMENCED 08:12 on 26 Nov · norm 650 · QUANTITY 30,605.68 MT on the list (20,000 on the DPR and on every list before) · ETC 28 NOV 08:47',
     nm='650', etc='11-28 08:47', qty=30605.68)
turn('OJ-4', 'Chemroad Nexus', '11-26 09:30', D + ': COMPLETED 05:55 on 26 Nov — 10,950 MT · ' + SG + ': RT OUT 09:30 · Capt Karan · ' + L + ': printed in brackets at [4] — outgoing',
     'Ocean Star', '11-26 12:30', False, L + ': at OJ-4, "B\'TODAY" — 12:30 on 26 Nov printed against her berthing · norm 225 · ETC 27 NOV 17:37 · ' + SG + ': IN "o/c" · Capt Karan, behind Chemroad Nexus · ' + P + ': OUT readiness 27 Nov 16:00, 6.2 m → MT CHEMROAD QUEST in',
     nm='225', etc='11-27 16:00')
berth('OJ-6', 'Culture', D + ' + ' + L + ': MADE FAST 10:53, COMMENCED 13:06 on 25 Nov (the board had ~10:00) — 13,833 MT loaded by 07:00 on 26 Nov, 10,167 left · no norm · ' + P + ': OUT readiness 27 Nov 12:00, 10.1 m — nobody named behind her',
      f='11-25 10:53', est=False, etc='11-27 12:00')
turn('OJ-7', 'Sriwangi V', '11-26 02:15', D + ': COMPLETED 22:24 on 25 Nov, LEFT THE BERTH 02:15 on 26 Nov — 10,000 MT (signal: OUT "o/c", est 02:00)',
     'Peonia', '11-26 03:48', False, D + ' + ' + L + ': MADE FAST 03:48, COMMENCED 07:42 on 26 Nov · norm 650 · 27,000.62 MT · ETC 28 NOV 03:20',
     nm='650', etc='11-28 03:20')

# ---- waiting and expected tankers: rebuilt from the two sheets; a vessel already on the board keeps her line and her history
LJ = json.load(open('/home/claude/work/in26/l26r.json'))
def nrm(x):
    x = x.upper(); x = re.sub(r"\(LPG/C\)", '', x); x = re.sub(r"^(LPG/C\.?|M\.?T\.?)\s*[.]?\s*", '', x.strip()); return re.sub(r'[^A-Z0-9]', '', x)
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
have = {}
for ln in B.s[w0 + 8:e0].split('\n') + B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n'):
    ln = ln.strip().rstrip(',')
    if ln.startswith('{n:'): d = obj(ln); have[nrm(d['n'][1:-1])] = d
peg = dict(peg); peg['rem'] = "''"; peg['q'] = '600'; have['CHEMROUTEPEGASUS'] = peg
ALIAS = {'NO5OCEANPIONEER': 'NO5OCEANPIONEERATLANTICSHG'}
DISP = {'ISHAAN': 'Ishaan', 'SURA': 'Sura', 'KRUIBEKE': 'Kruibeke (LPG/C)', 'YCPANSY': 'YC Pansy', 'NCCDANAH': 'NCC Danah'}
AGD = {'ATLANTIC SHG': 'Atlantic Shg', 'SCORPIO SHG': 'Scorpio Shg', 'NEXWAVE': 'Nexwave', 'INTEROCEAN': 'Interocean', 'JM BAXI': 'JM Baxi', 'WILHELMSEN': 'Wilhelmsen', 'ADMIRAL': 'Admiral', 'GAC SHG': 'GAC Shg', 'VOCEAN': 'V Ocean', 'OCEAN SHG': 'Ocean Shg', 'VICTORY SHG': 'Victory Shg'}
CGD = {'CHEMICALS': 'Chemicals', 'PROPANE': 'Propane', 'CDSBO': 'CDSBO', 'PHOSPHORIC ACID': 'Phosphoric acid', 'CPO': 'CPO', 'HSD': 'HSD', 'METHANOL': 'Methanol', 'PROPANE & BUTANE': 'Propane & butane'}
def dm(x):
    m = re.match(r'(\d{4})-(\d\d)-(\d\d)[ T](\d\d):(\d\d)', x or ''); return '%s-%s %s:%s' % (m.group(2), m.group(3), m.group(4), m.group(5)) if m else None
def say(t):
    d_, hm = t.split(' '); return '%d %s %s' % (int(d_[3:]), 'Nov' if d_[:2] == '11' else 'Dec', hm)
def num(x):
    try: v = round(float(x), 2); return repr(int(v)) if v == int(v) else repr(v)
    except Exception: return None
def tank_rows(sheet):
    out, sec = [], None
    for r in LJ[sheet]:
        r = [('' if x is None else str(x).strip()) for x in r] + [''] * 25
        if r[3] in ('CARGO JETTY VESSELS', 'OIL TANKERS', 'CONTAINERS', 'TUNA VESSELS', 'VADINAR'): sec = r[3]; continue
        if sec == 'OIL TANKERS' and r[3] and r[3] != 'NIL' and r[6] in ('IMP', 'EXP'): out.append(r)
    return out
def val(d, k): return d.get(k, "''").strip("'")
def fresh(k, r):
    nm_ = DISP.get(k)
    if not nm_: B.die('new tanker, give her a display name: ' + r[3] + ' / ' + k)
    return {'n': js(nm_), 'c': js(CGD.get(r[7].upper(), r[7].capitalize())), 'q': num(r[8]) or '0', 'u': "'MT'", 'ie': js(r[6]), 'loa': num(r[5]) or 'null', 'dr': num(r[4]) or 'null', 'ag': js(AGD.get(r[20].upper(), r[20].title())), 'rem': "''"}
WAIT, ETAS, used, chg = [], [], set(), []
for r in tank_rows('WAITING LIST'):
    k = nrm(r[3]); k = ALIAS.get(k, k)
    if k in ('OCEANSTAR', 'MCHERA'): continue                     # "B'TODAY" — on the board at OJ-4 and OJ-2
    isnew = k not in have
    d = dict(have.get(k) or fresh(k, r)); used.add(k); was_eta = 'eta' in d
    rep, rdy = dm(r[10]), dm(r[11]); rank = next((x for x in r[12:20] if x and x != 'X'), '')
    bits = []
    if isnew: bits.append('NEW — reported ' + say(rep))
    elif k == 'CHEMROUTEPEGASUS': bits.append('BACK ON THE WAITING SHEET — shifted out of OJ-2 on 25 Nov 16:45 with 600 MT still on board')
    elif was_eta: bits.append('ON THE WAITING SHEET — reported ' + say(rep))
    oldr = val(d, 'rdy') if d.get('rdy', 'null') != 'null' else ''
    if (rdy or '') != oldr: bits.append(('READY ' + say(rdy)) if rdy else ('readiness now N/A' if r[11] in ('N/A', '') else 'readiness printed "' + r[11] + '" — not ready'))
    elif not rdy and r[11] not in ('N/A', '') and ('"' + r[11] + '"') not in val(d, 'rem'): bits.append('readiness printed "' + re.sub(r'\s+', ' ', r[11]) + '" — not ready')
    if rank != val(d, 'rank'): bits.append('rank ' + (rank or 'none') + ((' (' + val(d, 'rank') + ' before)') if val(d, 'rank') else ''))
    if num(r[8]) and num(r[8]) != d.get('q'): bits.append('quantity ' + num(r[8]) + ' MT (' + d.get('q', '?') + ' before)')
    d.pop('eta', None); d['rep'] = js(rep); d['rdy'] = js(rdy) if rdy else 'null'; d['rank'] = js(rank)
    if num(r[8]): d['q'] = num(r[8])
    if num(r[4]): d['dr'] = num(r[4])
    if 'dr' not in d: d['dr'] = 'null'
    if bits:
        if r[21]: bits.append('"' + r[21] + '"')
        d['rem'] = "'" + q(L + ': ' + ' · '.join(bits) + ' · ') + d.get('rem', "''")[1:]; chg.append(val(d, 'n') + ': ' + ' · '.join(bits))
    WAIT.append('  ' + unobj(d, ('n', 'c', 'q', 'u', 'ie', 'loa', 'dr', 'rep', 'rdy', 'rank', 'ag', 'rem')))
for r in tank_rows('ETA'):
    k = nrm(r[3]); k = ALIAS.get(k, k) if k not in have else k; et = dm(r[10]); rdy = dm(r[11])
    d = dict(have.get(k) or {}); used.add(k); bits = []
    if not d: d = fresh(k, r); bits = ['NEW', 'ETA ' + say(et)]
    else:
        old = val(d, 'eta')
        if old != et: bits.append('ETA ' + say(et) + (' (' + say(old) + ' before)' if old else ''))
        if num(r[8]) and num(r[8]) != d.get('q'): bits.append('quantity ' + num(r[8]) + ' MT (' + d.get('q', '?') + ' before)'); d['q'] = num(r[8])
        if r[20] and AGD.get(r[20].upper(), r[20].title()) != val(d, 'ag'): bits.append('agent ' + AGD.get(r[20].upper(), r[20].title())); d['ag'] = js(AGD.get(r[20].upper(), r[20].title()))
    if num(r[4]): d['dr'] = num(r[4])
    d['eta'] = js(et); d['rdy'] = js(rdy) if rdy else 'null'; d.pop('rep', None); d.pop('rank', None)
    if bits:
        if r[21]: bits.append('"' + r[21] + '"')
        d['rem'] = "'" + q(L + ' (ETA sheet): ' + ' · '.join(bits) + ' · ') + d.get('rem', "''")[1:]; chg.append(val(d, 'n') + ': ' + ' · '.join(bits))
    ETAS.append('  ' + unobj(d, ('n', 'c', 'q', 'u', 'ie', 'loa', 'dr', 'eta', 'rdy', 'ag', 'rem')))
print('\n'.join(chg))
print('tankers no longer on either sheet (dropped):', [have[k]['n'] for k in have if k not in used])
B.s = B.s[:w0 + 8] + ",\n".join(WAIT) + B.s[e0:]
e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
B.s = B.s[:e0 + len("\n ],\n eta:[\n")] + ",\n".join(ETAS) + B.s[m0:]
def rem(name, text):
    a, b = B.line_of("  {n:'%s'," % name); i = B.s.index("rem:'", a) + 5; assert i < b; B.s = B.s[:i] + q(text + ' · ') + B.s[i:]
rem('Chemroad Quest', P + ': OJ-04 — IN behind Ocean Star (out readiness 27 Nov 16:00) → about 18:00 on 27 Nov, est')
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-25 23:39',",
    lambda m: "const LIQ={prog:'" + q("PROGRAMME 27.11 — OJ-1 LPG/C Green Bhavishya out 27 Nov 03:00 · OJ-6 Culture out 27 Nov 12:00 · OJ-4 Ocean Star out 27 Nov 16:00 → Chemroad Quest in · HM SIGNAL 26 Nov day sheet — OJ-4 Chemroad Nexus OUT 09:30 → Ocean Star in (list: 12:30) · OJ-2 Thetis Leona OUT 14:00 → MC Hera in, about 17:00 est · "
        "DPR 26.11 — five turnovers in the night of 25 / 26 Nov: OJ-1 Bogazici → Green Bhavishya 23:32 · OJ-2 Chemroute Pegasus (600 MT left on board) → Thetis Leona 16:00 · OJ-3 Hafnia Ammolite → Lumis 03:42 · OJ-7 Sriwangi V → Peonia 03:48 · ") + m.group(1)
    + "',src:'DPA berthing list 26.11.26 as revised after the meeting · DPR 26.11 · programme 27.11 · signals to the day sheet of 26 Nov (to 0910)',asOf:'11-26 15:14',", B.s, count=1)
if k != 1: B.die('LIQ head not found')
LQN = ['HM signal 26 Nov — day sheet (extended 08:15 / 09:10) · Capt Pathak / Capt Omesh · oil-jetty rows', [
 ['09:30', 'OUT', 'Chemroad Nexus', 'OJ-4 → OTB', 'Karan', '11-26 09:30', 'RT OUT · completed 05:55'],
 ['o/c', 'IN', 'Ocean Star', 'OTB → OJ-4', 'Karan', '11-26 12:30', 'behind Chemroad Nexus · the revised list prints 12:30'],
 ['14:00', 'OUT', 'Thetis Leona', 'OJ-2 → OTB', 'Pathak', '11-26 14:00', 'RT OUT · list ETC 18:13'],
 ['o/c', 'IN', 'MC Hera', 'OTB → OJ-2', 'Karan', '11-26 17:00', 'behind his 13:00 sailing of Ocean Kudos — est']]]
LQD = ['DPR 26.11 and list 26.11 — actual hours at the oil jetties, 25 / 26 Nov', [
 ['10:53', 'IN', 'Culture', 'OTB → OJ-6', '—', '11-25 10:53', 'made fast 10:53, commenced 13:06'],
 ['13:30', 'OUT', 'Chemroute Pegasus', 'OJ-2 → OTB', '—', '11-25 13:30', 'work stopped 13:00, left the berth 13:30, at OTB 16:45 — 600 MT still on board'],
 ['16:00', 'IN', 'Thetis Leona', 'OTB → OJ-2', '—', '11-25 16:00', 'made fast 16:00, commenced 18:18'],
 ['22:30', 'OUT', 'Bogazici (LPG/C)', 'OJ-1 → OTB', '—', '11-25 22:30', 'completed 19:30, left the berth 22:30'],
 ['23:32', 'IN', 'Green Bhavishya (LPG/C)', 'OTB → OJ-1', '—', '11-25 23:32', 'made fast 23:32, commenced 01:36 — board had ~23:15'],
 ['00:30', 'OUT', 'Hafnia Ammolite', 'OJ-3 → OTB', '—', '11-26 00:30', 'completed 21:30, left the berth 00:30'],
 ['02:15', 'OUT', 'Sriwangi V', 'OJ-7 → OTB', '—', '11-26 02:15', 'completed 22:24, left the berth 02:15'],
 ['03:42', 'IN', 'Lumis', 'OTB → OJ-3', '—', '11-26 03:42', 'made fast 03:42, commenced 08:12 — board had ~03:00'],
 ['03:48', 'IN', 'Peonia', 'OTB → OJ-7', '—', '11-26 03:48', 'made fast 03:48, commenced 07:42 — board had ~04:00'],
 ['05:55', '—', 'Chemroad Nexus', 'OJ-4', '—', '11-26 05:55', 'completed 05:55 — 10,950 MT']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n  " + js(LQD) + ",\n")

# ================= TUNA =================
B.s, k = re.subn(r"const TUNA=\{src:'(?:[^'\\]|\\.)*',", lambda m: "const TUNA={src:'" + q("DPA berthing list 26.11.26 (revised) · DPR 26.11 · TT-1 Blue Ionian and TT-3 MP Postpanamax 1 working · TT-2 and TT-4 vacant · waiting: Sakizaya Star, RB Leah (both ready; RB Leah marked TT-03) · nothing expected") + "',", B.s, count=1)
if k != 1: B.die('TUNA head')
def tnote_tt(bid, text):
    k_ = "  {b:'%s',n:" % bid
    a, b = B.line_of(k_); i = B.s.index("note:'", a) + 6; assert i < b; B.s = B.s[:i] + q(text + ' ') + B.s[i:]
tnote_tt('TT-3', D + ': 23,200 MT in 24 h (25,386 the day before) — 50,100 off, 37,900 left → about 27 Nov 22:10 at this rate.')
tnote_tt('TT-1', D + ': 12,800 MT in 24 h — 38,200 off, 35,155 left → about 29 Nov 00:55 at this rate.')

# ================= TIMBER =================
def tnote(name, text, tag=P):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
B.rep("{n:'Uni Blossom',cbm:34870,from:'Uruguay',c:'Pine logs',eta:'11-09 11:36',etb:'11-20',comm:'11-21 03:45',note:'", "{n:'Uni Blossom',cbm:34870,from:'Uruguay',c:'Pine logs',eta:'11-09 11:36',etb:'11-20',comm:'11-21 03:45',note:'" + q(D + " (sailing block): SAILED 10:35 on 25 Nov · "))
B.rep("{n:'AG Varvara',cbm:39113,from:'Australia',c:'Pine logs',eta:'11-12 07:06',etb:'11-24',note:'", "{n:'AG Varvara',cbm:39113,from:'Australia',c:'Pine logs',eta:'11-12 07:06',etb:'11-24',comm:'11-25 15:15',note:'" + q(D + ": MADE FAST 12:12, COMMENCED 15:15 on 25 Nov at CJ-13 — 29,767 pcs / 4,064 CBM in her first 16 hours on 8 hooks; 256,746 pcs / 35,048 CBM left · stevedore RSIPL · " + L + ": norm 4,000, ETC 5 Dec 08:52 · "))
tnote('CD Glory', "not on it. The vacant Govt place went to Hai Nam 81 (salt, HP 1) as \"GOV(30K)\" at CJ-15A; CJ-14 goes to Blue Shark, shifted from CJ-5 · revised list: SGR 1 · 8K 5 · GEN 10 · the SAAGAR place she waits for is Asian Summit's — petcoke, 26,200 MT a day, 30,499 left at 07:00 on 26 Nov; being shifted CJ-7 → CJ-5 tonight")
tnote('Paiwan Ace', "not on it · revised list: SGR 4 · 8K 8 · GEN 17")
tnote('Dariya Priya', "SGR 2 · 8K 6 · GEN 12 · " + D + ": 1,315 CBM at midstream + 1,354 CBM landed at the barge area in 24 h — 8,219 CBM off, 36,749 left", tag=L)
tnote('African Tiger', "SGR 3 · 8K 7 · GEN 14", tag=L)
tnote('African Pheasant', "SGR 5 · 8K 10 · GEN 19", tag=L)
tnote('Erna Oldendorff', "SGR 6 · GEN 20", tag=L)
a, b = B.line_of(" {n:'Paiwan Wisdom',cbm:19320,")
B.s = B.s[:b] + "\n {n:'Team Bravo',cbm:20722,from:'—',c:'Pine logs',eta:'11-29',etb:null,note:'" + q(L + ": FIRST TIME ON THE PORT LIST (expected sheet) — pine logs 20,722 CBM · ETA 29 Nov · N/A · SGR Y · 8K Y · Sr No 07 · 179.99 m · agent Synergy · not on the timber desk sheet of 24 Nov") + "'}," + B.s[b:]
B.save(); print('saved 74c')
