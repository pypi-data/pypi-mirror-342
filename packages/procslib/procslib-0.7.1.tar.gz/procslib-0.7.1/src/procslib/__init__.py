"""procslib package.

Multi-purpose processing library for downstream use
"""

from __future__ import annotations

from .config import get_config, get_configs, set_config
from .model_registry import get_model, get_model_keys, print_model_keys

__all__: list[str] = [get_model, get_model_keys, print_model_keys]
