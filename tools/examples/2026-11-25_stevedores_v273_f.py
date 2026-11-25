#!/usr/bin/env python3
# apply69f — v273 part 6 — Mihir, 25 Nov 16:23: "agar stevedoring company ka naam ho to woh bhi dikhaya karo".
# The DPR prints the stevedore of every working vessel (column "Stevd."). tools/stevedores.py reads it from every xlsx DPR in data/ and writes const STV;
# the board shows it beside the agent wherever a vessel's agent is shown and a stevedore is on record. Re-run the tool with every new xlsx DPR.
import sys
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html')
STV = open('/home/claude/work/stv/stv.js', encoding='utf-8').read().strip()
assert STV.startswith('const STV={') and STV.endswith('};')
B.rep("const agTxt=n=>AG[n]?' · agent '+AG[n]:'';",
  "// ---- stevedores (Mihir, 25 Nov 16:23): as the DPR prints them — written by tools/stevedores.py from every xlsx DPR in data/. key = vessel name, capitals / digits only; value = runs [first DPR day, last DPR day, stevedore]\n"
  + STV + "\n"
  "const stvKey=n=>String(n).replace(/\\s*\\(.*?\\)/g,'').toUpperCase().replace(/\\bWITH\\b/g,'').replace(/[^A-Z0-9]/g,'');\n"
  "// stvOf(name, t, te): the stevedore on the DPRs of the call that began about hour t (made fast, or reporting for a waiting vessel) and ended te; without t, the last one printed (never for a \"next call\" name — that would be the earlier call's)\n"
  "const stvOf=(n,t,te)=>{const r=STV[stvKey(n)];if(!r||!r.length)return '';const H=d=>h(d+' 07:00');if(t==null)return /next call/i.test(String(n))?'':r[r.length-1][2];const x=r.slice().reverse().find(e=>H(e[1])>=t-24&&H(e[0])<=(te!=null?te+24:t+60*24));return x?x[2]:'';};\n"
  "const stvS=(n,t,te)=>{const s=stvOf(n,t,te);return s?'<br><small class=\"stv\">stev. '+s+'</small>':'';};\n"
  "const agSt=(n,t,te)=>(agOf(n)||'—')+stvS(n,t,te);\n"
  "const agTxt=n=>(AG[n]?' · agent '+AG[n]:'')+(stvOf(n)?' · stevedore '+stvOf(n):'');")
i = B.s.index('</style>'); B.s = B.s[:i] + ".stv{color:var(--muted);font-size:11px;font-weight:400;white-space:nowrap}\n" + B.s[i:]
# HP table
B.rep("'Ready / ETA','Agent','Berths she can use'", "'Ready / ETA','Agent · stevedore','Berths she can use'")
B.rep("<td class=\"l\">${agOf(w.n)}</td><td class=\"l\">${c.al.length", "<td class=\"l\">${agSt(w.n,w.rep)}</td><td class=\"l\">${c.al.length")
# next-meeting section
B.rep("ag(w.n)?'agent '+ex(ag(w.n)):'',", "ag(w.n)?'agent '+ex(ag(w.n)):'',stvOf(w.n,w.rep)?'stevedore '+ex(stvOf(w.n,w.rep)):'',")
B.rep("ag(v.n)?'agent '+ex(ag(v.n)):'',", "ag(v.n)?'agent '+ex(ag(v.n)):'',stvOf(v.n,F0)?'stevedore '+ex(stvOf(v.n,F0)):'',")
# Salt page
B.rep("${agOf(v.n)||'—'}</td></tr>`;}));}", "${agSt(v.n,v.F)}</td></tr>`;}));}", 2)
B.rep("${agOf(w.n)||'—'}</td></tr>`;}));}", "${agSt(w.n,w.rep)}</td></tr>`;}));}", 2)
B.rep("'MT a day','Out about','Agent']", "'MT a day','Out about','Agent · stevedore']")
B.rep("'Waited by then','Under','Agent']", "'Waited by then','Under','Agent · stevedore']")
B.rep("'Board: berth','Board: about','Board: under','Agent']", "'Board: berth','Board: about','Board: under','Agent · stevedore']", 2)
B.rep("<td class=\"l\">${r.ag||'—'}</td></tr>`).join('')+`<tr class=\"tot\"><td class=\"l\">${FM[k%100]} total", "<td class=\"l\">${r.ag||'—'}${stvS(r.n,r.mf,r.out)}</td></tr>`).join('')+`<tr class=\"tot\"><td class=\"l\">${FM[k%100]} total")
B.rep("<th>MT a day</th><th class=\"l\">Agent</th></tr>';", "<th>MT a day</th><th class=\"l\">Agent · stevedore</th></tr>';")
# Timber page
B.rep("<td class=\"l\">${ag(r)}</td></tr>", "<td class=\"l\">${ag(r)}${stvS(r.n,r.mf!=null?r.mf:(r.nor!=null?r.nor:null))}</td></tr>", 3)
B.rep("'At completion','Agent']", "'At completion','Agent · stevedore']", 2)
B.rep("'Board: about','From','Agent']", "'Board: about','From','Agent · stevedore']")
B.rep("<td>${resC(r)}</td><td class=\"l\">${r.ag||'—'}</td></tr>`).join('')", "<td>${resC(r)}</td><td class=\"l\">${r.ag||'—'}${stvS(r.n,r.mf,r.done)}</td></tr>`).join('')")
B.rep("<th>Demurrage / despatch</th><th class=\"l\">Agent</th></tr>';", "<th>Demurrage / despatch</th><th class=\"l\">Agent · stevedore</th></tr>';")
# CJ-9 / 10 card, waiting table, berth detail
B.rep("· agent ${agOf(cur.n)}</small>", "· agent ${agOf(cur.n)}${stvOf(cur.n,cur.F)?' · stevedore '+stvOf(cur.n,cur.F):''}</small>")
B.rep("<td class=\"l\">${(typeof AG!=='undefined'&&AG[w.n])||'—'}</td></tr>`;}).join('');", "<td class=\"l\">${(typeof AG!=='undefined'&&AG[w.n])||'—'}${stvS(w.n,w.rep!=null?w.rep:(atB?w.F:null))}</td></tr>`;}).join('');")
B.rep("<th>LOA m</th><th class=\"l\">Agent</th></tr></thead>", "<th>LOA m</th><th class=\"l\">Agent · stevedore</th></tr></thead>")
B.rep("['Agent',agOf(n)],", "['Agent',agOf(n)],...((sv=>sv?[['Stevedore',sv]]:[])(stvOf(n,v.proj?(v.w?v.w.rep:null):v.F))),")
B.save(); print('saved 69f')
