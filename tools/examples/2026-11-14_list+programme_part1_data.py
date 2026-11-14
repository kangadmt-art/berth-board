#!/usr/bin/env python3
# apply14c — v158 (part 1): Daily Berthing List 14.11 (0700) + Programme for 15.11 (TF/SH/2102, dated 14 Nov), received 14 Nov 15:55.
import re, shutil, sys
W='/home/claude/work/'; P=W+'dpa-berth-board.html'
shutil.copy(P, W+'bak_v157.html')
s=open(P,encoding='utf-8').read(); n0=len(s)
def die(m): print(m); sys.exit(1)
def rep(old,new,cnt=1):
    global s
    k=s.count(old)
    if k!=cnt: die('ANCHOR FAIL (%d found, want %d): %r'%(k,cnt,old[:150]))
    s=s.replace(old,new)
def entry_span(marker):
    a=s.index(marker); b=s.index("},\n",a)+1; return a,b
def sub_entry(marker,old,new):
    global s
    if s.count(marker)!=1: die('MARKER not unique (%d): %s'%(s.count(marker),marker))
    a,b=entry_span(marker); ent=s[a:b]
    if ent.count(old)!=1: die('ENTRY FAIL %s: %d × %r'%(marker,ent.count(old),old))
    s=s[:a]+ent.replace(old,new)+s[b:]
def note_prefix(marker,text):
    global s
    if s.count(marker)!=1: die('MARKER not unique (%d): %s'%(s.count(marker),marker))
    a,b=entry_span(marker); ent=s[a:b]; i=ent.index("note:'")+6; s=s[:a]+ent[:i]+text+ent[i:]+s[b:]
def add_after(marker,text):
    global s
    if s.count(marker)!=1: die('MARKER not unique (%d): %s'%(s.count(marker),marker))
    a,b=entry_span(marker); s=s[:b+2]+text+s[b+2:]
def line_of(prefix):
    if s.count(prefix)!=1: die('LINE prefix not unique (%d): %s'%(s.count(prefix),prefix))
    a=s.index(prefix); b=s.index("\n",a); return a,b
def set_line(prefix,new):
    global s
    a,b=line_of(prefix); s=s[:a]+new+s[b:]
def q(t): return t.replace("\\","\\\\").replace("'","\\'")

L="LIST 14.11"; PG="PROGRAMME 15.11 (TF/SH/2102)"

# ================= HEADER =================
rep("const NOW=h('11-14 10:15');","const NOW=h('11-14 16:00');")
rep("const UPDATED='14 Nov 2026 · 10:30 IST';","const UPDATED='14 Nov 2026 · 16:30 IST';")
rep("const PROG_END=h('11-14 18:00');","const PROG_END=h('11-15 18:00');")
rep("List <b>13.11 · 0700</b> · DPR <b>14.11</b> · Programme <b>14.11</b> · Signals to","List <b>14.11 · 0700</b> · DPR <b>14.11</b> · Programme <b>15.11</b> · Signals to")
rep("Berthing List 13.11.26 (0700) and Programme 14.11 (TF/SH/2102, meeting 13 Nov), both received 13 Nov 15:13 ·",
    "Berthing List 14.11.26 (0700) and Programme 15.11 (TF/SH/2102, dated 14 Nov), both received 14 Nov 15:55 · Berthing List 13.11.26 (0700) and Programme 14.11 (TF/SH/2102, meeting 13 Nov), both received 13 Nov 15:13 ·")
rep("const BOARD_SRC='list 13.11 (0700) · programme 14.11 (TF/SH/2102, meeting 13.11) ·","const BOARD_SRC='list 14.11 (0700) · programme 15.11 (TF/SH/2102, dated 14.11) ·")
rep("'Belasitza','Chang Hang','Karpathos Dawn','Torero','DM Bea']);","'Belasitza','Chang Hang','Karpathos Dawn','Torero','DM Bea','Bristol','CD Cherry','Princess Joanna']);")

# ================= V — berths =================
# CJ-1 Drake Well: list ETC
sub_entry("{b:'1',n:'Drake Well'","f:'11-13 14:00',t:'11-16 20:20',est:1,","f:'11-13 14:00',t:'11-16 22:20',")
note_prefix("{b:'1',n:'Drake Well'", L+": 6.5K / 8K · CJ-1 · 7¼–N · norm 8,000 · made fast 13 Nov 14:00, commenced 15:35 · ETC 16 Nov 22:20 — the permissible time (commencement + 26,111 ÷ 8,000 days); not on programme 15.11. ")
# CJ-3 Merchia: list norm 21,160 → ETC 16 Nov 08:45
sub_entry("{b:'3',n:'Merchia'","nm:30000,p:[19,27.75]","nm:21160,p:[19,27.75]")
sub_entry("{b:'3',n:'Merchia'","f:'11-14 16:00',t:'11-15 18:00'","f:'11-14 16:00',t:'11-16 08:45'")
note_prefix("{b:'3',n:'Merchia'", L+": COASTAL · CJ-3 · 19–27¾ · \"S1 FROM CJ-08\" · norm now 21,160 (was 30,000 at CJ-8) → ETC 16 Nov 08:45; not programmed out on 15.11. ")
# CJ-7/8 Cape Venture: balance at berthing 121,377 MT
for b in ("7","8"):
    sub_entry("{b:'%s',n:'Cape Venture'"%b,"q:115000","q:121377")
    sub_entry("{b:'%s',n:'Cape Venture'"%b,"t:'11-17 09:00'","t:'11-17 14:30'")
