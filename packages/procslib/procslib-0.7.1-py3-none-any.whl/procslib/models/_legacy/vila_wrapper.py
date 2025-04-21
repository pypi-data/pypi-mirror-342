"""wrapper class that uses the installed VILA library to tag images.

!! you NEED to install VILA repo first (see below for details)
"""

from typing import List

import pandas as pd
import torch
from llava import load
from llava.media import Image, Video
from PIL import Image as PILImage
from termcolor import colored
from tqdm import tqdm

from ..base_inference import BaseImageInference


# Implementation of BaseImageInference
class VILAInference(BaseImageInference):
    """wrapper class that uses the installed VILA library to tag images.

    !! you NEED to install VILA repo first:

    ```bash
    git clone https://github.com/NVlabs/VILA && cd VILA
    conda create --name vila python=3.10  ipykernel jupyterlab -y
    conda activate vila

    # # in the VILA repo:
    ./environment_setup.sh

    # then install procslib in the vila conda env
    ```
    """

    TEXT_PROMPT = "Please describe the image in 50 words"
    VIDEO_PROMPT = "Please describe the video in 50 words"

    def __init__(self, model_path: str = "Efficient-Large-Model/NVILA-15B", device: str = "cuda", batch_size: int = 1):
        super().__init__(device=device, batch_size=batch_size)
        self.model_path = model_path
        self._load_model(model_path)

    def _load_model(self, checkpoint_path: str):
        """Load the LLaVA model from the given path."""
        self.model = load(checkpoint_path)

    def _preprocess_image(self, pil_image: PILImage.Image) -> torch.Tensor:
        """Preprocess the PIL image into the format required by LLaVA."""
        # Placeholder: Convert PIL image to tensor (implement actual preprocessing if needed)
        return torch.tensor([])  # Replace with actual preprocessing logic

    def _postprocess_output(self, logits):
        """Postprocess the model output to generate a human-readable response."""
        return logits  # Replace with actual postprocessing logic (e.g., parsing logits)

    def _generate_response(self, media_path: str):
        """Helper to generate response from a single media path."""
        if any(media_path.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
            media = Image(media_path)
            text = self.TEXT_PROMPT
        elif any(media_path.endswith(ext) for ext in [".mp4", ".mkv", ".webm"]):
            media = Video(media_path)
            text = self.VIDEO_PROMPT
        else:
            raise ValueError(f"Unsupported media type: {media_path}")

        prompt = [media, text]
        response = self.model.generate_content(prompt)
        return response

    def infer_one(self, media_path: str):
        """Infer for a single media file (image or video)."""
        return self._generate_response(media_path)

    def infer_batch(self, media_paths: List[str]):
        """Infer for a batch of media files."""
        return [self.infer_one(path) for path in media_paths]

    def infer_many(self, media_paths: List[str]):
        """Infer for many media files and return a DataFrame with results."""
        results = []
        for path in tqdm(media_paths, desc="Processing media files"):
            response = self.infer_one(path)
            results.append(
                {
                    "path": path,  # Changed from "filename": os.path.basename(path)
                    "caption-nvila15b": response,
                },
            )

        # Debug: Print results to verify structure
        print(results)

        # Create DataFrame
        return pd.DataFrame(results)


# Demo of the refactored class
def demo():
    media_url = "https://huggingface.co/datasets/Efficient-Large-Model/VILA-inference-demos/resolve/main/OAI-sora-tokyo-walk.mp4"

    inference = VILAInference()
    response = inference.infer_one(media_url)
    print(colored(response, "green"))

    media_urls = [media_url] * 10
    df = inference.infer_many(media_urls)
    print(df)


if __name__ == "__main__":
    demo()
