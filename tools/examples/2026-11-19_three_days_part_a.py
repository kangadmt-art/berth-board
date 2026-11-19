#!/usr/bin/env python3
# apply19a — v173 (part 1, data): three days of documents received 19 Nov 12:29 —
# Daily Berthing List 17.11 and 18.11 (two issues each; the revised 18.11 sheet is the one used), Programme for 18.11 and 19.11 (TF/SH/2102),
# DPR 17.11 / 18.11 / 19.11 (position 0700), signal sheets: night 16 Nov (disp 2005), 17 Nov (disp 1250, amended to 1750),
# 18 Nov (disp 2130 on the 17th, amended to 0933), 19 Nov (disp 0745 / 1040).
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v172.html')
B = Board(P, list_tag='LIST 18.11'); q = B.q
L = "LIST 18.11 (revised sheet)"; D19 = "DPR 19.11"; D18 = "DPR 18.11"; D17 = "DPR 17.11"
PG18 = "PROGRAMME 18.11 (TF/SH/2102)"; PG19 = "PROGRAMME 19.11 (TF/SH/2102)"; S19 = "SIGNAL 19 Nov (disp 0745 / 1040)"

def pre(marker, text): B.note_prefix(marker, q(text) + " ")
def sub(marker, old, new): B.sub_entry(marker, old, new)
def add(marker, b, n, p, c, qty, u, cat, f, t, note, nm=None, est=False, extra=''):
    s = " {b:'%s',n:'%s',%sp:[%s,%s],c:'%s',q:%s,u:'%s',cat:'%s',%sf:'%s',t:'%s',%snote:'%s'},\n" % (
        b, q(n), ("nm:%d," % nm) if nm else '', p[0], p[1], q(c), qty, u, cat, extra, f, t, 'est:1,' if est else '', q(note))
    B.add_after(marker, s)

# ================= HEADER =================
B.rep("const NOW=h('11-16 18:17');", "const NOW=h('11-19 12:29');")
B.rep("const PROG_END=h('11-17 18:00');", "const PROG_END=h('11-19 22:30');")
B.rep("const HZ=h('11-24 00:00'); let HZRUN=HZ; const OPT_HZ=h('12-08 00:00');", "const HZ=h('11-27 00:00'); let HZRUN=HZ; const OPT_HZ=h('12-11 00:00');")
B.rep("List <b>16.11 · 0700, revised</b> · DPR <b>15.11</b> · Programme <b>17.11</b> · Signals to <b>16 Nov night sheet (disp 1710)</b>",
      "List <b>18.11 · 0700, revised</b> · DPR <b>19.11</b> · Programme <b>19.11</b> · Signals to <b>19 Nov day sheet (disp 1040)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 19 Nov 12:29, three days together: Berthing List 17.11 and 18.11 (two issues each — the 18.11 sheet revised after the meeting is the one used), Programme 18.11 and 19.11 (TF/SH/2102), DPR 17.11, 18.11 and 19.11 (0700), and the signal sheets of 16 Nov night (disp 2005), 17 Nov (disp 1250, amended to 1750), 18 Nov (disp 2130 on the 17th, amended to 0933) and 19 Nov (disp 0745 / 1040, Capt Madaan). List 19.11, the evening sheet of 18 Nov and programme 20.11 are not in hand · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='list 18.11 (0700, revised after the meeting) · DPR 19.11 (0700) · programme 19.11 and 18.11 (TF/SH/2102) · signals 19 Nov (disp 0745 / 1040), 18 Nov (disp 2130, amended), 17 Nov (amended to 1750), night 16 Nov (disp 2005) · DPR 18.11 / 17.11 · ")
B.rep("'African Hornbill','Tug Chandra Sun + barge Victoria 251']);",
      "'African Hornbill','Tug Chandra Sun + barge Victoria 251','Bristol (salt, next call)','HN Doris (salt, next call)','Theometor','Rahma','African Peacock','Enshi','Propel Confidence']);")
B.rep("// last movement programme covers till here (programme for 04.11, meeting 03.11)", "// programme 19.11 + the day signal of 19 Nov (last movement about 22:00) cover till here")

# ================= V — berths =================
# ---- CJ-1
M = "{b:'1',n:'Drake Well',nm:6500,p:[0,7.25]"
pre(M, D17 + ": COMPLETED 20:00 on 16 Nov, LET GO 01:40 on the 17th — 26,111 CBM in 3 d 4½ h from commencement (about 8,200 CBM a day; 5,269 CBM on the last day). NIGHT SIGNAL 16 Nov (disp 2005): OUT 01:00 (Capt Verma) — the programme had 07:00.")
sub(M, "f:'11-13 14:00',t:'11-17 07:00',lt:'11-17 16:24'", "f:'11-13 14:00',t:'11-17 01:40',lt:'11-17 16:24'")
M = "{b:'1',n:'New Bliss',nm:6500,p:[0,7.5]"
pre(M, L + ": 6.5K / 8K · CJ-1 · 7½–N · MADE FAST 17 Nov 02:33, commenced 04:40 · norm 6,500 · ETC 22 Nov 10:05. " + D19 + ": 7,089 MT in 24 h, 13,887 of 34,000 loaded, 20,113 left → ~22 Nov 03:00 at this rate. NIGHT SIGNAL 16 Nov (disp 2005): IN o/c (Capt Karan) → 7½–N, FLOOD.")
sub(M, "f:'11-17 09:00',t:'11-22 19:30',est:1", "f:'11-17 02:33',t:'11-22 10:05'")
# ---- CJ-2
M = "{b:'2',n:'Bomustafao O',nm:3450,p:[9,16]"
pre(M, D17 + ": COMPLETED 21:50 on 16 Nov, LET GO 00:01 on the 17th — 21,945 MT. NIGHT SIGNAL 16 Nov (disp 2005): RT OUT 24:00 (Capt Rawat).")
sub(M, "f:'11-08 00:54',t:'11-17 01:30',lt:'11-14 11:33',est:1", "f:'11-08 00:54',t:'11-17 00:01',lt:'11-14 11:33'")
M = "{b:'15A',n:'North Gate',nm:3000,p:[156.5,164.75]"
pre(M, D18 + ": work stopped 11:30, LET GO 13:07 on 17 Nov — shifted to CJ-2. SIGNAL 17 Nov: SHIFT 12:30 (Capt Omesh) 156½–164¾ → 8¾–16½.")
sub(M, "f:'11-11 17:45',t:'11-17 09:00',est:1", "f:'11-11 17:45',t:'11-17 13:07'")
M = "{b:'2',n:'North Gate',nm:3000,p:[8.75,16.5]"
pre(M, S19 + ": OUT 10:00 (Capt Sandeep) 8¾–16½ → OTB; DSM London in on completion. " + D19 + ": 1,004 MT in 24 h, 23,940 of 27,000 loaded — 3,060 MT still on the 0700 sheet, so she leaves three hours later either short or with the last parcel done that morning. " + D18 + ": RE-MADE FAST CJ-2 14:05, re-commenced 15:50 on 17 Nov. " + L + ": BITUMEN row · BIT(GEN) · ETC 18 Nov 01:20 — she lay 33 h past it, inside the two days allowed to bag cargo under General. " + PG19 + " had her out 18 Nov 18:00 (9.5 m), night sailing.")
sub(M, "f:'11-17 10:00',t:'11-18 01:20',est:1", "f:'11-17 14:05',t:'11-19 10:00',lt:'11-18 01:20'")
add(M, '2', 'DSM London', (8.5, 16.5), 'Rice bags + wheat flour', 26700, 'MT', 'GEN', '11-19 12:30', '11-28 10:00',
    S19 + ": IN o/c (Capt Sandeep, after he takes North Gate out at 10:00) OTB → 8½–16½ → about 12:30 — under berthing at the time of this update. " + PG19 + ": CJ-02, 8½–16½, BIT(GEN), NIGHT SAILING / BERTHING. " + D19 + ": \"BERTHING TODAY\" — rice bags 22,500 MT + wheat flour 4,200 MT to load for Somalia (the list has 32,700 MT rice / sugar bags). " + L + ": reported 12 Oct 23:05, READINESS DECLARED 16 Nov 11:00, GEN 1 — the senior General vessel, taken against the Bitumen slot as North Gate was. No norm or ETC printed yet: 26,700 MT at the 3,000 norm North Gate had → about 28 Nov 10:00, the board's estimate.",
    nm=3000, est=True, extra="slot:'BIT',via:'Bitumen slot · as General (\"BIT(GEN)\")',")
