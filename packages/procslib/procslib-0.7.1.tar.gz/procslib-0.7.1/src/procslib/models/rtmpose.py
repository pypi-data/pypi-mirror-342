"""Using RTMPose to estimate the body keypoints in images, as more body parts = more anatomy shown.
Code adapted from /rmt/larry/code/diffuser_xl_train/data_clean_scripts/rtmpose/main.py

Using RTMPose:

1. determine your cudnn environment: `ls /root/miniconda3/lib/python3.10/site-packages/nvidia/cudnn/lib/`

    - see: https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html#requirements

    - if there IS `libcudnn.so.9`, then use the latest onnxruntime-gpu: >= 1.20.x

    - if there is NO `libcudnn.so.9`, but there is `libcudnn.so.8`, then use onnxruntime-gpu==1.18.0

    - otherwise, install cuDNN

"""

from typing import List, Tuple

import cv2
import numpy as np
import onnxruntime as ort
import pandas as pd
from PIL import Image
from tqdm.auto import tqdm

from .base_inference import BaseImageInference


class RTMPoseInference(BaseImageInference):
    """Inference class for RTMPose models.
    https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose
    """

    def __init__(self, onnx_file: str, device: str = "cpu", batch_size: int = 32, bone_threshold: float = 0.3):
        super().__init__(device=device, batch_size=batch_size)
        self.onnx_file = onnx_file
        self.bone_threshold = bone_threshold
        self._load_model(onnx_file)

    def _load_model(self, onnx_file: str):
        """Load the ONNX model."""
        providers = ["CPUExecutionProvider"] if self.device == "cpu" else ["CUDAExecutionProvider"]
        self.model = ort.InferenceSession(onnx_file, providers=providers)

    def _preprocess_image(self, pil_image: Image.Image) -> np.ndarray:
        """Preprocess a single PIL image into the format required by the model."""
        img = np.array(pil_image)
        input_size = self.model.get_inputs()[0].shape[2:]
        resized_img, center, scale = self.preprocess(img, input_size)
        self.current_center = center
        self.current_scale = scale
        return resized_img.transpose(2, 0, 1).astype(np.float32)

    def _postprocess_output(self, logits: List[np.ndarray]) -> dict:
        """Postprocess the raw logits from the model into desired predictions."""
        simcc_x, simcc_y = logits
        keypoints, scores = self.decode(simcc_x, simcc_y, simcc_split_ratio=2.0)
        keypoints = (
            keypoints / self.model_input_size * self.current_scale + self.current_center - self.current_scale / 2
        )
        return {"keypoints": keypoints, "scores": scores}

    def preprocess(self, img: np.ndarray, input_size: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Preprocess the input image for inference."""
        img_shape = img.shape[:2]
        bbox = np.array([0, 0, img_shape[1], img_shape[0]])
        center, scale = self.bbox_xyxy2cs(bbox, padding=1.25)
        resized_img, scale = self.top_down_affine(input_size, scale, center, img)
        mean = np.array([123.675, 116.28, 103.53])
        std = np.array([58.395, 57.12, 57.375])
        resized_img = (resized_img - mean) / std
        return resized_img, center, scale

    def bbox_xyxy2cs(self, bbox: np.ndarray, padding: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        x1, y1, x2, y2 = bbox
        center = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
        scale = np.array([(x2 - x1) * padding, (y2 - y1) * padding])
        return center, scale

    def top_down_affine(
        self,
        input_size: Tuple[int, int],
        scale: np.ndarray,
        center: np.ndarray,
        img: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        warp_size = tuple(map(int, input_size))
        warp_mat = self.get_warp_matrix(center, scale, 0, warp_size)
        return cv2.warpAffine(img, warp_mat, warp_size, flags=cv2.INTER_LINEAR), scale

    def decode(
        self,
        simcc_x: np.ndarray,
        simcc_y: np.ndarray,
        simcc_split_ratio: float,
    ) -> Tuple[np.ndarray, np.ndarray]:
        keypoints = np.stack([np.argmax(simcc_x, axis=-1), np.argmax(simcc_y, axis=-1)], axis=-1) / simcc_split_ratio
        scores = np.maximum(simcc_x.max(axis=-1), simcc_y.max(axis=-1))
        return keypoints, scores

    def get_warp_matrix(
        self,
        center: np.ndarray,
        scale: np.ndarray,
        rot: float,
        output_size: Tuple[int, int],
    ) -> np.ndarray:
        """Calculate the affine transformation matrix."""
        src_w = scale[0]
        rot_rad = np.deg2rad(rot)
        src_dir = np.array([0.0, src_w * -0.5]).dot(
            [[np.cos(rot_rad), -np.sin(rot_rad)], [np.sin(rot_rad), np.cos(rot_rad)]],
        )
        dst_dir = np.array([0.0, output_size[0] * -0.5])

        src = np.zeros((3, 2), dtype=np.float32)
        dst = np.zeros((3, 2), dtype=np.float32)
        src[0, :] = center
        src[1, :] = center + src_dir
        src[2, :] = center + np.array([-src_dir[1], src_dir[0]])
        dst[0, :] = [output_size[0] / 2, output_size[1] / 2]
        dst[1, :] = dst[0, :] + dst_dir
        dst[2, :] = dst[0, :] + np.array([-dst_dir[1], dst_dir[0]])

        return cv2.getAffineTransform(src, dst)

    def process_image(self, img_path: str) -> dict:
        """Process a single image for inference."""
        img = cv2.imread(img_path)
        h, w = self.model.get_inputs()[0].shape[2:]
        model_input_size = (w, h)

        resized_img, center, scale = self.preprocess(img, model_input_size)
        outputs = self.model.run(
            None,
            {self.model.get_inputs()[0].name: [resized_img.transpose(2, 0, 1).astype(np.float32)]},
        )
        keypoints, scores = self.decode(outputs[0], outputs[1], simcc_split_ratio=2.0)
        keypoints = keypoints / model_input_size * scale + center - scale / 2
        return {"keypoints": keypoints.tolist(), "scores": scores.tolist(), "bone_count": self.count_bones(scores)}

    def count_bones(self, scores: List[float]) -> int:
        """Count the number of valid bones based on scores and a threshold. (specified during model init)"""
        threshold = self.bone_threshold
        # skeleton = [(15, 13), (13, 11), (16, 14), (14, 12), (11, 12), (5, 11),
        #             (6, 12), (5, 6), (5, 7), (6, 8), (7, 9), (8, 10), (1, 2),
        #             (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]

        skeleton = [
            (15, 13),
            (13, 11),
            (16, 14),
            (14, 12),
            (11, 12),
            (5, 11),
            (6, 12),
            (5, 6),
            (5, 7),
            (6, 8),
            (7, 9),
            (8, 10),
            (1, 2),
            (0, 1),
            (0, 2),
            (1, 3),
            (2, 4),
            (3, 5),
            (4, 6),
            (15, 17),
            (15, 18),
            (15, 19),
            (16, 20),
            (16, 21),
            (16, 22),
            (91, 92),
            (92, 93),
            (93, 94),
            (94, 95),
            (91, 96),
            (96, 97),
            (97, 98),
            (98, 99),
            (91, 100),
            (100, 101),
            (101, 102),
            (102, 103),
            (91, 104),
            (104, 105),
            (105, 106),
            (106, 107),
            (91, 108),
            (108, 109),
            (109, 110),
            (110, 111),
            (112, 113),
            (113, 114),
            (114, 115),
            (115, 116),
            (112, 117),
            (117, 118),
            (118, 119),
            (119, 120),
            (112, 121),
            (121, 122),
            (122, 123),
            (123, 124),
            (112, 125),
            (125, 126),
            (126, 127),
            (127, 128),
            (112, 129),
            (129, 130),
            (130, 131),
            (131, 132),
        ]

        bone_count = 0
        scores = np.array(scores).flatten()  # Ensure scores is a 1D array

        for u, v in skeleton:
            if u < len(scores) and v < len(scores) and scores[u] > threshold and scores[v] > threshold:
                bone_count += 1

        return bone_count

    def infer_many(self, image_paths: List[str]) -> pd.DataFrame:
        """Override infer_many to process multiple images."""
        results = []
        for img_path in tqdm(image_paths, desc="Processing images"):
            result = self.process_image(img_path)
            results.append(
                {
                    "filename": os.path.basename(img_path),
                    "rtm_keypoints": result["keypoints"],
                    "rtm_keypoint_scores": result["scores"],
                    "rtm_bone_count": result["bone_count"],
                },
            )
        return pd.DataFrame(results)


import os


def demo_rtmpose():
    model_path = "/rmd/yada/checkpoints/rtmpose-l_8xb256-420e_humanart-256x192-389f2cb0_20230611_e2e.onnx"
    folder_path = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    inference = RTMPoseInference(model_path, device="gpu")

    results_df = inference.infer_many([os.path.join(folder_path, f) for f in os.listdir(folder_path)])
    results_df.to_parquet("rtmpose_metrics.parquet", index=False)
    print("Inference done, saved results to rtmpose_metrics.parquet")


# Example usage
if __name__ == "__main__":
    demo_rtmpose()
