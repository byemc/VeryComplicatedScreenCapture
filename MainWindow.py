from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *
from PySide6.QtCore import *

from rich import print

import iconography
import models.inputs
import widgets
from CameraController import CameraController
from SettingsWidget import SettingsWidget
from VideoWidget import VideoWidget


class MainWindow(QMainWindow):
    def __init__(self, camera_controller: CameraController, parent = None, application: QApplication = None):
        super().__init__(parent)

        self.application: QGuiApplication | None = application
        if self.application is not None:
            self.setWindowTitle(self.application.applicationName())

        self.settingsWindow = None
        self.settings = None
        self.viewfinder = VideoWidget(self)
        self.audio_context = QAudioOutput(parent=self)

        self.controller: CameraController = camera_controller
        self.controller.map_outputs(self.viewfinder, self.audio_context)

        self.setCentralWidget(self.viewfinder)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(True)
        self.addToolBar(self.toolbar)

        icon = QIcon.fromTheme(iconography.icon("configure"))
        settings_action = QAction("&Settings", self, shortcut=QKeySequence("Ctrl+I"))
        settings_action.triggered.connect(self.open_settings)
        # self.toolbar.addAction(settings_action)
        self.menuBar().addAction(settings_action)
        self.addAction(settings_action)

        copy_image_icon = QIcon.fromTheme(QIcon.ThemeIcon.EditCopy)
        copy_image_action = QAction(copy_image_icon, "&Copy screenshot", self, shortcut=QKeySequence("Ctrl+C"))
        copy_image_action.triggered.connect(self.controller.capture_image)
        self.controller.image_captured.connect(self.copy_image)
        self.toolbar.addAction(copy_image_action)
        self.addAction(copy_image_action)
        # self.menuBar().addAction(copy_image_action)

        fullscreen_action = QAction("Fullscreen (F11)", self, shortcut=QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        # self.toolbar.addAction(fullscreen_action)
        self.menuBar().addAction(fullscreen_action)
        self.addAction(fullscreen_action)


        self.controller.video_input_changed.connect(self.set_status)
        self.controller.video_format_changed.connect(self.set_status)

    def toggle_fullscreen(self):
        print("Toggling fullscreen!", not self.isFullScreen())
        if not self.isFullScreen():
            self.showFullScreen()
            self.toolbar.hide()
            self.statusBar().hide()
            self.menuBar().hide()
        else:
            self.showNormal()
            self.toolbar.show()
            self.statusBar().show()
            self.menuBar().show()


    # def mouseDoubleClickEvent(self, event: QMouseEvent):
    #     self.toggle_fullscreen()
    #     event.accept()

    @Slot(int, QImage)
    def copy_image(self, id: int, preview: QImage):
        clipboard = self.application.clipboard()
        clipboard.setImage(preview)
        self.set_status("Copied to clipboard.", 5000)

    # @Slot(str, int)
    @Slot(str)
    def set_status(self, message: str, timeout: int | None = None):
        if timeout is not None:
            self.statusBar().showMessage(message, timeout)
        else:
            self.statusBar().showMessage(message)

    @Slot()
    def destroy_settings(self):
        if self.settings is not None:
            self.settings.destroy()
        self.settings = None

    @Slot()
    def open_settings(self):
        if not self.settings:
            self.settings = SettingsWidget(self.controller, self.application, self)
            self.settings.finished.connect(self.destroy_settings)
        if self.settings.isHidden():
            self.settings.show()
        self.settings.raise_()
        self.settings.activateWindow()
