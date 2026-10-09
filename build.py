import re,glob,os
src=open('index.src.html',encoding='utf-8').read()
used=set(re.findall(r'href="#([a-z-]+)"',src))|{'plus','minus','check'}
sym=[]
for f in sorted(glob.glob('icons/*.svg')):
    n=os.path.basename(f)[:-4]
    if n not in used: continue
    s=open(f).read()
    vb=re.search(r'viewBox="([^"]+)"',s).group(1)
    inner=re.sub(r'^<svg[^>]*>|</svg>\s*$','',s.strip())
    sym.append(f'<symbol id="{n}" viewBox="{vb}">{inner}</symbol>')
sprite='<svg width="0" height="0" style="position:absolute" aria-hidden="true">'+''.join(sym)+'</svg>'
import json
lq=json.load(open('lqip.json'))
out=src.replace('<!--SPRITE-->',sprite)
out=re.sub(r'<!--LQ:([a-z0-9-]+)-->',lambda m:'style="background-image:url('+lq[m.group(1)]+')"',out)
open('index.html','w',encoding='utf-8').write(out)
bad=[c for c in ('—','–') if c in out]
print('icons',len(sym),'used',sorted(used-{n for n in used if os.path.exists(f"icons/{n}.svg")}),'dashes',bad,'bytes',len(out))
