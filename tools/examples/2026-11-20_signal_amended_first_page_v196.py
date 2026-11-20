#!/usr/bin/env python3
# apply41 — v196: the FIRST page of the HM signal sheet of 20 Nov as amended (disp 12:40 / 13:25 / 14:00, Capt Pathak) — image sent by Mihir at 20:26 (with a
# screenshot of the chat it came from, not archived). The image of 20:11 was the continuation sheet. This page still carries Konrad RT OUT 15:15 and SAFI ALFA IN "o/c"
# at 23–31¾ (Capt G. Raj + Neeraj) — not struck. Corrections: Jag Pushpa OUT is 17:45 (15:30 struck) — the board had read 14:45 off the other sheet;
# Meghna Prestige's first outward row is struck "postponed due to delay in cargo operation".   argv[1] = UPDATED
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
UPD = sys.argv[1]
SG = "HM SIGNAL 20 Nov (amended, first page, disp 14:00)"
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    if isinstance(o, dict): return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
m = re.search(r"const UPDATED='[^']*';", B.s); B.s = B.s[:m.start()] + "const UPDATED='%s';" % UPD + B.s[m.end():]
B.rep("const NOW=h('11-20 20:22');", "const NOW=h('11-20 20:26');")
B.rep("Signals to <b>20 Nov evening sheet, amended (disp 1240 / 1325 / 1400)</b>", "Signals to <b>20 Nov amended sheets, both pages (disp 1240 / 1325 / 1400)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>",
      "<summary>Sources, rules &amp; tide</summary><div>Received 20 Nov 20:26: the FIRST page of the amended signal sheet of 20 Nov — it carries Safi Alfa IN \"o/c\" at 23–31¾ (Capt G. Raj + Neeraj) and Konrad RT OUT 15:15; Jag Pushpa out 17:45; Meghna Prestige's first outward row struck \"postponed due to delay in cargo operation\" · ")
