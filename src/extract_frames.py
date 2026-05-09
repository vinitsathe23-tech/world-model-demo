"""Extract sampled frames from a driving or cabin video."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


def extract_frames(video_path: Path, output_root: Path, sample_every: int = 10) -> Path:
    """Extract every Nth frame from a video into a named output folder."""
    if sample_every < 1:
        raise ValueError("sample_every must be 1 or greater")
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    output_dir = output_root / video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    frame_index = 0
    saved_count = 0

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            if frame_index % sample_every == 0:
                frame_name = f"frame_{saved_count:06d}.jpg"
                frame_path = output_dir / frame_name
                cv2.imwrite(str(frame_path), frame)
                saved_count += 1

            frame_index += 1
    finally:
        capture.release()

    if saved_count == 0:
        raise RuntimeError("No frames were extracted. Check the video and sampling rate.")

    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract sampled frames from a video.")
    parser.add_argument("video_path", type=Path, help="Path to the input video.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data/frames"),
        help="Root directory where frame folders are written.",
    )
    parser.add_argument(
        "--sample-every",
        type=int,
        default=10,
        help="Save one frame every N input frames.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = extract_frames(args.video_path, args.output_root, args.sample_every)
    print(f"Extracted frames to {output_dir}")


if __name__ == "__main__":
    main()
