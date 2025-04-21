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

# NOTE: Iteration over satisfying constraints is not tested, as it's
# (potentially) an infinite iterator, and because its inner workings should
# already be covered under tests for 'determine_length_normalization_strategy',
# 'find_least_common_multiplier' and length-normalization functions.
from amend.utilities.normalization import (
    determine_length_normalization_strategy,
    find_least_common_multiplier,
    get_immutable_mapping,
    normalize_length_of_immutable_binary,
    normalize_length_of_immutable_sequence,
    normalize_length_of_mutable_binary,
    normalize_length_of_mutable_sequence,
    normalize_length_of_text,
)


class TestLengthNormalizationStrategyDetermination(unittest.TestCase):
    def test_no_modification_needed(self):
        try:
            determine_length_normalization_strategy(length=1)
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when no modification was needed: {e}",
            )

        try:
            determine_length_normalization_strategy(
                length=1,
                minimum_length=1,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception with exact minimum: {e}",
            )

        try:
            determine_length_normalization_strategy(
                length=1,
                maximum_length=1,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception with exact maximum: {e}",
            )

        try:
            determine_length_normalization_strategy(
                length=2,
                length_is_multiple_of=(2,),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception with exact length-is-multiple-of: {e}",
            )

    def test_truncation(self):
        try:
            result = determine_length_normalization_strategy(
                length=5,
                maximum_length=2,
                truncation_side="left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (-3, 0),
        )

        try:
            result = determine_length_normalization_strategy(
                length=5,
                maximum_length=2,
                truncation_side="right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (0, -3),
        )

        try:
            result = determine_length_normalization_strategy(
                length=5,
                maximum_length=2,
                truncation_side="both-but-prioritize-left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (-2, -1),
        )

        try:
            result = determine_length_normalization_strategy(
                length=5,
                maximum_length=2,
                truncation_side="both-but-prioritize-right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (-1, -2),
        )

    def test_padding(self):
        try:
            result = determine_length_normalization_strategy(
                length=2,
                minimum_length=5,
                padding_side="left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (3, 0),
        )

        try:
            result = determine_length_normalization_strategy(
                length=2,
                minimum_length=5,
                padding_side="right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (0, 3),
        )

        try:
            result = determine_length_normalization_strategy(
                length=2,
                minimum_length=5,
                padding_side="both-but-prioritize-left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (2, 1),
        )

        try:
            result = determine_length_normalization_strategy(
                length=2,
                minimum_length=5,
                padding_side="both-but-prioritize-right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (1, 2),
        )

    def test_multiple_of(self):
        try:
            result = determine_length_normalization_strategy(
                length=4,
                length_is_multiple_of=(2,),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when length was already valid multiple-of: {e}",
            )
        try:
            result = determine_length_normalization_strategy(
                length=4,
                length_is_multiple_of=(2, 4),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when length was already valid multiple-of: {e}",
            )
        try:
            result = determine_length_normalization_strategy(
                length=10,
                length_is_multiple_of=(2, 5),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when length was already valid multiple-of: {e}",
            )

        try:
            result = determine_length_normalization_strategy(
                length=5,
                length_is_multiple_of=(3,),
                truncation_side="left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (-2, 0),
        )
        try:
            result = determine_length_normalization_strategy(
                length=5,
                length_is_multiple_of=(3,),
                truncation_side="right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (0, -2),
        )
        try:
            result = determine_length_normalization_strategy(
                length=8,
                length_is_multiple_of=(5,),
                truncation_side="both-but-prioritize-left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (-2, -1),
        )
        try:
            result = determine_length_normalization_strategy(
                length=8,
                length_is_multiple_of=(5,),
                truncation_side="both-but-prioritize-right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (-1, -2),
        )

        try:
            result = determine_length_normalization_strategy(
                length=5,
                length_is_multiple_of=(3,),
                padding_side="left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (1, 0),
        )
        try:
            result = determine_length_normalization_strategy(
                length=5,
                length_is_multiple_of=(3,),
                padding_side="right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (0, 1),
        )
        try:
            result = determine_length_normalization_strategy(
                length=7,
                length_is_multiple_of=(5,),
                padding_side="both-but-prioritize-left",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (2, 1),
        )
        try:
            result = determine_length_normalization_strategy(
                length=7,
                length_is_multiple_of=(5,),
                padding_side="both-but-prioritize-right",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (1, 2),
        )


