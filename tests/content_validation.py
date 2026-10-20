"""Basic independent pack/bundle integrity checks: run python tests/content_validation.py."""
import re,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
s=(root/'lessons/builtin.js').read_text()
ls=json.loads(s[s.index('['):s.rindex(';')])
assert len(ls)==8 and len({x['id'] for x in ls})==8
for l in ls:
 assert len(l['stages'])==5 and len(l['quiz'])>=5,l['id']
 words=sum(len(p.split()) for x in l['stages'] for p in x['paragraphs'])
 assert words>=600,(l['id'],words)
 assert l['minutes']>=8
 for q in l['quiz']:
  assert len(q['options'])>=2 and isinstance(q['answer'],int) and 0<=q['answer']<len(q['options'])
 for src in l['sources']:assert src['url'].startswith('https://')
cards_source=(root/'data.js').read_text()
def card_assignment(name):
 match=re.search(r'window\.'+re.escape(name)+r'\s*=\s*',cards_source)
 assert match,f'Missing {name} content assignment'
 return json.JSONDecoder().raw_decode(cards_source[match.end():])[0]
quick=card_assignment('STARTER_IDEAS')
legacy=card_assignment('KS_LEGACY_IDEAS')
by_id={lesson['id']:lesson for lesson in ls}
assert len(quick)==len(ls)==8
assert len({card['id'] for card in quick})==len(quick)
assert {card['lessonId'] for card in quick}==set(by_id),'Each full lesson needs exactly one public quick card'
for card in quick:
 assert card['category']==by_id[card['lessonId']]['category'],card['id']
 for field in ['id','title','hook','body','example','takeaway','question','lessonId']:
  assert isinstance(card.get(field),str) and card[field].strip(),(card['id'],field)
assert len(legacy)==32 and len({card['id'] for card in legacy})==32,'Original saved cards must remain recoverable'
example=json.loads((root/'docs/EXAMPLE-LESSON-PACK.json').read_text());assert example['schemaVersion']==2
f=(root/'index.html').read_text()
for a in ['app.js','data.js','visuals.js','lessons/builtin.js','style.css','sw.js','packs/community.json','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png']:
 assert (root/a).is_file(),a
for p in (root/'lessons').glob('*.js'):assert p.stat().st_size>0
print('PASS: 8 full lessons and 8 linked quick cards, legacy recovery, quizzes, sources, sample pack and assets')
