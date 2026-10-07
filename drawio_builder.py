"""
drawio_builder.py
------------------
Deterministically converts a `DiagramIR` into a draw.io-compatible
`.drawio` (mxGraph) XML file. Pure stdlib (xml.etree.ElementTree) --
same IR always produces byte-identical XML, which matters for an
evaluation pipeline that needs reproducible artifacts.
"""

from __future__ import annotations

from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from ir_schema import DiagramIR

# Normalized IR canvas is 0-1000 on each axis; scale into a comfortable
# draw.io canvas size in px.
CANVAS_SCALE = 0.8

SHAPE_STYLES = {
    "rectangle": "rounded=0;whiteSpace=wrap;html=1;",
    "ellipse": "ellipse;whiteSpace=wrap;html=1;",
    "circle": "ellipse;whiteSpace=wrap;html=1;aspect=fixed;",
    "diamond": "rhombus;whiteSpace=wrap;html=1;",
    "parallelogram": "shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;",
    "hexagon": "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;",
    "cylinder": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;",
    "text": "text;html=1;align=center;verticalAlign=middle;",
}
DEFAULT_STYLE = SHAPE_STYLES["rectangle"]


def _scale(value: float) -> float:
    return round(value * CANVAS_SCALE, 2)


def _edge_style(edge) -> str:
    parts = ["edgeStyle=orthogonalEdgeStyle", "rounded=0", "html=1"]
    if edge.style == "dashed":
        parts.append("dashed=1")
    if edge.arrow == "none":
        parts.append("endArrow=none")
    elif edge.arrow == "open":
        parts.append("endArrow=open")
    else:
        parts.append("endArrow=classic")
    return ";".join(parts) + ";"


def build_drawio_xml(ir: DiagramIR, diagram_name: str = "Extracted Diagram") -> str:
    """
    Build a full .drawio XML document (mxfile > diagram > mxGraphModel)
    from a validated DiagramIR. Node/edge ids from the IR are reused
    verbatim as mxCell ids so downstream tooling (e.g. the evaluator,
    or a human editor in draw.io) can trace cells back to the IR.
    """
    mxfile = Element("mxfile", {"host": "AI-Elevate-Diagram-POC", "version": "1.0"})
    diagram_el = SubElement(mxfile, "diagram", {"name": diagram_name, "id": "diagram-1"})
    model = SubElement(
        diagram_el,
        "mxGraphModel",
        {
            "dx": "800",
            "dy": "600",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": "850",
            "pageHeight": "1100",
            "math": "0",
            "shadow": "0",
        },
    )
    root = SubElement(model, "root")
    SubElement(root, "mxCell", {"id": "0"})
    SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    known_ids = {n.id for n in ir.nodes}

    for node in ir.nodes:
        style = SHAPE_STYLES.get(node.shape, DEFAULT_STYLE)
        cell = SubElement(
            root,
            "mxCell",
            {
                "id": node.id,
                "value": node.label,
                "style": style,
                "vertex": "1",
                "parent": "1",
            },
        )
        SubElement(
            cell,
            "mxGeometry",
            {
                "x": str(_scale(node.x)),
                "y": str(_scale(node.y)),
                "width": str(_scale(node.width)),
                "height": str(_scale(node.height)),
                "as": "geometry",
            },
        )

    for i, edge in enumerate(ir.edges):
        if edge.source not in known_ids or edge.target not in known_ids:
            continue  # already filtered at IR-load time, but stay defensive here too
        cell = SubElement(
            root,
            "mxCell",
            {
                "id": edge.id or f"edge-{i}",
                "value": edge.label or "",
                "style": _edge_style(edge),
                "edge": "1",
                "parent": "1",
                "source": edge.source,
                "target": edge.target,
            },
        )
        SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})

    raw = tostring(mxfile, encoding="unicode")
    pretty = minidom.parseString(raw).toprettyxml(indent="  ")
    # minidom adds an XML declaration line; drop it for a cleaner .drawio file
    lines = [line for line in pretty.splitlines() if line.strip()]
    if lines and lines[0].startswith("<?xml"):
        lines = lines[1:]
    return "\n".join(lines) + "\n"


def save_drawio_file(ir: DiagramIR, path: str, diagram_name: str = "Extracted Diagram") -> str:
    xml_text = build_drawio_xml(ir, diagram_name=diagram_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml_text)
    return path
