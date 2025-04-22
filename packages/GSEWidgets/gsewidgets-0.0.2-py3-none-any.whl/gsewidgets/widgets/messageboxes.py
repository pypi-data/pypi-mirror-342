#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: messageboxes.py
# Description: Implementation of various message box widgets.
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

from qtpy.QtWidgets import QMessageBox
from typing import Optional

__all__ = ["ErrorMessageBox"]


class ErrorMessageBox(QMessageBox):
    """Generic QMessageBox for creating custom error message boxes."""

    def __init__(self, message: str, title: Optional[str] = None) -> None:
        super(ErrorMessageBox, self).__init__()

        # Check the error title
        if title is None:
            title = "Error"

        # Set the critical message box values
        self.critical(self, title, message, QMessageBox.Ok)
