#!/usr/bin/env python3
# apply85a — v289 part 1. 28 Nov 11:12, no text: DAILY BERTHING LIST 28.11.2026 (07:00) + DPR 28-11-2026 + HM SIGNAL 28/11/26 day sheet (disp 10:45).
# Papers reached the board AFTER the 11:00 meeting hour → the call for the meeting of 28 Nov was frozen first from v288 (call_2811.txt).
import sys, re, json
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html', list_tag='LIST 28.11'); q = B.q
L = 'LIST 28.11'; D = 'DPR 28.11'; SG = 'HM SIGNAL 28 Nov day sheet (disp 10:45)'
src = open('/home/claude/work/apply76a.py', encoding='utf-8').read()
exec(src[src.index('def js(o):'):src.index('# ================= HEADER')])
# ================= HEADER =================
B.rep("const NOW=h('11-27 23:33');", "const NOW=h('11-28 11:12');")
B.rep("const PROG_END=h('11-28 18:00');", "const PROG_END=h('11-28 18:00');")
B.rep("<i>List</i><b>27.11 · revised after the meeting</b>", "<i>List</i><b>28.11</b>")
B.rep("<i>DPR</i><b>27.11</b>", "<i>DPR</i><b>28.11</b>")
B.rep("<i>Signals to</i><b>27 Nov evening sheet (disp 1727, to 2215)</b>", "<i>Signals to</i><b>28 Nov day sheet (disp 1045)</b>")
B.rep("HM signal sheets to the evening sheet of 27 Nov (disp 17:27, extended 22:15) ·", "HM signal sheets to the day sheet of 28 Nov (disp 10:45) ·")
B.rep("berthing list 27.11 as revised after the meeting (no list came for 22.11 or 24.11) · programme 28.11 · DPR 27.11 (position 07:00) ·", "berthing list 28.11 (07:00; no list came for 22.11 or 24.11) · programme 28.11 · DPR 28.11 (position 07:00) ·")
B.rep("const BOARD_SRC='", "const BOARD_SRC='list 28.11 (0700) · DPR 28.11 (0700) · HM signal 28 Nov day sheet (disp 1045) · ")
setline("const CALL_FROZEN=null;", "const CALL_FROZEN={d:'11-28',at:'11-27 23:33',basis:'board v288 — list 27.11 (revised), DPR 27.11, signals to the evening sheet of 27 Nov',call:[['Crystal Land','2'],['Rex','5'],['Meghna Prestige','16'],['KM Jakarta','15A'],['Tai Keystone','8'],['Star Unity','13'],['Tug Marigold + barge Alaacrity 666','3'],['Sea Postman','7'],['Josco Taicang','15']]}; // the call as it stood BEFORE the meeting of 28 Nov: list 28.11 and DPR 28.11 reached the board at 11:12, after the meeting hour — the call is not rebuilt. Put it into MEETLOG when programme 29.11 comes, then set this back to null.")
# ================= V =================
M = "{b:'14',n:'Tug Varahi + barge AKG 11',p:[128,134.75]"
pre(M, D + ": COMPLETED 14:00, LEFT THE BERTH 16:20 on 27 Nov — 640 pipes / 3,811 MT (the signal had OUT 17:30)."); setf(M, t='11-27 16:20', est=False)
M = "{b:'5',n:'Blue Shark',p:[32,39.25]"
pre(M, D + ": WORK STOPPED 19:35, LEFT CJ-5 20:25 on 27 Nov — shifted to CJ-14."); setf(M, t='11-27 20:25', est=False)
M = "{b:'14',n:'Blue Shark',p:[128,141]"
pre(M, D + " + " + L + ": RE-MADE FAST AT CJ-14 21:15 on 27 Nov, RESUMED 02:40 on 28 Nov · 1,803 MT in the day of the shift (rice 855 + flour 773 + sugar 175) on 12 hooks; 10,679 loaded, 15,803 left → at the earlier 2,650 a day about 4 Dec 06:10; list ETC 30 NOV 13:00 · remark \"W1, W2, S1 32–39¼\".")
setf(M, f='11-27 21:15', est=False)
M = "{b:'7',n:'Asian Summit',nm:16100,p:[50,57]"
pre(M, D + ": WORK STOPPED 20:00, LEFT CJ-7 22:00 on 27 Nov — shifted to CJ-5; 43,600 MT off by then."); setf(M, t='11-27 22:00', est=False)
M = "{b:'5',n:'Asian Summit',nm:16100,p:[30.5,39.25]"
pre(M, D + " + " + L + ": RE-MADE FAST AT CJ-5 22:54, RESUMED 23:30 on 27 Nov · 14,700 MT in 24 h on 13 hooks — 58,300 off, ONLY 2,199 MT LEFT at 07:00 on 28 Nov → about 28 Nov 10:35 at this rate; list ETC 28 NOV 22:59 · remark \"S1 50–57\".")
setf(M, f='11-27 22:54', t='11-28 22:59', est=False)
M = "{b:'7',n:'Jumbo Kinetic',p:[52,57]"
pre(M, D + " + " + L + ": MADE FAST 23:25 on 27 Nov at CJ-7, 52–57 · NOT COMMENCED — \"project cargo: can unlash and discharge only in daylight\" · 2 harbour cranes + 19 packages, 843 MT · no ETC printed → taken as about 29 Nov 12:00, est (two daylight spells).")
setf(M, f='11-27 23:25', t='11-29 12:00')
pre("{b:'1',n:'Manta Sena',nm:6500,p:[0,7.5]", D + ": 4,461 MT in 24 h on 15 hooks — 10,900 loaded, 19,270 left → about 2 Dec 14:40 at this rate; list ETC 30 Nov 04:03.")
pre("{b:'2',n:'DSM London',nm:3000,p:[8.5,16.5]", D + ": 2,301 MT in 24 h on 12 hooks (rice 1,900 + flour 142 + sugar 259, sugar complete) — 30,352 loaded, 2,348 left → about 29 Nov 07:30 at this rate; list ETC 30 Nov 13:50.")
pre("{b:'4',n:'Safi Alfa',nm:3450,p:[21.25,29.5]", D + ": 3,301 MT in 24 h on 12 hooks — 29,136 loaded, 2,964 left → about 29 Nov 04:35 at this rate; list ETC 30 Nov 01:58 (list quantity now 23,287, \"32100 total\").")
pre("{b:'6',n:'Katerina K',nm:3450,p:[40.25,49]", D + ": bentonite 2,760 J-bags / 3,450 MT in 24 h on 9 hooks — 6,406 MT loaded; left: kaolin 4,981 + bentonite 14,986 + soya bean meal 20,600 = 40,567 MT → about 10 Dec 01:10 at this rate. No ETC on the list.")
pre("{b:'8',n:'Zheng Hui',p:[58,67.75]", D + ": 16,330 MT in 24 h on 9 hooks — 61,950 off, 4,050 MT LEFT at 07:00 on 28 Nov → about 28 Nov 12:55 at this rate; list ETC 28 Nov 16:15 · " + L + " (ETA sheet): she is listed again for 30 Nov — iron ore pellets 65,700 MT EXPORT, agent Genesis.")
pre("{b:'9',n:'Pioneer Fortune',nm:6500,p:[69,76.25]", D + ": 3,754 MT in 24 h on 12 hooks — 9,193 loaded, 15,887 left → about 2 Dec 12:35 at this rate.")
pre("{b:'13',n:'AG Varvara',nm:4000,p:[112,125]", D + ": 31,115 pcs / 4,231 CBM in 24 h on 12 hooks (norm 4,000) — 12,495 CBM off, 26,617 left → about 4 Dec 14:00 at this rate; list ETC 5 Dec 08:52.")
M = "{b:'15',n:'Xin Hai Tong 71',p:[143,156.25]"
pre(M, D + ": only 282 packages / 381 MT in 24 h on 11 hooks (1,767 the day before) — 3,081 MT off, 1,054 packages / 2,625 MT left → at the two-day average (1,074 a day) about 30 Nov 17:40; no ETC on the list.")
setf(M, t='11-30 17:40')
M = "{b:'15A',n:'Hai Nam 81',nm:30000,p:[157.5,166.25]"
pre(M, D + ": 24,455 MT in her first 23¾ hours on 12 hooks — 27,545 left → about 29 Nov 10:00 at this rate; list ETC 29 NOV 01:54.")
M = "{b:'16',n:'MSC Magali',nm:50000,p:[169.5,188]"
pre(M, D + ": 46,879 MT in 24 h on 11 hooks (norm 50,000) — 67,806 off, 32,922 left → about 28 Nov 23:50 at this rate; list ETC 28 NOV 17:18.")
# ================= W — ranks, readiness, quantity straight from the list =================
board = {}
a = B.s.index('const WRAW=['); e = B.s.index('\n];', a)
for ln in B.s[a:e].split('\n')[1:]:
    m = re.match(r"\s*\['((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)',([^,]+),'([^']*)',([^,]+),([^,]+),('[^']*'|null),\{([^}]*)\},", ln)
    if m: board[m.group(1)] = dict(q=m.group(3), rdy=m.group(7).strip("'"), rk=m.group(8))
