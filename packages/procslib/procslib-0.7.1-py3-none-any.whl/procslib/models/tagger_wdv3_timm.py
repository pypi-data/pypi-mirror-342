from typing import List, Optional

import numpy as np
import pandas as pd
import timm
import torch
from huggingface_hub import hf_hub_download
from PIL import Image
from timm.data import create_transform, resolve_data_config
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from .base_inference import (
    BaseImageInference,
    UniboxImagePathDataset,
    custom_collate,
)

# Repos provided by the original wdv3 code
# MODEL_REPO_MAP = {
#     "vit": "SmilingWolf/wd-vit-tagger-v3",
#     "swinv2": "SmilingWolf/wd-swinv2-tagger-v3",
#     "convnext": "SmilingWolf/wd-convnext-tagger-v3",
# }


def pil_ensure_rgb(image: Image.Image) -> Image.Image:
    """Converts image to RGB or RGBA if needed, then ensures final result is RGB."""
    if image.mode not in ["RGB", "RGBA"]:
        image = image.convert("RGBA") if "transparency" in image.info else image.convert("RGB")
    if image.mode == "RGBA":
        bg = Image.new("RGBA", image.size, (255, 255, 255))
        bg.alpha_composite(image)
        image = bg.convert("RGB")
    return image


def pil_pad_square(image: Image.Image) -> Image.Image:
    """Pads the input PIL image to a white-background square."""
    w, h = image.size
    px = max(w, h)
    bg = Image.new("RGB", (px, px), (255, 255, 255))
    bg.paste(image, ((px - w) // 2, (px - h) // 2))
    return bg


class LabelData:
    """Holds lists of indices for rating, general, and character tags, plus tag names."""

    def __init__(self, names, rating_indices, general_indices, character_indices):
        self.names = names
        self.rating = rating_indices
        self.general = general_indices
        self.character = character_indices


def load_labels_hf(repo_id: str, revision: Optional[str] = None) -> LabelData:
    """Download `selected_tags.csv` from the Hugging Face repo and parse it."""
    try:
        csv_path = hf_hub_download(
            repo_id=repo_id,
            filename="selected_tags.csv",
            revision=revision,
        )
    except Exception as e:
        print(f"Error downloading selected_tags.csv from {repo_id}: {e}")

    df = pd.read_csv(csv_path, usecols=["name", "category"])
    names = df["name"].tolist()
    # In wd-v3, category=9 => rating, 0 => general, 4 => character
    rating_indices = list(np.where(df["category"] == 9)[0])
    general_indices = list(np.where(df["category"] == 0)[0])
    character_indices = list(np.where(df["category"] == 4)[0])
    return LabelData(names, rating_indices, general_indices, character_indices)


def get_tags(probs: torch.Tensor, labels: LabelData, gen_threshold: float, char_threshold: float):
    """Given a vector of probabilities, returns (caption, taglist, rating_dict, character_dict, general_dict)."""
    # Convert to CPU numpy if needed:
    if probs.is_cuda:
        probs = probs.cpu()
    probs_np = probs.numpy()

    # Build (tag_name -> prob)
    tag_probs = list(zip(labels.names, probs_np))

    # Rating tags (first 4 are rating in WDv3)
    rating = {tag_probs[i][0]: tag_probs[i][1] for i in labels.rating}

    # General tags
    general_candidates = [tag_probs[i] for i in labels.general]
    general_dict = {k: v for (k, v) in general_candidates if v > gen_threshold}
    # Sort by descending confidence
    general_dict = dict(sorted(general_dict.items(), key=lambda x: x[1], reverse=True))

    # Character tags
    character_candidates = [tag_probs[i] for i in labels.character]
    character_dict = {k: v for (k, v) in character_candidates if v > char_threshold}
    character_dict = dict(sorted(character_dict.items(), key=lambda x: x[1], reverse=True))

    # potentially add rating to caption if it's not "general"
    _rating_cap = []
    if len(rating) > 0:
        # Get the highest rating tag
        rating_tag = max(rating, key=rating.get)
        # Check if it's not "general"
        if rating_tag != "general":
            _rating_cap.append(rating_tag)

    # Combine the top general + character tags for a single "caption" string
    combined_names = list(character_dict.keys()) + _rating_cap + list(general_dict.keys())

    # Make a caption that is typical for training (escape parentheses, etc.)
    caption = ", ".join(combined_names).replace("_", " ").replace("(", "\\(").replace(")", "\\)")
    return caption, rating, character_dict, general_dict


class WDV3TaggerTimmInference(BaseImageInference):
    """Inference class for the SmilingWolf WDv3 Tagger, using timm from HF Hub.

    Args:
        repo_id: eg. SmilingWolf/wd-eva02-large-tagger-v3
        gen_threshold: Probability threshold for general tags.
        char_threshold: Probability threshold for character tags.
        device: "cuda" or "cpu".
        batch_size: Batch size for inference.
    """

    def __init__(
        self,
        repo_id: str = "SmilingWolf/wd-eva02-large-tagger-v3",
        gen_threshold: float = 0.35,
        char_threshold: float = 0.75,
        device: str = "cuda",
        batch_size: int = 16,
    ):
        super().__init__(device=device, batch_size=batch_size)
        # self.model_name = model_name
        # if model_name not in MODEL_REPO_MAP:
        #     raise ValueError(f"Unknown model_name '{model_name}'. Must be one of {list(MODEL_REPO_MAP.keys())}.")

        self.gen_threshold = gen_threshold
        self.char_threshold = char_threshold
        self.repo_id = repo_id

        self.transform = None
        self.labels = None

        # We don't need a separate checkpoint_path, but we keep interface consistent:
        self._load_model(None)

    def _load_model(self, checkpoint_path: Optional[str]) -> None:
        """Loads the model from Hugging Face Hub and sets up transforms/labels."""
        # Create the timm model
        self.model = timm.create_model(f"hf-hub:{self.repo_id}", pretrained=False)
        # Download & load weights
        state_dict = timm.models.load_state_dict_from_hf(self.repo_id)
        self.model.load_state_dict(state_dict)

        # Resolve data config and create transform
        data_cfg = resolve_data_config(self.model.pretrained_cfg, model=self.model)
        self.transform = create_transform(**data_cfg)

        # Download/parse the label CSV
        self.labels = load_labels_hf(self.repo_id)

        # Move model to device
        self.model.to(self.device)
        self.model.eval()

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Pad to square, ensure RGB, then transform -> (C, H, W) tensor."""
        img = pil_ensure_rgb(pil_image)
        img = pil_pad_square(img)
        # Use timm transform, which returns CHW in [0,1], then standard normalization
        tensor = self.transform(img)
        # WDv3 expects BGR instead of RGB
        tensor = tensor[[2, 1, 0], ...]
        return tensor

    def _postprocess_output(self, logits: torch.Tensor):
        """Apply sigmoid, threshold for rating/general/character tags.
        Return a list of dicts, one per batch element.
        """
        # logits shape: [B, n_tags]
        probs = torch.sigmoid(logits)
        results = []
        for i in range(probs.shape[0]):
            caption, rating, character, general = get_tags(
                probs=probs[i],
                labels=self.labels,
                gen_threshold=self.gen_threshold,
                char_threshold=self.char_threshold,
            )
            results.append(
                {
                    "caption": caption,
                    "rating": {k: float(v) for k, v in rating.items()},
                    "character_tags": {k: float(v) for k, v in character.items()},
                    "general_tags": {k: float(v) for k, v in general.items()},
                },
            )
        return results

    def infer_one(self, pil_image: Image.Image, **kwargs):
        """Infer tags for a single image."""
        self.model.eval()
        with torch.no_grad(), torch.autocast(device_type="cuda" if self.device == "cuda" else "cpu"):
            image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            output = self.model(image)
            return self._postprocess_output(output)[0]  # Return first (only) element

    def infer_batch(self, pil_images: List[Image.Image], **kwargs):
        """Infer tags for a batch of images."""
        self.model.eval()
        with torch.no_grad(), torch.autocast(device_type="cuda" if self.device == "cuda" else "cpu"):
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            output = self.model(images)
            return self._postprocess_output(output)

    def infer_many(self, image_paths: List[str], **kwargs):
        """Infer tags for many images using a DataLoader."""
        dataset = UniboxImagePathDataset(
            image_files=image_paths,
            preprocess_fn=self._preprocess_image,
        )
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=24,  # more loader since it's could be io-bottle-necked for images by url
            pin_memory=True,
            collate_fn=custom_collate,
        )

        self.model.eval()
        results = []

        with torch.no_grad(), torch.autocast(device_type="cuda" if self.device == "cuda" else "cpu"):
            for batch in tqdm(dataloader, desc="Inferring tags"):
                if batch is None:
                    continue

                images, paths = batch
                images = images.to(self.device)
                output = self.model(images)
                batch_results = self._postprocess_output(output)

                for path, res in zip(paths, batch_results):
                    res["path"] = path
                    results.append(res)

        return pd.DataFrame(results)


# Test script
def test_wdv3_tagger():
    """Test the WD-v3 tagger implementation."""
    import glob

    from PIL import Image

    # Initialize model
    model = get_wdv3_tagger_model(
        repo_id="SmilingWolf/wd-eva02-large-tagger-v3",
        gen_threshold=0.35,
        char_threshold=0.75,
        device="cuda",
        batch_size=16,
    )

    # Test directory with some anime images
    test_dir = "path/to/test/images/*.jpg"
    image_paths = glob.glob(test_dir)

    # Test single image inference
    if image_paths:
        print("\nTesting single image inference:")
        test_image = Image.open(image_paths[0]).convert("RGB")
        result = model.infer_one(test_image)
        print(f"Single image results:\nCaption: {result['caption']}\n")
        print("Top general tags:", dict(list(result["general_tags"].items())[:5]))
        print("Rating scores:", result["rating"])

        # Test batch inference
        if len(image_paths) >= 3:
            print("\nTesting batch inference:")
            test_images = [Image.open(p).convert("RGB") for p in image_paths[:3]]
            results = model.infer_batch(test_images)
            print(f"Processed {len(results)} images in batch")

        # Test many inference with DataLoader
        print("\nTesting many inference:")
        df = model.infer_many(image_paths[:10])
        print("\nDataFrame head:")
        print(df[["filename", "caption"]].head())

        # Save results
        df.to_csv("wdv3_test_results.csv", index=False)
        print("\nResults saved to wdv3_test_results.csv")
    else:
        print("No test images found!")


if __name__ == "__main__":
    test_wdv3_tagger()
