#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: tables.py
# Description: Implementation of various table widgets.
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

from qtpy.QtCore import QObject, Signal, QSize, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import (
    QTableWidget,
    QAbstractItemView,
    QHeaderView,
    QWidget,
    QVBoxLayout,
)
from typing import Optional

from gsewidgets.widgets.inputboxes import FileNameInputBox
from gsewidgets.widgets.spinboxes import NoWheelNumericSpinBox, NumericDataSpinBoxModel
from gsewidgets.widgets.checkboxes import ToggleCheckBox

__all__ = ["XYZCollectionPointsTable"]


class TableWidget(QTableWidget):
    """Used to create instances of simple table templates."""

    def __init__(
        self,
        columns: Optional[int] = None,
        rows: Optional[int] = None,
        horizontal_headers: Optional[list[str]] = None,
        column_stretch: Optional[int] = None,
        object_name: Optional[str] = None,
    ) -> None:
        super(TableWidget, self).__init__()

        self._columns = columns
        self._rows = rows
        self._horizontal_headers = horizontal_headers
        self._column_stretch = column_stretch
        self._object_name = object_name

        self._configure_table_widget()

    def _configure_table_widget(self) -> None:
        """Basic configuration of the table widget."""
        # Set the columns
        if self._columns is not None:
            if self._columns >= 1:
                self.setColumnCount(self._columns)

        # Set the rows
        if self._rows is not None:
            if self._rows >= 1:
                self.setRowCount(self._rows)

        # Set horizontal headers
        if self._horizontal_headers is not None:
            self.setHorizontalHeaderLabels(self._horizontal_headers)
            self.horizontalHeader().setVisible(True)
        else:
            self.horizontalHeader().setVisible(False)

        # Set column stretch
        if self._column_stretch is not None:
            if 0 <= self._column_stretch <= self._columns - 1:
                self.horizontalHeader().setSectionResizeMode(
                    self._column_stretch, QHeaderView.Stretch
                )
        # Set object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Hide vertical header
        self.verticalHeader().setVisible(False)
        # Disable grid
        self.setShowGrid(False)
        # Disable header buttons
        self.horizontalHeader().setDisabled(True)
        # Set alternating row colors
        self.setAlternatingRowColors(True)
        # Set selection behavior and mode
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def delete_selection(self) -> None:
        """Removes the selected row from the table."""
        # Get the row index
        row_index = self.currentRow()
        # Remove the row
        if row_index >= 0:
            self.removeRow(row_index)

    def clear_table(self) -> None:
        """Removes all the existing rows from the table, excluding the headers."""
        # Get the total rows
        row_count = self.rowCount()
        # Remove the rows
        for row in range(row_count):
            self.removeRow(row)
        # Reset the row count
        self.setRowCount(0)