# ---- CJ-3
M = "{b:'3',n:'Merchia',nm:21160,p:[19,27.75]"
sub(M, "t:'11-16 13:00'", "t:'11-16 13:15'")
M = "{b:'3',n:'Rahma',p:[17.5,25.5]"
pre(M, D19 + ": COMPLETED 16:15 on 18 Nov, LET GO 03:35 on the 19th — 11,763 MT / 9,880 pipes in all; two minutes inside her list ETC. " + L + ": PROJECT/STEEL · CJ-3 · 17½–25½ · made fast 16 Nov 15:54, commenced 17:30 · norm 3,000 · ETC 19 Nov 03:37. " + PG19 + ": outward readiness 19 Nov 03:37 (8.2 m).")
sub(M, "f:'11-16 16:00',t:'11-18 04:00',est:1", "f:'11-16 15:54',t:'11-19 03:35',lt:'11-19 03:37'")
add(M, '3', 'Sea Gautham', (17.5, 22.25), 'Ammonium sulphate', 7000, 'MT', 'COASTAL', '11-19 05:40', '11-21 05:40',
    D19 + ": MADE FAST 05:40 on 19 Nov — ammonium sulphate 7,000 MT to load, not commenced at the time of the sheet. " + PG19 + ": 17½–22¼, \"SPACE A/C\", NIGHT BERTHING — a 110 m coaster put in the quay left west of Propel Confidence (23½–31¾); she uses no priority place. " + L + ": CSTL 1 · 24H 2 · GEN 18, reported / ready 12 Nov 13:50, remark \"DISPUTE (WAITING FOR SHIPPER'S CONFIRMATION)\" — the dispute is evidently over. No norm or ETC printed yet: two days is the board's estimate.",
    est=True, extra="slot:'SPC',via:'Space a/c — free quay, no priority place used (programme 19.11)',")
# ---- CJ-4
M = "{b:'4',n:'African Hornbill',nm:11500,p:[27.25,36]"
pre(M, D17 + ": work stopped 20:20, LET GO 22:00, at OTB 23:50 on 16 Nov — 14,500 of 25,000 MT ball clay loaded, 10,500 left behind. " + L + " has her back on the waiting list for windmill blades (54), steel pipes and I-beams, 11,531.5 MT EXP — SGR 2 · GEN 12.")
M = "{b:'4',n:'Phoenix Coral',p:[26.5,32]"
pre(M, D18 + ": COMPLETED 13:00, LET GO 15:30 on 17 Nov — 1,926 MT / 269 coils in 13 h. " + D17 + ": MADE FAST 00:06, commenced 02:00 on 17 Nov. SIGNAL 17 Nov: RT OUT 15:30 (Capt Madaan).")
sub(M, "f:'11-17 00:30',t:'11-18 00:30',est:1", "f:'11-17 00:06',t:'11-17 15:30'")
# ---- CJ-5
M = "{b:'5',n:'Princess Joanna',nm:17193,p:[37,45.75]"
pre(M, D17 + ": COMPLETED 18:30, LET GO 22:40 on 16 Nov — 25,000 MT. NIGHT SIGNAL 16 Nov (disp 2005): OUT 22:30 (Capt Verma) — the programme had 08:00 on the 17th.")
sub(M, "f:'11-16 00:15',t:'11-17 08:00',lt:'11-16 09:35'", "f:'11-16 00:15',t:'11-16 22:40',lt:'11-16 09:35'")
M = "{b:'5',n:'Saga Viking',nm:3450,p:[33,41.75]"
pre(M, L + ": GENERAL · CJ-5 · 33–41¾ · MADE FAST 17 Nov 01:24, commenced 04:05 · norm 3,450 · ETC 21 Nov 18:58. " + D19 + ": 5,014 MT in 24 h on 2 gangs a shift, 11,480 of 16,038 off, 4,558 left → ~20 Nov 05:00 at this rate, a day and a half inside the permissible time. " + PG19 + ": \"NIGHT WARPING AT PANELS\" → 32¾–41½, a quarter panel west, to make room down the line for the shift of Propel Confidence.")
sub(M, "f:'11-17 10:00',t:'11-22 06:30',est:1", "f:'11-17 01:24',t:'11-21 18:58'")
sub(M, "p:[33,41.75]", "p:[32.75,41.5]")
# ---- CJ-6
M = "{b:'6',n:'Truong Minh Dream',nm:17193,p:[46.75,54.5]"
pre(M, "SIGNAL 17 Nov: SHIFT 15:30 (Capt Pathak) 46¾–54½ → 42¾–51½.")
sub(M, "f:'11-16 06:10',t:'11-17 16:00',est:1", "f:'11-16 06:10',t:'11-17 15:30'")
M = "{b:'6',n:'Truong Minh Dream',nm:17193,p:[42.75,51.5]"
pre(M, L + ": GOV · CJ-6 · 42¾–51½ · norm 17,193 · ETC 19 Nov 13:46. " + D19 + ": 12,852 MT in 24 h, 42,725 of 55,600 off, 12,875 left → ~20 Nov 07:00 at this rate, 17 h past the permissible time. NO OUTWARD ROW on programme 19.11 or the 19 Nov signal — she is not being moved today. " + PG19 + ": \"NIGHT WARPING AT PANELS\" → 42½–51¼.")
sub(M, "f:'11-17 16:30',t:'11-19 13:46'", "f:'11-17 16:00',t:'11-19 13:46'")
sub(M, "p:[42.75,51.5]", "p:[42.5,51.25]")
# ---- CJ-7 / CJ-8
for M in ("{b:'7',n:'Cape Venture',nm:42500,p:[55.75,67.5]", "{b:'8',n:'Cape Venture',nm:42500,p:[59.25,67.5]"):
    pre(M, D18 + ": COMPLETED 12:30, LET GO 16:35 on 17 Nov — 165,051 MT in all. SIGNAL 17 Nov: RT OUT 16:30 (Capt Bali; 17:00 → 16:00 → 16:30).")
    sub(M, "t:'11-17 17:00',lt:'11-17 18:17'", "t:'11-17 16:35',lt:'11-17 18:17'")
