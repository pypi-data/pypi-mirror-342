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

import math
from typing import Literal
import warnings

from amend.built_in.numbers.integers import amend_integer


def amend_real_number(
    real_number,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: float = None,
    minimum_value: float = None,
    maximum_value: float = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    infinite_value_action: Literal[
        "error",
        "warning",
    ] = None,
    not_a_number_value_action: Literal[
        "error",
        "warning",
    ] = None,
    number_of_rounding_decimals: int = None,
    warning_stack_level: int = None,
) -> int:
    """Amend a real number.

    Parameters
    ----------
    real_number
        Something that should in essence be a real_number.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `real_number` isn't a float. If 'error', raises a TypeError. If
        'warning', raises a UserWarning. Ignores type mismatches by default.
    value_on_cast_error : float
        Value to set `real_number` to if `float(real_number)` throws an Exception. By
        default, raises a TypeError.
    minimum_value : float
        The smallest value `real_number` can have. Defaults to no lower limit.
    maximum_value : float
        The largest value `real_number` can have. Defaults to no upper limit.
    value_violation_action: Literal['error', 'warning', 'clamp']
        What to do if `real_number` is not between `minimum_value` and `maximum_value`.
        If 'error', raises a ValueError. If 'warning', raises a UserWarning. If 'clamp',
        clamps `real_number` between `minimum_value` and `maximum_value`. Ignores value
        violations by default.
    infinite_value_action : Literal['error', 'warning']
        What to do if `real_number` is an infinity. If 'error', raises a ValueError. If
        'warning', raises a UserWarning. Ignores infinite values by default.
    not_a_number_value_action : Literal['error', 'warning']
        What to do if `real_number` is not-a-number. If 'error', raises a ValueError.
        If 'warning', raises a UserWarning. Ignores not-a-number values by default.
    number_of_rounding_decimals : int
        Number of decimals to round `real_number` to. Leave as-is by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    float
        The amended real number.

    Raises
    ------
    TypeError
        When any of the following applies
        - `real_number` isn't a float and `type_mismatch_action` is 'error'
        - `float(real_number)` throws an Exception and `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a float
        - `minimum_value` isn't None and isn't a float
        - `maximum_value` isn't None and isn't a float
        - `value_violation_action` isn't None, 'error', 'warning' or 'clamp'
        - `infinite_value_action` isn't None, 'error' or 'warning'
        - `not_a_number_value_action` isn't None, 'error' or 'warning'
        - `real_number` isn't between `minimum_value` and `maximum_value` and
        `value_violation_action` is 'error'
        - `real_number` is an inifinity and `infinite_value_action` is 'error'
        - `real_number` is not-a-number and `not_a_number_value_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `real_number` isn't a float and `type_mismatch_action` is 'warning'
        - `real_number` isn't between `minimum_length` and `maximum_length` and
        `value_violation_action` is 'warning'
    """
    if type_mismatch_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(f"Invalid type mismatch action {repr(type_mismatch_action)}")
    if not (
        value_on_cast_error is None
        or isinstance(
            value_on_cast_error,
            float,
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not (
        minimum_value is None
        or isinstance(
            minimum_value,
            float,
        )
    ):
        raise ValueError(f"Invalid minimum value {repr(minimum_value)}")
    if not (
        maximum_value is None
        or isinstance(
            maximum_value,
            float,
        )
    ):
        raise ValueError(f"Invalid maximum value {repr(maximum_value)}")
    if value_violation_action not in (
        None,
        "error",
        "warning",
        "clamp",
    ):
        raise ValueError(
            f"Invalid value violation action {repr(value_violation_action)}"
        )
    if infinite_value_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(f"Invalid infinite value action {repr(infinite_value_action)}")
    if not_a_number_value_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid not-a-number value action {repr(not_a_number_value_action)}"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if number_of_rounding_decimals is not None:
        number_of_rounding_decimals = amend_integer(
            integer=number_of_rounding_decimals,
            type_mismatch_action="warning",
            warning_stack_level=warning_stack_level + 1,
        )

    if not isinstance(
        real_number,
        float,
    ):
        if type_mismatch_action is not None:
            message = f"Entity {repr(real_number)} isn't a float"
            if type_mismatch_action == "error":
                raise TypeError(message)
            elif type_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    stacklevel=warning_stack_level,
                )
        try:
            real_number = float(real_number)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(f"Failed to cast {repr(real_number)} to float")

            real_number = value_on_cast_error

    if minimum_value is not None and real_number < minimum_value:
        message = "".join(
            (
                f"Real number {real_number} is smaller than minimum value ",
                f"{minimum_value}",
            )
        )
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )
        elif value_violation_action == "clamp":
            real_number = minimum_value

    if maximum_value is not None and real_number > maximum_value:
        message = "".join(
            (
                f"Real number {real_number} is greater than minimum value ",
                f"{maximum_value}",
            )
        )
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )
        elif value_violation_action == "clamp":
            real_number = maximum_value

    if infinite_value_action is not None and math.isinf(real_number):
        message = f"Real number {real_number} is an infinity"
        if infinite_value_action == "error":
            raise ValueError(message)
        elif infinite_value_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )

    if not_a_number_value_action is not None and math.isnan(real_number):
        message = f"Real number {real_number} isn't a number"
        if not_a_number_value_action == "error":
            raise ValueError(message)
        elif not_a_number_value_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                stacklevel=warning_stack_level,
            )

    if number_of_rounding_decimals is not None:
        real_number = round(
            real_number,
            number_of_rounding_decimals,
        )

    return real_number