def norm(x):
    x = x.upper(); x = re.sub(r"\(GL\)|\(MV\)|\(DV\)|\(SALT, NEXT CALL\)|\(LPG/C\)", '', x); x = re.sub(r"^(M\.?V\.?|M\.?T\.?|LPG/C\.?)\s*[-.]?\s*", '', x.strip()); return re.sub(r'[^A-Z0-9]', '', x)
ALI = {'PAIWANICE': 'PAIWANACE', 'TUGMARIGOLDBARGEALAACRITY': 'TUGMARIGOLDBARGEALAACRITY666', 'ERNAOLDENDROFF': 'ERNAOLDENDORFF', 'LANNANAREE': 'LANNANAREERELOAD', 'YARAJ': 'YARAJNEXTCALL', 'TUGCANARAJOGWITHBARGERMG254': 'TUGCANARAJOGBARGERMG254'}
bn = {norm(k): k for k in board}; bn['LANNANAREERELOAD'] = 'Lanna Naree (reload)'; bn['YARAJNEXTCALL'] = 'Yara J (next call)'
LJ = json.load(open('/home/claude/work/in28/l28.json'))
K = ['GOV', 'COASTAL', 'HP', 'SAAGAR', '24H', '8K', 'STL', 'GEN']; LBL = {'GOV': 'GOV', 'COASTAL': 'CSTL', 'HP': 'HP', 'SAAGAR': 'SGR', '24H': '24H', '8K': '8K', 'STL': 'STL', 'GEN': 'GEN'}
def cj(sheet):
    out, sec = [], None
    for r in LJ[sheet]:
        r = [('' if x is None else str(x).strip()) for x in r] + [''] * 25
        if r[3] == 'CARGO JETTY VESSELS': sec = 'CJ'; continue
        if r[3] in ('OIL TANKERS', 'CONTAINERS', 'TUNA VESSELS', 'VADINAR'): sec = r[3]; continue
        if sec == 'CJ' and r[1] == 'CJ': out.append(r)
    return out
