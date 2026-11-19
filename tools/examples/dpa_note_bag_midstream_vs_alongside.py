import re,statistics
def num(x):
    try: return float(str(x).replace(',',''))
    except Exception: return 0.0
ms=[];al=[];tot={}
for day in ['11','12','17','18','19']:
    shipside=0
    for ln in open('/home/claude/work/dprx/dpr%s.txt'%day,encoding='utf-8'):
        p=[x.strip() for x in ln.rstrip('\n').split(' | ')]
        if len(p)<17 or p[2] not in('IMP','EXP'): continue
        loc=p[0].upper(); t=num(p[6]); g=[num(x) for x in p[13:16]]; hooks=sum(g)
        isbag=bool(re.search(r'BAG|J/B',p[3],re.I))
        if re.match(r'^(MS|MRG)',loc) and not re.search(r'\(\s*(MV|DV)\s*\)',p[1]) and t>0:
            shipside+=t
            if isbag: ms.append((day,p[1],p[3],t,hooks,g))
        if re.match(r'^CJ-?\s*\d',loc) and isbag and t>0: al.append((day,loc,p[1],p[3],t,hooks,g))
    tot[day]=shipside
print('ship-side barge totals',tot,'mean',round(statistics.mean(tot.values())))
print('MIDSTREAM bag vessel-days',len(ms),'mean',round(statistics.mean(x[3] for x in ms)),'range',min(x[3] for x in ms),max(x[3] for x in ms))
h=[x for x in ms if x[4]>0]; print('  with hooks printed',len(h),'MT',sum(x[3] for x in h),'hooks',sum(x[4] for x in h),'MT/hook',round(sum(x[3] for x in h)/sum(x[4] for x in h)),'avg hooks/day',round(statistics.mean(x[4] for x in h),1))
print('  one gang a shift or less (hooks<=3):',sum(1 for x in h if x[4]<=3),'of',len(h))
full=[x for x in al if all(v>0 for v in x[6])]
print('ALONGSIDE bag vessel-days (all three shifts)',len(full),'mean',round(statistics.mean(x[4] for x in full)),'range',min(x[4] for x in full),max(x[4] for x in full),'MT/hook',round(sum(x[4] for x in full)/sum(x[5] for x in full)),'avg hooks/day',round(statistics.mean(x[5] for x in full),1))
for x in full: print('   ',x[0],x[1],x[2][5:22],x[3][:20],int(x[4]),int(x[5]))
print('alongside not full:',[(x[0],x[2][5:18],int(x[4]),x[6]) for x in al if x not in full])
