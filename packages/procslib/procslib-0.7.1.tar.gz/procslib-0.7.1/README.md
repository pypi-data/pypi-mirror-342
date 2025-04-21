# procslib

[![ci](https://github.com/arot-devs/procslib/workflows/ci/badge.svg)](https://github.com/arot-devs/procslib/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://arot-devs.github.io/procslib/)
[![pypi version](https://img.shields.io/pypi/v/procslib.svg)](https://pypi.org/project/procslib/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#procslib:gitter.im)

**Multi-purpose processing library** for various inference tasks.  
Generated with [copier-uv](https://github.com/pawamoy/copier-uv).

---

## Installation

```bash
pip install procslib
```

Or using [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install procslib
```

> **Note**: The inference requirements are not included for faster unittesting.
> See [Dev Guide](https://urban-meme-g6ok8om.pages.github.io/dev_guide/) for a proper inference setup.

## Quick Usage

Below is a minimal example of how to infer images with `procslib`:

```python
from procslib import get_model_keys, get_model

# List available models
print(get_model_keys())

# Create a model, e.g. "twitter_logfav"
model = get_model("twitter_logfav")

# Infer on some images
image_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]
results_df = model.infer_many(image_paths)
print(results_df.head())
```

## Supported Models

You can retrieve a model via `get_model(key)`. Here’s a quick reference:

| Key                    | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| `twitter_logfav`       | Predicts log-scaled Twitter favorites for anime images.      |
| `weakm_v2`             | Aesthetic prediction model for anime images using WeakM v2 scoring. |
| `weakm_v3`             | Updated WeakM v3-based aesthetic scoring model for anime images. |
| `siglip_aesthetic`     | A Siglip-based model for aesthetic prediction (requires specific `transformers` versions). |
| `pixiv_compound_score` | Predicts a compound aesthetic score for Pixiv-based anime images. |
| `cv2_metrics`          | Computes basic image quality metrics (noise, brightness, contrast, sharpness, etc.). |
| `complexity_ic9600`    | Predicts image complexity using the IC9600 model.            |
| `rtmpose`              | Detects human pose keypoints in images using RTMPose.        |
| `depth`                | Uses MiDaS-based depth estimation to provide a "depthness" score (0.0-1.0). |
| `q_align_quality`      | Predicts image quality scores using the QAlign model.        |
| `q_align_aesthetics`   | Predicts image aesthetics using the QAlign model.            |
| `laion_watermark`      | Detects watermarks in images using a model from LAION.       |
| `clip_aesthetic`       | Uses CLIP-based embeddings for aesthetic scoring and zero-shot classification. |
| `vila`                 | Generates textual descriptions of images using the NVILA-15B model. |
| `jz_tagger`            | Multi-label image classification model with aesthetic scoring (Danbooru-based). |
| `aigc_classifier`      | Classifies images as AI-generated or real using `incantor/aigc_real_cls`. |
| `szh_image_category`   | Categorizes images using `szh/image_category_cls`.           |
| `anime_real_cls`       | Classifies images as anime or real with confidence scores using `incantor/anime_real_cls`. |

> **Note**: Q-Align and Siglip Aesthetics are incompatible with each other’s `transformers` version.
> If you need both, see [Docs: Handling Conflicting Dependencies]().

## Development

For development tasks (testing, formatting, releasing), see [Dev Guide](https://urban-meme-g6ok8om.pages.github.io/dev_guide/) or run:

```bash
make setup   # one-time
make format  # auto-format
make test
make check
make changelog
make release version=x.y.z
```

To build wheels manually, run the following commands:

```bash
python -m pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```

## Documentation

To learn more, visit our [MkDocs-based docs](https://urban-meme-g6ok8om.pages.github.io/) or run:

```bash
make docs host=0.0.0.0
```

- [Quick Start: Using Models](https://urban-meme-g6ok8om.pages.github.io/quick_start/using_models/)
- [Quick Start: Adding New Models](https://urban-meme-g6ok8om.pages.github.io/quick_start/adding_new_models/)
- [VSCode Tips](https://urban-meme-g6ok8om.pages.github.io/quick_start/decluttering_vscode/)
- [Detailed metric descriptions](https://urban-meme-g6ok8om.pages.github.io/quick_start/detailed_metrics/)