M = "{b:'7',n:'Propel Confidence',nm:30000,p:[52.5,58.75]"
pre(M, D19 + ": work stopped 02:30, LET GO 03:40 on 19 Nov — SHIFTED TO CJ-4 with 10,000 MT done at CJ-7 (the next line). " + L + ": she is printed under COASTAL with the pellet norm 21,160 and ETC 20 Nov 11:47 — and the Sr No 7 row of the at-berth sheet reads NIL: she holds the plain Coastal place, not a 30K / 25K quote as the board read programme 17.11. " + D18 + ": MADE FAST 19:30, commenced 21:15 on 17 Nov.")
sub(M, "cat:'COASTAL',via:'30k/25k quote (Sr No 7)',f:'11-17 19:00',t:'11-19 20:00',est:1", "cat:'COASTAL',f:'11-17 19:30',t:'11-19 03:40',lt:'11-20 11:47'")
sub(M, "nm:30000,p:[52.5,58.75]", "nm:21160,p:[52.5,58.75]")
M = "{b:'7',n:'Propel Confidence',nm:21160,p:[52.5,58.75]"
add(M, '7', 'Meghna Prestige', (52.25, 58.75), 'Coal in bulk', 60500, 'MT', 'HP', '11-19 07:30', '11-20 19:30',
    D19 + ": MADE FAST 07:30 on 19 Nov, not commenced at the time of the sheet — coal 60,500 MT IMP. " + PG19 + ": CJ-07, 52¼–58¾, HP(42.5K), 42,500 MTPD — the berth was cleared for her by shifting Propel Confidence to CJ-4 at the port's convenience. " + L + ": HP 3 · SGR 6 · 8K 10 · GEN 24, reported / ready 15 Nov 12:06. No ETC printed yet: 60,500 MT at the 42,500 quote is 34 h of work → about 20 Nov 19:30, the board's estimate. HP time is enforced: Evangelia D was taken off CJ-16 unfinished on 17 Nov when hers ran out.",
    nm=42500, est=True)
add(M, '4', 'Propel Confidence', (23.5, 31.75), 'Iron ore pellets', 54918, 'MT', 'COASTAL', '11-19 05:00', '11-20 11:47',
    D19 + ": \"(FROM CJ 07) RE-MADE FAST 05:00, RE-COMMENCED 06:40\" on 19 Nov — 19,100 MT in the 24 h across the two berths, 29,100 of 54,918 off, 25,818 left → ~20 Nov 15:30 at this rate. " + PG19 + ": \"NIGHT SHIFTING FROM CJ-07 … PORT C.\" → 23½–31¾ (the row prints CJ-03; she lies across the CJ-3 / CJ-4 line) — moved on the PORT'S account to give the deep berth CJ-7 to the HP vessel Meghna Prestige. " + L + ": COASTAL · norm 21,160 · ETC 20 Nov 11:47 (printed while she was still at CJ-7).",
    nm=21160)
M = "{b:'8',n:'Vishva Bandhan',nm:8050,p:[59.5,68]"
pre(M, L + ": GOV · CJ-8 · 59½–68 · MADE FAST 17 Nov 18:30, commenced 20:45 · norm 9,258 · ETC 22 Nov 14:33. " + D19 + ": 12,755 MT in 24 h, 17,650 of 44,000 off, 26,348 left → ~21 Nov 08:30 at this rate, 30 h inside the permissible time. SIGNAL 17 Nov: IN o/c (Capt Madaan, after Phoenix Coral 15:30).")
sub(M, "f:'11-17 19:30',t:'11-23 11:40',est:1", "f:'11-17 18:30',t:'11-22 14:33'")
sub(M, "nm:8050,p:[59.5,68]", "nm:9258,p:[59.5,68]")
# ---- CJ-9 (GFPL)
M = "{b:'9',n:'Leya',nm:20000,p:[69.25,79.5]"
pre(M, D17 + ": COMPLETED 19:30 on 16 Nov, LET GO 05:20 on the 17th — 89,000 MT. NIGHT SIGNAL 16 Nov (disp 2005): RT OUT 05:00 (Capt Yadav).")
sub(M, "f:'11-13 08:18',t:'11-17 05:00',lt:'11-17 21:06'", "f:'11-13 08:18',t:'11-17 05:20',lt:'11-17 21:06'")
M = "{b:'9',n:'Honor Star',nm:20000,p:[69.25,79.25]"
pre(M, D18 + ": MADE FAST 08:00, commenced 10:30, COMPLETED 23:15 on 17 Nov, LET GO 03:20 on the 18th — 24,000 MT coal in 13 h. SIGNAL 18 Nov: RT OUT 03:00 (Capt Deepak; 08:30 struck).")
sub(M, "f:'11-17 08:00',t:'11-18 14:00',est:1", "f:'11-17 08:00',t:'11-18 03:20'")
add(M, '9', 'Seacon Monaco', (69, 76.75), 'Soda ash in bulk', 41000, 'MT', 'PPP', '11-18 06:36', '11-20 09:48',
    L + ": GFPL · CJ-9 · 69–76¾ · MADE FAST 18 Nov 06:36 · norm 20,000 · ETC 20 Nov 09:48. " + D19 + ": commenced 08:35 on 18 Nov — 12,885 MT in her first 22½ h (about 13,800 a day), 28,115 of 41,000 left → ~21 Nov 08:00 at that rate, a day past the list ETC. SIGNAL 18 Nov: IN o/c (Capt Deepak) → 69–76¾. " + PG18 + ": CJ-09, GFPL. She had waited since 15 Nov for this berth (remark \"10K CJ-09\").",
    nm=20000)
# ---- CJ-13
M = "{b:'13',n:'African Peacock',nm:3450,p:[112.5,124.5]"
pre(M, D19 + ": COMPLETED 12:00, LET GO 14:45 on 18 Nov — 36,926 CBM / 282,103 pcs; a day and a quarter inside her list ETC (19 Nov 18:34). SIGNAL 18 Nov: OUT 15:00 (Capt Pankaj), Rome Trader in on completion.")
sub(M, "f:'11-08 23:42',t:'11-19 18:34'", "f:'11-08 23:42',t:'11-18 14:45',lt:'11-19 18:34'")
add(M, '13', 'Rome Trader (salt, next call)', (113, 125.25), 'Salt in bulk', 55275, 'MT', 'SAAGAR', '11-18 17:00', '11-21 09:30',
    "MIHIR & COMPANY · " + D19 + ": MADE FAST 17:00, COMMENCED 19:25 on 18 Nov at CJ-13 — 10,324 MT loaded by 0700 on the 19th, the first 11½ h, on two shifts of 4 gangs (about 21,400 MT a day); 44,951 of 55,275 MT left → about 21 Nov 09:30 at that rate. That is the board's estimate — no norm or ETC is printed for her yet (list 18.11 has only \"B'TODAY\"). " + L + ": SAAGAR · CJ-13 · 113–125¼ · remark \"SGR- NEELKANTH\". SIGNAL 18 Nov (amended): IN o/c (Capt Pankaj) OTB → 113–125¼ behind African Peacock's 15:00 sailing. " + PG18 + " had named CJ-15 (145½–157¾, after Enishi) — the 18 Nov signal put her at CJ-13, which freed first. THE SAAGAR BULK PLACE, as the board read it on 14 Nov: the first SAAGAR berth a log vessel left went to the waiting bulk vessel, and ML Egret took the other.",
    est=True)
