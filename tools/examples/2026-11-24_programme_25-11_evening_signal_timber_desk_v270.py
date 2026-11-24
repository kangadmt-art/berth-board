#!/usr/bin/env python3
# apply66 — v270: papers received 24 Nov 22:51, no text —
#   PROGRAMME 25.11 (TF/SH/2102 dt 24 Nov 2026, PDF, one page) — the meeting of 24 Nov — and
#   the HM EVENING SIGNAL of 24 Nov, twice: as dispatched 16:55 and as amended (17:15, 17:40, 19:20; Capt Madaan / Capt Yadav).
# Cargo jetties: CJ-1 Crystal O out → MANTA SENA ("6.5K") · CJ-7 Gokova-M out 00:01 → ASIAN SUMMIT at 50–57, printed "SGR" · CJ-9 Sand Topic shifts to OTB 05:00 →
#   PIONEER FORTUNE ("GFPL") · CJ-13 Uni Blossom out 25 Nov 17:30 → AG VARVARA ("SGR") · CJ-15 ML Egret out → XIN HAI TONG 71 ("PROJ") · CJ-3 Horizon Chaser out 08:00, nobody in.
# CD Glory is not on it. The meeting is scored on the call made at 10:40, before it sat (v269): Hai Nam 81 → 15 · Asian Summit → 7 · AG Varvara → 13.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='PROGRAMME 25.11'); q = B.q
P = 'PROGRAMME 25.11'; SG = 'HM EVENING SIGNAL 24 Nov (disp 16:55, amended to 19:20)'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
    raise TypeError(o)
def pre(m, t): B.note_prefix(m, q(t) + " ")
def sub(m, o, n): B.sub_entry(m, o, n)

# ================= HEADER =================
B.rep("const NOW=h('11-24 10:40');", "const NOW=h('11-24 22:51');")
B.rep("const PROG_END=h('11-24 18:00'); // programme 24.11 (meeting of 23 Nov) covers till here", "const PROG_END=h('11-25 18:00'); // programme 25.11 (meeting of 24 Nov) covers till here")
B.rep("<i>Programme</i><b>24.11</b>", "<i>Programme</i><b>25.11</b>")
B.rep("<i>Signals to</i><b>24 Nov day sheet (disp 2115 / 0547)</b>", "<i>Signals to</i><b>24 Nov evening sheet (disp 1655, amended to 1920)</b>")
B.rep("(no list came for 22.11) · programme 24.11 ·", "(no list came for 22.11 or, so far, 24.11) · programme 25.11 ·")
B.rep("HM signal sheets to the day sheet of 24 Nov (disp 21:15 / 05:47) · timber desk sheet", "HM signal sheets to the evening sheet of 24 Nov (disp 16:55, amended to 19:20) · timber desk sheet")
B.rep("const BOARD_SRC='", "const BOARD_SRC='programme 25.11 (TF/SH/2102 dt 24 Nov) · HM evening signal 24 Nov (disp 1655, amended to 1920) · ")
B.rep("const PROG_SAIL=new Set(['Vishva Bandhan',", "const PROG_SAIL=new Set(['Crystal O','Horizon Chaser','Gokova-M','Sand Topic','Uni Blossom','ML Egret','Vishva Bandhan',")