note_prefix("{b:'7',n:'Cape Venture'", L+": HP · CJ-7 · 55¾–67½ · B\\'TODAY · 121,377 MT to discharge alongside (total 165,051; 43,674 lightered) at the 42,500 norm ≈ 68½ h → ~17 Nov 14:30 est; berthing time still to come from the day sheet / DPR 15.11. ")
# CJ-9 Leya: list ETC
sub_entry("{b:'9',n:'Leya'","t:'11-17 07:00'","t:'11-17 21:06'")
note_prefix("{b:'9',n:'Leya'", L+": GFPL · CJ-9 · norm 20,000 → ETC 17 Nov 21:06. ")
# CJ-15 CD Cherry: list panels, programme 15.11 readiness
sub_entry("{b:'15',n:'CD Cherry'","p:[142.5,155]","p:[147.5,155]")
sub_entry("{b:'15',n:'CD Cherry'","f:'11-14 16:30',t:'11-15 16:30'","f:'11-14 17:00',t:'11-15 17:00'")
note_prefix("{b:'15',n:'CD Cherry'", PG+": outward readiness 15 Nov 17:00 (9.5 m) → ENISHI shifts in behind her. "+L+": 24 HRS · CJ-15 · 147½–155 (the 110 m vessel needs only 7½ panels; the programme had printed 142½–155) · B\\'TODAY — berthing ~17:00 est, 24 hours to the programmed readiness. ")
# CJ-4 Enishi → CJ-15 (agent's a/c, Delta) ; African Hornbill 24 HRS at CJ-4
sub_entry("{b:'4',n:'Enshi',nm:3450,p:[28.75,36.75]","f:'11-14 10:30',t:'11-19 09:34',note:'","f:'11-14 10:30',t:'11-15 18:00',est:1,note:'"+PG+": \"SHIFTING FROM CJ-04 TO CJ-15. AGENT\\'S A/C (DELTA SHG)\" — she leaves CJ-4 once CD Cherry is out of CJ-15 (readiness 17:00) → ~18:00 est, so that AFRICAN HORNBILL (24 HRS, agent Delta) can take 27¼–36. "+L+": SAAGAR · CJ-4 · 28¾–36¾ · \"S1 22¼–30¼\" · ETC 19 Nov 09:34. ")
add_after("{b:'4',n:'Enshi',nm:3450,p:[28.75,36.75]",
 " {b:'15',n:'Enshi',nm:3450,p:[142.5,155],c:'JAS pine logs',q:33134,u:'MT',cat:'SAAGAR',f:'11-15 19:00',t:'11-19 09:34',est:1,note:'"+PG+": CJ-15, 142½–155, \"SHIFTING FROM CJ-04 TO CJ-15. AGENT\\'S A/C (DELTA SHG)\" — the same vessel continuing after CD Cherry (readiness 15 Nov 17:00); re-made fast ~19:00 est. Her permissible time stays 19 Nov 09:34 (list ETC, norm 3,450); DPR 14.11: 11,072 MT left at 4,578/day → ~16 Nov 17:00, so she finishes about a day after the shift. The shift is paid by Delta Shipping, the agent of African Hornbill, who needs CJ-4.'},\n"
 " {b:'4',n:'African Hornbill',nm:25000,p:[27.25,36],c:'Ball clay bulk',q:25000,u:'MT',cat:'24H',f:'11-15 20:00',t:'11-16 20:00',est:1,note:'"+PG+": CJ-04, 27¼–36, 24 HRS, sailing draft 10.0 m — after Enishi is shifted to CJ-15 at Delta\\'s account (~18:00) → ~20:00 est; must sail within 24 hours. "+L+": ball clay 25,000 MT EXP, readiness 14 Nov 11:00 (declared for today\\'s meeting; N/A until now), reported 9 Nov 17:18 · SGR 2 · 24H 1 · STL 3 · GEN 16 · remark \"25K/10K DD- 10.5\" · 199.98 m · agent Delta. The 24-hr slot goes to her as 24H 1; she loads to 10.0 m, inside the 10.5 m of CJ-1 to CJ-5. Her 27¼–36 touches Merchia\\'s 19–27¾ by half a panel and Merchia is not programmed out — the port will set the panels at berthing.'},\n")
# CJ-6 / CJ-5: Bristol out 23:45 → Princess Joanna shifts CJ-6 → CJ-5 → Truong Minh Dream CJ-6 (Govt)
sub_entry("{b:'5',n:'Bristol'","cat:'GEN',f:'11-14 19:00',t:'11-15 02:49'","cat:'GOV',f:'11-14 19:00',t:'11-14 23:45'")
note_prefix("{b:'5',n:'Bristol'", PG+": outward readiness 14 Nov 23:45 (7.5 m), NIGHT SAILING — three hours before the list ETC (15 Nov 02:49). "+L+": GOV · CJ-5 · 37¾–46 · \"W1, S1 40½–49¼\" (pre-printed at CJ-5; the shift follows Belasitza\\'s 17:30 sailing). DPR 14.11: 4,311 MT left at 0700 — she finishes about 15:00, is shifted to free CJ-6 and sails on the night tide. ")
sub_entry("{b:'6',n:'Princess Joanna'","nm:8000,p:[47,54.5]","nm:17193,p:[47,54.5]")
sub_entry("{b:'6',n:'Princess Joanna'","f:'11-14 20:30',t:'11-17 20:00'","f:'11-14 20:30',t:'11-15 01:00'")
note_prefix("{b:'6',n:'Princess Joanna'", PG+": \"NIGHT SHIFTING FROM CJ-06 TO CJ-05. PORT C.\" — she berths at CJ-6 this evening and is moved to CJ-5 (37–45¾) in the night, after Bristol sails (readiness 23:45) → ~01:00 est, so that TRUONG MINH DREAM (12.8 m) gets CJ-6. "+L+": GOV · CJ-6 · 47–54½ · B\\'TODAY · norm 17,193 printed (the same figure as Bristol\\'s row; the 8,000 assumed before is dropped). ")
add_after("{b:'6',n:'Princess Joanna'",
 " {b:'5',n:'Princess Joanna',nm:17193,p:[37,45.75],c:'MOP (muriate of potash)',q:25000,u:'MT',cat:'GOV',f:'11-15 02:00',t:'11-16 09:30',est:1,note:'"+PG+": CJ-05, 37–45¾, \"NIGHT SAILING [Bristol]. NIGHT SHIFTING FROM CJ-06 TO CJ-05. PORT C.\" — the same vessel continuing; re-made fast ~02:00 est. 25,000 MT at the printed norm of 17,193 ≈ 35 h of work from her commencement at CJ-6 (~22:30 est) → ~16 Nov 09:30 est; the list will print her ETC once she has commenced.'},\n"
 " {b:'6',n:'Truong Minh Dream',nm:17193,p:[46.75,54.5],c:'DAP + TSP bulk',q:55600,u:'MT',cat:'GOV',f:'11-15 03:00',t:'11-18 09:00',est:1,note:'"+PG+": CJ-06, 46¾–54½, GOVT, NIGHT BERTHING — after Princess Joanna is moved to CJ-5 (~01:00) → ~03:00 est. "+L+": DAP 39,100 + TSP 16,500 = 55,600 MT IMP, 199.99 m, 12.8 m, reported 9 Nov 16:54, readiness 13 Nov 11:00 (N/A on the 13.11 list) · GP 1 · GEN 15 · agent Taurus. Norm not printed for her yet — 17,193 (Bristol, the same cargo at the same berth) assumed → ≈ 78 h → ~18 Nov 09:00 est.'},\n")
