# src/procslib/model_builder.py

import logging

from procslib.config import get_config

logger = logging.getLogger(__name__)


def get_hf_automodel_model(**overrides):
    """A custom-trained image model from Hugging Face transformers supporting classification, regression, or ordinal tasks.
    Input: images, Output: predicted labels/values based on task type.
    Can be initialized with a Hugging Face model ID or a local folder path.

    Args:
        model_path (str): Either a Hugging Face model ID or a local folder path.
        task (str): Task type ('classification', 'regression', 'ordinal').
        device (str): Device to run inference on ('cuda' or 'cpu').
        batch_size (int): Batch size for inference.
    """
    from procslib.models.hf_automodel_inference import HfAutomodelInference

    default_model = "google/vit-base-patch16-224"  # Example base model
    model_path = overrides.get("model_path", default_model)
    task = overrides.get("task", "classification")  # Default to classification

    logger.info(f"Loading custom image model from {model_path} for task: {task}")

    return HfAutomodelInference(
        model_path=model_path,
        task=task,
        device=overrides.get("device", "cuda"),
        batch_size=overrides.get("batch_size", 32),
    )


def get_custom_image_model_repreciate(**overrides):
    """A custom-trained image model from Hugging Face transformers supporting classification, regression, or ordinal tasks.

    DEPRECATED: use get_hf_automodel_model instead
    """
    print("DEPRECATED: use get_hf_automodel_model instead")
    return get_hf_automodel_model(**overrides)


def get_wdv3_timm_model(**overrides):
    """WDv3 Tagger using timm from SmilingWolf's HF repos.

    Args:
        repo_id: eg. SmilingWolf/wd-eva02-large-tagger-v3
        gen_threshold: Probability threshold for general tags.
        char_threshold: Probability threshold for character tags.
        device: "cuda" or "cpu".
        batch_size: Batch size for inference.
    """
    from procslib.models.tagger_wdv3_timm import WDV3TaggerTimmInference

    return WDV3TaggerTimmInference(**overrides)


def get_q_align_quality_model(**overrides):
    """A model trained for predicting image quality using QAlign.
    输入图片, 输出图片质量评

    Params:
        device: "cuda" or "cpu".
        batch_size: Batch size for inference.
    """
    from procslib.models.hf_automodel_inference import HfAutomodelInference

    return HfAutomodelInference(
        model_path="trojblue/distill-q-align-quality-siglip2-base",
        task="classification",
        device=overrides.get("device", "cuda"),
        batch_size=overrides.get("batch_size", 32),
    )


def get_q_align_aesthetics_model(**overrides):
    """A model trained for predicting image aesthetics using QAlign.
    输入图片, 输出图片美学评分

    Params:
        device: "cuda" or "cpu".
        batch_size: Batch size for inference.
    """
    from procslib.models.hf_automodel_inference import HfAutomodelInference

    return HfAutomodelInference(
        model_path="trojblue/distill-q-align-aesthetic-siglip2-base",
        task="classification",
        device=overrides.get("device", "cuda"),
        batch_size=overrides.get("batch_size", 32),
    )


def get_pixai_aesthetic_model(**overrides):
    """Aesthetic model trained on pixiv data (of the constructed pixiv compound aesthetic score)
    model at "https://bucket-public-access-uw2.s3.us-west-2.amazonaws.com/dist/compound_score_aesthetic_predictor/model.ckpt"
    """
    from procslib.models.hf_automodel_inference import HfAutomodelInference

    curr_org = get_config("HF_ORG")

    return HfAutomodelInference(
        model_path=f"{curr_org}/incantor/aes-pixai-1.1",
        task="regression",
        device=overrides.get("device", "cuda"),
        batch_size=overrides.get("batch_size", 32),
    )


def get_pixai_anatomy_model(**overrides):
    """Aesthetic model trained on pixiv data (of the constructed pixiv compound aesthetic score)
    model at "https://bucket-public-access-uw2.s3.us-west-2.amazonaws.com/dist/compound_score_aesthetic_predictor/model.ckpt"
    """
    from procslib.models.hf_automodel_inference import HfAutomodelInference

    curr_org = get_config("HF_ORG")

    return HfAutomodelInference(
        model_path=f"{curr_org}/aes-pixai-1.1-anatomy",
        task="regression",
        device=overrides.get("device", "cuda"),
        batch_size=overrides.get("batch_size", 32),
    )


# ================== LEGACY MODELS ==================

# def get_weakm_v2_model():
#     """A model trained for WeakM aesthetic predictions (v2) with low mean absolute error.
#     输入anime图片, 输出预测的weakm v2 score (base score:10)
#     """
#     from procslib.models import AnimeAestheticInference

#     curr_org = get_config("HF_ORG")

#     # Download the model checkpoint from the Hugging Face Hub
#     checkpoint_path = hf_hub_download(
#         repo_id=f"{curr_org}/{'aes-pred-convbase-weakm-v2'}",
#         filename="epoch=4,mae=0.0824,step=0.ckpt",
#     )
#     print(checkpoint_path)
#     return AnimeAestheticInference(checkpoint_path=checkpoint_path, column_name="weakm_v2_score")


# def get_weakm_v3_model():
#     """A model trained for WeakM aesthetic predictions (v2) with low mean absolute error.
#     输入anime图片, 输出预测的weakm v2 score (base score:10)
#     """
#     from procslib.models import AnimeAestheticInference

#     curr_org = get_config("HF_ORG")

#     # Download the model checkpoint from the Hugging Face Hub
#     checkpoint_path = hf_hub_download(
#         repo_id=f"{curr_org}/{'aes-pred-convbase-weakm-v3'}",
#         filename="epoch=7,mae=0.2295,step=0.ckpt",
#     )
#     print(checkpoint_path)
#     return AnimeAestheticInference(checkpoint_path=checkpoint_path, column_name="weakm_v3_score")

# def get_q_align_aesthetics_model(**overrides):
#     """A model trained for predicting image aesthetics using QAlign.
#     输入图片, 输出图片美学评分
#     """
#     from procslib.models.q_align import QAlignAsyncInference

#     return QAlignAsyncInference(task="aesthetics", **overrides)


# def get_laion_watermark_model(**overrides):
#     """A model trained for predicting watermarks using Laion.
#     输入图片, 输出水印评分
#     """
#     from procslib.models.laion_watermark import LaionWatermarkInference

#     return LaionWatermarkInference(**overrides)

# def get_twitter_logfav_model():
#     """A model trained for predicting Twitter log-favorites using AnimeAestheticInference.
#     Takes an anime image as input and outputs the predicted log-scaled number of Twitter favorites.
#     """
#     from procslib.models import AnimeAestheticInference

#     curr_org = get_config("HF_ORG")

#     # Download the model checkpoint from the Hugging Face Hub
#     checkpoint_path = hf_hub_download(
#         repo_id=f"{curr_org}/{'aes-pred-convbase-twitter-logfav'}",
#         filename="convbase_twitter_aes_logfav_full_v2cont3_e4_mae0.50.ckpt",
#     )
#     print(checkpoint_path)

#     # Initialize the inference model
#     return AnimeAestheticInference(checkpoint_path=checkpoint_path, column_name="twitter_logfav_score")


# def get_vila_model():
#     """A model trained for generating captions using VILA (Efficient-Large-Model/NVILA-15B)
#     https://github.com/NVlabs/VILA

#     输入图片, 输出描述
#     """
#     from procslib.models.vila_wrapper import VILAInference

#     return VILAInference(model_path="Efficient-Large-Model/NVILA-15B", device="cuda", batch_size=1)
