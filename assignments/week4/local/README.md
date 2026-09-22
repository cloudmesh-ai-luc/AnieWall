# W4.1 - Local VM Management with Multipass and Make

## Local VM Framework

Multipass was selected as the local virtual machine framework. Multipass version 1.16.3 was installed on Windows and used with the available virtualization environment.

## Makefile Targets

A Makefile was created to automate the basic lifecycle of a virtual machine.

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
