#!/usr/bin/env python3
# apply19c — v173 (part 3): UPDATED, PRED snapshot, PREDLOG (actuals + new rows), MYLOG, LEARN. argv[1] = UPDATED string.
import re, sys, json, shutil
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'pre19c.html')
B = Board(P); q = B.q
S = json.load(open(W + 'S173.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CL = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CL.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')

m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]

# ================= PRED snapshot =================
fixed = [
 ['Avyaan', 'sails', '19 Nov 15:00', 'signal 19 Nov: OUT 15:00 (Capt Karan) · OJ-4'],
 ['Beagle', 'sails', '19 Nov 19:45', 'DPR 19.11 pace · Tuna TT-3 — no sailing on any sheet in hand'],
 ['Bristol (salt, next call)', 'sails', '19 Nov 20:30', 'signal 19 Nov: RT OUT 20:30 (Capt Yadav)'],
 ['Yara J', 'sails', '19 Nov 20:30', '24-hr berth — 24 h from her berthing; no outward row yet, about 6,500 MT will still be on board'],
 ['Heng Yuan Fa Zhan', '15A', '19 Nov 21:30', 'signal 19 Nov: IN 18:45 → 161¾–169, alongside once Bristol is out · est'],
 ['HN Doris (salt, next call)', 'sails', '19 Nov 22:00', 'signal 19 Nov: RT OUT o/c after Heng Yuan Fa Zhan is berthed · est'],
 ['Ocean Kudos', '16', '20 Nov 00:30', 'signal 19 Nov: IN o/c after HN Doris → 171½–188 · HP(42.5K) · est'],
 ['Saga Viking', 'sails', '20 Nov 04:49', 'DPR 19.11 pace — list ETC 21 Nov 18:58'],
 ['Truong Minh Dream', 'sails', '20 Nov 07:02', 'DPR 19.11 pace — list ETC 19 Nov 13:46, no outward row for the 19th'],
 ['Seacon Monaco', 'sails', '20 Nov 09:48', 'list ETC — her first-day pace points to 21 Nov 08:00'],
 ['Propel Confidence', 'sails', '20 Nov 11:47', 'list ETC — DPR 19.11 pace 20 Nov 15:30'],
 ['Meghna Prestige', 'sails', '20 Nov 19:30', 'board estimate — 60,500 MT at the 42,500 quote'],
 ['Sea Gautham', 'sails', '21 Nov 05:40', 'board estimate — no norm or ETC printed'],
 ['Vishva Bandhan', 'sails', '21 Nov 08:34', 'DPR 19.11 pace — list ETC 22 Nov 14:33'],
 ['Rome Trader (salt, next call)', 'sails', '21 Nov 09:30', 'board estimate — her first-night pace, about 21,400 MT a day; no norm or ETC printed yet'],
 ['Ocean Kudos', 'sails', '21 Nov 18:00', 'board estimate — 70,190 MT at the 42,500 quote'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — project vessel, two days'],
 ['New Bliss', 'sails', '22 Nov 03:05', 'DPR 19.11 pace — list ETC 22 Nov 10:05'],
]
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-25 12:00']
rows = fixed + proj
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v173) — list 18.11 (revised) + DPR 19.11 + programme 19.11 + day signal 19 Nov applied; to be read against list 19.11 / 20.11, DPR 20.11, programme 20.11 and the evening sheet of 19 Nov\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a), b, c, q(d)) for a, b, c, d in rows)) + B.s[j:]

# ================= PREDLOG — actuals =================
ACT = {'Phoenix Coral': ('4', '11-17 00:06'), 'New Bliss': ('1', '11-17 02:33'), 'Saga Viking': ('5', '11-17 01:24'), 'Honor Star': ('9', '11-17 08:00'), 'Vishva Bandhan': ('8', '11-17 18:30'),
       'Propel Confidence': ('7', '11-17 19:30'), 'Bristol (salt, next call)': ('15A', '11-17 21:30'), 'HN Doris (salt, next call)': ('16', '11-17 21:12'), 'Rome Trader (salt, next call)': ('13', '11-18 17:00'),
       'Yara J': ('14', '11-18 20:30'), 'ML Egret': ('15', '11-18 21:45'), 'Meghna Prestige': ('7', '11-19 07:30'), 'Sea Gautham': ('3', '11-19 05:40')}
a0 = B.s.index("const PREDLOG=["); b0 = B.s.index("\n];", a0); blk = B.s[a0:b0]; nfill = 0
for n, (ab, at) in ACT.items():
    rx = re.compile(r"(\{v:'" + re.escape(q(n)) + r"',predAt:'[^']*',pb:(?:null|'[^']*'),pt:(?:null|'[^']*'),)ab:'[^']*',at:''")
    blk, k = rx.subn(lambda m: m.group(1) + "ab:'%s',at:'%s'" % (ab, at), blk); nfill += k
    if not k: print('no open PREDLOG row for', n)
