import pytest

from src.llm_client import provider_name
from src.support_bot import SupportBot


@pytest.fixture(scope="session")
def bot() -> SupportBot:
    return SupportBot()


@pytest.fixture(scope="session")
def provider() -> str:
    return provider_name()
