#!/usr/bin/env python3
# apply14d — v158 (part 2): prediction snapshot, prediction log, own-vessel log, learning entry — after the re-run on list 14.11 + programme 15.11
import re, sys, json
W='/home/claude/work/'; P=W+'dpa-berth-board.html'
s=open(P,encoding='utf-8').read(); n0=len(s)
S=json.load(open(W+'S158.json'))
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

# ================= PRED snapshot =================
fixed=[
 ['Chang Hang','sails','14 Nov 13:45','amended night sheet: OUT 13:45 — actual from DPR 15.11'],
 ['Karpathos Dawn','sails','14 Nov 14:30','programme 14.11 readiness · list 14.11: [15] sailing today'],
 ['Merchia','3','14 Nov 16:00','port-convenience shift from CJ-8 after Chang Hang · list 14.11 prints her at CJ-3 · est'],
 ["Cape Venture","7","14 Nov 16:30","list 14.11: B'TODAY (HP), across CJ-7/8 · est"],
 ["CD Cherry","15","14 Nov 17:00","list 14.11: B'TODAY (24 HRS), 147½–155 · est"],
 ['Belasitza','sails','14 Nov 17:30','programme 14.11 readiness'],
 ['Bristol','5','14 Nov 19:00','shift CJ-6 → CJ-5 after Belasitza · est'],
 ["Princess Joanna","6","14 Nov 20:30","list 14.11: B'TODAY (Govt) · est"],
 ['Bristol','sails','14 Nov 23:45','programme 15.11: readiness 23:45, night sailing'],
 ['Princess Joanna','5','15 Nov 02:00','programme 15.11: night shift CJ-6 → CJ-5 (port convenience) · est'],
 ['Truong Minh Dream','6','15 Nov 03:00','programme 15.11: GOVT, night berthing · est'],
 ['CD Cherry','sails','15 Nov 17:00','programme 15.11 readiness (24 hrs)'],
 ["Enishi","15","15 Nov 19:00","programme 15.11: shift CJ-4 → CJ-15, agent's a/c (Delta) · est"],
 ['African Hornbill','4','15 Nov 20:00','programme 15.11: 24 HRS, 27¼–36 · est'],
 ['Cape Diversity','sails','15 Nov 19:12','DPR 14.11 pace — NOT on programme 15.11 (list ETC 15 Nov 05:43)'],
 ["TPT Heart","OJ-2","14 Nov 16:00","list 14.11: B'TODAY · est"],
 ["Bow Platinum","OJ-3","14 Nov 15:00","list 14.11: B'TODAY · est"],
 ["Searay","OJ-7","14 Nov 15:00","list 14.11: B'TODAY · est"],
 ['Doukato','sails','15 Nov 03:00','programme 15.11 (TT-1) → Europa Graeca, night berthing'],
 ['TPT Heart','sails','15 Nov 04:00','programme 15.11 → Lavraki ~06:00'],
 ['Searay','OJ-1','15 Nov 10:00','programme 15.11: shift OJ-7 → OJ-1 (port convenience) · placeholder'],
 ['CS Rotterdam','OJ-7','15 Nov 12:00','programme 15.11 · est'],
 ['Bochem Ghent','sails','15 Nov 12:30','programme 15.11 readiness'],
 ['SC Larimar','sails','15 Nov 17:30','programme 15.11 → Lujain ~19:30'],
]
proj=[[x['n'],x['b'],nice(x['F']),'board projection — '+how(x)+(' · after '+x['prev'] if x['prev'] else '')] for x in S if x['F']<='11-19 12:00']
rows=fixed+proj
i=s.index("const PRED=["); j=s.index("\n];",i)
s=s[:i]+"const PRED=[ // snapshot 14 Nov 16:30 (v158) — list 14.11 + programme 15.11 applied; for the 14 Nov day / night sheets, DPR 15.11, list 15.11, programme 16.11\n "+",".join("['%s','%s','%s','%s']"%(a.replace("'","\\'"),b,c,d.replace("'","\\'")) for a,b,c,d in rows)+s[j:]

