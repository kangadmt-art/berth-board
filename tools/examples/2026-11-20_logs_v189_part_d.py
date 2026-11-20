#!/usr/bin/env python3
# apply34d — v189 (part 4, logs): UPDATED, own-vessel route notes, snapshot, prediction log, own-vessel log, lesson. argv[1] = UPDATED.
import re, sys, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
B = Board(P); q = B.q
S = json.load(open(W + 'S189.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]

# Rome Trader's sailing hour is an estimate — show it as one
B.sub_entry("{b:'13',n:'Rome Trader (salt, next call)',nm:23000,p:[113,125.25]", "f:'11-18 17:00',t:'11-20 21:00',lt:'11-21 04:40'", "f:'11-18 17:00',t:'11-20 21:00',lt:'11-21 04:40',est:1")

# ================= OPTS notes =================
def note_of(label, text):
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "THE BOARD'S PICK NOW. SAAGAR group — one bulk and one break-bulk place. List 20.11: Uni Blossom (SGR 1), AG Varvara (3), Xin Hai Tong 71 (4 — project cargo), CD Glory (5), Dariya Priya (6), African Tiger (7), Flag Marina (8). Uni Blossom takes Rome Trader's place tonight (timber desk, after the meeting of 20 Nov: 23:00). AG Varvara is projected into CJ-5 by General on 21 Nov and Xin Hai Tong 71 into CJ-14 by the project / coastal place — which leaves CD Glory next for ML Egret's place. At the DPR 20.11 pace (8,070 CBM a day; norm 4,600, list ETC 28 Nov 07:30) ML Egret is through about 24 Nov, and the board counts the place from the evening of the 23rd: CJ-14 behind Xin Hai Tong 71, 23 Nov 21:26. The timber desk writes ETB 26 Nov for her. If AG Varvara does NOT berth by General she takes this place first, and CD Glory waits for Uni Blossom's — about 28 Nov.")
note_of('6.5K / 8K', "8K 8 on list 20.11 — CLOSED for now. Mihir (20 Nov 11:24): Manta Sena is the most senior vessel in 6.5K / 8K. The place (New Bliss at CJ-1, out about 21 Nov 22:20 at the DPR pace) goes to her — CJ-1 about 22 Nov 00:20 — and after her to Pioneer Fortune (8K 2), about 26 Nov. Nothing for CD Glory by this line before about 30 Nov. (The date the board showed between 11:24 and 12:52 on 20 Nov — CJ-5, 21 Nov 21:30 — stood on a note it had misread, which kept Manta Sena to CJ-1 to 4. Corrected in v189.)")
note_of('General · by seniority', "The General queue — GEN 20 on list 20.11. General berths by seniority with at most three bag vessels alongside (Mihir, 19 Nov). Safi Alfa (GEN 1) goes into CJ-4 tonight (HM signal 12:40); with DSM London at CJ-2 and Aboudi D, if she gets CJ-3, the three bag places are full, so the next General berth goes to the senior vessel that does not load bags — AG VARVARA (GEN 16): CJ-5 when Ken Ann's 24 hours end, about 21 Nov 12:30. CD Glory is the next such vessel after her — by this line alone CJ-15 about 25 Nov 11:40, against a vacant Higher-productivity place. If AG Varvara were passed over, CJ-5 on 21 Nov would be CD Glory's — she is the next vessel in line for it.")

# ================= PRED snapshot =================
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
SG = 'HM signal 20 Nov (12:40 sheet)'
fixed = [
 ['Konrad', 'sails', '20 Nov 15:15', SG + ' · RT OUT · CJ-12 → Flexi-2 (IN 17:00)'],
 ['Jag Pushpa', 'sails', '20 Nov 15:30', SG + ' · RT OUT · OJ-3 → SG Friendship (IN 15:15)'],
 ['Propel Confidence', 'sails', '20 Nov 17:00', SG + ' · RT OUT · CJ-4 → Safi Alfa'],
 ['Orchids', 'OJ-6', '20 Nov 17:30', SG + ' · IN on arrival · est'],
 ['Truong Minh Dream', 'sails', '20 Nov 18:15', SG + ' · CJ-6'],
 ['Safi Alfa', '4', '20 Nov 19:00', SG + ' · IN o/c at 23–31¾ · General, GEN 1 · est'],
 ['Jeil Crystal', 'sails', '20 Nov 19:00', SG + ' · RT OUT · OJ-2 → Hatnyanawati'],
 ['Meghna Prestige', 'sails', '20 Nov 19:39', 'list ETC (HP 42,500) — DPR 20.11 pace about 19:00'],
 ['Hatnyanawati', 'OJ-2', '20 Nov 21:00', SG + ' · IN o/c behind Jeil Crystal · est'],
 ['Rome Trader (salt, next call)', 'sails', '20 Nov 21:00', 'IMPLIED by the timber desk sheet (Uni Blossom 23:00) — est · list ETC 21 Nov 04:40 · DPR pace about 01:30'],
 ['Uni Blossom', '13', '20 Nov 23:00', 'timber desk, after the meeting of 20 Nov: "will berth 23:00 under Saagar" — the berth is the board\'s reading'],
 ['Seacon Monaco', 'sails', '21 Nov 06:37', 'DPR 20.11 pace — her list ETC (20 Nov 09:48) is past'],
 ['Ken Ann', 'sails', '21 Nov 12:30', '24-hr berth — in on the 11:00 signal of 20 Nov, alongside about 12:30 (est)'],
 ['Vishva Bandhan', 'sails', '21 Nov 17:13', 'DPR 20.11 pace — list ETC 22 Nov 14:33'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — project vessel'],
 ['Europa Graeca', 'sails', '21 Nov 21:45', 'DPR 20.11 pace · Tuna TT-1 → Blue Ionian'],
 ['New Bliss', 'sails', '21 Nov 22:21', 'DPR 20.11 pace — list ETC 22 Nov 10:05'],
 ['Nord Copper', 'sails', '22 Nov 03:03', 'list ETC at the 23,000 norm'],
 ['African Hornbill (blades, next call)', 'sails', '24 Nov 04:00', 'board estimate — no norm printed'],
 ['ML Egret', 'sails', '24 Nov 09:40', 'DPR 20.11 pace — list ETC 28 Nov 07:30 · stays at CJ-15, her shift is off'],
]
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-26 00:00']
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v189) — the two HM signal sheets of 20 Nov and the timber desk sheet applied on list 20.11 + DPR 20.11; to be read against the evening signal sheet, programme 21.11, DPR 21.11 and list 21.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a_), b_, c_, q(d_)) for a_, b_, c_, d_ in fixed + proj)) + B.s[j:]

