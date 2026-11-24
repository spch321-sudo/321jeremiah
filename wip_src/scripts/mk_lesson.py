# -*- coding: utf-8 -*-
"""lesson 建構器：lesson/src/NN.py (TITLE, TEXT, HUA) -> lesson/NN.json（Isaiah 同 schema），不合規不出檔"""
import json,os,sys,re,importlib.util
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from book import *
H=re.compile('[一-鿿]')
def han(s):return len(H.findall(s))
PUN=re.compile(r'[\s，。、；：？！「」『』（）()—…·‧－\-　“”‘’]')
def norm(s):return PUN.sub('',s)
ALLV=None
def allverses():
    global ALLV
    if ALLV is None:
        ALLV=''.join(norm(''.join(json.load(open(os.path.join(ROOT,'txt/%02d.json'%i),encoding='utf-8')))) for i in range(1,CHAPTERS+1))
    return ALLV
def grams(s,k=8):return {s[i:i+k] for i in range(len(s)-k+1)}
STEPS=['看見自己','聽神說話','想通關卡','說出口','走一步']
def run(n):
    p=os.path.join(ROOT,'lesson/src/%02d.py'%n)
    sp=importlib.util.spec_from_file_location('l%d'%n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    err=[];bl=[];sec=None;secs=[]
    for raw in m.TEXT.strip().split('\n'):
        l=raw.strip()
        if not l:continue
        if l.startswith('## '):
            bl.append(['h',l[3:].strip()]);secs.append(l[3:].strip());sec=len(secs)
        elif l.startswith('?? '):
            q,a=[x.strip() for x in l[3:].split('｜',1)]
            bl.append(['d',[q,a]])
        else:bl.append(['p',l])
    # 結構
    hs=[b[1] for b in bl if b[0]=='h']
    if len(hs)!=10:err.append('前十節需 10 個標題，實有 %d'%len(hs))
    else:
        ords='一二三四五六七八九十'
        for i,h in enumerate(hs):
            if not h.startswith(ords[i]+'、'):err.append('標題序號 %s'%h)
        if hs[4]!='五、幾個必須認得的偏差':err.append('第五節標題')
        if hs[5]!='六、兩個華人處境的真實問題':err.append('第六節標題')
        if not hs[6].startswith('七、活出321——'):err.append('第七節標題')
        if not hs[7].startswith('八、四種心，'):err.append('第八節標題')
        if hs[8]!='九、這一週，你可以做的幾件事':err.append('第九節標題')
        if hs[9]!='十、結語':err.append('第十節標題')
        if not any('原文' in h for h in hs[:4]):err.append('一至四節須有一節標題含「原文」')
    if not re.fullmatch(r'.+——[^、]+、[^、]+、[^、]+',m.TITLE):err.append('標題格式 主標題——副標題三詞 ：'+m.TITLE)
    # 分節取段
    S={};cur=None
    for b in bl:
        if b[0]=='h':cur=b[1][0];S[cur]=[]
        else:S[cur].append(b)
    P=lambda k:[x[1] for x in S.get(k,[]) if x[0]=='p']
    first=[x for x in bl if x[0]=='p'][0][1]
    if not first.startswith('弟兄姊妹平安'):err.append('首段需以「弟兄姊妹平安」起頭')
    p5=P('五')
    if len(p5)!=5 or any(not p5[i].startswith('第%s個'%'一二三四五'[i]) for i in range(len(p5))):err.append('五節需 5 段「第一個…第五個」')
    p6=P('六')
    if len(p6)!=2 or not p6[0].startswith('第一個問題') or not p6[1].startswith('第二個問題'):err.append('六節需 2 段「第一個問題／第二個問題」')
    t7=''.join(P('七'))
    for kw,lab in [('榜樣','耶穌是我的榜樣'),('準則','聖經是我的準則'),('引導','聖靈是我的引導'),('作王','讓耶穌作王'),('榮耀','得著一切的榮耀'),('屬神的體系','建立屬神的體系')]:
        if kw not in t7:err.append('七節缺「%s」'%lab)
    p8=P('八')
    if len(p8)!=4 or not all(k in p8[i] for i,k in enumerate(['驕傲','恐懼','羞恥','受傷'])):err.append('八節需 4 段：驕傲、恐懼、羞恥、受傷')
    p9=P('九')
    if len(p9)!=9 or any(not p9[i].startswith('第%s，'%'一二三四五'[i]) for i in range(min(5,len(p9)))) or any(not x.startswith('我宣告：') for x in p9[5:]):err.append('九節需 5 件事（第一，…第五，）＋4 句「我宣告：」')
    p10=P('十')
    if len(p10)<3 or '焦點' not in p10[-2] or not p10[-1].endswith('奉主耶穌基督的名禱告，阿們。'):err.append('十節：倒數第二段含「焦點」，末句「奉主耶穌基督的名禱告，阿們。」')
    # 想更深
    deeps=[b for b in bl if b[0]=='d'];dh=0
    if len(deeps)!=8:err.append('想更深需 8 則，實 %d'%len(deeps))
    where=set()
    cur=None
    for b in bl:
        if b[0]=='h':cur=b[1][0]
        if b[0]=='d':where.add(cur)
    if len(where)<5:err.append('想更深需分散在 5 節以上，實 %d'%len(where))
    for q,a in [b[1] for b in deeps]:
        if not q.endswith('？') or han(q)<10:err.append('想更深問句：'+q[:16])
        if not 150<=han(a)<=460:err.append('想更深回答字數 %d：%s'%(han(a),q[:12]))
    # 三個化
    H_=m.HUA
    def chk(k,cnt):
        if len(H_[k]['qs'])!=cnt:err.append('%s 題數 %d≠%d'%(k,len(H_[k]['qs']),cnt))
        if not H_[k].get('aim') or not H_[k].get('note'):err.append(k+' 缺 aim/note')
        if not any(s=='★★★' for s,_ in H_[k]['qs']):err.append(k+' 缺 ★★★')
        for s,t in H_[k]['qs']:
            if s not in('★','★★','★★★'):err.append(k+' 星級 '+s)
    chk('h1',4);chk('h2',5);chk('h3',5)
    for i,(s,t) in enumerate(H_['h2']['qs']):
        if not t.startswith(STEPS[i]+'：'):err.append('第二化第%d題需以「%s：」起頭'%(i+1,STEPS[i]))
    if not any('920' in t for s,t in H_['h3']['qs']):err.append('第三化缺 920 題')
    if '【必做】' not in H_['h3']['qs'][-1][1] or H_['h3']['qs'][-1][0]!='★★★':err.append('第三化最後一題需 ★★★ 且含【必做】')
    for k in('h1','h3'):
        if '不追問' not in H_[k]['note']:err.append(k+' note 需含「不追問」等關懷提醒')
    if len(H_['close'])!=2:err.append('收尾需 2 段')
    # 組裝第十一節
    tri=[['h','十一、小組討論分享：三個化'],
     ['m','帶領說明：今天這一課，我們用三個化來走一遍：先把話放進自己心裡（內化），再一起想通、說出口、走一步（消化），最後把這一課帶到人面前（轉化）。'],
     ['m','優先順序標示：★★★＝最優先，時間不足時每一化至少討論這一題；★★＝次優先；★＝時間充裕再討論。標【必做】的繁殖任務不可省略，可帶回家完成。']]
    num=0
    def addq(qs):
        nonlocal num
        for s,t in qs:
            num+=1;tri.append(['n','%d. %s %s'%(num,s,t)])
    tri+= [['s','第一化　內化（約20分鐘）'],['m','目的：'+H_['h1']['aim']]];addq(H_['h1']['qs']);tri.append(['m','帶領提醒：'+H_['h1']['note']])
    tri+= [['s','第二化　消化（約35分鐘·主軸）'],['m','目的：'+H_['h2']['aim']]]
    for i,(s,t) in enumerate(H_['h2']['qs']):
        tri.append(['t','【%s】%s'%('看聽想講行'[i],STEPS[i])]);addq([(s,t)])
    tri.append(['m','帶領提醒：'+H_['h2']['note']])
    tri+= [['s','第三化　轉化（約25分鐘）'],['m','目的：'+H_['h3']['aim']]];addq(H_['h3']['qs']);tri.append(['m','帶領提醒：'+H_['h3']['note']])
    tri+= [['s','收尾（5分鐘）'],['p',H_['close'][0]],['p',H_['close'][1]]]
    # 字數
    chars=sum(han(b[1]) for b in bl if b[0]=='p')
    dchars=sum(han(b[1][0])+han(b[1][1]) for b in deeps)
    tchars=sum(han(b[1]) for b in tri if b[0]!='h')
    if not 4700<=chars<=5700:err.append('本體 %d 字不在 4700–5700'%chars)
    if not 7200<=chars+dchars+tchars<=8400:err.append('全課 %d 字不在 7200–8400'%(chars+dchars+tchars))
    # 經文引用逐字
    allv=allverses()
    for b in bl:
        if b[0]!='p':continue
        for q in re.findall(r'「([^」]{10,})」',b[1]):
            for part in q.split('……'):
                nq=norm(part)
                if len(nq)>=8 and grams(nq)&grams(allv) and nq not in allv:
                    err.append('引用疑非逐字和合本：'+part[:30])
    if err:
        print('第%d課 ✗'%n);[print('  -',e) for e in err[:25]];return False
    blocks=bl+tri
    out=dict(no=n,vol='《321耶利米書講義》第%d課·耶利米書第%d章'%(n,n),title=m.TITLE,chars=chars,min=60,deep=8,dchars=dchars,tchars=tchars,blocks=blocks)
    json.dump(out,open(os.path.join(ROOT,'lesson/%02d.json'%n),'w',encoding='utf-8'),ensure_ascii=False)
    print('✓ 第%d課 通過：本體 %d＋深 %d＋三個化 %d＝%d'%(n,chars,dchars,tchars,chars+dchars+tchars));return True
if __name__=='__main__':
    sys.exit(0 if all([run(int(x)) for x in sys.argv[1:]]) else 1)
