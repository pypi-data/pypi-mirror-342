#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: __init__.py
# Description: Implementation of a custom widget collection, primarily
#              used in GSECARS software.
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

from gsewidgets import _version
from gsewidgets.widgets.filters import (
    FileNameEventFilter,
    FilePathEventFilter,
    URIParseEventFilter,
    IPv4EventFilter,
    MultiFloatEventFilter,
)
from gsewidgets.widgets.messageboxes import ErrorMessageBox
from gsewidgets.widgets.lines import VerticalLine, HorizontalLine
from gsewidgets.widgets.labels import Label, StatusLabel
from gsewidgets.widgets.buttons import (
    SimpleButton,
    FlatButton,
    FileBrowserButton,
    DirectoryBrowserButton,
    MultiFileBrowserButton,
    ColorDialogButton,
)
from gsewidgets.widgets.spinboxes import (
    NumericSpinBox,
    NoWheelNumericSpinBox,
    NumericDataSpinBoxModel,
)
from gsewidgets.widgets.inputboxes import (
    InputBox,
    FilePathInputBox,
    FileNameInputBox,
    URIInputBox,
    IPv4InputBox,
    MultiFloatInputBox,
    TextInfoBox,
)
from gsewidgets.widgets.comboboxes import FullComboBox
from gsewidgets.widgets.checkboxes import CheckBox, ToggleCheckBox
from gsewidgets.widgets.tables import XYZCollectionPointsTable

__version__ = _version.get_versions()["version"]
