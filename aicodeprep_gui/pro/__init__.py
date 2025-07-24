"""Premium plugin loader."""
import os
import sys

# Check if pro mode is enabled
enabled = '--pro' in sys.argv or os.path.isfile('pro_enabled')

# Preview window instance
_preview_window = None

def get_preview_window():
    """Get the global preview window instance."""
    global _preview_window
    if enabled and _preview_window is None:
        from .preview_window import FilePreviewDock
        _preview_window = FilePreviewDock()
    return _preview_window
