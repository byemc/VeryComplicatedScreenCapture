from PySide6.QtCore import *
from PySide6.QtWidgets import *

from vcsc.CameraController import CameraController, ResolutionListModel
from vcsc.models.styles import AppStylesModel
class SettingsWidget(QDialog):
    def __init__(self, camera_controller: CameraController, application: QApplication, parent=None):
        super().__init__(parent)

        self.app = application

        self.buttons = QDialogButtonBox()
        self.buttons.addButton(QDialogButtonBox.StandardButton.Close)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        window_layout = QVBoxLayout(self)
        tabs = QTabWidget()
        window_layout.addWidget(tabs)
        window_layout.addWidget(self.buttons)

        # Camera config page
        self.controller = camera_controller

        self.camera_selector = QComboBox()
        self.camera_selector.setModel(self.controller.video_input_model)
        self.camera_selector.activated.connect(self.controller.change_video_index)
        self.camera_selector.activated.connect(self.video_changed)

        self.audio_selector = QComboBox()
        self.audio_selector.setModel(self.controller.audio_input_model)
        self.audio_selector.activated.connect(self.controller.change_audio_index)

        self.resolution_selector = QComboBox()
        self.resolutions_model = ResolutionListModel(self.controller.get_supported_resolutions())
        self.resolution_selector.setModel(self.resolutions_model)
        try:
            current = self.controller.get_supported_resolutions().index(self.controller.get_current_resolution())
            self.resolution_selector.setCurrentIndex(current)
        except ValueError:
            print("Oh noes!")
        self.resolution_selector.activated.connect(self.resolution_changed)

        self.fps_selector = QComboBox()
        self.fps_selector.activated.connect(self.framerate_changed)
        self.refresh_framerates()

        self.pixel_format_selector = QComboBox()
        self.pixel_format_selector.activated.connect(self.pixel_format_changed)
        self.refresh_pixel_formats()

        camera_options_widget = QWidget(tabs)
        camera_options_layout = QFormLayout(camera_options_widget)
        camera_options_layout.addRow(QLabel("Video"), self.camera_selector)
        camera_options_layout.addRow(QLabel("Audio"), self.audio_selector)
        camera_options_layout.addRow(QLabel("Resolution"), self.resolution_selector)
        camera_options_layout.addRow(QLabel("Frame rate"), self.fps_selector)
        camera_options_layout.addRow(QLabel("Pixel format"), self.pixel_format_selector)
        tabs.addTab(camera_options_widget, "Inputs")

        # App settings page
        app_options_widget = QWidget(tabs)
        tabs.addTab(app_options_widget, "App")
        app_options_layout = QFormLayout(app_options_widget)

        self.style_box = QComboBox()
        style_model = AppStylesModel()
        self.style_box.setModel(style_model)
        self.style_box.activated.connect(self.set_appstyle)
        self.style_box.setCurrentIndex(self.style_box.findText(self.app.style().name()))
        app_options_layout.addRow(QLabel("Style"), self.style_box)

        self.setWindowTitle("Settings")

    @Slot(int)
    def set_appstyle(self, index):
        key = self.style_box.itemText(index)
        self.app.setStyle(QStyleFactory.create(key))

    def refresh_framerates(self, new_resolution: QSize = None):
        if not new_resolution:
            new_resolution = self.controller.get_current_resolution()
        current_rate = self.controller.get_current_fps()
        rates = self.controller.get_supported_framerates(new_resolution)
        self.fps_selector.clear()
        for rate in rates:
            self.fps_selector.addItem(str(rate), rate)
        if self.fps_selector.findData(current_rate):
            self.fps_selector.setCurrentIndex(self.fps_selector.findData(current_rate))

    def refresh_pixel_formats(self, new_resolution: QSize = None, new_framerate: float = None):
        if not new_resolution:
            new_resolution = self.controller.get_current_resolution()
        if not new_framerate:
            new_framerate = self.controller.get_current_fps()
        current_pixel_format = self.controller.get_current_pixel_format()
        if new_framerate == 0:
            new_framerate = None
        formats = self.controller.get_supported_pixel_formats(new_resolution, new_framerate)
        self.pixel_format_selector.clear()
        for format in formats:
            self.pixel_format_selector.addItem(str(format), format)
        self.pixel_format_selector.setCurrentIndex(self.pixel_format_selector.findData(current_pixel_format))

    @Slot(int)
    def pixel_format_changed(self, index):
        new_pixel_format = self.pixel_format_selector.itemData(index)
        new_format = self.controller.find_nearest_video_format(self.controller.get_current_resolution(), self.controller.get_current_fps(), new_pixel_format)
        self.controller.change_video_format(new_format)
        self.refresh_framerates(new_format.resolution())
        self.refresh_pixel_formats(new_format.resolution(), new_format.maxFrameRate())

    @Slot(int)
    def framerate_changed(self, index):
        new_rate = self.fps_selector.itemData(index)
        new_format = self.controller.find_nearest_video_format(self.controller.get_current_resolution(), new_rate, self.controller.get_current_pixel_format())
        self.controller.change_video_format(new_format)
        self.refresh_framerates(new_format.resolution())
        self.refresh_pixel_formats(new_format.resolution(), new_format.maxFrameRate())

    @Slot(int)
    def resolution_changed(self, index):
        new_size = self.resolution_selector.itemData(index, 873)
        if new_size is None:
            new_size = QSize(640, 480)
        new_format = self.controller.find_nearest_video_format(new_size, self.controller.get_current_fps(), self.controller.get_current_pixel_format())
        self.controller.change_video_format(new_format)
        self.refresh_framerates(new_format.resolution())
        self.refresh_pixel_formats(new_format.resolution(), new_format.maxFrameRate())

    @Slot()
    def video_changed(self):
        # Resolution stuff needs updating
        self.resolutions_model = ResolutionListModel(self.controller.get_supported_resolutions())
        self.resolution_selector.setModel(self.resolutions_model)
