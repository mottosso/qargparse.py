import re
import logging

from collections import OrderedDict as odict
from Qt import QtCore, QtWidgets

__version__ = "1.0.0"
_log = logging.getLogger(__name__)


class QArgumentParser(QtWidgets.QWidget):
    """User interface arguments

    Arguments:
        arguments (list, optional): Instances of QArgument
        storage (QSettings, optional): Persistence to disk, providing
            value() and setValue() methods

    """

    changed = QtCore.Signal(QtCore.QObject)  # A QArgument

    def __init__(self, arguments=None, storage=None, parent=None):
        super(QArgumentParser, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        # Create internal settings
        if storage is True:
            storage = QtCore.QSettings(
                QtCore.QSettings.IniFormat,
                QtCore.QSettings.UserScope,
                __name__, "QArgparse",
            )

        if storage is not None:
            _log.info("Storing settings @ %s" % storage.fileName())

        arguments = arguments or []

        assert hasattr(arguments, "__iter__"), "arguments must be iterable"
        assert isinstance(storage, (type(None), QtCore.QSettings)), (
            "storage must be of type QSettings"
        )

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QWidget(), 0, 999)
        layout.setRowStretch(999, 1)

        self._row = 0
        self._storage = storage
        self._arguments = odict()

        for arg in arguments or []:
            self._addArgument(arg)

        self.setStyleSheet(style)

    def addArgument(self, name, type=None, default=None, **kwargs):
        # Infer type from default
        if type is None and default is not None:
            type = __builtins__["type"](default)

        # Default to string
        type = type or str

        Argument = {
            None: String,
            int: Integer,
            float: Float,
            bool: Boolean,
            str: String,
            list: Enum,
            tuple: Enum,
        }.get(type, type)

        arg = Argument(name, default=default, **kwargs)
        self._addArgument(arg)
        return arg

    def _addArgument(self, arg):
        if arg["name"] in self._arguments:
            raise ValueError("Duplicate argument '%s'" % arg["name"])

        if self._storage is not None:
            arg["default"] = self._storage.value(arg["name"]) or arg["default"]

        arg.changed.connect(lambda: self.changed.emit(arg))
        factory = _WidgetFactory()

        layout = self.layout()
        c0, c1 = factory.create(arg)

        for widget in (c0, c1):
            widget.setToolTip(arg["help"])
            widget.setObjectName(arg["name"])  # useful in CSS
            widget.setProperty("type", type(arg).__name__)
            widget.setAttribute(QtCore.Qt.WA_StyledBackground)

        layout.addWidget(c0, self._row, 0)
        layout.addWidget(c1, self._row, 1)

        self._row += 1
        self._arguments[arg["name"]] = arg

    def clear(self):
        assert self._storage, "Cannot clear without persistent storage"
        self._storage.clear()
        _log.info("Clearing settings @ %s" % self._storage.fileName())

    def find(self, name):
        return self._arguments[name]

    # Optional PEP08 syntax
    add_argument = addArgument


class QArgument(QtCore.QObject):
    changed = QtCore.Signal()

    def __init__(self, name, **kwargs):
        super(QArgument, self).__init__(kwargs.pop("parent", None))

        kwargs["name"] = name
        kwargs["label"] = kwargs.get("label", self.camelToTitle(name))
        kwargs["default"] = kwargs.get("default", None)
        kwargs["help"] = kwargs.get("help", "")
        kwargs["read"] = kwargs.get("read")
        kwargs["write"] = kwargs.get("write")

        self._data = kwargs

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def camelToTitle(self, text):
        """Convert camelCase `text` to Title Case

        Example:
            >>> camelToTitle("mixedCase")
            "Mixed Case"
            >>> camelToTitle("myName")
            "My Name"
            >>> camelToTitle("you")
            "You"
            >>> camelToTitle("You")
            "You"
            >>> camelToTitle("This is That")
            "This Is That"

        """

        return re.sub(
            r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))",
            r" \1", text
        ).title()

    camel_to_title = camelToTitle


class Boolean(QArgument):
    pass


class Tristate(QArgument):
    pass


class Integer(QArgument):
    pass


class Float(QArgument):
    pass


class Range(QArgument):
    pass


class String(QArgument):
    pass


class Info(QArgument):
    pass


class Color(QArgument):
    pass


class Button(QArgument):
    pass


class Toggle(QArgument):
    pass


class Separator(QArgument):
    """Visual separator

    Example:

        item1
        item2
        ------------
        item3
        item4

    """


class Enum(QArgument):
    def __init__(self, name, **kwargs):
        kwargs["items"] = kwargs.get("items", ["No items"])
        super(Enum, self).__init__(name, **kwargs)


