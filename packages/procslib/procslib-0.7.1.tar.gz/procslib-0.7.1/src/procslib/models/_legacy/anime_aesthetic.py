# src/procslib/models/anime_aesthetic_cls.py
import os
from copy import deepcopy

import pandas as pd
import pytorch_lightning as pl
import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm.auto import tqdm
from transformers import ConvNextV2ForImageClassification

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class AnimeAestheticCore(pl.LightningModule):
    """The core model architecture for Anime Aesthetic classification.
    This wraps a ConvNext-based classifier.
    """

    DEFAULT_PRETRAIN = "facebook/convnextv2-base-22k-384"

    def __init__(self, cfg="base", pretrain_path="", drop_path_rate=0.0, ema_decay=0):
        super().__init__()
        if not pretrain_path:
            pretrain_path = self.DEFAULT_PRETRAIN
        pretrain_model = ConvNextV2ForImageClassification.from_pretrained(
            pretrain_path,
        )
        # The original code sets to 1 output dim. If it's classification with scores,
        # you might adapt as needed. For now, we keep 1 for regression-like output.
        pretrain_model.classifier = nn.Linear(pretrain_model.classifier.in_features, 1)
        self.net = pretrain_model

        self.ema_decay = ema_decay
        self.ema = None
        if ema_decay > 0:
            self.ema = deepcopy(self.net)
            self.ema.requires_grad_(False)

    def forward(self, x, use_ema=False):
        net = self.ema if (use_ema and self.ema is not None) else self.net
        outputs = net(x)
        return outputs.logits


class AnimeAestheticInference(BaseImageInference):
    """An inference class for Anime Aesthetic classification/regression.
    This class inherits from a BaseImageInference class and defines model-specific details.
    """

    IMG_SIZE = 768

    def __init__(
        self,
        cfg="base",
        pretrain_path="",
        drop_path_rate=0.0,
        ema_decay=0.0,
        checkpoint_path=None,
        device="cuda",
        batch_size=32,
        use_ema=True,
        column_name: str = "score",
    ):
        super().__init__(device=device, batch_size=batch_size)
        self.cfg = cfg
        self.pretrain_path = pretrain_path
        self.drop_path_rate = drop_path_rate
        self.ema_decay = ema_decay
        self.use_ema = use_ema
        self._load_model(checkpoint_path)
        self.model.eval()

        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Resize((self.IMG_SIZE, self.IMG_SIZE), antialias=True),
                transforms.CenterCrop(self.IMG_SIZE),
            ],
        )
        if column_name == "score":
            print("WARNING: Using default column name 'score'. If you need a different column name, please specify it.")

        self.column_name = column_name

    def _load_model(self, checkpoint_path: str):
        self.model = AnimeAestheticCore(
            cfg=self.cfg,
            pretrain_path=self.pretrain_path,
            drop_path_rate=self.drop_path_rate,
            ema_decay=self.ema_decay,
        )
        if checkpoint_path:
            checkpoint = torch.load(checkpoint_path, map_location=self.device)
            state_dict = checkpoint["state_dict"]

            # Adjust keys
            new_state_dict = {
                key.replace("model.net.", "net.") if key.startswith("model.net.") else key: value
                for key, value in state_dict.items()
            }

            missing, unexpected = self.model.load_state_dict(new_state_dict, strict=False)
            if missing:
                print("Missing keys:", missing)
            if unexpected:
                print("Unexpected keys:", unexpected)

            if self.use_ema and self.model.ema is not None:
                self.model.net = self.model.ema  # Use EMA weights
            print(f"Loaded model from {checkpoint_path}")
        else:
            raise ValueError("Checkpoint path is required for inference")
        self.model.to(self.device)

    def _preprocess_image(self, pil_image: Image.Image):
        return self.transform(pil_image.convert("RGB"))

    def _postprocess_output(self, logits: torch.Tensor):
        # For this model, logits are a single value (like a score).
        # Just return as a scalar or a list of scalars.
        if logits.ndim == 2:
            # shape: [batch_size, 1]
            return logits.squeeze(1).cpu().tolist()
        return logits.cpu().tolist()

    def infer_one(self, pil_image: Image.Image):
        self.model.eval()
        with torch.no_grad():
            image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            logits = self.model(image)
            scores = self._postprocess_output(logits)
            return scores[0] if len(scores) == 1 else scores

    def infer_batch(self, pil_images: list[Image.Image]):
        self.model.eval()
        with torch.no_grad():
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            logits = self.model(images)
            scores = self._postprocess_output(logits)
        return scores

    def infer_many(self, image_paths: list[str]):
        """Infer for many images using a DataLoader."""
        dataset = ImagePathDataset(image_paths, preprocess_fn=self._preprocess_image)
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
                logits = self.model(images)
                scores = self._postprocess_output(logits)
                for path, score in zip(paths, scores):
                    results.append({"path": path, self.column_name: score})

        return pd.DataFrame(results)

    # For this particular model, we do not implement extract_features or predict_proba right now.
    # If needed, you can implement them similarly.


# Sample usage
def demo():
    cfg = "base"
    model_path = "/rmd/yada/checkpoints/aesthetics_weakm-v2_volcanic-salad-49/epoch=4,mae=0.0824,step=0.ckpt"
    folder_path = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"

    inference = AnimeAestheticInference(
        cfg=cfg,
        checkpoint_path=model_path,
        device="cuda",
        batch_size=32,
    )
    results_df = inference.infer_many([os.path.join(folder_path, f) for f in os.listdir(folder_path)])
    results_df.to_csv("aa_results.csv", index=False)
    print("Inference done, saved results to aa_results.csv")


if __name__ == "__main__":
    demo()
