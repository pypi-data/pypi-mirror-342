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

from amend.built_in.numbers.real_numbers import amend_real_number


class TestAmendRealNumber(unittest.TestCase):
    def test_no_amendment_needed(self):
        try:
            amend_real_number(real_number=0.0)
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        real_number = "0"
        expected_result = 0

        try:
            result = amend_real_number(real_number=real_number)
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
            amend_real_number,
            real_number=real_number,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = 1.0

        self.assertRaises(
            TypeError,
            amend_real_number,
            real_number=None,
        )
        self.assertRaises(
            ValueError,
            amend_real_number,
            real_number=None,
            value_on_cast_error="a",
        )

        try:
            result = amend_real_number(
                real_number=None,
                value_on_cast_error=value_on_cast_error,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when value on cast error was valid: {e}",
            )

        self.assertAlmostEqual(
            result,
            value_on_cast_error,
        )

    def test_value_violation(
        self,
    ):
        try:
            amend_real_number(
                real_number=0,
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation without defined limits: {e}",
            )

        try:
            amend_real_number(
                real_number=0.0,
                minimum_value=0.0,
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact minimum: {e}",
            )

        try:
            amend_real_number(
                real_number=0.0,
                maximum_value=0.0,
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_real_number,
            real_number=0.0,
            minimum_value=0.01,
            value_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_real_number,
            real_number=0.01,
            maximum_value=0.0,
            value_violation_action="error",
        )

    def test_infinite_value(
        self,
    ):
        try:
            amend_real_number(
                real_number=0.0,
                infinite_value_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for infinite value for finite value: {e}",
            )
        try:
            amend_real_number(
                real_number=float("nan"),
                infinite_value_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for infinite value for non-a-number: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_real_number,
            real_number=float("inf"),
            infinite_value_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_real_number,
            real_number=float("+inf"),
            infinite_value_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_real_number,
            real_number=float("-inf"),
            infinite_value_action="error",
        )

    def test_not_a_number_value(
        self,
    ):
        try:
            amend_real_number(
                real_number=0.0,
                not_a_number_value_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for not-a-number value for number: {e}",
            )

        try:
            amend_real_number(
                real_number=float("inf"),
                not_a_number_value_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for not-a-number value for infinity: {e}",
            )
        try:
            amend_real_number(
                real_number=float("+inf"),
                not_a_number_value_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for not-a-number value for positive infinity: {e}",
            )
        try:
            amend_real_number(
                real_number=float("-inf"),
                not_a_number_value_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for not-a-number value for negative infinity: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_real_number,
            real_number=float("nan"),
            not_a_number_value_action="error",
        )

    def test_number_of_rounding_decimals(
        self,
    ):
        self.assertAlmostEqual(
            amend_real_number(
                real_number=0.123456,
                number_of_rounding_decimals=3,
            ),
            0.123,
        )

        self.assertAlmostEqual(
            amend_real_number(
                real_number=0.123456,
                number_of_rounding_decimals=6,
            ),
            0.123456,
        )
        self.assertAlmostEqual(
            amend_real_number(
                real_number=0.123456,
                number_of_rounding_decimals=7,
            ),
            0.123456,
        )

        self.assertAlmostEqual(
            amend_real_number(
                real_number=123456.789,
                number_of_rounding_decimals=0,
            ),
            123457,
        )

        self.assertEqual(
            int(
                amend_real_number(
                    real_number=123456.789,
                    number_of_rounding_decimals=-3,
                )
            ),
            123000,
        )
        self.assertEqual(
            int(
                amend_real_number(
                    real_number=123456.789,
                    number_of_rounding_decimals=-2,
                )
            ),
            123500,
        )


if __name__ == "__main__":
    unittest.main()
