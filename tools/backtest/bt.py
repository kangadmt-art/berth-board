import sys,re; sys.path.insert(0,'/home/claude/work/bt')
from load import load
tags=['l13','l14','l16','l17','l18','l19','l20','l21','l21r']
L={t:load(t) for t in tags}
cb=lambda b: re.sub(r"[\[\]']",'',b)
CJ=lambda x: cb(x['b']) in ('1','2','3','4','5','6','7','8','13','14','15','15A','15B','16') and x['pr'] in ('GOV','COASTAL','HP','SAAGAR','24 HRS','6.5K / 8K','PROJECT/STEEL','BITUMEN','GENERAL','SR. NO. 07','OTHERS')
COL={'GOV':'GP','COASTAL':'CSTL','HP':'HP','SAAGAR':'SGR','24 HRS':'24H','6.5K / 8K':'8K','PROJECT/STEEL':'STL','GENERAL':'GEN','BITUMEN':'GEN'}
SH={'GOV':'GOV','COASTAL':'CSTL','HP':'HP','SAAGAR':'SGR','24 HRS':'24H','6.5K / 8K':'8K','PROJECT/STEEL':'STL','BITUMEN':'BIT','GENERAL':'GEN','SR. NO. 07':'SR7','OTHERS':'OTH'}
num=lambda s: float(s) if re.fullmatch(r'\d+(\.\d+)?',s or '') else None
ev=[]
for i in range(1,len(tags)):
    P,N=L[tags[i-1]],L[tags[i]]
    prevB={x['n'] for x in P['berth'] if CJ(x)}
    wait={w['n']:w for w in P['wait']}; eta={w['n']:w for w in P['eta']}
    for x in N['berth']:
        if not CJ(x) or x['n'] in prevB or x['n']=='VACANT' or x['b'].startswith('['): continue
        w=wait.get(x['n']) or eta.get(x['n']); src='W' if x['n'] in wait else ('E' if x['n'] in eta else '-')
        col=COL.get(x['pr']); r=num(w['rk'].get(col,'')) if (w and col) else None
        ranked=sorted([(num(q['rk'].get(col,'')),q['n'],q) for q in P['wait'] if col and num(q['rk'].get(col,'')) is not None]) if col else []
        ahead=[(a,n,q) for a,n,q in ranked if r is not None and a<r]
        ev.append(dict(day=tags[i][1:],prev=tags[i-1][1:],pr=SH[x['pr']],b=cb(x['b']),n=x['n'],cargo=x['cargo'],rem=x['rem'],src=src,rk=(w or {}).get('rk',{}),r=r,top=ranked[0][0] if ranked else None,topn=ranked[0][1] if ranked else '',ahead=ahead,wrem=(w or {}).get('rem','')))
if __name__=='__main__':
    for e in ev:
        tag='TOP' if (e['r'] is not None and e['r']==e['top']) else ('no-rank' if e['r'] is None else 'SKIP %d'%len(e['ahead']))
        print(f"{e['prev']}→{e['day']} {e['pr']:4} CJ-{e['b']:3} {e['n'][:22]:22} {e['cargo'][:20]:20} [{e['src']}] ranks {str(e['rk'])[:44]:44} {tag:8} {e['rem'][:34]}")
        for a,n,q in e['ahead'][:4]: print(f"        ahead: {int(a)} {n[:22]:22} {q['cargo'][:22]:22} loa {q['loa']:6} dr {q['dr']:5} rdy {q['rdy'][:16]:16} | {q['rem'][:60]}")
