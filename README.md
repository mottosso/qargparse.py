### QArgparse

![image](https://user-images.githubusercontent.com/2152766/58029512-ab005980-7b14-11e9-8161-d38e2ce3038c.png)

Easily build settings-style user interfaces, using syntax akin to Python's [`argparse`]() module.

**Features**

- [x] Automatic user interface for settings-style GUIs
- [x] Automatic tooltips from argument `help=`
- [ ] Persistence to disk
- [x] Automatic label from name
- [x] Tab-support for transitioning between arguments
- [x] Rich selection of types
- [x] Infer type from default value
- [x] Imperative and declarative mode
- [ ] Theme support
- [ ] Min/max values for sliders
- [ ] Wrap any command-line tool using `ArgumentParser` with a GUI

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

<br>

### Usage

Use `qargparse.QArgumentParser` as you would `argparse.ArgumentParser`.

```python
import sys
from Qt import QtWidgets
from qargparse import QArgumentParser

app = QtWidgets.QApplication(sys.argv)

parser = QArgumentParser()
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