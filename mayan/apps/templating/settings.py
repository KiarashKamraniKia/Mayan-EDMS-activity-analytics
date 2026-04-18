from django.utils.translation import gettext_lazy as _

from mayan.apps.smart_settings.settings import setting_cluster

from .literals import DEFAULT_TEMPLATING_TAGS_DANGEROUS_ALLOW_LIST

setting_namespace = setting_cluster.do_namespace_add(
    label=_(message='Templating'), name='templating'
)

setting_templating_dangerous_tags_allow_list = setting_namespace.do_setting_add(
    default=DEFAULT_TEMPLATING_TAGS_DANGEROUS_ALLOW_LIST,
    global_name='TEMPLATING_TAGS_DANGEROUS_ALLOW_LIST', help_text=_(
        message='A comma separated list of dangerous templating tags and '
        'filters that are allowed.'
    )
)
