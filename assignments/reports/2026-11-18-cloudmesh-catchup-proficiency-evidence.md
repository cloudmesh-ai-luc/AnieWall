# Cloudmesh DevOps — Catch-Up and LLM Proficiency Evidence Report

**Student:** Stephanie Wallace  
**GitHub ID:** AnieWall  
**Course:** Cloud Computing, DevOps, and AI  
**Instructor:** Professor Gregor von Laszewski  
**Evidence Dates:** November 17–18, 2026  
**Repository:** [cloudmesh-ai-luc/AnieWall](https://github.com/cloudmesh-ai-luc/AnieWall)  
**Status:** Technical demonstrations completed; instructor proficiency acceptance pending.

---

## 1. Objective

This report documents the completion and verification of foundational Cloudmesh DevOps assignments, including Git Bash proficiency, SSH authentication, GitHub repository management, development-environment configuration, and Jetstream-hosted large language model (LLM) integration.

The objective was to demonstrate the ability to establish an organized development environment, authenticate securely with GitHub, work with the required course repositories, launch Visual Studio Code from Git Bash, and successfully perform LLM inference using both Cline and Python.

Evidence was collected through screenshots of actual command execution, successful results, and GitHub commits.

No video recordings are included in this submission.

## 2. Class Workspace Setup

### 2.1 Creating the Required Class Directory

A dedicated class directory was created using standalone Git Bash on Windows.

**Commands executed:**

```bash
cd ~
mkdir -p ~/work
cd ~/work
pwd
ls -la
```

**Verification:** The terminal confirmed the directory:

`/c/Users/Stephanie Wallace/work`

The directory was initially empty and ready to accommodate the required course repositories.

**Figure 1 — Successful creation of the class workspace**

![Class directory created](evidence/Evidence_Work%20Directory_AnieWall%281%29.png)

### 2.2 Cloning the Required GitHub Repositories

Four required repositories were cloned into `~/work` using SSH authentication.

**Commands executed:**

```bash
git clone git@github.com:cloudmesh-ai-luc/AnieWall.git
git clone git@github.com:cloudmesh-ai/cloudmesh-ai-common.git
git clone git@github.com:AnieWall/cloudmesh-ai-vm.git
git clone git@github.com:cloudmesh-ai/cloudmesh-ai-llm-mock.git
```

**Repositories successfully cloned:**

| Repository | Purpose | Result |
|---|---|---|
| `AnieWall` | Personal assignments and individual project | Passed |
| `cloudmesh-ai-common` | Shared framework components | Passed |
| `cloudmesh-ai-vm` | VM provider development and testing | Passed |
| `cloudmesh-ai-llm-mock` | Reference LLM mock-service implementation | Passed |

The final directory listing confirmed that all four repositories were present.

**Figure 2 — SSH cloning operations and repository verification**

![Required repositories cloned](evidence/Evidence_Cloned%20Required%20Repositories%281%29.png)

## 3. Git Bash Utilities Verification

The required development utilities were checked in standalone Git Bash.

**Verification commands:**

```bash
for tool in git curl jq make; do
    command -v "$tool" || echo "MISSING: $tool"
done

git --version
curl --version | head -n 1
jq --version
make --version | head -n 1
```

**Results:**

| Utility | Verified version | Result |
|---|---|---|
| Git | 2.48.1 | Passed |
| curl | 8.12.1 | Passed |
| jq | 1.8.2 | Passed |
| GNU Make | 4.4.1 | Passed |

The `jq` utility was installed using Chocolatey before final verification.

All four executable paths were successfully detected in Git Bash.

**Figure 3 — Required Bash utilities and version verification**

![Bash utility verification](evidence/Evidence_Bash%20Utilities%20Requirements.png)

## 4. SSH Authentication and Key Management

### 4.1 Starting the SSH Agent

An SSH authentication agent was started within Git Bash to manage the existing ED25519 key.

**Commands executed:**

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add -l
ssh -T git@github.com
```

### 4.2 Verification Results

The terminal confirmed:

- The SSH agent started successfully.
- The existing ED25519 private key was loaded into the agent.
- `ssh-add -l` displayed the corresponding public-key fingerprint.
- GitHub SSH authentication succeeded for the `AnieWall` account.

GitHub returned its successful authentication message, indicating that the configured SSH identity was recognized.

**Figure 4 — SSH-agent initialization and successful GitHub authentication**

![SSH authentication verification](evidence/Evidence_SSH%20Authentication%281%29.png)

**Security considerations:** No private SSH key contents, passphrases, or authentication tokens were included in the evidence.

## 5. Repository Configuration and VS Code Launch

### 5.1 Cloudmesh VM Repository Configuration

The personal `cloudmesh-ai-vm` fork was configured with the official Cloudmesh repository as its `upstream` remote.

**Commands executed:**

```bash
cd ~/work/cloudmesh-ai-vm

git remote add upstream git@github.com:cloudmesh-ai/cloudmesh-ai-vm.git

git fetch upstream
git switch --track upstream/dev3

git status -sb
git branch -vv
git remote -v
```

The local `dev3` branch was established to track the official `upstream/dev3` branch.

The final status showed a clean, synchronized working tree:

```text
## dev3...upstream/dev3
```

This configuration preserves the separation between the student's GitHub fork (`origin`) and the official Cloudmesh development repository (`upstream`).

**Figure 5 — Cloudmesh repository configuration and terminal workflow**

![Cloudmesh repository configuration](evidence/Evidence_Configuration_Cloudmesh%20VM%20Directory%281%29.png)

### 5.2 Launching VS Code Using `code .`

The class workspace was opened directly from standalone Git Bash.

**Commands executed:**

```bash
cd ~/work
code .
```

Visual Studio Code launched successfully, displaying all four required repositories in the Explorer.

This demonstrates command-line proficiency and the ability to transition from a Bash environment to a graphical development environment without manually navigating to the project directory.

**Figure 6 — Launching VS Code from standalone Git Bash**

![VS Code launch through Git Bash](evidence/Evidence_Demonstrable%20Launch%20into%20VS%20Code%20using%20Code..png)

## 6. Jetstream LLM Integration with Cline

### 6.1 Cline Configuration

The Cline extension was configured in Visual Studio Code to communicate with the Jetstream-hosted LLM service.

**Verified configuration:**

| Setting | Configuration |
|---|---|
| VS Code extension | Cline |
| API provider | OpenAI Compatible |
| Base URL | Jetstream-hosted LLM endpoint |
| Model identifier | `qwen-3.8-27b` |
| API credential | Configured and masked |

The screenshot confirms that the API configuration was present without revealing the authentication credential.

**Figure 7 — Jetstream LLM configuration in Cline**

![Jetstream Cline integration](evidence/Evidence_Jetstream%20LLM%20Integration%20with%20Cline.png)

### 6.2 Inference Demonstration in Cline

A test prompt was submitted through the Cline interface requesting an explanation of cloud VM providers, the use of Multipass, Jetstream2, and Chameleon, and the importance of smoke testing.

Cline successfully generated a relevant technical explanation discussing virtual-machine provisioning, provider differences, OpenStack environments, and multi-cloud validation.

The response was reviewed rather than accepted without verification.

**Figure 8 — Successful Jetstream LLM inference through Cline**

![Cline LLM inference response](evidence/Evidence_Cline%20Inference.png)

**Result:** Successful LLM inference demonstrated within the Cline development environment.

## 7. Direct Jetstream LLM Inference Using Python

### 7.1 Python Development Environment

A separate Python virtual environment was created in the `AnieWall` repository.

**Python version:** 3.11.9

The OpenAI-compatible Python client was installed to communicate directly with the Jetstream LLM service.

The inference script was saved under:

`scripts/jetstream_inference.py`

The Python project's development dependencies were updated in `pyproject.toml` to include the OpenAI-compatible client.

### 7.2 Secure Configuration Management

The Python inference script reads configuration from:

`~/.config/cloudmesh-ai/jetstream.json`

This configuration file is stored outside the GitHub repository.

It contains the connection settings required by the Python client, while the committed script contains no hardcoded API credentials.

The project's `.gitignore` excludes the local `.venv/` environment.

### 7.3 Inference Execution

**Command executed:**

```bash
python scripts/jetstream_inference.py
```

The script submitted a prompt asking the Jetstream-hosted Qwen model to explain why smoke testing is important in multi-cloud DevOps.

**Verified output:**

```text
Cloudmesh Jetstream LLM — Python Inference Test
Model: qwen-3.8-27b
Sending test inference request...

Finish reason: stop
Generated tokens: 274

LLM Response:
[Successful explanation of smoke testing in multi-cloud DevOps]

Inference request completed successfully.
```

The response explained how smoke testing detects deployment misconfigurations, connectivity problems, and environment-specific failures before applications receive production traffic.

**Figure 9 — Successful direct Python inference against Jetstream LLM**

![Jetstream Python inference result](evidence/Evidence_Python%20Inference.png)

**Result:** The model returned a meaningful response through a Python API request, independently of the Cline interface.

### 7.4 Automated Verification

The following checks were completed:

| Verification | Observed result |
|---|---|
| Editable project installation | Successful |
| `pip check` | No broken requirements |
| Existing project pytest suite | 1 test passed |
| Python syntax compilation | Passed |
| Git whitespace validation | Exit code 0 |
| Jetstream Python inference | Successful response |
| Empty-response error handling | Implemented |
| Private configuration outside repository | Verified by script design |

The single passing pytest test validates the existing project package import. It should not be interpreted as comprehensive coverage of the Jetstream inference script.

## 8. GitHub Version Control and Submission

The inference implementation and dependency changes were committed and pushed to the `main` branch of the personal course repository.

**Repository:** [cloudmesh-ai-luc/AnieWall](https://github.com/cloudmesh-ai-luc/AnieWall)

**Verified commits:**

| Commit | Description |
|---|---|
| [`be5e431`](https://github.com/cloudmesh-ai-luc/AnieWall/commit/be5e4311a8b2b9668c78e404ea1c102d941c17e4) | Added secure Jetstream Python inference example and development dependency |
| [`bea349f`](https://github.com/cloudmesh-ai-luc/AnieWall/commit/bea349f2204fda23d06c495355a76534e5cdacf3) | Final script formatting correction |

The empty-response handling was also reviewed in the committed implementation, ensuring an unsuccessful final response results in a nonzero process exit status.

The final Git push completed successfully using SSH authentication, and the working branch was synchronized with `origin/main`.

## 9. Security and Responsible LLM Use

The workflow applied several security and verification practices:

- SSH keys were used for GitHub authentication without publishing private-key material.
- LLM credentials were maintained outside the repository.
- The Cline configuration screenshot displayed a masked credential.
- The local Python virtual environment was excluded from Git tracking.
- Python-generated code and LLM responses were independently reviewed.
- API failures and empty model responses were handled explicitly.
- No real biometric data was required for any demonstration.

These precautions are particularly important for the planned Cloud-Native Biometric Consent and Audit Platform, which will require strict separation between public interfaces, protected consent records, authentication services, and audit functions.

## 10. Relationship to Cloudmesh VM Development

This catch-up exercise complements previous development work on the shared `cloudmesh-ai-vm` framework.

Previous provider validation and engineering contributions are documented separately in:

- [November 4 Multi-Cloud Verification Report](2026-11-04-multicloud-verification.md)
- [November 11 WSL2 Investigation](2026-11-11-wsl2-issue109-verification.md)
- [Chameleon Safety PR #132](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/132)

Those earlier tests and contributions are not represented as new test executions in this report.

## 11. Outstanding Requirements

The technical activities described in this report are complete and supported by screenshots and GitHub evidence.

The following remain separate follow-up requirements:

1. Obtain Professor Gregor's confirmation that the mandatory proficiency demonstration has been accepted.
2. Complete any remaining current-week provider smoke tests, including the pending Chameleon verification.
3. Confirm the required Piazza posts and notification settings have been reviewed.
4. Continue implementing the executable Cloud-Native Biometric Consent and Audit Platform.
5. Maintain `assignments/STATUS.md` using concise weekly summaries linked to supporting reports.

## 12. Conclusion

The catch-up work established and verified a functional Cloudmesh development environment using Git Bash, SSH authentication, four required course repositories, Visual Studio Code, Cline, and the Jetstream-hosted Qwen model.

Successful inference was demonstrated both interactively through Cline and programmatically through Python.

The work also demonstrated GitHub repository synchronization, secure configuration handling, dependency management, automated validation, and source-control practices.

**Final technical result: The documented development-environment, Git workflow, Cline inference, and Python inference demonstrations completed successfully.**

Formal satisfaction of the mandatory proficiency assessment remains subject to Professor Gregor's confirmation.
