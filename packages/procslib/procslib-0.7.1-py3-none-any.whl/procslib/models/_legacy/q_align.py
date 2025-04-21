"""IMPORTANT Q-align和siglip aesthetics 2.5不兼容; 两者只能单独使用.

- Q-align: 需要`pip install "transformers==4.36.1"`

- siglip aesthetics: 需要更高版本的transformers

inference之后重新安装transformers来切换可用的模型版本
"""

# Apply nest_asyncio to allow reentrant event loops in Jupyter Notebooks
import nest_asyncio

nest_asyncio.apply()

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List

import nest_asyncio
import pandas as pd
import torch
from PIL import Image
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM

from ..base_inference import BaseImageInference

nest_asyncio.apply()


class QAlignAsyncInference(BaseImageInference):
    def __init__(
        self,
        task: str = "quality",
        device: str = "cuda",
        batch_size: int = 48,
        max_workers: int = 16,
        prefetch_batches: int = 10,
    ):
        """QAlign Async Inference class with pipelined loading + GPU compute.

        Args:
            task (str): "quality" or "aesthetics".
            device (str): Inference device, usually "cuda".
            batch_size (int): How many images to process per inference call.
            max_workers (int): Number of threads for image loading.
            prefetch_batches (int): Number of batches to prefetch for processing.
        """
        super().__init__(device=device, batch_size=batch_size)
        assert task in ["quality", "aesthetics"], "Task must be either 'quality' or 'aesthetics'."
        self.task = task
        self.prefetch_batches = prefetch_batches
        self._load_model()

        # ThreadPoolExecutor for I/O-bound loading
        self.io_executor = ThreadPoolExecutor(max_workers=max_workers)

    def _load_model(self):
        """Load the QAlign model."""
        self.model = AutoModelForCausalLM.from_pretrained(
            "q-future/one-align",
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
        ).to(self.device)

    def _preprocess_image(self, pil_image: Image.Image):
        """Preprocess the input image."""
        return pil_image

    def _postprocess_output(self, output):
        """Postprocess the model output."""
        return output

    def _set_tokenizer_env(self):
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

    def _unset_tokenizer_env(self):
        del os.environ["TOKENIZERS_PARALLELISM"]

    def infer_one(self, pil_image: Image.Image):
        return self.infer_batch([pil_image])[0]

    def infer_batch(self, pil_images: List[Image.Image]):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._infer_batch_async(pil_images))

    async def _infer_batch_async(self, pil_images: List[Image.Image]):
        self._set_tokenizer_env()
        scores = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.model.score(pil_images, task_=self.task, input_="image").tolist(),
        )
        self._unset_tokenizer_env()
        return scores

    async def _load_image_async(self, path: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.io_executor, self._load_image_sync, path)

    def _load_image_sync(self, path: str):
        return Image.open(path).convert("RGB")

    async def _produce_image_batches(self, image_paths: List[str], queue: asyncio.Queue, pbar):
        """Producer that prefetches batches and adds them to a queue."""
        for i in range(0, len(image_paths), self.batch_size):
            batch_paths = image_paths[i : i + self.batch_size]
            loaded_images = await asyncio.gather(*[self._load_image_async(p) for p in batch_paths])
            pbar.update(len(batch_paths))  # Update progress bar
            await queue.put((batch_paths, loaded_images))
        # Signal that all batches are produced
        for _ in range(self.prefetch_batches):
            await queue.put(None)

    async def _consume_batches(self, queue: asyncio.Queue, pbar):
        """Consumer that processes batches from the queue."""
        results = []
        while True:
            batch = await queue.get()
            if batch is None:
                break
            batch_paths, batch_images = batch
            batch_scores = await self._infer_batch_async(batch_images)
            for path, score in zip(batch_paths, batch_scores):
                results.append(
                    {
                        "path": path,  # Changed from "filename": os.path.basename(path)
                        f"qalign_{self.task}_score": score,
                    },
                )
        return results

    async def _infer_many_pipeline(self, image_paths: List[str]):
        """Pipeline that orchestrates prefetching and processing with a queue."""
        queue = asyncio.Queue(maxsize=self.prefetch_batches)
        with tqdm(total=len(image_paths), desc="Processing Images", unit="image") as pbar:
            producer = asyncio.create_task(self._produce_image_batches(image_paths, queue, pbar))
            consumer = asyncio.create_task(self._consume_batches(queue, pbar))
            await producer
            results = await consumer
        return results

    def infer_many(self, image_paths: List[str]):
        """High-level API to run pipeline inference for many images."""
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self._infer_many_pipeline(image_paths))
        return pd.DataFrame(results)


# Example usage
async def q_align_demo_async():
    import warnings

    warnings.filterwarnings("ignore")

    task = "quality"  # or "aesthetics"
    folder_path = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"

    inference = QAlignAsyncInference(task=task, device="cuda", batch_size=8)
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

    results_df = await inference.infer_many(image_paths)
    results_df.to_csv("qalign_results_async.csv", index=False)
    print("Inference done, saved results to qalign_results_async.csv")


if __name__ == "__main__":
    asyncio.run(q_align_demo_async())
