#!/usr/bin/env python3
# apply21b — v175 (part 2): liquid / Tuna / timber rows from list 19.11 + programme 20.11, own-vessel options, snapshot, logs. argv[1] = UPDATED.
import re, sys, json, shutil
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'pre21b.html')
B = Board(P); q = B.q
S = json.load(open(W + 'S175.json')); byn = {x['n']: x for x in S}
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

# ================= LIQ =================
src = open(W + 'apply19b.py', encoding='utf-8').read()
ns = {}; exec(src[src.index("def Wt("):src.index("LM = [")], ns)   # Wt, Et, LW, LE as written for list 18.11
Wt, Et, LW, LE = ns['Wt'], ns['Et'], ns['LW'], ns['LE']
LW = [x for x in LW if x['n'] != 'Artigo']
for x in LW:
    if x['n'] == 'Silver Gertrude': x['rank'] = '1E'; x['rem'] = 'rank "1E" · PROGRAMME 20.11: OJ-7 behind NV Sunshine (out 20 Nov 01:00) — night, starboard'
    if x['n'] == 'Willows': x['rem'] = 'rank "1O" · PROGRAMME 20.11: OJ-6 behind Kestrel (out 20 Nov 11:00)'
LW += [
 Wt('Hatnyanawati', 'Chemicals', 10000, 123.5, 4.9, '11-18 07:12', None, '', 'GAC Shg', 'reported 18 Nov 07:12 · N/A · REQ OJ 2, 3, 4', 'EXP'),
 Wt('Rasheeda', 'Chemicals', 5000, 114.5, 3.8, '11-18 12:30', None, '', 'V Ocean', 'at OTB since she left OJ-2 on 18 Nov · N/A · 5,000 MT to load', 'EXP'),
 Wt('SG Friendship', 'Chemicals', 8172.93, 144.03, 7.6, '11-18 15:36', '11-19 11:00', '1C', 'Atlantic Shg', 'rank "1C" · REQ OJ 2, 3, 4 · PROGRAMME 20.11: OJ-3 behind Jag Pushpa (out 20 Nov 13:00)'),
 Wt('Eva Richway', 'Chemicals', 8627.19, 145.53, 7.36, '11-18 15:48', '11-18 15:48', '2C', 'GAC Shg', 'rank "2C"'),
 Wt('Hartati', 'Chemicals', 11000, 123.19, 5.4, '11-18 23:24', None, '', 'GAC Shg', 'reported 18 Nov 23:24 · N/A · REQ OJ 2, 3, 4', 'EXP'),
 Wt('Bow Fortitude', 'Chemicals', 10172.11, 158.93, 7.8, '11-19 06:42', '11-19 06:42', '3C', 'GAC Shg', 'rank "3C"')]
gone = {'Hatnyanawati', 'Rasheeda', 'Eva Richway', 'SG Friendship', 'Hartati', 'Bow Fortitude'}
LE = [x for x in LE if x['n'] not in gone]
for x in LE:
    if x['n'] == 'PVT Aurora': x['eta'] = '11-19 11:32'; x['rem'] = 'ETA / readiness 19 Nov 11:32 · REQ OJ 2, 3, 4'
    if x['n'] == 'Al Mahboobah': x['eta'] = '11-19 23:00'; x['q'] = 9336.42; x['rem'] = 'ETA / readiness 19 Nov 23:00 · REQ OJ 2, 3, 4'
    if x['n'] == 'Thetis Leona': x['eta'] = '11-21 07:00'; x['rem'] = ''
    if x['rem'] == 'new on list 18.11': x['rem'] = ''