def dm(x):
    m = re.match(r'\d{4}-(\d\d)-(\d\d) (\d\d):(\d\d)', x or ''); return '%s-%s %s:%s' % m.groups() if m else ''
def say(t): return '%d %s %s' % (int(t[3:5]), 'Nov' if t[:2] == '11' else 'Dec', t[6:])
SKIP = {'Shree Krishna IX'}
REPN, done, etaN = {}, [], {}
for r in cj('WAITING LIST'):
    nm = norm(r[3]); nm = ALI.get(nm, nm); b = bn.get(nm)
    if not b: print('NEW on waiting sheet, not on board:', r[3]); continue
    if b in SKIP: continue
    o = board[b]; rk = {}
    for i, k in enumerate(K):
        v = r[12 + i]
        if v.isdigit(): rk[k] = int(v)
        elif v == 'Y' and k != 'STL': rk[k] = 98
    rks = ','.join(("'%s'" % k if k[0].isdigit() else k) + ':' + str(v) for k, v in rk.items())
    rdy = dm(r[11]); rep = dm(r[10]); REPN[b] = rep
    was_exp = o['rdy'] == 'null' and b in ('Xin Bo', 'Bunun Miracle', 'Tomkar', 'Jiaxin', 'Star New London', 'Paiwan Wisdom', 'Propel Fortune', 'New Faith', 'New Joyful', 'Tug Canara Jog + barge RMG 254')
    same = (rks.replace(' ', '') == o['rk'].replace(' ', '')) and ((rdy or 'null') == o['rdy']) and not was_exp
    if same: continue
    bits = []
    if was_exp: bits.append('ON THE WAITING SHEET — reported ' + say(rep))
    if (rdy or 'null') != o['rdy']: bits.append(('READY — readiness ' + say(rdy)) if rdy else 'readiness N/A')
    bits.append(' · '.join(LBL[k] + ' ' + ('Y' if v == 98 else str(v)) for k, v in rk.items()) or 'no rank printed')
    if r[21]: bits.append('"' + re.sub(r'\s+', ' ', r[21]) + '"')
    B.wrow(b, q(' · '.join(bits)), rk=rks, rdy=rdy); done.append(b)
