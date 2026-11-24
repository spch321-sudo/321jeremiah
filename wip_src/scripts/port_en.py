"""以賽亞書英文外殼 → 耶利米書英文外殼（DATA 佔位 @@DATA@@）。每項替換都要找到。"""
import re,json,os
R='/home/claude/jer'
s=open(R+'/ref/shell_en.html',encoding='utf-8').read()
def rep(a,b,n=None):
    global s
    c=s.count(a);assert c>0 and (n is None or c==n),f'替換失敗 {a[:50]!r} 找到 {c}';s=s.replace(a,b);print('✓',c,a[:40].replace('\n',' '))
ARC=[["Call",1,1,"Call: the call — before I formed you I knew you; the almond branch and the boiling pot; uproot, tear down, build, plant"],
["Accusation",2,10,"Accusation: accusation and the call to return — forsaking the fountain of living waters; return, faithless Israel; disaster from the north and a broken heart; the deceptive temple, boast in Yahweh alone"],
["Covenant",11,20,"Covenant: covenant, confessions, and the potter — the prophet’s weeping and complaint, why the wicked prosper, if you return; the potter’s house, the deceitful heart, fire in the bones"],
["Kings",21,29,"Kings: kings, prophets, and the exiles — the way of life and the way of death, the righteous Branch and false prophets, two baskets of figs; the yoke, Hananiah, the letter to the exiles"],
["Consolation",30,33,"Consolation: the book of consolation — the time of Jacob’s trouble, the new covenant written on the heart, buying the field, call to me and I will answer"],
["Fall",34,45,"Fall: before and after the city falls — the betrayed covenant, the Rechabites, the scroll burned and written again, the cistern, the fall of Jerusalem, taken to Egypt, Baruch"],
["Nations",46,51,"Nations: the nations and Babylon — Egypt, Philistia, Moab, Ammon, Edom, the judgment of Babylon; every nation stands under one King"],
["Appendix",52,52,"Appendix: the account of the fall of the city, and the release of Jehoiachin"]]
i=s.index('const ARCS = [');j=s.index('/* seven movements: [word, from, to, note] */',i)+len('/* seven movements: [word, from, to, note] */')
s=s[:i]+'const ARCS = '+json.dumps(ARC,ensure_ascii=False)+';   /* eight movements: [word, from, to, note] */'+s[j:];print('✓ ARCS')
i=s.index("if (R.sub === 'map') return `");j=s.index('const dl = due().length',i)
MAP='''if (R.sub === 'map') return `<div class="sect"><p class="eyebrow">Whole-Book Terrain Map</p>
    <h2 class="big">From uprooting and tearing down, to building and planting.</h2>
    <p class="sm muted" style="margin:-6px 0 12px">In eight movements the whole book follows one line: God will uproot and tear down in order to build and plant; the prophet stands between judgment and hope and speaks through tears; and in the end God writes the new covenant on the human heart.</p>${terrain(S.last)}
    <div class="card"><p style="margin:0 0 10px"><b>Call</b> (chapter 1)　<b>1:5</b> I knew you　→　<b>1:10</b> uproot, tear down, build, plant　→　<b>1:12</b> the almond branch</p>
    <p style="margin:0 0 10px"><b>Accusation</b> (2–10)　<b>2:13</b> two evils　→　<b>3:22</b> return　→　<b>7:4</b> the deceptive temple　→　<b>9:24</b> let the one who boasts boast in this</p>
    <p style="margin:0 0 10px"><b>Covenant</b> (11–20)　<b>12:1</b> why the wicked prosper　→　<b>15:19</b> if you return　→　<b>18:6</b> the potter’s house　→　<b>20:9</b> like fire in my bones</p>
    <p style="margin:0 0 10px"><b>Kings</b> (21–29)　<b>21:8</b> the way of life and the way of death　→　<b>23:5</b> the righteous Branch　→　<b>24:7</b> a heart to know me　→　<b>29:7</b> seek the peace of the city</p>
    <p style="margin:0 0 10px"><b>Consolation</b> (30–33)　<b>30:3</b> I will bring them back　→　<b>31:31</b> the new covenant　→　<b>32:15</b> buying the field　→　<b>33:3</b> call to me</p>
    <p style="margin:0 0 10px"><b>Fall</b> (34–45)　<b>36:23</b> the scroll burned　→　<b>38:6</b> the muddy cistern　→　<b>39:8</b> the city falls　→　<b>45:5</b> Baruch</p>
    <p style="margin:0 0 10px"><b>Nations</b> (46–51)　<b>46:28</b> do not be afraid　→　<b>50:34</b> their Redeemer is strong　→　<b>51:64</b> Babylon will sink</p>
    <p style="margin:0"><b>Appendix</b> (52)　<b>52:31</b> Jehoiachin released</p></div>
    <div class="card"><p class="eyebrow">The book’s axis · six turning points</p>
    <table><tr><th>Turning point</th><th>Text</th></tr>
    <tr><td><b>① The call: before I formed you I knew you</b></td><td>1:5</td></tr><tr><td><b>② The deceptive temple: religious symbols cannot replace obedience</b></td><td>7:4</td></tr><tr><td><b>③ The prophet’s weeping and complaint: telling God the truth</b></td><td>12:1; 20:9</td></tr><tr><td><b>④ How the exiles live: seek the peace of the city</b></td><td>29:7, 11</td></tr><tr><td><b>⑤ The new covenant: written on their hearts</b></td><td>31:31–34</td></tr><tr><td><b>⑥ The field and the scroll: God’s word cannot be burned</b></td><td>32:15; 36:32</td></tr></table></div>`;
  '''