LE += [
 Et('Orchids', 'VLSFO', 8000, 128.6, None, '11-20 17:00', 'Atlantic Shg', 'new on list 19.11'),
 Et('Chemroad Quest', 'Chemicals', 4956.47, 174.43, 10.13, '11-22 14:00', 'JM Baxi', 'new on list 19.11'),
 Et('Stolt Endurance', 'CPO', 29997.93, 174.38, 10.5, '11-24 00:00', 'JM Baxi', 'new on list 19.11'),
 Et('Chase Ocean', 'CDSBO', 21350, 183.2, 10.5, '11-24 00:00', 'JM Baxi', 'new on list 19.11'),
 Et('Western Carnation', 'CPO', 17500.75, 149.8, 9.4, '11-24 22:00', 'JM Baxi', 'new on list 19.11'),
 Et('Bow Saturn', 'Chemicals', 6600, 157.03, 7.1, '11-25 00:00', 'GAC Shg', 'REQ OJ 2, 3, 4 · new on list 19.11'),
 Et('Camelia', 'CPO', 10990.83, 126.5, 7.8, '11-25 04:00', 'JM Baxi', 'new on list 19.11'),
 Et('No 5 Ocean Pioneer', 'Chemicals', 5000, 145.53, None, '11-26 00:00', 'Admiral', 'new on list 19.11'),
 Et('Sundo Horn', 'Veg oil', 15000, 182.5, 8.7, '11-26 18:00', 'GAC Shg', 'OJ-07 · new on list 19.11'),
 Et('Lyng Trader', 'Chemicals', 1500, 143.02, 5, '11-28 00:00', 'GAC Shg', 'new on list 19.11')]
LE.sort(key=lambda x: x['eta'])
a = B.s.index("const LIQ={"); w0 = B.s.index(" wait:[\n", a); m0 = B.s.index(" moves:[\n", w0)
B.s = B.s[:w0] + " wait:[\n  " + ",\n  ".join(js(x) for x in LW) + "\n ],\n eta:[\n  " + ",\n  ".join(js(x) for x in LE) + "\n ],\n" + B.s[m0:]
def nxt(n, c, qv, loa, f, ag, note, rank=''): return {'n': n, 'c': c, 'q': qv, 'u': 'MT', 'ie': 'IMP', 'loa': loa, 'f': f, 'est': 1, 'rank': rank, 'ag': ag, 'note': note}
def berth_tail(bid, out, outBy, nx):
    global B
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]
    tail = "," if ln.endswith("}},") else ""
    if not (ln.endswith("}},") or ln.endswith("}}")): B.die(bid + ' line does not end with }}')
    core = ln[:-1] if tail else ln
    B.s = B.s[:a] + core[:-1] + ",out:" + js(out) + ",outBy:" + js(outBy) + ",next:" + js(nx) + "}" + tail + B.s[b:]
berth_tail('OJ-3', '11-20 13:00', 'programme 20.11: outward readiness 20 Nov 13:00 (8.2 m) · list 19.11: ETC 20 Nov 08:34',
           nxt('SG Friendship', 'Chemicals', 8172.93, 144.03, '11-20 15:00', 'Atlantic Shg', 'programme 20.11: OJ-03 behind Jag Pushpa — about 15:00, the board\'s estimate · list 19.11: chemicals 8,173 MT IMP, 7.6 m, reported 18 Nov 15:36, ready 19 Nov 11:00, rank "1C"', '1C'))
berth_tail('OJ-6', '11-20 11:00', 'programme 20.11: outward readiness 20 Nov 11:00 (10.0 m)',
           nxt('Willows', 'MS', 28000, 179.88, '11-20 13:00', 'Atlantic Shg', 'programme 20.11: OJ-06 behind Kestrel — about 13:00, the board\'s estimate · list 19.11: MS 28,000 MT IMP, 9.1 m, ready 18 Nov 11:00, rank "1O"', '1O'))
