import re

DEFAULT_TEMPLATING_TAGS_DANGEROUS_ALLOW_LIST = 'method'

AJAX_TEMPLATE_HASH_EXCLUDE_END = '<!--mayan-templating-hash-exclude-end-->'
AJAX_TEMPLATE_HASH_EXCLUDE_START = '<!--mayan-templating-hash-exclude-start-->'

REGULAR_AJAX_TEMPLATE_HASH_EXCLUDE_PAIR = r'{}.*?{}'.format(
    re.escape(pattern=AJAX_TEMPLATE_HASH_EXCLUDE_START),
    re.escape(pattern=AJAX_TEMPLATE_HASH_EXCLUDE_END)
)
