"""
Big Dict Energy - A composable language model workflow builder for DSPy
with dictionary-based data storage
"""

from pipeline import Pipeline, PipelineConfig
from processors import BaseProcessor, LMProcessor
from steps import BaseStep, LMStep
from parse_lm_config import LMForTask, TaskConfig

__version__ = "0.1.0"

__all__ = [
    "Pipeline",
    "PipelineConfig",
    "BaseProcessor",
    "LMProcessor",
    "BaseStep",
    "LMStep",
    "LMForTask",
    "TaskConfig",
]