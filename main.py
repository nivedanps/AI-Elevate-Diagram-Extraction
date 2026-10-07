"""
main.py
-------
Headless CLI for the AI Elevate Diagram Extraction pipeline.

Examples
--------
Run with a real image against Azure OpenAI, save the .drawio file:
    python main.py --image student_answer.png --output extracted.drawio

Also score the extraction against an examiner ground-truth IR file:
    python main.py --image student_answer.png --ground-truth gt.json --output extracted.drawio

Try the whole pipeline with zero Azure credentials (bundled mock data):
    python main.py --demo --output demo.drawio
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys

from azure_client import AzureConfigError, AzureVLMExtractor
from drawio_builder import save_drawio_file
from evaluator import evaluate
from ir_schema import DiagramIR, IRValidationError
from mock_data import get_mock_extraction, get_sample_ground_truth


def _guess_mime(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    return mime or "image/png"


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Elevate Diagram Extraction pipeline (CLI)")
    parser.add_argument("--image", help="Path to the student's hand-drawn diagram image")
    parser.add_argument("--ground-truth", help="Path to an examiner ground-truth IR JSON file")
    parser.add_argument("--output", default="extracted.drawio", help="Output .drawio file path")
    parser.add_argument(
        "--demo", action="store_true", help="Run with bundled mock data instead of calling Azure OpenAI"
    )
    args = parser.parse_args()

    if not args.demo and not args.image:
        parser.error("Provide --image <path>, or pass --demo to run with bundled mock data.")

    if args.demo:
        print("[demo mode] Using bundled mock extraction (no Azure OpenAI call made).")
        ir = get_mock_extraction()
    else:
        extractor = AzureVLMExtractor()
        try:
            with open(args.image, "rb") as f:
                image_bytes = f.read()
        except OSError as exc:
            print(f"ERROR: could not read image '{args.image}': {exc}", file=sys.stderr)
            return 1

        print(f"Calling Azure OpenAI deployment '{extractor.deployment}' ...")
        try:
            ir = extractor.extract(image_bytes, mime_type=_guess_mime(args.image))
        except (AzureConfigError, IRValidationError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    if ir.warnings:
        for w in ir.warnings:
            print(f"WARNING: {w}")

    print("\n--- Extracted Diagram IR ---")
    print(ir.to_json())

    save_drawio_file(ir, args.output)
    print(f"\nSaved draw.io file to: {args.output}")

    if args.ground_truth or args.demo:
        if args.ground_truth:
            try:
                with open(args.ground_truth, "r", encoding="utf-8") as f:
                    gt_dict = json.load(f)
                ground_truth = DiagramIR.from_dict(gt_dict)
            except (OSError, json.JSONDecodeError, IRValidationError) as exc:
                print(f"ERROR: could not load ground truth '{args.ground_truth}': {exc}", file=sys.stderr)
                return 1
        else:
            print("[demo mode] Using bundled sample ground truth for scoring.")
            ground_truth = get_sample_ground_truth()

        result = evaluate(ir, ground_truth)
        print("\n--- Evaluation ---")
        print(json.dumps(result.to_dict(), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
