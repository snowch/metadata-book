"""Server-rendered, progressively enhanced metadata map."""
from html import escape
import json


def _e(value):
    return escape(str(value), quote=True)


def _chapter_links(record):
    return ' '.join(
        f'<a href="{_e(chapter["href"])}">Chapter {_e(chapter["number"])} · {_e(chapter["label"])}</a>'
        for chapter in record.get('chapters', [])
    )


def _details(record, records):
    def value(field):
        rendered = f'<code>{_e(field.get("value", ""))}</code>'
        target = field.get('target')
        if target in records:
            return f'<a href="#record-{_e(target)}" data-record-target="{_e(target)}" title="View {_e(records[target]["label"])}">{rendered}<span class="map-follow"> ↗</span></a>'
        return rendered

    fields = record.get('fields', [])
    example = ''.join(f'<div><dt><code>{_e(field["name"])}</code></dt><dd>{value(field)}</dd></div>' for field in fields)
    schema = ''.join(f'<tr><th scope="row"><code>{_e(field["name"])}</code></th><td><code>{_e(field["type"])}</code></td><td>{_e(field["description"])}</td></tr>' for field in fields)
    rows = record.get('rows')
    row_html = ''
    if rows:
        headings = ''.join(f'<th scope="col">{_e(c)}</th>' for c in rows['columns'])
        values = ''.join('<tr>' + ''.join(f'<td>{_e(v)}</td>' for v in row) + '</tr>' for row in rows['values'])
        row_html = f'<div class="map-table-scroll" tabindex="0" aria-label="Example rows"><table><thead><tr>{headings}</tr></thead><tbody>{values}</tbody></table></div>'
    code = f'<pre><code>{_e(record["code"])}</code></pre>' if record.get('code') else ''
    related = ''.join(
        f'<li><a href="#record-{_e(item["target"])}" data-record-target="{_e(item["target"])}">{_e(item["label"])} · {_e(records[item["target"]]["label"])}</a></li>'
        for item in record.get('related', []) if item['target'] in records
    )
    related_html = f'<div class="map-related"><h3>Related record types</h3><p>These associations may refer to different examples.</p><ul>{related}</ul></div>' if related else ''
    return f'''<div class="map-record-content" data-detail-record="{_e(record['id'])}">
      <p class="map-eyebrow">Selected record type</p>
      <h2 tabindex="-1">{_e(record['label'])}</h2>
      <p class="map-record-description">{_e(record['description'])}</p>
      <p class="map-evidence">{_e(record['evidence'])}</p>
      <div class="map-detail-tabs" hidden></div>
      <section class="map-example-panel"><h3>Example · {_e(record.get('exampleLabel', record['label']))}</h3>
        <p class="map-value-hint">Linked values open the matching example record.</p>
        <dl class="map-example-values">{example}</dl>{row_html}{code}
        <div class="map-reading"><h3>What this tells us</h3><p>{_e(record.get('interpretation', ''))}</p></div>
        <div class="map-limit"><h3>What it does not tell us</h3><p>{_e(record.get('limit', ''))}</p></div>
      </section>
      <section class="map-fields-panel"><h3>Fields and types</h3>
        <p>Types describe this example; real systems may use different names and representations.</p>
        <div class="map-table-scroll" tabindex="0" aria-label="Fields and types"><table><thead><tr><th scope="col">Field</th><th scope="col">Type</th><th scope="col">Meaning</th></tr></thead><tbody>{schema}</tbody></table></div>
      </section><nav class="map-chapter-links" aria-label="Read about {_e(record['label'])}"><h3>Read in the book</h3>{_chapter_links(record)}</nav>{related_html}
    </div>'''


