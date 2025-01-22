from big_dict_energy.pipeline import Pipeline, PipelineConfig
from big_dict_energy.processors import BaseProcessor
from big_dict_energy.steps import BaseStep

def test_pipeline():
    class TestProcessor(BaseProcessor):
        def _process(self, data: dict) -> dict:
            return {"processed": True}

    config = PipelineConfig(
        steps=[
            BaseStep(
                step_type="test",
                processor_class=TestProcessor,
                output_key="test_output"
            ),
            BaseStep(
                step_type="test2",
                processor_class=TestProcessor,
                depends_on=["test_output"],
                output_key="test_output2"
            )
        ]
    )
    
    pipeline = Pipeline(config)
    
    result = pipeline.execute({"input": "data"})
    assert "test_output" in result and "test_output2" in result
    assert (
        result["test_output"] == {"processed": True} and
        result["test_output2"] == {"processed": True}
    )
    
    
def test_nested_pipeline():
    class TestProcessor(BaseProcessor):
        def _process(self, data: dict) -> dict:
            return {"processed": True}

    inner_config = PipelineConfig(
        steps=[
            BaseStep(
                step_type="inner_step",
                processor_class=TestProcessor,
                output_key="inner_output"
            )
        ]
    )
    
    inner_pipeline = Pipeline(inner_config)

    class NestedProcessor(BaseProcessor):
        def _process(self, data: dict) -> dict:
            inner_result = inner_pipeline.execute(data)
            return {"nested_processed": inner_result["inner_output"]}

    outer_config = PipelineConfig(
        steps=[
            BaseStep(
                step_type="outer_step",
                processor_class=NestedProcessor,
                output_key="outer_output"
            )
        ]
    )

    outer_pipeline = Pipeline(outer_config)
    
    result = outer_pipeline.execute({"input": "data"})
    assert "outer_output" in result
    assert result["outer_output"]["nested_processed"]["processed"] is True