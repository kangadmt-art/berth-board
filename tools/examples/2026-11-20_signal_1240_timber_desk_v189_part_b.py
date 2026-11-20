#!/usr/bin/env python3
# apply34b — v189 (part 2, data): the SECOND signal sheet of 20 Nov (dispatched 12:40) and the timber desk sheet of 20 Nov 12:00 (after the berthing meeting),
# both sent by Mihir at 12:52 while part 1 was being applied. Run after apply34a.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P, list_tag='HM SIGNAL 20 Nov (12:40 sheet)'); q = B.q
SG = "HM SIGNAL 20 Nov (12:40 sheet)"; DK = "TIMBER DESK SHEET 20 Nov 12:00 (after the berthing meeting)"
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

B.rep("const NOW=h('11-20 12:46');", "const NOW=h('11-20 12:52');")
B.rep("Signals to <b>20 Nov day sheet (amended, disp 1025 / 1035 / 1055)</b>", "Signals to <b>20 Nov afternoon sheet (disp 1240)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 20 Nov 12:52: the second HM signal sheet of 20 Nov (dispatched 12:40) — Safi Alfa into CJ-4, Parvraj in with her berth \"pending\", Truong Minh Dream out 18:15, Hatnyanawati into OJ-2 — and the timber desk sheet of 20 Nov 12:00, written after the berthing meeting (Uni Blossom to berth 23:00 tonight under Saagar; CD Glory ETB 26 Nov) · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 20 Nov (12:40 sheet) · timber desk 20 Nov 12:00 · ")

# ---------------- V ----------------
M = "{b:'5',n:'Ken Ann',p:[33.5,41.5]"
pre(M, "The 12:40 sheet no longer carries her — she was in hand or alongside by then; 12:30 is the board's estimate.")
sub(M, "f:'11-20 13:00',t:'11-21 13:00',est:1", "f:'11-20 12:30',t:'11-21 12:30',est:1")
M = "{b:'6',n:'Truong Minh Dream',nm:17193,p:[42.5,51.25]"
pre(M, SG + ": OUT 18:15 · Capt Verma (17:45 on the earlier sheet).")
sub(M, "t:'11-20 17:45',lt:'11-19 13:46'", "t:'11-20 18:15',lt:'11-19 13:46'")
M = "{b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75]"
pre(M, SG + ": RT OUT 17:00 · Capt Sud + Dixit — and SAFI ALFA is signalled IN behind her at 23–31¾.")
# ML Egret is NOT shifted: her CJ-4 entry goes, the CJ-15 entry runs to the list ETC
a, b = B.line_of(" {b:'4',n:'ML Egret',nm:4600,p:[23,31.75],")
B.s = B.s[:a] + B.s[b + 1:]
M = "{b:'15',n:'ML Egret',nm:4600,p:[143.5,156.75]"
pre(M, SG + ": SAFI ALFA is signalled IN at 23–31¾ — the very CJ-4 panels that list 20.11 had printed for ML Egret. Her shift on the port's account (programme 20.11) is OFF: she stays at CJ-15 on her list ETC, 28 Nov 07:30 (about 24 Nov at the DPR 20.11 pace).")
sub(M, "t:'11-20 17:30',est:1", "t:'11-28 07:30'")
# Belmoira — the berth programme 20.11 gave her (CJ-15, behind ML Egret's shift) is not vacated: she returns to the waiting rows
a, b = B.line_of(" {b:'15',n:'Belmoira',nm:30000,p:[143.5,156.75],")
B.s = B.s[:a] + B.s[b + 1:]
# Safi Alfa — signalled IN at CJ-4
a, b = B.line_of(" {b:'4',n:'Propel Confidence',nm:21160,p:[23.5,31.75],")
B.s = B.s[:b + 1] + vline({'b': '4', 'n': 'Safi Alfa', 'nm': 3000, 'p': [23, 31.75], 'c': 'Rice bags', 'q': 24750, 'u': 'MT', 'cat': 'GEN', 'f': '11-20 19:00', 't': '11-29 01:00', 'est': 1,
    'note': SG + ': IN "o/c" · Capt G. Raj · OTB → 23–31¾ (CJ-4), behind Propel Confidence (RT OUT 17:00) — about 19:00 alongside is the board\'s estimate. GENERAL by seniority — GEN 1 on list 20.11, the senior vessel of the line; she takes the berth that programme 20.11 and list 20.11 had marked for ML Egret\'s shift. Rice bags, 24,750 MT still to load of 32,100 · 189.99 m · no norm printed yet — about 3,000 a day assumed, to 29 Nov · agent as on the list'}) + "\n" + B.s[b + 1:]
