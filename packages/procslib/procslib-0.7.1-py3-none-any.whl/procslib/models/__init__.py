import importlib

# List of model modules to import
model_modules = [
    # "anime_aesthetic.AnimeAestheticInference",
    # "anime_aesthetic_cls.AnimeAestheticClassificationInference",
    # "complexity_ic9600.IC9600Inference",
    # "cv2_wrapper.OpenCVMetricsInference",
    # "depth_wrapper.DepthEstimationInference",
    # "pixiv_compound_score.PixivCompoundScoreInference",
    # "rtmpose.RTMPoseInference",
    # "siglip_aesthetics.SiglipAestheticInference",
    # "q_align.QAlignInference",
    # "q_align.QAlignAsyncInference",
    # "laion_watermark.LaionWatermarkInference",
    # "clip_aesthetic_cached.CachedClipAestheticInference",
    # "clip_aesthetic_cached.get_mlp_model",
]

# Dictionary to hold successfully imported models
loaded_models = {}

for module_path in model_modules:
    module_name, class_name = module_path.rsplit(".", 1)
    try:
        module = importlib.import_module(f".{module_name}", __package__)
        loaded_models[class_name] = getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        print(f"Failed to load {module_path}: {e}")

# Dynamically set attributes for successfully imported models
globals().update(loaded_models)
