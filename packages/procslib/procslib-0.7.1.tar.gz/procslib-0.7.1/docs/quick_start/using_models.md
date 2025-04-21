# Using Models

This guide shows how to call the models in `procslib`.

## Basic API

Every model in `procslib` has three main methods:

- `infer_one(image_path_or_PIL)`: Inference on a single image
- `infer_batch([...])`: Inference on a small list of images
- `infer_many([...])`: Inference on a large list of images, using DataLoader

## Example

```python
from procslib import get_model_keys, get_model

print(get_model_keys())  # see available models
model = get_model("cv2_metrics")

# Single image
res1 = model.infer_one("path/to/image.jpg")
print(res1)

# Batch
res2 = model.infer_batch(["path/to/img1.jpg", "path/to/img2.jpg"])

# Large dataset
res3 = model.infer_many([...])

```

If you want to combine multiple models on a list of images:

```python
import unibox as ub
img_paths = ub.traverses("my/image/folder", ub.IMG_FILES)

for key in ["twitter_logfav", "weakm_v2", "siglip_aesthetic"]:
    model = get_model(key)
    df = model.infer_many(img_paths)
    df.to_csv(f"results_{key}.csv", index=False)

```