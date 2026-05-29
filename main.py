import sys

# Qt
import PySide6
from PySide6 import QtCore, QtWidgets, QtGui

# Console formatting
from rich import print

import iconography
from MainWindow import MainWindow
from CameraController import CameraController

# Startup sequence! Imagine something cool and hackery. Idk i thought it would be cool to comment it like this but not
# really huh

if __name__ != "__main__":
    print("Please don't import VCSC as a module!")
    raise Exception("Please don't import VCSC as a module!")

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
