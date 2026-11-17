"""Builds the blog: every blog/_posts/*.md (front matter + Markdown) becomes blog/<slug>.html,
plus blog/index.html and the site's sitemap.xml. Run from the site folder: python3 blog/_build.py"""
import datetime, html, json, re
from pathlib import Path
import markdown

SITE = 'https://getfitted.nl'
ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / 'blog'
T = {'nl': {'blog': 'Blog', 'home': 'Home', 'guide': 'Handleiding', 'new': 'Wat is er nieuw', 'privacy': 'Privacyverklaring',
            'read': 'Lees verder', 'other': 'Read in English', 'back': 'Alle artikelen', 'months': ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'],
            'cta': 'Fitted CV stemt je cv in een paar minuten af op elke vacature, alleen met wat je echt gedaan hebt.', 'ctab': 'Bekijk Fitted CV', 'get': 'Gratis downloaden'},
     'en': {'blog': 'Blog', 'home': 'Home', 'guide': 'User guide', 'new': "What's new", 'privacy': 'Privacy policy',
            'read': 'Read more', 'other': 'Lees in het Nederlands', 'back': 'All articles', 'months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            'cta': 'Fitted CV tailors your CV to every job ad in a few minutes, using only what you really did.', 'ctab': 'See Fitted CV', 'get': 'Get it free'}}

HEAD_CSS = (ROOT / 'guide.html').read_text(encoding='utf-8').split('<style>', 1)[1].split('</style>', 1)[0]
HEAD_CSS = HEAD_CSS.replace('url("fonts/', 'url("../fonts/')
EXTRA_CSS = """
article em{font-size:inherit;color:var(--ink-2)}
.crumbs{font-size:14px;color:var(--ink-3);margin:0 0 14px} .crumbs a{color:var(--ink-3)}
article h2{font-size:26px} article blockquote p+p{margin-top:8px}
.cta{margin-top:34px;padding:20px 22px;border-radius:16px;background:var(--amber-soft)} .cta p{margin:0 0 10px}
.posts{list-style:none;padding:0;margin:18px 0 0} .posts li{border-top:1px solid var(--line);padding:18px 0;margin:0}
.posts h2{margin:0 0 4px;font-size:24px} .posts h2 a{color:var(--ink);text-decoration:none} .posts h2 a:hover{color:var(--petrol)}
.posts p{margin:4px 0;color:var(--ink-2)} .meta{font-size:14px;color:var(--ink-3)}
"""

def parse(p):
    raw = p.read_text(encoding='utf-8')
    _, fm, body = raw.split('---', 2)
    meta = dict(l.split(':', 1) for l in fm.strip().splitlines())
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    meta['html'] = markdown.markdown(body.strip(), extensions=['extra'])
    meta['words'] = len(re.findall(r'\w+', body))
    return meta

def nice_date(d, lang):
    d = datetime.date.fromisoformat(d)
    return f"{d.day} {T[lang]['months'][d.month - 1]} {d.year}"

def esc(s): return html.escape(s, quote=True)

def footer(lang, up='../'):
    t = T[lang]
    return f"""<footer><div class="wrap">
  <span>© 2026 FITTED · Fitted CV</span>
  <a href="{up}index.html">{t['home']}</a>
  <a href="{up}blog/index.html">{t['blog']}</a>
  <a href="{up}guide.html">{t['guide']}</a>
  <a href="{up}changelog.html">{t['new']}</a>
  <a href="{up}privacy.html">{t['privacy']}</a>
  <span>info@getfitted.nl</span>
</div></footer>"""

def page(lang, title, desc, url, body, extra_head='', alt=None):
    alts = ''
    if alt:
        alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{u}">\n' for l, u in alt.items())
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<script>if(location.protocol==="http:"&&/(^|\\.)getfitted\\.nl$/.test(location.hostname))location.replace("https://getfitted.nl"+location.pathname+location.search+location.hash)</script>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://assets.mailerlite.com; object-src 'none'; base-uri 'self'; form-action 'self'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{alts}<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/share.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.ico">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
{extra_head}<style>{HEAD_CSS}{EXTRA_CSS}</style>
<link rel="stylesheet" href="../calm.css">
</head>
<body>
<header><div class="wrap">
  <a href="../index.html" aria-label="Fitted CV home"><img class="logo dark" src="../img/logo.svg" alt="Fitted CV" width="131" height="32"><img class="logo white" src="../img/logo-white.svg" alt="Fitted CV" width="131" height="32"></a>
  <nav class="topnav" aria-label="Site"><a href="../guide.html">{T[lang]['guide']}</a><a href="index.html" aria-current="page">{T[lang]['blog']}</a><a class="get" href="https://apps.microsoft.com/detail/9N3J1XHVJQ75" rel="noopener">{T[lang]['get']}</a></nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
{footer(lang)}
</body>
</html>
"""

import os
TODAY = os.environ.get('FITTED_BLOG_DATE') or datetime.date.today().isoformat()  # set to build a future week's upload
# Scheduled posts: a post with a date in the future is skipped until a build on or after that date.
posts = sorted((m for m in (parse(p) for p in (BLOG / '_posts').glob('*.md')) if m['date'] <= TODAY),
               key=lambda m: (m['date'], m['slug']), reverse=True)
by_slug = {m['slug']: m for m in posts}
for m in posts:
    lang, t = m['lang'], T[m['lang']]
    url = f"{SITE}/blog/{m['slug']}.html"
    pair = by_slug.get(m.get('pair', ''))
    alt = {lang: url}
    if pair:
        alt[pair['lang']] = f"{SITE}/blog/{pair['slug']}.html"
    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': m['title'], 'description': m['description'],
          'datePublished': m['date'], 'dateModified': m.get('updated', m['date']), 'inLanguage': lang, 'mainEntityOfPage': url,
          'image': f'{SITE}/img/share.png', 'wordCount': m['words'],
          'author': {'@type': 'Organization', 'name': 'FITTED', 'url': SITE}, 'publisher': {'@type': 'Organization', 'name': 'FITTED', 'url': SITE}}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Fitted CV', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': SITE + '/blog/index.html'},
        {'@type': 'ListItem', 'position': 3, 'name': m['title'], 'item': url}]}
    head = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld, crumbs))
    other = f' · <a href="{pair["slug"]}.html" hreflang="{pair["lang"]}" lang="{pair["lang"]}">{t["other"]}</a>' if pair else ''
    body = f"""<p class="crumbs"><a href="index.html">{t['blog']}</a> · {nice_date(m['date'], lang)}{other}</p>
<article>
<h1>{esc(m['title'])}</h1>
<p class="lead">{esc(m['description'])}</p>
{m['html']}
</article>
<div class="cta"><p>{t['cta']}</p><a class="dl" href="../index.html">{t['ctab']}</a></div>
<p class="crumbs" style="margin-top:22px"><a href="index.html">← {t['back']}</a></p>"""
    (BLOG / f"{m['slug']}.html").write_text(page(lang, m['title'] + ' | Fitted CV', m['description'], url, body, head, alt), encoding='utf-8')

def items(lang):
    return '\n'.join(f"""<li><h2><a href="{m['slug']}.html">{esc(m['title'])}</a></h2>
<p>{esc(m['description'])}</p><p class="meta">{nice_date(m['date'], lang)} · <a href="{m['slug']}.html">{T[lang]['read']}</a></p></li>""" for m in posts if m['lang'] == lang)

idx_body = f"""<div data-l="nl"><h1>Blog</h1>
<p class="lead">Praktische tips om je cv af te stemmen op elke vacature, een goede motivatiebrief te schrijven en je sollicitaties bij te houden.</p>
<ul class="posts">{items('nl')}</ul></div>
<div data-l="en"><h1>Blog</h1>
<p class="lead">Practical tips for tailoring your CV to every job ad, writing a good cover letter and keeping track of your applications.</p>
<ul class="posts">{items('en')}</ul></div>"""
idx = page('nl', 'Blog: cv, sollicitatie en vacatures | Fitted CV',
           'Praktische tips over je cv afstemmen op een vacature, motivatiebrieven en navragen na je sollicitatie. Practical CV and job application tips.',
           f'{SITE}/blog/index.html', idx_body)
idx = idx.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
idx = idx.replace('<style>', '<style>html[lang="en"] [data-l="nl"],html[lang="nl"] [data-l="en"]{display:none!important}\n', 1)
idx = idx.replace('<header><div class="wrap">\n  <a href="../index.html" aria-label="Fitted CV home">', '<header><div class="wrap">\n  <a href="../index.html" aria-label="Fitted CV home">', 1)
idx = idx.replace('</div></header>', '  <div class="lang" role="group" aria-label="Language / Taal"><button type="button" data-set="nl" aria-pressed="true">NL</button><button type="button" data-set="en" aria-pressed="false">EN</button></div>\n</div></header>', 1)
idx = idx.replace('</body>', """<script>(function(){const r=document.documentElement;function set(l){r.lang=l;document.querySelectorAll('.lang button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.set===l)));try{localStorage.setItem('fitted-lang',l)}catch(e){}}
let s='nl';try{s=localStorage.getItem('fitted-lang')||((navigator.language||'').toLowerCase().startsWith('nl')?'nl':'en')}catch(e){}
set(s);document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>set(b.dataset.set)));})();</script>
</body>""", 1)
fn, fe = footer('nl'), footer('en')
both = fn.replace('<footer><div class="wrap">', '<footer><div class="wrap" data-l="nl">') + '\n' + fe.replace('<footer><div class="wrap">', '<footer><div class="wrap" data-l="en">')
idx = idx.replace(fn, both, 1)
(BLOG / 'index.html').write_text(idx, encoding='utf-8')

today = datetime.date.today().isoformat()
urls = [('/', today), ('/guide.html', today), ('/changelog.html', today), ('/blog/index.html', today),
        ('/privacy.html', None), ('/terms.html', None), ('/refund.html', None)]
urls += [(f"/blog/{m['slug']}.html", m.get('updated', m['date'])) for m in posts]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, d in urls:
    sm.append(f'  <url><loc>{SITE}{u}</loc>' + (f'<lastmod>{d}</lastmod>' if d else '') + '</url>')
sm.append('</urlset>')
(ROOT / 'sitemap.xml').write_text('\n'.join(sm) + '\n', encoding='utf-8')
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /blog/_posts/\n\nSitemap: {SITE}/sitemap.xml\n', encoding='utf-8')
print('built', len(posts), 'posts')
