#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: inputboxes.py
# Description: Implementation of various input box widgets.
#
# License: GNU General Public License v3.0
# ------------------------------------------------------------------------------
# GSEWidgets - Collection of gui widgets to be used in GSE software.
# Author: Christofanis Skordas (skordasc@uchicago.edu)
# Copyright (C) 2022-2025 GSECARS, The University of Chicago
# Copyright (C) 2024-2025 NSF SEES, Synchrotron Earth and Environmental Science
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

from qtpy.QtCore import QSize, Qt, QRegularExpression
from qtpy.QtGui import QRegularExpressionValidator
from qtpy.QtWidgets import QLineEdit, QTextEdit
from typing import Optional

from gsewidgets.widgets.filters import (
    FileNameEventFilter,
    FilePathEventFilter,
    URIParseEventFilter,
    IPv4EventFilter,
    MultiFloatEventFilter,
)

__all__ = [
    "InputBox",
    "FileNameInputBox",
    "FilePathInputBox",
    "URIInputBox",
    "IPv4InputBox",
    "MultiFloatInputBox",
    "TextInfoBox",
]


class InputBox(QLineEdit):
    """Used to create instances of simple input boxes."""

    def __init__(
        self,
        placeholder: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "input-box",
    ) -> None:
        super(InputBox, self).__init__()

        self._placeholder = placeholder
        self._size = size
        self._object_name = object_name

        # Run configuration method
        self._configure_input_box()

    def _configure_input_box(self) -> None:
        """Basic configuration of the simple input box."""
        # Set placeholder text
        if self._placeholder is not None:
            self.setPlaceholderText(self._placeholder)

        # Set size
        if self._size is not None:
            self.setFixedSize(self._size)

        # Set object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Center align
        self.setAlignment(Qt.AlignCenter)

        # Connect the return pressed event
        self.returnPressed.connect(self._return_pressed_event)

    def _return_pressed_event(self) -> None:
        """Clears the focus state."""
        self.clearFocus()


class FileNameInputBox(InputBox):
    """Creates an input box that validates its input for file names."""

    def __init__(
        self,
        placeholder: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "filename-input-box",
        invalid_characters: Optional[str] = '<>"/\\|?*#&$: ',
    ):
        super(FileNameInputBox, self).__init__(
            placeholder=placeholder,
            size=size,
            object_name=object_name,
        )

        # Set the file name event filter
        self._file_name_filter = FileNameEventFilter(
            invalid_characters=invalid_characters
        )
        self.installEventFilter(self._file_name_filter)


class FilePathInputBox(InputBox):
    """Creates a file path input box with a path validation. The path will be created if it doesn't exist."""

    def __init__(
        self,
        placeholder: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "filepath-input-box",
        invalid_characters: Optional[str] = '<>"|?*#&$: ',
    ):
        super(FilePathInputBox, self).__init__(
            placeholder=placeholder,
            size=size,
            object_name=object_name,
        )

        # Set the file path event filter
        self._file_path_filter = FilePathEventFilter(
            invalid_characters=invalid_characters
        )
        self.installEventFilter(self._file_path_filter)


class URIInputBox(InputBox):
    """
    Creates a URI input box with https/http validation. The text will be removed if the
    correct scheme is not followed.
    """

    def __init__(
        self,
        placeholder: Optional[str] = "URI",
        size: Optional[QSize] = None,
        object_name: Optional[str] = "uri-input-box",
        validate_uri: Optional[bool] = True,
    ) -> None:
        super(URIInputBox, self).__init__(
            placeholder=placeholder,
            size=size,
            object_name=object_name,
        )

        if validate_uri:
            # Set the URI event filter
            self._uri_filter = URIParseEventFilter()
            self.installEventFilter(self._uri_filter)


class IPv4InputBox(InputBox):
    """
    Creates an IPv4 input box with validation. The text will not be changed if the
    correct scheme is not followed.
    """

    def __init__(
        self,
        placeholder: Optional[str] = "e.g. 127.0.0.1",
        size: Optional[QSize] = None,
        object_name: Optional[str] = "ipv4-input-box",
    ) -> None:
        super().__init__(placeholder=placeholder, size=size, object_name=object_name)

        # Set up a regular expression validator
        expression = QRegularExpression("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        validator = QRegularExpressionValidator(expression, self)
        self.setValidator(validator)

        # Set the IPv4 event filter
        self._ipv4_filter = IPv4EventFilter()
        self.installEventFilter(self._ipv4_filter)


class MultiFloatInputBox(InputBox):
    """
    Creates an input box that validates its input for single or multiple comma separated floats.
    """

    def __init__(
        self,
        placeholder: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "multi-float-input-box",
    ) -> None:
        super(MultiFloatInputBox, self).__init__(
            placeholder=placeholder,
            size=size,
            object_name=object_name,
        )

        # Set up a regular expression validator
        expression = QRegularExpression(
            "^((?:0|[1-9][0-9]*)(?:\.[0-9]*)?(?:,\s*(?:0|[1-9][0-9]*)(?:\.[0-9]*)?)*)$"
        )
        validator = QRegularExpressionValidator(expression, self)
        self.setValidator(validator)

        # Set the multi float event filter
        self._multi_float_filter = MultiFloatEventFilter()
        self.installEventFilter(self._multi_float_filter)


class TextInfoBox(QTextEdit):
    """Used to display information in a text box."""

    def __init__(
        self,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "text-info-box",
    ) -> None:
        super(TextInfoBox, self).__init__()

        self._size = size
        self._object_name = object_name

        # Run configuration method
        self._configure_text_info_box()

    def _configure_text_info_box(self) -> None:
        """Basic configuration of the text info box."""
        # Set size
        if self._size is not None:
            self.setFixedSize(self._size)

        # Set object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Set read only
        self.setReadOnly(True)

        # Set word wrap mode
          

        # Disable focus
        self.setFocusPolicy(Qt.NoFocus)