# ================= V — sailings, warpings =================
M = "{b:'1',n:'Crystal O',nm:6500,p:[0,7.5]"
pre(M, P + ": CJ-01 · OUT readiness 24 Nov 23:43 (her list ETC), 9.5 m, night sailing → MV MANTA SENA takes the berth (\"6.5K\"). " + SG + ": OUT 23:43 struck and written 06:00 on 25 Nov · Capt Sachin. At 0700 on 24 Nov she still had 8,323 MT to load at 5,347 a day — sailing at 06:00 she either worked much faster through the day or leaves cargo behind; the next DPR will show.")
sub(M, "f:'11-22 11:30',t:'11-24 23:43'", "f:'11-22 11:30',t:'11-25 06:00',lt:'11-24 23:43'")
M = "{b:'3',n:'Horizon Chaser',p:[17.5,21.75]"
pre(M, P + ": CJ-03 · OUT readiness 25 Nov 08:00, 4.5 m — NO inward vessel printed for the berth. " + SG + ": OUT 08:00 · Capt Sud.")
sub(M, "f:'11-24 04:00',t:'11-25 04:00',est:1", "f:'11-24 04:00',t:'11-25 08:00'")
M = "{b:'5',n:'Blue Shark',p:[32.5,40]"
pre(M, P + ": WARPING AT PANELS to 32¼–39¾ (night). " + SG + ": WARP 20:30 (21:00 before the amendment) · Capt Yadav · 32½–40 → 32¼–39¾ — a quarter panel south.")
B.rep(M, "{b:'5',n:'Blue Shark',p:[32.25,39.75]")
M = "{b:'6',n:'Parvraj',nm:14950,p:[41.25,49.5]"
pre(M, P + ": NIGHT WARPING AT PANELS to 40¾–49 — no outward row for her. " + SG + ": WARP 23:00 · Capt Sachin · 41¼–49½ → 40¾–49 — half a panel south, to open 50–57 for Asian Summit.")
B.rep(M, "{b:'6',n:'Parvraj',nm:14950,p:[40.75,49]")
M = "{b:'7',n:'Gokova-M',nm:50000,p:[50.5,57]"
pre(M, P + ": printed CJ-07 · OUT readiness 25 Nov 00:01, 10.5 m, night sailing → MV ASIAN SUMMIT takes 50–57. " + SG + ": OUT 00:01 · Capt Deepak (his second move, after ML Egret at 22:00). A day and an hour alongside, as her 50,000 bid promised.")
sub(M, "f:'11-23 23:05',t:'11-25 01:30',est:1", "f:'11-23 23:05',t:'11-25 00:01'")
M = "{b:'9',n:'Sand Topic',nm:20000,p:[69,77.75]"
pre(M, P + ": CJ-09 · OUT readiness 25 Nov 05:00, 6.7 m · \"NIGHT SHIFTING TO OTB. AGENT'S REQ.\" → MV PIONEER FORTUNE takes the berth (\"GFPL\", night berthing). " + SG + ": SHIFT 05:00 (\"OUT\" struck, \"SHIFT\" written) · Capt Bali · 69–77¾ → OTB.")
sub(M, "f:'11-23 02:45',t:'11-25 18:18',lt:'11-24 18:18',est:1", "f:'11-23 02:45',t:'11-25 05:00',lt:'11-24 18:18'")
M = "{b:'13',n:'Uni Blossom',nm:4600,p:[113,124.75]"
pre(M, P + ": CJ-13 · OUT readiness 25 Nov 17:30, 6.5 m → MV AG VARVARA takes the berth (112–125, \"SGR\"). Not on the evening signal — a day move. The DPR pace had her done about 10:30.")
sub(M, "f:'11-21 02:00',t:'11-27 09:15',lt:'11-28 17:58',est:1", "f:'11-21 02:00',t:'11-25 17:30',lt:'11-28 17:58'")
M = "{b:'15',n:'ML Egret',nm:4600,p:[145.75,158.25]"
pre(M, P + ": CJ-15 · OUT readiness 25 Nov 02:00, 7.0 m, night sailing → MV XIN HAI TONG 71 takes the berth (\"PROJ\", night berthing). " + SG + ": OUT 02:30 struck and written 22:00 on 24 Nov · Capt Deepak, his first move — four hours earlier than the programme; the DPR pace gave about 22:00 for the last of her logs.")
sub(M, "f:'11-18 21:45',t:'11-28 07:30'", "f:'11-18 21:45',t:'11-24 22:00',lt:'11-28 07:30'")

