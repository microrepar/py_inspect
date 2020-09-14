import sys

from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QMouseEvent, QPixmap
from PySide2.QtWidgets import (QApplication, QFileDialog, QLabel, QWidget)


class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super(CustomLabel, self).__init__(parent)
        self.setMouseTracking(True)
        
    def mousePressEvent(self, e):
        img, re = QFileDialog.getOpenFileName(self, 'Selecionar Arquivo', filter='All(*.png *.jpg)')
        if re:
            self.setPixmap(QPixmap(img).scale(250,150,Qt.KeepAspectRatio))

    def mouseMoveEvent(self, event: QMouseEvent):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event: QEvent):
        QApplication.setOverrideCursor(Qt.ArrowCursor)


class HandlerWindow(QWidget):
    def __init__(self, parent=None):
        super(HandlerWindow, self).__init__(parent)
        self.resize(300,350)
        self.label = CustomLabel(self)
        self.label.setPixmap(QPixmap('imgs/user.png').scaled(250,150, Qt.KeepAspectRatio))
    

if __name__ == "__main__":
    root = QApplication(sys.argv)
    app = HandlerWindow()
    app.show()
    sys.exit(root.exec_())