B.wdel('Safi Alfa')
# Uni Blossom — the timber desk, after the meeting: will berth 20 Nov 23:00 under Saagar. Berth not named: CJ-13 behind Rome Trader is the board's reading.
a, b = B.line_of(" {b:'13',n:'Rome Trader (salt, next call)',nm:23000,p:[113,125.25],")
B.s = B.s[:b + 1] + vline({'b': '13', 'n': 'Uni Blossom', 'nm': 4600, 'p': [113, 125.25], 'c': 'Pine logs', 'q': 34870, 'u': 'CBM', 'cat': 'SAAGAR', 'f': '11-20 23:00', 't': '11-28 15:00', 'est': 1,
    'note': DK + ': "Will berth – 20.11.2026 @ 2300 hrs under Saagar Priority". The sheet names no berth: CJ-13 behind Rome Trader is the BOARD\'S READING — hers is the only SAAGAR place that frees tonight. To be set right by programme 21.11. Pine logs 34,870 CBM from Uruguay · SGR 1 on list 20.11 · arrived 9 Nov 11:36 · 179.97 m, 10.8 m · norm 4,600 CBM a day assumed (ML Egret\'s), to 28 Nov'}) + "\n" + B.s[b + 1:]
B.wdel('Uni Blossom')
M = "{b:'13',n:'Rome Trader (salt, next call)',nm:23000,p:[113,125.25]"
pre(M, "MIHIR & COMPANY · " + DK + " has Uni Blossom berthing at 23:00 tonight under Saagar. If that is CJ-13 (the board's reading), ROME TRADER must be out about 21:00 on 20 Nov — entered as an ESTIMATE, seven and a half hours ahead of her list ETC (21 Nov 04:40) and four and a half ahead of the DPR 20.11 pace. Her outward row on programme 21.11 will give the hour.")
sub(M, "f:'11-18 17:00',t:'11-21 04:40'", "f:'11-18 17:00',t:'11-20 21:00',lt:'11-21 04:40'")

# ---------------- cargo rule: rock phosphate is not Govt priority unless the list prints it ----------------
B.rep("&&!/bag|acid/i.test(w.c)&&!(w.rk&&w.rk.GOV)).sort(", "&&!/bag|acid|rock/i.test(w.c)&&!(w.rk&&w.rk.GOV)).sort(")

# ---------------- W ----------------
w = B.wrow
w('Parvraj', "IN \"o/c\" · Capt Karan + Nikhil — berth \"PENDING\" on the sheet. She is the Govt vessel (GP Y) of the day; the board seats her at the fertiliser berth that frees first")
w('Sea Postman', "PARVRAJ (GP Y, reported 20 Nov) is signalled in ahead of her, and on programme 20.11 the vacant Govt place went to a 30K quote (Belmoira) while she lay ready since 17 Nov — rock phosphate is NOT being treated as Govt priority. From v189 she stands in General only (GEN 22)")
m = B._row('Dariya Priya').search(B.s); e = B.s.index("],\n", m.start()) + 3
ROW = (" ['Belmoira','Salt in bulk',58300,'MT',199.92,6.71,'11-16 17:30',{HP:3.5,'8K':11,GEN:21.5},'" + q(
  "HM SIGNAL 20 Nov (12:40 sheet): the berth programme 20.11 gave her — CJ-15 as GOVT(30K), behind ML Egret's shift to CJ-4 — is NOT being vacated (Safi Alfa is signalled into CJ-4, ML Egret stays). She is back in the waiting rows until programme 21.11 says where she goes. List 20.11 printed her starred (\"GOVT(30K) B'TODAY\", ranks X) between Dariya Priya and Sea Postman — carried as HP 3.5 · 8K 11 · GEN 21.5 until a list prints her ranks again. With Parvraj (GP Y) ready, the Govt place is no longer open to a 30K quote · LIST 18.11: REPORTED / READY 16 Nov 17:30 · HP 4 · 8K 12 · GEN 26 · 30K/25K/10K Sr No 7 · 6.71 m · 58,300 MT EXP · agent Cross Trade") + "'],\n")
