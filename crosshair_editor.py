#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from PySide6 import QtWidgets, QtCore, QtGui
from crosshair_config import CrosshairConfig
from slider_input import SliderInput
from crosshair_preview import CrosshairPreview

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
        self.inner_opacity_slider = SliderInput(0, 10, self.config.inner_opacity, is_float=True, scale=0.1)
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
        self.outer_frame_opacity_slider = SliderInput(0, 10, self.config.outer_frame_opacity, is_float=True, scale=0.1)
        self.outer_frame_opacity_slider.valueChanged.connect(self.onParameterChanged)
        outer_frame_form.addRow("不透明度:", self.outer_frame_opacity_slider)
        self.outer_frame_thickness_slider = SliderInput(1, 20, self.config.outer_frame_thickness)
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
        self.outer_cross_opacity_slider = SliderInput(0, 10, self.config.outer_cross_opacity, is_float=True, scale=0.1)
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
        self.overall_angle_slider = SliderInput(0, 360, self.config.overall_angle_offset)
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
        self.advanced_cap_style_button_group.button(self.config.advanced_cap_style).setChecked(True)
        self.advanced_cap_style_button_group.buttonClicked.connect(self.onParameterChanged)
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
        self.history_list.customContextMenuRequested.connect(self.show_history_context_menu)
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
        self.config.outer_frame_thickness = int(self.outer_frame_thickness_slider.getValue())
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
        self.config.advanced_cap_style = self.advanced_cap_style_button_group.checkedId()
        self.preview.updateConfig(self.config)

    def chooseInnerColor(self):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.inner_color_edit.text()), self, "选择颜色")
        if col.isValid():
            self.inner_color_edit.setText(col.name())
            self.onParameterChanged()

    def chooseCenterColor(self):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.center_color_edit.text()), self, "选择颜色")
        if col.isValid():
            self.center_color_edit.setText(col.name())
            self.onParameterChanged()

    def chooseOuterFrameColor(self):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.outer_frame_color_edit.text()), self, "选择颜色")
        if col.isValid():
            self.outer_frame_color_edit.setText(col.name())
            self.onParameterChanged()

    def chooseOuterCrossColor(self):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.outer_cross_color_edit.text()), self, "选择颜色")
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
        QtWidgets.QMessageBox.information(self, "导出成功", f"准星已导出。\n代码: {code}")
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
            
            # 先更新各功能组的选中状态
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
            
            # 更新各参数控件
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
            self.onParameterChanged()
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
            QtWidgets.QMessageBox.information(self, "设为默认", f"已将“{entry['name']}”设为默认准星。")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "操作失败", str(e))
