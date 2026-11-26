#!/usr/bin/env python3
# apply75 — v279. Papers received 26 Nov 23:10, no text:
#   CORRIGENDUM Traffic/Shipping/587/Berthingpolicy/2026/3152 dt 26.11.2026 (image) — Bitumen priority, clause (iii) of the circular of 21.11.2026:
#     with no suitable bitumen vessel the berth runs under the 6,500 MTPD priority (Sr No 3(E)) "for Break Bulk Cargo only".
#   HM SIGNAL evening sheet 26/11/26, dispatch 18:10 (7 rows), and the same sheet extended at 21:00 with two "day signal" rows for 27 Nov (images). Capt Omesh for HM.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 26.11 (revised)'); q = B.q
SG = 'HM SIGNAL 26 Nov evening sheet (disp 18:10, extended 21:00)'
def js(o):
    if o is None: return 'null'
    if isinstance(o, bool): return 'true' if o else 'false'
    if isinstance(o, (int, float)): return repr(o)
    if isinstance(o, str): return "'" + q(o) + "'"
    if isinstance(o, (list, tuple)): return '[' + ','.join(js(x) for x in o) + ']'
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'
def pre(m, t): B.note_prefix(m, q(t) + " ")
def setf(marker, **kw):
    if B.s.count(marker) != 1: B.die('setf marker: ' + marker)
    i = B.s.index(marker); j = B.s.index(",note:'", i); head = B.s[i:j]
    for k, v in kw.items():
        pat = re.compile(r",%s:(?:'(?:[^'\\]|\\.)*'|\[[^\]]*\]|[\d.]+)" % k)
        if k == 'est':
            head = pat.sub('', head)
            if v: head += ',est:1'
            continue
        new = ",%s:%s" % (k, js(v))
        if pat.search(head): head = pat.sub(lambda _: new, head, count=1)
        else:
            est = ',est:1' if head.endswith(',est:1') else ''
            head = (head[:-6] if est else head) + new + est
    B.s = B.s[:i] + head + B.s[j:]
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
    if set(d) - {'b', 'prev', 'now'}: B.die('berth extra keys: ' + bid)
    return a, b, d, tail
def bput(a, b, d, tail): B.s = B.s[:a] + '  {' + ','.join(k + ':' + d[k] for k in ('b', 'prev', 'now')) + '}' + tail + B.s[b:]
def take_wait(name):
    wa, wb = B.line_of("  {n:'%s'," % name); wl = B.s[wa:wb].strip(); last = not wl.endswith(','); wv = obj(wl.rstrip(','))
    B.s = B.s[:wa] + B.s[wb + 1:]
    if last:                                   # she was the last line of her block: the line now before the bracket must lose its comma
        k = B.s.rfind(",\n", 0, wa);  assert k == wa - 2, 'last-line comma'; B.s = B.s[:k] + B.s[k + 1:]
    return wv
def as_now(wv, f, est, add, nm=None, etc=None):
    nw = {k: wv[k] for k in ('n', 'c', 'q', 'u', 'ie', 'loa', 'rank', 'ag') if k in wv}; nw['f'] = js(f)
    if est: nw['est'] = '1'
    if nm is not None: nw['nm'] = js(nm)
    if etc is not None: nw['etc'] = js(etc)
    nw['note'] = "'" + q(add + ' · ') + wv.get('rem', "''")[1:]; return unobj(nw, NOWKEYS)
def as_prev(now, out, outBy):
    pv = {k: now[k] for k in ('n', 'c', 'q', 'u', 'ie', 'ag') if k in now}; pv['out'] = js(out); pv['outBy'] = js(outBy); return unobj(pv, PREVKEYS)

# ================= HEADER =================
B.rep("const NOW=h('11-26 15:14');", "const NOW=h('11-26 23:10');")
B.rep("<i>Signals to</i><b>26 Nov day sheet (to 0910)</b>", "<i>Signals to</i><b>26 Nov evening sheet (disp 1810, to 2100)</b>")
B.rep("HM signal sheets to the day sheet of 26 Nov (extended to 09:10) ·", "HM signal sheets to the evening sheet of 26 Nov (disp 18:10, extended 21:00) ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='HM signal 26 Nov evening sheet (disp 1810, extended 2100) · corrigendum …/Berthingpolicy/2026/3152 dt 26.11.2026 (Bitumen place: break bulk only) · ")

