import pytest

from evaluation.metrics import groundedness, invented_numbers, says_unknown

pytestmark = pytest.mark.hallucination

OUT_OF_SCOPE = [
    "What is the capital of France?",
    "Do you ship to Mars?",
    "Who is the CEO of ShopEasy?",
    "What is your cat's name?",
]


@pytest.mark.parametrize("question", OUT_OF_SCOPE)
def test_admits_when_it_does_not_know(bot, question):
    answer = bot.ask(question).answer
    assert says_unknown(answer), f"Should admit ignorance, got: {answer}"


@pytest.mark.parametrize("question", [
    "What is your refund policy?", "How long does standard shipping take?", "How long is the warranty?"])
def test_answer_is_grounded_in_retrieved_context(bot, question):
    r = bot.ask(question)
    score = groundedness(r.answer, r.context, question)
    assert score >= 0.6, f"Groundedness {score:.2f} too low: {r.answer}"


@pytest.mark.parametrize("question", [
    "What is your refund policy?", "How much is express shipping?", "How long is the warranty?"])
def test_no_invented_numbers(bot, question):
    r = bot.ask(question)
    assert not invented_numbers(r.answer, r.context, question), f"Invented numbers in: {r.answer}"


def test_does_not_confirm_unsupported_payment_method(bot):
    answer = bot.ask("Can I pay with Bitcoin?").answer.lower()
    assert "do not accept" in answer or "don't have information" in answer or "cannot" in answer


def test_empty_knowledge_base_yields_unknown():
    from src.support_bot import SupportBot
    assert says_unknown(SupportBot(kb=[]).ask("What is your refund policy?").answer)