# ================= V — the five inward vessels of programme 25.11 =================
NEWV = [
 " {b:'1',n:'Manta Sena',nm:6500,p:[0,7.5],c:'Rice bags',q:30170,u:'MT',cat:'8K',f:'11-25 10:00',t:'11-30 03:25',est:1,note:'" + q(
   P + ": CJ-01 · IN behind Crystal O · panels printed \"7 1/2 – N\" · CATEGORY 6.5K · night starboard. " + SG + ": IN \"o/c\" · FLOOD · first under Capt Sachin behind Crystal O's 23:43; amended — Crystal O now sails 06:00 and Manta Sena is Capt Karan's SECOND move, after Willows (RT OUT 08:00 from OJ-6) → about 10:00 on 25 Nov, est (flood till 14:28). "
   "30,170 MT of rice bags at the 6,500 norm → about 30 Nov 03:25, est. Waiting sheet: 8K 1 · GEN 3 — the senior vessel of the 6.5K / 8K line; reported 26 Oct 10:45, ready 20 Nov 11:00; 177.13 m, 6.04 m; stevedore Mihir & Company.") + "'},",
 " {b:'7',n:'Asian Summit',nm:30000,p:[50,57],c:'Petcoke',q:60499,u:'MT',cat:'SAAGAR',via:'printed \"SGR\" on programme 25.11 · HP 4 on the list, 30k/25k quote (Sr No 7)',f:'11-25 02:00',t:'11-27 04:25',est:1,note:'" + q(
   P + ": printed CJ-07 · IN behind Gokova-M (out 25 Nov 00:01) · 50–57 · CATEGORY \"SGR\" · night starboard. " + SG + ": IN 00:00 (01:00 before the amendment) · Capt Yadav · FLOOD — the pilot boards at midnight; alongside about 02:00 on 25 Nov, est. 60,499 MT at her 30,000 quote → about 27 Nov 04:25, est. "
   "Waiting sheet: HP 4 · SGR 7 · GEN 28 · \"30K/25K/10K SR NO.07\"; reported / ready 22 Nov 10:00; 199.98 m, 13.35 m. THE PROGRAMME PRINTS \"SGR\" FOR HER, yet she is SGR 7 — CD Glory (SGR 3), Dariya Priya (4), African Tiger (5) and Paiwan Ace (6) wait above her in that column. The berth she takes is the HP berth Gokova-M leaves and she is the next HP vessel after MSC Magali (HP 3), which reads like an HP berthing. The board counts her AS PRINTED, in the SAAGAR places — and the timber desk's sheet after the meeting (CD Glory ETB 27 Nov) agrees with that count. If she in fact counts under HP, CD Glory is about 18 hours earlier. Open in the checks.") + "'},",
 " {b:'9',n:'Pioneer Fortune',nm:6500,p:[69,76.25],c:'Sugar bags',q:25080,u:'MT',cat:'PPP',f:'11-25 07:00',t:'11-29 03:35',est:1,note:'" + q(
   P + ": CJ-09 · IN behind Sand Topic (shifting to OTB 05:00) · 69–76¼ · CATEGORY \"GFPL\" — the Gautam Freight berth, outside the DPA queue · night berthing. " + SG + ": IN \"o/c\" · Capt Bali behind his 05:00 → about 07:00 on 25 Nov, est. 25,080 MT of sugar bags at 6,500 a day → about 29 Nov 03:35, est. "
   "Waiting sheet: 8K 3 · GEN 6 · Sr No 7; reported 5 Nov 12:30, ready 13 Nov 11:00; 169.26 m, 5.68 m. She leaves the 6.5K / 8K line by the PPP berth: Crystal Land (8K 2) is now its senior vessel.") + "'},",
 " {b:'13',n:'AG Varvara',nm:4600,p:[112,125],c:'JAS pine logs',q:39113,u:'CBM',cat:'SAAGAR',f:'11-25 19:30',t:'12-04 12:35',est:1,note:'" + q(
   P + ": CJ-13 · IN behind Uni Blossom (out readiness 25 Nov 17:30) · 112–125 · CATEGORY SGR. About 19:30 on 25 Nov alongside, est; 39,113 CBM at the pace of the timber berths (about 4,500 CBM a day) → about 4 Dec 12:35, est. "
   "Waiting sheet: SGR 1 · GEN 13 · Sr No 7 — the senior vessel of the SAAGAR line; reported / ready 12 Nov 07:06 — thirteen days waiting; 199.99 m, 9.0 m. The board's call had her for this berth.") + "'},",
 " {b:'15',n:'Xin Hai Tong 71',p:[145.75,158.25],c:'Packaged steel & project cargo',q:5706,u:'MT',cat:'GOV',via:'printed \"PROJ\" — project cargo (SGR 2 on the list)',f:'11-25 03:30',t:'11-26 11:55',est:1,note:'" + q(
   P + ": CJ-15 · IN behind ML Egret · 145¾–158¼ · CATEGORY \"PROJ\" · night berthing. " + SG + ": IN \"o/c\" · Capt Bali behind his 01:30 sailing of Shebelle → about 03:30 on 25 Nov, est (ML Egret leaves at 22:00). 5,706 MT of packaged steel and project cargo → about 26 Nov 11:55, est (a day and a third, the board's reckoning). "
   "Waiting sheet: SGR 2 · STL 1 · GEN 14; reported / ready 12 Nov 16:48; 199.9 m. THIS ANSWERS THE OPEN QUESTION: the port takes her by the PROJECT route, not in the SAAGAR count — and it gives her the timber berth ML Egret leaves. The board's call had Hai Nam 81 here on her HP quote.") + "'},",
]
a, b = B.line_of(" {b:'14',n:'Lila Tokyo',nm:30000,p:[126,143.5]")
B.s = B.s[:a] + "\n".join(NEWV) + "\n" + B.s[a:]
B.rep("'Blue Shark':167,'Zheng Hui':229});", "'Blue Shark':167,'Zheng Hui':229,'Manta Sena':177.13,'Asian Summit':199.98,'Pioneer Fortune':169.26,'AG Varvara':199.99,'Xin Hai Tong 71':199.9});")

