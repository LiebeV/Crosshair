#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6 import QtWidgets
from crosshair_editor import CrosshairEditor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("准星编辑器")
        self.resize(1100, 750)
        self.editor = CrosshairEditor(self)
        self.setCentralWidget(self.editor)
