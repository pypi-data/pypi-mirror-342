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

from typing import (
    Any,
    FrozenSet,
    Literal,
    Set,
    Type,
    Union,
)
import warnings

from amend.built_in.numbers.integers import amend_integer


def _amend_data_set(
    data_set_type: Union[
        Type[frozenset],
        Type[set],
    ],
    data_set,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: FrozenSet[Any] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_violation_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Union[
    FrozenSet[Any],
    Set[Any],
]:
    """Amend a data set.

    Parameters
    ----------
    data_set_type : Union[Type[frozenset], Type[set]]
        Type of the sequence container; either a frozenset or set.
    data_set
        Something that should in essence be a data set.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `data_set` isn't a `data_set_type`. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : FrozenSet[Any]
        Value to set `data_set` to if `data_set_type(data_set)` throws an Exception. By
        default, raises a TypeError.
    minimum_length : int
        The smallest length `data_set` can have. Defaults to no lower limit.
    maximum_length : int
        The largest value `data_set` can have. Defaults to no upper limit.
    length_violation_action: Literal['error', 'warning']
        What to do if `data_set` length is not between `minimum_length` and
        `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. Ignores length violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Union[FrozenSet[Any], Set[Any]]
        The amended data set.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `data_set` isn't a `data_set_type` and `type_mismatch_action` is 'error'
        - `data_set_type(data_set)` throws an Exception and `value_on_cast_error` is
        None

    ValueError
        When any of the following applies:
        - `data_set_type` is not a list or tuple
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a frozenset
        - `length_violation_action` isn't None, 'error' or 'warning'
        - `data_set` length isn't between `minimum_length` and `maximum_length` and
        `length_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `data_set` isn't a `data_set_type` and `type_mismatch_action` is 'warning'
        - `data_set` length isn't between `minimum_length` and `maximum_length` and
        `value_violation_action` is 'warning'
    """
    if data_set_type not in (
        frozenset,
        set,
    ):
        raise ValueError(f"Invalid data set type {repr(data_set_type)}")
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
            frozenset,
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if minimum_length is not None:
        minimum_length = amend_integer(
            integer=minimum_length,
            type_mismatch_action="error",
            minimum_value=0,
            value_violation_action="error",
            warning_stack_level=warning_stack_level + 1,
        )
    if maximum_length is not None:
        maximum_length = amend_integer(
            integer=maximum_length,
            type_mismatch_action="error",
            minimum_value=0,
            value_violation_action="error",
            warning_stack_level=warning_stack_level + 1,
        )
    if length_violation_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid length violation action {repr(length_violation_action)}"
        )
    if not isinstance(
        data_set,
        data_set_type,
    ):
        if type_mismatch_action is not None:
            message = f"Entity {repr(data_set)} isn't a {data_set_type}"
            if type_mismatch_action == "error":
                raise TypeError(message)
            elif type_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )
        try:
            data_set = data_set_type(data_set)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(f"Failed to cast {repr(data_set)} to {data_set_type}")

            data_set = value_on_cast_error
            data_set = data_set_type(data_set)

    if length_violation_action is not None:
        if minimum_length is not None and len(data_set) < minimum_length:
            message = "".join(
                (
                    f"Data set has length {len(data_set)} smaller than minimum length",
                    f"{minimum_length}",
                )
            )
            if length_violation_action == "error":
                raise ValueError(message)
            elif length_violation_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )

        if maximum_length is not None and len(data_set) > maximum_length:
            message = "".join(
                (
                    f"Data set has length {len(data_set)} greater than maximum length",
                    f"{maximum_length}",
                )
            )
            if length_violation_action == "error":
                raise ValueError(message)
            elif length_violation_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )

    return data_set


def amend_immutable_data_set(
    immutable_data_set,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: FrozenSet[Any] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_violation_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> FrozenSet[Any]:
    """Amend a immutable data set.

    Parameters
    ----------
    immutable_data_set
        Something that should in essence be a immutable data set.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `immutable_data_set` isn't a frozenset. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : FrozenSet[Any]
        Value to set `data_set` to if `frozenset(data_set)` throws an Exception. By
        default, raises a TypeError.
    minimum_length : int
        The smallest length `immutable_data_set` can have. Defaults to no lower limit.
    maximum_length : int
        The largest value `immutable_data_set` can have. Defaults to no upper limit.
    length_violation_action: Literal['error', 'warning']
        What to do if `immutable_data_set` length is not between `minimum_length` and
        `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. Ignores length violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    FrozenSet[Any]
        The amended immutable data set.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `immutable_data_set` isn't a frozenset and `type_mismatch_action` is 'error'
        - `frozenset(data_set)` throws an Exception and `value_on_cast_error` is
        None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a frozenset
        - `length_violation_action` isn't None, 'error' or 'warning'
        - `immutable_data_set` length isn't between `minimum_length` and
        `maximum_length` and `length_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `immutable_data_set` isn't a frozenset and `type_mismatch_action` is 'warning'
        - `immutable_data_set` length isn't between `minimum_length` and
        `maximum_length` and `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_set(
        data_set_type=frozenset,
        data_set=immutable_data_set,
        type_mismatch_action=type_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_violation_action=length_violation_action,
        warning_stack_level=warning_stack_level,
    )


def amend_mutable_data_set(
    mutable_data_set,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: FrozenSet[Any] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_violation_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Set[Any]:
    """Amend a mutable data set.

    Parameters
    ----------
    mutable_data_set
        Something that should in essence be a mutable data set.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `mutable_data_set` isn't a frozenset. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : FrozenSet[Any]
        Value to set `data_set` to if `set(data_set)` throws an Exception. By default,
        raises a TypeError.
    minimum_length : int
        The smallest length `mutable_data_set` can have. Defaults to no lower limit.
    maximum_length : int
        The largest value `mutable_data_set` can have. Defaults to no upper limit.
    length_violation_action: Literal['error', 'warning']
        What to do if `mutable_data_set` length is not between `minimum_length` and
        `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. Ignores length violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Set[Any]
        The amended mutable data set.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `mutable_data_set` isn't a set and `type_mismatch_action` is 'error'
        - `set(data_set)` throws an Exception and `value_on_cast_error` is
        None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a frozenset
        - `length_violation_action` isn't None, 'error' or 'warning'
        - `mutable_data_set` length isn't between `minimum_length` and `maximum_length`
        and `length_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `mutable_data_set` isn't a set and `type_mismatch_action` is 'warning'
        - `mutable_data_set` length isn't between `minimum_length` and `maximum_length`
        and `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_set(
        data_set_type=set,
        data_set=mutable_data_set,
        type_mismatch_action=type_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_violation_action=length_violation_action,
        warning_stack_level=warning_stack_level,
    )