# ---- CJ-14
M = "{b:'14',n:'Theometor',nm:4025,p:[125.5,139.5]"
pre(M, D19 + " (sailing vessels): SAILED 11:10 on 18 Nov. " + D18 + ": COMPLETED 06:30 on 17 Nov — 45,000 MT; she then lay 28 h idle alongside. SIGNAL 18 Nov: RT OUT 11:00 (Capt Pankaj). " + PG18 + ": outward readiness 18 Nov 17:00 (11.3 m) → Yara J.")
sub(M, "f:'11-02 21:06',t:'11-16 02:06'", "f:'11-02 21:06',t:'11-18 11:10',lt:'11-16 02:06'")
add(M, '14', 'Yara J', (126.5, 141.75), 'Rice bags', 11666, 'MT', '24H', '11-18 20:30', '11-19 20:30',
    D19 + ": \"FROM OTB 16:25, RE-MADE FAST 20:30, RE-COMMENCED 21:50\" on 18 Nov — 1,589 MT in the first 9 h on 4 gangs; of 30,000 MT, 21,083 are off (19,494 at midstream), 8,917 LEFT at 0700 on the 19th. " + L + ": 24 HRS · CJ-14 · 126½–141¾ · \"B'TODAY (TOTAL - 30000MT)\" · 11,666 MT for the berth; she was given 24H 1 at the 17 Nov meeting (revised list 17.11). " + PG18 + ": CJ-14, 127–142½, 24 HRS, after Theometor. A 24-hr berth: she must leave within 24 h of berthing → 19 Nov 20:30. At about 4,200 MT a day she will have some 6,500 MT still on board then — no outward row for her on programme 19.11 or the 19 Nov signal, so the hour is the rule, not an order.",
    est=True)
# ---- CJ-15
M = "{b:'15',n:'Enshi',nm:3450,p:[142,154.75]"
pre(M, D19 + ": COMPLETED 14:30, LET GO 19:30 on 18 Nov — 33,134 CBM / 230,822 pcs; 19 h inside her list ETC (19 Nov 09:34). " + PG18 + ": outward readiness 18 Nov 17:30 (6.29 m).")
sub(M, "f:'11-15 19:00',t:'11-19 09:34',est:1", "f:'11-15 19:00',t:'11-18 19:30',lt:'11-19 09:34'")
add(M, '15', 'ML Egret', (143.5, 156.75), 'JAS pine logs', 42885, 'CBM', 'SAAGAR', '11-18 21:45', '12-01 09:55',
    D19 + ": MADE FAST 21:45, COMMENCED 23:35 on 18 Nov at CJ-15 — 7,734 pcs / 2,695 CBM by 0700, 40,190 CBM left. " + L + ": SAAGAR · CJ-15 · 143½–156¾ · \"B'TODAY\" · 42,885 CBM — the SAAGAR break-bulk place, SGR 1. No norm or ETC printed yet: 42,885 CBM at the 3,450 norm the last two log vessels had is 12½ days → about 1 Dec 10:00, the permissible time as the board works it out. African Peacock and Enishi each finished about a day inside theirs.",
    nm=3450, est=True)
# ---- CJ-15A
M = "{b:'15A',n:'Tug Chandra Sun + barge Victoria 251',p:[166.5,171.75]"
pre(M, D18 + ": COMPLETED 19:00, LET GO 20:15 on 17 Nov — 4,114 MT / 1,532 pipes. " + D17 + ": made fast 09:36, commenced 11:00 on 16 Nov. SIGNAL 17 Nov: OUT 20:00 (Capt G Raj).")
sub(M, "f:'11-16 08:00',t:'11-17 16:00'", "f:'11-16 09:36',t:'11-17 20:15'")
M = "{b:'15A',n:'Bristol (salt, next call)',nm:46000,p:[158.75,169]"
pre(M, S19 + ": RT OUT 20:30 (Capt Yadav) 158¾–169 → OTB — 12 h after her list ETC. " + D19 + ": 41,022 MT in 24 h on 5 gangs a shift, 50,222 of 63,200 loaded, 12,978 left → cargo done about 14:30 on the 19th at this rate; the 20:30 is the tide for her loaded draught (13.3 m). " + L + ": HP · CJ-15A · 158¾–169 · MADE FAST 17 Nov 21:30, commenced 22:30 · norm 46,000 · ETC 19 Nov 08:28. " + PG19 + ": outward readiness 19 Nov 08:28 (13.3 m) → Heng Yuan Fa Zhan.")
sub(M, "f:'11-17 18:00',t:'11-19 08:00',est:1", "f:'11-17 21:30',t:'11-19 20:30',lt:'11-19 08:28'")
add(M, '15A', 'Heng Yuan Fa Zhan', (161.75, 169), 'Windmill blades & accessories', 1895, 'MT', 'STL', '11-19 21:30', '11-21 21:30',
    S19 + ": IN 18:45 (Capt Deepak — the hour he boards at OTB) → 161¾–169; she can only come alongside once Bristol has left at 20:30 → about 21:30, the board's estimate. " + PG19 + ": CJ-15A, 161¾–169, PROJ, after Bristol. " + D19 + ": \"BERTHING TODAY\" — windmill blades and accessories 1,895 MT IMP. " + L + ": STL 1 · GEN 9, ready 10 Nov. A project vessel has no norm: two days is the board's estimate (Feng Hai Da took 28 h for 48 blades on 1–2 Nov).",
    est=True)
# ---- CJ-16
M = "{b:'16',n:'Evangelia D',nm:50000,p:[173.5,188]"
pre(M, D18 + ": WORK STOPPED 18:00, LET GO 19:15 on 17 Nov — \"SHIFTED TO OTB\" with 7,716 MT of 60,216 still to load (45,000 on her first day, 7,500 on the second). SIGNAL 17 Nov: her RT OUT 17:15 was struck — \"(OUT IDLE) VSL NOT READY FOR SAILING\" — and she was moved off all the same. So the HP berth is taken back when the quoted time is over, finished or not. " + D17 + ": made fast 07:54, commenced 11:15 on 16 Nov.")
sub(M, "f:'11-16 08:30',t:'11-17 17:00'", "f:'11-16 07:54',t:'11-17 19:15',lt:'11-17 17:00'")
M = "{b:'16',n:'HN Doris (salt, next call)',nm:46000,p:[171.25,188]"
pre(M, S19 + ": RT OUT o/c (Capt Deepak, after he berths Heng Yuan Fa Zhan) 171¼–188 → OTB → about 22:00, the board's estimate; Ocean Kudos follows. " + D19 + ": ONLY 17,542 MT in 24 h on 3 gangs a shift against the 46,000 quote — 33,142 of 75,000 loaded, 41,858 MT LEFT at 0700 on the 19th. At that pace she cannot finish before the 21st, yet she is signalled out tonight: either the pace picks up sharply, or she leaves the berth with cargo still to load, as Evangelia D did on the 17th. " + L + ": HP · CJ-16 · 171¼–188 · MADE FAST 17 Nov 21:12, commenced 18 Nov 00:30 · norm 46,000 · ETC 19 Nov 14:19. " + PG19 + ": outward readiness 19 Nov 14:19 (14.0 m) → Ocean Kudos.")
sub(M, "f:'11-17 19:00',t:'11-19 15:00',est:1", "f:'11-17 21:12',t:'11-19 22:00',lt:'11-19 14:19',est:1")
add(M, '16', 'Ocean Kudos', (171.5, 188), 'Salt in bulk', 70190, 'MT', 'HP', '11-20 00:30', '11-21 18:00',
    S19 + ": IN o/c (Capt Yadav, after he takes Bristol out at 20:30) OTB → 171½–188 — once HN Doris is clear, about 00:30 on the 20th, the board's estimate. " + PG19 + ": CJ-16, 171½–188, HP(42.5K), after HN Doris; sailing draught 14.1 m. " + L + " (ETA sheet): salt in bulk 70,190 MT EXP, 225 m, ETA / readiness 18 Nov 15:00, HP Y · 8K Y · 30K/25K/10K Sr No 7, agent True Blue — she arrived on the 18th and takes an HP place the next day at 42,500 MTPD, past Gokova-M (HP 1), Belmoira (HP 4) and Lila Tokyo (HP 5). 70,190 MT at the quote is 40 h of work → about 21 Nov 18:00, the board's estimate.",
    nm=42500, est=True)

