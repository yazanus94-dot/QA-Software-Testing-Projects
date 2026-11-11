"""Promptfoo custom Python provider: exposes our SupportBot (whatever LLM_PROVIDER is set) to Promptfoo."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.support_bot import SupportBot  # noqa: E402

_bot = SupportBot()


def call_api(prompt, options, context):
    """Promptfoo calls this for every test case. `prompt` is the rendered user question."""
    result = _bot.ask(prompt)
    return {"output": result.answer, "metadata": {"context": result.context}}
