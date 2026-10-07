"""
app.py
------
Streamlit UI for the AI Elevate Diagram Extraction POC.

Run with:
    streamlit run app.py

Pipeline shown in the UI mirrors the architecture:
  Student Hand-Drawn Image
    -> Azure OpenAI (GPT-4.1 VLM)          [Extract tab]
    -> Normalized Diagram IR (JSON)        [Extract tab]
    -> Python draw.io Builder              [Extract tab]
    -> Evaluation & Grading Layer          [Evaluate tab]
"""

from __future__ import annotations

import json

import streamlit as st

from azure_client import AzureConfigError, AzureVLMExtractor
from diagram_renderer import render_ir_svg
from drawio_builder import build_drawio_xml
from evaluator import evaluate
from ir_schema import DiagramIR, IRValidationError
from mock_data import get_mock_extraction, get_sample_ground_truth

st.set_page_config(page_title="AI Elevate — Diagram Extraction POC", page_icon="🧩", layout="wide")

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "extracted_ir" not in st.session_state:
    st.session_state.extracted_ir = None  # type: DiagramIR | None
if "drawio_xml" not in st.session_state:
    st.session_state.drawio_xml = None  # type: str | None
if "last_error" not in st.session_state:
    st.session_state.last_error = None
if "input_image_bytes" not in st.session_state:
    st.session_state.input_image_bytes = None  # type: bytes | None
if "extracted_svg" not in st.session_state:
    st.session_state.extracted_svg = None  # type: str | None

# ---------------------------------------------------------------------------
# Sidebar: Azure config + mode
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuration")

demo_mode = st.sidebar.checkbox(
    "Demo Mode (no Azure credentials needed)",
    value=True,
    help="Uses bundled sample data to exercise the full pipeline without calling Azure OpenAI.",
)

st.sidebar.markdown("---")
st.sidebar.subheader("Azure OpenAI (GPT-4.1)")
st.sidebar.caption("Only needed when Demo Mode is off. Values default to your .env if set.")

env_extractor = AzureVLMExtractor()
azure_endpoint = st.sidebar.text_input("Endpoint", value=env_extractor.endpoint, placeholder="https://<resource>.openai.azure.com")
azure_key = st.sidebar.text_input("API Key", value=env_extractor.api_key, type="password")
azure_deployment = st.sidebar.text_input("Deployment name", value=env_extractor.deployment, placeholder="gpt-4.1")
azure_api_version = st.sidebar.text_input("API version", value=env_extractor.api_version)

st.sidebar.markdown("---")
st.sidebar.caption("AI Elevate — Diagram Extraction POC")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🧩 AI Elevate — Diagram Extraction POC")
st.markdown(
    "Reconstructs a student's hand-drawn academic diagram as an editable **draw.io** "
    "diagram, so automated evaluation layers can inspect, mark, and score drawn answers "
    "alongside handwritten text."
)

with st.expander("Pipeline architecture", expanded=False):
    st.code(
        "Student Hand-Drawn Image\n"
        "        |\n"
        "        v\n"
        "Azure OpenAI (GPT-4.1 VLM)   --> Emits Normalized Diagram IR (JSON)\n"
        "        |\n"
        "        v\n"
        "Python draw.io Builder      --> Generates .drawio / .mxgraph.xml deterministically\n"
        "        |\n"
        "        v\n"
        "Evaluation & Grading Layer  --> Scores extracted IR against examiner Ground Truth",
        language="text",
    )

tab_extract, tab_evaluate, tab_about = st.tabs(["1️⃣ Extract & Build", "2️⃣ Evaluate", "ℹ️ About"])

