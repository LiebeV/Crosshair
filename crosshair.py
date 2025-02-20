#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json, argparse, re, math
from datetime import datetime
from PySide6 import QtWidgets, QtCore, QtGui
import keyboard


# ----------------------------
# 数据模型：CrosshairConfig
# ----------------------------
class CrosshairConfig:
    def __init__(
        self,
        inner_gap=10,
        inner_length=20,
        inner_thickness=2,
        inner_color="#FF0000",
        inner_opacity=1.0,
        inner_line_count=4,
        center_enabled=False,
        center_color=None,
        center_thickness=None,
        outer_frame_enabled=False,
        outer_frame_color=None,
        outer_frame_opacity=None,
        outer_frame_thickness=None,
        outer_cross_enabled=False,
        outer_gap=30,
        outer_length=20,
        outer_thickness=2,
        outer_cross_color=None,
        outer_cross_opacity=None,
        outer_line_count=4,
        advanced_enabled=False,
        inner_angle_offset=0,
        offset_x=0,
        offset_y=0,
        overall_angle_offset=0,
        advanced_cap_style=0,
    ):
        self.inner_gap = inner_gap
        self.inner_length = inner_length
        self.inner_thickness = inner_thickness
        self.inner_color = inner_color
        self.inner_opacity = inner_opacity
        self.inner_line_count = inner_line_count
        self.center_enabled = center_enabled
        self.center_color = center_color if center_color is not None else inner_color
        self.center_thickness = (
            center_thickness if center_thickness is not None else inner_thickness
        )
        self.outer_frame_enabled = outer_frame_enabled
        self.outer_frame_color = (
            outer_frame_color if outer_frame_color is not None else inner_color
        )
        self.outer_frame_opacity = (
            outer_frame_opacity if outer_frame_opacity is not None else inner_opacity
        )
        self.outer_frame_thickness = (
            outer_frame_thickness
            if outer_frame_thickness is not None
            else inner_thickness
        )
        self.outer_cross_enabled = outer_cross_enabled
        self.outer_gap = outer_gap
        self.outer_length = outer_length
        self.outer_thickness = outer_thickness
        self.outer_cross_color = (
            outer_cross_color if outer_cross_color is not None else inner_color
        )
        self.outer_cross_opacity = (
            outer_cross_opacity if outer_cross_opacity is not None else inner_opacity
        )
        self.outer_line_count = outer_line_count
        self.advanced_enabled = advanced_enabled
        self.inner_angle_offset = inner_angle_offset
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.overall_angle_offset = overall_angle_offset
        self.advanced_cap_style = advanced_cap_style

    def to_dict(self):
        return {
            "inner_gap": self.inner_gap,
            "inner_length": self.inner_length,
            "inner_thickness": self.inner_thickness,
            "inner_color": self.inner_color,
            "inner_opacity": self.inner_opacity,
            "inner_line_count": self.inner_line_count,
            "center_enabled": self.center_enabled,
            "center_color": self.center_color,
            "center_thickness": self.center_thickness,
            "outer_frame_enabled": self.outer_frame_enabled,
            "outer_frame_color": self.outer_frame_color,
            "outer_frame_opacity": self.outer_frame_opacity,
            "outer_frame_thickness": self.outer_frame_thickness,
            "outer_cross_enabled": self.outer_cross_enabled,
            "outer_gap": self.outer_gap,
            "outer_length": self.outer_length,
            "outer_thickness": self.outer_thickness,
            "outer_cross_color": self.outer_cross_color,
            "outer_cross_opacity": self.outer_cross_opacity,
            "outer_line_count": self.outer_line_count,
            "advanced_enabled": self.advanced_enabled,
            "inner_angle_offset": self.inner_angle_offset,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            "overall_angle_offset": self.overall_angle_offset,
            "advanced_cap_style": self.advanced_cap_style,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            inner_gap=d.get("inner_gap", 10),
            inner_length=d.get("inner_length", 20),
            inner_thickness=d.get("inner_thickness", 2),
            inner_color=d.get("inner_color", "#FF0000"),
            inner_opacity=d.get("inner_opacity", 1.0),
            inner_line_count=d.get("inner_line_count", 4),
            center_enabled=d.get("center_enabled", False),
            center_color=d.get("center_color", None),
            center_thickness=d.get("center_thickness", None),
            outer_frame_enabled=d.get("outer_frame_enabled", False),
            outer_frame_color=d.get("outer_frame_color", None),
            outer_frame_opacity=d.get("outer_frame_opacity", None),
            outer_frame_thickness=d.get("outer_frame_thickness", None),
            outer_cross_enabled=d.get("outer_cross_enabled", False),
            outer_gap=d.get("outer_gap", 30),
            outer_length=d.get("outer_length", 20),
            outer_thickness=d.get("outer_thickness", 2),
            outer_cross_color=d.get("outer_cross_color", None),
            outer_cross_opacity=d.get("outer_cross_opacity", None),
            outer_line_count=d.get("outer_line_count", 4),
            advanced_enabled=d.get("advanced_enabled", False),
            inner_angle_offset=d.get("inner_angle_offset", 0),
            offset_x=d.get("offset_x", 0),
            offset_y=d.get("offset_y", 0),
            overall_angle_offset=d.get("overall_angle_offset", 0),
            advanced_cap_style=d.get("advanced_cap_style", 0),
        )

    def encode(self) -> str:
        s = ""
        s += f"ig{self.inner_gap}"
        s += f"il{self.inner_length}"
        s += f"it{self.inner_thickness}"
        s += f"ic{self.inner_color.lstrip('#').upper()}"
        s += f"io{int(round(self.inner_opacity*10))}"
        s += f"inl{self.inner_line_count}"
        s += f"ce{1 if self.center_enabled else 0}"
        if self.center_enabled:
            s += f"cc{self.center_color.lstrip('#').upper()}"
            s += f"ct{self.center_thickness}"
        s += f"ofr{1 if self.outer_frame_enabled else 0}"
        if self.outer_frame_enabled:
            s += f"ofc{self.outer_frame_color.lstrip('#').upper()}"
            s += f"oo{int(round(self.outer_frame_opacity*10))}"
            s += f"oft{self.outer_frame_thickness}"
        s += f"ocx{1 if self.outer_cross_enabled else 0}"
        if self.outer_cross_enabled:
            s += f"oxg{self.outer_gap}"
            s += f"oxl{self.outer_length}"
            s += f"oxt{self.outer_thickness}"
            s += f"oxc{self.outer_cross_color.lstrip('#').upper()}"
            s += f"oxo{int(round(self.outer_cross_opacity*10))}"
            s += f"olc{self.outer_line_count}"
        s += f"adv{1 if self.advanced_enabled else 0}"
        if self.advanced_enabled:
            s += f"ia{self.inner_angle_offset}"
            s += f"ax{self.offset_x}"
            s += f"ay{self.offset_y}"
            s += f"oa{self.overall_angle_offset}"
            s += f"acp{self.advanced_cap_style}"
        return s

    @classmethod
    def decode(cls, code: str):
        pattern = (
            r"ig(\d+)"
            r"il(\d+)"
            r"it(\d+)"
            r"ic([0-9A-Fa-f]+)"
            r"io(\d+)"
            r"inl(\d+)"
            r"ce([01])"
            r"(?:cc([0-9A-Fa-f]+)ct(\d+))?"
            r"ofr([01])"
            r"(?:ofc([0-9A-Fa-f]+)oo(\d+)oft(\d+))?"
            r"ocx([01])"
            r"(?:oxg(\d+)oxl(\d+)oxt(\d+)oxc([0-9A-Fa-f]+)oxo(\d+)olc(\d+))?"
            r"adv([01])"
            r"(?:ia(\d+)ax(-?\d+)ay(-?\d+)oa(-?\d+)acp(\d+))?"
        )
        m = re.fullmatch(pattern, code)
        if not m:
            raise ValueError("准星代码格式错误")
        inner_gap = int(m.group(1))
        inner_length = int(m.group(2))
        inner_thickness = int(m.group(3))
        inner_color = "#" + m.group(4).upper()
        inner_opacity = int(m.group(5)) / 10.0
        inner_line_count = int(m.group(6))
        center_enabled = m.group(7) == "1"
        center_color = (
            "#" + m.group(8).upper() if center_enabled and m.group(8) else inner_color
        )
        center_thickness = (
            int(m.group(9)) if center_enabled and m.group(9) else inner_thickness
        )
        outer_frame_enabled = m.group(10) == "1"
        outer_frame_color = (
            "#" + m.group(11).upper()
            if outer_frame_enabled and m.group(11)
            else inner_color
        )
        outer_frame_opacity = (
            int(m.group(12)) / 10.0
            if outer_frame_enabled and m.group(12)
            else inner_opacity
        )
        outer_frame_thickness = (
            int(m.group(13)) if outer_frame_enabled and m.group(13) else inner_thickness
        )
        outer_cross_enabled = m.group(14) == "1"
        if outer_cross_enabled:
            outer_gap = int(m.group(15))
            outer_length = int(m.group(16))
            outer_thickness = int(m.group(17))
            outer_cross_color = "#" + m.group(18).upper()
            outer_cross_opacity = int(m.group(19)) / 10.0
            outer_line_count = int(m.group(20))
        else:
            outer_gap = 30
            outer_length = 20
            outer_thickness = 2
            outer_cross_color = inner_color
            outer_cross_opacity = inner_opacity
            outer_line_count = 4
        advanced_enabled = m.group(21) == "1"
        if advanced_enabled:
            inner_angle_offset = int(m.group(22))
            offset_x = int(m.group(23))
            offset_y = int(m.group(24))
            overall_angle_offset = int(m.group(25))
            advanced_cap_style = int(m.group(26))
        else:
            inner_angle_offset = 0
            offset_x = 0
            offset_y = 0
            overall_angle_offset = 0
            advanced_cap_style = 0
        return cls(
            inner_gap,
            inner_length,
            inner_thickness,
            inner_color,
            inner_opacity,
            inner_line_count,
            center_enabled,
            center_color,
            center_thickness,
            outer_frame_enabled,
            outer_frame_color,
            outer_frame_opacity,
            outer_frame_thickness,
            outer_cross_enabled,
            outer_gap,
            outer_length,
            outer_thickness,
            outer_cross_color,
            outer_cross_opacity,
            outer_line_count,
            advanced_enabled,
            inner_angle_offset,
            offset_x,
            offset_y,
            overall_angle_offset,
            advanced_cap_style,
        )