class Settings(QtCore.QSettings):
    """Implement changed signal whenever a value changes"""
    changed = QtCore.Signal(str, object)  # key, value

    def setValue(self, key, value):
        super(Settings, self).setValue(key, value)
        self.changed.emit(key, value)


class _WidgetFactory(object):
    def create(self, argument):
        if isinstance(argument, Boolean):
            return self.boolean(argument)

        elif isinstance(argument, (Info, String)):
            return self.string(argument)

        elif isinstance(argument, Button):
            return self.button(argument)

        elif isinstance(argument, (Integer, Float)):
            return self.number(argument)

        elif isinstance(argument, Enum):
            return self.enum(argument)

        elif isinstance(argument, Separator):
            return self.separator(argument)

        else:
            raise TypeError("Unsupported argument type: %s" % argument["name"])

    def string(self, argument):
        label = QtWidgets.QLabel(argument["label"])
        widget = QtWidgets.QLineEdit()
        widget.editingFinished.connect(argument.changed.emit)
        argument.read = lambda: widget.text()
        argument.write = lambda value: widget.setText(value)

        if isinstance(argument, Info):
            widget.setReadOnly(True)

        if argument["default"] is not None:
            argument.write(argument["default"])

        return label, widget

    def boolean(self, argument):
        label = QtWidgets.QLabel(argument["label"])
        widget = QtWidgets.QCheckBox()
        widget.clicked.connect(argument.changed.emit)

        if isinstance(argument, Tristate):
            argument.read = lambda: widget.checkState()
            state = {
                0: QtCore.Qt.Unchecked,
                1: QtCore.Qt.PartiallyChecked,
                2: QtCore.Qt.Checked,
                "1": QtCore.Qt.PartiallyChecked,
                "0": QtCore.Qt.Unchecked,
                "2": QtCore.Qt.Checked,
            }
        else:
            argument.read = lambda: bool(widget.checkState())
            state = {
                0: QtCore.Qt.Unchecked,
                1: QtCore.Qt.Checked,

                # May be stored as string, if used with QSettings(..IniFormat)
                "false": QtCore.Qt.Unchecked,
                "true": QtCore.Qt.Checked,
            }

        argument.write = lambda value: widget.setCheckState(state[value])

        if argument["default"] is not None:
            argument.write(argument["default"])

        return label, widget

    def number(self, argument):
        label = QtWidgets.QLabel(argument["label"])

        if isinstance(argument, Float):
            widget = QtWidgets.QDoubleSpinBox()
        else:
            widget = QtWidgets.QSpinBox()

        widget.editingFinished.connect(argument.changed.emit)
        argument.read = lambda: widget.value()
        argument.write = lambda value: widget.setValue(value)

        if argument["default"] is not None:
            argument.write(argument["default"])

        return label, widget

    def button(self, argument):
        label = QtWidgets.QLabel()
        widget = QtWidgets.QPushButton(argument["label"])
        widget.clicked.connect(argument.changed.emit)

        state = [
            QtCore.Qt.Unchecked,
            QtCore.Qt.Checked,
        ]

        if isinstance(argument, Toggle):
            widget.setCheckable(True)
            argument.read = lambda: widget.checkState()
            argument.write = (
                lambda value: widget.setCheckState(state[int(value)])
            )
        else:
            argument.read = lambda: "clicked"
            argument.write = lambda value: None

        if argument["default"] is not None:
            argument.write(argument["default"])

        return label, widget

    def enum(self, argument):
        label = QtWidgets.QWidget()
        widget = QtWidgets.QComboBox()
        widget.addItems(argument["items"])
        widget.currentIndexChanged.connect(
            lambda index: argument.changed.emit())

        argument.read = lambda: widget.currentText()
        argument.write = lambda value: widget.setCurrentIndex(value)

        if argument["default"] is not None:
            argument.write(argument["default"])

        return label, widget

    def separator(self, argument):
        label = QtWidgets.QLabel(argument["name"])
        label.setAlignment(QtCore.Qt.AlignBottom)
        widget = QtWidgets.QWidget()
        widget.setProperty("sep", True)

        argument.read = lambda: None
        argument.write = lambda value: None

        return label, widget


style = """\

*[type="Button"] {
    text-align:left;
}

*[type="Info"] {
    background: transparent;
    border: none;
}

QLabel[type="Separator"] {
    min-height: 20px;
    text-decoration: underline;
}

QWidget[sep=true] {
    min-height: 1px;
    max-height: 1px;
    background: transparent;
    /*border-bottom: 1px solid #ccc;*/
}

"""
