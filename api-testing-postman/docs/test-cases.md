# Test Cases

| ID | Endpoint | Scenario | Expected | Type |
|---|---|---|---|---|
| API-001 | GET /ping | Health check | 201 | Smoke |
| API-002 | POST /auth | Valid credentials | 200 + token | Functional |
| API-003 | POST /auth | Bad credentials | 200 + `reason: Bad credentials`, no token | Negative |
| API-010 | POST /booking | Create booking | 200, schema valid, data echoed | Functional |
| API-011 | GET /booking | List ids contains new booking | 200, schema valid | Functional |
| API-012 | GET /booking/:id | Read booking | 200, schema valid, checkout ≥ checkin | Functional |
| API-013 | PUT /booking/:id | Full update with token | 200, fields updated | Functional |
| API-014 | PATCH /booking/:id | Partial update | 200, only price changed | Functional |
| API-015 | DELETE /booking/:id | Delete with token | 201 | Functional |
| API-016 | GET /booking/:id | After delete | 404 | Functional |
| API-020 | PUT | No token | 403 | Security |
| API-021 | DELETE | No token | 403 | Security |
| API-022 | GET /booking/99999999 | Unknown id | 404 | Negative |
| API-023 | POST /booking | Malformed JSON | 4xx/5xx | Negative |
| API-030 | POST /booking (CSV x5) | Data-driven creation | Echoed values equal CSV | Data-driven |
| DB-001 | API→DB | Persisted row equals created booking | Equal | Integrity |
| DB-002 | API vs DB | Fresh API read equals DB row | Equal | Integrity |
| DB-003 | Delete | Gone from API and DB | 404 / no row | Integrity |
| DB-004 | POST x3 | IDs are unique | Unique | Integrity |
| DB-005 | DB constraints | checkout<checkin / negative price rejected | IntegrityError | Business rule |
| HYB-001 | API→UI | Booking created via API visible in admin UI | Visible | Hybrid |
