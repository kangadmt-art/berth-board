#!/usr/bin/env python3
# apply73 — v277 — Mihir, 25 Nov 23:56: "Upar Priority, Salt jaise hai waise chahiye — 16 number berth non-clean cargo. And also jo sawal khule hue hain uska bhi aisa bana de upar, to turant pata chale."
# Two new TABS in the top bar, like Priority and Salt:
#   CJ-16 · non-clean  (#cj16)  — the section added at v276 moves off the Cargo page into its own tab
#   Open questions     (#sawal) — every question the board is waiting on, the question itself in one line, who has to answer; moved off the Cargo page
# LEARN rows get two new fields: ask (the question in one line) and who ('Mihir' | 'port'). Three questions asked in the chat are added as rows.
import sys, re
sys.path.insert(0, '/home/claude/berth-board/tools')
from boardpatch import Board
B = Board('/home/claude/work/dpa-berth-board.html'); q = B.q
STAMP = sys.argv[1]
def js(o):
    if isinstance(o, str): return "'" + q(o) + "'"
    return '{' + ','.join(k + ':' + js(v) for k, v in o.items()) + '}'

# ---- tabs
B.rep("<span class=\"vb\" id=\"vb-priority\"></span></a>\n",
      "<span class=\"vb\" id=\"vb-priority\"></span></a>\n"
      "    <a href=\"#sawal\" data-view=\"sawal\"><b>Open questions</b><small>Khule sawal · what the board is waiting on · who has to answer</small><span class=\"vb\" id=\"vb-sawal\"></span></a>\n")
B.rep("<span class=\"vb\" id=\"vb-salt\"></span></a>\n",
      "<span class=\"vb\" id=\"vb-salt\"></span></a>\n"
      "    <a href=\"#cj16\" data-view=\"cj16\"><b>CJ-16 · non-clean</b><small>Coal · coke · iron ore · pellets at berth 16 · how many · berth time</small><span class=\"vb\" id=\"vb-cj16\"></span></a>\n")
B.rep(".views a[data-view=\"timber\"]{--sc:var(--tmb)}", ".views a[data-view=\"sawal\"]{--sc:var(--warn)}.views a[data-view=\"cj16\"]{--sc:var(--amber)}.views a[data-view=\"timber\"]{--sc:var(--tmb)}")
B.rep("salt:'Deendayal Port · Kandla · Salt vessels',", "salt:'Deendayal Port · Kandla · Salt vessels',cj16:'Deendayal Port · Kandla · CJ-16 · non-clean cargo',sawal:'Deendayal Port · Kandla · Open questions',")
B.rep("const VIEW_NAME={ppp:'CJ-9 · CJ-10',salt:'Salt',", "const VIEW_NAME={ppp:'CJ-9 · CJ-10',cj16:'CJ-16 · non-clean cargo',sawal:'Open questions',salt:'Salt',")

# ---- the two views; the two sections leave the Cargo page
a = B.s.index("  <section class=\"card\" data-sec=\"c16\" aria-labelledby=\"c16h\">"); b = B.s.index("  <section class=\"card\" data-sec=\"mpt\" aria-labelledby=\"mp\">")
B.s = B.s[:a] + B.s[b:]
a = B.s.index("  <section class=\"card\" data-sec=\"learn\" aria-labelledby=\"lh\">"); b = B.s.index("</section>", a) + len("</section>\n")
assert 'id="learn"' in B.s[a:b]
B.s = B.s[:a] + B.s[b:]
B.rep("const SEC_OPEN_DEFAULT=new Set(['finder','mine','hpb','c16']);", "const SEC_OPEN_DEFAULT=new Set(['finder','mine','hpb']);")
B.rep("  <div class=\"view\" data-view=\"salt\" id=\"view-salt\">",
      "  <div class=\"view\" data-view=\"sawal\" id=\"view-sawal\">\n"
      "  <div class=\"tsum\" id=\"sawalstats\" aria-label=\"Open questions — summary\" style=\"grid-template-columns:repeat(3,minmax(0,1fr))\"></div>\n"
      "  <section class=\"card\"><div class=\"sechead\"><h2 id=\"lh\">Open questions · khule sawal</h2><p>What the board is waiting on, newest first. <b>Mihir to say</b> = it needs your word — answer in the chat and it goes into the rules and leaves this page. <b>Waits for the port</b> = the next programme or meeting settles it. Tap a question for the background.</p></div>\n"
      "    <div class=\"learn\" id=\"learn\"></div>\n"
      "  </section>\n"
      "  </div>\n"
      "  <div class=\"view\" data-view=\"cj16\" id=\"view-cj16\">\n"
      "  <div class=\"tsum\" id=\"c16tiles\" aria-label=\"CJ-16 non-clean cargo — summary\" style=\"grid-template-columns:repeat(4,minmax(0,1fr))\"></div>\n"
      "  <section class=\"card\"><div class=\"sechead\"><h2 id=\"c16h\">CJ-16 · non-clean cargo vessels</h2><p id=\"c16sub\"></p></div><div id=\"c16tbl\"></div></section>\n"
      "  <section class=\"card\"><div class=\"sechead\"><h2>Every vessel at CJ-16 · record</h2><p>Every call at CJ-16 on the board's record since 28 Oct 2026 — clean and non-clean, newest first. The non-clean ones are marked.</p></div><div id=\"c16all\"></div></section>\n"
      "  </div>\n"
      "  <div class=\"view\" data-view=\"salt\" id=\"view-salt\">")

