#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtCore, QtGui
from crosshair_preview import CrosshairPreview

class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("准星")
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool
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
