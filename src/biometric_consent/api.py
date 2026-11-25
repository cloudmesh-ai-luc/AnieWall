"""MVP 2: locally scoped, authenticated HTTP boundary for the consent engine.

This is an educational prototype using externally supplied bearer-token identities,
NOT a production identity provider. Bind only to loopback for demonstrations;
never expose this in a public cloud without production authentication, HTTPS,
rate limiting, durable storage, and protected audit infrastructure.
"""

from __future__ import annotations

import os
import secrets
from dataclasses import asdict
from typing import Mapping

from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field
from fastapi.staticfiles import StaticFiles

from .consent import (
    ConsentConflict,
    ConsentNotFound,
    ConsentService,
    NotAuthorized,
    Principal,
    Role,
)


class GrantRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    purpose: str = Field(min_length=1)


class VerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subject_id: str = Field(min_length=1)
    purpose: str = Field(min_length=1)


def create_app(*, service: ConsentService, token_principals: Mapping[str, Principal]) -> FastAPI:
    """Build the API from trusted, server-side credentials (never request JSON).

    The token registry is copied at startup; clients cannot supply their role,
    identity, or purpose permissions through HTTP requests. Configuration
    and bearer tokens are intentionally not logged or returned by the service.
    """
    if not token_principals or any(
        not isinstance(token, str) or not token or not isinstance(actor, Principal)
        for token, actor in token_principals.items()
    ):
        raise ValueError("A nonempty, trusted token-to-principal mapping is required")

    registry = dict(token_principals)
    bearer = HTTPBearer(auto_error=False)
    app = FastAPI(
        title="Biometric Consent & Audit (MVP 2)",
        description="Local synthetic-data educational prototype; not production authentication.",
        version="0.2.0",
    )
    
    app.mount("/static", StaticFiles(directory=Path(__file__).parent / "web"), name="static")

    @app.get("/", response_class=FileResponse, include_in_schema=False)
    def homepage() -> FileResponse:
        page = Path(__file__).parent / "web" / "index.html"
        return FileResponse(page)
    
    def get_principal(
        authorization: HTTPAuthorizationCredentials | None = Depends(bearer),
    ) -> Principal:
        if authorization is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        # Avoid ordinary string comparison when checking bearer credentials.
        for expected_token, principal in registry.items():
            if secrets.compare_digest(authorization.credentials, expected_token):
                return principal
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    def require_role(actor: Principal, role: Role) -> None:
        if actor.role is not role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/consents", status_code=status.HTTP_201_CREATED, tags=["consent"])
    def grant(payload: GrantRequest, actor: Principal = Depends(get_principal)) -> dict:
        require_role(actor, Role.SUBJECT)
        try:
            return asdict(service.grant(actor=actor, purpose=payload.purpose))
        except ConsentConflict as exc:
            raise HTTPException(status_code=409, detail="Consent already active") from exc
        except (ValueError, NotAuthorized) as exc:
            raise HTTPException(status_code=422 if isinstance(exc, ValueError) else 403,
                                detail="Invalid consent request" if isinstance(exc, ValueError) else "Forbidden") from exc

    @app.get("/consents/{consent_id}", tags=["consent"])
    def get_consent(consent_id: str, actor: Principal = Depends(get_principal)) -> dict:
        require_role(actor, Role.SUBJECT)
        try:
            return asdict(service.get_consent(actor=actor, consent_id=consent_id))
        except ConsentNotFound as exc:
            raise HTTPException(status_code=404, detail="Consent not found") from exc
        except NotAuthorized as exc:
            raise HTTPException(status_code=403, detail="Forbidden") from exc

    @app.post("/consents/{consent_id}/revoke", tags=["consent"])
    def revoke(consent_id: str, actor: Principal = Depends(get_principal)) -> dict:
        require_role(actor, Role.SUBJECT)
        try:
            return asdict(service.revoke(actor=actor, consent_id=consent_id))
        except ConsentNotFound as exc:
            raise HTTPException(status_code=404, detail="Consent not found") from exc
        except NotAuthorized as exc:
            raise HTTPException(status_code=403, detail="Forbidden") from exc

    @app.post("/verifications", tags=["consent"])
    def verify(payload: VerifyRequest, actor: Principal = Depends(get_principal)) -> dict:
        require_role(actor, Role.CLIENT)
        return asdict(service.verify(actor=actor, subject_id=payload.subject_id,
                                     purpose=payload.purpose))

    @app.get("/audit/events", tags=["audit"])
    def audit_events(actor: Principal = Depends(get_principal)) -> list[dict]:
        require_role(actor, Role.AUDITOR)
        return [asdict(event) for event in service.audit_events(actor=actor)]

    return app


def create_demo_app() -> FastAPI:
    """Make a loopback-only *demonstration* app from server-side environment keys.

    Required environment variables are not to be placed in source control.
    The app uses synthetic users and in-memory state; never deploy it publicly.
    """
    names = (
        "BIOCONSENT_SUBJECT_TOKEN", "BIOCONSENT_CLIENT_TOKEN", "BIOCONSENT_AUDITOR_TOKEN"
    )
    values = [os.environ.get(name, "") for name in names]
    if any(len(value) < 32 for value in values) or len(set(values)) != len(values):
        raise RuntimeError("Set three distinct, random 32+-character demo tokens in the environment")
    service = ConsentService(
        purposes={"account-authentication", "advertising"},
        client_purposes={"demo-client": {"account-authentication"}},
    )
    return create_app(service=service, token_principals={
        values[0]: Principal("demo-subject", Role.SUBJECT, "synthetic-subject-001"),
        values[1]: Principal("demo-client", Role.CLIENT),
        values[2]: Principal("demo-auditor", Role.AUDITOR),
    })
