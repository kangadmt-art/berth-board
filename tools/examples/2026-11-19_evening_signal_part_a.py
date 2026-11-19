#!/usr/bin/env python3
# apply22a — v176 (part 1): evening signal sheet of 19 Nov — "AMENDMENT & NEW SIGNAL", disp 1640, amended 1940 (Capt Omesh / Capt Madaan). Image from Mihir, 19 Nov 19:51.
import shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v175.html')
B = Board(P, list_tag='SIGNAL 19 Nov evening'); q = B.q
SG = "EVENING SIGNAL 19 Nov (\"amendment & new signal\", disp 1640, amended 1940)"
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

B.rep("const NOW=h('11-19 16:12');", "const NOW=h('11-19 19:51');")
B.rep("Signals to <b>19 Nov day sheet (disp 1040)</b>", "Signals to <b>19 Nov evening sheet (disp 1640, amended 1940)</b>")
B.rep("<summary>Sources, rules &amp; tide</summary><div>", "<summary>Sources, rules &amp; tide</summary><div>Received 19 Nov 19:51: the evening signal sheet of 19 Nov — \"amendment &amp; new signal\", dispatched 1640, amended 1940 (Capt Omesh / Capt Madaan). It sends African Hornbill to 175–188 (CJ-16) tonight; Ocean Kudos, programmed for that berth, is not on it · ")
B.rep("const BOARD_SRC='", "const BOARD_SRC='evening signal 19 Nov (disp 1640, amended 1940) · ")

# ---- CJ-16: HN Doris out 21:00 → AFRICAN HORNBILL (not Ocean Kudos)
M = "{b:'16',n:'HN Doris (salt, next call)',nm:46000,p:[171.25,188]"
pre(M, SG + ": RT OUT 21:00 (Capt Omesh) 171¼–188 → OTB — a fixed hour now (the morning sheet had \"on completion\"). Behind her the sheet sends AFRICAN HORNBILL to 175–188, not Ocean Kudos.")
sub(M, "f:'11-17 21:12',t:'11-19 22:00',lt:'11-19 14:19',est:1", "f:'11-17 21:12',t:'11-19 21:00',lt:'11-19 14:19'")
a, b = B.line_of(" {b:'16',n:'Ocean Kudos',nm:42500,p:[171.5,188],")
B.s = B.s[:a] + B.s[b + 1:]
B.add_after(M, " {b:'16',n:'African Hornbill (blades, next call)',p:[175,188],c:'Windmill blades / steel pipes / I-beams',q:11532,u:'MT',cat:'SAAGAR',slot:'SPJ',via:'SAAGAR project parcel · category not printed yet',f:'11-19 23:30',t:'11-24 04:00',est:1,note:'" + q(
    SG + ": IN 21:30 (Capt Deepak, his second job — the hour he boards) OTB → 175–188, marked for the ebb — behind HN Doris (out 21:00); about 23:30 alongside is the board's estimate. NEW: she is on neither programme 19.11 nor programme 20.11 — those gave CJ-16 to Ocean Kudos under HP(42.5K), who is not on tonight's sheet. LIST 19.11: SGR 2 · GEN 11 · 54 windmill blades (51,897 CBM) + steel pipes + I-beams, 11,531.5 MT EXP · reported 9 Nov 17:18, ready 14 Nov. Under which priority she takes the berth is not printed yet — the board counts her against no place until the next list says. No norm: about four days is the board's estimate.") + "'},\n")
# ---- CJ-15A
M = "{b:'15A',n:'Bristol (salt, next call)',nm:46000,p:[158.75,169]"
pre(M, SG + ": RT OUT 20:30 stands — pilot now Capt Verma.")
M = "{b:'15A',n:'Heng Yuan Fa Zhan',p:[161.75,169]"
pre(M, SG + ": IN 18:45 (Capt Deepak, first job) → 161¾–169 — unchanged.")
# ---- CJ-14
M = "{b:'14',n:'Yara J',p:[126.5,141.75]"
pre(M, SG + ": RT OUT 23:30 (Capt Deepak, third job) 126½–141¾ → OTB — as programmed.")
M = "{b:'14',n:'Nord Copper',p:[126.5,141.75]"
pre(M, SG + ": IN 22:30 (Capt Yadav — the hour he boards) OTB → 126½–141¾, behind Yara J (23:30) → about 01:00 on the 20th.")
sub(M, "f:'11-20 01:30',t:'11-21 21:00',est:1", "f:'11-20 01:00',t:'11-21 21:00',est:1")

