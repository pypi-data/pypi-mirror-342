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
    Iterable,
    List,
    Literal,
    Tuple,
    Type,
    Union,
)
import warnings

from amend.built_in.numbers.integers import amend_integer
from amend.utilities.normalization import (
    _normalize_length_of_sequence_container,
    determine_length_normalization_strategy,
)


def _amend_sequence_container(
    sequence_container_type: Union[
        Type[list],
        Type[tuple],
    ],
    sequence_container,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[Any, ...] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    length_violation_action: Literal[
        "error",
        "warning",
        "truncate-and-pad",
    ] = None,
    truncation_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> Union[
    List[Any],
    Tuple[Any, ...],
]:
    """Amend a sequence container.

    Parameters
    ----------
    sequence_container_type : Union[Type[list], Type[tuple]]
        Type of the sequence container; either a list or tuple.
    sequence_container
        Something that should in essence be a sequence container.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `sequence_container` isn't a `sequence_container_type`. If
        'error', raises a TypeError. If 'warning', raises a UserWarning. Ignores type
        mismatches by default.
    value_on_cast_error : Tuple[Any, ...]
        Value to set `sequence_container` to if
        `sequence_container_type(sequence_container)` throws an Exception. By default,
        raises a TypeError.
    minimum_length : int
        The smallest length `sequence_container` can have. Defaults to no lower limit.
    maximum_length : int
        The largest value `sequence_container` can have. Defaults to no upper limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers `sequence_container` length should be a multiple of. Ignores length factorization by default.
    length_violation_action: Literal['error', 'warning', 'truncate-and-pad']
        What to do if `sequence_container` length is not between `minimum_length` and
        `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. If 'truncate-and-pad', will attempt to truncate or pad
        `sequence_container` to satisfy `minimum_length`, `maximum_length` and
        `length_is_multiple_of`. Ignores length violations by default.
    truncation_side : Literal["left", "right", "both-but-prioritize-left", "both-but-prioritize-right"]
        What side to truncate on. If 'left', will truncate from the left. If 'right',
        will truncate from the right. If 'both-but-prioritize-left', will truncate from
        both sides equally, giving priority to left-truncation. If
        'both-but-prioritize-right', will truncate from both sides equally, giving
        priority to right-truncation. Truncation is disabled by default.
    padding_side : Literal["left", "right", "both-but-prioritize-left", "both-but-prioritize-right"]
        What side to pad to. If 'left', will pad to the left. If 'right', will pad to
        the right. If 'both-but-prioritize-left', will pad to both sides equally, giving priority to left-padding. If 'both-but-prioritize-right', will pad to
        both sides equally, giving priority to right-padding. Padding is disabled by
        default.
    padding_value : Tuple[Any, ...]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with None.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Union[List[Any], Tuple[Any, ...]]
        The amended sequence container.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `sequence_container` isn't a `sequence_container_type` and
        `type_mismatch_action` is 'error'
        - `sequence_container_type(sequence_container)` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `sequence_container_type` is not a list or tuple
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a tuple
        - `length_violation_action` isn't None, 'error', 'warning' or 'truncate-or-pad'
        - `sequence_container` length isn't between `minimum_length` and
        `maximum_length` and/or doesn't satisfy `length_is_multiple_of` and
        `length_violation_action` is 'error'
        - impossible to transform `sequence_container` to fit length constraints

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `sequence_container` isn't a `sequence_container_type` and
        `type_mismatch_action` is 'warning'
        - `sequence_container` isn't between `minimum_length` and `maximum_length`
        and/or doesn't satisfy `length_is_multiple_of` and `value_violation_action` is
        'warning'
    """
    if sequence_container_type not in (
        list,
        tuple,
    ):
        raise ValueError(
            f"Invalid sequence container type {repr(sequence_container_type)}"
        )
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
            tuple,
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
    if length_violation_action not in (
        None,
        "error",
        "warning",
        "truncate-and-pad",
    ):
        raise ValueError(
            f"Invalid length violation action {repr(length_violation_action)}"
        )
    if (
        not isinstance(
            sequence_container,
            sequence_container_type,
        )
        and type_mismatch_action is not None
    ):
        message = f"Entity {repr(sequence_container)} isn't {sequence_container_type}"
        if type_mismatch_action == "error":
            raise TypeError(message)
        elif type_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )

    try:
        sequence_container = sequence_container_type(sequence_container)
    except Exception:
        if value_on_cast_error is None:
            raise TypeError(
                "".join(
                    (
                        f"Failed to cast {repr(sequence_container)} to ",
                        f"{sequence_container_type}",
                    )
                )
            )

        sequence_container = value_on_cast_error
        sequence_container = sequence_container_type(sequence_container)

    proposed_length_changes = determine_length_normalization_strategy(
        length=len(sequence_container),
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_is_multiple_of=length_is_multiple_of,
        truncation_side=truncation_side,
        padding_side=padding_side,
        warning_stack_level=warning_stack_level + 1,
    )
    if proposed_length_changes != (
        0,
        0,
    ):
        message = "".join(
            (
                f"Entity {repr(sequence_container)} has incorrect length ",
                f"{len(sequence_container)}",
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
        else:
            if proposed_length_changes == None:
                raise ValueError(
                    "".join(
                        (
                            "Impossible to satisfy length constraints for ",
                            f"{repr(sequence_container)}",
                        )
                    )
                )

        sequence_container = _normalize_length_of_sequence_container(
            sequence_container=sequence_container,
            proposed_length_change=proposed_length_changes,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )

    return sequence_container


def amend_immutable_sequence(
    immutable_sequence,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[Any, ...] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    length_violation_action: Literal[
        "error",
        "warning",
        "truncate-and-pad",
    ] = None,
    truncation_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> Tuple[Any, ...]:
    """Amend an immutable sequence container.

    Parameters
    ----------
    immutable_sequence_container
        Something that should in essence be an immutable sequence container.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `immutable_sequence_container` isn't a tuple. If 'error', raises
        a TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : Tuple[Any, ...]
        Value to set `immutable_sequence_container` to if
        `tuple(immutable_sequence_container)` throws an Exception. By default, raises a
        TypeError.
    minimum_length : int
        The smallest length `immutable_sequence_container` can have. Defaults to no
        lower limit.
    maximum_length : int
        The largest value `immutable_sequence_container` can have. Defaults to no upper
        limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers `immutable_sequence_container` length should be a multiple of.
        Ignores length factorization by default.
    length_violation_action: Literal['error', 'warning', 'truncate-and-pad']
        What to do if `immutable_sequence_container` length is not between `minimum_length` and `maximum_length`. If 'error', raises a ValueError. If
        'warning', raises a UserWarning. If 'truncate-and-pad', will attempt to
        truncate or pad `immutable_sequence_container` to satisfy `minimum_length`,
        `maximum_length` and `length_is_multiple_of`. Ignores length violations by
        default.
    truncation_side : Literal["left", "right", "both-but-prioritize-left", "both-but-prioritize-right"]
        What side to truncate on. If 'left', will truncate from the left. If 'right',
        will truncate from the right. If 'both-but-prioritize-left', will truncate from
        both sides equally, giving priority to left-truncation. If
        'both-but-prioritize-right', will truncate from both sides equally, giving
        priority to right-truncation. Truncation is disabled by default.
    padding_side : Literal["left", "right", "both-but-prioritize-left", "both-but-prioritize-right"]
        What side to pad to. If 'left', will pad to the left. If 'right', will pad to
        the right. If 'both-but-prioritize-left', will pad to both sides equally, giving priority to left-padding. If 'both-but-prioritize-right', will pad to
        both sides equally, giving priority to right-padding. Padding is disabled by
        default.
    padding_value : Tuple[Any, ...]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with None.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Tuple[Any, ...]
        The amended immutable sequence container.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `immutable_sequence_container` isn't a tuple and `type_mismatch_action` is
        'error'
        - `tuple(immutable_sequence_container)` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a tuple
        - `length_violation_action` isn't None, 'error', 'warning' or 'truncate-or-pad'
        - `immutable_sequence_container` length isn't between `minimum_length` and
        `maximum_length` and/or doesn't satisfy `length_is_multiple_of` and
        `length_violation_action` is 'error'
        - impossible to transform `immutable_sequence_container` to fit length
        constraints

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `immutable_sequence_container` isn't a tuple and `type_mismatch_action` is
        'warning'
        - `immutable_sequence_container` isn't between `minimum_length` and
        `maximum_length` and/or doesn't satisfy `length_is_multiple_of` and
        `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return tuple(
        _amend_sequence_container(
            sequence_container_type=tuple,
            sequence_container=immutable_sequence,
            type_mismatch_action=type_mismatch_action,
            value_on_cast_error=value_on_cast_error,
            minimum_length=minimum_length,
            maximum_length=maximum_length,
            length_is_multiple_of=length_is_multiple_of,
            length_violation_action=length_violation_action,
            truncation_side=truncation_side,
            padding_side=padding_side,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )
    )


def amend_mutable_sequence(
    mutable_sequence,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Tuple[Any, ...] = None,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    length_violation_action: Literal[
        "error",
        "warning",
        "truncate-and-pad",
    ] = None,
    truncation_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_side: Literal[
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ] = None,
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> List[Any]:
    """Amend a mutable sequence container.

    Parameters
    ----------
    mutable_sequence_container
        Something that should in essence be an mutable sequence container.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `mutable_sequence_container` isn't a list. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : Tuple[Any, ...]
        Value to set `mutable_sequence_container` to if
        `list(mutable_sequence_container)` throws an Exception. By default, raises a
        TypeError.
    minimum_length : int
        The smallest length `mutable_sequence_container` can have. Defaults to no lower
        limit.
    maximum_length : int
        The largest value `mutable_sequence_container` can have. Defaults to no upper
        limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers `mutable_sequence_container` length should be a multiple of.
        Ignores length factorization by default.
    length_violation_action: Literal['error', 'warning', 'truncate-and-pad']
        What to do if `mutable_sequence_container` length is not between
        `minimum_length` and `maximum_length`. If 'error', raises a ValueError. If
        'warning', raises a UserWarning. If 'truncate-and-pad', will attempt to
        truncate or pad `mutable_sequence_container` to satisfy `minimum_length`,
        `maximum_length` and `length_is_multiple_of`. Ignores length violations by
        default.
    truncation_side : Literal["left", "right", "both-but-prioritize-left", "both-but-prioritize-right"]
        What side to truncate on. If 'left', will truncate from the left. If 'right',
        will truncate from the right. If 'both-but-prioritize-left', will truncate from
        both sides equally, giving priority to left-truncation. If
        'both-but-prioritize-right', will truncate from both sides equally, giving
        priority to right-truncation. Truncation is disabled by default.
    padding_side : Literal["left", "right", "both-but-prioritize-left", "both-but-prioritize-right"]
        What side to pad to. If 'left', will pad to the left. If 'right', will pad to
        the right. If 'both-but-prioritize-left', will pad to both sides equally, giving priority to left-padding. If 'both-but-prioritize-right', will pad to
        both sides equally, giving priority to right-padding. Padding is disabled by
        default.
    padding_value : Tuple[Any, ...]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with None.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    List[Any]
        The amended mutable sequence container.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `mutable_sequence_container` isn't a tuple and `type_mismatch_action` is
        'error'
        - `list(mutable_sequence_container)` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't a list
        - `length_violation_action` isn't None, 'error', 'warning' or 'truncate-or-pad'
        - `mutable_sequence_container` length isn't between `minimum_length` and
        `maximum_length` and/or doesn't satisfy `length_is_multiple_of` and
        `length_violation_action` is 'error'
        - impossible to transform `mutable_sequence_container` to fit length constraints

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `mutable_sequence_container` isn't a list and `type_mismatch_action` is
        'warning'
        - `mutable_sequence_container` isn't between `minimum_length` and
        `maximum_length` and/or doesn't satisfy `length_is_multiple_of` and
        `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return list(
        _amend_sequence_container(
            sequence_container_type=tuple,
            sequence_container=mutable_sequence,
            type_mismatch_action=type_mismatch_action,
            value_on_cast_error=value_on_cast_error,
            minimum_length=minimum_length,
            maximum_length=maximum_length,
            length_is_multiple_of=length_is_multiple_of,
            length_violation_action=length_violation_action,
            truncation_side=truncation_side,
            padding_side=padding_side,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )
    )