berth_tail('OJ-7', '11-20 01:00', 'programme 20.11: outward readiness 20 Nov 01:00 (8.5 m), NIGHT SAILING · list 19.11: norm 500 MT/h, ETC 21 Nov 02:30',
           nxt('Silver Gertrude', 'CDSBO', 22500, 183.06, '11-20 03:00', 'Interocean', 'programme 20.11: OJ-07 behind NV Sunshine, NIGHT, STARBOARD — about 03:00, the board\'s estimate · list 19.11: CDSBO 22,500 MT IMP, 12.9 m, commercially ready 15 Nov, rank "1E"', '1E'))
B.rep("asOf:'11-19 12:29',\n berths:[", "asOf:'11-19 16:12',\n berths:[")
B.rep("const LIQ={src:'DPA berthing list 18.11.26 (0700, revised) · programme 19.11 and 18.11 (TF/SH/2102)", "const LIQ={src:'DPA berthing list 19.11.26 (0700) · programme 20.11, 19.11 and 18.11 (TF/SH/2102)")
LMN = ['Programme for 20.11 — TF/SH/2102 (dated 19 Nov) — oil-jetty rows', [
  ['01:00', 'OUT', 'NV Sunshine (LPG/C)', 'OJ-7 → OTB', '—', '11-20 01:00', 'NIGHT SAILING · 8.5 m → Silver Gertrude, NIGHT, STARBOARD'],
  ['11:00', 'OUT', 'Kestrel', 'OJ-6 → OTB', '—', '11-20 11:00', '10.0 m → Willows'],
  ['13:00', 'OUT', 'Jag Pushpa', 'OJ-3 → OTB', '—', '11-20 13:00', '8.2 m → SG Friendship']]]
a = B.s.index("const LIQ={"); m0 = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:m0] + "  " + js(LMN) + ",\n" + B.s[m0:]
# ================= TUNA =================
B.rep("next:'Marvelous Star (coal 50,000 MT, ready 15 Nov 13:18, \"TT-03\") waits behind'", "next:'Marvelous Star (coal 50,000 MT) — PROGRAMME 20.11: she berths behind Beagle tonight, NIGHT BERTHING'")
B.rep("note:'DPR 17.11: MADE FAST 19:42, commenced 22:50 on 16 Nov (board est 14:30).", "note:'PROGRAMME 20.11: TT-03 · outward readiness 19 Nov 20:00 (7.5 m), NIGHT SAILING → Marvelous Star. DPR 17.11: MADE FAST 19:42, commenced 22:50 on 16 Nov (board est 14:30).")
B.rep("rem:'TT-03 · reported / ready 15 Nov 13:18 — behind Beagle (about 19 Nov evening at the DPR pace)'", "rem:'TT-03 · reported / ready 15 Nov 13:18 — PROGRAMME 20.11: berths tonight behind Beagle (out 19 Nov 20:00)'")
B.rep("const TUNA={src:'DPA berthing list 18.11.26 (0700, revised) · DPR 19.11, 18.11 and 17.11 — no Tuna row on programme 18.11 or 19.11, none on the signal sheets", "const TUNA={src:'DPA berthing list 19.11.26 (0700) · programme 20.11 (TT-03: Beagle out, Marvelous Star in) · DPR 19.11")
# ================= TIMBER =================
def T(pfx, d): B.set_line(pfx, " " + js(d) + ",")
T(" {n:'ML Egret',cbm:42886,", {'n': 'ML Egret', 'cbm': 42886, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-06 14:24', 'etb': '11-18', 'comm': '11-18 23:35',
   'note': 'berthed 18 Nov 21:45 at CJ-15 under SAAGAR · list 19.11: norm 4,600 CBM, ETC 28 Nov 07:30 · PROGRAMME 20.11: SHIFTED to CJ-4 (23–31¾) on 20 Nov on the port\'s account, to give CJ-15 to a salt vessel · 12.11 m'})
T(" {n:'Uni Blossom',cbm:34870,", {'n': 'Uni Blossom', 'cbm': 34870, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-09 11:36', 'etb': '11-19',
   'note': 'SGR 1 · 8K 3 · GEN 9 on list 19.11 — next for a SAAGAR place when Rome Trader is through (list ETC 20 Nov 22:01) · the desk had 19 Nov · 10.8 m'})
