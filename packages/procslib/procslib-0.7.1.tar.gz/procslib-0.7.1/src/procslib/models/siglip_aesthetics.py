# src/procslib/models/siglip_aesthetic_inference.py
import glob

import pandas as pd
import torch

# Import the function from the external library
from aesthetic_predictor_v2_5 import convert_v2_5_from_siglip
from PIL import Image
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class SiglipAestheticInference(BaseImageInference):
    """A wrapper class that uses the Siglip aesthetics model from aesthetic_predictor_v2_5."""

    def __init__(self, device="cuda", batch_size=32):
        super().__init__(device=device, batch_size=batch_size)
        self._load_model()
        self.model.eval()

    def _load_model(self, checkpoint_path: str = None):
        # The function doesn't use a checkpoint_path, it downloads/prepares the model directly
        model, preprocessor = convert_v2_5_from_siglip(
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        self.model = model.to(torch.bfloat16).to(self.device)
        self.preprocessor = preprocessor

    def _preprocess_image(self, pil_image: Image.Image):
        # The preprocessor returns pixel_values already in tensor form
        inputs = self.preprocessor(images=pil_image, return_tensors="pt")
        pixel_values = inputs.pixel_values
        return pixel_values.squeeze(0)  # shape: (C,H,W)

    def _postprocess_output(self, logits: torch.Tensor):
        # Logits is a single value representing the aesthetics score
        # Convert to float
        return logits.squeeze().float().cpu().item()

    def infer_one(self, pil_image: Image.Image):
        self.model.eval()
        with torch.inference_mode():
            image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device, dtype=torch.bfloat16)
            logits = self.model(image).logits
            score = self._postprocess_output(logits)
        return score

    def infer_batch(self, pil_images: list[Image.Image]):
        self.model.eval()
        scores = []
        with torch.inference_mode():
            batch = torch.stack([self._preprocess_image(img) for img in pil_images]).to(
                self.device,
                dtype=torch.bfloat16,
            )
            logits = self.model(batch).logits  # shape: [B, 1]
            for logit in logits:
                scores.append(logit.squeeze().float().cpu().item())
        return scores

    def infer_many(self, image_paths: list[str]):
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
        with torch.inference_mode():
            for batch in tqdm(dataloader, desc="Inferring paths"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device, dtype=torch.bfloat16)
                logits = self.model(images).logits
                for path, logit in zip(paths, logits):
                    score = logit.squeeze().float().cpu().item()
                    results.append({"path": path, "siglip_aesthetic": score})
        return pd.DataFrame(results)


# Demo usage
def demo_siglip():
    folder_to_infer = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    image_paths = glob.glob(folder_to_infer + "/*.jpg")

    inference = SiglipAestheticInference(device="cuda", batch_size=4)

    # Single image
    img = Image.open(image_paths[0])
    print("Single image score:", inference.infer_one(img))

    # Batch inference
    imgs = [Image.open(p) for p in image_paths]
    print("Batch scores:", inference.infer_batch(imgs))

    # Many images inference
    df = inference.infer_many(image_paths)
    df.to_csv("siglip_scores.csv", index=False)
    print("Inference completed. Results saved to 'siglip_scores.csv'.")


if __name__ == "__main__":
    demo_siglip()
