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

A student-specific Chameleon validation script was preserved in a local development commit for documentation and testing evidence. It was not submitted as a pull request because the script contains environment-specific configuration and was intended to validate Professor Gregor's new OpenStackSDK and `python-chi` workflow rather than modify the shared implementation.

## Week 6 Self-Assessment

Week 6 completed real-provider validation against both Jetstream and Chameleon Cloud.
The Jetstream work focused on identifying reproducible provider defects, documenting them through GitHub issues, developing regression tests, and submitting pull requests. Testing demonstrated how cmx, Libcloud, OpenStack CLI fallbacks, clouds.yaml, and the underlying OpenStack services interact during provider operations.
The standalone Jetstream workflow successfully created an m3.tiny VM, reached the ACTIVE state, attached a floating IP, and removed the temporary resources after testing.
The Chameleon work required a different provider path because the current Chameleon implementation is moving away from the previous Libcloud-based approach. The updated workflow used OpenStackSDK, python-chi, and Blazar reservations. Several authentication and session compatibility problems were isolated and resolved during adaptation of the standalone reference script.
The final Chameleon validation successfully created an active reservation, launched a reserved KVM virtual machine, associated a floating IP, configured SSH access, and established an SSH session into the Ubuntu 24.04 instance. Resource cleanup was then completed and independently verified.
This present assignment therefore demonstrated successful real-cloud validation across two OpenStack providers while also providing practical experience with provider abstraction, service catalogs, authentication sessions, reservation systems, SDK compatibility, failure diagnosis, regression testing, and cloud resource cleanup.
