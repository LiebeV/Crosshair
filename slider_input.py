#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtCore

# 自定义禁止滚轮的 QSlider
class NoWheelSlider(QtWidgets.QSlider):
    def wheelEvent(self, event):
        event.ignore()

# SliderInput 组件（包含滑块和文本框）
class SliderInput(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)

    def __init__(self, min_value, max_value, initial, is_float=False, scale=1, parent=None):
        super().__init__(parent)
        self.is_float = is_float
        self.scale = scale
        self.slider = NoWheelSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(int(round(initial / self.scale)))
        self.lineEdit = QtWidgets.QLineEdit(self.format_value(initial))
        self.lineEdit.setFixedWidth(50)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.slider)
        layout.addWidget(self.lineEdit)
        self.slider.valueChanged.connect(self.on_slider_changed)
        self.lineEdit.editingFinished.connect(self.on_lineedit_changed)

    def format_value(self, val):
        return f"{val:.1f}" if self.is_float else f"{int(val)}"

    def on_slider_changed(self, val):
        actual = val * self.scale
        self.lineEdit.setText(self.format_value(actual))
        self.valueChanged.emit(actual)

    def on_lineedit_changed(self):
        text = self.lineEdit.text().strip()
        try:
            val = float(text) if self.is_float else int(text)
        except:
            val = self.getValue()
        min_val = self.slider.minimum() * self.scale
        max_val = self.slider.maximum() * self.scale
        if val < min_val:
            val = min_val
        elif val > max_val:
            val = max_val
        self.setValue(val)
        self.valueChanged.emit(val)

    def getValue(self):
        return self.slider.value() * self.scale

    def setValue(self, val):
        self.slider.setValue(int(round(val / self.scale)))
        self.lineEdit.setText(self.format_value(val))
