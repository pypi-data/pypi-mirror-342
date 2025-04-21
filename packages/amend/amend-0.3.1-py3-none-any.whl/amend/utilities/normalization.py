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
from typing import (
    Any,
    Generator,
    Iterable,
    List,
    Literal,
    Tuple,
    Type,
    Union,
)

from amend.built_in.numbers.integers import amend_integer
from amend.built_in.mappings.data_mappings import amend_mutable_data_mapping


def find_least_common_multiplier(
    multiples: Iterable[int] = None,
    warning_stack_level: int = None,
) -> int:
    """Finds the least common multiplier for 1 or more natural number multiples.

    Parameters
    ----------
    multiples : Iterable[int]
        Natural numbers the result should be a multiple of. By default, returns 1
        (trivial solution).
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    int
        The least common multiplier of `multiples`.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `multiples` isn't iterable

    ValueError
        - any element of `multiples` is smaller than 1

    Warns
    -----
        When any of the following applies:
        - every time element in `multiples` isn't an int
    """
    if multiples is None:
        return 1
    try:
        multiples = iter(multiples)
    except Exception:
        raise TypeError(f"Multiples {repr(multiples)} isn't iterable")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    multiples = tuple(
        amend_integer(
            multiple,
            type_mismatch_action="warning",
            minimum_value=1,
            value_violation_action="error",
            warning_stack_level=warning_stack_level,
        )
        for multiple in multiples
    )
    if len(multiples) == 0:
        return 1

    least_common_multiplier = multiples[0]
    for element in multiples[1:]:
        least_common_multiplier = (least_common_multiplier * element) // math.gcd(
            least_common_multiplier,
            element,
        )

    return least_common_multiplier