class TestLeastCommonMultiplierSearch(unittest.TestCase):
    def test_single_common_multiplier_search(self):
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(-1,),
        )
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(0,),
        )

        try:
            result = find_least_common_multiplier(multiples=(1,))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            1,
        )

        try:
            result = find_least_common_multiplier(multiples=(2,))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            2,
        )

        try:
            result = find_least_common_multiplier(multiples=(5782165987216521,))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            5782165987216521,
        )

    def test_multiple_common_multiplier_search(self):
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(0, -1, -2, -3),
        )
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(2, 3, 5, 0),
        )
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(2, 3, 5, -1),
        )

        try:
            result = find_least_common_multiplier(multiples=(1, 2))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            2,
        )

        try:
            result = find_least_common_multiplier(multiples=(2, 4))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            4,
        )

        try:
            result = find_least_common_multiplier(multiples=(2, 3, 6))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            6,
        )

        try:
            result = find_least_common_multiplier(multiples=(426781469721, 57261852619))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            24438297619684113049299,
        )

    def test_multiple_repeating_common_multiplier_search(self):
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(0, 0, -1, -1, -2, -2),
        )
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(2, 2, 3, 3, 5, 0, 0),
        )
        self.assertRaises(
            ValueError,
            find_least_common_multiplier,
            multiples=(2, 3, 5, 5, -1, -1),
        )

        try:
            result = find_least_common_multiplier(multiples=(1, 1))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            1,
        )

        try:
            result = find_least_common_multiplier(multiples=(2, 2, 4))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            4,
        )

        try:
            result = find_least_common_multiplier(multiples=(2, 2, 3, 3, 6))
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            6,
        )

        try:
            result = find_least_common_multiplier(
                multiples=(3271849, 8597216052819521, 3271849)
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when common multiplier exists: {e}",
            )
        self.assertEqual(
            result,
            28128792745201496964329,
        )


class TestImmutableMappingAcquisition(unittest.TestCase):
    def test_identity(self):
        mutable_mapping = {
            "a": 1,
            "b": 2,
            "c": 0,
        }
        immutable_mapping = (
            ("a", 1),
            ("b", 2),
            ("c", 0),
        )

        try:
            result = get_immutable_mapping(
                mapping=mutable_mapping,
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when immutable mapping acquisition was possible: {e}",
            )
        self.assertEqual(
            result,
            immutable_mapping,
        )

        try:
            result = dict(immutable_mapping)
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when tuple could become dictionary: {e}",
            )
        self.assertEqual(
            result,
            mutable_mapping,
        )


class TestLengthNormalizationOfImmutableBinary(unittest.TestCase):
    def test_truncation(self):
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(-1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            b"2345",
        )
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(0, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            b"1234",
        )
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(-2, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            b"34",
        )

        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(-6, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            b"",
        )
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(0, -6),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            b"",
        )

    def test_padding(self):
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            b"".join(
                (
                    b"\0",
                    b"12345",
                )
            ),
        )
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(0, 1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            b"".join(
                (
                    b"12345",
                    b"\0",
                )
            ),
        )
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(1, 2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            b"".join(
                (
                    b"\0",
                    b"12345",
                    b"\0",
                    b"\0",
                )
            ),
        )

        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(2, 1),
                padding_value=b"a",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            b"aa12345a",
        )
        try:
            result = normalize_length_of_immutable_binary(
                immutable_binary=b"12345",
                proposed_length_change=(3, 4),
                padding_value=b"ab",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            b"aba12345abab",
        )


