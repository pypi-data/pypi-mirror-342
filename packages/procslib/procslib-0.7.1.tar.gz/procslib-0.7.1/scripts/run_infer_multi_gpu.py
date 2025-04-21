# run_infer_multi_gpu.py

import argparse
import multiprocessing as mp
import os
from pathlib import Path

import unibox as ub

from procslib import get_model


def worker(images, model_name, gpu_id, output_path, log_path):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    import logging

    from tqdm.contrib.logging import logging_redirect_tqdm

    logging.basicConfig(
        filename=log_path,
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )

    model = get_model(model_name)

    with logging_redirect_tqdm():
        result_df = model.infer_many(images)

    result_df.to_parquet(output_path, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("img_dir", type=str, help="Directory containing images")
    parser.add_argument("--model", type=str, default="aesthetic-pixai-1.1-anatomy")
    parser.add_argument("--gpus", type=int, default=4)
    args = parser.parse_args()

    all_images = ub.ls(args.img_dir, ub.IMG_FILES)
    chunks = [all_images[i :: args.gpus] for i in range(args.gpus)]

    dir_id = "_".join(Path(args.img_dir).parts[-2:]).replace("/", "_")

    processes = []
    for i, chunk in enumerate(chunks):
        output_path = f"{dir_id}_{i}.parquet"
        log_path = f"{dir_id}_{i}.log"
        p = mp.Process(
            target=worker,
            args=(chunk, args.model, i, output_path, log_path),
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
