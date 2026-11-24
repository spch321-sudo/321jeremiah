import json,re,os,sys,glob,copy
R='/home/claude/jer';sys.path.insert(0,R+'/en')
import units as U
H=U.H;FW=U.FW
def mapping():
    allu=json.load(open(R+'/en/units_all.json',encoding='utf-8'))
    M=json.load(open(R+'/en/auto.json',encoding='utf-8'))
    miss=0
    for f in sorted(sorted(glob.glob(R+'/en/out/P*.json'))+sorted(glob.glob(R+'/en/out/Q*.json'))):
        o=json.load(open(f,encoding='utf-8'))
        for k,v in o.items():
            if k in allu:M[allu[k]]=v
    return M,allu
def build(strict=True):
    M,allu=mapping()
    D=json.loads(json.dumps(U.D))
    missing=[]
    def conv(o):
        if isinstance(o,str):
            if H.search(o) or FW.search(o):
                if o in M:return M[o]
                r=U.auto(o)
                if r is not None:return r
                missing.append(o);return o
            return o
        if isinstance(o,list):return [conv(x) for x in o]
        if isinstance(o,dict):return {k:conv(x) for k,x in o.items()}
        return o
    E={k:conv(v) for k,v in D.items() if k!='txt'}
    E['txt']={str(n):WEBL[str(n)] for n in range(1,53)}
    # 字數改英文字數
    w=lambda b:len(re.findall(r"[A-Za-z0-9’'\-]+",re.sub(r'<[^>]+>','',b if isinstance(b,str) else ' '.join(b))))
    for n,L in E['lesson'].items():
        bl=L['blocks']
        L['chars']=sum(w(b[1]) for b in bl if b[0] in('h','p'));L['dchars']=sum(w(b[1]) for b in bl if b[0]=='d');L['tchars']=sum(w(b[1]) for b in bl if b[0] in('s','t','m','n'))
    E={k:E[k] for k in('ch','txt','blk','serm','issues','terrain','tracks','lesson')}
    return E,missing
WEBL=json.load(open(R+'/en/web_jer.json',encoding='utf-8'))
def han_left(E):
    bad=[]
    def walk(o,p):
        if isinstance(o,str):
            if H.search(o) or FW.search(o):bad.append((p,o[:40]))
        elif isinstance(o,list):
            for i,x in enumerate(o):walk(x,p+[i])
        elif isinstance(o,dict):
            for k,x in o.items():walk(x,p+[k])
    walk(E,[]);return bad
if __name__=='__main__':
    E,missing=build()
    print('missing',len(missing),'han left',len(han_left(E)))
    if '--write' in sys.argv:
        assert not missing
        json.dump(E,open(R+'/build/data_en.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'));print('written')
