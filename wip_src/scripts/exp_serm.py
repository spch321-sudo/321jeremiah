import re,json,sys
n=int(sys.argv[1])
raw=open('../serm/src/%02d.raw'%n,encoding='utf-8').read()
txt=json.load(open('../txt/%02d.json'%n))
s=re.sub(r'@@Q(\d+)',lambda m:'> %s（耶%d:%s）'%(txt[int(m.group(1))-1],n,m.group(1)),raw)
open('../serm/src/%02d.txt'%n,'w',encoding='utf-8').write(s)
