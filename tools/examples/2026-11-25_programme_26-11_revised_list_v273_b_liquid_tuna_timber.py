#!/usr/bin/env python3
# apply69b — v273 part 2: oil jetties, Tuna and timber rows from programme 26.11 and the revised list 25.11; one berth rule learnt from the programme.
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 25.11 (revised)'); q = B.q
L = 'LIST 25.11 (revised)'; P = 'PROGRAMME 26.11'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)

# ================= ENGINE — a gearless coal / ore vessel may lie at CJ-16 =================
# Programme 26.11 berths MSC MAGALI (gearless, 253.54 m, steam coal) at CJ-16 as HP(50K). The board had held every vessel over 200 m to the shore-crane berths CJ-7 / 8,
# so it never offered her CJ-16. Coal / coke / ore are handled at CJ-16 (Trade Notice 3089); a gearless vessel with such cargo keeps CJ-16 as well as CJ-7 / 8.
B.rep("if(GEARLESS(w)&&!CLEANONLY(c))A=A.filter(b=>SHORECRANE.includes(b));",
      "if(GEARLESS(w)&&!CLEANONLY(c))A=A.filter(b=>SHORECRANE.includes(b)||(OPEN16&&b==='16'&&(COAL(c)||DIRTY(c)))); // programme 26.11: MSC Magali (gearless, 253 m, coal) is given CJ-16 — a gearless coal / ore vessel keeps CJ-16 beside CJ-7 / 8")

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
def turn(bid, oldn, out, outBy, newn, f, est, add, nm=None, etc=None):
    wa, wb = B.line_of("  {n:'%s'," % newn); wl = B.s[wa:wb].strip().rstrip(','); wv = obj(wl); assert 'n' in wv and 'c' in wv
    B.s = B.s[:wa] + B.s[wb + 1:]
    a, b, d, tail = bline(bid); now = obj(d['now']); assert oldn in now['n'], (oldn, now['n'])
    pv = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}; pv['out'] = js(out); pv['outBy'] = js(outBy)
    nw = {k: wv[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'rank', 'ag') if k in wv}; nw['f'] = js(f)
    if est: nw['est'] = '1'
    if nm is not None: nw['nm'] = js(nm)
    if etc is not None: nw['etc'] = js(etc)

berth('OJ-1', 'Bogazici', P + ': OJ-01 · 25 Nov 20:00, 8.0 m — "NIGHT SHIFTING FROM OJ-01 TO OTB. AGENT\'S REQ." → LPG/C GREEN BHAVISHYA in, night starboard', etc='11-25 20:00')
berth('OJ-2', 'Chemroute Pegasus', L + ': norm now 360 · ETC 25 Nov 12:06 (08:54 on the morning sheet; programme 25.11 readiness 17:30)')
berth('OJ-3', 'Hafnia Ammolite', P + ': OJ-03 · OUT readiness 25 Nov 23:00, 7.8 m, night sailing → MT LUMIS in, night berthing', etc='11-25 23:00')
berth('OJ-4', 'Chemroad Nexus', L + ': norm now 250 (525 on the morning sheet) · ETC 26 NOV 17:20 (01:11 before) · ' + P + ': printed "CJ-04" — OUT readiness 26 Nov 17:20, 7.64 m → MT OCEAN STAR in', nm='250', etc='11-26 17:20')
berth('OJ-7', 'Sriwangi V', P + ': OJ-07 · OUT readiness 25 Nov 18:35, 10.0 m, night sailing → MT PEONIA in, night starboard', etc='11-25 18:35')
LJ = json.load(open('/home/claude/work/in25b/l25r.json'))
def nrm(x):
    x = x.upper(); x = re.sub(r"\(LPG/C\)", '', x); x = re.sub(r"^(LPG/C\.?|M\.?T\.?)\s*[.]?\s*", '', x.strip()); return re.sub(r'[^A-Z0-9]', '', x)
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0); m0 = B.s.index("\n ],\n moves:[\n", e0)
have = {}
for ln in B.s[w0 + 8:e0].split('\n') + B.s[e0 + len("\n ],\n eta:[\n"):m0].split('\n'):
    ln = ln.strip().rstrip(',')
    if ln.startswith('{n:'): d = obj(ln); have[nrm(d['n'][1:-1])] = d
