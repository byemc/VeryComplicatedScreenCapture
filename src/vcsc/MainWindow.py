from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtCore import *

from vcsc import iconography
from vcsc.CameraController import CameraController
from vcsc.SettingsWidget import SettingsWidget
from vcsc.VideoWidget import VideoWidget

class MainWindow(QMainWindow):
    def __init__(self, camera_controller: CameraController, parent = None, application: QApplication = None):
        super().__init__(parent)


        self.application: QApplication | None = application
        if self.application is not None:
            self.setWindowTitle(self.application.applicationName())

        self.settingsWindow = None
        self.settings = None
        self.viewfinder = VideoWidget(self)
        self.audio_context = QAudioOutput(parent=self)

        self.controller: CameraController = camera_controller
        self.controller.map_outputs(self.viewfinder, self.audio_context)

        self.setCentralWidget(self.viewfinder)

        # Menu bar
        file_menu = self.menuBar().addMenu("&File")
        view_menu = self.menuBar().addMenu("&View")

        settings_icon = QIcon.fromTheme(iconography.icon("configure"))
        settings_action = QAction(settings_icon, "&Settings", self, shortcut=QKeySequence("Ctrl+I"))
        settings_action.triggered.connect(self.open_settings)
        self.addAction(settings_action)

        copy_image_icon = QIcon.fromTheme(QIcon.ThemeIcon.EditCopy)
        copy_image_action = QAction(copy_image_icon, "&Copy screenshot", self, shortcut=QKeySequence("Ctrl+C"))
        copy_image_action.triggered.connect(self.controller.capture_image)
        self.controller.image_captured.connect(self.copy_image)
        self.addAction(copy_image_action)

        fullscreen_action = QAction("&Fullscreen", self, shortcut=QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        self.addAction(fullscreen_action)

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.open_about)

        # Finally, build the menu structure
        file_menu.addAction(copy_image_action)
        file_menu.addSeparator()
        file_menu.addAction(settings_action)

        view_menu.addAction(fullscreen_action)
        view_menu.addAction(about_action)

        self.controller.video_input_changed.connect(self.set_status)
        self.controller.video_format_changed.connect(self.set_status)

        self.prefersMaximised = False
        self.prefersSize = QSize()

    def toggle_fullscreen(self):
        if not self.isFullScreen():
            self.prefersMaximised = self.isMaximized()
            self.prefersSize = self.size()
            print("Setting fullscreen\t", "Is fullscreen:", self.isFullScreen(), "Is maximised:", self.prefersMaximised, "Size:", self.prefersSize)

            self.showFullScreen()
            self.statusBar().hide()
            self.menuBar().hide()
        else:
            print("Setting fullscreen\t", "Is fullscreen:", self.isFullScreen(), "Is maximised:", self.prefersMaximised, "Size:", self.prefersSize)
            self.showNormal()
            if self.prefersMaximised:
                print("Setting maximised")
                self.showMaximized()
            else:
                print("Setting size", self.prefersSize)
                self.resize(self.prefersSize)
            self.statusBar().show()
            self.menuBar().show()

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
        if not self.settings and self.application is not None:
            self.settings = SettingsWidget(self.controller, self.application, self)
            self.settings.finished.connect(self.destroy_settings)
        if self.settings.isHidden():
            self.settings.show()
        self.settings.raise_()
        self.settings.activateWindow()

    @Slot()
    def open_about(self):
        QMessageBox.about(self, "About", "Very Complicated Video Capture\n\nhttps://byespace.net\nMade available under the zlib license\nThanks for using my program!")
