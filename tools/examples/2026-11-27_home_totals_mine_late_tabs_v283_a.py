#!/usr/bin/env python3
# apply79 — v283. Mihir, 27 Nov 14:46: totals (vessels waiting / expected) on top, the page icons under them · the 10-day berth timeline is of no use now ·
# "Routine se hat ke" in a page of its own · news not needed — take it out · Mihir & Company in an icon of its own · keep everything simple.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'); s = B.s
def cut(start, end):
    global s
    assert s.count(start) == 1, start
    a = s.index(start); b = s.index(end, a) + len(end); blk = s[a:b]; s = s[:a] + s[b:]; return blk
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70]); s = s.replace(a, b)
mine = cut('  <section class="card mine" data-sec="mine"', '  </section>\n').replace(' data-sec="mine"', '')
rules = cut('  <section class="card" data-sec="rules"', '  </section>\n').replace(' data-sec="rules"', '')
stats = cut('  <div class="stats" id="stats" aria-label="Waiting at Kandla"></div>\n', '')
news = cut('  <section class="card" aria-labelledby="nwh">', '  </section>\n')
gantt = cut('  <section class="card" data-sec="gantt">', '  </section>\n')
# totals on top, above the page icons (home tab only)
rep('  <nav class="views" id="views" aria-label="Boards on this page">\n', '  <div class="stats topstats" id="stats" aria-label="Waiting at Kandla"></div>\n  <nav class="views" id="views" aria-label="Boards on this page">\n')
# new tabs
rep('    <a href="#priority" data-view="priority">', '    <a href="#mine" data-view="mine"><b>Mihir &amp; Co</b><small>Our vessels · where each one stands · when it berths</small><span class="vb" id="vb-mine"></span></a>\n    <a href="#priority" data-view="priority">')
rep('    <a href="#barge" data-view="barge">', '    <a href="#late" data-view="late"><b>Routine se hat ke</b><small>Not sailing on time · past ETC · sailing postponed</small><span class="vb" id="vb-late"></span></a>\n    <a href="#barge" data-view="barge">')
rep('  <div class="view" data-view="priority" id="view-priority">\n', '  <div class="view" data-view="mine" id="view-mine">\n' + mine + '  </div>\n  <div class="view" data-view="late" id="view-late">\n' + rules + '  </div>\n'
    + '  <div hidden style="display:none" aria-hidden="true">\n' + news.replace('<section class="card"', '<section') + gantt.replace(' data-sec="gantt"', '').replace('<section class="card"', '<section') + '  </div>\n'
    + '  <div class="view" data-view="priority" id="view-priority">\n')
rep("const VIEWS={dpr:", "const VIEWS={mine:'Deendayal Port · Kandla · Mihir & Company vessels',late:'Deendayal Port · Kandla · Not sailing on time',dpr:")
rep("const VIEW_NAME={dpr:'DPR',", "const VIEW_NAME={mine:'Mihir & Co',late:'Routine se hat ke',dpr:'DPR',")
rep('.views a[data-view="dpr"]{--sc:var(--dry)}', '.views a[data-view="mine"]{--sc:var(--brass)}.views a[data-view="late"]{--sc:var(--bad)}body:not([data-view="cargo"]) .topstats{display:none}.topstats{margin:0 0 14px}\n.views a[data-view="dpr"]{--sc:var(--dry)}')
# the totals tile alone on top; Timber and Salt tiles join "More figures" (their pages have icons of their own)
rep("if(all.length===12){const keep=[all[10],all[11],all[0]],more=all.filter(e=>!keep.includes(e));", "if(all.length===12){const keep=[all[0]],more=all.filter(e=>!keep.includes(e));")
rep("<summary>More figures · dry cargo by commodity · import / export · bulk · bagged · break bulk · expected · berths occupied · oil jetties · Tuna</summary>", "<summary>More figures · dry cargo by commodity · import / export · bulk · bagged · break bulk · timber · salt · oil jetties · Tuna</summary>")
rep("Dry cargo berths CJ-1–16 run under the berthing policy (projected below) · liquid and Tuna are status only, and timber vessels have their own sheet — tabs above:", "Dry cargo berths CJ-1–16 run under the berthing policy · liquid and Tuna are status only · every page has its icon below:")
# badges
rep("  setSum('mine',", "  {const vb=document.getElementById('vb-mine');if(vb)vb.innerHTML=sts.length?`<b>${sts.length}</b> vessel${sts.length===1?'':'s'}${atB?' · '+atB+' at berth':''}${nx?' · next '+nx.n.replace(/\\s*\\(.*\\)\\s*$/,'')+' '+fday(nx.F):''}`:'no vessel today';}\n  setSum('mine',")
rep("  setSum('rules',", "  {const vb=document.getElementById('vb-late');if(vb)vb.innerHTML=rc?`<b>${rc}</b> vessel${rc===1?'':'s'} past ETC`:'nobody past ETC';}\n  setSum('rules',")
rep("const SEC_OPEN_DEFAULT=new Set(['finder','mine','hpb']);", "const SEC_OPEN_DEFAULT=new Set(['finder','quay','hpb']);")
rep('<span>Sections open on tap · detail only when you want it</span>', '<span>Tap a heading to open or close it</span>')
B.s = s; B.save()
