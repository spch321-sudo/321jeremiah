import sys,json,re,threading,http.server,socketserver,os
from playwright.sync_api import sync_playwright
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory='/home/claude/jer/site',**k)
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(('127.0.0.1',8766),Q);threading.Thread(target=srv.serve_forever,daemon=True).start()
errs=[];han={}
with sync_playwright() as p:
    b=p.chromium.launch();c=b.new_context(viewport={'width':430,'height':900});pg=c.new_page()
    pg.on('pageerror',lambda e:errs.append(('pageerror',str(e)[:200])))
    pg.on('console',lambda m:errs.append(('console',m.text[:200])) if m.type=='error' else None)
    pg.on('response',lambda r:errs.append(('404',r.url[-70:])) if r.status==404 else None)
    pg.goto('http://127.0.0.1:8766/en.html');pg.wait_for_timeout(2500)
    print('title',pg.title(),'lang',pg.evaluate("document.documentElement.lang"))
    pg.evaluate("S.set.role='read';save();render()")
    print('fn',pg.evaluate("['speak','fOpen','askXz','mkTap','exportMarks','toggleSC','ttsClear','go'].map(n=>typeof window[n])"))
    T="""()=>{const o=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.parentElement&&['SCRIPT','STYLE'].includes(n.parentElement.tagName))continue;const t=n.nodeValue;if(/[\\u3400-\\u9fff]/.test(t))o.push(t.slice(0,60))}return o}"""
    views=[('today',0,''),('text',0,''),('course',0,''),('tools',0,''),('me',0,''),('tools',0,'tracks'),('tools',0,'issues'),('tools',0,'review'),('tools',0,'map')]
    for n in range(1,53):
        for sub in('card','core','group','serm','lesson','prac','safe'):views.append(('course',n,sub))
    for v in views:
        pg.evaluate(f"go('{v[0]}',{v[1]},'{v[2]}')");pg.wait_for_timeout(15)
        t=pg.evaluate(T)
        if t:han[v]=t
    pg.evaluate("R={tab:'tools',ch:0,sub:'search'};render()")
    print('views',len(views),'views with Han',len(han))
    for k,v in list(han.items())[:8]:print(k,v[:3])
    print('errors',len(errs),errs[:8])
    b.close()