# ---------------------------------------------------------------------------
# TAB 1: Extract & Build
# ---------------------------------------------------------------------------
with tab_extract:
    col_input, col_output = st.columns(2)

    with col_input:
        st.subheader("Input")
        uploaded_file = None
        if demo_mode:
            st.info("Demo Mode is on — click **Run Extraction** to use a bundled sample instead of an upload.")
        else:
            uploaded_file = st.file_uploader(
                "Upload the student's hand-drawn diagram",
                type=["png", "jpg", "jpeg", "webp"],
            )
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded diagram", use_container_width=True)

        run_clicked = st.button("▶ Run Extraction", type="primary", use_container_width=True)

        if run_clicked:
            st.session_state.last_error = None
            try:
                if demo_mode:
                    st.session_state.extracted_ir = get_mock_extraction()
                    st.session_state.input_image_bytes = None  # no source image in Demo Mode
                else:
                    if uploaded_file is None:
                        raise IRValidationError("Please upload an image first (or enable Demo Mode).")
                    extractor = AzureVLMExtractor(
                        endpoint=azure_endpoint,
                        api_key=azure_key,
                        api_version=azure_api_version,
                        deployment=azure_deployment,
                    )
                    with st.spinner(f"Calling Azure OpenAI deployment '{azure_deployment}' ..."):
                        st.session_state.extracted_ir = extractor.extract(
                            uploaded_file.getvalue(),
                            mime_type=uploaded_file.type or "image/png",
                        )
                    st.session_state.input_image_bytes = uploaded_file.getvalue()
                st.session_state.drawio_xml = None  # invalidate stale build
                st.session_state.extracted_svg = render_ir_svg(st.session_state.extracted_ir)
            except (AzureConfigError, IRValidationError) as exc:
                st.session_state.last_error = str(exc)
            except Exception as exc:  # last-resort guard so the UI never hard-crashes
                st.session_state.last_error = f"Unexpected error: {exc}"

        if st.session_state.last_error:
            st.error(st.session_state.last_error)

        if st.session_state.input_image_bytes is not None:
            st.image(st.session_state.input_image_bytes, caption="Input image", use_container_width=True)
        elif st.session_state.extracted_ir is not None:
            st.caption("No source image to show (Demo Mode used bundled sample data instead of an upload).")

    with col_output:
        st.subheader("Extracted Diagram — Coordinate Graph")
        ir = st.session_state.extracted_ir
        if ir is None:
            st.caption("Run an extraction to see the extracted diagram plotted here, next to the input image.")
        else:
            if ir.warnings:
                for w in ir.warnings:
                    st.warning(w)
            if st.session_state.extracted_svg:
                st.image(st.session_state.extracted_svg, use_container_width=True)
                st.caption(
                    f"{len(ir.nodes)} node(s), {len(ir.edges)} edge(s) — plotted at their literal "
                    "(x, y) / (width, height) IR coordinates on the normalized 0-1000 grid."
                )

            with st.expander("View extracted diagram IR (JSON)"):
                st.json(ir.to_dict())

            build_clicked = st.button("🛠 Generate draw.io file", use_container_width=True)
            if build_clicked:
                st.session_state.drawio_xml = build_drawio_xml(ir)

            if st.session_state.drawio_xml:
                with st.expander("View generated .drawio XML"):
                    st.code(st.session_state.drawio_xml, language="xml")
                st.download_button(
                    "⬇ Download .drawio file",
                    data=st.session_state.drawio_xml,
                    file_name="extracted_diagram.drawio",
                    mime="application/xml",
                    use_container_width=True,
                )
                st.caption("Open the downloaded file at app.diagrams.net (File → Open From → Device) to view/edit it.")