rep("const LOA={","const LOA={'African Hornbill':199.98,'Truong Minh Dream':199.99,")
rep("const ieOf=n=>IE[n]||'';",
    "Object.assign(AG,{'African Hornbill':'Delta','Truong Minh Dream':'Taurus','Rome Trader (salt, next call)':'Mihir & Company','CD Glory':'Mihir & Company','Propel Confidence':'Genesis','Stalo':'Dariya Shg','Meghna Prestige':'Dariya Shg','Dariya Priya':'DBC','African Tiger':'Synergy','Sea Postman':'DBC','True Mariner':'JM Baxi','Josco Taicang':'JM Baxi'}); // list 14.11\n"
    "Object.assign(IE,{'African Hornbill':'EXP','Truong Minh Dream':'IMP','Rome Trader (salt, next call)':'EXP','CD Glory':'IMP','Propel Confidence':'IMP','Stalo':'IMP','Meghna Prestige':'IMP','Dariya Priya':'IMP','African Tiger':'IMP','Sea Postman':'IMP','True Mariner':'EXP','Josco Taicang':'IMP'});\n"
    "const ieOf=n=>IE[n]||'';")

# ================= WRAW =================
ROW=lambda name: re.compile(r" \['"+re.escape(name)+r"','((?:[^'\\]|\\.)*)',([^,]*),'([^']*)',([^,]*),([^,]*),(null|'[^']*'),\{([^}]*)\},'")
def wrow(name, add, rk=None, rdy=None, cargo=None, qty=None, dr=None, loa=None):
    global s
    m=ROW(name).search(s)
    if not m or len(ROW(name).findall(s))!=1: die('WRAW row not found / not unique: '+name)
    c,qq,u,lo,d,r,k=m.groups()
    new=" ['%s','%s',%s,'%s',%s,%s,%s,{%s},'%s"%(name, cargo if cargo is not None else c, qty if qty is not None else qq, u, loa if loa is not None else lo,
        dr if dr is not None else d, ("'%s'"%rdy if rdy else 'null') if rdy is not None else r, rk if rk is not None else k, L+": "+add+" · ")
    s=s[:m.start()]+new+s[m.end():]
def wdel(name):
    global s
    m=ROW(name).search(s)
    if not m: die('WRAW del: '+name)
    b=s.index("],\n",m.start())+3; s=s[:m.start()]+s[b:]

wrow('Deniz ID',"GEN 1 · ready since 21 Oct")
wrow('Saga Viking',"GEN 2")
wrow('Safi Alfa',"GEN 3 · the 8K 1 is no longer printed (Pioneer Fortune is 8K 1 now) · working at MS", rk="GEN:3")
wrow('Fortunelit',"GEN 4 · quantity now 30,500 MT (was 27,500) · working at MS", qty="30500")
wrow('Crystal O',"GEN 5 · working at MS")
wrow('Yara J',"GEN 6 · working at MS")
wrow('Mak 1',"GEN 7 · working at MS")
wrow('Libra',"GEN 8 (was 9) · docs NR (3,000 MT pending) · working at MS", rk="GEN:8")
wrow('Rahma',"STL 1 · GEN 9", rk="STL:1,GEN:9")
wrow('Pioneer Fortune',"READINESS DECLARED 13 Nov 11:00 (was N/A) · 8K 1 · GEN 10 · Sr No 7 · sugar bags 25,080 MT EXP — first in the 6.5K / 8K queue, behind Drake Well\\'s berth", rk="'8K':1,GEN:10", rdy="11-13 11:00", qty="25080")
wrow('ML Egret',"SGR \"Y\" only (was SGR 1 on the 13.11 sheet) · 8K 2 (back) · GEN 11 · 12.11 m", rk="SAAGAR:98,'8K':2,GEN:11")
wrow('Heng Yuan Fa Zhan',"STL 2 · GEN 12", rk="STL:2,GEN:12")
wrow('Uni Blossom',"SGR 1 · 8K 3 · GEN 13 · Sr No 7", rk="SAAGAR:1,'8K':3,GEN:13")
wrow('Ariston Bulker',"GEN 14 · working at MS", rk="GEN:14")
wdel('Truong Minh Dream'); wdel('African Hornbill')
wrow('Honor Star',"24H 2 · 8K 4 · GEN 17 · reported / ready 11 Nov 10:30 · 14.14 m · Sr No 7 · the wrong berth remark is still printed", rk="'24H':2,'8K':4,GEN:17", rdy="11-11 10:30", dr="14.14")
wrow('Tan Bin 259',"WORKING AT MRG 3 · readiness 14 Nov 11:00 · 12,000 MT")
wrow('Gokova-M',"HP 1 · 24H 3 · 8K 5 · GEN 18 · reported / ready 11 Nov 23:40 · 30K/25K · LP Karachi", rk="HP:1,'24H':3,'8K':5,GEN:18", rdy="11-11 23:40")
wrow('Tug Chandra Sun + barge Victoria 251',"reported 12 Nov 01:30 · \"RDY\" · CSTL Y · steel pipe 4,114 MT (1,600 pipes) · barge, taken on free quay space — not projected", qty="4114")
wrow('Glimlit',"arrived 12 Nov 06:35 · N/A · DOC NR")
wrow('AG Varvara',"SGR 3 · GEN 19 · reported / ready 12 Nov 07:06 · Sr No 7", rk="SAAGAR:3,GEN:19", rdy="11-12 07:06")
wrow('Sea Gautham',"readiness 12 Nov 13:50 · CSTL 1 · GEN 21 still printed, but remark \"DISPUTE (WAITING FOR SHIPPER\\'S CONFIRMATION)\" — the board HOLDS her out of the projection until the remark goes", rk="COASTAL:1,GEN:21", rdy="")
wrow('Xin Hai Tong 71',"SGR 4 · STL 4 · GEN 22 — the \"4\" of the 13.11 sheet stood under 24H, today it stands under SGR (project cargo); taken as printed, so she is out of the 24-hr queue · remark 13 TO 16", rk="SAAGAR:4,STL:4,GEN:22")
wrow('Queen Coral',"working at MRG 2 (2 holds) · STL 5 · GEN 23", rk="STL:5,GEN:23")
wrow('Vishva Bandhan',"GEN 24 only (no Govt rank printed — bulk urea, so Govt by the cargo rule) · 10.95 m · 2 SHORE CRANE REQ", rk="GEN:24", dr="10.95")
wrow('Tug Sagar 5 + barge Victoria 250',"reported 13 Nov 04:10 · N/A · CSTL Y · STL Y")
wrow('Alberta (re-berthing)',"GEN 25 · \"WAITING FOR LOADING OF BALANCED CARGO (3517MT)\" · ready 13 Nov 07:18", rk="GEN:25")
wrow('Porto Fiscardo',"reported 13 Nov 15:05 · N/A · DOC NR")
wrow('Evangelia D',"REPORTED / READY 13 Nov 14:48 · HP 2 · 8K 6 · GEN 26 · remark DOC NR", rk="HP:2,'8K':6,GEN:26", rdy="11-13 14:48")
wrow('Captainannis L',"reported 13 Nov 16:54 · N/A · 8K Y · DOC NR", rk="'8K':98")
wrow('HN Doris (salt, next call)',"REPORTED / READY 14 Nov 03:54 · HP 3 · 8K 7 · GEN 26 (printed twice — taken as 27 behind Evangelia D) · 30K/25K/10K Sr No 7 · 229 m", rk="HP:3,'8K':7,GEN:27", rdy="11-14 03:54", loa="229")
wrow('New Bliss',"N/A · 8K Y · REQ CJ-01 TO 04, part doc pending", rk="'8K':98")
wrow('Crystal Land',"N/A · 8K Y · DOC NR", rk="'8K':98")
wrow('African Loon',"N/A · \"STS operation, transhipment — waiting for daughter vessel\"")
wrow('Coastal Amigo',"at the Bunder area (BA), B\\'TODAY · CSTL Y · steel slab 2,036 MT")
wrow('Nord Copper',"ETA 14 Nov 15:00 · N/A")
wrow('Tai Keystone',"ETA / readiness moved to 15 Nov 00:00 · no group rank printed (bulk urea — Govt by the cargo rule)", rdy="11-15 00:00")
wrow('Phoenix Coral',"ETA / readiness 15 Nov 06:00 · 24H Y · \"SPACE A/C\" · quantity printed 1,159 MT (the same figure as Queen Coral — likely a copy slip)", rk="'24H':98", rdy="11-15 06:00")
wrow('Seacon Monaco',"ETA / readiness 15 Nov 08:00 · 8K Y · 10K · 10.71 m", rk="'8K':98", rdy="11-15 08:00", dr="10.71")
wrow('Marsal',"ETA 15 Nov 14:00 · N/A")
wrow('Lolo Gate',"ETA 16 Nov · N/A")
wrow('Bristol (salt, next call)',"ETA / readiness 16 Nov 00:00 · HP Y · 8K Y · \"DD 13.60 M\" · 30K/25K/10K Sr No 7 · agent Trueblue", rdy="11-16 00:00")
wrow('Outlander',"ETA 17 Nov · N/A")
wrow('Ken Ann',"ETA / readiness 17 Nov 00:00 · 24H Y · 7.1 m", rk="'24H':98", rdy="11-17 00:00", dr="7.1")
wrow('Hai Long 1',"ETA 17 Nov · N/A")
wrow('Valentina Sea',"ETA 17 Nov · N/A")
wrow('KSS Edmond',"ETA 19 Nov · N/A")