# ================= PREDLOG =================
a0 = B.s.index("const PREDLOG=["); b0 = B.s.index("\n];", a0)
AT = '11-20 12:52'
def prow(n, note, src=''):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',%snote:'%s'}" % (q(n), AT, x['b'], x['F'], ("src:'%s'," % src) if src else '', q(note))
R = "20 Nov 12:52 re-run on the HM signal sheets of 20 Nov + the timber desk sheet (meeting held, programme 21.11 awaited) — "
new = [
 " {v:'Safi Alfa',predAt:'%s',pb:'4',pt:'11-20 19:00',ab:'',at:'',src:'prog',note:'%s'}" % (AT, q("HM signal 20 Nov 12:40 — IN o/c at 23–31¾ behind Propel Confidence (RT OUT 17:00); reading, not scored")),
 " {v:'Uni Blossom',predAt:'%s',pb:'13',pt:'11-20 23:00',ab:'',at:'',src:'prog',note:'%s'}" % (AT, q("timber desk after the meeting of 20 Nov — will berth 23:00 under Saagar; the berth (CJ-13 behind Rome Trader) is the board's reading; not scored")),
 prow('Parvraj', R + 'Govt (DAP, GP Y) — signalled IN with the berth "pending"; the board seats her at CJ-6 behind Truong Minh Dream (out 18:15)'),
 prow('Flag Marina', R + 'Higher productivity (HP 5), CJ-7 after Meghna Prestige — the Govt place of the day goes to Parvraj at CJ-6'),
 prow('AG Varvara', R + 'General (GEN 16), CJ-5 when Ken Ann\'s 24 hours end — the three bag places are full once Safi Alfa is in, and she is the senior vessel that does not load bags'),
 prow('Tai Keystone', R + 'Govt (bulk urea), CJ-8 after Vishva Bandhan'),
 prow('Belmoira', R + 'Higher productivity, CJ-15A after Heng Yuan Fa Zhan — her programmed berth (CJ-15) was not vacated: ML Egret\'s shift is off'),
 prow('Manta Sena', R + '6.5K / 8K (8K 1, most senior — Mihir), CJ-1 behind New Bliss'),
 prow('Blue Shark', R + 'General (GEN 2), CJ-15A after Belmoira — first bag place to open, when Aboudi D is out'),
 prow('CD Glory', R + 'Mihir & Co — SAAGAR (SGR 5), CJ-14 behind Xin Hai Tong 71 when ML Egret\'s place opens at the DPR pace. General line: CJ-15 about 25 Nov. 6.5K / 8K closed (Manta Sena). Timber desk after the meeting: 26 Nov. Supersedes CJ-5 21 Nov 21:30, which stood on a misread note'),
 prow('Sea Postman', R + 'General (GEN 22) only — rock phosphate is no longer given an automatic Govt rank; CJ-6 after Parvraj'),
 prow('Dariya Priya', R + 'General against a vacant HP place, CJ-15 after ML Egret'),
]
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]

