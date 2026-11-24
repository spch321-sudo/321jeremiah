# -*- coding: utf-8 -*-
"""素材總表：每章經文(和合)＋希伯來文逐字(含Strong's)＋藍圖段落，供寫作唯一素材來源"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from book import *
import wlc
W=wlc.cuv_index(wlc.load())
B=json.load(open(os.path.join(ROOT,'blueprint.json'),encoding='utf-8'))
os.makedirs(os.path.join(ROOT,'build/brief'),exist_ok=True)
for n in range(1,CHAPTERS+1):
    txt=json.load(open(os.path.join(ROOT,'txt/%02d.json'%n),encoding='utf-8'))
    ch=B['ch'][str(n)] if isinstance(B['ch'],dict) else B['ch'][n-1]
    o=['# 耶利米書 %d 章：%s（%s・%s級・%s）'%(n,ch['t'],ch['sub'],ch['lv'],ch['arc']),'','## 藍圖段落']
    for r,t in ch['sec']:o.append('- %s %s'%(r,t))
    o+=['','## 講章三點']
    for p in ch['serm']['pts']:o.append('- %s｜%s｜「%s」'%(p[0],p[1],p[2]))
    o+=['','## 逐節（和合本＋WLC逐字）']
    for v,t in enumerate(txt,1):
        ws=W.get((n,v),[])
        o.append('%d:%d %s'%(n,v,t))
        o.append('   ⟨%s⟩'%' '.join('%s[%s]'%(w,'/'.join('H'+s for s in wlc.strongs(l))) for l,w in ws))
    open(os.path.join(ROOT,'build/brief/%02d.md'%n),'w',encoding='utf-8').write('\n'.join(o))
print('✓ brief 52')
