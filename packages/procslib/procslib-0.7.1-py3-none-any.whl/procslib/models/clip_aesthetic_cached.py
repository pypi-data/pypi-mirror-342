"""Cached Clip Score calculation:

Gets clip scores -> stores to hdf5 -> compuates additional metrics with MLPs

Migrating Guide:

for old config (mlp_model, key_name), change to (mlp_model, key_name, task_type, label_map);

- eg. mlp_configs=[(my_regression_mlp, "aesthetic_score", "regression", {})]

for new config, a sample is:

mlp_configs=[
  (my_regression_mlp, "aesthetic_score", "regression", {}),
  (my_nsfw_mlp, "nsfw", "classification", {0:"SFW",1:"NSFW"}),
]
"""

import os
import warnings
from pathlib import Path
from typing import Dict, List, Tuple

import h5py
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from huggingface_hub import hf_hub_download
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from transformers import CLIPModel, CLIPProcessor

from .base_inference import BaseImageInference, custom_collate

# ======== Custom Dataset


class ClipImageDataset(Dataset):
    """A simple dataset that:
    - Takes a list of image paths (absolute or otherwise).
    - Uses a CLIPProcessor to convert each image to pixel_values (shape [3,H,W]).
    """

    def __init__(self, image_paths: List[str], processor: CLIPProcessor):
        self.image_paths = image_paths
        self.processor = processor

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        try:
            image = Image.open(path).convert("RGB")
            # Convert the PIL Image to [3, H, W] using the processor's image transform
            pixel_values = self.processor.image_processor(image).pixel_values[0]
            return torch.from_numpy(pixel_values), path
        except Exception as e:
            warnings.warn(f"Error loading image {path}: {e}")
            # Return a zero-tensor if loading fails
            zero_tensor = torch.zeros(3, 224, 224, dtype=torch.float32)
            return zero_tensor, path


# ======== Helpers


def sanitize_key(path: str) -> str:
    """HDF5 treats '/' as nested groups, so we replace them (and backslashes)
    with a harmless token. This yields a single-level key.
    """
    return path.replace("\\", "__").replace("/", "__")


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def tensor_to_float(tensor, precision=5):
    # Move tensor to CPU if it's on GPU, convert to numpy array, and get the first element
    value = tensor.cpu().detach().numpy().item()
    return round(value, precision)


# ======== MLP classes (unchanged MLP for regression, plus a new classifier MLP).


class MLP(nn.Module):
    """Existing MLP used for aesthetic score (regression)."""

    def __init__(self, input_size, xcol="emb", ycol="avg_rating"):
        super().__init__()
        self.input_size = input_size
        self.xcol = xcol
        self.ycol = ycol
        self.layers = nn.Sequential(
            nn.Linear(self.input_size, 1024),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            nn.Linear(16, 1),  # Single output for regression
        )

    def forward(self, x):
        return self.layers(x)


class ClassifierMLP(nn.Module):
    """Example multi-class (or binary) classification MLP.
    For 2-class tasks like NSFW (SFW vs. NSFW), set output_size=2.
    For 3-class tasks, set output_size=3, etc.
    """

    def __init__(self, input_size=768, output_size=2):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 1024),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            nn.Linear(16, output_size),
        )

    def forward(self, x):
        return self.layers(x)


