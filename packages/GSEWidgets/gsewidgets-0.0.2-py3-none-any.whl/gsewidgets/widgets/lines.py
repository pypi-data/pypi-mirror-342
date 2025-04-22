#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: lines.py
# Description: Implementation of vertical and horizontal line widgets.
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

from qtpy.QtWidgets import QFrame
from typing import Optional

__all__ = ["VerticalLine", "HorizontalLine"]


class Line(QFrame):
    def __init__(self, object_name: Optional[str] = None) -> None:
        super(Line, self).__init__()

        # Set the object name
        if object_name is not None:
            self.setObjectName(object_name)


class VerticalLine(Line):
    """Used to create vertical lines."""

    def __init__(self, object_name: Optional[str] = "vertical-line") -> None:
        super(VerticalLine, self).__init__(object_name=object_name)

        # Set vertical orientation
        self.setFrameShape(QFrame.Shape.VLine)


class HorizontalLine(Line):
    """Used to create horizontal lines."""

    def __init__(self, object_name: Optional[str] = "horizontal-line") -> None:
        super(HorizontalLine, self).__init__(object_name=object_name)

        # Set horizontal orientation
        self.setFrameShape(QFrame.Shape.HLine)
