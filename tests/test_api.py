"""MVP 2 API security integration tests (synthetic identities and fake tokens)."""

from fastapi.testclient import TestClient
import pytest

from biometric_consent.api import create_app, create_demo_app
from biometric_consent.consent import ConsentService, Principal, Role


@pytest.fixture
def api():
    service = ConsentService(
        purposes={"account-authentication", "advertising", "workplace-access"},
        client_purposes={"demo-client": {"account-authentication", "advertising"}},
    )
    tokens = {
        "fake-alice-token": Principal("alice", Role.SUBJECT, "synthetic-alice"),
        "fake-bob-token": Principal("bob", Role.SUBJECT, "synthetic-bob"),
        "fake-client-token": Principal("demo-client", Role.CLIENT),
        "fake-admin-token": Principal("admin", Role.ADMIN),
        "fake-auditor-token": Principal("auditor", Role.AUDITOR),
        "fake-unknown-client-token": Principal("other-client", Role.CLIENT),
    }
    with TestClient(create_app(service=service, token_principals=tokens)) as client:
        yield client


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def grant(api, purpose="account-authentication", token="fake-alice-token"):
    return api.post("/consents", headers=auth(token), json={"purpose": purpose})


def verify(api, purpose="account-authentication", token="fake-client-token",
           subject_id="synthetic-alice"):
    return api.post("/verifications", headers=auth(token), json={
        "subject_id": subject_id, "purpose": purpose
    })


def test_unauthenticated_requests_fail_closed(api):
    for path, method in (("/consents", "post"), ("/verifications", "post"),
                         ("/audit/events", "get")):
        request = getattr(api, method)
        response = request(path, json={"purpose": "account-authentication"}) if method == "post" else request(path)
        assert response.status_code == 401
    assert grant(api, token="unknown-token").status_code == 401


def test_health_contains_no_secrets(api):
    result = api.get("/health")
    assert result.status_code == 200
    assert result.json() == {"status": "ok"}


def test_homepage_loads(api):
    response = api.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Consent should be enforceable" in response.text
    assert 'href="/static/styles.css"' in response.text


def test_stylesheet_loads(api):
    response = api.get("/static/styles.css")

    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
    assert ":root" in response.text
    assert "--accent" in response.text

def test_consent_lifecycle_over_http(api):
    record = grant(api)
    assert record.status_code == 201
    consent_id = record.json()["consent_id"]
    assert record.json()["subject_id"] == "synthetic-alice"
    allowed = verify(api)
    assert (allowed.status_code, allowed.json()["decision"]) == (200, "allow")
    denied = verify(api, purpose="advertising")
    assert (denied.status_code, denied.json()["decision"]) == (200, "deny")
    revoked = api.post(f"/consents/{consent_id}/revoke", headers=auth("fake-alice-token"))
    assert revoked.status_code == 200
    assert revoked.json()["revoked_at"] is not None
    assert verify(api).json()["decision"] == "deny"


def test_role_spoofing_from_json_is_rejected(api):
    response = api.post("/consents", headers=auth("fake-client-token"),
                        json={"purpose": "account-authentication", "role": "subject"})
    assert response.status_code in (403, 422)
    response = api.post("/consents", headers=auth("fake-alice-token"), json={
        "purpose": "account-authentication", "subject_id": "synthetic-bob"
    })
    assert response.status_code == 422


def test_client_cannot_grant_or_revoke(api):
    record = grant(api).json()
    assert grant(api, token="fake-client-token").status_code == 403
    assert api.post(f"/consents/{record['consent_id']}/revoke",
                    headers=auth("fake-client-token")).status_code == 403


def test_admin_cannot_grant_revoke_or_audit(api):
    record = grant(api).json()
    assert grant(api, token="fake-admin-token").status_code == 403
    assert api.post(f"/consents/{record['consent_id']}/revoke",
                    headers=auth("fake-admin-token")).status_code == 403
    assert api.get("/audit/events", headers=auth("fake-admin-token")).status_code == 403


def test_subject_cannot_impersonate_or_read_another_subject(api):
    record = grant(api).json()
    url = f"/consents/{record['consent_id']}"
    assert api.get(url, headers=auth("fake-bob-token")).status_code == 403
    assert api.post(url + "/revoke", headers=auth("fake-bob-token")).status_code == 403
    assert api.get(url, headers=auth("fake-alice-token")).status_code == 200


def test_no_consent_default_deny(api):
    decision = verify(api)
    assert decision.status_code == 200
    assert decision.json()["decision"] == "deny"


def test_unregistered_client_cannot_verify(api):
    grant(api)
    response = verify(api, token="fake-unknown-client-token")
    assert response.json()["decision"] == "deny"
    assert response.json()["consent_id"] is None


def test_unapproved_client_purpose_denied(api):
    grant(api, purpose="workplace-access")
    response = verify(api, purpose="workplace-access")
    assert (response.status_code, response.json()["decision"]) == (200, "deny")
    assert response.json()["reason"] == "client-purpose-not-permitted"
    assert response.json()["consent_id"] is None


def test_duplicate_and_unknown_purpose_errors(api):
    assert grant(api).status_code == 201
    assert grant(api).status_code == 409
    assert grant(api, purpose="unknown-purpose").status_code == 422


def test_audit_events_only_for_auditor(api):
    grant(api)
    verify(api)
    assert api.get("/audit/events", headers=auth("fake-alice-token")).status_code == 403
    response = api.get("/audit/events", headers=auth("fake-auditor-token"))
    assert response.status_code == 200
    assert {event["action"] for event in response.json()} >= {"grant", "verify"}


def test_invalid_verification_payload_rejected(api):
    assert api.post("/verifications", headers=auth("fake-client-token"),
                    json={"purpose": "account-authentication"}).status_code == 422
    assert api.post("/verifications", headers=auth("fake-client-token"),
                    json={"purpose": "account-authentication", "subject_id": "synthetic-alice",
                          "role": "administrator"}).status_code == 422


def test_missing_or_duplicate_registry_is_rejected():
    service = ConsentService(purposes={"p"}, client_purposes={})
    with pytest.raises(ValueError):
        create_app(service=service, token_principals={})


def test_demo_app_requires_server_credentials(monkeypatch):
    for name in ("BIOCONSENT_SUBJECT_TOKEN", "BIOCONSENT_CLIENT_TOKEN", "BIOCONSENT_AUDITOR_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(RuntimeError):
        create_demo_app()