def get_mlp_model(input_source, model_type: str = "regression", device: str = "cuda"):
    """Load a pre-trained MLP model from either a local path or a Hugging Face Hub repo id.
    The model file (.pth) is expected to contain a state dict whose final linear layer
    defines the output dimension. For regression, the final layer is expected to have 1 output.
    For classification, the final layer's output dimension will be used to instantiate the model.

    :param input_source: either a local path or a Hugging Face Hub repo id.
    :param model_type: "regression" (default) or "classification".
    :param device: device to load the model on, e.g. "cuda" or "cpu".
    :return: an instance of MLP (for regression) or ClassifierMLP (for classification), loaded with weights.
    """
    try:
        print(f"Attempting to load model from Hugging Face Hub: {input_source}")
        model_path = Path(hf_hub_download(repo_id=input_source, filename="model.pth"))
    except Exception as e:
        print(f"Failed to load from Hugging Face Hub, trying local path. Error: {e}")
        model_path = Path(input_source)

    # Load the state dict
    state_dict = torch.load(model_path, map_location=torch.device(device))
    keys = list(state_dict.keys())
    # Find the final layer's weight key in the sequential block
    final_keys = [k for k in keys if "layers" in k and "weight" in k]
    if not final_keys:
        raise ValueError("No layer weight keys found in the state dict.")
    final_key = final_keys[-1]
    output_dim = state_dict[final_key].shape[0]

    if model_type == "regression":
        model = MLP(768)  # Regression MLP is defined to output 1 value.
        if output_dim != 1:
            print(f"Warning: Expected regression output dimension 1, but state dict shows {output_dim}.")
    else:  # classification
        model = ClassifierMLP(768, output_size=output_dim)

    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


# ======== Inference Class