B.s = B.s[:e] + ROW + B.s[e:]

# ---------------- PROG_SAIL ----------------
a, b = B.line_of("const PROG_SAIL=new Set([")
ln = B.s[a:b]
assert ln.count(",'ML Egret'") == 1, ln.count("'ML Egret'")
ln = ln.replace(",'ML Egret'", "").replace("const PROG_SAIL=new Set([", "const PROG_SAIL=new Set(['Rome Trader (salt, next call)',", 1)
B.s = B.s[:a] + ln + B.s[b:]

# ---------------- MV ----------------
MVN = ['HM signal 20 Nov — afternoon sheet (dispatched 12:40) · Capt Pathak', [
  ['15:15', 'OUT', 'Konrad', 'CJ-12 · 101–109 → OTB', 'G. Raj', '11-20 15:15', 'RT OUT · container'],
  ['o/c', 'IN', 'Safi Alfa', 'OTB → CJ-4 · 23–31¾', 'G. Raj', '11-20 19:00', 'behind Propel Confidence — about 19:00, est · General, GEN 1'],
  ['17:00', 'OUT', 'Propel Confidence', 'CJ-4 · 23½–31¾ → OTB', 'Sud + Dixit', '11-20 17:00', 'RT OUT'],
  ['16:00', '—', 'Heng Yuan Fa Zhan', 'CJ-15A · 161¾–169 · turned round at the berth', 'Karan + Nikhil', '11-20 16:00', 'TURN AROUND · flood to ebb · agent\'s account'],
  ['17:00', 'IN', 'Flexi-2', 'OTB → CJ-12 · 100–109½', 'Karan + Nikhil', '11-20 17:00', 'container · flood'],
  ['o/c', 'IN', 'Parvraj', 'OTB → berth "PENDING"', 'Karan + Nikhil', '11-20 20:30', 'Govt (GP Y) · the berth is not written — est'],
  ['18:15', 'OUT', 'Truong Minh Dream', 'CJ-6 · 42½–51¼ → OTB', 'Verma', '11-20 18:15', '17:45 on the earlier sheet']]]
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
def oj2(d):
    d['out'] = "'11-20 19:00'"
    d['outBy'] = js('HM SIGNAL 20 Nov (12:40 sheet): Jeil Crystal RT OUT 19:00 · Capt Karan + Nikhil — list ETC 20 Nov 21:29')
    d['next'] = js({'n': 'Hatnyanawati', 'c': 'Chemicals', 'q': 10000, 'u': 'MT', 'ie': 'EXP', 'loa': 123.5, 'f': '11-20 21:00', 'est': 1, 'rank': '', 'ag': 'GAC Shg',
        'note': 'HM SIGNAL 20 Nov (12:40 sheet): IN "o/c" at OJ-2 behind Jeil Crystal (RT OUT 19:00) · Capt Sud + Dixit — about 21:00 alongside, est · list 20.11: readiness N/A, REQ OJ 2, 3, 4 · reported 18 Nov 07:12'})
    return d
