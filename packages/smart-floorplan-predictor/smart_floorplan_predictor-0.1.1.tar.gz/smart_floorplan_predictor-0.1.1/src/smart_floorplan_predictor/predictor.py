import os
import hashlib
import requests
import base64
import json
from pathlib import Path
import numpy as np
import onnxruntime as ort
from PIL import Image
from typing import Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FloorplanPredictorError(Exception):
    """Base exception class for FloorplanPredictor"""
    pass

class ModelDownloadError(FloorplanPredictorError):
    """Raised when there are issues downloading the model"""
    pass

class ModelVerificationError(FloorplanPredictorError):
    """Raised when model hash verification fails"""
    pass

class ImageLoadError(FloorplanPredictorError):
    """Raised when there are issues loading or processing the image"""
    pass

class InferenceError(FloorplanPredictorError):
    """Raised when there are issues during model inference"""
    pass

class FloorplanPredictor:
    MODEL_URL = "https://api.github.com/repos/Resipedia/domusview_epc_floorplan_image_detection/contents/model.onnx"
    MODEL_HASH = "c5df041fdb3e8e86db4c5492cad65f916d5a8d93e9bead87b59669b7b18bd62f"
    CLASS_NAMES = ["epc", "floorplans", "property_image", "property_outer"]
    
    def __init__(self, model_path: Optional[str] = None, github_token: Optional[str] = None, verify_hash: bool = False):
        """
        Initialize the FloorplanPredictor.
        
        Args:
            model_path (str, optional): Path to the ONNX model file.
                                      If not provided, will use default location.
            github_token (str, optional): GitHub personal access token for downloading the model.
                                        Can also be set via GITHUB_TOKEN environment variable.
            verify_hash (bool, optional): Whether to verify the model hash. 
                                        Defaults to False for development.
        
        Raises:
            ModelDownloadError: If the model cannot be downloaded
            ModelVerificationError: If the downloaded model fails verification
            FloorplanPredictorError: For other initialization errors
        """
        try:
            self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
            self.verify_hash = verify_hash
            
            if model_path is None:
                model_path = self._get_default_model_path()
                logger.info(f"Using default model path: {model_path}")
                
            # Always redownload if we don't have a valid model
            if not os.path.exists(model_path) or not self._is_valid_model(model_path):
                logger.info("Model not found or invalid, downloading...")
                self._download_model(model_path)
            else:
                logger.info("Found existing valid model file")
                
            logger.info("Initializing ONNX session...")
            self.session = ort.InferenceSession(model_path)
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            logger.info("FloorplanPredictor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {str(e)}")
            raise FloorplanPredictorError(f"Failed to initialize predictor: {str(e)}")

    def _is_valid_model(self, model_path: str) -> bool:
        """Check if the model file is a valid ONNX model."""
        try:
            ort.InferenceSession(model_path)
            return True
        except Exception:
            return False

    def _get_default_model_path(self) -> str:
        """
        Get the default path for the model file.
        
        Returns:
            str: Path to the model file
        
        Raises:
            FloorplanPredictorError: If unable to create model directory
        """
        try:
            home = str(Path.home())
            model_dir = os.path.join(home, ".domusview_epc_floorplan_image_detection")
            os.makedirs(model_dir, exist_ok=True)
            return os.path.join(model_dir, "model.onnx")
        except Exception as e:
            raise FloorplanPredictorError(f"Failed to setup model directory: {str(e)}")

    def _download_model(self, model_path: str) -> None:
        """Download the model from the private GitHub repository."""
        try:
            logger.info("Downloading model...")
            if not self.github_token:
                raise ModelDownloadError("GitHub token is required for downloading from private repository")
            
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': f'token {self.github_token}'
            }
            
            # First request to get the file metadata and download URL
            response = requests.get(self.MODEL_URL, headers=headers)
            response.raise_for_status()
            
            file_data = response.json()
            if 'download_url' not in file_data:
                raise ModelDownloadError("No download URL found in GitHub API response")
            
            # Download the actual file using the download_url
            download_response = requests.get(
                file_data['download_url'],
                headers={'Authorization': f'token {self.github_token}'},
                stream=True
            )
            download_response.raise_for_status()
            
            # Write the model file
            with open(model_path, 'wb') as f:
                for chunk in download_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            if self.verify_hash and not self._verify_model_hash(model_path):
                os.remove(model_path)
                raise ModelVerificationError("Downloaded model hash verification failed")
            
            # Verify the model is valid ONNX
            if not self._is_valid_model(model_path):
                os.remove(model_path)
                raise ModelDownloadError("Downloaded file is not a valid ONNX model")
                
        except requests.exceptions.RequestException as e:
            if os.path.exists(model_path):
                os.remove(model_path)
            logger.error(f"Failed to download model: {str(e)}")
            raise ModelDownloadError(f"Failed to download model: {str(e)}")
        except Exception as e:
            if os.path.exists(model_path):
                os.remove(model_path)
            logger.error(f"Unexpected error during model download: {str(e)}")
            raise ModelDownloadError(f"Unexpected error during model download: {str(e)}")

    def _verify_model_hash(self, model_path: str) -> bool:
        """
        Verify the hash of the downloaded model.
        
        Args:
            model_path (str): Path to the model file.
            
        Returns:
            bool: True if hash verification succeeds
            
        Raises:
            ModelVerificationError: If unable to read model file
        """
        try:
            sha256_hash = hashlib.sha256()
            with open(model_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest() == self.MODEL_HASH
        except Exception as e:
            logger.error(f"Failed to verify model hash: {str(e)}")
            raise ModelVerificationError(f"Failed to verify model hash: {str(e)}")

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
            
            # Convert to numpy array and normalize, explicitly as float32
            img_array = np.array(image, dtype=np.float32)
            
            # Normalize to [0, 1] and then apply standard normalization
            img_array = img_array / 255.0
            mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
            std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
            img_array = (img_array - mean) / std
            
            # Transpose from HWC to CHW format
            img_array = img_array.transpose(2, 0, 1)
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array.astype(np.float32)  # Ensure final output is float32
        except Exception as e:
            logger.error(f"Failed to preprocess image: {str(e)}")
            raise ImageLoadError(f"Failed to preprocess image: {str(e)}")

    def predict_with_confidence(self, image_path: str, confidence_threshold: float = 0.9) -> Tuple[str, float]:
        """
        Predicts the class of an image and returns the confidence.

        Args:
            image_path (str): Path to the image file
            confidence_threshold (float): Minimum confidence for a valid prediction

        Returns:
            tuple: (predicted_class_name, confidence) or ("none of the above", confidence)
            
        Raises:
            ImageLoadError: If image cannot be loaded or processed
            InferenceError: If model inference fails
            FloorplanPredictorError: For other unexpected errors
        """
        if not isinstance(image_path, str):
            logger.error("Image path must be a string")
            raise ValueError("Image path must be a string")
        
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            raise ImageLoadError(f"Image file not found: {image_path}")
            
        if not 0 <= confidence_threshold <= 1:
            logger.error("Confidence threshold must be between 0 and 1")
            raise ValueError("Confidence threshold must be between 0 and 1")

        try:
            logger.info(f"Loading image from {image_path}")
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            logger.error(f"Failed to open image {image_path}: {str(e)}")
            raise ImageLoadError(f"Failed to open image {image_path}: {str(e)}")

        try:
            logger.info("Preprocessing image...")
            input_tensor = self.preprocess(image)
            
            logger.info("Running inference...")
            try:
                outputs = self.session.run([self.output_name], {self.input_name: input_tensor})
                output = outputs[0]
            except Exception as e:
                logger.error(f"Model inference failed: {str(e)}")
                raise InferenceError(f"Model inference failed: {str(e)}")

            logger.info("Processing model output...")
            try:
                exp_output = np.exp(output - np.max(output, axis=1, keepdims=True))
                probabilities = exp_output / np.sum(exp_output, axis=1, keepdims=True)
                
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
                logger.error(f"Failed to process model output: {str(e)}")
                raise InferenceError(f"Failed to process model output: {str(e)}")
                
        except (ImageLoadError, InferenceError) as e:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during prediction: {str(e)}")
            raise FloorplanPredictorError(f"Unexpected error during prediction: {str(e)}")

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