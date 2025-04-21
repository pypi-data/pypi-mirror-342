# src/procslib/models/base_inference.py

from abc import ABC, abstractmethod
from typing import List

import pandas as pd
import torch
import unibox as ub
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm


class BaseImageInference(ABC):
    """A base class to define a common interface for image inference models.
    All models should extend this class and implement required methods.
    """

    def __init__(self, device: str = "cuda", batch_size: int = 32, **kwargs):
        """Initialize inference class with a device and default batch size."""
        self.device = device
        self.batch_size = batch_size
        self.model = None

    @abstractmethod
    def _load_model(self, checkpoint_path: str):
        """Load the model from a checkpoint.
        Should set self.model as a torch.nn.Module instance on self.device.
        """

    @abstractmethod
    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Preprocess a single PIL image into the format required by the model.
        Return a torch.Tensor of shape (C, H, W).
        """

    @abstractmethod
    def _postprocess_output(self, logits: torch.Tensor):
        """Postprocess the raw logits from the model into desired predictions.
        For classification models, this might mean applying softmax and argmax.
        """

    def infer_one(self, pil_image: Image.Image, **kwargs):
        """Infer for a single image (PIL)."""
        self.model.eval()
        with torch.no_grad():
            image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            output = self.model(image)
            return self._postprocess_output(output.logits)

    def infer_batch(self, pil_images: List[Image.Image], **kwargs):
        """Infer for a batch of images (list of PIL images)."""
        self.model.eval()
        with torch.no_grad():
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            output = self.model(images)
            return self._postprocess_output(output.logits)

    def infer_many(self, image_paths: List[str], **kwargs):
        """Infer for many images given their paths using a DataLoader for efficiency.
        Returns a pandas DataFrame with the results.
        """
        dataset = ImagePathDataset(
            image_files=image_paths,
            preprocess_fn=self._preprocess_image,
        )
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=8,
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
                    results.append({"path": path, "prediction": pred})

        return pd.DataFrame(results)

    def extract_features(self, pil_image: Image.Image):
        """Extract features from a single image at some layer before the classifier.
        This might vary per model and can be implemented as needed.
        By default, raise NotImplementedError if a model doesn't support it.
        """
        raise NotImplementedError("Feature extraction not implemented for this model.")

    def extract_features_batch(self, pil_images: List[Image.Image]):
        """Extract features for a batch of images."""
        raise NotImplementedError("Batch feature extraction not implemented.")

    def predict_proba(self, pil_images: List[Image.Image], **kwargs):
        """Predict class probabilities for a list of images.
        May be applicable only for classification models.
        """
        raise NotImplementedError("Probability prediction not implemented for this model.")


class ImagePathDataset(Dataset):
    """A dataset that loads images from paths and preprocesses them using a given preprocess function."""

    def __init__(self, image_files: List[str], preprocess_fn):
        self.image_files = image_files
        self.preprocess_fn = preprocess_fn

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = self.image_files[idx]
        try:
            image = Image.open(image_path).convert("RGB")
            image = self.preprocess_fn(image)
            return image, image_path
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None


class UniboxImagePathDataset(Dataset):
    """A dataset that loads images from paths and preprocesses them using a given preprocess function."""

    def __init__(self, image_files: List[str], preprocess_fn):
        self.image_files = image_files
        self.preprocess_fn = preprocess_fn

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = self.image_files[idx]
        try:
            # image = Image.open(image_path).convert("RGB")
            image = ub.loads(image_path, debug_print=False)
            image = self.preprocess_fn(image)
            return image, image_path
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None


def custom_collate(batch):
    """Custom collate function to filter out None values."""
    batch = [item for item in batch if item is not None]
    if not batch:
        return None
    return torch.utils.data.dataloader.default_collate(batch)
