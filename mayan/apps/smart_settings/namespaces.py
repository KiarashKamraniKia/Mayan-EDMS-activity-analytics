from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from .classes import Setting
from .literals import NAMESPACE_VERSION_INITIAL


class SettingNamespaceMetaclass(type):
    _registry = {}

    def __call__(mcls, cluster, name, **kwargs):
        if name in mcls._registry:
            raise ImproperlyConfigured(
                'Setting namespace `{}` already exists.'.format(name)
            )
        else:
            instance = super().__call__(
                cluster=cluster, name=name, **kwargs
            )
            mcls._registry[name] = instance

        return instance

    @classmethod
    def unregister(mcls, instance):
        for setting in instance.get_setting_list():
            Setting.unregister(instance=setting)

        mcls._registry.pop(instance.name, None)


class SettingNamespace(metaclass=SettingNamespaceMetaclass):
    def __init__(
        self, cluster, name, label, migration_class=None,
        version=NAMESPACE_VERSION_INITIAL
    ):
        self.cluster = cluster
        self.migration_class = migration_class
        self.name = name
        self.label = label
        self.setting_dict = {}
        self.version = version

        self.do_cluster_join()

    def __str__(self):
        return force_str(s=self.label)

    def do_cache_invalidate(self):
        for setting in self.setting_dict.values():
            setting.do_cache_invalidate()

    def do_cluster_join(self):
        cluster = self.get_cluster()
        cluster.do_namespace_join(namespace=self)

    def do_post_edit_function_call(self):
        for setting in self.setting_dict.values():
            setting.do_post_edit_function_call()

    def do_migrate(self, setting):
        if self.migration_class:
            self.migration_class(namespace=self).do_migrate(setting=setting)

    def do_setting_add(self, **kwargs):
        setting = Setting(namespace=self, **kwargs)
        self.setting_dict[setting.global_name] = setting

        return setting

    def do_setting_remove(self, setting):
        self.setting_dict.pop(setting.global_name)
        cluster = self.get_cluster()
        cluster.do_setting_remove(setting=setting)

    def get_cluster(self):
        return self.cluster

    def get_configuration_file_version(self):
        return self.cluster.get_namespace_configuration(name=self.name).get(
            'version', NAMESPACE_VERSION_INITIAL
        )

    def get_setting(self, global_name):
        return self.setting_dict[global_name]

    def get_setting_list(self):
        return sorted(
            self.setting_dict.values(), key=lambda x: x.global_name
        )


SettingNamespace.verbose_name = _(message='Settings namespace')
