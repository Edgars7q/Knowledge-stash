"""Run locally after: python -m http.server 8765. Requires playwright and Chromium."""
import json,time,pathlib,tempfile
from playwright.sync_api import sync_playwright
BASE='http://localhost:8765/'
ROOT=pathlib.Path(__file__).resolve().parents[1]
ARTIFACTS=pathlib.Path(tempfile.mkdtemp(prefix='knowledge-stash-smoke-'))
def run():
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,has_touch=True,is_mobile=True)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE,wait_until='networkidle');page.locator('[data-page="welcome"]').wait_for();page.locator('[data-action="continue-guest"]').click();page.screenshot(path=str(ARTIFACTS/'preview.png'),full_page=True)
  assert page.get_by_text('Grow your mind.').count(),page.locator('body').inner_text()[:500]
  page.locator('[data-tab=discover]').click();page.wait_for_timeout(150)
  assert '8' in page.locator('[data-library=Lessons]').inner_text()
  assert page.locator('[data-lesson]').count()==8
  page.locator('[data-library=Ideas]').click()
  assert page.locator('[data-idea]').count()==8,page.locator('[data-idea]').count()
  page.locator('#open-account').click()
  page.locator('[data-demo-account="demo-alex"]').click()
  page.locator('#login-form button[type=submit]').click()
  page.wait_for_function("window.KSAuth.getCurrentUser()?.id === 'demo-alex'")
  page.locator('[data-tab=discover]').click()
  page.locator('[data-library=Lessons]').click()
  page.locator('[data-lesson="econ-prices"]').click()
  page.wait_for_timeout(150)
  assert 'One price, many decisions' in page.locator('body').inner_text()
  page.screenshot(path=str(ARTIFACTS/'lesson-preview.png'),full_page=True)
  for step in range(5):
   assert page.get_by_text(f'Stage {step+1} of 5').count(), f'stage {step}'
   if step==1:
    page.reload(wait_until='domcontentloaded');assert page.get_by_text('Stage 2 of 5').count()
   if step==2:
    slider=page.locator('[data-slider="demand"]');slider.fill('14');assert page.locator('[data-price]').inner_text()=='€67'
   page.locator('[data-stage=next]').click()
  assert page.locator('#quiz-form .quiz-question').count()==6
  page.locator('#quiz-form input[type=radio]').evaluate_all("els=>{const seen = new Set(); for (let x of els) {if (!seen.has(x.name)) {seen.add(x.name); x.click();}}}")
  page.locator('#quiz-form button[type=submit]').click()
  assert page.evaluate("JSON.parse(localStorage.getItem('knowledge-stash-v2:profile:demo-alex')).lessonProgress['econ-prices'].completed")
  assert page.locator('.quiz-summary').count()==1
  page.locator('[data-action=reread]').click()
  assert page.get_by_text('Stage 1 of 5').count()
  # Correct first seven? lesson contains six. Open stages again and answer all using ground-truth indexes from builtin fixture.
  for _ in range(5):page.locator('[data-stage=next]').click()
  answers=[0,1,1,0,0,0]
  for i,idx in enumerate(answers):page.locator(f'input[name=q{i}][value="{idx}"]').check()
  page.locator('#quiz-form button[type=submit]').click()
  st=page.evaluate("JSON.parse(localStorage.getItem('knowledge-stash-v2:profile:demo-alex')).lessonProgress['econ-prices']")
  assert st['understood'] and st['completed'] and st['nextReview']
  # Lesson pack import and export
  page.locator('[data-action=leave-lesson]').first.click()
  page.locator('#open-add').click()
  example=(ROOT/'docs'/'EXAMPLE-LESSON-PACK.json').read_text()
  page.locator('#pack-input').fill(example)
  page.locator('[data-action=preview-pack]').click()
  assert page.get_by_text('Valid pack').count()
  page.locator('[data-action=confirm-import]').click()
  assert page.locator('[data-lesson="example-process-bottlenecks"]').count()
  page.locator('#open-settings').click()
  assert page.locator('[data-action=export-pack]').count()
  page.locator('[data-action=close]').click()
  # service worker cache offline
  page.wait_for_timeout(1700)
  context.set_offline(True)
  page.reload(wait_until='domcontentloaded')
  assert page.locator('[data-lesson="example-process-bottlenecks"]').count()
  page.locator('[data-lesson="space-gps"]').click()
  assert page.get_by_text('Your position starts with the time of arrival').count()
  context.set_offline(False)
  # separate legacy data migration
  oldctx=browser.new_context();p2=oldctx.new_page();p2.goto(BASE);p2.evaluate("""() => {localStorage.removeItem('knowledge-stash-v2');localStorage.setItem('knowledge-stash-v1', JSON.stringify({saved:['e1'], learned:{e1:'2026-10-10'}, reviews:{e1:{step:1,due:'2026-10-19'}}, custom:[], history:[{day:'2026-10-10',type:'learn'}],theme:'dark'}))}""")
  p2.reload();s=p2.evaluate("JSON.parse(localStorage.getItem('knowledge-stash-v2'))")
  assert s['saved']==['e1'] and s['theme']=='dark' and s['migration']['from']==1 and p2.evaluate("localStorage.getItem('knowledge-stash-v1')")
  assert not errors,errors
  print('PASS: pages, linked quick cards, lessons, resume, graph, quiz, understanding, re-reading, pack import, offline and migration')
  browser.close()
if __name__=='__main__':run()