# CD Glory — real particulars from the ETA sheet; Rome Trader (salt) — second Mihir & Co vessel; other new arrivals
m=ROW('CD Glory').search(s)
if not m: die('CD Glory row')
b=s.index("]\n];",m.start())
NEW=[
 " ['Propel Confidence','Iron ore pellets',54918,'MT',189.99,12.68,'11-14 23:00',{HP:98},'"+L+" (ETA sheet): NEW · ETA / readiness 14 Nov 23:00 · HP Y · 30K/25K/10K Sr No 7 · 54,918 MT IMP · agent Genesis'],",
 " ['Stalo','Coal in bulk',43400,'MT',228.9,11.3,'11-15 09:00',{HP:98,'8K':98},'"+L+" (ETA sheet): NEW · ETA / readiness 15 Nov 09:00 · HP Y · 8K Y · 30K/25K/10K · 43,400 MT IMP · agent Dariya'],",
 " ['Meghna Prestige','Coal in bulk',60500,'MT',199.9,12.65,'11-15 13:00',{HP:98,'8K':98},'"+L+" (ETA sheet): NEW · ETA / readiness 15 Nov 13:00 · HP Y · 8K Y · 30K/25K/10K Sr No 7 · 60,500 MT IMP · agent Dariya'],",
 " ['Dariya Priya','Pine logs',44968,'CBM',199.9,11,'11-16 08:00',{SAAGAR:98,'8K':98},'"+L+" (ETA sheet): NEW · ETA / readiness 16 Nov 08:00 · SGR Y · 8K Y · Sr No 7 · 44,968 CBM pine logs IMP, 11.0 m · agent DBC (timber desk: \"Darya Priya\", ETA 16 Nov 19:30)'],",
 " ['African Tiger','Pine logs',36328,'MT',179.97,null,null,{SAAGAR:98,'8K':98},'"+L+" (ETA sheet): NEW · ETA 18 Nov · N/A · SGR Y · 8K Y · Sr No 7 · agent Synergy'],",
 " ['Sea Postman','Rock phosphate bulk',28500,'MT',189.95,7.5,null,{},'"+L+" (ETA sheet): NEW · ETA 17 Nov · N/A · 28,500 MT IMP · agent DBC'],",
 " ['True Mariner','Rice bags',25000,'MT',179.97,5.4,null,{},'"+L+" (ETA sheet): NEW · ETA 18 Nov 10:00 · N/A · agent JM Baxi'],",
 " ['Josco Taicang','Project / steel cargo',15424,'MT',197,11.4,null,{},'"+L+" (ETA sheet): NEW · ETA 20 Nov · N/A · project cargo 389 pkgs + CR steel coils · agent JM Baxi'],",
 " ['Rome Trader (salt, next call)','Salt in bulk',55275,'MT',189.9,6.6,'11-14 17:00',{SAAGAR:5},'MIHIR & COMPANY · "+L+" (ETA sheet): ETA / readiness 14 Nov 17:00 · SGR Y · remark \"SGR- NEELKANTH\" · 55,275 MT salt EXP, 189.9 m, arrival draught 6.6 m — the Rome Trader that discharged petcoke at CJ-6 on 1 to 5 Nov, back to load. The sheet prints only the SGR flag; the board ranks her SGR 5 for now (behind Uni Blossom 1, African Hornbill 2, AG Varvara 3, Xin Hai Tong 71 4) until the list prints her number. Options by other priorities are on the Mihir & Co card.'],",
 " ['CD Glory','Hardwood logs',29158,'CBM',179.9,10.5,'11-15 12:00',{SAAGAR:6,'8K':8},'MIHIR & COMPANY · "+L+" (ETA sheet): \"IMP TIMBER LOG 29,158.216 CBM\", 179.9 m, 10.5 m, ETA 15 Nov 12:00, readiness N/A, no group flag printed yet · timber desk: hardwood logs ex Malaysia. The board takes her as ready on arrival and ranks her SGR 6 / 8K 8 for now (the next free numbers) so that the options on the Mihir & Co card can be run; the list will print the real ranks once readiness is declared. 10.5 m is the limit of CJ-1 to CJ-5.']"
]
s=s[:m.start()]+"\n".join(NEW)+s[b+1:]
rep(" // waiting list 11.11 (0700) in the list's own order;"," // ranks, readiness and remarks refreshed from the waiting + ETA sheets of list 14.11 (0700) — each row's note starts with what that list prints\n // waiting list 11.11 (0700) in the list's own order;")
# reporting times that the 14.11 sheet now gives
for old,new in (("'Tai Keystone':'11-13 00:00'","'Tai Keystone':'11-15 00:00'"),("'Evangelia D':'11-13 00:00'","'Evangelia D':'11-13 14:48'"),("'HN Doris (salt, next call)':'11-13 00:00'","'HN Doris (salt, next call)':'11-14 03:54'"),("'Gokova-M':'11-09 00:00'","'Gokova-M':'11-11 23:40'"),("'Bristol (salt, next call)':'11-14 00:00'","'Bristol (salt, next call)':'11-16 00:00'")):
    if s.count(old)<1: die('REP '+old)
    s=s.replace(old,new)