def iterate_over_lengths_satisfying_constraints(
    length: int,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
    warning_stack_level: int = None,
) -> Generator[
    int,
    None,
    None,
]:
    """Iterates over all lengths that satisfy given constraints.

    Parameters
    ----------
    length : int
        The base length proposition.
    minimum_length : int
        The smallest allowed length. Defaults to no lower limit.
    maximum_length : int
        The largest allowed length. Defaults to no upper limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers length propositions should be a multiple of. Ignores length
        factorization by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Yields
    ------
    int
        Length proposal satisfying given constraints.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `length` isn't an int

    ValueError
        When any of the following applies:
        - `length` is smaller than 0

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `maximum_length` isn't None and isn't an int
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    length = amend_integer(
        length,
        type_mismatch_action="error",
        minimum_value=0,
        value_violation_action="error",
        warning_stack_level=warning_stack_level + 1,
    )
    minimum_length = amend_integer(
        minimum_length,
        value_on_cast_error=0,
        minimum_value=0,
        value_violation_action="clamp",
        warning_stack_level=warning_stack_level + 1,
    )
    if maximum_length is not None:
        maximum_length = amend_integer(
            maximum_length,
            type_mismatch_action="warning",
            minimum_value=0,
            value_violation_action="clamp",
            warning_stack_level=warning_stack_level + 1,
        )

    if length_is_multiple_of is None:
        differential = 1
    else:
        differential = find_least_common_multiplier(
            multiples=length_is_multiple_of,
            warning_stack_level=warning_stack_level + 1,
        )

    length_when_truncated = length - (length % differential)
    length_when_padded = length + differential - (length % differential)

    new_length_when_truncated = length_when_truncated
    new_length_when_padded = length_when_padded

    while (
        length_when_truncated >= minimum_length
        or maximum_length is None
        or length_when_padded <= maximum_length
    ):
        if length_when_truncated >= minimum_length:
            if maximum_length is None or length_when_truncated <= maximum_length:
                yield length_when_truncated - length
            new_length_when_truncated = length_when_truncated - differential

        if maximum_length is None or length_when_padded <= maximum_length:
            if length_when_padded >= minimum_length:
                yield length_when_padded - length
            new_length_when_padded = length_when_padded + differential

        if (
            new_length_when_truncated == length_when_truncated
            and new_length_when_padded == length_when_padded
        ):
            break

        length_when_truncated = new_length_when_truncated
        length_when_padded = new_length_when_padded
    return


def determine_length_normalization_strategy(
    length: int,
    minimum_length: int = None,
    maximum_length: int = None,
    length_is_multiple_of: Iterable[int] = None,
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
    warning_stack_level: int = None,
) -> Union[
    Tuple[int, int],
    None,
]:
    """Determines how many elements to truncate or pad on the left and/or on the right.

    Parameters
    ----------
    length : int
        The base length proposition.
    minimum_length : int
        The smallest allowed length. Defaults to no lower limit.
    maximum_length : int
        The largest allowed length. Defaults to no upper limit.
    length_is_multiple_of : Iterable[int]
        Natural numbers length propositions should be a multiple of. Ignores length
        factorization by default.
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
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Union[Tuple[int, int], None]
        A pair of integers showing how many elements on each side need to be added or
        removed, or None if there is no valid length normalization strategy for the
        given constraints.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `length` isn't an int

    ValueError
        When any of the following applies:
        - `length` is smaller than 0

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `maximum_length` isn't None and isn't an int
    """
    if truncation_side is not None and truncation_side not in (
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ):
        raise ValueError(f"Invalid truncation side {repr(truncation_side)}")
    if padding_side is not None and padding_side not in (
        "left",
        "right",
        "both-but-prioritize-left",
        "both-but-prioritize-right",
    ):
        raise ValueError(f"Invalid padding side {repr(padding_side)}")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    for proposed_length_change in iterate_over_lengths_satisfying_constraints(
        length=length,
        minimum_length=minimum_length,
        maximum_length=maximum_length,
        length_is_multiple_of=length_is_multiple_of,
        warning_stack_level=warning_stack_level + 1,
    ):
        if proposed_length_change == 0:
            return (
                0,
                0,
            )
        elif truncation_side is None and padding_side is None:
            return None

        side_to_look_at = (
            truncation_side if proposed_length_change < 0 else padding_side
        )
        if side_to_look_at is None:
            continue

        if side_to_look_at == "left":
            return (
                proposed_length_change,
                0,
            )
        elif side_to_look_at == "right":
            return (
                0,
                proposed_length_change,
            )
        elif (
            side_to_look_at == "both-but-prioritize-left" and proposed_length_change > 0
        ) or (
            side_to_look_at == "both-but-prioritize-right"
            and proposed_length_change < 0
        ):
            return (
                (proposed_length_change + 1) // 2,
                proposed_length_change // 2,
            )

        return (
            proposed_length_change // 2,
            (proposed_length_change + 1) // 2,
        )

    return None


def _normalize_length_of_data_sequence(
    data_sequence_type: Union[
        Type[bytearray],
        Type[bytes],
        Type[str],
    ],
    data_sequence: Union[
        bytearray,
        bytes,
        str,
    ],
    proposed_length_change: Tuple[
        int,
        int,
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
    """Normalizes length of a data sequence given contraints.

    Parameters
    ----------
    data_sequence_type : Union[Type[bytearray], Type[bytes], Type[str]]
        Type of the data sequence; either a bytearray, bytes or str.
    data_sequence : Union[bytearray, bytes, str]
        A data sequence; either an instance of a bytearray, bytes or str.
    proposed_length_change : Tuple[int, int]
        A pair of integers showing how many elements on each side should be added or
        removed.
    padding_value : Union[bytes, str]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with the
        null byte or ASCII underscore ('_').
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Union[bytearray, bytes, str]
        The data sequence with normalized length.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `data_sequence` isn't a `data_sequence_type`
        - `proposed_length_change` isn't a tuple
        - `padding_value` isn't None and isn't bytes when `data_sequence_type` is
        is bytearray or bytes, or str when `data_sequence_type` is str

    ValueError
        When any of the following applies:
        - `data_sequence_type` is not bytearray, bytes or str
        - `proposed_length_change` doesn't have length of 2
        - any element in `proposed_length_change` fails to be cast into int

    Warns
    -----
    UserWarning
        When any of the following applies:
        - any element in `proposed_length_change` isn't an int
    """
    if data_sequence_type not in (
        bytearray,
        bytes,
        str,
    ):
        raise ValueError(f"Invalid data sequence type {repr(data_sequence_type)}")
    if not isinstance(
        data_sequence,
        data_sequence_type,
    ):
        raise TypeError(f"Entity {repr(data_sequence)} isn't {data_sequence_type}")
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if proposed_length_change is None:
        proposed_length_change = (
            0,
            0,
        )
    elif not isinstance(
        proposed_length_change,
        tuple,
    ):
        raise TypeError(
            f"Proposed length change {repr(proposed_length_change)} isn't a tuple"
        )
    elif len(proposed_length_change) != 2:
        raise ValueError(
            f"Proposed length change has length {len(proposed_length_change)}, not 2"
        )
    else:
        proposed_length_change = tuple(
            amend_integer(
                integer=length_change,
                type_mismatch_action="warning",
                warning_stack_level=warning_stack_level + 1,
            )
            for length_change in proposed_length_change
        )
    if padding_value is None:
        if isinstance(
            data_sequence,
            (bytearray, bytes),
        ):
            padding_value = b"\0"
        else:
            padding_value = "_"
    elif isinstance(
        data_sequence,
        (bytearray, bytes),
    ):
        if not isinstance(
            padding_value,
            bytes,
        ):
            raise TypeError(f"Padding value {repr(padding_value)} isn't bytes")
    elif not isinstance(
        padding_value,
        data_sequence_type,
    ):
        raise TypeError(
            f"Padding value {repr(padding_value)} isn't {data_sequence_type}"
        )

    if data_sequence_type == bytearray:
        padding_value = bytearray(padding_value)

    (
        left_change,
        right_change,
    ) = proposed_length_change

    if left_change < 0:
        data_sequence = data_sequence[abs(left_change) :]
    elif left_change > 0:
        left_padding = (left_change + len(padding_value) - 1) // len(padding_value)
        left_padding = padding_value * left_padding
        left_padding = left_padding[:left_change]

        data_sequence = left_padding + data_sequence

    if right_change < 0:
        data_sequence = data_sequence[:right_change]
    elif right_change > 0:
        right_padding = (right_change + len(padding_value) - 1) // len(padding_value)
        right_padding = padding_value * right_padding
        right_padding = right_padding[:right_change]

        data_sequence = data_sequence + right_padding

    return data_sequence


def normalize_length_of_immutable_binary(
    immutable_binary: bytes,
    proposed_length_change: Tuple[
        int,
        int,
    ] = None,
    padding_value: bytes = None,
    warning_stack_level: int = None,
) -> bytes:
    """Normalizes length of an immutable binary given contraints.

    Parameters
    ----------
    immutable_binary : bytes
        An immutable binary; an instance of bytes.
    proposed_length_change : Tuple[int, int]
        A pair of integers showing how many elements on each side should be added or
        removed.
    padding_value : bytes
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with the
        null byte.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    bytes
        The immutable binary with normalized length.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `immutable_binary` isn't bytes
        - `proposed_length_change` isn't a tuple
        - `padding_value` isn't None and isn't bytes

    ValueError
        When any of the following applies:
        - `proposed_length_change` doesn't have length of 2
        - any element in `proposed_length_change` fails to be cast into int

    Warns
    -----
    UserWarning
        When any of the following applies:
        - any element in `proposed_length_change` isn't an int
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _normalize_length_of_data_sequence(
        data_sequence_type=bytes,
        data_sequence=immutable_binary,
        proposed_length_change=proposed_length_change,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def normalize_length_of_mutable_binary(
    mutable_binary: bytearray,
    proposed_length_change: Tuple[
        int,
        int,
    ] = None,
    padding_value: bytes = None,
    warning_stack_level: int = None,
) -> bytearray:
    """Normalizes length of a mutable binary given contraints.

    Parameters
    ----------
    mutable_binary : bytearray
        A mutable binary; an instance of bytearray.
    proposed_length_change : Tuple[int, int]
        A pair of integers showing how many elements on each side should be added or
        removed.
    padding_value : bytes
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with the
        null byte.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    bytearray
        The mutable binary with normalized length.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `mutable_binary` isn't a bytearray
        - `proposed_length_change` isn't a tuple
        - `padding_value` isn't None and isn't bytes

    ValueError
        When any of the following applies:
        - `proposed_length_change` doesn't have length of 2
        - any element in `proposed_length_change` fails to be cast into int

    Warns
    -----
    UserWarning
        When any of the following applies:
        - any element in `proposed_length_change` isn't an int
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _normalize_length_of_data_sequence(
        data_sequence_type=bytearray,
        data_sequence=mutable_binary,
        proposed_length_change=proposed_length_change,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def normalize_length_of_text(
    text: str,
    proposed_length_change: Tuple[
        int,
        int,
    ] = None,
    padding_value: str = None,
    warning_stack_level: int = None,
) -> str:
    """Normalizes length of text given contraints.

    Parameters
    ----------
    text : str
        Text; an instance of str.
    proposed_length_change : Tuple[int, int]
        A pair of integers showing how many elements on each side should be added or
        removed.
    padding_value : str
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with the
        ASCII underscore ('_').
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    str
        The text with normalized length.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `text` isn't a str
        - `proposed_length_change` isn't a tuple
        - `padding_value` isn't None and isn't a str

    ValueError
        When any of the following applies:
        - `proposed_length_change` doesn't have length of 2
        - any element in `proposed_length_change` fails to be cast into int

    Warns
    -----
    UserWarning
        When any of the following applies:
        - any element in `proposed_length_change` isn't an int
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return _normalize_length_of_data_sequence(
        data_sequence_type=str,
        data_sequence=text,
        proposed_length_change=proposed_length_change,
        padding_value=padding_value,
        warning_stack_level=warning_stack_level + 1,
    )


def _normalize_length_of_sequence_container(
    sequence_container_type: Union[
        Type[list],
        Type[tuple],
    ],
    sequence_container: Union[
        List[Any],
        Tuple[Any, ...],
    ],
    proposed_length_change: Tuple[
        int,
        int,
    ] = None,
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> Union[
    List[Any],
    Tuple[Any, ...],
]:
    """Normalizes length of a sequence container given contraints.

    Parameters
    ----------
    sequence_container_type: Union[Type[list], Type[tuple]]
        Type of the sequence container; either a list or tuple.
    sequence_container:
        A sequence container; either an instance of a list or tuple.
    proposed_length_change : Tuple[int, int]
        A pair of integers showing how many elements on each side should be added or
        removed.
    padding_value : Tuple[Any, ...]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with None.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    List[Any]
        The sequence container with normalized length as a list.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `sequence_container` isn't a `sequence_container_type`
        - `proposed_length_change` isn't a tuple
        - `padding_value` isn't None and isn't a tuple

    ValueError
        When any of the following applies:
        - `sequence_container_type` isn't a list or tuple
        - `proposed_length_change` doesn't have length of 2
        - any element in `proposed_length_change` fails to be cast into int

    Warns
    -----
    UserWarning
        When any of the following applies:
        - any element in `proposed_length_change` isn't an int
    """
    if sequence_container_type not in (
        list,
        tuple,
    ):
        raise ValueError(
            f"Invalid sequence container type {repr(sequence_container_type)}"
        )
    if not isinstance(
        sequence_container,
        sequence_container_type,
    ):
        raise TypeError(
            f"Entity {repr(sequence_container)} isn't {sequence_container_type}"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    if proposed_length_change is None:
        proposed_length_change = (
            0,
            0,
        )
    elif not isinstance(
        proposed_length_change,
        tuple,
    ):
        raise TypeError(
            f"Proposed length change {repr(proposed_length_change)} isn't a tuple"
        )
    elif len(proposed_length_change) != 2:
        raise ValueError(
            f"Proposed length change has length {len(proposed_length_change)}, not 2"
        )
    else:
        proposed_length_change = tuple(
            amend_integer(
                integer=length_change,
                type_mismatch_action="warning",
                warning_stack_level=warning_stack_level + 1,
            )
            for length_change in proposed_length_change
        )
    if padding_value is None:
        padding_value = [None]
    elif not isinstance(
        padding_value,
        tuple,
    ):
        raise TypeError(f"Padding value {repr(padding_value)} isn't a tuple")
    else:
        padding_value = list(padding_value)

    sequence_container = list(sequence_container)

    (
        left_change,
        right_change,
    ) = proposed_length_change

    if left_change < 0:
        sequence_container = sequence_container[abs(left_change) :]
    elif left_change > 0:
        left_padding = (left_change + len(padding_value) - 1) // len(padding_value)
        left_padding = padding_value * left_padding
        left_padding = left_padding[:left_change]

        sequence_container = left_padding + sequence_container

    if right_change < 0:
        sequence_container = sequence_container[:right_change]
    elif right_change > 0:
        right_padding = (right_change + len(padding_value) - 1) // len(padding_value)
        right_padding = padding_value * right_padding
        right_padding = right_padding[:right_change]

        sequence_container = sequence_container + right_padding

    return sequence_container


def normalize_length_of_immutable_sequence(
    immutable_sequence: Tuple[Any, ...],
    proposed_length_change: Tuple[
        int,
        int,
    ] = None,
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> Tuple[Any, ...]:
    """Normalizes length of an immutable sequence given contraints.

    Parameters
    ----------
    immutable_sequence:
        An immutable sequence; an instance of a tuple.
    proposed_length_change : Tuple[int, int]
        A pair of integers showing how many elements on each side should be added or
        removed.
    padding_value : Tuple[Any, ...]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with None.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Tuple[Any, ...]
        The immutable sequence with normalized length.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `immutable_sequence` isn't a tuple
        - `proposed_length_change` isn't a tuple
        - `padding_value` isn't None and isn't a tuple

    ValueError
        When any of the following applies:
        - `proposed_length_change` doesn't have length of 2
        - any element in `proposed_length_change` fails to be cast into int

    Warns
    -----
    UserWarning
        When any of the following applies:
        - any element in `proposed_length_change` isn't an int
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return tuple(
        _normalize_length_of_sequence_container(
            sequence_container_type=tuple,
            sequence_container=immutable_sequence,
            proposed_length_change=proposed_length_change,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )
    )


def normalize_length_of_mutable_sequence(
    mutable_sequence: List[Any],
    proposed_length_change: Tuple[
        int,
        int,
    ] = None,
    padding_value: Tuple[Any, ...] = None,
    warning_stack_level: int = None,
) -> List[Any]:
    """Normalizes length of a mutable sequence given contraints.

    Parameters
    ----------
    mutable_sequence:
        A mutable sequence; an instance of a list.
    proposed_length_change : Tuple[int, int]
        A pair of integers showing how many elements on each side should be added or
        removed.
    padding_value : Tuple[Any, ...]
        Value with which to pad. If value is shorter than the amount to pad it will be
        automatically repeated to fit the necessary length. By default, pad with None.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    List[Any]
        The mutable sequence with normalized length.

    Raises
    ------
    TypeError
        When any of the following applies:
        - `mutable_sequence` isn't a list
        - `proposed_length_change` isn't a tuple
        - `padding_value` isn't None and isn't a tuple

    ValueError
        When any of the following applies:
        - `proposed_length_change` doesn't have length of 2
        - any element in `proposed_length_change` fails to be cast into int

    Warns
    -----
    UserWarning
        When any of the following applies:
        - any element in `proposed_length_change` isn't an int
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    return list(
        _normalize_length_of_sequence_container(
            sequence_container_type=list,
            sequence_container=mutable_sequence,
            proposed_length_change=proposed_length_change,
            padding_value=padding_value,
            warning_stack_level=warning_stack_level + 1,
        )
    )


def get_immutable_mapping(
    mapping,
    warning_stack_level: int = None,
) -> Tuple[
    Tuple[
        Any,
        Any,
    ],
    ...,
]:
    """Gets an immutable mapping from a mapping.

    Parameters
    ----------
    mapping
        Something that should in essence be a mapping.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    Tuple[Tuple[Any, Any], ...]
        The immutable mapping.

    Raises
    ------
    TypeError
        When any of the following applies
        - `dict(data_mapping)` throws an Exception
    """
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )
    mapping = amend_mutable_data_mapping(
        mutable_data_mapping=mapping,
        warning_stack_level=3,
    )

    mapping = mapping.items()
    mapping = (tuple(pair) for pair in mapping)
    mapping = tuple(mapping)

    return mapping
