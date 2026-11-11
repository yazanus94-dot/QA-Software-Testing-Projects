"""Deterministic offline 'LLM' so the whole suite runs without keys, network or cost.

It imitates the behaviours we want to TEST in a real model:
  * answers only from the supplied CONTEXT
  * says it doesn't know when the context is empty
  * refuses prompt-injection and requests for sensitive data
Swap it for a real model with LLM_PROVIDER=openai|anthropic|ollama - the tests stay identical.
"""
import re

UNKNOWN = "I don't have information about that."
REFUSAL = "I can't help with that request."
PII_REFUSAL = "I can't share personal or sensitive information."

INJECTION = re.compile(
    r"(ignore (all|any|the|your|previous|prior)[\w\s]*(instruction|rule|prompt)s?|system prompt|"
    r"reveal (your|the) (instruction|prompt|rule)s?|you are now|developer mode|jailbreak|"
    r"disregard (the|your) (above|previous)|act as (an? )?(unrestricted|different))", re.I)
SENSITIVE = re.compile(
    r"(credit card|card number|password|other customers?|another customer|home address|phone number of|"
    r"email address of|social security|api key)", re.I)

STOP = set("a an the is are was were do does did you your i me my we our of to in for on at and or it its this that "
           "what which who how when where why can could would should will shall be been with about any there "
           "please tell us if so as by from have has not".split())


def tokens(text: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if w in STOP:
            continue
        out.append(w[:-1] if len(w) > 3 and w.endswith("s") else w)
    return out


class MockLLM:
    name = "mock-llm"

    def complete(self, system: str, user: str) -> str:
        if INJECTION.search(user):
            return REFUSAL
        if SENSITIVE.search(user):
            return PII_REFUSAL

        m = re.search(r"CONTEXT:\n(.*?)\nEND CONTEXT", system, re.S)
        context = (m.group(1).strip() if m else "")
        if not context:
            return UNKNOWN

        q = set(tokens(user))
        best, best_score = "", 0
        for passage in (p.strip() for p in context.split("\n") if p.strip()):
            score = len(q & set(tokens(passage)))
            if score > best_score:
                best, best_score = passage, score
        return best if best_score else UNKNOWN
