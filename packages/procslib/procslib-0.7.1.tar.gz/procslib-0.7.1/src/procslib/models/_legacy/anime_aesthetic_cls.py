# Classifier variant of the convnext anime aesthetic model; predicts categories (worst -> best) for anime images instead of a continuous score.


import torch
from PIL import Image
from torchvision import transforms
from transformers import ConvNextV2ForImageClassification

# src/procslib/models/anime_aesthetic_cls.py
from .base_inference import BaseImageInference


class AnimeAestheticClassificationInference(BaseImageInference):
    IMG_SIZE = 768

    def __init__(self, checkpoint_path: str, num_classes: int = 5, device: str = "cuda", batch_size: int = 32):
        super().__init__(device=device, batch_size=batch_size)
        self.num_classes = num_classes
        self._load_model(checkpoint_path)
        self.model.eval()

        # Predefine the transform once
        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Resize((self.IMG_SIZE, self.IMG_SIZE), antialias=True),
                transforms.CenterCrop(self.IMG_SIZE),
            ],
        )

    def _load_model(self, checkpoint_path: str):
        model = ConvNextV2ForImageClassification.from_pretrained("facebook/convnextv2-base-22k-384")
        model.classifier = torch.nn.Linear(model.classifier.in_features, self.num_classes)

        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        state_dict = checkpoint["state_dict"]

        # Adjust state dict keys for compatibility
        new_state_dict = {k.replace("net.", ""): v for k, v in state_dict.items()}
        model.load_state_dict(new_state_dict, strict=False)

        model.to(self.device)
        self.model = model

    def _preprocess_image(self, pil_image):
        pil_image = pil_image.convert("RGB")
        return self.transform(pil_image)

    def _postprocess_output(self, logits: torch.Tensor):
        probabilities = torch.softmax(logits, dim=1)
        predicted_classes = torch.argmax(probabilities, dim=1).tolist()
        return predicted_classes

    def predict_proba(self, pil_images):
        self.model.eval()
        with torch.no_grad():
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            output = self.model(images)
            probabilities = torch.softmax(output.logits, dim=1)
        return probabilities.cpu().numpy()

    def extract_features(self, pil_image):
        """Extract features from the penultimate layer."""
        self.model.eval()
        with torch.no_grad():
            image = self._preprocess_image(pil_image).unsqueeze(0).to(self.device)
            outputs = self.model.convnext(image)
            # Assuming outputs: (last_hidden_state, pooled_output)
            pooled_output = outputs[1]
        return pooled_output.squeeze().cpu().numpy()

    def extract_features_batch(self, pil_images):
        self.model.eval()
        with torch.no_grad():
            images = torch.stack([self._preprocess_image(img) for img in pil_images]).to(self.device)
            outputs = self.model.convnext(images)
            pooled_output = outputs[1]
        return pooled_output.cpu().numpy()


def custom_collate(batch):
    """Custom collate function to filter out None values."""
    batch = [item for item in batch if item is not None]
    if not batch:
        return None  # Return None if the entire batch is invalid
    return torch.utils.data.dataloader.default_collate(batch)


# sample usage (e.g. in a demo script, src/procslib/demo.py)
# from .models.anime_aesthetic_cls import AnimeAestheticClassificationInference
import glob


def demo():
    model_checkpoint = "/rmd/yada/checkpoints/aesthetics_cls_6k-mix_soft-firebrand-34/e9_acc0.8120.ckpt"
    folder_to_infer = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    image_paths = glob.glob(folder_to_infer + "/*.jpg")

    inference = AnimeAestheticClassificationInference(
        checkpoint_path=model_checkpoint,
        num_classes=5,
        device="cuda",
        batch_size=32,
    )

    # Single image inference
    img = Image.open(image_paths[0])
    print("Single Image Prediction:", inference.infer_one(img))

    # Batch inference
    batch_images = [Image.open(p) for p in image_paths[:8]]
    print("Batch Predictions:", inference.infer_batch(batch_images))

    # Many images inference (DataFrame)
    results_df = inference.infer_many(image_paths)
    results_df.to_csv("classification_results.csv", index=False)
    print("Inference completed. Results saved to 'classification_results.csv'.")


if __name__ == "__main__":
    demo()
