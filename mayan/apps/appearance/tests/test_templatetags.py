from unittest import mock

from django.template import Context, Template

from mayan.apps.testing.tests.base import BaseTestCase

from ..templatetags import appearance_tags
from ..templatetags.appearance_tags import app_templates_cache

from .literals import (
    TEST_APP_TEMPLATE_CACHE_LANGUAGE_FIRST,
    TEST_APP_TEMPLATE_CACHE_LANGUAGE_SECOND,
    TEST_APP_TEMPLATE_NAME
)


class AppearanceAppTemplatesTagTestCase(BaseTestCase):
    auto_login_user = False

    def setUp(self):
        super().setUp()
        app_templates_cache.clear()

    def tearDown(self):
        app_templates_cache.clear()
        super().tearDown()

    def _render_test_app_templates_tag(self, language):
        template = Template(
            template_string='{{% load appearance_tags %}}'
            '{{% appearance_app_templates template_name=\'{}\' %}}'.format(
                TEST_APP_TEMPLATE_NAME
            )
        )

        with mock.patch.object(
            attribute='get_language', return_value=language,
            target=appearance_tags
        ):
            context = Context()
            return template.render(context=context)

    def test_app_template_cache_key_is_language_aware(self):
        self._render_test_app_templates_tag(
            language=TEST_APP_TEMPLATE_CACHE_LANGUAGE_FIRST
        )

        self.assertTrue(
            any(
                key.endswith(
                    '.{}.{}'.format(
                        TEST_APP_TEMPLATE_NAME,
                        TEST_APP_TEMPLATE_CACHE_LANGUAGE_FIRST
                    )
                ) for key in app_templates_cache
            )
        )

    def test_app_template_cache_entries_per_language_coexist(self):
        self._render_test_app_templates_tag(
            language=TEST_APP_TEMPLATE_CACHE_LANGUAGE_FIRST
        )
        self._render_test_app_templates_tag(
            language=TEST_APP_TEMPLATE_CACHE_LANGUAGE_SECOND
        )

        cache_key_list = tuple(app_templates_cache)

        self.assertTrue(
            any(
                key.endswith(
                    '.{}.{}'.format(
                        TEST_APP_TEMPLATE_NAME,
                        TEST_APP_TEMPLATE_CACHE_LANGUAGE_FIRST
                    )
                ) for key in cache_key_list
            )
        )
        self.assertTrue(
            any(
                key.endswith(
                    '.{}.{}'.format(
                        TEST_APP_TEMPLATE_NAME,
                        TEST_APP_TEMPLATE_CACHE_LANGUAGE_SECOND
                    )
                ) for key in cache_key_list
            )
        )
