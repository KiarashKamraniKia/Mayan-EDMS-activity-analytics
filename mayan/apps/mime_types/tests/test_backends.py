from django.test import tag

from mayan.apps.dependencies.exceptions import DependenciesException
from mayan.apps.documents.tests.literals import TEST_FILE_PDF_PATH
from mayan.apps.testing.tests.base import BaseTestCase

from ..backends.file_command import MIMETypeBackendFileCommand


@tag('mime_types')
class MIMETypeBackendFileCommandTestCase(BaseTestCase):
    def test_bad_path(self):
        with self.assertRaises(expected_exception=DependenciesException):
            MIMETypeBackendFileCommand(file_path='/tmp/badpath')

    def test_pdf_mime_type_only(self):
        backend = MIMETypeBackendFileCommand()

        with open(TEST_FILE_PDF_PATH, mode='rb') as file_object:
            mime_type, encoding = backend.get_mime_type(
                file_object=file_object, mime_type_only=True
            )

        self.assertEqual(mime_type, 'application/pdf')
        self.assertEqual(encoding, 'binary')

    def test_pdf_mime_type_and_encoding(self):
        backend = MIMETypeBackendFileCommand()

        with open(TEST_FILE_PDF_PATH, mode='rb') as file_object:
            mime_type, encoding = backend.get_mime_type(
                file_object=file_object, mime_type_only=False
            )

        self.assertEqual(mime_type, 'application/pdf')
        self.assertIn(
            encoding, ('binary', 'unknown-8bit')
        )