# ================= name maps =================
B.rep("Object.assign(LOA,{'New Bliss':175.6,", "Object.assign(LOA,{'DSM London':180,'Sea Gautham':109.8,'Meghna Prestige':199.9,'Seacon Monaco':179.99,'Rome Trader (salt, next call)':189.9,'Yara J':199.99,'ML Egret':199.9,'Heng Yuan Fa Zhan':139.8,'Ocean Kudos':225}); // list 18.11\nObject.assign(LOA,{'New Bliss':175.6,")
B.rep("Object.assign(AG,{'Belmoira':'Cross Trade','Sheng Tai':'Synergy',",
      "Object.assign(AG,{'Ocean Kudos':'True Blue','DSM London':'DBC','Seacon Monaco':'Cross Trade','Yara J':'DBC','ML Egret':'Cross Trade','Heng Yuan Fa Zhan':'Shantilal','Sea Gautham':'Atlantic Shg','Lila Tokyo':'Jeel Kandla','African Hornbill (blades, next call)':'Synergy','Tug Varahi + barge AKG 11':'JM Baxi','Haj Ali':'DBC','Yuan Hang Wei Ye (next call)':'Genesis','Parvraj':'Interocean','MSC Magali':'Genesis','Zheng Hui':'Interocean','Zheng Run':'Genesis','Asian Summit':'Atlantic Shg','Sand Topic':'Ben Line','Momentum Phonix':'Malara','Vishva Bandhan':'JM Baxi','New Bliss':'GAC Shg','Saga Viking':'Ben Line','Bristol (salt, next call)':'True Blue','HN Doris (salt, next call)':'Cross Trade','Porto Fiscardo':'DBC','Coral Bay':'Liladhar Pasoo'}); // list 18.11\n"
      "Object.assign(IE,{'Ocean Kudos':'EXP','DSM London':'EXP','Seacon Monaco':'IMP','Yara J':'IMP','ML Egret':'IMP','Heng Yuan Fa Zhan':'IMP','Sea Gautham':'EXP','Lila Tokyo':'IMP','African Hornbill (blades, next call)':'EXP','Tug Varahi + barge AKG 11':'EXP','Haj Ali':'EXP','Yuan Hang Wei Ye (next call)':'IMP','Parvraj':'IMP','MSC Magali':'IMP','Zheng Hui':'IMP','Zheng Run':'IMP','Asian Summit':'IMP','Sand Topic':'IMP','Momentum Phonix':'EXP','New Bliss':'EXP','Saga Viking':'IMP','Vishva Bandhan':'IMP','Bristol (salt, next call)':'EXP','HN Doris (salt, next call)':'EXP'});\n"
      "Object.assign(AG,{'Belmoira':'Cross Trade','Sheng Tai':'Synergy',")
B.rep("W.forEach(w=>{w.rep=REP[w.n]?h(REP[w.n]):w.rdy;});",
      "Object.assign(REP,{'DSM London':'10-12 23:05','African Hornbill (blades, next call)':'11-09 17:18','Porto Fiscardo':'11-13 15:05','Captainannis L':'11-13 16:54','Belmoira':'11-16 17:30','Ken Ann':'11-16 23:35','Sea Postman':'11-17 03:12','Sheng Tai':'11-17 04:45','Lila Tokyo':'11-17 19:05','Coral Bay':'11-18 03:18','African Tiger':'11-18 06:30'}); // list 18.11\n"
      "W.forEach(w=>{w.rep=REP[w.n]?h(REP[w.n]):w.rdy;});")
a, b = B.line_of("const ETA={'Dariya Priya':'11-16 09:00',")
B.s = B.s[:a] + ("const ETA={'Tug Varahi + barge AKG 11':'11-18 06:30','Flag Marina':'11-18 07:30','Ocean Kudos':'11-18 15:00','Tug Marigold + barge Alaacrity 666':'11-19 00:00','Haj Ali':'11-19 05:00','Yuan Hang Wei Ye (next call)':'11-19 09:00',"
                 "'Tai Keystone':'11-20 00:00','True Mariner':'11-20 00:00','Lolo Gate':'11-20 00:00','Gutian Trust':'11-20 00:00','Outlander':'11-20 00:00','Josco Taicang':'11-20 00:00','Parvraj':'11-20 00:00','MSC Magali':'11-20 00:00','Zheng Hui':'11-20 22:00',"
                 "'Hai Long 1':'11-21 00:00','Zheng Run':'11-21 00:00','Asian Summit':'11-21 04:00','Sand Topic':'11-21 23:00','Valentina Sea':'11-22 00:00','Princess Manissa':'11-22 00:00','Manta Omer Mecit':'11-22 10:00','KSS Edmond':'11-24 00:00','Momentum Phonix':'12-02 00:00'}; // expected sheet, list 18.11") + B.s[b:]
a, b = B.line_of("const NOHP=new Set(['Orion','Rome Trader (salt, next call)']);")
B.s = B.s[:a] + "const NOHP=new Set(['Orion']); // the HP place goes to the highest MTPD quote of the day, not to the rank (16 Nov). A ranked vessel passed over for a berth she could use is entered here. Rome Trader was (16 Nov) — she berthed under SAAGAR on 18 Nov and is off the list." + B.s[b:]

# ================= W — waiting list (list 18.11, revised) =================
w = B.wrow
for n in ('DSM London', 'Yara J', 'ML Egret', 'Heng Yuan Fa Zhan', 'Pioneer Fortune', 'Sea Gautham', 'Seacon Monaco', 'Meghna Prestige', 'Rome Trader (salt, next call)'):
    B.wdel(n)
