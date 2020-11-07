import qargparse

from qargparse import (
    px,

    # Reuse multi-binding logic
    QtWidgets,
    QtCore,
)


class BindSkinOptions(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(BindSkinOptions, self).__init__(parent)
        self.setWindowTitle("Bind Skin Options")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(px(550))
        self.setMinimumHeight(px(370))

        buttons = [
            QtWidgets.QPushButton("Bind Skin"),
            QtWidgets.QPushButton("Apply"),
            QtWidgets.QPushButton("Close"),
        ]

        central = QtWidgets.QWidget()
        header = self.menuBar()
        footer = QtWidgets.QWidget()

        edit = header.addMenu("&Edit")
        hlp = header.addMenu("&Help")

        edit.addAction("Save Settings")
        edit.addAction("Reset Settings")
        hlp.addAction("Help on Bind Skin Options")

        layout = QtWidgets.QHBoxLayout(footer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(buttons[0])
        layout.addWidget(buttons[1])
        layout.addWidget(buttons[2])

        args = [
            qargparse.Enum("Bind to", items=["Joint Hierarchy",
                                             "Selected Joints",
                                             "Object Hierarchy"]),
            qargparse.Enum("Bind method", items=["Closest Distance",
                                                 "Closest in hierarchy",
                                                 "Geodesic voxel"]),
            qargparse.Enum("Skinning method", items=["Classic linear",
                                                     "Dual quaternion"]),
            qargparse.Enum("Normalize weights", items=["Interactive",
                                                       "Post"]),
            qargparse.Enum("Weight distribution", items=["Distance",
                                                         "Neighbors"]),
            qargparse.Boolean("Allow multiple bind poses", default=True),
            qargparse.Integer("Max influences", default=5, min=1, max=30),
            qargparse.Boolean("Maintain max influences", default=True),
            qargparse.Boolean("Remove unused influences", default=True),
            qargparse.Boolean("Colorize skeleton", default=True),
            qargparse.Boolean("Include hidden selections on creation",
                              default=False),
            qargparse.Float("Falloff", min=0.0, max=1.0, default=0.2),
            qargparse.Enum("Resolution", items=["1024", "512", "256"],
                           default="256"),
            qargparse.Boolean("Validate voxel state", default=True),
        ]

        parser = qargparse.QArgumentParser(args)

        layout = QtWidgets.QVBoxLayout(central)
        layout.addWidget(parser)
        layout.addWidget(footer)

        self.setCentralWidget(central)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = BindSkinOptions()
    window.show()
    app.exec_()
