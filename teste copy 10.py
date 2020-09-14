from PySide2.QtWidgets import QApplication, QMainWindow, QProgressBar, QStatusBar, QLabel, QPushButton
import sys
from PySide2.QtGui import QIcon
from PySide2.QtCore import QBasicTimer


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ProgressBar")
        self.setGeometry(300,200,500,400)

        self.statusLabel = QLabel("Showing Progress")
        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        
        self.button = QPushButton('OK', self)
        self.button.clicked.connect(self.clicou)


        self.setIcon()

        self.createStatusBar()

    def clicou(self):
        print('clicou!')

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)


    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.progressbar.setValue(10)
        self.statusBar.addWidget(self.statusLabel, 1)
        self.statusBar.addWidget(self.progressbar, 2)
        self.setStatusBar(self.statusBar)

        #timer creating
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(100, self)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
        self.step += 1
        self.progressbar.setValue(self.step)




if __name__ == "__main__":
    myapp = QApplication(sys.argv)
    window = Window()
    window.show()


    myapp.exec_()
    sys.exit()