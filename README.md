# Worflow Builder for DSPy

I wanted a simple-ish workflow builder for LLM workflows (LM as DSPy calls them)
so wrote this - it's composable action blocks that all operate on a shared dictionary.

You can create layers of `Pipeline`s made of `Step`s.

Each `Step` (`BaseStep` or `LMStep`) uses `Processor`s which define either arbitrary code execution and/or language-model use. `dspy.Signature`s are used in each `Processor` input into `LMStep`s.

Configuration allows for setting per-task modules and `dspy.Module`s such as `Predict`, `ChainOfThought`, and `ReAct` (soon, with tools).

# Usage

1. Define a `lm_config.yaml` in your root based on `lm_config.yaml.example`
2. Define `OPENROUTER_API_KEY` in your `.env` if using it
3. See `example_workflow.py` for a basic workflow created using this framework

