The goal: The test checkbox will now just toggle between displaying "pro toggle test 1" and "pro toggle test 2" at the bottom of the UI, without affecting the actual Pro mode state. The Pro mode will only be enabled by the `--pro` command line argument, and the checkbox will be greyed out when Pro is not enabled.

Here are the changes needed:

1. **Remove the banner modification logic** from the Pro patches
2. **Update the GUI to show the test text** instead of modifying the banner
3. **Update the checkbox behavior** to just toggle the test text
4. **Keep the checkbox greyed out** when Pro is not enabled via command line

Let me make these changes:

## 1. Update aicodeprep_gui/pro/patches.py

Since we're no longer using the banner modification, we can simplify this file:

```python
"""UI patches for Pro mode - now just a placeholder since we're not modifying the banner."""
def patch_banner(label):
    """No longer needed - banner stays the same regardless of toggle state."""
    pass
```

## 2. Update aicodeprep_gui/gui.py

Find the section where the checkbox is created and update it:

```python
# Replace the existing pro_toggle setup with this:

# Add a label for the test text
self.pro_test_label = QtWidgets.QLabel("")
self.pro_test_label.setAlignment(QtCore.Qt.AlignCenter)
self.pro_test_label.setVisible(False)  # Initially hidden

# Update the checkbox setup
self.pro_toggle = QtWidgets.QCheckBox("Pro toggle test")
self.pro_toggle.setChecked(False)  # Start with test 1
self.pro_toggle.setEnabled(pro.enabled)  # Greyed out if --pro not used
if pro.enabled:
    self.pro_test_label.setText("pro toggle test 1")
    self.pro_test_label.setVisible(True)

# Update the connection
self.pro_toggle.toggled.connect(self._toggle_pro_test)

# Add the test label to the premium content layout
premium_content_layout.addWidget(self.pro_toggle)
premium_content_layout.addWidget(self.pro_test_label)
```

## 3. Add the new toggle method

Replace the existing `_toggle_pro` method with this new one:

```python
def _toggle_pro_test(self, checked):
    """Toggle between test 1 and test 2 text display."""
    if checked:
        self.pro_test_label.setText("pro toggle test 2")
    else:
        self.pro_test_label.setText("pro toggle test 1")
```

## 4. Update the banner creation to always use the same style

In the GUI initialization, modify the banner section:

```python
# Remove the Pro banner modification
self.vibe_label = QtWidgets.QLabel("AI Code Prep GUI")
vibe_font = QtGui.QFont(self.default_font)
vibe_font.setBold(True)
vibe_font.setPointSize(self.default_font.pointSize() + 8)
self.vibe_label.setFont(vibe_font)
self.vibe_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
self.vibe_label.setStyleSheet(
    "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #40203f, stop:1 #1f103f); "
    "color: white; padding: 0px 0px 0px 0px; border-radius: 8px;"
)
self.vibe_label.setFixedHeight(44)
# Remove the Pro banner patch call
```

## 5. Update the checkbox text and tooltip

Update the checkbox creation:

```python
self.pro_toggle = QtWidgets.QCheckBox("Pro toggle test")
self.pro_toggle.setToolTip("Toggle between test 1 and test 2 display")
```

These changes will:

- Remove the banner color change functionality
- Make the checkbox toggle between "pro toggle test 1" and "pro toggle test 2" text at the bottom
- Keep the checkbox greyed out when `--pro` is not used
- Ensure Pro mode is only enabled by the `--pro` command line argument

The test text will appear below the checkbox in the Premium Features section, making it clear that this is just a test toggle without affecting the actual Pro functionality.
