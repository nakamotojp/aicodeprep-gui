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

def create_checkmark_pixmap(size=16, color="#0078D4"):
    """Create a checkmark pixmap programmatically."""
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtCore.Qt.transparent)
    
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    
    pen = QtGui.QPen(QtGui.QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(QtCore.Qt.RoundCap)
    pen.setJoinStyle(QtCore.Qt.RoundJoin)
    painter.setPen(pen)
    
    # Draw checkmark
    painter.drawLine(4, 8, 7, 11)
    painter.drawLine(7, 11, 12, 4)
    
    painter.end()
    return pixmap

def _checkbox_style_with_images(dark: bool) -> str:
    """Alternative approach using programmatically created images."""
    
    if dark:
        bg_unchecked = '#2B2B2B'
        bg_checked = '#2B2B2B'
        border_unchecked = '#555555'
        border_checked = '#0078D4'
        checkmark_color = '#0078D4'
    else:
        bg_unchecked = '#FFFFFF'
        bg_checked = '#FFFFFF'
        border_unchecked = '#AAAAAA'
        border_checked = '#0078D4'
        checkmark_color = '#0078D4'

    # Create checkmark image and save it temporarily
    import tempfile
    checkmark_pixmap = create_checkmark_pixmap(16, checkmark_color)
    temp_dir = tempfile.gettempdir()
    checkmark_path = os.path.join(temp_dir, f"checkmark_{'dark' if dark else 'light'}.png")
    checkmark_pixmap.save(checkmark_path)

    return f"""
    QTreeView::indicator, QTreeWidget::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 3px;
    }}

    QTreeView::indicator:unchecked,
    QTreeWidget::indicator:unchecked {{
        background-color: {bg_unchecked};
        border: 2px solid {border_unchecked};
    }}

    QTreeView::indicator:checked,
    QTreeWidget::indicator:checked {{
        background-color: {bg_checked};
        border: 2px solid {border_checked};
        image: url({checkmark_path.replace(os.sep, '/')});
    }}

    QTreeView::indicator:unchecked:hover,
    QTreeWidget::indicator:unchecked:hover {{
        border-color: {border_checked};
    }}
    """



def _checkbox_style(dark: bool) -> str:
    """Return a style-sheet that shows a visible tick using Unicode checkmarks."""
    
    if dark:
        bg_unchecked = '#2B2B2B'
        bg_checked = '#2B2B2B'
        border_unchecked = '#555555'
        border_checked = '#0078D4'
        checkmark_color = '#0078D4'
        disabled_bg = '#1F1F1F'
        disabled_border = '#3A3A3A'
    else:
        bg_unchecked = '#FFFFFF'
        bg_checked = '#FFFFFF'
        border_unchecked = '#AAAAAA'
        border_checked = '#0078D4'
        checkmark_color = '#0078D4'
        disabled_bg = '#F5F5F5'
        disabled_border = '#CCCCCC'

    return f"""
    QTreeView::indicator, QTreeWidget::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 3px;
    }}

    /* Unchecked state */
    QTreeView::indicator:unchecked,
    QTreeWidget::indicator:unchecked {{
        background-color: {bg_unchecked};
        border: 2px solid {border_unchecked};
    }}

    /* Checked state with Unicode checkmark */
    QTreeView::indicator:checked,
    QTreeWidget::indicator:checked {{
        background-color: {bg_checked};
        border: 2px solid {border_checked};
        color: {checkmark_color};
        font-weight: bold;
        font-size: 12px;
        text-align: center;
    }}

    QTreeView::indicator:checked::after,
    QTreeWidget::indicator:checked::after {{
        content: "✓";
        color: {checkmark_color};
        font-weight: bold;
        font-size: 12px;
        position: absolute;
        top: -1px;
        left: 1px;
    }}

    /* Disabled states */
    QTreeView::indicator:disabled,
    QTreeWidget::indicator:disabled {{
        background-color: {disabled_bg};
        border: 2px solid {disabled_border};
    }}

    /* Hover effects */
    QTreeView::indicator:unchecked:hover,
    QTreeWidget::indicator:unchecked:hover {{
        border-color: {border_checked};
        background-color: {bg_unchecked};
    }}

    QTreeView::indicator:checked:hover,
    QTreeWidget::indicator:checked:hover {{
        background-color: {bg_checked};
        border-color: {border_checked};
    }}
    """

def get_checkbox_style_dark()  -> str: 
    return _checkbox_style_with_images(True)

def get_checkbox_style_light() -> str: 
    return _checkbox_style_with_images(False)