print('tankers on the board:', sorted(have))
DISP = {'MULAN': 'Mulan', 'ZAHRA': 'Zahra', 'ZHENGHE3': 'Zheng He 3', 'HANYUCAMELLIA': 'Hanyu Camellia'}
AGD = {'ATLANTIC SHG': 'Atlantic Shg', 'SCORPIO SHG': 'Scorpio Shg', 'NEXWAVE': 'Nexwave', 'INTEROCEAN': 'Interocean', 'JM BAXI': 'JM Baxi', 'WILHELMSEN': 'Wilhelmsen', 'ADMIRAL': 'Admiral', 'GAC SHG': 'GAC Shg', 'VOCEAN': 'V Ocean', 'OCEAN SHG': 'Ocean Shg'}
CGD = {'CHEMICALS': 'Chemicals', 'PROPANE': 'Propane', 'CDSBO': 'CDSBO', 'PHOSPHORIC ACID': 'Phosphoric acid', 'CPO': 'CPO'}
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
        if sec == 'OIL TANKERS' and r[1] == 'OJ': out.append(r)
    return out
def val(d, k): return d.get(k, "''").strip("'")
WAIT, ETAS, used, chg = [], [], set(), []
for r in tank_rows('WAITING LIST'):
    k = nrm(r[3])
    if k == 'CULTURE': continue                                   # alongside OJ-6 since 25 Nov
    d = dict(have.get(k) or {}); used.add(k); was_eta = 'eta' in d
    if not d: B.die('new tanker on the waiting sheet, give her a line: ' + r[3])
    rep, rdy = dm(r[10]), dm(r[11]); rank = next((x for x in r[12:20] if x and x != 'X'), '')
    if r[12:20].count('X'): rank = val(d, 'rank')                 # berthing today: keep the rank she had
    bits = []
    if was_eta: bits.append('ON THE WAITING SHEET — reported ' + say(rep))
    if (rdy or '') != (val(d, 'rdy') if d.get('rdy', 'null') != 'null' else ''): bits.append(('READY ' + say(rdy)) if rdy else 'readiness now N/A')
    if rank != val(d, 'rank'): bits.append('rank ' + (rank or 'none') + ' (' + (val(d, 'rank') or 'none') + ' on the morning sheet)')
    if num(r[8]) and num(r[8]) != d.get('q'): bits.append('quantity ' + num(r[8]) + ' MT (' + d.get('q', '?') + ' before)')
    d.pop('eta', None); d['rep'] = js(rep); d['rdy'] = js(rdy) if rdy else 'null'; d['rank'] = js(rank)
    if num(r[8]): d['q'] = num(r[8])
    if num(r[4]): d['dr'] = num(r[4])
    if bits:
        if r[21]: bits.append('"' + r[21] + '"')
        d['rem'] = "'" + q(L + ': ' + ' · '.join(bits) + ' · ') + d.get('rem', "''")[1:]; chg.append(val(d, 'n') + ': ' + ' · '.join(bits))
    WAIT.append('  ' + unobj(d, ('n', 'c', 'q', 'u', 'ie', 'loa', 'dr', 'rep', 'rdy', 'rank', 'ag', 'rem')))
