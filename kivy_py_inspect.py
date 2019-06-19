from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import *
from kivy.config import Config
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.uix.bubble import Bubble

from pywinauto import backend

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'desktop', '1')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '960')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

Builder.load_string('''
<SelectCopy>:
    size_hint: (None, None)
    size: (160, 50)
    pos_hint: {'center_x': .5, 'y': .6}
    BubbleButton:
        text: 'Select'
        on_press: root.select_row()
    BubbleButton:
        text: 'Copy'
        on_release: root.copy_row()
<SelectableLabel>:
    font_name: 'DejaVuSans.ttf'
    text_size: root.width, None
    color: 0,0,0,1
    canvas.before:
        Color:
            rgba: (0.3, 0.3, 0.3, 0.3) if self.selected else (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<TreeViewLabel>:
    font_name: 'DejaVuSans.ttf'
    text_size: root.width, None
    color: 0,0,0,1
    color_selected: (0.3, 0.3, 0.3, 0.3)
    on_touch_down:
        app.root.select_node(self)
<MyWindow>
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    id: my_window
    BoxLayout:
        id: main_boxlayout
        BoxLayout:
            padding: [5, 5, 5, 5]
            id: left_boxlayout
            orientation: 'vertical'
            Spinner:
                id: spinner
                text: 'uia'
                size_hint: (None, None)
                size: (100,44)
            ScrollView:
                id: left_scrollview
                do_scroll_x: True
                bar_width: 20
                scroll_type: ['bars', 'content']
                TreeView:
                    id: treeview
                    viewclass: 'TreeViewLabel'
                    hide_root: True
                    indent_level: 32
                    size_hint_y: None
                    size_hint_x: None
                    width: self.parent.width*3
        BoxLayout:
            padding: [5, 5, 5, 5]
            id: right_boxlayout
            orientation: 'vertical'
            Button:
                id: clipboard
                size: 150, 44
                size_hint: None, None
                text: 'Copy to clipboard'
                on_press: root.on_clipboard()
            RecycleView:
                id: recycle_view
                do_scroll_x: True
                bar_width: 20
                scroll_type: ['bars', 'content']
                viewclass: 'SelectableLabel'
                SelectableRecycleGridLayout:
                    id: recycle_grid
                    cols: 2
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    multiselect: True
                    touch_multiselect: True
''')


