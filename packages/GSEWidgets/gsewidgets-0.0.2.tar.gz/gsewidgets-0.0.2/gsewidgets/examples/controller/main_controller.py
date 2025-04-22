#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: main_controller.py
# Description: Main controller for the GSEWidgets example application.
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

import sys
from qtpy.QtWidgets import QApplication
from random import randrange
from typing import Optional

from gsewidgets import ErrorMessageBox, NumericDataSpinBoxModel
from gsewidgets.examples.widget import MainWidget
from gsewidgets.examples.model import PathModel


class MainController:
    def __init__(self) -> None:
        """Initialize the main controller."""
        self._app = QApplication(sys.argv)
        self._model = PathModel()
        self._widget = MainWidget(model=self._model)

        self._connect_widgets()

    def _connect_widgets(self) -> None:
        self._widget.example_widget.btn_flat.clicked.connect(
            self._trigger_error_message
        )
        self._widget.example_widget.btn_file_browser.file_path_changed.connect(
            self._update_filepath_label
        )
        self._widget.example_widget.btn_directory_browser.directory_changed.connect(
            self._update_directory_label
        )
        self._widget.example_widget.btn_color_dialog.color_changed.connect(
            self._update_color_label
        )
        self._widget.example_widget.btn_add.clicked.connect(self._btn_add_clicked)
        self._widget.example_widget.btn_delete.clicked.connect(
            self._widget.example_widget.xyz_table.delete_selection
        )
        self._widget.example_widget.btn_clear.clicked.connect(
            self._widget.example_widget.xyz_table.clear_table
        )
        self._widget.example_widget.btn_check_all.clicked.connect(
            self._widget.example_widget.xyz_table.enable_all_points
        )
        self._widget.example_widget.btn_uncheck_all.clicked.connect(
            self._widget.example_widget.xyz_table.disable_all_points
        )

    @staticmethod
    def _trigger_error_message() -> None:
        """Opens an error message window."""
        ErrorMessageBox(
            message="This is an example error message.", title="Example Error"
        )

    def _update_filepath_label(self) -> None:
        """Updates the file path label text."""
        self._widget.example_widget.lbl_selected_file.setText(
            f"Selected file: {self._widget.example_widget.btn_file_browser.file_path}"
        )

    def _update_directory_label(self) -> None:
        """Updates the directory label text."""
        self._widget.example_widget.lbl_selected_directory.setText(
            f"Selected directory: {self._widget.example_widget.btn_directory_browser.directory}"
        )

    def _update_color_label(self) -> None:
        """Updates the selected color label text."""
        self._widget.example_widget.lbl_selected_color.setText(
            f"Selected color: RGBA {self._widget.example_widget.btn_color_dialog.color.getRgb()}, "
            f"HEX ({self._widget.example_widget.btn_color_dialog.color.name()})"
        )

    def _btn_add_clicked(self) -> None:
        randon_point_x = NumericDataSpinBoxModel(
            min_value=-100,
            max_value=100,
            current_value=randrange(-100, 100),
            incremental_step=1,
        )
        randon_point_y = NumericDataSpinBoxModel(
            min_value=-100,
            max_value=100,
            current_value=randrange(-100, 100),
            incremental_step=1,
        )
        randon_point_z = NumericDataSpinBoxModel(
            min_value=-100,
            max_value=100,
            current_value=randrange(-100, 100),
            incremental_step=1,
        )
        self._widget.example_widget.xyz_table.add_point(
            randon_point_x, randon_point_y, randon_point_z
        )

    def run(self, version: Optional[str] = "") -> None:
        self._widget.display_window(version=version)
        sys.exit(self._app.exec())
