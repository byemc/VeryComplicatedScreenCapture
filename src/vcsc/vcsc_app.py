
import sys

# Qt
import PySide6
from PySide6 import QtCore, QtWidgets

# Console formatting
from rich import print

from vcsc.widgets.MainWindow import MainWindow
from vcsc.CameraController import CameraController

def main():
    _APPNAME = "Very Complicated Screen Capture"
    print(_APPNAME + " 0.0.0")
    print("(c) https://byespace.net")
    print()

    print(f"Using\tPySide\t{PySide6.__version__}")
    print(f"\tQt\t{QtCore.__version__}")
    print()
    print()

    # Qt time
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(_APPNAME)
    app.setOrganizationName("Byespace")

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
