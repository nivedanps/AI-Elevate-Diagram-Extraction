# AI Elevate — Diagram Extraction POC

Reconstructs a student's hand-drawn academic diagram as an editable **draw.io**
diagram, enabling automated evaluation layers to inspect, mark, and score drawn
answers alongside handwritten text.

```text
Student Hand-Drawn Image
        │
        ▼
Azure OpenAI (GPT-4.1 VLM)   ──►  Emits Normalized Diagram IR (JSON)
        │
        ▼
Python draw.io Builder       ──►  Generates .drawio / .mxgraph.xml deterministically
        │
        ▼
Evaluation & Grading Layer   ──►  Scores extracted IR against examiner Ground Truth
```

This is a plain Python project (Streamlit UI + a small CLI) — no special
runtime beyond Python 3.9+ is required, so it runs the same whether you launch
it by hand, from an IDE, or via an agentic tool like **Antigravity**: open the
folder, install the requirements, and run the `streamlit` command below.

---

## 1. Setup

```bash
pip install -r requirements.txt
```

Only needed if you'll call the real Azure OpenAI model (skip this if you're
only using **Demo Mode**, see below):

```bash
cp .env.example .env
# then edit .env and fill in your Azure OpenAI endpoint / key / deployment
```

## 2. Run the app

```bash
streamlit run app.py
```

This opens a browser tab with three tabs:

1. **Extract & Build** — upload a hand-drawn diagram image, run extraction,
   view the resulting Diagram IR (JSON), and generate/download a `.drawio` file.
2. **Evaluate** — score the extracted IR against a ground-truth IR (a bundled
   sample, or your own pasted/uploaded JSON), with a full precision/recall/F1
   breakdown at the node and edge level.
3. **About** — architecture notes and design rationale.

**Demo Mode** (checked by default in the sidebar) runs the entire pipeline
using bundled sample data, so you can verify everything works with **zero
Azure credentials**. Uncheck it once you have Azure OpenAI configured to
process real uploaded images.

## 3. Run the CLI (headless)

```bash
# Try the whole pipeline with bundled sample data, no Azure needed:
python main.py --demo --output demo.drawio

# Real run against Azure OpenAI:
python main.py --image path/to/student_answer.png --output extracted.drawio

# Real run + score against an examiner ground-truth file:
python main.py --image path/to/student_answer.png --ground-truth gt.json --output extracted.drawio
```

## 4. Verify the project is working

A dependency-free sanity check exercises the IR schema, the draw.io builder
(including a determinism check), and the evaluator, with no network calls:

```bash
python test_pipeline.py
```

You should see 13/13 checks pass.

---

## Project layout

| File | Purpose |
|---|---|
| `ir_schema.py` | Normalized Diagram IR data model, validation, robust JSON parsing (handles markdown-fenced or noisy model output) |
| `azure_client.py` | Azure OpenAI GPT-4.1 vision call: image in, validated `DiagramIR` out |
| `drawio_builder.py` | Deterministic `DiagramIR` → `.drawio` (mxGraph XML) converter |
| `evaluator.py` | Scores an extracted `DiagramIR` against an examiner ground-truth `DiagramIR` |
| `mock_data.py` | Bundled sample ground truth + a deliberately imperfect mock extraction, for Demo Mode |
| `app.py` | Streamlit UI |
| `main.py` | Headless CLI equivalent of the same pipeline |
| `test_pipeline.py` | Offline automated sanity checks |

## Diagram IR schema

```json
{
  "diagram_type": "flowchart",
  "nodes": [
    {
      "id": "n1",
      "label": "Start",
      "shape": "rectangle | ellipse | diamond | parallelogram | circle | hexagon | cylinder | text",
      "x": 400, "y": 20, "width": 160, "height": 60
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "n1",
      "target": "n2",
      "label": "yes",
      "style": "solid | dashed",
      "arrow": "standard | open | none"
    }
  ]
}
```

Node coordinates are on a normalized 0–1000 canvas grid; the draw.io builder
scales this into actual draw.io coordinate space (see `CANVAS_SCALE` in
`drawio_builder.py`).

## Notes on scoring

The evaluator matches ground-truth nodes to extracted nodes by label
similarity (`difflib`, no extra dependency), then uses that correspondence to
check whether each ground-truth edge has a matching extracted edge between
the *matched* nodes. The final score blends node F1, edge F1, and shape
accuracy (weights in `evaluator.SCORE_WEIGHTS`) — tune these to match how
strict your rubric should be.

## Troubleshooting

- **"Azure OpenAI is not configured"** — set the four `AZURE_OPENAI_*`
  values in `.env`, or fill them into the sidebar fields directly, or just
  use Demo Mode.
- **Model response isn't valid JSON** — the app/CLI will show a clear error
  rather than crashing; `ir_schema.extract_json_object` already strips
  markdown code fences, so this should be rare. If it happens often, lower
  `temperature` further or shorten `SYSTEM_PROMPT` in `azure_client.py`.
- **An edge references a node id that doesn't exist** — this is handled
  automatically: the edge is dropped and a warning is surfaced rather than
  the app failing.
