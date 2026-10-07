"""
test_pipeline.py
-----------------
Zero-dependency sanity check for the deterministic parts of the pipeline
(IR schema, draw.io builder, evaluator). Does NOT call Azure OpenAI, so
it can be run immediately after cloning, with no credentials and no
extra installs, to confirm the project is working correctly.

Run with:
    python test_pipeline.py
"""

import sys
import xml.etree.ElementTree as ET

from drawio_builder import build_drawio_xml
from evaluator import evaluate
from ir_schema import DiagramIR, IRValidationError, extract_json_object
from mock_data import get_mock_extraction, get_sample_ground_truth

PASS = "PASS"
FAIL = "FAIL"


def check(label: str, condition: bool, results: list) -> None:
    status = PASS if condition else FAIL
    results.append((status, label))
    print(f"[{status}] {label}")


def main() -> int:
    results = []

    # 1. IR parsing + validation
    valid_ir = DiagramIR.from_dict(
        {
            "diagram_type": "flowchart",
            "nodes": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}],
            "edges": [{"id": "e1", "source": "a", "target": "b"}, {"id": "e2", "source": "a", "target": "zzz"}],
        }
    )
    check("IR parses valid dict", len(valid_ir.nodes) == 2, results)
    check("IR drops edges with unknown node ids", len(valid_ir.edges) == 1, results)
    check("IR records a warning for the dropped edge", len(valid_ir.warnings) == 1, results)

    try:
        DiagramIR.from_dict({"nodes": "not-a-list", "edges": []})
        check("IR rejects malformed 'nodes' field", False, results)
    except IRValidationError:
        check("IR rejects malformed 'nodes' field", True, results)

    fenced = '```json\n{"diagram_type": "x", "nodes": [], "edges": []}\n```'
    parsed = extract_json_object(fenced)
    check("extract_json_object handles markdown fences", parsed.get("diagram_type") == "x", results)

    # 2. draw.io builder: determinism + XML validity
    gt = get_sample_ground_truth()
    xml_1 = build_drawio_xml(gt)
    xml_2 = build_drawio_xml(gt)
    check("draw.io builder is deterministic", xml_1 == xml_2, results)

    try:
        root = ET.fromstring(xml_1)
        check("Generated .drawio is well-formed XML", root.tag == "mxfile", results)
    except ET.ParseError:
        check("Generated .drawio is well-formed XML", False, results)

    node_count_in_xml = xml_1.count('vertex="1"')
    check(
        "draw.io XML contains one vertex per IR node",
        node_count_in_xml == len(gt.nodes),
        results,
    )

    # 3. Evaluator: sanity on identical IR (should score 100) and mock vs ground truth
    perfect = evaluate(gt, gt)
    check("Evaluator scores identical IR as ~100", round(perfect.overall_score) == 100, results)

    mock_result = evaluate(get_mock_extraction(), gt)
    check(
        "Evaluator scores imperfect mock extraction between 0 and 100",
        0 < mock_result.overall_score < 100,
        results,
    )
    check(
        "Evaluator correctly finds all 6 ground-truth nodes matched",
        sum(1 for m in mock_result.node_matches if m.extracted_id is not None) == 6,
        results,
    )
    check(
        "Evaluator correctly flags the one wrong shape",
        sum(1 for m in mock_result.node_matches if m.shape_correct is False) == 1,
        results,
    )
    check(
        "Evaluator correctly flags the one missing edge",
        sum(1 for m in mock_result.edge_matches if not m.matched) == 1,
        results,
    )

    print()
    failures = [r for r in results if r[0] == FAIL]
    if failures:
        print(f"{len(failures)} check(s) FAILED.")
        return 1
    print(f"All {len(results)} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
