# W4.1 - Local VM Management with Multipass and Make

## Local VM Framework

Multipass was selected as the local virtual machine framework. Multipass version 1.16.3 was installed on Windows and used with the available virtualization environment.

The installation was verified using:

```bash
multipass version
```

## Makefile Targets

A Makefile was created to automate the basic lifecycle of a local virtual machine.

The following targets were implemented:

- `make create` - creates the default VM named `week4-vm`
- `make start` - starts the VM
- `make stop` - stops the VM
- `make list` - displays available Multipass VMs and their current state
- `make delete` - deletes and purges the VM
- `make help` - displays the available Makefile commands

## Managing Multiple Virtual Machines

The Makefile uses a configurable `NAME` variable:

```makefile
NAME ?= week4-vm
```

The default virtual machine can be created with:

```bash
make create
```

A different virtual machine can be created and managed by overriding the `NAME` variable:

```bash
make create NAME=vm2
make stop NAME=vm2
make start NAME=vm2
make delete NAME=vm2
```

Two Multipass virtual machines, `week4-vm` and `vm2`, were successfully created and managed using the same Makefile.

This demonstrates that multiple virtual machines can be managed without creating separate Makefiles.

## VM Lifecycle Verification

The virtual machine lifecycle was tested using the Makefile commands.

The VM state was checked with:

```bash
make list
```

The default VM was stopped with:

```bash
make stop
```

The stopped state was verified using `make list`, after which the VM was started again with:

```bash
make start
```

The VM returned to the running state successfully.

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

Multipass was successfully used to create and manage local virtual machines on Windows.

A Makefile automated virtual machine creation, startup, shutdown, listing, and deletion. The configurable `NAME` variable also allowed multiple virtual machines to be managed using the same Makefile.

The assignment demonstrates basic virtual machine lifecycle automation using Make and Multipass.
