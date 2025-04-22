#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: comboboxes.py
# Description: Implementation of various combobox widgets.
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
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QComboBox
from typing import Optional

__all__ = ["FullComboBox"]


class FullComboBox(QComboBox):
    """Used to create instanced of combo boxes that open the popup menu by click anywhere on the widget."""

    def __init__(
        self, size: Optional[QSize] = None, object_name: Optional[str] = "full-combobox"
    ) -> None:
        super(FullComboBox, self).__init__()

        self._size = size
        self._object_name = object_name

        self._configure_full_combobox()

    def _configure_full_combobox(self) -> None:
        """Basic configuration for the full combobox."""
        # Set the size
        if self._size is not None:
            self.setFixedSize(self._size)
        # Set object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Shows the popup using mouse clicks."""
        self.showPopup()