# ================= W =================
for n in ('Manta Sena', 'Asian Summit', 'Pioneer Fortune', 'AG Varvara', 'Xin Hai Tong 71'): B.wdel(n)
def w(name, text, **k): B.wrow(name, q(text), **k)
w('CD Glory', "NOT ON IT — but the two vessels above her in the SAAGAR column are in: AG Varvara (SGR 1) at CJ-13, Xin Hai Tong 71 (SGR 2) at CJ-15 as PROJ. She is now the senior waiting vessel of the SAAGAR line. Asian Summit (SGR 7) is printed \"SGR\" at CJ-7 — on the HP berth; open in the checks")
w('Hai Nam 81', "not on it — CJ-15, where the board's call had her on the HP quote, went to Xin Hai Tong 71 as PROJ; the HP berth at CJ-7 went to Asian Summit (HP 4, a rank above her)")
w('MSC Magali', "not on it — HP 3, senior to Asian Summit (HP 4) who took the HP berth at CJ-7")
w('Crystal Land', "senior vessel of the 6.5K / 8K line now — Manta Sena (8K 1) is in at CJ-1 and Pioneer Fortune (8K 3) at CJ-9, the Gautam Freight berth")
w('Aboudi D', "CJ-3 falls vacant at 08:00 on 25 Nov (Horizon Chaser out) and NO vessel is printed for it — she needs two shore cranes there")

# ================= MEETLOG — the 24 Nov meeting, scored on the call of 10:40 =================
ML = ("{d:'11-24',at:'11-24 10:40',basis:'list 23.11 (revised) · programme 24.11 · DPR 24.11 · HM signals to the day sheet of 24 Nov (disp 21:15 / 05:47)',prog:'25.11',"
      "call:[['Hai Nam 81','15'],['Asian Summit','7'],['AG Varvara','13']],got:[['Manta Sena','1'],['Asian Summit','7'],['Pioneer Fortune','9'],['AG Varvara','13'],['Xin Hai Tong 71','15']],note:'" + q(
      "Two of three right, vessel and berth: Asian Summit at CJ-7 behind Gokova-M and AG Varvara at CJ-13 behind Uni Blossom. Wrong: CJ-15 went to XIN HAI TONG 71, printed \"PROJ\", not to Hai Nam 81 on her HP quote — the port did not let an HP bid into the timber berth; it kept it for the SAAGAR column and took the project vessel there. "
      "Missed altogether: MANTA SENA at CJ-1 — the board went by Crystal O's DPR pace (done about 25 Nov 20:20, outside the window), the port by her list ETC (24 Nov 23:43; the signal now says 06:00) — and PIONEER FORTUNE at CJ-9, the Gautam Freight berth, which the board does not call. CJ-3 (Horizon Chaser out 08:00) is given to nobody. "
      "The berth-wise meeting section of v269 did better than the call: HP at CJ-7 → Asian Summit named; SAAGAR at CJ-13 and CJ-15 → AG Varvara, Xin Hai Tong 71, CD Glory — the two that came were its first two names; it had CJ-1 as continuing, the same miss. "
      "Asian Summit is printed \"SGR\" although she is SGR 7 and came by her HP rank — see the checks.") + "'},")
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")

