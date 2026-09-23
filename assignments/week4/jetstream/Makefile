CLOUD ?= jetstream
NAME ?= week4-js
IMAGE ?= Featured-Minimal-Ubuntu24
FLAVOR ?= m3.tiny
NETWORK ?= auto_allocated_network
KEY ?= swallace1

.PHONY: create start stop list delete help

create:
	openstack --os-cloud $(CLOUD) server create \
		--image $(IMAGE) \
		--flavor $(FLAVOR) \
		--network $(NETWORK) \
		--key-name $(KEY) \
		$(NAME)

start:
	openstack --os-cloud $(CLOUD) server start $(NAME)

stop:
	openstack --os-cloud $(CLOUD) server stop $(NAME)

list:
	openstack --os-cloud $(CLOUD) server list

delete:
	openstack --os-cloud $(CLOUD) server delete $(NAME)

help:
	@echo "Available commands:"
	@echo "  make create              Create a Jetstream VM"
	@echo "  make start               Start the VM"
	@echo "  make stop                Stop the VM"
	@echo "  make list                List Jetstream VMs"
	@echo "  make delete              Delete the VM"
	@echo "  make help                Show available commands"
	@echo "  make create NAME=vm2     Create another VM"
