(() => {
  'use strict';

  const KEY = 'knowledge-stash-v1';
  const CATEGORIES = ['All', 'Psychology', 'Science', 'Engineering', 'Space', 'Philosophy', 'Business', 'Faith & ideas', 'History'];
  const ICONS = {'Psychology':'◉','Science':'⚛','Engineering':'⚙','Space':'✧','Philosophy':'◇','Business':'↗','Faith & ideas':'✺','History':'⌛'};
  const INTERVALS = [1, 3, 7, 14, 30];
  const app = document.getElementById('app-content');
  const overlay = document.getElementById('overlay');
  const dialog = document.getElementById('dialog');
  const toast = document.getElementById('toast');
  let toastTimeout;
  let selection = 'All';
  let searchTerm = '';
  let returnFocus = null;
  let state = load();

  function freshState() { return {saved:[], learned:{}, reviews:{}, history:[], custom:[], theme:'light'}; }
  function load() {
    try {
      const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (saved && typeof saved === 'object') return {...freshState(), ...saved};
    } catch (err) { console.warn('Storage unavailable:', err); }
    return freshState();
  }
  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch (err) { notify('Storage unavailable. Export a backup before leaving.'); }
  }
  function escapeHTML(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  }
  function textValue(value, max=1600) { return String(value ?? '').trim().slice(0, max); }
  function dateKey(date=new Date()) {
    return [date.getFullYear(), String(date.getMonth()+1).padStart(2,'0'), String(date.getDate()).padStart(2,'0')].join('-');
  }
  function offsetDate(days, from=new Date()) {
    const d = new Date(from.getFullYear(), from.getMonth(), from.getDate()+days,12);
    return dateKey(d);
  }
  function allIdeas() { return [...window.STARTER_IDEAS, ...(Array.isArray(state.custom) ? state.custom : [])]; }
  function byId(id) { return allIdeas().find(idea => idea.id === id); }
  function isSaved(id) { return Array.isArray(state.saved) && state.saved.includes(id); }
  function isLearned(id) { return !!state.learned?.[id]; }
  function dueIdeas() {
    return allIdeas().filter(idea => state.reviews?.[idea.id]?.due && state.reviews[idea.id].due <= dateKey());
  }
  function dayIndex() {
    const d = new Date();
    const ordinal = Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/86400000;
    return Math.floor(ordinal);
  }
  function todaysIdeas() {
    const items = allIdeas();
    if (!items.length) return [];
    const start = ((dayIndex()*3) % items.length + items.length) % items.length;
    return Array.from({length:Math.min(3,items.length)},(_,n)=>items[(start+n)%items.length]);
  }
  function daysActive() {
    return new Set((Array.isArray(state.history) ? state.history : []).map(entry => entry.day));
  }
  function streak() {
    const days = daysActive();
    let date = new Date();
    if (!days.has(dateKey(date))) date.setDate(date.getDate()-1);
    let total = 0;
    while (days.has(dateKey(date))) { total++; date.setDate(date.getDate()-1); }
    return total;
  }
  function activity(type) {
    state.history ||= [];
    state.history.push({day:dateKey(), type});
    state.history = state.history.slice(-1200);
  }
  function notify(message) {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(()=>toast.classList.remove('show'), 2600);
  }
  function ideaCard(idea) {
    const learned = isLearned(idea.id);
    return `<button class="idea-card" data-open="${escapeHTML(idea.id)}" aria-label="Read ${escapeHTML(idea.title)}">
      <span class="card-art" data-category="${escapeHTML(idea.category)}" aria-hidden="true">${ICONS[idea.category] || '✦'}</span>
      <span class="idea-card-body">
        <span class="card-meta"><span class="badge">${escapeHTML(idea.category)}</span><span>2 min read</span>${learned?'<span>✓ Learned</span>':''}</span>
        <h3>${escapeHTML(idea.title)}</h3>
        <p>${escapeHTML(idea.hook)}</p>
      </span><span class="arrow" aria-hidden="true">›</span>
    </button>`;
  }
  function empty(icon,title,description,buttonHtml='') {
    return `<div class="empty"><span class="emoji" aria-hidden="true">${icon}</span><strong>${title}</strong><p>${description}</p>${buttonHtml}</div>`;
  }
  function heading(kicker,title,description='') {
    return `<div class="kicker">${kicker}</div><h1>${title}</h1>${description?`<p class="subtext">${description}</p>`:''}`;
  }

  function renderToday() {
    const picks = todaysIdeas();
    const feature = picks[0];
    const done = picks.filter(idea => isLearned(idea.id)).length;
    const percentage = Math.round((done / Math.max(1,picks.length))*100);
    app.innerHTML = `<div class="page">
      ${heading('A little learning, every day','Grow your mind.','Short ideas, useful insights, and a few minutes well spent.')}
      <section class="hero" aria-label="Today’s featured idea">
        <div class="hero-content"><div class="hero-top">✦ &nbsp; Today’s idea</div>
          <h2>${escapeHTML(feature.title)}</h2><p>${escapeHTML(feature.hook)}</p>
          <button class="light-button" data-open="${escapeHTML(feature.id)}">${isLearned(feature.id)?'Read again':'Start learning'} <span aria-hidden="true">→</span></button>
        </div>
      </section>
      <div class="stat-row">
        <div class="stat-card"><strong>${streak()} <span aria-hidden="true">🔥</span></strong><span>Day streak</span></div>
        <div class="stat-card"><strong>${Object.keys(state.learned||{}).length} <span aria-hidden="true">✦</span></strong><span>Ideas learned</span></div>
      </div>
      <div class="progress-card">
        <div class="progress-header"><strong>Today's 3 ideas</strong><span>${done}/${picks.length} complete</span></div>
        <div class="progress-track" role="progressbar" aria-label="Today's ideas completed" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${percentage}"><div class="progress-fill" style="width:${percentage}%"></div></div>
        <p class="progress-caption">${done === picks.length?'Great work! Come back tomorrow for another selection.':'No rush. Small steps build lasting knowledge.'}</p>
      </div>
      <div class="section-head"><h2>More to discover</h2><a class="text-link" href="#discover">See all →</a></div>
      <div class="cards">${picks.slice(1).map(ideaCard).join('')}</div>
      <div class="tip-card"><strong>✦ Make these ideas your own</strong><p>Ask ChatGPT for more learning cards, then add them with the + button. No paid API or extra subscription needed.</p></div>
    </div>`;
  }

  function renderDiscover() {
    app.innerHTML = `<div class="page">
      ${heading('Explore the library','Follow your curiosity.','Browse small ideas across eight subjects.')}
      <input id="search" class="searchbox" type="search" placeholder="Search ideas and topics…" autocomplete="off" aria-label="Search knowledge cards" value="${escapeHTML(searchTerm)}">
      <div class="chips" id="category-chips" aria-label="Filter by category">${CATEGORIES.map(cat=>`<button class="chip ${selection===cat?'selected':''}" data-cat="${escapeHTML(cat)}" aria-pressed="${selection===cat}">${escapeHTML(cat)}</button>`).join('')}</div>
      <p class="count-label" id="results-count"></p>
      <div class="cards" id="discover-results"></div>
    </div>`;
    refreshDiscover();
  }
  function refreshDiscover() {
    const term = searchTerm.toLocaleLowerCase();
    const ideas = allIdeas().filter(idea => (selection==='All'||idea.category===selection)
      && [idea.title,idea.hook,idea.body,idea.category,idea.takeaway].some(x=>x.toLocaleLowerCase().includes(term)));
    document.getElementById('results-count').textContent = `${ideas.length} ${ideas.length===1?'idea':'ideas'} available`;
    document.getElementById('discover-results').innerHTML = ideas.length ? ideas.map(ideaCard).join('') :
      empty('⌕','No matching ideas','Try another search or choose a different category.');
  }

  function renderStash() {
    const ideas = allIdeas().filter(idea => isSaved(idea.id));
    app.innerHTML = `<div class="page">
      ${heading('Your personal collection','My Stash.','Save the ideas you want to return to.')}
      <div class="section-head"><h2>${ideas.length} saved ${ideas.length===1?'idea':'ideas'}</h2><button class="text-link" data-action="add">＋ Add idea</button></div>
      <div class="cards">${ideas.length ? ideas.map(ideaCard).join('') : empty('▣','Nothing saved yet','Find a topic you like and tap “Save” while reading.', '<a href="#discover" class="primary">Explore ideas →</a>')}</div>
    </div>`;
  }

  function renderReview() {
    const due = dueIdeas();
    const upcoming = allIdeas().filter(idea=>state.reviews?.[idea.id]?.due && state.reviews[idea.id].due > dateKey())
      .sort((a,b)=>state.reviews[a.id].due.localeCompare(state.reviews[b.id].due)).slice(0,4);
    app.innerHTML = `<div class="page">
      ${heading('Keep what you learn','Review & remember.','A small reminder today makes an idea easier to recall later.')}
      <div class="progress-card" style="margin-top:19px">
        <div class="progress-header"><strong>Ready to review</strong><span>${due.length} due</span></div>
        <p class="subtext" style="margin:0">Ideas come back after 1, 3, 7, 14 and 30 days. Try recalling each idea before opening the card, then check yourself.</p>
      </div>
      <div class="section-head"><h2>Due today</h2></div>
      <div class="cards">${due.length ? due.map(ideaCard).join('') : empty('✓',"You're all caught up",'When you mark an idea as learned, it will appear here for review tomorrow.', '<a href="#discover" class="primary">Learn something new →</a>')}</div>
      ${upcoming.length ? `<div class="section-head"><h2>Coming up</h2></div><div class="cards">${upcoming.map(ideaCard).join('')}</div>`:''}
    </div>`;
  }

  function render() {
    document.documentElement.classList.toggle('dark', state.theme === 'dark');
    const route = location.hash.replace('#','') || 'today';
    const current = ['today','discover','stash','review'].includes(route)?route:'today';
    document.querySelectorAll('[data-tab]').forEach(el => {
      const active = el.dataset.tab === current;
      el.classList.toggle('active',active);
      if (active) el.setAttribute('aria-current','page'); else el.removeAttribute('aria-current');
    });
    ({today:renderToday,discover:renderDiscover,stash:renderStash,review:renderReview})[current]();
  }

  function showDialog(content, label) {
    returnFocus = document.activeElement;
    dialog.innerHTML = content;
    dialog.setAttribute('aria-label',label);
    overlay.hidden = false;
    document.body.style.overflow = 'hidden';
    dialog.querySelector('[data-action="close"]')?.focus();
  }
  function closeDialog() {
    overlay.hidden = true;
    dialog.innerHTML = '';
    document.body.style.overflow = '';
    if (returnFocus?.isConnected) returnFocus.focus();
  }
  function dialogHeader(title) {
    return `<div class="dialog-head"><span class="kicker">${title}</span><button class="close-button" data-action="close" aria-label="Close">×</button></div>`;
  }
  function openIdea(id) {
    const idea = byId(id); if (!idea) return;
    const due = state.reviews?.[id]?.due <= dateKey();
    showDialog(`${dialogHeader('2-minute learning card')}
      <span class="badge">${escapeHTML(idea.category)}</span>
      <h2 class="detail-title">${escapeHTML(idea.title)}</h2>
      <p class="detail-hook">${escapeHTML(idea.hook)}</p>
      <div class="detail-section"><small>The idea</small><p>${escapeHTML(idea.body)}</p></div>
      <div class="detail-section"><small>Real-world example</small><p>${escapeHTML(idea.example)}</p></div>
      <div class="detail-section takeaway"><small>Key takeaway</small><p>${escapeHTML(idea.takeaway)}</p></div>
      <div class="detail-section"><small>Think a little deeper</small><p>${escapeHTML(idea.question)}</p></div>
      <div class="actions">
        <button class="secondary" data-save="${escapeHTML(id)}">${isSaved(id)?'✓ Saved':'▣ Save idea'}</button>
        ${!isLearned(id)?`<button class="primary" data-learn="${escapeHTML(id)}">✓ Mark learned</button>`:
        due?`<button class="primary" data-review="${escapeHTML(id)}" data-result="good">✓ I remembered</button>
             <button class="secondary" data-review="${escapeHTML(id)}" data-result="again">↻ Review tomorrow</button>`:
           `<button class="secondary" disabled>✓ Learned · Next review ${escapeHTML(state.reviews[id]?.due||'soon')}</button>`}
      </div>`, idea.title);
  }
  function toggleSaved(id) {
    if (!byId(id)) return;
    state.saved ||= [];
    if (isSaved(id)) { state.saved = state.saved.filter(x=>x!==id); notify('Removed from My Stash'); }
    else { state.saved.push(id); notify('Saved to My Stash'); }
    persist(); render(); openIdea(id);
  }
  function learn(id) {
    if (!byId(id) || isLearned(id)) return;
    state.learned[id] = dateKey();
    state.reviews[id] = {step:0, due:offsetDate(INTERVALS[0])};
    activity('learn'); persist(); render(); openIdea(id);
    notify('Idea learned. You’ll review it tomorrow.');
  }
  function review(id, result) {
    const record = state.reviews?.[id];
    if (!record || record.due > dateKey()) return;
    record.step = result === 'good' ? Math.min((Number(record.step)||0)+1, INTERVALS.length-1) : 0;
    record.due = offsetDate(INTERVALS[record.step]);
    activity('review'); persist(); render(); closeDialog();
    notify(result==='good'?'Well remembered! Review scheduled.':'No problem. Try again tomorrow.');
  }

  function addModal() {
    showDialog(`${dialogHeader('Build your collection')}
      <h2 style="font-size:24px;letter-spacing:-.65px;margin-bottom:5px">Add a new idea</h2>
      <p class="subtext">Write one yourself, or use ChatGPT to create more.</p>
      <form id="add-form">
        <label class="form-field">Title *<input name="title" maxlength="110" required placeholder="e.g. Why friction matters"></label>
        <label class="form-field">Category <select name="category">${CATEGORIES.slice(1).map(x=>`<option>${escapeHTML(x)}</option>`).join('')}</select></label>
        <label class="form-field">Interesting opening *<textarea name="hook" maxlength="250" required placeholder="One sentence that makes me curious"></textarea></label>
        <label class="form-field">Explanation *<textarea name="body" maxlength="1600" required placeholder="Explain the concept clearly"></textarea></label>
        <label class="form-field">Real-world example <textarea name="example" maxlength="900" placeholder="How does this appear in real life?"></textarea></label>
        <label class="form-field">Key takeaway *<textarea name="takeaway" maxlength="300" required placeholder="What should I remember?"></textarea></label>
        <label class="form-field">Reflection question <input name="question" maxlength="300" placeholder="What could I explore next?"></label>
        <button class="primary" style="width:100%" type="submit">＋ Add to library</button>
      </form>
      <div class="hint-panel"><h3>✦ Generate ideas in ChatGPT, free</h3>
        <p>Copy a ready-made prompt. Ask ChatGPT for JSON learning cards, then paste the result below. No API key or payment needed.</p>
        <button class="secondary" data-action="copy-prompt">Copy ChatGPT prompt</button>
        <label class="form-field" style="margin-bottom:8px">Paste JSON array<textarea id="bulk-input" rows="4" placeholder='[{"title":"...","category":"Science","hook":"...","body":"...","example":"...","takeaway":"...","question":"..."}]'></textarea></label>
        <button class="secondary" data-action="import-cards">Import generated cards</button>
        <p class="form-hint" style="margin:8px 0 0">Tip: Review generated facts for accuracy before saving.</p>
      </div>`, 'Add a new idea');
  }
  function validateIdea(source) {
    if (!source || typeof source !== 'object') return null;
    const title = textValue(source.title,110), hook = textValue(source.hook,250);
    const body = textValue(source.body,1600), takeaway = textValue(source.takeaway,300);
    if (!title || !hook || !body || !takeaway) return null;
    const category = CATEGORIES.includes(source.category)&&source.category!=='All'?source.category:'Science';
    return {id:`own-${Date.now()}-${Math.floor(Math.random()*1e9)}`,title,hook,body,takeaway,category,
      example:textValue(source.example,900)||'Think of a situation where this idea appears.',
      question:textValue(source.question,300)||'Where might this idea be useful?'};
  }
  function createIdea(form) {
    const idea = validateIdea(Object.fromEntries(new FormData(form).entries()));
    if (!idea) {notify('Complete the required fields.');return;}
    state.custom.push(idea); persist(); closeDialog(); location.hash = '#stash';
    state.saved ||= []; state.saved.push(idea.id); persist(); render();
    notify('Idea added and saved.');
  }
  const CARD_PROMPT = `Create 5 accurate, fascinating, beginner-friendly microlearning cards about [TOPIC]. Each card should be readable in roughly 1–2 minutes. Return ONLY a valid JSON array, no markdown fences. Each object must have exactly these string fields: "title", "category", "hook", "body", "example", "takeaway", "question". Allowed categories: Psychology, Science, Engineering, Space, Philosophy, Business, Faith & ideas, History. Make each explanation specific, not generic; distinguish established facts from hypotheses and avoid made-up statistics. Max 1,000 characters for "body". I will paste this JSON into my offline Knowledge Stash app.`;
  async function copyPrompt() {
    try { await navigator.clipboard.writeText(CARD_PROMPT); notify('Prompt copied. Paste it into ChatGPT.'); }
    catch { showDialog(`${dialogHeader('Copy this ChatGPT prompt')}<textarea class="searchbox" readonly style="height:280px">${escapeHTML(CARD_PROMPT)}</textarea>`, 'ChatGPT prompt'); }
  }
  function bulkImport() {
    const input = document.getElementById('bulk-input');
    try {
      const value = JSON.parse(input.value.trim());
      if (!Array.isArray(value) || !value.length || value.length>100) throw Error('Need an array of 1–100 cards');
      const valid = value.map(validateIdea);
      if (valid.some(x=>!x)) throw Error('Each card needs title, hook, body and takeaway');
      state.custom.push(...valid);
      persist(); closeDialog(); location.hash = '#discover'; render();
      notify(`Imported ${valid.length} learning ${valid.length===1?'card':'cards'}!`);
    } catch (error) {notify(`Import failed: ${String(error.message).slice(0,80)}`);}
  }
  function settingsModal() {
    showDialog(`${dialogHeader('Preferences and data')}
      <h2 style="font-size:24px;margin-bottom:5px">Settings</h2>
      <p class="subtext">Everything stays on this device unless you export a backup.</p>
      <div class="toggle-row"><label for="dark-toggle">Dark mode</label><input id="dark-toggle" type="checkbox" ${state.theme==='dark'?'checked':''}></div>
      <div class="section-head"><h2>Your data</h2></div>
      <p class="subtext">${allIdeas().length} cards (${state.custom.length} added by you), ${state.saved.length} saved, ${Object.keys(state.learned).length} learned.</p>
      <div class="actions"><button class="primary" data-action="export">↓ Export backup</button><button class="secondary" data-action="choose-backup">↑ Restore backup</button></div>
      <input hidden type="file" id="backup-file" accept="application/json,.json">
      <p class="form-hint" style="margin:10px 0 20px">Backups are JSON files. Restoring replaces data currently saved in this browser.</p>
      <div class="hint-panel"><h3>Free & private by design</h3><p>No ads, logins, analytics or external APIs. Your saved ideas and learning progress are stored locally in your browser. They will not sync automatically between phones.</p></div>
      <button class="secondary" data-action="reset" style="color:#d26364">Delete my saved data</button>
    `, 'Settings');
  }
  function exportBackup() {
    const blob = new Blob([JSON.stringify({format:'knowledge-stash-backup',version:1,exported: new Date().toISOString(),state},null,2)],{type:'application/json'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a'); link.href=url;link.download=`knowledge-stash-backup-${dateKey()}.json`;
    document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),5000);
    notify('Backup exported. Keep it somewhere safe.');
  }
  async function restoreBackup(file) {
    try {
      if (file.size>3_000_000) throw Error('File is too large');
      const json = JSON.parse(await file.text());
      if (json.format!=='knowledge-stash-backup' || json.version!==1 || typeof json.state!=='object') throw Error('Not a Knowledge Stash backup');
      if (!confirm('Replace the learning data stored on this device with this backup?')) return;
      const incoming = json.state;
      const custom = (Array.isArray(incoming.custom)?incoming.custom:[]).slice(0,500).map(raw=>{
        const idea = validateIdea(raw);
        if (idea && typeof raw?.id === 'string' && /^own-\d+-\d+$/.test(raw.id)) idea.id = raw.id;
        return idea;
      }).filter(Boolean);
      const validIds = new Set([...window.STARTER_IDEAS,...custom].map(x=>x.id));
      const safeObject = value => value&&typeof value==='object'&&!Array.isArray(value)?value:{};
      state = {
        saved:(Array.isArray(incoming.saved)?incoming.saved:[]).filter(x=>validIds.has(x)),
        learned:Object.fromEntries(Object.entries(safeObject(incoming.learned)).filter(([id,v])=>validIds.has(id)&&typeof v==='string')),
        reviews:Object.fromEntries(Object.entries(safeObject(incoming.reviews)).filter(([id,v])=>validIds.has(id)&&v&&typeof v.due==='string'&&/\d{4}-\d\d-\d\d/.test(v.due)).map(([id,v])=>[id,{step:Math.max(0,Math.min(4,Number(v.step)||0)),due:v.due}])),
        history:(Array.isArray(incoming.history)?incoming.history:[]).filter(x=>x&&typeof x.day==='string'&&/^\d{4}-\d\d-\d\d$/.test(x.day)).slice(-1200),
        custom,theme:incoming.theme==='dark'?'dark':'light'
      };
      persist();closeDialog();render();notify('Backup restored.');
    } catch (err) { notify(`Restore failed: ${String(err.message).slice(0,80)}`); }
  }
  function reset() {
    if (!confirm('Delete all saved ideas, custom cards and learning progress from this device? Export a backup first if you want to keep them.')) return;
    state = freshState(); persist(); closeDialog();render();notify('Local learning data cleared.');
  }

  document.getElementById('open-add').addEventListener('click',addModal);
  document.getElementById('open-settings').addEventListener('click',settingsModal);
  window.addEventListener('hashchange',()=>{closeDialog();render();window.scrollTo(0,0);});
  document.addEventListener('keydown', event=>{if(event.key==='Escape'&&!overlay.hidden)closeDialog();});
  overlay.addEventListener('click',event=>{if(event.target===overlay)closeDialog();});
  document.addEventListener('submit',event=>{
    if (event.target.id==='add-form') {event.preventDefault();createIdea(event.target);}
  });
  document.addEventListener('input',event=>{
    if(event.target.id==='search'){searchTerm=event.target.value;refreshDiscover();}
  });
  document.addEventListener('change',event=>{
    if(event.target.id==='dark-toggle'){state.theme=event.target.checked?'dark':'light';persist();document.documentElement.classList.toggle('dark',state.theme==='dark');}
    if(event.target.id==='backup-file' && event.target.files?.[0]) restoreBackup(event.target.files[0]);
  });
  document.addEventListener('click', event=>{
    const opened = event.target.closest('[data-open]'); if(opened) {openIdea(opened.dataset.open);return;}
    const save = event.target.closest('[data-save]'); if(save) {toggleSaved(save.dataset.save);return;}
    const learnButton = event.target.closest('[data-learn]'); if(learnButton) {learn(learnButton.dataset.learn);return;}
    const reviewButton = event.target.closest('[data-review]'); if(reviewButton) {review(reviewButton.dataset.review, reviewButton.dataset.result);return;}
    const chip = event.target.closest('[data-cat]');
    if(chip){selection=chip.dataset.cat;document.querySelectorAll('[data-cat]').forEach(el=>{const yes=el.dataset.cat===selection;el.classList.toggle('selected',yes);el.setAttribute('aria-pressed',yes);});refreshDiscover();return;}
    const action = event.target.closest('[data-action]')?.dataset.action;
    if(!action)return;
    if(action==='close')closeDialog();
    if(action==='add')addModal();
    if(action==='copy-prompt')copyPrompt();
    if(action==='import-cards')bulkImport();
    if(action==='export')exportBackup();
    if(action==='choose-backup')document.getElementById('backup-file')?.click();
    if(action==='reset')reset();
  });

  if(!location.hash) history.replaceState(null,'','#today');
  render();
  if ('serviceWorker' in navigator && ['http:','https:'].includes(location.protocol)) {
    window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(err=>console.warn('Offline cache unavailable',err)));
  }
})();
