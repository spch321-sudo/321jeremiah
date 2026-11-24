import json,re,sys,copy
D=json.load(open('build/data.json',encoding='utf-8'))
def check(D):
    E=[];W=[]
    if len(D['ch'])!=52:E.append('ch count')
    tv=sum(len(v) for v in D['txt'].values())
    if tv!=1364:E.append(f'verses {tv}')
    def text(o):
        if isinstance(o,str):yield o
        elif isinstance(o,list):
            for x in o:yield from text(x)
        elif isinstance(o,dict):
            for x in o.values():yield from text(x)
    reader={k:D[k] for k in('ch','blk','serm','lesson','txt')}
    for k,v in reader.items():
        for s in text(v):
            if re.search(r'ISS\d',s):E.append(f'{k}: ISS code visible')
            pass
            if 'Isaiah' in s or '以賽亞' in s and k!='blk' and False:pass
    has={int(i['id'][3:5]) for i in D['issues'] if i['id'][3:5]!='00'}
    for n,v in D['blk'].items():
        for b in v:
            for x in b.values():
                if isinstance(x,str) and re.search(r'見議題|見爭議議題',x) and int(n) not in has:E.append(f'blk{n}: dangling 見議題')
    for n in range(1,53):
        s=str(n);c=D['ch'][n-1]
        if c['n']!=n:E.append(f'ch{n} n')
        if len(c['card'])!=7 or not c['card'][6].startswith('最終整合：'):E.append(f'ch{n} card')
        if len(c['grp'])!=5:E.append(f'ch{n} grp')
        if len(c['prac']['items'])!=5:E.append(f'ch{n} prac')
        if not (6<=len(D['blk'][s])<=22 or len(D['txt'][s])<6):E.append(f'blk{n} count {len(D["blk"][s])}')
        sc=sum(len(x) for b in D['serm'][s]['blocks'] for x in b[1:2] if isinstance(x,str))
        if not 3600<=sc<=5000:E.append(f'serm{n} len {sc}')
        L=D['lesson'][s]
        if sum(1 for b in L['blocks'] if b[0]=='d')!=8:E.append(f'lesson{n} deep')
        if not L['blocks'][1][1].startswith('弟兄姊妹平安'):E.append(f'lesson{n} opening')
        if not 7200<=L['chars']+L['dchars']+L['tchars']<=8600 and not 7200<=L['chars']<=8600:W.append(f'lesson{n} size {L["chars"]}')
        # blk coverage
        last=0
        for b in D['blk'][s]:
            if b['a']!=last+1 and last:E.append(f'blk{n} gap at {b["a"]}')
            last=b['z']
        if last and last!=len(D['txt'][s]):E.append(f'blk{n} end {last}/{len(D["txt"][s])}')
    ops=[len(set(D['lesson'][str(n)]['blocks'][1][1][:30] for n in range(1,53)))]
    if ops[0]<40:E.append(f'lesson openings {ops[0]}')
    for i in D['issues']:
        if len(i['pos'])<2:E.append(i['id']+' pos')
    return E,W
E,W=check(D)
# mutation tests
def mut(f,tag):
    M=copy.deepcopy(D);f(M);e,_=check(M);assert e,'mutation missed: '+tag
mut(lambda M:M['txt']['1'].pop(),'txt');mut(lambda M:M['ch'][0]['card'].pop(),'card')
mut(lambda M:M['blk']['3'][0].__setitem__('exp','ISS03_1'),'iss')
mut(lambda M:M['blk']['49'][0].__setitem__('exp','（見議題）'),'dangling')
mut(lambda M:M['lesson']['2']['blocks'].pop(1),'opening')
mut(lambda M:M['issues'][0].__setitem__('pos',M['issues'][0]['pos'][:1]),'pos')
print('錯誤',len(E),'警告',len(W));[print(x) for x in E+W]
sys.exit(1 if E else 0)
