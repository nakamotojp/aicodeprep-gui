# Qt: Multi-State Checkbox Tree (QTreeWidget/QTreeView) – Research & Implementation Notes

## 1. Built-in Tristate Support

- Qt checkboxes and tree items support a `tristate` property:
  - `Qt.Unchecked`
  - `Qt.PartiallyChecked`
  - `Qt.Checked`
- Enable tristate with:
  ```python
  checkbox.setTristate(True)
  ```
  or for items:
  ```python
  item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
  item.setCheckState(0, Qt.PartiallyChecked)
  ```

## 2. Limitation: Only 3 States by Default

- The built-in tristate only supports 3 states.
- For more than 3 states, you must implement a custom delegate.

## 3. Custom Multi-State Checkbox Implementation

### a. Subclass QStyledItemDelegate

- Override `paint()` to draw custom icons for each state.
- Override `editorEvent()` to handle mouse clicks and cycle through all desired states.

#### Example Skeleton (for N states):

```python
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import Qt

class MultiStateCheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        state = index.data(Qt.CheckStateRole)
        # Draw custom icon for each state (0, 1, 2, ...)

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease:
            state = index.data(Qt.CheckStateRole) or 0
            next_state = (state + 1) % N  # N = number of states
            model.setData(index, next_state, Qt.CheckStateRole)
            return True
        return False
```

### b. Store State in Model

- Use `Qt.CheckStateRole` to store an integer for the current state.
- The delegate interprets this value and draws the appropriate icon.

### c. Custom Icons

- Use `QPixmap` or `QIcon` for each state (checked, unchecked, skeleton, etc.).
- You can load icons from files or generate them programmatically.

## 4. QML/QtQuick Tristate

- QML CheckBox and CheckDelegate support `tristate: true` and a `checkState` property with 3 values.
- For more than 3 states, use a custom `nextCheckState` callback to cycle through additional states.

## 5. Useful Doc Snippets

- [QCheckBox.tristate](https://doc.qt.io/qtforpython-6.5/PySide6/QtWidgets/QCheckBox)
- [QTreeWidgetItem.setCheckState](https://doc.qt.io/qtforpython-6.5/PySide6/QtWidgets/QTreeWidgetItem)
- [QStandardItem.setUserTristate](https://doc.qt.io/qt-6/qstandarditem)
- [QStyledItemDelegate](https://doc.qt.io/archives/qt-5.15/modelview)
- [QML CheckBox](https://doc.qt.io/qt-6/qml-qtquick-controls-checkbox)
- [QML CheckDelegate](https://doc.qt.io/qt-6/qml-qtquick-controls-checkdelegate)

## 6. Summary

- Qt supports up to 3 states natively (unchecked, partially checked, checked).
- For more than 3 states, subclass QStyledItemDelegate and manage state cycling and drawing.
- Store the state as an integer in the model using `Qt.CheckStateRole`.
- Use custom icons for each state.
- In QML, use `nextCheckState` for custom cycling logic.
