#!/usr/bin/env python3
# apply52 — v255: PROGRAMME 23.11 (TF/SH/2102 dt 22 Nov 2026, xlsx), received 22 Nov 15:39, no text.
# Cargo jetties: CJ-14 tug Sagar 5 + barge OUT 23 Nov 17:30 → HAI NAM 81 in, 126½–141, CSTL(30K), provisional; Sanghi Sudarshan OUT 03:00 (no inward).
# Containers: CJ-11 Al Hadbaa in (night) · CJ-12 TCI Anand out 12:00 → Enzo 2. Oil: OJ-2 PVT Aurora out 07:00 → Rasheeda · OJ-4 Bow Fortitude out 07:00 → Al Mahboobah. Tuna: TT-03 MP Post Panamax in (ETA 22 Nov 18:30).
# The 22 Nov meeting is scored on the call frozen at 00:26 (Xin Hai Tong 71 → CJ-14): right berth, wrong vessel.
import re, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='PROGRAMME 23.11'); q = B.q
P = 'PROGRAMME 23.11'
def pre(m, t): B.note_prefix(m, q(t) + " ")
def sub(m, o, n): B.sub_entry(m, o, n)
B.rep("const NOW=h('11-22 12:18');", "const NOW=h('11-22 15:39');")
B.rep("const PROG_END=h('11-22 18:00'); // programme 22.11 (meeting of 21 Nov) covers till here", "const PROG_END=h('11-23 18:00'); // programme 23.11 (meeting of 22 Nov) covers till here")
B.rep("<i>Programme</i><b>22.11</b>", "<i>Programme</i><b>23.11</b>")
B.rep("· programme 22.11 · DPR 22.11 (position 07:00)", "· programme 23.11 · DPR 22.11 (position 07:00)")
B.rep("const PROG_SAIL=new Set(['New Bliss',", "const PROG_SAIL=new Set(['Tug Sagar 5 + barge Victoria 250','Sanghi Sundarshan','New Bliss',")
a, b = B.line_of("const CALL_FROZEN={d:'11-22',at:'11-22 00:26'")
B.s = B.s[:a] + "const CALL_FROZEN=null; // {d,at,basis,call} = the meeting call as it stood BEFORE the meeting, when papers written after it reach the board before the programme; null = show the live call" + B.s[b:]
# ---- V: sailings
M = "{b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133]"
pre(M, P + ": OUT readiness 23 Nov 17:30, 4.0 m, night sailing → MV HAI NAM 81 takes the berth (126½–141, CSTL(30K), provisional berthing). The board had her out about 14:00.")
sub(M, "f:'11-22 05:55',t:'11-23 14:00',est:1", "f:'11-22 05:55',t:'11-23 17:30'")
M = "{b:'14',n:'Sanghi Sundarshan',p:[135,141.75]"
pre(M, P + ": \"CJ-14A\" · OUT readiness 23 Nov 03:00, 3.7 m, night sailing — no inward vessel named for her space.")
sub(M, "f:'11-22 04:00',t:'11-23 04:00',est:1", "f:'11-22 04:00',t:'11-23 03:00'")
# ---- V: Hai Nam 81 programmed
a, b = B.line_of(" {b:'14',n:'Tug Sagar 5 + barge Victoria 250',p:[126.5,133]")
NEWV = " {b:'14',n:'Hai Nam 81',nm:30000,p:[126.5,141],c:'Salt in bulk',q:52000,u:'MT',cat:'COASTAL',via:'30k/25k quote (Sr No 7)',f:'11-23 19:30',t:'11-25 13:05',est:1,note:'" + q(P + ": CJ-14 · IN behind the tug Sagar 5 with barge (out readiness 23 Nov 17:30) · 126½–141 · CATEGORY CSTL(30K) · sailing draught 12.6 m · night sailing · PROVISIONAL BERTHING. About 19:30 alongside, est; 52,000 MT at her 30,000 quote → about 25 Nov 13:00, est. LIST 21.11 (revised): salt in bulk 52,000 MT · ETA / readiness 22 Nov 15:00 · HP Y · 8K Y · 30K/25K. The board had her at CJ-15A behind Belmoira (23 Nov 20:30) and Xin Hai Tong 71 at CJ-14: the port gave the first clean berth of the window to the coastal 30K quote, not to the SAAGAR line.") + "'},"
B.s = B.s[:a] + NEWV + "\n" + B.s[a:]
B.rep("'Tug Sagar 5 + barge Victoria 250':75});", "'Tug Sagar 5 + barge Victoria 250':75,'Hai Nam 81':189.94});")
B.wdel('Hai Nam 81')
# ---- meeting of 22 Nov: scored on the call frozen before the meeting
ML = "{d:'11-22',at:'11-22 00:26',basis:'list 21.11 (revised) · HM signal 21 Nov night sheet as amended (disp 22:30) · DPR 21.11 · programme 22.11',prog:'23.11',call:[['Xin Hai Tong 71','14']],got:[['Hai Nam 81','14']],note:'" + q("Right berth, wrong vessel. CJ-14 comes free behind the tug-and-barge (out readiness 23 Nov 17:30) and the port gave it to HAI NAM 81 — salt, coastal, a 30,000 quote (\"CSTL(30K)\", provisional berthing) — not to Xin Hai Tong 71 on the SAAGAR line through the vacant Govt place. The board had Hai Nam 81 at CJ-15A behind Belmoira two hours later: a coastal vessel with a 30K quote took the first clean berth of the window ahead of the SAAGAR vessel. Nothing else was programmed at the cargo jetties — no move at CJ-7 / 8 (Flag Marina stays, so no HP bid at this meeting, as the HP table said), at CJ-15A (Belmoira stays) or at CJ-5 (Vishva Bandhan is not on the sheet).") + "'},"
B.rep("const MEETLOG=[\n", "const MEETLOG=[\n " + ML + "\n")
# ---- TUNA
B.rep("next:'nobody named — MP Postpanamax 1 (coal 88,000 MT) is expected on 22 Nov 17:30'", "next:'" + q("PROGRAMME 23.11: MP Postpanamax 1 (coal 88,000 MT) IN at TT-03 — ETA 22 Nov 18:30, night berthing, arrival draught 14.15 m; no outward hour is printed for Marvelous Star") + "'")
B.rep("rem:'revised list 20.11: ETA / readiness 22 Nov 17:30 (24 Nov before)'", "rem:'" + q("PROGRAMME 23.11: TT-03 — IN, ETA 22 Nov 18:30, night berthing, arrival draught 14.15 m · revised list 20.11: ETA / readiness 22 Nov 17:30 (24 Nov before)") + "'")
B.rep("· DPR 22.11 · programme 21.11 ·", "· DPR 22.11 · programme 23.11 ·")
# ---- LIQ
B.s, k = re.subn(r"const LIQ=\{prog:'(?:[^'\\]|\\.)*',", "const LIQ={prog:'" + q("PROGRAMME 23.11 — OJ-2 PVT Aurora out 23 Nov 07:00 (6.5 m) → Rasheeda · OJ-4 Bow Fortitude out 23 Nov 07:00 (7.0 m) → Al Mahboobah · no other oil-jetty move printed") + "',", B.s, count=1)
assert k == 1
def liqout(bid, name, txt):
    a, b = B.line_of("  {b:'%s',prev:" % bid); ln = B.s[a:b]; i = ln.index("now:{n:'%s'" % name); j = ln.index(",note:'", i)
    assert 'etc:' not in ln[i:j]
    B.s = B.s[:a] + ln[:j] + ",etc:'11-23 07:00',note:'" + q(P + ": " + txt + " · ") + ln[j + len(",note:'"):] + B.s[b:]
