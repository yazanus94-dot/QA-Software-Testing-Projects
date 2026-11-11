# Sample Bug Report

| Field | Value |
|---|---|
| **ID** | BUG-API-004 |
| **Title** | `POST /auth` returns HTTP 200 for invalid credentials |
| **Severity / Priority** | Medium / Medium |
| **Environment** | https://restful-booker.herokuapp.com, Postman 11 / Newman 6 |
| **Reported by** | YOUR NAME |

### Request
```http
POST /auth
Content-Type: application/json

{"username": "admin", "password": "wrong"}
```
### Expected result
HTTP **401 Unauthorized** with an error body.

### Actual result
HTTP **200 OK** with body `{"reason": "Bad credentials"}`.

### Impact
Clients that rely on status codes will treat failed logins as successful. The test `POST /auth (bad credentials)` documents the current behaviour; update it when the status code is fixed.

> *Real, observable behaviour of the demo API — used as a portfolio example of a REST-semantics defect.*