T(" {n:'AG Varvara',cbm:39113,", {'n': 'AG Varvara', 'cbm': 39113, 'from': 'Australia', 'c': 'Pine logs', 'eta': '11-12 07:06', 'etb': '11-24', 'note': 'SGR 3 · GEN 16 on list 19.11 · 199.99 m, 9.0 m'})
T(" {n:'CD Glory',cbm:29158,", {'n': 'CD Glory', 'cbm': 29158, 'from': 'Malaysia', 'c': 'Hardwood logs', 'eta': '11-15 06:42', 'etb': '11-25',
   'note': 'list 19.11: SGR 5 · 8K 8 · GEN 20 · 179.9 m, 10.4 m — fits CJ-1, CJ-4, CJ-5; CJ-4 goes to ML Egret on 20 Nov'})
T(" {n:'Dariya Priya',cbm:44968,", {'n': 'Dariya Priya', 'cbm': 44968, 'from': 'New Zealand', 'c': 'Pine logs', 'eta': '11-16 09:00', 'etb': '11-29',
   'note': '"Darya Priya" on the desk sheet · list 19.11: SGR 6 · 8K 10 · GEN 21 · 11.0 m'})
T(" {n:'African Tiger',cbm:36328,", {'n': 'African Tiger', 'cbm': 36328, 'from': 'Uruguay', 'c': 'Pine logs', 'eta': '11-18 06:30', 'etb': '12-03',
   'note': 'list 19.11: ranked now — SGR 7 · 8K 12 · GEN 27 · reported 18 Nov 06:30 · 180 m, 10.8 m'})
# ================= OPTS notes =================
def note_of(label, text):
    global B
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "SAAGAR group — one bulk and one break-bulk place. List 19.11: Uni Blossom (SGR 1), African Hornbill (2 — windmill blades, a project parcel), AG Varvara (3), Xin Hai Tong 71 (4 — project cargo), CD Glory (5). Rome Trader's place frees at her ETC (20 Nov 22:01) and goes to Uni Blossom — no bulk vessel that is ready is ranked ahead. ML Egret keeps the log place: programme 20.11 moves her to CJ-4, list ETC 28 Nov 07:30. The board expects the three vessels between Uni Blossom and CD Glory to berth by other lines by about 21 Nov, so the place ML Egret leaves comes to CD Glory — about 28 Nov, at CJ-4.")
note_of('6.5K / 8K', "8K 8 on list 19.11. One place: New Bliss has it at CJ-1 till about 22 Nov (list ETC 22 Nov 10:05). Ahead of her: Crystal Land (8K 1 — needs a clean berth), PIONEER FORTUNE (8K 2 — back on the waiting list; sugar bags, 169 m, CJ-1 suits her), Uni Blossom (3 — SAAGAR takes her first), Tan Bin 259 (4 — finishing at the mooring), Gokova-M (5 — clay, CJ-7 / CJ-8 only), Porto Fiscardo (6); Nord Copper (7) berths under Coastal on the night of the 19th. At least two turns of this place pass before hers — the end of the month by this line.")
note_of('General · by seniority', "The General queue — GEN 20 on list 19.11. The board seats her at CJ-1 when New Bliss leaves (about 22 Nov) for two reasons, and both are weak: it expects the 6.5K place to go to Crystal Land at a clean berth first, so that CJ-1 falls to General; and it holds back the bag vessels senior to her — Safi Alfa (GEN 1), Pioneer Fortune (GEN 6, also 8K 2) — by a limit of three bag vessels at a time under General, which the port has not confirmed. If CJ-1 is given to Pioneer Fortune under 6.5K, this date falls away. CJ-4 is closed to her now (ML Egret is moved there on the 20th); CJ-5 frees again on the evening of the 21st (Ken Ann, 24 hours) and AG Varvara (GEN 16) is senior for it. For three days running the port has not put a General vessel on a free berth where the board did. The timber desk says 25 Nov.")

