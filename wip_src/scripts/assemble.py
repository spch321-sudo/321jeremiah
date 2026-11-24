import json,glob,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=lambda p:json.load(open(os.path.join(R,p),encoding='utf-8'))
bp=L('blueprint.json')
N=52
ch=[];txt={};blk={};serm={};lesson={}
for n in range(1,N+1):
    k=f'{n:02d}'
    c=L(f'ch/{k}.json'); assert c['n']==n; ch.append(c)
    txt[str(n)]=L(f'txt/{k}.json'); blk[str(n)]=L(f'blk/{k}.json')
    serm[str(n)]=L(f'serm/{k}.json'); lesson[str(n)]=L(f'lesson/{k}.json')
iss=[i for i in bp['issues'] if i['id'].startswith('ISS00_')]
for f in sorted(glob.glob(os.path.join(R,'iss/*.json'))): iss+=json.load(open(f,encoding='utf-8'))
ids=[i['id'] for i in iss]; assert len(ids)==len(set(ids))
D=dict(ch=ch,txt=txt,blk=blk,serm=serm,issues=iss,terrain=bp['terrain'],tracks=bp['tracks'],lesson=lesson)
os.makedirs(os.path.join(R,'build'),exist_ok=True)
json.dump(D,open(os.path.join(R,'build/data.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('ok',{k:len(v) for k,v in D.items()},os.path.getsize(os.path.join(R,'build/data.json')))