# ---- Safi Alfa: the row is on the sheet
M = "{b:'4',n:'Safi Alfa',nm:3000,p:[23,31.75]"
B.note_prefix(M, q(SG + ": IN \"o/c\" · Capt G. Raj + Neeraj · OTB → 23–31¾ — the row stands on the first page of the amended sheet, after Konrad's RT OUT (15:15) and behind Propel Confidence's shift (17:00). About 19:30 alongside is the board's estimate.") + " ")
B.sub_entry(M, "f:'11-20 23:00',t:'11-29 05:00',est:1", "f:'11-20 19:30',t:'11-29 01:30',est:1")
B.note_prefix("{b:'7',n:'Meghna Prestige',nm:42500,p:[52.25,58.75]", q(SG + ": her first outward row (\"o/c\", Capt Sud) is struck — \"POSTPONED DUE TO DELAY IN CARGO OPERATION\"; the continuation sheet has her RT OUT under Capt Omesh after Uni Blossom is in.") + " ")
# ---- MV
MVN = ['HM signal 20 Nov — amended sheet, FIRST page (dispatched 12:40 / 13:25 / 14:00) · Capt Pathak · received 20 Nov 20:26', [
  ['15:15', 'OUT', 'Konrad', 'CJ-12 · 101–109 → OTB', 'G. Raj + Neeraj', '11-20 15:15', 'RT OUT'],
  ['o/c', 'IN', 'Safi Alfa', 'OTB → CJ-4 · 23–31¾', 'G. Raj + Neeraj', '11-20 19:30', 'General (GEN 1) · behind Propel Confidence — est'],
  ['16:45', 'IN', 'Flexi-2', 'OTB → CJ-12 · 100–109½', 'Nikhil + Karan', '11-20 16:45', 'flood · 17:00 struck'],
  ['17:00', 'SHIFT', 'Propel Confidence', 'CJ-4 · 23½–31¾ → OTB', 'Sud + Dixit', '11-20 17:00', '"RT SHIFTING" (OUT struck) · agent\'s account'],
  ['17:45', 'OUT', 'Jag Pushpa', 'OJ-3 → OTB', 'Sandeep', '11-20 17:45', '15:30 struck'],
  ['o/c', 'IN', 'SG Friendship', 'OTB → OJ-3', 'Sandeep', '11-20 19:30', 'est'],
  ['o/c', 'IN', 'Orchids', 'OTB → OJ-6', 'Sud', '11-20 19:30', 'on arrival (ETA) · est'],
  ['18:15', 'OUT', 'Truong Minh Dream', 'CJ-6 · 42½–51¼ → OTB', 'Verma', '11-20 18:15', ''],
  ['o/c', 'IN', 'Hatnyanawati', 'OTB → OJ-2', 'Verma', '11-20 21:00', 'est'],
  ['19:00', 'OUT', 'Jeil Crystal', 'OJ-2 → OTB', 'Nikhil + Karan', '11-20 19:00', 'RT OUT'],
  ['o/c', 'IN', 'Parvraj', 'OTB → CJ-6 · 43–51¼', 'Nikhil + Karan', '11-20 21:30', 'est'],
  ['23:15', '—', 'Heng Yuan Fa Zhan', 'CJ-15A · 161¾–169 · turned round at the berth', 'Nikhil + Karan', '11-20 23:15', 'TURN AROUND · flood to ebb · agent\'s account · 16:00 struck'],
  ['o/c', '—', 'Meghna Prestige', 'CJ-7 · 52¼–58¾ → OTB — STRUCK OUT', 'Sud', '11-21 04:00', '"postponed due to delay in cargo operation" — re-entered on the continuation sheet, RT OUT under Capt Omesh']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")
B.rep("['14:45','OUT','Jag Pushpa','OJ-3 → OTB','Sandeep','11-20 14:45','15:30 on the 12:40 dispatch'],['o/c','IN','SG Friendship','OTB → OJ-3','Sandeep','11-20 17:00','est']",
      "['17:45','OUT','Jag Pushpa','OJ-3 → OTB','Sandeep','11-20 17:45','15:30 on the 12:40 dispatch (first read here as 14:45 — corrected from the first page)'],['o/c','IN','SG Friendship','OTB → OJ-3','Sandeep','11-20 19:30','est']")
B.rep("'HM signal 20 Nov — evening sheet, AMENDED (dispatched 12:40 / 13:25 / 14:00) · Capt Pathak · received 20 Nov 20:11'", "'HM signal 20 Nov — amended sheet, CONTINUATION page (dispatched 12:40 / 13:25 / 14:00) · Capt Pathak · received 20 Nov 20:11'")
B.rep("['—','—','Not on this sheet','Safi Alfa IN at 23–31¾ · Konrad OUT from 101–109 (both on the 12:40 dispatch, Capt G. Raj)','—','11-20 20:11','" + q("Mihir, 20:22: Safi Alfa WILL berth at CJ-4 under General — a row missing from an amended sheet is not a cancellation") + "']",
      "['—','—','Not on this page','Safi Alfa IN at 23–31¾ · Konrad OUT from 101–109 — both are on the FIRST page (received 20:26), Capt G. Raj + Neeraj','—','11-20 20:11','" + q("this is the continuation page; Mihir, 20:22: Safi Alfa berths at CJ-4 under General") + "']")
# ---- LIQ: Jag Pushpa 17:45
a, b = B.line_of("  {b:'OJ-3',prev:"); ln = B.s[a:b]
assert ln.count("out:'11-20 14:45',outBy:'HM SIGNAL 20 Nov (amended sheet, disp 14:00): Jag Pushpa OUT 14:45 · Capt Sandeep (15:30 on the 12:40 dispatch)") == 1
ln = ln.replace("out:'11-20 14:45',outBy:'HM SIGNAL 20 Nov (amended sheet, disp 14:00): Jag Pushpa OUT 14:45 · Capt Sandeep (15:30 on the 12:40 dispatch)", "out:'11-20 17:45',outBy:'HM SIGNAL 20 Nov (amended, disp 14:00): Jag Pushpa OUT 17:45 · Capt Sandeep (15:30 struck; the board first read 14:45)")
assert ln.count("ie:'IMP',loa:144.03,f:'11-20 17:00',est:1") == 1
ln = ln.replace("ie:'IMP',loa:144.03,f:'11-20 17:00',est:1", "ie:'IMP',loa:144.03,f:'11-20 19:30',est:1")
B.s = B.s[:a] + ln + B.s[b:]
B.rep("['14:45','OUT','Jag Pushpa','OJ-3 → OTB','Sandeep','11-20 14:45',''],['o/c','IN','SG Friendship','OTB → OJ-3','Sandeep','11-20 17:00','est']",
      "['17:45','OUT','Jag Pushpa','OJ-3 → OTB','Sandeep','11-20 17:45','15:30 struck'],['o/c','IN','SG Friendship','OTB → OJ-3','Sandeep','11-20 19:30','est']")
B.rep("signals to the evening sheet of 20 Nov as amended (disp 1400)',asOf:'11-20 20:11',", "signals to the amended sheets of 20 Nov, both pages (disp 1400)',asOf:'11-20 20:26',")
# ---- MEETLOG note, PRED row, LEARN
B.rep("Safi Alfa (GEN 1) goes into CJ-4 under General — signalled at 12:40, absent from the sheet as amended at 14:00, confirmed by Mihir at 20:22.'},",
      "Safi Alfa (GEN 1) goes into CJ-4 under General — by signal (IN \"o/c\", Capt G. Raj), confirmed by Mihir at 20:22.'},")
B.rep("['Safi Alfa','4','20 Nov 23:00','" + q("Mihir, 20 Nov 20:22: berths at CJ-4 under General (GEN 1) — the hour is the board's estimate") + "']",
      "['Safi Alfa','4','20 Nov 19:30','" + q("HM signal 20 Nov (amended, first page): IN o/c · Capt G. Raj + Neeraj · General (GEN 1) — Mihir, 20:22 · est") + "']")
b0 = B.s.index("\n];", B.s.index("const PREDLOG=["))
B.s = B.s[:b0] + ",\n {v:'Safi Alfa',predAt:'11-20 20:26',pb:'4',pt:'11-20 19:30',ab:'',at:'',src:'prog',note:'" + q("HM signal 20 Nov, amended sheet, first page — IN o/c at 23–31¾, Capt G. Raj + Neeraj; reading, not scored") + "'}" + B.s[b0:]
B.rep("Only a struck-out row is a cancellation; when the papers fall silent on a berthing, ask before taking it off.',st:'closed'},",
      "Only a struck-out row is a cancellation; when the papers fall silent on a berthing, ask before taking it off. AND (20:26): the image of 20:11 was only the CONTINUATION page — the first page of the same amended sheet, received at 20:26, still carries Safi Alfa IN \"o/c\" at 23–31¾ and Konrad RT OUT 15:15, neither struck. A signal sheet can run to two pages; rows missing from one page may simply be on the other. The first page also corrects one hour the board had misread on the continuation page — Jag Pushpa OUT 17:45, not 14:45 — and shows why Meghna Prestige is late: her first outward row is struck \"postponed due to delay in cargo operation\".',st:'closed'},")
B.save()
