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

from pathlib import Path
from typing import Literal
import warnings

from amend.built_in.numbers.integers import amend_integer


def amend_directory(
    directory,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Path = None,
    not_existing_action: Literal[
        "error",
        "warning",
        "make",
    ] = None,
    category_mismatch_action: Literal[
        "error",
        "warning",
        "take-parent",
    ] = None,
    warning_stack_level: int = None,
) -> Path:
    """Amend a directory.

    Parameters
    ----------
    directory
        Something that should in essence be a directory.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `directory` isn't a pathlib.Path. If 'error', raises a
        TypeError. If 'warning', raises a UserWarning. Ignores type mismatches by
        default.
    value_on_cast_error : Path
        Value to set `directory` to if `directory` is None, if `str(directory)` throws an Exception or `pathlib.Path(directory)` throws an Exception. By default,
        raises a TypeError.
    not_existing_action : Literal['error', 'warning', 'make']
        What to do if `directory` doesn't exist. If 'error', raises an OSError. If
        'warning', raises a UserWarning. If 'make', creates the directory alongside all
        of its parents that don't exist. Ignores if `directory` doesn't exist by
        default.
    category_mismatch_action : Literal['error', 'warning', 'take-parent']
        What to do if `directory` isn't an actual directory. If 'error', raises
        NotADirectoryError. If 'warning', raises UserWarning. If 'take-parent', sets
        `directory` to its parent. Ignores if `directory` is something else by default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    pathlib.Path
        The amended directory.

    Raises
    ------
    NotADirectoryError
        When any of the following applies:
        - `directory` exists but isn't a directory and `category_mismatch_action` is
        'error'

    OSError
        When any of the following applies:
        - `directory` doesn't exist and `not_existing_action` is 'error'
        - `directory` doesn't exist, `not_existing_action` is 'make' and directory
        creation fails
        - `directory` isn't an actual directory, `category_mismatch_action` is
        'take-parent', but the parent of `directory` is also not a directory (I don't
        know why this would happen, actually, but I'm no expert)

    TypeError
        When any of the following applies:
        - `directory` isn't a pathlib.Path and `type_mismatch_action` is 'error'
        - `directory` is None, `str(directory)` throws an Exception or
        `pathlib.Path(directory)` throws an Exception and `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None or a pathlib.Path
        - `not_existing_action` isn't None, 'error', 'warning' or 'make'
        - `category_mismatch_action` isn't None, 'error', 'warning' or 'take-parent'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `directory` isn't a pathlib.Path and `type_mismatch_action` is 'warning'
        - `directory` doesn't exist and `not_existing_action` is 'warning'
        - `directory` isn't an actual directory and `category_mismatch_action` is
        'warning'
    """
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
                Path,
            )
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not_existing_action not in (
        None,
        "error",
        "warning",
        "make",
    ):
        raise ValueError(f"Invalid not-existing action {repr(not_existing_action)}")

    if category_mismatch_action not in (
        None,
        "error",
        "warning",
        "take-parent",
    ):
        raise ValueError(
            f"Invalid category mismatch action {repr(category_mismatch_action)}"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    if not isinstance(
        directory,
        Path,
    ):
        if type_mismatch_action is not None:
            message = f"Entity {repr(directory)} isn't a pathlib.Path"
            if type_mismatch_action == "error":
                raise TypeError(message)
            elif type_mismatch_action == "warning":
                warnings.warn(
                    message,
                    UserWarning,
                    warning_stack_level,
                )
        try:
            assert directory is not None
            directory = str(directory)
            directory = Path(directory)
        except Exception:
            if value_on_cast_error is None:
                raise TypeError(f"Failed to cast {repr(directory)} to pathlib.Path")

            directory = value_on_cast_error

    if not_existing_action is not None and not directory.exists():
        message = f"Directory {directory} is missing"
        if not_existing_action == "error":
            raise OSError(message)
        elif not_existing_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif not_existing_action == "make":
            try:
                directory.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                assert directory.exists()
            except Exception as e:
                raise OSError(f"Failed to make directory {directory}:\n{e}")

    if (
        category_mismatch_action is not None
        and directory.exists()
        and not directory.is_dir()
    ):
        message = f"Path {directory} isn't a directory"
        if category_mismatch_action == "error":
            raise NotADirectoryError(message)
        elif category_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif category_mismatch_action == "take-parent":
            try:
                proposed_directory = directory.parent
                assert proposed_directory.is_dir()
                directory = proposed_directory
            except Exception:
                raise OSError(
                    f"Path {directory}'s parent {proposed_directory} isn't a directory"
                )

    return directory


def amend_file(
    file,
    type_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    value_on_cast_error: Path = None,
    not_existing_action: Literal[
        "error",
        "warning",
        "make",
        "make-parent",
    ] = None,
    category_mismatch_action: Literal[
        "error",
        "warning",
    ] = None,
    warning_stack_level: int = None,
) -> Path:
    """Amend a file.

    Parameters
    ----------
    file
        Something that should in essence be a file.
    type_mismatch_action : Literal['error', 'warning']
        What to do if `file` isn't a pathlib.Path. If 'error', raises a TypeError. If
        'warning', raises a UserWarning. Ignores type mismatches by default.
    value_on_cast_error : Path
        Value to set `file` to if `file` is None, if `str(file)` throws an Exception or `pathlib.Path(file)` throws an Exception. By default, raises a TypeError.
    not_existing_action : Literal['error', 'warning', 'make', 'make-parent']
        What to do if `file` doesn't exist. If 'error', raises a OSError. If
        'warning', raises a UserWarning. If 'make', amends its parent and creates it alongside its missing parents if missing and creates an empty file. If
        'make-parent', amends its parent and creates it alongside its missing parents if missing. Ignores if `file` doesn't exist by default.
    category_mismatch_action : Literal['error', 'warning']
        What to do if `file` isn't an actual file. If 'error', raises ValueError. If
        'warning', raises UserWarning. Ignores if `directory` is something else by
        default.
    warning_stack_level : int
        Stack level which to report for warnings. Defaults to 2 (whatever called this).

    Returns
    -------
    pathlib.Path
        The amended file.

    Raises
    ------
    OSError
        When any of the following applies:
        - `file` doesn't exist and `not_existing_action` is 'error'
        - `file` doesn't exist, `not_existing_action` is 'make' and file creation fails

    TypeError
        When any of the following applies:
        - `file` isn't a pathlib.Path and `type_mismatch_action` is 'error'
        - `file` is None, `str(file)` throws an Exception or `pathlib.Path(file)`
        throws an Exception and `value_on_cast_error` is None

    ValueError
        When any of the following applies:
        - `type_mismatch_action` is not None, 'error' or 'warning'
        - `value_on_cast_error` isn't None or a pathlib.Path
        - `not_existing_action` isn't None, 'error', 'warning', 'make', or 'make-parent'
        - `category_mismatch_action` isn't None, 'error', or 'warning'
        - `file` exists but isn't a file and `category_mismatch_action` is 'error'

    Warns
    -----
    UserWarning
        When any of the following applies:
        - `directory` isn't a pathlib.Path and `type_mismatch_action` is 'warning'
        - `directory` doesn't exist and `not_existing_action` is 'warning'
        - `directory` isn't an actual directory and `category_mismatch_action` is
        'warning'
    """
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
                Path,
            )
            and (value_on_cast_error.is_file() or not value_on_cast_error.exists())
        )
    ):
        raise ValueError(f"Invalid value on cast error {repr(value_on_cast_error)}")
    if not_existing_action not in (
        None,
        "error",
        "warning",
        "make",
        "make-parent",
    ):
        raise ValueError(f"Invalid not-existing action {repr(not_existing_action)}")
    if category_mismatch_action not in (
        None,
        "error",
        "warning",
    ):
        raise ValueError(
            f"Invalid category mismatch action {repr(category_mismatch_action)}"
        )
    warning_stack_level = amend_integer(
        integer=warning_stack_level,
        value_on_cast_error=2,
        minimum_value=2,
        value_violation_action="clamp",
        warning_stack_level=3,
    )

    if (
        not isinstance(
            file,
            Path,
        )
        and type_mismatch_action is not None
    ):
        message = f"Entity {repr(file)} isn't a pathlib.Path"
        if type_mismatch_action == "error":
            raise TypeError(message)
        elif type_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )

    try:
        assert file is not None
        file = str(file)
        file = Path(file)
    except Exception:
        if value_on_cast_error is None:
            raise TypeError(f"Failed to cast {repr(file)} to pathlib.Path")

        file = value_on_cast_error

    if not_existing_action is not None and not file.exists():
        message = f"File {file} is missing"
        if not_existing_action == "error":
            raise OSError(message)
        elif not_existing_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )
        elif not_existing_action in (
            "make",
            "make-parent",
        ):
            amend_directory(
                directory=file.parent,
                not_existing_action="make",
                warning_stack_level=warning_stack_level + 1,
            )

            if not_existing_action == "make":
                try:
                    with open(
                        file,
                        mode="a",
                    ):
                        pass
                    assert file.exists()
                except Exception as e:
                    raise OSError(f"Failed to make file {file}:\n{e}")

    if category_mismatch_action is not None and file.exists() and not file.is_file():
        message = f"Path {file} isn't a file"
        if category_mismatch_action == "error":
            raise ValueError(message)
        elif category_mismatch_action == "warning":
            warnings.warn(
                message,
                UserWarning,
                warning_stack_level,
            )

    return file