# ---- waiting list: African Hornbill off, Ocean Kudos back
B.wdel('African Hornbill (blades, next call)')
m = B._row('Pioneer Fortune').search(B.s); e = B.s.index("],\n", m.start()) + 3
B.s = B.s[:e] + (" ['Ocean Kudos','Salt in bulk',70190,'MT',225,7.1,'11-18 16:06',{HP:0.5},'EVENING SIGNAL 19 Nov: BACK IN THE LINE — programme 19.11 and list 19.11 (\"B\\'TODAY\") gave her the far clean berth under HP(42.5K) behind HN Doris, but tonight\\'s sheet sends African Hornbill there and does not name her. She holds an HP allotment at 42,500 MTPD, so the board seats her first for the next HP place at a clean berth · salt in bulk 70,190 MT EXP · 225 m · reported / ready 18 Nov 16:06 · 30K/25K/10K Sr No 7 · agent True Blue'],\n") + B.s[e:]
B.rep("Object.assign(REP,{'Pioneer Fortune':'11-05 12:30',", "Object.assign(REP,{'Ocean Kudos':'11-18 16:06','Pioneer Fortune':'11-05 12:30',")
B.rep("Object.assign(LOA,{'Belmoira':199.92,", "Object.assign(LOA,{'African Hornbill (blades, next call)':199.98,'Belmoira':199.92,")

# ---- liquid
a, b = B.line_of("  {b:'OJ-1',prev:"); ln = B.s[a:b]
o1 = "f:'11-19 19:30'"; o2 = "note:'signal 19 Nov: IN 17:15 (Capt Verma — the hour he boards) → OJ-1, FLOOD → about 19:30 est"
if ln.count(o1) != 1 or ln.count(o2) != 1: B.die('OJ-1 anchors')
ln = ln.replace(o1, "f:'11-19 20:00'").replace(o2, "note:'evening signal 19 Nov (disp 1640): IN 17:30 (Capt Omesh; \"1800\" written beside her name) → OJ-1, FLOOD → about 20:00 est — the morning sheet had 17:15, Capt Verma")
B.s = B.s[:a] + ln + B.s[b:]
a, b = B.line_of("  {b:'OJ-4',prev:")
B.s = B.s[:a] + "  " + js({'b': 'OJ-4',
  'prev': {'n': 'Avyaan', 'c': 'HSD', 'q': 35000, 'u': 'MT', 'ie': 'IMP', 'ag': 'Victory Shg', 'out': '11-19 15:00', 'outBy': 'signal 19 Nov (morning sheet): OUT 15:00 (Capt Karan) — DPR 19.11: 3,455 MT left at 0700, done about noon · list ETC 20 Nov 04:38 — the hour is the signal\'s, not yet confirmed'},
  'now': {'n': 'Bow Endeavour', 'c': 'Chemicals', 'q': 13047.17, 'u': 'MT', 'ie': 'IMP', 'loa': 159.73, 'f': '11-19 16:30', 'est': 1, 'nm': '475', 'rank': '', 'ag': 'GAC Shg',
          'note': 'signal 19 Nov (morning sheet): IN 14:00 (Capt Verma — the hour he boards) → OJ-4, behind Avyaan\'s 15:00 sailing → about 16:30 est · list 19.11: OJ-4 "B\'TODAY", chemicals 13,047 MT IMP, norm 475 MT/h, reported / ready 18 Nov 13:00'}}) + "," + B.s[b:]
