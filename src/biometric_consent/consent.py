"""Deterministic consent lifecycle engine using synthetic identities.

MVP-1 is an in-memory educational prototype, NOT a production authorization
service. The caller supplies Principal objects; an authenticated boundary must
construct those principals before this can be exposed as a network API.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Callable, Iterable, Mapping
from uuid import uuid4


class Role(str, Enum):
    SUBJECT = "subject"
    CLIENT = "relying-client"
    ADMIN = "administrator"
    AUDITOR = "auditor"


class ConsentError(Exception):
    """Base class for lifecycle errors."""


class NotAuthorized(ConsentError):
    """The supplied principal is not authorized for this operation."""


class ConsentConflict(ConsentError):
    """An active consent already exists for the same subject and purpose."""


class ConsentNotFound(ConsentError):
    """A consent identifier does not exist."""


@dataclass(frozen=True)
class Principal:
    actor_id: str
    role: Role
    subject_id: str | None = None


@dataclass(frozen=True)
class ConsentRecord:
    consent_id: str
    subject_id: str
    purpose: str
    created_at: datetime
    revoked_at: datetime | None = None

    @property
    def active(self) -> bool:
        return self.revoked_at is None


@dataclass(frozen=True)
class Decision:
    decision: str
    reason: str
    subject_id: str
    purpose: str
    consent_id: str | None = None


@dataclass(frozen=True)
class AuditEvent:
    sequence: int
    occurred_at: datetime
    action: str
    actor_id: str
    actor_role: str
    subject_id: str | None
    purpose: str | None
    consent_id: str | None
    outcome: str
    reason: str


class ConsentService:
    """In-memory prototype enforcing purpose, role and revocation rules.

    Client-purpose assignments are trusted configuration, not user-submitted
    API request fields. Audit events are append-only through this interface,
    but not tamper-proof or durable across process restarts.
    """

    def __init__(
        self,
        *,
        purposes: Iterable[str],
        client_purposes: Mapping[str, Iterable[str]],
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._purposes = frozenset(purposes)
        if not self._purposes or any(not p or not isinstance(p, str) for p in self._purposes):
            raise ValueError("At least one nonempty consent purpose is required")
        self._client_purposes = {
            client: frozenset(allowed) for client, allowed in client_purposes.items()
        }
        for allowed in self._client_purposes.values():
            if not allowed <= self._purposes:
                raise ValueError("Client purpose permissions must be configured purposes")
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._records: dict[str, ConsentRecord] = {}
        self._latest: dict[tuple[str, str], str] = {}
        self._events: list[AuditEvent] = []
        self._lock = RLock()

    def _now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Clock must return timezone-aware timestamps")
        return now

    def _audit(
        self,
        actor: Principal,
        action: str,
        outcome: str,
        reason: str,
        *,
        subject_id: str | None = None,
        purpose: str | None = None,
        consent_id: str | None = None,
    ) -> None:
        self._events.append(
            AuditEvent(
                sequence=len(self._events) + 1,
                occurred_at=self._now(),
                action=action,
                actor_id=actor.actor_id,
                actor_role=actor.role.value,
                subject_id=subject_id,
                purpose=purpose,
                consent_id=consent_id,
                outcome=outcome,
                reason=reason,
            )
        )

    def _require_subject(
        self, actor: Principal, subject_id: str, *, action: str, purpose: str | None = None,
        consent_id: str | None = None,
    ) -> None:
        if (actor.role is not Role.SUBJECT or not actor.subject_id
                or actor.subject_id != subject_id):
            self._audit(actor, action, "deny", "subject-authorization-failed",
                        subject_id=subject_id, purpose=purpose, consent_id=consent_id)
            raise NotAuthorized("Only the data subject can change their consent")

    def grant(self, *, actor: Principal, purpose: str) -> ConsentRecord:
        """Create explicit active consent for a configured purpose."""
        with self._lock:
            if actor.role is not Role.SUBJECT or not actor.subject_id:
                self._audit(actor, "grant", "deny", "subject-authorization-failed", purpose=purpose)
                raise NotAuthorized("Only an identified subject may grant consent")
            if purpose not in self._purposes:
                self._audit(actor, "grant", "deny", "unsupported-purpose",
                            subject_id=actor.subject_id, purpose=purpose)
                raise ValueError("Purpose must be explicitly configured")
            key = (actor.subject_id, purpose)
            previous = self._records.get(self._latest[key]) if key in self._latest else None
            if previous is not None and previous.active:
                self._audit(actor, "grant", "deny", "already-active",
                            subject_id=actor.subject_id, purpose=purpose,
                            consent_id=previous.consent_id)
                raise ConsentConflict("Active consent already exists")
            record = ConsentRecord(
                consent_id=str(uuid4()),
                subject_id=actor.subject_id,
                purpose=purpose,
                created_at=self._now(),
            )
            self._records[record.consent_id] = record
            self._latest[key] = record.consent_id
            self._audit(actor, "grant", "allow", "explicit-consent-recorded",
                        subject_id=record.subject_id, purpose=purpose,
                        consent_id=record.consent_id)
            return record

    def revoke(self, *, actor: Principal, consent_id: str) -> ConsentRecord:
        """Only the original subject may revoke; repeated revocation is idempotent."""
        with self._lock:
            record = self._records.get(consent_id)
            if record is None:
                self._audit(actor, "revoke", "deny", "unknown-consent", consent_id=consent_id)
                raise ConsentNotFound("Consent identifier not found")
            self._require_subject(actor, record.subject_id, action="revoke",
                                  purpose=record.purpose, consent_id=consent_id)
            if record.revoked_at is not None:
                self._audit(actor, "revoke", "allow", "already-revoked",
                            subject_id=record.subject_id, purpose=record.purpose,
                            consent_id=consent_id)
                return record
            updated = replace(record, revoked_at=self._now())
            self._records[consent_id] = updated
            self._audit(actor, "revoke", "allow", "consent-revoked",
                        subject_id=record.subject_id, purpose=record.purpose,
                        consent_id=consent_id)
            return updated

    def verify(self, *, actor: Principal, subject_id: str, purpose: str) -> Decision:
        """Deny by default; no LLM output can influence the decision."""
        with self._lock:
            consent_id = None
            if actor.role is not Role.CLIENT or actor.actor_id not in self._client_purposes:
                reason = "unregistered-client"
            elif purpose not in self._client_purposes[actor.actor_id]:
                reason = "client-purpose-not-permitted"
            elif not subject_id or purpose not in self._purposes:
                reason = "invalid-subject-or-purpose"
            else:
                key = (subject_id, purpose)
                consent_id = self._latest.get(key)
                record = self._records.get(consent_id) if consent_id is not None else None
                if record is None:
                    reason = "no-consent"
                elif not record.active:
                    reason = "revoked"
                else:
                    reason = "active-purpose-matched"
            outcome = "allow" if reason == "active-purpose-matched" else "deny"
            # Never reveal a consent identifier to an unauthorized client.
            if reason in ("unregistered-client", "client-purpose-not-permitted"):
                consent_id = None
            self._audit(actor, "verify", outcome, reason,
                        subject_id=subject_id, purpose=purpose, consent_id=consent_id)
            return Decision(outcome, reason, subject_id, purpose, consent_id)

    def get_consent(self, *, actor: Principal, consent_id: str) -> ConsentRecord:
        with self._lock:
            record = self._records.get(consent_id)
            if record is None:
                self._audit(actor, "read-consent", "deny", "unknown-consent", consent_id=consent_id)
                raise ConsentNotFound("Consent identifier not found")
            self._require_subject(actor, record.subject_id, action="read-consent",
                                  purpose=record.purpose, consent_id=consent_id)
            self._audit(actor, "read-consent", "allow", "subject-access",
                        subject_id=record.subject_id, purpose=record.purpose,
                        consent_id=consent_id)
            return record

    def audit_events(self, *, actor: Principal) -> tuple[AuditEvent, ...]:
        """Return an immutable snapshot only to the designated auditor role."""
        with self._lock:
            if actor.role is not Role.AUDITOR:
                self._audit(actor, "read-audit", "deny", "auditor-role-required")
                raise NotAuthorized("Auditor role is required")
            self._audit(actor, "read-audit", "allow", "auditor-access")
            return tuple(self._events)
