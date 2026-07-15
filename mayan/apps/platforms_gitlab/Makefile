#!make

gitlab-ci-update: ## Update the GitLab CI file from the platform template.
gitlab-ci-update: config-env-copy
	./manage.py platforms_template gitlab-ci > .gitlab-ci.yml

gitlab-ci-run: ## Execute a GitLab CI job locally
gitlab-ci-run:
	if [ -z $(GITLAB_CI_JOB) ]; then echo "Specify the job to execute using GITLAB_CI_JOB."; exit 1; fi; \
	docker rm --force gitlab-runner || true
	docker run --detach --name gitlab-runner --restart no --volume $$PWD:$$PWD --volume /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner:latest
	docker exec --interactive --tty --workdir $$PWD gitlab-runner gitlab-runner exec docker --docker-privileged --docker-volumes /var/run/docker.sock:/var/run/docker.sock --docker-volumes $$PWD/gitlab-ci-volume:/builds $(GITLAB_CI_JOB)
	docker rm --force gitlab-runner || true

# Major releases

gitlab-ci-release-documentation: ## Trigger the documentation build and publication using GitLab CI
gitlab-ci-release-documentation:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME)
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) --tags
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_DOCUMENTATION) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_DOCUMENTATION)

gitlab-ci-release-docker-major: ## Trigger the Docker image build and publication using GitLab CI
gitlab-ci-release-docker-major:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME)
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) --tags
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_DOCKER_MAJOR) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_DOCKER_MAJOR)

gitlab-ci-release-python-major: ## Trigger the Python package build and publication using GitLab CI
gitlab-ci-release-python-major:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME)
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) --tags
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_PYTHON_MAJOR) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_PYTHON_MAJOR)

gitlab-ci-release-all-major: ## Trigger the Python package, Docker image, and documentation build and publication using GitLab CI
gitlab-ci-release-all-major:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME)
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) --tags
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_ALL_MAJOR) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_ALL_MAJOR)

# Minor releases

gitlab-ci-release-docker-minor: ## Trigger the Docker image build and publication of a minor version using GitLab CI
gitlab-ci-release-docker-minor:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME)
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) --tags
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_DOCKER_MINOR) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_DOCKER_MINOR)

gitlab-ci-release-python-minor: ## Trigger the Python package build and publication of a minor version using GitLab CI
gitlab-ci-release-python-minor:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME)
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) --tags
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_PYTHON_MINOR) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_PYTHON_MINOR)

gitlab-ci-release-all-minor: ## Trigger the Python package, Docker image build and publication of a minor version using GitLab CI
gitlab-ci-release-all-minor:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME)
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) --tags
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_ALL_MINOR) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_ALL_MINOR)

# Development releases

gitlab-ci-release-nightly: ## Trigger the Docker image build and publication of a nightly version using GitLab CI
gitlab-ci-release-nightly:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_NIGHTLY) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_NIGHTLY)

gitlab-ci-release-testing: ## Trigger the Docker image build and publication of a test version using GitLab CI
gitlab-ci-release-testing:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_RELEASES_TESTING) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_RELEASES_TESTING)

# GitOps builds

gitlab-ci-builds-docker: ## Trigger building the Docker image for all architectures.
gitlab-ci-builds-docker:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCKER_ALL) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCKER_ALL)

gitlab-ci-builds-docker-amd64: ## Trigger building the Docker image for AMD64.
gitlab-ci-builds-docker-amd64:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCKER_AMD64) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCKER_AMD64)

gitlab-ci-builds-docker-arm64: ## Trigger building the Docker image for ARM64.
gitlab-ci-builds-docker-arm64:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCKER_ARM64) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCKER_ARM64)

gitlab-ci-builds-documentation: ## Trigger building the documentation.
gitlab-ci-builds-documentation:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCUMENTATION) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_BUILDS_DOCUMENTATION)

gitlab-ci-builds-python: ## Trigger building the Python package.
gitlab-ci-builds-python:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_BUILDS_PYTHON) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_BUILDS_PYTHON)

# GitOps deployments

gitlab-ci-deployments-demo: ## Trigger the demo deployment
gitlab-ci-deployments-demo:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_DEMO) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_DEMO)

gitlab-ci-deployments-staging: ## Trigger the staging deployment
gitlab-ci-deployments-staging:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING_ALL) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING_ALL)

gitlab-ci-deployments-staging-amd64: ## Trigger the AMD64 staging deployment
gitlab-ci-deployments-staging-amd64:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING_AMD64) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING_AMD64)

gitlab-ci-deployments-staging-arm64: ## Trigger the ARM64 staging deployment
gitlab-ci-deployments-staging-arm64:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING_ARM64) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING_ARM64)

# GitOps testing

gitlab-ci-tests-all: ## Trigger all tests as a CD/CI pipeline
gitlab-ci-tests-all:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_TESTS_ALL) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_TESTS_ALL)

gitlab-ci-tests-docker: ## Trigger a build and test of a Docker image as a CD/CI pipeline
gitlab-ci-tests-docker:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_TESTS_DOCKER) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_TESTS_DOCKER)

gitlab-ci-tests-python: ## Trigger Python tests as a CD/CI pipeline
gitlab-ci-tests-python:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_TESTS_PYTHON) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_TESTS_PYTHON)

# GitOps Combined

gitlab-ci-try-staging: ## Trigger a multi arch build and deploy to staging.
gitlab-ci-try-staging:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_TRY_STAGING_ALL) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_TRY_STAGING_ALL)

gitlab-ci-try-staging-amd64: ## Trigger an AMD64 build and deploy to staging.
gitlab-ci-try-staging-amd64:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_TRY_STAGING_AMD64) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_TRY_STAGING_AMD64)

gitlab-ci-try-staging-arm64: ## Trigger an ARM64 build and deploy to staging.
gitlab-ci-try-staging-arm64:
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) :$(CONFIG_GITLAB_CI_BRANCH_TRY_STAGING_ARM64) || true
	git push $(CONFIG_GITLAB_CI_REMOTE_NAME) HEAD:$(CONFIG_GITLAB_CI_BRANCH_TRY_STAGING_ARM64)
