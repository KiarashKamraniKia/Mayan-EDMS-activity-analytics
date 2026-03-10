from django.core.exceptions import ValidationError
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from mayan.apps.testing.tests.base import BaseTestCase

from ..settings import setting_cluster

from .literals import (
    TEST_SETTING_GLOBAL_NAME, TEST_SETTING_VALIDATION_BAD_VALUE,
    TEST_SETTING_VALIDATION_GOOD_VALUE
)
from .mocks import test_validation_function


class ClusterTestCase(BaseTestCase):
    def test_setting_check_changed(self):
        self._test_setting_namespace_create()
        test_setting = self._test_setting_namespace.do_setting_add(
            global_name=TEST_SETTING_GLOBAL_NAME,
            default='test value'
        )
        test_setting.do_value_set(value='test value edited')
        self.assertTrue(
            setting_cluster.get_is_changed()
        )

    def test_setting_check_changed_for_translations(self):
        """
        Settings with translatable values should not trigger the
        `.check_changed()` method when the language is changed.
        """
        self._test_setting_namespace_create()
        self._test_setting_namespace.do_setting_add(
            global_name=TEST_SETTING_GLOBAL_NAME,
            default=_(message='English')
        )
        translation.activate(language='es')

        self.assertFalse(
            setting_cluster.get_is_changed()
        )

        translation.activate(language='en')
        self.assertFalse(
            setting_cluster.get_is_changed()
        )

    def test_setting_validation_at_loading(self):
        self._test_setting_namespace_create()
        self._create_test_setting(
            validation_function=test_validation_function
        )

        setting_cluster.do_cache_invalidate()

        self._test_configuration_value = TEST_SETTING_VALIDATION_BAD_VALUE
        self._create_test_configuration_file()

        with self.assertRaises(expected_exception=ValidationError):
            self._test_setting.value

    def test_setting_validation_call(self):
        self._test_setting_namespace_create()
        self._create_test_setting(
            validation_function=test_validation_function
        )

        self._test_setting.do_value_raw_validate(
            raw_value=TEST_SETTING_VALIDATION_GOOD_VALUE
        )

        with self.assertRaises(expected_exception=ValidationError):
            self._test_setting.do_value_raw_validate(
                raw_value=TEST_SETTING_VALIDATION_BAD_VALUE
            )
