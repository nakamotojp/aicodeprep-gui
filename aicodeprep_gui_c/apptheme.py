from PySide6 import QtCore, QtGui, QtWidgets
import platform
import os
import sys
import ctypes
import json

def system_pref_is_dark() -> bool:
    """Detect if system is using dark mode."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            import subprocess
            cmd = "defaults read -g AppleInterfaceStyle"
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            return result.stdout.strip() == "Dark"
        except:
            pass
    
    elif system == "Windows":  # Windows 10+
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            reg_keypath = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            key = winreg.OpenKey(registry, reg_keypath)
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except:
            pass
    
    # Fallback: use palette heuristic
    return QtWidgets.QApplication.palette().color(QtGui.QPalette.Window).lightness() < 128

def apply_dark_palette(app: QtWidgets.QApplication):
    """Apply dark color palette to application."""
    dark = QtGui.QPalette()
    dark.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
    dark.setColor(QtGui.QPalette.Base, QtGui.QColor(42, 42, 42))
    dark.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(66, 66, 66))
    dark.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(53, 53, 53))
    dark.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
    dark.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
    dark.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
    dark.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    dark.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))
    
    # Disabled colors
    dark.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(128, 128, 128))
    dark.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(128, 128, 128))
    dark.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(128, 128, 128))
    
    app.setPalette(dark)

def apply_light_palette(app: QtWidgets.QApplication):
    """Apply light color palette to application."""
    light = QtGui.QPalette()
    light.setColor(QtGui.QPalette.Window, QtGui.QColor(240, 240, 240))
    light.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
    light.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
    light.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(233, 233, 233))
    light.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 255))
    light.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(0, 0, 0))
    light.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 0, 0))
    light.setColor(QtGui.QPalette.Button, QtGui.QColor(240, 240, 240))
    light.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))
    light.setColor(QtGui.QPalette.Link, QtGui.QColor(0, 0, 255))
    light.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    light.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))
    
    # Disabled colors
    light.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(120, 120, 120))
    light.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(120, 120, 120))
    light.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(120, 120, 120))
    
    app.setPalette(light)
