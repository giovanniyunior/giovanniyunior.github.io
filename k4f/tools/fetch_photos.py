# Downloads candidate real photos from Wikimedia Commons (free licenses) for the K4F class page.
import json, os, urllib.request, urllib.parse, time
UA = {'User-Agent': 'K4F-classroom-page/1.0 (https://giovanniyunior.github.io/k4f/)'}
Q = json.load(open('k4f/tools/photo_queries.json'))
out = 'k4f/cand'; os.makedirs(out, exist_ok=True)
meta = {}
def get(u):
    req = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()
for key, query in Q.items():
    api = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action':'query','format':'json','generator':'search','gsrnamespace':6,'gsrlimit':8,
        'gsrsearch': query + ' filetype:bitmap', 'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':900})
    try: d = json.loads(get(api))
    except Exception as e: print('ERR', key, e); continue
    pages = sorted((d.get('query') or {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    n = 0
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]; u = ii.get('thumburl')
        if not u or ii.get('width', 0) < 600: continue
        try: b = get(u)
        except Exception as e: print('ERR img', key, e); continue
        fn = f'{key}_{n}.jpg'; open(os.path.join(out, fn), 'wb').write(b)
        em = ii.get('extmetadata', {})
        meta[fn] = {'title': p['title'], 'artist': em.get('Artist', {}).get('value', ''), 'license': em.get('LicenseShortName', {}).get('value', ''), 'page': ii.get('descriptionurl')}
        n += 1; time.sleep(0.3)
        if n >= 6: break
    print(key, n)
json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=1)
