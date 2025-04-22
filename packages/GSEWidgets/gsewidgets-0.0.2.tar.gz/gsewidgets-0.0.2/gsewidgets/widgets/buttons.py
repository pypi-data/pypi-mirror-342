#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: buttons.py
# Description: Implementation of various button widgets.
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

from pathlib import Path
from qtpy.QtCore import QSize, QObject, Signal
from qtpy.QtGui import QIcon, QColor
from qtpy.QtWidgets import QPushButton, QFileDialog, QColorDialog
from typing import Optional

__all__ = [
    "SimpleButton",
    "FlatButton",
    "FileBrowserButton",
    "DirectoryBrowserButton",
    "ColorDialogButton",
]


class SimpleButton(QPushButton):
    """Used to create instances of simple buttons"""

    def __init__(
        self,
        text: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "flat-button",
        icon: Optional[QIcon] = None,
    ) -> None:
        super(SimpleButton, self).__init__()

        self._text = text
        self._size = size
        self._object_name = object_name
        self._icon = icon

        # Run configuration method
        self._configure_flat_button()

    def _configure_flat_button(self) -> None:
        """Basic configuration for the simple button."""
        # Add text
        if self._text is not None:
            self.setText(self._text)

        # Set the object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Set size
        if self._size is not None:
            self.setFixedSize(self._size)

        # Set icon
        if self._icon is not None:
            self.setIcon(self._icon)

        # Connect click event
        self.clicked.connect(self._button_click_event)

    def _button_click_event(self) -> None:
        """Clears the focus state of the button."""
        self.clearFocus()


class FlatButton(SimpleButton):
    """Used to create instances of simple flat buttons"""

    def __init__(
        self,
        text: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "flat-button",
        icon: Optional[QIcon] = None,
    ) -> None:
        super(FlatButton, self).__init__(
            text=text, icon=icon, size=size, object_name=object_name
        )

        # Run configuration method
        self._configure_flat_button()

    def _configure_flat_button(self) -> None:
        """Basic configuration for the flat button."""
        # Set flat
        self.setFlat(True)


class AbstractBrowserButton(SimpleButton):
    """Abstract button class to used for buttons that open QFileDialog widgets."""

    def __init__(
        self,
        text: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "flat-button",
        icon: Optional[QIcon] = None,
        caption: Optional[str] = "Select File",
        invalid_characters: Optional[str] = '<>"\\|?*#& ',
    ) -> None:
        super(AbstractBrowserButton, self).__init__(
            text=text,
            size=size,
            object_name=object_name,
            icon=icon,
        )

        self._caption = caption
        self._invalid_characters = invalid_characters

        # Set the initial target directory
        self._target_directory = str(Path.home())

    @property
    def caption(self) -> str:
        return self._caption

    @property
    def target_directory(self) -> str:
        return self._target_directory

    @target_directory.setter
    def target_directory(self, value: str) -> None:
        # Check invalid characters
        if self._invalid_characters is None:
            self._invalid_characters = '<>"\\|?*#& '
        # Validate based on invalid characters
        for char in self._invalid_characters:
            value = value.replace(char, "_")
        # Set the target directory
        self._target_directory = value


class FileBrowserButton(AbstractBrowserButton, QObject):
    """Used to create instances of flat button that open a QFileDialog to select a file."""

    file_path_changed: Signal = Signal(bool)

    def __init__(
        self,
        text: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "flat-button",
        icon: Optional[QIcon] = None,
        caption: Optional[str] = "Select File",
        invalid_characters: Optional[str] = '<>"\\|?*#& ',
        file_extensions: Optional[list[str]] = None,
    ) -> None:
        super(FileBrowserButton, self).__init__(
            text=text,
            size=size,
            object_name=object_name,
            icon=icon,
            caption=caption,
            invalid_characters=invalid_characters,
        )

        self._file_extensions = file_extensions

        self._file_path: str = ""
        self._filter: str = ""

        # Configure the file filter string
        self._configure_file_filter()

    def _configure_file_filter(self) -> None:
        """Sets the value of the filter string for the accepted files."""
        if self._file_extensions is None:
            # Keep filter open to all files
            self._filter = "All files (*)"
        else:
            for extension in self._file_extensions:
                # Make sure that the extension starts with *.
                if not extension.startswith("*."):
                    extension = f"*.{extension}"
                # Add extensions to the filter string
                self._filter += f" {extension}"

            # Remove first character
            self._filter = self._filter[1:]

    def _button_click_event(self) -> None:
        """Uses QFileDialog to get the selected file path, and emits a file_path_changed signal."""
        # Clears the focus state of the button
        self.clearFocus()
        # Create the QFileDialog widget
        dialog = QFileDialog()
        # Set the file mode
        dialog.setFileMode(QFileDialog.ExistingFile)
        # Get the new path for the file
        new_file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption=self.caption,
            directory=self.target_directory,
            filter=self._filter,
        )

        # Update the file path and emit the file_path_changed signal
        if new_file_path != "":
            self._file_path = Path(new_file_path).as_posix()
            self.file_path_changed.emit(True)

    @property
    def file_path(self) -> str:
        return self._file_path


