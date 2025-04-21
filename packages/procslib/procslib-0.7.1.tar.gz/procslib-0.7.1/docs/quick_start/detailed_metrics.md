# Detailed Metrics & Models

This page provides more in-depth references about the available model keys, their backbones, and any extra columns in their output DataFrames.

## Model Keys

| key                    | field   | description                                                  | backbone           |
| ---------------------- | ------- | ------------------------------------------------------------ | ------------------ |
| `twitter_logfav`       | anime   | log(predicted twitter favorite count)                        | convnext v2 base   |
| `weakm_v2`             | anime   | previous version of numerical aesthetics score               | convnext v2 base   |
| `siglip_aesthetic`     | general | an Clip Aesthetics alternative that uses siglip backbone and with better performance on anime<br />[discus0434/aesthetic-predictor-v2-5](https://github.com/discus0434/aesthetic-predictor-v2-5) | siglip (vit) + mlp |
| `pixiv_compound_score` | anime   | numerical aesthetics score based on pixiv bookmarks and other metrics | convnext v2 tiny   |
| `cv2_metrics`          | general | many useful image related metrics, such as noise, exposure, edge count, etc | (Not a model)      |
| `complexity_ic9600`    | general | a model that analyzes the "complexity" of images<br />[tinglyfeng/IC9600](https://github.com/tinglyfeng/IC9600) | ICNet (resnet18)   |
| `rtmpose`              | general | analyzes the presence of body parts of images<br />[mmpose/projects/rtmpose at main](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose) | RTMDet             |
| `depth`                | general | using MiDaS 3.0 to analyze the "depthness" of images and returns a numerical metric<br />[Intel/dpt-hybrid-midas · Hugging Face](https://huggingface.co/Intel/dpt-hybrid-midas) | MiDaS              |
| `q_align_quality`      | general | image quality assessment using Q-Align model (rough/distorted images = lower score; refined images = higher score)<br />[Q-Future/Q-Align](https://github.com/Q-Future/Q-Align) | VLM                |
| `q_align_aesthetics`   | general | image aesthetics assessment using Q-Align model (warn: has a western, or "midjourney-like" taste for higher qualities)<br />[Q-Future/Q-Align](https://github.com/Q-Future/Q-Align) | VLM                |
| `laion_watermark`      | general | a very fast watermark detection model that detects if there's text on the image. (works 80% of the time but could be inaccurate)<br />[LAION-AI/LAION-5B-WatermarkDetection](https://github.com/LAION-AI/LAION-5B-WatermarkDetection) | EfficientNet B3    |
| `clip_aesthetic`       | general | (WIP) caches clip embeddings, calculates similarities with a given list of prompts, then outputs aesthetics scores by supplying a list of MLP models. Very fast when embeddings are cached.<br />[troph-team/pixai-aesthetic](https://github.com/troph-team/pixai-aesthetic/tree/main) | clip (vit) + mlp   |

### 1. `cv2_metrics`

When you run `infer_many` with the `cv2_metrics` model, you get a DataFrame containing columns like:

- **edge_density**  
  The density of 'lines' in image, higher typically means more details but could go overcrowded if it's too high

- **focus_measure**  
  Laplacian variance of the image; higher = sharper image. laplacian variance is typically reduced when image is resized or upscaled (RESOLUTION DEPENDANT)

- **texture_score**  
  Some measure of local variation in the image.

- **noise_level**  
  Estimate of noise in the image.  

- **saturation**, **contrast**, **brightness**  
  Simple color channel stats.  

- **avg_dynamic_range**  
  The difference between 5% and 95% percentile of pixel intensities


### 2. `depth` (MiDaS)

This model outputs columns:

- **depth_score**  
  The difference between the upper (95%) and lower (15%) depth percentiles—effectively how much “range” the image has in 3D space.


### 3. Additional Models

You can add more details about the output columns for other models. Alternatively, keep them minimal if the user can see them from the code or from a sample inference.