w('Deniz ID', "no group rank printed now · readiness \"21 Oct 11:00 / NR\" · owners and charterers in dispute — still held", rk="", rdy="")
w('Safi Alfa', "GEN 2 · \"(24750- BALANCE) 32100 MT - TOTAL\"", rk="GEN:2")
w('Fortunelit', "GEN 3 · working at MS (DPR 19.11: sugar complete, 3,650 MT rice left)", rk="GEN:3")
w('Crystal O', "GEN 4 · working at MS", rk="GEN:4")
w('Mak 1', "GEN 5 · working at MS (DPR 19.11: 800 MT left)", rk="GEN:5")
w('Crystal Land', "8K 1 · GEN 6", rk="'8K':1,GEN:6")
w('Libra', "GEN 7 · docs NR (3,000 MT pending) · working at MS", rk="GEN:7")
w('Katerina K', "GEN 8", rk="GEN:8")
w('Uni Blossom', "SGR 1 (ML Egret has berthed) · 8K 3 · GEN 10 · Sr No 7", rk="SAAGAR:1,'8K':3,GEN:10")
w('Ariston Bulker', "GEN 11 · working at MS", rk="GEN:11")
w('Aboudi D', "GEN 13 · two shore cranes needed", rk="GEN:13")
w('African Loon', "GEN 14 printed · ship-to-ship transhipment, WORKING AT MS with Sheng Tai — she takes no berth; still held out of the projection", rk="GEN:14", rdy="")
w('Tan Bin 259', "8K 4 · GEN 15 · Sr No 7 · working at MRG 3 (DPR 19.11: 5,395 MT left)", rk="'8K':4,GEN:15")
w('Gokova-M', "HP 1 · 24H 1 · 8K 5 · GEN 16 — passed again on 18 and 19 Nov: the HP places went to Meghna Prestige (HP 3) and Ocean Kudos at 42,500, the 24-hr place to Yara J", rk="HP:1,'24H':1,'8K':5,GEN:16")
w('AG Varvara', "SGR 3 · GEN 17 · Sr No 7", rk="SAAGAR:3,GEN:17")
w('Xin Hai Tong 71', "SGR 4 · STL 2 · GEN 19", rk="SAAGAR:4,GEN:19")
w('Porto Fiscardo', "READINESS DECLARED 17 Nov 11:00 (was N/A) · 8K 6 · GEN 20 · remark \"CJ 1 - 4\" · 6.6 m · LP Bin Qasim", rk="'8K':6,GEN:20", rdy="11-17 11:00", dr="6.6")
w('Captainannis L', "N/A · 8K Y · DOC NR · working at MS · 7.06 m", dr="7.06")
w('Nord Copper', "CSTL 2 (behind Sea Gautham, who berthed on the 19th) · 8K 7 · GEN 21 · 30K/25K/10K Sr No 7", rk="COASTAL:2,'8K':7,GEN:21")
w('CD Glory', "SGR 5 · 8K 8 — NEW: the 6.5K / 8K rank is printed on the sheet revised after the 18 Nov meeting (the morning sheet and lists 16.11 / 17.11 had none) · GEN 22 · Sr No 7", rk="SAAGAR:5,'8K':8,GEN:22")
w('Stalo', "HP 2 · 8K 9 · GEN 23 · 30K/25K/10K — but she is FINISHING AT MIDSTREAM: DPR 19.11 has 39,514 of 43,400 MT off and 3,886 left at 0700 on the 19th. HELD out of the projection — she needs no berth", rk="HP:2,'8K':9,GEN:23", rdy="")
w('Dariya Priya', "REPORTED / READY 16 Nov 09:00 · SGR 7 · 8K 11 · GEN 25 · Sr No 7", rk="SAAGAR:7,'8K':11,GEN:25", rdy="11-16 09:00")
w('Belmoira', "REPORTED / READY 16 Nov 17:30 · HP 4 · 8K 12 · GEN 26 · 30K/25K/10K Sr No 7 · 6.71 m", rk="HP:4,'8K':12,GEN:26", rdy="11-16 17:30", dr="6.71")
w('Ken Ann', "REPORTED / READY 16 Nov 23:35 · 24H 3 · STL 3 · GEN 27 · 7.53 m", rk="'24H':3,STL:3,GEN:27", rdy="11-16 23:35", dr="7.53")
w('Sea Postman', "REPORTED / READY 17 Nov 03:12 · GEN 28 (no Govt rank printed — rock phosphate in bulk is Govt by the cargo rule)", rk="GEN:28", rdy="11-17 03:12")
w('Sheng Tai', "reported 17 Nov 04:45 · readiness 18 Nov 11:00 · \"DAUGHTER VESSEL — WORKING AT MS (STS)\" — no berth; held", rdy="", dr="6.6")
w('Coral Bay', "REPORTED 18 Nov 03:18 · N/A · 4.7 m", dr="4.7")
w('African Tiger', "REPORTED 18 Nov 06:30 · READINESS 18 Nov 11:00 (revised sheet) · SGR Y · 8K Y · Sr No 7 · 180 m, 10.8 m", rk="SAAGAR:98,'8K':98", rdy="11-18 11:00", dr="10.8", loa="180")
w('Tai Keystone', "ETA / readiness moved to 20 Nov 00:00", rdy="11-20 00:00")
w('Flag Marina', "ETA / readiness 18 Nov 07:30 — still on the ETA sheet at 0700 · HP Y · SGR Y", rk="HP:98,SAAGAR:98", rdy="11-18 07:30")
for n, t in (('True Mariner', 'ETA 20 Nov · N/A'), ('Lolo Gate', 'ETA 20 Nov · N/A'), ('Gutian Trust', 'ETA 20 Nov · N/A'), ('Outlander', 'ETA 20 Nov · N/A'), ('Josco Taicang', 'ETA 20 Nov · N/A'),
             ('Hai Long 1', 'ETA 21 Nov · N/A'), ('Valentina Sea', 'ETA 22 Nov · N/A'), ('Princess Manissa', 'ETA 22 Nov · N/A'), ('Manta Omer Mecit', 'ETA 22 Nov 10:00 · N/A'), ('KSS Edmond', 'ETA 24 Nov · N/A'),
             ('Tug Marigold + barge Alaacrity 666', 'ETA 19 Nov · N/A')):
    w(n, t)
