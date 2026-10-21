Git-ID -> AnieWall

*  Accounts: [https://piazza.com/class/mt5rkdsycb31c3/post/12]

## Week 7 Tasks

- [x] Continue testing and fixing the shared `cloudmesh-ai-vm` framework against the current upstream `dev2` branch.
- [x] Keep changes isolated in feature branches and submit focused pull requests with validation evidence.
- [x] Improve smoke-test reliability and provider-specific test isolation.
- [x] Continue OpenStack/Jetstream testing and identify provider-level defects.
- [x] Test the SSH/GitHub key-management commands on Windows.
- [x] Add regression tests for newly reproduced key-management defects.
- [x] Validate SSH passphrase detection using real local keys without exposing private-key material.
- [x] Complete additional repeatable provider testing for Multipass using the existing CLI and unified lifecycle smoke tests.
- [x] Review pull requests after Professor Gregor's feedback and make the requested follow-up changes.
- [x] Relocate generated Multipass benchmark results to the dedicated `cloudmesh-ai-vm-results` repository.
- [ ] Validate the selected public-cloud provider, Azure, against the current `dev2` implementation.

### Week 7 Shared-Repository Contributions

Week 7 work continued against the shared `cloudmesh-ai/cloudmesh-ai-vm` repository. The emphasis expanded from exercising provider commands to reproducing defects, developing focused fixes and regression tests, validating the changes in real environments, and responding to Professor Gregor's review feedback.

| PR | Final Status | Contribution |
| --- | --- | --- |
| [#55](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/55) | Merged | Added the missing `Optional` import that prevented smoke-test collection. |
| [#56](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/56) | Merged | Isolated provider-specific lifecycle smoke tests so a target runs only the intended provider case. |
| [#60](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/60) | Merged | Restored the missing OpenStack floating-IP helper used by VM information workflows. |
| [#65](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/65) | Closed as redundant | Investigated GitHub SSH-key field handling. Current `dev2` already contained equivalent GitHub key-list functionality, so no duplicate implementation was required. |
| [#67](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/67) | Merged | Fixed local SSH-key passphrase detection so protected keys are detected without interactive prompts. |
| [#70](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/70) | Closed / Relocated | Originally submitted Multipass benchmark evidence to the implementation repository. Professor Gregor clarified that generated results belong in the dedicated results repository. |
| [Results PR #1](https://github.com/cloudmesh-ai/cloudmesh-ai-vm-results/pull/1) | Merged | Added the validated `swallace6` Multipass CLI and lifecycle smoke-test results to the correct results repository. |

Professor Gregor approved and merged Pull Requests #60 and #67 on October 19, 2026.

The corrected Multipass results submission, `cloudmesh-ai/cloudmesh-ai-vm-results` Pull Request #1, was approved and merged by Professor Gregor on October 21, 2026.

### Smoke-Test Reliability

The `dev2` smoke-test path initially failed during collection because `tests/smoke/benchmark_helper.py` referenced `Optional[str]` without importing `Optional`.

Pull Request #55 added the missing import so the smoke lifecycle tests could be collected successfully.

Provider-specific Makefile targets were then reviewed. A target such as `make multipass` previously included the complete parametrized lifecycle test file, which allowed unrelated provider cases to be collected.

Pull Request #56 changed each provider target so that only the corresponding lifecycle test is selected.

Both Pull Requests #55 and #56 were merged into the shared repository.

### OpenStack Floating-IP Defect

Further Jetstream testing reproduced an error in VM information handling:

`OpenstackManager object has no attribute '_get_floating_ip'`

The surrounding implementation already expected an internal floating-IP helper, but the method was not correctly available on the class.

Pull Request #60 restored `_get_floating_ip()` and checked OpenStack server-address records for entries whose `OS-EXT-IPS:type` value is `floating`.

Validation included:

- Python compilation;
- `git diff --check`;
- confirmation that `_get_floating_ip()` existed on `OpenstackManager`; and
- a focused test using fixed and floating address data.

Professor Gregor approved and merged Pull Request #60 into `dev2` on October 19, 2026.

The upstream repository subsequently also added dedicated floating-IP commands:

`cmx vm ip assign`

`cmx vm ip release`

The local `dev2` installation was synchronized after these upstream changes, and the `cmx vm ip` command group was confirmed to be available.

### GitHub SSH-Key Listing

Testing of the GitHub SSH-key listing initially identified a mismatch between raw GitHub API fields and values needed by the Cloudmesh display workflow.

Pull Request #65 proposed normalization of the returned GitHub key information.

During review, Professor Gregor noted that equivalent functionality might already exist in the current implementation.

The current `dev2` branch was re-inspected and confirmed to already provide the required behavior through the existing GitHub key-list workflow, including:

- determining the SSH key type;
- calculating SHA256 and MD5 fingerprints;
- locating the corresponding local SSH key; and
- displaying verification information.

Real Windows validation with:

`cmx key github list`

completed successfully.

Because the required functionality had already been implemented upstream through a different code path, Pull Request #65 was closed as redundant rather than introducing duplicate logic.

### SSH Passphrase Detection

Local key scanning exposed a separate key-management defect.

Before the fix, `cmx key scan` could trigger interactive `Enter passphrase:` prompts on Windows and incorrectly report password-protected Ed25519 private keys as:

`Passphrase: No`

The original implementation used:

`ssh-keygen -y -f <key>`

to determine whether a private key required a passphrase.

On Windows, this subprocess could enter an interactive passphrase path, making it unsuitable for a noninteractive scan.

Pull Request #67 replaced that check with Paramiko's private-key loader.

Paramiko was selected because it:

- can inspect private keys programmatically;
- does not require an interactive `ssh-keygen` process;
- supports platform-independent passphrase detection; and
- was already a dependency of the project.

Three focused regression cases were added:

1. an unprotected key returns `False`;
2. a password-protected key returns `True`; and
3. an unrelated parsing error is not falsely classified as passphrase protection.

Validation produced:

```text
3 passed
```
The implementation also passed Python compilation and git diff --check.

Real Windows validation was repeated with cmx key scan. The command completed without interactive prompts and correctly identified the protected Ed25519 private keys as:

`Passphrase: Yes`

Professor Gregor approved and merged Pull Request #67 into dev2 on October 19, 2026.

After the merge, the local repository was synchronized with official upstream dev2, the editable package was reinstalled, and the command was tested again.

The official merged implementation correctly displayed all three local Ed25519 private keys as passphrase-protected.

`cmx key github list` also successfully identified the registered GitHub key as verified and matched it to the corresponding local path.

No private key, passphrase, cloud credential, or other secret was added to any repository.

### Windows SSH-Agent Verification

The Windows OpenSSH agent was also used so that passphrase-protected identities could remain encrypted on disk while unlocked identities were available during the active session.

The distinction between the two verification mechanisms was documented:

`cmx key scan`

shows which local private-key files exist and whether those private keys are encrypted with passphrases.

`ssh-add -l`

shows which identities are currently unlocked and loaded into the Windows SSH agent.

The final validation environment contained three passphrase-protected local Ed25519 private keys while two active identities were loaded into the Windows SSH agent.

This was expected because an older Cloudmesh key remained encrypted locally after its passphrase was no longer available, while a replacement protected Cloudmesh key was generated and loaded into the agent.

### Multipass Provider Validation

Multipass was selected for additional Week 7 provider validation because the shared provider work identified it as requiring additional repeatable testing.

Testing was performed on Windows using Multipass 1.16.3+win against the current dev2 branch.

Before testing, the local cmx installation was refreshed from the editable repository because a previously installed executable referenced an outdated command entry point.

The current package was reinstalled with:

`python -m pip install -e . --no-deps --force-reinstall`

After the refresh, both `cmx --help` and provider commands executed successfully.

The Multipass provider was selected and validated through two repeatable smoke-test paths.

### Multipass CLI Smoke Test
Executed:

`python -m pytest -s tests\smoke\test-multipass-cli.py`

Result:

`1 passed, 1 warning in 103.95s`

The test validated:
- provider listing and selection;
- VM creation;
- VM listing;
- VM stop;
- VM deletion;
- image discovery; and
- flavor discovery.
  
### Unified Multipass Lifecycle Test
Executed:

`python -m pytest -s -vv "tests\smoke\test_lifecycle_unified.py::test_provider_lifecycle[multipass]"`

Result:

`1 passed, 1 warning in 157.43s`

The lifecycle test additionally validated:
- provider requirements;
- image and flavor discovery;
- VM creation and running-state detection;
- VM connectivity;
- temporary SSH-key upload and verification;
- SSH-key deletion and verification;
- shelve and unshelve behavior;
- VM information and listing; and
- VM stop, deletion, and cleanup.
After testing, multipass list confirmed that the temporary smoke-test VMs had been removed and that no test resources remained.

The generated benchmark files were checked for passwords, secrets, tokens, private keys, credentials, and API keys before submission.

### Multipass Results Repository

The Multipass benchmark results were initially submitted in:
- cloudmesh-ai/cloudmesh-ai-vm Pull Request #70
Professor Gregor clarified during review that generated smoke-test results belong in the dedicated:

cloudmesh-ai/cloudmesh-ai-vm-results 

repository rather than in the implementation repository.

Pull Request #70 was therefore closed.

The four validated result files were relocated to:

`swallace6/smoke/`

in the results repository:
- multipass-cli-swallace6-2026-10-15--00-22.json
- multipass-cli-swallace6-2026-10-15--00-22.txt
- multipass-smoke-swallace6-2026-10-15--00-35.json
- multipass-smoke-swallace6-2026-10-15--00-35.txt
Before submission, the files were rechecked for sensitive values and whitespace problems.

The corrected results submission was:
- [cloudmesh-ai-vm-results PR #1](https://github.com/cloudmesh-ai/cloudmesh-ai-vm-results/pull/1)
Professor Gregor approved and merged the corrected results pull request on October 21, 2026.

### Week 7 Testing Status

Week 7 produced completed and merged contributions to the shared cloudmesh-ai-vm framework as well as repeatable provider-validation evidence.

Completed work includes:
- smoke-test collection repair;
- provider-specific lifecycle-test isolation;
- OpenStack floating-IP helper repair;
- Windows SSH passphrase-detection repair;
- GitHub SSH-key workflow verification;
- SSH-agent verification;
- repeatable Windows Multipass CLI testing;
- repeatable Multipass lifecycle testing;
- secure review of generated benchmark files;
- relocation of benchmark evidence to the dedicated results repository; and
- review and cleanup of outstanding pull requests after Professor Gregor's feedback.
The major remaining Week 7 provider requirement is the selected public-cloud environment.

The current three-cloud selection is:
| Environment | Category | Current Status |
| --- | --- | --- |
| Multipass | Local | Repeatable CLI and lifecycle validation completed |
| Jetstream 2 | OpenStack | Real-cloud VM and provider workflows previously validated |
| Azure | Public Cloud | Selected; live `cmx` provider validation remains outstanding |

Azure is therefore the next provider-validation priority.

### Week 7 Contribution Outcome

The Week 7 shared-repository work resulted in four merged implementation or testing pull requests:
- PR #55
- PR #56
- PR #60
- PR #67
The Multipass benchmark evidence was additionally accepted through the dedicated results repository in:
- cloudmesh-ai-vm-results PR #1
Pull Request #65 was closed after confirming that the required GitHub-key functionality was already available upstream, avoiding duplicate implementation.

Pull Request #70 was closed after Professor Gregor clarified the correct repository for generated benchmark evidence.

The work therefore demonstrates not only code contribution but also the full repository workflow of reproducing defects, validating fixes, responding to review feedback, identifying redundant changes, correcting submission location, and synchronizing the local environment with accepted upstream code.

### Use of ChatGPT as a Supporting Tool

ChatGPT was used selectively during Week 7 as a supporting tool for debugging, reviewing implementation alternatives, organizing regression-test ideas, interpreting command output, and improving technical documentation.

One example occurred during the SSH passphrase-detection investigation. The existing `ssh-keygen` approach produced interactive prompts and incorrect passphrase results on Windows.

ChatGPT was used to explore possible noninteractive approaches and reason through the observed terminal behavior. An initial ssh-keygen option was tested against the installed Windows OpenSSH version but produced a Too many arguments error. The approach was therefore discarded based on direct local verification.

Further investigation led to testing Paramiko's private-key-loading functionality. Paramiko was already a project dependency and was tested directly against the local SSH-key environment before the implementation was changed.

The final change was independently validated through:
- unit testing;
- Python compilation;
- `git diff --check`;
- real Windows cmx key scan execution; and
- subsequent validation against official upstream dev2 after Professor Gregor merged PR #67.
ChatGPT was also used to assist with pull-request wording, review-response preparation, repository-structure checks, and README organization.

Technical conclusions were based on repository code, locally reproduced behavior, command-line results, automated tests, and Professor Gregor's review feedback rather than accepting generated suggestions without verification.

No private keys, passphrases, cloud credentials, or other secrets were shared with the tool.


## Week 6 Tasks (Due Oct 8, 2026, 9am)

- [x] Continue the libcloud/provider assignment using the current `cloudmesh-ai-vm` development branch.
- [x] Communicate progress and findings through Piazza.
- [x] Use GitHub issues, feature branches, regression tests, and pull requests.
- [x] Stay synchronized with the current upstream `dev2` branch.
- [x] Validate Jetstream as the first provider using real cloud resources.
- [x] Validate Chameleon Cloud as the second provider.
- [x] Develop or adapt a smoke test for a second provider.

### Jetstream Provider Validation

Jetstream testing was performed against the current `dev2` branch of `cloudmesh-ai/cloudmesh-ai-vm`.

A defect was reproduced in `cmx vm list` when Libcloud failed and the OpenStack CLI fallback incorrectly returned no virtual machines even though a VM existed in the Jetstream project.

- Issue #35: https://github.com/cloudmesh-ai/cloudmesh-ai-vm/issues/35
- Pull Request #36: https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/36

A second defect was identified in Jetstream flavor discovery. `get_flavors()` returned an empty result when Libcloud raised an exception instead of using the OpenStack CLI fallback.

- Issue #37: https://github.com/cloudmesh-ai/cloudmesh-ai-vm/issues/37
- Pull Request #38: https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/38

The flavor fallback fix was validated with a regression unit test and against the real Jetstream provider. The provider successfully returned the available Jetstream flavors, including `m3.tiny`.

### Standalone Jetstream Validation

The `tests/standalone` examples from the shared repository were also used.

The Jetstream cloud-services test successfully authenticated, retrieved the Keystone service catalog, and identified 17 registered services. The Heat orchestration service was registered but its endpoint was not responding.

The standalone Libcloud VM test was then executed with the smallest available flavor, `m3.tiny`, using:

- Image: `Featured-Minimal-Ubuntu24`
- Flavor: `m3.tiny`
- Network: `auto_allocated_network`
- Security group: `default`
- Keypair: `swallace1`

The VM reached the `ACTIVE` state and a floating IP was successfully attached. The temporary VM and floating IP were deleted immediately after validation, and cleanup was confirmed.

### Chameleon Cloud Provider Validation

Chameleon Cloud was validated as the second provider using the KVM@TACC site.

Initial service discovery confirmed successful authentication and access to the Chameleon OpenStack environment. The environment exposed the required OpenStack services, including the Blazar reservation service used for KVM resource leases.

The current `dev2` branch introduced a new Chameleon workflow based on OpenStackSDK and `python-chi`, replacing the older Libcloud-based approach. The reference workflow in `tests/standalone/gregor-kvm-tacc-lease.py` was used as the basis for a student-specific validation script.

The Chameleon test used:

- Site: `KVM@TACC`
- Image: `CC-Ubuntu24.04`
- Base flavor: `m1.small`
- Network: `sharednet1`
- Keypair: `swallace6`
- Security group: `allow-ssh`
- Reservation duration: one hour

Several compatibility issues were identified while adapting the standalone workflow.

The installed OpenStackSDK connection did not expose `conn.catalog`, so the Blazar endpoint was retrieved through the authenticated session using the `reservation` service type.

The installed `python-chi` package also retained internal authentication and connection references after import. This initially produced authentication failures including `identity/token/id: None` and a later OpenStackSDK session compatibility error. The standalone validation script was adapted so that the authenticated OpenStackSDK session and connection were reused by the required `python-chi` client and server interfaces.

The Blazar client configuration was also updated to use the `reservation` service type, public interface, and active region.

After these adaptations, the end-to-end Chameleon workflow completed successfully:

1. Authentication to KVM@TACC succeeded.
2. A one-hour Blazar lease was created and reached `ACTIVE`.
3. A reserved `m1.small` flavor was allocated.
4. A `CC-Ubuntu24.04` virtual machine was launched.
5. The VM reached the `ACTIVE` state.
6. A floating IP was associated successfully.
7. The existing `allow-ssh` security group was attached.
8. SSH access succeeded using the `swallace6` keypair.

The remote session confirmed execution inside the Chameleon VM:

```text
hostname: ssh-vm-demo-swallace-74c78a51
user: cc
kernel: 6.8.0-124-generic
```

After validation, the VM, floating IP, and Blazar lease were deleted. Final checks confirmed that no test VM, floating IP, or lease remained.

A student-specific Chameleon validation script was preserved in a local development commit for documentation and testing evidence. It was not submitted as a pull request because the script contains environment-specific configuration and was intended to validate the Professor Gregor's new OpenStackSDK and python-chi workflow rather than modify the shared implementation.

## Week 6 Self-Assessment

Week 6 completed real-provider validation against both Jetstream and Chameleon Cloud.
The Jetstream work focused on identifying reproducible provider defects, documenting them through GitHub issues, developing regression tests, and submitting pull requests. Testing demonstrated how cmx, Libcloud, OpenStack CLI fallbacks, clouds.yaml, and the underlying OpenStack services interact during provider operations.
The standalone Jetstream workflow successfully created an m3.tiny VM, reached the ACTIVE state, attached a floating IP, and removed the temporary resources after testing.
The Chameleon work required a different provider path because the current Chameleon implementation is moving away from the previous Libcloud-based approach. The updated workflow used OpenStackSDK, python-chi, and Blazar reservations. Several authentication and session compatibility problems were isolated and resolved during adaptation of the standalone reference script.
The final Chameleon validation successfully created an active reservation, launched a reserved KVM virtual machine, associated a floating IP, configured SSH access, and established an SSH session into the Ubuntu 24.04 instance. Resource cleanup was then completed and independently verified.
This present assignment therefore demonstrated successful real-cloud validation across two OpenStack providers while also providing practical experience with provider abstraction, service catalogs, authentication sessions, reservation systems, SDK compatibility, failure diagnosis, regression testing, and cloud resource cleanup.

## Week 5 Tasks (Due Oct 1, 2026, 9am)

- [x] Fork and clone the shared `cloudmesh-ai-vm` repository.
- [x] Create feature/testing branches rather than working directly on the shared branch.
- [x] Evaluate the OpenStack/Jetstream provider implementation.
- [x] Test provider information and VM-list behavior against a real Jetstream environment.
- [x] Identify reproducible provider defects and document them through GitHub issues.
- [x] Add regression tests before applying provider fixes.
- [x] Submit small, separate pull requests for independent defects.
- [ ] Complete a shell-based command verification script covering the remaining `cmx vm` commands.

## Week 5 Self-Assessment

The Week 5 work concentrated on understanding and testing the shared Cloudmesh VM framework rather than implementing a new provider from scratch.

Testing demonstrated how the Click-based CLI selects the configured provider, how Jetstream authentication is obtained from `clouds.yaml`, and how the OpenStack provider uses Libcloud with native OpenStack CLI fallbacks.

Initial testing exposed several environment and provider issues, including dependency and startup problems in earlier development revisions. After upstream updates were incorporated, the work was redirected toward the current `dev2` branch.

Real Jetstream testing reproduced a VM-list fallback defect, which was documented as Issue #35 and addressed in Pull Request #36. The investigation showed that the OpenStack CLI returned an existing VM while the Cloudmesh fallback incorrectly discarded the result.

The main remaining Week 5 item is broader command-validation coverage. Manual, unit, smoke, and standalone testing have been performed, but a dedicated shell verification script covering the remaining `cmx vm` command set is still to be completed.

## Week 4 Tasks (Due Sep 24, 2026, 9am)

- [x] Assignment W4.1: VM on local machine via Makefile

    - [x] Pick a local VM framework and ensure it is installed. Multipass 1.16.3 was used on Windows.
    - [x] Write a Makefile with the necessary targets to manage a single VM.
    - [x] Configure and demonstrate management of multiple machines using the configurable `NAME` variable.
    - [x] Organize local and cloud Makefiles in separate directories.
    - [x] [W4.1 Local VM Assignment](https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week4/local)

- [x] Assignment W4.2: VM on Jetstream 2

    - [x] Install the OpenStack command-line client using `pipx`.
    - [x] Configure Jetstream access through `clouds.yaml`.
    - [x] Write a Makefile with the necessary targets to manage a Jetstream VM.
    - [x] Configure and demonstrate management of multiple Jetstream VMs using the same Makefile.
    - [x] Check the work into the repository.
    - [x] [W4.2 Jetstream Assignment](https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week4/jetstream)

- [x] Assignment W4.3: VM on Chameleon Cloud

    - [x] Use the OpenStack command-line client for Chameleon Cloud.
    - [x] Install and verify `python-chi` in a Python virtual environment.
    - [x] Configure Chameleon access through `clouds.yaml`.
    - [x] Create a KVM@TACC flavor reservation for the required VM resources.
    - [x] Write a Makefile with the necessary targets to manage a Chameleon VM.
    - [x] Configure and demonstrate management of multiple Chameleon VMs using the same Makefile.
    - [x] Check the work into the repository.
    - [x] [W4.3 Chameleon Cloud Assignment](https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week4/chameleon)

- [ ] Assignment W4.4: Review Python

    - [x] Set up and use a Python virtual environment with `venv`.
    - [x] Ensure the OpenStack command-line tool is installed using `pipx`.
    - [x] Review the use of `pip install` and `pipx install`.
    - [ ] Review import statements and create a program using `os.system("ls")`.
    - [ ] Review how to create a `__main__` block.
    - [ ] Review how to write a Python function.
    - [ ] Review how to pass command-line arguments to a Python program using `click`.
    - [ ] Review running shell commands from Python using `os.system()` and `subprocess.run()`.
    - [ ] Complete the W4.4 Python review documentation.

    Did the Python review take more than 3 hours?

    - [ ] Yes
    - [ ] No

## Week 4 Self-Assessment

Assignments W4.1 through W4.3 were completed and documented in separate directories for the local Multipass, Jetstream 2, and Chameleon Cloud environments.

The local assignment demonstrated VM lifecycle automation with Multipass and a Makefile. The same Makefile was successfully used to manage more than one virtual machine by overriding the `NAME` variable.

The Jetstream assignment extended the same Makefile-based approach to an OpenStack cloud environment. OpenStack authentication was configured through `clouds.yaml`, and multiple Jetstream virtual machines were successfully managed using one Makefile.

The Chameleon assignment required additional configuration because KVM@TACC used a reservation-specific flavor. A lease was created for two `m1.small` instances, the generated reservation flavor was incorporated into the Makefile, and multiple Chameleon virtual machines were successfully created and managed. The `python-chi` package was also installed and verified in a Python virtual environment.

The most significant challenges involved configuring the OpenStack environments correctly, combining the Jetstream and Chameleon entries in `clouds.yaml`, working with Chameleon application credentials, and understanding the KVM@TACC reservation workflow. These issues were resolved through command-line verification and incremental testing before VM creation.

The Week 4 work strengthened understanding of Makefile automation, OpenStack CLI usage, cloud-specific VM configuration, virtual environments, and management of multiple virtual machines across local and cloud platforms.

Assignment W4.4 remains in progress. The virtual-environment, `pip`, and `pipx` portions have already been exercised during W4.2 and W4.3, while the remaining Python review topics will be completed separately.

## Week 3

* [x] Assignment W3.1: VM on Jetstream (Due Sep 17, 2026, 9am)
  * [x] Start a VM on Jetstream and follow the tutorial provided.
  * [x] Reviewed the tutorial; no issues requiring a pull request were identified.
  * [x] Document the activity with a screenshot of the terminal (800x600).
  * [x] [vms.md] [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/assignments/week3/vms.md]


* [x] Assignment W3.2: VM on Chameleon Cloud (Due Sep 17, 2026, 9am)
  * [x] Set your preferred time zone in Chameleon settings.
  * [x] Make sure you have a key in your `.ssh` dir on your laptop and upload the public key to Chameleon.
  * [x] Explore the portal and browse around to develop a plan first.
  * [x] Make a reservation not exceeding 1 hour.
  * [x] Start up a VM using a Chameleon Cloud image for Ubuntu 24.04 using the smallest image size possible.
  * [x] Document the activity with a screenshot of the terminal (800x600).
  * [x] [vms.md] [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/assignments/week3/vms.md]


* [ ] Assignment W3.3: OPTIONAL: VM on public cloud (Due Sep 17, 2026, 9am)
  * [ ] Optional: Create a VM on a cloud of your choice (AWS, Azure, Google) using the free tier.
  * [ ] Document with screenshots how you created your account, ensuring sensitive information is blurred out.
  * [ ] [VM.MD](https://github.com/cloudmesh-ai-luc/YOURREPO/blob/main/assignments/week3/vm.md)


* [x] Assignment W3.4: Compare (Due Sep 17, 2026, 9am)
  * [x] Compare your experience between starting a VM on your local machine vs using Chameleon Cloud.
  * [x] Put all assignment answers into: [https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week3]
  * [x] [vms.md] [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/assignments/week3/vms.md]
     
* [x] Assignment W3.5: README.md (Due Sep 17, 2026, 9am)
  * [x] LINK to README: [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/README.md]

* [x] Assignment W3.6 git from commandline
  * [x] Pull request: [https://github.com/cloudmesh-ai-luc/AnieWall/pull/2]

## Week 2
  
* [x] Assignment W2.1: Google Account, Piazza Account post cleanup (Due Sep 10, 2026, 9am)
  * [x] Locate your account post in Piazza and add your google account.
  * [x] Correct your Chameleon ID to the registered email.
  * [x] Fix your subject line to `Firstname Lastname (lucid@luc.edu)`.


* [x] Assignment W2.2: GitHub Repository (Due Sep 10, 2026, 9am)
  * [x] Verify that you can write into a file in your assigned GitHub repository.
  * [x] Put something useful into the README such as your first and last name. [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/README.md]
  * [x] Upload your public key. [Public SSH Key] [https://github.com/AnieWall.keys]


* [x] Assignment W2.3: Backup Your Computer (Due Sep 10, 2026, 9am)
  * [x] Write a one‑paragraph explanation (4–6 sentences) on why backing up a computer is important. 
  * [x] List three real‑world consequences of not having a backup.
  * [x] Choose one backup method and outline the setup steps.
  * [x] Create a weekly backup schedule (day, time, what to back up).
  * [x] Research an example from cloud computing where a missing backup strategy led to issues and write a short incident case.
  * [x] Backup Assignment [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/assignments/week2/backup.md]


* [x] Assignment W2.4: Local VM (Due Sep 10, 2026, 9am)
  * [x] Windows: Install a terminal on Windows (Git Bash/WSL). [Used Git Bash on Windows]
  * [x] Pick a hypervisor (VirtualBox, VMware, Hyper-V, Multipass). [Microsoft Hyper-V]
  * [x] Create and start a minimal VM (e.g., Ubuntu 22.04).
  * [x] Capture proof of login with a terminal screenshot (≤ 800×600 px) showing your prompt and a command.
  * [x] Write/update the tutorial in `assignments/week1/local-vm.md`
        - (Local VM Tutorial) [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/assignments/week1/local-vm.md]
  * [x] VM Login Screenshot. [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/assignments/week1/vm-login.png]


* [x] Assignment W2.5: Project proposal (Due Sep 10, 2026, 9am)
  * [x] Start working towards a project proposal and fill out administrative fields and text. [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/project.md]


# Week 1

  * [x] Assignment W1.1: What hardware do you have? (Past Due)
    - Dell Latitude 7480 laptop with an Intel Core i5-7200U 2.50 GHz dual-core processor, 8 GB RAM
  * [x] Fill out the LUC Hardware Questionnaire.
        - LUC Hardware Questionnaire: [https://docs.google.com/forms/d/e/1FAIpQLSdxxTnj8JFrrbREcM0wQ7B9nGmqpYfBPRddhKnGE7e7Dui_lA/viewform]


* [x] Assignment W1.2: Lecture review (Past Due)
  * [x] Review all sections under LECTURES -> INTRODUCTIONS and post questions on Piazza.


* [x] Assignment W1.3: Look over the assignment sections (Past Due)
  * [x] Review all sections under ASSIGNMENTS (Overview and weekly sections).


* [x] Assignment W1.4: Create class accounts (Past Due)
  * [x] Create an account on access-ci.org.
  * [x] Create an account on chameleoncloud.org.
  * [x] Set up a GitHub account.
  * [x] Post account information to Piazza under the accounts category. [https://piazza.com/class/mt5rkdsycb31c3/post/12]


* [x] Assignment W1.5: Work ahead: Refresh knowledge about Python and Linux (Past Due)
  * [x] Review optional material in the class documentation.


* [ ] Assignment W1.6: Improve the Web Site (Past Due)
  * [ ] Update errors or notify instructors throughout the semester.

