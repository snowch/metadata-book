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
  const compact = window.matchMedia('(max-width: 1199px)');
  const explorer = root.querySelector('.map-explorer');
  const paneTabs = root.querySelector('.map-section-tabs');
  const paneButtons = [...paneTabs.querySelectorAll('[data-pane]')];
  const selection = root.querySelector('.map-selection');
  let focusNodes = new Map();
  const focusLayer = root.querySelector('.map-focus-nodes');
  const svg = root.querySelector('.map-connections');
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
  let pane = initial.get('panel') === 'details' || records.has(hashRecord) ? 'details' : 'map';
  let mapPosition = {y: 0, left: 0, top: 0};
  let scale = 1;
  let fitToWidth = true;
  let currentTab = 'example';
  let drawPending = false;
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const chapterMatch = id => chapter === 'all' || records.get(id).chapters.some(item => String(item.number) === chapter);
  const relationships = () => data.relationships.filter(edge =>
    (edge.from === selected || edge.to === selected) && records.has(edge.from) && records.has(edge.to));

  function saveState() {
    const url = new URL(window.location.href);
    if (origin) url.searchParams.set('chapter', origin); else url.searchParams.delete('chapter');
    if (chapter === (origin || 'all')) url.searchParams.delete('focus'); else url.searchParams.set('focus', chapter);
    url.searchParams.set('record', selected);
    url.searchParams.set('view', view);
    if (pane === 'details') url.searchParams.set('panel', pane); else url.searchParams.delete('panel');
    if (url.hash.startsWith('#record-')) url.hash = '';
    window.history.replaceState(null, '', url);
  }

  function applyPane() {
    const tabbed = compact.matches;
    paneTabs.hidden = !tabbed;
    root.dataset.pane = pane;
    paneButtons.forEach(button => {
      const active = button.dataset.pane === pane;
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
    });
    for (const [name, item] of [['map', explorer], ['details', panel]]) {
      item.hidden = tabbed && pane !== name;
      if (tabbed) {
        item.setAttribute('role', 'tabpanel');
        item.setAttribute('aria-labelledby', `map-section-${name}`);
      } else {
        item.removeAttribute('role');
        item.removeAttribute('aria-labelledby');
      }
    }
    scheduleDraw();
  }

  function showPane(next, focusContent = false) {
    const changing = pane !== next;
    if (changing && pane === 'map' && compact.matches) {
      mapPosition = {y: window.scrollY, left: viewport.scrollLeft, top: viewport.scrollTop};
    }
    pane = next;
    applyPane();
    saveState();
    requestAnimationFrame(() => {
      if (compact.matches && changing) {
        if (pane === 'map') {
          viewport.scrollLeft = mapPosition.left;
          viewport.scrollTop = mapPosition.top;
          window.scrollTo({top: mapPosition.y, behavior: 'instant'});
        } else paneTabs.scrollIntoView({block: 'start'});
      }
      if (focusContent) {
        const target = pane === 'map' ? (view === 'map' ? focusNodes.get(selected).querySelector('[data-focus-record]') : nodes.get(selected).querySelector('[data-select-record]')) : panel.querySelector('h2');
        target.focus({preventScroll: compact.matches});
      }
    });
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
    const backToRecords = element('button', '← Back to map', 'map-back-to-records');
    backToRecords.type = 'button';
    backToRecords.addEventListener('click', () => showPane('map', true));
    panel.replaceChildren(backToRecords, content);
    panel.scrollTop = 0;
  }

  function renderFocus() {
    const related = new Set([selected, ...relationships().flatMap(edge => [edge.from, edge.to])]);
    focusLayer.replaceChildren();
    focusNodes = new Map();
    related.forEach(id => {
      const node = nodes.get(id).cloneNode(true);
      node.className = 'map-focus-node';
      node.classList.toggle('is-selected', id === selected);
      node.classList.toggle('is-chapter', chapter !== 'all' && chapterMatch(id));
      delete node.dataset.node;
      node.dataset.focusNode = id;
      const button = node.querySelector('[data-select-record]');
      button.dataset.focusRecord = id;
      delete button.dataset.selectRecord;
      button.className = 'map-focus-select';
      button.removeAttribute('aria-pressed');
      if (id === selected) {
        button.prepend(element('span', 'Selected record type', 'map-focus-kicker'));
        button.append(element('span', 'View example and fields →', 'map-focus-description'));
        button.setAttribute('aria-label', `View record: ${records.get(id).label}`);
      }
      focusLayer.append(node);
      focusNodes.set(id, node);
    });
  }

  function renderSummary() {
    summary.replaceChildren();
    const edges = relationships();
    summary.append(element('h2', `Connections · ${records.get(selected).label}`));
    summary.append(element('p', 'Relationships between record types. Linked example values in Record details connect matching records.'));
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
    summary.parentElement.hidden = false;
  }

  function updateNodes() {
    selection.querySelector('.map-selection-label').textContent = records.get(selected).label;
    selection.querySelector('button').setAttribute('aria-label', `View record: ${records.get(selected).label}`);
    nodes.forEach((node, id) => {
      const matching = chapterMatch(id);
      node.classList.toggle('is-selected', id === selected);
      node.classList.toggle('is-chapter', chapter !== 'all' && matching);
      node.classList.toggle('is-outside-chapter', chapter !== 'all' && !matching);
      const button = node.querySelector('[data-select-record]');
      button.setAttribute('aria-pressed', String(id === selected));
      button.setAttribute('aria-label', `${records.get(id).label}: ${id === selected ? 'selected record' : 'show connections'}${chapter !== 'all' && matching ? `; highlighted for Chapter ${chapter}` : ''}`);
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
    renderFocus();
    renderSummary();
    scheduleDraw();
    saveState();
    applyPane();
    if (intentional && focusDetail) showPane('details', true);
    else if (intentional && view === 'map') requestAnimationFrame(() => {
      focusNodes.get(selected).querySelector('[data-focus-record]').focus({preventScroll: true});
      viewport.scrollIntoView({block: 'nearest'});
    });
  }

  function applyView() {
    root.dataset.view = view;
    root.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === view)));
    zoomControls.hidden = view !== 'map';
    viewport.hidden = view !== 'map';
    summary.parentElement.open = view === 'list';
    viewport.setAttribute('aria-label', view === 'map' ? 'Record map. Scroll to explore the diagram.' : 'Records grouped by purpose');
    if (view === 'map') viewport.tabIndex = 0; else viewport.removeAttribute('tabindex');
    scheduleDraw();
  }

  function draw() {
    if (view !== 'map' || explorer.hidden) return;
    // Keep labels readable at normal zoom; narrower screens can scroll or use the list.
    canvas.style.width = `${Math.max(760, viewport.clientWidth - 2)}px`;
    window.layoutMetadataFocus(svg, canvas, focusNodes, relationships(), selected);
    const width = canvas.offsetWidth;
    const height = canvas.offsetHeight;
    if (fitToWidth) scale = Math.max(.25, Math.min(1, (viewport.clientWidth - 2) / width));
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
    const target = event.target.closest('[data-select-record], [data-record-target], [data-focus-record]');
    if (target && root.contains(target)) {
      event.preventDefault();
      const id = target.dataset.selectRecord || target.dataset.recordTarget || target.dataset.focusRecord;
      if (target.dataset.focusRecord === selected) showPane('details', true);
      else selectRecord(id, true, Boolean(target.closest('.map-detail')));
    }
  });
  selection.querySelector('button').addEventListener('click', () => showPane('details', true));
  paneButtons.forEach(button => {
    button.addEventListener('click', () => showPane(button.dataset.pane));
    button.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? paneButtons[0] : event.key === 'End' ? paneButtons[1] : paneButtons.find(item => item !== button);
      showPane(next.dataset.pane);
      next.focus();
    });
  });
  compact.addEventListener('change', () => {
    applyPane();
    if (compact.matches && document.activeElement.closest('.map-explorer, .map-detail')?.hidden) {
      paneButtons.find(button => button.dataset.pane === pane).focus();
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
    fitToWidth = button.dataset.zoom === 'fit';
    if (fitToWidth) {
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
  selection.hidden = false;
  root.querySelector('.map-controls').hidden = false;
  root.querySelector('.map-tools').hidden = false;
  root.querySelector('.map-legend').hidden = false;
  applyView();
  selectRecord(selected);
  if (window.ResizeObserver) new ResizeObserver(scheduleDraw).observe(canvas);
  window.addEventListener('resize', scheduleDraw, {passive: true});
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(scheduleDraw);
})();
