"""inferencing Huggingface Automodel classes, that's been trained with trainlib:

https://github.com/arot-devs/trainlib
"""
# src/procslib/models/custom_classifier.py

import os
from typing import Dict, List, Literal, Union

import pandas as pd
import torch
import torch.nn.functional as F
from PIL import Image
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import AutoImageProcessor, AutoModelForImageClassification

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class HfAutomodelInference(BaseImageInference):
    """Inference class for custom-trained image models (classification, regression, ordinal) from Hugging Face transformers."""

    def __init__(
        self,
        model_path: str,
        task: Literal["classification", "regression", "ordinal"] = "classification",
        device: str = "cuda",
        batch_size: int = 32,
    ):
        """Initialize the inference class with a trained model.

        Args:
            model_path (str): Either a Hugging Face model ID or a local folder path.
            task (str): Task type ('classification', 'regression', 'ordinal').
            device (str): Device to run inference on ('cuda' or 'cpu').
            batch_size (int): Batch size for inference.
        """
        self.device = device
        self.batch_size = batch_size
        self.model_path = model_path
        self.task = task.lower()
        if self.task not in ["classification", "regression", "ordinal"]:
            raise ValueError("Task must be 'classification', 'regression', or 'ordinal'.")
        self.image_processor = None
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the model and image processor from either a Hugging Face ID or a local folder."""
        # Check if model_path is a local directory
        is_local = os.path.isdir(self.model_path) and os.path.isfile(os.path.join(self.model_path, "pytorch_model.bin"))

        # Load the image processor
        self.image_processor = AutoImageProcessor.from_pretrained(
            self.model_path,
            # use_fast=True,    # <-- this errors
            local_files_only=is_local,
        )

        # Load the model (assumes it’s compatible with AutoModelForImageClassification)
        # Note: Regression/ordinal models typically use the same base class with a custom head
        self.model = AutoModelForImageClassification.from_pretrained(
            self.model_path,
            local_files_only=is_local,
        ).to(self.device)
        self.model.eval()

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Preprocess a single PIL image into the format required by the model."""
        inputs = self.image_processor(images=pil_image, return_tensors="pt")
        return inputs["pixel_values"].squeeze(0)  # Shape: [C, H, W]

    def _postprocess_output(self, logits: torch.Tensor):
        """Convert raw logits into human-readable outputs."""
        if self.task == "classification":
            probabilities = F.softmax(logits, dim=-1)
            predicted_class_idx = torch.argmax(logits, dim=-1)
            confidence_scores = probabilities.max(dim=-1).values
            id2label = self.model.config.id2label

            results = []
            for idx, conf in zip(predicted_class_idx, confidence_scores):
                idx_key = str(idx.item()) if str(idx.item()) in id2label else idx.item()
                label = id2label[idx_key]
                results.append({"label": label, "confidence": float(conf)})

            return results

        if self.task == "regression":
            preds = logits.squeeze(-1)  # Shape: [B] or scalar
            return float(preds.item()) if preds.dim() == 0 else preds.tolist()

        if self.task == "ordinal":
            preds = torch.round(logits).squeeze(-1)  # Shape: [B]
            return int(preds.item()) if preds.dim() == 0 else preds.tolist()

    def infer_one(self, pil_image: Image.Image) -> Dict[str, Union[str, float]]:
        """Infer for a single image."""
        self.model.eval()
        with torch.no_grad():
            image_tensor = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            output = self.model(image_tensor)
            # _postprocess_output now always returns a list for classification
            # so indexing [0] is valid:
            result = self._postprocess_output(output.logits)[0]
        return result

    def infer_batch(self, pil_images: List[Image.Image]) -> List[Dict[str, Union[str, float]]]:
        """Infer for a batch of images."""
        self.model.eval()
        with torch.no_grad():
            image_tensors = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            output = self.model(image_tensors)
            results = self._postprocess_output(output.logits)
        return results

    def infer_many(self, image_paths: List[str]) -> pd.DataFrame:
        """Infer for many images given their paths."""
        dataset = ImagePathDataset(
            image_files=image_paths,
            preprocess_fn=self._preprocess_image,
        )

        # get platform: if windows, set num_workers=0
        num_workers = 4 if os.name != "nt" else 0

        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=num_workers,
            pin_memory=True,
            collate_fn=custom_collate,
        )

        self.model.eval()
        results = []
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Inferring paths"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device)
                output = self.model(images)
                preds = self._postprocess_output(output.logits)

                for path, pred in zip(paths, preds):
                    if self.task == "classification":
                        # pred is a dict with 'label' and 'confidence'
                        results.append(
                            {
                                "path": path,
                                "label": pred["label"],
                                "confidence": pred["confidence"],
                            },
                        )
                    else:  # regression or ordinal
                        # pred is a float (or int for ordinal)
                        results.append(
                            {
                                "path": path,
                                "value": pred,
                            },
                        )

        return pd.DataFrame(results)

    def predict_proba(self, pil_images: List[Image.Image]) -> List[Dict[str, float]]:
        """Predict class probabilities for a list of images (classification only)."""
        if self.task != "classification":
            raise NotImplementedError("predict_proba is only implemented for classification tasks.")

        self.model.eval()
        with torch.no_grad():
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            output = self.model(images)
            probs = torch.softmax(output.logits, dim=-1).cpu().numpy()
            id2label = self.model.config.id2label

            results = []
            for prob in probs:
                prob_dict = {id2label[str(i)]: float(p) for i, p in enumerate(prob)}
                results.append(prob_dict)
            return results
