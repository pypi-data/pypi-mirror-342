#!/usr/bin/python3
# ------------------------------------------------------------------------------
# Script Name: checkboxes.py
# Description: Implementation of various checkbox widgets.
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

from qtpy.QtCore import (
    Qt,
    QSize,
    Property,
    QPoint,
    QPointF,
    QRectF,
    QEasingCurve,
    QPropertyAnimation,
    QSequentialAnimationGroup,
)
from qtpy.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from qtpy.QtWidgets import QCheckBox
from typing import Optional

__all__ = ["CheckBox", "ToggleCheckBox"]


class CheckBox(QCheckBox):
    """Used to create instances of simple checkboxes."""

    def __init__(
        self,
        text: Optional[str] = None,
        right_orientation: Optional[bool] = False,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "simple-checkbox",
    ) -> None:
        super(CheckBox, self).__init__()

        self._text = text
        self._right_orientation = right_orientation
        self._size = size
        self._object_name = object_name

        # Run configuration
        self._configure_checkbox()

    def _configure_checkbox(self) -> None:
        """Basic configuration for the checkbox widget."""
        # Disable tristate
        self.setTristate(False)

        # Set text
        if self._text is not None:
            self.setText(self._text)

        # Set orientation
        if self._right_orientation:
            self.setLayoutDirection(Qt.RightToLeft)

        # Set the overall size
        if self._size is not None:
            self.setFixedSize(self._size)

        # Set the object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

    def _state_change_event(self, state: bool) -> None:
        """Clears the focus state of the checkbox."""
        self.clearFocus()


class ToggleCheckBox(QCheckBox):
    """Used to create instances of toggle checkboxes."""

    def __init__(
        self,
        inactive_color: Optional[QColor] = QColor(206, 206, 206),
        active_color: Optional[QColor] = QColor(45, 200, 20),
        circle_color: Optional[QColor] = QColor(255, 255, 255),
        size: Optional[QSize] = None,
        circle_radius_multiplier: Optional[float] = 0.28,
        bar_size_multiplier: Optional[float] = 0.35,
    ) -> None:
        super(ToggleCheckBox, self).__init__()

        self._inactive_brush = QBrush(inactive_color)
        self._circle_inactive_brush = QBrush(circle_color)
        self._active_brush = QBrush(QColor(active_color).lighter())
        self._circle_active_brush = QBrush(QColor(active_color))
        self._size = size
        self._circle_radius_multiplier = circle_radius_multiplier
        self._bar_size_multiplier = bar_size_multiplier

        self._circle_position: float = 0
        self._animation = QPropertyAnimation(self, b"circle_position")
        self._animation_group = QSequentialAnimationGroup()

        # Run the configuration methods
        self._configure_toggle_checkbox()

    def _configure_toggle_checkbox(self) -> None:
        """Basic configuration of the toggle checkbox."""
        # Set the overall size
        if self._size is not None:
            self.setFixedSize(self._size)
        # Set the margins
        self.setContentsMargins(8, 0, 8, 0)
        # Set the animation method
        self._animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        # Set the animation duration
        self._animation.setDuration(350)
        # Add the animation to the group
        self._animation_group.addAnimation(self._animation)
        # Connect the state changed signal of the checkbox
        self.stateChanged.connect(self._run_animations)

    def _run_animations(self, state: bool) -> None:
        """Runs the animations for each checkbox state."""
        # Stop any animations that are already running
        self._animation_group.stop()
        # Clear the focus
        self.clearFocus()
        # Set and start the animation
        self._animation.setEndValue(1) if state else self._animation.setEndValue(0)
        self._animation_group.start()

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, position: QPoint) -> QPoint:
        return self.contentsRect().contains(position)

    def paintEvent(self, event: QPaintEvent) -> None:
        # Set the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.GlobalColor.transparent))

        # Compute and draw the rectangle
        contents_rect = self.contentsRect()
        circle_radius = round(self._circle_radius_multiplier * contents_rect.height())
        bar_rectangle = QRectF(
            0,
            0,
            contents_rect.width() - circle_radius,
            self._bar_size_multiplier * contents_rect.height(),
        )
        bar_rectangle.moveCenter(contents_rect.center().toPointF())

        trail_bar = contents_rect.width() - 2 * circle_radius
        x_position = (
            contents_rect.x() + circle_radius + trail_bar * self._circle_position
        )
        radius = bar_rectangle.height() / 2

        if self.isChecked():
            # Set active status
            painter.setBrush(self._active_brush)
            painter.drawRoundedRect(bar_rectangle, radius, radius)
            painter.setBrush(self._circle_active_brush)

        else:
            # Set inactive status
            painter.setBrush(self._inactive_brush)
            painter.drawRoundedRect(bar_rectangle, radius, radius)
            painter.setPen(QPen(Qt.GlobalColor.lightGray))
            painter.setBrush(self._circle_inactive_brush)

        # Draw the ellipse
        painter.drawEllipse(
            QPointF(x_position, bar_rectangle.center().y()),
            circle_radius,
            circle_radius,
        )

        painter.end()

    def update_toggle(self, value: float) -> None:
        self.setChecked(value)

    @Property(float)
    def circle_position(self) -> float:
        return self._circle_position

    @circle_position.setter
    def circle_position(self, value: float) -> None:
        self._circle_position = value
        self.update()
