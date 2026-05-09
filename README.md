# world-model-demo

A small, beginner-friendly demo for exploring World Foundation Models in an ADAS/DMS context.

The project starts with a practical scaffold:

1. Extract frames from a short driving or cabin video.
2. Organise those frames into a simple dataset folder.
3. Define counterfactual cabin scenario prompts.
4. Generate placeholder variants by copying frames into scenario folders.
5. Compare original and scenario outputs in a Streamlit UI.
6. Create a lightweight JSON evaluation report.

The first version does not require NVIDIA Cosmos or any video generation model. The generation step is intentionally a placeholder so you can connect a real WFM later.

## Project Structure

```text
world-model-demo/
  README.md
  requirements.txt
  .gitignore
  data/
    input/
    frames/
    outputs/
  prompts/
    cabin_scenarios.yaml
  src/
    extract_frames.py
    generate_variants.py
    evaluate_outputs.py
    app.py
```

## Setup

From this folder:

```powershell
cd world-model-demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Place a short test video in `data/input/`, for example:

```text
data/input/cabin_sample.mp4
```

## Extract Frames

Save one frame every 10 frames:

```powershell
python src/extract_frames.py data/input/cabin_sample.mp4 --sample-every 10
```

This writes frames to:

```text
data/frames/cabin_sample/
```

Use a smaller sampling value for more frames:

```powershell
python src/extract_frames.py data/input/cabin_sample.mp4 --sample-every 5
```

## Generate Placeholder Variants

Create one output folder per scenario prompt:

```powershell
python src/generate_variants.py data/frames/cabin_sample
```

This writes placeholder variants to:

```text
data/outputs/cabin_sample/
  daylight_baseline/
  night_cabin/
  harsh_sunlight/
  low_light/
  sunglasses_occlusion/
  driver_looking_down/
```

Each variant folder contains copied frames plus a `prompt.txt` file. This keeps the pipeline runnable before real generation is connected.

## Evaluate Outputs

Create a JSON summary:

```powershell
python src/evaluate_outputs.py data/frames/cabin_sample data/outputs/cabin_sample
```

The report is saved to:

```text
data/outputs/cabin_sample/evaluation.json
```

The current evaluator includes placeholder fields for:

- temporal consistency
- identity preservation
- scenario accuracy

## Launch Streamlit

Start the comparison UI:

```powershell
streamlit run src/app.py
```

Use the sidebar to choose a frame folder and frame index. The app shows the original frame beside the generated or placeholder scenario variants, then displays the evaluation JSON summary if it exists.

## Scenario Prompts

Prompts live in:

```text
prompts/cabin_scenarios.yaml
```

The starter scenarios are:

- `daylight_baseline`
- `night_cabin`
- `harsh_sunlight`
- `low_light`
- `sunglasses_occlusion`
- `driver_looking_down`

Edit this YAML file to add new ADAS/DMS counterfactuals, such as rain, glare, face mask occlusion, camera blur, or unusual cabin illumination.

## Future integration with NVIDIA Cosmos / World Foundation Models

`src/generate_variants.py` is the integration point for a real WFM.

The current placeholder flow:

1. Loads extracted input frames.
2. Loads a scenario prompt from YAML.
3. Creates an output folder for the scenario.
4. Copies the original frames into that folder.

A future Cosmos or WFM integration can replace the copy step with a generation call that:

- sends the input frame sequence or source clip to the model
- passes the selected scenario prompt
- preserves driver identity, cabin geometry, and camera viewpoint
- writes generated frames or video clips back to the scenario folder

Keep the output folder convention stable so the Streamlit app and evaluator continue to work as generation quality improves.
