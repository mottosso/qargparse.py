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
            qargparse.Integer("maxInfluences", default=5, min=1, max=30),
            qargparse.Boolean("maintainMaxInfluences", default=True),
            qargparse.Boolean("removeUnusedInfluences", default=True),
            qargparse.Boolean("colorizeSkeleton", default=True),
            qargparse.Boolean("includeHiddenSelectionsOnCreation",
                              default=False),
            qargparse.Float("falloff", min=0.0, max=1.0, default=0.2),
            qargparse.Enum("resolution", items=["1024", "512", "256"],
                           default="256"),
            qargparse.Boolean("validateVoxelState", default=True),
        ]

        parser = qargparse.QArgumentParser(args)
        parser.changed.connect(self.on_changed)

        layout = QtWidgets.QVBoxLayout(central)
        layout.addWidget(parser)
        layout.addWidget(footer)

        self.setCentralWidget(central)

    def on_changed(self, arg):
        print("%s changed to %s" % (arg["name"], arg.read()))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = BindSkinOptions()
    window.show()
    app.exec_()
