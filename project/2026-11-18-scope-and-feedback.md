# Project Scope and Professor Feedback — November 18, 2026

## Purpose

This decision record distinguishes the **existing project proposal** from the **implementation scope** and prevents the class's weekly multi-cloud VM assignments from being confused with the individual project deployment target.

## Instructor feedback applied

### November 15 clarification (Piazza, as supplied in course discussion)

- The weekly `cloudmesh-ai-vm` provider assignments **remain unchanged** and continue to require improving the selected three providers and leveraging an LLM.
- The individual project needs **one non-local cloud**, not three. Additional clouds are optional demonstrations, not a prerequisite.
- Chameleon offers an attractive orchestration path using Heat; this is a reason to evaluate it, not evidence that our project has already deployed on it.

### Midterm presentation feedback

- Prefer a clear, working application, not just a conceptual architecture or set of slides.
- A single-cloud deployment of VMs/containers is acceptable, and a second provider can be shown if useful.
- Explicitly address how administrators could exploit or mishandle biometric data.
- State clearly how LLMs were used and validate their outputs; use the code/model as engineering aids, not an authorization shortcut.

## Updated build sequence

1. **MVP 1 (implemented locally):** Consent lifecycle and audit behavior with synthetic identifiers, deterministic ALLOW/DENY, wrong-purpose denial, revocation, admin-abuse tests.
2. **MVP 2:** Authenticated FastAPI and purpose-scoped relying-client API; avoid trusting caller-supplied roles.
3. **MVP 3:** PostgreSQL persistence, transaction-safe revocation, protected audit store and retention policy.
4. **MVP 4:** Docker deployment to one non-local cloud (evaluate Chameleon). Keep `cmx vm` infrastructure provisioning separate from the app's consent enforcement.
5. **MVP 5:** Jetstream LLM or mocked model for suggestions on consent-language mapping; deterministic validation and user approval remain mandatory. Unit tests should not require a live LLM.
6. **MVP 6:** Demo and presentation using Sam Stewart's clear report/architecture format and Kbass's modular code/tests practices, while writing our own implementation.

## Out-of-scope for MVP 1

- Real biometric data or face-recognition models
- Public HTTP exposure, production identity management or a live database
- Claim of completed GDPR/BIPA/Ghana DPA compliance
- Deployed Kubernetes, multi-region failover, or working cross-cloud access
- Use of LLM output to permit access or grant consent autonomously

## Definition of done for MVP 1

- Source modules exist in `src/biometric_consent` and are importable from an editable installation.
- `python -m biometric_consent.demo` prints ALLOW for active matched consent, DENY for a different purpose, and DENY after revocation.
- `python -m pytest -q` passes the existing import test plus new consent lifecycle/security tests.
- No API keys, secrets or biometric images are added to the repository.
- Security responsibilities, current limitations and next milestone are documented.
- Results are recorded truthfully in `assignments/STATUS.md` only **after** running the tests in the student's own development environment.
