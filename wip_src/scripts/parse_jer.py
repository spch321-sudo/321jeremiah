import re,sys,json,collections
src=sys.argv[1]
txt=open(src,encoding='utf-8').read()
ch=collections.OrderedDict();cur=None
for line in txt.splitlines():
    m=re.match(r'\\c (\d+)',line)
    if m: cur=int(m.group(1)); ch[cur]={}; continue
    m=re.match(r'\\v (\d+)(?:-(\d+))? ?(.*)',line)
    if m and cur:
        ch[cur][m.group(1)+('-'+m.group(2) if m.group(2) else '')]=m.group(3)
print('chapters',len(ch),'verses',sum(len(v) for v in ch.values()))
print({k:len(v) for k,v in ch.items()})
merged=[(c,v) for c,d in ch.items() for v in d if '-' in v]
print('merged verse lines:',merged)
print('9:1=',ch[9].get('1','')[:30]);print('8:22=',ch[8].get('22','')[:30])
print('33:14-26 present:',[v for v in ch[33] if int(v.split('-')[0])>=14][:3])
