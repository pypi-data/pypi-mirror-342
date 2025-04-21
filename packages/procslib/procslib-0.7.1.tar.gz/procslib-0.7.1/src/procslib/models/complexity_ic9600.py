# src/procslib/models/ic9600_inference.py
import glob

import pandas as pd
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import torchvision
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm.auto import tqdm

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate

# ========= Model =========


class slam(nn.Module):
    def __init__(self, spatial_dim):
        super(slam, self).__init__()
        self.spatial_dim = spatial_dim
        self.linear = nn.Sequential(
            nn.Linear(spatial_dim**2, 512),
            nn.ReLU(),
            nn.Linear(512, 1),
            nn.Sigmoid(),
        )

    def forward(self, feature):
        n, c, h, w = feature.shape
        if h != self.spatial_dim:
            x = F.interpolate(feature, size=(self.spatial_dim, self.spatial_dim), mode="bilinear", align_corners=True)
        else:
            x = feature

        x = x.view(n, c, -1)
        x = self.linear(x)
        x = x.unsqueeze(dim=3)
        out = x.expand_as(feature) * feature

        return out


class to_map(nn.Module):
    def __init__(self, channels):
        super(to_map, self).__init__()
        self.to_map = nn.Sequential(
            nn.Conv2d(in_channels=channels, out_channels=1, kernel_size=1, stride=1),
            nn.Sigmoid(),
        )

    def forward(self, feature):
        return self.to_map(feature)


class conv_bn_relu(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, padding=1, stride=1):
        super(conv_bn_relu, self).__init__()
        self.conv = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            padding=padding,
            stride=stride,
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


class up_conv_bn_relu(nn.Module):
    def __init__(self, up_size, in_channels, out_channels=64, kernal_size=1, padding=0, stride=1):
        super(up_conv_bn_relu, self).__init__()
        self.upSample = nn.Upsample(size=(up_size, up_size), mode="bilinear", align_corners=True)
        self.conv = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernal_size,
            stride=stride,
            padding=padding,
        )
        self.bn = nn.BatchNorm2d(num_features=out_channels)
        self.act = nn.ReLU()

    def forward(self, x):
        x = self.upSample(x)
        x = self.conv(x)
        x = self.bn(x)
        x = self.act(x)
        return x


