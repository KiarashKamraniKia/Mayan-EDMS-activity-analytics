from django.template import Library

from mayan.apps.platforms.utils import yaml_dump
from mayan.literals import LINUX_PACKAGES_DEBIAN_PUSH

from .literals import (
    DEFAULT_APK_CACHE_PATH, DEFAULT_APT_CACHE_PATH, DEFAULT_CACHE_POLICY,
    DEFAULT_PIP_CACHE_PATH, DEFAULT_VENV_CACHE_PATH, VENV_CACHE_IMAGE_MAP,
    VENV_CACHE_KEY_FILE_LIST
)
from .utils import (
    get_cache_entry, get_cache_key_slug, get_cache_version, get_package_list,
    get_string_literal
)

register = Library()


@register.simple_tag(name='platforms_gitlab_ci_cache_before_script')
def tag_platforms_gitlab_ci_cache_before_script(
    indent, apk=False, apt=False, pip=False, venv=None
):
    data = []

    if apk:
        data.extend(
            [
                'echo ${APK_CACHE_DIR}',
                'mkdir -p ${APK_CACHE_DIR}',
                'rm -f /etc/apk/cache',
                'ln -s ${APK_CACHE_DIR} /etc/apk/cache',
                'apk update'
            ]
        )

    if apt:
        data.extend(
            [
                'export APT_STATE_LISTS=${APT_CACHE_DIR}/lists && export APT_CACHE_ARCHIVES=${APT_CACHE_DIR}/archives',
                'mkdir -p "${APT_STATE_LISTS}/partial" && mkdir -p "${APT_CACHE_ARCHIVES}/partial"',
                'printf "dir::state::lists    ${APT_STATE_LISTS};\\ndir::cache::archives    ${APT_CACHE_ARCHIVES};\\n" > /etc/apt/apt.conf.d/99gitlab-ci-cache',
                'if [ "${APT_PROXY}" ]; then echo "Acquire::http { Proxy \\"http://${APT_PROXY}\\"; };" > /etc/apt/apt.conf.d/01proxy; fi',
                'apt-get update'
            ]
        )

    if pip:
        data.extend(
            [
                'mkdir -p ${PIP_CACHE_DIR}'
            ]
        )

    if venv:
        # A restored virtual environment is only a warm start. The
        # `dev-setup-python-*` targets still run and reconcile it against the
        # requirement files.
        data.extend(
            [
                'if [ -x {path}/bin/python ]; then echo "Restored virtual environment cache."; else rm -rf {path}; fi'.format(
                    path=DEFAULT_VENV_CACHE_PATH
                )
            ]
        )

    return yaml_dump(data=data, indent=indent)


@register.simple_tag(name='platforms_gitlab_ci_cache_paths')
def tag_platforms_gitlab_ci_cache_paths(
    indent, apk=False, apt=False, pip=False, policy=DEFAULT_CACHE_POLICY,
    venv=None
):
    cache_list = []

    policy = get_string_literal(value=policy)

    version_current, version_previous = get_cache_version()

    def do_cache_entry_add(name, path_list):
        key_fallback_list = None

        if version_previous:
            key_fallback_list = [
                '{}-cache-{}'.format(name, version_previous)
            ]

        cache_list.append(
            get_cache_entry(
                key='{}-cache-{}'.format(name, version_current),
                key_fallback_list=key_fallback_list, path_list=path_list,
                policy=policy
            )
        )

    if apk:
        do_cache_entry_add(
            name='apk', path_list=(DEFAULT_APK_CACHE_PATH,)
        )

    if apt:
        do_cache_entry_add(
            name='apt', path_list=(DEFAULT_APT_CACHE_PATH,)
        )

    if pip:
        do_cache_entry_add(
            name='pip', path_list=(DEFAULT_PIP_CACHE_PATH,)
        )

    if venv:
        image_slug = get_cache_key_slug(
            value=VENV_CACHE_IMAGE_MAP[
                get_string_literal(value=venv)
            ]
        )

        cache_list.append(
            get_cache_entry(
                key={
                    'files': list(VENV_CACHE_KEY_FILE_LIST),
                    'prefix': 'venv-cache-{}-{}'.format(
                        image_slug, version_current
                    )
                }, path_list=(DEFAULT_VENV_CACHE_PATH,), policy=policy
            )
        )

    return yaml_dump(data=cache_list, indent=indent)


@register.simple_tag(name='platforms_gitlab_ci_cache_variables')
def tag_platforms_gitlab_ci_cache_variables(
    indent, apk=False, apt=False, pip=False
):
    apk_cache_path = DEFAULT_APK_CACHE_PATH
    apt_cache_path = DEFAULT_APT_CACHE_PATH
    pip_cache_path = DEFAULT_PIP_CACHE_PATH
    variables = {}

    if apk:
        variables['APK_CACHE_DIR'] = f'${{CI_PROJECT_DIR}}/{apk_cache_path}'

    if apt:
        variables['APT_CACHE_DIR'] = f'${{CI_PROJECT_DIR}}/{apt_cache_path}'

    if pip:
        variables['PIP_CACHE_DIR'] = f'${{CI_PROJECT_DIR}}/{pip_cache_path}'

    return yaml_dump(data=variables, indent=indent)


@register.simple_tag(name='platforms_gitlab_ci_docker_variables')
def tag_platforms_gitlab_ci_docker_variables(indent):
    variables = {
        'DOCKER_BUILDKIT': '1',
        'DOCKER_DRIVER': 'overlay2',
        'DOCKER_HOST': 'tcp://docker:2375',
        'DOCKER_TLS_CERTDIR': ''
    }

    return yaml_dump(data=variables, indent=indent)


@register.simple_tag(name='platforms_gitlab_ci_package_list')
def tag_platforms_gitlab_ci_package_list(*args):
    return get_package_list(package_group_list=args)


@register.simple_tag(name='platforms_gitlab_ci_ssh_before_script')
def tag_platforms_gitlab_ci_ssh_before_script(indent, known_hosts, private_key):
    data = [
        'mkdir --parents ~/.ssh',
        'chmod 700 ~/.ssh',
        'echo "{}" > ~/.ssh/known_hosts'.format(known_hosts),
        'chmod 644 ~/.ssh/known_hosts',
        '\'which ssh-agent || ( apt-get update --yes && apt-get install --yes --no-install-recommends {debian_packages} )\''.format(debian_packages=LINUX_PACKAGES_DEBIAN_PUSH),
        'eval $(ssh-agent -s)',
        'echo "{}" | tr -d \'\\r\' | ssh-add - > /dev/null'.format(private_key)
    ]

    return yaml_dump(data=data, indent=indent)
