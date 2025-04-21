# src/procslib/models/pixai_tagger.py
import json
from typing import Any, Dict, List

import pandas as pd
import timm
import torch
from huggingface_hub import hf_hub_download
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm.auto import tqdm

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class PixAITaggerInference(BaseImageInference):
    """A model that tags images using PixAI tagger models.
    输入图片, 输出图片标签
    """

    def __init__(
        self,
        device="cuda",
        batch_size=16,
        model_version="tagger_v_2_2_7",
        general_threshold=0.15,
        character_threshold=0.7,
        **kwargs,
    ):
        super().__init__(device=device, batch_size=batch_size)
        self.model_version = model_version
        self.general_threshold = general_threshold
        self.character_threshold = character_threshold

        # Model version configuration
        self.model_version_map = {
            "tagger_v_2_2_7": {
                "repo_id": "incantor/pixai-tagger",
                "ckpt_name": "tagger_v2_2_7.pth",
                "num_classes": 13461,
                "tag_dict_name": "tags_v2_13k.json",
                "base_model": "eva02_large_patch14_448",
            },
        }

        if model_version not in self.model_version_map:
            raise ValueError(f"Model version {model_version} not supported")

        self._load_model(None)  # We don't use the checkpoint_path directly

    def _load_model(self, checkpoint_path=None):
        """Load the tagger model from Hugging Face Hub."""
        config = self.model_version_map[self.model_version]

        # Download model checkpoint
        ckpt_path = hf_hub_download(
            repo_id=config["repo_id"],
            filename=config["ckpt_name"],
        )

        # Create model and load state dict
        self.model = timm.create_model(
            config["base_model"],
            pretrained=False,
            num_classes=config["num_classes"],
        )
        self.model.load_state_dict(torch.load(ckpt_path, map_location="cpu"))
        self.model = self.model.to(self.device)
        self.model.eval()

        # Load tag dictionary
        tag_dict_path = hf_hub_download(
            repo_id=config["repo_id"],
            filename=config["tag_dict_name"],
        )
        with open(tag_dict_path) as file:
            tag_info = json.load(file)

        self.tag_map = tag_info["tag_map"]
        tag_split = tag_info["tag_split"]
        self.gen_tag_count = tag_split["gen_tag_count"]
        self.character_tag_count = tag_split["character_tag_count"]

        # Set up image transforms
        self.transform = transforms.Compose(
            [
                transforms.Resize((448, 448)),  # Ensure image size matches encoder
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
            ],
        )

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Preprocess a single PIL image for the model."""
        return self.transform(pil_image.convert("RGB"))

    def _postprocess_output(self, logits: torch.Tensor) -> List[Dict[str, Any]]:
        """Process model outputs into tag dictionaries."""
        # Apply sigmoid to get probabilities (since this is multi-label classification)
        probs = torch.sigmoid(logits)

        # Apply thresholds for general and character tags
        general_tags = probs[:, : self.gen_tag_count] > self.general_threshold
        char_tags = probs[:, self.gen_tag_count :] > self.character_threshold
        combined_tags = torch.hstack((general_tags, char_tags))

        batch_results = []
        for batch_idx in range(combined_tags.size(0)):
            cur_gen_tags = []
            cur_char_tags = []
            # Collect tags that pass the threshold
            for tag, i in self.tag_map.items():
                if combined_tags[batch_idx, i].item():
                    if i < self.gen_tag_count:
                        cur_gen_tags.append(tag)
                    else:
                        cur_char_tags.append(tag)

            # Create a dictionary with general and character tags
            batch_results.append(
                {
                    "general_tags": cur_gen_tags,
                    "character_tags": cur_char_tags,
                    "general_tag_count": len(cur_gen_tags),
                    "character_tag_count": len(cur_char_tags),
                    "total_tag_count": len(cur_gen_tags) + len(cur_char_tags),
                },
            )

        return batch_results

    def infer_many(self, image_paths: List[str]):
        """Infer tags for many images given their paths."""
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

        with torch.no_grad(), torch.autocast("cuda"):
            for batch in tqdm(dataloader, desc="Inferring tags"):
                if batch is None:
                    continue

                images, paths = batch
                images = images.to(self.device, non_blocking=True)

                # Get model predictions
                logits = self.model(images)
                batch_results = self._postprocess_output(logits)

                # Combine results with file paths
                for path, tags in zip(paths, batch_results):
                    result = {
                        "path": path,  # Keep this line
                        # Remove the line with "filename": os.path.basename(path)
                        "general_tags": tags["general_tags"],
                        "character_tags": tags["character_tags"],
                        "general_tag_count": tags["general_tag_count"],
                        "character_tag_count": tags["character_tag_count"],
                        "total_tag_count": tags["total_tag_count"],
                    }
                    results.append(result)

        return pd.DataFrame(results)


# Demo usage
def demo_pixai_tagger():
    import glob

    folder_to_infer = (
        "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"  # Using same demo path as in example
    )
    image_paths = glob.glob(folder_to_infer + "/*.jpg")[:10]  # Limit to 10 images for demo

    inference = PixAITaggerInference(
        device="cuda",
        batch_size=8,
        model_version="tagger_v_2_2_7",
        general_threshold=0.15,
        character_threshold=0.7,
    )

    # Run inference on multiple images
    df = inference.infer_many(image_paths)

    # Save results to CSV
    df.to_csv("pixai_tags.csv", index=False)
    print("Inference completed. Results saved to 'pixai_tags.csv'.")

    # Also print a sample result
    print("\nSample tags for first image:")
    sample = df.iloc[0]
    print(f"Filename: {sample['filename']}")
    print(f"General tags: {', '.join(sample['general_tags'][:10])}...")  # Show first 10 tags
    print(f"Character tags: {', '.join(sample['character_tags'])}")
    print(f"Total tags: {sample['total_tag_count']}")


if __name__ == "__main__":
    demo_pixai_tagger()
