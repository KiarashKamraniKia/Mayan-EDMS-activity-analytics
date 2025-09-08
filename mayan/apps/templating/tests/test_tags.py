from datetime import datetime

from mayan.apps.testing.tests.base import BaseTestCase

from ..exceptions import DangerousTagError
from ..settings import setting_templating_dangerous_tags_allow_list
from ..templatetags.templating_test_tags import (
    templating_test_filter_dangerous, templating_test_tag,
    templating_test_tag_dangerous
)

from .literals import TEST_TEMPLATE_TAG_RESULT
from .mixins import TemplateTestMixin


class TemplateFilterDangerousTestCase(TemplateTestMixin, BaseTestCase):
    def test_user_template_filter_dangerous(self):
        with self.assertRaises(expected_exception=DangerousTagError):
            self._render_test_template(
                template_string='{% load templating_test_tags %}{{ 1|dangerous_filter }}'
            )

    def test_user_template_filter_dangerous_allowed(self):
        setting_templating_dangerous_tags_allow_list.do_value_raw_set(
            raw_value='dangerous_filter'
        )

        result = self._render_test_template(
            template_string='{% load templating_test_tags %}{{ 1|dangerous_filter }}'
        )
        self.assertEqual(result, TEST_TEMPLATE_TAG_RESULT)


class TemplateFilterDateParseTestCase(TemplateTestMixin, BaseTestCase):
    def test_basic_functionality(self):
        now = datetime.now()

        result = self._render_test_template(
            template_string='{{% set "{}"|date_parse as date_object %}}{{{{ date_object.year }}}}'.format(
                now.isoformat()
            )
        )
        self.assertEqual(
            result, str(now.year)
        )


class TemplateFilterDictGetTestCase(TemplateTestMixin, BaseTestCase):
    def test_filter_dict_get_valid(self):
        result = self._render_test_template(
            template_string='{{ dict|dict_get:1 }}', context={
                'dict': {1: 'a'}
            }
        )
        self.assertEqual(result, 'a')

    def test_filter_dict_get_invalid(self):
        result = self._render_test_template(
            template_string='{{ dict|dict_get:2 }}', context={
                'dict': {1: 'a'}
            }
        )
        self.assertEqual(result, '')


class TemplateFilterSplitTestCase(TemplateTestMixin, BaseTestCase):
    def test_filter_split_valid(self):
        result = self._render_test_template(
            template_string='{% with x|split:"," as result %}{{ result.0 }}-{{ result.1 }}-{{ result.2 }}{% endwith %}', context={'x': '1,2,3'}
        )
        self.assertEqual(result, '1-2-3')


class TemplateTagDangerousTestCase(TemplateTestMixin, BaseTestCase):
    def test_user_template_tag_dangerous(self):
        with self.assertRaises(expected_exception=DangerousTagError):
            self._render_test_template(
                template_string='{% load templating_test_tags %}{% dangerous_tag %}'
            )

    def test_user_template_tag_dangerous_allowed(self):
        setting_templating_dangerous_tags_allow_list.do_value_raw_set(
            raw_value='dangerous_tag'
        )

        result = self._render_test_template(
            template_string='{% load templating_test_tags %}{% dangerous_tag %}'
        )
        self.assertEqual(result, TEST_TEMPLATE_TAG_RESULT)


class TemplateTagDocstringTestCase(TemplateTestMixin, BaseTestCase):
    def test_user_template_get_docstring(self):
        result = templating_test_filter_dangerous.__doc__
        self.assertEqual(result, '\nTest docstring dangerous filter\n')

        result = templating_test_tag.__doc__
        self.assertEqual(result, '\nTest docstring\n')

        result = templating_test_tag_dangerous.__doc__
        self.assertEqual(result, '\nTest docstring dangerous tag\n')


class TemplateTagLoadingTestCase(TemplateTestMixin, BaseTestCase):
    def test_user_template_tag_loading(self):
        result = self._render_test_template(
            template_string='{% load templating_test_tags %}{% templating_test_tag %}'
        )
        self.assertEqual(result, TEST_TEMPLATE_TAG_RESULT)


class TemplateTagRegexTestCase(TemplateTestMixin, BaseTestCase):
    def test_tag_regex_findall_false(self):
        result = self._render_test_template(
            template_string='{% regex_findall "\\d" "abcxyz" as result %}{% if result %}{{ result }}{% endif %}'
        )
        self.assertEqual(result, '')

    def test_tag_regex_findall_true(self):
        result = self._render_test_template(
            template_string='{% regex_findall "\\d" "abc123" as result %}{{ result.0 }}{{ result.1 }}{{ result.2 }}'
        )
        self.assertEqual(result, '123')

    def test_tag_regex_match_false(self):
        result = self._render_test_template(
            template_string='{% regex_match "\\d" "abc123" as result %}{% if result %}{{ result }}{% endif %}'
        )
        self.assertEqual(result, '')

    def test_tag_regex_match_true(self):
        result = self._render_test_template(
            template_string='{% regex_match "\\d" "123abc" as result %}{% if result %}{{ result.0 }}{% endif %}'
        )
        self.assertEqual(result, '1')

    def test_tag_regex_search_false(self):
        result = self._render_test_template(
            template_string='{% regex_search "\\d" "abcxyz" as result %}{% if result %}{{ result }}{% endif %}'
        )
        self.assertEqual(result, '')

    def test_tag_regex_search_true(self):
        result = self._render_test_template(
            template_string='{% regex_search "\\d" "abc123" as result %}{{ result.0 }}'
        )
        self.assertEqual(result, '1')

    def test_tag_regex_sub_false(self):
        result = self._render_test_template(
            template_string='{% regex_sub "\\d" "XX" "abcxyz" as result %}{{ result }}'
        )
        self.assertEqual(result, 'abcxyz')

    def test_tag_regex_sub_true(self):
        result = self._render_test_template(
            template_string='{% regex_sub "\\d" "XX" "abc123" as result %}{{ result }}'
        )
        self.assertEqual(result, 'abcXXXXXX')


class TemplateTagSetTestCase(TemplateTestMixin, BaseTestCase):
    def test_tag_set_string(self):
        result = self._render_test_template(
            template_string='{% set "string" as result %}{{ result }}'
        )
        self.assertEqual(result, 'string')

    def test_tag_set_number(self):
        result = self._render_test_template(
            template_string='{% set 99 as result %}{{ result }}'
        )
        self.assertEqual(result, '99')

    def test_tag_set_logical(self):
        result = self._render_test_template(
            template_string='{% set True as result %}{{ result }}'
        )
        self.assertEqual(result, 'True')

    def test_tag_set_nonexistant(self):
        result = self._render_test_template(
            template_string='{% set nonexistent as result %}{{ result }}'
        )
        self.assertEqual(result, '')


class TemplateTagTimeDeltaTestCase(TemplateTestMixin, BaseTestCase):
    def test_basic_functionality(self):
        now = datetime.now()

        result = self._render_test_template(
            template_string='{{% set "{}"|date_parse as date_object %}}{{% timedelta date_object days=366 as date_new %}}{{{{ date_new.year }}}}'.format(
                now.isoformat()
            )
        )
        self.assertEqual(
            result, str(now.year + 1)
        )