# ---- c16(): tiles in the tab style + the tab's own line
B.rep("const sub=document.getElementById('c16sub'),st=document.getElementById('c16stats'),tb=", "const sub=document.getElementById('c16sub'),st=document.getElementById('c16tiles'),tb=")
a = B.s.index("  if(st)st.innerHTML=nc.length?["); b = B.s.index("  const TH=['Vessel','Cargo','MT','I / E','Berthed under'", a)
B.s = B.s[:a] + (
  "  const tp=(c,v,l)=>`<div class=\"tp\" style=\"--sc:${c}\"><b>${v}</b><span>${l}</span></div>`;\n"
  "  if(st)st.innerHTML=tp('var(--warn)',been.length,'non-clean vessels so far'+(been.length?' · '+Object.entries(been.reduce((a,r)=>{const k=NC16_FAM(r.c);a[k]=(a[k]||0)+1;return a;},{})).map(([k,n])=>n+' '+k.toLowerCase()).join(' · '):''))\n"
  "    +tp('var(--gold)',next.length,'coming'+(next.length?' · '+next.map(r=>r.n+' ~'+fmt(r.F).replace(/ \\d\\d:\\d\\d$/,'')).join(' · '):''))\n"
  "    +tp('var(--dry)',nf.format(Math.round(mt)),'MT of non-clean cargo so far')\n"
  "    +tp('var(--brk)',nc.length?d1(used):'0',nc.length?`berth-days · ${Math.round(used/span*100)} % of CJ-16's time since ${fmt(first).replace(/ \\d\\d:\\d\\d$/,'')}`:'berth-days');\n"
  "  {const vb=document.getElementById('vb-cj16');if(vb)vb.innerHTML=`<b>${been.length}</b> so far · <b>${next.length}</b> coming`;}\n"
  "  if(sub&&since.length)sub.innerHTML+=` Since ${fmt(first).replace(/ \\d\\d:\\d\\d$/,'')} CJ-16 has taken <b>${since.length} vessels</b>: ${Object.entries(mix).sort((a,z)=>z[1]-a[1]).map(([k,n])=>n+' '+k).join(' · ')}.`;\n") + B.s[b:]

# ---- learn(): the question first
B.rep("const card=(x,i)=>`<details class=\"lc ${x.st}\" ${openAll?'open':''}><summary class=\"hd\"><div><b><span class=\"sn\">${i+1}</span>${x.v}</b><small>${x.d}</small></div><span class=\"st\">${L[x.st]||x.st}</span></summary>",
      "const WHO=x=>x.who==='port'?'Waits for the port':'Mihir to say';\n"
      "  const card=(x,i)=>`<details class=\"lc ${x.st}\"><summary class=\"hd\"><div><b><span class=\"sn\">${i+1}</span>${x.ask||x.v}</b><small>${x.ask?x.v+' · ':''}${x.d}</small></div><span class=\"st\"${x.st==='open'&&x.who!=='port'?' style=\"color:var(--warn);border-color:var(--warn)\"':''}>${x.st==='open'?WHO(x):(L[x.st]||x.st)}</span></summary>")
