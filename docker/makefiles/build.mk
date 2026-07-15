#!make

# BuildKit

docker-buildkitd-config-create:
	@echo "debug = true" > /tmp/buildkitd.toml
	@if [ "$(DOCKER_MIRROR)" ]; then \
		echo "" >> /tmp/buildkitd.toml; \
		echo '[registry."docker.io"]' >> /tmp/buildkitd.toml; \
		echo '  mirrors = ["$(DOCKER_MIRROR)"]' >> /tmp/buildkitd.toml; \
	fi

docker-buildx-create: docker-buildkitd-config-create
	@if docker buildx inspect $(DOCKER_BUILDX_BUILDER_NAME) > /dev/null 2>&1; then \
		docker buildx use $(DOCKER_BUILDX_BUILDER_NAME); \
	else \
		docker context create \
		$(DOCKER_BUILDX_CONTEXT_NAME); \
		docker buildx create \
		--bootstrap \
		--config /tmp/buildkitd.toml \
		--driver docker-container \
		--name $(DOCKER_BUILDX_BUILDER_NAME) \
		--use $(DOCKER_BUILDX_CONTEXT_NAME); \
	fi

docker-buildx-rm: ## Delete the buildx builder and everything it has cached.
docker-buildx-rm:
	docker buildx rm \
	$(DOCKER_BUILDX_BUILDER_NAME) || true
	docker context rm \
	$(DOCKER_BUILDX_CONTEXT_NAME) || true

docker-buildx-stop:
	docker buildx stop \
	$(DOCKER_BUILDX_BUILDER_NAME)

docker-build-all: ## Build images for all platforms.
docker-build-all: docker-dockerfile-update docker-buildx-create docker-build-amd64 docker-build-arm64 docker-buildx-stop

docker-build-amd64: ## Build a new amd64 image.
	DOCKER_BUILDKIT=1 \
	docker build \
	--build-arg APT_PROXY=$(APT_PROXY) \
	--build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) \
	--build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) \
	--build-arg HTTP_PROXY=$(HTTP_PROXY) \
	--build-arg HTTPS_PROXY=$(HTTPS_PROXY) \
	--builder $(DOCKER_BUILDX_BUILDER_NAME) \
	--cache-from type=registry,ref=$(DOCKER_IMAGE_BUILD_CACHE_AMD64) \
	--cache-to type=registry,ref=$(DOCKER_IMAGE_BUILD_CACHE_AMD64),mode=max \
	--file docker/Dockerfile $(DOCKER_IMAGE_LABELS) \
	--output $(DOCKER_IMAGE_BUILD_OUTPUT) \
	--platform linux/amd64 \
	--tag $(DOCKER_IMAGE_NAME_FULL_TAGGED)-amd64 \
	.

docker-build-arm64: ## Build a new arm64 image.
	DOCKER_BUILDKIT=1 \
	docker build \
	--build-arg APT_PROXY=$(APT_PROXY) \
	--build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) \
	--build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) \
	--build-arg HTTP_PROXY=$(HTTP_PROXY) \
	--build-arg HTTPS_PROXY=$(HTTPS_PROXY) \
	--builder $(DOCKER_BUILDX_BUILDER_NAME) \
	--cache-from type=registry,ref=$(DOCKER_IMAGE_BUILD_CACHE_ARM64) \
	--cache-to type=registry,ref=$(DOCKER_IMAGE_BUILD_CACHE_ARM64),mode=max \
	--file docker/Dockerfile $(DOCKER_IMAGE_LABELS) \
	--output $(DOCKER_IMAGE_BUILD_OUTPUT) \
	--platform linux/arm64 \
	--tag $(DOCKER_IMAGE_NAME_FULL_TAGGED)-arm64 \
	.

# Dockerfile

docker-dockerfile-update: ## Update the Dockerfile file from the platform template.
docker-dockerfile-update: config-env-copy
	./manage.py platforms_template docker_dockerfile > docker/Dockerfile
