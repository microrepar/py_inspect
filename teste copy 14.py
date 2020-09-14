"""QFormLayout com QMainWindow."""
import sys

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import (QApplication, QFormLayout, QLineEdit,
                               QMainWindow, QPushButton, QWidget)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        # Título da janela.
        self.setWindowTitle('QFormLayout com QMainWindow.')

        # Ícone da janela principal
        icon = QIcon()
        icon.addPixmap(QPixmap('../../../images/icons/icon.png'))
        self.setWindowIcon(icon)

        # Tamanho inicial da janela.
        available_geometry = app.desktop().availableGeometry(self)        
        width = available_geometry.width()
        height = available_geometry.height()
        self.resize(width / 2, height / 2)

        # Tamanho mínimo da janela.
        self.setMinimumSize(width / 2, height / 2)

        # Tamanho maximo da janela.
        self.setMaximumSize(width - 200, height - 200)

        # Layout.
        form_layout = QFormLayout()

        # Widget central.
        widget = QWidget()
        widget.setLayout(form_layout)
        self.setCentralWidget(widget)

        button1 = QPushButton('Button 1')
        line_edit1 = QLineEdit()
        form_layout.addRow(button1, line_edit1)

        button2 = QPushButton('Button 2')
        line_edit2 = QLineEdit()
        form_layout.addRow(button2, line_edit2)

        button3 = QPushButton('Button 3')
        line_edit3 = QLineEdit()
        form_layout.addRow(button3, line_edit3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())