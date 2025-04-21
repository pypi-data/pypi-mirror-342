import argparse
import os

import pandas as pd
import unibox as ub

# If your path is different, update accordingly
from procslib.model_builder import get_model

# Optional: If you still want to handle a default anime aesthetic if --models is not provided,
# you can import it directly:


def main(args):
    """1. Reads the parquet file containing image paths.
    2. Splits --models into a list of model keys (e.g. "weakm_v2 cv2_metrics rtmpose").
    3. For each model key, fetches the model from model_builder and performs inference.
    4. Saves each result to a new parquet file, e.g. "<orig_filename>_tagged_<model_key>.parquet".
    """
    # Load the parquet containing paths
    df = pd.read_parquet(args.paths_file)
    img_paths = df[args.path_column].tolist()
    print("Data file loaded:", ub.peeks(img_paths))

    # If user gave a list of models, use that. Otherwise, fall back to the original anime aesthetic logic.
    if args.models.strip():
        model_list = args.models.strip().split()
    else:
        print("No --models specified, it is required to provide at least one model.")
        return

    # Otherwise, we have multiple models specified:
    # For each model, get the instance, run inference, save parquet.
    orig_filename = os.path.basename(args.paths_file)  # e.g. "0.parquet"
    os.makedirs(args.save_dir, exist_ok=True)

    for model_name in model_list:
        print(f"\n=== Building model '{model_name}' ===")
        model = get_model(model_name)  # calls the function from MODEL_REGISTRY
        print(f"Model '{model_name}' built. Starting inference...")

        # This model is expected to adhere to the BaseImageInference interface
        # res = model.infer_many(img_paths, batch_size=args.batch_size)
        res = model.infer_many(img_paths)
        print(f"Inference for '{model_name}' completed:", ub.peeks(res))

        # Save results
        save_filename = f"{orig_filename}_tagged_{model_name}.parquet"
        save_path = os.path.join(args.save_dir, save_filename)
        ub.saves(res, save_path)
        print(f"Results for '{model_name}' saved to: {save_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Infer aesthetics (or multiple models) on a parquet of image paths.")
    parser.add_argument(
        "--paths_file",
        type=str,
        required=True,
        help="Path to the parquet file containing image paths.",
    )
    parser.add_argument(
        "--path_column",
        type=str,
        default="local_path",
        help="Name of the dataframe column containing the image paths.",
    )
    parser.add_argument("--save_dir", type=str, default="./", help="Directory to save output parquet files.")
    parser.add_argument(
        "--checkpoint_path",
        type=str,
        default="",
        help="Checkpoint path for anime_aesthetic_cls if you are not providing --models.",
    )
    parser.add_argument(
        "--models",
        type=str,
        default="",
        help="Space-separated list of models (keys in MODEL_REGISTRY) to run sequentially.",
    )
    parser.add_argument("--batch_size", type=int, default=64, help="Batch size for inference.")
    return parser.parse_args()


if __name__ == "__main__":
    # Example usage:
    # python infer_many.py --paths_file /lv0/test_aesthetics/procslib/data/twitter_path_chunks/0.parquet --models "cv2_metrics"
    args = parse_args()
    main(args)
