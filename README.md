# Stephanie Wallace — Cloud Computing, DevOps, and AI

**GitHub ID:** AnieWall  
**Course Repository:** `cloudmesh-ai-luc/AnieWall`  
**Accounts Post:** [Piazza Account Information](https://piazza.com/class/mt5rkdsycb31c3/post/12)

This repository contains course assignments, shared Cloudmesh framework contributions, provider-validation work, documentation, and the **Cloud-Native Biometric Consent and Audit Platform** project.

## Repository Structure

```text
.
├── assignments/          Weekly course assignments and validation reports
├── benchmarks/           Benchmark and validation documentation
├── docs/                 Project architecture, security, and contribution documentation
├── project/              Academic project report and presentation material
├── src/                  Project source-code package
├── tests/                Project tests
├── Makefile              Common development commands
├── mkdocs.yml            Documentation-site configuration
└── pyproject.toml        Python project metadata and dependencies
```

## Course Assignments

Course work is organized under [`assignments/`](assignments/).

- [Week 1](assignments/week1/)
- [Week 2](assignments/week2/)
- [Week 3](assignments/week3/)
- [Week 4](assignments/week4/)
- [Week 5](assignments/week5/README.md)
- [Week 6](assignments/week6/README.md)
- [Week 7](assignments/week7/README.md)

A consolidated assignment index is available in [assignments/README.md](assignments/README.md).

## Current Project

### Cloud-Native Biometric Consent and Audit Platform

The project investigates how biometric-consent requirements can be implemented as a secure cloud-native service.

The system separates public consent interaction from protected consent-management and audit functions. Synthetic identifiers and simulated biometric events are used so that real biometric information is not required for the class implementation.

| Environment | Category | Role | Current Status |
| --- | --- | --- | --- |
| Multipass | Local | Development and repeatable testing | Validated |
| Jetstream 2 | OpenStack | Protected consent-management and audit tier | Real-cloud workflows validated |
| Azure | Public cloud | Public-facing application tier | Selected; live provider validation remains outstanding |

The authoritative project report is:

- [project/project.md](project/project.md)

Supporting documentation includes:

- [Architecture](docs/architecture.md)
- [Security and Privacy](docs/security.md)
- [Shared Cloudmesh Contributions](docs/contributions.md)
- [Benchmark and Validation Evidence](benchmarks/README.md)
- [Project Presentation Material](project/presentation/README.md)

## Shared Cloudmesh Contributions

Course work also includes testing and contributions to the shared [`cloudmesh-ai/cloudmesh-ai-vm`](https://github.com/cloudmesh-ai/cloudmesh-ai-vm) framework.

### Merged Contributions

| PR | Contribution |
| --- | --- |
| [#55](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/55) | Fixed smoke-test collection by adding the missing `Optional` import. |
| [#56](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/56) | Isolated provider-specific lifecycle smoke tests. |
| [#60](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/60) | Restored the OpenStack floating-IP helper. |
| [#67](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/67) | Fixed noninteractive SSH private-key passphrase detection on Windows. |
| [Results PR #1](https://github.com/cloudmesh-ai/cloudmesh-ai-vm-results/pull/1) | Added accepted Multipass CLI and lifecycle benchmark results to the dedicated results repository. |

### Other Reviewed Contributions

- [PR #65](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/65) — closed as redundant after equivalent GitHub SSH-key functionality was confirmed upstream.
- [PR #70](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/70) — closed after benchmark evidence was moved to the dedicated results repository.

### October 24 Smoke-Test Rerun

The current rerun against upstream `dev2` produced three focused open pull requests:

- [PR #97](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/97) — DockerManager Python 3.11 annotation compatibility.
- [PR #98](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/98) — Jetstream smoke test uses the configured SSH key path.
- [PR #101](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/101) — Chameleon smoke test uses the configured SSH key path.

Multipass, Jetstream, and Chameleon provider workflows have been exercised against the current development branch. Docker lifecycle testing is currently deferred because Docker is not installed in the local Windows environment.

A fuller contribution record is maintained in [docs/contributions.md](docs/contributions.md).

## Development Layout

Project application code is maintained under:

```text
src/biometric_consent/
```

Tests are maintained under:

```text
tests/
```

The repository uses `pyproject.toml` for Python package metadata and dependency groups.

Available Makefile targets include:

```text
make install
make test
make view
make clean
```

Application-specific `run` targets will be added when an executable service entry point exists.

## Documentation

The documentation site is built with MkDocs Material.

The navigation currently includes:

- Home
- Project Report
- Architecture
- Security and Privacy
- Shared Contributions

The GitHub Pages workflow automatically publishes documentation from the repository.

## Current Project Priorities

1. Continue implementation of the consent-service components under `src/`.
2. Add consent-policy, revocation, authorization, API, and audit tests under `tests/`.
3. Validate the selected Azure public-cloud environment.
4. Extend the security architecture as authentication, authorization, storage, and inter-cloud communication are implemented.
5. Record project-specific experiments, benchmarks, and evaluation results for the final academic report.

## Security

No passwords, API tokens, private SSH keys, cloud credentials, application credentials, or other secrets should be committed to this repository.

The class prototype uses synthetic identifiers and simulated biometric events. Security controls include least privilege, separation of public and administrative functions, encryption, key and secrets management, audit logging, purpose limitation, and revocation enforcement.