# ================= PREDLOG =================
# actuals from DPR 14.11 that were still blank
rep("{v:'Drake Well',predAt:'11-11 12:30',pb:'16',pt:'11-12 01:00',ab:'1',at:'',","{v:'Drake Well',predAt:'11-11 12:30',pb:'16',pt:'11-12 01:00',ab:'1',at:'11-13 14:00',")
rep("{v:'Leya',predAt:'11-11 12:30',pb:'7',pt:'11-13 05:00',ab:'9',at:'',","{v:'Leya',predAt:'11-11 12:30',pb:'7',pt:'11-13 05:00',ab:'9',at:'11-13 08:18',")
rep("{v:'Drake Well',predAt:'11-11 15:00',pb:'1',pt:'11-12 21:00',ab:'1',at:'',","{v:'Drake Well',predAt:'11-11 15:00',pb:'1',pt:'11-12 21:00',ab:'1',at:'11-13 14:00',")
rep("{v:'Drake Well',predAt:'11-13 09:30',pb:'1',pt:'11-13 13:00',ab:'1',at:'',src:'prog',","{v:'Drake Well',predAt:'11-13 09:30',pb:'1',pt:'11-13 13:00',ab:'1',at:'11-13 14:00',src:'prog',")
# this morning's predictions that programme 15.11 did not take
def addnote(anchor,extra):
    global s
    if s.count(anchor)!=1: die('PREDLOG anchor (%d): %s'%(s.count(anchor),anchor[:90]))
    a=s.index(anchor); b=s.index("'},",a) if s.find("'},",a)!=-1 and s.find("'},",a)<s.find("\n",a) else s.index("'}",a)
    s=s[:b]+extra+s[b:]
addnote("{v:'Sea Gautham',predAt:'11-13 23:15',pb:'5',"," · PROGRAMME 15.11: not taken — CJ-5 goes to Princess Joanna (moved from CJ-6); list 14.11 marks Sea Gautham \"DISPUTE\", the board now holds her")
addnote("{v:'Xin Hai Tong 71',predAt:'11-14 10:15',pb:'15',"," · PROGRAMME 15.11: not taken — the 24-hr slot goes to African Hornbill (24H 1, ready 14 Nov 11:00) at CJ-4 and CJ-15 to Enishi (shifted); list 14.11 prints her SGR 4, not 24H")
addnote("{v:'Rahma',predAt:'11-14 10:15',pb:'14',"," · PROGRAMME 15.11: not programmed — Theometor is not moved")
addnote("{v:'HN Doris (salt, next call)',predAt:'11-14 10:15',pb:'16',"," · PROGRAMME 15.11: not programmed — Cape Diversity has no outward row")
addnote("{v:'CD Glory',predAt:'11-14 10:15',pb:'5',"," · superseded 14 Nov 16:30: real particulars from list 14.11 (29,158 CBM, 10.5 m, ETA 15 Nov 12:00) and Pioneer Fortune ready as 8K 1")
a=s.index("const PREDLOG=["); b=s.index("\n];",a)
byn={x['n']:x for x in S}
def prow(n,note):
    x=byn[n]; return " {v:'%s',predAt:'11-14 16:00',pb:'%s',pt:'%s',ab:'',at:'',note:'%s'}"%(n.replace("'","\\'"),x['b'],x['F'],note)
