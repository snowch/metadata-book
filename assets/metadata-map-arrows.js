/* Measured, orthogonal connections for the existing record overview. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const CLEARANCE = 6;
  const STUB = 14;
  const BEND_COST = 96;
  const EPSILON = .05;
  let instance = 0;

  const svgElement = (name, attributes = {}) => {
    const item = document.createElementNS(NS, name);
    Object.entries(attributes).forEach(([key, value]) => item.setAttribute(key, value));
    return item;
  };
  const round = value => Math.round(value * 10) / 10;
  const inflate = (box, padding) => ({left: box.left - padding, top: box.top - padding, right: box.right + padding, bottom: box.bottom + padding});
  const overlaps = (a, b) => a.left < b.right - EPSILON && a.right > b.left + EPSILON && a.top < b.bottom - EPSILON && a.bottom > b.top + EPSILON;
  const distance = (a, b) => Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
  const inside = (point, box) => point.x > box.left + EPSILON && point.x < box.right - EPSILON && point.y > box.top + EPSILON && point.y < box.bottom - EPSILON;
  function crosses(a, b, box) {
    if (Math.abs(a.y - b.y) < EPSILON) {
      return a.y > box.top + EPSILON && a.y < box.bottom - EPSILON && Math.max(a.x, b.x) > box.left + EPSILON && Math.min(a.x, b.x) < box.right - EPSILON;
    }
    return a.x > box.left + EPSILON && a.x < box.right - EPSILON && Math.max(a.y, b.y) > box.top + EPSILON && Math.min(a.y, b.y) < box.bottom - EPSILON;
  }
  function simplify(points) {
    const result = [];
    points.forEach(point => {
      if (result.length && distance(result[result.length - 1], point) < EPSILON) return;
      while (result.length > 1) {
        const a = result[result.length - 2], b = result[result.length - 1];
        // Only merge points travelling in the same direction; retain U turns.
        if ((Math.abs(a.x - b.x) < EPSILON && Math.abs(b.x - point.x) < EPSILON && (b.y - a.y) * (point.y - b.y) >= 0) ||
            (Math.abs(a.y - b.y) < EPSILON && Math.abs(b.y - point.y) < EPSILON && (b.x - a.x) * (point.x - b.x) >= 0)) result.pop();
        else break;
      }
      result.push(point);
    });
    return result;
  }

  // A small binary heap keeps route searches responsive on the full overview.
  class Queue {
    constructor() { this.items = []; }
    push(item) {
      const items = this.items;
      let index = items.length;
      items.push(item);
      while (index) {
        const parent = (index - 1) >> 1;
        if (items[parent].priority <= item.priority) break;
        items[index] = items[parent];
        index = parent;
      }
      items[index] = item;
    }
    pop() {
      const items = this.items, first = items[0], last = items.pop();
      if (items.length) {
        let index = 0;
        while (index * 2 + 1 < items.length) {
          let child = index * 2 + 1;
          if (child + 1 < items.length && items[child + 1].priority < items[child].priority) child++;
          if (items[child].priority >= last.priority) break;
          items[index] = items[child];
          index = child;
        }
        items[index] = last;
      }
      return first;
    }
  }

  function ports(box) {
    const result = [];
    for (const fraction of [.5, .22, .78]) {
      const x = round(box.left + (box.right - box.left) * fraction);
      const y = round(box.top + (box.bottom - box.top) * fraction);
      const penalty = fraction === .5 ? 0 : 24;
      result.push(
        {x, y: box.top - STUB, anchor: {x, y: box.top}},
        {x, y: box.bottom + STUB, anchor: {x, y: box.bottom}},
        {x: box.left - STUB, y, anchor: {x: box.left, y}},
        {x: box.right + STUB, y, anchor: {x: box.right, y}}
      );
      result.slice(-4).forEach(port => { port.penalty = penalty; });
    }
    return result;
  }

  function grid(obstacles, allPorts, station, width, height) {
    const coordinates = (values, limit) => [...new Set(values.filter(value => value >= 2 && value <= limit - 2))].sort((a, b) => a - b);
    const xs = coordinates([2, width - 2, station.left, station.right, ...obstacles.flatMap(box => [box.left, box.right]), ...allPorts.map(point => point.x)], width);
    const ys = coordinates([2, height - 2, station.y, ...obstacles.flatMap(box => [box.top, box.bottom]), ...allPorts.map(point => point.y)], height);
    const xIndex = new Map(xs.map((x, index) => [x, index]));
    const yIndex = new Map(ys.map((y, index) => [y, index]));
    const point = index => ({x: xs[index % xs.length], y: ys[Math.floor(index / xs.length)]});
    const index = p => yIndex.get(p.y) * xs.length + xIndex.get(p.x);
    const valid = new Int8Array(xs.length * ys.length);
    const links = new Map();
    function neighbors(current) {
      if (links.has(current)) return links.get(current);
      const p = point(current), x = current % xs.length, y = Math.floor(current / xs.length);
      const next = [];
      for (const candidate of [x > 0 ? current - 1 : -1, x + 1 < xs.length ? current + 1 : -1, y > 0 ? current - xs.length : -1, y + 1 < ys.length ? current + xs.length : -1]) {
        if (candidate < 0) continue;
        const q = point(candidate);
        if (!valid[candidate]) valid[candidate] = obstacles.some(box => inside(q, box)) ? -1 : 1;
        if (valid[candidate] < 0 || obstacles.some(box => crosses(p, q, box))) continue;
        next.push({index: candidate, point: q, direction: Math.abs(p.y - q.y) < EPSILON ? 0 : 1, length: distance(p, q)});
      }
      links.set(current, next);
      return next;
    }
    return {point, index, neighbors, size: xs.length * ys.length};
  }

  function trafficPenalty(a, b, segments) {
    let cost = 0;
    for (const [c, d] of segments) {
      const horizontal = Math.abs(a.y - b.y) < EPSILON;
      const otherHorizontal = Math.abs(c.y - d.y) < EPSILON;
      if (horizontal === otherHorizontal) {
        if (Math.abs((horizontal ? a.y : a.x) - (horizontal ? c.y : c.x)) > 2) continue;
        const overlap = Math.min(horizontal ? Math.max(a.x, b.x) : Math.max(a.y, b.y), horizontal ? Math.max(c.x, d.x) : Math.max(c.y, d.y)) - Math.max(horizontal ? Math.min(a.x, b.x) : Math.min(a.y, b.y), horizontal ? Math.min(c.x, d.x) : Math.min(c.y, d.y));
        if (overlap > 0) cost += overlap * 4;
      } else {
        const h1 = horizontal ? a : c, h2 = horizontal ? b : d;
        const v1 = horizontal ? c : a, v2 = horizontal ? d : b;
        if (v1.x > Math.min(h1.x, h2.x) && v1.x < Math.max(h1.x, h2.x) && h1.y > Math.min(v1.y, v2.y) && h1.y < Math.max(v1.y, v2.y)) cost += 12;
      }
    }
    return cost;
  }

  function route(network, starts, end, obstacles, segments) {
    const target = network.index(end);
    if (!Number.isFinite(target)) return null;
    const costs = new Float64Array(network.size * 3).fill(Infinity);
    const previous = new Int32Array(network.size * 3).fill(-1);
    const sources = new Map();
    const queue = new Queue();
    starts.forEach(start => {
      if (obstacles.some(box => inside(start, box))) return;
      const index = network.index(start);
      if (!Number.isFinite(index)) return;
      const state = index * 3 + 2;
      costs[state] = STUB + (start.penalty || 0);
      sources.set(state, start);
      queue.push({state, cost: costs[state], priority: costs[state] + distance(start, end)});
    });
    while (queue.items.length) {
      const item = queue.pop();
      if (item.cost !== costs[item.state]) continue;
      const current = Math.floor(item.state / 3), direction = item.state % 3;
      if (current === target) {
        const points = [];
        let state = item.state;
        while (state >= 0) {
          points.push(network.point(Math.floor(state / 3)));
          if (previous[state] < 0) {
            points.push(sources.get(state).anchor);
            break;
          }
          state = previous[state];
        }
        return {points: simplify(points.reverse()), cost: item.cost};
      }
      const p = network.point(current);
      for (const next of network.neighbors(current)) {
        const state = next.index * 3 + next.direction;
        const cost = item.cost + next.length + (direction !== 2 && direction !== next.direction ? BEND_COST : 0) + trafficPenalty(p, next.point, segments);
        if (cost >= costs[state]) continue;
        costs[state] = cost;
        previous[state] = item.state;
        queue.push({state, cost, priority: cost + distance(next.point, end)});
      }
    }
    return null;
  }

  function labelSize(svg, label) {
    const measure = svgElement('text', {'font-size': 12, 'font-family': 'var(--sans, sans-serif)'});
    svg.append(measure);
    const width = text => {
      measure.textContent = text;
      return measure.getComputedTextLength() || text.length * 6;
    };
    const lines = [];
    let line = '';
    String(label).split(/\s+/).forEach(word => {
      const candidate = line ? `${line} ${word}` : word;
      if (line && width(candidate) > 160) { lines.push(line); line = word; }
      else line = candidate;
    });
    if (line) lines.push(line);
    const size = {lines, width: Math.ceil(Math.max(0, ...lines.map(width))) + 12, height: Math.max(1, lines.length) * 14 + 6};
    measure.remove();
    return size;
  }

  function stations(size, obstacles, segments, from, to, width, height) {
    const halfHeight = size.height / 2 + 1;
    const boundaries = [...new Set([0, height, ...obstacles.flatMap(box => [box.top, box.bottom])])].sort((a, b) => a - b);
    const ys = [];
    boundaries.forEach((value, index) => {
      if (index) ys.push(round((value + boundaries[index - 1]) / 2));
      ys.push(round(value - halfHeight - 1), round(value + halfHeight + 1));
    });
    const candidates = [];
    const seen = new Set();
    const center = {x: (from.x + to.x) / 2, y: (from.y + to.y) / 2};
    for (const y of ys) {
      if (y - halfHeight < 3 || y + halfHeight > height - 3) continue;
      const blocked = obstacles.filter(box => box.top < y + halfHeight && box.bottom > y - halfHeight).map(box => [box.left - 3, box.right + 3]).sort((a, b) => a[0] - b[0]);
      const spaces = [];
      let left = 3;
      for (const [start, end] of blocked) {
        if (start > left) spaces.push([left, start]);
        left = Math.max(left, end);
      }
      spaces.push([left, width - 3]);
      for (const [min, max] of spaces) {
        if (max - min < size.width + 8) continue;
        for (const preferred of [center.x, from.x, to.x, (min + max) / 2]) {
          const x = round(Math.max(min + size.width / 2 + 4, Math.min(max - size.width / 2 - 4, preferred)));
          const box = {left: x - size.width / 2 - 2, right: x + size.width / 2 + 2, top: y - halfHeight, bottom: y + halfHeight};
          const key = `${x},${y}`;
          if (seen.has(key) || obstacles.some(obstacle => overlaps(box, obstacle)) || segments.some(([a, b]) => crosses(a, b, box))) continue;
          seen.add(key);
          candidates.push({x, y, left: box.left, right: box.right, box, score: distance(from, {x, y}) + distance(to, {x, y}) + Math.abs(y - center.y) * .1});
        }
      }
    }
    return candidates.sort((a, b) => a.score - b.score);
  }

  // Choose the line first. A vertical connection keeps its label beside the
  // line; a long horizontal run can carry a label with clear arrow stubs.
  function labelAlong(points, size, obstacles, segments, width, height) {
    const candidates = [];
    for (let index = 1; index < points.length; index++) {
      const a = points[index - 1], b = points[index];
      const horizontal = Math.abs(a.y - b.y) < EPSILON;
      for (const fraction of [.5, .35, .65]) {
        const x = a.x + (b.x - a.x) * fraction, y = a.y + (b.y - a.y) * fraction;
        if (horizontal) {
          if (Math.abs(b.x - a.x) >= size.width + STUB * 2 + 4 && x - size.width / 2 >= Math.min(a.x, b.x) + STUB && x + size.width / 2 <= Math.max(a.x, b.x) - STUB) candidates.push({x, y, inline: index, cost: Math.abs(fraction - .5) * 10});
          for (const direction of [-1, 1]) candidates.push({x, y: y + direction * (size.height / 2 + 5), cost: 8 + Math.abs(fraction - .5) * 10});
        } else {
          if (y - size.height / 2 < Math.min(a.y, b.y) + 4 || y + size.height / 2 > Math.max(a.y, b.y) - 4) continue;
          for (const direction of [1, -1]) candidates.push({x: x + direction * (size.width / 2 + 5), y, cost: 3 + Math.abs(fraction - .5) * 10});
        }
      }
    }
    candidates.sort((a, b) => a.cost - b.cost);
    for (const candidate of candidates) {
      const box = {left: candidate.x - size.width / 2 - 2, right: candidate.x + size.width / 2 + 2, top: candidate.y - size.height / 2 - 1, bottom: candidate.y + size.height / 2 + 1};
      if (box.left < 3 || box.right > width - 3 || box.top < 3 || box.bottom > height - 3 || obstacles.some(obstacle => overlaps(box, obstacle)) || segments.some(([a, b]) => crosses(a, b, box))) continue;
      if (points.slice(1).some((point, index) => index + 1 !== candidate.inline && crosses(points[index], point, box))) continue;
      return {...candidate, box};
    }
    return null;
  }

  function routeFirst(fromPorts, toPorts, size, obstacles, segments, width, height) {
    // Prefer centers, with offset ports available to separate crowded lines.
    const starts = fromPorts.filter(port => !obstacles.some(box => !inside(port.anchor, box) && crosses(port.anchor, port, box)));
    const ends = toPorts.filter(port => !obstacles.some(box => !inside(port.anchor, box) && crosses(port.anchor, port, box)));
    const network = grid(obstacles, [...starts, ...ends], {left: width / 2, right: width / 2, y: height / 2}, width, height);
    let chosen = null;
    function consider(rawPoints, sourcePenalty, targetPenalty) {
      const points = simplify(rawPoints);
      if (points.slice(2).some((point, index) => {
        const a = points[index], b = points[index + 1];
        return (b.x - a.x) * (point.x - b.x) + (b.y - a.y) * (point.y - b.y) < -EPSILON;
      })) return;
      if (points.slice(1).some((point, index) => obstacles.some(box => {
        if (index === 0 && inside(points[0], box)) return false;
        if (index === points.length - 2 && inside(point, box)) return false;
        return crosses(points[index], point, box);
      }))) return;
      const station = labelAlong(points, size, obstacles, segments, width, height);
      if (!station) return;
      const cost = points.slice(1).reduce((sum, point, index) => sum + distance(points[index], point) + trafficPenalty(points[index], point, segments), 0) + Math.max(0, points.length - 2) * BEND_COST + sourcePenalty + targetPenalty + station.cost;
      if (!chosen || cost < chosen.cost) chosen = {points, station, cost};
    }
    // A lane halfway between facing ports leaves room for a label and avoids
    // wrapping a line around a neighboring card merely to fit its text.
    for (const start of starts.filter(port => !port.penalty)) {
      for (const end of ends.filter(port => !port.penalty)) {
        const x = round((start.x + end.x) / 2), y = round((start.y + end.y) / 2);
        consider([start.anchor, start, {x: start.x, y}, {x: end.x, y}, end, end.anchor], 0, 0);
        consider([start.anchor, start, {x, y: start.y}, {x, y: end.y}, end, end.anchor], 0, 0);
      }
    }
    for (const end of ends) {
      const found = route(network, starts, end, obstacles, segments);
      if (!found) continue;
      const points = simplify([...found.points, end.anchor]);
      // A route must approach each card normally, without doubling back at a
      // port. Its final visible segment therefore stays at least STUB long.
      if (points.slice(2).some((point, index) => {
        const a = points[index], b = points[index + 1];
        return (b.x - a.x) * (point.x - b.x) + (b.y - a.y) * (point.y - b.y) < -EPSILON;
      })) continue;
      const start = starts.find(port => distance(port.anchor, points[0]) < EPSILON);
      consider(points, start ? start.penalty : 0, end.penalty || 0);
    }
    return chosen;
  }

  window.drawMetadataConnections = function (svg, canvas, nodes, edges, scale, chapterMatch, chapter) {
    svg.replaceChildren();
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    const bounds = canvas.getBoundingClientRect();
    if (!bounds.width || !bounds.height || !Number.isFinite(scale) || scale <= 0) return;
    const width = canvas.offsetWidth, height = canvas.offsetHeight;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
    const measured = node => {
      const rect = node.getBoundingClientRect();
      if (!rect.width || !rect.height) return null;
      return {left: round((rect.left - bounds.left) / scale), top: round((rect.top - bounds.top) / scale), right: round((rect.right - bounds.left) / scale), bottom: round((rect.bottom - bounds.top) / scale)};
    };
    const boxes = new Map();
    nodes.forEach((node, id) => { const box = measured(node); if (box) boxes.set(id, box); });
    const obstacles = [...boxes.values()].map(box => inflate(box, CLEARANCE));
    canvas.querySelectorAll('.map-group > h2').forEach(heading => { const box = measured(heading); if (box) obstacles.push(inflate(box, CLEARANCE)); });
    const defs = svgElement('defs');
    const markerId = `map-arrow-${++instance}`;
    const marker = svgElement('marker', {id: markerId, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 9, markerHeight: 9, orient: 'auto', markerUnits: 'userSpaceOnUse'});
    marker.append(svgElement('path', {d: 'M 0 1 L 9 5 L 0 9 Z', fill: 'var(--accent, #a44932)'}));
    defs.append(marker);
    svg.append(defs);
    const segments = [];
    const lineLayer = svgElement('g', {class: 'map-connection-lines'});
    const labelLayer = svgElement('g', {class: 'map-connection-labels'});
    svg.append(lineLayer, labelLayer);
    const center = box => ({x: (box.left + box.right) / 2, y: (box.top + box.bottom) / 2});
    for (const edge of edges) {
      const source = boxes.get(edge.from), target = boxes.get(edge.to);
      if (!source || !target || edge.from === edge.to) continue;
      const size = labelSize(svg, edge.label);
      const fromPorts = ports(source), toPorts = ports(target);
      let chosen = routeFirst(fromPorts, toPorts, size, obstacles, segments, width, height);
      const candidates = chosen ? [] : stations(size, obstacles, segments, center(source), center(target), width, height);
      for (const station of candidates) {
        const blocked = [...obstacles, station.box];
        const network = grid(blocked, [...fromPorts, ...toPorts], station, width, height);
        for (const reverse of [false, true]) {
          const first = {x: reverse ? station.right : station.left, y: station.y};
          const second = {x: reverse ? station.left : station.right, y: station.y};
          const start = route(network, fromPorts, first, blocked, segments);
          if (!start) continue;
          const added = start.points.slice(1).map((point, index) => [start.points[index], point]);
          const end = route(network, toPorts, second, blocked, [...segments, ...added]);
          if (!end) continue;
          const cost = start.cost + end.cost;
          if (!chosen || cost < chosen.cost) chosen = {station, cost, points: simplify([...start.points, ...end.points.reverse()])};
        }
        // Stations are ordered by their geometric lower bound. A nearby viable
        // station is preferable to sending a label into a distant group.
        if (chosen) break;
      }
      if (!chosen) continue;
      const {station, points} = chosen;
      const contextual = chapter !== 'all' && typeof chapterMatch === 'function' && (!chapterMatch(edge.from) || !chapterMatch(edge.to));
      const path = svgElement('path', {
        class: `map-connection${contextual ? ' is-context' : ''}`,
        'data-from': edge.from, 'data-to': edge.to,
        d: points.map((point, index) => `${index ? 'L' : 'M'} ${round(point.x)} ${round(point.y)}`).join(' '),
        fill: 'none', stroke: 'var(--accent, #a44932)', 'stroke-width': 1.6,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'marker-end': `url(#${markerId})`
      });
      lineLayer.append(path);
      points.slice(1).forEach((point, index) => segments.push([points[index], point]));
      const label = svgElement('g', {class: 'map-connection-label', 'data-from': edge.from, 'data-to': edge.to, transform: `translate(${station.x}, ${station.y})`});
      label.append(svgElement('rect', {x: -size.width / 2, y: -size.height / 2, width: size.width, height: size.height, rx: 3, fill: 'var(--surface, #fffdf8)', stroke: 'var(--accent, #a44932)', 'stroke-width': .7}));
      const text = svgElement('text', {'text-anchor': 'middle', fill: 'var(--accent, #a44932)', 'font-size': 12, 'font-family': 'var(--sans, sans-serif)'});
      size.lines.forEach((line, index) => {
        const span = svgElement('tspan', {x: 0, y: -size.lines.length * 7 + 12 + index * 14});
        span.textContent = line;
        text.append(span);
      });
      label.append(text);
      labelLayer.append(label);
      obstacles.push(station.box);
    }
  };
})();
