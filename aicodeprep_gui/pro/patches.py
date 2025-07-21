"""Tiny UI patches for Pro mode."""
from PySide6.QtGui import QLinearGradient, QColor

def patch_banner(label):
    """Switch banner to Pro colors & text."""
    gradient = QLinearGradient(0, 0, 1, 0)
    gradient.setColorAt(0, QColor("#00b894"))
    gradient.setColorAt(1, QColor("#00cec9"))
    label.setStyleSheet(
        "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00b894, stop:1 #00cec9);"
        "color: white; padding: 0px; border-radius: 8px;"
    )
    label.setText("AI Code Prep Pro")
