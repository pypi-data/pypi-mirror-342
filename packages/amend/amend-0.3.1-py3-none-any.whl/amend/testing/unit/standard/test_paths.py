# Copyright 2025 Miljenko Šuflaj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import shutil
import unittest
import uuid


from amend.standard.paths import (
    amend_directory,
    amend_file,
)


class TestAmendDirectory(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_directory(directory=Path(__file__).resolve().parent)
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        expected_result = Path(__file__).resolve().parent
        directory = str(expected_result)

        try:
            result = amend_directory(directory=directory)
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when amendment was possible: {e}",
            )
        self.assertEqual(
            result,
            expected_result,
        )

        self.assertRaises(
            TypeError,
            amend_directory,
            directory=directory,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = Path(__file__).resolve().parent

        self.assertRaises(
            TypeError,
            amend_directory,
            directory=None,
        )
        self.assertRaises(
            ValueError,
            amend_directory,
            directory=None,
            value_on_cast_error=str(value_on_cast_error),
        )

        try:
            result = amend_directory(
                directory=None,
                value_on_cast_error=value_on_cast_error,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when value on cast error was valid: {e}",
            )

        self.assertEqual(
            result,
            value_on_cast_error,
        )

    def test_not_existing(
        self,
    ):
        try:
            amend_directory(
                directory=Path(__file__).resolve().parent,
                not_existing_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when directory exists: {e}",
            )

        directory = Path.home().resolve() / ".cache" / str(uuid.uuid4())

        self.assertRaises(
            OSError,
            amend_directory,
            directory=directory,
            not_existing_action="error",
        )
        try:
            amend_directory(
                directory=directory,
                not_existing_action="make",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when making directory: {e}",
            )
        self.assertTrue(
            directory.exists(),
            f"Failed to make directory {directory}",
        )
        try:
            shutil.rmtree(str(directory))
        except Exception as e:
            self.assert_(False, f"Threw exception when removing made directory: {e}")

    def test_category_mismatch(
        self,
    ):
        file = Path(__file__).resolve()

        try:
            amend_directory(
                directory=file.parent,
                category_mismatch_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when entity was directory: {e}",
            )

        self.assertRaises(
            NotADirectoryError,
            amend_directory,
            directory=file,
            category_mismatch_action="error",
        )
        try:
            result = amend_directory(
                directory=file,
                category_mismatch_action="take-parent",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when taking parent: {e}",
            )
        self.assertEqual(
            result,
            file.parent,
        )


class TestAmendFile(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_file(file=Path(__file__).resolve())
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        expected_result = Path(__file__).resolve()
        file = str(expected_result)

        try:
            result = amend_file(file=file)
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when amendment was possible: {e}",
            )
        self.assertEqual(
            result,
            expected_result,
        )

        self.assertRaises(
            TypeError,
            amend_file,
            file=file,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = Path(__file__).resolve()

        self.assertRaises(
            TypeError,
            amend_file,
            file=None,
        )
        self.assertRaises(
            ValueError,
            amend_file,
            file=None,
            value_on_cast_error=str(value_on_cast_error),
        )

        try:
            result = amend_file(
                file=None,
                value_on_cast_error=value_on_cast_error,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when value on cast error was valid: {e}",
            )

        self.assertEqual(
            result,
            value_on_cast_error,
        )

    def test_not_existing(
        self,
    ):
        try:
            amend_file(
                file=Path(__file__).resolve(),
                not_existing_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when file exists: {e}",
            )

        file = Path.home().resolve() / ".cache" / str(uuid.uuid4()) / "test-file"
        self.assertRaises(
            OSError,
            amend_file,
            file=file,
            not_existing_action="error",
        )
        try:
            amend_file(
                file=file,
                not_existing_action="make",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when making file: {e}",
            )
        self.assertTrue(
            file.exists(),
            f"Failed to make file {file}",
        )
        try:
            shutil.rmtree(str(file.parent))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when removing made directory & file: {e}",
            )

        try:
            amend_file(
                file=file,
                not_existing_action="make-parent",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when making file parent: {e}",
            )
        self.assertTrue(
            file.parent.exists(),
            f"Failed to make directory {file.parent}",
        )
        try:
            shutil.rmtree(str(file.parent))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when removing made directory: {e}",
            )

    def test_category_mismatch(
        self,
    ):
        file = Path(__file__).resolve()

        try:
            amend_file(
                file=file,
                category_mismatch_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when entity was file: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_file,
            file=file.parent,
            category_mismatch_action="error",
        )


if __name__ == "__main__":
    unittest.main()
