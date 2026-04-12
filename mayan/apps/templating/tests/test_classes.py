from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import REGEX_COMPILED_AJAX_TEMPLATE_HASH_EXCLUDE


class AJAXTemplateHashExclusionRegexTestCase(BaseTestCase):
    def test_regular_expression(self):
        test_string = '<!--mayan-templating-hash-exclude-start-->TEST1<!--mayan-templating-hash-exclude-end-->TEST2<!--mayan-templating-hash-exclude-start-->TEST3<!--mayan-templating-hash-exclude-end-->'

        result = REGEX_COMPILED_AJAX_TEMPLATE_HASH_EXCLUDE.sub(
            repl='', string=test_string
        )
        self.assertEqual(result, 'TEST2')
