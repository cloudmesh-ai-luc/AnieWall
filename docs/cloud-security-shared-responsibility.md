# Cloud Security — Responsibility and Threat Model

**Source connection:** Professor Mohammed Abuhamad, COMP 301/401 Week 10 Cloud Security, especially **slide 61 (security groups)** and **slide 63 (Cloud Responsibility Matrix)**. This document applies the lecture to the Cloud-Native Biometric Consent and Audit Platform. These control designs are implementation goals unless separately marked as completed.

## How the lecture applies

Slide 63 compares Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS), separating responsibility for infrastructure, applications/data, security/compliance, backup/recovery, and identity/access management. For our project running our application on a Chameleon virtual machine, the relevant framing is **IaaS/shared responsibility**, not a claim that the cloud provider will secure our custom consent application.

| Area | Infrastructure provider / Chameleon | Our application team |
|---|---|---|
| Physical hardware and physical network | Provides and operates underlying infrastructure | Cannot treat that as proof of application security |
| VM guest and application | Exposes compute and infrastructure capabilities | Hardens operating system, containers, APIs, dependencies and code |
| Network boundaries | Provides networking and security-group controls where available | Configures allowed traffic and limits exposed ports; no public database port |
| Identity and access | Provides cloud account / infrastructure access features | Authenticates subjects, relying clients, administrators, auditors; enforces least privilege |
| Data, keys and backup | Provides supporting infrastructure and available storage services | Encrypts databases, manages keys in protected configuration, controls retention, tests backup restore |
| Security and compliance | Shared responsibilities | Proves technical controls with tests, audits and policy documentation; avoids unsupported legal-compliance claims |

A security group is a *network* firewall mechanism, not a substitute for purpose-specific consent authorization. A request that passes a firewall must still receive `DENY` if consent is missing, wrong-purpose or revoked.

## Roles and operational privileges

- **Data subject:** Grant/revoke **their own** specific consent and view their own state.
- **Relying client:** Verify consent only for registered purposes; cannot create or override consent.
- **Administrator:** May eventually manage infrastructure or predefined policy metadata, but **cannot grant/revoke consent on behalf of users or read biometric templates** by virtue of the admin role.
- **Auditor:** May inspect permitted audit metadata only; no consent modification permission.

The MVP-1 `Principal` is a **test fixture, not verified authentication**. A subsequent trusted API boundary must authenticate identities and refuse client-supplied roles. The database and audit service should use separate credentials, and cloud operators should not get direct production secret access by default.

## Threat scenarios and controls

| Threat or abuse case | Required defense | MVP-1 evidence / remaining work |
|---|---|---|
| Admin tries to grant consent for advertising without subject approval | Subject-bound grant, no admin override | **Tested:** admin grant denied |
| Admin tries to revoke another subject or inspect record | Subject isolation, restricted methods | **Tested:** admin revoke/read denied |
| Client asks for a purpose it is not registered to use | Per-client purpose allowlist | **Tested:** unapproved client purpose denied |
| Consent revoked but stale cached decision still allows access | Central, current consent state and cache invalidation | **Tested in-process**; multi-replica/cache invalidation remains pending |
| Bypass via alternate spelling of purpose | Strict, validated purpose identifiers | **Tested:** exact-match denial |
| Audit tampering or incomplete records | Protected append-only durable audit store with controlled retention | **Partially tested:** in-memory event sequence only; persistence/tamper evidence pending |
| Forged actor identity in HTTP request | Verified authentication tokens and server-side principal construction | **Not implemented**; must precede public API |
| Interception/credential leakage across cloud links | TLS, key management, protected secrets, private network paths | **Planned** for deployment; never store `.env` or tokens in GitHub |
| AI hallucinates an authorized purpose | LLM suggestions only; human confirmation; deterministic engine | **Designed**; no LLM in decision path |
| Loss of consent or revocation records | Persistent transactions, tested backups/restore, retention rules | **Not implemented** in MVP 1 |

## Sensitive-data handling

Only synthetic subject identifiers are used. The prototype does not store biometric images or templates. A future relying-client demo should simulate a biometric action without actually processing personal biometric data. For a real implementation, pseudonymization, limited retention, encryption in transit/at rest, purpose limitation, revocation semantics, and documented deletion-vs-audit-retention policy require separate engineering and legal review.

## Cloud/project scope following Professor Gregor's November 15 note

**Separate two tasks:** (1) ongoing `cloudmesh-ai-vm` *assignments* continue development and regression coverage for the three course providers; (2) the *individual class project* needs only **one non-local cloud** for deployment. The earlier Multipass+Jetstream2+Azure design may remain as a stretch architecture, but should not be represented as a required deployment. Chameleon is a practical candidate given the professor's Heat observation. Actual access, deployment and usable orchestration must be verified before claiming success.

## Acceptance tests for the next iteration

- Unauthorized administrator cannot view or modify subject consent even with a valid infrastructure login.
- Unknown client and wrong-purpose request return DENY without exposing consent IDs.
- Revoked consent returns DENY after restarts and across distinct application workers.
- Audit records persist across restarts and ordinary admin permissions cannot rewrite them.
- Cloud security groups expose only essential service ports; database and management APIs are not open publicly.
- LLM-generated text cannot invoke the consent grant function without a separately authenticated subject action.
