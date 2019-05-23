import sys
import logging
import argparse
import contextlib

from Qt import QtCore, QtWidgets
import qargparse

_app = QtWidgets.QApplication(sys.argv)

parser = argparse.ArgumentParser()
parser.add_argument("--interactive", action="store_true")

opts = parser.parse_args()

logging.basicConfig(format="%(message)s")
logging.getLogger().setLevel(logging.DEBUG)


def _kill(widget):
    widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    QtCore.QTimer.singleShot(500, widget.close)


@contextlib.contextmanager
def __auto__(title):
    sys.stdout.write(title)

    parser = qargparse.QArgumentParser()
    parser.setWindowTitle(title)
    parser.setMinimumWidth(300)

    yield parser
    parser.show()

    if not opts.interactive:
        _kill(parser)

    _app.exec_()

    sys.stdout.write(" ok\n")


@contextlib.contextmanager
def __manual__(title):
    sys.stdout.write(title)
    yield
    _app.exec_()
    sys.stdout.write(" ok\n")


with __auto__("All..") as parser:
    parser.add_argument("name", default="Marcus", help="Your name")
    parser.add_argument("age", default=33, help="Your age")
    parser.add_argument("height", default=1.87, help="Your height")
    parser.add_argument("alive", default=True, help="Your state")
    parser.add_argument("class", type=qargparse.Enum, items=[
        "Ranger",
        "Warrior",
        "Sorcerer",
        "Monk",
    ], default=2, help="Your class")


with __auto__("Enum..") as parser:
    en = parser.add_argument("myOptions", default=1, items=["a", "b", "c"])


with __auto__("Defaults..") as parser:
    name = parser.add_argument("name", default="Marcus")
    age = parser.add_argument("age", default=33)
    height = parser.add_argument("height", default=1.87)
    alive = parser.add_argument("alive", default=True)
    en = parser.add_argument("myOptions", default=1, items=["a", "b", "c"])

    assert name.read() == "Marcus", name.read()
    assert age.read() == 33, age.read()
    assert height.read() == 1.87, height.read()
    assert alive.read() is True, alive.read()
    assert en.read() == 1, en.read()


with __manual__("Explicit persistence.."):
    settings = QtCore.QSettings(QtCore.QSettings.IniFormat,
                                QtCore.QSettings.UserScope,
                                __name__, "test.py")
    settings.clear()
    settings.setValue("name", "Marcus")

    parser = qargparse.QArgumentParser(storage=settings)
    name = parser.add_argument("name")

    # Coming from settings
    assert name.read() == "Marcus"

    parser.show()
    parser.setMinimumWidth(300)
    _kill(parser)


with __manual__("Implicit persistence.."):
    parser = qargparse.QArgumentParser(storage=True)
    parser.clear()
    parser._storage.setValue("name", "Marcus")
    name = parser.add_argument("name")

    # Coming from settings
    assert name.read() == "Marcus"

    parser.show()
    parser.setMinimumWidth(300)
    _kill(parser)


with __auto__("addArgument return value.. ") as parser:
    def on_pressed():
        print("%s was changed!" % button["name"])

    button = parser.addArgument("pressMe", type=qargparse.Button)
    button.changed.connect(on_pressed)


with __auto__("Individual signal.. ") as parser:
    def on_pressed():
        print("%s was changed!" % button["name"])

    button = parser.add_argument("pressMe", type=qargparse.Button)
    button.changed.connect(on_pressed)


with __auto__("Global signal.. ") as parser:
    def on_changed(argument):
        print("%s was changed!" % argument["name"])

    parser.add_argument("name", type=str)
    parser.add_argument("strong", type=bool)
    parser.changed.connect(on_changed)


with __auto__("Vanilla..") as parser:
    parser.add_argument("name", type=str, help="Your name")
    parser.add_argument("age", type=int, help="Your age")
    parser.add_argument("height", type=float, help="Your height")
    parser.add_argument("alive", type=bool, help="Your state")


with __manual__("Explicit arguments.. "):
    args = [
        qargparse.String("name", help="Your name"),
        qargparse.Integer("age", help="Your age"),
        qargparse.Float("height", help="Your height"),
        qargparse.Boolean("alive", help="Your state"),
    ]

    parser = qargparse.QArgumentParser(args)
    parser.setMinimumWidth(300)
    parser.show()

    _kill(parser) if not opts.interactive else None
