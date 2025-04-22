#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: main_widget.py
# Description: Main widget for the GSEWidgets example application.
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

from qtpy.QtWidgets import QMainWindow

from gsewidgets.examples.widget import ExampleWidget
from gsewidgets.examples.model import PathModel


class MainWidget(QMainWindow):
    def __init__(self, model: PathModel) -> None:
        """Initialize the main window."""
        super(MainWidget, self).__init__()

        # Set the central widget
        self.example_widget = ExampleWidget(model=model)
        self.setCentralWidget(self.example_widget)

    def display_window(self, version: str) -> None:
        """Set the title of the main window and display to screen."""
        # Set window title based on current version
        self.setWindowTitle(f"GSEWidgets {version}")
        # Display the window
        self.showNormal()
