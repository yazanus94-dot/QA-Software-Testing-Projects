# 🔌 API Testing — Postman + Newman + Database Checks + API→UI Hybrid

![Postman](https://img.shields.io/badge/Postman-collections-FF6C37) ![Newman](https://img.shields.io/badge/Newman-CLI_runner-orange) ![Pytest](https://img.shields.io/badge/Pytest-DB_checks-green) ![CI](https://img.shields.io/badge/GitHub_Actions-ready-black)

One API-testing project that combines **four layers** against the public
[Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) API:

| Layer | Tooling | What it proves |
|---|---|---|
| 1. Functional API | **Postman** collection (chained requests, JSON-schema, auth, negatives) | CRUD flow, contracts, security basics |
| 2. Data-driven | Postman + **CSV** via Newman | Many inputs, one test (unicode, apostrophes, boundaries) |
| 3. Automation & CI | **Newman** + htmlextra report + **GitHub Actions** | Tests run on every push, nightly |
| 4. API + Database | **Python / pytest** + SQLite | API responses match the persisted data; DB constraints enforce business rules |
| 5. API + UI hybrid | **pytest + Playwright** | Data created through the API is visible in the UI |

> Author: **Yazan Aljabari** | QA / Software Test Engineer

## Structure
```
postman/
  restful-booker.functional.postman_collection.json
  restful-booker.datadriven.postman_collection.json
  environments/restful-booker.postman_environment.json
  data/bookings.csv
tools/build_collections.py     generates the collections (readable, diff-friendly source)
db_checks/                     API <-> DB integrity tests (pytest)
hybrid/                        API-created data verified in the browser (manual / experimental)
docs/                          test plan, test cases, sample bug report
```

## Run it
### Postman (GUI)
Import both collections and the environment from `postman/`, select the environment, run the collection with the Collection Runner. For the data-driven one, select `postman/data/bookings.csv` as the data file.

### Newman (CLI)
```bash
npm install
npm run test:functional      # HTML report -> reports/functional-report.html
npm run test:datadriven      # one iteration per CSV row
```
### Database integrity checks
```bash
pip install -r requirements.txt
pytest -m db                 # HTML report -> reports/db-report.html
```
### Hybrid API → UI (optional)
```bash
playwright install chromium
pytest hybrid -m hybrid --headed
```
*(The hybrid test targets a different public demo app; selectors may change — treat it as a showcase.)*

## Techniques showcased
* Request chaining (`token` and `bookingId` saved to the environment)
* JSON-schema contract validation (`pm.response.to.have.jsonSchema`)
* Response-time assertions, header/status checks, authorisation negatives (403/404)
* Cleanup after tests (no leftover data)
* Collections generated from code so schemas are defined once and reused
