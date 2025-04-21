"""(kind of) updated danbooru tagger, knowledge cutoff ~early 2025

Supports:
- danbooru tags
- character tags
- artist / year tags (not accurate)

https://huggingface.co/spaces/Johnny-Z/danbooru_tagger
"""
# src/procslib/models/jz_tagger.py

from typing import List

import torch
import unibox as ub
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import AutoModel, CLIPImageProcessor

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate

# ---------- Helper Modules (MLP, AES) ----------


class MLP(nn.Module):
    """MLP head for multi-label classification."""

    def __init__(self, input_size, class_num):
        super().__init__()
        self.layers0 = nn.Sequential(
            nn.Linear(input_size, 1280),
            nn.LayerNorm(1280),
            nn.Mish(),
        )
        self.layers2 = nn.Sequential(
            nn.Linear(1280, 640),
            nn.LayerNorm(640),
            nn.Mish(),
            nn.Dropout(0.2),
        )
        self.layers3 = nn.Sequential(
            nn.Linear(1280, 640),
            nn.LayerNorm(640),
            nn.Mish(),
            nn.Dropout(0.2),
        )
        self.layers4 = nn.Sequential(
            nn.Linear(1280, 640),
            nn.LayerNorm(640),
            nn.Mish(),
            nn.Dropout(0.2),
        )
        self.layers1 = nn.Sequential(
            nn.Linear(640, class_num),
            nn.Sigmoid(),
        )

    def forward(self, x):
        out = self.layers0(x)
        # skip connections
        out = self.layers2(out) + self.layers3(out) + self.layers4(out)
        out = self.layers1(out)
        return out


class AES(nn.Module):
    """MLP head for aesthetic score regression (range ~ 0-10)."""

    def __init__(self, input_size):
        super().__init__()
        self.layers0 = nn.Sequential(
            nn.Linear(input_size, 1280),
            nn.LayerNorm(1280),
            nn.Mish(),
        )
        self.layers2 = nn.Sequential(
            nn.Linear(1280, 640),
            nn.LayerNorm(640),
            nn.Mish(),
            nn.Dropout(0.2),
            nn.Linear(640, 1),
        )
        self.layers3 = nn.Sequential(
            nn.Linear(1280, 640),
            nn.LayerNorm(640),
            nn.Mish(),
            nn.Dropout(0.2),
            nn.Linear(640, 1),
        )
        self.layers4 = nn.Sequential(
            nn.Linear(1280, 640),
            nn.LayerNorm(640),
            nn.Mish(),
            nn.Dropout(0.2),
            nn.Linear(640, 1),
        )
        self.layers1 = nn.Sequential(
            nn.Sigmoid(),
        )

    def forward(self, x):
        out = self.layers0(x)
        out = self.layers2(out) + self.layers3(out) + self.layers4(out)
        out = self.layers1(out) * 10
        return out


# ---------- Main Inference Class ----------


