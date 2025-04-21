"""Using MiDaS 3.0 to analyze the "depthness" of images and returns a numerical metric

[Intel/dpt-hybrid-midas · Hugging Face](https://huggingface.co/Intel/dpt-hybrid-midas)

- To improve speed of inference: lower out_size to 512x512, or use more workers (12 is mostly enough)

- To improve accuracy of inference: increase out_size to 1024x1024

"""

# src/procslib/models/depth_wrapper.py

from typing import List

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from PIL import Image
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import DPTForDepthEstimation, DPTImageProcessor

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class DepthEstimationInference(BaseImageInference):
    def __init__(
        self,
        device="cuda",
        batch_size=48,
        lower_percentile=15,
        upper_percentile=95,
        out_size=(768, 768),  # Reduced from 1024x1024 -> 512x512
        num_workers=12,  # Use 4 CPU workers for loading
    ):
        super().__init__(device=device, batch_size=batch_size)
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.out_size = out_size
        self.num_workers = num_workers
        self._load_model(None)

    def _load_model(self, checkpoint_path=None):
        self.feature_extractor = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
        self.model = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas").to(self.device)
        self.model.eval()

    def _preprocess_image(self, pil_image: Image.Image):
        inputs = self.feature_extractor(images=pil_image, return_tensors="pt")
        return inputs.pixel_values.squeeze(0)  # shape [3, H, W]

    def _postprocess_output(self, depth_map: torch.Tensor):
        # Depth map shape: [B, H, W]
        if depth_map.ndim == 3:
            depth_map = depth_map.unsqueeze(1)  # -> [B, 1, H, W]

        # Resize/normalize depth map
        depth_map = F.interpolate(
            depth_map,
            size=self.out_size,  # e.g. (512, 512) instead of (1024, 1024)
            mode="bicubic",
            align_corners=False,
        )
        depth_min = torch.amin(depth_map, dim=[1, 2, 3], keepdim=True)
        depth_max = torch.amax(depth_map, dim=[1, 2, 3], keepdim=True)
        depth_map_norm = (depth_map - depth_min) / (depth_max - depth_min + 1e-8)

        results = []
        # Now do CPU percentile for each image. 512x512 is 262,144 elements, a quarter the cost of 1024^2
        for i in range(depth_map_norm.size(0)):
            dm = depth_map_norm[i].squeeze().cpu().numpy()  # shape [512, 512]
            depth_values = dm.ravel()
            p_low = np.percentile(depth_values, self.lower_percentile)
            p_high = np.percentile(depth_values, self.upper_percentile)
            depth_score = float(p_high - p_low)

            results.append({"depth_score": depth_score})
        return results

    def infer_many(self, image_paths: List[str]):
        dataset = ImagePathDataset(image_paths, preprocess_fn=self._preprocess_image)
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,  # changed from 0
            pin_memory=True,
            collate_fn=custom_collate,
        )
        self.model.eval()
        results = []
        with torch.no_grad(), torch.autocast("cuda"):
            for batch in tqdm(dataloader, desc="Inferring paths"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device, non_blocking=True)
                output = self.model(images)
                batch_results = self._postprocess_output(output.predicted_depth)

                for path, res in zip(paths, batch_results):
                    res["path"] = path
                    results.append(res)

        return pd.DataFrame(results)


import glob


# Demo usage
def demo_depth_wrapper():
    folder_to_infer = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    image_paths = glob.glob(folder_to_infer + "/*.jpg")
    inference = DepthEstimationInference(
        device="cuda",
        batch_size=24,
        lower_percentile=15,
        upper_percentile=95,
    )

    # Many images (parallelized with ProcessPoolExecutor)
    df = inference.infer_many(image_paths)
    df.to_csv("depth_scores.csv", index=False)
    print("Inference completed. Results saved to 'depth_scores.csv'.")


if __name__ == "__main__":
    demo_depth_wrapper()
