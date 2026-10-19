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
example=json.loads((root/'docs/EXAMPLE-LESSON-PACK.json').read_text());assert example['schemaVersion']==2
f=(root/'index.html').read_text()
for a in ['app.js','data.js','visuals.js','lessons/builtin.js','style.css','sw.js','packs/community.json','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png']:
 assert (root/a).is_file(),a
for p in (root/'lessons').glob('*.js'):assert p.stat().st_size>0
print('PASS: 8 complete built-in lessons, quiz indices, source URLs, sample pack and critical assets')
