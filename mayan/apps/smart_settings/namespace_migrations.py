import re


class SettingNamespaceMigration:
    @staticmethod
    def get_method_name(setting):
        return setting.global_name.lower()

    def __init__(self, namespace):
        self.namespace = namespace

    def do_migrate(self, setting):
        if self.namespace.get_configuration_file_version() != self.namespace.version:
            setting_method_name = SettingNamespaceMigration.get_method_name(
                setting=setting
            )

            # Get methods for this setting.
            pattern = r'{}_\d{{4}}'.format(setting_method_name)
            setting_methods = re.findall(
                pattern=pattern, string='\n'.join(
                    dir(self)
                )
            )

            # Get order of execution of setting methods.
            version_list = [
                method.replace(
                    '{}_'.format(setting_method_name), ''
                ) for method in setting_methods
            ]
            try:
                start = version_list.index(
                    self.namespace.get_configuration_file_version()
                )
            except ValueError:
                start = 0

            try:
                end = version_list.index(self.namespace.version)
            except ValueError:
                end = None

            value = setting.value_raw
            for version in version_list[start:end]:
                method = getattr(
                    self, self.get_method_name_full(
                        setting=setting, version=version
                    ), None
                )
                if method:
                    value = method(value=value)

            setting.value_raw = value

    def get_method_name_full(self, setting, version):
        return '{}_{}'.format(
            self.get_method_name(setting=setting), version
        )
