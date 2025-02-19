# 🎯 Crosshair Overlay

📄 [中文](README.md) 📄 [English](README_en.md)

A global crosshair tool for Windows that supports highly customizable parameters and hotkey operations. It offers both a GUI editor mode and a lightweight overlay mode.

⚠ **Disclaimer**

> **This tool overlays the screen display, which may pose an anti-cheat risk. By continuing to use this tool, you acknowledge the risks and take full responsibility. The author is not liable for any consequences.**

---

## ✨ Features

-   🎨 **Crosshair Editor**: Visually adjust spacing, line length, thickness, transparency, and 20+ other parameters. Feel free to suggest more options in the issues section.
-   🌈 **Customization**: Supports solid, dashed, and dotted lines, as well as inner, outer, and multi-ray layouts.
-   📥 **Configuration Management**: Import/export crosshair codes, save history, delete entries, and set defaults.
-   🖥️ **Global Overlay**: Borderless full-screen display with transparent click-through support and hotkey operations.
-   ⚙ **Dual Running Modes**:
    -   GUI Editor Mode (for customizing the crosshair).
    -   No-GUI Crosshair Overlay Mode (`--nogui`) for lightweight operation.

---

## 📌 Installation

```bash
git clone https://github.com/LiebeV/Crosshair.git
cd Crosshair
pip install -r requirements.txt
```

It is recommended to use **Python 3.8+**, and the program has been optimized for Windows compatibility.

---

## 🚀 Quick Start

### **1️⃣ Editor Mode** (Recommended for first-time use)

```bash
python crosshair.py
```

-   This mode allows you to customize the crosshair, export its code, or set it as default for use in overlay mode.

### **2️⃣ Crosshair Overlay Mode** (No GUI, direct execution)

```bash
python crosshair.py --nogui "<config_str>"
```

-   Ideal for quickly loading a preset crosshair without an additional interface.

---

## ⚙ Parameter Description

| Parameter    | Description                                                |
| ------------ | ---------------------------------------------------------- |
| `--nogui`    | Runs the crosshair overlay in no-GUI mode                  |
| `config_str` | Crosshair code (preset in editor mode or manually entered) |

### 🎮 **Hotkeys**

-   **Ctrl + Alt + F9**: Exit the program
-   **Ctrl + Alt + F10**: Toggle show/hide

---

## 📜 License

This tool is released under the **LGPL-3.0 (PySide6) + MIT (keyboard)** open-source license.

---

## ❓ FAQ

### **🔹 Why is Python required? Will an EXE version be available?**

The tool is still in development, and an **EXE version** will be released in the future. Currently, only the source code is available.

### **🔹 Can the crosshair overlay only be started via command-line arguments?**

Yes, this allows for quick launching via **Win + R**, making it accessible in most scenarios.

### **🔹 Will there be a command prompt window when running the `.py` file?**

Yes, for now. This issue will be resolved in the future EXE version.

### **🔹 Will the tool be adapted for other operating systems?**

This tool is **developed exclusively for Windows**, and there are no plans to support other platforms.

---

💡 **Tip**: If you have feature requests or encounter bugs, feel free to submit an issue!

---