class ICNet(nn.Module):
    def __init__(self, is_pretrain=True, size1=512, size2=256):
        super(ICNet, self).__init__()
        resnet18Pretrained1 = torchvision.models.resnet18(pretrained=is_pretrain)
        resnet18Pretrained2 = torchvision.models.resnet18(pretrained=is_pretrain)

        self.size1 = size1
        self.size2 = size2

        ## detail branch
        self.b1_1 = nn.Sequential(*list(resnet18Pretrained1.children())[:5])
        self.b1_1_slam = slam(32)

        self.b1_2 = list(resnet18Pretrained1.children())[5]
        self.b1_2_slam = slam(32)

        ## context branch
        self.b2_1 = nn.Sequential(*list(resnet18Pretrained2.children())[:5])
        self.b2_1_slam = slam(32)

        self.b2_2 = list(resnet18Pretrained2.children())[5]
        self.b2_2_slam = slam(32)

        self.b2_3 = list(resnet18Pretrained2.children())[6]
        self.b2_3_slam = slam(16)

        self.b2_4 = list(resnet18Pretrained2.children())[7]
        self.b2_4_slam = slam(8)

        ## upsample
        self.upsize = size1 // 8
        self.up1 = up_conv_bn_relu(up_size=self.upsize, in_channels=128, out_channels=256)
        self.up2 = up_conv_bn_relu(up_size=self.upsize, in_channels=512, out_channels=256)

        ## map prediction head
        self.to_map_f = conv_bn_relu(256 * 2, 256 * 2)
        self.to_map_f_slam = slam(32)
        self.to_map = to_map(256 * 2)

        ## score prediction head
        self.to_score_f = conv_bn_relu(256 * 2, 256 * 2)
        self.to_score_f_slam = slam(32)
        self.head = nn.Sequential(
            nn.Linear(256 * 2, 512),
            nn.ReLU(),
            nn.Linear(512, 1),
            nn.Sigmoid(),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

    def forward(self, x1):
        assert x1.shape[2] == x1.shape[3] == self.size1
        x2 = F.interpolate(x1, size=(self.size2, self.size2), mode="bilinear", align_corners=True)

        x1 = self.b1_2_slam(self.b1_2(self.b1_1_slam(self.b1_1(x1))))
        x2 = self.b2_2_slam(self.b2_2(self.b2_1_slam(self.b2_1(x2))))
        x2 = self.b2_4_slam(self.b2_4(self.b2_3_slam(self.b2_3(x2))))

        x1 = self.up1(x1)
        x2 = self.up2(x2)
        x_cat = torch.cat((x1, x2), dim=1)

        cly_map = self.to_map(self.to_map_f_slam(self.to_map_f(x_cat)))

        score_feature = self.to_score_f_slam(self.to_score_f(x_cat))
        score_feature = self.avgpool(score_feature)
        score_feature = score_feature.squeeze()
        score = self.head(score_feature)
        score = score.squeeze()

        return score, cly_map


class InferenceICNet(pl.LightningModule):
    def __init__(self, model_path):
        super().__init__()
        self.model = ICNet()
        state_dict = torch.load(model_path, map_location="cpu")
        self.model.load_state_dict(state_dict, strict=True)
        self.model.eval()

    def forward(self, image):
        with torch.no_grad():
            score, cly_map = self.model(image)
        return score

    def predict_score(self, pil_image: Image.Image, device: str = "cuda"):
        inference_transform = transforms.Compose(
            [
                transforms.Resize((512, 512)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ],
        )
        image = inference_transform(pil_image).unsqueeze(0).to(device)
        score = self.forward(image)
        return score.item()


class IC9600Inference(BaseImageInference):
    """A wrapper class for IC9600 inference."""

    def __init__(self, model_path: str, device="cuda", batch_size=32):
        super().__init__(device=device, batch_size=batch_size)
        self.model = InferenceICNet(model_path).to(self.device)
        self.model.eval()

        # Define a transform for single/batch preprocessing
        self.transform = transforms.Compose(
            [
                transforms.Resize((512, 512)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ],
        )

    def _load_model(self, checkpoint_path: str):
        # The model is loaded in __init__ directly.
        pass

    def _preprocess_image(self, pil_image: Image.Image):
        return self.transform(pil_image.convert("RGB"))

    def _postprocess_output(self, logits: torch.Tensor):
        # Logits here is actually a score (float)
        return logits.item()

    def infer_one(self, pil_image: Image.Image):
        image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            score = self.model(image)
        return score.item()

    def infer_batch(self, pil_images: list[Image.Image]):
        images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
        with torch.no_grad():
            scores = self.model(images)  # shape: [B]
        return scores.cpu().tolist()

    def infer_many(self, image_paths: list[str]):
        dataset = ImagePathDataset(image_paths, preprocess_fn=self._preprocess_image)
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=8,
            pin_memory=True,
            collate_fn=custom_collate,
        )
        results = []
        self.model.eval()
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Inferring IC9600"):
                if batch is None:
                    continue
                images, paths = batch
                images = images.to(self.device)
                scores = self.model(images)
                scores = scores.cpu().tolist()
                for path, score in zip(paths, scores):
                    results.append({"path": path, "ic9600_score": score})
        return pd.DataFrame(results)


# Demo usage
def demo_ic9600():
    # Download model weights if needed and specify the model_path
    model_path = "/rmd/yada/model_weights/complexity_ic9600_ck.pth"  # Update with a correct path
    folder_to_infer = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    image_paths = glob.glob(folder_to_infer + "/*.jpg")

    inference = IC9600Inference(model_path=model_path, device="cuda", batch_size=32)

    img = Image.open(image_paths[0])
    print("Single image IC9600 score:", inference.infer_one(img))

    # Batch inference
    imgs = [Image.open(p) for p in image_paths]
    print("Batch IC9600 scores:", inference.infer_batch(imgs))

    # Many images inference
    df = inference.infer_many(image_paths)
    df.to_csv("complexity_scores.csv", index=False)
    print("Inference completed. Results saved to 'complexity_scores.csv'.")


if __name__ == "__main__":
    demo_ic9600()
