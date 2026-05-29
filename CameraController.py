from PySide6.QtCore import Slot, QAbstractListModel, QModelIndex, Qt, Signal, QObject, QCameraPermission, \
    QMicrophonePermission, SignalInstance, QSize
from PySide6.QtMultimedia import *
from PySide6.QtMultimedia import QVideoFrameFormat
from PySide6.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PySide6.QtGui import QGuiApplication, QImage

from models.inputs import DeviceListModel, CameraFormatListModel

from rich import print

class ResolutionListModel(QAbstractListModel):
    def __init__(self, resolutions: list[QSize], parent=None):
        super().__init__(parent)
        self._resolutions = resolutions

    def rowCount(self, parent=None):
        return len(self._resolutions)

    def columnCount(self, parent=None):
        return 4

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if section == 0:
            return "Resolution"
        elif section == 1:
            return "Width"
        elif section == 2:
            return "Height"
        return None

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        if index.row() < 0 or index.row() >= len(self._resolutions):
            return None
        if role == 873:
            return self._resolutions[index.row()]
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        row = index.row()
        col = index.column()
        res = self._resolutions[row]

        # $(width)x$(height)
        if col == 0:
            return f"{res.width()}x{res.height()}"
        # width
        elif col == 1:
            return f"{res.width()}"
        # height
        elif col == 2:
            return f"{res.height()}"
        # QSize object
        elif col == 3:
            return f"{res}"

        return None

