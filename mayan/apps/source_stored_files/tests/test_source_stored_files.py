import base64

from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import SourceStoredFile


class SourceStoredFileTestCase(BaseTestCase):
    def _get_encoded_filename(self, filename):
        return base64.urlsafe_b64encode(
            s=filename.encode('utf8')
        ).decode('ascii')

    # Encoded filename

    def test_encoded_filename_base64_invalid(self):
        with self.assertRaises(ValueError):
            SourceStoredFile(encoded_filename='..', source=None)

    def test_encoded_filename_base64_unpadded(self):
        stored_file = SourceStoredFile(
            encoded_filename='ZGlyZWN0b3J5L2RvY3VtZW50LnR4dA', source=None
        )

        self.assertEqual(
            stored_file.get_full_path(), 'directory/document.txt'
        )

    def test_encoded_filename_empty(self):
        with self.assertRaises(ValueError):
            SourceStoredFile(
                encoded_filename=self._get_encoded_filename(filename=''),
                source=None
            )

    def test_encoded_filename_relative_path(self):
        encoded_filename = self._get_encoded_filename(
            filename='directory/document.txt'
        )

        stored_file = SourceStoredFile(
            encoded_filename=encoded_filename, source=None
        )
        self.assertEqual(
            stored_file.get_full_path(), 'directory/document.txt'
        )

    # Raw filename

    def test_filename_absolute_path(self):
        with self.assertRaises(ValueError):
            SourceStoredFile(filename='/etc/passwd', source=None)

    def test_filename_path_valid(self):
        stored_file = SourceStoredFile(
            filename='directory/document.txt', source=None
        )
        self.assertEqual(
            stored_file.get_full_path(), 'directory/document.txt'
        )

    def test_filename_path_traversal(self):
        with self.assertRaises(ValueError):
            SourceStoredFile(
                filename='directory/../document.txt', source=None
            )

    def test_filename_null_byte(self):
        with self.assertRaises(ValueError):
            SourceStoredFile(filename='document\x00.txt', source=None)
