import json,re,os,sys,hashlib,shutil,subprocess
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,R+'/scripts')
import mk_scmap
from tc2sc import icu
subprocess.check_call([sys.executable,'-I',R+'/scripts/port_app.py'],stdout=subprocess.DEVNULL)
shell=open(R+'/build/shell_jer_tc.html',encoding='utf-8').read()
data=open(R+'/build/data.json',encoding='utf-8').read().replace('</','<\\/')
page=shell.replace('@@DATA@@',data)
SC_RE=re.compile(r'<script id="SCMAP" type="application/json">.*?</script>',re.S)
ISA='/home/claude/spch321-sudo/321isaiah/'
extra=[open(ISA+f,encoding='utf-8').read() for f in('xz2.js','coread.js')]
pieces=mk_scmap.pieces_from(page,extra)
print('pieces',len(pieces))
sc=mk_scmap.finalize(pieces)
bad,idem=mk_scmap.check_js_equiv(sc,pieces)
print('逐字表',len(sc['m'][0]),'詞組',len(sc['p']),'不符',bad,'非冪等',idem)
assert bad==0
page=SC_RE.sub(lambda m:'<script id="SCMAP" type="application/json">'+json.dumps(sc,ensure_ascii=False,separators=(',',':'))+'</script>',page,1)
S=R+'/site';shutil.rmtree(S,ignore_errors=True);os.makedirs(S)
open(S+'/index.html','w',encoding='utf-8').write(page)
# 簡體：head 轉簡 + SCBOOT
head_end=page.index('<style>')
head=page[:head_end];rest=page[head_end:]
sch=re.sub(r'(content="|<title>)([^"<]*)',lambda m:m.group(1)+icu(m.group(2)),head)
boot='''<script id="SCBOOT">/* 简体页：一律以简体开启（保留其他存档） */
try { var K='r321.jer.v1', o=JSON.parse(localStorage.getItem(K)||'null'); if(!o||typeof o!=='object') o={ v:1, last:1, steps:{}, notes:{}, lnote:{}, prac:{}, mem:{}, set:{ fs:1, grk:1, dark:0, role:'' }, seen:{} }; o.set=o.set||{}; o.set.sc=1; localStorage.setItem(K,JSON.stringify(o)); } catch(e){}
</script>
'''
k=rest.index('<script id="DATA"')
open(S+'/sc.html','w',encoding='utf-8').write(sch+rest[:k]+boot+rest[k:])
ISA='/home/claude/spch321-sudo/321isaiah/'
for f in('xz2.js','coread.js','peerjs.min.js','404.html','.nojekyll'):shutil.copy(ISA+f,S+'/'+f)
for z in(32,64,120,152,167,180,192,512,1024):shutil.copy(f'{R}/assets/icons/icon-{z}.png',f'{S}/icon-{z}.png')
shutil.copy(R+'/assets/icons/favicon.ico',S+'/favicon.ico')
ver='耶利米書-'+hashlib.sha1(page.encode()).hexdigest()[:12]
mf=json.load(open(ISA+'manifest.webmanifest',encoding='utf-8'))
mf.update(name='耶利米書講義',short_name='耶利米書講義',description='耶利米書全書五十二章：逐節原文解經、講章逐字稿、教學講章、321 生命應用。',id='/321jeremiah/')
json.dump(mf,open(S+'/manifest.webmanifest','w',encoding='utf-8'),ensure_ascii=False,indent=2)
sw=open(ISA+'sw.js',encoding='utf-8').read()
sw=re.sub(r"const V = '[^']*';","const V = '%s';"%ver,sw);sw=sw.replace("const PFX = '以賽亞書-';","const PFX = '耶利米書-';").replace('321以賽亞書講義','321耶利米書講義')
E=json.load(open(R+'/build/data_en.json',encoding='utf-8'))
sh=open(R+'/build/shell_jer_en.html',encoding='utf-8').read()
assert sh.count('@@DATA@@')==1
dj=json.dumps(E,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
for a_,b_ in [('{"n":21,"t":"以賽亞書"','{"n":21,"t":"傳道書"'),('["以賽亞書",21]','["傳道書",21]'),("const BOOK = T('以賽亞書'","const BOOK = T('耶利米書'"),("T('以賽亞書' + n","T('耶利米書' + n"),("目前讀到：以賽亞書 第","目前讀到：耶利米書 第"),("目前读到：以赛亚书 第","目前读到：耶利米书 第")]:
    assert sh.count(a_)==1,a_
    sh=sh.replace(a_,b_)
enp=sh.replace('@@DATA@@',dj)
import build_en
assert not build_en.han_left(E),'Han in English DATA'
open(S+'/en.html','w',encoding='utf-8').write(enp)
me=json.load(open(ISA+'manifest-en.webmanifest',encoding='utf-8'))
me.update(name='Jeremiah Study Notes',short_name='Jeremiah Notes',description='Jeremiah, all fifty-two chapters: verse-by-verse exposition from the original, sermon manuscripts, teaching lessons and 321 life application.',id='/321jeremiah/en.html')
json.dump(me,open(S+'/manifest-en.webmanifest','w',encoding='utf-8'),ensure_ascii=False,indent=2)
has_en=True
shell_list=['./','./index.html','./sc.html']+(['./en.html','./manifest-en.webmanifest'] if has_en else [])+['./manifest.webmanifest']+[f'./icon-{z}.png' for z in(192,512,180,167,152,120,64,32)]+['./favicon.ico','./xz2.js','./coread.js','./peerjs.min.js']
sw=re.sub(r'const SHELL = \[.*?\];','const SHELL = '+json.dumps(shell_list)+';',sw,flags=re.S)
assert '以賽亞' not in sw and 'Isaiah' not in sw
open(S+'/sw.js','w',encoding='utf-8').write(sw)
json.dump({'v':ver},open(S+'/version.json','w',encoding='utf-8'),ensure_ascii=False)
open(S+'/README.md','w',encoding='utf-8').write('國度321空中團契《321聖經講義》耶利米書（五十二章、1,364 節），版本 v1.0。\n\n- 繁體中文：`index.html`（完整）\n- 简体中文：`sc.html`（完整；同一支 App 以简体开启，内嵌繁简对照表一键切换）\n- English：`en.html`（完整）\n\n發佈網址：https://spch321-sudo.github.io/321jeremiah/\n\n離線可用的 PWA；iPhone 請先刪除舊的主畫面捷徑再重新「加入主畫面」。\n')
print('site ok',ver,{f:os.path.getsize(S+'/'+f) for f in('index.html','sc.html')})
