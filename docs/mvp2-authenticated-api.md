# MVP 2 — Authenticated Consent API (local synthetic-data prototype)

**Scope:** This milestone wraps the existing deterministic `ConsentService` in a FastAPI HTTP layer. It does **not** use real biometric data or claim production authentication, compliance, persistent storage, cloud deployment, or LLM integration.

## API architecture and trust boundary

```text
HTTP Bearer token
    |
    v
Trusted server-side token registry (demo only)
    |
    v
Principal (server-derived subject / client / auditor / administrator)
    |
    v
FastAPI route-level authorization
    |
    v
Existing ConsentService (deterministic purpose and revocation checks)
    |
    +--> In-memory consent records
    +--> In-memory audit events
```

**Critical rule:** The API never trusts a user-provided `role`, grant `subject_id`, or client purpose authorization. Grant requests contain only a purpose; subject identity comes from the verified bearer token. Verification requests name a synthetic subject and a purpose, but only registered relying clients may call that route, and the existing engine checks the client's configured purpose permissions. Attempts to add unexpected JSON fields are rejected.

The demo has a preconfigured client with permission for `account-authentication`, **not** `advertising`. A subject may grant both; the client's authorization remains restricted.

## HTTP endpoints

| Method | Path | Role | Behavior |
|---|---|---|---|
| GET | `/health` | No authentication | Minimal health status only |
| POST | `/consents` | Subject | Create purpose-specific consent |
| GET | `/consents/{consent_id}` | Owning subject | Inspect own consent record |
| POST | `/consents/{consent_id}/revoke` | Owning subject | Revoke consent |
| POST | `/verifications` | Registered relying client | Return deterministic `allow` or `deny` |
| GET | `/audit/events` | Auditor | Read audit snapshot |

Requests with no/invalid bearer token receive 401. Roles not authorized for a route receive 403. Invalid structured payloads receive 422; a duplicate active grant receives 409. Consent not found returns 404. Non-authorizing consent decisions are returned as structured `deny` results by the policy engine rather than translated to authentication errors.

## Run tests in VS Code Git Bash

From your personal course repository, using a suitable Python virtual environment:

```bash
cd ~/work/AnieWall
python -m pip install -e '.[dev]'
python -m pytest tests/test_consent.py tests/test_api.py -q
python -m pip check
```

## Optional live local demonstration

Generate **fresh** temporary tokens in the Git Bash terminal (do not commit, share, or capture actual token values in screenshots):

```bash
export BIOCONSENT_SUBJECT_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export BIOCONSENT_CLIENT_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export BIOCONSENT_AUDITOR_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
make api-demo
```

The service binds to **127.0.0.1 only** on port 8000. The generated tokens live in your process environment and disappear when that shell session ends. If using a second terminal to make requests, the same credentials must be passed explicitly to that terminal; do not store them in Git. A `uvicorn` error about missing credentials is intentional fail-closed behavior.

For an automated HTTP demonstration, run `python -m pytest tests/test_api.py -v`, which creates a fresh `TestClient` application with synthetic *test-only* credentials and exercises the routes without any network listener. No live cloud API or Jetstream model is required.

## Security tests and limitations

The integration tests cover no/invalid credentials, role spoofing, unauthorized administrators, client role restrictions, cross-subject access, wrong-purpose requests, revocation, duplicate grants, denied unregistered clients, and audit access restrictions. Test tokens are intentionally fake and **must never be used as credentials outside automated tests**.

**Remaining controls before non-local deployment:** Replace the local in-memory demo token registry with managed authentication/session verification; HTTPS/TLS and a secure reverse proxy; rate limiting, secure token lifecycle, monitoring, durable and transactional PostgreSQL storage, protected/retained audit records, key management, cloud security groups, and tenant isolation. Do not expose this MVP 2 demo as a public endpoint. A cloud VM administrator may still inspect the in-memory process; this prototype does not yet provide administrator-resistant storage or operations.

## Relationship to Professor Gregor's mock service

`cloudmesh-ai-llm-mock` is an inspiration for reproducible API and failure-mode testing, but **the LLM integration is not part of MVP 2**. In a later milestone, an optional LLM may suggest structured consent language. A mock LLM can simulate timeouts, hallucinations, and invalid responses; none may override the deterministic consent engine's `allow`/`deny` result.
