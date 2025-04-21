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

import unittest

from amend.built_in.sequences.data_sequences import (
    amend_immutable_binary,
    amend_mutable_binary,
    amend_text,
)


class TestAmendImmutableBinary(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_immutable_binary(immutable_binary=b"")
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        immutable_binary = bytearray(b"0")
        expected_result = b"0"

        try:
            result = amend_immutable_binary(immutable_binary=immutable_binary)
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
            amend_immutable_binary,
            immutable_binary=immutable_binary,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = b"1"

        self.assertRaises(
            TypeError,
            amend_immutable_binary,
            immutable_binary=None,
        )
        self.assertRaises(
            ValueError,
            amend_immutable_binary,
            immutable_binary=None,
            value_on_cast_error=(0,),
        )

        try:
            result = amend_immutable_binary(
                immutable_binary=None,
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

    def test_length_violation(
        self,
    ):
        immutable_binary = b"01"

        try:
            amend_immutable_binary(
                immutable_binary=immutable_binary,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation without defined limits: {e}",
            )

        try:
            amend_immutable_binary(
                immutable_binary=immutable_binary,
                minimum_length=0,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with minimum 0 length: {e}",
            )

        try:
            amend_immutable_binary(
                immutable_binary=immutable_binary,
                maximum_length=len(immutable_binary),
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with exact length maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_immutable_binary,
            immutable_binary=immutable_binary,
            minimum_length=len(immutable_binary) + 1,
            length_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_immutable_binary,
            immutable_binary=immutable_binary,
            maximum_length=len(immutable_binary) - 1,
            length_violation_action="error",
        )


class TestAmendMutableBinary(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_mutable_binary(mutable_binary=bytearray(b""))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        mutable_binary = b"0"
        expected_result = bytearray(mutable_binary)

        try:
            result = amend_mutable_binary(mutable_binary=mutable_binary)
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
            amend_mutable_binary,
            mutable_binary=mutable_binary,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = b"1"

        self.assertRaises(
            TypeError,
            amend_mutable_binary,
            mutable_binary=None,
        )
        self.assertRaises(
            ValueError,
            amend_mutable_binary,
            mutable_binary=None,
            value_on_cast_error=(0,),
        )

        try:
            result = amend_mutable_binary(
                mutable_binary=None,
                value_on_cast_error=value_on_cast_error,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when value on cast error was valid: {e}",
            )

        self.assertEqual(
            result,
            bytearray(value_on_cast_error),
        )

    def test_length_violation(
        self,
    ):
        mutable_binary = bytearray(b"01")

        try:
            amend_mutable_binary(
                mutable_binary=mutable_binary,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation without defined limits: {e}",
            )

        try:
            amend_mutable_binary(
                mutable_binary=mutable_binary,
                minimum_length=0,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with minimum 0 length: {e}",
            )

        try:
            amend_mutable_binary(
                mutable_binary=mutable_binary,
                maximum_length=len(mutable_binary),
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with exact length maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_mutable_binary,
            mutable_binary=mutable_binary,
            minimum_length=len(mutable_binary) + 1,
            length_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_mutable_binary,
            mutable_binary=mutable_binary,
            maximum_length=len(mutable_binary) - 1,
            length_violation_action="error",
        )


class TestAmendText(unittest.TestCase):
    class BadString:
        def __str__(self) -> str:
            raise NotImplementedError

    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_text(text="")
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        text = 0
        expected_result = "0"

        try:
            result = amend_text(text=text)
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
            amend_text,
            text=text,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = "1"

        self.assertRaises(
            TypeError,
            amend_text,
            text=self.BadString(),
        )
        self.assertRaises(
            ValueError,
            amend_text,
            text=self.BadString(),
            value_on_cast_error=(0,),
        )

        try:
            result = amend_text(
                text=self.BadString(),
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

    def test_length_violation(
        self,
    ):
        text = "01"

        try:
            amend_text(
                text=text,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation without defined limits: {e}",
            )

        try:
            amend_text(
                text=text,
                minimum_length=0,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with minimum 0 length: {e}",
            )

        try:
            amend_text(
                text=text,
                maximum_length=len(text),
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with exact length maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_text,
            text=text,
            minimum_length=len(text) + 1,
            length_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_text,
            text=text,
            maximum_length=len(text) - 1,
            length_violation_action="error",
        )


if __name__ == "__main__":
    unittest.main()
