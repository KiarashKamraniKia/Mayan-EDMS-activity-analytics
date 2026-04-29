from pathlib import Path

from django.conf import settings

from mayan.apps.smart_settings.utils import get_environment_variable_full_name
from mayan.apps.storage.utils import NamedTemporaryFile, fs_cleanup
from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.views.settings import setting_paginate_by

from ..setting_clusters import setting_cluster

from .literals import ENVIRONMENT_TEST_NAME, ENVIRONMENT_TEST_VALUE


class ConfigurationFilesDomainTestCase(BaseTestCase):
    _setting_old_value = None

    def setUp(self):
        self._setting_old_value = settings.SETTINGS_BACKUP_ENABLED
        settings.SETTINGS_BACKUP_ENABLED = True
        super().setUp()

    def tearDown(self):
        settings.SETTINGS_BACKUP_ENABLED = self._setting_old_value
        self._setting_old_value = None
        super().tearDown()

    def test_config_backup_creation(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(
            filename=str(path_config_backup)
        )

        setting_cluster.do_ready()
        self.assertTrue(
            path_config_backup.exists()
        )

    def test_config_backup_creation_no_tags(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(
            filename=str(path_config_backup)
        )

        setting_cluster.do_ready()
        self.assertTrue(
            path_config_backup.exists()
        )

        with path_config_backup.open(mode='r') as file_object:
            self.assertFalse(
                '!!python/' in file_object.read()
            )

    def test_config_save(self):
        self._test_setting_namespace_create()
        self._create_test_setting()
        test_value = 'config_test_value123'

        self._test_setting.do_value_pending_set(value=test_value)

        with NamedTemporaryFile(mode='w+', encoding='utf-8', delete=True) as _test_configuration_file_object:
            setting_cluster.do_make_persistent(
                kwargs={'filepath': _test_configuration_file_object.name}
            )

            _test_configuration_file_object.seek(0)

            content = _test_configuration_file_object.read()

            self.assertTrue(test_value in content)


class EnvironmentDomainTestCase(BaseTestCase):
    def test_environment_override(self):
        test_environment_value = 'test environment value'
        test_file_value = 'test file value'

        self._test_setting_namespace_create()
        self._create_test_setting()

        environment_variable_name = get_environment_variable_full_name(
            name=self._test_setting.global_name
        )
        self._set_environment_variable(
            name=environment_variable_name, value=test_environment_value
        )

        self._test_configuration_value = test_file_value
        self._create_test_configuration_file()

        self.assertEqual(self._test_setting.value, test_environment_value)

    def test_environment_variable(self):
        environment_variable_name = get_environment_variable_full_name(
            name=ENVIRONMENT_TEST_NAME
        )
        self._set_environment_variable(
            name=environment_variable_name, value=ENVIRONMENT_TEST_VALUE
        )

        self.assertEqual(
            setting_paginate_by.value, int(ENVIRONMENT_TEST_VALUE)
        )