berth('OJ-2', oj2)
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); e0 = B.s.index("\n ],\n eta:[\n", w0)
wait = [r.rstrip(',') for r in B.s[w0 + len(" wait:[\n"):e0].split('\n')]
W2 = [r for r in wait if not r.startswith("  {n:'Hatnyanawati',")]
assert len(W2) == len(wait) - 1
B.s = B.s[:w0] + " wait:[\n" + ",\n".join(W2) + B.s[e0:]
LMN = ['HM signal 20 Nov — afternoon sheet (dispatched 12:40)', [
  ['15:15', 'IN', 'SG Friendship', 'OTB → OJ-3', 'Sud + Dixit', '11-20 15:15', 'about 17:00 alongside, est'],
  ['15:30', 'OUT', 'Jag Pushpa', 'OJ-3 → OTB', 'Sandeep', '11-20 15:30', 'RT OUT'],
  ['o/c', 'IN', 'Orchids', 'OTB → OJ-6', 'Sandeep', '11-20 17:30', 'on arrival (ETA) · est'],
  ['19:00', 'OUT', 'Jeil Crystal', 'OJ-2 → OTB', 'Karan + Nikhil', '11-20 19:00', 'RT OUT'],
  ['o/c', 'IN', 'Hatnyanawati', 'OTB → OJ-2', 'Sud + Dixit', '11-20 21:00', 'behind Jeil Crystal — est']]]
a = B.s.index("const LIQ={"); mm = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:mm] + "  " + js(LMN) + ",\n" + B.s[mm:]
B.rep("signals to the day sheet of 20 Nov (amended, disp 1055)',asOf:'11-20 12:46',", "signals to the afternoon sheet of 20 Nov (disp 1240)',asOf:'11-20 12:52',")

# ---------------- TIMBER — desk sheet 20 Nov 12:00 ----------------
a, b = B.line_of("const TIMBER={src:")
B.s = B.s[:a] + "const TIMBER={src:\"Kandla Timber Vessel's Position · Mihir & Co timber desk\",d:'20 Nov 1200',upto:'21 Nov 1800, after the berthing meeting of 20 Nov'," + B.s[b:]
B.rep(" asOf:'11-16 18:00',etaFromDesk:false,waiting:null,", " asOf:'11-20 12:00',etaFromDesk:true,waiting:43,")
def T(pfx, d): B.set_line(pfx, " " + js(d) + ",")
T(" {n:'ML Egret',cbm:42886,", {'n': 'ML Egret', 'cbm': 42886, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-06 14:24', 'etb': '11-18', 'comm': '11-18 23:35',
   'note': 'berthed 18 Nov 21:45 at CJ-15 under SAAGAR · DPR 20.11: 22,561 pcs / 7,863 CBM in 24 h — 10,558 off, 32,327 left · list 20.11: norm 4,600 CBM, ETC 28 Nov 07:30 · her shift to CJ-4 is OFF — the 12:40 signal of 20 Nov sends Safi Alfa there · 12.11 m'})
T(" {n:'Uni Blossom',cbm:34870,", {'n': 'Uni Blossom', 'cbm': 34870, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-09 11:36', 'etb': '11-20',
   'note': 'desk 20 Nov, after the meeting: WILL BERTH 20 Nov 23:00 under Saagar priority — no berth named; the board reads CJ-13 behind Rome Trader · SGR 1 on list 20.11 · 10.8 m'})
T(" {n:'AG Varvara',cbm:39113,", {'n': 'AG Varvara', 'cbm': 39113, 'from': 'Australia', 'c': 'Pine logs', 'eta': '11-12 07:06', 'etb': '11-26', 'note': 'desk ETB 26 Nov (24 Nov on the sheet of 16 Nov) · SGR 3 · GEN 16 on list 20.11 · 199.99 m, 9.0 m'})
T(" {n:'CD Glory',cbm:29158,", {'n': 'CD Glory', 'cbm': 29158, 'from': 'Malaysia', 'c': 'Hardwood logs', 'eta': '11-15 06:42', 'etb': '11-26',
   'note': 'desk ETB 26 Nov (25 Nov on the sheet of 16 Nov) · list 20.11: SGR 5 · 8K 8 · GEN 20 · 179.9 m, 10.4 m — fits CJ-1, CJ-4, CJ-5'})
T(" {n:'Dariya Priya',cbm:44968,", {'n': 'Dariya Priya', 'cbm': 44968, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-16 09:00', 'etb': '11-30',
   'note': '"Darya Priya" on the desk sheet · desk ETB 30 Nov (29 Nov before) · list 20.11: SGR 6 · 8K 10 · GEN 21 · 11.0 m'})
