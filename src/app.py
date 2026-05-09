"""Streamlit UI for comparing original frames with scenario variants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st
from PIL import Image


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRAME_ROOT = PROJECT_ROOT / "data" / "frames"
OUTPUT_ROOT = PROJECT_ROOT / "data" / "outputs"


def list_folders(root: Path) -> list[Path]:
    """List child directories in display order."""
    if not root.exists():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def list_images(folder: Path) -> list[Path]:
    """List image files in display order."""
    if not folder.exists():
        return []
    return sorted(path for path in folder.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)


def load_json(path: Path) -> dict[str, Any] | None:
    """Load a JSON file if it exists and is valid."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def image_preview(path: Path) -> Image.Image:
    """Open an image for Streamlit display."""
    return Image.open(path)


def main() -> None:
    st.set_page_config(page_title="World Model Demo", layout="wide")
    st.title("World Model Demo")

    frame_folders = list_folders(FRAME_ROOT)
    if not frame_folders:
        st.info("No extracted frame folders found. Run extract_frames.py first.")
        st.stop()

    folder_names = [folder.name for folder in frame_folders]
    selected_name = st.sidebar.selectbox("Frame folder", folder_names)
    selected_frame_dir = FRAME_ROOT / selected_name
    selected_output_dir = OUTPUT_ROOT / selected_name

    original_frames = list_images(selected_frame_dir)
    if not original_frames:
        st.warning(f"No frames found in {selected_frame_dir}")
        st.stop()

    max_index = len(original_frames) - 1
    frame_index = st.sidebar.slider("Frame index", 0, max_index, 0)
    selected_frame = original_frames[frame_index]

    st.subheader("Original vs scenario variants")
    variant_dirs = list_folders(selected_output_dir)

    columns = st.columns(1 + max(len(variant_dirs), 1))
    with columns[0]:
        st.caption("original")
        st.image(image_preview(selected_frame), use_container_width=True)

    if variant_dirs:
        for column, variant_dir in zip(columns[1:], variant_dirs):
            variant_frames = list_images(variant_dir)
            matching_frame = variant_dir / selected_frame.name
            preview_path = matching_frame if matching_frame.exists() else None

            if preview_path is None and frame_index < len(variant_frames):
                preview_path = variant_frames[frame_index]

            with column:
                st.caption(variant_dir.name)
                if preview_path:
                    st.image(image_preview(preview_path), use_container_width=True)
                else:
                    st.info("No preview frame")
    else:
        with columns[1]:
            st.info("No variant folders found. Run generate_variants.py first.")

    st.subheader("Evaluation summary")
    report = load_json(selected_output_dir / "evaluation.json")
    if report:
        st.json(report)
    else:
        st.info("No evaluation.json found. Run evaluate_outputs.py after generation.")


if __name__ == "__main__":
    main()
