#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: example_widget.py
# Description: Example widget for the GSEWidgets example application.
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

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QFrame, QVBoxLayout, QGridLayout

from gsewidgets.examples.model import PathModel
from gsewidgets import (
    VerticalLine,
    HorizontalLine,
    Label,
    NumericSpinBox,
    NoWheelNumericSpinBox,
    FlatButton,
    FileBrowserButton,
    DirectoryBrowserButton,
    ColorDialogButton,
    FullComboBox,
    InputBox,
    FilePathInputBox,
    FileNameInputBox,
    URIInputBox,
    CheckBox,
    ToggleCheckBox,
    XYZCollectionPointsTable,
)


class ExampleWidget(QFrame):
    """Used to create example widget for use as the central widget for gsewidgets examples window."""

    def __init__(self, model: PathModel) -> None:
        super(ExampleWidget, self).__init__()

        self._model = model

        # Widgets
        self.btn_flat = FlatButton("Flat button")
        self.btn_file_browser = FileBrowserButton(text="Open file")
        self.btn_directory_browser = DirectoryBrowserButton("Open directory")
        self.btn_color_dialog = ColorDialogButton(
            size=QSize(35, 32), default_color=QColor(4, 132, 117, 155)
        )
        self.btn_add = FlatButton("Add", size=QSize(80, 32))
        self.btn_delete = FlatButton("Delete", size=QSize(80, 32))
        self.btn_clear = FlatButton("Clear", size=QSize(80, 32))
        self.btn_check_all = FlatButton("Check all", size=QSize(80, 32))
        self.btn_uncheck_all = FlatButton("Uncheck all", size=QSize(80, 32))

        self.check_normal = CheckBox(text="Simple checkbox")
        self.check_toggle = ToggleCheckBox(size=QSize(55, 35))

        self.cmb_items = FullComboBox(size=QSize(50, 32))

        self.spin_normal = NumericSpinBox(
            min_value=-10.00,
            max_value=25.00,
            default_value=1.00,
            incremental_step=0.5,
            precision=2,
        )
        self.spin_no_wheel = NoWheelNumericSpinBox(
            min_value=-10.0000,
            max_value=25.0000,
            default_value=1.0000,
            incremental_step=0.005,
            precision=4,
        )

        self.input_normal = InputBox(placeholder="Normal Input")
        self.input_filename = FileNameInputBox(placeholder="Filename Input")
        self.input_filepath = FilePathInputBox(placeholder="Filepath Input")
        self.input_uri = URIInputBox(placeholder="https://google.com")

        self.xyz_table = XYZCollectionPointsTable()

        self.lbl_buttons = Label("Buttons | Checkboxes", object_name="title-label")
        self.lbl_selected_file = Label("Selected file: None")
        self.lbl_selected_directory = Label("Selected directory: None")
        self.lbl_selected_color = Label(
            f"Selected color: RGBA {self.btn_color_dialog.color.getRgb()}, "
            f"HEX ({self.btn_color_dialog.color.name()})"
        )
        self.lbl_spin = Label(
            "Combobox | Spinbox | NoWheel Spinbox | Normal Input | Filename Input | Filepath Input",
            object_name="title-label",
        )

        # Run configuration methods
        self._configure_example_widget()
        self._layout_example_widget()

    def _configure_example_widget(self) -> None:
        """Basic configuration of the example widget frame."""
        # Set the frame shape
        self.setFrameShape(QFrame.NoFrame)
        # Set the frame shadow
        self.setFrameShadow(QFrame.Raised)
        # Set object name
        self.setObjectName("example-frame")
        # Set the minimum window size
        self.setMinimumSize(650, 450)
        # Add example items to combo box
        self.cmb_items.addItems(["Item 1", "Item 2", "Item 3"])

    def _layout_example_widget(self) -> None:
        layout = QVBoxLayout()

        # Example buttons and checkboxes layout
        buttons_layout = QGridLayout()
        buttons_layout.addWidget(self.lbl_buttons, 0, 0)
        buttons_layout.addWidget(self.btn_flat, 1, 0, 1, 1)
        buttons_layout.addWidget(VerticalLine(), 1, 1, 1, 1)
        buttons_layout.addWidget(self.btn_file_browser, 1, 2, 1, 1)
        buttons_layout.addWidget(VerticalLine(), 1, 3, 1, 1)
        buttons_layout.addWidget(self.btn_directory_browser, 1, 4, 1, 1)
        buttons_layout.addWidget(VerticalLine(), 1, 5, 1, 1)
        buttons_layout.addWidget(self.btn_color_dialog, 1, 6, 1, 1)
        buttons_layout.addWidget(VerticalLine(), 1, 7, 1, 1)
        buttons_layout.addWidget(
            self.check_normal, 1, 8, 1, 1, alignment=Qt.AlignCenter
        )
        buttons_layout.addWidget(VerticalLine(), 1, 9, 1, 1)
        buttons_layout.addWidget(self.check_toggle, 1, 10, 1, 1)
        buttons_layout.addWidget(self.lbl_selected_file, 2, 0, 1, 11)
        buttons_layout.addWidget(self.lbl_selected_directory, 3, 0, 1, 11)
        buttons_layout.addWidget(self.lbl_selected_color, 4, 0, 1, 11)

        # Example spinboxes, combo and input widgets
        spin_layout = QGridLayout()
        spin_layout.addWidget(self.lbl_spin, 0, 0, 1, 11)
        spin_layout.addWidget(self.cmb_items, 1, 0, 1, 1)
        spin_layout.addWidget(VerticalLine(), 1, 1, 1, 1)
        spin_layout.addWidget(self.spin_normal, 1, 2, 1, 1)
        spin_layout.addWidget(VerticalLine(), 1, 3, 1, 1)
        spin_layout.addWidget(self.spin_no_wheel, 1, 4, 1, 1)
        spin_layout.addWidget(VerticalLine(), 1, 5, 1, 1)
        spin_layout.addWidget(self.input_normal, 1, 6, 1, 1)
        spin_layout.addWidget(VerticalLine(), 1, 7, 1, 1)
        spin_layout.addWidget(self.input_filename, 1, 8, 1, 1)
        spin_layout.addWidget(VerticalLine(), 1, 9, 1, 1)
        spin_layout.addWidget(self.input_filepath, 1, 10, 1, 1)
        spin_layout.addWidget(self.input_uri, 1, 11, 1, 1)

        # Example xyz table layout
        table_layout = QGridLayout()
        table_layout.addWidget(self.btn_add, 0, 3, 1, 1)
        table_layout.addWidget(self.btn_delete, 0, 4, 1, 1)
        table_layout.addWidget(self.btn_clear, 0, 5, 1, 1)
        table_layout.addWidget(self.btn_check_all, 0, 6, 1, 1)
        table_layout.addWidget(self.btn_uncheck_all, 0, 7, 1, 1)
        table_layout.addWidget(self.xyz_table, 1, 0, 1, 8)

        # Example main layout
        layout.addLayout(buttons_layout)
        layout.addWidget(HorizontalLine())
        # layout.addStretch(1)
        layout.addLayout(spin_layout)
        layout.addWidget(HorizontalLine())
        # layout.addStretch(1)
        layout.addLayout(table_layout)

        # Set the widget layout
        self.setLayout(layout)
