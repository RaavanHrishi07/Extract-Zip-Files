
import tempfile
import unittest
import zipfile
from pathlib import Path
from contextlib import redirect_stderr
from io import StringIO

from extract_zip_files import extract_zip, is_safe_member


class TestZipExtraction(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_zip(self, name, members):
        zip_path = self.base_path / name

        with zipfile.ZipFile(zip_path, "w") as archive:
            for filename, content in members.items():
                archive.writestr(filename, content)

        return zip_path

    def test_extracts_valid_zip(self):
        zip_path = self.create_zip(
            "sample.zip",
            {"hello.txt": "ZIP extraction works!"},
        )

        result = extract_zip(zip_path)

        extracted_file = self.base_path / "sample" / "hello.txt"

        self.assertEqual(result, 0)
        self.assertTrue(extracted_file.exists())
        self.assertEqual(
            extracted_file.read_text(encoding="utf-8"),
            "ZIP extraction works!",
        )

    def test_extracts_to_custom_output_folder(self):
        zip_path = self.create_zip(
            "custom_sample.zip",
            {"hello.txt": "Custom destination works!"},
        )
        output_dir = self.base_path / "my_custom_folder"

        result = extract_zip(zip_path, output_dir)

        extracted_file = output_dir / "hello.txt"

        self.assertEqual(result, 0)
        self.assertTrue(extracted_file.exists())
        self.assertEqual(
            extracted_file.read_text(encoding="utf-8"),
            "Custom destination works!",
        )

    def test_missing_file_returns_error(self):
        missing_path = self.base_path / "missing.zip"

        with redirect_stderr(StringIO()):
            result = extract_zip(missing_path)

        self.assertEqual(result, 1)

    def test_rejects_non_zip_extension(self):
        text_file = self.base_path / "notes.txt"
        text_file.write_text("not a ZIP", encoding="utf-8")

        with redirect_stderr(StringIO()):
            result = extract_zip(text_file)

        self.assertEqual(result, 1)

    def test_rejects_corrupted_zip(self):
        zip_path = self.base_path / "corrupted.zip"
        zip_path.write_bytes(b"This is not a valid ZIP archive")

        with redirect_stderr(StringIO()):
            result = extract_zip(zip_path)

        self.assertEqual(result, 1)

    def test_rejects_parent_directory_traversal(self):
        destination = self.base_path / "output"

        self.assertFalse(
            is_safe_member("../outside.txt", destination)
        )

    def test_rejects_windows_style_traversal(self):
        destination = self.base_path / "output"

        self.assertFalse(
            is_safe_member(r"..\outside.txt", destination)
        )

    def test_rejects_absolute_paths(self):
        destination = self.base_path / "output"

        self.assertFalse(
            is_safe_member("/outside.txt", destination)
        )
        self.assertFalse(
            is_safe_member(r"C:\outside.txt", destination)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
