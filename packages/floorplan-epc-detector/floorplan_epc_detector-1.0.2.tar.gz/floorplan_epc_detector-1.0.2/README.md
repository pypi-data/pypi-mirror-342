# Smart Floorplan Predictor

A Python package for classifying images as EPCs, floorplans, property photos, or exterior shots using a pre-trained ONNX model.

## Prerequisites

- Python 3.7 or higher

## Installation

```bash
pip install floorplan-epc-detector
```

## Features

- Image Classification into 4 categories:
  - EPC (Energy Performance Certificate)
  - Floorplans
  - Property Interior Images
  - Property Exterior Images
- Confidence Scoring
- Automatic model download from private/public repositories
- Progress bar for model downloads
- Configurable confidence thresholds
- Raw probability access for advanced use cases

## Usage

```python
import os
from floorplan_epc_detector import FloorplanPredictor, FloorplanPredictorError

# --- Configuration for Private Repositories --- 
# If the model is hosted in a private GitHub repository, 
# you MUST provide a GitHub Personal Access Token (PAT).
# Set it as an environment variable:
# export GITHUB_TOKEN="your_github_pat_here"
# Ensure the token has the 'repo' scope to access private repository content.

github_token = os.environ.get("GITHUB_TOKEN")

try:
    # Initialize the predictor with options
    predictor = FloorplanPredictor(
        github_token=github_token,  # Optional: For private repos
        model_path="custom/path/model.onnx",  # Optional: Custom model path
        skip_download=False  # Optional: Skip auto-download
    )

    # Basic prediction (returns just the class)
    predicted_class = predictor.predict("path/to/your/image.jpg")
    print(f"Predicted Class: {predicted_class}")

    # Prediction with confidence score
    predicted_class, confidence = predictor.predict_with_confidence(
        "path/to/your/image.jpg",
        confidence_threshold=0.7  # Optional: Default is 0.7
    )
    print(f"Predicted Class: {predicted_class}")
    print(f"Confidence: {confidence:.2%}")

    # Get raw probabilities for all classes
    probabilities = predictor.get_raw_probabilities("path/to/your/image.jpg")
    print("Raw probabilities:", probabilities)

except FloorplanPredictorError as e:
    print(f"An error occurred: {e}")
    # Handle specific errors:
    # - ModelDownloadError
    # - ImageLoadError
    # - InferenceError
```

## Model Downloading

The package supports two ways to use the model:

1. **Automatic Download**: The model will be automatically downloaded from the configured repository on first use
2. **Local Model**: Provide a local path to an existing model file

- The package automatically attempts to download the `model.onnx` file using the GitHub API if it's not found locally
- Progress bar shows download progress for large model files
- Supports Git LFS for efficient model file handling
- **Private Repositories:** Downloading from private GitHub repositories requires a `GITHUB_TOKEN` environment variable or direct token provision

## Error Handling

The package provides specific error types for better error handling:

- `ModelDownloadError`: Issues with model downloading
- `ImageLoadError`: Problems with image loading or preprocessing
- `InferenceError`: Issues during model inference
- `FloorplanPredictorError`: Base class for all package errors

## Common Errors & Troubleshooting

*   **`ModelDownloadError: ... 404 Not Found ...`**: 
    *   Check if the `GITHUB_TOKEN` environment variable is set correctly (if accessing a private repo)
    *   Verify the token is valid, not expired, and has the **`repo` scope** enabled
    *   Confirm the repository and model path settings are correct

*   **`ModelDownloadError: ... 403 Forbidden ...`**: 
    *   Usually indicates the provided `GITHUB_TOKEN` lacks necessary permissions

*   **`FloorplanPredictorError: GITHUB_TOKEN is required...`**: 
    *   Set the `GITHUB_TOKEN` environment variable for private repository access

*   **`FileNotFoundError` or `ImageLoadError`**: 
    *   Ensure the image path is correct and the file exists
    *   Verify the image format is supported (JPEG, PNG, etc.)

*   **ONNX Runtime Issues**: 
    *   Ensure `onnxruntime` is installed correctly for your OS
    *   Check Python version compatibility

## Running Tests (Development)

1.  Clone the repository
2.  Install development dependencies: `pip install -r requirements.txt`
3.  Set the `GITHUB_TOKEN` environment variable if testing with private repo
4.  Place test images in the root directory
5.  Run the test script: `python test.py`

## Requirements

- Python >= 3.7
- onnxruntime >= 1.12.0
- numpy >= 1.19.0
- requests >= 2.25.0
- Pillow >= 10.0.0
- tqdm >= 4.65.0

## License

MIT License

## Author

Oliver Brown
