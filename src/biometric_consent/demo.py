"""Command-line demonstration with synthetic identities only."""

from .consent import ConsentService, Principal, Role


def main() -> None:
    service = ConsentService(
        purposes={"account-authentication", "advertising"},
        client_purposes={"demo-client": {"account-authentication", "advertising"}},
    )
    subject = Principal("synthetic-subject-001", Role.SUBJECT, "synthetic-subject-001")
    client = Principal("demo-client", Role.CLIENT)
    auditor = Principal("demo-auditor", Role.AUDITOR)

    record = service.grant(actor=subject, purpose="account-authentication")
    allowed = service.verify(actor=client, subject_id=subject.subject_id or "", purpose="account-authentication")
    wrong_purpose = service.verify(actor=client, subject_id=subject.subject_id or "", purpose="advertising")
    service.revoke(actor=subject, consent_id=record.consent_id)
    revoked = service.verify(actor=client, subject_id=subject.subject_id or "", purpose="account-authentication")

    print("Cloud-Native Biometric Consent and Audit — MVP 1")
    print("All identifiers below are synthetic; no biometric data is stored.")
    print(f"Approved purpose before revocation: {allowed.decision.upper()} ({allowed.reason})")
    print(f"Different purpose: {wrong_purpose.decision.upper()} ({wrong_purpose.reason})")
    print(f"Approved purpose after revocation: {revoked.decision.upper()} ({revoked.reason})")
    print(f"Recorded audit events: {len(service.audit_events(actor=auditor))}")


if __name__ == "__main__":
    main()
