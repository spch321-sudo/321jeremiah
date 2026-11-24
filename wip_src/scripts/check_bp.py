import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import book,bp_data
def rng(r):
    a,b=r.split('-'); return int(a),int(b)
def txt(c): return json.load(open(os.path.join(book.ROOT,'txt','%02d.json'%c),encoding='utf-8'))
errs=[];lv={'A':0,'B':0,'C':0}
assert [c[0] for c in bp_data.CH]==list(range(1,53)),'章數不對'
for n,t,sub,l,secs,pts in bp_data.CH:
    N=book.VERSES[n];T=txt(n);lv[l]+=1
    if len(sub.split('、'))!=3 or any(len(x)!=1 for x in sub.split('、')): errs.append((n,'sub',sub))
    nxt=1
    for r,title in secs:
        a,b=rng(r)
        if a!=nxt or b<a: errs.append((n,'sec不連續',r,nxt))
        nxt=b+1
    if nxt!=N+1: errs.append((n,'sec未涵蓋全章',nxt-1,N))
    nxt=1
    if len(pts)!=3: errs.append((n,'pts不是3',len(pts)))
    for lab,r,q in pts:
        a,b=rng(r)
        if a!=nxt: errs.append((n,'pts不連續',r,nxt))
        nxt=b+1
        body=''.join(T[a-1:b])
        if q not in body: errs.append((n,'引句不在範圍',r,q))
    if nxt!=N+1: errs.append((n,'pts未涵蓋全章',nxt-1,N))
print('A/B/C',lv)
for e in errs: print('ERR',e)
print('錯誤',len(errs))
