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


from amend.built_in.sets.data_sets import (
    amend_immutable_data_set,
    amend_mutable_data_set,
)


class TestAmendImmutableDataSet(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_immutable_data_set(immutable_data_set=frozenset())
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        immutable_data_set = {1, 2}
        expected_result = frozenset(immutable_data_set)

        try:
            result = amend_immutable_data_set(immutable_data_set=immutable_data_set)
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
            amend_immutable_data_set,
            immutable_data_set=immutable_data_set,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = frozenset({1, 2})

        self.assertRaises(
            TypeError,
            amend_immutable_data_set,
            immutable_data_set=None,
        )
        self.assertRaises(
            ValueError,
            amend_immutable_data_set,
            immutable_data_set=None,
            value_on_cast_error={1, 2},
        )

        try:
            result = amend_immutable_data_set(
                immutable_data_set=None,
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
        immutable_data_set = frozenset({1, 2})

        try:
            amend_immutable_data_set(
                immutable_data_set=immutable_data_set,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation without defined limits: {e}",
            )

        try:
            amend_immutable_data_set(
                immutable_data_set=immutable_data_set,
                minimum_length=0,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with minimum 0 length: {e}",
            )

        try:
            amend_immutable_data_set(
                immutable_data_set=immutable_data_set,
                maximum_length=len(immutable_data_set),
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with exact length maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_immutable_data_set,
            immutable_data_set=immutable_data_set,
            minimum_length=len(immutable_data_set) + 1,
            length_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_immutable_data_set,
            immutable_data_set=immutable_data_set,
            maximum_length=len(immutable_data_set) - 1,
            length_violation_action="error",
        )


class TestAmendMutableDataSet(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_mutable_data_set(mutable_data_set=set())
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        expected_result = {1, 2}
        mutable_data_set = frozenset(expected_result)

        try:
            result = amend_mutable_data_set(mutable_data_set=mutable_data_set)
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
            amend_mutable_data_set,
            mutable_data_set=mutable_data_set,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = frozenset({1, 2})

        self.assertRaises(
            TypeError,
            amend_mutable_data_set,
            mutable_data_set=None,
        )
        self.assertRaises(
            ValueError,
            amend_mutable_data_set,
            mutable_data_set=None,
            value_on_cast_error={1, 2},
        )

        try:
            result = amend_mutable_data_set(
                mutable_data_set=None,
                value_on_cast_error=value_on_cast_error,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when value on cast error was valid: {e}",
            )

        self.assertEqual(
            result,
            set(value_on_cast_error),
        )

    def test_length_violation(
        self,
    ):
        mutable_data_set = {1, 2}

        try:
            amend_mutable_data_set(
                mutable_data_set=mutable_data_set,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation without defined limits: {e}",
            )

        try:
            amend_mutable_data_set(
                mutable_data_set=mutable_data_set,
                minimum_length=0,
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with minimum 0 length: {e}",
            )

        try:
            amend_mutable_data_set(
                mutable_data_set=mutable_data_set,
                maximum_length=len(mutable_data_set),
                length_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for length violation with exact length maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_mutable_data_set,
            mutable_data_set=mutable_data_set,
            minimum_length=len(mutable_data_set) + 1,
            length_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_mutable_data_set,
            mutable_data_set=mutable_data_set,
            maximum_length=len(mutable_data_set) - 1,
            length_violation_action="error",
        )


if __name__ == "__main__":
    unittest.main()
