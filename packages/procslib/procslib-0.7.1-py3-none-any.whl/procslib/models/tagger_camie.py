# https://huggingface.co/Camais03/camie-tagger

"""image_tagger_wrapper.py

Contains:
- FlashAttention: optional custom multi-head attention module
- TagDataset: utility for mapping indices to tag names/categories
- ImageTagger: the two-stage tagger model (backbone + refined predictions)
- load_model: helper function to load a saved ImageTagger
- ImageTaggerInference: procslib-style inference class that wraps ImageTagger
"""

import json
import os
from typing import Any, Dict, List, Optional

import torch
import torch.nn.functional as F
import torchvision.transforms as T
from huggingface_hub import hf_hub_download
from PIL import Image
from torch import nn

# You may already have these in your codebase:
from torchvision.models import EfficientNet_V2_L_Weights, efficientnet_v2_l

# If you don't have tqdm installed in your environment or want to rely on the procslib
# style tqdm, you can omit or adapt accordingly:
from tqdm.auto import tqdm


# -------------------------------------------------------------------------
# 1) Custom FlashAttention (from your snippet)
# -------------------------------------------------------------------------
def flash_attn_func(q, k, v, dropout_p=0.0, softmax_scale=1.0, causal=False):
    """Mock or minimal replacement for a more specialized FlashAttention kernel.
    If you have a real flash_attn function, import and use that directly here.
    For demonstration, we'll do a regular scaled dot-product attention.
    """
    # q, k, v shape: [B, H, S, D]
    # We can do a simple scaled dot product manually:
    B, H, S, D = q.shape
    # (B, H, S, D) x (B, H, D, S) -> [B, H, S, S]
    attn_logits = torch.matmul(q, k.transpose(-2, -1)) * softmax_scale

    # Optionally apply causal mask (not strictly needed for your snippet)
    if causal:
        mask = torch.triu(torch.ones(S, S, device=q.device, dtype=torch.bool), diagonal=1)
        attn_logits[..., mask] = float("-inf")

    attn_weights = F.softmax(attn_logits, dim=-1)
    if dropout_p > 0.0 and q.requires_grad:
        attn_weights = F.dropout(attn_weights, p=dropout_p)

    # Weighted sum
    out = torch.matmul(attn_weights, v)
    return out


