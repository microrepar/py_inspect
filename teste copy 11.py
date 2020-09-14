import sys

from PySide2.QtCore import Qt, QTimer, QRect
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (QApplication, QFileDialog, QGridLayout, QLabel,
                               QPushButton, QWidget)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.preview_screen = QApplication.primaryScreen().grabWindow(0)
        self.settings()
        self.create_widgets()
        self.set_layout()
        print(type(self.preview_screen))

    def settings(self):
        self.resize(370, 270)
        self.setWindowTitle('Screenshoter')

    def create_widgets(self):
        self.img_preview = QLabel()
        self.img_preview.setPixmap(self.preview_screen.scaled(350,350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.btn_save_screenshot = QPushButton('Save screenshot')
        self.btn_new_screenshot = QPushButton('New screenshot')
                
        # Signals connections
        self.btn_save_screenshot.clicked.connect(self.save_screenshot)
        self.btn_new_screenshot.clicked.connect(self.new_screenshot)
    
    def set_layout(self):
        self.img_preview.setParent(self)
        self.img_preview.move(10, 10)

        self.btn_save_screenshot.setParent(self)
        self.btn_new_screenshot.setParent(self)
        self.btn_save_screenshot.move(10,240)
        self.btn_new_screenshot.move(100,240)
        

    def save_screenshot(self):
        img, _ = QFileDialog.getSaveFileName(self, 'Salvar Arquivo', filter='PNG(*.png);; JPEG(*.jpg)')
        if img[-3:] == 'png':
            self.preview_screen.save(img, 'png')
        elif img[-3:] == 'jpg':
            self.preview_screen.save(img, 'jpg')
    
    def new_screenshot(self):
        self.hide()
        QTimer.singleShot(500, self.take_screenshot)
        

    def take_screenshot(self):
        self.preview_screen = QApplication.primaryScreen().grabWindow(0)
        self.img_preview.setPixmap(self.preview_screen.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    sys.exit(0)
