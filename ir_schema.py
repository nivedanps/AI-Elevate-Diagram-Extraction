"""
ir_schema.py
------------
Defines the Normalized Diagram Intermediate Representation (IR) used
throughout the pipeline: Azure VLM -> IR -> draw.io Builder -> Evaluator.

Deliberately dependency-free (stdlib only, no pydantic) so the core
pipeline has zero third-party install requirements beyond the VLM
client and the UI layer.

Coordinate convention
----------------------
Nodes are positioned on a normalized 0-1000 x 0-1000 canvas grid,
top-left origin, matching how the VLM is instructed to report
positions in `azure_client.SYSTEM_PROMPT`. `drawio_builder.py` scales
this grid into actual draw.io coordinate space.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

VALID_SHAPES = {
    "rectangle",
    "ellipse",
    "diamond",
    "parallelogram",
    "circle",
    "hexagon",
    "cylinder",
    "text",
}
VALID_EDGE_STYLES = {"solid", "dashed"}
VALID_ARROWS = {"standard", "open", "none"}
DEFAULT_SHAPE = "rectangle"
DEFAULT_EDGE_STYLE = "solid"
DEFAULT_ARROW = "standard"


class IRValidationError(ValueError):
    """Raised when raw extracted/uploaded JSON does not match the IR contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IRValidationError(message)


def _as_float(value: Any, field_name: str, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        raise IRValidationError(f"Field '{field_name}' must be numeric, got {value!r}")


@dataclass
class DiagramNode:
    id: str
    label: str
    shape: str = DEFAULT_SHAPE
    x: float = 0.0
    y: float = 0.0
    width: float = 120.0
    height: float = 60.0

    @staticmethod
    def from_dict(d: Dict[str, Any], index: int) -> "DiagramNode":
        _require(isinstance(d, dict), f"nodes[{index}] must be an object")
        node_id = d.get("id")
        _require(bool(node_id) and isinstance(node_id, str), f"nodes[{index}].id is required and must be a string")
        label = d.get("label", "")
        _require(isinstance(label, str), f"nodes[{index}].label must be a string")
        shape = d.get("shape", DEFAULT_SHAPE) or DEFAULT_SHAPE
        if shape not in VALID_SHAPES:
            shape = DEFAULT_SHAPE  # tolerate unknown shapes from the VLM rather than hard-fail
        return DiagramNode(
            id=node_id,
            label=label,
            shape=shape,
            x=_as_float(d.get("x"), f"nodes[{index}].x", 0.0),
            y=_as_float(d.get("y"), f"nodes[{index}].y", 0.0),
            width=_as_float(d.get("width"), f"nodes[{index}].width", 120.0) or 120.0,
            height=_as_float(d.get("height"), f"nodes[{index}].height", 60.0) or 60.0,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DiagramEdge:
    id: str
    source: str
    target: str
    label: str = ""
    style: str = DEFAULT_EDGE_STYLE
    arrow: str = DEFAULT_ARROW

    @staticmethod
    def from_dict(d: Dict[str, Any], index: int) -> "DiagramEdge":
        _require(isinstance(d, dict), f"edges[{index}] must be an object")
        edge_id = d.get("id") or f"e{index}"
        source = d.get("source")
        target = d.get("target")
        _require(bool(source), f"edges[{index}].source is required")
        _require(bool(target), f"edges[{index}].target is required")
        style = d.get("style", DEFAULT_EDGE_STYLE) or DEFAULT_EDGE_STYLE
        if style not in VALID_EDGE_STYLES:
            style = DEFAULT_EDGE_STYLE
        arrow = d.get("arrow", DEFAULT_ARROW) or DEFAULT_ARROW
        if arrow not in VALID_ARROWS:
            arrow = DEFAULT_ARROW
        return DiagramEdge(
            id=str(edge_id),
            source=str(source),
            target=str(target),
            label=d.get("label", "") or "",
            style=style,
            arrow=arrow,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DiagramIR:
    diagram_type: str
    nodes: List[DiagramNode] = field(default_factory=list)
    edges: List[DiagramEdge] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DiagramIR":
        _require(isinstance(d, dict), "Top-level IR must be a JSON object")
        diagram_type = d.get("diagram_type", "diagram") or "diagram"
        raw_nodes = d.get("nodes", [])
        raw_edges = d.get("edges", [])
        _require(isinstance(raw_nodes, list), "'nodes' must be a list")
        _require(isinstance(raw_edges, list), "'edges' must be a list")

        nodes = [DiagramNode.from_dict(n, i) for i, n in enumerate(raw_nodes)]
        node_ids = {n.id for n in nodes}

        edges: List[DiagramEdge] = []
        warnings: List[str] = []
        for i, e in enumerate(raw_edges):
            edge = DiagramEdge.from_dict(e, i)
            if edge.source not in node_ids or edge.target not in node_ids:
                warnings.append(
                    f"Dropped edge '{edge.id}' ({edge.source} -> {edge.target}): "
                    f"references a node id not present in 'nodes'."
                )
                continue
            edges.append(edge)

        return DiagramIR(diagram_type=diagram_type, nodes=nodes, edges=edges, warnings=warnings)

    @staticmethod
    def from_json_text(text: str) -> "DiagramIR":
        obj = extract_json_object(text)
        return DiagramIR.from_dict(obj)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "diagram_type": self.diagram_type,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


def extract_json_object(text: str) -> Dict[str, Any]:
    """
    Robustly pull a single JSON object out of raw model output that may be
    wrapped in markdown code fences or preceded/followed by prose.
    """
    if not text or not text.strip():
        raise IRValidationError("Empty response: nothing to parse as JSON.")

    cleaned = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise IRValidationError("Could not locate a JSON object in the response.")

    candidate = cleaned[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise IRValidationError(f"Extracted text is not valid JSON: {exc}") from exc