print('W rows updated:', len(done))
ETAROWS = cj('ETA')
for r in ETAROWS:
    nm = norm(r[3]); nm = ALI.get(nm, nm); b = bn.get(nm)
    if b == 'Zheng Hui': b = None
    if b: etaN[b] = dm(r[10])
m = B._row('Star Unity').search(B.s); e = B.s.index("],\n", m.start()) + 3
NEW = [
 " ['Zheng Hui (pellets, next call)','Iron ore pellets',65700,'MT',229,null,null,{},'" + q(L + " (ETA sheet): NEW · iron ore pellets 65,700 MT EXPORT · ETA 30 Nov · N/A · 229 m, gearless · agent Genesis — the same vessel now discharging DAP at CJ-8") + "'],",
 " ['Century Zhengzhou','Salt in bulk',61320,'MT',199.85,6.5,null,{HP:98},'" + q(L + " (ETA sheet): NEW · salt in bulk 61,320 MT EXP · ETA 1 Dec · N/A · HP Y · \"30K/25K/10K SR.NO 07 DD-13.40M\" · 199.85 m · agent True Blue") + "'],",
 " ['Bos Costa','Rice bags',18000,'MT',176.63,5.6,null,{},'" + q(L + " (ETA sheet): NEW · rice in bags 18,000 MT EXP · ETA 1 Dec · N/A · \"CJ-02,3\" · 176.63 m · agent DBC") + "'],",
 " ['Jaador','Salt in bulk',54000,'MT',null,null,null,{},'" + q(L + " (ETA sheet): NEW · salt in bulk 54,000 MT EXP · ETA 3 Dec · N/A · \"LP: Bin Qasim, Pakistan\" · agent Cross Trade") + "'],",
]
B.s = B.s[:e] + "\n".join(NEW) + "\n" + B.s[e:]
etaN.update({'Zheng Hui (pellets, next call)': '11-30 00:00', 'Century Zhengzhou': '12-01 00:00', 'Bos Costa': '12-01 00:00', 'Jaador': '12-03 00:00'})
etaN.pop('Shree Krishna IX', None)
setline("const ETA={'Xin Bo':", "const ETA={" + ",".join("'%s':'%s'" % (k, v) for k, v in etaN.items()) + "}; // expected sheet, list 28.11")
a, b = B.line_of("Object.assign(REP,{'Princess Manissa':'11-26 09:15',")
NEWREP = {k: REPN[k] for k in ('Xin Bo', 'Bunun Miracle', 'Tomkar', 'Jiaxin', 'Star New London', 'Paiwan Wisdom', 'Propel Fortune', 'New Faith', 'New Joyful', 'Tug Canara Jog + barge RMG 254') if k in REPN}
B.s = B.s[:b] + "\nObject.assign(REP,{" + ",".join("'%s':'%s'" % kv for kv in NEWREP.items()) + "}); // list 28.11 — now on the waiting sheet" + B.s[b:]
a, b = B.line_of("Object.assign(AG,{'Shree Krishna IX':'Indoglobal',")
B.s = B.s[:b] + "\nObject.assign(AG,{'Zheng Hui (pellets, next call)':'Genesis','Century Zhengzhou':'True Blue','Bos Costa':'DBC','Jaador':'Cross Trade'});Object.assign(IE,{'Zheng Hui (pellets, next call)':'EXP','Century Zhengzhou':'EXP','Bos Costa':'EXP','Jaador':'EXP'}); // list 28.11" + B.s[b:]
B.rep("'KM Jakarta':13.3,'Hai Nam 81':12.6,'Jiaxin':12.8});", "'KM Jakarta':13.3,'Hai Nam 81':12.6,'Jiaxin':12.8,'Xin Bo':12.25,'Century Zhengzhou':13.4,'Tomkar':10.7});")
print('REP new:', NEWREP); print('ETA:', etaN)
B.save(); print('saved 85a')
