from PySide2.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, 
                            QHBoxLayout, QMessageBox, QRadioButton, QGroupBox, 
                            QVBoxLayout)


import sys


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.button = QPushButton('Exibir Mensagem')
        self.button.clicked.connect(self.exibir)
        self.line_edit = QLineEdit()

        # Group box of widgets
        self.group_box = QGroupBox('Opções de Diálogo')

        # Options
        self.option_information = QRadioButton('Information')
        self.option_information.setChecked(True)
        self.option_warning = QRadioButton('Warning')
        self.option_critical = QRadioButton('Critical')

        # Layout of items of group box
        self.layout_options = QVBoxLayout()
        self.layout_options.addWidget(self.option_information)
        self.layout_options.addWidget(self.option_warning)
        self.layout_options.addWidget(self.option_critical)
        self.group_box.setLayout(self.layout_options)

        # Layout of QPushButton e QLineEdit
        self.layout_first_widgets = QHBoxLayout()
        self.layout_first_widgets.addWidget(self.line_edit)
        self.layout_first_widgets.addWidget(self.button)

        # Main layout
        self.layout_master = QVBoxLayout()
        self.layout_master.addLayout(self.layout_first_widgets)
        self.layout_master.addWidget(self.group_box)
        
        self.setLayout(self.layout_master)

    def exibir(self):
        text = self.line_edit.text()
        if self.option_information.isChecked():
            self.message_box = QMessageBox.information(self, 'Exemplo 1', text)
        elif self.option_warning.isChecked():
            self.message_box = QMessageBox.warning(self, 'Exemplo 1', text)
        else:
            self.message_box = QMessageBox.critical(self, 'Exemplo 1', text)

    def closeEvent(self, e):
        e.ignore()
        question_close = QMessageBox.question(self, 'Fechamento', "Deseja realmente fechar a aplicação?", 
                                            QMessageBox.Yes | QMessageBox.No)
        if question_close == QMessageBox.Yes:
            exit(0)
    

if __name__ == "__main__":
    root = QApplication(sys.argv)
    app = Window()
    app.show()
    sys.exit(root.exec_())
