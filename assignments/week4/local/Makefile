NAME ?= week4-vm

.PHONY: create start stop list delete help

create:
	multipass launch --name $(NAME)

start:
	multipass start $(NAME)

stop:
	multipass stop $(NAME)

list:
	multipass list

delete:
	multipass delete --purge $(NAME)

help:
	@echo "Available commands:"
	@echo "  make create              Create the VM"
	@echo "  make start               Start the VM"
	@echo "  make stop                Stop the VM"
	@echo "  make list                List Multipass VMs"
	@echo "  make delete              Delete the VM"
	@echo "  make create NAME=vm2     Create another VM"
