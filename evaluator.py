"""
evaluator.py
------------
Scores an extracted `DiagramIR` against an examiner-authored ground-truth
`DiagramIR`. Pure stdlib (difflib for label similarity) -- no extra
dependency needed just to grade a diagram.

Matching strategy
------------------
1. Greedy label-similarity matching of ground-truth nodes to extracted
   nodes (difflib.SequenceMatcher ratio), above a configurable threshold.
2. Shape-accuracy is measured only across matched node pairs.
3. Edges are scored using the node-id correspondence discovered in
   step 1: a ground-truth edge counts as matched if there exists an
   extracted edge between the two *matched* extracted nodes (direction
   sensitive).
4. Final score is a weighted blend of node F1, edge F1, and shape
   accuracy -- weights are tunable via `SCORE_WEIGHTS`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

from ir_schema import DiagramIR, DiagramNode

LABEL_MATCH_THRESHOLD = 0.55  # 0..1, minimum similarity to consider two nodes "the same"
SCORE_WEIGHTS = {
    "node_f1": 0.45,
    "edge_f1": 0.40,
    "shape_accuracy": 0.15,
}


def _label_similarity(a: str, b: str) -> float:
    a_norm = (a or "").strip().lower()
    b_norm = (b or "").strip().lower()
    if not a_norm and not b_norm:
        return 1.0
    if not a_norm or not b_norm:
        return 0.0
    return SequenceMatcher(None, a_norm, b_norm).ratio()


@dataclass
class NodeMatch:
    gt_id: str
    gt_label: str
    extracted_id: Optional[str]
    extracted_label: Optional[str]
    similarity: float
    shape_correct: Optional[bool]  # None if unmatched


@dataclass
class EdgeMatch:
    gt_source_label: str
    gt_target_label: str
    gt_label: str
    matched: bool


@dataclass
class EvaluationResult:
    node_precision: float
    node_recall: float
    node_f1: float
    edge_precision: float
    edge_recall: float
    edge_f1: float
    shape_accuracy: float
    overall_score: float  # 0..100
    node_matches: List[NodeMatch] = field(default_factory=list)
    edge_matches: List[EdgeMatch] = field(default_factory=list)
    unmatched_extracted_node_labels: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "overall_score": round(self.overall_score, 2),
            "node_precision": round(self.node_precision, 4),
            "node_recall": round(self.node_recall, 4),
            "node_f1": round(self.node_f1, 4),
            "edge_precision": round(self.edge_precision, 4),
            "edge_recall": round(self.edge_recall, 4),
            "edge_f1": round(self.edge_f1, 4),
            "shape_accuracy": round(self.shape_accuracy, 4),
            "node_matches": [
                {
                    "ground_truth": m.gt_label,
                    "matched_extracted": m.extracted_label,
                    "similarity": round(m.similarity, 3),
                    "shape_correct": m.shape_correct,
                }
                for m in self.node_matches
            ],
            "edge_matches": [
                {
                    "ground_truth_edge": f"{m.gt_source_label} -> {m.gt_target_label}"
                    + (f" [{m.gt_label}]" if m.gt_label else ""),
                    "matched": m.matched,
                }
                for m in self.edge_matches
            ],
            "unmatched_extracted_nodes": self.unmatched_extracted_node_labels,
        }


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _match_nodes(
    gt_nodes: List[DiagramNode], ex_nodes: List[DiagramNode]
) -> Tuple[Dict[str, str], List[NodeMatch]]:
    """Greedy best-first matching by label similarity. Returns {gt_id: extracted_id} and detail rows."""
    candidates = []
    for gi, g in enumerate(gt_nodes):
        for ei, e in enumerate(ex_nodes):
            sim = _label_similarity(g.label, e.label)
            candidates.append((sim, gi, ei))
    candidates.sort(key=lambda t: t[0], reverse=True)

    matched_gt: Dict[str, str] = {}
    used_gt_idx: set = set()
    used_ex_idx: set = set()
    match_rows: List[NodeMatch] = []

    for sim, gi, ei in candidates:
        if gi in used_gt_idx or ei in used_ex_idx:
            continue
        if sim < LABEL_MATCH_THRESHOLD:
            continue
        g, e = gt_nodes[gi], ex_nodes[ei]
        matched_gt[g.id] = e.id
        used_gt_idx.add(gi)
        used_ex_idx.add(ei)
        match_rows.append(
            NodeMatch(
                gt_id=g.id,
                gt_label=g.label,
                extracted_id=e.id,
                extracted_label=e.label,
                similarity=sim,
                shape_correct=(g.shape == e.shape),
            )
        )

    # Any ground-truth nodes left unmatched
    for gi, g in enumerate(gt_nodes):
        if gi not in used_gt_idx:
            match_rows.append(
                NodeMatch(
                    gt_id=g.id,
                    gt_label=g.label,
                    extracted_id=None,
                    extracted_label=None,
                    similarity=0.0,
                    shape_correct=None,
                )
            )

    match_rows.sort(key=lambda m: gt_nodes.index(next(n for n in gt_nodes if n.id == m.gt_id)))
    return matched_gt, match_rows


def evaluate(extracted: DiagramIR, ground_truth: DiagramIR) -> EvaluationResult:
    gt_nodes = ground_truth.nodes
    ex_nodes = extracted.nodes

    matched_gt_to_ex, node_match_rows = _match_nodes(gt_nodes, ex_nodes)

    matched_ex_ids = set(matched_gt_to_ex.values())
    unmatched_extracted = [n.label for n in ex_nodes if n.id not in matched_ex_ids]

    true_positive_nodes = len(matched_gt_to_ex)
    node_precision = true_positive_nodes / len(ex_nodes) if ex_nodes else (1.0 if not gt_nodes else 0.0)
    node_recall = true_positive_nodes / len(gt_nodes) if gt_nodes else 1.0
    node_f1 = _f1(node_precision, node_recall)

    shape_checks = [m.shape_correct for m in node_match_rows if m.shape_correct is not None]
    shape_accuracy = (sum(1 for s in shape_checks if s) / len(shape_checks)) if shape_checks else 0.0

    ex_edge_pairs = {(e.source, e.target) for e in extracted.edges}
    edge_match_rows: List[EdgeMatch] = []
    edge_true_positive = 0
    gt_node_by_id = {n.id: n for n in gt_nodes}

    for edge in ground_truth.edges:
        ex_source = matched_gt_to_ex.get(edge.source)
        ex_target = matched_gt_to_ex.get(edge.target)
        matched = (
            ex_source is not None
            and ex_target is not None
            and (ex_source, ex_target) in ex_edge_pairs
        )
        if matched:
            edge_true_positive += 1
        edge_match_rows.append(
            EdgeMatch(
                gt_source_label=gt_node_by_id.get(edge.source, DiagramNode(id="?", label="?")).label,
                gt_target_label=gt_node_by_id.get(edge.target, DiagramNode(id="?", label="?")).label,
                gt_label=edge.label,
                matched=matched,
            )
        )

    edge_precision = edge_true_positive / len(extracted.edges) if extracted.edges else (1.0 if not ground_truth.edges else 0.0)
    edge_recall = edge_true_positive / len(ground_truth.edges) if ground_truth.edges else 1.0
    edge_f1 = _f1(edge_precision, edge_recall)

    overall = (
        SCORE_WEIGHTS["node_f1"] * node_f1
        + SCORE_WEIGHTS["edge_f1"] * edge_f1
        + SCORE_WEIGHTS["shape_accuracy"] * shape_accuracy
    ) * 100

    return EvaluationResult(
        node_precision=node_precision,
        node_recall=node_recall,
        node_f1=node_f1,
        edge_precision=edge_precision,
        edge_recall=edge_recall,
        edge_f1=edge_f1,
        shape_accuracy=shape_accuracy,
        overall_score=overall,
        node_matches=node_match_rows,
        edge_matches=edge_match_rows,
        unmatched_extracted_node_labels=unmatched_extracted,
    )
