import os
import hashlib
import requests
import base64
import json
import subprocess
from pathlib import Path
import numpy as np
import onnxruntime as ort
from PIL import Image
from typing import Tuple, Optional
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FloorplanPredictorError(Exception):
    """Base exception class for FloorplanPredictor"""
    pass

class ModelDownloadError(FloorplanPredictorError):
    """Raised when there are issues downloading the model"""
    pass

class ImageLoadError(FloorplanPredictorError):
    """Raised when there are issues loading or processing the image"""
    pass

class InferenceError(FloorplanPredictorError):
    """Raised when there are issues during model inference"""
    pass

class FloorplanPredictor:
    # Repository details for LFS model
    REPO_OWNER = "Resipedia"
    REPO_NAME = "domusview_epc_floorplan_image_detection"
    MODEL_FILE_PATH = "model.onnx"  # Path to model file within the repository
    CLASS_NAMES = ["epc", "floorplans", "property_image", "property_outer"]
    DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.onnx")
    
    def __init__(self, model_path: Optional[str] = None, github_token: Optional[str] = None, skip_download: bool = False):
        """Initialize the FloorplanPredictor.
        
        Args:
            model_path: Path to the model file. If None, will use the default path or download.
            github_token: GitHub token for accessing private repositories. Can also be set as GITHUB_TOKEN env var.
            skip_download: If True, will not attempt to download the model even if it doesn't exist locally.
        """
        try:
            self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
            model_path = model_path or self.DEFAULT_MODEL_PATH
            
            if not os.path.exists(model_path) and not skip_download:
                logger.info(f"Model not found at {model_path}, attempting to download via LFS...")
                if not self.github_token:
                    raise FloorplanPredictorError("GITHUB_TOKEN is required to download the LFS model from a private repository.")
                self._download_lfs_model(model_path)
            elif os.path.exists(model_path):
                logger.info(f"Using existing model at {model_path}")
            else: # skip_download is True and file doesn't exist
                 raise FloorplanPredictorError(f"Model download skipped, but model not found at {model_path}")

            logger.info("Initializing ONNX session...")
            self.session = ort.InferenceSession(model_path)
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            logger.info("FloorplanPredictor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {str(e)}")
            # Avoid wrapping the exception if it's already one of ours
            if isinstance(e, FloorplanPredictorError):
                raise e
            raise FloorplanPredictorError(f"Failed to initialize predictor: {str(e)}")

    def _download_lfs_model(self, model_path: str) -> None:
        """Download the model file using GitHub API for LFS."""
        if not self.github_token:
            raise ModelDownloadError("GitHub token is required for LFS download from private repo.")

        api_url = f"https://api.github.com/repos/{self.REPO_OWNER}/{self.REPO_NAME}/contents/{self.MODEL_FILE_PATH}"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json" # Request JSON metadata first
        }
        
        try:
            # 1. Get LFS metadata from GitHub API
            logger.info(f"Fetching LFS metadata from {api_url}...")
            meta_response = requests.get(api_url, headers=headers)
            logger.debug(f"LFS metadata response status: {meta_response.status_code}")
            
            if meta_response.status_code == 404:
                 error_message = (
                    f"Failed to get LFS metadata (404 Not Found) from {api_url}. "
                    "Possible reasons:\n"
                    "1. The repository or file path is incorrect.\n"
                    "2. The provided GitHub token is invalid, expired, or lacks 'repo' scope."
                )
                 logger.error(error_message)
                 raise ModelDownloadError(error_message)
            elif meta_response.status_code == 403:
                 error_message = f"Failed to get LFS metadata (403 Forbidden) from {api_url}. Check token permissions ('repo' scope required)."
                 logger.error(error_message)
                 raise ModelDownloadError(error_message)
                 
            meta_response.raise_for_status() # Raise for other HTTP errors
            
            metadata = meta_response.json()
            
            if "download_url" not in metadata or not metadata["download_url"]:
                # Check if it's actually an LFS file - pointer file content might be in 'content'
                if metadata.get("type") == "file" and metadata.get("size", 0) < 1000: # Pointer files are small
                     pointer_content = base64.b64decode(metadata.get("content", "")).decode('utf-8')
                     if "oid sha256:" in pointer_content:
                         logger.error(f"Received LFS pointer file content instead of download URL. LFS resolution might require git-lfs or a different API approach.")
                         raise ModelDownloadError("GitHub API did not provide a direct LFS download URL. Manual git lfs pull might be needed.")
                logger.error(f"Could not find 'download_url' in LFS metadata response: {metadata}")
                raise ModelDownloadError("Could not find LFS download URL in API response.")

            download_url = metadata["download_url"]
            logger.info(f"Found LFS download URL: {download_url}")

            # 2. Download the actual file content from the LFS download URL
            # Note: LFS download URLs might not require the auth header, but include it for safety
            logger.info(f"Downloading model from LFS URL...")
            # Use the same headers for the download request
            download_response = requests.get(download_url, headers=headers, stream=True)
            logger.debug(f"LFS download response status: {download_response.status_code}")
            download_response.raise_for_status()

            # Get file size for progress bar
            file_size = int(download_response.headers.get('content-length', 0))
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Download with progress bar
            with open(model_path, 'wb') as f, tqdm(
                desc="Downloading LFS model",
                total=file_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for data in download_response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    pbar.update(size)
            
            logger.info("LFS model downloaded successfully")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed during LFS model download request: {str(e)}")
            raise ModelDownloadError(f"Failed during LFS model download request: {str(e)}")
        except KeyError as e:
             logger.error(f"Missing expected key in API response: {str(e)}")
             raise ModelDownloadError(f"Missing expected key in API response: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during LFS model download: {str(e)}")
            # Clean up potentially incomplete file
            if os.path.exists(model_path):
                try:
                    os.remove(model_path)
                    logger.info(f"Removed incomplete download file: {model_path}")
                except OSError as rm_err:
                    logger.error(f"Failed to remove incomplete download file {model_path}: {rm_err}")
            raise ModelDownloadError(f"Unexpected error during LFS model download: {str(e)}")

    def preprocess(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess the image for the ONNX model.
        
        Args:
            image (PIL.Image): Input image in RGB format
            
        Returns:
            numpy.ndarray: Preprocessed image ready for inference
            
        Raises:
            ImageLoadError: If preprocessing fails
        """
        try:
            # Resize the image to the required input size (assuming 224x224)
            image = image.resize((224, 224), Image.Resampling.BILINEAR)
            
            # Convert to numpy array and normalize
            img_array = np.array(image).astype(np.float32)
            
            # Normalize to [0, 1] and then apply standard normalization
            img_array = img_array / 255.0
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            img_array = (img_array - mean) / std
            
            # Transpose from HWC to CHW format
            img_array = img_array.transpose(2, 0, 1)
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            logger.error(f"Failed to preprocess image: {str(e)}")
            raise ImageLoadError(f"Failed to preprocess image: {str(e)}")

    def get_raw_probabilities(self, image_path: str) -> np.ndarray:
        """Get raw probabilities for all classes before thresholding."""
        if not isinstance(image_path, str):
            logger.error("Image path must be a string")
            raise ValueError("Image path must be a string")
        
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            raise ImageLoadError(f"Image file not found: {image_path}")

        try:
            image = Image.open(image_path).convert('RGB')
            input_tensor = self.preprocess(image)
            outputs = self.session.run([self.output_name], {self.input_name: input_tensor.astype(np.float32)})
            output = outputs[0]
            
            # Apply softmax to get probabilities
            exp_output = np.exp(output - np.max(output, axis=1, keepdims=True))
            probabilities = exp_output / np.sum(exp_output, axis=1, keepdims=True)
            
            return probabilities.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Failed to get raw probabilities: {str(e)}")
            raise

    def predict_with_confidence(self, image_path: str, confidence_threshold: float = 0.7) -> Tuple[str, float]:
        """
        Predicts the class of an image and returns the confidence.

        Args:
            image_path (str): Path to the image file
            confidence_threshold (float): Minimum confidence for a valid prediction

        Returns:
            tuple: (predicted_class_name, confidence) or ("none of the above", confidence)
        """
        try:
            # Get raw probabilities
            probabilities = self.get_raw_probabilities(image_path)
            
            # Log raw probabilities for debugging
            logger.debug("Raw probabilities for each class:")
            for idx, (class_name, prob) in enumerate(zip(self.CLASS_NAMES, probabilities[0])):
                logger.debug(f"{class_name}: {prob:.4f}")
            
            confidence = float(np.max(probabilities))
            predicted_class_idx = int(np.argmax(probabilities))
            
            if predicted_class_idx >= len(self.CLASS_NAMES):
                logger.error("Model output index out of range")
                raise InferenceError("Model output index out of range")
            
            logger.info(f"Prediction complete: class={self.CLASS_NAMES[predicted_class_idx]}, confidence={confidence:.2%}")
            if confidence >= confidence_threshold:
                return self.CLASS_NAMES[predicted_class_idx], confidence
            else:
                return "none of the above", confidence
                
        except Exception as e:
            logger.error(f"Failed during prediction: {str(e)}")
            raise

    def predict(self, input_data: str) -> str:
        """
        Make a prediction using the model.
        
        Args:
            input_data: Path to the image file
            
        Returns:
            str: Predicted class name
            
        Raises:
            ImageLoadError: If image cannot be loaded or processed
            InferenceError: If model inference fails
            FloorplanPredictorError: For other unexpected errors
        """
        try:
            predicted_class, _ = self.predict_with_confidence(input_data)
            return predicted_class
        except Exception as e:
            raise