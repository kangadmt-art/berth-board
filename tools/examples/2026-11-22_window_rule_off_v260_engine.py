# v260 (engine part) — Mihir, 22 Nov 18:09: "maine jo rule diya tha woh nikal do". The rule of 1 / 7 Nov — a place whose vessel sails inside the same
# meeting window is allotted again for that window while she is still alongside — is switched off. A place is free only once its vessel has sailed:
# the vessel leaving under a priority is replaced by the next vessel of that priority ("24 ke badle 24").
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/dpa-berth-board.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)
rep("function simulate(ov,PRE){", "const WINDOW_ALLOT=false; // Mihir, 22 Nov 18:09: the 1 / 7 Nov rule is withdrawn — a place whose vessel sails later in the window is NOT given out while she is still alongside; it is free when she has sailed (\"24 ke badle 24\"). true = the old behaviour.\nfunction simulate(ov,PRE){")
rep("&&!(C.k==='HP'&&(x.cat==='GEN'||x.cat==='STL'))&&!(x.T>e.t&&x.T<=WX&&firmX(x))).length;", "&&!(C.k==='HP'&&(x.cat==='GEN'||x.cat==='STL'))&&!(WINDOW_ALLOT&&x.T>e.t&&x.T<=WX&&firmX(x))).length;")
rep("const occS=o.filter(x=>x.cat==='SAAGAR'&&!(x.T>e.t&&x.T<=WX&&firmX(x)));", "const occS=o.filter(x=>x.cat==='SAAGAR'&&!(WINDOW_ALLOT&&x.T>e.t&&x.T<=WX&&firmX(x)));")
open(P, 'w', encoding='utf-8').write(s)
print('engine: window allotment switched off', len(s))
