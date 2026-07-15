from mayan.literals import (
    DOCKER_CLI_IMAGE_VERSION, DOCKER_LINUX_IMAGE_NAME, DOCKER_LINUX_IMAGE_TAG
)

DEFAULT_APK_CACHE_PATH = '.cache/apk'
DEFAULT_APT_CACHE_PATH = '.cache/apt'
DEFAULT_PIP_CACHE_PATH = '.cache/pip'
DEFAULT_VENV_CACHE_PATH = 'venv'

DEFAULT_CACHE_POLICY = 'pull-push'
DEFAULT_CACHE_WHEN = 'always'

VENV_CACHE_IMAGE_MAP = {
    'alpine': DOCKER_CLI_IMAGE_VERSION,
    'debian': '{}:{}'.format(DOCKER_LINUX_IMAGE_NAME, DOCKER_LINUX_IMAGE_TAG)
}

VENV_CACHE_KEY_FILE_LIST = (
    'requirements/production.txt', 'requirements/testing.txt'
)