print('PREDLOG rows filled:', nfill)
AT = '11-19 12:29'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
def grow(n, pb, pt, note): return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',src:'prog',note:'%s'}" % (q(n), AT, pb, pt, q(note))
R = "19 Nov 12:29 re-run on list 18.11 + DPR 19.11 + programme 19.11 — "
new = [
 " {v:'Seacon Monaco',predAt:'11-16 18:17',pb:null,pt:null,ab:'9',at:'11-18 06:36',note:'not projected — she waited for the GFPL berth CJ-9 (remark \"10K CJ-09\"), which the board does not allot; berthed behind Honor Star'}",
 grow('DSM London', '2', '11-19 12:30', 'programme 19.11 + signal 19 Nov — BIT(GEN), 8½–16½, IN o/c after North Gate (10:00); reading, not scored'),
 grow('Heng Yuan Fa Zhan', '15A', '11-19 21:30', 'programme 19.11 + signal 19 Nov — PROJ, 161¾–169, IN 18:45, alongside once Bristol is out (20:30); reading, not scored'),
 grow('Ocean Kudos', '16', '11-20 00:30', 'programme 19.11 + signal 19 Nov — HP(42.5K), 171½–188, IN o/c after HN Doris; reading, not scored'),
 prow('Ken Ann', R + '24 hrs (24H 3), CJ-14 when Yara J\'s 24 hours are up — if Yara J is not given more time'),
 prow('AG Varvara', R + 'General, CJ-5 after Saga Viking (DPR pace) — a soft pick; CD Glory is next in line for the same berth'),
 prow('Safi Alfa', R + 'General (GEN 2), CJ-4 after Propel Confidence'),
 prow('Gokova-M', R + 'Sr No 7 quote against a vacant Govt place, CJ-7 after Meghna Prestige — she has been passed for HP three times'),
 prow('African Hornbill (blades, next call)', R + 'SAAGAR project parcel against the Coastal slot, CJ-14 after Ken Ann'),
 prow('Aboudi D', R + 'General, CJ-3 after Sea Gautham (2 shore cranes → CJ-2 / CJ-3)'),
 prow('Sea Postman', R + 'Govt (rock phosphate in bulk), CJ-6 after Truong Minh Dream'),
 prow('Tai Keystone', R + 'Govt (bulk urea), CJ-8 after Vishva Bandhan — if she reports as declared (20 Nov)'),
 prow('Uni Blossom', R + 'SAAGAR (SGR 1), CJ-13 when Rome Trader is through — no bulk vessel is ranked in SAAGAR now'),
 prow('Nord Copper', R + 'Sr No 7 quote against the 24-hr place, CJ-16 after Ocean Kudos'),
 prow('Crystal Land', R + '6.5K / 8K (8K 1), CJ-15A after Heng Yuan Fa Zhan — she needs a clean berth'),
 prow('CD Glory', R + 'Mihir & Co — General, CJ-1 when New Bliss leaves (DPR pace 22 Nov 03:05; list ETC 22 Nov 10:05); a soft pick — 8K 8 is printed now, but the 6.5K place goes to Crystal Land first; SAAGAR line end of the month; desk 25 Nov'),
 prow('Lila Tokyo', R + 'Higher productivity (HP 5), CJ-7 after Gokova-M — if she quotes at the level of the day'),
 prow('Belmoira', R + 'Sr No 7 quote against the 24-hr place, CJ-16 after Nord Copper — passed for HP on 18 Nov'),
 prow('Katerina K', R + 'General (GEN 8), CJ-7 after Lila Tokyo'),
]
blk = blk + ",\n" + ",\n".join(new)
B.s = B.s[:a0] + blk + B.s[b0:]

