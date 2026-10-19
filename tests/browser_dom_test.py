"""DOM-level smoke test without URL navigation; needed on browsers with managed URLBlocklist."""
from playwright.sync_api import sync_playwright
import pathlib,re,json
root=pathlib.Path('/mnt/data/Knowledge-Stash-v0.2')
html=(root/'index.html').read_text();html=re.sub(r'<script [^>]*></script>','',html)
html=re.sub(r'<link [^>]*rel="(?:stylesheet|manifest|apple-touch-icon|icon)"[^>]*>','',html)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844});errs=[];page.on('pageerror',lambda x:errs.append(str(x)))
 page.set_content(html)
 page.add_style_tag(content=(root/'style.css').read_text())
 page.evaluate('''()=>{Object.defineProperty(window,'localStorage',{configurable:true,value:{_d:{},getItem(k){return this._d[k]??null},setItem(k,v){this._d[k]=String(v)},removeItem(k){delete this._d[k]}}});window.fetch=async()=>({ok:true,json:async()=>({format:'knowledge-stash-lesson-pack',schemaVersion:2,lessons:[]})});}''')
 for f in ['data.js','lessons/builtin.js','visuals.js','app.js']:
  page.add_script_tag(content=(root/f).read_text())
 print('after app startup:',page.locator('main').inner_text()[:120]);print('errors',errs)
 page.screenshot(path='/mnt/data/Knowledge-Stash-v0.2-preview.png',full_page=True)
 assert 'Grow your mind.' in page.locator('body').inner_text(),errs
 page.locator('[data-tab="discover"]').click()
 print('after discover',page.locator('main').inner_text()[:120]);print('errors',errs)
 assert page.locator('[data-lesson]').count()>=8
 page.locator('[data-lesson="econ-prices"]').click()
 assert 'One price, many decisions' in page.locator('main').inner_text(),errs
 page.screenshot(path='/mnt/data/Knowledge-Stash-v0.2-lesson-preview.png',full_page=True)
 for i in range(5):
  assert f'Stage {i+1} of 5' in page.locator('main').inner_text(),errs
  page.locator('[data-stage="next"]').click()
 print('quiz forms',page.locator('#quiz-form').count());assert page.locator('#quiz-form').count()
 for i,ans in enumerate([0,1,1,0,0,0]):page.locator(f'input[name=q{i}][value="{ans}"]').check()
 page.locator('#quiz-form button[type=submit]').click()
 assert 'Understanding demonstrated' in page.locator('main').inner_text(),errs
 page.locator('[data-action="reread"]').click();assert 'Stage 1 of 5' in page.locator('main').inner_text()
 page.locator('[data-action="leave-lesson"]').click()
 page.locator('#open-add').click()
 page.locator('#pack-input').fill((root/'docs/EXAMPLE-LESSON-PACK.json').read_text())
 page.locator('[data-action="preview-pack"]').click()
 assert 'Valid pack' in page.locator('#pack-preview').inner_text(),page.locator('#pack-preview').inner_text()
 page.locator('[data-action="confirm-import"]').click()
 print('imported',page.locator('[data-lesson="example-process-bottlenecks"]').count(), 'head',page.locator('main').inner_text()[:250], 'state',page.evaluate("localStorage.getItem('knowledge-stash-v2')")[:350], 'errors',errs)
 assert page.locator('[data-lesson="example-process-bottlenecks"]').count()
 page.locator('#open-settings').click();assert page.locator('[data-action="export-pack"]').count()
 assert not errs,errs
 print('PASS DOM smoke: library, lesson navigation, quiz, reread, import, settings')
 b.close()