# ================= MYLOG =================
g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 12:52 · HM signals 20 Nov (10:55, 12:40) + timber desk after the meeting',exp:'%s',b:'%s',slot:'SAAGAR — CJ-14 about 23 Nov night, when ML Egret\\'s place opens · General — CJ-15 about 25 Nov · 6.5K / 8K closed (Manta Sena) · timber desk after the meeting: 26 Nov',why:'" % (g['F'], g['b']) + q(
 "The board's date moves from the night of 21 Nov to the night of 23 Nov. Three things did it. (1) A BOARD ERROR: the date shown since 11:24 (CJ-5, 21 Nov 21:30 under 6.5K / 8K) stood on a note the board had misread, which kept Manta Sena to CJ-1 to 4. Corrected: she is the senior 8K vessel wherever she can lie, and the 6.5K place — CJ-1 behind New Bliss, about 22 Nov 00:20 — is hers. (2) The 12:40 signal: SAFI ALFA (GEN 1, rice bags) goes into CJ-4 tonight, the berth that had been printed for ML Egret's shift. With DSM London and Aboudi D that fills the three bag places under General, so CJ-5 (free when Ken Ann's 24 hours end, about 21 Nov 12:30) falls to the senior vessel that does not load bags — AG VARVARA, GEN 16 against CD Glory's GEN 20. (3) ML Egret is not shifted, so no clean berth is handed out early. What is left for CD Glory is the SAAGAR line: Uni Blossom takes Rome Trader's place tonight, AG Varvara berths by General, Xin Hai Tong 71 goes by the project / coastal place, and CD Glory (SGR 5) is next when ML Egret's place opens — about 24 Nov at the DPR 20.11 pace (8,070 CBM a day against the 4,600 norm), counted by the board from the evening of the 23rd: CJ-14 behind Xin Hai Tong 71, 23 Nov 21:26. The timber desk, after today's meeting, writes ETB 26 Nov for her and for AG Varvara alike. Read the two together: 23 Nov night is the early case, 26 Nov the desk's. Weak points of the early case — AG Varvara must indeed get CJ-5 by General (if not, she is ahead of CD Glory for the SAAGAR place and CD Glory waits for Uni Blossom's, about 28 Nov); ML Egret must keep her pace; Xin Hai Tong 71, a project vessel with no norm, must be out of CJ-14 by the 23rd. Laytime (arrival + 12 hours) runs out 23 Nov 01:38 in either case.") + "'}") + B.s[i:]
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); e = B.s.index("\n ]\n};", a)
B.s = B.s[:e] + (",\n  {d:'20 Nov 12:52 · timber desk after the meeting — Uni Blossom to berth 23:00 tonight',exp:'11-18 17:00',b:'13',slot:'alongside CJ-13 · SAAGAR · sailing about 20 Nov 21:00 — IMPLIED, not printed · list ETC 21 Nov 04:40 · DPR pace about 21 Nov 01:30',why:'" + q(
 "The timber desk's sheet of 20 Nov 12:00, written after the berthing meeting, has Uni Blossom berthing at 23:00 tonight under Saagar. It names no berth. Rome Trader's is the only SAAGAR place that can free tonight (ML Egret stays at CJ-15 — her shift is off), so the board reads it as CJ-13 behind Rome Trader. That needs her off the berth by about 21:00 — seven and a half hours inside her permissible time and four and a half ahead of the DPR 20.11 pace (19,631 MT left at 0700, at 25,320 a day → about 01:30). To be done by about 20:00 she has to load at roughly 36,000 a day today. Entered as an ESTIMATE: neither signal sheet of today carries her outward movement yet (they run to 19:00). The evening signal sheet or programme 21.11 will give the hour. If Uni Blossom is meant for another berth, Rome Trader stays on her list ETC.") + "'}") + B.s[e:]

