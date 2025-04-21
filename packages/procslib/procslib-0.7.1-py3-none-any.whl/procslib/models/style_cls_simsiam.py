# src/procslib/models/style_cls_simsiam.py
import glob
from typing import List

import pandas as pd
import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm.auto import tqdm

# Assuming convnext_v2 and other dependencies are resolved and in the path.
from ._convnext_v2 import convnextv2  # Make sure convnext_v2 is defined or imported
from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


class AttentionPoolNoPos2d(nn.Module):
    def __init__(
        self,
        in_features: int,
        out_features: int = None,
        embed_dim: int = None,
        num_heads: int = 4,
        qkv_bias: bool = True,
    ):
        super().__init__()
        embed_dim = embed_dim or in_features
        out_features = out_features or in_features
        assert embed_dim % num_heads == 0
        self.qkv = nn.Linear(in_features, embed_dim * 3, bias=qkv_bias)
        self.proj = nn.Linear(embed_dim, out_features)
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = self.head_dim**-0.5
        nn.init.zeros_(self.qkv.bias)

    def forward(self, x: torch.Tensor):
        B, _, H, W = x.shape
        N = H * W
        x = x.reshape(B, -1, N).permute(0, 2, 1)
        x = torch.cat([x.mean(1, keepdim=True), x], dim=1)

        x = self.qkv(x).reshape(B, N + 1, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = x[0], x[1], x[2]
        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)

        x = (attn @ v).transpose(1, 2).reshape(B, N + 1, -1)
        x = self.proj(x)
        return x[:, 0]


class StyleEmbdModel(nn.Module):
    def __init__(self, n_style_dim):
        super().__init__()
        self.n_style_dim = n_style_dim
        self.net = convnextv2("tiny", in_chans=3, num_classes=1, drop_path_rate=0)
        del self.net.norm
        del self.net.head
        self.pool = AttentionPoolNoPos2d(768, 768, num_heads=8)
        self.mlp = nn.Sequential(
            nn.Linear(768, 2048),
            nn.GELU(),
            nn.Linear(2048, 256),
        )
        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.trunc_normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor):
        N = x.size(0)
        h = self.net.forward_backbone(x)
        h = self.pool(h).view(N, -1)
        h = self.mlp(h)
        return h


class StyleClassifier(nn.Module):
    def __init__(self, n_style_dim, n_style):
        super().__init__()
        self.n_style_dim = n_style_dim
        self.n_style = n_style
        self.last_layer = nn.utils.weight_norm(nn.Linear(n_style_dim, n_style, bias=False))
        self.last_layer.weight_g.data.fill_(1)
        self.last_layer.weight_g.requires_grad = False

    def forward(self, x: torch.Tensor):
        return self.last_layer(x)


class StyleDinoModel(nn.Module):
    def __init__(self, n_style=1024):
        super().__init__()
        self.embd = StyleEmbdModel(256)
        self.head = StyleClassifier(256, n_style)

    def forward(self, x):
        h = self.embd(x)
        m, s = torch.std_mean(h.detach(), dim=0)
        h = self.head(h)
        return h, m, s


# SimSiam model definition
class projection_MLP(nn.Module):
    def __init__(self, in_dim, hidden_dim=2048, out_dim=2048):
        super().__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
        )
        self.layer2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
        )
        self.layer3 = nn.Sequential(
            nn.Linear(hidden_dim, out_dim),
            nn.BatchNorm1d(out_dim),
        )
        self.num_layers = 3

    def set_layers(self, num_layers):
        self.num_layers = num_layers

    def forward(self, x):
        if self.num_layers == 3:
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
        elif self.num_layers == 2:
            x = self.layer1(x)
            x = self.layer3(x)
        else:
            raise Exception
        return x


class prediction_MLP(nn.Module):
    def __init__(self, in_dim=2048, hidden_dim=512, out_dim=2048):
        super().__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
        )
        self.layer2 = nn.Linear(hidden_dim, out_dim)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        return x


class SimSiam(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = convnextv2("tiny", in_chans=3, num_classes=1, drop_path_rate=0)
        del self.backbone.norm
        del self.backbone.head
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.projector = projection_MLP(768, hidden_dim=2048, out_dim=256)
        self.predictor = prediction_MLP(256, hidden_dim=64, out_dim=256)

    def forward_encoder(self, x):
        N = x.size(0)
        h = self.backbone.forward_backbone(x)
        h = self.pool(h).view(N, -1)
        h = self.projector(h)
        return h

    def forward_predictor(self, x):
        return self.predictor(x)

    def forward(self, x):
        z = self.forward_encoder(x)
        p = self.forward_predictor(z)
        return z, p


def load_simsiam_model(weight_path: str):
    model = SimSiam()
    sd = torch.load(weight_path, map_location="cpu")
    sd2 = {k.replace("module.", ""): v for k, v in sd.items() if k.startswith("module.")}
    model.load_state_dict(sd2, strict=True)
    return model


class StyleSimsiamInference(BaseImageInference):
    """Inference class for StyleSimsiam model to get embeddings from images."""

    def __init__(self, weight_path: str, device="cuda", batch_size=32):
        super().__init__(device=device, batch_size=batch_size)
        self.model = load_simsiam_model(weight_path)
        self.model.eval()
        self.model.to(self.device)

        self.transform = transforms.Compose(
            [
                transforms.Resize((640, 640)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
            ],
        )

    def _load_model(self, checkpoint_path: str):
        # This class loads model in constructor directly.
        pass

    def _preprocess_image(self, pil_image: Image.Image):
        return self.transform(pil_image.convert("RGB"))

    def _postprocess_output(self, logits: torch.Tensor):
        # For embeddings, just return the tensor as numpy.
        return logits.cpu().numpy()

    def infer_one(self, pil_image: Image.Image):
        with torch.no_grad():
            image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            emb = self.model.forward_encoder(image)
        return emb.cpu().numpy()[0]

    def infer_batch(self, pil_images: List[Image.Image]):
        with torch.no_grad():
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            emb = self.model.forward_encoder(images)
        return emb.cpu().numpy()

    def infer_many(self, image_paths: List[str]):
        """Infer for many images using a DataLoader."""
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
            for batch in tqdm(dataloader, desc="Inferring images"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device)
                embeddings = self.model.forward_encoder(images)
                embeddings = embeddings.cpu().numpy()
                for path, emb in zip(paths, embeddings):
                    results.append({"path": path, "embedding": emb.tolist()})

        return pd.DataFrame(results)


def demo():
    model_path = "/rmd/yada/model_weights/style_emb/style_simsiam_v1-ep39.ckpt"
    folder_path = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    output_csv = "simsiam_inference_results.csv"

    # Initialize the StyleSimsiamInference class
    inference = StyleSimsiamInference(weight_path=model_path, device="cuda", batch_size=32)

    # Collect image paths from the specified folder
    image_paths = glob.glob(folder_path + "/*.jpg")

    # Single Image Inference
    if len(image_paths) > 0:
        img = Image.open(image_paths[0])
        single_embedding = inference.infer_one(img)
        print("Single Image Embedding:", single_embedding)

    # Batch Inference (first 8 images)
    batch_images = [Image.open(p) for p in image_paths[:8]]
    batch_embeddings = inference.infer_batch(batch_images)
    print("Batch Embeddings Shape:", batch_embeddings.shape)

    # Many images inference using DataLoader
    results_df = inference.infer_many(image_paths)
    results_df.to_csv(output_csv, index=False)
    print(f"Inference completed. Results saved to '{output_csv}'.")
