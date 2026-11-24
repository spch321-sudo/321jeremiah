import re,os,sys,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
def load():
    x=open('/home/claude/morphhb/wlc/Jer.xml',encoding='utf-8').read()
    out={}
    for c,v,body in re.findall(r'<verse osisID="Jer\.(\d+)\.(\d+)">(.*?)</verse>',x,flags=re.S):
        words=re.findall(r'<w lemma="([^"]*)"[^>]*>(.*?)</w>',body,flags=re.S)
        out[(int(c),int(v))]=[(l,re.sub(r'<[^>]+>','',w).replace('/','')) for l,w in words]
    return out
def mt2cuv(c,v):
    if (c,v)==(8,23): return (9,1)
    if c==9: return (9,v+1)
    return (c,v)
def cuv_index(W):
    return {mt2cuv(c,v):w for (c,v),w in W.items()}
def lemmas(l): return [p.strip() for p in re.split(r'[/ ]',l) if re.search(r'\d',p)]
def strongs(l): return [re.sub(r'[^0-9]','',p) for p in lemmas(l)]
if __name__=='__main__':
    W=load()
    for ref in [(34,8),(34,9),(34,18),(34,19),(43,5),(43,6)]:
        print(ref,' '.join(w for l,w in W[ref]))
    C=cuv_index(W)
    def cnt(nums):
        res=collections.OrderedDict()
        for k in sorted(C):
            n=sum(1 for l,w in C[k] if any(s in nums for s in strongs(l)))
            if n: res[k]=n
        return res
    for name,nums in [('shuv',{'7725'}),('natash',{'5428'}),('natas',{'5422'}),('banah',{'1129'}),('nata',{'5193'}),('sheqer',{'8267'}),('lev',{'3820','3824'}),('shalom',{'7965'}),('haras',{'2040'}),('abad',{'6'}),('hebel',{'1892'})]:
        r=cnt(set(nums));print(name,sum(r.values()),'in',len(r),'verses',list(r.items())[:60] if sum(r.values())<45 else '')
