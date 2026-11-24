import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import book,bp_data,bp_data2,wlc
C=wlc.cuv_index(wlc.load())
def txt(c): return json.load(open(os.path.join(book.ROOT,'txt','%02d.json'%c),encoding='utf-8'))
errs=[]
# tracks 驗證
tracks=[]
for t in bp_data2.TRACKS:
    stops=[]
    for ref,q,note,top in t['stops']:
        c,v=map(int,ref.split(':'))
        if not any(s in t['nums'] for l,w in C[(c,v)] for s in wlc.strongs(l)): errs.append(('lemma',t['tr'],ref))
        if q not in txt(c)[v-1]: errs.append(('quote',t['tr'],ref,q))
        stops.append([ref,'「%s」%s'%(q,note),top])
    tracks.append(dict(gk=t['gk'],tr=t['tr'],gl=t['gl'],code=t['code'],root=t['root'],stops=stops,ins=t['ins']))
# 全卷計數：寫進 ins 的數字要與 WLC 一致
import collections
def cnt(nums):
    n=0;vs=set()
    for k,w in C.items():
        m=sum(1 for l,x in w if any(s in nums for s in wlc.strongs(l)))
        if m: n+=m;vs.add(k)
    return n,len(vs)
for t in bp_data2.TRACKS:
    if t['tr'] in ('shuv','sheqer','lev','shalom'):
        n,v=cnt(set(t['nums']));
        if ('%d 次，分布於 %d 節'%(n,v)) not in t['ins']: errs.append(('ins計數',t['tr'],n,v))
chs=[]
for n,t,sub,l,secs,pts in bp_data.CH:
    chs.append(dict(n=n,t=t,sub=sub,lv=l,arc=bp_data.arc(n),
      sec=[['%d:%s'%(n,r.replace('-','--')),title] for r,title in secs],
      serm=dict(pts=[[lab,'%d:%s'%(n,r.replace('-','--')),q] for lab,r,q in pts])))
# 單節寫成 N:V--V（secs 本來就 a-a）
bp=dict(book=book.NAME_TC,slug=book.SLUG,total_verses=book.TOTAL,ch=chs,terrain=dict(points=bp_data2.TERRAIN),tracks=tracks,issues=bp_data2.ISS00,issue_index=[dict(ch=c,t=t) for c,t in bp_data2.ISSUE_INDEX])
json.dump(bp,open(os.path.join(book.ROOT,'blueprint.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
for e in errs: print('ERR',e)
print('blueprint.json 錯誤',len(errs),'章',len(chs),'追蹤字',len(tracks),'ISS00',len(bp_data2.ISS00),'terrain',len(bp_data2.TERRAIN))
