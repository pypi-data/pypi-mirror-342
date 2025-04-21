import os

import torch
from PIL import Image
from torch.utils.data import Dataset
from transformers import CLIPProcessor


class ImageDataset(Dataset):
    def __init__(self, root_dir: str, image_paths: list[str], processor: CLIPProcessor):
        self.root_dir = root_dir
        self.image_paths = image_paths
        self.processor = processor

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        rel_path = self.image_paths[idx]
        img_path = os.path.join(self.root_dir, rel_path)
        try:
            image = Image.open(img_path).convert("RGB")
            image_proc = torch.from_numpy(self.processor.image_processor(image).pixel_values[0])
        except Exception as e:
            print(f"Error loading image {rel_path}: {e}")
            image_proc = torch.zeros(3, 224, 224, dtype=torch.float32)

        return image_proc, rel_path


# for downloading models from huggingface hub
from pathlib import Path

import torch.nn.functional as F
from huggingface_hub import hf_hub_download
from torch import nn


class MLP(nn.Module):
    def __init__(self, input_size, xcol="emb", ycol="avg_rating"):
        super().__init__()
        self.input_size = input_size
        self.xcol = xcol
        self.ycol = ycol
        self.layers = nn.Sequential(
            nn.Linear(self.input_size, 1024),
            # nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            # nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            # nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            # nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.layers(x)

    def training_step(self, batch, batch_idx):
        x = batch[self.xcol]
        y = batch[self.ycol].reshape(-1, 1)
        x_hat = self.layers(x)
        loss = F.mse_loss(x_hat, y)
        return loss

    def validation_step(self, batch, batch_idx):
        x = batch[self.xcol]
        y = batch[self.ycol].reshape(-1, 1)
        x_hat = self.layers(x)
        loss = F.mse_loss(x_hat, y)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


def get_mlp_model(input_source):
    """Load a pre-trained MLP model from either a local path or a huggingface hub repo id.
    MLP is in the format of https://github.com/christophschuhmann/improved-aesthetic-predictor

    :param input_source: either a local path to a model, or a huggingface hub repo id
        (e.g. "openai/clip-vit-large-patch14")
    :return:
    """
    try:
        print(f"Attempting to load model from Hugging Face Hub: {input_source}")
        model_path = Path(hf_hub_download(repo_id=input_source, filename="model.pth"))
    except Exception as e:
        print(f"Failed to load from Hugging Face Hub, trying local path. Error: {e}")
        model_path = input_source

    model = MLP(768)
    s = torch.load(model_path, map_location=torch.device("cuda"))
    model.load_state_dict(s)
    model.to("cuda")
    model.eval()
    return model


from typing import List

import h5py
import unibox as ub
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import CLIPModel, CLIPProcessor

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def normalized(a, axis=-1, order=2):
    import numpy as np  # pylint: disable=import-outside-toplevel

    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def tensor_to_float(tensor, precision=5):
    # Move tensor to CPU if it's on GPU, convert to numpy array, and get the first element
    value = tensor.cpu().detach().numpy().item()

    # Format the value to a float with specified precision
    formatted_value = round(value, precision)

    return formatted_value


class CachedClipScoreCalculator:
    def __init__(
        self,
        prompts_list: list[str],
        h5_path: str = None,
        model_id: str = "openai/clip-vit-large-patch14",
    ):
        """:param prompts_list: ["a manga", "a poster", "a photo"]
        :param h5_path: "features.h5", path to the HDF5 image feature store
        :param model_id: Huggingface model identifier
        """
        self.logger = ub.UniLogger()
        self.prompts_list = prompts_list
        self.h5_path = h5_path

        # Initialize CLIP model and processor
        self.model = CLIPModel.from_pretrained(model_id).cuda()
        self.processor = CLIPProcessor.from_pretrained(model_id)

        # Process text inputs
        text_inputs = self.processor.tokenizer(prompts_list, padding="max_length", return_tensors="pt").to("cuda")
        text_features = self.model.get_text_features(**text_inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
        self.text_features = text_features.t()

        # placeholder for image features
        self.image_features = {}

    def _get_relative_path(self, path, root_dir):
        return str(Path(path).relative_to(root_dir).as_posix())

    def load_all_features(self):
        """Loads all features from the h5 file into self.image_features.
        Assumes that self.h5_path is valid and points to an existing h5 file.
        """
        if not self.h5_path or not os.path.exists(self.h5_path):
            print("h5 file path is not set or the file does not exist.")
            return

        with h5py.File(self.h5_path, "r") as features_file:
            for relative_path in tqdm(features_file.keys(), desc="Loading all features"):
                self.image_features[relative_path] = features_file[relative_path][()]

    def _get_images_to_process(self, root_dir: str, image_paths: list) -> list[str]:
        """Updates self.image_features with features in h5 file.
        :param root_dir:
        :param image_paths:
        :return: a list of images that are not in the provided h5 file
        """
        images_to_process = []

        if self.h5_path and os.path.exists(self.h5_path):
            with h5py.File(self.h5_path, "r") as features_file:
                for path in tqdm(image_paths, desc="Loading features"):
                    relative_path = self._get_relative_path(path, root_dir)
                    if relative_path in features_file:
                        self.image_features[relative_path] = features_file[relative_path][()]
                    else:
                        images_to_process.append(path)
        else:
            # If the HDF5 file does not exist, all images need to be processed
            images_to_process = image_paths

            # Create the HDF5 file's parent directory if it does not exist
            dir_name = os.path.dirname(self.h5_path)
            if dir_name:  # Check if the directory name is not empty
                os.makedirs(dir_name, exist_ok=True)

        return images_to_process

    def _cache_images_batched(self, root_dir: str, image_batch, paths: list, features_file):
        image_batch = image_batch.cuda()
        image_features = self.model.get_image_features(pixel_values=image_batch)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)

        for path, features in zip(paths, image_features.cpu().numpy()):
            relative_path = self._get_relative_path(path, root_dir)
            # Store raw image features, not the final scores
            self.image_features[relative_path] = features
            features_file.create_dataset(relative_path, data=features)

    def cache_images(self, root_dir: str, images_to_process: list[str]) -> None:
        """Calculate clip embeddings for new images and update the precomputed features."""
        if images_to_process:
            dataset = ImageDataset(root_dir, images_to_process, self.processor)
            dataloader = DataLoader(dataset, batch_size=64, num_workers=4)
            with torch.no_grad(), h5py.File(self.h5_path, "a") as features_file:
                for image_batch, paths in tqdm(dataloader, desc="Processing images"):
                    self._cache_images_batched(root_dir, image_batch, paths, features_file)

        # image features is modified in-place

    def _compute_scores_from_feature(self, mlp_configs_list: List) -> dict:
        """Calculate clip scores and mlp scores for each image, and return a dict of scores

        :param mlp_configs_list: [(mlp_model, key_name), ...]
        :return: scores: {path: {"clip_scores": {prompt: score, ...}, "mlp_key_name": score, ...}, ...}
        """
        scores = {}
        with torch.no_grad():
            for path, image_feature in tqdm(self.image_features.items(), desc="Computing scores"):
                image_feature_tensor = torch.tensor(image_feature).unsqueeze(0).to("cuda")

                # Compute CLIP scores
                image_scores = (
                    (torch.matmul(image_feature_tensor, self.text_features) * self.model.logit_scale.exp())
                    .cpu()
                    .numpy()[0]
                )
                clip_scores = {prompt: round(float(score), 5) for prompt, score in zip(self.prompts_list, image_scores)}

                # Initialize the scores dictionary for this path
                scores[path] = {"clip_scores": clip_scores}

                # Compute scores for each provided MLP model
                for mlp_model, key_name in mlp_configs_list:
                    normalized_feature = normalized(image_feature_tensor.cpu().detach().numpy())
                    model_score_tensor = mlp_model(
                        torch.from_numpy(normalized_feature).to("cuda").type(torch.cuda.FloatTensor),
                    )
                    model_score = tensor_to_float(model_score_tensor)
                    scores[path][key_name] = model_score

        return scores

    def calculate_scores(self, root_dir: str, mlp_configs_list: List):
        """Driver function to calculate clip scores and mlp scores for each image

        :param root_dir: image root directory
        :param mlp_configs_list: [(mlp_model, key_name), ...]
        :return:
        """
        image_paths = ub.traverses(root_dir, include_extensions=ub.IMG_FILES)
        images_to_process = self._get_images_to_process(root_dir, image_paths)

        todo_count = len(images_to_process)
        found_count = len(image_paths) - todo_count
        self.logger.info(f"Processing images: total {len(image_paths)} | found {found_count} | new {todo_count}")
        self.cache_images(root_dir, images_to_process)

        scores = self._compute_scores_from_feature(mlp_configs_list)
        return scores


def score_diver():
    root_dir = r"E:\_benchmark\1k"
    prompts_list = ub.loads(r"D:\CSC\pixai-aesthetic\clip_prompts_list_pixiv.txt")

    calculator = CachedClipScoreCalculator(
        prompts_list,
        h5_path="features.h5",
        model_id="openai/clip-vit-large-patch14",
    )

    # Initialize MLP models
    clip_mlp = get_mlp_model("kiriyamaX/clip-aesthetic")
    twitter_mlp = get_mlp_model("kiriyamaX/twitter-aesthetic-e20")
    mlp_configs = [(clip_mlp, "clip_aesthetic"), (twitter_mlp, "twitter_aesthetic")]

    # Calculate scores
    scores = calculator.calculate_scores(root_dir, mlp_configs)

    # Output results
    ub.saves(scores, "scores_debug.json")
    print("done")


def rerun_driver():
    clip_mlp = get_mlp_model("kiriyamaX/clip-aesthetic")
    mlp_configs = [(clip_mlp, "clip_aesthetic")]
    additional_tags = ub.loads("s3://bucket-external/misc/yada_store/configs/clip_prompts_list_full_v2.txt")
    local_path = "/home/ubuntu/dev/twitter-data-process/yada/0.h5"
    calc = CachedClipScoreCalculator(prompts_list=additional_tags, h5_path=local_path)
    calc.load_all_features()
    scores = calc._compute_scores_from_feature(mlp_configs)

    print("D")


if __name__ == "__main__":
    rerun_driver()
    # score_diver()