# ================= PRED snapshot =================
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
PGs = 'programme 20.11'
fixed = [
 ['Beagle', 'sails', '19 Nov 20:00', PGs + ' · Tuna TT-3, night sailing → Marvelous Star'],
 ['Bristol (salt, next call)', 'sails', '19 Nov 20:30', 'signal 19 Nov: RT OUT 20:30'],
 ['Heng Yuan Fa Zhan', '15A', '19 Nov 21:30', 'signal 19 Nov: IN 18:45, alongside once Bristol is out · est'],
 ['HN Doris (salt, next call)', 'sails', '19 Nov 22:00', 'signal 19 Nov: RT OUT o/c · est'],
 ['Yara J', 'sails', '19 Nov 23:30', PGs + ' · night sailing'],
 ['Ocean Kudos', '16', '20 Nov 00:30', 'signal 19 Nov: IN o/c after HN Doris · HP(42.5K) · est'],
 ['NV Sunshine (LPG/C)', 'sails', '20 Nov 01:00', PGs + ' · OJ-7 → Silver Gertrude'],
 ['Nord Copper', '14', '20 Nov 01:30', PGs + ' · CSTL, night berthing after Yara J · est'],
 ['Sea Gautham', 'sails', '20 Nov 08:00', PGs],
 ['Kestrel', 'sails', '20 Nov 11:00', PGs + ' · OJ-6 → Willows'],
 ['Jag Pushpa', 'sails', '20 Nov 13:00', PGs + ' · OJ-3 → SG Friendship'],
 ['Propel Confidence', 'sails', '20 Nov 15:00', PGs + ' — list ETC 11:47'],
 ['ML Egret', '4', '20 Nov 17:30', PGs + ' · SHIFT from CJ-15, port account · est'],
 ['Saga Viking', 'sails', '20 Nov 17:30', PGs + ' · shifts to OTB at her agent\'s request'],
 ['Truong Minh Dream', 'sails', '20 Nov 17:45', PGs],
 ['Belmoira', '15', '20 Nov 18:30', PGs + ' · GOVT(30K), after ML Egret is moved · est'],
 ['Ken Ann', '5', '20 Nov 19:30', PGs + ' · 24HRS, after Saga Viking · est'],
 ['Meghna Prestige', 'sails', '20 Nov 19:39', 'list ETC (HP 42,500)'],
 ['Katerina K', '6', '20 Nov 19:45', PGs + ' · provisional berthing, after Truong Minh Dream · est'],
 ['Rome Trader (salt, next call)', 'sails', '20 Nov 22:01', 'list ETC at the 26,000 norm — her first-night pace points to 21 Nov 09:30'],
 ['Vishva Bandhan', 'sails', '21 Nov 08:34', 'DPR 19.11 pace — list ETC 22 Nov 14:33'],
 ['Ocean Kudos', 'sails', '21 Nov 18:00', 'board estimate — 70,190 MT at the 42,500 quote'],
 ['Ken Ann', 'sails', '21 Nov 19:30', '24-hr berth'],
 ['Nord Copper', 'sails', '21 Nov 21:00', 'board estimate — no norm printed'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — project vessel, two days'],
 ['New Bliss', 'sails', '22 Nov 03:05', 'DPR 19.11 pace — list ETC 22 Nov 10:05'],
 ['Belmoira', 'sails', '22 Nov 19:00', 'board estimate — 58,300 MT at 30,000 a day'],
]
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-25 12:00']
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v175) — list 19.11 + programme 20.11 applied; to be read against the evening sheet of 19 Nov, DPR 20.11, list 20.11 and programme 21.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a), b, c, q(d)) for a, b, c, d in fixed + proj)) + B.s[j:]

