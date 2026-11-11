import pytest

pytestmark = pytest.mark.functional

CASES = [
    ("What is your refund policy?", ["30 days"]),
    ("How long does standard shipping take?", ["3-5 business days"]),
    ("How much is express shipping?", ["$15"]),
    ("When is customer support available?", ["Monday to Friday"]),
    ("How long is the warranty on electronics?", ["12-month"]),
    ("Which payment methods do you accept?", ["Visa", "PayPal"]),
]


@pytest.mark.parametrize("question,expected", CASES, ids=[c[0] for c in CASES])
def test_answers_contain_the_key_fact(bot, question, expected):
    result = bot.ask(question)
    for fact in expected:
        assert fact.lower() in result.answer.lower(), f"Missing '{fact}' in: {result.answer}"


def test_answer_is_concise(bot):
    assert len(bot.ask("What is your refund policy?").answer) < 600


def test_retrieval_finds_the_right_document(bot):
    ctx = bot.ask("Can I return an item for a refund?").context
    assert ctx and "Refunds" in ctx[0]
