"""A small, transparent self-healing locator for Playwright (Python).

Idea (same as commercial tools such as Healenium, Testim, mabl):
  1. Try the primary locator.
  2. If it no longer matches, try ranked fall-back strategies (test-id, role+name, text, attributes, structure).
  3. Use the first candidate that matches EXACTLY ONE element, record a 'healing event' and keep the test running.
  4. Export a report so a human can update the primary locator (healing must never hide real defects).
"""
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from playwright.sync_api import Locator, Page


@dataclass
class HealingEvent:
    name: str
    broken: str
    healed_with: str
    strategy: str


@dataclass
class HealingLog:
    events: list[HealingEvent] = field(default_factory=list)

    def save(self, path: str = "reports/healing-report.json") -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps([asdict(e) for e in self.events], indent=2))


class HealingLocator:
    def __init__(self, page: Page, log: HealingLog | None = None):
        self.page = page
        self.log = log or HealingLog()

    def find(self, name: str, primary: str, fallbacks: list[tuple[str, Locator | str]]) -> Locator:
        """
        :param name:      logical name of the element (used in the report)
        :param primary:   CSS/XPath selector that used to work
        :param fallbacks: ordered list of (strategy_label, selector_or_locator)
        """
        loc = self.page.locator(primary)
        if loc.count() == 1:
            return loc
        for label, candidate in fallbacks:
            cand = self.page.locator(candidate) if isinstance(candidate, str) else candidate
            if cand.count() == 1:  # ambiguous matches are NOT trusted
                self.log.events.append(HealingEvent(name, primary, str(candidate), label))
                return cand
        raise AssertionError(f"Could not locate '{name}': primary '{primary}' and {len(fallbacks)} fallbacks failed")
