import logging
from PySide6 import QtWidgets, QtGui, QtCore

"""
MultiStateLevelDelegate
-----------------------

A QStyledItemDelegate for rendering and interacting with a 5-state indicator in
a QTreeWidget/QTreeView column. Each state is represented by a colored square,
and clicking cycles through the states (0..4). State is stored on the item
using a custom data role (LEVEL_ROLE), keeping it separate from the standard
checkbox logic on column 0.

Key points:
- Column target: intended for column 1 in the tree.
- State storage: integer 0..4 in LEVEL_ROLE (Qt.UserRole + 1).
- Painting: draws a 16x16 rounded square centered in the cell.
- Interaction: left click cycles state modulo 5.

How to customize the visual:
- Change COLORS_LIGHT mapping below to use different colors.
- Replace the fill with icons:
    * Load a QPixmap/QIcon and draw it inside the `rect` returned by
      _indicator_rect(option) using painter.drawPixmap(...) or icon.paint(...).
- Draw dynamic graphics:
    * Use QPainterPath, gradients, or custom shapes in the `paint()` method.
- Size and position:
    * Adjust BOX_SIZE and _indicator_rect to control size/position.

How to customize interaction:
- Modify editorEvent() to:
    * Skip cycling on double click.
    * Use right-click or keyboard events to change state.
    * Open a popup menu to select a specific state.

Why use a delegate:
- Qt’s native checkbox supports 2 or 3 states only. A delegate allows arbitrary
  visual and interaction logic while keeping the existing model intact.
"""

# Custom data role for the 5-state level column
LEVEL_ROLE = QtCore.Qt.UserRole + 1


class MultiStateLevelDelegate(QtWidgets.QStyledItemDelegate):
    """
    Delegate for rendering and editing a 5-state colored indicator in column 1.

    Stores the state (0..4) as an int in LEVEL_ROLE on column 1. This does not
    affect the built-in checkbox in column 0 and uses a separate role to avoid
    conflicts.

    States (default colors):
      0: neutral/none (gray)
      1: blue
      2: green
      3: gold
      4: orange-red

    Customization tips:
    - To use icons instead of colors:
        icon = QtGui.QIcon(":/path/to/icon.png")
        icon.paint(painter, rect)
      Or:
        pix = QtGui.QPixmap(":/path/to/icon.png")
        painter.drawPixmap(rect.adjusted(1,1,-1,-1), pix)
    - To generate icons programmatically, use QPainter on a QPixmap and cache
      the results in the delegate instance to avoid re-rendering on every paint.
    """
    BOX_SIZE = 16
    PADDING = 2

    COLORS_LIGHT = {
        0: QtGui.QColor("#A0A0A0"),     # gray
        1: QtGui.QColor("#1E90FF"),     # dodgerblue
        2: QtGui.QColor("#32CD32"),     # limegreen
        3: QtGui.QColor("#FFD700"),     # gold
        4: QtGui.QColor("#FF4500"),     # orangered
    }

    BORDER_LIGHT = QtGui.QColor("#666666")
    BORDER_DARK = QtGui.QColor("#BBBBBB")

    def __init__(self, parent=None, is_dark_mode: bool = False):
        super().__init__(parent)
        self.is_dark_mode = is_dark_mode

    def _indicator_rect(self, option: QtWidgets.QStyleOptionViewItem) -> QtCore.QRect:
        """
        Compute the rectangle where the indicator should be drawn.

        By default this centers a BOX_SIZE x BOX_SIZE square inside the cell.
        Adjust this to shift the indicator left/right or change its size.
        """
        r = option.rect
        size = self.BOX_SIZE
        x = r.x() + (r.width() - size) // 2
        y = r.y() + (r.height() - size) // 2
        return QtCore.QRect(x, y, size, size)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        """
        Paint the cell content.

        Default behavior:
        - Let the base style draw the cell background/selection.
        - Draw a rounded rectangle filled with a color mapping for the state.
        To use icons, replace the fill/drawPath code with icon painting.
        """
        if index.column() != 1:
            # Default paint for other columns
            return super().paint(painter, option, index)

        # Fetch current state, default to 0
        state = index.data(LEVEL_ROLE)
        if state is None:
            state = 0
        try:
            state = int(state)
        except Exception:
            state = 0
        state = max(0, min(4, state))

        # Prepare style
        painter.save()
        # Ensure background/selection is drawn by base style first
        opt = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        style = QtWidgets.QApplication.style() if opt.widget is None else opt.widget.style()
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem,
                          opt, painter, opt.widget)

        rect = self._indicator_rect(option)
        color = self.COLORS_LIGHT.get(state, self.COLORS_LIGHT[0])

        # Draw rounded rect with fill color and border
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(rect), 3, 3)

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.fillPath(path, QtGui.QBrush(color))

        border_color = self.BORDER_DARK if self.is_dark_mode else self.BORDER_LIGHT
        pen = QtGui.QPen(border_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.restore()

    def editorEvent(self,
                    event: QtCore.QEvent,
                    model: QtCore.QAbstractItemModel,
                    option: QtWidgets.QStyleOptionViewItem,
                    index: QtCore.QModelIndex) -> bool:
        """
        Handle mouse/keyboard events to change state.

        Current behavior:
        - On left mouse press/release within the indicator rect, cycle state: (current + 1) % 5.
        - Writes state back using LEVEL_ROLE to keep it separate from column 0 checkbox.

        To change interaction patterns:
        - Check for QtCore.QEvent.KeyPress and handle keys to increment/decrement.
        - Use context menus on right click to directly pick a specific state.
        """
        # Only handle clicks in column 1
        if index.column() != 1:
            return False

        if event.type() in (QtCore.QEvent.MouseButtonRelease, QtCore.QEvent.MouseButtonDblClick, QtCore.QEvent.MouseButtonPress):
            # Only react on Left click release within indicator rect
            if isinstance(event, QtGui.QMouseEvent):
                if event.button() != QtCore.Qt.LeftButton:
                    return False
                # For robustness, allow change on release or press
                if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonRelease:
                    indicator = self._indicator_rect(option)
                    if indicator.contains(event.position().toPoint()):
                        current = index.data(LEVEL_ROLE)
                        try:
                            current = int(
                                current) if current is not None else 0
                        except Exception:
                            current = 0
                        next_state = (current + 1) % 5
                        # Write back to model under our custom role
                        ok = model.setData(index, next_state, LEVEL_ROLE)
                        if not ok:
                            # If model refuses custom role, attempt to set via the item directly (for QTreeWidget)
                            try:
                                item = index.model().itemFromIndex(index)  # for QStandardItemModel
                                if item:
                                    item.setData(next_state, LEVEL_ROLE)
                                    ok = True
                            except Exception:
                                pass
                        return ok
        return False
