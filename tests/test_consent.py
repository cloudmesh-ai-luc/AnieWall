"""MVP 1 security and lifecycle regression tests (synthetic data only)."""

from datetime import datetime, timezone

import pytest

from biometric_consent.consent import (
    ConsentConflict,
    ConsentNotFound,
    ConsentService,
    NotAuthorized,
    Principal,
    Role,
)


@pytest.fixture
def setup():
    svc = ConsentService(
        purposes={"account-authentication", "advertising", "workplace-access"},
        client_purposes={
            "demo-client": {"account-authentication", "advertising"},
            "door-client": {"workplace-access"},
        },
        clock=lambda: datetime(2026, 11, 18, tzinfo=timezone.utc),
    )
    alice = Principal("alice", Role.SUBJECT, "synthetic-alice")
    bob = Principal("bob", Role.SUBJECT, "synthetic-bob")
    client = Principal("demo-client", Role.CLIENT)
    admin = Principal("admin", Role.ADMIN)
    auditor = Principal("auditor", Role.AUDITOR)
    return svc, alice, bob, client, admin, auditor


def test_active_matching_consent_allows(setup):
    svc, alice, _, client, _, _ = setup
    svc.grant(actor=alice, purpose="account-authentication")
    decision = svc.verify(actor=client, subject_id=alice.subject_id, purpose="account-authentication")
    assert decision.decision == "allow"
    assert decision.reason == "active-purpose-matched"


def test_unapproved_purpose_denied(setup):
    svc, alice, _, client, _, _ = setup
    svc.grant(actor=alice, purpose="account-authentication")
    decision = svc.verify(actor=client, subject_id=alice.subject_id, purpose="advertising")
    assert (decision.decision, decision.reason) == ("deny", "no-consent")


def test_missing_consent_denied(setup):
    svc, alice, _, client, _, _ = setup
    assert svc.verify(actor=client, subject_id=alice.subject_id, purpose="account-authentication").decision == "deny"


def test_revocation_denies_future_verification(setup):
    svc, alice, _, client, _, _ = setup
    record = svc.grant(actor=alice, purpose="account-authentication")
    assert svc.verify(actor=client, subject_id=alice.subject_id, purpose="account-authentication").decision == "allow"
    revoked = svc.revoke(actor=alice, consent_id=record.consent_id)
    assert not revoked.active
    decision = svc.verify(actor=client, subject_id=alice.subject_id, purpose="account-authentication")
    assert (decision.decision, decision.reason) == ("deny", "revoked")


def test_regrant_after_revocation_requires_new_consent(setup):
    svc, alice, _, client, _, _ = setup
    old = svc.grant(actor=alice, purpose="account-authentication")
    svc.revoke(actor=alice, consent_id=old.consent_id)
    new = svc.grant(actor=alice, purpose="account-authentication")
    assert old.consent_id != new.consent_id
    assert svc.verify(actor=client, subject_id=alice.subject_id, purpose="account-authentication").consent_id == new.consent_id


def test_cannot_duplicate_active_grant(setup):
    svc, alice, *_ = setup
    svc.grant(actor=alice, purpose="account-authentication")
    with pytest.raises(ConsentConflict):
        svc.grant(actor=alice, purpose="account-authentication")


def test_unknown_grant_purpose_rejected(setup):
    svc, alice, *_ = setup
    with pytest.raises(ValueError):
        svc.grant(actor=alice, purpose="secret-profiling")


def test_unregistered_client_denied(setup):
    svc, alice, *_ = setup
    svc.grant(actor=alice, purpose="account-authentication")
    stranger = Principal("unknown-client", Role.CLIENT)
    result = svc.verify(actor=stranger, subject_id=alice.subject_id, purpose="account-authentication")
    assert (result.decision, result.reason, result.consent_id) == ("deny", "unregistered-client", None)


def test_client_cannot_use_unapproved_purpose(setup):
    svc, alice, *_ = setup
    svc.grant(actor=alice, purpose="workplace-access")
    unauthorized_client = Principal("demo-client", Role.CLIENT)
    result = svc.verify(actor=unauthorized_client, subject_id=alice.subject_id, purpose="workplace-access")
    assert (result.decision, result.reason, result.consent_id) == ("deny", "client-purpose-not-permitted", None)


