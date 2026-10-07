"""
diagram_renderer.py
--------------------
Renders a `DiagramIR` as a self-contained SVG "linear coordinate graph":
nodes and edges are plotted at their literal (x, y) / (width, height)
values on the same normalized 0-1000 grid the VLM is instructed to use
(see `ir_schema.py` module docstring), with graph-paper style axis
gridlines and tick labels along the bottom and left edges.

This gives graders a direct, at-a-glance way to compare the extracted
diagram against the original hand-drawn input image, side by side --
independent of (and faster than) opening the generated .drawio file.

Pure stdlib, no third-party dependencies, matching the rest of the core
pipeline (`ir_schema.py`, `drawio_builder.py`).
"""

from __future__ import annotations

import html
import math
from typing import Dict, List, Tuple

from ir_schema import DiagramIR, DiagramNode

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
MIN_GRAPH_MAX = 1000.0     # the IR's nominal 0-1000 canvas
AXIS_MARGIN_L = 55         # px reserved for y-axis tick labels
AXIS_MARGIN_B = 58         # px reserved for x-axis tick labels
OUTER_PAD = 20             # px breathing room around the whole plot
DEFAULT_RENDER_SIZE = 640  # px, final on-screen width/height of the square plot

GRID_STEP_CANDIDATES = [50, 100, 200, 250, 500, 1000]

NODE_FILL = "#ffffff"
NODE_STROKE = "#1f2937"
GRID_COLOR = "#e5e7eb"
AXIS_COLOR = "#9ca3af"
EDGE_COLOR = "#2563eb"
EDGE_LABEL_BG = "#fef9c3"
TEXT_COLOR = "#111827"


def _pick_grid_step(graph_max: float) -> float:
    target_divisions = 8
    ideal = graph_max / target_divisions
    for step in GRID_STEP_CANDIDATES:
        if step >= ideal:
            return step
    return GRID_STEP_CANDIDATES[-1]


def _graph_max(ir: DiagramIR) -> float:
    extent = MIN_GRAPH_MAX
    for n in ir.nodes:
        extent = max(extent, n.x + n.width, n.y + n.height)
    # round up to the next grid-friendly multiple of 100
    return float(math.ceil(extent / 100.0) * 100.0)


def _rect_boundary_point(
    cx: float, cy: float, w: float, h: float, toward_x: float, toward_y: float
) -> Tuple[float, float]:
    """Point where the segment from (cx,cy) to (toward_x,toward_y) exits the
    axis-aligned box of half-width w/2, half-height h/2 centered at (cx,cy)."""
    dx = toward_x - cx
    dy = toward_y - cy
    if dx == 0 and dy == 0:
        return (cx, cy)
    half_w, half_h = w / 2.0, h / 2.0
    # scale factor to hit vertical or horizontal edge first
    scales = []
    if dx != 0:
        scales.append(half_w / abs(dx))
    if dy != 0:
        scales.append(half_h / abs(dy))
    t = min(scales) if scales else 0
    return (cx + dx * t, cy + dy * t)


