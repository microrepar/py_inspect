from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sys
from PySide2.QtGui import QIcon


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pyside2 QPushButton")
        self.setGeometry(500,400,500,400)

        self.setIcon()
        self.setButton()

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def setButton(self):
        btn1 = QPushButton("Quit", self)
        btn1.move(50,100)
        btn1.clicked.connect(self.quiteApp)

    def quiteApp(self):
        userInfo = QMessageBox.question(self, "Confirmation", "Do You Want To Quit The Application",
                                        QMessageBox.Yes | QMessageBox.No)

        if userInfo == QMessageBox.Yes:
            myapp.quit()

        elif userInfo == QMessageBox.No:
            print('Quit cancelled')



if __name__ == "__main__":
    myapp = QApplication(sys.argv)
    window = Window()
    window.show()
    myapp.exec_()
    sys.exit()