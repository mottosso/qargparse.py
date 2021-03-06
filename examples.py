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

        save = edit.addAction("Save Settings")
        save.setEnabled(False)
        reset = edit.addAction("Reset Settings")
        reset.triggered.connect(self.on_reset)
        hlp.addAction("Help on Bind Skin Options")

        layout = QtWidgets.QHBoxLayout(footer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(buttons[0])
        layout.addWidget(buttons[1])
        layout.addWidget(buttons[2])

        args = [
            qargparse.Enum("bindTo", items=["Joint Hierarchy",
                                            "Selected Joints",
                                            "Object Hierarchy"]),
            qargparse.Enum("bindMethod", items=["Closest Distance",
                                                "Closest in hierarchy",
                                                "Geodesic voxel"]),
            qargparse.Enum("skinningMethod", items=["Classic linear",
                                                    "Dual quaternion"]),
            qargparse.Enum("normalizeWeights", items=["Interactive",
                                                      "Post"]),
            qargparse.Enum("weightDistribution", items=["Distance",
                                                        "Neighbors"]),
            qargparse.Boolean("allowMultipleBindPoses", default=True),
            qargparse.Integer("maxInfluences", default=5, min=1, max=30,
                              initial=12),
            qargparse.Boolean("maintainMaxInfluences",

                              # Value resetted to
                              default=True,

                              # Initial value on launch, differs from default
                              initial=False),
            qargparse.Boolean("removeUnusedInfluences", default=True),
            qargparse.Boolean("colorizeSkeleton", default=True, initial=False),
            qargparse.Boolean("includeHiddenSelectionsOnCreation",
                              default=False),
            qargparse.Float("falloff", min=0.0, max=1.0, default=0.2),
            qargparse.Enum("resolution", items=["1024", "512", "256"],
                           default="256"),
            qargparse.Boolean("validateVoxelState", default=True, help=(
                "A more lengthy description of what this option does"
            )),
        ]

        parser = qargparse.QArgumentParser(args)
        parser.changed.connect(self.on_changed)
        parser.entered.connect(self.on_entered)
        parser.exited.connect(self.on_exited)

        layout = QtWidgets.QVBoxLayout(central)
        layout.addWidget(parser)
        layout.addWidget(footer)

        self._parser = parser
        self.setCentralWidget(central)

    def on_reset(self):
        for arg in self._parser:
            arg.write(arg["default"])

    def on_changed(self, arg):
        print("%s changed to %s" % (arg["name"], arg.read()))

    def on_entered(self, arg):
        print("%s entered" % (arg["name"]))

    def on_exited(self, arg):
        print("%s exited" % (arg["name"]))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = BindSkinOptions()
    window.show()
    app.exec_()
