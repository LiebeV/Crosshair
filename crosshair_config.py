#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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
        self.center_thickness = center_thickness if center_thickness is not None else inner_thickness
        self.outer_frame_enabled = outer_frame_enabled
        self.outer_frame_color = outer_frame_color if outer_frame_color is not None else inner_color
        self.outer_frame_opacity = outer_frame_opacity if outer_frame_opacity is not None else inner_opacity
        self.outer_frame_thickness = outer_frame_thickness if outer_frame_thickness is not None else inner_thickness
        self.outer_cross_enabled = outer_cross_enabled
        self.outer_gap = outer_gap
        self.outer_length = outer_length
        self.outer_thickness = outer_thickness
        self.outer_cross_color = outer_cross_color if outer_cross_color is not None else inner_color
        self.outer_cross_opacity = outer_cross_opacity if outer_cross_opacity is not None else inner_opacity
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