new=[
 " {v:'Truong Minh Dream',predAt:'11-14 10:15',pb:null,pt:null,ab:'6',at:'',note:'not projected — N/A on the list the board had (13.11); list 14.11: ready 13 Nov 11:00, GP 1 → programme 15.11 gives her CJ-6 (Govt), night berthing'}",
 " {v:'African Hornbill',predAt:'11-14 10:15',pb:null,pt:null,ab:'4',at:'',note:'not projected — N/A on the list the board had; readiness declared 14 Nov 11:00, 24H 1 → programme 15.11 gives her CJ-4 under 24 HRS, with Enishi shifted to CJ-15 at Delta\\'s account'}",
 " {v:'Truong Minh Dream',predAt:'11-14 16:00',pb:'6',pt:'11-15 03:00',ab:'',at:'',src:'prog',note:'programme 15.11 — GOVT, night berthing; reading, not scored'}",
 " {v:'African Hornbill',predAt:'11-14 16:00',pb:'4',pt:'11-15 20:00',ab:'',at:'',src:'prog',note:'programme 15.11 — 24 HRS; reading, not scored'}",
 prow('Rome Trader (salt, next call)','list 14.11 first reading — Mihir & Co — SAAGAR bulk place (the place Enishi vacates), CJ-16 after Cape Diversity; only "Y" printed under SGR'),
 prow('Rahma',"list 14.11 + programme 15.11 re-run — Steel / project (STL 1), CJ-14 at Theometor\\'s permissible time"),
 prow('Saga Viking','list 14.11 + programme 15.11 re-run — General (GEN 2), CJ-5 after Princess Joanna'),
 prow('Xin Hai Tong 71','list 14.11 + programme 15.11 re-run — SAAGAR project against a vacant Govt slot, CJ-15 after Enishi'),
 prow('Pioneer Fortune','list 14.11 + programme 15.11 re-run — 6.5K / 8K (8K 1, ready 13 Nov), CJ-4 after African Hornbill'),
 prow('AG Varvara','list 14.11 + programme 15.11 re-run — General, CJ-1 after Drake Well'),
 prow('HN Doris (salt, next call)','list 14.11 + programme 15.11 re-run — 30k/25k quote against the vacant Coastal slot, CJ-15A after North Gate'),
 prow('Vishva Bandhan','list 14.11 + programme 15.11 re-run — Govt (bulk urea), CJ-7 after Cape Venture'),
 prow('Gokova-M','list 14.11 + programme 15.11 re-run — Higher productivity (HP 1), CJ-8 after Cape Venture'),
 prow('Uni Blossom','list 14.11 + programme 15.11 re-run — SAAGAR break-bulk place when African Peacock is through, CJ-15'),
 prow('Propel Confidence','list 14.11 first reading — 30k/25k quote against the 24-hr slot, CJ-14'),
 prow('CD Glory','list 14.11 re-run on her real particulars — Mihir & Co — SAAGAR (the place Rome Trader leaves), CJ-4 after Pioneer Fortune; ready on arrival assumed'),
]
s=s[:b]+",\n"+",\n".join(new)+s[b:]

# ================= MYLOG =================
g=byn['CD Glory']; r=byn['Rome Trader (salt, next call)']
rep("\n ],\n 'African Quail':[",
    ",\n  {d:'14 Nov 15:55 · list 14.11',exp:'11-16 22:20',b:'1',slot:'alongside CJ-1 — list ETC (permissible time)',why:'List 14.11 prints her for the first time: 6.5K / 8K · CJ-1 · 7¼–N · norm 8,000 · made fast 13 Nov 14:00, commenced 15:35 · ETC 16 Nov 22:20 (commencement + 26,111 ÷ 8,000 days). DPR 14.11 pace — about 6,800 MT/day over the first 15½ hours — points to ~17 Nov 12:00, some 14 hours past the permissible time; she is not on programme 15.11. Laytime ended 12 Nov 03:39, so demurrage runs till she completes.'}\n ],\n 'African Quail':[")