class CameraController(QObject):
    @staticmethod
    def is_camera_allowed(app: QGuiApplication):
        camera_allowed_status = app.checkPermission(QCameraPermission())
        return camera_allowed_status == Qt.PermissionStatus.Granted

    @staticmethod
    def is_microphone_allowed(app: QGuiApplication):
        camera_allowed_status = app.checkPermission(QMicrophonePermission())
        return camera_allowed_status == Qt.PermissionStatus.Granted

    video_input_changed = Signal(str)
    video_format_changed = Signal(str)
    image_captured = Signal(int, QImage)

    def __init__(self):
        super().__init__()

        self.video_inputs = QMediaDevices.videoInputs()
        self.audio_inputs = QMediaDevices.audioInputs()
        self.refresh_inputs()

        self.video_input_info: QCameraDevice | None = None
        self.video_input: QCamera | None = None

        self.audio_input_info = None
        self.audio_input = None

        self.video_output = None
        self.audio_output = None

        self.video_input_model = DeviceListModel(self.video_inputs)
        self.audio_input_model = DeviceListModel(self.audio_inputs)
        # self.video_format_model = CameraFormatListModel([])

        self.capture_session = QMediaCaptureSession()
        self.image_capturer = QImageCapture()
        self.capture_session.setImageCapture(self.image_capturer)
        self.image_capturer.imageCaptured.connect(self.image_captured)

        self.set_camera(QMediaDevices.defaultVideoInput())
        self.set_microphone(QMediaDevices.defaultAudioInput())

    @Slot()
    def capture_image(self):
        self.image_capturer.capture()

    def refresh_inputs(self):
        self.video_inputs = QMediaDevices.videoInputs()
        print("Cameras:")
        for camera in self.video_inputs:
            print(f"\t- {camera.description()} [dim]{camera.id()}[/dim]")
        self.audio_inputs = QMediaDevices.audioInputs()

        print("Microphones:")
        for mic in self.audio_inputs:
            print(f"\t- {mic.description()} [dim]{mic.id()}[/dim]")

    def map_outputs(self, video_input : QVideoWidget | QGraphicsVideoItem, audio_input : QAudioOutput):
        self.video_output = video_input
        self.audio_output = audio_input
        self.capture_session.setVideoOutput(self.video_output)
        self.capture_session.setAudioOutput(self.audio_output)

    def set_camera(self, device: QCameraDevice, camera_format: QCameraFormat | None = None):
        self.video_input_info = device
        if self.video_input is not None:
            self.video_input.stop()
        self.video_input = QCamera(device)
        self.video_input_changed.emit(f"Changed video to {device.description()}")
        if self.video_input is not None:
            self.capture_session.setCamera(self.video_input)
            if camera_format is not None:
                self.video_input.setCameraFormat(camera_format)
            elif len(device.videoFormats()) > 0:
                # first supported format
                self.video_input.setCameraFormat(device.videoFormats()[0])
            self.video_input.start()

    def set_microphone(self, device: QAudioDevice):
        self.audio_input_info = device
        self.audio_input = QAudioInput(device)
        self.capture_session.setAudioInput(self.audio_input)

    def get_current_resolution(self) -> QSize:
        if self.video_input is not None:
            return self.video_input.cameraFormat().resolution()
        return QSize()

    def get_current_fps(self) -> float:
        if self.video_input is not None:
            return self.video_input.cameraFormat().maxFrameRate()
        return 0.0

    def get_current_pixel_format(self) -> QVideoFrameFormat.PixelFormat | None:
        if self.video_input is not None:
            return self.video_input.cameraFormat().pixelFormat()
        return None

    def get_supported_resolutions(self) -> list[QSize]:
        if self.video_input_info is None:
            return []

        formats = self.video_input_info.videoFormats()
        output = []

        for format in formats:
            res = format.resolution()
            if res not in output:
                output.append(res)

        def sort_function(obj: QSize):
            return obj.height() * obj.width()

        output.sort(key=sort_function, reverse=True)
        return output

    def _get_supported_resolution_areas(self) -> list[int]:
        resolutions = self.get_supported_resolutions()
        output = []
        for res in resolutions:
            output.append(res.width() * res.height())
        return output

    def get_supported_framerates(self, supports_resolution: QSize = None) -> list[float]:
        if self.video_input_info is None:
            return []

        formats = self.video_input_info.videoFormats()
        output = []

        for format in formats:
            rate = format.maxFrameRate()
            if supports_resolution and supports_resolution != format.resolution():
                continue
            if rate not in output:
                output.append(rate)

        output.sort(reverse=True)
        return output

    def get_supported_pixel_formats(self, supports_resolution: QSize = None, supports_frame_rate: float = None) -> list[QVideoFrameFormat.PixelFormat]:
        if self.video_input_info is None:
            return []

        formats = self.video_input_info.videoFormats()
        output = []
        for format in formats:
            pixel = format.pixelFormat()
            if supports_resolution and supports_resolution != format.resolution():
                continue
            if supports_frame_rate and supports_frame_rate != format.maxFrameRate():
                continue
            if pixel not in output:
                output.append(pixel)
        return output

    @Slot(int)
    def change_video_index(self, index: int):
        video_device_index = self.video_input_model.index(index)
        video_device = self.video_input_model.data(video_device_index, Qt.ItemDataRole.FileInfoRole)
        self.set_camera(video_device)

    @Slot(int)
    def change_audio_index(self, index: int):
        device_index = self.audio_input_model.index(index)
        device = self.audio_input_model.data(device_index, Qt.ItemDataRole.FileInfoRole)
        self.set_microphone(device)

    def change_video_format(self, format: QCameraFormat=None):
        if self.video_input is not None and format is not None:
            self.set_camera(self.video_input_info, format)
            self.video_format_changed.emit(f"Changed format to {format.resolution().height()}p{format.maxFrameRate()} (min: {format.minFrameRate()}) / {format.pixelFormat()}")

    def find_nearest_video_format(self, resolution: QSize, framerate: float, pixel_format) -> QCameraFormat:
        if self.video_input_info is None:
            return QCameraFormat()

        formats = self.video_input_info.videoFormats()
        print(f"{len(formats)} formats remain.")

        # Get closest resolution
        target_resolution_area = resolution.width() * resolution.height()
        closest_resolution = min(self.get_supported_resolutions(), key=lambda x: abs(target_resolution_area - (x.width() * x.height())))
        for format in formats.copy():
            # print(format.resolution(), "vs", closest_resolution)
            if format.resolution() != closest_resolution:
                formats.remove(format)
        print(f"{len(formats)} formats remain.")

        # Get closest frame rate
        closest_frame_rate = min(self.get_supported_framerates(closest_resolution), key=lambda x: abs(framerate - x))
        for format in formats.copy():
            if format.maxFrameRate() != closest_frame_rate:
                formats.remove(format)
        print(f"{len(formats)} formats remain.")

        # Use the preferred pixel format if available, if not use the first one
        backup_formats = formats.copy()
        for format in formats.copy():
            if format.pixelFormat() != pixel_format:
                formats.remove(format)
        print(f"{len(formats)} formats remain.")
        if not formats:
            return backup_formats[0]
        print(formats[0].resolution(), formats[0], resolution, formats[0].maxFrameRate(), framerate)
        return formats[0]

    @Slot(QModelIndex)
    def change_video_format_index(self, index: QModelIndex):
        model = self.video_format_model
        if not self.video_format_model:
            model = self.get_video_format_model()

        format: QCameraFormat | None = model.data(index, Qt.ItemDataRole.FileInfoRole)
        self.change_video_format(format)