for r in tank_rows('ETA'):
    k = nrm(r[3]); et = dm(r[10]); rdy = dm(r[11])
    if k == 'NO5OCEANPIONEER': k = 'NO5OCEANPIONEERATLANTICSHG' if 'NO5OCEANPIONEERATLANTICSHG' in have and r[20].upper() != 'ADMIRAL' else k
    d = dict(have.get(k) or {}); used.add(k); bits = []
    if not d:
        nm_ = DISP.get(k)
        if not nm_: B.die('new expected tanker, give her a display name: ' + r[3] + ' / ' + k)
        d = {'n': js(nm_), 'c': js(CGD.get(r[7].upper(), r[7].capitalize())), 'q': num(r[8]) or '0', 'u': "'MT'", 'ie': js(r[6]), 'loa': num(r[5]) or 'null', 'dr': num(r[4]) or 'null', 'ag': js(AGD.get(r[20].upper(), r[20].title())), 'rem': "''"}
        bits = ['NEW', 'ETA ' + say(et)]
    else:
        old = val(d, 'eta')
        if old != et: bits.append('ETA ' + say(et) + (' (' + say(old) + ' before)' if old else ''))
        if num(r[8]) and num(r[8]) != d.get('q'): bits.append('quantity ' + num(r[8]) + ' MT (' + d.get('q', '?') + ' before)'); d['q'] = num(r[8])
        if r[20] and AGD.get(r[20].upper(), r[20].title()) != val(d, 'ag'): bits.append('agent ' + AGD.get(r[20].upper(), r[20].title())); d['ag'] = js(AGD.get(r[20].upper(), r[20].title()))
    if rdy and (d.get('rdy', 'null') == 'null'): bits.append('READINESS printed ' + say(rdy))
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
rem('Green Bhavishya (LPG/C)', P + ': OJ-01 — IN behind LPG/C Bogazici (shifting to OTB 25 Nov 20:00), night starboard → about 22:00 on 25 Nov, est')
rem('Lumis', P + ': OJ-03 — IN behind Hafnia Ammolite (out readiness 25 Nov 23:00), night berthing → about 01:00 on 26 Nov, est')
rem('Ocean Star', P + ': OJ-04 (printed "CJ-04") — IN behind Chemroad Nexus (out readiness 26 Nov 17:20) → about 19:20 on 26 Nov, est')
rem('Peonia', P + ': OJ-07 — IN behind Sriwangi V (out readiness 25 Nov 18:35), night starboard → about 20:35 on 25 Nov, est')
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-25 13:02',",
    lambda m: "const LIQ={prog:'" + q("PROGRAMME 26.11 — OJ-7 Sriwangi V out 25 Nov 18:35 → Peonia in, night · OJ-1 LPG/C Bogazici shifts to OTB 25 Nov 20:00 → LPG/C Green Bhavishya in · OJ-3 Hafnia Ammolite out 25 Nov 23:00 → Lumis in, night · OJ-4 Chemroad Nexus out 26 Nov 17:20 → Ocean Star in · REVISED LIST 25.11 — Lumis and Peonia now ready and ranked 1E / 2E · ") + m.group(1)
    + "',src:'DPA berthing list 25.11.26 as revised after the meeting · DPR 25.11 · programme 26.11 · signals to the evening sheet of 24 Nov (disp 1655, amended to 1920)',asOf:'11-25 16:11',", B.s, count=1)
if k != 1: B.die('LIQ head not found')

# ================= TUNA =================
a, b = B.line_of("  {n:'RB Leah',"); ln = B.s[a:b]
assert ln.count("rep:'11-24 19:00',rdy:null") == 1 and ln.count("rem:'") == 1
ln = ln.replace("rep:'11-24 19:00',rdy:null", "rep:'11-24 19:00',rdy:'11-25 11:00'").replace("rem:'", "rem:'" + q(L + ": READY — commercial readiness 25 Nov 11:00 · remark \"TT-03\" · "))
B.s = B.s[:a] + ln + B.s[b:]

# ================= TIMBER =================
def tnote(name, text, tag=P):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('CD Glory', "not on it — no timber berth came free in this window (CJ-14's head went to the coastal tug and barge; CJ-15A to the shift of African Hornbill) · revised list: SGR 1 · 8K 6 · GEN 10, unchanged")
tnote('Paiwan Ace', "not on it · revised list: SGR 4 · 8K 10 · GEN 20")
tnote('Dariya Priya', "SGR 2 · 8K 7 · GEN 12", tag=L)
tnote('African Tiger', "SGR 3 · 8K 8 · GEN 16", tag=L)
tnote('African Pheasant', "SGR 5 · 8K 12 · GEN 22", tag=L)
tnote('Erna Oldendorff', "SGR 6 · GEN 23", tag=L)
B.rep("{n:'Paiwan Wisdom',cbm:null,from:'USA',c:'Logs',eta:'11-28',", "{n:'Paiwan Wisdom',cbm:19320,from:'USA',c:'Pine logs',eta:'11-28',")
tnote('Paiwan Wisdom', "FIRST TIME ON THE PORT LIST (expected sheet) — pine logs 19,320 CBM · ETA 28 Nov · N/A · SGR Y · 8K Y · Sr No 07 · 175.53 m · agent Synergy", tag=L)
B.save(); print('saved 69b')