a=s.index(" 'CD Glory':[\n"); b=s.index("\n ]\n};",a)
CDG=(",\n  {d:'14 Nov 15:55 · list 14.11 — her real particulars',exp:'%s',b:'%s',slot:'SAAGAR ~21 Nov 01:30 at CJ-4 (board\\'s earliest) · General ~21 Nov 10:00 at CJ-5 · 6.5K / 8K ~26 Nov 23:00 at CJ-5',"
 "why:'List 14.11 (ETA sheet): timber logs 29,158 CBM, 179.9 m, 10.5 m, ETA 15 Nov 12:00, readiness N/A, no group marked. Why the date moved from 16 Nov: (1) at 10.5 m she fits only CJ-1, CJ-4 and CJ-5 (timber cannot work CJ-2 / 3 / 6), and the list fills all three before she is in line — CJ-5 Saga Viking (GEN 2), CJ-4 Pioneer Fortune, CJ-1 AG Varvara; (2) PIONEER FORTUNE (sugar bags) declared readiness and is 8K 1 — she takes the 6.5K / 8K berth at CJ-4 (~16 to 20 Nov) and ML Egret (8K 2) follows, so that route reaches CD Glory only ~26 Nov. Under SAAGAR she takes the place Rome Trader leaves (~18 Nov) as soon as CJ-4 is free, and works at the 3,450 norm (ETC ~29 Nov at the norm; log vessels are doing 4,500 to 7,000 a day on the DPR). Laytime at 4,000 CBM a day runs 7.3 days from NOR — to ~22 Nov 19:00 if NOR is tendered on arrival.'}\n ],\n")%(g['F'],g['b'])
RT=(" 'Rome Trader (salt, next call)':[\n  {d:'14 Nov 15:55 · list 14.11 (ETA sheet) — first reading',exp:'%s',b:'%s',slot:'SAAGAR — bulk place · if the port ranks her behind the log vessels ~18 Nov at CJ-13 · HP if declared ~19 Nov 21:30 at CJ-15 · 6.5K / 8K or General ~20 Nov 20:00 at CJ-15A',"
 "why:'Salt 55,275 MT EXP, 189.9 m, 6.6 m on arrival, ETA / readiness 14 Nov 17:00, agent Mihir, \"SGR- NEELKANTH\", SGR Y. Salt works only at CJ-13 to CJ-16. The SAAGAR group is one bulk place and one break-bulk place; log vessels (Enishi, African Peacock) hold both today only because no SAAGAR bulk vessel was waiting. She is now the only one, so the place Enishi vacates is hers ahead of Uni Blossom (SGR 1, logs). Enishi finishes ~16 Nov 17:00 on the DPR pace — inside the window of the 15 Nov meeting (15 Nov 18:00 to 16 Nov 18:00) — so that meeting can programme Rome Trader into CJ-16 as soon as Cape Diversity is out (~15 Nov 19:00 on the DPR pace; she is not on programme 15.11). Three things must hold: the port accepts her under SAAGAR bulk, Cape Diversity sails on the 15th, and Enishi stays on pace; if any slips it is the 16th evening or later. 55,275 MT at ~21,000 a day ≈ 2¾ days.'}\n ]\n};")%(r['F'],r['b'])
s=s[:b]+CDG+RT+s[b+len("\n ]\n};"):]

# ================= LEARN =================
rep("Does the port let a 24-hr vessel that has finished wait for the tide, or was an extension given?',st:'open'},",
    "Does the port let a 24-hr vessel that has finished wait for the tide, or was an extension given? — (1) ANSWERED by list 14.11: CD Glory is on the ETA sheet under agent Mihir — timber logs 29,158 CBM, 179.9 m, 10.5 m, ETA 15 Nov 12:00. (2) carried into the 15:55 entry.',st:'closed'},")
