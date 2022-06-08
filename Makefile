# Variables
.DEFAULT_GOAL := help
BASE_PATH := $(shell pwd)

# Import .env to this Makefile
ifneq (,$(wildcard ./.env))
    include .env
    export
endif


define build
	docker build -t 2fa:latest .
endef

define server-up
	docker-compose -f $(BASE_PATH)/docker-compose.yml up
endef

define server-down
	docker-compose  -f $(BASE_PATH)/docker-compose.yml down
endef

# Normalize goals
all: help build server-up server-down
.PHONY: all

##help:	@ List available tasks on this project
help:
	@fgrep -h "##" $(MAKEFILE_LIST)| sort | fgrep -v fgrep | tr -d '##'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

##build: @ Build a new docker image
build:
	$(call build)

##server-up: @ Start the server
server-up:
	$(call server-up)
	
##server-down: @ Stop the server
server-down:
	$(call server-down)	 

