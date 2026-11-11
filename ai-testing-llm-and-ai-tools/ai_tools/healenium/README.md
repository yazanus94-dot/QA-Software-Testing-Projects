# Healenium — open-source self-healing for Selenium

Healenium sits between your Selenium test and the browser. When a locator fails, it compares the current DOM
with the last known-good DOM (stored in a database), picks the closest matching element using a tree-comparison
algorithm and continues the test — and it produces a report with the "healed" locators.

```
Test ──► Healenium proxy/wrapper ──► WebDriver
              │  (locator failed?)
              ▼
        Healenium backend + Postgres  (stores selectors, finds nearest match, reports)
```

## How to use it (Java / Selenium example)
```java
WebDriver delegate = new ChromeDriver();
SelfHealingDriver driver = SelfHealingDriver.create(delegate);   // wrap the normal driver
driver.get("https://www.saucedemo.com");
driver.findElement(By.id("login-button")).click();               // heals if the id changes later
```
Dependencies, docker-compose and the Python/other-language options are documented in the official repository:
<https://github.com/healenium/healenium> (use the compose file from the release you install).

## Where it fits in this portfolio
* `ai_tools/self_healing/` — a transparent Python implementation of the same idea (works offline, shows the logic)
* `ai_tools/visual_ai/` — Applitools Visual AI
* Key lesson: **healing reduces maintenance, but every healed locator must be reviewed** — otherwise real UI regressions get hidden.
