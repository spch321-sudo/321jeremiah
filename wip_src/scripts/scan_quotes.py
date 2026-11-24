import json,re,sys,difflib
D=json.load(open('build/data.json',encoding='utf-8'))
P=re.compile(r'[，。、；：？！「」『』—－\s（）()…·,.;:?!]')
V=[(f'{n}:{i+1}',P.sub('',v)) for n in D['txt'] for i,v in enumerate(D['txt'][n])]
bible=''.join(v for _,v in V)
def strip(s):return re.sub(r'<[^>]+>','',s)
def texts(o,k,path=''):
    if isinstance(o,str):yield k,strip(o)
    elif isinstance(o,list):
        for x in o:yield from texts(x,k)
    elif isinstance(o,dict):
        for kk,x in o.items():
            if kk in('lit','grk'):continue
            yield from texts(x,k)
out=[];seen=set()
for k in('ch','blk','lesson','serm'):
    for _,s in texts(D[k],k):
        for m in re.finditer(r'[「『]([^「」『』]{10,})[」』]',s):
            q=P.sub('',m.group(1))
            if q in bible or (k,q) in seen:continue
            seen.add((k,q))
            best=(0,'')
            for ref,v in V:
                sm=difflib.SequenceMatcher(None,q,v,autojunk=False)
                if sm.real_quick_ratio()<.5 or sm.quick_ratio()<.5:continue
                # longest common block coverage
                blks=sm.get_matching_blocks();cov=sum(b.size for b in blks)/len(q)
                if cov>best[0]:best=(cov,ref)
            if best[0]>=.6:out.append((k,round(best[0],2),best[1],m.group(1)))
for o in out:print(*o)
print('suspects',len(out))
if len(sys.argv)>1 and sys.argv[1]=='fix':
    import glob
    sus={(k,q) for k,_,_,q in out}
    cnt=0
    for k in('ch','blk','lesson','serm'):
        for f in sorted(glob.glob(f'{k}/*.json')):
            raw=open(f,encoding='utf-8').read();new=raw
            for kk,q in sus:
                if kk!=k:continue
                for a,b in(('「','」'),('『','』')):
                    t=a+q+b
                    if t in new:new=new.replace(t,q);cnt+=1
            if new!=raw:open(f,'w',encoding='utf-8').write(new)
    print('stripped',cnt)
