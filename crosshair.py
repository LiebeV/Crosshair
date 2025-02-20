#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json, argparse
from PySide6 import QtWidgets, QtCore
import keyboard

from crosshair_config import CrosshairConfig
from overlay_window import OverlayWindow
from main_window import MainWindow

def main():
    parser = argparse.ArgumentParser(description="准星编辑器与显示工具")
    parser.add_argument("--nogui", action="store_true", help="启动无编辑器模式，仅在屏幕上显示准星")
    parser.add_argument("config_str", nargs="?", default=None, help="准星参数代码字符串")
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
            QtCore.QMetaObject.invokeMethod(QtWidgets.QApplication.instance(), "quit", QtCore.Qt.QueuedConnection)

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
    # version 0.0.0220
    main()
