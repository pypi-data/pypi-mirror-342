#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: labels.py
# Description: Implementation of various label widgets.
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

from qtpy.QtCore import QSize
from qtpy.QtWidgets import QLabel
from typing import Optional

__all__ = ["Label", "StatusLabel"]


class Label(QLabel):
    """Used to create instances of simple labels."""

    def __init__(
        self,
        text: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "label",
    ) -> None:
        super(Label, self).__init__()

        self._text = text
        self._size = size
        self._object_name = object_name

        # Run label configuration method
        self._configure_label()

    def _configure_label(self) -> None:
        """Basic configuration for the label."""
        # Set the text
        if self._text is not None:
            self.setText(self._text)
        # Set the size
        if self._size is not None:
            self.setFixedSize(self._size)
        # Set the object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)


class StatusLabel(Label):
    """Used to create instances of status labels, that provide enabled/disabled status."""

    def __init__(
        self,
        text: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "label-status",
        on_status: Optional[str] = "On",
        off_status: Optional[str] = "Off",
    ) -> None:
        super(StatusLabel, self).__init__(text=text, size=size, object_name=object_name)

        # Current status helper
        self._status = False
        self._on_status = on_status
        self._off_status = off_status

    def update_status(self, status: bool) -> None:
        """Updates the status of the status label."""
        self.status = status

    @property
    def status(self) -> bool:
        """Returns the current status that is set for the status label."""
        return self._status

    @status.setter
    def status(self, value: bool) -> None:
        """Sets the status of the status label."""
        self._status = value
        self.setText(self._on_status if self._status else self._off_status)
