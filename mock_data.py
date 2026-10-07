"""
mock_data.py
------------
Bundled sample data so the full pipeline (extraction -> draw.io ->
evaluation) can be exercised end-to-end with zero Azure OpenAI
credentials -- useful for first-run verification, demos, and offline
development.

`MOCK_EXTRACTED_IR` intentionally differs slightly from
`SAMPLE_GROUND_TRUTH_IR` (one wrong shape, one paraphrased label, one
missing edge) so the evaluation tab has something meaningful to show
on first run instead of a trivial 100% score.
"""

from ir_schema import DiagramIR

SAMPLE_GROUND_TRUTH_IR = {
    "diagram_type": "flowchart",
    "nodes": [
        {"id": "g1", "label": "Start", "shape": "ellipse", "x": 400, "y": 20, "width": 160, "height": 60},
        {"id": "g2", "label": "Read Input", "shape": "rectangle", "x": 380, "y": 150, "width": 200, "height": 60},
        {"id": "g3", "label": "Is Valid?", "shape": "diamond", "x": 400, "y": 300, "width": 160, "height": 100},
        {"id": "g4", "label": "Show Error", "shape": "rectangle", "x": 650, "y": 320, "width": 200, "height": 60},
        {"id": "g5", "label": "Process Data", "shape": "rectangle", "x": 380, "y": 470, "width": 200, "height": 60},
        {"id": "g6", "label": "End", "shape": "ellipse", "x": 400, "y": 600, "width": 160, "height": 60},
    ],
    "edges": [
        {"id": "ge1", "source": "g1", "target": "g2"},
        {"id": "ge2", "source": "g2", "target": "g3"},
        {"id": "ge3", "source": "g3", "target": "g5", "label": "yes"},
        {"id": "ge4", "source": "g3", "target": "g4", "label": "no"},
        {"id": "ge5", "source": "g4", "target": "g2", "style": "dashed"},
        {"id": "ge6", "source": "g5", "target": "g6"},
    ],
}

# A deliberately imperfect "extraction" of the same diagram, standing in
# for what a real VLM call might return: label paraphrased, one shape
# misread, and one edge missed -- so Demo Mode shows a realistic,
# non-trivial score rather than a hollow 100%.
MOCK_EXTRACTED_IR = {
    "diagram_type": "flowchart",
    "nodes": [
        {"id": "n1", "label": "Start", "shape": "ellipse", "x": 410, "y": 25, "width": 150, "height": 55},
        {"id": "n2", "label": "Read the Input", "shape": "rectangle", "x": 390, "y": 155, "width": 190, "height": 55},
        {"id": "n3", "label": "Valid?", "shape": "rectangle", "x": 405, "y": 305, "width": 150, "height": 90},
        {"id": "n4", "label": "Show Error", "shape": "rectangle", "x": 645, "y": 325, "width": 190, "height": 55},
        {"id": "n5", "label": "Process Data", "shape": "rectangle", "x": 390, "y": 475, "width": 190, "height": 55},
        {"id": "n6", "label": "End", "shape": "ellipse", "x": 405, "y": 605, "width": 150, "height": 55},
    ],
    "edges": [
        {"id": "e1", "source": "n1", "target": "n2"},
        {"id": "e2", "source": "n2", "target": "n3"},
        {"id": "e3", "source": "n3", "target": "n5", "label": "yes"},
        {"id": "e4", "source": "n3", "target": "n4", "label": "no"},
        {"id": "e6", "source": "n5", "target": "n6"},
        # note: the "Show Error -> Read the Input" (dashed retry) edge is
        # missing here on purpose, simulating a plausible extraction gap.
    ],
}


def get_sample_ground_truth() -> DiagramIR:
    return DiagramIR.from_dict(SAMPLE_GROUND_TRUTH_IR)


def get_mock_extraction() -> DiagramIR:
    return DiagramIR.from_dict(MOCK_EXTRACTED_IR)
