# v257 — MEETING page (new tab #meeting): the next berthing meeting berth by berth, as Mihir asked on 22 Nov (16:58–17:32):
# which vessel is on each berth, CONTINUE or KHALI, which priority operates there, who has a chance. Display + one ordering fix.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
assert 'function meetBoard' not in s, 'already applied'
JS = open('tools/examples/2026-11-22_meeting_page_v257_meetboard.js (was /home/claude/work/mtg/meetboard.js)', encoding='utf-8').read()
CSS = open('tools/examples/2026-11-22_meeting_page_v257_meetboard.css (was /home/claude/work/mtg/meetboard.css)', encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
# 1 styles — end of the main style block
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
# 2 the tab, second after Cargo jetties
rep('    <a href="#priority" data-view="priority">', '    <a href="#meeting" data-view="meeting"><b>Meeting</b><small>Next berthing meeting · berth by berth · who leaves, which priority, who has a chance</small><span class="vb" id="vb-meeting"></span></a>\n    <a href="#priority" data-view="priority">')
rep("const VIEWS={cargo:'Deendayal Port · Kandla · Dry cargo jetty',", "const VIEWS={cargo:'Deendayal Port · Kandla · Dry cargo jetty',meeting:'Deendayal Port · Kandla · Berthing meeting',")
rep("const VIEW_NAME={ppp:", "const VIEW_NAME={meeting:'Meeting',ppp:")
# 3 the page
rep('  <div class="view" data-view="priority" id="view-priority">', '  <div class="view" data-view="meeting" id="view-meeting">\n  <section class="card"><div class="mbhead"><div class="mbey">Agli meeting</div><h2 id="mbh"></h2><p id="mbsub"></p></div><div id="mtgb"></div></section>\n  </div>\n  <div class="view" data-view="priority" id="view-priority">')
# 4 code
rep('function preview(){\n', JS + 'function preview(){\n')
rep("  const stTxt=c=>{const w=c.w;const t=[", "  HPB_CAND=cand;\n  const stTxt=c=>{const w=c.w;const t=[")
rep('hpbid();', 'hpbid();meetBoard();')
# 5 Govt line with no printed rank: the reported time decides; where the sheet gives none, the readiness / ETA time (Zheng Hui, reported 21 Nov 08:12, before Tai Keystone, still expected for 22 Nov)
rep(".sort((a,z)=>(a.rep||1e9)-(z.rep||1e9));\n l.forEach((w,i)=>{w.rk=Object.assign({},w.rk,{GOV:60+i});w.govAuto=1;});})();", ".sort((a,z)=>(Math.max(a.rep||0,a.rdy||0)||1e9)-(Math.max(z.rep||0,z.rdy||0)||1e9)); // 22 Nov: the later of reported and readiness / ETA time decides — an expected vessel's old reporting entry goes stale as her ETA moves, so a vessel that has arrived stands before one still expected (Zheng Hui before Tai Keystone)\n l.forEach((w,i)=>{w.rk=Object.assign({},w.rk,{GOV:60+i});w.govAuto=1;});})();")
# 6 the stamp — the call changed (Zheng Hui before Tai Keystone) and a page was added
rep("const UPDATED='22 Nov 2026 · 15:43 IST';", "const UPDATED='22 Nov 2026 · 17:42 IST';")
open(P, 'w', encoding='utf-8').write(s)
print('meeting page applied', len(s))
