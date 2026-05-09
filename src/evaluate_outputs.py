"""Create a lightweight JSON report for generated scenario folders."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def count_images(folder: Path) -> int:
    """Count image files directly inside a folder."""
    if not folder.exists():
        return 0
    return sum(1 for path in folder.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)


def evaluate_outputs(frame_dir: Path, output_dir: Path, report_path: Path) -> dict[str, Any]:
    """Build and save a simple report for one input frame set."""
    if not frame_dir.exists():
        raise FileNotFoundError(f"Frame directory not found: {frame_dir}")
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    variants: dict[str, Any] = {}
    for scenario_dir in sorted(path for path in output_dir.iterdir() if path.is_dir()):
        variants[scenario_dir.name] = {
            "file_count": count_images(scenario_dir),
            "temporal_consistency": None,
            "identity_preservation": None,
            "scenario_accuracy": None,
            "notes": "Placeholder report fields for future evaluator integration.",
        }

    report = {
        "input_frame_folder": str(frame_dir),
        "output_folder": str(output_dir),
        "input_frame_count": count_images(frame_dir),
        "output_variant_names": list(variants.keys()),
        "variants": variants,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate placeholder scenario outputs.")
    parser.add_argument("frame_dir", type=Path, help="Folder of extracted input frames.")
    parser.add_argument("output_dir", type=Path, help="Folder containing scenario variants.")
    parser.add_argument(
        "--report-path",
        type=Path,
        default=None,
        help="Path for the JSON report. Defaults to output_dir/evaluation.json.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    report_path = args.report_path or (args.output_dir / "evaluation.json")
    report = evaluate_outputs(args.frame_dir, args.output_dir, report_path)
    print(json.dumps(report, indent=2))
    print(f"Saved report to {report_path}")


if __name__ == "__main__":
    main()
