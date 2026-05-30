from PySide6.QtCore import *
from PySide6.QtWidgets import QStyleFactory


class AppStylesModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def rowCount(self, parent=None) -> int:
        keys = QStyleFactory.keys()
        return len(keys)

    def data(self, index: QModelIndex, role: int = 0, parent=None):
        if not index.isValid():
            return None
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if index.row() >= self.rowCount():
            return None

        return QStyleFactory.keys()[index.row()]