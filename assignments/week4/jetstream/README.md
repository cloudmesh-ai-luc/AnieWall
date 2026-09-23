# W4.2 - Jetstream 2 VM Management with OpenStack and Make

## OpenStack Command-Line Client

The OpenStack command-line client was installed using `pipx` as required for the assignment.

The installed client was verified with:

```bash
openstack --version
```

The Jetstream cloud configuration in `~/.config/openstack/clouds.yaml` was used for OpenStack authentication. The configuration file remains local to the system and is not stored in the repository.

## Jetstream Configuration

The Makefile uses the following Jetstream resources:

- Cloud: `jetstream`
- Image: `Featured-Minimal-Ubuntu24`
- Flavor: `m3.tiny`
- Network: `auto_allocated_network`
- SSH keypair: `swallace1`

No credentials or application secrets are stored in the repository.

## Makefile Targets

The following targets were implemented:

- `make create` - creates a Jetstream VM
- `make start` - starts the VM
- `make stop` - stops the VM
- `make list` - lists Jetstream VMs
- `make delete` - deletes the VM
- `make help` - displays available commands

## Managing Multiple Virtual Machines

The Makefile uses a configurable `NAME` variable.

The default VM is:

```makefile
NAME ?= week4-js
```

A different VM can be managed by overriding the variable:

```bash
make create NAME=vm2
make stop NAME=vm2
make start NAME=vm2
make delete NAME=vm2
```

Two Jetstream instances, `week4-js` and `vm2`, were successfully created and managed using the same Makefile.

## Directory Organization

## Directory Organization

The Week 4 environments are separated into directories:

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

The Jetstream 2 environment was successfully configured for command-line management using the OpenStack client.

A Makefile was used to automate virtual machine creation, startup, shutdown, listing, and deletion. The configurable `NAME` variable also allowed multiple Jetstream virtual machines to be managed using the same Makefile.

The assignment demonstrates automated virtual machine lifecycle management using Make and the OpenStack command-line interface on Jetstream 2.
