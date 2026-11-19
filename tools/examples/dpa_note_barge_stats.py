import re,sys,collections
def num(x):
    try: return float(str(x).replace(',',''))
    except Exception: return 0.0
for day in sys.argv[1:]:
    path='/home/claude/work/dprx/dpr%s.txt'%day
    shore=collections.OrderedDict(); ship=[]; sts=[]; ms_total=None; codes=collections.Counter()
    for ln in open(path,encoding='utf-8'):
        p=[x.strip() for x in ln.rstrip('\n').split(' | ')]
        if len(p)>4 and re.match(r'MID\s*STREAM',p[1],re.I): ms_total=(p[2],p[3],p[4])
        if len(p)<13: continue
        loc=p[0].upper(); raw=p[1]
        if re.match(r'^(MS|MRG)',loc):
            if re.search(r'\(\s*(MV|DV)\s*\)',raw): sts.append((raw,num(p[6]))); continue
            ship.append((loc,raw,p[2],p[3],num(p[6]),num(p[9]),num(p[12]),p[13:17]))
        elif re.match(r'^(CJ$|CJ/OP|OP/CJ|OP$|IFFCO|BA$)',loc):
            codes[loc]+=1; shore.setdefault(loc,0); shore[loc]+=num(p[6])
    print('=== DPR',day,'MID STREAM row (loaded, unloaded, total):',ms_total)
    print(' shore points 24h:',dict(shore),'rows per code',dict(codes),'sum',sum(shore.values()))
    tot=0; work=0
    for s in ship:
        tot+=s[4]; work+= 1 if s[4]>0 else 0
        print('   %-6s %-28s %-3s %-22s 24h %7d upto %7d bal %7d gangs %s'%(s[0],s[1][:28],s[2],s[3][:22],s[4],s[5],s[6],'/'.join(s[7])))
    print(' ship-side rows',len(ship),'working',work,'24h sum',tot,'| ship-to-ship',sts)
