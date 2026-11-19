import re,sys,statistics
def num(x):
    try: return float(str(x).replace(',',''))
    except Exception: return 0.0
bag=[];bulk=[]
for day in sys.argv[1:]:
    print('== DPR',day)
    for ln in open('/home/claude/work/dprx/dpr%s.txt'%day,encoding='utf-8'):
        p=[x.strip() for x in ln.rstrip('\n').split(' | ')]
        if len(p)<17: continue
        loc=p[0].upper()
        if re.match(r'^(CJ$|CJ/OP|OP/CJ|OP$|IFFCO|BA$)',loc):
            print('  SHORE %-6s %-26s %-3s %-24s 24h %6d upto %6d bal %6d g %s'%(loc,p[1][:26],p[2],p[3][:24],num(p[6]),num(p[9]),num(p[12]),'/'.join(p[13:17])))
        if re.match(r'^(MS|MRG)',loc) and not re.search(r'\(\s*(MV|DV)\s*\)',p[1]) and 0<num(p[6])<60000 and p[2] in('IMP','EXP'):
            (bag if re.search(r'BAG|J/B',p[3],re.I) else bulk).append((day,p[1],p[3],num(p[6]),'/'.join(p[13:17])))
        if re.match(r'^CJ-?\s*\d',loc) and re.search(r'BAG',p[3],re.I) and num(p[6])>0:
            print('  BERTH %-6s %-26s %-3s %-24s 24h %6d bal %6d g %s  %s'%(loc,p[1][:26],p[2],p[3][:24],num(p[6]),num(p[12]),'/'.join(p[13:17]),p[20][:50] if len(p)>20 else ''))
print('bag rows',len(bag),'min',min(x[3] for x in bag),'max',max(x[3] for x in bag),'mean',round(statistics.mean(x[3] for x in bag)),'median',statistics.median(x[3] for x in bag))
print('bag gangs',[x[4] for x in bag])
print('bulk rows',[(x[0],x[1][5:20],int(x[3]),x[4]) for x in bulk])