# ================= OPTIONS (own vessels) =================
a=s.index("const OPTS={'CD Glory':{fixed:[],"); b=s.index("const OPTRES=",a)
s=s[:a]+("const OPTS={'CD Glory':{fixed:[],\n"
 " routes:[{label:'SAAGAR',only:'SAAGAR',rk:{SAAGAR:6},note:'Break-bulk place of the SAAGAR group. Ahead of her on list 14.11: Uni Blossom (SGR 1), AG Varvara (3), Xin Hai Tong 71 (4), and Rome Trader if she is ranked — African Hornbill (2) berths under 24 HRS tomorrow.'},\n"
 "  {label:'6.5K / 8K',only:'8K',rk:{'8K':8},note:'One 6.5K / 8K berth at a time, by seniority. Ahead of her on list 14.11: Pioneer Fortune (8K 1), ML Egret (2), Uni Blossom (3), Honor Star (4), Gokova-M (5), Evangelia D (6), HN Doris (7) — those who berth through another group drop out of this queue.'},\n"
 "  {label:'General · by seniority',only:'GEN',rk:{},note:'Every vessel also stands in the General queue. Bag vessels are capped at three working at a time, so a clean berth can reach a junior logs vessel under General.'}]},\n"
 " 'Rome Trader (salt, next call)':{fixed:[],\n"
 " routes:[{label:'SAAGAR · as declared',only:'SAAGAR',rk:{SAAGAR:5},note:'The route printed on the list (\"SGR- NEELKANTH\"). Two SAAGAR berths, both held by log vessels now (Enishi, African Peacock); ahead of her: Uni Blossom (SGR 1), AG Varvara (3), Xin Hai Tong 71 (4).'},\n"
 "  {label:'HP · 40K quote (if declared)',only:'HP',rk:{HP:4},note:'Not declared on the list — shown for comparison. HP queue on list 14.11: Gokova-M (1), Evangelia D (2), HN Doris (3); she would rank next by her arrival.'},\n"
 "  {label:'6.5K / 8K (if declared)',only:'8K',rk:{'8K':8},note:'Not declared on the list — shown for comparison. Seven vessels are ranked ahead (Pioneer Fortune 1 … HN Doris 7).'},\n"
 "  {label:'General · by seniority',only:'GEN',rk:{},note:'The General queue by reporting time — she reports today, so she is the junior-most ready vessel.'}]}};\n")+s[b:]

# ================= TIMBER desk table =================
rep("{n:'CD Glory',cbm:null,from:'Malaysia',c:'Hardwood logs',eta:'11-15 11:00',etb:'11-28',st:'eta',note:'",
    "{n:'CD Glory',cbm:29158,from:'Malaysia',c:'Hardwood logs',eta:'11-15 12:00',etb:'11-28',st:'eta',note:'DPA list 14.11 (ETA sheet): timber logs 29,158.216 CBM, 179.9 m, 10.5 m, ETA 15 Nov 12:00, readiness N/A, agent Mihir · ")
rep("{n:'Darya Priya',cbm:null,from:'New Zealand',c:'Pine logs',eta:'11-16 19:30',etb:'12-03',st:'eta',note:'",
    "{n:'Dariya Priya',cbm:44968,from:'New Zealand',c:'Pine logs',eta:'11-16 08:00',etb:'12-03',st:'eta',note:'\"Darya Priya\" on the team sheet (ETA 16 Nov 19:30) · DPA list 14.11: ETA / readiness 16 Nov 08:00, 44,968 CBM, SGR Y · 8K Y, 11.0 m, agent DBC · ")
add_after("{n:'Dariya Priya',cbm:44968",
 " {n:'African Tiger',cbm:36328,from:'—',c:'Pine logs',eta:'11-18 00:00',etb:'',st:'eta',note:'not on the team report — DPA ETA sheet 14.11: pine logs 36,328 (printed MT), ETA 18 Nov, N/A, SGR Y · 8K Y, Sr No 7, 179.97 m · agent Synergy'},\n")

# ================= LIQUID =================
a0=s.index("const LIQ={")
rep("const LIQ={src:'DPA berthing list 11.11.26 (revised) · DPR 12.11 · HM signals to the 13 Nov night sheet — amendment (dated 14/11, disp 2000 / 2055)',asOf:'11-14 10:15',",
    "const LIQ={src:'DPA berthing list 14.11.26 (0700) · programme 15.11 (TF/SH/2102) · DPR 14.11 · HM signals to the 13 Nov night sheet — 2nd amendment',asOf:'11-14 16:00',")
