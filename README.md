# NOT PRODUCTION READY

There are a few kinks left and examples to make before this is generally useful.

<br>
<br>

### QArgparse

![image](https://user-images.githubusercontent.com/2152766/58029512-ab005980-7b14-11e9-8161-d38e2ce3038c.png)

Build settings-style graphical user interfaces with Python's [`argparse`](https://docs.python.org/3/library/argparse.html) syntax.

```python
import sys
from Qt import QtWidgets
from qargparse import QArgumentParser

app = QtWidgets.QApplication(sys.argv)

parser = QArgumentParser(description="My first graphical parser")
parser.add_argument("name", type=str, help="Your name")
parser.add_argument("age", type=int, help="Your age")
parser.add_argument("height", type=float, help="Your height")
parser.add_argument("alive", type=bool, help="Your state")
parser.show()

app.exec_()
```

**Features**

- [x] Automatic user interface for settings-style GUIs
- [x] Automatic tooltips from argument `help=`
- [x] Persistence to disk
- [x] Rich selection of types
- [x] Infer type from default value
- [x] Imperative and declarative mode
- [x] Tab-support for transitioning between arguments
- [x] Automatic label from name
- [x] Dual PEP8 and Qt syntax
- [ ] Theme support
- [ ] Min/max values for sliders
- [ ] Wrap any instance of `argparse.ArgumentParser` with a GUI
- [ ] Argument Icons, for extra flare
- [ ] Argument Groups, e.g. tree view or side-panel

<br>

### Types

In addition to being able to subclass and create your own widgets, these are the ones included out-of-the-box.

| Type        | Description               | Example
|:------------|:--------------------------|:---------------------------------
| `Boolean`   | Checkbox for on/off state | ![](https://placehold.it/300x30)
| `Tristate`  | Checkbox with 3 states | ![](https://placehold.it/300x30)
| `Integer`   | Whole number | ![](https://placehold.it/300x30)
| `Float`     | Fraction | ![](https://placehold.it/300x30)
| `Range`     | Two numbers, a start and an end | ![](https://placehold.it/300x30)
| `String`    | A single line of text | ![](https://placehold.it/300x30)
| `Text`      | A multi-line segment of text | ![](https://placehold.it/300x30)
| `Info`      | Read-only single line of text | ![](https://placehold.it/300x30)
| `Color`     | An RGB or HSV color | ![](https://placehold.it/300x30)
| `Button`    | A clickable button | ![](https://placehold.it/300x30)
| `Toggle`    | A checkable button | ![](https://placehold.it/300x30)
| `Enum`      | Multiple choice | ![](https://placehold.it/300x30)
| `Separator` | A visual separation between subsequent arguments | ![](https://placehold.it/300x30)
| `List` | Multiple string-values | ![](https://placehold.it/300x30)
| `Path` | A formatted string, with OS-specific file-browser | ![](https://placehold.it/300x30)
| `EnvironmentVariable` | A key/value string with limited character support | ![](https://placehold.it/300x30)
| `EnvironmentPath` | An `os.pathsep`-separated string | ![](https://placehold.it/300x30)
| `Color` | A color with visual swatch and hex, HSV and RGB support | ![](https://placehold.it/300x30)
| `Image` | A `Path` with thumbnail and restrictions on file extension | ![](https://placehold.it/300x30)

<br>

### Install

qargparse.py is available on PyPI.

```bash
$ pip install qargparse.py
$ python -m qargparse --demo
```

> This also installs [Qt.py](https://github.com/mottosso/Qt.py) as a dependency. Skip this by passing `--no-deps` to `pip install`, not however that it is required in order for `qargparse.py` to run.

<br>

### Usage

Use `qargparse.QArgumentParser` as you would `argparse.ArgumentParser`.

```python
import sys
from Qt import QtWidgets
from qargparse import QArgumentParser

app = QtWidgets.QApplication(sys.argv)

parser = QArgumentParser(description="My first graphical parser")
parser.add_argument("name", type=str, help="Your name")
parser.add_argument("age", type=int, help="Your age")
parser.add_argument("height", type=float, help="Your height")
parser.add_argument("alive", type=bool, help="Your state")
parser.show()

app.exec_()
```

Or declaratively, using explicit types.

```python
import qargparse
parser = qargparse.QArgumentParser([
    qargparse.String("name", help="Your name"),
    qargparse.Integer("age", help="Your age"),
    qargparse.Float("height", help="Your height"),
    qargparse.Boolean("alive", help="Your state"),
])
```

Types can also be inferred by their default value.

```python
import qargparse
parser = qargparse.QArgumentParser()
parser.add_argument("name", default="My Name")  # `str` inferred
parser.add_argument("age", default=54)  # `int` inferred
```

<br>

### Types

In addition to standard types, QArgparse also supports user interface types.

```python
import qargparse
qargparse.Button("press me", help="See what happens!")
```

<br>

### Camel and Snake

Consistency is important. Sometimes you work with a camel_case codebase, sometimes not. This library supports both, use the one which best suits your current codebase.

```python
import qargparse
qargparse.addArgument()
qargparse.add_argument()
```

<br>

### Signals

Respond to any change via the `.changed` signal.

```python
import qargparse

def on_changed(argument):
    print("%s was changed!" % argument["name"])

args = [
    qargparse.Integer("age")
]

parser = qargparse.QArgumentParser(args)
parser.changed.connect(on_changed)
```

Or respond to individual changes.

```python
import qargparse

def on_pressed():
    print("%s was changed!" % button["name"])

button = qargparse.Button("press me")
button.changed.connect(on_pressed)

parser = qargparse.QArgumentParser([button])
```
