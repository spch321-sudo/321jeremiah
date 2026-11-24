# -*- coding: utf-8 -*-
"""ch 建構器：ch/src/NN.py 的 C(dict) 與 藍圖前七欄合併 -> ch/NN.json（16欄）
C: q,truth,mv(t,r),card[7],self,t321{k,g,p},grp[5],prac{main,items[5]},safe[(誤,正,驗)]"""
import json,os,sys,re,importlib.util
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from book import *
PUN=re.compile(r'[\s，。、；：？！「」『』（）()—…·‧－\-　“”‘’]')
def norm(s):return PUN.sub('',s)
CIRC='①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯'
B=json.load(open(os.path.join(ROOT,'blueprint.json'),encoding='utf-8'))
def run(n):
    p=os.path.join(ROOT,'ch/src/%02d.py'%n)
    sp=importlib.util.spec_from_file_location('c%d'%n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);C=m.C
    bp=B['ch'][str(n)] if isinstance(B['ch'],dict) else B['ch'][n-1]
    txt=json.load(open(os.path.join(ROOT,'txt/%02d.json'%n),encoding='utf-8'));allv=norm(''.join(txt))
    err=[]
    if not 120<=len(C['q'])<=340:err.append('q 長度 %d'%len(C['q']))
    if not 25<=len(C['truth'])<=140:err.append('truth 長度 %d'%len(C['truth']))
    mv=C['mv'];mr=re.fullmatch(r'耶(\d+):(\d+)(?:[–\-]+(\d+))?',mv['r'])
    if not mr:err.append('mv.r 格式')
    else:
        c,a=int(mr.group(1)),int(mr.group(2));z=int(mr.group(3) or a)
        if c!=n:err.append('mv 章號')
        else:
            seg=norm(''.join(txt[a-1:z]))
            for part in re.split('……',mv['t']):
                if norm(part) not in seg:err.append('mv 不在 %s：%s'%(mv['r'],part[:20]))
    card=C['card']
    if len(card)!=7:err.append('card 需 7 張')
    elif not card[6].startswith('最終整合：'):err.append('card[6] 需「最終整合：」起頭')
    if not C.get('self'):err.append('self 空')
    for k in 'kgp':
        if not re.search(r'耶\d+:\d+',C['t321'][k]):err.append('t321.%s 缺經文引用'%k)
    g=C['grp']
    heads=['【一、破冰】','【二、扎心】','【三、經文】','【四、福音】','【五、行動】']
    if len(g)!=5 or any(not g[i].startswith(heads[i]) for i in range(min(5,len(g)))):err.append('grp 需五題且標題依序 '+''.join(heads))
    pr=C['prac']
    labs=['對神：','對自己：','對人：','對生活：','對使命：']
    if len(pr['items'])!=5 or any(not pr['items'][i].startswith(labs[i]) for i in range(min(5,len(pr['items'])))):err.append('prac.items 五項依序 對神/自己/人/生活/使命')
    lo,hi=LV_QUOTA[bp['lv']]
    if not lo<=len(C['safe'])<=hi:err.append('safe %d 條不在 %s級 %d–%d'%(len(C['safe']),bp['lv'],lo,hi))
    safe=[]
    for i,(w,r,v) in enumerate(C['safe']):
        if len(w)<8 or len(r)<10:err.append('safe%d 太短'%(i+1))
        if '?' in v and False:pass
        safe+=['%s 錯誤講法：%s'%(CIRC[i],w),'正確理解：%s'%r,'檢驗標準：%s'%v]
    if err:
        print('第%d章 ch ✗'%n);[print('  -',e) for e in err];return False
    out=dict(n=bp['n'],t=bp['t'],sub=bp['sub'],lv=bp['lv'],arc=bp['arc'],sec=bp['sec'],serm=bp['serm'],q=C['q'],truth=C['truth'],mv=C['mv'],card=card,self=C['self'],t321=C['t321'],grp=g,prac=pr,safe=safe)
    json.dump(out,open(os.path.join(ROOT,'ch/%02d.json'%n),'w',encoding='utf-8'),ensure_ascii=False)
    print('✓ 第%d章 ch 通過：%s級 safe %d 條'%(n,bp['lv'],len(C['safe'])));return True
if __name__=='__main__':
    sys.exit(0 if all([run(int(x)) for x in sys.argv[1:]]) else 1)
