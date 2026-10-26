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
