"""
Processor implementations for LLM and compute-based workflow steps.
"""
from functools import reduce
import logging

import dspy

from .steps import BaseStep, LMStep
from .utils.logging import log_step
from .utils.text_utils import normalize_text_fields, serialize_paths


class BaseProcessor:
    """Base class for all processors"""
    def __init__(self, step: BaseStep):
        self.step = step
        self.logger = logging.getLogger(f"processor.{step.step_type}")

    @log_step()
    def process(self, data: dict) -> dict:
        pre_processed = self._pre_process(data)
        result = self._process(pre_processed)
        return self._post_process(result)
    
    def _get_by_path(self, data: dict, path: str):
        """Get a value from a nested dictionary using dot notation"""
        return reduce(lambda d, key: d[key], path.split('.'), data)

    def _post_process(self, data: dict) -> dict:
        result = serialize_paths(data)
        if not self._validate_output(result):
            raise ValueError(
                f"Output validation failed for step: {self.step.step_type}"
                f"\n\nFailing Result:"
                f"\n\n{result}"
            )
        return result

    def _pre_process(self, data: dict) -> dict:
        self._validate_dependencies(data)
        if self.step.depends_on:
            if "*" in self.step.depends_on:
                return normalize_text_fields(data)
            return normalize_text_fields({
                path.split('.')[-1]: self._get_by_path(data, path)
                for path in self.step.depends_on
            })
        return normalize_text_fields(data)

    def _process(self, data: dict) -> dict:
        raise NotImplementedError()

    def _try_get_path(self, data: dict, path: str) -> bool:
        """Safely try to get a value by path, return False if not found"""
        try:
            self._get_by_path(data, path)
            return True
        except (KeyError, TypeError):
            return False
        
    def _validate_dependencies(self, data: dict) -> None:
        """Validate that declared dependencies exist in data"""
        if not self.step.depends_on or "*" in self.step.depends_on:
            return
        
        missing = [
            path for path in self.step.depends_on
            if not self._try_get_path(data, path)
        ]
            
        if missing:
            raise ValueError(f"{self.__class__.__name__} missing required dependencies: {missing}")

    def _validate_output(self, result) -> bool:
        """Validate processor output. Override in subclasses for specific validation."""
        return bool(result)


class LMProcessor(dspy.Module, BaseProcessor):
    """Base class for LM-based processors"""
    def __init__(self, step: LMStep):
        dspy.Module.__init__(self)
        BaseProcessor.__init__(self, step)
        
        self.lm = step.lm_name.get_lm()
        dspy.settings.configure(lm=self.lm)        
        predictor_type = step.lm_name.get_predictor_type()
        
        try:
            predictor_class = getattr(dspy, predictor_type.value)
        except AttributeError:
            raise ValueError(f"Invalid predictor type: {predictor_type.value}")
        
        self.predictors = {
            sig.__name__: predictor_class(sig)
            for sig in step.signatures
        }
        
