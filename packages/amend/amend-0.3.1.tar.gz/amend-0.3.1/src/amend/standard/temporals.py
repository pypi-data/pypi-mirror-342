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
from typing import (
    Literal,
    Type,
    Union,
)
import warnings

from amend.built_in.numbers.integers import amend_integer


def _amend_temporal_value(
    temporal_value_type: Union[
        Type[datetime.date],
        Type[datetime.datetime],
        Type[datetime.time],
        Type[datetime.timedelta],
    ],
    temporal_value,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Union[
        datetime.date,
        datetime.datetime,
        datetime.time,
        datetime.timedelta,
    ] = None,
    minimum_value: Union[
        datetime.date,
        datetime.datetime,
        datetime.time,
        datetime.timedelta,
    ] = None,
    maximum_value: Union[
        datetime.date,
        datetime.datetime,
        datetime.time,
        datetime.timedelta,
    ] = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> Union[
    datetime.date,
    datetime.datetime,
    datetime.time,
    datetime.timedelta,
]:
    """Amend a temporal value.

    Parameters
    ----------
    temporal_value_type : Union[Type[datetime.date], Type[datetime.datetime], Type
    [datetime.time], Type[datetime.timedelta]]
        Type of the temporal value; either a datetime.date, datetime.datetime,
        datetime.time or datetime.timedelta.
    temporal_value
        Something that should in essence be a temporal value.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `temporal_value` isn't an int. If 'error', raises a TypeError. If
        'warning', raises a UserWarning. Ignores type mismatches by default.
    value_on_cast_error : Union[datetime.date, datetime.datetime, datetime.time,
    datetime.timedelta]
        Value to set `temporal_value` to if
        `temporal_value_type(**vars(temporal_value))` throws an Exception. By default,
        raises a TypeError.
    minimum_value : Union[datetime.date, datetime.datetime, datetime.time,
    datetime.timedelta]
        The smallest value `temporal_value` can have. Defaults to no lower limit.
    maximum_value : Union[datetime.date, datetime.datetime, datetime.time,
    datetime.timedelta]
        The largest value `temporal_value` can have. Defaults to no upper limit.
    value_violation_action: Literal['error', 'warning', 'clamp']
        What to do if `temporal_value` is not between `minimum_value` and
        `maximum_value`. If 'error', raises a ValueError. If 'warning', raises a UserWarning. If 'clamp', clamps `temporal_value` between `minimum_value` and
        `maximum_value`. Ignores value violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Union[datetime.date, datetime.datetime, datetime.time, datetime.timedelta]
        The amended temporal value.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `temporal_value` isn't a `temporal_value_type` and `type_mismatch_action` is
        'error'
        - `temporal_value_type(**vars(temporal_value))` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a `temporal_value_type`
        - `minimum_value` isn't None and isn't a `temporal_value_type`
        - `maximum_value` isn't None and isn't a `temporal_value_type`
        - `value_violation_action` isn't None, 'error', 'warning' or 'clamp'
        - `temporal_value` isn't between `minimum_value` and `maximum_value` and
        `value_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `temporal_value` isn't a `temporal_value_type` and `type_mismatch_action` is
        'warning'
        - `temporal_value` isn't between `minimum_length` and `maximum_length` and
        `value_violation_action` is 'warning'
    """
    if temporal_value_type not in (
        datetime.date,
        datetime.datetime,
        datetime.time,
        datetime.timedelta,
    ):
        raise ValueError(f"Invalid temporal value type {repr(temporal_value_type)}")
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
            temporal_value_type,
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not (
        minimum_value is None
        or isinstance(
            minimum_value,
            temporal_value_type,
        )
    ):
        raise ValueError(f"Invalid minimum value {repr(minimum_value)}")
    if not (
        maximum_value is None
        or isinstance(
            maximum_value,
            temporal_value_type,
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
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    if not isinstance(
        temporal_value,
        temporal_value_type,
    ):
        if type_mismatch_action is not None:
            message = f"Entity {repr(temporal_value)} isn't a {temporal_value_type}"
            if type_mismatch_action == "error":
                raise TypeError(message)
            elif type_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    stacklevel=warning_stack_level,
                )
        try:
            if not isinstance(
                temporal_value,
                dict,
            ):
                temporal_value = vars(temporal_value)
            temporal_value = temporal_value_type(**temporal_value)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(
                    f"Failed to cast {repr(temporal_value)} to {temporal_value_type}"
                )

            temporal_value = value_on_cast_error

    if minimum_value is not None and temporal_value < minimum_value:
        message = f"Temporal value {temporal_value} is lesser than {minimum_value}"
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif value_violation_action == "clamp":
            temporal_value = minimum_value

    if maximum_value is not None and temporal_value > maximum_value:
        message = f"Temporal value {temporal_value} is greater than {maximum_value}"
        if value_violation_action == "error":
            raise ValueError(message)
        elif value_violation_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif value_violation_action == "clamp":
            temporal_value = maximum_value

    return temporal_value


def amend_date(
    date,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.date = None,
    minimum_value: datetime.date = None,
    maximum_value: datetime.date = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.date:
    """Amend a date.

    Parameters
    ----------
    date
        Something that should in essence be a date.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `date` isn't a `datetime.date`. If 'error', raises a TypeError. If
        'warning', raises a UserWarning. Ignores type mismatches by default.
    value_on_cast_error : datetime.date
        Value to set `date` to if `datetime.date(**vars(date))` throws an Exception. By
        default, raises a TypeError.
    minimum_value : datetime.date
        The smallest value `date` can have. Defaults to no lower limit.
    maximum_value : datetime.date
        The largest value `date` can have. Defaults to no upper limit.
    value_violation_action: Literal['error', 'warning', 'clamp']
        What to do if `date` is not between `minimum_value` and `maximum_value`. If
        'error', raises a ValueError. If 'warning', raises a UserWarning. If 'clamp', clamps `date` between `minimum_value` and `maximum_value`. Ignores value
        violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    datetime.date
        The amended date.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `date` isn't a datetime.date and `type_mismatch_action` is 'error'
        - `datetime.date(**vars(date))` throws an Exception and `value_on_cast_error`
        is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a datetime.date
        - `minimum_value` isn't None and isn't a datetime.date
        - `maximum_value` isn't None and isn't a datetime.date
        - `value_violation_action` isn't None, 'error', 'warning' or 'clamp'
        - `date` isn't between `minimum_value` and `maximum_value` and
        `value_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `date` isn't a datetime.date and `type_mismatch_action` is 'warning'
        - `date` isn't between `minimum_length` and `maximum_length` and
        `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.date,
        temporal_value=date,
        type_mismatch_action=type_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_date_and_time(
    date_and_time,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.date = None,
    minimum_value: datetime.date = None,
    maximum_value: datetime.date = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.datetime:
    """Amend date-and-time.

    Parameters
    ----------
    date_and_time
        Something that should in essence be a date-and-time.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `date_and_time` isn't a `datetime.datetime`. If 'error', raises a TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : datetime.datetime
        Value to set `date_and_time` to if `datetime.datetime(**vars(date))` throws an
        Exception. By default, raises a TypeError.
    minimum_value : datetime.datetime
        The smallest value `date_and_time` can have. Defaults to no lower limit.
    maximum_value : datetime.datetime
        The largest value `date_and_time` can have. Defaults to no upper limit.
    value_violation_action: Literal['error', 'warning', 'clamp']
        What to do if `date_and_time` is not between `minimum_value` and
        `maximum_value`. If 'error', raises a ValueError. If 'warning', raises a UserWarning. If 'clamp', clamps `date` between `minimum_value` and
        `maximum_value`. Ignores value violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    datetime.datetime
        The amended date-and-time.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `date_and_time` isn't a datetime.datetime and `type_mismatch_action` is
        'error'
        - `datetime.datetime(**vars(date))` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a datetime.datetime
        - `minimum_value` isn't None and isn't a datetime.datetime
        - `maximum_value` isn't None and isn't a datetime.datetime
        - `value_violation_action` isn't None, 'error', 'warning' or 'clamp'
        - `date_and_time` isn't between `minimum_value` and `maximum_value` and
        `value_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `date_and_time` isn't a datetime.datetime and `type_mismatch_action` is
        'warning'
        - `date_and_time` isn't between `minimum_length` and `maximum_length` and
        `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.datetime,
        temporal_value=date_and_time,
        type_mismatch_action=type_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_time(
    time,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.date = None,
    minimum_value: datetime.date = None,
    maximum_value: datetime.date = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.time:
    """Amend time.

    Parameters
    ----------
    time
        Something that should in essence be time.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `time` isn't a `datetime.time`. If 'error', raises a TypeError. If
        'warning', raises a UserWarning. Ignores type mismatches by default.
    value_on_cast_error : datetime.date
        Value to set `time` to if `datetime.time(**vars(time))` throws an Exception. By
        default, raises a TypeError.
    minimum_value : datetime.time
        The smallest value `time` can have. Defaults to no lower limit.
    maximum_value : datetime.date
        The largest value `time` can have. Defaults to no upper limit.
    value_violation_action: Literal['error', 'warning', 'clamp']
        What to do if `time` is not between `minimum_value` and `maximum_value`. If
        'error', raises a ValueError. If 'warning', raises a UserWarning. If 'clamp', clamps `time` between `minimum_value` and `maximum_value`. Ignores value
        violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    datetime.time
        The amended time.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `time` isn't a datetime.time and `type_mismatch_action` is 'error'
        - `datetime.time(**vars(time))` throws an Exception and `value_on_cast_error`
        is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a datetime.time
        - `minimum_value` isn't None and isn't a datetime.time
        - `maximum_value` isn't None and isn't a datetime.time
        - `value_violation_action` isn't None, 'error', 'warning' or 'clamp'
        - `time` isn't between `minimum_value` and `maximum_value` and
        `value_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `time` isn't a datetime.time and `type_mismatch_action` is 'warning'
        - `time` isn't between `minimum_length` and `maximum_length` and
        `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.time,
        temporal_value=time,
        type_mismatch_action=type_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )


def amend_temporal_offset(
    temporal_offset,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: datetime.timedelta = None,
    minimum_value: datetime.timedelta = None,
    maximum_value: datetime.timedelta = None,
    value_violation_action: Literal[
        "error",
        "warning",
        "clamp",
    ] = None,
    warning_stack_level: int = None,
) -> datetime.timedelta:
    """Amend a temporal offset.

    Parameters
    ----------
    temporal_offset
        Something that should in essence be a temporal offset.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `temporal_offset` isn't a `datetime.timedelta`. If 'error',
        raises a TypeError. If 'warning', raises a UserWarning. Ignores type mismatches
        by default.
    value_on_cast_error : datetime.timedelta
        Value to set `temporal_offset` to if
        `datetime.timedelta(**vars(temporal_offset))` throws an Exception. By default,
        raises a TypeError.
    minimum_value : datetime.timedelta
        The smallest value `temporal_offset` can have. Defaults to no lower limit.
    maximum_value : datetime.timedelta
        The largest value `temporal_offset` can have. Defaults to no upper limit.
    value_violation_action: Literal['error', 'warning', 'clamp']
        What to do if `temporal_offset` is not between `minimum_value` and
        `maximum_value`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. If 'clamp', clamps `temporal_offset` between `minimum_value` and
        `maximum_value`. Ignores value violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    datetime.timedelta
        The amended temporal offset.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `temporal_offset` isn't a datetime.timedelta and `type_mismatch_action` is
        'error'
        - `datetime.timedelta(**vars(temporal_offset))` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a datetime.timedelta
        - `minimum_value` isn't None and isn't a datetime.timedelta
        - `maximum_value` isn't None and isn't a datetime.timedelta
        - `value_violation_action` isn't None, 'error', 'warning' or 'clamp'
        - `temporal_offset` isn't between `minimum_value` and `maximum_value` and
        `value_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `temporal_offset` isn't a datetime.timedelta and `type_mismatch_action` is
        'warning'
        - `temporal_offset` isn't between `minimum_length` and `maximum_length` and
        `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_temporal_value(
        temporal_value_type=datetime.timedelta,
        temporal_value=temporal_offset,
        type_mismatch_action=type_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_value=minimum_value,
        maximum_value=maximum_value,
        value_violation_action=value_violation_action,
        warning_stack_level=warning_stack_level + 1,
    )
