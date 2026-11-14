#!/usr/bin/env python3
# apply14h — v159 (part 3): Mihir's SAAGAR confirmation recorded; texts, snapshot, prediction log, own-vessel log and learning card after the HP-slot correction
import re, sys, json
W='/home/claude/work/'; P=W+'dpa-berth-board.html'
s=open(P,encoding='utf-8').read(); n0=len(s)
S=json.load(open(W+'S159.json')); byn={x['n']:x for x in S}
def die(m): print(m); sys.exit(1)
def rep(old,new,cnt=1):
    global s
    k=s.count(old)
    if k!=cnt: die('ANCHOR FAIL (%d found, want %d): %r'%(k,cnt,old[:150]))
    s=s.replace(old,new)
MON={'10':'Oct','11':'Nov','12':'Dec'}
def nice(t): return "%d %s %s"%(int(t[3:5]),MON[t[:2]],t[6:])
CL={'GOV':'Govt','COASTAL':'Coastal','HP':'Higher productivity','SAAGAR':'SAAGAR','24H':'24 hrs','8K':'6.5K / 8K','STL':'Steel / project','BIT':'Bitumen slot','GEN':'General'}
def how(x): return CL.get(x['cat'],x['cat'])+((' — as '+x['via']) if x['via'] else '')
def js(t): return t.replace("\\","\\\\").replace("'","\\'")

# ---- A. rule comment
rep("          // Regulation (Mihir, 1 Nov): 1 slot bulk, 1 slot break bulk (logs); a free BULK slot may be given to break bulk, not the reverse.\n",
    "          // Regulation (Mihir, 1 Nov): 1 slot bulk, 1 slot break bulk (logs); a free BULK slot may be given to break bulk, not the reverse.\n"
    "          // Confirmed (Mihir, 14 Nov 18:00): SAAGAR bulk and break bulk are separate priorities. With no bulk vessel waiting, a SAAGAR break-bulk vessel takes the berth and the priority is occupied;\n"
    "          // when a berth frees again, a waiting SAAGAR bulk vessel gets it — even if a break-bulk SAAGAR vessel is senior to her.\n")

# ---- B. Rome Trader row note
rep("so the board gives her the place that frees when Enishi finishes, ahead of the next log vessel; the rank 5 here is a placeholder until the list prints her number.",
    "so the place that frees when Enishi finishes is hers, ahead of the next log vessel even though the log vessel is senior (confirmed by Mihir, 14 Nov 18:00); the rank 5 here is a placeholder until the list prints her number.")

# ---- C. option notes
a=s.index("note:'The route printed on the list (\"SGR- NEELKANTH\"). SAAGAR is one bulk place"); b=s.index("'}",a)
s=s[:a]+"note:'The route printed on the list (\"SGR- NEELKANTH\"). SAAGAR bulk and break bulk are separate priorities (Mihir, 14 Nov): log vessels hold both places today only because no bulk vessel was waiting, and the place Enishi vacates goes to her ahead of Uni Blossom (SGR 1). Enishi finishes ~16 Nov 17:00 on the DPR pace — inside the window of the 15 Nov meeting — so that meeting can programme her. CJ-16 (free ~15 Nov 19:00) goes first to the HP queue (Evangelia D, HN Doris), which stands above SAAGAR; her berth is CJ-14 at Theometor\\'s permissible time (16 Nov 02:06), or CJ-15 behind Enishi (~16 Nov 19:00) if Theometor is not moved."+s[b:]
rep("HP queue on list 14.11: Gokova-M (1), Evangelia D (2), HN Doris (3); she would rank next by her arrival.'}",
    "HP queue on list 14.11: Gokova-M (1), Evangelia D (2), HN Doris (3); she would rank next by her arrival. One HP place frees when Cape Diversity sails and Evangelia D takes CJ-16 with it — so HP is later than SAAGAR for her.'}")
rep("African Hornbill (SGR 2) berths under 24 HRS tomorrow; AG Varvara (3) is projected under General.'}",
    "African Hornbill (SGR 2) berths under 24 HRS tomorrow; AG Varvara (3) is projected under General — if she takes the SAAGAR place instead, CD Glory waits for the next one (about 27 Nov).'}")

