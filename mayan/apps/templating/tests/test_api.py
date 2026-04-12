from django.test import override_settings

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import AJAXTemplate

from .literals import TEST_AJAXTEMPLATE_RESULT


class AJAXTemplateAPIViewTestCase(BaseAPITestCase):
    auto_login_user = False

    def test_template_detail_anonymous_api_view(self):
        template_main_menu = AJAXTemplate.get(name='menu_main')
        template_path = template_main_menu.get_absolute_url()

        self._clear_events()

        response = self.get(path=template_path)
        self.assertNotContains(
            response=response, text=TEST_AJAXTEMPLATE_RESULT, status_code=403
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(LANGUAGE_CODE='de')
    def test_template_detail_api_view(self):
        self.login_user()
        template_main_menu = AJAXTemplate.get(name='menu_main')
        template_path = template_main_menu.get_absolute_url()

        self._clear_events()

        response = self.get(path=template_path)
        self.assertContains(
            response=response, text=TEST_AJAXTEMPLATE_RESULT, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_template_detail_api_view_hash_change(self):
        self.login_user()
        template_main_menu = AJAXTemplate.get(name='menu_topbar')
        template_path = template_main_menu.get_absolute_url()

        self._clear_events()

        response = self.get(path=template_path)

        hash_first = response.json()['hex_hash']

        response = self.get(path=template_path)

        hash_second = response.json()['hex_hash']

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.assertEqual(hash_first, hash_second)
