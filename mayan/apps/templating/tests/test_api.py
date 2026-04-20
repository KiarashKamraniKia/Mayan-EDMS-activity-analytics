from django.test import override_settings

from mayan.apps.documents.tests.mixins.document_mixins import (
    DocumentTestMixin
)
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import AJAXTemplate
from ..permissions import permission_template_sandbox

from .literals import TEST_AJAXTEMPLATE_RESULT
from .mixins import ObjectTemplateSandboxActionApiViewTestMixin


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


class ObjectTemplateSandboxActionApiViewTestCase(
    DocumentTestMixin, ObjectTemplateSandboxActionApiViewTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super().setUp()

        self._test_object = self._test_document
        self._inject_test_object_content_type()

    def test_object_template_sanbox_get_api_view_no_permission(self):
        response = self._request_object_template_sandbox_get_api_view()
        self.assertEqual(response.status_code, 405)

    def test_object_template_sanbox_get_api_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_template_sandbox
        )

        response = self._request_object_template_sandbox_get_api_view()
        self.assertEqual(response.status_code, 405)

    def test_object_template_sanbox_post_api_view_no_permission(self):
        response = self._request_object_template_sandbox_post_api_view()
        self.assertEqual(response.status_code, 404)

    def test_object_template_sanbox_post_api_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_template_sandbox
        )

        response = self._request_object_template_sandbox_post_api_view()
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json['result'], str(self._test_object)
        )

    def test_object_template_sanbox_post_api_view_with_access_invalid_model(self):
        self._test_case_user.is_staff = True
        self._test_case_user.save()

        response = self._request_object_template_sandbox_post_api_view_invalid_model()
        self.assertEqual(response.status_code, 400)
