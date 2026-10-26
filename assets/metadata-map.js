/* Progressive enhancement: no dependencies, requests, or generated HTML. */
(() => {
  'use strict';
  const root = document.querySelector('.metadata-map');
  const source = document.getElementById('metadata-map-data');
  if (!root || !source) return;
  let data;
  try { data = JSON.parse(source.textContent); } catch (_) { return; }
  if (!Array.isArray(data.records) || !data.records.length) return;
  const records = new Map(data.records.map(record => [record.id, record]));
  const chapters = new Map(data.chapters.map(chapter => [String(chapter.number), chapter]));
  const nodes = new Map([...root.querySelectorAll('[data-node]')].map(node => [node.dataset.node, node]));
  const fallback = new Map([...root.querySelectorAll('.map-fallback-record')].map(node => [node.id.slice(7), node]));
  const panel = root.querySelector('.map-detail');
  const viewport = root.querySelector('.map-viewport');
  const canvas = root.querySelector('.map-canvas');
  const frame = root.querySelector('.map-scale-frame');
  const filter = root.querySelector('#map-chapter-filter');
  const status = root.querySelector('.map-status');
  const summary = root.querySelector('.map-relationship-summary');
  const zoomControls = root.querySelector('.map-zoom-controls');
  const defaults = {1: 'metric-definition', 2: 'column', 3: 'report-refresh', 4: 'report-refresh', 5: 'source-observation', 6: 'source-observation', 7: 'quality-check', 8: 'decision'};
  const initial = new URLSearchParams(window.location.search);
  const origin = chapters.has(initial.get('chapter')) ? initial.get('chapter') : null;
  let chapter = chapters.has(initial.get('focus')) ? initial.get('focus') : initial.get('focus') === 'all' ? 'all' : origin || 'all';
  const preferred = chapter !== 'all' ? defaults[chapter] : 'report-refresh';
  const hashRecord = window.location.hash.startsWith('#record-') ? window.location.hash.slice(8) : null;
  let selected = records.has(initial.get('record')) ? initial.get('record') : records.has(hashRecord) ? hashRecord : records.has(preferred) ? preferred : data.records[0].id;
  let view = ['map', 'list'].includes(initial.get('view')) ? initial.get('view') : window.matchMedia('(max-width: 700px)').matches ? 'list' : 'map';
  let scale = 1;
  let currentTab = 'example';
  let drawPending = false;
  const trace = [['report-refresh', 'published-output', 'reads'], ['published-output', 'run', 'produced by'], ['run', 'input-snapshot', 'read'], ['run', 'code-version', 'executed']];
  const traceNodes = new Set(trace.flatMap(edge => edge.slice(0, 2)));

  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const chapterMatch = id => chapter === 'all' || records.get(id).chapters.some(item => String(item.number) === chapter);
  const relationships = () => traceNodes.has(selected)
    ? trace.filter(edge => records.has(edge[0]) && records.has(edge[1])).map(([from, to, label]) => ({from, to, label}))
    : data.relationships.filter(edge => (edge.from === selected || edge.to === selected) && records.has(edge.from) && records.has(edge.to));

  function saveState() {
    const url = new URL(window.location.href);
    if (origin) url.searchParams.set('chapter', origin); else url.searchParams.delete('chapter');
    if (chapter === (origin || 'all')) url.searchParams.delete('focus'); else url.searchParams.set('focus', chapter);
    url.searchParams.set('record', selected);
    url.searchParams.set('view', view);
    if (url.hash.startsWith('#record-')) url.hash = '';
    window.history.replaceState(null, '', url);
  }

  function renderDetail() {
    const original = fallback.get(selected);
    if (!original) return;
    const content = original.querySelector('.map-record-content').cloneNode(true);
    const tablist = content.querySelector('.map-detail-tabs');
    tablist.hidden = false;
    tablist.setAttribute('role', 'tablist');
    tablist.setAttribute('aria-label', 'Record information');
    const panels = {example: content.querySelector('.map-example-panel'), fields: content.querySelector('.map-fields-panel')};
    const buttons = [];
    const chooseTab = name => {
      currentTab = name;
      buttons.forEach(button => {
        const active = button.dataset.tab === name;
        button.setAttribute('aria-selected', String(active));
        button.tabIndex = active ? 0 : -1;
      });
      Object.entries(panels).forEach(([key, item]) => { item.hidden = key !== name; });
    };
    for (const [name, label] of [['example', 'Example'], ['fields', 'Fields & types']]) {
      const button = element('button', label);
      button.type = 'button';
      button.dataset.tab = name;
      button.id = `map-tab-${name}`;
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-controls', `map-panel-${name}`);
      panels[name].id = `map-panel-${name}`;
      panels[name].setAttribute('role', 'tabpanel');
      panels[name].setAttribute('aria-labelledby', button.id);
      button.addEventListener('click', () => chooseTab(name));
      button.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? buttons[0] : event.key === 'End' ? buttons[buttons.length - 1] : buttons.find(item => item !== button);
        chooseTab(next.dataset.tab);
        next.focus();
      });
      buttons.push(button);
      tablist.append(button);
    }
    chooseTab(currentTab);
    const backToRecords = element('button', '← Back to records', 'map-back-to-records');
    backToRecords.type = 'button';
    backToRecords.addEventListener('click', () => {
      const button = nodes.get(selected).querySelector('[data-select-record]');
      button.focus({preventScroll: true});
      button.scrollIntoView({block: 'center', inline: 'nearest'});
    });
    panel.replaceChildren(backToRecords, content);
    panel.hidden = false;
    panel.scrollTop = 0;
  }

  function renderSummary() {
    summary.replaceChildren();
    const edges = relationships();
    const explanation = traceNodes.has(selected)
      ? 'Report provenance: follow matching identifiers from the refresh to its output, run, inputs and code.'
      : 'Record-type relationships: these associations may refer to different examples.';
    summary.append(element('h2', traceNodes.has(selected) ? 'Follow the report’s evidence' : `Connections · ${records.get(selected).label}`));
    summary.append(element('p', explanation));
    const list = element('ul');
    edges.forEach(edge => {
      const item = element('li');
      for (const [id, prefix] of [[edge.from, ''], [edge.to, `${edge.label} →`]]) {
        if (prefix) item.append(element('span', prefix, 'map-relationship-verb'));
        const link = element('a', records.get(id).label);
        link.href = `#record-${id}`;
        link.dataset.recordTarget = id;
        item.append(link);
      }
      list.append(item);
    });
    if (!edges.length) list.append(element('li', 'Select a related record type in the details to continue exploring.'));
    summary.append(list);
    summary.hidden = false;
  }

  function updateNodes() {
    nodes.forEach((node, id) => {
      const matching = chapterMatch(id);
      node.classList.toggle('is-selected', id === selected);
      node.classList.toggle('is-chapter', chapter !== 'all' && matching);
      node.classList.toggle('is-outside-chapter', chapter !== 'all' && !matching);
      const button = node.querySelector('[data-select-record]');
      button.setAttribute('aria-pressed', String(id === selected));
      button.setAttribute('aria-label', `${records.get(id).label}: ${id === selected ? 'selected record' : 'view record'}${chapter !== 'all' && matching ? `; highlighted for Chapter ${chapter}` : ''}`);
    });
    const count = data.records.filter(record => chapterMatch(record.id)).length;
    status.textContent = chapter === 'all'
      ? `${data.records.length} record types · Selected: ${records.get(selected).label}`
      : `Chapter ${chapter}: ${count} highlighted · Selected: ${records.get(selected).label}`;
    filter.value = chapter;
  }

  function selectRecord(id, intentional = false, focusDetail = false) {
    if (!records.has(id)) return;
    selected = id;
    currentTab = 'example';
    updateNodes();
    renderDetail();
    renderSummary();
    scheduleDraw();
    saveState();
    const belowExplorer = window.matchMedia('(max-width: 1199px)').matches;
    if (intentional && (belowExplorer || focusDetail)) {
      requestAnimationFrame(() => {
        if (belowExplorer) panel.scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start'});
        panel.querySelector('h2').focus({preventScroll: belowExplorer});
      });
    }
  }

  function applyView() {
    root.dataset.view = view;
    root.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === view)));
    zoomControls.hidden = view !== 'map';
    viewport.setAttribute('aria-label', view === 'map' ? 'Record map. Scroll to explore the diagram.' : 'Records grouped by purpose');
    if (view === 'map') viewport.tabIndex = 0; else viewport.removeAttribute('tabindex');
    scheduleDraw();
  }

  function draw() {
    if (view !== 'map') return;
    // Keep labels readable at normal zoom; narrower screens can scroll or use the list.
    canvas.style.width = `${Math.max(660, viewport.clientWidth - 2)}px`;
    const width = canvas.offsetWidth;
    const height = canvas.offsetHeight;
    frame.style.width = `${width * scale}px`;
    frame.style.height = `${height * scale}px`;
    canvas.style.transform = `scale(${scale})`;
    root.querySelector('.map-zoom-value').textContent = `${Math.round(scale * 100)}%`;
  }

  function scheduleDraw() {
    if (drawPending) return;
    drawPending = true;
    requestAnimationFrame(() => { drawPending = false; draw(); });
  }

  nodes.forEach((node, id) => {
    const link = node.querySelector('[data-select-record]');
    const button = element('button');
    button.type = 'button';
    button.className = link.className;
    button.dataset.selectRecord = id;
    while (link.firstChild) button.append(link.firstChild);
    link.replaceWith(button);
  });
  root.addEventListener('click', event => {
    const target = event.target.closest('[data-select-record], [data-record-target]');
    if (target && root.contains(target)) {
      event.preventDefault();
      selectRecord(target.dataset.selectRecord || target.dataset.recordTarget, true, Boolean(target.dataset.recordTarget));
    }
  });
  filter.addEventListener('change', () => {
    chapter = chapters.has(filter.value) ? filter.value : 'all';
    const next = chapter === 'all' ? selected : chapterMatch(selected) ? selected : defaults[chapter];
    selectRecord(records.has(next) ? next : selected);
  });
  root.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => {
    view = button.dataset.view;
    applyView();
    saveState();
  }));
  root.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => {
    if (button.dataset.zoom === 'fit') {
      scale = Math.max(.25, Math.min(1, (viewport.clientWidth - 2) / canvas.offsetWidth));
      viewport.scrollLeft = 0;
      viewport.scrollTop = 0;
    } else scale = Math.max(.25, Math.min(1.5, Math.round((scale + (button.dataset.zoom === 'in' ? .1 : -.1)) * 100) / 100));
    scheduleDraw();
  }));
  if (origin) {
    const back = root.querySelector('.map-return');
    back.textContent = `← Back to Chapter ${origin}: ${chapters.get(origin).title}`;
    back.href = chapters.get(origin).href;
    back.hidden = false;
  }
  root.classList.add('is-ready');
  root.querySelector('.map-controls').hidden = false;
  root.querySelector('.map-legend').hidden = false;
  applyView();
  selectRecord(selected);
  if (window.ResizeObserver) new ResizeObserver(scheduleDraw).observe(canvas);
  window.addEventListener('resize', scheduleDraw, {passive: true});
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(scheduleDraw);
})();
