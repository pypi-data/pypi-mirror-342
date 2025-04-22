# Smart Floorplan Predictor

A Python package for classifying images as EPCs, floorplans, property photos, or exterior shots using a pre-trained ONNX model.

## Prerequisites

- Python 3.7 or higher

## Installation

```bash
pip install smart-floorplan-predictor
```

## Usage

```python
import os
from smart_floorplan_predictor import FloorplanPredictor, FloorplanPredictorError

# --- Configuration for Private Repositories --- 
# If the model is hosted in a private GitHub repository, 
# you MUST provide a GitHub Personal Access Token (PAT).
# Set it as an environment variable:
# export GITHUB_TOKEN="your_github_pat_here"
# Ensure the token has the 'repo' scope to access private repository content.

github_token = os.environ.get("GITHUB_TOKEN")

try:
    # Initialize the predictor
    # If using a private repo, the token will be read from the environment variable
    # or you can pass it directly: FloorplanPredictor(github_token="your_token")
    predictor = FloorplanPredictor(github_token=github_token)

    # Make a prediction using the path to an image file
    image_path = "path/to/your/image.jpg" 
    predicted_class, confidence = predictor.predict_with_confidence(image_path)

    print(f"Predicted Class: {predicted_class}")
    print(f"Confidence: {confidence:.2%}")

    # Or just get the class name directly
    # predicted_class_only = predictor.predict(image_path)
    # print(f"Predicted Class (direct): {predicted_class_only}")

except FloorplanPredictorError as e:
    print(f"An error occurred: {e}")
    # Handle specific errors, e.g., ModelDownloadError

```

## Model Downloading

- The package automatically attempts to download the `model.onnx` file using the GitHub API if it's not found locally within the package directory (`src/smart_floorplan_predictor/`). This works even for files stored using Git LFS.
- **Private Repositories:** Downloading from private GitHub repositories requires a `GITHUB_TOKEN` environment variable containing a valid Personal Access Token with the `repo` scope.

## Common Errors & Troubleshooting

*   **`ModelDownloadError: ... 404 Not Found ...`**: 
    *   Check if the `GITHUB_TOKEN` environment variable is set correctly (if accessing a private repo).
    *   Verify the token is valid, not expired, and has the **`repo` scope** enabled in your GitHub Developer settings.
    *   Confirm the repository owner, name, and model file path (`REPO_OWNER`, `REPO_NAME`, `MODEL_FILE_PATH` constants in `predictor.py`) are correct.
*   **`ModelDownloadError: ... 403 Forbidden ...`**: 
    *   Usually indicates the provided `GITHUB_TOKEN` lacks the necessary permissions (`repo` scope) for a private repository.
*   **`FloorplanPredictorError: GITHUB_TOKEN is required...`**: 
    *   You are trying to download from the default private repository location without providing a token. Set the `GITHUB_TOKEN` environment variable.
*   **`FileNotFoundError` or `ImageLoadError`**: 
    *   Ensure the image path passed to `predict` or `predict_with_confidence` is correct and the file exists.
*   **ONNX Runtime Issues**: 
    *   Ensure `onnxruntime` is installed correctly for your OS and architecture.

## Running Tests (Development)

1.  Clone the repository.
2.  Install development dependencies: `pip install -r requirements.txt` (if available) or `pip install pytest requests tqdm Pillow numpy onnxruntime`.
3.  Set the `GITHUB_TOKEN` environment variable if testing against the private repo.
4.  Place test images (like `test_image.png`) in the root directory.
5.  Run the test script: `python test.py`

## Requirements

- Python >= 3.7
- requests
- numpy
- Pillow
- onnxruntime
- tqdm

## License

MIT License

## Author

Oliver Brown