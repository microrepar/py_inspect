import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ['Hallo Welt', 'Hei maailma', 'Hola Mundo', 'Привет мир']

        self.button = QtWidgets.QPushButton('Click me!')
        self.text = QtWidgets.QLabel('Hello World')
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(random.choice(self.hello))



def executar():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    my_widget = MyWidget()
    my_widget.show()
    app.exec_()


if __name__ == "__main__":
    executar()
    sys.exit(0)
