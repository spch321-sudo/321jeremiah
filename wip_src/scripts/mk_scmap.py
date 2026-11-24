"""由本卷全部文字（DATA＋外殼）用 ICU 推導 SCMAP：逐字表＋詞組表，逐字驗證。"""
import json,re,html,collections,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tc2sc import icu
CJK=re.compile(r'[㐀-䶿一-鿿]')
def pieces_from(page_html_noscm,extra=()):
    P=set()
    def add(t):
        t=html.unescape(t)
        if CJK.search(t):P.add(t)
    m=re.search(r'<script id="DATA"[^>]*>(.*?)</script>',page_html_noscm,re.S)
    D=json.loads(m.group(1).replace('<\\/','</'))
    def walk(o):
        if isinstance(o,str):
            for t in re.split(r'<[^>]*>',o):add(t)
        elif isinstance(o,list):
            for x in o:walk(x)
        elif isinstance(o,dict):
            for x in o.values():walk(x)
    walk(D)
    shell=page_html_noscm.replace(m.group(0),'')
    shell=re.sub(r'<script id="SCMAP".*?</script>','',shell,flags=re.S)
    for t in re.split(r'<[^>]*>|\$\{[^}]*\}|[\'"`\n\\]',shell+'\n'.join(extra)):add(t)
    return sorted(P)
def build(pieces):
    T='\u0001'.join(pieces);S='\u0001'.join(icu(p) for p in pieces)
    assert len(T)==len(S),'長度不一致'
    cnt=collections.defaultdict(collections.Counter)
    for a,b in zip(T,S):
        if CJK.match(a) or a!=b:cnt[a][b]+=1
    default={c:k.most_common(1)[0][0] for c,k in cnt.items()}
    P={}
    def sim(t):
        out=[];i=0;n=len(t)
        heads=collections.defaultdict(list)
        for k in P:heads[k[0]].append(k)
        for h in heads:heads[h].sort(key=len,reverse=True)
        while i<n:
            c=t[i];hit=False
            if c in heads:
                for k in heads[c]:
                    if t.startswith(k,i):out.append(P[k]);i+=len(k);hit=True;break
            if hit:continue
            out.append(default.get(c,c));i+=1
        return ''.join(out)
    for it in range(30):
        R=sim(T)
        bad=[i for i,(a,b) in enumerate(zip(R,S)) if a!=b]
        print('iter',it,'mismatch',len(bad))
        if not bad:break
        added=0
        for i in bad:
            ok=False
            for L in range(2,16):
                for a in range(0,min(L,4)):
                    l=i-a;r=l+L
                    if l<0 or r>len(T):continue
                    W=T[l:r]
                    if '\u0001' in W:continue
                    out=S[l:r]
                    if P.get(W)==out:ok=True;break
                    if W in P:continue
                    good=True;p=T.find(W)
                    while p!=-1:
                        if S[p:p+L]!=out:good=False;break
                        p=T.find(W,p+1)
                    if good:P[W]=out;added+=1;ok=True;break
                if ok:break
        if not added:raise SystemExit('無法收斂')
    # 逐字表：只放 default!=c
    m=[(c,d) for c,d in default.items() if c!=d and CJK.match(c)]
    m.sort()
    # 冪等
    return m,P,pieces,sim
def finalize(pieces):
    m,P,pieces,sim=build(pieces)
    for O in set(P.values()):
        if O not in P and not any(ch in P and False for ch in O):P[O]=O
    pr=sorted(P.items())
    return {'m':[''.join(a for a,_ in m),''.join(b for _,b in m)],'p':[[a,b] for a,b in pr]}
def check_js_equiv(sc,pieces):
    mm=dict(zip(*sc['m']));PP={a:b for a,b in sc['p']};lens=sorted({len(a) for a in PP},reverse=True);heads={a[0] for a in PP}
    def toSC(s):
        o=[];i=0;n=len(s)
        while i<n:
            c=s[i]
            if c in heads:
                hit=False
                for L in lens:
                    r=PP.get(s[i:i+L])
                    if r is not None:o.append(r);i+=L;hit=True;break
                if hit:continue
            o.append(mm.get(c,c));i+=1
        return ''.join(o)
    bad=0;idem=0
    for p in pieces:
        e=icu(p);r=toSC(p)
        if r!=e:bad+=1;print('不符',p[:30],r[:30],e[:30]) if bad<5 else 0
        if toSC(e)!=e:idem+=1
    return bad,idem