set_line("  {b:'OJ-1',", "  {b:'OJ-1',prev:{n:'Seychelles Pioneer',c:'CPO',q:35000,u:'MT',ie:'IMP',ag:'GAC Shg',out:'11-11 07:10',outBy:'DPR 11.11: COMPLETED 03:24, LET GO 07:10 (day sheet RT OUT 07:00, Capt Rawat) — 35,000 MT in all'},now:null,next:{n:'Searay',c:'CPO',q:29999.06,u:'MT',ie:'IMP',loa:178.69,f:'11-15 10:00',est:1,rank:'',ag:'JM Baxi',note:'"+PG+": \"SHIFTING FROM OJ-07 TO OJ-01. PORT C.\" — a port-convenience shift so that CS Rotterdam (12.0 m) can take OJ-7; no time printed, ~10:00 on the 15th is the board\\'s placeholder'}},")
set_line("  {b:'OJ-2',", "  {b:'OJ-2',prev:{n:'Torero',c:'Mono ethylene glycol',q:8100,u:'MT',ie:'EXP',ag:'JM Baxi',out:'11-14 14:00',outBy:'programme 14.11: outward readiness 14 Nov 14:00 (8.2 m) · DPR 14.11: completed 07:18 · list 14.11: [2] — sailing today'},now:{n:'TPT Heart',c:'Chemicals',q:6302,u:'MT',ie:'EXP',loa:121.8,f:'11-14 16:00',est:1,nm:'250',rank:'',ag:'Ocean Harmony',note:'"+L+": OJ-2 · B\\'TODAY · chemicals 6,302 MT EXP, norm 250 MT/h — she takes OJ-2 behind Torero (the OJ-3 berthing signalled last night was cancelled); ~16:00 est; waiting since 9 Nov, ready 13 Nov 11:00'},out:'11-15 04:00',outBy:'"+PG+": outward readiness 15 Nov 04:00 (8.6 m), NIGHT SAILING → Lavraki, NIGHT BERTHING',next:{n:'Lavraki',c:'Chemicals',q:1999.61,u:'MT',ie:'IMP',loa:145.53,f:'11-15 06:00',est:1,rank:'',ag:'Atlantic Shg',note:'"+PG+": OJ-02 after TPT Heart (readiness 04:00), NIGHT BERTHING → ~06:00 est · list 14.11: chemicals 1,999.612 MT IMP, arrived / ready 14 Nov 07:06, REQ OJ 2, 3, 4'}},")
set_line("  {b:'OJ-3',", "  {b:'OJ-3',prev:{n:'DM Bea',c:'Chemicals',q:3328.87,u:'MT',ie:'IMP',ag:'Wilhelmsen',out:'11-14 13:00',outBy:'list 14.11: [3] — sailing today. Her 06:00 RT OUT was cancelled on the night sheet (\"idle\") and no new time has reached the board — ~13:00 est (programme 14.11 readiness 13:15)'},now:{n:'Bow Platinum',c:'Chemicals',q:15997.81,u:'MT',ie:'IMP',loa:165.12,f:'11-14 15:00',est:1,nm:'475',rank:'',ag:'GAC Shg',note:'"+L+": OJ-3 · B\\'TODAY · chemicals 15,997.807 MT IMP, norm 475 MT/h, arrived / ready 13 Nov 10:12 — takes OJ-3 behind DM Bea; ~15:00 est'},out:'11-16 04:30',outBy:'board estimate on the list\\'s own rule (made fast + quantity ÷ hourly norm + 4 h) — not on programme 15.11'},")
set_line("  {b:'OJ-4',", "  {b:'OJ-4',prev:{n:'Chemical Marketer',c:'Chemicals',q:4056,u:'MT',ie:'IMP',ag:'JM Baxi',out:'11-14 08:30',outBy:'night sheet 13 Nov — 2nd amendment (hand-corrected to 14 Nov 09:35): RT OUT 08:30 (was 10:00), Capt Sachin — DPR 14.11: made fast 17:20, commenced 19:30 on the 13th, completed 04:45'},now:{n:'SC Larimar',c:'Chemicals',q:5000,u:'MT',ie:'EXP',loa:158.98,f:'11-14 10:30',est:1,nm:'250',rank:'',ag:'Atlantic Shg',note:'"+L+": OJ-4 · B\\'TODAY · chemicals 5,000 MT EXP, norm 250 MT/h · amended night sheet: IN o/c after Chemical Marketer (RT OUT 08:30) → ~10:30 est'},out:'11-15 17:30',outBy:'"+PG+": outward readiness 15 Nov 17:30 (10.6 m) → Lujain',next:{n:'Lujain',c:'Caustic soda',q:21000,u:'MT',ie:'EXP',loa:183,f:'11-15 19:30',est:1,rank:'1C',ag:'Atlantic Shg',note:'"+PG+": OJ-04 after SC Larimar (readiness 17:30) → ~19:30 est · list 14.11: caustic soda 21,000 MT EXP, arrived / ready 13 Nov 21:48, rank \"1C\", REQ OJ 2, 3, 4'}},")
a,b=line_of("  {b:'OJ-5',"); l=s[a:b]; k=",out:'11-15 04:00',outBy:'"
if l.count(k)!=1: die('OJ-5 tail')
s=s[:a]+l[:l.index(k)]+",out:'11-15 12:30',outBy:'"+PG+": outward readiness 15 Nov 12:30 (5.5 m), no inward named — three days inside the list ETC (18 Nov 14:36 at the norm of 200 MT/h); DPR 14.11 pace ≈ 860 MT/h'},"+s[b:]
a,b=line_of("  {b:'OJ-6',"); l=s[a:b]; k="outBy:'DPR 14.11 pace (≈ 820 MT/h) — board estimate, no sailing signalled'"
if l.count(k)!=1: die('OJ-6 tail')
s=s[:a]+l.replace(k,"outBy:'DPR 14.11 pace (≈ 820 MT/h) — board estimate; not on programme 15.11, no ETC printed on the list'")+s[b:]
set_line("  {b:'OJ-7',", "  {b:'OJ-7',prev:{n:'Pacific Era',c:'CPO',q:15003.55,u:'MT',ie:'IMP',ag:'Marine Links',out:'11-12 06:00',outBy:'re-issued night sheet: RT OUT 06:00, Capt Karan; DPR 12.11: COMPLETED 03:54 — 15,004 MT'},now:{n:'Searay',c:'CPO',q:29999.06,u:'MT',ie:'IMP',loa:178.69,f:'11-14 15:00',est:1,rank:'',ag:'JM Baxi',note:'"+L+": OJ-7 · B\\'TODAY · CPO 29,999 MT IMP, 11.0 m — waiting since 2 Nov (ullage); ~15:00 est'},out:'11-15 10:00',outBy:'"+PG+": \"SHIFTING FROM OJ-07 TO OJ-01. PORT C.\" — moved to OJ-1 to finish; no time printed, ~10:00 is the board\\'s placeholder',next:{n:'CS Rotterdam',c:'CPO',q:10199.8,u:'MT',ie:'IMP',loa:182.7,f:'11-15 12:00',est:1,rank:'',ag:'JM Baxi',note:'"+PG+": OJ-07, \"STARBOARD.\" — after Searay is moved to OJ-1 → ~12:00 est · list 14.11: CPO 10,199.8 MT IMP, 12.0 m, waiting since 7 Nov (commercially ready 9 Nov, ullage issue NR)'}}")
# waiting / expected tankers
a=s.index(" wait:[\n",a0); b=s.index(" moves:[",a)
s=s[:a]+""" wait:[
  {n:'Jag Pushpa',c:'CDSBO',q:44252,u:'MT',ie:'IMP',loa:183,dr:12.44,rep:'11-02 21:36',rdy:'11-06 11:00',rank:'',ag:'JM Baxi',rem:'commercially ready 6 Nov · ULLAGE ISSUE — NR (list 14.11)',st:''},
  {n:'Artigo',c:'CPO',q:24000,u:'MT',ie:'IMP',loa:185,dr:10.5,rep:'11-07 14:36',rdy:'11-08 11:00',rank:'',ag:'GAC Shg',rem:'commercially ready 8 Nov · ULLAGE ISSUE — NR (list 14.11)',st:''},
  {n:'Ginga Cheetah',c:'CDSBO + CDSFO',q:24270,u:'MT',ie:'IMP',loa:159.98,dr:10,rep:'11-08 01:24',rdy:null,rank:'',ag:'Interocean',rem:'N/A · ullage issue',st:''},
  {n:'Silver Gertrude',c:'CDSBO',q:22500,u:'MT',ie:'IMP',loa:183.06,dr:12.9,rep:'11-08 19:54',rdy:null,rank:'',ag:'Interocean',rem:'N/A',st:''},
  {n:'Hafnia Ammolite',c:'CDSBO',q:30800,u:'MT',ie:'IMP',loa:184.06,dr:10.5,rep:'11-10 07:00',rdy:null,rank:'',ag:'Interocean',rem:'N/A',st:''},
  {n:'Lumis',c:'CPO',q:20000,u:'MT',ie:'IMP',loa:174.38,dr:10.7,rep:'11-11 09:00',rdy:null,rank:'',ag:'Atlantic Shg',rem:'N/A · ullage issue',st:''},
  {n:'Ahinos',c:'CPO',q:16609.19,u:'MT',ie:'IMP',loa:183,dr:12.65,rep:'11-12 01:30',rdy:null,rank:'',ag:'Marine Links',rem:'N/A · REQ OJ-07',st:''},
  {n:'Peonia',c:'CDSBO',q:27000,u:'MT',ie:'IMP',loa:164.5,dr:10.4,rep:'11-13 15:42',rdy:null,rank:'',ag:'Interocean',rem:'N/A · REQ OJ-03, 07',st:''},
  {n:'Ishaan',c:'MS',q:29822.6,u:'MT',ie:'IMP',loa:183,dr:9.9,rep:'11-13 18:00',rdy:null,rank:'',ag:'Victory Shg',rem:'N/A · "under process" · OJ-06',st:''}
 ],
 eta:[
  {n:'Avyaan',c:'HSD',q:35000,u:'MT',ie:'IMP',loa:183.06,dr:10.7,eta:'11-14 23:00',rdy:null,ag:'Victory Shg',rem:'REQ OJ-04 · N/A (she is loading at Nayara-A today)'},
  {n:'Haein Hope',c:'Chemicals',q:9504.99,u:'MT',ie:'IMP',loa:124,dr:null,eta:'11-15 00:00',rdy:'11-15 00:00',ag:'Anline',rem:'REQ OJ 2, 3, 4 · readiness with the ETA'},
  {n:'Stolt Norland',c:'Butyl cellosolve',q:997.75,u:'MT',ie:'IMP',loa:182.75,dr:7,eta:'11-15 22:00',rdy:'11-15 22:00',ag:'JM Baxi',rem:'REQ OJ-02 & 3 · readiness with the ETA'},
  {n:'Korea Chemi',c:'Chemicals',q:5000,u:'MT',ie:'IMP',loa:134.16,dr:6,eta:'11-16 00:00',rdy:null,ag:'GAC Shg',rem:''},
  {n:'Bow Fortitude',c:'Chemicals',q:10000,u:'MT',ie:'IMP',loa:158.93,dr:8,eta:'11-17 00:00',rdy:null,ag:'GAC Shg',rem:''},
  {n:'Sriwangi V',c:'CPO',q:10000,u:'MT',ie:'IMP',loa:183.21,dr:11.6,eta:'11-17 16:00',rdy:null,ag:'GAC Shg',rem:'OJ-07'},
  {n:'Eva Richway',c:'Chemicals',q:5750,u:'MT',ie:'IMP',loa:145.53,dr:6,eta:'11-17 20:00',rdy:null,ag:'GAC Shg',rem:''},
  {n:'Bow Endeavor',c:'Chemicals',q:5000,u:'MT',ie:'IMP',loa:159.03,dr:6,eta:'11-17 20:00',rdy:null,ag:'GAC Shg',rem:''},
  {n:'Hartati',c:'Chemicals',q:11000,u:'MT',ie:'IMP',loa:123.19,dr:5.7,eta:'11-19 08:00',rdy:null,ag:'GAC Shg',rem:'REQ OJ 2, 3, 4 · new on list 14.11'},
  {n:'SC Draco',c:'Methanol',q:21336.35,u:'MT',ie:'IMP',loa:182.9,dr:9.9,eta:'11-22 00:00',rdy:null,ag:'Interocean',rem:'new on list 14.11'}
 ],
"""+s[b:]
rep(" moves:[\n  ['Night signal · 13 Nov — 2nd AMENDMENT",
    " moves:[\n  ['Programme for 15.11 — TF/SH/2102 (dated 14 Nov; received 15:55) — oil-jetty rows',[['04:00','OUT','TPT Heart','OJ-2 → OTB · 8.6 m','—','11-15 04:00','NIGHT SAILING · Lavraki after her, NIGHT BERTHING (~06:00 est)'],['—','IN','Lavraki','OTB → OJ-2','—','11-15 06:00','chemicals 2,000 IMP · ready 14 Nov 07:06'],['—','SHIFT','Searay','OJ-7 → OJ-1','—','11-15 10:00','PORT C. · no time printed — placeholder'],['—','IN','CS Rotterdam','OTB → OJ-7','—','11-15 12:00','STARBOARD · CPO 10,200 · after the Searay shift — est'],['12:30','OUT','Bochem Ghent','OJ-5 → OTB · 5.5 m','—','11-15 12:30','no inward named · list ETC was 18 Nov 14:36'],['17:30','OUT','SC Larimar','OJ-4 → OTB · 10.6 m','—','11-15 17:30','Lujain after her'],['—','IN','Lujain','OTB → OJ-4','—','11-15 19:30','caustic soda 21,000 EXP · rank 1C · est']]],\n"
    "  ['List 14.11 (0700) — berthing today at the oil jetties',[['—','IN','TPT Heart','OTB → OJ-2','—','11-14 16:00','B\\'TODAY · behind Torero (readiness 14:00) · est'],['—','IN','Bow Platinum','OTB → OJ-3','—','11-14 15:00','B\\'TODAY · behind DM Bea · est'],['—','IN','SC Larimar','OTB → OJ-4','—','11-14 10:30','B\\'TODAY · signalled o/c after Chemical Marketer 08:30'],['—','IN','Searay','OTB → OJ-7','—','11-14 15:00','B\\'TODAY · CPO 29,999 · est']]],\n"
    "  ['Night signal · 13 Nov — 2nd AMENDMENT")