T(" {n:'African Tiger',cbm:36328,", {'n': 'African Tiger', 'cbm': 36328, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-18 06:30', 'etb': '12-03',
   'note': 'desk: arrived 18 Nov 11:00, ETB 3 Dec · list 20.11: SGR 7 · 8K 12 · GEN 25 · reported 18 Nov 06:30 · 180 m, 10.8 m'})
T(" {n:'Paiwan Ace',cbm:null,", {'n': 'Paiwan Ace', 'cbm': None, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-22 01:00', 'etb': '12-08', 'note': 'desk 20 Nov: ETA 22 Nov 01:00 (21 Nov 21:00 before)'})
T(" {n:'Erna Oldendorff',cbm:null,", {'n': 'Erna Oldendorff', 'cbm': None, 'from': 'Australia', 'c': 'Pine logs', 'eta': '11-23 20:00', 'etb': '12-08', 'note': '"Erna Oldendroff" on the desk sheet'})
T(" {n:'African Pheasant',cbm:null,", {'n': 'African Pheasant', 'cbm': None, 'from': 'New Zealand', 'c': 'Logs', 'eta': '11-23 16:30', 'etb': '12-13', 'note': ''})
a, b = B.line_of(" {n:'Paiwan Wisdom',cbm:null,")
B.s = B.s[:a] + " " + js({'n': 'Paiwan Wisdom', 'cbm': None, 'from': 'USA', 'c': 'Logs', 'eta': '11-28', 'etb': '12-17', 'note': 'desk 20 Nov: ETA 28 Nov (26 Nov before)'}) + B.s[b:]

# ---------------- accuracy: the call for the 20 Nov meeting is FROZEN as it stood before the meeting ----------------
B.rep("function renderMeetlog(){\n", "const CALL_FROZEN={d:'11-20',at:'11-20 10:36',basis:'DPR 20.11 · list 20.11 · programme 20.11',call:[['Aboudi D','3'],['Tai Keystone','7'],['Uni Blossom','13'],['Sea Postman','8']]}; // the call as it stood BEFORE the meeting of that day (v187 / v188). Documents that reach the board after the meeting (signal sheets, the timber desk sheet) must not improve it. Replace with the next meeting's call when that one is frozen; null = show the live call.\nfunction renderMeetlog(){\n")
B.rep("  window.__CALL={d:iso(NXM).slice(0,5),at:iso(NOW),end:iso(end),pend:PEND,call:live.map(x=>[clean(x.n),String(x.b)])};\n",
      "  const FRZ=(CALL_FROZEN&&CALL_FROZEN.d===iso(NXM).slice(0,5))?CALL_FROZEN:null;\n  window.__CALL=FRZ?{d:FRZ.d,at:FRZ.at,end:iso(end),pend:PEND,call:FRZ.call,frozen:true}:{d:iso(NXM).slice(0,5),at:iso(NOW),end:iso(end),pend:PEND,call:live.map(x=>[clean(x.n),String(x.b)])};\n")
old = "    <div class=\"mc-row\"><i>Board says these ${live.length||''} will get a berth</i>${live.length?live.map(x=>chip('',' ',clean(x.n),bl(x.b))).join(''):'<span class=\"mc-chip x\">no berth frees for a waiting vessel in this window</span>'}</div>\n    <div class=\"mc-note\">Scored when the next programme comes. The call can still change if a new DPR, list or signal reaches the board before that.</div></div>`;"
new = "    <div class=\"mc-row\"><i>${FRZ?'Board said these '+FRZ.call.length+' will get a berth':'Board says these '+(live.length||'')+' will get a berth'}</i>${FRZ?FRZ.call.map(c=>chip('',' ',c[0],bl(c[1]))).join(''):(live.length?live.map(x=>chip('',' ',clean(x.n),bl(x.b))).join(''):'<span class=\"mc-chip x\">no berth frees for a waiting vessel in this window</span>')}</div>\n    <div class=\"mc-note\">${FRZ?'Call frozen '+fmt(h(FRZ.at))+', before the meeting · '+FRZ.basis+'. What reached the board after the meeting does not change it. Scored when the programme comes.':'Scored when the next programme comes. The call can still change if a new DPR, list or signal reaches the board before that.'}</div></div>`;"
B.rep(old, new)
B.save()
