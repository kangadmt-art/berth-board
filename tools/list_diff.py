import json,re,sys
s=open('/home/claude/work/pre67.html',encoding='utf-8').read()
a=s.index('const WRAW=['); e=s.index('\n];',a)
board={}
for ln in s[a:e].split('\n')[1:]:
    m=re.match(r"\s*\['((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)',([^,]+),'([^']*)',([^,]+),([^,]+),('[^']*'|null),(\{[^}]*\}),",ln)
    if not m: 
        if ln.strip() and not ln.strip().startswith('//'): print('??',ln[:90])
        continue
    n,c,q,u,loa,dr,rdy,rk=m.groups(); rk=dict((k.strip("'"),v) for k,v in re.findall(r"('?[A-Za-z0-9]+'?):([0-9]+)",rk))
    board[n]=dict(c=c,q=q,rdy=rdy.strip("'"),rk=rk,loa=loa,dr=dr)
def norm(x):
    x=x.upper(); x=re.sub(r"\(GL\)|\(MV\)|\(DV\)|\(SALT, NEXT CALL\)|\(LPG/C\)",'',x); x=re.sub(r"^(M\.?V\.?|M\.?T\.?|LPG/C\.?)\s*[-.]?\s*",'',x.strip()); return re.sub(r'[^A-Z0-9]','',x)
ALI={'PAIWANICE':'PAIWANACE','TUGMARIGOLDBARGEALAACRITY':'TUGMARIGOLDBARGEALAACRITY666','ERNAOLDENDROFF':'ERNAOLDENDORFF','TUGVARAHIWITHBARGEAKG11':'TUGVARAHIBARGEAKG11'}
bn={norm(k):k for k in board}
d=json.load(open('/home/claude/work/in25a/l25.json'))
K=['GP','COASTAL','HP','SAAGAR','24H','8K','STL','GEN']
def rows(sheet,stop):
    out=[];sec=None
    for r in d[sheet]:
        r=[('' if x is None else str(x).strip()) for x in r]+['']*25
        if r[3] in ('CARGO JETTY VESSELS',): sec='CJ'; continue
        if r[3] in ('OIL TANKERS','CONTAINERS','TUNA VESSELS','VADINAR'): sec=r[3]; continue
        if sec=='CJ' and r[1]=='CJ': out.append(r)
    return out
seen=set()
for sheet in ('WAITING LIST','ETA'):
    print('=====',sheet)
    for r in rows(sheet,None):
        nm=norm(r[3]); nm=ALI.get(nm,nm); b=bn.get(nm)
        rk={K[i]:r[12+i] for i in range(8) if r[12+i]}
        rk2={k:v for k,v in rk.items() if k!='STL'}
        rdy=r[11][5:16] if re.match(r'\d{4}-',r[11]) else r[11]
        rep=r[10][5:16] if re.match(r'\d{4}-',r[10]) else r[10]
        if not b: print('NEW  ',r[0],r[3],'|',r[7][:30],r[8],'| dr',r[4],'loa',r[5],'| rep',rep,'rdy',rdy,'|',rk,'|',r[20],'|',r[21][:70]); continue
        seen.add(b); o=board[b]
        ch=[]
        if {k:str(v) for k,v in o['rk'].items()}!={k:(v if v.isdigit() else '98') for k,v in rk2.items() if v not in ('X',)}: ch.append('rk %s -> %s'%(o['rk'],rk))
        if (o['rdy'] if o['rdy']!='null' else '')!=(rdy if re.match(r'\d\d-\d\d',rdy) else '') : ch.append('rdy %s -> %s'%(o['rdy'],rdy))
        try:
            if abs(float(o['q'])-float(r[8]))>1: ch.append('qty %s -> %s'%(o['q'],r[8]))
        except: 
            if sheet=='WAITING LIST': ch.append('qty? %s -> %s'%(o['q'],r[8]))
        print(('CHG  ' if ch else 'same ')+r[0].rjust(2),b,'| rep',rep,'|',' ; '.join(ch),'|',r[21][:60] if ch else '')
print('===== ON BOARD, NOT ON LIST:',[k for k in board if k not in seen])
