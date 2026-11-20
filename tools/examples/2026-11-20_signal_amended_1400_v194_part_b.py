#!/usr/bin/env python3
# apply39b — v194 (part 2, logs): UPDATED, CD Glory route note, snapshot, prediction log, own-vessel log, lesson (one question for Mihir: Safi Alfa / CJ-4). argv[1] = UPDATED
import re, sys, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; B = Board(W + 'dpa-berth-board.html'); q = B.q
S = json.load(open(W + 'S194.json')); byn = {x['n']: x for x in S}
UPD = sys.argv[1]
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
def note_of(label, text):
    a = B.s.index("{label:'%s'," % label, B.s.index("const OPTS={")); n0 = B.s.index("note:'", a) + 6; n1 = B.s.index("'}", n0)
    B.s = B.s[:n0] + q(text) + B.s[n1:]
note_of('SAAGAR', "THE ONLY LINE THAT COUNTS FOR HER NOW. SAAGAR group — one bulk and one break-bulk place. Revised list 20.11: Uni Blossom (SGR 1), AG Varvara (2), Xin Hai Tong 71 (3 — project cargo, goes by the project route), CD Glory (4), Dariya Priya (5), African Tiger (6). Uni Blossom takes Rome Trader's place tonight (signal: Rome Trader out 00:30, Uni Blossom in behind her). ML Egret's place — about 24 Nov at the DPR pace, list ETC 28 Nov — is AG Varvara's. Uni Blossom's place is CD Glory's: taken at 5,600 CBM a day (the record average of the completed log vessels; no norm is printed for her yet) Uni Blossom is through about 27 Nov 08:00, and the board counts the place from the evening of the 26th — 26 Nov about 22:00; the berth on today's reading is CJ-4, behind whoever takes it now. Mihir's own reckoning (20 Nov 17:13) and the timber desk: 26 Nov.")

MON = {'11': 'Nov', '12': 'Dec'}
def nice(t): return "%d %s %s" % (int(t[3:5]), MON[t[:2]], t[6:])
CLn = {'GOV': 'Govt', 'COASTAL': 'Coastal', 'HP': 'Higher productivity', 'SAAGAR': 'SAAGAR', '24H': '24 hrs', '8K': '6.5K / 8K', 'STL': 'Steel / project', 'BIT': 'Bitumen', 'GEN': 'General'}
def how(x): return CLn.get(x['cat'], x['cat']) + ((' slot as ' + x['via']) if x.get('via') else '')
SG = 'HM signal 20 Nov (amended, disp 14:00)'; PG = 'programme 21.11'
fixed = [
 ['Hatnyanawati', 'OJ-2', '20 Nov 21:00', SG + ' · IN o/c · Capt Verma · est'],
 ['Parvraj', '6', '20 Nov 21:30', SG + ' · IN o/c → 43–51¼ · GOV · est'],
 ['Bow Endeavour', 'sails', '20 Nov 22:00', SG + ' · RT OUT · OJ-4 → Eva Richway'],
 ['Woohyun Dream', 'TT-2', '20 Nov 22:30', PG + ' · Tuna · night berthing · est'],
 ['Eva Richway', 'OJ-4', '20 Nov 23:00', SG + ' · IN 20:45 · est'],
 ['Rome Trader (salt, next call)', 'sails', '21 Nov 00:30', SG + ' · RT OUT · Capt Omesh · ' + PG + ': 12.9 m, night sailing'],
 ['Uni Blossom', '13', '21 Nov 02:30', SG + ' · IN o/c behind Rome Trader · SGR · 113–124¾ · est'],
 ['Meghna Prestige', 'sails', '21 Nov 04:00', SG + ' · RT OUT o/c, after Uni Blossom is in · est — ' + PG + ' had 20 Nov 19:39'],
 ['Seacon Monaco', 'sails', '21 Nov 15:00', PG + ' · CJ-9 → Yuan Hang Wei Ye'],
 ['Ken Ann', 'sails', '21 Nov 16:00', PG + ' · CJ-5 → Vishva Bandhan shifted in'],
 ['Yuan Hang Wei Ye (next call)', '9', '21 Nov 17:00', PG + ' · GFPL · 69–77¼ · est'],
 ['Vishva Bandhan', '5', '21 Nov 18:00', PG + ' · SHIFT from CJ-8, port a/c · 33¼–41½ · est'],
 ['Flag Marina', '7', '21 Nov 18:00', PG + ' · HP(42.5K) · 56¾–67¼, across CJ-7 and CJ-8 — after the shift · est'],
 ['Vishva Bandhan', 'sails', '21 Nov 20:00', 'DPR 20.11 pace, from CJ-5 — list ETC 22 Nov 14:33'],
 ['Heng Yuan Fa Zhan', 'sails', '21 Nov 21:30', 'board estimate — project vessel'],
 ['Europa Graeca', 'sails', '21 Nov 21:45', 'DPR 20.11 pace · Tuna TT-1 → Blue Ionian'],
 ['New Bliss', 'sails', '21 Nov 22:21', 'DPR 20.11 pace — list ETC 22 Nov 10:05'],
 ['Nord Copper', 'sails', '22 Nov 03:03', 'list ETC at the 23,000 norm'],
 ['African Hornbill (blades, next call)', 'sails', '24 Nov 04:00', 'board estimate — no norm printed'],
 ['ML Egret', 'sails', '24 Nov 09:40', 'DPR 20.11 pace — list ETC 28 Nov 07:30 · stays at CJ-15'],
]
proj = [[x['n'], x['b'], nice(x['F']), 'board projection — ' + how(x) + (' · after ' + x['prev'] if x.get('prev') else '')] for x in S if x['F'] <= '11-27 00:00']
i = B.s.index("const PRED=["); j = B.s.index("\n];", i)
B.s = B.s[:i] + ("const PRED=[ // snapshot %s (v194) — the signal sheet of 20 Nov as amended at 14:00 on programme 21.11 and the revised list 20.11; to be read against DPR 21.11, list 21.11 and programme 22.11\n " % UPD[:6]
                 + ",".join("['%s','%s','%s','%s']" % (q(a_), b_, c_, q(d_)) for a_, b_, c_, d_ in fixed + proj)) + B.s[j:]