# ================= TUNA =================
rep("const TUNA={src:'DPA berthing list 11.11.26 (revised) · DPR 12.11 (Navios Felicity I completed 11:00, let go 15:24 on 11 Nov — TT-2, TT-3, TT-4 vacant)',",
    "const TUNA={src:'DPA berthing list 14.11.26 (0700) · programme 15.11 (TF/SH/2102) · DPR 14.11 — TT-2 vacant',")
sub_entry("{b:'TT-1',n:'Doukato'","next:'Europa Graeca (waiting, TT-01, N/A) · Blue Ionian (RDY, TT-01)',note:'","next:'Europa Graeca — programme 15.11: NIGHT BERTHING after Doukato (readiness 15 Nov 03:00) · Blue Ionian (ready 3 Nov, TT-01) waits behind',note:'"+PG+": outward readiness 15 Nov 03:00 (7.1 m), NIGHT SAILING → MT/MV EUROPA GRAECA, NIGHT BERTHING. ")
rep("rep:'10-29 17:30',rdy:null,ag:'Gautham Freight',rem:'TT-01 · N/A (list 11.11)'}","rep:'10-29 17:30',rdy:null,ag:'Gautham Freight',rem:'\"FOLLOWS TT-01\" · programme 15.11: night berthing at TT-1 after Doukato (15 Nov 03:00) → ~05:00 est'}")
rep("rem:'TT-01 · RDY — waits for Doukato (~14 Nov 03:00 at the DPR 13.11 pace); TT-2 is the only vacant Tuna berth now'}\n ],",
    "rem:'TT-01 · ready 3 Nov 11:00 — TT-1 goes to Europa Graeca (the senior, reported 29 Oct) on programme 15.11; she waits behind'},\n  {n:'Beagle',c:'Coal in bulk',q:77220,u:'MT',ie:'IMP',loa:228.99,dr:14.32,rep:'11-14 05:42',rdy:null,ag:'Dariya',rem:'new on list 14.11 · reported 14 Nov 05:42 · N/A'}\n ],")
