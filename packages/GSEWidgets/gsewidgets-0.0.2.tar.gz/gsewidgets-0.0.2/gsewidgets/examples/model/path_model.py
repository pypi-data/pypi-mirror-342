#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: path_model.py
# Description: Model that creates the paths for the assets directories.
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

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PathModel:
    """Model that creates the paths for the assets directories."""

    _assets_path: str = field(init=False, compare=False, repr=False)
    _qss_path: str = field(init=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "_assets_path",
            Path(Path.cwd(), "gsewidgets/examples/assets").as_posix(),
        )
        object.__setattr__(self, "_qss_path", Path(self._assets_path, "qss").as_posix())

    @property
    def qss_path(self) -> str:
        return self._qss_path