# ================= MYLOG =================
g = byn['CD Glory']
B.rep("\n ],\n 'African Quail':[",
 ",\n  {d:'19 Nov 12:29 · DPR 17.11 — completed and sailed',exp:'11-17 01:40',b:'1',slot:'COMPLETED 16 Nov 20:00 · left CJ-1 17 Nov 01:40',why:'" + q(
 "DPR 17.11: completed 20:00 on 16 Nov, let go 01:40 on the 17th (the re-issued night sheet had her OUT at 01:00; programme 17.11 had 07:00). 26,111 CBM in 3 d 4½ h from commencement — about 8,200 CBM a day against the 6,500 norm, 20 h inside the list ETC (17 Nov 16:24). The board's DPR-pace figure was 17 Nov 01:15; she was done five hours sooner. Laytime had ended 12 Nov 15:40 (NOR 5 Nov 15:00 + 12 free hours; 26,112 CBM ÷ 4,000 a day), so demurrage ran 4.2 days to completion — about USD 83,600. Her row is now in the completed record on the Timber tab.") + "'}\n ],\n 'African Quail':[")
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={"))
CDG = (",\n  {d:'19 Nov 12:29 · list 18.11 + DPR 19.11 + programme 19.11',exp:'%s',b:'%s',slot:'General — CJ-1 when New Bliss leaves, a soft date · 6.5K / 8K: now printed, 8K 8 · SAAGAR line end of the month · desk 25 Nov',why:'" % (g['F'], g['b']) + q(
 "Her date on the board stays 22 Nov, but the berth changes from CJ-5 to CJ-1. (1) THE 6.5K / 8K RANK IS PRINTED NOW — 8K 8, on the sheet revised after the 18 Nov meeting; she is SGR 5 and GEN 22 as well. (2) The 6.5K place: New Bliss holds it at CJ-1 till about 22 Nov (list ETC 22 Nov 10:05; DPR pace 03:00). Crystal Land (8K 1) is ahead and needs a clean berth — the board expects her to be given CJ-15A on the night of the 21st, which uses up the 6.5K place for about five days. (3) CJ-1 itself then falls to the General queue, and few vessels ahead of her can use it — bag vessels are stopped by the limit of three at a time, deep loaders cannot lie there — so the board seats CD Glory at CJ-1 on the morning of the 22nd. A soft date: Porto Fiscardo (8K 6, rice bags, asks for CJ-1 to 4) or any priority vessel given CJ-1 pushes her to the next turn, about 26–27 Nov; the SAAGAR line reaches her only at the end of the month (Uni Blossom, AG Varvara and two project parcels are ahead; ML Egret took the log place on the 18th). CJ-5, where the board had her before, frees about 20 Nov and AG Varvara (GEN 17) is senior for it. Laytime: NOR 15 Nov 06:42 + 12 free hours → 29,158 CBM ÷ 4,000 = 7.3 days → ends 23 Nov 01:38; berthing on the morning of the 22nd leaves her under a day of laytime to work in.") + "'}")
i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + CDG + B.s[i:]
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); e = B.s.index("\n ]\n};", a)
RT = (",\n  {d:'19 Nov 12:29 · BERTHED — CJ-13, 18 Nov 17:00, under SAAGAR',exp:'11-18 17:00',b:'13',slot:'alongside CJ-13 · SAAGAR bulk place · loading — about 21 Nov 09:30 at the first-night pace',why:'" + q(
 "DPR 19.11: MADE FAST 17:00, COMMENCED 19:25 on 18 Nov at CJ-13 (113–125¼), behind African Peacock, who completed 12:00 and left 14:45 — a day ahead of her list ETC. List 18.11 has her under SAAGAR with the remark \"SGR- NEELKANTH\"; programme 18.11 had named CJ-15 after Enishi, and the 18 Nov signal moved her to CJ-13, which freed first. The board (16 Nov) had CJ-13 on 19 Nov 00:31 by the same route — the SAAGAR bulk place — so the berth and the slot were right and she came 7½ h sooner. She waited 4 d 1 h from reporting (14 Nov 16:00). No HP place was taken: both went by quote again. Loading: 10,324 MT by 0700 on the 19th, the first 11½ h, on two shifts of 4 gangs — about 21,400 MT a day; 44,951 MT left → about 21 Nov 09:30 at that rate. No norm or ETC is printed for her yet; the next list will give the permissible time.") + "'}")
B.s = B.s[:e] + RT + B.s[e:]