liqout('OJ-2', 'PVT Aurora', "OUT readiness 23 Nov 07:00, 6.5 m → MT RASHEEDA in")
liqout('OJ-4', 'Bow Fortitude', "OUT readiness 23 Nov 07:00, 7.0 m → MT AL MAHBOOBA in")
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='22 Nov 2026 · 15:50 IST';", B.s, count=1)
B.save()

# ---- part 2 (same version): our vessel's reading, after the projection was read
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
a = B.s.index(" 'CD Glory':["); e = B.s.index("\n ]", a)
ent = "  {d:'22 Nov 15:39 · programme 23.11',exp:'11-25 21:05',b:'14',slot:'" + q("SAAGAR (SGR 3) — CJ-14, 25 Nov about 21:00, behind Hai Nam 81") + "',why:'" + q("Same night, CJ-14 instead of CJ-15A. Programme 23.11 put Hai Nam 81 (salt, coastal, 30K quote) into CJ-14 behind the tug-and-barge on the evening of 23 Nov — the berth the board had kept for Xin Hai Tong 71 — so the clean berth that opens for the SAAGAR line on the 25th is CJ-14, once Hai Nam 81 has loaded her 52,000 MT (about 25 Nov 13:00 at her quote). One estimate now instead of two: Hai Nam 81 is programmed, only her two days of loading are reckoned. If she runs a day over, CD Glory is on the 26th. Xin Hai Tong 71 moves to CJ-15 behind ML Egret on the morning of the 25th; AG Varvara to CJ-5 on the night of the 24th. Nothing is programmed for CD Glory yet.") + "'}"
B.s = B.s[:e] + ("" if B.s[e - 1] == ',' else ",") + "\n" + ent + B.s[e:]
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='22 Nov 2026 · 15:43 IST';", B.s, count=1)
B.save()
