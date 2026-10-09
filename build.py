import re,glob,os,json,sys,subprocess
# ---------------------------------------------------------------
# РЕЖИМ САЙТА. DEMO=True: макет, заявки уходят автору макета (Юлии).
# Когда Дмитрий оплатит: DEMO=False, убрать плашку .demo (см. заметки), python3 build.py, git push.
DEMO = True
PHONE_OWNER = "77052070537"   # повар (Дмитрий)
PHONE_AUTHOR = "77017591615"  # автор макета (Юлия)
# ---------------------------------------------------------------
phone = PHONE_AUTHOR if DEMO else PHONE_OWNER
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
lq=json.load(open('lqip.json'))
out=src.replace('<!--SPRITE-->',sprite)
out=re.sub(r'<!--LQ:([a-z0-9-]+)-->',lambda m:'style="background-image:url('+lq[m.group(1)]+')"',out)
# фото и шрифты отдаём с CDN jsDelivr (на GitHub Pages у части клиентов очень медленно).
# Версия закреплена коммитом, где менялись img/ или fonts/. Если они не закоммичены, берём локальные файлы.
def sh(*a): return subprocess.run(a,capture_output=True,text=True).stdout.strip()
sha=sh('git','log','-1','--format=%H','--','img','fonts'); dirty=sh('git','status','--porcelain','img','fonts')
CDN=f'https://cdn.jsdelivr.net/gh/jull1et/dmitry-catering@{sha}/' if sha and not dirty else ''
out=out.replace('__CDN__',CDN)
if CDN:
    out=re.sub(r'(?<![\w/.@-])img/(?=[a-z0-9-]+\.webp)',CDN+'img/',out)
out=out.replace('__PHONE__',phone)
out=out.replace('__SRC__','макета сайта' if DEMO else 'сайта')
if DEMO:
    out=out.replace('<!--ROBOTS-->','<meta name="robots" content="noindex, nofollow">')
    out=out.replace('<!--DEMONOTE-->','<p class="fine demo-note">Это макет сайта. Заявка из макета придёт его автору, а не повару. После запуска сайта заявки будут приходить повару.</p>')
    # телефон повара виден, но не кликабелен: звонок не уходит с макета
    out=re.sub(r'<a href="tel:\+7[0-9]+">(.*?)</a>',r'<span class="telx">\1</span>',out)
else:
    out=out.replace('<!--ROBOTS-->','').replace('<!--DEMONOTE-->','')
open('index.html','w',encoding='utf-8').write(out)
bad=[c for c in ('\u2014','\u2013') if c in out]
print('cdn',CDN or 'LOCAL','| mode','DEMO' if DEMO else 'LIVE','phone',phone,'icons',len(sym),'dashes',bad,'bytes',len(out),'owner-number-left',out.count(PHONE_OWNER) if DEMO else '-')