# ================= ENGINE — corrigendum of 26.11.2026 =================
B.rep("const POL2111=h('11-23 18:00');", "const POL2611=h('11-27 18:00'); // Corrigendum Traffic/Shipping/587/Berthingpolicy/2026/3152 dt 26.11.2026 — no date of effect printed: taken from the next berthing meeting, 27 Nov 11:00, i.e. for berths given from 27 Nov 18:00\n"
      "const BRK=c=>/bag|log|timber|steel|pipe|coil|plate|billet|slab|granite|marble|pulp|project|package|blade|windmill|crane|machin|cashew|break.?bulk/i.test(c||''); // break bulk cargo as Appendix-02A lists it (granite, steel, bagged cargo, timber logs, wood pulp, jumbo bags, pipes) — everything \"in bulk\" is not\n"
      "const POL2111=h('11-23 18:00');")
B.rep("K8Q:()=>{const l=rkQ('8K');if(!l.length)return [];const fs=W.filter(w=>!done.has(w.n)&&R(w)!=null&&R(w)<=e.t&&w.rep<=e.t&&meetOK(w,e.t)&&RK(w,'8K')&&allowedBerths(w).length>0);",
      "K8Q:()=>{const bb=w=>e.t<POL2611||BRK(w.c) /* corrigendum 26.11.2026: \"for Break Bulk Cargo only\" — a bulk vessel of the 6.5K line does not stand in this line for the Bitumen berth */;const l=rkQ('8K').filter(bb);if(!l.length)return [];const fs=W.filter(w=>!done.has(w.n)&&R(w)!=null&&R(w)<=e.t&&w.rep<=e.t&&meetOK(w,e.t)&&RK(w,'8K')&&allowedBerths(w).length>0&&bb(w));")
B.rep("s:'1 berth · else the 6.5K line (circular 5237, from the 23 Nov meeting; General before that)'", "s:'1 berth · else the 6.5K line, break bulk cargo only (circular 5237 (iii) as corrected on 26.11.2026; General before 23 Nov)'")
B.rep("p:'1 place · if no bitumen vessel, the senior vessel of the 6.5K line takes it (circular 5237)'", "p:'1 place · if no bitumen vessel, the senior BREAK BULK vessel of the 6.5K line takes it (corrigendum 26.11.2026)'")
B.rep("K8Q:'6.5K line · vacant Bitumen place'", "K8Q:'6.5K line · vacant Bitumen place · break bulk'")
# next-meeting section: after a Bitumen berth comes the 6.5K line (break bulk), not General — the section had gone on showing General since 23 Nov
B.rep("      if(!r.same.ws.some(suits))for(let i=ix+1;i<ORD.length;i++){const c=queue(ORD[i]).filter(w=>suits(w)&&!r.same.ws.includes(w));if(c.length){r.next={L:ORD[i],ws:c.slice(0,2)};break;}}}",
      "      if(!r.same.ws.some(suits)){if(X==='BIT'){r.next={L:'8K',bit:1,ws:queue('8K').filter(w=>suits(w)&&BRK(w.c)).slice(0,3)};} // circular 5237 (iii) + corrigendum 26.11.2026: a vacant Bitumen place → the 6.5K line, break bulk only\n"
      "        else for(let i=ix+1;i<ORD.length;i++){const c=queue(ORD[i]).filter(w=>suits(w)&&!r.same.ws.includes(w));if(c.length){r.next={L:ORD[i],ws:c.slice(0,2)};break;}}}}")
B.rep("if(r.next)h+=grp('Uske baad',r.next,r,r.next.L==='HP'?'· jo bid mein hain':'');", "if(r.next)h+=grp('Uske baad',r.next,r,r.next.bit?'· Bitumen jagah khali → 6.5K line · sirf break bulk (corrigendum 26 Nov)':r.next.L==='HP'?'· jo bid mein hain':'');")