b0 = B.s.index("\n];", B.s.index("const PREDLOG=["))
AT = '11-20 20:11'
def prow(n, note):
    x = byn[n]; return " {v:'%s',predAt:'%s',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}" % (q(n), AT, x['b'], x['F'], q(note))
R = "20 Nov 20:11 re-run on the signal sheet as amended at 14:00 (Safi Alfa's inward row withdrawn, CJ-4 empty from 17:00) — "
new = [
 prow('Manta Sena', R + '6.5K / 8K (8K 1), CJ-4 at the start of the next window — the place opens with New Bliss; CJ-1 behind New Bliss was the reading before'),
 prow('Safi Alfa', R + 'General (GEN 1) — back in the waiting rows; CJ-4 is the only cargo berth that takes her length, and the board gives it to the 6.5K line first; CJ-16 after African Hornbill. To confirm with Mihir'),
 prow('Blue Shark', R + 'General (GEN 2), CJ-1 once Safi Alfa is seated'),
 prow('Crystal Land', R + '6.5K / 8K (8K 2), after Manta Sena — CJ-14 after Hai Nam 81'),
 prow('CD Glory', R + 'Mihir & Co — SAAGAR (SGR 4), when Uni Blossom\'s place opens; the berth is CJ-4 behind Manta Sena on this reading. Date unchanged: 26 Nov night'),
]
B.s = B.s[:b0] + ",\n" + ",\n".join(new) + B.s[b0:]

g = byn['CD Glory']
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); i = B.s.rindex("\n ],", 0, a)
B.s = B.s[:i] + (",\n  {d:'20 Nov 20:11 · HM signal 20 Nov as amended (disp 14:00)',exp:'%s',b:'%s',slot:'SAAGAR — 26 Nov about 22:00, when Uni Blossom\\'s place opens · berth on this reading CJ-4 · General and 6.5K / 8K closed · Mihir and the timber desk: 26 Nov',why:'" % (g['F'], g['b']) + q(
 "The amended sheet does not touch her date. It confirms the step she depends on — Rome Trader out 00:30, Uni Blossom in behind her under Capt Omesh. What changes is the berth the board reads for her: Safi Alfa's inward row to CJ-4 is gone from the sheet, so CJ-4 is empty from 17:00 and the board now seats Manta Sena there under 6.5K on 21 Nov; CD Glory follows her at CJ-4 on the night of the 26th (before: CJ-14). The berth is the weak part of the reading, the date is not — it rests on Uni Blossom's rate (5,600 CBM a day assumed).") + "'}") + B.s[i:]
