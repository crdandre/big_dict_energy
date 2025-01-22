# big_dict_energy: Kind of simple orchestration for DSPy

![alt text](media/image.png)

If you have a better and more mature title, feel free to suggest. Maybe *kosofod* (**K**ind **o**f **s**imple **o**rchestration **fo**r **D**SPy)

I wanted a simple-ish workflow builder for LLM workflows and wanted to learn so wrote this - it's composable action blocks that all operate on a shared dictionary as the storage for output and memory. This has it's disadvantages but as long as it fits in memory, this seems useful to me for straightforward assembly of structured data through chains of LLM calls.

# How it works

## Building Blocks

You can create layers of `Pipeline`s made of `Step`s.

Each `Step` (`BaseStep` or `LMStep`) uses `Processor`s which define either arbitrary code execution and/or language-model use. `dspy.Signature`s are used in each `Processor` input into `LMStep`s.

Configuration allows for setting per-task modules and `dspy.Module`s such as `Predict`, `ChainOfThought`, and `ReAct` (soon, with tools).

## Information Flow
Here are two example steps:

```python
[
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
```

The `output_key` of the `BaseStep` writes to a shared dictionary which the `LMStep` can access, and which accumulates the outputs of all prior steps. Passing `depends_on=["*"]` is passing all output keys generated before this step into the current step.

Alternatively for larger workflows you could pass in `depends_on=["previously_written_key", "another_key.nested_key.another_nested_key"]` for precise control of which information is passed into each step (hence, the keys available for context for the LLM calls within that step).


# Installation
(you should use [`uv`](https://docs.astral.sh/uv/)) `uv pip install big_dict_energy`

or

`git clone *url* && uv pip install -e .`

# Usage
1. Define a `lm_config.yaml` in your root based on `lm_config.yaml.example`
2. Define `OPENROUTER_API_KEY` in your `.env` if using openrouter
3. Create! See `examples/example_pipeline.py` for a basic workflow created using this framework


# Desired Features to Add Next
1. `dspy.ReAct` support + any other new modules
2. Checkpoint support - tracking step execution and restarting from any step
3. Improved error transparency and aesthetics for logging
4. Interactivity? Tool template if needed? Infra for code-writing/editing agents?