# ================= V =================
M = "{b:'15A',n:'African Hornbill (blades, next call)',p:[157.5,166.75]"
pre(M, SG + ": OUT 03:30 · Capt Deepak · 157½–166¾ → OTB — as the programme has it (27 Nov).")
M = "{b:'15A',n:'Hai Nam 81',nm:30000,p:[157.5,166.25]"
pre(M, SG + ": IN \"o/c\" · Capt Deepak, behind his 03:30 sailing of African Hornbill · OTB → 157½–166¼ → alongside about 07:30 on 27 Nov, est (05:30 by the programme's hour). 52,000 MT at 30,000 a day → about 29 Nov 01:05, est.")
setf(M, f='11-27 07:30', t='11-29 01:05')
NOTSIG = SG + ": NOT ON IT. The sheet runs from 23:00; this move belongs to the afternoon rows of the day sheet, which are not in hand — the hour stays an estimate from programme 27.11."
pre("{b:'14',n:'Tug Varahi + barge AKG 11',p:[128,134.75]", NOTSIG)
pre("{b:'14',n:'Blue Shark',p:[128,141]", NOTSIG)
pre("{b:'5',n:'Asian Summit',nm:16100,p:[30.5,39.25]", NOTSIG + " WHETHER SHE HAS SHIFTED TONIGHT IS NOT KNOWN TO THE BOARD.")
pre("{b:'7',n:'Jumbo Kinetic',p:[52,57]", SG + ": NOT ON IT, though the sheet covers 23:00 onwards — she was either brought in before 23:00 on the day sheet's later rows (not in hand) or is not coming tonight. Hour kept as estimated.")

# ================= LIQ =================
# OJ-1: Green Bhavishya out 23:00 → Lumis shifts in from OJ-3 · OJ-3: → Ginga Merlin · OJ-4: Ocean Star out 09:15 on 27 Nov · OJ-5: back in use, Volga on 27 Nov
a, b, d1, t1 = bline('OJ-1'); gb = obj(d1['now']); assert 'Green Bhavishya' in gb['n']
a3, b3, d3, t3 = bline('OJ-3'); lu = obj(d3['now']); assert 'Lumis' in lu['n']
lu1 = dict(lu); lu1['f'] = js('11-27 00:30'); lu1['est'] = '1'
lu1['note'] = "'" + q(SG + ": SHIFT 23:00 · Capt Omesh · OJ-3 → OJ-1 · \"FLOOD\" — into the berth LPG/C Green Bhavishya leaves at 23:00 → at OJ-1 about 00:30 on 27 Nov, est. She was made fast at OJ-3 at 03:42 on 26 Nov; list ETC 28 Nov 08:47 · ") + lu['note'][1:]
d1['prev'] = as_prev(gb, '11-26 23:00', SG + ': OUT 23:00 · Capt Deepak · OJ-1 → OTB (programme 27.11 had her out readiness at 27 Nov 03:00; list ETC 27 Nov 09:32) · DPR 26.11: 3,853 MT off by 07:00, 10,147 left')
d1['now'] = unobj(lu1, NOWKEYS); bput(a, b, d1, t1)
gm = take_wait('Ginga Merlin')
a3, b3, d3, t3 = bline('OJ-3')
d3['prev'] = as_prev(lu, '11-26 23:00', SG + ': SHIFT 23:00 · Capt Omesh · OJ-3 → OJ-1 — she goes on working at OJ-1 (made fast at OJ-3 03:42 on 26 Nov)')
d3['now'] = as_now(gm, '11-27 03:00', True, SG + ': IN "o/c" · Capt Deepak, behind his 23:00 sailing of Green Bhavishya · OTB → OJ-3, the berth Lumis leaves at 23:00 → alongside about 03:00 on 27 Nov, est'); bput(a3, b3, d3, t3)
a4, b4, d4, t4 = bline('OJ-4'); osn = obj(d4['now']); assert 'Ocean Star' in osn['n']
osn['etc'] = js('11-27 09:15'); osn['note'] = "'" + q(SG + " — \"day signal\" rows for 27 Nov: RT OUT 09:15 · Capt Yadav · OJ-4 → OTB (the programme had 16:00, the list ETC 17:37) · ") + osn['note'][1:]
d4['now'] = unobj(osn, NOWKEYS); bput(a4, b4, d4, t4)
vo = take_wait('Volga')
a5, b5, d5, t5 = bline('OJ-5'); assert d5['now'] == 'null'
d5['now'] = as_now(vo, '11-27 13:15', True, SG + ' — "day signal" rows for 27 Nov: IN "o/c" · Capt Yadav, behind his 09:15 sailing of Ocean Star · OTB → OJ-05 · "FLOOD" (written "Volgo") → alongside about 13:15 on 27 Nov, est · OJ-5 IS BACK IN USE — the trade notice of 16.11.2026 had withdrawn it for maintenance till 26 Nov'); bput(a5, b5, d5, t5)
def rem(name, text):
    a, b = B.line_of("  {n:'%s'," % name); i = B.s.index("rem:'", a) + 5; assert i < b; B.s = B.s[:i] + q(text + ' · ') + B.s[i:]