# ================= PREDLOG =================
AT = '11-19 16:12'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
def grow(n, pb, pt, note): return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',src:'prog',note:'%s'}" % (q(n), AT, pb, pt, q(note))
R = "19 Nov 16:12 re-run on list 19.11 + programme 20.11 — "
new = [
 grow('Nord Copper', '14', '11-20 01:30', 'programme 20.11 — CSTL, 126½–141¾, night berthing behind Yara J (23:30); reading, not scored'),
 grow('Belmoira', '15', '11-20 18:30', 'programme 20.11 — GOVT(30K), 143½–156¾, after ML Egret is shifted to CJ-4; reading, not scored'),
 grow('Ken Ann', '5', '11-20 19:30', 'programme 20.11 — 24HRS, 33½–41½, behind Saga Viking (17:30); reading, not scored'),
 grow('Katerina K', '6', '11-20 19:45', 'programme 20.11 — provisional berthing, 42½–51¼, behind Truong Minh Dream (17:45); reading, not scored'),
 prow('Aboudi D', R + 'General, CJ-3 once the programme window is over — Sea Gautham leaves at 08:00 and nobody is named behind her'),
 prow('Tai Keystone', R + 'Govt (bulk urea), CJ-7 after Meghna Prestige — if she reports as declared (20 Nov 12:00)'),
 prow('Uni Blossom', R + 'SAAGAR (SGR 1), CJ-13 when Rome Trader is through — on her list ETC, 20 Nov 22:01'),
 prow('Sea Postman', R + 'Govt (rock phosphate in bulk), CJ-8 after Vishva Bandhan'),
 prow('Crystal Land', R + '6.5K / 8K (8K 1), CJ-16 after Ocean Kudos — she needs a clean berth'),
 prow('AG Varvara', R + 'General, CJ-5 after Ken Ann\'s 24 hours — a weak pick'),
 prow('African Hornbill (blades, next call)', R + 'SAAGAR project parcel against the Coastal place, CJ-14 after Nord Copper'),
 prow('Xin Hai Tong 71', R + 'General against a vacant HP place, CJ-15A after Heng Yuan Fa Zhan'),
 prow('CD Glory', R + 'Mihir & Co — General, CJ-1 when New Bliss leaves; a WEAK pick: Pioneer Fortune (8K 2, GEN 6) and Safi Alfa (GEN 1) are senior for CJ-1 and are held back only by the unconfirmed limit of three bag vessels. SAAGAR line ~28 Nov (CJ-4 after ML Egret); 6.5K line end of the month; desk 25 Nov'),
 prow('Dariya Priya', R + 'General, CJ-15 after Belmoira'),
 prow('Safi Alfa', R + 'General against a vacant HP place, CJ-15A after Xin Hai Tong 71'),
]
a0 = B.s.index("const PREDLOG=["); b0 = B.s.index("\n];", a0)
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]

