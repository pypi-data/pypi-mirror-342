# src/procslib/models/opencv_metrics_inference.py
import glob
from concurrent.futures import ProcessPoolExecutor

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from skimage.feature import local_binary_pattern
from tqdm.auto import tqdm

from .base_inference import BaseImageInference


def calculate_dynamic_range(gray_image):
    # Histogram of the grayscale image
    hist, bin_edges = np.histogram(gray_image, bins=256, range=(0, 255))

    # Calculate cumulative distribution function (CDF)
    cdf = hist.cumsum()

    # Normalize CDF
    cdf_normalized = cdf * hist.max() / cdf.max()

    # Dynamic range: difference between the highest and lowest intensities
    low_idx = np.searchsorted(cdf_normalized, cdf_normalized.max() * 0.05)
    high_idx = np.searchsorted(cdf_normalized, cdf_normalized.max() * 0.95)

    average_dynamic_range = high_idx - low_idx
    return float(average_dynamic_range)


def analyze_image(image: np.ndarray):
    # Ensure the image is in the correct format
    if len(image.shape) == 3 and image.shape[2] == 3:  # Color image
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        saturation = np.mean(hsv[:, :, 1])  # S channel represents saturation
    else:
        hsv = None
        saturation = 0.0  # No saturation in grayscale images

    # Convert to grayscale if necessary
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Edge detection
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])

    # Laplacian variance (focus measure)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    focus_measure = laplacian.var()

    # Texture analysis using Local Binary Patterns (LBP)
    radius = 1  # LBP radius
    n_points = 8 * radius  # Number of points to consider
    lbp = local_binary_pattern(gray, n_points, radius, method="uniform")
    texture_score = np.var(lbp)

    # Noise estimation using a high-pass filter
    high_pass = cv2.Laplacian(gray, cv2.CV_64F)
    noise_level = np.std(high_pass)

    # Calculate contrast
    contrast = gray.std()  # Standard deviation of the grayscale image

    # Calculate brightness (mean of the grayscale image)
    brightness = gray.mean()

    # Calculate dynamic range
    avg_dynamic_range = calculate_dynamic_range(gray)

    return {
        "edge_density": float(edge_density),
        "focus_measure": float(focus_measure),
        "texture_score": float(texture_score),
        "noise_level": float(noise_level),
        "saturation": float(saturation),
        "contrast": float(contrast),
        "brightness": float(brightness),
        "avg_dynamic_range": float(avg_dynamic_range),
    }


class OpenCVMetricsInference(BaseImageInference):
    """A class to calculate image metrics using OpenCV and NumPy,
    parallelized with ProcessPoolExecutor.
    """

    def __init__(self, device="cpu", batch_size=32):
        if device != "cpu":
            print("Warning: OpenCVMetricsInference does not use GPU, setting device to 'cpu'.")
        # device is irrelevant here since no GPU ops
        super().__init__(device=device, batch_size=batch_size)

    def _load_model(self, checkpoint_path: str = None):
        # No model to load
        pass

    def _preprocess_image(self, pil_image: Image.Image):
        # Convert PIL to a NumPy array (RGB)
        np_image = np.array(pil_image.convert("RGB"))
        return np_image

    def _postprocess_output(self, metrics):
        return metrics

    def infer_one(self, pil_image: Image.Image):
        np_image = self._preprocess_image(pil_image)
        metrics = analyze_image(np_image)
        return metrics

    def infer_batch(self, pil_images: list[Image.Image]):
        results = []
        for img in pil_images:
            np_image = self._preprocess_image(img)
            metrics = analyze_image(np_image)
            results.append(metrics)
        return results

    def _process_one_image(self, path: str):
        # This method is used by the ProcessPoolExecutor to process a single image.
        # We open the image, run infer_one, and return the results with filename included.
        try:
            pil_image = Image.open(path)
            metrics = self.infer_one(pil_image)
            metrics["path"] = path
            return metrics
        except Exception as e:
            # In case of error, return a placeholder with error info
            return {"path": path, "error": str(e)}

    def infer_many(self, image_paths: list[str], batch_size: int = 24):
        results = []
        # Using ProcessPoolExecutor to parallelize the work.
        with ProcessPoolExecutor(max_workers=batch_size) as executor:
            # executor.map returns results in the order of the input iterable
            # We can wrap it in tqdm for a progress bar
            for metric in tqdm(
                executor.map(self._process_one_image, image_paths),
                total=len(image_paths),
                desc="Calculating OpenCV metrics",
            ):
                results.append(metric)
        return pd.DataFrame(results)


# Demo usage
def demo_cv2_wrapper():
    folder_to_infer = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    image_paths = glob.glob(folder_to_infer + "/*.jpg")
    inference = OpenCVMetricsInference(batch_size=2)

    # Single image
    img = Image.open(image_paths[0])
    print("Single image metrics:", inference.infer_one(img))

    # Batch
    imgs = [Image.open(p) for p in image_paths[:4]]  # Just a few for batch
    print("Batch metrics:", inference.infer_batch(imgs))

    # Many images (parallelized with ProcessPoolExecutor)
    df = inference.infer_many(image_paths)
    df.to_csv("cv2_scores.csv", index=False)
    print("Inference completed. Results saved to 'cv2_scores.csv'.")


if __name__ == "__main__":
    demo_cv2_wrapper()
