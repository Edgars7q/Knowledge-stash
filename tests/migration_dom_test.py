"""Test migration and import rejection using DOM harness, without network navigation."""
from playwright.sync_api import sync_playwright
import pathlib,re,json
root=pathlib.Path('/mnt/data/Knowledge-Stash-v0.2')
html=re.sub(r'<script [^>]*></script>','',(root/'index.html').read_text())
html=re.sub(r'<link [^>]*rel="(?:stylesheet|manifest|apple-touch-icon|icon)"[^>]*>','',html)
legacy={'saved':['e1','own-123-456'],'learned':{'e1':'2026-10-01'},'reviews':{'e1':{'step':2,'due':'2026-11-01'}},'history':[{'day':'2026-10-01','type':'learn'}], 'custom':[{'id':'own-123-456','title':'My idea','category':'Science','hook':'Testing old content','body':'Legacy body for backward compatibility','takeaway':'Keep old data'}], 'theme':'dark'}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=b.new_page(viewport={'width':390,'height':844});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content(html)
 p.evaluate('''old=>{Object.defineProperty(window,'localStorage',{configurable:true,value:{_d:{'knowledge-stash-v1':JSON.stringify(old)},getItem(k){return this._d[k]??null},setItem(k,v){this._d[k]=String(v)},removeItem(k){delete this._d[k]}}});window.fetch=async()=>({ok:true,json:async()=>({format:'knowledge-stash-lesson-pack',schemaVersion:2,lessons:[]})});}''',legacy)
 for f in ['data.js','lessons/builtin.js','visuals.js','app.js']:p.add_script_tag(content=(root/f).read_text())
 s=p.evaluate("JSON.parse(localStorage.getItem('knowledge-stash-v2'))")
 assert s['saved']==['e1','own-123-456'] and s['theme']=='dark' and s['custom'][0]['id']=='own-123-456'
 assert p.evaluate("localStorage.getItem('knowledge-stash-v1')")
 p.locator('[data-tab=stash]').click();assert 'My idea' in p.locator('main').inner_text()
 p.locator('#open-add').click()
 invalid={'format':'knowledge-stash-lesson-pack','schemaVersion':2,'lessons':[{'id':'bad','version':1,'title':'Bad','category':'Invalid'}]}
 p.locator('#pack-input').fill(json.dumps(invalid));p.locator('[data-action=preview-pack]').click();assert 'Unsupported category' in p.locator('#pack-preview').inner_text() or 'Missing lesson' in p.locator('#pack-preview').inner_text()
 assert not p.evaluate("JSON.parse(localStorage.getItem('knowledge-stash-v2')).customLessons.length")
 p.locator('[data-action=close]').click()
 p.locator('#open-settings').click();p.evaluate('window.confirm=()=>true')
 p.locator('[data-action=reset]').click();s=p.evaluate("JSON.parse(localStorage.getItem('knowledge-stash-v2'))")
 assert s['schemaVersion']==2 and not s['custom'] and not s['saved']
 assert p.evaluate("localStorage.getItem('knowledge-stash-v1')")
 print('PASS: v0.1 saved content/ideas/theme/reviews migrated, invalid import rejected, safe reset preserves old key')
 assert not errors,errors
 b.close()
