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
    Dict,
    Literal,
    Tuple,
    Type,
)
import warnings

from amend.built_in.numbers.integers import amend_integer


def _amend_data_mapping(
    data_mapping_type: Type[dict],
    data_mapping,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[
        Tuple[Any, Any],
        ...,
    ] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_violation_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Dict[Any, Any]:
    """Amend a data mapping.

    Parameters
    ----------
    data_mapping_type : Type[dict]
        Type of the data mapping. Only dict for now.
    data_mapping
        Something that should in essence be a data mapping.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `data_mapping` isn't a `data_mapping_type`. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : Tuple[Tuple[Any, Any], ...]
        Value to set `data_mapping` to if `data_mapping_type(data_mapping)` throws an
        Exception. By default, raises a TypeError.
    minimum_length : int
        The smallest length `data_mapping` can have. Defaults to no lower limit.
    maximum_length : int
        The largest length `data_mapping` can have. Defaults to no upper limit.
    length_violation_action: Literal['error', 'warning']
        What to do if `data_mapping` length is not between `minimum_length` and
        `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a UserWarning. Ignores length violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Dict[Any, Any]
        The amended data mapping.

    Raises
    ------
    TypeError
        When any of the following applies
        - `data_mapping` isn't a `data_mapping_type` and `type_mismatch_action` is
        'error'
        - `data_mapping_type(data_mapping)` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `data_mapping_type` isn't a dict
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a tuple of only tuples
        - `warning_stack_level` isn't None or in essence an integer >= 2
        - `minimum_length` isn't None or in essence an integer >= 0
        - `maximum_length` isn't None or in essence an integer >= 0
        - `length_violation_action` isn't None, 'error', or 'warning'
        - `data_mapping` length isn't between `minimum_length` and `maximum_length` and
        `length_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `data_mapping` isn't a `data_mapping_type` and `type_mismatch_action` is
        'warning'
        - `data_mapping` length isn't between `minimum_length` and `maximum_length` and
        `length_violation_action` is 'warning'
    """

    if data_mapping_type not in (dict,):
        raise ValueError(f"Invalid data mapping type {repr(data_mapping_type)}")
    if type_mismatch_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(f"Invalid type mismatch action {repr(type_mismatch_action)}")
    if not (
        value_on_cast_error is None
        or (
            isinstance(
                value_on_cast_error,
                tuple,
            )
            and all(
                isinstance(
                    element,
                    tuple,
                )
                for element in value_on_cast_error
            )
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
        data_mapping,
        data_mapping_type,
    ):
        if type_mismatch_action is not None:
            message = f"Entity {repr(data_mapping)} isn't a {data_mapping_type}"
            if type_mismatch_action == "error":
                raise TypeError(message)
            elif type_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )
        try:
            data_mapping = data_mapping_type(data_mapping)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(
                    f"Failed to cast {repr(data_mapping)} to {data_mapping_type}"
                )

            data_mapping = value_on_cast_error
            data_mapping = data_mapping_type(data_mapping)

    if length_violation_action is not None:
        if minimum_length is not None and len(data_mapping) < minimum_length:
            message = "".join(
                (
                    f"Data mapping has length {len(data_mapping)} smaller than ",
                    f"minimum length {minimum_length}",
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

        if maximum_length is not None and len(data_mapping) > maximum_length:
            message = "".join(
                (
                    f"Data mapping has length {len(data_mapping)} greater than ",
                    f"maximum length {maximum_length}",
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

    return data_mapping


def amend_mutable_data_mapping(
    mutable_data_mapping,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[
        Tuple[Any, Any],
        ...,
    ] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_violation_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Dict[Any, Any]:
    """Amend a mutable data mapping.

    Parameters
    ----------
    mutable_data_mapping
        Something that should in essence be a mutable data mapping.
    mutable_data_mapping : Literal['error', 'warning']
        What to do if `mutable_data_mapping` isn't a `dict. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : Tuple[Tuple[Any, Any], ...]
        Value to set `mutable_data_mapping` to if `dict(data_mapping)` throws an
        Exception. By default, raises a TypeError.
    minimum_length : int
        The smallest length `data_mapping` can have. Defaults to no lower limit.
    maximum_length : int
        The largest length `data_mapping` can have. Defaults to no upper limit.
    length_violation_action: Literal['error', 'warning']
        What to do if `mutable_data_mapping` length is not between `minimum_length` and
        `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a UserWarning. Ignores length violations by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Dict[Any, Any]
        The amended mutable data mapping.

    Raises
    ------
    TypeError
        When any of the following applies
        - `mutable_data_mapping` isn't a dict and `type_mismatch_action` is 'error'
        - `dict(data_mapping)` throws an Exception and `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a tuple of only tuples
        - `warning_stack_level` isn't None or in essence an integer >= 2
        - `minimum_length` isn't None or in essence an integer >= 0
        - `maximum_length` isn't None or in essence an integer >= 0
        - `length_violation_action` isn't None, 'error', or 'warning'
        - `data_mapping` length isn't between `minimum_length` and `maximum_length` and
        `length_violation_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `data_mapping` isn't a dict and `type_mismatch_action` is 'warning'
        - `data_mapping` length isn't between `minimum_length` and `maximum_length` and
        `length_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_mapping(
        data_mapping_type=dict,
        data_mapping=mutable_data_mapping,
        type_mismatch_action=type_mismatch_action,
        value_on_cast_error=value_on_cast_error,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_violation_action=length_violation_action,
        warning_stack_level=warning_stack_level,
    )
