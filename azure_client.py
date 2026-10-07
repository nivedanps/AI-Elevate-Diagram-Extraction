"""
azure_client.py
----------------
Wraps Azure OpenAI's GPT-4.1 vision-language model to turn a photo/scan
of a student's hand-drawn diagram into the normalized Diagram IR (JSON).

This is the only module with a third-party dependency (`openai`), and
it is imported lazily so the rest of the app (schema, builder,
evaluator, and even the Streamlit UI in demo mode) works with zero
network calls and zero Azure setup.
"""

from __future__ import annotations

import base64
import os
from typing import Optional

try:
    from dotenv import load_dotenv

    load_dotenv()  # populate os.environ from a local .env file, if present
except ImportError:
    pass  # python-dotenv is optional; env vars can also be set directly

from ir_schema import DiagramIR, IRValidationError

SYSTEM_PROMPT = """You are a precise diagram digitization engine used in an academic \
grading pipeline. You will be shown a photo or scan of a STUDENT'S HAND-DRAWN diagram \
(flowchart, block diagram, circuit sketch, tree, or similar academic diagram).

Your job: reconstruct the diagram as a normalized JSON Intermediate Representation (IR). \
Be faithful to what the student actually drew -- do not "correct" their logic, wording, \
or structure. Read handwritten labels as literally as legible.

Respond with ONLY a single JSON object (no markdown fences, no commentary) matching \
exactly this schema:

{
  "diagram_type": "<short free-text label, e.g. 'flowchart', 'block_diagram', 'circuit', 'tree'>",
  "nodes": [
    {
      "id": "<short unique string id you invent, e.g. 'n1'>",
      "label": "<the text written inside/next to the shape>",
      "shape": "<one of: rectangle, ellipse, diamond, parallelogram, circle, hexagon, cylinder, text>",
      "x": <number 0-1000, horizontal position of the shape's top-left corner on a normalized canvas>,
      "y": <number 0-1000, vertical position of the shape's top-left corner on a normalized canvas>,
      "width": <number, approximate shape width on the same 0-1000 scale>,
      "height": <number, approximate shape height on the same 0-1000 scale>
    }
  ],
  "edges": [
    {
      "id": "<short unique string id you invent, e.g. 'e1'>",
      "source": "<id of the node the arrow starts at>",
      "target": "<id of the node the arrow points to>",
      "label": "<text written on/near the arrow, or empty string if none>",
      "style": "<'solid' or 'dashed'>",
      "arrow": "<'standard', 'open', or 'none'>"
    }
  ]
}

Rules:
- Every edge's "source" and "target" MUST reference an "id" that appears in "nodes".
- Preserve top-to-bottom / left-to-right layout proportionally using the 0-1000 grid.
- If a shape's type is ambiguous, default to "rectangle".
- If unsure of a label because handwriting is unclear, give your best-effort reading \
rather than leaving it blank.
- Do not invent nodes or connections that are not visibly present in the image."""

USER_PROMPT = (
    "Extract the diagram in this image into the normalized IR JSON schema described "
    "in the system prompt. Respond with the JSON object only."
)


class AzureConfigError(RuntimeError):
    """Raised when Azure OpenAI credentials/config are missing or invalid."""


class AzureVLMExtractor:
    """Thin wrapper around the Azure OpenAI Chat Completions vision API."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
        deployment: Optional[str] = None,
    ):
        endpoint_val = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.endpoint = endpoint_val.strip().replace(" ", "-") if endpoint_val else ""
        self.api_key = (api_key or os.getenv("AZURE_OPENAI_API_KEY", "")).strip()
        self.api_version = (api_version or os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")).strip()
        self.deployment = (deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT", "interns-gpt-4.1")).strip()
        self._client = None

    def is_configured(self) -> bool:
        return bool(self.endpoint and self.api_key and self.deployment)

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            from openai import AzureOpenAI
        except ImportError as exc:
            raise AzureConfigError(
                "The 'openai' package is not installed. Run: pip install -r requirements.txt"
            ) from exc

        if not self.is_configured():
            raise AzureConfigError(
                "Azure OpenAI is not configured. Set AZURE_OPENAI_ENDPOINT, "
                "AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT (see .env.example), "
                "or enable Demo Mode in the sidebar to try the pipeline without an API key."
            )
        self._client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version,
        )
        return self._client

    def extract(self, image_bytes: bytes, mime_type: str = "image/png") -> DiagramIR:
        """
        Send the image to the configured Azure OpenAI GPT-4.1 deployment and
        parse its response into a validated DiagramIR. Raises AzureConfigError
        if not configured, or IRValidationError if the model's response
        cannot be parsed into a valid IR.
        """
        client = self._get_client()
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{b64}"

        try:
            response = client.chat.completions.create(
                model=self.deployment,
                temperature=0,
                max_tokens=4000,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": USER_PROMPT},
                            {"type": "image_url", "image_url": {"url": data_url}},
                        ],
                    },
                ],
            )
        except Exception as exc:  # surface a clean, actionable error to the UI/CLI
            raise AzureConfigError(f"Azure OpenAI request failed: {exc}") from exc

        raw_text = (response.choices[0].message.content or "").strip()
        if not raw_text:
            raise IRValidationError("The model returned an empty response.")

        return DiagramIR.from_json_text(raw_text)