# ---- D. prediction snapshot
t=open(W+'apply14d.py',encoding='utf-8').read(); a=t.index("fixed=[\n"); b=t.index("\n]\n",a)+3
ns={}; exec(t[a:b],ns); fixed=ns['fixed']
proj=[[x['n'],x['b'],nice(x['F']),'board projection — '+how(x)+(' · after '+x['prev'] if x['prev'] else '')] for x in S if x['F']<='11-19 12:00']
rows=fixed+proj
i=s.index("const PRED=["); j=s.index("\n];",i)
s=s[:i]+"const PRED=[ // snapshot 14 Nov 18:20 (v159) — list 14.11 + programme 15.11 applied, HP-slot count corrected; for the 14 Nov day / night sheets, DPR 15.11, list 15.11, programme 16.11\n "+",".join("['%s','%s','%s','%s']"%(js(a_),b_,c_,js(d_)) for a_,b_,c_,d_ in rows)+s[j:]

# ---- E. prediction log
def addnote(anchor,extra):
    global s
    if s.count(anchor)!=1: die('PREDLOG anchor (%d): %s'%(s.count(anchor),anchor[:90]))
    a=s.index(anchor); e=s.index("\n",a); l=s[a:e]; k=l.rindex("'}")
    s=s[:a]+l[:k]+extra+l[k:]+s[e:]
SUP=" · SUPERSEDED 14 Nov 18:00 — the board had counted Bomustafao O against the HP slot; corrected, CJ-16 goes to an HP vessel and the picks behind it move"
for n in ('Rome Trader (salt, next call)','Rahma','Saga Viking','AG Varvara','Propel Confidence'):
    addnote("{v:'%s',predAt:'11-14 16:00',"%js(n),SUP)
def prow(n,note):
    x=byn[n]; return " {v:'%s',predAt:'11-14 18:00',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}"%(js(n),x['b'],x['F'],js(note))
new=[
 prow('Evangelia D','18:00 re-run (HP-slot correction) — Higher productivity (HP 2), CJ-16 after Cape Diversity; the list still carries "DOC NR" beside her readiness — if she is not taken, HN Doris (HP 3) is next for the berth'),
 prow('Rome Trader (salt, next call)',"18:00 re-run (HP-slot correction) — Mihir & Co — SAAGAR bulk place (rule confirmed by Mihir), CJ-14 at Theometor's permissible time; CJ-15 behind Enishi if Theometor is not moved"),
 prow('Rahma','18:00 re-run (HP-slot correction) — Steel / project (STL 1), CJ-13 after African Peacock is moved to CJ-5 (port convenience)'),
 prow('Saga Viking','18:00 re-run (HP-slot correction) — General (GEN 2), CJ-1 after Drake Well'),
 prow('Propel Confidence','18:00 re-run (HP-slot correction) — 30k/25k quote against the 24-hr slot, CJ-16 after Evangelia D'),
 prow('AG Varvara','18:00 re-run (HP-slot correction) — General against the Bitumen slot, CJ-5 after African Peacock'),
]
a=s.index("const PREDLOG=["); b=s.index("\n];",a)
s=s[:b]+",\n"+",\n".join(new)+s[b:]

# ---- F. own-vessel log
r=byn['Rome Trader (salt, next call)']; g=byn['CD Glory']
a=s.index(" 'CD Glory':[\n"); b=s.index("\n ],\n 'Rome Trader (salt, next call)':[",a)
s=s[:b]+(",\n  {d:'14 Nov 18:00 · after the HP-slot correction',exp:'%s',b:'%s',slot:'SAAGAR ~21 Nov 01:30 at CJ-4 (board\\'s earliest) · General ~21 Nov 18:00 at CJ-4 · 6.5K / 8K ~26 Nov 23:50 at CJ-4',why:'Her date does not move. The SAAGAR place she is counted for is the one Rome Trader leaves (~18 Nov 19:00): AG Varvara (SGR 3) is projected into CJ-5 under General a few hours earlier, so the place is CD Glory\\'s when CJ-4 clears behind Pioneer Fortune. If AG Varvara takes that SAAGAR place instead, CD Glory\\'s SAAGAR date becomes about 27 Nov and General (~21 Nov evening) is the earlier route.'}"%(g['F'],g['b']))+s[b:]
a=s.index(" 'Rome Trader (salt, next call)':[\n"); b=s.index("\n ]\n};",a)
s=s[:b]+(",\n  {d:'14 Nov 18:00 · Mihir confirms the SAAGAR rule · board correction',exp:'%s',b:'%s',slot:'SAAGAR — bulk place · CJ-14 at Theometor\\'s permissible time, else CJ-15 behind Enishi ~16 Nov 19:00 · HP if declared ~17 Nov 12:00 at CJ-16',why:'Mihir (14 Nov 18:00): SAAGAR bulk and break bulk are separate priorities — with no bulk vessel waiting a break-bulk vessel takes the berth and the priority is occupied; when a berth frees again the waiting bulk vessel gets it even if a break-bulk vessel is senior. So the place Enishi vacates is Rome Trader\\'s. Her BERTH changes from the 16:30 reading: the board had still counted Bomustafao O (a General cross-fill of 8 Nov) against the HP slot and so offered CJ-16 to SAAGAR. Corrected, CJ-16 after Cape Diversity goes to the HP queue (Evangelia D, HP 2; else HN Doris, HP 3) — HP stands above SAAGAR. Rome Trader takes the next clean berth: CJ-14 when Theometor reaches her permissible time (16 Nov 02:06) → ~04:00. Theometor is running about 1½ days behind (DPR pace ~17 Nov 19:30) and the port has not pulled Bomustafao O out at hers, so CJ-14 may not be cleared; then it is CJ-15 behind Enishi, ~16 Nov 19:00. Either way she needs the 15 Nov meeting to programme her.'}"%(r['F'],r['b']))+s[b:]