a = B.s.index("\n 'Rome Trader (salt, next call)':[\n", B.s.index("const MYLOG={")); e = B.s.index("\n ]\n};", a)
B.s = B.s[:e] + (",\n  {d:'20 Nov 20:11 · HM signal 20 Nov as amended (disp 14:00)',exp:'11-18 17:00',b:'13',slot:'alongside CJ-13 · SAAGAR · SIGNALLED OUT 21 Nov 00:30 · Capt Omesh · Uni Blossom in behind her',why:'" + q(
 "The amended signal sheet carries her outward movement: RT OUT 00:30, 113–125¼ → OTB, Capt Omesh, with Uni Blossom IN \"o/c\" at 113–124¾ and Meghna Prestige out after that. It agrees with programme 21.11 (00:30, 12.9 m). Her let-go hour comes with DPR 21.11; after that she leaves this card.") + "'}") + B.s[e:]

def LE_(d, v, exp, act, why, fix, st): return " {d:'%s',v:'%s',exp:'%s',act:'%s',why:'%s',fix:'%s',st:'%s'},\n" % tuple(q(x) for x in (d, v, exp, act, why, fix, st))
B.rep("const LEARN=[\n", "const LEARN=[\n" + LE_("20 Nov 20:11 · HM signal 20 Nov as amended (disp 12:40 / 13:25 / 14:00)",
 "TO CONFIRM WITH MIHIR: Safi Alfa's inward row to CJ-4 (on the 12:40 dispatch) is not on the sheet as amended at 14:00 — is she berthing at CJ-4 or not? And if not, who is CJ-4 for — the board reads Manta Sena under 6.5K.",
 "Board (v189–v193), from the 12:40 dispatch: Safi Alfa (GEN 1) in at 23–31¾ behind Propel Confidence, about 19:00; Propel Confidence sailing at 17:00; Meghna Prestige out 19:39 (programme 21.11); Heng Yuan Fa Zhan turned round at 16:00.",
 "Amended sheet: Propel Confidence \"(RT) SHIFT\" to OTB at 17:00 on agent's account · NO row for Safi Alfa, none for Konrad · Parvraj into 43–51¼ · Meghna Prestige RT OUT \"o/c\" under Capt Omesh, after Rome Trader (00:30) and Uni Blossom — about 04:00 on the 21st · Heng Yuan Fa Zhan turn-round 23:15 · Jag Pushpa out 14:45 · Eva Richway in 20:45, Bow Endeavour out 22:00 · Arrabbiata shifted to OTB 02:00. Programme 21.11 has no CJ-04 row, and the revised list keeps Safi Alfa waiting at GEN 1.",
 "A row on an early dispatch is not a berthing until the later dispatches and the programme carry it. Three later papers — the amended sheet, programme 21.11, the revised list — are silent on Safi Alfa at CJ-4; the board had built on the one that named her.",
 "v194: Safi Alfa is back in the waiting rows (GEN 1) and out of the 20 Nov meeting count; CJ-4 stands empty from 17:00; Meghna Prestige's sailing is entered at about 04:00 on 21 Nov (est); the oil-jetty hours follow the amended sheet. Projection: CJ-4 → Manta Sena under 6.5K at the start of the next window (the place opens with New Bliss); Safi Alfa, whose length only CJ-4 and the clean berths take, waits for CJ-16 on the 24th; CJ-1 behind New Bliss then goes to Blue Shark. If Mihir says Safi Alfa is for CJ-4, Manta Sena goes back to CJ-1 behind New Bliss. CD Glory's date does not move (26 Nov night).", "open"))
B.save()