# new rows — after the Manta Omer Mecit row
m = B._row('Manta Omer Mecit').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['African Hornbill (blades, next call)','Windmill blades / steel pipes / I-beams',11532,'MT',199.98,null,'11-14 11:00',{SAAGAR:2,GEN:12},'LIST 18.11: NEW ROW — back on the waiting list after she left the 24-hr berth on 16 Nov with 10,500 MT of ball clay unloaded: 54 windmill blades (51,897 CBM) + steel pipes + I-beams, 11,531.5 MT EXP · reported 9 Nov 17:18, readiness 14 Nov 11:00 · SGR 2 · GEN 12 · re-anchored 17 Nov 00:06 · agent Synergy'],",
 " ['Lila Tokyo','Gypsum in bulk',72633,'MT',229,14.04,'11-17 19:05',{HP:5,GEN:29},'LIST 18.11: NEW · reported / ready 17 Nov 19:05 · HP 5 · GEN 29 · 30K/25K/10K Sr No 7 · remark \"CJ 7 & 8 , 13-16\" · 72,633 MT IMP · gearless, 229 m, 14.04 m · agent Jeel Kandla'],",
 " ['Tug Varahi + barge AKG 11','Coated pipes',4000,'MT',77,3.5,null,{COASTAL:98,STL:98},'LIST 18.11 (ETA sheet): NEW · ETA 18 Nov 06:30 · N/A · CSTL Y · STL Y · a barge, taken on free quay space — not projected · agent JM Baxi'],",
 " ['Haj Ali','Rice bags',10000,'MT',113.22,2.2,null,{},'LIST 18.11 (ETA sheet): NEW · ETA 19 Nov 05:00 · N/A · agent DBC'],",
 " ['Yuan Hang Wei Ye (next call)','Iron ore pellets',50455,'MT',190,6.4,null,{},'LIST 18.11 (ETA sheet): NEW · ETA 19 Nov 09:00 · N/A · remark \"TRANSHIPMENT\" · agent Genesis'],",
 " ['Parvraj','DAP',49500,'MT',189.9,11.66,null,{},'LIST 18.11 (ETA sheet): NEW · ETA 20 Nov · N/A · agent Interocean'],",
 " ['MSC Magali','Steam coal',100728,'MT',253.54,13.38,null,{HP:98},'LIST 18.11 (ETA sheet): NEW · ETA 20 Nov · N/A · HP Y · 30K/25K/10K · gearless · 253.54 m · agent Genesis'],",
 " ['Zheng Hui','DAP',66000,'MT',229,12.85,null,{},'LIST 18.11 (ETA sheet): NEW · ETA 20 Nov 22:00 · N/A · agent Interocean'],",
 " ['Zheng Run','Iron ore pellets',66100,'MT',229,7.1,null,{},'LIST 18.11 (ETA sheet): NEW · ETA 21 Nov · N/A · remark \"TRANSHIPMENT\" · agent Genesis'],",
 " ['Asian Summit','Petcoke',60499,'MT',199.98,null,'11-21 04:00',{},'LIST 18.11 (ETA sheet): NEW · ETA / readiness 21 Nov 04:00 · no group rank printed · agent Atlantic Shg'],",
 " ['Sand Topic','Petcoke',51292,'MT',199.9,12,null,{},'LIST 18.11 (ETA sheet): NEW · ETA 21 Nov 23:00 · N/A · agent Ben Line'],",
 " ['Momentum Phonix','Rice in bags',23000,'MT',150.52,5,null,{},'LIST 18.11 (ETA sheet): NEW · ETA 2 Dec · N/A · agent Malara'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
B.rep(" // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 16.11 (0700, the issue revised after the meeting)", " // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 18.11 (0700, the issue revised after the meeting)")

# ================= DPR 19.11 =================
def R(loc, n, ie, c, l24, upto, bal, g, hk, note, partial=False, comm=None):
    return "  {loc:'%s',n:'%s',ie:'%s',c:'%s',l24:%d,upto:%d,bal:%d,g:'%s',hk:%d,%s%snote:'%s'}" % (loc, q(n), ie, q(c), l24, upto, bal, g, hk, 'partial:1,' if partial else '', ("comm:'%s'," % comm) if comm else '', q(note))