rep("{n:'Marvelous Star',c:'Coal in bulk',q:50000,u:'MT',ie:'IMP',loa:229,eta:'11-15 00:00',ag:'Atlantic Shg',rem:'moved from the cargo-jetty ETA sheet to Tuna (list 11.11)'}",
    "{n:'Marvelous Star',c:'Coal in bulk',q:50000,u:'MT',ie:'IMP',loa:229,eta:'11-15 14:00',ag:'Atlantic Shg',rem:'list 14.11: ETA / readiness 15 Nov 14:00 · TT-03'}")

# ================= CARGO-JETTY MOVEMENTS =================
rep("const MV=[\n", "const MV=[\n ['Programme for 15.11 — TF/SH/2102 (dated 14 Nov, after the 11:00 meeting; received 15:55; window 14 Nov 18:00 → 15 Nov 18:00) — cargo-jetty rows',["
 "['23:45','OUT','Bristol','CJ-5 · 7.5 m','—','11-14 23:45','NIGHT SAILING · TSP + DAP complete'],"
 "['—','SHIFT','Princess Joanna','CJ-6 → CJ-5 · 37–45¾','—','11-15 01:00','NIGHT SHIFTING · PORT C. · makes CJ-6 free for Truong Minh Dream — est'],"
 "['—','IN','Truong Minh Dream','OTB → CJ-6 · 46¾–54½ · GOVT','—','11-15 03:00','NIGHT BERTHING · DAP + TSP 55,600 · GP 1 · 12.8 m — est'],"
 "['04:40','OUT','SSL Mumbai','CJ-11 · 10.0 m','—','11-15 04:40','NIGHT SAILING · container, not tracked'],"
 "['03:45','IN','TCI Anand','OTB → CJ-11 · 86–94½','—','11-15 06:00','ETA 03:45 · NIGHT STARBOARD · arrival 7.5 m · container, not tracked'],"
 "['17:00','OUT','CD Cherry','CJ-15 · 9.5 m','—','11-15 17:00','24 HRS · kaolin & feldspar 10,800'],"
 "['—','SHIFT','Enishi','CJ-4 → CJ-15 · 142½–155','—','11-15 18:00','AGENT\\'S A/C (DELTA SHG) · logs, about a day of work left — est'],"
 "['—','IN','African Hornbill','OTB → CJ-4 · 27¼–36 · 24 HRS','—','11-15 20:00','ball clay 25,000 EXP · 24H 1 · sailing draft 10.0 m — est'],"
 "['—','—','Not programmed','Cape Diversity (list ETC 15 Nov 05:43, DPR pace ~19:00) · Bomustafao O (permissible time over since 14 Nov 11:33) · Theometor (16 Nov 02:06) · Merchia (16 Nov 08:45) — no outward row; Pioneer Fortune (8K 1) · Gokova-M (HP 1) · Uni Blossom (SGR 1) · Rahma (STL 1) · Saga Viking (GEN 2) · Honor Star · Evangelia D · HN Doris · Vishva Bandhan not berthed','—','11-15 18:00','next: meeting 15 Nov 11:00 → programme 16.11']]],\n"
 " ['List 14.11 (0700) — berthing today',[['—','IN','Cape Venture','OTB → CJ-7/8 · 55¾–67½ · HP','—','11-14 16:30','B\\'TODAY · 121,377 MT alongside (total 165,051) · after Chang Hang 13:45 — est'],['—','IN','CD Cherry','OTB → CJ-15 · 147½–155 · 24 HRS','—','11-14 17:00','B\\'TODAY · after Karpathos Dawn (14:30) — est'],['—','SHIFT','Bristol','CJ-6 → CJ-5 · 37¾–46','—','11-14 19:00','after Belasitza (17:30) — est'],['—','IN','Princess Joanna','OTB → CJ-6 · 47–54½ · GOV','—','11-14 20:30','B\\'TODAY · MOP 25,000 — est'],['—','IN','Coastal Amigo','→ Bunder area (BA)','—','11-14 12:00','B\\'TODAY · steel slab 2,036 · barge berth'],['—','—','Mooring','Queen Coral at MRG-2 · Tan Binh 259 at MRG-3 (B\\'TODAY)','—','11-14 09:45','']]],\n")

open(P,'w',encoding='utf-8').write(s); print('ok',n0,'->',len(s))
