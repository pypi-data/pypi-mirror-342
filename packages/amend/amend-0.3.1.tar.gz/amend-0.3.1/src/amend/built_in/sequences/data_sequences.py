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
    Iterable,
    Literal,
    Type,
    Union,
)
import warnings

from amend.built_in.numbers.integers import amend_integer
from amend.utilities.normalization import (
    _normalize_length_of_data_sequence,
    determine_length_normalization_strategy,
)


def _amend_data_sequence(
    data_sequence_type: Union[
        Type[bytearray],
        Type[bytes],
        Type[str],
    ],
    data_sequence,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Union[
        bytes,
        str,
    ] = None,
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
    padding_value: Union[
        bytes,
        str,
    ] = None,
    warning_stack_level: int = None,
) -> Union[
    bytearray,
    bytes,
    str,
]:
    """Amend a data sequence.

    Parameters
    ----------
    data_sequence_type : Union[Type[bytearray], Type[bytes], Type[str]]
        Type of the data sequence; either a bytearray, bytes or str.
    data_sequence
        Something that should in essence be a data sequence.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `data_sequence` isn't a `data_sequence_type`. If 'error', raises
        a TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by default.
    value_on_cast_error : Union[bytes, str]
        Value to set `data_sequence` to if `data_sequence_type(data_sequence)` throws
        an Exception. By default, raises a TypeError.
    minimum_length : int
        The smallest length `data_sequence` can have. Defaults to no lower limit.
    maximum_length : int
        The largest value `data_sequence` can have. Defaults to no upper limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers `data_sequence` length should be a multiple of. Ignores length
        factorization by default.
    length_violation_action: Literal['error', 'warning', 'truncate-and-pad']
        What to do if `data_sequence` length is not between `minimum_length` and `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a UserWarning. If 'truncate-and-pad', will attempt to truncate or pad `data_sequence` to satisfy `minimum_length`, `maximum_length` and
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
    padding_value : Union[bytes, str]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with the
        null byte or ASCII underscore ('_').
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Union[bytearray, bytes, str]
        The amended data sequence.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `data_sequence` isn't a `data_sequence_type` and `type_mismatch_action` is
        'error'
        - `data_sequence_type(data_sequence)` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `data_sequence_type` is not bytearray, bytes or str
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't bytes when `data_sequence_type` is
        is bytearray or bytes, or str when `data_sequence_type` is str
        - `length_violation_action` isn't None, 'error', 'warning' or 'truncate-or-pad'
        - `data_sequence` length isn't between `minimum_length` and `maximum_length`
        and/or doesn't satisfy `length_is_multiple_of` and `length_violation_action`
        is 'error'
        - isn't possible to transform `data_sequence` to fit length constraints

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `data_sequence` isn't a `data_sequence_type` and `type_mismatch_action` is
        'warning'
        - `data_sequence` isn't between `minimum_length` and `maximum_length` and/or
        doesn't satisfy `length_is_multiple_of` and `value_violation_action` is
        'warning'
    """
    if data_sequence_type not in (
        bytearray,
        bytes,
        str,
    ):
        raise ValueError(f"Invalid data sequence type {repr(data_sequence_type)}")
    if type_mismatch_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(f"Invalid type mismatch action {repr(type_mismatch_action)}")
    if not (
        value_on_cast_error is None
        or (
            data_sequence_type
            in (
                bytearray,
                bytes,
            )
            and isinstance(
                value_on_cast_error,
                bytes,
            )
        )
        or (
            data_sequence_type == str
            and isinstance(
                value_on_cast_error,
                str,
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
    if length_violation_action not in (
        None,
        "error",
        "warning",
        "truncate-and-pad",
    ):
        raise ValueError(
            f"Invalid length violation action {repr(length_violation_action)}"
        )
    if not isinstance(
        data_sequence,
        data_sequence_type,
    ):
        if type_mismatch_action is not None:
            message = f"Entity {repr(data_sequence)} isn't {data_sequence_type}"
            if type_mismatch_action == "error":
                raise TypeError(message)
            elif type_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )
        try:
            data_sequence = data_sequence_type(data_sequence)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(
                    f"Failed to cast {repr(data_sequence)} to {data_sequence_type}"
                )

            data_sequence = value_on_cast_error
            data_sequence = data_sequence_type(data_sequence)

    proposed_length_changes = determine_length_normalization_strategy(
        length=len(data_sequence),
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
        message = (
            f"Entity {repr(data_sequence)} has incorrect length {len(data_sequence)}"
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
                            f"{repr(data_sequence)}",
                        )
                    )
                )

        data_sequence = _normalize_length_of_data_sequence(
            data_sequence_type=data_sequence_type,
            data_sequence=data_sequence,
            proposed_length_change=proposed_length_changes,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )

    return data_sequence


def amend_immutable_binary(
    immutable_binary,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: bytes = None,
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
    padding_value: bytes = None,
    warning_stack_level: int = None,
) -> bytes:
    """Amend an immutable data sequence.

    Parameters
    ----------
    immutable_data_sequence
        Something that should in essence be an immutable data sequence.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `immutable_data_sequence` isn't bytes. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : bytes
        Value to set `immutable_data_sequence` to if `bytes(immutable_data_sequence)`
        throws an Exception. By default, raises a TypeError.
    minimum_length : int
        The smallest length `immutable_data_sequence` can have. Defaults to no lower
        limit.
    maximum_length : int
        The largest length `immutable_data_sequence` can have. Defaults to no lower
        limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers `immutable_data_sequence` length should be a multiple of.
        Ignores length factorization by default.
    length_violation_action: Literal['error', 'warning', 'truncate-and-pad']
        What to do if `immutable_data_sequence` length is not between `minimum_length`
        and `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. If 'truncate-and-pad', will attempt to truncate or pad
        `immutable_data_sequence` to satisfy `minimum_length`, `maximum_length` and
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
    padding_value : bytes
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with the
        null byte.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    bytes
        The amended immutable data sequence.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `immutable_data_sequence` isn't bytes and `type_mismatch_action` is 'error'
        - `bytes(immutable_data_sequence)` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't bytes
        - `length_violation_action` isn't None, 'error', 'warning' or 'truncate-or-pad'
        - `immutable_data_sequence` length isn't between `minimum_length` and
        `maximum_length`
        and/or doesn't satisfy `length_is_multiple_of` and `length_violation_action`
        is 'error'
        - isn't possible to transform `immutable_data_sequence` to fit length
        constraints

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `immutable_data_sequence` isn't bytes and `type_mismatch_action` is 'warning'
        - `immutable_data_sequence` isn't between `minimum_length` and `maximum_length`
        and/or doesn't satisfy `length_is_multiple_of` and `value_violation_action` is
        'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_sequence(
        data_sequence_type=bytes,
        data_sequence=immutable_binary,
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


def amend_mutable_binary(
    mutable_binary,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: bytes = None,
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
    padding_value: bytes = None,
    warning_stack_level: int = None,
) -> bytearray:
    """Amend a mutable data sequence.

    Parameters
    ----------
    mutable_data_sequence
        Something that should in essence be an mutable data sequence.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `mutable_data_sequence` isn't bytes. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : bytes
        Value to set `mutable_data_sequence` to if `bytes(mutable_data_sequence)`
        throws an Exception. By default, raises a TypeError.
    minimum_length : int
        The smallest length `mutable_data_sequence` can have. Defaults to no lower
        limit.
    maximum_length : int
        The largest length `mutable_data_sequence` can have. Defaults to no lower
        limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers `mutable_data_sequence` length should be a multiple of. Ignores
        length factorization by default.
    length_violation_action: Literal['error', 'warning', 'truncate-and-pad']
        What to do if `mutable_data_sequence` length is not between `minimum_length`
        and `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. If 'truncate-and-pad', will attempt to truncate or pad
        `mutable_data_sequence` to satisfy `minimum_length`, `maximum_length` and
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
    padding_value : bytes
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with the
        null byte.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    bytes
        The amended mutable data sequence.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `mutable_data_sequence` isn't a bytearray and `type_mismatch_action` is
        'error'
        - `bytearray(mutable_data_sequence)` throws an Exception and
        `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't bytes
        - `length_violation_action` isn't None, 'error', 'warning' or 'truncate-or-pad'
        - `mutable_data_sequence` length isn't between `minimum_length` and
        `maximum_length` and/or doesn't satisfy `length_is_multiple_of` and
        `length_violation_action` is 'error'
        - isn't possible to transform `mutable_data_sequence` to fit length constraints

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `mutable_data_sequence` isn't a bytearray and `type_mismatch_action` is
        'warning'
        - `mutable_data_sequence` isn't between `minimum_length` and `maximum_length`
        and/or doesn't satisfy `length_is_multiple_of` and `value_violation_action` is
        'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_sequence(
        data_sequence_type=bytearray,
        data_sequence=mutable_binary,
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


def amend_text(
    text,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: str = None,
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
    padding_value: str = None,
    warning_stack_level: int = None,
) -> str:
    """Amend text.

    Parameters
    ----------
    text
        Something that should in essence be text.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `text` isn't str. If 'error', raises a TypeError. If 'warning',
        raises a UserWarning. Ignores type mismatches by default.
    value_on_cast_error : str
        Value to set `text` to if `str(text)` throws an Exception. By default, raises a
        TypeError.
    minimum_length : int
        The smallest length `text` can have. Defaults to no lower limit.
    maximum_length : int
        The largest length `text` can have. Defaults to no lower limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers `text` length should be a multiple of. Ignores length
        factorization by default.
    length_violation_action: Literal['error', 'warning', 'truncate-and-pad']
        What to do if `text` length is not between `minimum_length` and
        `maximum_length`. If 'error', raises a ValueError. If 'warning', raises a
        UserWarning. If 'truncate-and-pad', will attempt to truncate or pad
        `mutable_data_sequence` to satisfy `minimum_length`, `maximum_length` and
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
    padding_value : str
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with ASCII
        underscore ('_').
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    str
        The amended text.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `text` isn't a str and `type_mismatch_action` is 'error'
        - `str(text)` throws an Exception and `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None and isn't str
        - `length_violation_action` isn't None, 'error', 'warning' or 'truncate-or-pad'
        - `text` length isn't between `minimum_length` and `maximum_length` and/or
        doesn't satisfy `length_is_multiple_of` and `length_violation_action` is 'error'
        - isn't possible to transform `text` to fit length constraints

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `text` isn't a str and `type_mismatch_action` is 'warning'
        - `text` isn't between `minimum_length` and `maximum_length` and/or doesn't
        satisfy `length_is_multiple_of` and `value_violation_action` is 'warning'
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _amend_data_sequence(
        data_sequence_type=str,
        data_sequence=text,
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