class CachedClipAestheticInference(BaseImageInference):
    """A model pipeline that:
      1) Loads or computes CLIP image embeddings,
      2) Optionally applies MLP(s) for final scores or classifications,
      3) Caches embeddings in HDF5 to skip re-computation.

    We override infer_many to do a custom pipeline:
      - load from HDF5 if cached,
      - compute new embeddings for uncached images,
      - produce final DataFrame with normal (original) paths.
    """

    def __init__(
        self,
        prompts_list: List[str],
        mlp_configs: List[Tuple[nn.Module, str, str, Dict[int, str]]],
        # Explanation for mlp_configs:
        #   Each item is (mlp_model, key_name, task_type, label_map)
        #   mlp_model  = either MLP (regression) or ClassifierMLP (classification)
        #   key_name   = string to store the result under in the final DataFrame
        #   task_type  = "regression" or "classification"
        #   label_map  = (optional) dictionary for classification index -> label
        #
        # For regression, set e.g. ("my_mlp", "score", "regression", {})
        # For classification, set e.g. ("nsfw_mlp", "nsfw", "classification", {0: "SFW", 1: "NSFW"})
        #
        h5_path: str,
        model_id: str = "openai/clip-vit-large-patch14",
        device: str = "cuda",
        batch_size: int = 32,
        num_workers: int = 4,
    ):
        """Args:
        prompts_list: list of text prompts for CLIP similarity scoring.
        mlp_configs: see doc above.
        h5_path: Path to the HDF5 file for caching embeddings.
        model_id: HF model id, e.g. "openai/clip-vit-large-patch14".
        device: "cpu" or "cuda".
        batch_size: batch size for DataLoader in infer_many.
        num_workers: # of workers for image loading.
        """
        super().__init__(device=device, batch_size=batch_size)
        self.prompts_list = prompts_list
        self.mlp_configs = mlp_configs
        self.h5_path = h5_path
        self.model_id = model_id
        self.num_workers = num_workers

        self.image_features = {}  # in-memory cache: {original_path -> np.array embedding}

        self._load_model()  # ignoring checkpoint_path
        self._prepare_text_embeddings()

    # -----------------------------
    # Overriding / implementing ABC methods
    # -----------------------------
    def _load_model(self, checkpoint_path: str = None):
        """Load CLIP model + processor from Hugging Face, onto self.device."""
        self.clip_model = CLIPModel.from_pretrained(self.model_id).to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained(self.model_id)
        self.clip_model.eval()

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Return a dummy [3,224,224]. We won't use base infer_many for real logic,
        since we do a custom pipeline below.
        """
        return torch.zeros(3, 224, 224)

    def _postprocess_output(self, logits: torch.Tensor):
        """Not used in the custom pipeline. Just return zeros to satisfy the ABC contract."""
        return [0.0] * logits.shape[0]

    # -----------------------------
    # Additional steps for CLIP + MLP logic
    # -----------------------------
    def _prepare_text_embeddings(self):
        """Precompute text embeddings for the prompts_list, store on GPU for quick multiply."""
        old_env = os.environ.get("TOKENIZERS_PARALLELISM", None)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

        with torch.no_grad():
            # If prompts_list is empty, skip
            if len(self.prompts_list) == 0:
                self.text_features = None
            else:
                inputs = self.clip_processor.tokenizer(
                    self.prompts_list,
                    padding=True,
                    return_tensors="pt",
                ).to(self.device)
                text_emb = self.clip_model.get_text_features(**inputs)
                text_emb = text_emb / text_emb.norm(p=2, dim=-1, keepdim=True)
                self.text_features = text_emb  # shape [num_prompts, D]

        # Restore environment var
        if old_env is None:
            del os.environ["TOKENIZERS_PARALLELISM"]
        else:
            os.environ["TOKENIZERS_PARALLELISM"] = old_env

    def _load_cached_embeddings(self, image_paths: List[str]) -> List[str]:
        """For each path in image_paths, if HDF5 has an entry, load it into self.image_features.
        Return a list of paths that are missing in the cache (need processing).
        """
        to_process = []
        if os.path.exists(self.h5_path):
            with h5py.File(self.h5_path, "r") as h5f:
                for p in image_paths:
                    key = sanitize_key(p)
                    if key in h5f:
                        self.image_features[p] = h5f[key][()]  # stored as np.array
                    else:
                        to_process.append(p)
        else:
            # If there's no HDF5, all paths are new
            to_process = image_paths
            # Ensure parent dirs for h5 exist
            os.makedirs(os.path.dirname(self.h5_path) or ".", exist_ok=True)
        return to_process

    def _compute_embeddings_for(self, paths_to_process: List[str]):
        """Load images for these paths, run CLIP image embedding,
        store them in memory and in the HDF5 file.
        """
        if not paths_to_process:
            return

        dataset = ClipImageDataset(paths_to_process, self.clip_processor)
        loader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=custom_collate,
        )
        with torch.no_grad(), h5py.File(self.h5_path, "a") as h5f:
            for batch in tqdm(loader, desc="Computing CLIP embeddings"):
                if batch is None:
                    continue
                images, batch_paths = batch
                images = images.to(self.device)
                emb = self.clip_model.get_image_features(pixel_values=images)
                emb = emb / emb.norm(p=2, dim=-1, keepdim=True)  # shape [B, D]

                for path, vec in zip(batch_paths, emb):
                    arr = vec.cpu().numpy()
                    self.image_features[path] = arr
                    key = sanitize_key(path)
                    if key not in h5f:
                        h5f.create_dataset(key, data=arr)

    def _compute_scores_from_features(self) -> dict:
        """For each path's embedding in self.image_features, compute:
          - CLIP similarity to each prompt (if prompts_list is not empty),
          - MLP-based scores/classifications if mlp_configs are given.

        Return { path: {...scores...} }.
        """
        results = {}
        scale = self.clip_model.logit_scale.exp()

        with torch.no_grad():
            for path, emb_np in tqdm(self.image_features.items(), desc="Computing final scores"):
                emb_tensor = torch.tensor(emb_np, device=self.device).unsqueeze(0)  # [1, D]

                # CLIP similarity
                clip_scores_dict = {}
                if self.text_features is not None and len(self.prompts_list) > 0:
                    clip_scores_tensor = (emb_tensor @ self.text_features.t()) * scale
                    clip_scores = clip_scores_tensor.squeeze(0).cpu().numpy()
                    clip_scores_dict = {prompt: float(sc) for prompt, sc in zip(self.prompts_list, clip_scores)}

                # MLP-based results
                mlp_results = {}
                # Re-normalize embeddings if your MLP expects normalized input
                emb_norm_np = normalized(emb_tensor.cpu().numpy())
                emb_norm_tensor = torch.from_numpy(emb_norm_np).to(self.device, dtype=torch.float32)

                for mlp_model, key_name, task_type, label_map in self.mlp_configs:
                    out = mlp_model(emb_norm_tensor)
                    if task_type == "regression":
                        # single output => out shape [1,1] or [1]
                        # we store a float
                        value = tensor_to_float(out.squeeze(dim=-1))
                        mlp_results[key_name] = value
                    elif task_type == "classification":
                        # out shape [1, num_classes]
                        probs = F.softmax(out, dim=-1)
                        pred_idx = torch.argmax(probs, dim=-1).item()
                        pred_label = label_map.get(pred_idx, f"cls_{pred_idx}")
                        conf = probs[0, pred_idx].item()

                        # For classification, we might store 2 columns:
                        #   <key_name>_label, <key_name>_conf
                        # or we can store a single dict. We'll do 2 columns for clarity.
                        mlp_results[f"{key_name}_label"] = pred_label
                        mlp_results[f"{key_name}_conf"] = round(conf, 5)
                    else:
                        # fallback if something else
                        mlp_results[key_name] = None

                results[path] = {
                    "clip_scores": clip_scores_dict,
                    **mlp_results,
                }

        return results

    # -----------------------------
    # Main function: infer_many
    # -----------------------------
    def infer_many(self, image_paths: List[str]) -> pd.DataFrame:
        """Overridden pipeline:
        1) Temporarily set TOKENIZERS_PARALLELISM="false".
        2) Load any cached embeddings from h5.
        3) Compute embeddings for new images.
        4) Compute final scores (CLIP + MLP).
        5) Return a DataFrame with columns:
           [filename, clip_scores, <mlp_keys>... ]
           where 'filename' is the original path.
        """
        old_env = os.environ.get("TOKENIZERS_PARALLELISM", None)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

        try:
            # 1) Identify missing embeddings
            to_process = self._load_cached_embeddings(image_paths)

            # 2) Compute embeddings for missing images
            self._compute_embeddings_for(to_process)

            # 3) Compute final scores from all embeddings
            results_dict = self._compute_scores_from_features()

        finally:
            # Restore environment variable
            if old_env is None:
                del os.environ["TOKENIZERS_PARALLELISM"]
            else:
                os.environ["TOKENIZERS_PARALLELISM"] = old_env

        # 4) Convert results_dict => DataFrame
        rows = []
        for path, score_dict in results_dict.items():
            row = {
                "path": path,  # Changed from "filename": path
                "clip_scores": score_dict.get("clip_scores", {}),
            }
            for k, v in score_dict.items():
                if k == "clip_scores":
                    continue
                row[k] = v
            rows.append(row)

        return pd.DataFrame(rows)


def main():
    # 1) Prepare your MLP(s)
    aesthetic_mlp = MLP(768)  # existing regression MLP
    aesthetic_mlp_state = torch.load("/path/to/aesthetic_mlp.pth", map_location="cpu")
    aesthetic_mlp.load_state_dict(aesthetic_mlp_state)
    aesthetic_mlp.to("cuda").eval()

    nsfw_mlp = ClassifierMLP(input_size=768, output_size=2)  # NSFW vs SFW
    nsfw_mlp_state = torch.load("/path/to/nsfw_mlp_v5.pth", map_location="cpu")
    nsfw_mlp.load_state_dict(nsfw_mlp_state)
    nsfw_mlp.to("cuda").eval()

    # 2) Create mlp_configs
    mlp_configs = [
        # Regression
        (aesthetic_mlp, "aesthetic_score", "regression", {}),
        # Classification
        (nsfw_mlp, "nsfw", "classification", {0: "SFW", 1: "NSFW"}),
    ]

    # 3) Initialize the pipeline
    inference_pipeline = CachedClipAestheticInference(
        prompts_list=["beautiful", "ugly"],  # optional textual prompts
        mlp_configs=mlp_configs,
        h5_path="/path/to/clip_emb_cache.h5",
        model_id="openai/clip-vit-large-patch14",
        device="cuda",
        batch_size=16,
        num_workers=4,
    )

    # 4) Gather image paths
    image_folder = "/path/to/test/images"
    image_paths = [
        os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    # 5) Run inference
    df_results = inference_pipeline.infer_many(image_paths)
    print(df_results.head(10))
    df_results.to_csv("combined_inference_results.csv", index=False)
    print("Done! Results saved to combined_inference_results.csv.")


if __name__ == "__main__":
    main()