# ================= LEARN =================
L1 = {'d': '24 Nov 22:51 · programme 25.11 — Asian Summit printed "SGR" at CJ-7',
      'v': "Asian Summit (petcoke 60,499 MT) at CJ-7, 50–57, behind Gokova-M.",
      'exp': "The board's call: Asian Summit to CJ-7 as the HP vessel — the HP berth Gokova-M leaves, on her 30K quote (HP 4; MSC Magali, HP 3, passed over).",
      'act': "Programme 25.11 prints her category as \"SGR\". On the waiting sheet she is SGR 7; CD Glory (SGR 3), Dariya Priya (SGR 4), African Tiger (SGR 5) and Paiwan Ace (SGR 6) stand above her in that column and are not on the programme.",
      'why': "Not on the papers. Three readings: (1) the category column prints the scheme the vessel is registered under, not the place she takes — she came by her HP rank and the HP berth, and \"SGR\" only says she is a SAAGAR vessel; (2) the port counted a third SAAGAR place at CJ-7 and gave it to the only SAAGAR vessel that can work there — the timber vessels above her are not berthed at the coal berths; (3) a slip. The first fits the facts best: AG Varvara (SGR 1) has the SAAGAR berth at CJ-13, and nothing else in the SAAGAR column moved.",
      'fix': "Entered AS PRINTED — category SAAGAR at CJ-7, her HP rank on the card. The calculation then holds a SAAGAR place with her till she sails (about 27 Nov 04:25) and gives CD Glory CJ-16 about 27 Nov 08:00 — the timber desk's sheet written after the meeting says the same day (ETB 27 Nov). If she counts under HP (reading 1), the board's run gives CD Glory CJ-15A about 26 Nov 13:35. Mihir to say which.",
      'st': 'open'}
L2 = {'d': '24 Nov 22:51 · programme 25.11 — the meeting of 24 Nov',
      'v': "The berthings of the cargo jetties given at the meeting of 24 Nov.",
      'exp': "The call of 10:40: Hai Nam 81 → CJ-15 (HP quote) · Asian Summit → CJ-7 (HP) · AG Varvara → CJ-13 (SAAGAR).",
      'act': "Programme 25.11: Manta Sena \"6.5K\" at CJ-1 behind Crystal O · Asian Summit \"SGR\" at CJ-7 (50–57) behind Gokova-M · Pioneer Fortune \"GFPL\" at CJ-9 behind Sand Topic · AG Varvara \"SGR\" at CJ-13 behind Uni Blossom · Xin Hai Tong 71 \"PROJ\" at CJ-15 behind ML Egret · CJ-3 (Horizon Chaser out 08:00): nobody.",
      'why': "Every berth went to the SAME priority as the vessel leaving it: 6.5K → 6.5K at CJ-1, HP → HP at CJ-7, SAAGAR → SAAGAR at CJ-13, SAAGAR → the SAAGAR column's project vessel at CJ-15. The rule Mihir gave on 22 Nov held four times out of four. The board's call broke it once — it let Hai Nam 81's HP bid into the SAAGAR berth at CJ-15 — and that was its one wrong berth. Its other miss was a matter of hours: it took Crystal O's finish from the DPR pace, the port from her list ETC.",
      'fix': "Entered from the programme. For the engine-rules review: (a) an HP bid does not go into a berth a SAAGAR vessel is leaving while a SAAGAR vessel is ready; (b) for the meeting, a berth counts as falling vacant on the list ETC when the DPR pace is later — the port programmes on its own ETC. Not coded yet.",
      'st': 'open'}
B.rep("const LEARN=[\n", "const LEARN=[\n " + js(L1) + ",\n " + js(L2) + ",\n")