s=s[:i]+MAP+s[j:];print('✓ MAP')
i=s.index("    '3. Disputes are not adjudicated:");j=s.index("\n",i)
s=s[:i]+"""    '3. Disputes are not adjudicated: on the composition of the book and its two texts (the Hebrew text and the Septuagint), the prophet\\'s confessions and the cursing of his birthday (chapters 11–20), "do not pray for this people," the use of 29:11, the new covenant of chapter 31 and the house of Israel, the seventy years, God\\'s "relenting," and the prophet and politics (chapters 27–28 and "false prophets") — always state first what all sides agree on, then present the main positions, and only then the position of these notes; never adjudicate, and never make political judgments.',"""+s[j:]
i=s.index("    'Do not judge people, do not get entangled");j=s.index("\n    'If they come about their own sin",i)
s=s[:i]+"""    'Do not judge people, do not get entangled in politics, do not pass verdicts on particular churches or people. Jeremiah is not a timetable and not a footnote to modern politics — its focus is: God will uproot and tear down in order to build and plant; the prophet speaks through tears; in the end God writes the new covenant on the human heart; let Jesus reign as King, and let trust in temple and king become a heart made new.',
    'The prophet\\'s confessions and Jeremiah 20:14–18: never present "I wish I had not been born" as a prayer to imitate, and never answer someone in pain with "just have faith"; stay with them and listen first, then gently point to the Lord who wept over Jerusalem, and encourage them to reach out to people they trust and their pastor.',
    'The end times and prophecy: do not count days, do not draw timetables (including the seventy years), do not identify any modern nation or person as a fulfilment; what calls people to repent, return and seek the peace of the city where they live is the original meaning.',
    'The marriage and sexual imagery of chapters 2, 3 and 13: speak first of God\\'s grief, never enlarge the picture, and never tell a wounded person "this picture is about you"; protect those present who have been hurt or whose marriages have broken.',
    'Despair and self-harm: if someone says life feels meaningless or they want to disappear, stay with them gently and take it seriously; never say "just have faith" and never answer with passages of judgment; encourage them to contact someone they trust and their pastor right away. In Taiwan they can call the 1925 mental-health hotline, or 119 in an emergency; elsewhere, their local crisis line and emergency number.',
    '"Do not pray for this people" (7:16 and elsewhere): this was a word for one generation at one moment; never use it to stop anyone from praying for anyone. The same book says God will build and plant and will write the new covenant on the heart — never preach only half of it.',"""+s[j:]
print('✓ XZ rules')
rep('Isaiah chapter three, verse eleven','Jeremiah chapter three, verse twenty-two',1)
rep("From the despised Holy One","From the despised Holy One") if False else None
rep("const KEY = 'r321.isa.v1.en';","const KEY = 'r321.jer.v1.en';",1)
rep("var K='r321.isa.v1'","var K='r321.jer.v1'",1)
rep("const LASTCH = 66;","const LASTCH = 52;",1)
rep("app: 'isa', pfx: 'xz-isa-'","app: 'jer', pfx: 'xz-jer-'",1)
rep('"slug": "isa"','"slug": "jer"',1)
rep('"zh": "以賽亞書"','"zh": "耶利米書"',1)
rep('"en": "Isaiah"','"en": "Jeremiah"',1)
rep('data-pfx="isa321-"','data-pfx="jer321-"',1)
rep('1,292','1,364')
rep('All sixty-six chapters','All fifty-two chapters')
rep('all sixty-six chapters','all fifty-two chapters')
s=s.replace('through chapter sixty-six','through chapter fifty-two')
rep('<meta name="apple-mobile-web-app-title" content="Isaiah">','<meta name="apple-mobile-web-app-title" content="Jeremiah Study Notes">',1)
rep('{"n":16,"t":"Isaiah","a":["Neh"','{"n":16,"t":"Nehemiah","a":["Neh"',1)
rep('{"n":21,"t":"Isaiah","a":["Eccl"','{"n":21,"t":"Ecclesiastes","a":["Eccl"',1)
rep('["Isaiah",21]','["Ecclesiastes",21]',1)
rep('["Isaiah",16]','["Nehemiah",16]',1)
rep("app: 'isa-en',","app: 'jer-en',",1)
rep("inApp: (n, ch) => n === 16 && ch >= 1 && ch <= 13","inApp: (n, ch) => n === 24 && ch >= 1 && ch <= 52",1)
rep("if (r.n === 16 && r.ch >= 1 && r.ch <= 13){","if (r.n === 24 && r.ch >= 1 && r.ch <= 52){",1)
rep("short_name: 'Isaiah Notes'","short_name: 'Jeremiah Study Notes'",1)
rep("(EN ? 'isa' : '321-Isaiah')","(EN ? 'jer' : '321-Jeremiah')",1)
rep("(EN ? 'isa-' : '321-Isaiah-')","(EN ? 'jer-' : '321-Jeremiah-')",2)
dead=re.search(r"const note = \(n === 12 && vn === 29\) \? '[^\n]*?' : '';",s);assert dead
s=s.replace(dead.group(0),"const note = '';");print('✓ dead note')
PROT={'{"n":23,"t":"Isaiah"':'@@P1@@','["Isaiah",23]':'@@P2@@',"isaiah: 'Isaiah'":'@@P3@@',"proph: 'Isaiah Jeremiah":'@@P4@@'}
for a,b in PROT.items():
    assert s.count(a)==1,a;s=s.replace(a,b)
s=s.replace('Isaiah','Jeremiah')
for a,b in PROT.items():s=s.replace(b,a)
print('Isaiah left:',len(re.findall('Isaiah',s)))
for m in re.finditer('Isaiah',s):print('   ',s[max(0,m.start()-80):m.start()+60].replace('\n',' '))
open(R+'/build/shell_jer_en.html','w',encoding='utf-8').write(s)
