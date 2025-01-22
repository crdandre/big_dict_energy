"""Configuration for language models used in different tasks."""
from dataclasses import dataclass
from typing import Dict, Optional
import dspy
import os
from enum import Enum
from pathlib import Path
import yaml

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/"
DEFAULT_TEMPERATURE = 0.9


class PredictorType(Enum):
    CHAIN_OF_THOUGHT = "ChainOfThought"
    PREDICT = "Predict"

    @classmethod
    def from_str(cls, value: str) -> 'PredictorType':
        try:
            return cls(value)
        except ValueError:
            return cls.PREDICT


@dataclass
class LMConfig:
    model_name: str
    temperature: float = 0.9
    api_base: Optional[str] = None
    api_key: str = os.getenv("OPENROUTER_API_KEY")
    max_tokens: Optional[int] = None

    def __post_init__(self):
        if self.api_base is None:
            self.api_base = OLLAMA_BASE_URL if self.model_name.startswith('ollama') else OPENROUTER_BASE_URL

    def create_lm(self) -> dspy.LM:
        params = {
            "model": self.model_name,
            "api_base": self.api_base,
            "api_key": self.api_key,
            "temperature": self.temperature,
            **({"max_tokens": self.max_tokens} if self.max_tokens is not None else {})
        }
        return dspy.LM(**params)


@dataclass
class TaskConfig:
    lm_config: LMConfig
    predictor_type: PredictorType = PredictorType.PREDICT

    def create_lm(self) -> dspy.LM:
        return self.lm_config.create_lm()


repo_root = Path(__file__).parent.parent.parent
config_path = repo_root / "lm_config.yaml"

if not config_path.exists():
    raise FileNotFoundError(
        f"Could not find lm_config.yaml in {config_path}. "
        "Please ensure the config file exists in the root of your repository."
    )

with open(config_path) as f:
    _raw_config = yaml.safe_load(f)


DEFAULT_CONFIGS = {
    task_name: TaskConfig(
        lm_config=LMConfig(
            model_name=task_config["model_name"],
            temperature=task_config.get("temperature", DEFAULT_TEMPERATURE),
            max_tokens=task_config.get("max_tokens")
        ),
        predictor_type=PredictorType.from_str(task_config.get("predictor_type", "Predict"))
    )
    for task_name, task_config in _raw_config.items()
}


# Create enum dynamically from YAML config
LMForTask = Enum(
    'LMForTask',
    [(k.upper(), k) for k in _raw_config.keys()],
    type=str
)

def get_config(self) -> TaskConfig:
    return DEFAULT_CONFIGS.get(self.value, DEFAULT_CONFIGS['default'])

def get_lm(self) -> dspy.LM:
    return self.get_config().create_lm()

def get_predictor_type(self) -> PredictorType:
    return self.get_config().predictor_type

# Add all methods to the Enum class
LMForTask.get_config = get_config
LMForTask.get_lm = get_lm
LMForTask.get_predictor_type = get_predictor_type