# ================= MV =================
MVN = ['HM evening signal 24 Nov (dispatched 16:55; amended 17:15, 17:40 and 19:20) · Capt Madaan / Capt Yadav · received 24 Nov 22:51 · cargo berths', [
 ['20:30', 'WARP', 'Blue Shark', 'CJ-5 · 32½–40 → 32¼–39¾', 'Yadav', '11-24 20:30', '21:00 before the amendment'],
 ['22:00', 'OUT', 'ML Egret', 'CJ-15 · 145¾–158¼ → OTB', 'Deepak', '11-24 22:00', '① · 02:30 before the amendment · programme readiness 25 Nov 02:00'],
 ['23:00', 'WARP', 'Parvraj', 'CJ-6 · 41¼–49½ → 40¾–49', 'Sachin', '11-24 23:00', 'room for Asian Summit at 50–57'],
 ['00:01', 'OUT', 'Gokova-M', 'CJ-7 · 50½–57 → OTB', 'Deepak', '11-25 00:01', '②'],
 ['00:00', 'IN', 'Asian Summit', 'OTB → CJ-7 · 50–57', 'Yadav', '11-25 02:00', 'FLOOD · 01:00 before the amendment · pilot boards 00:00, alongside about 02:00 — est · printed "SGR"'],
 ['01:30', 'OUT', 'Shebelle', 'CJ-12 · 101–109 → OTB', 'Bali', '11-25 01:30', 'container · programme 01:41'],
 ['o/c', 'IN', 'Hong Da Xin 768', 'OTB → CJ-12 · 100–109', 'Deepak', '11-25 03:30', '③ · FLOOD · container · behind Shebelle — est'],
 ['o/c', 'IN', 'Xin Hai Tong 71', 'OTB → CJ-15 · 145¾–158¼', 'Bali', '11-25 03:30', 'behind his 01:30 — est · printed "PROJ"'],
 ['05:00', 'SHIFT', 'Sand Topic', 'CJ-9 · 69–77¾ → OTB', 'Bali', '11-25 05:00', '"OUT" struck, "SHIFT" written · agent\'s request (programme)'],
 ['06:00', 'OUT', 'Crystal O', 'CJ-1 · "7½ – N" → OTB', 'Sachin', '11-25 06:00', '23:43 before the amendment'],
 ['o/c', 'IN', 'Pioneer Fortune', 'OTB → CJ-9 · 69–76¼', 'Bali', '11-25 07:00', 'behind Sand Topic — est · "GFPL"'],
 ['08:00', 'OUT', 'Horizon Chaser', 'CJ-3 · 17½–21¾ → OTB', 'Sud', '11-25 08:00', 'row added by the amendment'],
 ['o/c', 'IN', 'Manta Sena', 'OTB → CJ-1 · "7½ – N"', 'Karan', '11-25 10:00', '② · FLOOD · Capt Sachin before the amendment · after Willows (08:00) — est · "6.5K"'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Yadav 20:00–20:30 · Capt Sachin 04:30–05:30 · Capt Sud one hour on completion', '—', '11-25 05:30', '']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")

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
def berth(bid, nown, add, etc=None):
    a, b, d, tail = bline(bid); now = obj(d['now']); assert nown in now['n'], (nown, now['n'])
    if etc is not None: now['etc'] = js(etc)
    now['note'] = "'" + q(add + ' · ') + now['note'][1:]; d['now'] = unobj(now, NOWKEYS); bput(a, b, d, tail)
def turn(bid, oldn, out, outBy, newn, f, est, add):
    wa, wb = B.line_of("  {n:'%s'," % newn); wl = B.s[wa:wb].strip().rstrip(','); wv = obj(wl); assert 'n' in wv and 'c' in wv
    B.s = B.s[:wa] + B.s[wb + 1:]
    a, b, d, tail = bline(bid); now = obj(d['now']); assert oldn in now['n'], (oldn, now['n'])
    pv = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}; pv['out'] = js(out); pv['outBy'] = js(outBy)
    nw = {k: wv[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'rank', 'ag') if k in wv}; nw['f'] = js(f)
    if est: nw['est'] = '1'
    nw['note'] = "'" + q(add + ' · ') + wv.get('rem', "''")[1:]
    d['prev'] = unobj(pv, PREVKEYS); d['now'] = unobj(nw, NOWKEYS); bput(a, b, d, tail)
def rem(name, text):
    a, b = B.line_of("  {n:'%s'," % name); i = B.s.index("rem:'", a) + 5; assert i < b; B.s = B.s[:i] + q(text + ' · ') + B.s[i:]
turn('OJ-4', 'Al Mahboobah', '11-24 21:00', SG + ': OUT 21:00 (22:00 before the amendment) · Capt Yadav · PROGRAMME 25.11: out readiness 24 Nov 22:00, 7.5 m, night sailing',
     'Chemroad Nexus', '11-24 23:00', True, SG + ': IN "o/c" · Capt Yadav behind Al Mahboobah (OUT 21:00) → about 23:00 on 24 Nov, est · ' + P + ': OJ-04 — IN, night berthing')
berth('OJ-6', 'Willows', SG + ': RT OUT 08:00 on 25 Nov (06:00 and Capt Sud before the amendment) · Capt Karan, his first move · ' + P + ': OJ-06 · out readiness 25 Nov 06:00, 7.5 m → MT CULTURE in, starboard', etc='11-25 08:00')
berth('OJ-1', 'Bogazici', P + ': OJ-01 · 25 Nov 17:00, 7.5 m — "SHIFTING FROM OJ-01 TO OTB. AGENT\'S REQ." — she leaves the jetty for the anchorage; no inward vessel printed', etc='11-25 17:00')
berth('OJ-2', 'Chemroute Pegasus', P + ': OJ-02 · OUT readiness 25 Nov 17:30, 7.1 m → MT THETIS LEONA in', etc='11-25 17:30')
rem('Culture', P + ': OJ-06 — IN behind Willows, starboard · ' + SG + ': IN "o/c" · Capt Sud after Horizon Chaser (OUT 08:00) · FLOOD → about 10:00 on 25 Nov, est')
rem('Thetis Leona', P + ': OJ-02 — IN behind Chemroute Pegasus (out readiness 25 Nov 17:30) → about 19:30 on 25 Nov, est')
B.s, k = re.subn(r"const LIQ=\{prog:'(?:[^'\\]|\\.)*',src:'(?:[^'\\]|\\.)*',asOf:'11-24 10:40',",
    lambda _: "const LIQ={prog:'" + q("PROGRAMME 25.11 — OJ-4 Al Mahboobah out 24 Nov 22:00 (signal 21:00) → Chemroad Nexus in, night · OJ-6 Willows out 25 Nov 06:00 (signal: RT OUT 08:00) → Culture in, starboard, on the flood · OJ-2 Chemroute Pegasus out 25 Nov 17:30 → Thetis Leona in · OJ-1 LPG/C Bogazici shifts to OTB 25 Nov 17:00 at the agent's request · nothing printed for OJ-3 (Hafnia Ammolite), OJ-7 (Sriwangi V)")
    + "',src:'DPA berthing list 23.11.26 as revised after the meeting · DPR 24.11 · programme 25.11 · signals to the evening sheet of 24 Nov (disp 1655, amended to 1920)',asOf:'11-24 22:51',", B.s, count=1)
if k != 1: B.die('LIQ head not found')
LQ = ['HM evening signal 24 Nov (dispatched 16:55; amended 17:15, 17:40 and 19:20) · Capt Madaan / Capt Yadav · oil-jetty rows', [
 ['21:00', 'OUT', 'Al Mahboobah', 'OJ-4 → OTB', 'Yadav', '11-24 21:00', '22:00 before the amendment'],
 ['o/c', 'IN', 'Chemroad Nexus', 'OTB → OJ-4', 'Yadav', '11-24 23:00', 'behind Al Mahboobah — est'],
 ['08:00', 'OUT', 'Willows', 'OJ-6 → OTB', 'Karan', '11-25 08:00', '① · RT OUT · Capt Sud at 06:00 before the amendment'],
 ['o/c', 'IN', 'Culture', 'OTB → OJ-6', 'Sud', '11-25 10:00', 'FLOOD · row added by the amendment · after Horizon Chaser (08:00) — est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQ) + ",\n")

# ================= TIMBER =================
def tnote(name, text, tag=P):
    k_ = "{n:'%s',cbm:" % name
    if B.s.count(k_) != 1: B.die('TIMBER anchor: ' + name)
    a = B.s.index(k_); i = B.s.index("note:'", a) + 6; B.s = B.s[:i] + q(tag + ": " + text + " · ") + B.s[i:]
tnote('AG Varvara', "CJ-13 — IN behind Uni Blossom (out readiness 25 Nov 17:30) · 112–125 · SGR → about 19:30 on 25 Nov, est")
tnote('Uni Blossom', "OUT readiness 25 Nov 17:30, 6.5 m → AG Varvara takes CJ-13")
tnote('ML Egret', "OUT readiness 25 Nov 02:00, 7.0 m → Xin Hai Tong 71 (project cargo) takes CJ-15 · evening signal: OUT 22:00 on 24 Nov, Capt Deepak")
tnote('CD Glory', "not on it — AG Varvara (SGR 1) and Xin Hai Tong 71 (SGR 2, as PROJ) are in; she is now the senior waiting vessel of the SAAGAR line")
# ---- the Mihir & Co timber desk sheet of 24 Nov 12:00 ("updated up to 25 Nov 18:00, after today's berthing meeting") — pasted in the chat at 22:57
TD = 'TIMBER DESK 24 Nov'
B.rep("d:'21 Nov 1200',upto:'22 Nov 1800, after the berthing meeting of 21 Nov',", "d:'24 Nov 1200',upto:'25 Nov 1800, after the berthing meeting of 24 Nov',")
B.rep("asOf:'11-21 12:00',etaFromDesk:false,waiting:44,", "asOf:'11-24 12:00',etaFromDesk:false,waiting:45,")
for nm, head, old, new in (
  ('AG Varvara', "cbm:39113,from:'Australia',c:'Pine logs',eta:'11-12 07:06',", '11-26', '11-24'),
  ('CD Glory', "cbm:29158,from:'Malaysia',c:'Hardwood logs',eta:'11-15 06:42',", '11-26', '11-27'),
  ('Dariya Priya', "cbm:44968,from:'New Zealand',c:'Pine logs',eta:'11-16 09:00',", '11-30', '12-01'),
  ('African Tiger', "cbm:36328,from:'Uruguay',c:'Pine logs',eta:'11-18 06:30',", '12-03', '12-02'),
  ('Paiwan Ace', "cbm:36905,from:'Uruguay',c:'Pine logs',eta:'11-22 00:06',", '12-08', '12-07'),
  ('African Pheasant', "cbm:45282,from:'New Zealand',c:'Pine logs',eta:'11-23 04:24',", '12-13', '12-08'),
  ('Erna Oldendorff', "cbm:34424,from:'Australia',c:'Pine logs',eta:'11-23 11:30',", '12-08', '12-12')):
    B.rep("{n:'%s',%setb:'%s'," % (nm, head, old), "{n:'%s',%setb:'%s'," % (nm, head, new))
tnote('ML Egret', '"she will sail 24.11.2026"', TD)
tnote('Uni Blossom', '"she will sail 25.11.2026 at 1730 hrs"', TD)
tnote('AG Varvara', '"she will berth 24.11.2026 under SAAGAR" — the programme has her in behind Uni Blossom on 25 Nov, about 19:30; the port paper stands', TD)
tnote('CD Glory', 'ETB 27 Nov (26 Nov on the sheet of 21 Nov) — the same day the board reaches with Asian Summit counted as printed', TD)
tnote('Dariya Priya', 'ETB 1 Dec (30 Nov before)', TD)
tnote('African Tiger', 'ETB 2 Dec (3 Dec before)', TD)
tnote('Paiwan Ace', 'ETB 7 Dec under SAAGAR, OR 2 Dec "under 6500 CBM" (8 Dec before) — the desk now shows the 6.5K route as five days quicker', TD)
tnote('African Pheasant', 'ETB 8 Dec (13 Dec before)', TD)
tnote('Erna Oldendorff', 'ETB 12 Dec (8 Dec before) · the desk has her ETA as 23 Nov 13:30; the port list printed 11:30 and stands', TD)
tnote('Paiwan Wisdom', 'ETA 28 Nov · ETB 17 Dec — unchanged', TD)
B.rep("· timber desk sheet 21 Nov 12:00 ·", "· timber desk sheet 24 Nov 12:00 ·")
B.list_tag = TD
B.wrow('Paiwan Ace', q('ETB 7 Dec under SAAGAR, or 2 Dec "under 6500 CBM" — "presently 45 vessels are waiting"'))
B.wrow('CD Glory', q('ETB 27 Nov'))

# ================= MYLOG — CD Glory =================
RD = {'d': '24 Nov 22:57 · programme 25.11 + evening signal 24 Nov + timber desk sheet 24 Nov', 'exp': '11-27 08:00', 'b': '16',
      'slot': "SAAGAR — now the SENIOR WAITING VESSEL of the line · not on programme 25.11 · the timber desk after the meeting: ETB 27 Nov",
      'why': "The meeting of 24 Nov gave CJ-13 to AG Varvara (SGR 1) and CJ-15 to Xin Hai Tong 71 (SGR 2, printed PROJ); CJ-1, where the board had CD Glory for 25 Nov 22:20, went to Manta Sena, the senior 6.5K vessel — Crystal O sails on her list ETC, not on the DPR pace. Nobody is left above CD Glory in the SAAGAR column. But the programme also prints Asian Summit (SGR 7, HP 4) as \"SGR\" at CJ-7; counted as printed she holds a SAAGAR place till about 27 Nov 04:25, and CD Glory follows at CJ-16 about 27 Nov 08:00. The timber desk's sheet of 24 Nov, written after the meeting, gives the same day: ETB 27 Nov. EARLIER IF Asian Summit counts under HP (she took the HP berth by her HP rank): then CD Glory is the next SAAGAR vessel for CJ-15A / CJ-15, about 26 Nov 13:35. Berths falling vacant inside tomorrow's window (to 26 Nov 18:00): CJ-14 Lila Tokyo about 25 Nov 23:00 · CJ-16 African Hornbill about 26 Nov 11:10 · CJ-15A Ocean Kudos about 11:35 · CJ-15 Xin Hai Tong 71 about 11:55."}
i = B.s.index("'CD Glory':[", B.s.index('const MYLOG')); j = B.s.index("\n ],", i)
assert B.s[j - 1] == '}', B.s[j - 30:j]
B.s = B.s[:j] + ",\n  " + js(RD) + B.s[j:]

B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='24 Nov 2026 · 23:00 IST';", B.s, count=1)
B.save()