rep("const LEARN=[\n","const LEARN=[\n"
 " {d:'14 Nov 15:55 · list 14.11 + programme 15.11',v:'Programme 15.11 against the board: NONE of the three cargo-jetty berthings was projected. TRUONG MINH DREAM (Govt, CJ-6) and AFRICAN HORNBILL (24 hrs, CJ-4) declared readiness after the list the board had; ENISHI is shifted CJ-4 → CJ-15 at the cost of Hornbill\\'s agent.',"
 "exp:'Board (DPR 14.11, 10:15): CJ-15 after CD Cherry → Xin Hai Tong 71 (24 hrs); CJ-14 → Rahma, with Theometor moved; CJ-16 → HN Doris (salt) after Cape Diversity; CJ-5 after Bristol → Sea Gautham, then CD Glory; Princess Joanna to stay at CJ-6 till ~17 Nov; Enishi to finish at CJ-4.',"
 "act:'PROGRAMME 15.11 (TF/SH/2102): Bristol out 14 Nov 23:45 (night) → Princess Joanna moved CJ-6 → CJ-5, 37–45¾, port convenience → Truong Minh Dream CJ-6, 46¾–54½, GOVT, night berthing. CD Cherry out 15 Nov 17:00 → Enishi shifted CJ-4 → CJ-15, 142½–155, \"agent\\'s a/c (Delta Shg)\" → African Hornbill CJ-4, 27¼–36, 24 HRS, sailing draft 10.0. No outward row for Cape Diversity, Bomustafao O, Theometor or Merchia; Rahma, Xin Hai Tong 71, HN Doris, Gokova-M, Pioneer Fortune and Uni Blossom are not berthed. LIST 14.11: Truong Minh Dream ready 13 Nov 11:00, GP 1; African Hornbill ready 14 Nov 11:00, 24H 1 · SGR 2 · STL 3 — both were N/A on the 13.11 list, both reported 9 Nov. Pioneer Fortune ready, 8K 1. Sea Gautham \"DISPUTE (waiting for shipper\\'s confirmation)\". Xin Hai Tong 71: SGR 4 · STL 4, no 24H. ML Egret: SGR \"Y\", 8K 2. CD Glory: 29,158 CBM, 179.9 m, 10.5 m, ETA 15 Nov 12:00, N/A. Rome Trader: salt 55,275 MT, agent Mihir, SGR Y.',"
 "why:'(1) A senior vessel that is N/A on the morning list can declare readiness before the 11:00 meeting and take her group\\'s slot the same day; the board works from the printed readiness and cannot see that coming. (2) The port makes the particular berth a 24-hr vessel needs by shifting the working vessel at the incoming agent\\'s cost (Enishi for Hornbill), and re-seats a Govt vessel hours after berthing so that the deeper one gets CJ-6. (3) 25,000 MT loads to 10.0 m — CJ-4 suits a 25K loader; the board\\'s loaded-draught step (11.2 m from 25,000 MT) was too strict.',"
 "fix:'v158: programme 15.11 entered; ranks, readiness and remarks of every waiting vessel refreshed from list 14.11; CD Glory on her real particulars; Rome Trader (salt) added as a Mihir & Co vessel with options — as the only SAAGAR bulk vessel she is given the SAAGAR place Enishi vacates, ahead of the next log vessel (regulation: 1 bulk + 1 break bulk; the board had been counting the finishing vessel when deciding which place was free); loaded-draught step moved to 30,000 MT, so Pioneer Fortune (8K 1) can use CJ-1 to CJ-4 — she, not CD Glory, is next for the 6.5K / 8K berth; horizon extended to 22 Nov; Sea Gautham held while the DISPUTE remark stands; tanker ETC on the list = made fast + quantity ÷ hourly norm + 4 h (fits all four printed ETCs). The \"if ready today\" date on each N/A vessel\\'s card is the guard against point (1). OPEN (1): Rome Trader — only \"SGR Y\" is printed. Does the port give a SAAGAR BULK vessel the place ahead of the log vessels in the SGR queue (board: yes — CJ-16 from the night of the 15th), or does she stand behind Uni Blossom and AG Varvara (then ~18 Nov, CJ-13)? And is SAAGAR the only route to be declared? OPEN (2): CD Glory — readiness N/A and no group marked. Which groups will be declared, and will she be ready on arrival (15 Nov 12:00)? The board assumes ready on arrival, SGR + 6.5K. OPEN (3): Xin Hai Tong 71 — her \"4\" stood under 24H on the 13.11 sheet and stands under SGR today; taken as printed. Right? OPEN (4), carried: Karpathos Dawn stayed about 31 hours under the 24-hr priority — tide wait, or an extension?',st:'open'},\n")

open(P,'w',encoding='utf-8').write(s); print('ok',n0,'->',len(s))
