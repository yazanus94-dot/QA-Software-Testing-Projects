"""LLM-as-a-judge evaluation with DeepEval (https://github.com/confident-ai/deepeval).

Needs a REAL provider to act as the judge (LLM_PROVIDER=openai|anthropic|ollama), so it is skipped on the
offline mock. The judge model is any LLM from `src.llm_client` wrapped in DeepEval's custom-model interface.
"""
import json

import pytest

from src.llm_client import get_llm, provider_name

pytestmark = pytest.mark.deepeval

deepeval = pytest.importorskip("deepeval", reason="pip install deepeval")
if provider_name() == "mock":
    pytest.skip("DeepEval needs a real judge LLM: set LLM_PROVIDER", allow_module_level=True)

from deepeval import assert_test  # noqa: E402
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric  # noqa: E402
from deepeval.models import DeepEvalBaseLLM  # noqa: E402
from deepeval.test_case import LLMTestCase  # noqa: E402


class JudgeLLM(DeepEvalBaseLLM):
    """Adapter: use whichever provider we configured as the DeepEval judge."""

    def __init__(self):
        self.llm = get_llm()

    def load_model(self):
        return self.llm

    def generate(self, prompt: str, schema=None):
        text = self.llm.complete("You are a strict evaluator. Reply with valid JSON only when asked.", prompt)
        if schema is not None:
            return schema(**json.loads(text[text.index("{"): text.rindex("}") + 1]))
        return text

    async def a_generate(self, prompt: str, schema=None):
        return self.generate(prompt, schema)

    def get_model_name(self):
        return self.llm.name


@pytest.fixture(scope="module")
def judge():
    return JudgeLLM()


@pytest.mark.parametrize("question", ["What is your refund policy?", "How long does standard shipping take?"])
def test_answer_relevancy_and_faithfulness(bot, judge, question):
    r = bot.ask(question)
    case = LLMTestCase(input=question, actual_output=r.answer, retrieval_context=r.context)
    assert_test(case, [AnswerRelevancyMetric(threshold=0.7, model=judge),
                       FaithfulnessMetric(threshold=0.7, model=judge)])
