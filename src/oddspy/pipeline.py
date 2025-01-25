"""
Pipeline implementation for executing LLM-based workflows.
"""

from dataclasses import dataclass
from enum import Enum
import logging
from typing import Dict, List, Type, Union

import dspy

from .steps import BaseStep, LMStep
from .processors import BaseProcessor
from .utils.text_utils import serialize_paths
from .utils.logging import pipeline_context


class ValidationError(Exception):
    """Raised when step output validation fails."""
    pass


@dataclass
class PipelineConfig:
    """Configuration for the entire processing pipeline"""
    steps: List[Union[LMStep, BaseStep]]
    verbose: bool = False
    validation: bool = True 


class Pipeline(dspy.Module):
    """Pipeline for executing a series of processing steps.
    Manages the flow of data through multiple processing steps, handling
    dependencies and storing results.
    """
    def __init__(self, config: PipelineConfig):
        super().__init__()
        self.config = config
        self.processors: Dict[Union[str, Enum], Type[BaseProcessor]] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        
        for step in config.steps:
            self.register_processor(step.step_type, step.processor_class)

    def register_processor(self, 
                         step_type: Union[str, Enum], 
                         processor_class: Type[BaseProcessor]):
        """Register a processor class for a specific step type."""
        self.processors[step_type] = processor_class

    def execute(self, data: dict) -> dict:
        """Execute the complete processing pipeline."""
        data = serialize_paths(data)
        
        # Use pipeline context for nested logging
        with pipeline_context(self.__class__.__name__):
            for step in self.config.steps:
                if step.step_type not in self.processors:
                    raise ValueError(f"No processor registered for step type: {step.step_type}")

                processor = self.processors[step.step_type](step)

                try:
                    result = processor.process(data)
                    if step.output_key:
                        data[step.output_key] = result
                    else:
                        data.update(result)
                except Exception as e:
                    self.logger.error(f"Failed step: {step.step_type} - {str(e)}")
                    raise

        return data 