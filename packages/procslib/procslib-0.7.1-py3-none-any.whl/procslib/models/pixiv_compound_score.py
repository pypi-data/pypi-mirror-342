r"""basically the same as anime aesthetics, but uses convnext tiny;

used for the first version of pixiv aesthetics predict by larry

code adapted from https://github.com/troph-team/data-process-codebase-v4/blob/main/src/sagemaker_codebase/anime_aesthetic_runner/anime_aesthetic.py

Related docs:

- [(pixiv) Compound score quick test](https://mewtant-inc.larksuite.com/docx/MoSad8MgIoqI2pxEUFLu9DHeszc?from=from_copylink)

- [\[image model 2.0\] Pixiv Compound score test](https://mewtant-inc.larksuite.com/wiki/T9hbwOkcUiHu03k7VdNuGNQhsfb?from=from_copylink)

"""

from copy import deepcopy

import pandas as pd
import pytorch_lightning as pl
import torch
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm.auto import tqdm

from ._convnext_v2 import convnextv2  # Assuming _convnext_v2 is in the same module

# Imports from your existing codebase
from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class PixivCompoundScoreCore(pl.LightningModule):
    """Core model for compound score prediction, adapted from the code you provided.
    This uses convnextv2 as backbone, outputs a single scalar score.
    """

    def __init__(self, cfg="tiny", drop_path_rate=0.0, ema_decay=0):
        super().__init__()
        # Just like InferenceAnimeAesthetic, we build a convnextv2 with num_classes=1
        self.net = convnextv2(cfg, in_chans=3, num_classes=1, drop_path_rate=drop_path_rate)
        self.ema_decay = ema_decay
        self.ema = None
        if ema_decay > 0:
            self.ema = deepcopy(self.net)
            self.ema.requires_grad_(False)

    def forward(self, x, use_ema=False):
        # Apply the same normalization as done in the provided compound score code
        x = (x - 0.5) / 0.5
        net = self.ema if (use_ema and self.ema is not None) else self.net
        return net(x)


class PixivCompoundScoreInference(BaseImageInference):
    """Inference class for the compound score model.
    This follows the same structure as AnimeAestheticInference.
    """

    IMG_SIZE = 768

    def __init__(
        self,
        cfg="tiny",
        drop_path_rate=0.0,
        ema=False,
        model_path=None,
        device="cuda",
        batch_size=32,
        column_name: str = "score",
    ):
        super().__init__(device=device, batch_size=batch_size)
        self.cfg = cfg
        self.drop_path_rate = drop_path_rate
        self.use_ema = ema
        if not model_path:
            raise ValueError("model_path is required for CompoundScoreInference")

        # Initialize model
        self.model = PixivCompoundScoreCore(
            cfg=self.cfg,
            drop_path_rate=self.drop_path_rate,
            ema_decay=(0.9999 if self.use_ema else 0),
        )
        self._load_model(model_path)
        self.model.to(self.device)
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

    def _load_model(self, model_path: str):
        # Load state dict from the given model_path
        checkpoint = torch.load(model_path, map_location=self.device)
        state_dict = checkpoint["state_dict"]

        if self.use_ema and self.model.ema is not None:
            # Load EMA weights
            ema_state_dict = {k[len("ema.") :]: v for k, v in state_dict.items() if k.startswith("ema.")}
            self.model.net.load_state_dict(ema_state_dict, strict=False)
        else:
            # Load normal weights
            filtered_state_dict = {k: v for k, v in state_dict.items() if not k.startswith("ema.")}
            self.model.load_state_dict(filtered_state_dict, strict=False)

        print(f"Compound score model loaded from {model_path}")

    def _preprocess_image(self, pil_image: Image.Image):
        return self.transform(pil_image.convert("RGB"))

    def _postprocess_output(self, logits: torch.Tensor):
        # Logits is a scalar per image
        return logits.squeeze(1).cpu().tolist()

    def infer_one(self, pil_image: Image.Image):
        self.model.eval()
        with torch.no_grad():
            image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            logits = self.model(image, use_ema=self.use_ema)
            scores = self._postprocess_output(logits)
            return scores[0]

    def infer_batch(self, pil_images: list[Image.Image]):
        self.model.eval()
        with torch.no_grad():
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            logits = self.model(images, use_ema=self.use_ema)
            scores = self._postprocess_output(logits)
        return scores

    def infer_many(self, image_paths: list[str]):
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
            for batch in tqdm(dataloader, desc="Inferring compound scores"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device)
                logits = self.model(images, use_ema=self.use_ema)
                scores = self._postprocess_output(logits)
                for path, score in zip(paths, scores):
                    results.append({"path": path, self.column_name: score})

        return pd.DataFrame(results)
