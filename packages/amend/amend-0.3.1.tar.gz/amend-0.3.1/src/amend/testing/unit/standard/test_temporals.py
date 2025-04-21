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

import datetime
import unittest

from amend.standard.temporals import (
    amend_date,
    amend_date_and_time,
    amend_temporal_offset,
    amend_time,
)


class TestAmendDate(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_date(date=datetime.date.today())
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        expected_result = datetime.date.today()
        date = {
            "year": expected_result.year,
            "month": expected_result.month,
            "day": expected_result.day,
        }

        try:
            result = amend_date(date=date)
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
            amend_date,
            date=date,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = datetime.date.today()

        self.assertRaises(
            TypeError,
            amend_date,
            date=None,
        )
        self.assertRaises(
            ValueError,
            amend_date,
            date=None,
            value_on_cast_error={
                "year": value_on_cast_error.year,
                "month": value_on_cast_error.month,
                "day": value_on_cast_error.day,
            },
        )

        try:
            result = amend_date(
                date=None,
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

    def test_value_violation(
        self,
    ):
        try:
            amend_date(
                date=datetime.date.today(),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation without defined limits: {e}",
            )

        try:
            amend_date(
                date=datetime.date.today(),
                minimum_value=datetime.date.today(),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact minimum: {e}",
            )

        try:
            amend_date(
                date=datetime.date.today(),
                maximum_value=datetime.date.today(),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_date,
            date=datetime.date.today(),
            minimum_value=datetime.date.today() + datetime.timedelta(days=1),
            value_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_date,
            date=datetime.date.today(),
            maximum_value=datetime.date.today() - datetime.timedelta(days=1),
            value_violation_action="error",
        )


class TestAmendDateAndTime(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_date_and_time(date_and_time=datetime.datetime.now())
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        expected_result = datetime.datetime.now()
        date_and_time = {
            "year": expected_result.year,
            "month": expected_result.month,
            "day": expected_result.day,
            "hour": expected_result.hour,
            "minute": expected_result.minute,
            "second": expected_result.second,
            "microsecond": expected_result.microsecond,
        }

        try:
            result = amend_date_and_time(date_and_time=date_and_time)
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
            amend_date_and_time,
            date_and_time=date_and_time,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = datetime.datetime.now()

        self.assertRaises(
            TypeError,
            amend_date_and_time,
            date_and_time=None,
        )
        self.assertRaises(
            ValueError,
            amend_date_and_time,
            date_and_time=None,
            value_on_cast_error={
                "year": value_on_cast_error.year,
                "month": value_on_cast_error.month,
                "day": value_on_cast_error.day,
                "hour": value_on_cast_error.hour,
                "minute": value_on_cast_error.minute,
                "second": value_on_cast_error.second,
                "microsecond": value_on_cast_error.microsecond,
            },
        )

        try:
            result = amend_date_and_time(
                date_and_time=None,
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

    def test_value_violation(
        self,
    ):
        try:
            amend_date_and_time(
                date_and_time=datetime.datetime.now(),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation without defined limits: {e}",
            )

        date_and_time = datetime.datetime.now()
        try:
            amend_date_and_time(
                date_and_time=date_and_time,
                minimum_value=date_and_time,
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact minimum: {e}",
            )

        try:
            amend_date(
                date=date_and_time,
                maximum_value=date_and_time,
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_date_and_time,
            date_and_time=date_and_time,
            minimum_value=date_and_time + datetime.timedelta(microseconds=1),
            value_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_date_and_time,
            date_and_time=date_and_time,
            maximum_value=date_and_time - datetime.timedelta(microseconds=1),
            value_violation_action="error",
        )


class TestAmendTemporalOffset(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_temporal_offset(temporal_offset=datetime.timedelta())
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        expected_result = datetime.timedelta(microseconds=1)
        temporal_offset = {
            "days": expected_result.days,
            "seconds": expected_result.seconds,
            "microseconds": expected_result.microseconds,
        }

        try:
            result = amend_temporal_offset(temporal_offset=temporal_offset)
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
            amend_temporal_offset,
            temporal_offset=temporal_offset,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = datetime.timedelta(microseconds=1)

        self.assertRaises(
            TypeError,
            amend_temporal_offset,
            temporal_offset=None,
        )
        self.assertRaises(
            ValueError,
            amend_temporal_offset,
            temporal_offset=None,
            value_on_cast_error={
                "days": value_on_cast_error.days,
                "seconds": value_on_cast_error.seconds,
                "microseconds": value_on_cast_error.microseconds,
            },
        )

        try:
            result = amend_temporal_offset(
                temporal_offset=None,
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

    def test_value_violation(
        self,
    ):
        try:
            amend_temporal_offset(
                temporal_offset=datetime.timedelta(microseconds=1),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation without defined limits: {e}",
            )

        try:
            amend_temporal_offset(
                temporal_offset=datetime.timedelta(microseconds=1),
                minimum_value=datetime.timedelta(microseconds=1),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact minimum: {e}",
            )

        try:
            amend_temporal_offset(
                temporal_offset=datetime.timedelta(microseconds=1),
                maximum_value=datetime.timedelta(microseconds=1),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact maximum: {e}",
            )

        self.assertRaises(
            ValueError,
            amend_temporal_offset,
            temporal_offset=datetime.timedelta(microseconds=1),
            minimum_value=datetime.timedelta(microseconds=2),
            value_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_temporal_offset,
            temporal_offset=datetime.timedelta(microseconds=2),
            maximum_value=datetime.timedelta(microseconds=1),
            value_violation_action="error",
        )


class TestAmendTime(unittest.TestCase):
    def test_no_amendment_needed(
        self,
    ):
        try:
            amend_time(time=datetime.datetime.now().time())
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no amendment was needed: {e}",
            )

    def test_type_mismatch(
        self,
    ):
        expected_result = datetime.datetime.now().time()
        time = {
            "hour": expected_result.hour,
            "minute": expected_result.minute,
            "second": expected_result.second,
            "microsecond": expected_result.microsecond,
            "tzinfo": expected_result.tzinfo,
        }

        try:
            result = amend_time(time=time)
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
            amend_time,
            time=time,
            type_mismatch_action="error",
        )

    def test_cast_error(
        self,
    ):
        value_on_cast_error = datetime.datetime.now().time()

        self.assertRaises(
            TypeError,
            amend_time,
            time=None,
        )
        self.assertRaises(
            ValueError,
            amend_time,
            time=None,
            value_on_cast_error={
                "hour": value_on_cast_error.hour,
                "minute": value_on_cast_error.minute,
                "second": value_on_cast_error.second,
                "microsecond": value_on_cast_error.microsecond,
                "tzinfo": value_on_cast_error.tzinfo,
            },
        )

        try:
            result = amend_time(
                time=None,
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

    def test_value_violation(
        self,
    ):
        try:
            amend_time(
                time=datetime.datetime.now().time(),
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation without defined limits: {e}",
            )

        time = datetime.datetime.now().time()
        try:
            amend_time(
                time=time,
                minimum_value=time,
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact minimum: {e}",
            )

        try:
            amend_time(
                time=time,
                maximum_value=time,
                value_violation_action="error",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception for value violation with exact maximum: {e}",
            )

        time = datetime.datetime.now()
        earlier_time = time - datetime.timedelta(microseconds=1)
        time = time.time()
        earlier_time = earlier_time.time()

        self.assertRaises(
            ValueError,
            amend_time,
            time=earlier_time,
            minimum_value=time,
            value_violation_action="error",
        )
        self.assertRaises(
            ValueError,
            amend_time,
            time=time,
            maximum_value=earlier_time,
            value_violation_action="error",
        )


if __name__ == "__main__":
    unittest.main()