# ---------------------------------------------------------------------------
# TAB 2: Evaluate
# ---------------------------------------------------------------------------
with tab_evaluate:
    st.subheader("Score the extracted diagram against an examiner ground truth")

    if st.session_state.extracted_ir is None:
        st.info("Run an extraction in the **Extract & Build** tab first.")
    else:
        gt_source = st.radio(
            "Ground truth source",
            ["Use bundled sample ground truth", "Paste / upload ground-truth JSON"],
            horizontal=True,
        )

        ground_truth_ir = None
        gt_error = None

        if gt_source == "Use bundled sample ground truth":
            ground_truth_ir = get_sample_ground_truth()
            with st.expander("View sample ground truth"):
                st.json(ground_truth_ir.to_dict())
        else:
            gt_file = st.file_uploader("Upload ground-truth IR JSON", type=["json"], key="gt_upload")
            gt_text = st.text_area(
                "...or paste ground-truth IR JSON here",
                height=180,
                placeholder='{"diagram_type": "flowchart", "nodes": [...], "edges": [...]}',
            )
            raw_text = None
            if gt_file is not None:
                raw_text = gt_file.getvalue().decode("utf-8", errors="replace")
            elif gt_text.strip():
                raw_text = gt_text

            if raw_text:
                try:
                    ground_truth_ir = DiagramIR.from_json_text(raw_text)
                except IRValidationError as exc:
                    gt_error = str(exc)

        if gt_error:
            st.error(f"Ground truth JSON is invalid: {gt_error}")

        score_clicked = st.button("📊 Score Extraction", type="primary", disabled=ground_truth_ir is None)

        if score_clicked and ground_truth_ir is not None:
            result = evaluate(st.session_state.extracted_ir, ground_truth_ir)

            st.markdown("### Overall Score")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Overall", f"{result.overall_score:.1f} / 100")
            m2.metric("Node F1", f"{result.node_f1 * 100:.1f}%")
            m3.metric("Edge F1", f"{result.edge_f1 * 100:.1f}%")
            m4.metric("Shape Accuracy", f"{result.shape_accuracy * 100:.1f}%")

            st.markdown("### Node-Level Matches")
            node_rows = [
                {
                    "Ground Truth Label": m.gt_label,
                    "Matched Extracted Label": m.extracted_label or "— (missing)",
                    "Similarity": round(m.similarity, 2),
                    "Shape Correct": "—" if m.shape_correct is None else ("✅" if m.shape_correct else "❌"),
                }
                for m in result.node_matches
            ]
            st.dataframe(node_rows, use_container_width=True, hide_index=True)

            if result.unmatched_extracted_node_labels:
                st.markdown("**Extra nodes in extraction (no ground-truth match):**")
                st.write(", ".join(result.unmatched_extracted_node_labels))

            st.markdown("### Edge-Level Matches")
            edge_rows = [
                {
                    "Ground Truth Edge": f"{m.gt_source_label} → {m.gt_target_label}"
                    + (f"  [{m.gt_label}]" if m.gt_label else ""),
                    "Matched": "✅" if m.matched else "❌",
                }
                for m in result.edge_matches
            ]
            st.dataframe(edge_rows, use_container_width=True, hide_index=True)

            with st.expander("Raw evaluation JSON"):
                st.json(result.to_dict())

# ---------------------------------------------------------------------------
# TAB 3: About
# ---------------------------------------------------------------------------
with tab_about:
    st.subheader("About this POC")
    st.markdown(
        """
This proof of concept implements the four-stage workflow end-to-end:

1. **Student Hand-Drawn Image** — uploaded by the grader/teacher, or a scan pulled from an exam pipeline.
2. **Azure OpenAI (GPT-4.1 VLM)** — reads the image and emits a **Normalized Diagram IR** (JSON):
   a list of typed nodes (shape, label, position) and edges (source, target, label, style).
3. **Python draw.io Builder** — deterministically converts that IR into a `.drawio` / mxGraph XML
   file, with no randomness: the same IR always produces the same file, which matters for
   auditability in a grading context.
4. **Evaluation & Grading Layer** — matches extracted nodes/edges against an examiner-authored
   ground-truth IR (by label similarity), and reports precision/recall/F1 for nodes and edges,
   shape accuracy, and an overall weighted score.

**Design choices worth noting:**
- The IR schema and draw.io builder have **zero third-party dependencies** (pure Python stdlib) —
  only the Azure OpenAI call needs the `openai` package, and only the UI needs `streamlit`.
- **Demo Mode** lets you exercise the entire pipeline immediately, with no Azure account, using
  bundled sample data — useful for a first run or when credentials aren't ready yet.
- Malformed model output (extra prose, markdown fences, edges pointing at unknown node ids) is
  handled defensively rather than crashing the app — dropped/flagged issues surface as warnings.

**Files in this project:**
- `ir_schema.py` — the Diagram IR data model + robust JSON parsing
- `azure_client.py` — Azure OpenAI GPT-4.1 vision call
- `drawio_builder.py` — deterministic IR → `.drawio` XML
- `evaluator.py` — IR vs. ground-truth scoring
- `mock_data.py` — bundled sample IR + ground truth for Demo Mode
- `app.py` — this Streamlit UI
- `main.py` — headless CLI equivalent of the same pipeline
        """
    )
