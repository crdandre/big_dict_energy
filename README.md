# big_dict_energy: Worflow Builder for DSPy

I wanted a simple-ish workflow builder for LLM workflows so wrote this - it's composable action blocks that all operate on a shared dictionary. As long as it fits in memory, this seems useful to me for straightforward assembly of structured data through chains of LLM calls.

# How it works

You can create layers of `Pipeline`s made of `Step`s.

Each `Step` (`BaseStep` or `LMStep`) uses `Processor`s which define either arbitrary code execution and/or language-model use. `dspy.Signature`s are used in each `Processor` input into `LMStep`s.

Configuration allows for setting per-task modules and `dspy.Module`s such as `Predict`, `ChainOfThought`, and `ReAct` (soon, with tools).

# Installation
(you should use [`uv`](https://docs.astral.sh/uv/)) `uv pip install big_dict_energy`

or

`git clone *url* && uv pip install -e .`

# Usage
1. Define a `lm_config.yaml` in your root based on `lm_config.yaml.example`
2. Define `OPENROUTER_API_KEY` in your `.env` if using openrouter
3. Create! See `example_workflow.py` for a basic workflow created using this framework

