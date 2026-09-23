CLOUD ?= chameleon
NAME ?= week4-chi
IMAGE ?= CC-Ubuntu24.04
FLAVOR ?= reservation:c61813c3-961a-4d83-a464-4835edb7d33a
NETWORK ?= sharednet1
KEY ?= swallace6

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
	@echo "  make create              Create a Chameleon VM"
	@echo "  make start               Start the VM"
	@echo "  make stop                Stop the VM"
	@echo "  make list                List Chameleon VMs"
	@echo "  make delete              Delete the VM"
	@echo "  make help                Show available commands"
	@echo "  make create NAME=vm2     Create another VM"
