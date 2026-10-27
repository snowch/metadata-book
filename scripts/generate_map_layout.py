#!/usr/bin/env python3
"""Precompute the complete metadata graph; Graphviz is a development dependency.

Run this script after changing metadata-map.json relationships. The checked-in
geometry is consumed by the site, so neither its build nor its browser needs dot.
Use --check to check freshness and coverage with the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "metadata-map.json"
OUTPUT = ROOT / "assets" / "metadata-map-layout.json"
NODE_WIDTH = 200
NODE_HEIGHT = 70
PADDING = 24
FONT_SIZE = 13
LINE_HEIGHT = 15


def source_fingerprint(source: dict) -> str:
    """Hash graph identity rather than unrelated record prose or field examples."""
    graph = {
        "ids": sorted(record["id"] for record in source["records"]),
        "relationships": sorted(
            ({key: edge[key] for key in ("from", "to", "label")}
             for edge in source["relationships"]),
            key=lambda edge: (edge["from"], edge["to"], edge["label"]),
        ),
    }
    canonical = json.dumps(graph, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def label_lines(label: str) -> list[str]:
    if label == "assigns definition responsibility to":
        return ["assigns definition", "responsibility to"]
    return [label]


def dot_source(source: dict) -> str:
    quote = json.dumps
    lines = [
        "digraph Metadata {",
        'graph [rankdir=LR, nodesep=.45, ranksep=.65, margin=0, splines=spline];',
        f'node [shape=box, width={NODE_WIDTH / 72:.9f}, '
        f'height={NODE_HEIGHT / 72:.9f}, fixedsize=true, fontname="sans-serif"];',
        f'edge [fontname="sans-serif", fontsize={FONT_SIZE}];',
    ]
    for record in source["records"]:
        lines.append(f'{quote(record["id"])} [label={quote(record["label"])}];')
    for index, edge in enumerate(source["relationships"]):
        # Let the first production step wrap vertically. This keeps the entire
        # graph four columns wide without changing direction or dropping edges.
        wrap = ", constraint=false" if edge["from"] == "report-refresh" else ""
        label = quote("\n".join(label_lines(edge["label"])))
        lines.append(f'{quote(edge["from"])} -> {quote(edge["to"])} '
                     f'[id="relationship-{index}", label={label}{wrap}];')
    lines.append("}")
    return "\n".join(lines)


def rounded(value: float) -> float:
    return round(value, 2)


def generate(source: dict) -> dict:
    if not shutil.which("dot"):
        raise ValueError("Graphviz dot is required to regenerate the map layout")
    process = subprocess.run(["dot", "-Tjson"], input=dot_source(source),
                             capture_output=True, text=True, check=True)
    graph = json.loads(process.stdout)
    left, bottom, right, top = map(float, graph["bb"].split(","))

    def point(pair: list[float]) -> list[float]:
        return [rounded(pair[0] - left + PADDING),
                rounded(top - pair[1] + PADDING)]

    def coord(pair: list[float]) -> str:
        return f"{pair[0]:g},{pair[1]:g}"

    nodes = {}
    for node in graph["objects"]:
        center = point(list(map(float, node["pos"].split(","))))
        nodes[node["name"]] = {
            "x": rounded(center[0] - NODE_WIDTH / 2),
            "y": rounded(center[1] - NODE_HEIGHT / 2),
            "width": NODE_WIDTH,
            "height": NODE_HEIGHT,
        }

    def boundary(pair: list[float], node_id: str) -> list[float]:
        # dot clips against a stroked box with subpixel approximation. Snap to
        # the exact SVG card boundary so focus paths and arrow markers attach
        # cleanly even when rendered at a large zoom.
        node = nodes[node_id]
        x, y = pair
        candidates = [
            [node["x"], min(max(y, node["y"]), node["y"] + node["height"])],
            [node["x"] + node["width"], min(max(y, node["y"]), node["y"] + node["height"])],
            [min(max(x, node["x"]), node["x"] + node["width"]), node["y"]],
            [min(max(x, node["x"]), node["x"] + node["width"]), node["y"] + node["height"]],
        ]
        closest = min(candidates, key=lambda candidate: (candidate[0] - x) ** 2 +
                      (candidate[1] - y) ** 2)
        return [rounded(value) for value in closest]

    geometries = {}
    for edge in graph["edges"]:
        index = int(edge["id"].removeprefix("relationship-"))
        relationship = source["relationships"][index]
        drawing = next(op for op in edge["_draw_"] if op["op"] == "b")
        points = [point(pair) for pair in drawing["points"]]
        points[0] = boundary(points[0], relationship["from"])
        if (len(points) - 1) % 3:
            raise ValueError("Graphviz returned an unsupported spline")
        path = "M " + coord(points[0])
        for offset in range(1, len(points), 3):
            path += " C " + " ".join(coord(pair) for pair in points[offset:offset + 3])
        # Graphviz's spline stops before its own arrowhead. The SVG renderer
        # supplies a marker, whose tip must end at the actual target boundary.
        tip_token = next(token for token in edge["pos"].split() if token.startswith("e,"))
        tip = boundary(point(list(map(float, tip_token.split(",")[1:]))), relationship["to"])
        end = points[-1]
        extension = [[rounded(end[axis] + (tip[axis] - end[axis]) * fraction)
                      for axis in (0, 1)] for fraction in (1 / 3, 2 / 3)]
        path += " C " + " ".join(coord(pair) for pair in [*extension, tip])
        center = point(list(map(float, edge["lp"].split(","))))
        text_ops = [op for op in edge["_ldraw_"] if op["op"] == "T"]
        lines = label_lines(relationship["label"])
        geometries[index] = {
            **relationship,
            "path": path,
            "labelX": center[0],
            "labelY": center[1],
            "labelLines": lines,
            "labelWidth": rounded(max(op["width"] for op in text_ops)),
            "labelHeight": len(lines) * LINE_HEIGHT,
        }
    return {
        "sourceFingerprint": source_fingerprint(source),
        "width": rounded(right - left + PADDING * 2),
        "height": rounded(top - bottom + PADDING * 2),
        "labelFontSize": FONT_SIZE,
        "labelLineHeight": LINE_HEIGHT,
        "nodes": nodes,
        "edges": [geometries[index] for index in range(len(source["relationships"]))],
    }


def check(source: dict, layout: dict) -> None:
    if layout["sourceFingerprint"] != source_fingerprint(source):
        raise ValueError("Map layout is stale; run python scripts/generate_map_layout.py")
    expected_ids = [record["id"] for record in source["records"]]
    if len(set(expected_ids)) != len(expected_ids) or set(layout["nodes"]) != set(expected_ids):
        raise ValueError("Map layout must contain each source node exactly once")
    identities = lambda edges: sorted((edge["from"], edge["to"], edge["label"]) for edge in edges)
    if identities(layout["edges"]) != identities(source["relationships"]):
        raise ValueError("Map layout must contain every source relationship exactly once")
    for name, node in layout["nodes"].items():
        if not (0 <= node["x"] <= layout["width"] - node["width"] and
                0 <= node["y"] <= layout["height"] - node["height"]):
            raise ValueError(f"Node lies outside map bounds: {name}")
    for edge in layout["edges"]:
        if not edge["path"].startswith("M ") or " C " not in edge["path"]:
            raise ValueError("Relationship is missing its cubic SVG path")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check freshness without Graphviz")
    args = parser.parse_args()
    try:
        source = json.loads(SOURCE.read_text())
        if args.check:
            layout = json.loads(OUTPUT.read_text())
        else:
            layout = generate(source)
        check(source, layout)
        if not args.check:
            OUTPUT.write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n")
        print(f'Metadata layout: {len(layout["nodes"])} nodes, '
              f'{len(layout["edges"])} relationships, '
              f'{layout["width"]:g} × {layout["height"]:g}')
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
