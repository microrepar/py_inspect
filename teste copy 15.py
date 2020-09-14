# -*- coding: utf-8 -*-
"""QGridLayout com QMainWindow."""
import sys

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QGridLayout)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        # Título da janela.
        self.setWindowTitle('QGridLayout com QMainWindow.')

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
        grid_layout = QGridLayout()

        # Widget central.
        widget = QWidget()
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)

        button1 = QPushButton('Button 1')
        grid_layout.addWidget(button1, 0, 0)

        button2 = QPushButton('Button 2')
        grid_layout.addWidget(button2, 0, 1)

        button3 = QPushButton('Button 3')
        # addWidget(arg__1, row, column, rowSpan, columnSpan, alignment)
        grid_layout.addWidget(button3, 1, 0, 1, 2)

        button4 = QPushButton('Button 4')
        grid_layout.addWidget(button4, 2, 0)

        button5 = QPushButton('Button 5')
        grid_layout.addWidget(button5, 2, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())