# ================= LEARN =================
def LE(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
LA = LE("19 Nov 12:29 · lists 17.11 / 18.11, DPR 17–19.11, programmes 18.11 / 19.11, four signal sheets",
 "Three days against the board (run of 16 Nov 19:15). ROME TRADER berthed 18 Nov 17:00 at CJ-13 under SAAGAR and ML EGRET 18 Nov 21:45 at CJ-15 — the two SAAGAR places went one to the bulk vessel, one to the log vessel, as the 14 Nov rule said and not as the desk sheet had it (ML Egret and Uni Blossom). The General berthings the board expected at CJ-14 and CJ-4 did not happen; both HP places again went by quote.",
 "Board (v172): Rome Trader CJ-13 19 Nov 00:31 (SAAGAR bulk) · ML Egret CJ-15 19 Nov 03:56 · Safi Alfa CJ-14 17 Nov 20:00 · AG Varvara CJ-4 18 Nov 08:30 · Yara J CJ-2 18 Nov 13:05 (Bitumen slot as General) · Heng Yuan Fa Zhan CJ-15A 19 Nov 10:00 · Aboudi D CJ-3 19 Nov 14:00 · Meghna Prestige CJ-16 19 Nov 17:00 (HP) · Gokova-M CJ-7 19 Nov 22:00 (HP).",
 "Port: Rome Trader CJ-13 18 Nov 17:00 (SGR) · ML Egret CJ-15 18 Nov 21:45 (SGR) · Yara J CJ-14 18 Nov 20:30 (24 HRS — she was given 24H 1 at the 17 Nov meeting) · Seacon Monaco CJ-9 18 Nov 06:36 (GFPL) · Sea Gautham CJ-3 19 Nov 05:40 (space a/c) · Meghna Prestige CJ-7 19 Nov 07:30 (HP at 42,500, after Propel Confidence was shifted to CJ-4 on the port's account) · DSM London CJ-2 on the 19th (BIT(GEN)) · Heng Yuan Fa Zhan CJ-15A and Ocean Kudos CJ-16 (HP at 42,500) on the night of the 19th. Not berthed: Safi Alfa, AG Varvara, Aboudi D, Gokova-M. Evangelia D was taken off CJ-16 on 17 Nov with 7,716 MT still to load when her HP time was over.",
 "Right: the SAAGAR pair — berth and slot, each a few hours early because the two log vessels finished about a day inside their ETCs — and Heng Yuan Fa Zhan at CJ-15A behind Bristol. Wrong: (1) CJ-14 lay idle 9 h after Theometor and went to the 24-hr vessel; CJ-4 lay empty 37 h after Phoenix Coral until Propel Confidence was moved into it — the port did not put a General vessel on either, though Safi Alfa (GEN 2) and AG Varvara were ready; (2) the bag vessel for the Bitumen slot was DSM London (GEN 1, ready from 16 Nov), not Yara J; (3) HP went to Meghna Prestige (HP 3) and Ocean Kudos (unranked, arrived the day before) at 42,500 — past Gokova-M (HP 1) a third time; (4) the HP berth is taken back when the quoted time ends, finished or not.",
 "v173: no slot rule is changed — the SAAGAR bulk / break-bulk reading stands. Gokova-M and Belmoira are entered as passed over for HP (the 16 Nov rule); Stalo is held, she is finishing at midstream; Propel Confidence is carried as plain Coastal at the 21,160 norm — the list prints her so and its Sr No 7 row is NIL — not as a 30K / 25K quote. The empty hours at CJ-14 and CJ-4 are noted, not modelled: one case each.", "ok")
LB = LE("19 Nov 12:29 · the three points left open on 16 Nov — what the sheets answer",
 "(1) ROME TRADER and HP: she took no HP place — she berthed under SAAGAR (\"SGR- NEELKANTH\") on 18 Nov. (2) Desk sheet against the bulk-first rule: the port went by the rule — one SAAGAR place to Rome Trader, one to ML Egret; Uni Blossom, whom the desk had on 19 Nov, is still waiting as SGR 1. (3) CD GLORY's 6.5K / 8K rank: PRINTED NOW — 8K 8 on the sheet revised after the 18 Nov meeting; lists 16.11 and 17.11 and the morning sheet of 18.11 had none. Rome Trader was never given a Sr No 7 place.",
 "Board (16 Nov): asked Mihir whether Rome Trader was offered for HP and at what MTPD; held the bulk-first SAAGAR rule against the desk's ETBs; showed CD Glory's 6.5K route only as \"if ranked\".",
 "Lists 17.11 and 18.11, DPR 19.11, programme 18.11 and the 18 Nov signal, as above.",
 "The documents settle all three; nothing further is needed from Mihir on them.",
 "v173: CD Glory's 6.5K / 8K route now runs on her printed rank (8K 8); Rome Trader's option card is closed — she is alongside.", "closed")
B.rep("const LEARN=[\n", "const LEARN=[\n" + LA + LB)
# the 16 Nov 18:17 entry: its open points are answered by the entry above
a = B.s.index(" {d:'16 Nov 18:17 · list 16.11 + programme 17.11 + night signal 16 Nov',"); e = B.s.index("},\n", a)
ent = B.s[a:e]
if ent.count("st:'open'") != 1: B.die('16 Nov entry: st open count %d' % ent.count("st:'open'"))
B.s = B.s[:a] + ent.replace("st:'open'", "st:'closed'") + B.s[e:]
B.save()