class SelectCopy(Bubble):
    def __init__(self, row, text, touch, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.text = text
        self.touch = touch

    def select_row(self):
        if self.row.index % 2 == 0:
            self.row.parent.select_with_touch(self.row.index, self.touch)
            self.row.parent.select_with_touch(self.row.index + 1, self.touch)
        else:
            self.row.parent.select_with_touch(self.row.index - 1, self.touch)
            self.row.parent.select_with_touch(self.row.index, self.touch)
        self.row.remove_widget(self)

    def copy_row(self):
        Clipboard.copy(self.text)
        self.row.remove_widget(self)


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    pass


class SelectableLabel(RecycleDataViewBehavior, Label, FloatLayout):
    ''' Add selection support to the Label '''
    index = None
    rv = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.rv = rv
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable and self.index != 0 and self.index != 1:
            if touch.button == 'right':
                if self.index % 2 == 0:
                    text = str(self.rv.data[self.index]['text']) + '\t' + str(self.rv.data[self.index + 1]['text'])
                else:
                    text = str(self.rv.data[self.index - 1]['text']) + '\t' + str(self.rv.data[self.index]['text'])
                self.bubb = SelectCopy(self, text, touch)
                self.add_widget(self.bubb)
                return False
            if self.index % 2 == 0:
                self.rv.data[self.index]['is_selected'] = 1 if self.rv.data[self.index]['is_selected'] == 0 else 0
                self.rv.data[self.index + 1]['is_selected'] = 1 if self.rv.data[self.index + 1]['is_selected'] == 0 else 0
                return self.parent.select_with_touch(self.index, touch) and \
                       self.parent.select_with_touch(self.index + 1, touch)
            else:
                self.rv.data[self.index - 1]['is_selected'] = 1 if self.rv.data[self.index - 1]['is_selected'] == 0 else 0
                self.rv.data[self.index]['is_selected'] = 1 if self.rv.data[self.index]['is_selected'] == 0 else 0
                return self.parent.select_with_touch(self.index - 1, touch) and \
                       self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print(end='')  # print("selection applied for {0}".format(rv.data[index]))
        else:
            print(end='')  # print("selection removed for {0}".format(rv.data[index]))


class MyWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

        self.text = str()
        self.load_backends()
        self.backend = 'uia'
        self.__initialize_calc()
        self.ids.spinner.bind(text=self.show_tree)

    def select_node(self, node):
        data = node.text
        self.show_properties(self.tree_model.props_dict.get(data))

    def load_backends(self):
        for _backend in backend.registry.backends.keys():
            self.ids.spinner.values.append(_backend)

    def on_clipboard(self):
        Clipboard.copy(self.text)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if len(modifiers) > 0 and modifiers[0] == 'ctrl' and text == 'a':  # Ctrl+a
            for cell in self.ids.recycle_view.data:
                cell['is_selected'] = 1
        if len(modifiers) > 0 and modifiers[0] == 'ctrl' and text == 'c':  # Ctrl+c
            text = 'Property\tValue\n'
            i = 0
            for cell in self.ids.recycle_view.data:
                if cell['is_selected'] == 1:
                    text += cell['text']
                    if i % 2 == 0:
                        text += '\t'
                    else:
                        text += '\n'
                i = i + 1
            Clipboard.copy(text)

    def show_properties(self, data):
        col_titles = ['Property', 'Value']
        rows_len = len(data)
        columns = len(col_titles)
        table_data = []
        self.text = str()
        for t in col_titles:
            table_data.append({'text': '[b]' + str(t) + '[/b]', 'markup': True, 'font_size': '20sp', 'is_selected': 0})
            self.text += str(t) + '\t'
        for t in range(rows_len):
            # print()
            self.text += '\n'
            for r in range(columns):
                # print(str(data[t][r]), end=' ')
                table_data.append({'text': str(data[t][r]), 'is_selected': 0})
                self.text += str(data[t][r]) + '\t'
        self.ids.recycle_grid.cols = columns
        self.ids.recycle_view.data = table_data

    def show_tree(self, spinner, text):
        self.backend = text
        self.__initialize_calc(self.backend)

    def __initialize_calc(self, _backend='uia'):
        # for correct work ScrollView
        self.ids.treeview.bind(minimum_height=self.ids.treeview.setter('height'))

        for node in list(self.ids.treeview.iterate_all_nodes()):
            self.ids.treeview.remove_node(node)
        self.element_info = backend.registry.backends[_backend].element_info_class()
        self.tree_model = MyTreeModel(self.ids.treeview, self.element_info, _backend)


class MyTreeModel():
    def __init__(self, tv, element_info, backend):
        self.props_dict = {}
        self.backend = backend
        self.branch = self.__node_name(element_info)
        root_node = tv.add_node(TreeViewLabel(text=self.branch))
        self.__generate_props_dict(element_info)
        self.__get_next(tv, element_info, root_node)

    def __get_next(self, tv, element_info, root):
        for child in element_info.children():
            self.__generate_props_dict(child)
            self.child_item = self.__node_name(child)
            parent_node = tv.add_node(TreeViewLabel(text=self.child_item), root)
            self.__get_next(tv, child, parent_node)

    def __node_name(self, element_info):
        if 'uia' == self.backend:
            return '%s "%s" (%s)' % (str(element_info.control_type), str(element_info.name), id(element_info))
        return '"%s" (%s)' % (str(element_info.name), id(element_info))

    def __generate_props_dict(self, element_info):
        props = [
            ['control_id', str(element_info.control_id)],
            ['class_name', str(element_info.class_name)],
            ['enabled', str(element_info.enabled)],
            ['handle', str(element_info.handle)],
            ['name', str(element_info.name)],
            ['process_id', str(element_info.process_id)],
            ['rectangle', str(element_info.rectangle)],
            ['rich_text', str(element_info.rich_text)],
            ['visible', str(element_info.visible)]
        ]

        props_win32 = [
        ] if (self.backend == 'win32') else []

        props_uia = [
            ['control_type', str(element_info.control_type)],
            ['element', str(element_info.element)],
            ['framework_id', str(element_info.framework_id)],
            ['runtime_id', str(element_info.runtime_id)]
        ] if (self.backend == 'uia') else []

        props.extend(props_uia)
        props.extend(props_win32)
        node_dict = {self.__node_name(element_info): props}
        self.props_dict.update(node_dict)


class Application(App):
    def build(self):
        return MyWindow()


if __name__ == "__main__":
    Application().run()
