# -*- coding: utf-8 -*-
"""serm 建構器：serm/src/NN.txt -> serm/NN.json
格式：第一行 '# 《標題》'；'> 經文（耶x:y）' 為引經；其餘每行一段。引經須逐字在該章和合本。"""
import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from book import *
PUN=re.compile(r'[\s，。、；：？！「」『』（）()—…·‧－\-　“”‘’]')
def norm(s):return PUN.sub('',s)
def run(n):
    src=open(os.path.join(ROOT,'serm/src/%02d.txt'%n),encoding='utf-8').read().strip().split('\n')
    txt=json.load(open(os.path.join(ROOT,'txt/%02d.json'%n),encoding='utf-8'))
    allv=norm(''.join(txt))
    bl=[];err=[]
    for i,l in enumerate(src):
        l=l.strip()
        if not l:continue
        if l.startswith('# '):
            if i!=0:err.append('標題只能在第一行')
            t=l[2:].strip()
            if not(t.startswith('《') and t.endswith('》')):err.append('標題需《》')
            bl.append(['h',t])
        elif l.startswith('> '):
            q=l[2:].strip()
            m=re.search(r'（耶(\d+):(\d+)(?:[–\-]+(\d+))?）$',q)
            if not m:err.append('引經缺（耶x:y）：'+q[:20]);bl.append(['q',q]);continue
            body=q[:m.start()]
            c,v1=int(m.group(1)),int(m.group(2));v2=int(m.group(3) or v1)
            if c!=n:err.append('引經章號不是本章：'+q[:20])
            else:
                seg=norm(''.join(txt[v1-1:v2]))
                for part in re.split('……',body):
                    if norm(part) and norm(part) not in seg:err.append('引經不在 %d:%d–%d：%s'%(c,v1,v2,part[:24]))
            bl.append(['q',q])
        else:
            bl.append(['p',l])
    if not bl or bl[0][0]!='h':err.append('缺標題')
    body=[t for k,t in bl if k!='h']
    chars=sum(len(t) for t in body)
    ps=[t for k,t in bl if k=='p']
    avg=sum(len(t) for t in ps)/max(1,len(ps))
    if not 3600<=chars<=4600:err.append('字數 %d 不在 3600–4600'%chars)
    if avg>20:err.append('段落平均 %.1f 字 >20'%avg)
    if not bl[-1][1].endswith('阿們。'):err.append('末句需「阿們。」')
    if not any('禱告' in t or '讓我們禱告' in t for t in body[-12:]):err.append('結尾缺禱告')
    mn=round(chars/350)
    if err:
        print('第%d章 serm ✗'%n);[print('  -',e) for e in err];return False
    json.dump({'min':mn,'blocks':bl},open(os.path.join(ROOT,'serm/%02d.json'%n),'w',encoding='utf-8'),ensure_ascii=False)
    print('✓ 第%d章 serm 通過：%d 字 %d 分鐘 %d 段 平均 %.1f'%(n,chars,mn,len(bl),avg));return True
if __name__=='__main__':
    sys.exit(0 if all([run(int(x)) for x in sys.argv[1:]]) else 1)