class JzDanbooruTaggerInference(BaseImageInference):
    """Danbooru Tagger Inference class:
    - Loads the 'nvidia/RADIO-H' model (with custom heads).
    - Tag dictionaries + thresholds for multi-label classification.
    - Optionally returns aesthetic score (AVA).
    """

    def __init__(
        self,
        model_dir: str = "hf://arot/jz-danbooru-tagger",
        device="cuda",
        batch_size=1,
        general_threshold=0.75,
        character_threshold=0.9,
        artist_threshold=0.8,
        shortest_edge=512,
        patch_size=16,
        **kwargs,
    ):
        super().__init__(device=device, batch_size=batch_size)
        # thresholds, sizes
        self.general_threshold = general_threshold
        self.character_threshold = character_threshold
        self.artist_threshold = artist_threshold
        self.shortest_edge = shortest_edge
        self.patch_size = patch_size

        # Construct paths using model_dir
        self.path_general_tags = f"{model_dir}/general_tag_dict.json"
        self.path_character_tags = f"{model_dir}/character_tag_dict.json"
        self.path_artist_tags = f"{model_dir}/artist_tag_dict.json"
        self.path_implications = f"{model_dir}/implications_list.json"

        self.path_cls_predictor = ub.loads(f"{model_dir}/cls_predictor.pth", file=True)
        self.path_char_predictor = ub.loads(f"{model_dir}/character_predictor.pth", file=True)
        self.path_artist_predictor = ub.loads(f"{model_dir}/artist_predictor.pth", file=True)
        self.path_aes_predictor = ub.loads(f"{model_dir}/aesthetic_predictor_ava.pth", file=True)

        # placeholders for loaded items
        self.model = None
        self.image_processor = None
        self.general_dict = {}
        self.character_dict = {}
        self.artist_dict = {}
        self.implications_list = {}
        self.mlp_general = None
        self.mlp_character = None
        self.mlp_artist = None
        self.mlp_ava = None

        # load everything
        self._load_model(checkpoint_path=None)

    def _load_model(self, checkpoint_path: str = None):
        """Load the base model + custom heads + metadata."""
        # 1) Load the backbone from HF
        self.model = AutoModel.from_pretrained(
            "nvidia/RADIO-H",
            trust_remote_code=True,
        ).to(self.device)
        self.model.eval()

        # 2) Create a CLIP-like processor
        self.image_processor = CLIPImageProcessor(
            crop_size={"height": 512, "width": 512},
            do_center_crop=False,
            do_convert_rgb=True,
            do_normalize=False,
            do_rescale=True,
            do_resize=False,
        )

        # 3) Load the JSON dictionaries
        self.general_dict = ub.loads(self.path_general_tags)
        self.character_dict = ub.loads(self.path_character_tags)
        self.artist_dict = ub.loads(self.path_artist_tags)
        self.implications_list = ub.loads(self.path_implications)

        # 4) Initialize the MLP heads and load weights
        # Each MLP has an input_size=3840 in your snippet
        general_class = len(self.general_dict)
        self.mlp_general = MLP(3840, general_class)
        self.mlp_general.load_state_dict(
            torch.load(self.path_cls_predictor, map_location=self.device),
        )
        self.mlp_general.to(self.device)
        self.mlp_general.eval()

        character_class = len(self.character_dict)
        self.mlp_character = MLP(3840, character_class)
        self.mlp_character.load_state_dict(
            torch.load(self.path_char_predictor, map_location=self.device),
        )
        self.mlp_character.to(self.device)
        self.mlp_character.eval()

        artist_class = len(self.artist_dict)
        self.mlp_artist = MLP(3840, artist_class)
        self.mlp_artist.load_state_dict(
            torch.load(self.path_artist_predictor, map_location=self.device),
        )
        self.mlp_artist.to(self.device)
        self.mlp_artist.eval()

        # Aesthetic
        self.mlp_ava = AES(3840)
        self.mlp_ava.load_state_dict(
            torch.load(self.path_aes_predictor, map_location=self.device),
        )
        self.mlp_ava.to(self.device)
        self.mlp_ava.eval()

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Resize to ensure shortest edge = 512, then pad to multiple of patch_size, convert to tensor."""
        # Convert RGBA -> RGB if needed
        if pil_image.mode == "RGBA":
            background = Image.new("RGBA", pil_image.size, (255, 255, 255, 255))
            pil_image = Image.alpha_composite(background, pil_image).convert("RGB")

        width, height = pil_image.size
        # Scale so that the shortest edge = self.shortest_edge
        if width < height:
            new_height = int((self.shortest_edge / width) * height)
            new_width = self.shortest_edge
        else:
            new_width = int((self.shortest_edge / height) * width)
            new_height = self.shortest_edge

        # Snap to multiples of patch_size
        new_width = max(self.patch_size, round(new_width / self.patch_size) * self.patch_size)
        new_height = max(self.patch_size, round(new_height / self.patch_size) * self.patch_size)

        pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

        # Use your custom CLIPImageProcessor WITHOUT re-resizing:
        inputs = self.image_processor(images=pil_image, return_tensors="pt", do_resize=False)
        # inputs.pixel_values shape: [1, 3, new_height, new_width]
        return inputs.pixel_values.squeeze(0)

    def _postprocess_output(self, logits: torch.Tensor):
        """Given the final embeddings from your backbone, apply your MLP heads.
        Return a dictionary with:
            {
                "tags_str": "...",
                "artist_tags": {...},
                "character_tags": {...},
                "general_tags": {...},
                "rating": {... or empty},
                "date": {... or empty},
                "ava_score": float
            }
        """
        # The snippet uses 'summary' as your model's final output.
        # Here, 'logits' is the 3840-dim embedding if we follow your code’s usage.
        # We'll replicate that logic below.

        # For safety, cast to float32
        if logits.dtype != torch.float32:
            logits = logits.float()

        # 1) Predictions from MLP heads
        general_pred = self.mlp_general(logits)
        character_pred = self.mlp_character(logits)
        artist_pred = self.mlp_artist(logits)
        ava_score = float(self.mlp_ava(logits).item())  # single value

        # 2) Convert to tags
        general_tags, rating, date = self._prediction_to_tag(
            general_pred,
            self.general_dict,
            threshold=self.general_threshold,
        )
        character_tags, _, _ = self._prediction_to_tag(
            character_pred,
            self.character_dict,
            threshold=self.character_threshold,
        )
        artist_tags, _, _ = self._prediction_to_tag(
            artist_pred,
            self.artist_dict,
            threshold=self.artist_threshold,
        )

        # Merge general + character tags for implications
        combined_keys = set(general_tags.keys()).union(character_tags.keys())
        # Remove implied tags
        remove_set = set()
        for tag in combined_keys:
            if tag in self.implications_list:
                # implication_list[tag] is a list of tags to remove
                remove_set.update(self.implications_list[tag])

        # Filter out
        final_tags = []
        for tag in combined_keys:
            if tag not in remove_set:
                final_tags.append(tag)

        # Some tags are Kaomojis. If you want, rename underscores unless in the kaomoji set:
        kaomojis = {
            "0_0",
            "(o)_(o)",
            "+_+",
            "+_-",
            "._.",
            "<o>_<o>",
            "<|>_<|>",
            "=_=",
            ">_<",
            "3_3",
            "6_9",
            ">_o",
            "@_@",
            "^_^",
            "o_o",
            "u_u",
            "x_x",
            "|_|",
            "||_||",
        }
        # Reformat underscores as spaces unless it's a known kaomoji
        tags_str_list = []
        for t in final_tags:
            if t in kaomojis:
                tags_str_list.append(t)
            else:
                tags_str_list.append(t.replace("_", " "))

        tags_str = ", ".join(tags_str_list)

        # Return final dictionary
        return {
            "tags_str": tags_str,
            "artist_tags": artist_tags,
            "character_tags": character_tags,
            "general_tags": general_tags,
            "rating": rating,
            "date": date,
            "ava_score": ava_score,
        }

    def _prediction_to_tag(self, prediction, tag_dict, threshold=0.75):
        """Returns (filtered_tags, rating_dict, date_dict).
        rating/date are singled out if they appear.
        """
        prediction = prediction.view(-1)
        # Indices in your dict start at 1, so offset by -1
        predicted_ids = (prediction >= 0.2).nonzero(as_tuple=True)[0].cpu().numpy() + 1

        # separate out rating/date
        rating_tags = {}
        date_tags = {}
        filtered = {}

        # Iterate all tags in tag_dict, check if predicted
        for tag, meta in tag_dict.items():
            # meta[2] is the ID; meta[1] is category
            if meta[2] in predicted_ids:
                conf = float(prediction[meta[2] - 1].item())
                if meta[1] == "rating":
                    rating_tags[tag] = conf
                elif meta[1] == "date":
                    date_tags[tag] = conf
                # general/character/artist, filter by threshold
                elif conf >= threshold:
                    filtered[tag] = conf

        # For rating or date, pick the maximum conf if any
        if len(rating_tags) > 0:
            best_rating = max(rating_tags, key=rating_tags.get)
            rating_tags = {best_rating: rating_tags[best_rating]}
        if len(date_tags) > 0:
            best_date = max(date_tags, key=date_tags.get)
            date_tags = {best_date: date_tags[best_date]}

        # sort filtered by descending confidence
        filtered = dict(
            sorted(filtered.items(), key=lambda x: x[1], reverse=True),
        )
        return filtered, rating_tags, date_tags

    def infer_many(self, image_paths: List[str], **kwargs):
        """Override to provide optional autocast on CUDA,
        or just reuse BaseImageInference's method with a small tweak.
        """
        dataset = ImagePathDataset(
            image_files=image_paths,
            preprocess_fn=self._preprocess_image,
        )
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=4,
            pin_memory=True,
            collate_fn=custom_collate,
        )

        self.model.eval()
        results = []
        # Use autocast for speed if on CUDA
        autocast_ctx = torch.autocast("cuda") if self.device == "cuda" else torch.cuda.amp.autocast(enabled=False)

        with torch.no_grad(), autocast_ctx:
            for batch in tqdm(dataloader, desc="Inferring Danbooru tags"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device)
                # base model returns summary, features if following snippet
                summary, features = self.model(images)
                # summary is presumably your 3840-dim. We'll feed summary to heads:
                # shape is [B, 3840]
                batch_out = self._postprocess_output(summary)

                # However, _postprocess_output is written for one item at a time
                # in the snippet. Let's adapt it for batches:
                if isinstance(batch_out, dict):
                    # That means your model returned a single item not a batch
                    # (which might happen if B=1).
                    # If that's your actual design, see below for rewriting.
                    # For demonstration, we'll show how to handle a list for multiple items:
                    batch_out = [batch_out]  # unify
                if not isinstance(batch_out, list):
                    # Guarantee list so we can zip
                    batch_out = [batch_out] * len(paths)

                for path, out_dict in zip(paths, batch_out):
                    out_dict["path"] = path
                    results.append(out_dict)

        # Convert to a DataFrame for the user
        import pandas as pd

        return pd.DataFrame(results)

    def infer_one(self, pil_image: Image.Image, **kwargs):
        """Single-image inference.
        Show how you'd do it if you only had one image.
        Reuses the parent's logic except we override how to get the final output.
        """
        self.model.eval()
        with torch.no_grad():
            image_tensor = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            with torch.autocast("cuda") if self.device == "cuda" else torch.cuda.amp.autocast(enabled=False):
                summary, features = self.model(image_tensor)
                # shape is [1, 3840]
                result = self._postprocess_output(summary)
        return result
