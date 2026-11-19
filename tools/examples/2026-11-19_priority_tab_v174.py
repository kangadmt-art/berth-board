#!/usr/bin/env python3
# apply20 — v174: the PRIORITY CHART becomes the fifth tab of the board (Mihir, 19 Nov 14:23: "yes add this in final").
# The tab is the approved draft (tools/priority_page/template.html), now fed from the live objects V / W / S / OPTRES and
# drawn inside a shadow root on #pqtab, so its styles and the board's cannot touch each other.
import re, shutil, sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
W = '/home/claude/work/'; P = W + 'dpa-berth-board.html'
shutil.copy(P, W + 'bak_v173.html')
B = Board(P)
t = open(W + 'prio/template.html', encoding='utf-8').read()
css = t[t.index('<style>') + 7:t.index('</style>')]
css = re.sub(r':root\{.*?\}\n', '', css, count=1, flags=re.S)
css = (":host{display:block;--gold:#d9b25f;font-family:var(--f-body);font-size:15px;line-height:1.45;color:var(--fg);margin-top:16px}\n"
       ".sub{color:var(--muted);max-width:820px}\n" + css)
body = t[t.index('<div class="sec"><div class="sechead"><h2>Hamare vessels'):t.index('</div>\n<script>')]
body = ('<p class="sub">Port ki waiting sheet ka format: har vessel ki line, priority ke column — number list ka rank hai, Y = declared par rank nahi, N = us priority mein nahi. '
        'Upar hamare vessels aur at-berth sheet. Dates berth board ka projection hain, port ka order nahi.</p>\n' + body)
js = t[t.index('const D=/*DATA*/null;\n') + len('const D=/*DATA*/null;\n'):t.index('</script>')]
a = js.index("document.getElementById('asof').innerHTML="); b = js.index("\n", a) + 1
js = js[:a] + js[b:]
if 'document.querySelector' in js: B.die('unexpected document.querySelector in the draft script')
js = js.replace('document.getElementById(', 'root.getElementById(')
if 'document.' in js: B.die('document.* left in the draft script: ' + js[js.index('document.'):js.index('document.') + 60])
def tl(x):
    if '`' in x or '${' in x: B.die('backtick / ${ in css or body')
    return x.replace('\\', '\\\\')
module = ("""// ---- PRIORITY CHART — view "priority" (v174, 19 Nov; asked by Mihir 14:09, port format chosen 14:18, approved 14:23).
// The port's waiting-sheet format: one line a vessel, a column a priority (GP · CSTL · HP · SGR · 24H · 8K/6.5K · STL/PRJ · GEN · SR 7), the cell = rank / Y / N;
// on top our vessels (rank, vessels ahead, turn by each line) and an at-berth table priority-wise. It reads the live objects (V, W, S, OPTRES) — nothing to keep by hand.
// Drawn in a shadow root so that its CSS and the board's stay apart. Source of the markup / code: tools/priority_page/template.html.
(function(){const host=document.getElementById('pqtab');if(!host||!host.attachShadow)return;
 const proj={};S.filter(x=>x.proj).forEach(x=>{proj[x.n]={b:x.b,F:x.F,cat:x.cat,via:x.via||''};});
 const D={NOW,HZ,opt:OPTRES,
  berth:V.filter(v=>v.T>NOW&&!v.span).map(v=>({slot:v.slot||v.cat,cat:v.cat,via:v.via||'',b:v.b,n:v.n,c:v.c,q:v.q,u:v.u,F:v.F,T:v.T,est:!!v.est,lt:(v.listT&&Math.abs(v.listT-v.T)>0.5)?fmt(v.listT):'',future:v.F>NOW,mine:isMine(v.n)})),
  wait:W.map(w=>{const x=w.x||'',tags=[];if(/FINISHING AT MIDSTREAM/i.test(x.slice(0,400)))tags.push('finishing at midstream');else if(/working at (MS|MRG|midstream)/i.test(x.slice(0,260)))tags.push('working at midstream');
   if(/HELD|held out|still held|no berth; held/i.test(x.slice(0,400)))tags.push('held');
   return {n:w.n,c:w.c,q:w.q,u:w.u,rdy:w.rdy,rep:w.rep,rk:w.rk,govAuto:!!w.govAuto,q7:Q7(w),noHP:!!w.noHP,allowed:allowedBerths(w),tags,mine:isMine(w.n),proj:proj[w.n]||null};})};
 const root=host.attachShadow({mode:'open'});
 root.innerHTML=`<style>""" + tl(css) + """</style>""" + tl(body) + """`;
 (function(D,root){
""" + js + """ })(D,root);
 const vb=document.getElementById('vb-priority');if(vb){const m=D.wait.filter(w=>w.mine);const RL={SAAGAR:'SGR','8K':'8K',GEN:'GEN',HP:'HP',COASTAL:'CSTL','24H':'24H',STL:'STL'};
  vb.innerHTML=m.length?m.map(w=>'<b>'+w.n.replace(/ \\(.*\\)$/,'')+'</b> · '+Object.keys(w.rk).filter(k=>RL[k]&&w.rk[k]<98).map(k=>RL[k]+' '+w.rk[k]).join(' · ')).join(' | '):'<b>'+D.wait.filter(w=>w.rdy!=null).length+'</b> ready · rank / Y / N';}
})();
""")
# ---- markup
B.rep('.views a[data-view="timber"]{--sc:var(--tmb)}', '.views a[data-view="timber"]{--sc:var(--tmb)}.views a[data-view="priority"]{--sc:#d9b25f}')
a, b = B.line_of('    <a href="#cargo" data-view="cargo">')
B.s = B.s[:b + 1] + '    <a href="#priority" data-view="priority"><b>Priority chart</b><small>Dry cargo · port\'s waiting chart · rank / Y / N in each priority</small><span class="vb" id="vb-priority"></span></a>\n' + B.s[b + 1:]
B.rep('  <div class="view" data-view="timber" id="view-timber">', '  <div class="view" data-view="priority" id="view-priority"><div id="pqtab"></div></div>\n  <div class="view" data-view="timber" id="view-timber">')
# ---- views
B.rep("const VIEWS={cargo:'Deendayal Port · Kandla · Dry cargo jetty',", "const VIEWS={cargo:'Deendayal Port · Kandla · Dry cargo jetty',priority:'Deendayal Port · Kandla · Dry cargo · priority chart',")
B.rep("const VIEW_NAME={cargo:'Cargo jetties',", "const VIEW_NAME={cargo:'Cargo jetties',priority:'Priority chart',")
B.rep("// tabs: Cargo jetties · Timber · Tuna · Liquid — same page, hash remembers the open board (#cargo / #timber / #tuna / #liquid)",
      "// tabs: Cargo jetties · Priority chart · Timber · Tuna · Liquid — same page, hash remembers the open board (#cargo / #priority / #timber / #tuna / #liquid)")
B.rep("initSections();\n// tabs:", module + "initSections();\n// tabs:")
B.save()
