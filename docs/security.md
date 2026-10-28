# Security and Privacy

Security is a primary project requirement because the system models consent associated with biometric-data use.

## Core Controls

- **Synthetic data only:** the class prototype does not require real biometric information.
- **Role separation:** public consent operations are separated from administrator and auditor functions.
- **Least privilege:** each service receives only the permissions required for its role.
- **Encryption in transit:** client-to-service and service-to-service communication is designed to use TLS.
- **Encryption at rest:** persistent consent and audit data must be protected at rest.
- **Secrets management:** passwords, tokens, cloud credentials, and private SSH keys must not be committed to GitHub.
- **Audit logging:** consent creation, verification, denial, revocation, administrative access, and policy changes are recorded.
- **Purpose limitation:** consent is bound to an approved purpose and does not automatically authorize unrelated use.
- **Revocation enforcement:** revoked consent must result in a subsequent `DENY` decision.

## Threat Considerations

The current architecture considers:

- unauthorized administrative access;
- credential leakage;
- privilege escalation;
- unauthorized consent modification;
- replay or use of stale consent;
- processing after revocation;
- cross-cloud communication exposure;
- audit-log tampering; and
- unintended storage of sensitive biometric information.

## Repository Security

Generated results and documentation are reviewed before publication for passwords, secrets, tokens, API keys, private keys, and cloud credentials.

For the complete project security architecture, see [../project/project.md](../project/project.md).
