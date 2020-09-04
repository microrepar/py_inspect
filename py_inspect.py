import contextlib
import sys
import warnings
from typing import Tuple
from pyautogui import alert

import pyperclip
from PIL import Image
from PySide2.QtCore import (QAbstractTableModel, QCoreApplication, QLocale,
                            QRect, Qt)
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import (QApplication, QComboBox, QTableView, QTreeView,
                               QWidget)
from pywinauto import Desktop, backend

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2


def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())


class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.setFixedSize(930, 631)
        self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "PyInspect"))

        self.central_widget = QWidget(self)

        self.comboBox = QComboBox(self.central_widget)
        self.comboBox.setGeometry(QRect(10, 10, 451, 22))
        self.comboBox.setMouseTracking(False)
        self.comboBox.setMaxVisibleItems(5)
        self.comboBox.setObjectName("comboBox")

        for _backend in backend.registry.backends.keys():
            self.comboBox.addItem(_backend)

        self.tree_view = QTreeView(self.central_widget)
        self.tree_view.setGeometry(QRect(10, 40, 451, 581))
        self.tree_view.setColumnWidth(0, 150)

        self.comboBox.setCurrentText('uia')
        self.__show_tree()

        self.table_view = QTableView(self.central_widget)
        self.table_view.setGeometry(QRect(470, 40, 451, 581))

        self.comboBox.activated[str].connect(self.__show_tree)
        self.tree_view.clicked.connect(self.__show_property)

    def __show_tree(self, _backend='uia'):        
        self.__initialize_calc(_backend)

    def __initialize_calc(self, _backend):
        self.element_info = backend.registry.backends[_backend].element_info_class()
        self.tree_model = MyTreeModel(self.element_info, _backend)
        self.tree_model.setHeaderData(0, Qt.Horizontal, 'Controls')
        self.tree_view.setModel(self.tree_model)        

    def __show_property(self, index=None):
        data = index.data()
        self.table_model = MyTableModel(self.tree_model.props_dict.get(data), self)
        self.table_view.wordWrap()
        self.table_view.setModel(self.table_model)
        self.table_view.setColumnWidth(1, 320)
        
        element = self.tree_model.element_dict.get(data, None)
        if element is not None: 
            element.set_focus()
            locate_element =  center_locate_element(element)
            pyperclip.copy('{0}, {1}'.format(*locate_element))
            
            im: Image = element.capture_as_image()
            if im is not None and hasattr(im, 'show'):
                with contextlib.suppress(Exception):
                    im.show()
            else:
                alert(title='Atenção', text='O elemento selecionado não é uma imagem ou não contém o atributo show.')
            
            element.draw_outline(colour='green', thickness=4)


class MyTreeModel(QStandardItemModel):
    def __init__(self, element_info, _backend):
        QStandardItemModel.__init__(self)
        root_node = self.invisibleRootItem()
        self.props_dict = {}
        self.element_dict = {}
        self.backend = _backend
        self.branch = QStandardItem(self.__node_name(element_info))
        self.branch.setEditable(False)
        root_node.appendRow(self.branch)
        self.__generate_props_dict(element_info)
        self.__get_next(element_info, self.branch)

    def __get_next(self, element_info, parent):
        for child in element_info.children():
            self.__generate_props_dict(child)
            child_item = QStandardItem(self.__node_name(child))
            child_item.setEditable(False)
            parent.appendRow(child_item)
            self.__get_next(child, child_item)

    def __node_name(self, element_info):
        if 'uia' == self.backend:
            return '%s "%s" (%s)' % (str(element_info.control_type), str(element_info.name), id(element_info))
        return '"%s" (%s)' % (str(element_info.name), id(element_info))

    def __generate_props_dict(self, element_info):

        element = backend.registry.backends[self.backend].generic_wrapper_class(element_info)
        
        props = [
                    ['control_id', str(element_info.control_id)],
                    ['class_name', str(element_info.class_name)],
                    ['enabled', str(element_info.enabled)],
                    ['handle', str(element_info.handle)],
                    ['name', str(element_info.name)],
                    ['process_id', str(element_info.process_id)],
                    ['rectangle', str(element_info.rectangle)],
                    ['rich_text', str(element_info.rich_text)],
                    ['visible', str(element_info.visible)],
                ] 

        props_win32 = [
                        [''.center(15, '*'), 'METHODS'.center(50, '*')]
                      ] + [['', e] for e in dir(element) if not e.startswith('_') and not e[0].isupper()] if (self.backend == 'win32') else []

        props_uia = [
                        ['control_type', str(element_info.control_type)],
                        ['element', str(element_info.element)],
                        ['framework_id', str(element_info.framework_id)],
                        ['runtime_id', str(element_info.runtime_id)],
                        [''.center(15, '*'), 'METHODS'.center(50, '*')]
                        
                    ] + [['', e] for e in dir(element) if not e.startswith('_') and not e[0].isupper()] if (self.backend == 'uia') else []

        props.extend(props_uia)
        props.extend(props_win32)
        node_dict = {self.__node_name(element_info): props}
        self.props_dict.update(node_dict)
        element_dict = {self.__node_name(element_info): element}
        self.element_dict.update(element_dict)


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.header_labels = ['Property', 'Value']

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.arraydata[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)


def get_rectangle(element: Desktop)-> Tuple[int]:
    rectangle = element.rectangle()    
    return rectangle.left, rectangle.top, rectangle.right, rectangle.bottom


def center_locate_element(element)-> Tuple:
    box = get_rectangle(element)
    x1, y1, x2, y2 = box
    center = int(x1 + abs(x1-x2)/2), int(y1 + abs(y1-y2)/2)
    return center


if __name__ == "__main__":
    main()
    