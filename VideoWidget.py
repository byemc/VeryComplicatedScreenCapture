from PySide6.QtCore import Slot, QMargins
from PySide6.QtGui import QMouseEvent
from PySide6.QtMultimediaWidgets import *
from PySide6.QtWidgets import *


class VideoWidget(QVideoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
