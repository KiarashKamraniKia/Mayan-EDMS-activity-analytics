#!make

do_dollar_escape = $(subst $$,\$$,$(1))

PYTHON_BIN ?= python3
VERSION_SCRIPT_BIN ?= mayan/apps/dependencies/versions.py

DOCKER_CONSOLE_COLUMNS ?= `echo $$(tput cols)`
DOCKER_CONSOLE_LINES ?= `echo $$(tput lines)`

# BuildKit

DOCKER_BUILDX_BUILDER_NAME ?= mirrored
DOCKER_BUILDX_CONTEXT_NAME ?= tls-context

# Registry private

DOCKER_REGISTRY_NAME ?= $(CONFIG_DOCKER_REGISTRY_NAME)
DOCKER_REGISTRY_PASSWORD ?= $(CONFIG_DOCKER_REGISTRY_PASSWORD)

ifeq ($(origin DOCKER_REGISTRY_USERNAME), undefined)
  DOCKER_REGISTRY_USERNAME := $(CONFIG_DOCKER_REGISTRY_USERNAME)
endif

DOCKER_REGISTRY_USERNAME_ESCAPED := $(call do_dollar_escape,$(value DOCKER_REGISTRY_USERNAME))

# Registry public

DOCKER_REGISTRY_PUBLIC_NAME ?= $(CONFIG_DOCKER_REGISTRY_PUBLIC_NAME)
DOCKER_REGISTRY_PUBLIC_PASSWORD ?= $(CONFIG_DOCKER_REGISTRY_PUBLIC_PASSWORD)

ifeq ($(origin DOCKER_REGISTRY_PUBLIC_USERNAME), undefined)
  DOCKER_REGISTRY_PUBLIC_USERNAME := $(CONFIG_DOCKER_REGISTRY_PUBLIC_USERNAME)
endif

DOCKER_REGISTRY_PUBLIC_USERNAME_ESCAPED := $(call do_dollar_escape,$(value DOCKER_REGISTRY_PUBLIC_USERNAME))

# Image

DOCKER_IMAGE_NAME ?= $(CONFIG_DOCKER_IMAGE_MAYAN_NAME)
DOCKER_IMAGE_DATE_TIME ?= $(shell date -Iseconds  --utc)
DOCKER_IMAGE_VERSION ?= $(shell cat docker/rootfs/version)
DOCKER_IMAGE_VERSION_MAJOR := $(shell $(PYTHON_BIN) $(VERSION_SCRIPT_BIN) $(DOCKER_IMAGE_VERSION) major)
DOCKER_IMAGE_VERSION_MINOR := $(shell $(PYTHON_BIN) $(VERSION_SCRIPT_BIN) $(DOCKER_IMAGE_VERSION) minor)
DOCKER_IMAGE_TAG ?= $(DOCKER_IMAGE_VERSION)
DOCKER_IMAGE_BUILD_OUTPUT ?= type=docker
DOCKER_IMAGE_TAG_EXTRA ?= $(CONFIG_DOCKER_IMAGE_TAG_EXTRA)
DOCKER_IMAGE_LABELS ?= --label org.opencontainers.image.created="$(DOCKER_IMAGE_DATE_TIME)" --label org.opencontainers.image.version=$(DOCKER_IMAGE_VERSION) $(DOCKER_IMAGE_LABELS_EXTRA)
DOCKER_IMAGE_NAME_FULL = $(DOCKER_REGISTRY_NAME)/$(DOCKER_IMAGE_NAME)
DOCKER_IMAGE_NAME_FULL_TAGGED = $(DOCKER_IMAGE_NAME_FULL):$(DOCKER_IMAGE_TAG)

# The BuildKit cache manifest cannot share a tag with the image. Pushing the
# image to that tag replaces the cache manifest. The tag is deliberately not
# version scoped so that the cache survives a version increase.
DOCKER_IMAGE_BUILD_CACHE_SUFFIX ?= buildcache
DOCKER_IMAGE_BUILD_CACHE_AMD64 = $(DOCKER_IMAGE_NAME_FULL):amd64-$(DOCKER_IMAGE_BUILD_CACHE_SUFFIX)
DOCKER_IMAGE_BUILD_CACHE_ARM64 = $(DOCKER_IMAGE_NAME_FULL):arm64-$(DOCKER_IMAGE_BUILD_CACHE_SUFFIX)
DOCKER_IMAGE_PUBLIC_NAME_FULL = $(DOCKER_REGISTRY_PUBLIC_NAME)/$(DOCKER_IMAGE_NAME)

# The tag the image is published under. Separate from `DOCKER_IMAGE_TAG`,
# which is the tag it is pulled from in the private registry.
DOCKER_IMAGE_PUBLIC_TAG ?= $(DOCKER_IMAGE_TAG)

-include docker/makefiles/build.mk
-include docker/makefiles/compose.mk
-include docker/makefiles/image.mk
-include docker/makefiles/manifest.mk
-include docker/makefiles/registry.mk
-include docker/makefiles/staging.mk
-include docker/makefiles/testing.mk
