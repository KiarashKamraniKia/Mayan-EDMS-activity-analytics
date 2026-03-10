from pathlib import Path

from django.conf import settings

from mayan.apps.storage.utils import fs_cleanup
from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.views.settings import setting_paginate_by

from ..settings import setting_cluster

from .literals import ENVIRONMENT_TEST_NAME, ENVIRONMENT_TEST_VALUE


class ConfigurationFilesDomainTestCase(BaseTestCase):
    def test_config_backup_creation(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(
            filename=str(path_config_backup)
        )

        setting_cluster.do_last_known_good_save()
        self.assertTrue(
            path_config_backup.exists()
        )

    def test_config_backup_creation_no_tags(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(
            filename=str(path_config_backup)
        )

        setting_cluster.do_last_known_good_save()
        self.assertTrue(
            path_config_backup.exists()
        )

        with path_config_backup.open(mode='r') as file_object:
            self.assertFalse(
                '!!python/' in file_object.read()
            )


class EnvironmentDomainTestCase(BaseTestCase):
    def test_environment_override(self):
        test_environment_value = 'test environment value'
        test_file_value = 'test file value'

        self._test_setting_namespace_create()
        self._create_test_setting()

        self._set_environment_variable(
            name='MAYAN_{}'.format(self._test_setting.global_name),
            value=test_environment_value
        )

        self._test_configuration_value = test_file_value
        self._create_test_configuration_file()

        self.assertEqual(self._test_setting.value, test_environment_value)

    def test_environment_variable(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(ENVIRONMENT_TEST_NAME),
            value=ENVIRONMENT_TEST_VALUE
        )

        self.assertEqual(
            setting_paginate_by.value, int(ENVIRONMENT_TEST_VALUE)
        )
