import os

from django.conf import settings
from django.utils.encoding import force_bytes

from mayan.apps.storage.utils import NamedTemporaryFile, fs_cleanup
from mayan.apps.testing.tests.mixins import EnvironmentTestCaseMixin

from ..setting_clusters import setting_cluster
from ..setting_domains.configuration_files import SettingDomainConfigurationFile
from ..utils import (
    BaseSetting, SettingNamespaceSingleton, get_environment_variable_full_name
)

from .literals import (
    TEST_BOOTSTAP_SETTING_NAME, TEST_NAMESPACE_LABEL, TEST_NAMESPACE_NAME,
    TEST_SETTING_DEFAULT_VALUE, TEST_SETTING_GLOBAL_NAME
)


class BoostrapSettingTestMixin:
    def _create_test_bootstrap_singleton(self):
        self.test_globals = {}
        self.test_globals['BASE_DIR'] = ''
        self._test_setting_namespace_singleton = SettingNamespaceSingleton(
            global_symbol_table=self.test_globals
        )

    def _register_test_boostrap_setting(self):
        kwargs = {'default_value': 'value default', 'has_default': True}

        SettingNamespaceSingleton.register_setting(
            klass=BaseSetting, kwargs=kwargs, name=TEST_BOOTSTAP_SETTING_NAME
        )


class SettingClusterTestMixin(EnvironmentTestCaseMixin):
    def setUp(self):
        super().setUp()
        setting_cluster.do_cache_invalidate()

        environment_variable_name = get_environment_variable_full_name(
            name='CONFIGURATION_FILEPATH'
        )

        with NamedTemporaryFile(delete=False) as self._test_setting_config_file_object:
            settings.CONFIGURATION_FILEPATH = self._test_setting_config_file_object.name
            os.environ[
                environment_variable_name
            ] = self._test_setting_config_file_object.name

        setting_cluster.do_cache_invalidate()

    def tearDown(self):
        fs_cleanup(filename=self._test_setting_config_file_object.name)
        setting_cluster.do_cache_invalidate()
        super().tearDown()


class SettingClusterViewTestMixin(SettingClusterTestMixin):
    def _request_cluster_configuration_save_view(self):
        return self.post(
            viewname='settings:setting_cluster_configuration_save'
        )


class SettingNamespaceTestMixin(SettingClusterTestMixin):
    _test_setting_namespace_create_auto = False

    def setUp(self):
        super().setUp()
        self._test_setting_namespace_list = []

        if self._test_setting_namespace_create_auto:
            self._test_setting_namespace_create()

    def tearDown(self):
        for test_setting_namespace in self._test_setting_namespace_list:
            self._test_setting_namespace_remove(
                name=test_setting_namespace.name
            )

        super().tearDown()

    def _test_setting_namespace_create(self, label=None, name=None, **kwargs):
        test_setting_namespace_list_count = len(
            self._test_setting_namespace_list
        )

        if name is None:
            name = '{}_{}'.format(
                TEST_NAMESPACE_NAME, test_setting_namespace_list_count
            )

        if label is None:
            label = '{}_{}'.format(
                TEST_NAMESPACE_LABEL, test_setting_namespace_list_count
            )

        self._test_setting_namespace = setting_cluster.do_namespace_add(
            label=label, name=name, **kwargs
        )
        self._test_setting_namespace_list.append(
            self._test_setting_namespace
        )

    def _test_setting_namespace_remove(self, name=None):
        if name:
            namespace = setting_cluster.get_namespace(name=name)
        else:
            namespace = self._test_setting_namespace

        setting_cluster.do_namespace_remove(namespace=namespace)
        index = self._test_setting_namespace_list.index(namespace)
        self._test_setting_namespace_list.pop(index)


class SettingNamespaceViewTestMixin(SettingNamespaceTestMixin):
    def _request_namespace_detail_view(self, namespace_name=None):
        kwargs = {
            'namespace_name': namespace_name or self._test_setting_namespace.name
        }

        return self.get(
            kwargs=kwargs, viewname='settings:setting_namespace_detail'
        )

    def _request_namespace_list_view(self):
        return self.get(viewname='settings:setting_cluster_namespace_list')


class SettingTestMixin(SettingNamespaceTestMixin):
    _test_configuration_file_object = None
    _test_configuration_value = None
    _test_setting_global_name = None

    def setUp(self):
        # Make sure every test starts with fresh setting values.

        super().setUp()
        self._test_setting_list = []

    def tearDown(self):
        for test_setting in self._test_setting_list:
            test_setting.namespace.do_setting_remove(setting=test_setting)

        if self._test_configuration_file_object:
            fs_cleanup(filename=self._test_configuration_file_object.name)

        super().tearDown()

    def _create_test_configuration_file(self, callback=None):
        if not self._test_setting_global_name:
            self._test_setting_global_name = self._test_setting.global_name

        test_config_entry = {
            self._test_setting_global_name: self._test_configuration_value
        }

        with NamedTemporaryFile(delete=False) as _test_configuration_file_object:
            # Needed to load the config file from the Setting class
            # after bootstrap.
            settings.CONFIGURATION_FILEPATH = _test_configuration_file_object.name
            # Needed to update the globals before Mayan has loaded.

            environment_variable_name = get_environment_variable_full_name(
                name='CONFIGURATION_FILEPATH'
            )

            self._set_environment_variable(
                name=environment_variable_name,
                value=_test_configuration_file_object.name
            )

            data_serialized = SettingDomainConfigurationFile.serialize_data(
                data=test_config_entry
            )

            data_bytes = force_bytes(s=data_serialized)
            _test_configuration_file_object.write(data_bytes)
            _test_configuration_file_object.seek(0)
            setting_cluster.do_cache_invalidate()

            if callback:
                callback()

    def _create_test_setting(self, validation_function=None):
        self._test_setting = self._test_setting_namespace.do_setting_add(
            default=TEST_SETTING_DEFAULT_VALUE,
            global_name=TEST_SETTING_GLOBAL_NAME,
            validation_function=validation_function
        )


class SettingViewTestMixin(SettingTestMixin):
    def _request_setting_edit_view(self, value):
        data = {'value': value}
        kwargs = {'setting_global_name': self._test_setting.global_name}

        return self.post(
            data=data, kwargs=kwargs, viewname='settings:setting_edit_view'
        )

    def _request_setting_revert_view(self):
        kwargs = {'setting_global_name': self._test_setting.global_name}

        return self.post(
            kwargs=kwargs, viewname='settings:setting_revert_view'
        )


class TestMixinSettingDataType:
    _test_setting = None
    _test_setting_value = None

    def _do_test_setting_value_set(self):
        old_value = self._test_setting.value

        value_string = '{}'.format(self._test_setting_value)
        self._test_setting.do_value_pending_set(value=value_string)

        has_value_pending = self._test_setting.get_has_value_pending()
        self.assertEqual(has_value_pending, True)

        has_value_pending = self._test_setting.get_has_value_pending()
        self.assertEqual(has_value_pending, True)

        has_value_new = self._test_setting.get_has_value_new()
        self.assertEqual(has_value_new, True)

        value_current = self._test_setting.get_value_pending()
        self.assertEqual(value_current, self._test_setting_value)

        # Restore the setting.
        self._test_setting.do_value_pending_set(value=old_value)
