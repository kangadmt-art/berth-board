# v259 — (1) the meeting berth-by-berth section moves to the top of the Priority chart page; the separate Meeting tab is removed (Mihir, 22 Nov 17:56);
# (2) a pick that rests on a place freeing later in the window says so and shows the line that takes the berth otherwise (CJ-15A: 8K only if Crystal O sails in the window).
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
JS = open('/home/claude/work/mtg/meetboard3.js', encoding='utf-8').read()
CSS = open('/home/claude/work/mtg/meetboard3.css', encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
a = s.index('// ---- MEETING page (Mihir, 22 Nov 2026)'); b = s.index('function preview(){\n', a); s = s[:a] + JS + s[b:]
a = s.index('/* v257 Meeting page'); b = s.index('</style>', a); s = s[:a] + CSS + s[b:]
# the tab goes; its link still opens the Priority chart page
a = s.index('    <a href="#meeting" data-view="meeting">'); b = s.index('\n', a) + 1; s = s[:a] + s[b:]
rep("meeting:'Deendayal Port · Kandla · Berthing meeting',", "")
rep("const VIEW_NAME={meeting:'Meeting',ppp:", "const VIEW_NAME={ppp:")
rep("function setView(k,opts){opts=opts||{};if(!VIEWS[k])k='cargo';", "function setView(k,opts){opts=opts||{};if(k==='meeting')k='priority';if(!VIEWS[k])k='cargo';")
a = s.index('  <div class="view" data-view="meeting" id="view-meeting">'); b = s.index('  <div class="view" data-view="priority" id="view-priority">', a); s = s[:a] + s[b:]
rep('<div class="view" data-view="priority" id="view-priority"><div id="pqtab"></div></div>',
    '<div class="view" data-view="priority" id="view-priority">\n  <section class="card mbsec"><div class="mbhead"><a class="mbjump" href="#priority" onclick="document.getElementById(\'pqtab\').scrollIntoView({behavior:\'smooth\'});return false;">Priority chart ↓</a><div class="mbey">Agli meeting · berth-wise</div><h2 id="mbh"></h2><p id="mbsub"></p></div><div id="mtgb"></div></section>\n  <div id="pqtab"></div></div>')
rep("<small>Dry cargo · port's waiting chart · rank / Y / N in each priority</small>", "<small>Next meeting berth by berth · port's waiting chart · rank / Y / N in each priority</small>")
# the old #meeting link opens the Priority chart page
rep("window.addEventListener('hashchange',()=>{const k=location.hash.replace('#','');if(VIEWS[k]&&k!==VIEW)", "window.addEventListener('hashchange',()=>{let k=location.hash.replace('#','');if(k==='meeting')k='priority';if(VIEWS[k]&&k!==VIEW)")
rep("{let k0=(location.hash||'').replace('#','');if(!VIEWS[k0]){", "{let k0=(location.hash||'').replace('#','');if(k0==='meeting')k0='priority';if(!VIEWS[k0]){")
rep("const UPDATED='22 Nov 2026 · 17:52 IST';", "const UPDATED='22 Nov 2026 · 18:03 IST';")
assert 'data-view="meeting"' not in s and s.count('function meetBoard(') == 1
open(P, 'w', encoding='utf-8').write(s)
print('v259 applied', len(s))