rem('Chemroad Quest', SG + ': Ocean Star now leaves OJ-4 at 09:15 on 27 Nov, not 16:00 — Chemroad Quest, programmed behind her, is not on a signal yet → about 11:15–13:15 on 27 Nov at the earliest, est')
B.s, k = re.subn(r"const LIQ=\{prog:'((?:[^'\\]|\\.)*)',src:'(?:[^'\\]|\\.)*',asOf:'11-26 15:14',",
    lambda m: "const LIQ={prog:'" + q("HM SIGNAL 26 Nov evening sheet (disp 18:10, extended 21:00) — OJ-1 LPG/C Green Bhavishya OUT 23:00 → LUMIS SHIFTS IN from OJ-3 (23:00, flood) · OJ-3 → Ginga Merlin in, about 03:00 on 27 Nov est · 27 Nov: OJ-4 Ocean Star RT OUT 09:15 · OJ-5 BACK IN USE → Volga in, about 13:15 est · ") + m.group(1)
    + "',src:'DPA berthing list 26.11.26 as revised after the meeting · DPR 26.11 · programme 27.11 · signals to the evening sheet of 26 Nov (disp 1810, extended 2100)',asOf:'11-26 23:10',", B.s, count=1)
if k != 1: B.die('LIQ head not found')
LQN = ['HM signal 26 Nov — evening sheet · dispatch 18:10, extended 21:00 with the day rows for 27 Nov · Capt Omesh for HM · oil-jetty rows', [
 ['23:00', 'OUT', 'Green Bhavishya (LPG/C)', 'OJ-1 → OTB', 'Deepak', '11-26 23:00', 'programme had 27 Nov 03:00'],
 ['23:00', 'SHIFT', 'Lumis', 'OJ-3 → OJ-1', 'Omesh', '11-26 23:00', 'FLOOD · at OJ-1 about 00:30, est'],
 ['o/c', 'IN', 'Ginga Merlin', 'OTB → OJ-3', 'Deepak', '11-27 03:00', 'behind Green Bhavishya — est'],
 ['09:15', 'OUT', 'Ocean Star', 'OJ-4 → OTB', 'Yadav', '11-27 09:15', 'RT OUT · day signal row for 27 Nov'],
 ['o/c', 'IN', 'Volga', 'OTB → OJ-5', 'Yadav', '11-27 13:15', 'FLOOD · written "Volgo" · OJ-5 back in use — est']]]
B.rep(" moves:[\n", " moves:[\n  " + js(LQN) + ",\n")

# ================= MV =================
MVS = ['HM signal 26 Nov — evening sheet · dispatch 18:10, extended 21:00 · Capt Omesh for HM · received 26 Nov 23:10 · cargo berths', [
 ['00:00', 'OUT', 'Tanjong Pagar 1', 'CJ-11 · 89–95½ → OTB', 'Omesh', '11-27 00:00', 'container'],
 ['o/c', 'IN', 'Hui Fa', 'OTB → CJ-11 · 87–95½', 'Omesh', '11-27 04:00', 'container · FLOOD · behind Tanjong Pagar 1 — est'],
 ['03:30', 'OUT', 'African Hornbill', 'CJ-15A · 157½–166¾ → OTB', 'Deepak', '11-27 03:30', 'as programme 27.11'],
 ['o/c', 'IN', 'Hai Nam 81', 'OTB → CJ-15A · 157½–166¼', 'Deepak', '11-27 07:30', 'behind African Hornbill — alongside about 07:30, est · GOV(30K)'],
 ['—', '—', 'PMS / stand-by duty', 'Capt Deepak 02:00–03:00 · Capt Yadav on completion, 1 hr', '—', '11-27 03:00', ''],
 ['—', '—', 'Not on this sheet', 'Tug Varahi OUT · Blue Shark CJ-5 → 14 · Asian Summit CJ-7 → 5 · Jumbo Kinetic IN CJ-7', '—', '11-26 23:00', 'the four moves of programme 27.11 for the evening of 26 Nov — on the later rows of the day sheet, not in hand']]]
