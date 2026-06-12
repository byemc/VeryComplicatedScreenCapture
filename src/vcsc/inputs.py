from enum import Enum

from PySide6.QtCore import *
from PySide6.QtMultimedia import *
from PySide6.QtGui import QIcon

default_icon = QIcon.fromTheme(QIcon.ThemeIcon.DialogQuestion)
camera_icon = QIcon.fromTheme(QIcon.ThemeIcon.CameraVideo)
microphone_icon = QIcon.fromTheme(QIcon.ThemeIcon.AudioInputMicrophone)


def display_role_data(obj, row: int, col: int):
    # ASSUMES ALL CHECKS HAVE PASSED
    if col == 0:
        return obj.description()
    if col == 1:
        return obj.isDefault()
    if col == 2:
        return obj.id()
    if col == 3:
        return obj
    return None


class DeviceListModel(QAbstractListModel):
    class DeviceType(Enum):
        UNKNOWN = 0
        VIDEO = 1
        AUDIO = 2

    def __init__(self, devices, parent=None):
        super().__init__(parent)
        self._inputs = devices
        self._type = self.DeviceType.UNKNOWN
        if len(devices) <= 0:
            return
        if type(devices[0]) == QCameraDevice:
            self._type = self.DeviceType.VIDEO
        elif type(devices[0]) == QAudioDevice:
            self._type = self.DeviceType.AUDIO

    def rowCount(self, parent=None) -> int:
        return len(self._inputs)

    def columnCount(self, parent=None) -> int:
        return 4

    def indexDefaultOrNone(self) -> int | None:
        for device in self._inputs:
            if device.isDefault():
                return self._inputs.index(device)
        return None

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        if index.row() >= len(self._inputs):
            return None

        row = index.row()
        col = index.column()
        obj = self._inputs[row]

        if role == Qt.ItemDataRole.DisplayRole:
            return display_role_data(obj, row, col)
        elif role == Qt.ItemDataRole.FileInfoRole:
            return obj
        elif role == Qt.ItemDataRole.DecorationRole:
            if self._type == self.DeviceType.VIDEO:
                return camera_icon
            if self._type == self.DeviceType.AUDIO:
                return microphone_icon
            return default_icon

        return None


class CameraFormatListModel(QAbstractTableModel):
    def __init__(self, formats: list[QCameraFormat]):
        super().__init__()
        self._formats = formats

    def rowCount(self, parent=None):
        return len(self._formats)

    def columnCount(self, parent=None):
        return 3

    def headerData(self, section, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return "Resolution"
            elif section == 1:
                return "Framerate"
            elif section == 2:
                return "Pixel format"

        return None

    def data(self, index: QModelIndex, role: int, parent=None):
        formats = self._formats

        if not index.isValid():
            return None
        if index.row() >= len(formats):
            return None

        row = index.row()
        col = index.column()
        obj = formats[row]

        if role == Qt.ItemDataRole.FileInfoRole:
            return obj

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if col == 0:
            return f"{obj.resolution().width()}x{obj.resolution().height()}"
        if col == 1:
            return f"{obj.maxFrameRate()}"
        if col == 2:
            return f"{obj.pixelFormat()}"
        return None
