from PySide6 import QtGui, QtCore
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import *

from vcsc import __version_friendly__, __appname__

# Parts of this are shamelessly inspired by KTitleWidget and KAboutApplicationDialogue, but not directly stolen
class AboutWindow(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setWindowTitle("About Very Complicated Screen Capture")

        self.window_layout = QGridLayout(self)
        self.widget_layout = QGridLayout()

        icon_label = QLabel(self)
        icon_label.setPixmap(QtGui.QGuiApplication.windowIcon().pixmap(QSize(48, 48)))

        title_label = QLabel(self)
        title_label.setText(__appname__)
        title_label.setStyleSheet(
            "QLabel {{ font-size: {0}pt }}".format(QApplication.font().pointSize() * 1.35)
        )

        subtitle_label = QLabel(self)
        subtitle_label.setText(f"Version {__version_friendly__}")

        self.widget_layout.addWidget(icon_label, 0, 0, 2, 1)
        self.widget_layout.addWidget(title_label, 0, 1)
        self.widget_layout.addWidget(subtitle_label, 1, 1)
        self.widget_layout.setColumnStretch(0, 0)
        self.widget_layout.setColumnStretch(1, 1)

        about_label = QLabel()
        about_label.setWordWrap(True)
        about_label.setText("An overcomplicated capture card/webcam monitoring and recording tool.<br />&copy; "
                            "<a href='https://byespace.net'>byespace.net</a>, provided under the zlib license<br /><br />"
                            f"Using Qt version {QtCore.__version__}, licensed under LGPL v3.<br/><br/>"
                            "Trans rights!")
        about_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.close)

        self.window_layout.addLayout(self.widget_layout, 0, 0)
        self.window_layout.addWidget(about_label, 1, 0)
        self.window_layout.addWidget(buttons)
        self.window_layout.setRowStretch(0, 0)
        self.window_layout.setRowStretch(1, 1)
        self.window_layout.itemAt(0).setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.window_layout.itemAt(1).setAlignment(Qt.AlignmentFlag.AlignTop)

        # self.setFixedSize(self.size())