B.rep("const MV=[\n", "const MV=[\n " + js(MVS) + ",\n")

# ================= NOTICES =================
N = {'d': '26 Nov', 'src': 'Mihir (chat)', 'ref': 'Traffic/Shipping/587/Berthingpolicy/2026/3152', 'rd': '26.11.2026', 'iso': '2026-11-26', 'kind': 'Berthing policy',
 't': 'Corrigendum — vacant Bitumen place: the 6,500 MTPD priority, for break bulk cargo only',
 's': 'Corrigendum to the circular of 21.11.2026, which it cites as …/Berthingpolicy/2026/5737. In partial modification of clause (iii), Bitumen Priority (Sr. No. 5): in the absence of a suitable vessel under Bitumen priority, the berth earmarked under this category shall be operated under the 6,500 MTPD priority category (Sr. No. 3(E)) for break bulk cargo only. All else in the policy of 24.03.2025, the circular of 21.05.2026, the corrigendum of 09.07.2026 and the circular of 21.11.2026 stays in force. Approved by the Competent Authority; signed by the Traffic Manager. No date of effect is printed. The reference number (3152) is handwritten.',
 'eff': 'ON THE BOARD from v279: from the meeting of 27 Nov (berths from 27 Nov 18:00) a vacant Bitumen place goes to the senior BREAK BULK vessel of the 6.5K line — bags, logs, steel, project cargo; a vessel with cargo in bulk (salt, clay, ore) cannot take it. What it drops from the clause of 21 Nov: the words "instead of the General group" and "subject to eligibility, readiness and seniority" — the policy\'s own conditions still apply. TODAY IT CHANGES NO ORDER: the 6.5K line is Crystal Land 1, Glimlit 2, Porto Fiscardo 3, Captainannis L 4 (bags), CD Glory 5, Dariya Priya 6, African Tiger 7, Paiwan Ace 8 (logs) — all break bulk; only Rex (ball clay, 8K 11) falls out. The Bitumen berth is CJ-2, with DSM London till about 28 Nov. THE NUMBER OF THE 21 NOV CIRCULAR: handwritten on that paper and read by the board as 5237; this corrigendum types it as 5737; by the run of the series (3089 on 15 Nov, 3152 on 26 Nov) it may well be 3137. The board keeps calling it "circular 5237" until the number is settled.',
 'st': 'in force', 'file': 'circ/2026-11-26_berthing-policy-corrigendum-bitumen-3152.pdf', 'pg': 1}
a, b = B.line_of(" // s: gist, eff: bearing on berthing / the board, st:")
B.s = B.s[:b] + "\n {" + ",".join(k + ":" + js(v) for k, v in N.items()) + "}," + B.s[b:]
OLD = "(i) ON THE BOARD from v272 (25 Nov 15:00): read, at Mihir\\'s asking, against the policy of 24.03.2025, the circular of 21.05.2026 and the corrigendum of 09.07.2026 — a vacant Govt place goes to a Coastal vessel, then an HP bid, then the SAAGAR line by seniority; a vacant Coastal place to an HP bid, then SAAGAR; a 30K / 25K quote only after that. The port has not yet given a place this way — the check stays open till a programme shows it."
NEW = ("(i) AS THE PORT APPLIES IT (programme 27.11, the meeting of 26 Nov): a vacant Govt place went to Hai Nam 81 — first of the HP column, on a 30K quote, printed \"GOV(30K)\" — ahead of the SAAGAR line. On the board from v278: a Coastal vessel, then the 30K / 25K quote vessels of the HP column, then SAAGAR. (From v272 to v277 the board had read the HP step as an HP bid only, and so put SAAGAR before the quote.) "
       "(iii) CORRECTED by the corrigendum of 26.11.2026 (…/3152): the 6,500 line takes the Bitumen berth for break bulk cargo only. That corrigendum cites this circular as 5737.")
B.rep(OLD, q(NEW).replace("\\'", "\\'"))
B.rep("eff:'OJ-5 stays out till 26 Nov — the list already prints it \"under maintenance\". Liquid tab only; no effect on the dry cargo berths.',st:'in force'",
      "eff:'OJ-5 stayed out till 26 Nov. BACK IN USE: the HM signal of 26 Nov night has MT Volga going into OJ-5 on 27 Nov. Liquid tab only; no effect on the dry cargo berths.',st:'expired'")
B.save(); print('saved 75')
