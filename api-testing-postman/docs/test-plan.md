# API Test Plan — Restful-Booker

## Objective
Validate functional correctness, data integrity, contract stability and basic security of the Booking API.

## Scope
Endpoints: `/ping`, `/auth`, `/booking` (GET list, GET id, POST, PUT, PATCH, DELETE).

## Approach
| Layer | Focus |
|---|---|
| Contract | JSON schema on every success response |
| Functional | Full CRUD lifecycle with chained requests |
| Data-driven | CSV input incl. unicode and special characters |
| Security | Missing/invalid token → 403, bad credentials |
| Integrity | API vs database comparison, constraint checks |
| Non-functional (light) | Response-time budget < 3 s per call |
| Hybrid | API-created data visible in UI |

## Tools
Postman, Newman + htmlextra, Python 3 + pytest + requests, SQLite, Playwright, GitHub Actions.

## Entry / exit criteria
Entry: `/ping` returns 201. Exit: all functional tests pass, no schema drift, no leftover test data.

## Risks
Shared public API (other users' data, occasional resets, rate limits) → test data uses unique names and always cleans up.
