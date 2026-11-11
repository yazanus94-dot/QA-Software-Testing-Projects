"""Generates the Postman collections (JSON) so they stay readable and diff-friendly.

Run:  python tools/build_collections.py
Target API: Restful-Booker (https://restful-booker.herokuapp.com)
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "postman"

BOOKING_SCHEMA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {"checkin": {"type": "string"}, "checkout": {"type": "string"}},
        },
        "additionalneeds": {"type": "string"},
    },
}
CREATE_SCHEMA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {"bookingid": {"type": "integer"}, "booking": BOOKING_SCHEMA},
}
IDS_SCHEMA = {
    "type": "array",
    "items": {"type": "object", "required": ["bookingid"], "properties": {"bookingid": {"type": "integer"}}},
}

JSON_HDR = [{"key": "Content-Type", "value": "application/json"}, {"key": "Accept", "value": "application/json"}]
AUTH_HDR = JSON_HDR + [{"key": "Cookie", "value": "token={{token}}"}]

BODY = (
    '{\n  "firstname": "{{firstname}}",\n  "lastname": "{{lastname}}",\n  "totalprice": {{totalprice}},\n'
    '  "depositpaid": {{depositpaid}},\n  "bookingdates": {"checkin": "{{checkin}}", "checkout": "{{checkout}}"},\n'
    '  "additionalneeds": "{{additionalneeds}}"\n}'
)


def req(name, method, path, tests, headers=None, body=None, pre=None):
    r = {"method": method, "header": headers or [], "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"], "path": [p for p in path.strip("/").split("/") if p]}}
    if body is not None:
        r["body"] = {"mode": "raw", "raw": body, "options": {"raw": {"language": "json"}}}
    events = [{"listen": "test", "script": {"type": "text/javascript", "exec": tests}}]
    if pre:
        events.append({"listen": "prerequest", "script": {"type": "text/javascript", "exec": pre}})
    return {"name": name, "event": events, "request": r}


def schema_js(schema):
    return "const schema = " + json.dumps(schema) + ";"


COMMON = [
    "pm.test('Response time < 3000 ms', () => pm.expect(pm.response.responseTime).to.be.below(3000));",
]

DEFAULT_VARS = [
    {"key": k, "value": v} for k, v in {
        "firstname": "Yazan", "lastname": "Tester", "totalprice": "150", "depositpaid": "true",
        "checkin": "2026-11-01", "checkout": "2026-11-05", "additionalneeds": "Breakfast",
    }.items()
]  # collection variables = defaults; CSV iteration data overrides them automatically

functional = {
    "variable": DEFAULT_VARS,
    "info": {
        "name": "Restful-Booker — Functional API Suite",
        "description": "End-to-end CRUD flow with chained requests, schema validation, auth, negative tests.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "item": [
        {"name": "01 Health", "item": [
            req("GET /ping", "GET", "/ping", [
                "pm.test('Status is 201 Created (service healthy)', () => pm.response.to.have.status(201));", *COMMON]),
        ]},
        {"name": "02 Auth", "item": [
            req("POST /auth (valid)", "POST", "/auth", [
                "pm.test('Status 200', () => pm.response.to.have.status(200));",
                "const token = pm.response.json().token;",
                "pm.test('Token returned', () => pm.expect(token).to.be.a('string').and.not.empty);",
                "pm.environment.set('token', token);", *COMMON],
                JSON_HDR, '{"username": "{{username}}", "password": "{{password}}"}'),
            req("POST /auth (bad credentials)", "POST", "/auth", [
                "pm.test('API answers 200 with a failure reason', () => {",
                "  pm.response.to.have.status(200);",
                "  pm.expect(pm.response.json().reason).to.eql('Bad credentials');",
                "  pm.expect(pm.response.json()).to.not.have.property('token');",
                "});"], JSON_HDR, '{"username": "admin", "password": "wrong"}'),
        ]},
        {"name": "03 Booking CRUD", "item": [
            req("POST /booking (create)", "POST", "/booking", [
                "pm.test('Status 200', () => pm.response.to.have.status(200));",
                schema_js(CREATE_SCHEMA),
                "pm.test('Matches JSON schema', () => pm.response.to.have.jsonSchema(schema));",
                "const res = pm.response.json();",
                "pm.test('Echoes the data we sent', () => {",
                "  pm.expect(res.booking.firstname).to.eql(pm.variables.get('firstname'));",
                "  pm.expect(res.booking.lastname).to.eql(pm.variables.get('lastname'));",
                "});",
                "pm.environment.set('bookingId', res.bookingid);", *COMMON],
                JSON_HDR, BODY),
            req("GET /booking (list ids)", "GET", "/booking", [
                "pm.test('Status 200', () => pm.response.to.have.status(200));",
                schema_js(IDS_SCHEMA),
                "pm.test('Matches JSON schema', () => pm.response.to.have.jsonSchema(schema));",
                "pm.test('Contains the booking we created', () => {",
                "  const ids = pm.response.json().map(b => b.bookingid);",
                "  pm.expect(ids).to.include(Number(pm.environment.get('bookingId')));",
                "});"], JSON_HDR),
            req("GET /booking/:id", "GET", "/booking/{{bookingId}}", [
                "pm.test('Status 200', () => pm.response.to.have.status(200));",
                schema_js(BOOKING_SCHEMA),
                "pm.test('Matches JSON schema', () => pm.response.to.have.jsonSchema(schema));",
                "pm.test('Dates are logical (checkout >= checkin)', () => {",
                "  const b = pm.response.json().bookingdates;",
                "  pm.expect(new Date(b.checkout) >= new Date(b.checkin)).to.be.true;",
                "});", *COMMON], JSON_HDR),
            req("PUT /booking/:id (full update)", "PUT", "/booking/{{bookingId}}", [
                "pm.test('Status 200', () => pm.response.to.have.status(200));",
                "pm.test('Name updated', () => pm.expect(pm.response.json().firstname).to.eql('Updated'));"],
                AUTH_HDR,
                BODY.replace('{{firstname}}', 'Updated')),
            req("PATCH /booking/:id (partial update)", "PATCH", "/booking/{{bookingId}}", [
                "pm.test('Status 200', () => pm.response.to.have.status(200));",
                "pm.test('Only price changed', () => {",
                "  const b = pm.response.json();",
                "  pm.expect(b.totalprice).to.eql(999);",
                "  pm.expect(b.firstname).to.eql('Updated');",
                "});"], AUTH_HDR, '{"totalprice": 999}'),
            req("DELETE /booking/:id", "DELETE", "/booking/{{bookingId}}", [
                "pm.test('Status 201 Created (delete accepted)', () => pm.response.to.have.status(201));"], AUTH_HDR),
            req("GET /booking/:id (after delete → 404)", "GET", "/booking/{{bookingId}}", [
                "pm.test('Deleted booking is gone (404)', () => pm.response.to.have.status(404));"], JSON_HDR),
        ]},
        {"name": "04 Negative & security", "item": [
            req("PUT without token → 403", "PUT", "/booking/1", [
                "pm.test('Forbidden without auth', () => pm.response.to.have.status(403));"], JSON_HDR, '{"firstname":"x"}'),
            req("DELETE without token → 403", "DELETE", "/booking/1", [
                "pm.test('Forbidden without auth', () => pm.response.to.have.status(403));"], JSON_HDR),
            req("GET unknown id → 404", "GET", "/booking/99999999", [
                "pm.test('Not found', () => pm.response.to.have.status(404));"], JSON_HDR),
            req("POST malformed body → client/server error", "POST", "/booking", [
                "pm.test('Rejected (4xx/5xx)', () => pm.expect(pm.response.code).to.be.within(400, 599));"],
                JSON_HDR, '{"firstname": '),
        ]},
    ],
}

data_driven = {
    "info": {
        "name": "Restful-Booker — Data-Driven Create Booking",
        "description": "Run with: newman run ... -d postman/data/bookings.csv. One iteration per CSV row.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "item": [
        req("POST /booking (CSV row)", "POST", "/booking", [
            "pm.test('Status 200', () => pm.response.to.have.status(200));",
            schema_js(CREATE_SCHEMA),
            "pm.test('Matches JSON schema', () => pm.response.to.have.jsonSchema(schema));",
            "const b = pm.response.json().booking;",
            "pm.test('Data from CSV round-trips correctly', () => {",
            "  pm.expect(b.firstname).to.eql(pm.iterationData.get('firstname'));",
            "  pm.expect(b.lastname).to.eql(pm.iterationData.get('lastname'));",
            "  pm.expect(b.totalprice).to.eql(Number(pm.iterationData.get('totalprice')));",
            "  pm.expect(b.bookingdates.checkin).to.eql(pm.iterationData.get('checkin'));",
            "});"], JSON_HDR, BODY),
    ],
}

env = {
    "name": "Restful-Booker (public)",
    "values": [
        {"key": "baseUrl", "value": "https://restful-booker.herokuapp.com", "enabled": True},
        {"key": "username", "value": "admin", "enabled": True},
        {"key": "password", "value": "password123", "enabled": True},
        {"key": "token", "value": "", "enabled": True},
        {"key": "bookingId", "value": "", "enabled": True},
    ],
}

(OUT / "restful-booker.functional.postman_collection.json").write_text(json.dumps(functional, indent=2))
(OUT / "restful-booker.datadriven.postman_collection.json").write_text(json.dumps(data_driven, indent=2))
(OUT / "environments" / "restful-booker.postman_environment.json").write_text(json.dumps(env, indent=2))
print("Collections written to", OUT)