def _wrap_label(label: str, box_w: float, box_h: float, font_size: float) -> List[str]:
    if not label:
        return []
    # rough average glyph width for a proportional sans font
    avg_char_w = font_size * 0.58
    max_chars = max(4, int(box_w / avg_char_w))
    words = label.split()
    lines: List[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    max_lines = max(1, int(box_h / (font_size * 1.3)))
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        if len(last) > 3:
            lines[-1] = last[: max(3, max_chars - 1)].rstrip() + "…"
    return lines


def _node_shape_svg(node: DiagramNode, font_size: float) -> str:
    x, y, w, h = node.x, node.y, node.width, node.height
    cx, cy = x + w / 2.0, y + h / 2.0
    style = f'fill="{NODE_FILL}" stroke="{NODE_STROKE}" stroke-width="2"'
    parts: List[str] = []

    if node.shape == "text":
        pass  # no border, label only
    elif node.shape in ("ellipse", "circle"):
        parts.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{w/2:.1f}" ry="{h/2:.1f}" {style}/>')
    elif node.shape == "diamond":
        pts = f"{cx:.1f},{y:.1f} {x+w:.1f},{cy:.1f} {cx:.1f},{y+h:.1f} {x:.1f},{cy:.1f}"
        parts.append(f'<polygon points="{pts}" {style}/>')
    elif node.shape == "parallelogram":
        skew = w * 0.18
        pts = f"{x+skew:.1f},{y:.1f} {x+w:.1f},{y:.1f} {x+w-skew:.1f},{y+h:.1f} {x:.1f},{y+h:.1f}"
        parts.append(f'<polygon points="{pts}" {style}/>')
    elif node.shape == "hexagon":
        cut = w * 0.15
        pts = (
            f"{x+cut:.1f},{y:.1f} {x+w-cut:.1f},{y:.1f} {x+w:.1f},{cy:.1f} "
            f"{x+w-cut:.1f},{y+h:.1f} {x+cut:.1f},{y+h:.1f} {x:.1f},{cy:.1f}"
        )
        parts.append(f'<polygon points="{pts}" {style}/>')
    elif node.shape == "cylinder":
        cap_h = min(h * 0.2, 20)
        parts.append(f'<rect x="{x:.1f}" y="{y+cap_h/2:.1f}" width="{w:.1f}" height="{h-cap_h:.1f}" {style}/>')
        parts.append(f'<ellipse cx="{cx:.1f}" cy="{y+cap_h/2:.1f}" rx="{w/2:.1f}" ry="{cap_h/2:.1f}" {style}/>')
        parts.append(
            f'<path d="M {x:.1f} {y+h-cap_h/2:.1f} A {w/2:.1f} {cap_h/2:.1f} 0 0 0 {x+w:.1f} {y+h-cap_h/2:.1f}" '
            f'fill="none" stroke="{NODE_STROKE}" stroke-width="2"/>'
        )
    else:  # rectangle / default
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="4" {style}/>')

    lines = _wrap_label(node.label, w * 0.9, h * 0.85, font_size)
    n_lines = len(lines)
    line_h = font_size * 1.25
    start_y = cy - (n_lines - 1) * line_h / 2.0
    for i, line in enumerate(lines):
        ty = start_y + i * line_h
        parts.append(
            f'<text x="{cx:.1f}" y="{ty:.1f}" font-size="{font_size:.1f}" fill="{TEXT_COLOR}" '
            f'text-anchor="middle" dominant-baseline="middle" font-family="Helvetica, Arial, sans-serif">'
            f"{html.escape(line)}</text>"
        )
    return "\n".join(parts)


def render_ir_svg(ir: DiagramIR, render_size: int = DEFAULT_RENDER_SIZE) -> str:
    """
    Render a DiagramIR as a standalone SVG string: a linear (x/y) coordinate
    graph with gridlines/tick labels, node shapes plotted at their literal
    IR coordinates, and edges drawn between node boundaries with arrowheads.
    """
    graph_max = _graph_max(ir)
    step = _pick_grid_step(graph_max)
    font_size = max(11.0, min(18.0, graph_max / 60.0))

    plot_w = plot_h = graph_max
    total_w = plot_w + AXIS_MARGIN_L + OUTER_PAD * 2
    total_h = plot_h + AXIS_MARGIN_B + OUTER_PAD * 2
    ox, oy = AXIS_MARGIN_L + OUTER_PAD, OUTER_PAD  # plot origin (top-left) in SVG user space

    svg: List[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.0f} {total_h:.0f}" '
        f'width="{render_size}" height="{render_size}" font-family="Helvetica, Arial, sans-serif">'
    )
    svg.append(f'<rect x="0" y="0" width="{total_w:.0f}" height="{total_h:.0f}" fill="#ffffff"/>')

    # --- arrow markers ---
    svg.append("<defs>")
    svg.append(
        f'<marker id="arrow-std" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{EDGE_COLOR}"/></marker>'
    )
    svg.append(
        f'<marker id="arrow-open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9" fill="none" stroke="{EDGE_COLOR}" stroke-width="1.5"/></marker>'
    )
    svg.append("</defs>")

    # --- plot group, translated so (0,0) of the IR grid lands at (ox, oy) ---
    svg.append(f'<g transform="translate({ox},{oy})">')
    svg.append(f'<rect x="0" y="0" width="{plot_w:.0f}" height="{plot_h:.0f}" fill="#fcfcfd" stroke="{AXIS_COLOR}"/>')

    # gridlines + tick labels
    tick = 0.0
    while tick <= graph_max + 0.01:
        svg.append(f'<line x1="{tick:.1f}" y1="0" x2="{tick:.1f}" y2="{plot_h:.1f}" stroke="{GRID_COLOR}" stroke-width="1"/>')
        svg.append(f'<line x1="0" y1="{tick:.1f}" x2="{plot_w:.1f}" y2="{tick:.1f}" stroke="{GRID_COLOR}" stroke-width="1"/>')
        svg.append(
            f'<text x="{tick:.1f}" y="{plot_h+16:.1f}" font-size="10" fill="{AXIS_COLOR}" text-anchor="middle">{int(tick)}</text>'
        )
        svg.append(
            f'<text x="-6" y="{tick:.1f}" font-size="10" fill="{AXIS_COLOR}" text-anchor="end" dominant-baseline="middle">{int(tick)}</text>'
        )
        tick += step
    svg.append(f'<text x="{plot_w/2:.1f}" y="{plot_h+42:.1f}" font-size="11" fill="{AXIS_COLOR}" text-anchor="middle">x (normalized 0-{int(graph_max)})</text>')
    svg.append(
        f'<text x="{-AXIS_MARGIN_L+16:.1f}" y="{plot_h/2:.1f}" font-size="11" fill="{AXIS_COLOR}" '
        f'text-anchor="middle" transform="rotate(-90 {-AXIS_MARGIN_L+16:.1f} {plot_h/2:.1f})">y (normalized 0-{int(graph_max)})</text>'
    )

    # edges (drawn first so nodes sit on top)
    nodes_by_id: Dict[str, DiagramNode] = {n.id: n for n in ir.nodes}
    for edge in ir.edges:
        src = nodes_by_id.get(edge.source)
        tgt = nodes_by_id.get(edge.target)
        if src is None or tgt is None:
            continue
        scx, scy = src.x + src.width / 2.0, src.y + src.height / 2.0
        tcx, tcy = tgt.x + tgt.width / 2.0, tgt.y + tgt.height / 2.0
        x1, y1 = _rect_boundary_point(scx, scy, src.width, src.height, tcx, tcy)
        x2, y2 = _rect_boundary_point(tcx, tcy, tgt.width, tgt.height, scx, scy)
        dash = ' stroke-dasharray="6,4"' if edge.style == "dashed" else ""
        marker = ""
        if edge.arrow == "standard":
            marker = ' marker-end="url(#arrow-std)"'
        elif edge.arrow == "open":
            marker = ' marker-end="url(#arrow-open)"'
        svg.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{EDGE_COLOR}" stroke-width="2"{dash}{marker}/>'
        )
        if edge.label:
            mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            label_w = max(20, len(edge.label) * font_size * 0.55)
            svg.append(
                f'<rect x="{mx-label_w/2:.1f}" y="{my-font_size*0.8:.1f}" width="{label_w:.1f}" '
                f'height="{font_size*1.5:.1f}" fill="{EDGE_LABEL_BG}" opacity="0.9" rx="2"/>'
            )
            svg.append(
                f'<text x="{mx:.1f}" y="{my:.1f}" font-size="{font_size*0.85:.1f}" fill="{TEXT_COLOR}" '
                f'text-anchor="middle" dominant-baseline="middle">{html.escape(edge.label)}</text>'
            )

    # nodes
    for node in ir.nodes:
        svg.append(_node_shape_svg(node, font_size))

    svg.append("</g>")  # close plot group
    svg.append("</svg>")
    return "\n".join(svg)