B.rep("programme 20.11: outward readiness 20 Nov 01:00 (8.5 m), NIGHT SAILING · list 19.11: norm 500 MT/h, ETC 21 Nov 02:30", "programme 20.11: outward readiness 20 Nov 01:00 (8.5 m), NIGHT SAILING — evening signal 19 Nov: RT OUT 01:00 (Capt Yadav) · list 19.11: norm 500 MT/h, ETC 21 Nov 02:30")
B.rep("asOf:'11-19 16:12',\n berths:[", "asOf:'11-19 19:51',\n berths:[")
a = B.s.index("const LIQ={"); m0 = B.s.index(" moves:[\n", a) + len(" moves:[\n")
B.s = B.s[:m0] + "  " + js(['Evening signal · 19 Nov — "amendment & new signal" (disp 1640, amended 1940) — oil-jetty rows', [
  ['17:30', 'IN', 'Artigo', 'OTB → OJ-1', 'Omesh', '11-19 20:00', 'FLOOD · "1800" written beside her name · the morning sheet had 17:15, Capt Verma — est'],
  ['01:00', 'RT OUT', 'NV Sunshine (LPG/C)', 'OJ-7 → OTB', 'Yadav', '11-20 01:00', 'as programmed']]]) + ",\n" + B.s[m0:]

# ---- movement log
MVN = ['Evening signal · 19 Nov — "AMENDMENT & NEW SIGNAL" (disp 1640; amended 1940, Capt Omesh / Capt Madaan)', [
  ['17:30', 'IN', 'Arrabiata', 'OTB → 87–95 (KICT)', 'Verma', '11-19 17:30', 'FLOOD · container, not tracked'],
  ['18:45', 'IN', 'Heng Yuan Fa Zhan', 'OTB → CJ-15A · 161¾–169', 'Deepak', '11-19 21:30', 'job 1 · alongside once Bristol is out — est'],
  ['20:30', 'RT OUT', 'Bristol (salt, next call)', 'CJ-15A · 158¾–169 → OTB', 'Verma', '11-19 20:30', 'pilot changed (was Capt Yadav)'],
  ['21:00', 'RT OUT', 'HN Doris (salt, next call)', 'CJ-16 · 171¼–188 → OTB', 'Omesh', '11-19 21:00', 'a fixed hour now · 41,858 MT were still to load at 0700'],
  ['21:30', 'IN', 'African Hornbill (blades, next call)', 'OTB → CJ-16 · 175–188', 'Deepak', '11-19 23:30', 'job 2 · NEW — not on programme 19.11 or 20.11; Ocean Kudos (HP 42.5K) was programmed here · marked for the ebb — est'],
  ['22:00', 'SHIFT', 'Bon Voyage', 'barge basin → OTB', 'Omesh', '11-19 22:00', 'agent\'s request'],
  ['22:30', 'IN', 'Nord Copper', 'OTB → CJ-14 · 126½–141¾', 'Yadav', '11-20 01:00', 'alongside once Yara J is out — est'],
  ['23:30', 'RT OUT', 'Yara J', 'CJ-14 · 126½–141¾ → OTB', 'Deepak', '11-19 23:30', 'job 3 · as programmed'],
  ['o/c', 'IN', 'Flexi 2', 'OTB → 101–109½ (KICT)', 'Deepak', '11-20 01:30', 'job 4 · container, not tracked (programme 20.11 had Konrad for 101–109)'],
  ['—', '—', 'PMS / standby', 'Capt Verma: on completion 1 hour · Capt Yadav: on completion, till vessel profile completion', '—', '11-20 01:00', ''],
  ['—', '—', 'Not on the sheet', 'Ocean Kudos (programmed for CJ-16, HP 42.5K) · Beagle out / Marvelous Star in at TT-3 (programme 20.11: 20:00, night)', '—', '11-19 20:00', '']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVN) + ",\n")

# ---- priority chart: a vessel berthed on a signal before the list prints her priority gets her own line in the at-berth table
B.rep("const order=CATS.map(c=>c.k).concat(['SPC','PPP']);let sr=0;", "const order=CATS.map(c=>c.k).concat(['SPC','PPP']);B.forEach(v=>{if(!order.includes(v.slot))order.push(v.slot);});let sr=0;")
B.rep("||{l:CL[k],p:k==='PPP'?'CJ-9 / CJ-10 · outside the priority places':'free quay · uses no priority place'};", "||{l:CL[k]||'Priority not printed yet',p:k==='PPP'?'CJ-9 / CJ-10 · outside the priority places':k==='SPC'?'free quay · uses no priority place':'berthed on a signal sheet · the list has not printed her priority'};")
B.save()