def test_different_subject_cannot_revoke(setup):
    svc, alice, bob, *_ = setup
    record = svc.grant(actor=alice, purpose="account-authentication")
    with pytest.raises(NotAuthorized):
        svc.revoke(actor=bob, consent_id=record.consent_id)
    assert svc.get_consent(actor=alice, consent_id=record.consent_id).active


def test_admin_cannot_override_or_revoke(setup):
    svc, alice, _, client, admin, _ = setup
    record = svc.grant(actor=alice, purpose="account-authentication")
    with pytest.raises(NotAuthorized):
        svc.revoke(actor=admin, consent_id=record.consent_id)
    with pytest.raises(NotAuthorized):
        svc.grant(actor=admin, purpose="advertising")
    assert svc.verify(actor=client, subject_id=alice.subject_id, purpose="advertising").decision == "deny"


def test_admin_cannot_read_subject_record(setup):
    svc, alice, _, _, admin, _ = setup
    record = svc.grant(actor=alice, purpose="account-authentication")
    with pytest.raises(NotAuthorized):
        svc.get_consent(actor=admin, consent_id=record.consent_id)


def test_read_audit_requires_auditor(setup):
    svc, alice, _, _, admin, auditor = setup
    svc.grant(actor=alice, purpose="account-authentication")
    with pytest.raises(NotAuthorized):
        svc.audit_events(actor=admin)
    events = svc.audit_events(actor=auditor)
    assert all(e.sequence == i for i, e in enumerate(events, start=1))
    assert any(e.action == "read-audit" and e.outcome == "deny" for e in events)
    assert isinstance(events, tuple)


def test_denied_verification_audited(setup):
    svc, alice, _, client, _, auditor = setup
    svc.verify(actor=client, subject_id=alice.subject_id, purpose="account-authentication")
    assert any(e.action == "verify" and e.outcome == "deny" for e in svc.audit_events(actor=auditor))


def test_revocation_retains_audit_history(setup):
    svc, alice, _, client, _, auditor = setup
    record = svc.grant(actor=alice, purpose="account-authentication")
    svc.revoke(actor=alice, consent_id=record.consent_id)
    svc.verify(actor=client, subject_id=alice.subject_id, purpose="account-authentication")
    events = svc.audit_events(actor=auditor)
    assert [e.action for e in events[:3]] == ["grant", "revoke", "verify"]
    assert [e.outcome for e in events[:3]] == ["allow", "allow", "deny"]


def test_revocation_is_idempotent(setup):
    svc, alice, *_ = setup
    record = svc.grant(actor=alice, purpose="account-authentication")
    first = svc.revoke(actor=alice, consent_id=record.consent_id)
    second = svc.revoke(actor=alice, consent_id=record.consent_id)
    assert first == second


def test_unknown_consent_id_rejected(setup):
    svc, alice, *_ = setup
    with pytest.raises(ConsentNotFound):
        svc.revoke(actor=alice, consent_id="not-a-real-consent")


def test_purpose_is_exact_match_not_llm_interpreted(setup):
    svc, alice, _, client, _, _ = setup
    svc.grant(actor=alice, purpose="account-authentication")
    wrong_case = svc.verify(actor=client, subject_id=alice.subject_id, purpose="Account-Authentication")
    assert wrong_case.decision == "deny"


def test_grant_requires_subject_identity(setup):
    svc, *_ = setup
    with pytest.raises(NotAuthorized):
        svc.grant(actor=Principal("anonymous", Role.SUBJECT), purpose="account-authentication")


def test_invalid_client_permission_configuration():
    with pytest.raises(ValueError):
        ConsentService(purposes={"account-authentication"},
                       client_purposes={"client": {"advertising"}})


def test_reject_naive_clock():
    service = ConsentService(purposes={"account-authentication"},
                             client_purposes={}, clock=lambda: datetime(2026, 11, 18))
    with pytest.raises(ValueError):
        service.grant(actor=Principal("a", Role.SUBJECT, "a"), purpose="account-authentication")
