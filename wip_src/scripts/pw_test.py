import sys,json,re,asyncio,threading,http.server,socketserver,os,functools
sys.path.insert(0,'/home/claude/jer/scripts')
from tc2sc import icu
from playwright.sync_api import sync_playwright
os.chdir('/home/claude/jer/site')
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory='/home/claude/jer/site',**k)
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(('127.0.0.1',8765),Q);threading.Thread(target=srv.serve_forever,daemon=True).start()
errs=[]
def run(page_name,sc):
    with sync_playwright() as p:
        b=p.chromium.launch();c=b.new_context(viewport={'width':430,'height':900});pg=c.new_page()
        pg.on('pageerror',lambda e:errs.append((page_name,'pageerror',str(e)[:200])))
        pg.on('console',lambda m:errs.append((page_name,'console',m.text[:200])) if m.type=='error' else None)
        pg.on('requestfailed',lambda r:errs.append((page_name,'reqfail',r.url[-60:])) if '8765' in r.url else None)
        pg.on('response',lambda r:errs.append((page_name,'404',r.url[-70:])) if r.status==404 else None)
        pg.goto('http://127.0.0.1:8765/'+page_name);pg.wait_for_timeout(2500)
        pg.evaluate("S.set.role='read';save();render()")
        fn=pg.evaluate("['speak','fOpen','askXz','mkTap','exportMarks','toggleSC','ttsClear','go'].map(n=>typeof window[n])")
        print(page_name,'fn',fn)
        def texts():
            return pg.evaluate("""()=>{const o=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.parentElement&&['SCRIPT','STYLE'].includes(n.parentElement.tagName))continue;const t=n.nodeValue;if(/[\\u4e00-\\u9fff]/.test(t))o.push(t)}return o}""")
        res={}
        views=[('today',0,''),('text',0,''),('course',0,''),('tools',0,''),('me',0,''),('tools',0,'tracks'),('tools',0,'issues'),('tools',0,'review'),('tools',0,'map'),('tools',0,'safeall'),('tools',0,'search'),('me',0,'marks')]
        for n in range(1,53):
            for sub in('card','core','group','serm','lesson','prac','safe'):views.append(('course',n,sub))
        for v in views:
            pg.evaluate(f"go('{v[0]}',{v[1]},'{v[2]}')" if v[2] not in('safeall','search','marks') else f"R={{tab:'{v[0]}',ch:0,sub:'{v[2]}'}};render()")
            pg.wait_for_timeout(15)
            res[v]=texts()
        b.close();return res
tc=run('index.html',0)
sc=run('sc.html',1)
bad=0
for v in tc:
    a=[icu(t) for t in tc[v] if t.strip() not in('繁','简')];b=[t for t in sc[v] if t.strip() not in('繁','简')]
    if a!=b:
        bad+=1
        if bad<6:
            for x,y in zip(a,b):
                if x!=y:print('DIFF',v,repr(x[:60]),repr(y[:60]));break
            else:print('LEN',v,len(a),len(b))
print('views',len(tc),'sc不符',bad,'錯誤',len(errs));[print(e) for e in errs[:15]]