# ================= MYLOG =================
g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'19 Nov 16:12 · list 19.11 + programme 20.11',exp:'%s',b:'%s',slot:'General — CJ-1 when New Bliss leaves · a WEAK date · SAAGAR line ~28 Nov at CJ-4 · 6.5K line end of the month · desk 25 Nov',why:'" % (g['F'], g['b']) + q(
 "List 19.11: SGR 5 · 8K 8 · GEN 20. The date on the board has not moved (22 Nov, CJ-1) but it stands on weaker ground. (1) Pioneer Fortune is back on the waiting list as 8K 2 and GEN 6 — she never took the GFPL berth — and CJ-1 suits her; Safi Alfa is GEN 1. The board gives CJ-1 to CD Glory only because it expects the 6.5K place to go to Crystal Land (8K 1) at a clean berth, and because it holds the senior bag vessels back by a limit of three bag vessels under General — a rule not confirmed by the port. (2) Programme 20.11 takes two of her three berths out of play: ML Egret is moved to CJ-4 on the port's account (till about 28 Nov), and CJ-5 goes to the 24-hr vessel Ken Ann, then on the board to AG Varvara (GEN 16). (3) By the SAAGAR line her turn is the place ML Egret leaves — about 28 Nov at CJ-4; by 6.5K, the end of the month. So: 22 Nov only if CJ-1 really falls to General; otherwise 25 Nov (desk) to 28 Nov. Laytime ends 23 Nov 01:38 — on anything later than the 22nd she berths already on demurrage.") + "'}") + B.s[i:]
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); e = B.s.index("\n ]\n};", a)
B.s = B.s[:e] + (",\n  {d:'19 Nov 16:12 · list 19.11 — norm and ETC printed',exp:'11-18 17:00',b:'13',slot:'alongside CJ-13 · SAAGAR · norm 26,000 · list ETC 20 Nov 22:01',why:'" + q(
 "List 19.11 prints her under SAAGAR at CJ-13 with NORM 26,000 MT a day and ETC 20 Nov 22:01 (55,275 MT from commencement 18 Nov 19:25). Her first night ran at about 21,400 MT a day (DPR 19.11: 10,324 MT in 11½ h on two shifts of 4 gangs; 44,951 left at 0700 on the 19th) — at that rate she is through about 21 Nov 09:30, some 11 h past the permissible time; to make 22:01 on the 20th she needs about 27,700 MT a day from 0700 on the 19th. Programme 20.11 has no outward row for her — the ETC falls after its window — and names nobody for CJ-13; on the board Uni Blossom (SGR 1) follows her there.") + "'}") + B.s[e:]

# ================= LEARN =================
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("19 Nov 16:12 · list 19.11 + programme 20.11",
 "Programme 20.11 against the board (run of 19 Nov 13:10). TO CONFIRM WITH MIHIR: is there really a limit of three bag vessels at a time under General? CD Glory's 22 Nov at CJ-1 depends on it — without the limit, Safi Alfa (GEN 1) or Pioneer Fortune (GEN 6, 8K 2) takes CJ-1 before her.",
 "Board: Ken Ann CJ-14 19 Nov 22:30 (24 hrs) · AG Varvara CJ-5 20 Nov 06:49 (General) · Safi Alfa CJ-4 20 Nov 13:47 (General) · Gokova-M CJ-7 20 Nov 21:30 (Sr No 7 quote in a Govt place) · Nord Copper CJ-16 21 Nov 20:00 · Belmoira CJ-16 23 Nov · Katerina K CJ-7 26 Nov. Pioneer Fortune taken as berthed at the GFPL berth.",
 "Port: Nord Copper CJ-14 on the night of the 19th (CSTL) · ML Egret shifted CJ-15 → CJ-4 on the port's account · Belmoira CJ-15 (GOVT(30K)) · Ken Ann CJ-5 (24HRS) after Saga Viking leaves at her agent's request · Katerina K CJ-6 (provisional berthing) · nobody named for CJ-3. List 19.11: Pioneer Fortune back on the waiting list (8K 2, GEN 6); Rome Trader norm 26,000, ETC 20 Nov 22:01; ML Egret norm 4,600, ETC 28 Nov 07:30.",
 "The board's mechanism — a Sr No 7 quote vessel in a vacant Govt place — is what the port used, but for Belmoira at a clean berth made by shifting a log vessel, not for Gokova-M at CJ-7. The 24-hr place went to Ken Ann as the board said, at CJ-5 instead of CJ-14; CJ-14 went to the Coastal-ranked salt vessel. Both General picks (AG Varvara, Safi Alfa) again did not happen — the third day running the port has not put a General vessel on a free berth where the board did.",
 "v175: programme rows entered; Pioneer Fortune restored to the waiting list; Belmoira off the passed-over list; Rome Trader and ML Egret on their printed norms and ETCs. No rule changed. The board's General picks — CD Glory's 22 Nov included — are marked weak until the bag-vessel limit is confirmed.", "open"))
B.save()
