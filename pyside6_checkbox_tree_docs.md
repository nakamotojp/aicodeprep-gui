# PySide6: Multi-State Checkbox Tree (QTreeWidget/QTreeView) – Research & Implementation Notes

## 1. Standard Checkbox Support

- `QTreeWidget` and `QTreeView` support checkboxes via the `Qt.CheckStateRole` in the model.
- The built-in states are:
  - `Qt.Unchecked`
  - `Qt.Checked`
- Example (from docs):
  ```python
  if role == Qt.CheckStateRole and index.row() == 1 and index.column() == 0:
      return Qt.CheckState.Checked
  ```

## 2. Limitation: Only 2 States by Default

- Qt's standard checkboxes only support 2 states (checked/unchecked).
- For more states (e.g., "skeleton" or custom), you must implement a custom solution.

## 3. Custom Multi-State Checkbox Implementation

### a. Subclass QStyledItemDelegate

- Override `paint()` to draw custom icons for each state (e.g., unchecked, checked, skeleton, ...).
- Override `editorEvent()` to handle mouse clicks and cycle through states.

#### Example Skeleton (not from docs, but required for >2 states):

```python
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import Qt, QModelIndex

class MultiStateCheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        state = index.data(Qt.CheckStateRole)
        # Draw custom icon based on state (0, 1, 2, ...)
        # Use QPixmap or QIcon for each state

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease:
            state = index.data(Qt.CheckStateRole) or 0
            next_state = (state + 1) % 3  # For 3 states: 0, 1, 2
            model.setData(index, next_state, Qt.CheckStateRole)
            return True
        return False
```

- Assign the delegate to your tree:
  ```python
  tree.setItemDelegateForColumn(0, MultiStateCheckboxDelegate(tree))
  ```

### b. Store State in Model

- Use `Qt.CheckStateRole` to store an integer (0, 1, 2, ...).
- The delegate interprets this value and draws the appropriate icon.

### c. Custom Icons

- Use `QPixmap` or `QIcon` for each state (e.g., checkmark, skeleton, placeholder).
- You can load icons from files or generate them programmatically.

### d. Example: QStandardItemModel Tree

```python
from PySide6.QtGui import QStandardItem, QStandardItemModel

model = QStandardItemModel()
item = QStandardItem("File.txt")
item.setData(0, Qt.CheckStateRole)  # Start at state 0
model.appendRow(item)
```

## 4. Related PySide6/Qt Classes

- `QTreeWidget`, `QTreeView`
- `QStandardItemModel`, `QAbstractItemModel`
- `QStyledItemDelegate`
- `Qt.CheckStateRole`

## 5. Useful Doc Snippets

- [QTreeView API Reference](https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/dirview/README.md#_snippet_1)
- [Custom Delegate Example](https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/itemviews/stardelegate/README.md#_snippet_5)
- [QStandardItemModel Tree Setup](https://github.com/fernicar/pyside6_examples_doc_2025_v6.9.1/blob/6.9.1/examples/widgets/tutorials/modelview/README.md#_snippet_5)

## 6. State Persistence

- Use `QSettings` to persist user state (see "State Persistence with QSettings" in docs).

## 7. Summary

- Out-of-the-box, only 2-state checkboxes are supported.
- For 3+ states, subclass `QStyledItemDelegate`, override `paint` and `editorEvent`, and use custom icons.
- Store the state as an integer in the model using `Qt.CheckStateRole`.
- Assign your delegate to the tree to enable multi-state cycling on click.
