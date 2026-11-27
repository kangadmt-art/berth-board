import sys; sys.path.insert(0,'/home/claude/berth-board/tools'); from boardpatch import Board
B=Board('/home/claude/work/dpa-berth-board.html')
SRC='public AIS port calls (Maritime Optima), read 27 Nov'
LP=[("{n:'AG Varvara',cbm:39113,from:'Australia'","Hobart + Portland","last calls before Kandla: Hobart, then Portland (both Australia)"),
("{n:'CD Glory',cbm:29158,from:'Malaysia'","Port Klang ?","last calls before Kandla: Pengerang, then Port Klang (Malaysia) — the earlier calls are not shown, so a Sarawak load port cannot be ruled out"),
("{n:'Dariya Priya',cbm:44968,from:'New Zealand'","Port Chalmers","last calls before Kandla: Port Chalmers (New Zealand), then Singapore (bunkers)"),
("{n:'Paiwan Ace',cbm:36905,from:'Uruguay'","Montevideo","last calls before Kandla: Callao (Peru), then Montevideo (Uruguay)"),
("{n:'Erna Oldendorff',cbm:34424,from:'Australia'","Burnie + Portland","last calls before Kandla: Burnie, then Portland (both Australia)"),
("{n:'Paiwan Wisdom',cbm:19320,from:'USA'","Pascagoula","last calls shown: Palm Beach, Pascagoula (USA), then Ponce (Puerto Rico) 13–17 Oct"),
("{n:'Team Bravo',cbm:20722,from:'—'","Pascagoula","last calls shown: Barranquilla (Colombia), Pascagoula (USA), then Walvis Bay 9 Nov for 12 hours (bunkers)"),
("{n:'African Tiger',cbm:36328,from:'Uruguay'","","port not found — the public page still shows her September calls"),
("{n:'African Pheasant',cbm:45282,from:'New Zealand'","","port not found — the public page still shows her September calls")]
for m,lp,n in LP:
    new=m+",lp:'%s',lpn:'%s'"%(lp,B.q(n+' · '+SRC))
    if 'Team Bravo' in m: new=new.replace("from:'—'","from:'USA'")
    B.rep(m,new)
B.rep("from:tr.from&&tr.from!=='—'?tr.from:'',q,","from:tr.from&&tr.from!=='—'?tr.from:'',lp:tr.lp||'',lpn:tr.lpn||'',q,")
B.rep("const tmbKind=c=>","const lpC=r=>`<td class=\"l\" title=\"${(r.lpn||'').replace(/\"/g,'&quot;')}\">${r.lp?'<b>'+r.lp+'</b>'+(r.from?'<small> · '+r.from+'</small>':''):(r.from||'—')+'<small> · port not found</small>'}</td>`; // load port — from public AIS port calls, searched for every timber vessel when she first appears (Mihir, 27 Nov); the agent's paper overrides it\nconst tmbKind=c=>")
B.rep("['Vessel','Timber','Berth','Berthed under','CBM',","['Vessel','Timber','Load port','Berth','Berthed under','CBM',")
B.rep("nb.map(r=>tro(r)+nm(r)+`<td>${tmbKind(r.c)}</td><td>${bq(r)}</td>","nb.map(r=>tro(r)+nm(r)+`<td>${tmbKind(r.c)}</td>${lpC(r)}<td>${bq(r)}</td>")
B.rep("tbl(G.wait,['Vessel','Timber','CBM',","tbl(G.wait,['Vessel','Timber','Load port','CBM',")
B.rep("nw.map(r=>{const B=boardOf(r);return tro(r)+nm(r)+`<td>${tmbKind(r.c)}</td><td>","nw.map(r=>{const B=boardOf(r);return tro(r)+nm(r)+`<td>${tmbKind(r.c)}</td>${lpC(r)}<td>")
B.rep("tbl(G.eta,['Vessel','Timber','CBM','ETA','Team ETB','Board: about','From','Agent · stevedore']","tbl(G.eta,['Vessel','Timber','Load port','CBM','ETA','Team ETB','Board: about','Agent · stevedore']")
B.rep("ne.map(r=>{const B=boardOf(r);return tro(r)+nm(r)+`<td>${tmbKind(r.c)}</td><td>","ne.map(r=>{const B=boardOf(r);return tro(r)+nm(r)+`<td>${tmbKind(r.c)}</td>${lpC(r)}<td>")
B.rep("<td>${r.from||'—'}</td><td class=\"l\">${ag(r)}${stvS(r.n,r.mf!=null?r.mf:(r.nor!=null?r.nor:null))}</td></tr>`;}));","<td class=\"l\">${ag(r)}${stvS(r.n,r.mf!=null?r.mf:(r.nor!=null?r.nor:null))}</td></tr>`;}));")
B.rep("${r.from?' · '+r.from:''}${r.ag?' · agent '+r.ag:''} · ${srcTag}","${r.lp?' · loaded '+r.lp:''}${r.from?' · '+r.from:''}${r.lpn?' · '+r.lpn:''}${r.ag?' · agent '+r.ag:''} · ${srcTag}")
B.save()
