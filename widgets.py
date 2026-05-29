from PySide6.QtCore import *
from PySide6.QtWidgets import *

class LabelComboBox(QWidget):
    def __init__(self, label, model: QAbstractItemModel, parent=None):
        super().__init__(parent)
        self.setEnabled(True)
        # sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # self.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 0, 6, 0)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText(label)
        # sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        # self.label.setSizePolicy(sizePolicy1)
        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(u"comboBox")
        # sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.comboBox.setSizePolicy(sizePolicy2)
        self.comboBox.setModel(model)

        self.horizontalLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