class XYZCollectionPointsTable(TableWidget, QObject):
    """Used to create instances of simple XYZ Collection Points table."""

    enabled_checkboxes_updated: Signal = Signal()

    def __init__(
        self,
        columns: Optional[int] = 5,
        rows: Optional[int] = 0,
        horizontal_headers=None,
        column_stretch: Optional[int] = 0,
        object_name: Optional[str] = "xyz-table",
        inactive_color: Optional[QColor] = QColor(206, 206, 206),
        active_color: Optional[QColor] = QColor(45, 200, 20),
        circle_color: Optional[QColor] = QColor(255, 255, 255),
        size: Optional[QSize] = QSize(55, 35),
        circle_radius_multiplier: Optional[float] = 0.25,
        bar_size_multiplier: Optional[float] = 0.35,
    ) -> None:
        # Check mutable input
        if horizontal_headers is None:
            horizontal_headers = ["Name", "X", "Y", "Z", "Enabled"]
        # Initialize
        super(XYZCollectionPointsTable, self).__init__(
            columns=columns,
            rows=rows,
            horizontal_headers=horizontal_headers,
            column_stretch=column_stretch,
            object_name=object_name,
        )

        self._inactive_color = inactive_color
        self._active_color = active_color
        self._circle_color = circle_color
        self._size = size
        self._circle_radius_multiplier = circle_radius_multiplier
        self._bar_size_multiplier = bar_size_multiplier

        self._enabled_checkboxes: list[ToggleCheckBox] = []
        self._numeric_data_list: list[list[NumericDataSpinBoxModel]] = []
        self._file_names_list: list[str] = []
        self._name_counter: int = 1

    def add_point(
        self,
        x: NumericDataSpinBoxModel,
        y: NumericDataSpinBoxModel,
        z: NumericDataSpinBoxModel,
    ) -> None:
        """Adds a single collection point to the bottom of the list."""
        # Get rows
        row = self.rowCount()
        # Increase the row count by 1
        self.setRowCount(row + 1)

        # Check if the name already exists
        if row > 0:
            for name in self._file_names_list:
                if f"point_{self._name_counter}" == name:
                    self._name_counter += 1
        # Set the name based on the name counter without checking if there are missing names
        dynamically_created_name = f"point_{self._name_counter}"
        # Create the file name widget
        file_name_widget = FileNameInputBox(object_name="table-input-box")
        file_name_widget.setStyleSheet("background-color: transparent;" "border: none;")
        file_name_widget.setText(dynamically_created_name)
        # Append to the file names list
        self._file_names_list.append(dynamically_created_name)
        # Set the item
        self.setCellWidget(row, 0, file_name_widget)

        # Create the X,Y and Z widgets
        # X widget
        x_widget = NoWheelNumericSpinBox(
            min_value=x.min_value,
            max_value=x.max_value,
            default_value=x.current_value,
            incremental_step=x.incremental_step,
            precision=x.precision,
            object_name="table-spinbox",
        )
        x_widget.setStyleSheet("background-color: transparent;" "border: none;")
        x_widget.valueChanged.connect(
            lambda: x.spinbox_value_changed.emit(x_widget.value())
        )
        self.setCellWidget(row, 1, x_widget)
        # Y widget
        y_widget = NoWheelNumericSpinBox(
            min_value=y.min_value,
            max_value=y.max_value,
            default_value=y.current_value,
            incremental_step=y.incremental_step,
            precision=y.precision,
            object_name="table-spinbox",
        )
        y_widget.setStyleSheet("background-color: transparent;" "border: none;")
        y_widget.valueChanged.connect(
            lambda: y.spinbox_value_changed.emit(y_widget.value())
        )
        self.setCellWidget(row, 2, y_widget)
        # Z widget
        z_widget = NoWheelNumericSpinBox(
            min_value=z.min_value,
            max_value=z.max_value,
            default_value=z.current_value,
            incremental_step=z.incremental_step,
            precision=z.precision,
            object_name="table-spinbox",
        )
        z_widget.setStyleSheet("background-color: transparent;" "border: None;")
        z_widget.valueChanged.connect(
            lambda: z.spinbox_value_changed.emit(z_widget.value())
        )
        self.setCellWidget(row, 3, z_widget)
        # Append to the numeric list
        self.numeric_data_list.append([x, y, z])

        # Create the enabled checkbox
        checkbox = ToggleCheckBox(
            inactive_color=self._inactive_color,
            active_color=self._active_color,
            circle_color=self._circle_color,
            size=self._size,
            circle_radius_multiplier=self._circle_radius_multiplier,
            bar_size_multiplier=self._bar_size_multiplier,
        )
        # Set default state as checked
        checkbox.setChecked(True)
        # Create separate widget to center align the checkbox before adding to the table
        checkbox_widget = QWidget()
        checkbox_widget_layout = QVBoxLayout()
        checkbox_widget_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_widget_layout.setSpacing(0)
        checkbox_widget_layout.addWidget(checkbox, alignment=Qt.AlignCenter)
        checkbox_widget.setLayout(checkbox_widget_layout)
        # Add to table
        self.setCellWidget(row, 4, checkbox_widget)
        # Add to the enabled checkboxes list
        self.enabled_checkboxes.append(checkbox)
        # Connect checkbox state changed
        checkbox.stateChanged.connect(lambda: self.enabled_checkboxes_updated.emit())

    def enable_all_points(self) -> None:
        """Sets the check state to True for all the checkboxes included in the list of checkboxes."""
        for checkbox in self.enabled_checkboxes:
            checkbox.setChecked(True)

    def disable_all_points(self) -> None:
        """Sets the check state to False for all the checkboxes included in the list of checkboxes."""
        for checkbox in self.enabled_checkboxes:
            checkbox.setChecked(False)

    def clear_table(self) -> None:
        """Deletes all the rows of the table and clears the lists of checkboxes, numeric data and file names."""
        # Remove existing rows
        super(XYZCollectionPointsTable, self).clear_table()
        # Clear the lists
        self._enabled_checkboxes.clear()
        self.numeric_data_list.clear()
        self._file_names_list.clear()

    def delete_selection(self) -> None:
        """
        Removes the selected row from the table, the checkbox entry from the list of checkboxes,
        the numeric data entry from the list of numeric data and the file name entry from
        the file names list.
        """
        index = self.currentRow()
        if index >= 0:
            self.removeRow(index)
            self.enabled_checkboxes.pop(index)
            self.numeric_data_list.pop(index)
            self._file_names_list.pop(index)

    @property
    def enabled_checkboxes(self) -> list[ToggleCheckBox]:
        return self._enabled_checkboxes

    @property
    def numeric_data_list(self) -> list[list[NumericDataSpinBoxModel]]:
        return self._numeric_data_list
