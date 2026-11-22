import json,re
COLS=['GP','CSTL','HP','SGR','24H','8K','STL','GEN']
def norm(n):
    n=str(n).upper()
    n=re.sub(r'\(.*?\)','',n)
    n=re.sub(r'^\s*(M\.?\s*V\.?|M\.?\s*T\.?|MV\.?|MT\.?|TUG|BARGE)\s*[\.\-]?\s*','',n)
    n=re.sub(r'[^A-Z0-9 ]','',n); n=re.sub(r'\s+',' ',n).strip()
    return n
def load(tag):
    d=json.load(open(f'/home/claude/work/bt/{tag}.json'))
    out={'berth':[],'wait':[],'eta':[]}
    # AT BERTH
    rows=d.get('AT BERTH',[]); hi=next((i for i,r in enumerate(rows) if any(str(x).strip().upper()=='PRIORITY' for x in r)),None)
    if hi is not None:
        H=[str(x).strip().upper() for x in rows[hi]]
        ci=lambda *names: next((H.index(n) for n in names if n in H),None)
        cP,cB,cV,cC,cQ,cN,cMF,cE,cA,cR,cL=ci('PRIORITY'),ci('BERTH'),ci('VESSEL NAME','VESSEL'),ci('CARGO'),ci('QTY'),ci('NORMS (MT)','NORMS'),ci('MADE FAST'),ci('ETC'),ci('AGENT'),ci('REMARKS'),ci('LOA')
        pr=''
        for r in rows[hi+1:]:
            r=[str(x) for x in r]+['']*30
            if r[cP].strip(): pr=r[cP].strip()
            if not r[cV].strip() or not r[cB].strip(): continue
            out['berth'].append({'pr':pr,'b':r[cB].strip(),'v':r[cV].strip(),'n':norm(r[cV]),'cargo':r[cC].strip(),'qty':r[cQ].strip(),'norm':r[cN].strip() if cN is not None else '','mf':r[cMF].strip(),'etc':r[cE].strip(),'agent':r[cA].strip() if cA is not None else '','rem':r[cR].strip() if cR is not None else '','loa':r[cL].strip() if cL is not None else ''})
    for sh,key in (('WAITING LIST','wait'),('ETA','eta')):
        rows=d.get(sh,[]); hi=next((i for i,r in enumerate(rows) if any(str(x).strip()=='GP' for x in r)),None)
        if hi is None: continue
        H=[str(x).strip() for x in rows[hi]]; g=H.index('GP'); cV=next(i for i,x in enumerate(H) if x.lower().startswith('vessel')); cT=next((i for i,x in enumerate(H) if x.upper().startswith('CJ')),1)
        for r in rows[hi+1:]:
            r=[str(x) for x in r]+['']*30
            if not r[cV].strip() or not re.match(r'^\d',r[0].strip() or 'x'): continue
            rk={COLS[i]:r[g+i].strip() for i in range(8) if r[g+i].strip()}
            out[key].append({'typ':r[cT].strip(),'v':r[cV].strip(),'n':norm(r[cV]),'dr':r[cV+1].strip(),'loa':r[cV+2].strip(),'ie':r[cV+3].strip(),'cargo':r[cV+4].strip(),'qty':r[cV+5].strip(),'rep':r[g-2].strip(),'rdy':r[g-1].strip(),'rk':rk,'agent':r[g+8].strip(),'rem':r[g+9].strip()})
    return out
