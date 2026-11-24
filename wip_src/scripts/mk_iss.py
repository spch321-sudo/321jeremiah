# -*- coding: utf-8 -*-
"""議題建構器：iss/src/NN.py 的 I(list of dict t,r,why,pos,say,care) -> iss/NN.json"""
import json,os,sys,re,importlib.util
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from book import *
def run(n):
    p=os.path.join(ROOT,'iss/src/%02d.py'%n)
    sp=importlib.util.spec_from_file_location('i%d'%n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    out=[];err=[]
    for k,x in enumerate(m.I,1):
        if not re.fullmatch(r'\d+:\d+--\d+',x['r']):err.append('r 格式 '+x['r'])
        if len(x['pos'])<2:err.append('pos 至少 2：'+x['t'][:12])
        for q in x['pos']:
            if len(q)!=3 or not q[0] or not q[2]:err.append('pos 項格式')
        for f in('why','say','care'):
            if len(x[f])<20:err.append(f+' 過短：'+x['t'][:12])
        if re.search(r'ISS\d',x['why']+x['say']+x['care']):err.append('讀者可見文字不可含議題代號')
        out.append(dict(id='ISS%02d_%d'%(n,k),t=x['t'],r=x['r'],ch=x.get('ch',[n]),why=x['why'],pos=x['pos'],con=[],say=x['say'],care=x['care']))
    if err:
        print('第%d章 議題 ✗'%n);[print('  -',e) for e in err];return False
    json.dump(out,open(os.path.join(ROOT,'iss/%02d.json'%n),'w',encoding='utf-8'),ensure_ascii=False)
    print('✓ 第%d章 議題 通過：%d 條'%(n,len(out)));return True
if __name__=='__main__':
    sys.exit(0 if all([run(int(x)) for x in sys.argv[1:]]) else 1)