# ----------------------------
# 自定义 QSlider（禁止滚轮）
# ----------------------------
class NoWheelSlider(QtWidgets.QSlider):
    def wheelEvent(self, event):
        event.ignore()


# ----------------------------
# 自定义组件：SliderInput
# ----------------------------
class SliderInput(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)

    def __init__(
        self, min_value, max_value, initial, is_float=False, scale=1, parent=None
    ):
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


# ----------------------------
# 预览控件
# ----------------------------
class CrosshairPreview(QtWidgets.QWidget):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        self.config = config if config is not None else CrosshairConfig()

    def updateConfig(self, config):
        self.config = config
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # 清除背景为透明
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        w, h = self.width(), self.height()
        base_center = QtCore.QPoint(w // 2, h // 2)
        center = QtCore.QPoint(
            base_center.x() + self.config.offset_x,
            base_center.y() + self.config.offset_y,
        )
        effective_inner_angle = (
            self.config.overall_angle_offset + self.config.inner_angle_offset
        )
        # 绘制外框（对内侧准星描边）
        if self.config.outer_frame_enabled:
            pen_frame = QtGui.QPen(
                QtGui.QColor(self.config.outer_frame_color),
                self.config.outer_frame_thickness,
            )
            col_frame = QtGui.QColor(self.config.outer_frame_color)
            col_frame.setAlphaF(self.config.outer_frame_opacity)
            pen_frame.setColor(col_frame)
            painter.setPen(pen_frame)
            for i in range(self.config.inner_line_count):
                angle_deg = (
                    effective_inner_angle + (360 / self.config.inner_line_count) * i
                )
                angle_rad = math.radians(angle_deg)
                x1 = math.cos(angle_rad) * self.config.inner_gap
                y1 = math.sin(angle_rad) * self.config.inner_gap
                x2 = math.cos(angle_rad) * (
                    self.config.inner_gap + self.config.inner_length
                )
                y2 = math.sin(angle_rad) * (
                    self.config.inner_gap + self.config.inner_length
                )
                painter.drawLine(
                    QtCore.QPointF(center.x() + x1, center.y() + y1),
                    QtCore.QPointF(center.x() + x2, center.y() + y2),
                )
        # 绘制内侧十字准星
        pen_inner = QtGui.QPen(
            QtGui.QColor(self.config.inner_color), self.config.inner_thickness
        )
        col_inner = QtGui.QColor(self.config.inner_color)
        col_inner.setAlphaF(self.config.inner_opacity)
        pen_inner.setColor(col_inner)
        painter.setPen(pen_inner)
        for i in range(self.config.inner_line_count):
            angle_deg = effective_inner_angle + (360 / self.config.inner_line_count) * i
            angle_rad = math.radians(angle_deg)
            x1 = math.cos(angle_rad) * self.config.inner_gap
            y1 = math.sin(angle_rad) * self.config.inner_gap
            x2 = math.cos(angle_rad) * (
                self.config.inner_gap + self.config.inner_length
            )
            y2 = math.sin(angle_rad) * (
                self.config.inner_gap + self.config.inner_length
            )
            painter.drawLine(
                QtCore.QPointF(center.x() + x1, center.y() + y1),
                QtCore.QPointF(center.x() + x2, center.y() + y2),
            )
        # 绘制中心点
        if self.config.center_enabled:
            col_center = QtGui.QColor(self.config.center_color)
            col_center.setAlphaF(self.config.inner_opacity)
            painter.setBrush(QtGui.QBrush(col_center))
            d = self.config.center_thickness
            painter.drawEllipse(center, d // 2, d // 2)
        # 绘制外侧十字准星
        if self.config.outer_cross_enabled:
            effective_outer_angle = self.config.overall_angle_offset
            pen_outer = QtGui.QPen(
                QtGui.QColor(self.config.outer_cross_color), self.config.outer_thickness
            )
            col_outer = QtGui.QColor(self.config.outer_cross_color)
            col_outer.setAlphaF(self.config.outer_cross_opacity)
            pen_outer.setColor(col_outer)
            painter.setPen(pen_outer)
            for i in range(self.config.outer_line_count):
                angle_deg = (
                    effective_outer_angle + (360 / self.config.outer_line_count) * i
                )
                angle_rad = math.radians(angle_deg)
                x1 = math.cos(angle_rad) * self.config.outer_gap
                y1 = math.sin(angle_rad) * self.config.outer_gap
                x2 = math.cos(angle_rad) * (
                    self.config.outer_gap + self.config.outer_length
                )
                y2 = math.sin(angle_rad) * (
                    self.config.outer_gap + self.config.outer_length
                )
                painter.drawLine(
                    QtCore.QPointF(center.x() + x1, center.y() + y1),
                    QtCore.QPointF(center.x() + x2, center.y() + y2),
                )
        painter.end()


# ----------------------------
# 全局覆盖窗口
# ----------------------------
class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("准星")
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def updateConfig(self, config):
        self.config = config
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        preview = CrosshairPreview(self.config)
        preview.resize(self.size())
        pm = preview.grab()
        painter.drawPixmap(0, 0, pm)
        painter.end()


# ----------------------------
# 编辑器界面
# ----------------------------
class CrosshairEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 内外侧线条数量参数默认值为4
        self.config = CrosshairConfig(inner_line_count=4, outer_line_count=4)
        self.export_file = os.path.join(os.getcwd(), "exported_crosshairs.json")
        self.initUI()

    def initUI(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        # 左侧：预览与参数
        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        # 上部：预览区域
        preview_container = QtWidgets.QWidget()
        preview_layout = QtWidgets.QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        self.preview = CrosshairPreview(self.config)
        preview_layout.addWidget(self.preview)
        splitter.addWidget(preview_container)
        splitter.setStretchFactor(0, 3)
        # 下部：参数设置
        param_container = QtWidgets.QWidget()
        param_layout = QtWidgets.QVBoxLayout(param_container)
        # 内侧十字准星组
        inner_group = QtWidgets.QGroupBox("内侧十字准星")
        inner_form = QtWidgets.QFormLayout(inner_group)
        self.inner_gap_slider = SliderInput(0, 100, self.config.inner_gap)
        self.inner_gap_slider.valueChanged.connect(self.onParameterChanged)
        inner_form.addRow("间距:", self.inner_gap_slider)
        self.inner_length_slider = SliderInput(0, 100, self.config.inner_length)
        self.inner_length_slider.valueChanged.connect(self.onParameterChanged)
        inner_form.addRow("长度:", self.inner_length_slider)
        self.inner_thickness_slider = SliderInput(1, 20, self.config.inner_thickness)
        self.inner_thickness_slider.valueChanged.connect(self.onParameterChanged)
        inner_form.addRow("粗细:", self.inner_thickness_slider)
        self.inner_color_edit = QtWidgets.QLineEdit(self.config.inner_color)
        self.inner_color_btn = QtWidgets.QPushButton("选择颜色")
        self.inner_color_btn.clicked.connect(self.chooseInnerColor)
        hl_inner = QtWidgets.QHBoxLayout()
        hl_inner.addWidget(self.inner_color_edit)
        hl_inner.addWidget(self.inner_color_btn)
        inner_form.addRow("颜色:", hl_inner)
        self.inner_opacity_slider = SliderInput(
            0, 10, self.config.inner_opacity, is_float=True, scale=0.1
        )
        self.inner_opacity_slider.valueChanged.connect(self.onParameterChanged)
        inner_form.addRow("不透明度:", self.inner_opacity_slider)
        self.inner_line_count_slider = SliderInput(2, 12, self.config.inner_line_count)
        self.inner_line_count_slider.valueChanged.connect(self.onParameterChanged)
        inner_form.addRow("内侧线条数量:", self.inner_line_count_slider)
        param_layout.addWidget(inner_group)
        # 准星中心点组
        self.center_group = QtWidgets.QGroupBox("准星中心点")
        self.center_group.setCheckable(True)
        self.center_group.setChecked(self.config.center_enabled)
        center_form = QtWidgets.QFormLayout(self.center_group)
        self.center_color_edit = QtWidgets.QLineEdit(self.config.center_color)
        self.center_color_btn = QtWidgets.QPushButton("选择颜色")
        self.center_color_btn.clicked.connect(self.chooseCenterColor)
        hl_center = QtWidgets.QHBoxLayout()
        hl_center.addWidget(self.center_color_edit)
        hl_center.addWidget(self.center_color_btn)
        center_form.addRow("中心颜色:", hl_center)
        self.center_thickness_slider = SliderInput(1, 20, self.config.center_thickness)
        self.center_thickness_slider.valueChanged.connect(self.onParameterChanged)
        center_form.addRow("中心粗细:", self.center_thickness_slider)
        self.center_group.toggled.connect(self.onParameterChanged)
        param_layout.addWidget(self.center_group)
        # 外框组
        self.outer_frame_group = QtWidgets.QGroupBox("外框")
        self.outer_frame_group.setCheckable(True)
        self.outer_frame_group.setChecked(self.config.outer_frame_enabled)
        outer_frame_form = QtWidgets.QFormLayout(self.outer_frame_group)
        self.outer_frame_color_edit = QtWidgets.QLineEdit(self.config.outer_frame_color)
        self.outer_frame_color_btn = QtWidgets.QPushButton("选择颜色")
        self.outer_frame_color_btn.clicked.connect(self.chooseOuterFrameColor)
        hl_of = QtWidgets.QHBoxLayout()
        hl_of.addWidget(self.outer_frame_color_edit)
        hl_of.addWidget(self.outer_frame_color_btn)
        outer_frame_form.addRow("颜色:", hl_of)
        self.outer_frame_opacity_slider = SliderInput(
            0, 10, self.config.outer_frame_opacity, is_float=True, scale=0.1
        )
        self.outer_frame_opacity_slider.valueChanged.connect(self.onParameterChanged)
        outer_frame_form.addRow("不透明度:", self.outer_frame_opacity_slider)
        self.outer_frame_thickness_slider = SliderInput(
            1, 20, self.config.outer_frame_thickness
        )
        self.outer_frame_thickness_slider.valueChanged.connect(self.onParameterChanged)
        outer_frame_form.addRow("粗细:", self.outer_frame_thickness_slider)
        self.outer_frame_group.toggled.connect(self.onParameterChanged)
        param_layout.addWidget(self.outer_frame_group)
        # 外侧十字准星组
        self.outer_cross_group = QtWidgets.QGroupBox("外侧十字准星")
        self.outer_cross_group.setCheckable(True)
        self.outer_cross_group.setChecked(self.config.outer_cross_enabled)
        outer_cross_form = QtWidgets.QFormLayout(self.outer_cross_group)
        self.outer_gap_slider = SliderInput(0, 100, self.config.outer_gap)
        self.outer_gap_slider.valueChanged.connect(self.onParameterChanged)
        outer_cross_form.addRow("间距:", self.outer_gap_slider)
        self.outer_length_slider = SliderInput(0, 100, self.config.outer_length)
        self.outer_length_slider.valueChanged.connect(self.onParameterChanged)
        outer_cross_form.addRow("长度:", self.outer_length_slider)
        self.outer_thickness_slider = SliderInput(1, 20, self.config.outer_thickness)
        self.outer_thickness_slider.valueChanged.connect(self.onParameterChanged)
        outer_cross_form.addRow("粗细:", self.outer_thickness_slider)
        self.outer_cross_color_edit = QtWidgets.QLineEdit(self.config.outer_cross_color)
        self.outer_cross_color_btn = QtWidgets.QPushButton("选择颜色")
        self.outer_cross_color_btn.clicked.connect(self.chooseOuterCrossColor)
        hl_oc = QtWidgets.QHBoxLayout()
        hl_oc.addWidget(self.outer_cross_color_edit)
        hl_oc.addWidget(self.outer_cross_color_btn)
        outer_cross_form.addRow("颜色:", hl_oc)
        self.outer_cross_opacity_slider = SliderInput(
            0, 10, self.config.outer_cross_opacity, is_float=True, scale=0.1
        )
        self.outer_cross_opacity_slider.valueChanged.connect(self.onParameterChanged)
        outer_cross_form.addRow("不透明度:", self.outer_cross_opacity_slider)
        self.outer_line_count_slider = SliderInput(2, 12, self.config.outer_line_count)
        self.outer_line_count_slider.valueChanged.connect(self.onParameterChanged)
        outer_cross_form.addRow("外侧线条数量:", self.outer_line_count_slider)
        self.outer_cross_group.toggled.connect(self.onParameterChanged)
        param_layout.addWidget(self.outer_cross_group)
        # 进阶设置组
        self.advanced_group = QtWidgets.QGroupBox("进阶设置")
        self.advanced_group.setCheckable(True)
        self.advanced_group.setChecked(self.config.advanced_enabled)
        advanced_form = QtWidgets.QFormLayout(self.advanced_group)
        self.inner_angle_slider = SliderInput(0, 360, self.config.inner_angle_offset)
        self.inner_angle_slider.valueChanged.connect(self.onParameterChanged)
        advanced_form.addRow("内侧准星角度偏移:", self.inner_angle_slider)
        self.offsetx_slider = SliderInput(-100, 100, self.config.offset_x)
        self.offsetx_slider.valueChanged.connect(self.onParameterChanged)
        advanced_form.addRow("水平偏移:", self.offsetx_slider)
        self.offsety_slider = SliderInput(-100, 100, self.config.offset_y)
        self.offsety_slider.valueChanged.connect(self.onParameterChanged)
        advanced_form.addRow("垂直偏移:", self.offsety_slider)
        self.overall_angle_slider = SliderInput(
            0, 360, self.config.overall_angle_offset
        )
        self.overall_angle_slider.valueChanged.connect(self.onParameterChanged)
        advanced_form.addRow("整体角度偏移:", self.overall_angle_slider)
        self.advanced_cap_style_group = QtWidgets.QGroupBox("线端样式")
        hs_adv_cs = QtWidgets.QHBoxLayout()
        self.advanced_cap_style_button_group = QtWidgets.QButtonGroup(self)
        rb_adv_flat = QtWidgets.QRadioButton("Flat")
        rb_adv_square = QtWidgets.QRadioButton("Square")
        rb_adv_round = QtWidgets.QRadioButton("Round")
        self.advanced_cap_style_button_group.addButton(rb_adv_flat, 0)
        self.advanced_cap_style_button_group.addButton(rb_adv_square, 1)
        self.advanced_cap_style_button_group.addButton(rb_adv_round, 2)
        hs_adv_cs.addWidget(rb_adv_flat)
        hs_adv_cs.addWidget(rb_adv_square)
        hs_adv_cs.addWidget(rb_adv_round)
        self.advanced_cap_style_group.setLayout(hs_adv_cs)
        self.advanced_cap_style_button_group.button(
            self.config.advanced_cap_style
        ).setChecked(True)
        self.advanced_cap_style_button_group.buttonClicked.connect(
            self.onParameterChanged
        )
        advanced_form.addRow(self.advanced_cap_style_group)
        self.advanced_group.toggled.connect(self.onParameterChanged)
        param_layout.addWidget(self.advanced_group)
        splitter.addWidget(param_container)
        splitter.setStretchFactor(1, 2)
        left_layout.addWidget(splitter)
        # 导出按钮
        self.export_btn = QtWidgets.QPushButton("导出准星")
        self.export_btn.clicked.connect(self.exportCrosshair)
        left_layout.addWidget(self.export_btn)
        main_layout.addWidget(left_widget, stretch=2)
        # 右侧：历史记录
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.addWidget(QtWidgets.QLabel("历史准星记录："))
        self.history_list = QtWidgets.QListWidget()
        self.history_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(
            self.show_history_context_menu
        )
        self.history_list.itemClicked.connect(self.importCrosshair)
        right_layout.addWidget(self.history_list, stretch=1)
        self.refreshHistory_btn = QtWidgets.QPushButton("刷新列表")
        self.refreshHistory_btn.clicked.connect(self.loadExportedCrosshairs)
        right_layout.addWidget(self.refreshHistory_btn)
        main_layout.addWidget(right_widget, stretch=1)
        self.loadExportedCrosshairs()

    def onParameterChanged(self, _=None):
        self.config.inner_gap = int(self.inner_gap_slider.getValue())
        self.config.inner_length = int(self.inner_length_slider.getValue())
        self.config.inner_thickness = int(self.inner_thickness_slider.getValue())
        self.config.inner_color = self.inner_color_edit.text().strip()
        self.config.inner_opacity = self.inner_opacity_slider.getValue()
        self.config.inner_line_count = int(self.inner_line_count_slider.getValue())
        self.config.center_enabled = self.center_group.isChecked()
        self.config.center_color = self.center_color_edit.text().strip()
        self.config.center_thickness = int(self.center_thickness_slider.getValue())
        self.config.outer_frame_enabled = self.outer_frame_group.isChecked()
        self.config.outer_frame_color = self.outer_frame_color_edit.text().strip()
        self.config.outer_frame_opacity = self.outer_frame_opacity_slider.getValue()
        self.config.outer_frame_thickness = int(
            self.outer_frame_thickness_slider.getValue()
        )
        self.config.outer_cross_enabled = self.outer_cross_group.isChecked()
        self.config.outer_gap = int(self.outer_gap_slider.getValue())
        self.config.outer_length = int(self.outer_length_slider.getValue())
        self.config.outer_thickness = int(self.outer_thickness_slider.getValue())
        self.config.outer_cross_color = self.outer_cross_color_edit.text().strip()
        self.config.outer_cross_opacity = self.outer_cross_opacity_slider.getValue()
        self.config.outer_line_count = int(self.outer_line_count_slider.getValue())
        self.config.advanced_enabled = self.advanced_group.isChecked()
        self.config.inner_angle_offset = int(self.inner_angle_slider.getValue())
        self.config.offset_x = int(self.offsetx_slider.getValue())
        self.config.offset_y = int(self.offsety_slider.getValue())
        self.config.overall_angle_offset = int(self.overall_angle_slider.getValue())
        self.config.advanced_cap_style = (
            self.advanced_cap_style_button_group.checkedId()
        )
        self.preview.updateConfig(self.config)

    def chooseInnerColor(self):
        col = QtWidgets.QColorDialog.getColor(
            QtGui.QColor(self.inner_color_edit.text()), self, "选择颜色"
        )
        if col.isValid():
            self.inner_color_edit.setText(col.name())
            self.onParameterChanged()

    def chooseCenterColor(self):
        col = QtWidgets.QColorDialog.getColor(
            QtGui.QColor(self.center_color_edit.text()), self, "选择颜色"
        )
        if col.isValid():
            self.center_color_edit.setText(col.name())
            self.onParameterChanged()

    def chooseOuterFrameColor(self):
        col = QtWidgets.QColorDialog.getColor(
            QtGui.QColor(self.outer_frame_color_edit.text()), self, "选择颜色"
        )
        if col.isValid():
            self.outer_frame_color_edit.setText(col.name())
            self.onParameterChanged()

    def chooseOuterCrossColor(self):
        col = QtWidgets.QColorDialog.getColor(
            QtGui.QColor(self.outer_cross_color_edit.text()), self, "选择颜色"
        )
        if col.isValid():
            self.outer_cross_color_edit.setText(col.name())
            self.onParameterChanged()

    def exportCrosshair(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "导出准星", "请输入准星名称：")
        if not ok or not name.strip():
            return
        code = self.config.encode()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_entry = {"name": name.strip(), "code": code, "timestamp": timestamp}
        exports = []
        if os.path.exists(self.export_file):
            try:
                with open(self.export_file, "r", encoding="utf-8") as f:
                    exports = json.load(f)
            except:
                exports = []
        exports.append(export_entry)
        with open(self.export_file, "w", encoding="utf-8") as f:
            json.dump(exports, f, ensure_ascii=False, indent=4)
        QtWidgets.QMessageBox.information(
            self, "导出成功", f"准星已导出。\n代码: {code}"
        )
        self.loadExportedCrosshairs()

    def loadExportedCrosshairs(self):
        self.history_list.clear()
        exports = []
        if os.path.exists(self.export_file):
            try:
                with open(self.export_file, "r", encoding="utf-8") as f:
                    exports = json.load(f)
            except:
                exports = []
        exports = sorted(exports, key=lambda x: x["timestamp"], reverse=True)
        for entry in exports:
            text = f"{entry['name']} - {entry['code']}"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, entry)
            self.history_list.addItem(item)

    def importCrosshair(self, item):
        entry = item.data(QtCore.Qt.UserRole)
        try:
            config = CrosshairConfig.decode(entry["code"])
            
            # 为防止信号触发干扰，暂时屏蔽信号
            self.center_group.blockSignals(True)
            self.outer_frame_group.blockSignals(True)
            self.outer_cross_group.blockSignals(True)
            self.advanced_group.blockSignals(True)
            
            self.center_group.setChecked(config.center_enabled)
            self.outer_frame_group.setChecked(config.outer_frame_enabled)
            self.outer_cross_group.setChecked(config.outer_cross_enabled)
            self.advanced_group.setChecked(config.advanced_enabled)
            
            self.center_group.blockSignals(False)
            self.outer_frame_group.blockSignals(False)
            self.outer_cross_group.blockSignals(False)
            self.advanced_group.blockSignals(False)
            

            self.inner_gap_slider.setValue(config.inner_gap)
            self.inner_length_slider.setValue(config.inner_length)
            self.inner_thickness_slider.setValue(config.inner_thickness)
            self.inner_color_edit.setText(config.inner_color)
            self.inner_opacity_slider.setValue(int(round(config.inner_opacity * 10)))
            self.inner_line_count_slider.setValue(config.inner_line_count)
            
            self.center_color_edit.setText(config.center_color)
            self.center_thickness_slider.setValue(config.center_thickness)
            
            self.outer_frame_color_edit.setText(config.outer_frame_color)
            self.outer_frame_opacity_slider.setValue(int(round(config.outer_frame_opacity * 10)))
            self.outer_frame_thickness_slider.setValue(config.outer_frame_thickness)
            
            self.outer_gap_slider.setValue(config.outer_gap)
            self.outer_length_slider.setValue(config.outer_length)
            self.outer_thickness_slider.setValue(config.outer_thickness)
            self.outer_cross_color_edit.setText(config.outer_cross_color)
            self.outer_cross_opacity_slider.setValue(int(round(config.outer_cross_opacity * 10)))
            self.outer_line_count_slider.setValue(config.outer_line_count)
            
            self.inner_angle_slider.setValue(config.inner_angle_offset)
            self.offsetx_slider.setValue(config.offset_x)
            self.offsety_slider.setValue(config.offset_y)
            self.overall_angle_slider.setValue(config.overall_angle_offset)
            self.advanced_cap_style_button_group.button(config.advanced_cap_style).setChecked(True)
            
            # 更新当前配置并刷新预览
            self.config = config
            self.onParameterChanged()  # 该函数会从控件读取所有值，并更新预览
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "导入失败", str(e))

    def show_history_context_menu(self, pos):
        item = self.history_list.itemAt(pos)
        if item is None:
            return
        menu = QtWidgets.QMenu(self)
        copy_action = menu.addAction("复制代码")
        delete_action = menu.addAction("删除")
        set_default_action = menu.addAction("设为默认")
        action = menu.exec(self.history_list.mapToGlobal(pos))
        if action == copy_action:
            entry = item.data(QtCore.Qt.UserRole)
            code = entry.get("code", "")
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(code)
        elif action == delete_action:
            self.delete_history_item(item)
        elif action == set_default_action:
            self.set_default_history_item(item)

    def delete_history_item(self, item):
        entry = item.data(QtCore.Qt.UserRole)
        reply = QtWidgets.QMessageBox.question(
            self,
            "删除确认",
            f"确定删除“{entry['name']}”吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            exports = []
            if os.path.exists(self.export_file):
                try:
                    with open(self.export_file, "r", encoding="utf-8") as f:
                        exports = json.load(f)
                except:
                    exports = []
            exports = [e for e in exports if e["timestamp"] != entry["timestamp"]]
            with open(self.export_file, "w", encoding="utf-8") as f:
                json.dump(exports, f, ensure_ascii=False, indent=4)
            self.loadExportedCrosshairs()

    def set_default_history_item(self, item):
        entry = item.data(QtCore.Qt.UserRole)
        try:
            config = CrosshairConfig.decode(entry["code"])
            last_config_path = os.path.join(os.getcwd(), "last_config.json")
            with open(last_config_path, "w", encoding="utf-8") as f:
                json.dump(config.to_dict(), f, ensure_ascii=False, indent=4)
            QtWidgets.QMessageBox.information(
                self, "设为默认", f"已将“{entry['name']}”设为默认准星。"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "操作失败", str(e))


# ----------------------------
# 主窗口
# ----------------------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("准星编辑器")
        self.resize(1100, 750)
        self.editor = CrosshairEditor(self)
        self.setCentralWidget(self.editor)


# ----------------------------
# 主函数
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="准星编辑器与显示工具")
    parser.add_argument(
        "--nogui", action="store_true", help="启动无编辑器模式，仅在屏幕上显示准星"
    )
    parser.add_argument(
        "config_str", nargs="?", default=None, help="准星参数代码字符串"
    )
    args = parser.parse_args()
    if args.nogui:
        if args.config_str:
            try:
                config = CrosshairConfig.decode(args.config_str)
            except Exception as e:
                print("解析准星代码失败:", e)
                sys.exit(1)
        else:
            last_config_path = os.path.join(os.getcwd(), "last_config.json")
            if os.path.exists(last_config_path):
                try:
                    with open(last_config_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    config = CrosshairConfig.from_dict(data)
                except Exception as e:
                    print("加载上次准星配置失败:", e)
                    sys.exit(1)
            else:
                print("未提供准星代码且没有上次导出的配置。")
                sys.exit(1)
        app = QtWidgets.QApplication(sys.argv)
        overlay = OverlayWindow(config)
        overlay.showFullScreen()

        def exit_callback():
            QtCore.QMetaObject.invokeMethod(
                QtWidgets.QApplication.instance(), "quit", QtCore.Qt.QueuedConnection
            )

        def toggle_visibility_callback():
            if overlay.isVisible():
                overlay.hide()
            else:
                overlay.showFullScreen()

        keyboard.add_hotkey("ctrl+alt+f9", exit_callback)
        keyboard.add_hotkey("ctrl+alt+f10", toggle_visibility_callback)
        sys.exit(app.exec())
    else:
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle("Fusion")
        style = """
        QMainWindow { background-color: #F5F5F5; }
        QWidget { font-family: 'Roboto', sans-serif; font-size: 14px; }
        QPushButton {
            background-color: #2196F3; color: white; border: none; border-radius: 6px; padding: 8px 16px;
        }
        QPushButton:hover { background-color: #1976D2; }
        QPushButton:pressed { background-color: #1565C0; }
        QLineEdit, QComboBox {
            background-color: white; border: 1px solid #BDBDBD; border-radius: 6px; padding: 4px;
        }
        QSlider::groove:horizontal {
            height: 8px; background: #E0E0E0; border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #2196F3; border: none; height: 20px; width: 20px; margin: -6px 0; border-radius: 10px;
        }
        QListWidget {
            background-color: white; border: 1px solid #BDBDBD; border-radius: 6px;
        }
        QGroupBox { border: 1px solid #BDBDBD; border-radius: 6px; margin-top: 6px; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }
        """
        app.setStyleSheet(style)
        mainWin = MainWindow()
        mainWin.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    # version = "0.0.0220"
    main()
