"""Create placeholder scenario variants from extracted frames."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

import yaml


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def list_frames(frame_dir: Path) -> list[Path]:
    """Return image frames in stable filename order."""
    if not frame_dir.exists():
        raise FileNotFoundError(f"Frame directory not found: {frame_dir}")

    frames = sorted(
        path for path in frame_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not frames:
        raise RuntimeError(f"No image frames found in {frame_dir}")
    return frames


def load_scenarios(prompt_path: Path) -> dict[str, dict[str, Any]]:
    """Load scenario prompts from YAML."""
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with prompt_path.open("r", encoding="utf-8") as stream:
        scenarios = yaml.safe_load(stream) or {}

    if not isinstance(scenarios, dict) or not scenarios:
        raise RuntimeError(f"No scenarios found in {prompt_path}")
    return scenarios


def generate_placeholder_variants(
    frame_dir: Path,
    prompt_path: Path,
    output_root: Path,
    max_frames: int | None = None,
) -> Path:
    """Copy sampled input frames into one output folder per scenario."""
    frames = list_frames(frame_dir)
    scenarios = load_scenarios(prompt_path)

    selected_frames = frames[:max_frames] if max_frames else frames
    output_dir = output_root / frame_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)

    for scenario_name, scenario in scenarios.items():
        scenario_dir = output_dir / scenario_name
        scenario_dir.mkdir(parents=True, exist_ok=True)

        prompt_text = str(scenario.get("prompt", ""))
        (scenario_dir / "prompt.txt").write_text(prompt_text, encoding="utf-8")

        for frame_path in selected_frames:
            destination = scenario_dir / frame_path.name
            shutil.copy2(frame_path, destination)

        # TODO: Replace this copy-only placeholder with a real WFM call.
        # A future integration could pass `selected_frames` and `prompt_text` to
        # NVIDIA Cosmos or another video/image generation service, then write
        # generated frames into `scenario_dir`.

    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create placeholder counterfactual scenario variants."
    )
    parser.add_argument("frame_dir", type=Path, help="Folder of extracted input frames.")
    parser.add_argument(
        "--prompts",
        type=Path,
        default=Path("prompts/cabin_scenarios.yaml"),
        help="YAML file containing scenario prompts.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data/outputs"),
        help="Root directory where variant folders are written.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Optional maximum number of frames to copy per scenario.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = generate_placeholder_variants(
        frame_dir=args.frame_dir,
        prompt_path=args.prompts,
        output_root=args.output_root,
        max_frames=args.max_frames,
    )
    print(f"Generated placeholder variants in {output_dir}")


if __name__ == "__main__":
    main()
