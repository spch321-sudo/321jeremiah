import re,json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import book
src=os.path.join(book.ROOT,'usfm_raw','25-JERcmn-cu89t.usfm')
out=os.path.join(book.ROOT,'txt');os.makedirs(out,exist_ok=True)
ch={};cur=None;vk=None
for line in open(src,encoding='utf-8').read().splitlines():
    m=re.match(r'\\c (\d+)',line)
    if m: cur=int(m.group(1)); ch[cur]=[]; vk=None; continue
    if cur is None: continue
    if re.match(r'\\(s1|r|b|mt1|h|toc\d|id)\b',line): 
        if re.match(r'\\(s1|r)\b',line): vk=None  # 標題後不續接
        continue
    m=re.match(r'\\v (\d+)(?:-(\d+))? ?(.*)',line)
    if m:
        ch[cur].append([int(m.group(1)),int(m.group(2) or m.group(1)),m.group(3)]); vk=ch[cur][-1]; continue
    m=re.match(r'\\(q1|q2|p|m)\s*(.*)',line)
    if m and vk is not None: vk[2]+=m.group(2)
def clean(t):
    t=re.sub(r'\\f .*?\\f\*','',t)           # 註腳
    t=re.sub(r'\\(pn|add)\*?','',t)
    t=re.sub(r'\s+','',t)                    # 中文不留空白
    t=t.replace('上帝','神').replace('裏','裡').replace('着','著')  # 與以賽亞書 txt 同一規範
    return t
SPLIT={(34,8):'叫各人',(34,18):'後來又違背',(43,5):'男人、婦女'}
res={}
for c,vs in ch.items():
    arr=[]
    for a,b,t in vs:
        t=clean(t)
        if a!=b:
            k=SPLIT[(c,a)]; i=t.index(k)
            parts=[t[:i],t[i:]] if (c,a)!=(43,5) else None
            if parts is None:
                # 43:5--6：5 節到「…基大利那裏的眾人」止；6 節以「與先知」起
                parts=[t[:i],t[i:]]
            arr+=parts
        else: arr.append(t)
    res[c]=arr
    assert len(arr)==book.VERSES[c],(c,len(arr),book.VERSES[c])
    json.dump(arr,open(os.path.join(out,'%02d.json'%c),'w',encoding='utf-8'),ensure_ascii=False)
print('chapters',len(res),'verses',sum(len(v) for v in res.values()))
for c,v in ((34,(7,8,17,18)),(43,(4,5))):
    for i in v: print(c,i+1,res[c][i][:70],'…',res[c][i][-24:])
print(res[9][0]);print(res[8][22-1])