def render_map(data):
    """Return main-body HTML. The host provides the page heading and assets."""
    records = {record['id']: record for record in data['records']}
    groups = []
    for group in data['groups']:
        nodes = []
        for record in data['records']:
            if record['group'] != group['id']:
                continue
            primary = next((chapter for chapter in record['chapters'] if chapter['number'] == record['primaryChapter']), record['chapters'][0])
            nodes.append(f'''<article class="map-node" data-node="{_e(record['id'])}">
              <a class="map-node-select" href="#record-{_e(record['id'])}" data-select-record="{_e(record['id'])}"><span>{_e(record['label'])}</span></a>
              <a class="map-chapter-badge" href="{_e(primary['href'])}" title="Main chapter: {_e(primary['label'])}" aria-label="Read about {_e(record['label'])} in Chapter {_e(primary['number'])}">Ch. {_e(primary['number'])}</a>
            </article>''')
        groups.append(f'<section class="map-group" data-group="{_e(group["id"])}"><h2>{_e(group["title"])}</h2><div class="map-group-nodes">{"".join(nodes)}</div></section>')
    chapter_options = ''.join(f'<option value="{_e(c["number"])}">{_e(c["number"])} · {_e(c["title"])}</option>' for c in data['chapters'])
    fallback = ''.join(f'<article class="map-fallback-record" id="record-{_e(r["id"])}">{_details(r, records)}</article>' for r in data['records'])
    safe_json = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return f'''<section class="metadata-map" aria-label="Interactive metadata map">
      <a class="map-return" hidden></a>
      <details class="map-explainer"><summary>What does this map show?</summary><p>The book’s metadata record types, grouped by purpose. The whole map keeps all record types and their relationships visible. Select a record to highlight its connections. Choose View record to inspect its example and fields. Connections describe relationships, not processing order or a physical database schema. Each example says whether it is computed or illustrative.</p></details>
      <div class="map-controls" hidden>
        <div class="map-filter"><label for="map-chapter-filter">Highlight chapter</label><select id="map-chapter-filter"><option value="all">Show all chapters</option>{chapter_options}</select></div>
      </div>
      <p class="map-status" role="status" aria-live="polite"></p>
      <div class="map-section-tabs" role="tablist" aria-label="Metadata explorer" hidden>
        <button type="button" id="map-section-map" role="tab" data-pane="map" aria-controls="map-explorer-panel" aria-selected="true">Map</button>
        <button type="button" id="map-section-details" role="tab" data-pane="details" aria-controls="map-record-panel" aria-selected="false" tabindex="-1">Record details</button>
      </div>
      <div class="map-workspace">
        <div class="map-explorer" id="map-explorer-panel">
          <div class="map-selection" hidden><span class="map-selection-label"></span><button type="button" class="map-view-record">View record <span aria-hidden="true">→</span></button></div>
          <div class="map-tools" hidden>
          <p class="map-navigation-hint" hidden>Zoom in to read the labels; drag or scroll to move around. <strong>Fit</strong> brings the diagram back into view.</p>
          <div class="map-zoom-controls" role="group" aria-label="Map zoom" hidden><button type="button" data-zoom="out" aria-label="Zoom out">−</button><output class="map-zoom-value" aria-label="Zoom level">100%</output><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" data-zoom="fit">Fit</button></div></div>
          <div class="map-viewport" tabindex="0" aria-label="Record map. Scroll to explore the diagram."><div class="map-scale-frame"><div class="map-canvas"><svg class="map-connections" aria-hidden="true"></svg><div class="map-focus-nodes"></div></div></div></div>
          <details class="map-relationship-text" hidden><summary>Connections as text</summary><div class="map-relationship-summary" hidden></div></details>
          <section class="map-overview" aria-label="All metadata record types"><h2>Explore another record type</h2><div class="map-groups">{''.join(groups)}</div></section>
          <p class="map-legend" hidden><span class="map-legend-selected">Selected record</span><span class="map-legend-chapter">Chapter highlight</span><span>Arrows name relationships. Rust highlights the selected record’s connections.</span></p>
        </div>
        <aside class="map-detail" id="map-record-panel" aria-label="Selected record details" hidden></aside>
      </div>
      <section class="map-fallback"><h2>All example records</h2><p>Each record includes its chapter links, example values and field descriptions. Enable JavaScript to use the interactive map and detail tabs.</p>{fallback}</section>
      <script type="application/json" id="metadata-map-data">{safe_json}</script>
    </section>'''