class TestLengthNormalizationOfImmutableSequence(unittest.TestCase):
    def test_truncation(self):
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(-1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (2, 3, 4, 5),
        )
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(0, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (1, 2, 3, 4),
        )
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(-2, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            (3, 4),
        )

        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(-6, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            tuple(),
        )
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(0, -6),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            tuple(),
        )

    def test_padding(self):
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (None, 1, 2, 3, 4, 5),
        )
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(0, 1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (1, 2, 3, 4, 5, None),
        )
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(1, 2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (None, 1, 2, 3, 4, 5, None, None),
        )
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(2, 1),
                padding_value=(0,),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (0, 0, 1, 2, 3, 4, 5, 0),
        )

        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(3, 4),
                padding_value=(-1, -2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            (-1, -2, -1, 1, 2, 3, 4, 5, -1, -2, -1, -2),
        )
        try:
            result = normalize_length_of_immutable_sequence(
                immutable_sequence=(1, 2, 3, 4, 5),
                proposed_length_change=(4, 3),
                padding_value=("test", 1.2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertAlmostEqual(
            result,
            ("test", 1.2, "test", 1.2, 1, 2, 3, 4, 5, "test", 1.2, "test"),
        )


class TestLengthNormalizationOfMutableBinary(unittest.TestCase):
    def test_truncation(self):
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(-1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(b"2345"),
        )
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(0, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(b"1234"),
        )
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(-2, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(b"34"),
        )

        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(-6, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            bytearray(b""),
        )
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(0, -6),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            bytearray(b""),
        )

    def test_padding(self):
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(
                b"".join(
                    (
                        b"\0",
                        b"12345",
                    )
                )
            ),
        )
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(0, 1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(
                b"".join(
                    (
                        b"12345",
                        b"\0",
                    )
                )
            ),
        )
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(1, 2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(
                b"".join(
                    (
                        b"\0",
                        b"12345",
                        b"\0",
                        b"\0",
                    )
                )
            ),
        )

        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(2, 1),
                padding_value=b"a",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(b"aa12345a"),
        )
        try:
            result = normalize_length_of_mutable_binary(
                mutable_binary=bytearray(b"12345"),
                proposed_length_change=(3, 4),
                padding_value=b"ab",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            bytearray(b"aba12345abab"),
        )


class TestLengthNormalizationOfMutableSequence(unittest.TestCase):
    def test_truncation(self):
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(-1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            [2, 3, 4, 5],
        )
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(0, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            [1, 2, 3, 4],
        )
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(-2, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            [3, 4],
        )

        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(-6, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            list(),
        )
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(0, -6),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            list(),
        )

    def test_padding(self):
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            [None, 1, 2, 3, 4, 5],
        )
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(0, 1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            [1, 2, 3, 4, 5, None],
        )
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(1, 2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            [None, 1, 2, 3, 4, 5, None, None],
        )
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(2, 1),
                padding_value=(0,),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            [0, 0, 1, 2, 3, 4, 5, 0],
        )

        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(3, 4),
                padding_value=(-1, -2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            [-1, -2, -1, 1, 2, 3, 4, 5, -1, -2, -1, -2],
        )
        try:
            result = normalize_length_of_mutable_sequence(
                mutable_sequence=[1, 2, 3, 4, 5],
                proposed_length_change=(4, 3),
                padding_value=("test", 1.2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertAlmostEqual(
            result,
            ["test", 1.2, "test", 1.2, 1, 2, 3, 4, 5, "test", 1.2, "test"],
        )


class TestLengthNormalizationOfText(unittest.TestCase):
    def test_truncation(self):
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(-1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            "2345",
        )
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(0, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            "1234",
        )
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(-2, -1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was possible: {e}",
            )
        self.assertEqual(
            result,
            "34",
        )

        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(-6, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            "",
        )
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(0, -6),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when truncation was sane: {e}",
            )
        self.assertEqual(
            result,
            "",
        )

    def test_padding(self):
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(1, 0),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            "_12345",
        )
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(0, 1),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            "12345_",
        )
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(1, 2),
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            "_12345__",
        )

        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(2, 1),
                padding_value="a",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            "aa12345a",
        )
        try:
            result = normalize_length_of_text(
                text="12345",
                proposed_length_change=(3, 4),
                padding_value="ab",
            )
        except Exception as e:
            self.assert_(
                False,
                f"Threw exception when padding was possible: {e}",
            )
        self.assertEqual(
            result,
            "aba12345abab",
        )