# ---- G. learning card
rep("OPEN (1): Rome Trader — only \"SGR Y\" is printed. Does the port give a SAAGAR BULK vessel the place ahead of the log vessels in the SGR queue (board: yes — CJ-16 from the night of the 15th), or does she stand behind Uni Blossom and AG Varvara (then ~18 Nov, CJ-13)? And is SAAGAR the only route to be declared?",
    "(1) ANSWERED (Mihir, 14 Nov 18:00): yes — a waiting SAAGAR bulk vessel gets the freed place even if a break-bulk vessel is senior; see the 18:00 entry, where her berth is corrected to CJ-14 on 16 Nov. Still OPEN on Rome Trader: is SAAGAR the only route to be declared?")
rep("const LEARN=[\n","const LEARN=[\n"
 " {d:'14 Nov 18:00 · Mihir + board check',v:'RULE CONFIRMED — SAAGAR bulk and break bulk are separate priorities. BOARD ERROR FOUND while checking Rome Trader\\'s date on that rule: Bomustafao O was still counted against the HP slot, so the board saw HP as full and gave CJ-16 to SAAGAR.',"
 "exp:'v158 (16:30): CJ-16 after Cape Diversity → Rome Trader under SAAGAR bulk, 15 Nov ~21:00; the HP slot \"no taker\"; Rahma CJ-14 on 16 Nov 04:00.',"
 "act:'Mihir: bulk and break bulk are separate SAAGAR priorities. If no bulk vessel is waiting, a SAAGAR break-bulk vessel gets the berth and the priority is occupied; when a berth frees again and a SAAGAR bulk vessel is waiting, she gets it even if a SAAGAR break-bulk vessel is senior. — List 14.11 prints Bomustafao O under GENERAL (CJ-2), and from 12 Nov two HP vessels lay alongside while she worked (Cape Diversity + Chang Hang, then Cape Venture): her 8 Nov cross-fill (\"C/F\") against the vacant HP slot does not hold that slot against a real HP vessel.',"
 "why:'The bulk-first order was already in the board (regulation of 1 Nov) and stands as coded. The error was in the slot count: a General vessel cross-filled against HP was treated as an HP occupant for good. HP stands above SAAGAR in the slot order, and two HP vessels that fit CJ-16 are ready (Evangelia D, HP 2; HN Doris, HP 3) — so CJ-16 is theirs before Rome Trader\\'s.',"
 "fix:'v159: Bomustafao O carried as a General vessel; a General cross-fill no longer blocks a real HP vessel; CJ-16 after Cape Diversity → Evangelia D (HP); Rome Trader → CJ-14, ~16 Nov 04:00, in the SAAGAR bulk place — CJ-15 behind Enishi (~16 Nov 19:00) if the port does not clear Theometor at her permissible time. Also: the port-convenience shift is now made for the group\\'s SENIOR vessel that needs a clean berth, by cargo or by her berth requirement (Rahma, STL 1, REQ CJ 13–16, was being passed over for Heng Yuan Fa Zhan, STL 2). The 16:30 predictions that changed are kept in the log and marked superseded.',st:'adopted'},\n")

open(P,'w',encoding='utf-8').write(s); print('ok h',n0,'->',len(s))
