// Build-time data-driven renderer for medaffairs.tech
// Expects a data/articles.json present in the repo (populated by the sync workflow).
// Title selection: manual_title -> generated_title -> original_title.

// Path to local data file (bundled at build-time by the workflow)
const LOCAL_DATA_PATH = 'data/articles.json';

function displayTitle(a){
  if (a.manual_title && a.manual_title.trim()) return a.manual_title;
  if (a.generated_title && a.generated_title.trim()) return a.generated_title;
  return a.original_title || 'Untitled';
}

function formatDate(ms){
  try{ return new Date(ms).toLocaleString(); } catch(e) { return ''; }
}

function createHeroNode(h){
  const div = document.createElement('div');
  div.className = 'hero';
  const img = document.createElement('img');
  img.src = h.image || 'https://via.placeholder.com/180x150?text=+';
  img.alt = '';
  const meta = document.createElement('div');
  const a = document.createElement('a');
  a.className = 'hlink';
  a.href = h.url;
  a.target = '_blank';
  a.rel = 'noopener noreferrer';
  a.textContent = displayTitle(h);
  meta.appendChild(a);
  div.appendChild(img);
  div.appendChild(meta);
  return div;
}

function createListItemNode(it){
  const li = document.createElement('li');
  const a = document.createElement('a');
  a.href = it.url;
  a.target = '_blank';
  a.rel = 'noopener noreferrer';
  a.textContent = displayTitle(it);
  li.appendChild(a);
  const s = document.createElement('span');
  s.className = 'source';
  s.textContent = `${it.source || ''}${it.source ? ' • ' : ''}${formatDate(it.published_at)}`;
  li.appendChild(s);
  return li;
}

function render(data){
  if(!data) return;
  // update last updated
  const lu = document.getElementById('last-updated');
  if (lu) lu.textContent = formatDate(data.last_updated);

  // heroes (3)
  const heroStrip = document.getElementById('hero-strip');
  heroStrip.innerHTML = '';
  const heroes = (data.heroes || []).slice(0,3);
  if (heroes.length === 0) {
    heroStrip.innerHTML = '';
  } else {
    for (const h of heroes) heroStrip.appendChild(createHeroNode(h));
  }

  // columns
  const mapping = { news: 'news-list', tech: 'tech-list', opinion: 'opinion-list' };
  for (const col of Object.keys(mapping)){
    const el = document.getElementById(mapping[col]);
    el.innerHTML = '';
    const items = (data.columns && data.columns[col]) || [];
    for (const it of items) el.appendChild(createListItemNode(it));
  }
}

// Load local JSON (synchronous fetch will be fine for static pages)
fetch(LOCAL_DATA_PATH)
  .then(r => {
    if (!r.ok) throw new Error('Missing data file');
    return r.json();
  })
  .then(render)
  .catch(err => {
    console.error(err);
    document.getElementById('hero-strip').innerHTML = '<div style="padding:12px;color:#666">Data not available. Try refreshing in a moment.</div>';
  });