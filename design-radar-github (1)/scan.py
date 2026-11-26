import json,re,os,hashlib
from pathlib import Path
from datetime import datetime,timezone,timedelta
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent; OUT=ROOT/'docs'; SHOTS=OUT/'shots'; SHOTS.mkdir(parents=True,exist_ok=True)
SITES=json.loads((ROOT/'sites.json').read_text()); FILE=OUT/'state.json'
state=json.loads(FILE.read_text()) if FILE.exists() else {'sites':SITES,'snapshots':[],'checks':[]}
now=datetime.now(timezone.utc).isoformat(timespec='seconds'); checks=[]
def diff(a,b):
 a=Image.open(a).convert('RGB').resize((320,180)); b=Image.open(b).convert('RGB').resize((320,180)); return sum(max(p)>35 for p in ImageChops.difference(a,b).getdata())/(320*180)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for site in SITES:
  for device,w,h in [('PC',1440,900),('Mobile',390,844)]:
   ctx=None; path=None
   try:
    ctx=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1,locale='en-US',timezone_id='America/New_York',is_mobile=device=='Mobile',has_touch=device=='Mobile'); page=ctx.new_page(); resp=page.goto(site['url'],wait_until='domcontentloaded',timeout=25000); page.wait_for_timeout(3000)
    title=page.title(); body=page.locator('body').inner_text(timeout=5000)
    if not resp or resp.status>=400 or len(body.strip())<60 or re.search(r'access denied|verify (that )?you are human|just a moment|robot check|captcha|request blocked',title+' '+body[:600],re.I): raise RuntimeError('页面不可用或疑似访问限制')
    page.add_style_tag(content='*,*::before,*::after{animation-play-state:paused!important;transition:none!important;caret-color:transparent!important}')
    ident=hashlib.sha256((site['name']+device+now).encode()).hexdigest()[:20]; rel=f'shots/{ident}.jpg'; path=OUT/rel; page.screenshot(path=str(path),type='jpeg',quality=75,animations='disabled',timeout=15000)
    prev=next((s for s in state['snapshots'] if s['brand']==site['name'] and s['device']==device),None); score=diff(OUT/prev['image'],path) if prev else None; kind='baseline' if prev is None else ('candidate' if score>=.08 else 'stable')
    if kind=='stable': path.unlink(); path=None
    else: state['snapshots'].insert(0,{'id':ident,'brand':site['name'],'device':device,'ts':now,'url':page.url,'image':rel,'previous':prev['id'] if prev else None,'score':score,'kind':kind})
    checks.append({'brand':site['name'],'device':device,'status':'ok','message':kind,'ts':now})
   except Exception as e:
    if path: path.unlink(missing_ok=True)
    checks.append({'brand':site['name'],'device':device,'status':'error','message':str(e)[:220],'ts':now})
   finally:
    if ctx: ctx.close()
 browser.close()
# Keep most recent 10 stored changes per brand/device; remove old unreferenced files.
counts={}; kept=[]
for s in state['snapshots']:
 k=(s['brand'],s['device']); counts[k]=counts.get(k,0)+1
 if counts[k]<=10: kept.append(s)
state.update(sites=SITES,snapshots=kept,checks=checks,last_run=now,threshold=.08)
used={s['image'] for s in kept}
for f in SHOTS.glob('*.jpg'):
 if 'shots/'+f.name not in used: f.unlink()
FILE.write_text(json.dumps(state,ensure_ascii=False,indent=2)); (OUT/'notifications.json').write_text(json.dumps({'events':[s for s in kept if s['kind']=='candidate'],'last_run':now},ensure_ascii=False,indent=2))
