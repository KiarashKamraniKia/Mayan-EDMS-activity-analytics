import re

import mayan
from mayan.apps.dependencies.versions import Version

from .literals import DEFAULT_CACHE_WHEN


def get_cache_entry(key, path_list, policy, key_fallback_list=None):
    result = {
        'key': key, 'paths': list(path_list), 'policy': policy,
        'when': DEFAULT_CACHE_WHEN
    }

    if key_fallback_list:
        result['fallback_keys'] = list(key_fallback_list)

    return result


def get_cache_key_slug(value):
    """
    Cache keys are used as file names by the runner and cannot contain
    characters like `/`, `:`, or spaces.
    """
    result = re.sub(
        pattern=r'[^0-9A-Za-z]+', repl='-', string=value
    )

    return result.strip('-')


def get_cache_version():
    version_base = Version(version_string=mayan.__version__)
    version_upstream = Version(
        version_string=version_base.as_upstream()
    )

    version_current = version_upstream.as_minor()
    version_previous = None

    if version_upstream.minor > 0:
        version_previous = '{}.{}'.format(
            version_upstream.major, version_upstream.minor - 1
        )

    return (version_current, version_previous)


def get_package_list(package_group_list):
    """
    Merge, deduplicate and sort a series of package groups.
    """
    result = set()

    for package_group in package_group_list:
        result.update(
            package_group.split()
        )

    return ' '.join(
        sorted(result)
    )


def get_string_literal(value):
    """
    Django passes quoted template tag literals as `SafeString`. Its
    `__str__` returns itself, so `str()` does not demote it and the YAML
    dumper serializes the value as a Python object tag instead of as a
    scalar. Joining the value produces a plain `str`.
    """
    return ''.join(
        (value,)
    )
