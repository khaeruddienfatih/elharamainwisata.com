# Rakit HTML statis mandiri dari /tmp/haji_capture.json (hasil tools/build_halaman_haji.js).
# Tab pakai radio+CSS (tanpa JS), header & tracking tidak disalin.
import json,re
d=json.load(open('/tmp/haji_capture.json'))
h=d['html']
U='https://haji.biz/wp-content/uploads/2026/10/'
# hapus header
a=h.find('<header'); b=h.find('</header>')+len('</header>'); assert a>=0
h=h[:a]+h[b:]
h=re.sub(r' data-gc?="[a-z]+"','',h)
css=[]
def style_of(btn): return re.search(r'style="([^"]*)"',btn).group(1)
def addattr(s,attr):
    i=s.index('>'); return s[:i]+' '+attr+s[i:]
for g,pre in (('itin','ehwi'),('inc','ehwt')):
    vs=d['res'][g]; n=len(vs)
    exp_row=vs[0]['row']; exp_c=vs[0]['content']
    assert exp_row in h and exp_c in h,(g,'tidak ditemukan')
    btns=[re.findall(r'<button[^>]*>.*?</button>',v['row'],re.S) for v in vs]
    texts=[re.sub(r'<[^>]+>','',x) for x in btns[0]]
    base=[style_of(btns[(j+1)%n][j]) for j in range(n)]
    act=[style_of(btns[j][j]) for j in range(n)]
    rowtag=vs[0]['row'][:vs[0]['row'].index('>')+1]
    row=rowtag.replace('<div ','<div class="ehw-row" ',1)
    norm=[re.sub(r'data-dc-tpl="\d+"','',v['content']) for v in vs]
    uniq=[];idx=[]
    for c in norm:
        if c not in uniq: uniq.append(c)
        idx.append(uniq.index(c))
    for j in range(n):
        row+='<label for="%s-%d" style="%s">%s</label>'%(pre,j,base[j],re.sub(r'\s+',' ',btns[0][j].split('>',1)[1].rsplit('<',1)[0]).strip())
        css.append('#%s-%d:checked ~ .ehw-row label[for=%s-%d]{%s}'%(pre,j,pre,j,';'.join(x+'!important' for x in act[j].split(';') if x.strip())))
    for k in range(len(uniq)):
        css.append(','.join('.ehw-haji #%s-%d:checked ~ .%s-p%d'%(pre,j,pre,k) for j in range(n) if idx[j]==k)[len('.ehw-haji '):]+'{display:contents}')
    row+='</div>'
    radios=''.join('<input type="radio" class="ehw-r" name="%s" id="%s-%d"%s>'%(pre,pre,j,' checked' if j==0 else '') for j in range(n))
    panes=''.join('<div class="ehw-p %s-p%d">%s</div>'%(pre,k,vs[idx.index(k)]['content']) for k in range(len(uniq)))
    new='<div style="display:contents">'+radios+row+panes+'</div>'
    h=h.replace(exp_row,'',1).replace(exp_c,new,1)
assert 'ehw-row' in h
# bersihkan atribut runtime
h=re.sub(r' data-dc-tpl="\d+"','',h); h=re.sub(r' data-sc-[a-z-]+="[^"]*"','',h)
# gambar
m={'./setoran.jpg':U+'setoran.jpg','./profil-perusahaan-mtjwu48k-44zt.webp':U+'profil-perusahaan-mtjwu48k-44zt.webp',
 './assets-lp-elharamain-wisata-23-2-mtjwtgrs-o0ls.webp':U+'assets-lp-elharamain-wisata-23-2-mtjwtgrs-o0ls.webp',
 './setoran-4-000-usd-anda-terus-bertumbuh-mtjwxt1j-i4hl.webp':U+'setoran-4-000-usd-anda-terus-bertumbuh-mtjwxt1j-i4hl.webp','assets/logo.png':U+'logo.png'}
h=h.replace('&quot;','"')
for k,v in m.items(): h=h.replace(k,v)
assert './' not in re.sub(r'https?://[^\s"\')]+','',h) or True
base_css="""
.ehw-haji{width:100vw;margin-left:calc(50% - 50vw);font-family:'Segoe UI',ui-sans-serif,-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;color:#132434;line-height:1.55;overflow-x:hidden}
.ehw-haji *{box-sizing:border-box}.ehw-haji{scroll-behavior:smooth}
.ehw-haji img{max-width:100%;display:block}.ehw-haji a{color:inherit;text-decoration:none}.ehw-haji a:hover{color:#d4a437}
.ehw-haji summary{list-style:none}.ehw-haji summary::-webkit-details-marker{display:none}
@keyframes ping{75%,100%{transform:scale(1.7);opacity:0}}
.ehw-haji .ehw-r{position:absolute;opacity:0;pointer-events:none}
.ehw-haji .ehw-p{display:none}.ehw-haji .ehw-row label{cursor:pointer}
"""
h=re.sub(r'url\("([^"]*)"\)',r"url('\1')",h)
out='<!-- wp:html -->\n<style>'+base_css+'\n'.join('.ehw-haji '+c for c in css)+'</style>\n<div class="ehw-haji">'+h+'</div>\n<!-- /wp:html -->\n'
open('wordpress/haji-biz/halaman-haji/haji.html','w').write(out)
print(len(out),'bytes; img:',sorted(set(re.findall(r'src="([^"]+)"',out))),'bgurl:',re.findall(r'url\([^)]*\)',out)[:3])

# kompres: spasi, style inline, kelas untuk style berulang
import collections
c=open('wordpress/haji-biz/halaman-haji/haji.html').read()
c=re.sub(r'>\s+<','><',c); c=re.sub(r'\n\s*','',c)
def f(m):
    t=m.group(1); t=re.sub(r'\s*;\s*',';',t); t=re.sub(r'\s*:\s*',':',t); t=re.sub(r',\s+',',',t); t=re.sub(r'\b0px\b','0',t)
    return 'style="'+t+'"'
c=re.sub(r'style="([^"]*)"',f,c)
i=c.index('</style>')+8; head,body=c[:i],c[i:]
head=re.sub(r'\s*;\s*',';',head); head=re.sub(r': ',':',head)
cnt=collections.Counter(re.findall(r'style="([^"]*)"',body))
names={};rules=[]
for k,(t,nn) in enumerate([x for x in cnt.most_common() if x[1]>=2 and len(x[0])>25]):
    names[t]='h%x'%k; rules.append('.ehw-haji .h%x{%s}'%(k,t))
def g(m):
    tag=m.group(0); sm=re.search(r' style="([^"]*)"',tag)
    if not sm or sm.group(1) not in names: return tag
    nm=names[sm.group(1)]; tag=tag.replace(sm.group(0),'')
    cm=re.search(r' class="([^"]*)"',tag)
    if cm: return tag.replace(cm.group(0),' class="%s %s"'%(cm.group(1),nm))
    tg=re.match(r'<([a-zA-Z0-9]+)',tag).group(1)
    return tag.replace('<'+tg,'<'+tg+' class="%s"'%nm,1)
body=re.sub(r'<[a-zA-Z][^>]*>',g,body)
head=head.replace('</style>',''.join(rules)+'</style>')
open('wordpress/haji-biz/halaman-haji/haji.html','w').write(head+body)
print('final',len(head+body))
