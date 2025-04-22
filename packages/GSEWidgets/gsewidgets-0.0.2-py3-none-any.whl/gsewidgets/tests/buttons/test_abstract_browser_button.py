#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: test_abstract_browser_button.py
# Description: Test the abstract browser button widget.
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
from qtpy.QtWidgets import QApplication

from gsewidgets.widgets.buttons import AbstractBrowserButton


class TestAbstractBrowserButton(unittest.TestCase):
    """Test the AbstractBrowserButton"""

    def setUp(self) -> None:
        """Set up the test"""
        self._app = QApplication(sys.argv)
        self._btn_browser = AbstractBrowserButton()

    def tearDown(self) -> None:
        """Tear down the test"""
        del self._app

    def test_empty_caption(self) -> None:
        """Test the empty caption"""
        self.assertEqual(self._btn_browser.caption, "Select File")

    def test_caption(self) -> None:
        """Test the caption"""
        btn_browser = AbstractBrowserButton(caption="Select Folder")
        self.assertEqual(btn_browser.caption, "Select Folder")

    def test_empty_invalid_characters_argument(self) -> None:
        """Test the empty invalid characters argument"""
        self.assertEqual(self._btn_browser._invalid_characters, '<>"\\|?*#& ')

    def test_default_invalid_characters_for_target_directory(self) -> None:
        """Test the invalid characters for target directory"""
        invalid_characters = '<>"\\|?*#& '
        for char in invalid_characters:
            self._btn_browser.target_directory = f"test{char}invalid{char}characters"
            self.assertEqual(self._btn_browser.target_directory, "test_invalid_characters")


if __name__ == "__main__":
    unittest.main()
