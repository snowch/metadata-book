/* A focused, ordered fan: each relationship has its own row and card port. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const ROW = 78;
  const PADDING = 24;
  const CARD_WIDTH = 200;
  const CARD_HEIGHT = 60;
  let instance = 0;

  function svgElement(name, attributes = {}) {
    const node = document.createElementNS(NS, name);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  }

  function wrapLabel(svg, value) {
    const measure = svgElement('text', {'font-size': 12.5, 'font-family': 'var(--sans, sans-serif)'});
    svg.append(measure);
    const textWidth = text => {
      measure.textContent = text;
      return measure.getComputedTextLength() || text.length * 6.5;
    };
    const lines = [];
    let line = '';
    String(value).split(/\s+/).forEach(word => {
      const next = line ? `${line} ${word}` : word;
      if (line && textWidth(next) > 180) {
        lines.push(line);
        line = word;
      } else line = next;
    });
    if (line) lines.push(line);
    const result = {lines, width: Math.ceil(Math.max(0, ...lines.map(textWidth))) + 12, height: Math.max(1, lines.length) * 15 + 8};
    measure.remove();
    return result;
  }

  function place(node, left, top, height) {
    Object.assign(node.style, {
      position: 'absolute', boxSizing: 'border-box',
      left: `${left}px`, top: `${top}px`,
      width: `${CARD_WIDTH}px`, height: `${height}px`
    });
  }

  window.layoutMetadataFocus = function (svg, canvas, focusNodes, edges, selected) {
    svg.replaceChildren();
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    const selectedNode = focusNodes.get(selected);
    if (!selectedNode) return;
    const relationships = edges.filter(edge => (edge.from === selected || edge.to === selected) && edge.from !== edge.to && focusNodes.has(edge.from) && focusNodes.has(edge.to));
    const count = relationships.length;
    const width = Math.max(760, canvas.clientWidth);
    const height = PADDING * 2 + Math.max(160, count * ROW);
    const selectedHeight = Math.max(160, count * 28 + 40);
    const selectedX = width - PADDING - CARD_WIDTH;
    const centerY = height / 2;
    const leftEnd = PADDING + CARD_WIDTH;
    const gap = selectedX - leftEnd;
    const curveStart = leftEnd + Math.min(gap - 74, Math.max(220, gap * .72));
    const curveEnd = selectedX - 14;
    const control1 = curveStart + (curveEnd - curveStart) * .42;
    const control2 = curveStart + (curveEnd - curveStart) * .78;
    const labelX = (leftEnd + curveStart) / 2;
    canvas.style.position = 'relative';
    canvas.style.height = `${height}px`;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
    place(selectedNode, selectedX, centerY - selectedHeight / 2, selectedHeight);

    const markerId = `map-focus-arrow-${++instance}`;
    const defs = svgElement('defs');
    const marker = svgElement('marker', {id: markerId, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 9, markerHeight: 9, orient: 'auto', markerUnits: 'userSpaceOnUse'});
    marker.append(svgElement('path', {d: 'M 0 1 L 9 5 L 0 9 Z', fill: 'var(--accent, #a44932)'}));
    defs.append(marker);
    const paths = svgElement('g', {class: 'map-connection-lines'});
    const labels = svgElement('g', {class: 'map-connection-labels'});
    svg.append(defs, paths, labels);

    relationships.forEach((edge, index) => {
      const neighbor = edge.from === selected ? edge.to : edge.from;
      const rowY = centerY + (index - (count - 1) / 2) * ROW;
      const portY = centerY + (index - (count - 1) / 2) * 28;
      place(focusNodes.get(neighbor), PADDING, rowY - CARD_HEIGHT / 2, CARD_HEIGHT);
      // Common x coordinates and matching row/port order keep every curve
      // disjoint. Reverse outgoing paths so the arrowhead preserves direction.
      const incoming = edge.to === selected;
      const d = incoming
        ? `M ${leftEnd} ${rowY} L ${curveStart} ${rowY} C ${control1} ${rowY} ${control2} ${portY} ${curveEnd} ${portY} L ${selectedX} ${portY}`
        : `M ${selectedX} ${portY} L ${curveEnd} ${portY} C ${control2} ${portY} ${control1} ${rowY} ${curveStart} ${rowY} L ${leftEnd} ${rowY}`;
      paths.append(svgElement('path', {
        class: 'map-connection', 'data-from': edge.from, 'data-to': edge.to,
        d, fill: 'none', stroke: 'var(--accent, #a44932)', 'stroke-width': 1.8,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'marker-end': `url(#${markerId})`
      }));
      const size = wrapLabel(svg, edge.label);
      const label = svgElement('g', {class: 'map-connection-label', 'data-from': edge.from, 'data-to': edge.to, transform: `translate(${labelX}, ${rowY})`});
      label.append(svgElement('rect', {x: -size.width / 2, y: -size.height / 2, width: size.width, height: size.height, rx: 3, fill: 'var(--surface, #fffdf8)', stroke: 'var(--line, #d9d5cc)', 'stroke-width': .7}));
      const text = svgElement('text', {'text-anchor': 'middle', fill: 'var(--accent, #a44932)', 'font-size': 12.5, 'font-family': 'var(--sans, sans-serif)'});
      size.lines.forEach((line, lineIndex) => {
        const span = svgElement('tspan', {x: 0, y: -(size.lines.length - 1) * 7.5 + 4.5 + lineIndex * 15});
        span.textContent = line;
        text.append(span);
      });
      label.append(text);
      labels.append(label);
    });
  };
})();

/* Precomputed whole-graph layout: no layout engine or downloads in the browser. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const make = (name, attributes = {}) => {
    const node = document.createElementNS(NS, name);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  };
  window.layoutMetadataWhole = (svg, canvas, nodes, layout, selected) => {
    canvas.style.height = `${layout.height}px`;
    svg.replaceChildren();
    svg.setAttribute('viewBox', `0 0 ${layout.width} ${layout.height}`);
    svg.setAttribute('width', layout.width);
    svg.setAttribute('height', layout.height);
    Object.entries(layout.nodes).forEach(([id, rect]) => {
      Object.assign(nodes.get(id).style, {left: `${rect.x}px`, top: `${rect.y}px`, width: `${rect.width}px`, height: `${rect.height}px`});
    });
    const defs = make('defs');
    for (const [id, color] of [['whole-active', 'var(--accent)'], ['whole-context', 'var(--muted)']]) {
      const marker = make('marker', {id, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 9, markerHeight: 9, orient: 'auto', markerUnits: 'userSpaceOnUse'});
      marker.append(make('path', {d: 'M 0 1 L 9 5 L 0 9 Z', fill: color}));
      defs.append(marker);
    }
    const paths = make('g'), labels = make('g');
    svg.append(defs, paths, labels);
    // Draw highlighted relationships last so they stay clear at crossings.
    const active = edge => edge.from === selected || edge.to === selected;
    [...layout.edges].sort((a, b) => Number(active(a)) - Number(active(b))).forEach(edge => {
      const highlighted = active(edge);
      const color = highlighted ? 'var(--accent)' : 'var(--muted)';
      const attrs = {'data-from': edge.from, 'data-to': edge.to, 'data-highlighted': String(highlighted)};
      paths.append(make('path', {...attrs, class: 'map-connection', d: edge.path, fill: 'none', stroke: color, 'stroke-width': highlighted ? 2.3 : 1.25, 'marker-end': `url(#whole-${highlighted ? 'active' : 'context'})`}));
      const label = make('g', {...attrs, class: 'map-connection-label', transform: `translate(${edge.labelX},${edge.labelY})`});
      label.append(make('rect', {x: -edge.labelWidth / 2 - 4, y: -edge.labelHeight / 2 - 3, width: edge.labelWidth + 8, height: edge.labelHeight + 6, rx: 3, fill: 'var(--surface)'}));
      const text = make('text', {'text-anchor': 'middle', fill: color, 'font-size': 13, 'font-family': 'var(--sans, sans-serif)'});
      edge.labelLines.forEach((line, i) => {
        const span = make('tspan', {x: 0, y: (i - (edge.labelLines.length - 1) / 2) * 16 + 4.5});
        span.textContent = line;
        text.append(span);
      });
      label.append(text);
      labels.append(label);
    });
  };
})();
