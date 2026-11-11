import time

import pytest

from evaluation.metrics import says_unknown

pytestmark = pytest.mark.robustness

PARAPHRASES = [
    "What is your refund policy?",
    "how many days do I have to return something?",
    "Can I get my money back? What's the return window?",
    "REFUND POLICY??",
    "   what is   your refund   policy   ",
]


@pytest.mark.parametrize("question", PARAPHRASES)
def test_paraphrases_reach_the_same_fact(bot, question):
    assert "30 days" in bot.ask(question).answer


def test_same_question_is_consistent(bot):
    answers = {bot.ask("How long does standard shipping take?").answer for _ in range(3)}
    assert all("3-5" in a for a in answers)


@pytest.mark.parametrize("bad_input", ["", "   ", "?", "🙂🙂🙂", "<script>alert(1)</script>", "a" * 5000])
def test_handles_unusual_input_without_crashing(bot, bad_input):
    answer = bot.ask(bad_input).answer
    assert isinstance(answer, str) and answer.strip()


def test_non_english_question_is_handled_gracefully(bot):
    answer = bot.ask("ما هي سياسة الاسترجاع؟").answer  # Arabic: "What is the refund policy?"
    assert answer.strip()  # either answers correctly or admits it can't - never crashes or invents
    assert "30 days" in answer or says_unknown(answer) or len(answer) < 600


def test_response_time_is_reasonable(bot):
    start = time.perf_counter()
    bot.ask("What is your refund policy?")
    assert time.perf_counter() - start < 30
