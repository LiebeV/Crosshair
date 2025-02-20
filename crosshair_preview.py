#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from PySide6 import QtWidgets, QtCore, QtGui
from crosshair_config import CrosshairConfig

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
        effective_inner_angle = self.config.overall_angle_offset + self.config.inner_angle_offset
        # 绘制外框（对内侧准星描边）
        if self.config.outer_frame_enabled:
            pen_frame = QtGui.QPen(QtGui.QColor(self.config.outer_frame_color), self.config.outer_frame_thickness)
            col_frame = QtGui.QColor(self.config.outer_frame_color)
            col_frame.setAlphaF(self.config.outer_frame_opacity)
            pen_frame.setColor(col_frame)
            painter.setPen(pen_frame)
            for i in range(self.config.inner_line_count):
                angle_deg = effective_inner_angle + (360 / self.config.inner_line_count) * i
                angle_rad = math.radians(angle_deg)
                x1 = math.cos(angle_rad) * self.config.inner_gap
                y1 = math.sin(angle_rad) * self.config.inner_gap
                x2 = math.cos(angle_rad) * (self.config.inner_gap + self.config.inner_length)
                y2 = math.sin(angle_rad) * (self.config.inner_gap + self.config.inner_length)
                painter.drawLine(
                    QtCore.QPointF(center.x() + x1, center.y() + y1),
                    QtCore.QPointF(center.x() + x2, center.y() + y2),
                )
        # 绘制内侧十字准星
        pen_inner = QtGui.QPen(QtGui.QColor(self.config.inner_color), self.config.inner_thickness)
        col_inner = QtGui.QColor(self.config.inner_color)
        col_inner.setAlphaF(self.config.inner_opacity)
        pen_inner.setColor(col_inner)
        painter.setPen(pen_inner)
        for i in range(self.config.inner_line_count):
            angle_deg = effective_inner_angle + (360 / self.config.inner_line_count) * i
            angle_rad = math.radians(angle_deg)
            x1 = math.cos(angle_rad) * self.config.inner_gap
            y1 = math.sin(angle_rad) * self.config.inner_gap
            x2 = math.cos(angle_rad) * (self.config.inner_gap + self.config.inner_length)
            y2 = math.sin(angle_rad) * (self.config.inner_gap + self.config.inner_length)
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
            pen_outer = QtGui.QPen(QtGui.QColor(self.config.outer_cross_color), self.config.outer_thickness)
            col_outer = QtGui.QColor(self.config.outer_cross_color)
            col_outer.setAlphaF(self.config.outer_cross_opacity)
            pen_outer.setColor(col_outer)
            painter.setPen(pen_outer)
            for i in range(self.config.outer_line_count):
                angle_deg = effective_outer_angle + (360 / self.config.outer_line_count) * i
                angle_rad = math.radians(angle_deg)
                x1 = math.cos(angle_rad) * self.config.outer_gap
                y1 = math.sin(angle_rad) * self.config.outer_gap
                x2 = math.cos(angle_rad) * (self.config.outer_gap + self.config.outer_length)
                y2 = math.sin(angle_rad) * (self.config.outer_gap + self.config.outer_length)
                painter.drawLine(
                    QtCore.QPointF(center.x() + x1, center.y() + y1),
                    QtCore.QPointF(center.x() + x2, center.y() + y2),
                )
        painter.end()
