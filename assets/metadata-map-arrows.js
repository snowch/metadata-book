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