rows = [
 R('CJ-1', 'New Bliss', 'EXP', 'Sugar bags', 7089, 13887, 20113, '4/4/4', 12, '7,089 MT in 24 h on 12 hooks (norm 6,500) — 20,113 left → ~22 Nov 03:00 at this rate, 7 h inside the list ETC (22 Nov 10:05)'),
 R('CJ-2', 'North Gate', 'EXP', 'Chick peas / rice J-bags', 1004, 23940, 3060, '4/4/4', 12, '1,004 MT in 24 h — 3,060 MT still on the sheet at 0700; signalled OUT 10:00 the same morning (DSM London in behind her)'),
 R('CJ-2', 'DSM London', 'EXP', 'Rice bags + wheat flour', 0, 0, 26700, '0/0/0', 0, '"BERTHING TODAY" — rice bags 22,500 MT + wheat flour 4,200 MT for Somalia'),
 R('CJ-3', 'Rahma', 'EXP', 'Steel pipes', 1180, 11763, 0, '2/2/2', 6, 'COMPLETED 16:15 on 18 Nov, LET GO 03:35 on the 19th — 11,763 MT / 9,880 pipes'),
 R('CJ-3', 'Sea Gautham', 'EXP', 'Ammonium sulphate', 0, 0, 7000, '0/0/0', 0, 'MADE FAST 05:40 on 19 Nov — 7,000 MT to load'),
 R('CJ-4', 'Propel Confidence', 'IMP', 'Iron ore pellets', 19100, 29100, 25818, '7/5/7', 19, 'two rows on the sheet: CJ-7 (work stopped 02:30, let go 03:40, shifted) and CJ-4 (re-made fast 05:00, re-commenced 06:40) — 19,100 MT in the 24 h, 25,818 left → ~20 Nov 15:30 at this rate (list ETC 20 Nov 11:47)'),
 R('CJ-5', 'Saga Viking', 'IMP', 'Kraft pulp', 5014, 11480, 4558, '2/2/2', 6, '5,014 MT / 2,507 units in 24 h — 4,558 left → ~20 Nov 05:00 at this rate (list ETC 21 Nov 18:58)'),
 R('CJ-6', 'Truong Minh Dream', 'IMP', 'DAP / TSP bulk', 12852, 42725, 12875, '4/4/4', 12, '12,852 MT in 24 h — 12,875 left → ~20 Nov 07:00 at this rate (list ETC 19 Nov 13:46)'),
 R('CJ-7', 'Meghna Prestige', 'IMP', 'Coal in bulk', 0, 0, 60500, '0/0/0', 0, 'MADE FAST 07:30 on 19 Nov, not commenced at the time of the sheet — HP at 42,500 MTPD'),
 R('CJ-8', 'Vishva Bandhan', 'IMP', 'Urea bulk', 12755, 17650, 26348, '4/4/4', 12, '12,755 MT in 24 h (norm 9,258) — 26,348 left → ~21 Nov 08:30 at this rate (list ETC 22 Nov 14:33)'),
 R('CJ-9', 'Seacon Monaco', 'IMP', 'Soda ash in bulk', 12885, 12885, 28115, '4/6/5', 15, 'COMMENCED 08:35 on 18 Nov — 12,885 MT in her first 22½ h; 28,115 left → ~21 Nov 08:00 at that rate (list ETC 20 Nov 09:48)', True, '11-18 08:35'),
 R('CJ-13', 'African Peacock', 'IMP', 'Pine logs', 823, 36926, 0, '2/0/0', 2, 'COMPLETED 12:00, LET GO 14:45 on 18 Nov — 36,926 CBM / 282,103 pcs'),
 R('CJ-13', 'Rome Trader (salt, next call)', 'EXP', 'Salt in bulk', 10324, 10324, 44951, '0/4/4', 8, 'MADE FAST 17:00, COMMENCED 19:25 on 18 Nov — 10,324 MT in the first 11½ h on two shifts of 4 gangs (about 21,400 a day); 44,951 left → ~21 Nov 09:30 at that rate · agent and stevedore Mihir', True, '11-18 19:25'),
 R('CJ-14', 'Yara J', 'IMP', 'Rice bags', 1589, 21083, 8917, '0/4/4', 8, 'from OTB 16:25, RE-MADE FAST 20:30, re-commenced 21:50 on 18 Nov — 1,589 MT at the berth; 19,494 MT had come off at midstream; 8,917 of 30,000 left · 24-hr berth', True, '11-18 21:50'),
 R('CJ-15', 'Enshi', 'IMP', 'Pine logs', 761, 33134, 0, '4/0/0', 4, 'COMPLETED 14:30, LET GO 19:30 on 18 Nov — 33,134 CBM / 230,822 pcs'),
 R('CJ-15', 'ML Egret', 'IMP', 'Pine logs', 2695, 2695, 40190, '0/4/4', 8, 'MADE FAST 21:45, COMMENCED 23:35 on 18 Nov — 7,734 pcs / 2,695 CBM by 0700; 40,190 CBM left', True, '11-18 23:35'),
 R('CJ-15A', 'Bristol (salt, next call)', 'EXP', 'Salt bulk', 41022, 50222, 12978, '5/5/5', 15, '41,022 MT in 24 h on 15 hooks (quote 46,000) — 12,978 left → cargo done ~14:30 on the 19th; signalled RT OUT 20:30'),
 R('CJ-15A', 'Heng Yuan Fa Zhan', 'IMP', 'Windmill blades & accessories', 0, 0, 1895, '0/0/0', 0, '"BERTHING TODAY" — behind Bristol'),
 R('CJ-16', 'HN Doris (salt, next call)', 'EXP', 'Salt bulk', 17542, 33142, 41858, '3/3/3', 9, 'only 17,542 MT in 24 h on 9 hooks against the 46,000 quote — 41,858 of 75,000 left → ~21 Nov 16:00 at this rate, yet she is signalled out on the evening of the 19th (list ETC 19 Nov 14:19)'),
 R('MS', 'Stalo', 'IMP', 'Coal in bulk', 12581, 39514, 3886, '1/1/1', 3, 'discharging at midstream — 3,886 of 43,400 MT left → done on the 19th; she will not need a berth'),
 R('MS', 'African Loon', 'IMP', 'Barite ore', 2715, 3215, 54535, '1/1/1', 3, 'mother vessel — ship-to-ship to Sheng Tai (daughter) at anchorage: 2,715 MT in the 24 h, 54,535 left'),
 R('MS', 'Libra', 'EXP', 'Rice bags', 1350, 12197, 10803, '1/1/1', 3, '1,350 MT in 24 h (another 1,400 at IFFCO) — 10,803 left'),
 R('MS', 'Crystal O', 'EXP', 'Sugar bags', 1500, 15385, 15815, '1/1/1', 3, '1,500 MT in 24 h — 15,815 left'),
 R('MS', 'Fortunelit', 'EXP', 'Sugar / rice bags', 861, 18850, 3650, '2/0/0', 2, 'sugar bags COMPLETED 14:50 (12,500 MT); rice 6,350 MT done, 3,650 left'),
 R('MS', 'MAK 1', 'EXP', 'Rice in J-bags', 0, 21088, 800, '0/0/0', 0, 'no work in the 24 h — 800 MT left'),
 R('MS', 'Captainannis L', 'EXP', 'Rice bags', 357, 1748, 16052, '1/1/1', 3, '357 MT in 24 h — 16,052 left'),
 R('MS', 'Ariston Bulker', 'EXP', 'Bentonite J-bags', 1084, 3530, 4470, '1/1/1', 3, '1,084 MT in 24 h — 4,470 left'),
 R('MRG-3', 'Tan Bin 259', 'EXP', 'NPK in jumbo bags', 1819, 6942, 5395, '2/2/2', 6, '1,819 MT in 24 h (another 1,500 at the Bunder area) — 5,395 left → ~3 days'),
 R('BA', 'Bon Voyage', 'IMP', 'Steel slab', 1334, 1334, 839, '', 0, 'MADE FAST 21:00, commenced 22:00 on 18 Nov at the barge berth (north) — 54 slabs / 1,334 MT; 839 left', True, '11-18 22:00'),
 R('OJ-1', 'Searay', 'IMP', 'CPO', 4763, 29999, 0, '', 0, 'COMPLETED 05:42 on 19 Nov — 29,999 MT; signalled OUT 08:30'),
 R('OJ-2', 'Rasheeda', 'IMP', 'Chemicals', 352, 6150, 0, '', 0, 'COMPLETED 08:18, LET GO 09:25 on 18 Nov'),
 R('OJ-2', 'Korea Chemi', 'IMP', 'Chemicals', 7144, 7144, 0, '', 0, 'MADE FAST 12:30, commenced 14:20 on 18 Nov, COMPLETED 07:25 on the 19th — 7,144 MT; signalled OUT 11:00'),
 R('OJ-3', 'Jag Pushpa', 'IMP', 'CDSBO', 9424, 26700, 17552, '', 0, 'shifted from OJ-7 on 18 Nov: work stopped 13:00, let go 15:30, RE-MADE FAST OJ-3 17:00, re-commenced 18:24. The OJ-3 row restarts its count (9,424 MT "up to date", balance 34,828); with the 17,276 MT discharged at OJ-7 the balance is 17,552 MT at most'),
 R('OJ-4', 'Avyaan', 'IMP', 'HSD', 16810, 31545, 3455, '', 0, '16,810 MT in 24 h — 3,455 left → done about noon on the 19th; signalled OUT 15:00'),
 R('OJ-6', 'Ishaan', 'IMP', 'MS', 3078, 29823, 0, '', 0, 'COMPLETED 12:12, LET GO 17:55 on 18 Nov'),
 R('OJ-6', 'Kestrel', 'EXP', 'VLSFO', 7585, 7585, 16415, '', 0, 'MADE FAST 19:00, commenced 21:00 on 18 Nov — 7,585 MT loaded in 10 h; 16,415 left', True, '11-18 21:00'),
 R('OJ-7', 'NV Sunshine', 'IMP', 'Propane', 10242, 10242, 13758, '', 0, 'LPG carrier — MADE FAST 20:30, commenced 22:12 on 18 Nov; 13,758 left', True, '11-18 22:12'),
 R('TT-1', 'Europa Graeca', 'IMP', 'Sugar bulk', 11394, 46388, 29289, '', 0, '11,394 MT in 24 h — 29,289 left → ~21 Nov 20:30 at this rate'),
 R('TT-3', 'Beagle', 'IMP', 'Coal in bulk', 27265, 62695, 14525, '', 0, '27,265 MT in 24 h — 14,525 left → ~19 Nov 19:45 at this rate'),
]
a = B.s.index("const DPR={d:'15.11.2026'"); e = B.s.index("\n ]};\n", a) + len("\n ]};\n")
old = B.s[a:e]
i1 = old.index(" tot:{"); i2 = old.index(" rows:[")
mid = old[old.index("\n", i1) + 1:i2]   # the comment line(s) between tot and rows
NEWDPR = ("const DPR={d:'19.11.2026',asOf:'11-19 07:00',src:'DPA Traffic Dept Daily Performance Report, position 0700 hrs 19 Nov (xlsx from Mihir, 19 Nov 12:29 — with DPR 17.11 and 18.11, used for the completion and let-go hours of the two days before)',\n"
          " tot:{dry:146852,dryL:77044,dryU:69808,ms:21052,kict:5773,tuna:44086,oj:59398,vad:230928,all:508089,gangs:'PR 18 · 41 + 12 W gangs demanded / 41 + 12 W supplied',rakes:'4',wb:792,sail:'Theometor · CJ-14 · 11:10'},\n"
          + mid + " rows:[\n" + ",\n".join(rows) + "\n ]};\n")
B.s = B.s[:a] + NEWDPR + B.s[e:]
B.save()
