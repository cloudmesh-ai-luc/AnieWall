# W4.2 - Jetstream 2 VM Management with OpenStack and Make

## OpenStack Command-Line Client

The OpenStack command-line client was installed using `pipx` as required for the assignment.

The installed client was verified with:

```bash
openstack --version

The existing jetstream configuration in ~/.config/openstack/clouds.yaml was used to authenticate to the cloud.

## Jetstream Configuration

The Makefile uses the following Jetstream resources:

- Cloud: `openstack`
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

The Makefile uses a configurable NAME variable.

The default VM is:

```makefile
NAME ?= week4-js

A different VM can be managed by overriding the variable:

```markdown
```bash
- make create NAME=vm2
- make stop NAME=vm2
- make start NAME=vm2
- make delete NAME=vm2

Two Jetstream instances, week4-js and vm2, were successfully created and managed using the same Makefile.

## Directory Organization

The Week 4 environments are separated into directories:

assignments/
└── week4/
    ├── local/
    ├── jetstream/
    │   ├── Makefile
    │   └── README.md
    └── chameleon/

This structure separates local Multipass automation from Jetstream and Chameleon cloud automation.