B.rep("const O=LEARN.filter(x=>x.st==='open'), C=LEARN.filter(x=>x.st!=='open');",
      "const O=LEARN.filter(x=>x.st==='open').sort((a,z)=>(a.who==='port')-(z.who==='port')), C=LEARN.filter(x=>x.st!=='open'); // Mihir's questions first, then those the port will settle\n"
      "  {const nm=O.filter(x=>x.who!=='port').length,tp=(c,v,l)=>`<div class=\"tp\" style=\"--sc:${c}\"><b>${v}</b><span>${l}</span></div>`,ss=document.getElementById('sawalstats'),vb=document.getElementById('vb-sawal');\n"
      "   if(ss)ss.innerHTML=tp('var(--warn)',O.length,'open questions')+tp('var(--amber)',nm,'Mihir to say')+tp('var(--dry)',O.length-nm,'wait for the port');\n"
      "   if(vb)vb.innerHTML=O.length?`<b>${O.length}</b> open · <b>${nm}</b> for Mihir`:'none open';}")

# ---- the questions: ask + who on the three open rows, and three asked in the chat
def addf(prefix, ask, who):
    a, b = B.line_of(prefix); ln = B.s[a:b]
    assert ln.count(",v:'") >= 1 and "ask:'" not in ln
    i = ln.index(",v:'"); ln = ln[:i] + ",ask:" + js(ask) + ",who:" + js(who) + ln[i:]
    B.s = B.s[:a] + ln + B.s[b:]
addf(" {d:'25 Nov 16:11 · programme 26.11 — MSC Magali \"HP(50K)\" at CJ-16'", "Is any waiting vessel bidding for HP? You said none; programme 26.11 then printed MSC Magali as HP(50K).", 'Mihir')
addf(" {d:'23 Nov 14:10 · programme 24.11 — the meeting of 23 Nov'", "When the team puts a vessel on hold and a later port list still prints her ready and ranked — should the board drop the hold?", 'Mihir')
addf(" {d:'21 Nov 20:25 · Circular 5237, point (i) — vacant Govt / Coastal places'", "Will the port give a vacant Govt / Coastal place to the SAAGAR line before a 30K quote? First test: Parvraj's Govt place, at the meeting of 26 Nov.", 'port')
NEW = [
 {'d': '25 Nov 23:52 · CJ-16 non-clean cargo', 'ask': "Are aggregates to be counted as non-clean cargo at CJ-16?", 'who': 'Mihir', 'v': 'Which cargoes count as non-clean at CJ-16.',
  'exp': "The CJ-16 tab counts coal, coke (petcoke too), iron ore and pellets — the cargoes of Trade Notice 3089.",
  'act': "Two aggregates vessels have also lain at CJ-16: Alasia (1 to 3 Nov, before the notice) and Evangelia D (16 to 17 Nov).",
  'why': "Aggregates were berthed at CJ-16 before the berth was opened to coal and ore, so the board has left them out.",
  'fix': "If they are to be counted, the tally goes from 1 to 3 vessels so far. OPEN — Mihir to say.", 'st': 'open'},
 {'d': '25 Nov 17:06 · our vessels by stevedore', 'ask': "Which waiting or expected vessels are ours as stevedore only (another firm is the agent)?", 'who': 'Mihir', 'v': 'Vessels where Mihir & Company is the stevedore but not the agent.',
  'exp': "A vessel is ours when Mihir & Company is her agent or her stevedore (Mihir, 25 Nov 17:02).",
  'act': "The stevedore is printed only on the DPR — after a vessel has started work. For a vessel still waiting, no paper names it.",
  'why': "Until the name is given, such a vessel is not marked as ours and gets no reading of her own.",
  'fix': "Name them in the chat; they are marked ours at once. OPEN — Mihir to say.", 'st': 'open'},
 {'d': '25 Nov 16:33 · revised list 25.11 — Steel / Project ranks', 'ask': "Should Josco Taicang (STL 2) and Jumbo Kinetic (STL 3) be counted in the Steel / Project line? On 15 Nov you kept that rank out for Xin Hai Tong 71.", 'who': 'Mihir', 'v': 'Steel / Project ranks the board is not using.',
  'exp': "The list prints STL 2 for Josco Taicang and STL 3 for Jumbo Kinetic.",
  'act': "The board does not use these two ranks: on 15 Nov Mihir said to keep the STL rank out for Xin Hai Tong 71, and the board applied the same to these two on its own.",
  'why': "Xin Hai Tong 71 has since berthed as \"PROJ\"; the Steel / Project place falls vacant when she sails, about 26 Nov.",
  'fix': "If yes, Josco Taicang is the next vessel for that place. OPEN — Mihir to say.", 'st': 'open'},
]
B.rep("const LEARN=[\n", "const LEARN=[\n" + "".join(" " + js(r) + ",\n" for r in NEW))
B.s = re.sub(r"const UPDATED='[^']*';", "const UPDATED='" + STAMP + "';", B.s, count=1)
B.save(); print('saved 73')
