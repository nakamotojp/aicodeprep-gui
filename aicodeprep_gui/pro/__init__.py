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


def get_level_delegate(parent, is_dark_mode: bool = False):
    """
    Return (delegate_instance, LEVEL_ROLE) if pro is enabled; otherwise None.

    The delegate renders a multi-state 'Level' indicator in column 1.
    """
    if not enabled:
        return None
    try:
        from .multi_state_level_delegate import ComboBoxLevelDelegate, LEVEL_ROLE
        return ComboBoxLevelDelegate(parent, is_dark_mode=is_dark_mode), LEVEL_ROLE
    except Exception as e:
        # Descriptive error for later debugging per .clinerules
        import logging
        logging.error(f"Failed to load Pro Level delegate: {e}")
        return None
