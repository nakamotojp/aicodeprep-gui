# PySide6: Styling and Using QTreeWidget, File Trees, and Checkboxes

## 1. Importing QTreeWidget and QTreeWidgetItem

```python
import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
```

## 2. Defining Project Data Structure

```python
data = {"Project A": ["file_a.py", "file_a.txt", "something.xls"],
        "Project B": ["file_b.csv", "photo.jpg"],
        "Project C": []}
```

## 3. Configuring QTreeWidget Columns

```python
tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["Name", "Type"])
```

## 4. Populating QTreeWidget with Data

```python
items = []
for key, values in data.items():
    item = QTreeWidgetItem([key])
    for value in values:
        ext = value.split(".")[-1].upper()
        child = QTreeWidgetItem([value, ext])
        item.addChild(child)
    items.append(item)

tree.insertTopLevelItems(0, items)
```

## 5. Displaying Tree and Executing Application

```python
tree.show()
sys.exit(app.exec())
```

## 6. Initializing QApplication

```python
app = QApplication()
```

## 7. Styling with Qt Style Sheets

### Applying External Qt Style Sheet

```python
if __name__ == "__main__":
    app = QApplication()

    w = Widget()
    w.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
```

### Example .qss File

```css
QLabel {
  background-color: red;
}

QLabel#title {
  font-size: 20px;
}
```

### Inline Styling Example

```python
w.setStyleSheet("""
    background-color: #262626;
    color: #FFFFFF;
    font-family: Titillium;
    font-size: 18px;
    """)
```

## 8. CheckState/Checkbox in QTreeWidget

To add a checkbox to a QTreeWidgetItem:

```python
item.setCheckState(0, Qt.Checked)  # 0 = column index
```

You can use `Qt.Checked`, `Qt.Unchecked`, or `Qt.PartiallyChecked`.

## 9. Useful Links

- [TreeWidget Tutorial](https://github.com/pyside/pyside-setup/blob/dev/sources/pyside6/doc/tutorials/basictutorial/treewidget.rst)
- [Widget Styling](https://github.com/pyside/pyside-setup/blob/dev/sources/pyside6/doc/tutorials/basictutorial/widgetstyling.rst)
