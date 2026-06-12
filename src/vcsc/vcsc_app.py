import os
import signal
import sys

import PySide6
from PySide6 import QtCore, QtWidgets, QtGui

from vcsc import __version__, __appname__
from vcsc.MainWindow import MainWindow
from vcsc.CameraController import CameraController

def main():
    print(__appname__, __version__)
    print("(c) https://byespace.net")
    print("Provided under the zlib license.")
    print()

    print(f"Launching with arguments: {sys.argv}")
    print()

    print(f"Using\tPySide\t{PySide6.__version__}")
    print(f"\tQt\t{QtCore.__version__}")
    print(f"PySide6 path: {PySide6.__file__}")
    print()
    print()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Qt time
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.setOrganizationName("Byespace")

    app.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "net.byespace.vcsc.svg")))

    def handle_permissions():
        camera_allowed_status = app.checkPermission(QtCore.QCameraPermission())
        print(camera_allowed_status)

    if not CameraController.is_camera_allowed(app):
        app.requestPermission(QtCore.QCameraPermission(), app, handle_permissions)

    camera_controller = CameraController()

    widget = MainWindow(camera_controller, application=app)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
