# Project Architecture

## Cloud-Native Biometric Consent and Audit Platform

The project separates public consent interactions from protected consent-management and audit functions.

### Cloud Roles

| Environment | Category | Primary Role |
| --- | --- | --- |
| Multipass | Local | Development, container testing, smoke testing, and demo/client execution |
| Jetstream 2 | OpenStack | Protected consent-management, policy, persistent data, and audit tier |
| Azure | Public cloud | Public-facing consent interface and API tier |

### Logical Flow

```text
Data Subject / Relying Client
            |
            v
Azure Public Consent Interface / API
            |
            v
Jetstream Protected Consent Management
            |
      +-----+------+
      |            |
      v            v
Policy Engine   Consent / Audit Data
      |
      v
ALLOW / DENY
```

The final authorization decision remains deterministic. AI may assist with consent-language normalization or ambiguity detection, but the AI component does not independently authorize biometric-data use.

### Infrastructure Management

The shared `cmx vm` framework is used as the provider and VM-management layer. It supports provider selection, VM lifecycle operations, image/flavor discovery, key-management validation, smoke testing, and cleanup evidence.

For the complete architecture and current implementation status, see [../project/project.md](../project/project.md).