class DirectoryBrowserButton(AbstractBrowserButton, QObject):
    """Used to create instances of flat button that open a QFileDialog to select a directory."""

    directory_changed: Signal = Signal(bool)

    def __init__(
        self,
        text: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "flat-button",
        icon: Optional[QIcon] = None,
        caption: Optional[str] = "Select File",
        invalid_characters: Optional[str] = '<>"\\|?*#& ',
    ) -> None:
        super(DirectoryBrowserButton, self).__init__(
            text=text,
            size=size,
            object_name=object_name,
            icon=icon,
            caption=caption,
            invalid_characters=invalid_characters,
        )

        self._directory = ""

    def _button_click_event(self) -> None:
        """Uses QFileDialog to get the selected directory, and emits a directory_changed signal."""
        # Clears the focus state of the button
        self.clearFocus()
        # Open file dialog and get the directory
        new_directory = QFileDialog.getExistingDirectory(
            parent=self, caption=self.caption, directory=self.target_directory
        )
        # Update the directory path and emit the directory_changed signal
        if new_directory != "":
            self._directory = Path(new_directory).as_posix()
            self.directory_changed.emit(True)

    @property
    def directory(self) -> str:
        return self._directory


class MultiFileBrowserButton(FileBrowserButton):
    """Used to create instances of flat button that open a QFileDialog to select multiple files."""

    def __init__(self, text = None, size = None, object_name = "flat-button", icon = None, caption = "Select File", invalid_characters = '<>"\|?*#& ', file_extensions = None):
        super(MultiFileBrowserButton, self).__init__(text, size, object_name, icon, caption, invalid_characters, file_extensions)

    def _button_click_event(self) -> None:
        """Uses QFileDialog to get the selected file paths, and emits a file_path_changed signal."""
        # Clears the focus state of the button
        self.clearFocus()
        # Create the QFileDialog widget
        dialog = QFileDialog()
        # Set the file mode
        dialog.setFileMode(QFileDialog.ExistingFiles)
        # Get the new path for the files
        new_file_paths, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption=self.caption,
            directory=self.target_directory,
            filter=self._filter,
        )

        # Update the file paths and emit the file_path_changed signal
        if new_file_paths != "":
            self._file_path = [Path(file_path).as_posix() for file_path in new_file_paths]
            self.file_path_changed.emit(True)

class ColorDialogButton(FlatButton, QObject):
    """
    Used to create instances of flat button that open a QColorDialog to select a color.
    The background color of the button will change to reflect the selected color.
    """

    color_changed: Signal = Signal(bool)

    def __init__(
        self,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "color-button",
        default_color: Optional[QColor] = None,
    ) -> None:
        super(ColorDialogButton, self).__init__(
            text=None, size=size, object_name=object_name, icon=None
        )

        self._color = default_color

        # Set the QColorDialog
        self._color_dialog = QColorDialog()
        # Run the color button configuration method
        self._configure_color_button()

    def _configure_color_button(self) -> None:
        # Enable alpha channel
        self._color_dialog.setOption(QColorDialog.ShowAlphaChannel)

        # Set the color
        if self._color is not None:
            self._color_dialog.setCurrentColor(self._color)
        else:
            self._color = self._color_dialog.currentColor()

        # Temporary disable flat
        self.setFlat(False)

        # Set the background color of the button
        self.setStyleSheet(f"background-color: {self.color.name()};")

        # Connect color selected event
        self._color_dialog.colorSelected.connect(self._color_selection_changed)

    def _button_click_event(self) -> None:
        # Clears the focus state of the button.
        self.clearFocus()
        # Open the color dialog window
        self._color_dialog.showNormal()
        # Bring the color dialog window in front of all windows
        self._color_dialog.activateWindow()

    def _color_selection_changed(self) -> None:
        # Get color selection
        new_color = self._color_dialog.currentColor()
        # Update the color value, change the background color of the button and
        # emit the color_changed signal
        if self._color != new_color:
            # Update color
            self._color = new_color
            # Change background color
            self.setStyleSheet(f"background-color: {self.color.name()};")
            # Emit the color_changed signal
            self.color_changed.emit(True)

    @property
    def color(self) -> QColor:
        return self._color
