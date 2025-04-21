import os
from pathlib import Path
from typing import List

import pandas as pd
import timm
import torch
import torchvision.transforms as T
from huggingface_hub import hf_hub_download
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class LaionWatermarkInference(BaseImageInference):
    HF_REPO_ID = "kiriyamaX/laion-watermark"
    HF_FILENAME = "watermark_model_v1.pt"

    def __init__(self, device: str = "cuda", batch_size: int = 32):
        """Initialize WatermarkInference.

        Args:
            device (str): Device for inference (default: "cuda").
            batch_size (int): Batch size for inference.
        """
        super().__init__(device=device, batch_size=batch_size)
        self.transforms = T.Compose(
            [
                T.Resize((256, 256)),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ],
        )
        self._load_model()

    def _download_model(self) -> Path:
        """Download model weights from Hugging Face Hub."""
        print(f"Downloading model from Hugging Face Hub ({self.HF_REPO_ID}/{self.HF_FILENAME})")
        return Path(hf_hub_download(repo_id=self.HF_REPO_ID, filename=self.HF_FILENAME))

    def _load_model(self):
        """Load the model and weights."""
        model_path = self._download_model()
        self.model = timm.create_model("efficientnet_b3a", pretrained=False, num_classes=2)
        self.model.classifier = nn.Sequential(
            nn.Linear(in_features=1536, out_features=625),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(in_features=625, out_features=256),
            nn.ReLU(),
            nn.Linear(in_features=256, out_features=2),
        )
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Preprocess a single image.

        Args:
            pil_image (Image.Image): Input PIL image.

        Returns:
            torch.Tensor: Preprocessed image tensor.
        """
        return self.transforms(pil_image)

    def _postprocess_output(self, logits: torch.Tensor):
        """Postprocess model logits into probabilities.

        Args:
            logits (torch.Tensor): Raw model outputs.

        Returns:
            dict: Dictionary containing watermark and clear probabilities.
        """
        probs = torch.nn.functional.softmax(logits, dim=1)
        return {
            "laion_watermark_prob": probs[:, 0].item(),
            # "clear_prob": probs[:, 1].item(),
        }

    def infer_many(self, image_paths: List[str]) -> pd.DataFrame:
        """Infer watermark probabilities for multiple images.

        Args:
            image_paths (List[str]): List of image file paths.

        Returns:
            pd.DataFrame: DataFrame containing filenames and predictions.
        """
        dataset = ImagePathDataset(image_files=image_paths, preprocess_fn=self._preprocess_image)
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=8,
            pin_memory=True,
            collate_fn=custom_collate,
        )

        results = []
        with torch.no_grad():
            for images, paths in tqdm(dataloader, desc="Inferring Watermarks"):
                images = images.to(self.device)
                logits = self.model(images)
                for path, logit in zip(paths, logits):
                    result = self._postprocess_output(logit.unsqueeze(0))
                    results.append({"path": path, **result})

        return pd.DataFrame(results)


# Example demo function
def laion_watermark_demo():
    folder_path = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"

    inference = LaionWatermarkInference(device="cuda", batch_size=32)
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".jpg")]

    results_df = inference.infer_many(image_paths)
    results_df.to_csv("watermark_results.csv", index=False)
    print("Inference complete. Results saved to watermark_results.csv.")


if __name__ == "__main__":
    laion_watermark_demo()