# ================= LEARN =================
def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 12:52 · HM signals 20 Nov (disp 10:55 and 12:40) + timber desk sheet 20 Nov 12:00",
 "The day sheets of 20 Nov against programme 20.11 and the board. TO CONFIRM WITH MIHIR: (1) Uni Blossom \"will berth 23:00 under Saagar\" — at CJ-13 behind Rome Trader? Then Rome Trader sails about 21:00 tonight. (2) Parvraj is signalled in with the berth \"pending\" — is it CJ-6 behind Truong Minh Dream?",
 "Programme 20.11 / board v188: Katerina K into CJ-6 behind Truong Minh Dream (\"provisional berthing\") · ML Egret shifted CJ-15 → CJ-4 on the port's account about 17:30, and Belmoira into CJ-15 as GOVT(30K) · Ken Ann into CJ-5 about 19:30 · Willows into OJ-6 · Sea Postman next under Govt (bulk rock phosphate — the board's cargo rule) · Uni Blossom into CJ-13 about 21 Nov 06:40 · CD Glory CJ-5 21 Nov 21:30 under 6.5K / 8K.",
 "Signals: KEN ANN in at 11:00 behind Saga Viking (shifted to OTB) — eight hours early · KATERINA K struck out, \"cancelled by Traffic\" · SAFI ALFA (GEN 1) in at 23–31¾ — CJ-4 — behind Propel Confidence (RT OUT 17:00): the berth printed for ML Egret, whose shift is not signalled · PARVRAJ (DAP, GP Y, reported 01:56 today) in \"o/c\", berth \"PENDING\" · Truong Minh Dream out 18:15 · Orchids, not Willows, into OJ-6 · Hatnyanawati into OJ-2 behind Jeil Crystal (19:00) · Belmoira not signalled. Timber desk, after the meeting: Uni Blossom berths 23:00 tonight under Saagar; ETB AG Varvara 26 Nov, CD Glory 26 Nov, Dariya Priya 30 Nov, African Tiger 3 Dec; 43 vessels waiting.",
 "The board's reading: a \"provisional berthing\" is just that — Katerina K was pencilled into the fertiliser berth and lost it when a Govt vessel reported ready (Parvraj), so the Govt place at CJ-6 passes from Truong Minh Dream to her. The port preferred the senior General vessel (Safi Alfa, waiting since 19 Oct) to its own programmed shift of ML Egret, so Belmoira's clean berth did not open — the board's run of 19 Nov 12:29, before programme 20.11, had Safi Alfa at CJ-4 behind Propel Confidence. Sea Postman has lain ready since 17 Nov while the vacant Govt place went to a 30K quote on programme 20.11 and to Parvraj today: rock phosphate is not Govt-priority cargo in the port's hands unless the list prints GP. And the board's own date for CD Glory stood on a note it had misread (Manta Sena kept to CJ-1 to 4).",
 "v189: signals entered (Safi Alfa CJ-4, Ken Ann CJ-5, Katerina K and Belmoira back in the waiting rows, Parvraj at the fertiliser berth that frees first, oil jetties). RULES — (a) the automatic Govt rank by cargo no longer covers ROCK phosphate; (b) NO_SHIFT: a shift the port has dropped (ML Egret) is not projected again until a programme prints it; (c) the meeting call is FROZEN as it stood before the meeting, so papers that arrive after the meeting cannot improve the score; (d) Manta Sena's note reworded — a note that says \"CJ-1 to 4\" is read as a berth request. Uni Blossom is entered at CJ-13 for 23:00 and Rome Trader's sailing at about 21:00, both as estimates. CD Glory: SAAGAR line, CJ-14 about 23 Nov night (desk 26 Nov). OPEN (1) Uni Blossom's berth and Rome Trader's hour. OPEN (2) Parvraj's berth.", "open"))
B.save()
