#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: test_flat_button.py
# Description: Test the FlatButton widget.
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
import unittest
from qtpy.QtCore import Qt, QSize
from qtpy.QtTest import QTest, QSignalSpy
from qtpy.QtWidgets import QApplication

from gsewidgets.widgets.buttons import FlatButton


class TestFlatButton(unittest.TestCase):
    """Test the FlatButton widget."""

    def setUp(self) -> None:
        """Set up the test."""
        self._app = QApplication(sys.argv)
        self._btn_flat = FlatButton()

    def tearDown(self) -> None:
        """Tear down the test."""
        del self._btn_flat
        del self._app

    def test_empty_initialization(self) -> None:
        """Test the initialization of the widget."""
        btn = FlatButton()
        self.assertIsInstance(btn, FlatButton)
    
    def test_initialization_with_text(self) -> None:
        """Test initialization of FlatButton with text only."""
        btn = FlatButton(text="Test Button")
        self.assertIsInstance(btn, FlatButton)

    def test_initialization_with_size(self) -> None:
        """Test initialization of FlatButton with size only."""
        btn = FlatButton(size=QSize(100, 50))
        self.assertIsInstance(btn, FlatButton)

    def test_initialization_with_object_name(self) -> None:
        """Test initialization of FlatButton with object name only."""
        btn = FlatButton(object_name="test-button")
        self.assertIsInstance(btn, FlatButton)

    def test_initialization_with_text_and_size(self) -> None:
        """Test initialization of FlatButton with text and size."""
        btn = FlatButton(text="Test Button", size=QSize(100, 50))
        self.assertIsInstance(btn, FlatButton)

    def test_initialization_with_text_and_object_name(self) -> None:
        """Test initialization of FlatButton with text and object name."""
        btn = FlatButton(text="Test Button", object_name="test-button")
        self.assertIsInstance(btn, FlatButton)

    def test_initialization_with_size_and_object_name(self) -> None:
        """Test initialization of FlatButton with size and object name."""
        btn = FlatButton(size=QSize(100, 50), object_name="test-button")
        self.assertIsInstance(btn, FlatButton)

    def test_initialization_with_all_parameters(self) -> None:
        """Test initialization of FlatButton with all parameters."""
        btn = FlatButton(text="Test Button", size=QSize(100, 50), object_name="test-button")
        self.assertIsInstance(btn, FlatButton)

    def test_button_click_slot(self) -> None:
        """Test the button click."""
        # A QSignalSpy instance to spy on the clicked signal.
        spy = QSignalSpy(self._btn_flat.clicked)

        QTest.mouseClick(self._btn_flat, Qt.LeftButton)

        # Check if the clicked signal was emitted.
        self.assertEqual(len(spy), 1)

    def _button_clicked(self) -> None:
        """Set the button to clicked."""
        self._btn_flat.clicked = True


if __name__ == "__main__":
    unittest.main()
