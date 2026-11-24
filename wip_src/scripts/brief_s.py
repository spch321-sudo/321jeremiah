# -*- coding: utf-8 -*-
"""精簡素材：中文經文＋內容詞（無母音希伯來字根形＋Strong's號），供選字用"""
import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from book import *
import wlc
W=wlc.cuv_index(wlc.load())
STOP={'3068','834','3588','413','5921','854','853','3808','408','559','1961','2009','4480','3605','5002','3069','136','589','595','859','3541','1992','1931','2088','2063','5973','935','3212','5414','6213','1121','376','935','1696','3027','4100'}
def show(n):
    txt=json.load(open(os.path.join(ROOT,'txt/%02d.json'%n),encoding='utf-8'))
    for v,t in enumerate(txt,1):
        ws=[]
        for l,w in W.get((n,v),[]):
            ss=wlc.strongs(l)
            if not ss or ss[-1] in STOP:continue
            ws.append('%s%s'%(re.sub('[֑-ׇ]','',w),ss[-1]))
        print('%d:%d %s'%(n,v,t));print('   '+' '.join(ws))
if __name__=='__main__':
    for x in sys.argv[1:]:show(int(x))
