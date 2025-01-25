from enum import Enum
from pathlib import Path
from datetime import datetime
import json

import dspy

from oddspy.lm_setup import LMForTask
from oddspy.processors import BaseProcessor, LMProcessor
from oddspy.pipeline import Pipeline, PipelineConfig
from oddspy.steps import BaseStep, LMStep
from oddspy.utils.logging import setup_logging


class ExampleBaseProcessor(BaseProcessor):
    def _process(self, data: dict) -> dict:
        return "Yes."

class ExampleLMProcessor(LMProcessor):
    class Signature(dspy.Signature):
        question = dspy.InputField(desc="Input question to be answered", format=str)
        answer = dspy.OutputField(desc="Output answer to question", format=str)
        
    def _process(self, data: dict) -> dict:
        question = data.get("question", "")
        return self.predictors['Signature'](question=question)


def create_pipeline(verbose: bool = False) -> Pipeline:
    steps = [
        BaseStep(
            step_type="test base step",
            processor_class=ExampleBaseProcessor,
            output_key="base_step_answer"
        ),
        LMStep(
            step_type="test lm step",
            lm_name=LMForTask.DEFAULT,
            processor_class=ExampleLMProcessor,
            output_key="lm_step_answer",
            depends_on=["*"]
        ),
        
    ]
    return Pipeline(PipelineConfig(steps=steps, verbose=verbose))


class ExamplePipeline:
    """Orchestrates the paper review workflow using a processing pipeline"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = setup_logging(None, timestamp, "example_pipeline")
        
        self.pipeline = create_pipeline(verbose=verbose)

    def do_the_thing(self, question: str) -> dict:
        self.logger.info(f"Starting pipeline execution")
        
        try:
            results = self.pipeline.execute({
                "question": question
            })
            
            # Convert DSPy Prediction object to its value
            if 'lm_step_answer' in results and hasattr(results['lm_step_answer'], 'answer'):
                results['lm_step_answer'] = results['lm_step_answer'].answer
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error executing pipeline: {str(e)}")
            raise ValueError(f"Error executing pipeline: {str(e)}")
        
        
if __name__ == "__main__":
    pipeline = ExamplePipeline(verbose=True)
    output = pipeline.do_the_thing("Yes or no, one word. Is 42 the meaning of life?")
    print("Pipeline Result:")
    print(json.dumps(output, indent=4))
            
        
        
