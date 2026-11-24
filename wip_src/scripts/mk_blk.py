# -*- coding: utf-8 -*-
"""blk 建構器：src/NN.py 的 B 列表 -> blk/NN.json；希伯來文取自WLC，key表逐列驗證；通過才出檔
B 每項: dict(a,z,star,lit,key=[(中,原,音,H號,義)],gram=[段],exp=[段])  段內 **x** -> <strong>
可選 grk_note 無；整段希伯來由 WLC 自動產生。"""
import json,os,sys,re,importlib.util,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from book import *
import wlc
W=wlc.cuv_index(wlc.load())
CANT=re.compile('[֑-֯]')
def pointed(w): return CANT.sub('',w)
def cons(s): return re.sub('[֑-ׇ]','',s).replace('־',' ').strip()
def bold(s):
    s=html.escape(s,quote=False)
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
def he_span(s): # 內文裡的希伯來字串不另包，已在 strong
    return s
def build(n,B):
    err=[];out=[];nxt=1
    maxv=VERSES[n]
    for i,b in enumerate(B,1):
        a,z=b['a'],b['z']
        if a!=nxt:err.append('block%d 起點 %d 應為 %d'%(i,a,nxt))
        if z<a or z>maxv:err.append('block%d 終點 %d 不合'%(i,z))
        nxt=z+1
        if b['star'] not in (0,1,2,3):err.append('block%d star'%i)
        words=[]
        for v in range(a,z+1):
            ws=W.get((n,v))
            if not ws:err.append('WLC 缺 %d:%d'%(n,v));continue
            words.append(' '.join(pointed(w) for l,w in ws)+'׃')
        heb=' '.join(words)
        grk='<blockquote dir="rtl" lang="he"><p>%s</p></blockquote>'%heb
        rng=[x for v in range(a,z+1) for x in W.get((n,v),[])]
        rc=cons(' '.join(w for l,w in rng)); rs={s for l,w in rng for s in wlc.strongs(l)}
        rows=[]
        def hebfor(num,occ=1):
            c=0
            for v in range(a,z+1):
                for l,w in W.get((n,v),[]):
                    if num in wlc.strongs(l):
                        c+=1
                        if c==occ:return pointed(w)
            return None
        for r in b['key']:
            if len(r)==4:
                zh,hs,tr,mean=r
                nums=re.findall(r'H(\d+)(?:#(\d+))?',hs)
                hl=[hebfor(x,int(o or 1)) for x,o in nums]
                if not nums or None in hl:err.append('block%d key Strong 不在範圍：%s'%(i,hs));continue
                he=' '.join(hl);st='／'.join('H'+x for x,o in nums)
                r=(zh,he,tr,st,mean)
            zh,he,tr,st,mean=r
            if not re.search('[ְ-ּ]',he):err.append('block%d key 原文缺母音點:%s'%(i,he))
            hc=cons(he)
            if hc not in rc:err.append('block%d key 原文不在 %d:%d-%d：%s'%(i,n,a,z,he))
            nums=re.findall(r'H(\d+)',st)
            if not nums or not any(x in rs for x in nums):err.append('block%d key Strong 不在範圍：%s %s'%(i,he,st))
            rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(zh,he,html.escape(tr,quote=False),st,mean))
        if not (2<=len(b['key'])<=7):err.append('block%d key 列數 %d'%(i,len(b['key'])))
        key='<table><thead><tr class="header"><th>中文</th><th>原文</th><th>音譯</th><th>Strong\'s</th><th>意義</th></tr></thead><tbody>%s</tbody></table>'%''.join(rows)
        lit=b['lit']
        if not(lit.startswith('「') and lit.endswith('」')):err.append('block%d lit 需以「」包'%i)
        def fill(t):
            def f(m):
                h=hebfor(m.group(1),int(m.group(2) or 1))
                if h is None:err.append('block%d {H%s} 不在範圍'%(i,m.group(1)));return '?'
                return '<strong>%s</strong>'%h
            t=re.sub(r'\{H(\d+)(?:#(\d+))?\}','\x00\\1|\\2\x00',t) if False else t
            return re.sub(r'\{H(\d+)(?:#(\d+))?\}',f,t)
        gram=''.join('<p>%s</p>'%fill(bold(p)) for p in b['gram'])
        exp=''.join('<p>%s</p>'%fill(bold(p)) for p in b['exp'])
        if len(b['exp'])<2:err.append('block%d exp 至少兩段'%i)
        if not b['gram']:err.append('block%d gram 空'%i)
        out.append(dict(a=a,z=z,star=b['star'],grk=grk,lit='<blockquote><p>%s</p></blockquote>'%html.escape(lit,quote=False),key=key,gram=gram,exp=exp))
    if nxt!=maxv+1:err.append('未覆蓋到 %d 節（止於 %d）'%(maxv,nxt-1))
    if not(6<=len(B)<=22):err.append('區塊數 %d 不在 6–22'%len(B))
    return out,err
def run(n):
    p=os.path.join(ROOT,'blk/src/%02d.py'%n)
    spec=importlib.util.spec_from_file_location('s%d'%n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    out,err=build(n,m.B)
    if err:
        print('第%d章 ✗'%n);[print('  -',e) for e in err];return False
    json.dump(out,open(os.path.join(ROOT,'blk/%02d.json'%n),'w',encoding='utf-8'),ensure_ascii=False)
    ec=sum(len(re.sub('<[^>]+>','',b['exp'])) for b in out)
    print('✓ 第%d章 blk 通過：%d 區塊，解經 %d 字'%(n,len(out),ec));return True
if __name__=='__main__':
    ok=all([run(int(x)) for x in sys.argv[1:]])
    sys.exit(0 if ok else 1)
