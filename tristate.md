A QCheckBox is an option button that can be switched on (checked) or off (unchecked). Checkboxes are typically used to represent features in an application that can be enabled or disabled without affecting others. Different types of behavior can be implemented. For example, a QButtonGroup can be used to group check buttons logically, allowing exclusive checkboxes. However, QButtonGroup does not provide any visual representation.

The image below further illustrates the differences between exclusive and non-exclusive checkboxes.

checkboxes-exclusive1

checkboxes-non-exclusive2

Whenever a checkbox is checked or cleared, it emits the signal checkStateChanged() . Connect to this signal if you want to trigger an action each time the checkbox changes state. You can use isChecked() to query whether or not a checkbox is checked.

In addition to the usual checked and unchecked states, QCheckBox optionally provides a third state to indicate “no change”. This is useful whenever you need to give the user the option of neither checking nor unchecking a checkbox. If you need this third state, enable it with setTristate() , and use checkState() to query the current toggle state.

Just like QPushButton , a checkbox displays text, and optionally a small icon. The icon is set with setIcon() . The text can be set in the constructor or with setText() . A shortcut key can be specified by preceding the preferred character with an ampersand. For example:

checkbox = QCheckBox("Case sensitive", self)
In this example, the shortcut is Alt+A. See the QShortcut documentation for details. To display an actual ampersand, use ‘&&’.

See also

QAbstractButton QRadioButton

Note

Properties can be used directly when from **feature** import true_property is used or via accessor functions otherwise.

property tristateᅟ: bool
This property holds whether the checkbox is a tri-state checkbox.

The default is false, i.e., the checkbox has only two states.

Access functions:
isTristate()

setTristate()

**init**([parent=None])
Parameters:
parent – QWidget

Constructs a checkbox with the given parent, but with no text.

parent is passed on to the QAbstractButton constructor.

**init**(text[, parent=None])
Parameters:
text – str

parent – QWidget

Constructs a checkbox with the given parent and text.

parent is passed on to the QAbstractButton constructor.

checkState()
Return type:
CheckState

Returns the checkbox’s check state. If you do not need tristate support, you can also use isChecked() , which returns a boolean.

See also

setCheckState() CheckState

checkStateChanged(state)
Parameters:
state – CheckState

This signal is emitted whenever the checkbox’s state changes, i.e., whenever the user checks or unchecks it.

state contains the checkbox’s new Qt::CheckState.

initStyleOption(option)
Parameters:
option – QStyleOptionButton

Initializes option with the values from this QCheckBox . This method is useful for subclasses that require a QStyleOptionButton , but do not want to fill in all the information themselves.

See also

initFrom()

isTristate()
Return type:
bool

Getter of property tristateᅟ .

setCheckState(state)
Parameters:
state – CheckState

Sets the checkbox’s check state to state. If you do not need tristate support, you can also use setChecked() , which takes a boolean.

See also

checkState() CheckState

setTristate([y=true])
Parameters:
y – bool

See also

isTristate()

Setter of property tristateᅟ .

stateChanged(state)
Parameters:
state – int

Note

This function is deprecated.

Use checkStateChanged (Qt::CheckState) instead.

This signal is emitted whenever the checkbox’s state changes, i.e., whenever the user checks or unchecks it.

state contains the checkbox’s new Qt::CheckState.
