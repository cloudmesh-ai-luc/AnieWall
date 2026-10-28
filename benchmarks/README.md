# Benchmark and Validation Evidence

Project and provider benchmark evidence is organized here rather than in the repository root.

## Accepted Multipass Results

Week 7 Multipass provider testing produced four benchmark files that were submitted to the dedicated `cloudmesh-ai-vm-results` repository.

The corrected submission was approved and merged in:

- [cloudmesh-ai-vm-results PR #1](https://github.com/cloudmesh-ai/cloudmesh-ai-vm-results/pull/1)

Authoritative location:

```text
cloudmesh-ai/cloudmesh-ai-vm-results
└── swallace6/
    └── smoke/

```
### Multipass CLI Smoke Test
`python -m pytest -s tests\smoke\test-multipass-cli.py`
1 passed, 1 warning in 103.95s

### Unified Multipass Lifecycle Test
`python -m pytest -s -vv "tests\smoke\test_lifecycle_unified.py::test_provider_lifecycle[multipass]"`
1 passed, 1 warning in 157.43s

The official generated files remain in the dedicated results repository to avoid duplicating benchmark artifacts across repositories.

Future benchmark work for the biometric-consent project can be added under this directory with a documented methodology, environment, raw results, and summary.