class FlashAttention(nn.Module):
    """Custom multi-head attention block from your snippet.
    Uses 'flash_attn_func' above as a placeholder for real flash-attn.
    """

    def __init__(self, dim, num_heads=8, dropout=0.1, batch_first=True):
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.dropout = dropout
        self.batch_first = batch_first
        self.head_dim = dim // num_heads
        assert self.head_dim * num_heads == dim, "dim must be divisible by num_heads"

        self.q_proj = nn.Linear(dim, dim, bias=False)
        self.k_proj = nn.Linear(dim, dim, bias=False)
        self.v_proj = nn.Linear(dim, dim, bias=False)
        self.out_proj = nn.Linear(dim, dim, bias=False)

        for proj in [self.q_proj, self.k_proj, self.v_proj, self.out_proj]:
            nn.init.xavier_uniform_(proj.weight, gain=0.1)

        self.scale = self.head_dim**-0.5
        self.debug = False

    def forward(
        self,
        query: torch.Tensor,
        key: Optional[torch.Tensor] = None,
        value: Optional[torch.Tensor] = None,
        mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        batch_size, seq_len, _ = query.shape
        if key is None:
            key = query
        if value is None:
            value = query

        # Project
        q = self.q_proj(query)
        k = self.k_proj(key)
        v = self.v_proj(value)

        # Reshape to [B, H, S, D]
        q = q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # Prepare optional mask
        # (For your snippet, you might do a more advanced mask, but we'll skip detail here.)
        output = flash_attn_func(
            q,
            k,
            v,
            dropout_p=self.dropout if self.training else 0.0,
            softmax_scale=self.scale,
            causal=False,
        )

        # [B, H, S, D] -> [B, S, H, D] -> [B, S, D]
        output = output.transpose(1, 2).contiguous()
        output = output.view(batch_size, seq_len, self.dim)

        # Output linear
        output = self.out_proj(output)
        return output


# -------------------------------------------------------------------------
# 2) TagDataset: simple dataset to map indices <-> tag names/categories
# -------------------------------------------------------------------------
class TagDataset:
    """Lightweight dataset wrapper for inference only"""

    def __init__(self, total_tags, idx_to_tag, tag_to_category):
        self.total_tags = total_tags
        # Convert string keys to int if needed
        if not isinstance(idx_to_tag, dict):
            self.idx_to_tag = {int(k): v for k, v in idx_to_tag.items()}
        else:
            self.idx_to_tag = idx_to_tag

        self.tag_to_category = tag_to_category

    def get_tag_info(self, idx):
        """Get tag name and category for a given index."""
        tag_name = self.idx_to_tag.get(str(idx), f"unknown-{idx}")
        category = self.tag_to_category.get(tag_name, "general")
        return tag_name, category


# -------------------------------------------------------------------------
# 3) Two-stage ImageTagger (backbone, initial + refined predictions)
# -------------------------------------------------------------------------
class ImageTagger(nn.Module):
    """Two-stage image tagger model:
    - EfficientNet V2 (L) backbone for image features
    - Stage 1: initial classifier
    - Stage 2: top-K tag selection, cross-attention, refined classifier
    """

    def __init__(
        self,
        total_tags: int,
        dataset: TagDataset,
        model_name: str = "efficientnet_v2_l",
        num_heads: int = 16,
        dropout: float = 0.1,
        pretrained: bool = True,
        tag_context_size: int = 256,
    ):
        super().__init__()
        self.dataset = dataset
        self.total_tags = total_tags
        self.tag_context_size = tag_context_size
        self.embedding_dim = 1280  # fixed for EfficientNet_V2_L features
        self._flags = {"debug": False, "model_stats": False}

        # 1) Initialize backbone
        if model_name == "efficientnet_v2_l":
            weights = EfficientNet_V2_L_Weights.DEFAULT if pretrained else None
            self.backbone = efficientnet_v2_l(weights=weights)
            # remove final classifier so we only have feature extractor
            self.backbone.classifier = nn.Identity()

        # spatial pooling
        self.spatial_pool = nn.AdaptiveAvgPool2d((1, 1))

        # 2) Initial classifier
        self.initial_classifier = nn.Sequential(
            nn.Linear(self.embedding_dim, self.embedding_dim * 2),
            nn.LayerNorm(self.embedding_dim * 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(self.embedding_dim * 2, self.embedding_dim),
            nn.LayerNorm(self.embedding_dim),
            nn.GELU(),
            nn.Linear(self.embedding_dim, total_tags),
        )

        # 3) Tag embedding for second stage
        self.tag_embedding = nn.Embedding(total_tags, self.embedding_dim)
        self.tag_attention = FlashAttention(self.embedding_dim, num_heads, dropout)
        self.tag_norm = nn.LayerNorm(self.embedding_dim)

        # 4) Cross attention projection
        self.cross_proj = nn.Sequential(
            nn.Linear(self.embedding_dim, self.embedding_dim * 2),
            nn.LayerNorm(self.embedding_dim * 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(self.embedding_dim * 2, self.embedding_dim),
        )
        self.cross_attention = FlashAttention(self.embedding_dim, num_heads, dropout)
        self.cross_norm = nn.LayerNorm(self.embedding_dim)

        # 5) Refined classifier
        self.refined_classifier = nn.Sequential(
            nn.Linear(self.embedding_dim * 2, self.embedding_dim * 2),  # concatenated dim
            nn.LayerNorm(self.embedding_dim * 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(self.embedding_dim * 2, self.embedding_dim),
            nn.LayerNorm(self.embedding_dim),
            nn.GELU(),
            nn.Linear(self.embedding_dim, total_tags),
        )

        # 6) Temperature scaling
        self.temperature = nn.Parameter(torch.ones(1) * 1.5)

    @property
    def debug(self):
        return self._flags["debug"]

    @debug.setter
    def debug(self, value):
        self._flags["debug"] = value

    @property
    def model_stats(self):
        return self._flags["model_stats"]

    @model_stats.setter
    def model_stats(self, value):
        self._flags["model_stats"] = value

    def _get_selected_tags(self, logits: torch.Tensor):
        """Select top-K tags based on initial prediction confidence.
        Return (topk_indices, topk_values).
        """
        # apply sigmoid to get probabilities
        probs = torch.sigmoid(logits)
        batch_size = logits.size(0)

        # get top-K predictions for each image
        topk_values, topk_indices = torch.topk(
            probs,
            k=self.tag_context_size,
            dim=1,
            largest=True,
            sorted=True,
        )
        return topk_indices, topk_values

    def preprocess_image(self, image_path: str, image_size: int = 512):
        """Convert an image file on disk to the same shape as training.
        Adjust if you used different transformations or augmentations.
        """
        if not os.path.exists(image_path):
            raise ValueError(f"Image not found at path: {image_path}")

        transform = T.Compose(
            [
                T.ToTensor(),
            ],
        )

        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            width, height = img.size
            aspect_ratio = width / height
            if aspect_ratio > 1:
                new_width = image_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = image_size
                new_width = int(new_height * aspect_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            new_image = Image.new("RGB", (image_size, image_size), (0, 0, 0))
            paste_x = (image_size - new_width) // 2
            paste_y = (image_size - new_height) // 2
            new_image.paste(img, (paste_x, paste_y))

            img_tensor = transform(new_image)
        return img_tensor

    def forward(self, x: torch.Tensor):
        """Main forward pass returning (initial_preds, refined_preds)."""
        # 1) image feature extraction
        feats = self.backbone.features(x)
        feats = self.spatial_pool(feats).squeeze(-1).squeeze(-1)

        # 2) initial predictions
        initial_logits = self.initial_classifier(feats)
        initial_preds = torch.clamp(initial_logits / self.temperature, min=-15.0, max=15.0)

        # 3) select top-K tags
        pred_tag_indices, _ = self._get_selected_tags(initial_preds)

        # 4) self-attention on selected tags
        tag_embeddings = self.tag_embedding(pred_tag_indices)  # [B, K, D]
        attended_tags = self.tag_attention(tag_embeddings)  # [B, K, D]
        attended_tags = self.tag_norm(attended_tags)

        # 5) cross-attention
        feats_proj = self.cross_proj(feats)  # [B, D]
        feats_expanded = feats_proj.unsqueeze(1).expand(-1, self.tag_context_size, -1)  # [B, K, D]
        cross_attended = self.cross_attention(feats_expanded, attended_tags)
        cross_attended = self.cross_norm(cross_attended)

        # 6) fuse features
        fused_features = cross_attended.mean(dim=1)  # [B, D]
        combined_features = torch.cat([feats, fused_features], dim=-1)  # [B, 2D]

        # 7) refined predictions
        refined_logits = self.refined_classifier(combined_features)
        refined_preds = torch.clamp(refined_logits / self.temperature, min=-15.0, max=15.0)

        return initial_preds, refined_preds

    def predict(
        self,
        image_path: str,
        threshold: float = 0.325,
        category_thresholds: Optional[Dict[str, float]] = None,
    ):
        """Single-image inference, applying optional category-specific thresholds.
        Returns a dict with:
         - 'initial_probabilities'
         - 'refined_probabilities'
         - 'predictions' (binary thresholded)
        """
        device = next(self.parameters()).device
        dtype = next(self.parameters()).dtype

        # load and preprocess
        img_tensor = self.preprocess_image(image_path).unsqueeze(0)
        img_tensor = img_tensor.to(device, dtype=dtype)

        with torch.no_grad():
            init_preds, ref_preds = self.forward(img_tensor)
            init_probs = torch.sigmoid(init_preds)
            ref_probs = torch.sigmoid(ref_preds)

            # apply thresholds
            if category_thresholds:
                # create binary predictions
                refined_binary = torch.zeros_like(ref_probs)
                for cat, cat_thresh in category_thresholds.items():
                    category_mask = torch.zeros_like(ref_probs, dtype=torch.bool)
                    # find indices for this category
                    for tag_idx in range(ref_probs.size(-1)):
                        tag_name, tag_cat = self.dataset.get_tag_info(tag_idx)
                        if tag_cat == cat:
                            category_mask[:, tag_idx] = True
                    # threshold
                    cat_threshold_tensor = torch.tensor(cat_thresh, device=device, dtype=dtype)
                    refined_binary[category_mask] = (ref_probs[category_mask] >= cat_threshold_tensor).to(dtype)
                predictions = refined_binary
            else:
                threshold_tensor = torch.tensor(threshold, device=device, dtype=dtype)
                predictions = (ref_probs >= threshold_tensor).to(dtype)

        return {
            "initial_probabilities": init_probs,
            "refined_probabilities": ref_probs,
            "predictions": predictions,
        }

    def get_tags_from_predictions(self, predictions: torch.Tensor, include_probabilities: bool = True):
        """Convert model predictions to human-readable tags grouped by category.
        `predictions` is expected to be shape [B, total_tags] or [total_tags].
        """
        if predictions.dim() > 1:
            predictions = predictions[0]  # remove batch dimension

        # indices of positive predictions
        indices = torch.where(predictions > 0)[0].cpu().tolist()

        result = {}
        for idx in indices:
            tag_name, category = self.dataset.get_tag_info(idx)
            if category not in result:
                result[category] = []
            if include_probabilities:
                prob = predictions[idx].item()
                result[category].append((tag_name, prob))
            else:
                result[category].append(tag_name)

        # sort by probability
        if include_probabilities:
            for cat in result:
                result[cat] = sorted(result[cat], key=lambda x: x[1], reverse=True)
        return result


# -------------------------------------------------------------------------
# 4) load_model function
# -------------------------------------------------------------------------
def load_model(model_dir: str, device: str = "cuda"):
    """Load the two-stage ImageTagger from a directory containing:
    - metadata.json  (with total_tags, idx_to_tag, tag_to_category)
    - model_info.json (with num_heads, precision, tag_context_size, etc.)
    - model.pt       (the saved state_dict)
    """
    print(f"Loading model from {model_dir} ...")

    if os.path.exists(model_dir):
        metadata_path = f"{model_dir}/metadata.json"
    else:
        # not a local pass; download instead
        metadata_path = hf_hub_download(model_dir, filename="metadata.json")

    with open(metadata_path) as f:
        metadata = json.load(f)
    if not metadata:
        raise FileNotFoundError(f"Missing or failed to load metadata.json in {model_dir}")
    total_tags = metadata["total_tags"]
    idx_to_tag = metadata["idx_to_tag"]
    tag_to_category = metadata["tag_to_category"]

    # optional model_info
    if os.path.exists(f"{model_dir}/model_info_refined.json"):
        model_info_path = f"{model_dir}/model_info_refined.json"
    else:
        model_info_path = hf_hub_download(model_dir, filename="model_info_refined.json")

    with open(model_info_path) as f:
        model_info = json.load(f)
    if model_info:
        print("✓ Model info loaded.")
    else:
        print("WARNING: model_info.json not found; using defaults.")
        model_info = {
            "precision": "float16",
            "num_heads": 16,
            "tag_context_size": 256,
        }

    dataset = TagDataset(
        total_tags=total_tags,
        idx_to_tag=idx_to_tag,
        tag_to_category=tag_to_category,
    )

    model = ImageTagger(
        total_tags=total_tags,
        dataset=dataset,
        num_heads=model_info.get("num_heads", 16),
        tag_context_size=model_info.get("tag_context_size", 256),
        pretrained=False,
    )

    # load weights
    if os.path.exists(f"{model_dir}/model_refined.pt"):
        state_dict_path = f"{model_dir}/model_refined.pt"
    else:
        # not a local pass; download instad
        state_dict_path = hf_hub_download(model_dir, filename="model_refined.pt")
    if not os.path.exists(state_dict_path):
        raise FileNotFoundError(f"Missing {state_dict_path} in {model_dir}")

    state_dict = torch.load(state_dict_path, map_location=device)
    try:
        model.load_state_dict(state_dict, strict=True)
        print("✓ Model state dict loaded (strict=True).")
    except Exception as e:
        print(f"! Strict loading failed: {e!s}")
        print("Attempting non-strict loading...")
        missing_keys, unexpected_keys = model.load_state_dict(state_dict, strict=False)
        print(f"  - Missing keys: {missing_keys}")
        print(f"  - Unexpected keys: {unexpected_keys}")

    model = model.to(device)
    if model_info.get("precision", "float16") == "float16":
        model = model.half()
        print("✓ Converted model to half precision.")
    model.eval()
    print("✓ Model is ready on device:", device)

    return model, dataset


# -------------------------------------------------------------------------
# 5) procslib-style inference class
# -------------------------------------------------------------------------
import pandas as pd

from procslib.models.base_inference import BaseImageInference


class CamieTaggerInference(BaseImageInference):
    """A procslib-style wrapper around the two-stage ImageTagger."""

    def __init__(
        self,
        model_dir: str,
        threshold: float = 0.325,
        category_thresholds: dict = None,
        device: str = "cuda",
        batch_size: int = 1,
        **kwargs,
    ):
        super().__init__(device=device, batch_size=batch_size, **kwargs)
        self.model_dir = model_dir
        self.threshold = threshold
        self.category_thresholds = category_thresholds
        self._load_model(None)  # ignoring the checkpoint path param in this design

    def _load_model(self, checkpoint_path: str):
        self.model, self.dataset = load_model(self.model_dir, device=self.device)
        self.model.eval()

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Convert a PIL image to the same shape as training.
        We'll do a basic transform here or re-implement logic from model.
        """
        transform = T.Compose(
            [
                T.Resize(512),
                T.CenterCrop(512),
                T.ToTensor(),
            ],
        )
        return transform(pil_image)

    def _postprocess_output(self, prediction_dict: dict) -> Dict[str, Any]:
        """Convert the raw dictionary from `model.predict(...)` into final predictions."""
        if prediction_dict is None:
            return {}
        bin_preds = prediction_dict["predictions"]  # shape [B, total_tags]
        # Convert to tags
        tags = self.model.get_tags_from_predictions(bin_preds, include_probabilities=True)
        return tags

    def infer_many(self, image_paths: List[str], **kwargs) -> pd.DataFrame:
        """If your model is single-image-based (like 'model.predict'),
        just loop. If you want real batching, override accordingly.
        """
        results = []
        for path in tqdm(image_paths, desc="Inferring with ImageTagger"):
            try:
                pred_dict = self.model.predict(
                    image_path=path,
                    threshold=self.threshold,
                    category_thresholds=self.category_thresholds,
                )
                tags = self._postprocess_output(pred_dict)

                result_entry = {"path": path}
                for key, values in tags.items():
                    result_entry[f"camie_pred_{key}"] = " ".join([tag for tag, _ in values])

                results.append(result_entry)
            except Exception as e:
                print(f"Error on {path}: {e}")
                results.append({"path": path})

        return pd.DataFrame(results)
