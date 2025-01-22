import pytest
from big_dict_energy import Pipeline, PipelineConfig, BaseStep, BaseProcessor

def test_pipeline_initialization():
    class TestProcessor(BaseProcessor):
        def _process(self, data: dict) -> dict:
            return data

    config = PipelineConfig(
        steps=[
            BaseStep(
                step_type="test",
                processor_class=TestProcessor,
                output_key="test_output"
            )
        ]
    )
    
    pipeline = Pipeline(config)
    assert pipeline is not None