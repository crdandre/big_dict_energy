"""
Step configurations and base classes for LLM-based workflows.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Type, Optional, Union, TYPE_CHECKING
from inspect import isclass

import dspy
from big_dict_energy.lm_setup import TaskConfig

if TYPE_CHECKING:
    from processors import BaseProcessor

@dataclass
class BaseStep:
    """Base configuration for any processing step"""
    step_type: Union[str, Enum]
    processor_class: Type["BaseProcessor"]
    output_key: str
    depends_on: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    verbose: bool = False


@dataclass
class LMStep(BaseStep):
    """Configuration specific to LLM-based processing steps"""
    lm_name: str = "default"
    task_config: Optional[TaskConfig] = None
    signatures: Optional[List[Type[dspy.Signature]]] = None
    
    def __post_init__(self):
        """Use provided signatures or auto-discover from processor class"""
        if self.signatures is None:
            self.signatures = [
                member for _, member in vars(self.processor_class).items()
                if isclass(member) and issubclass(member, dspy.Signature) 
                and member != dspy.Signature
            ]
        if not self.signatures:
            raise ValueError(f"No Signature classes found for {self.processor_class.__name__}")

