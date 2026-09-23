# W4.3 - VM Management on Chameleon Cloud

## Environment

The assignment was completed using the Chameleon Cloud KVM@TACC environment.

The OpenStack command-line client was installed through `pipx`, and the `python-chi` package was installed in a Python virtual environment.

The Chameleon environment was configured in:

```text
~/.config/openstack/clouds.yaml
```
The configuration contains separate cloud entries for Jetstream and Chameleon. No credentials or application secrets are stored in the repository.

No credentials or application secrets are stored in the repository.

## Chameleon Resources

The following Chameleon Cloud resources were used:

- Cloud: `chameleon`
- Image: `CC-Ubuntu24.04`
- Base flavor: `m1.small`
- Network: `sharednet1`
- SSH keypair: `swallace6`

KVM@TACC required a flavor reservation before the virtual machines could be launched. A lease named `week4-chameleon-lease` was created for two `m1.small` instances.

The active lease generated the following reservation-specific flavor:

```text
reservation:c61813c3-961a-4d83-a464-4835edb7d33a
```

The reservation-specific flavor was used by the Makefile to create the virtual machines.

## Makefile Targets

The Makefile implements the following targets:

```text
make create
make start
make stop
make list
make delete
make help
```

The default virtual machine name is:

```text
week4-chi
```

The `create` target creates a Chameleon virtual machine using the configured image, reservation flavor, network, and SSH keypair.

The `start` and `stop` targets control the virtual machine state.

The `list` target displays the available Chameleon virtual machines.

The `delete` target removes the selected virtual machine.

The `help` target displays the available Makefile commands.

## Managing Multiple Virtual Machines

The Makefile uses a configurable `NAME` variable. This allows multiple virtual machines to be managed using the same Makefile.

For example:

```bash
make create
make create NAME=vm2
make list
```

Two Chameleon virtual machines, `week4-chi` and `vm2`, were successfully created using the same Makefile.

Individual virtual machines can also be managed by overriding the `NAME` variable:

```bash
make stop NAME=vm2
make start NAME=vm2
make delete NAME=vm2
```

This demonstrates that multiple virtual machines can be managed without creating separate Makefiles.

## Python-Chi

The `python-chi` package was installed inside a Python virtual environment instead of Conda.

The installation was verified with:

```bash
python -c "import chi; print('python-chi installed successfully')"
```

The verification completed successfully.

## Directory Organization

The Week 4 environments are organized into separate directories:

```text
assignments/
└── week4/
    ├── local/
    │   ├── Makefile
    │   └── README.md
    ├── jetstream/
    │   ├── Makefile
    │   └── README.md
    └── chameleon/
        ├── Makefile
        └── README.md
```

This structure separates local Multipass automation from Jetstream and Chameleon Cloud automation.

## Summary

The Chameleon Cloud environment was successfully configured using the OpenStack command-line client and `python-chi`.

A KVM@TACC reservation was created for two `m1.small` virtual machine instances. The reservation-specific flavor was incorporated into the Makefile, and the same Makefile was used to create and manage multiple virtual machines.

The assignment demonstrates automated virtual machine lifecycle management using Make and OpenStack on Chameleon Cloud.
