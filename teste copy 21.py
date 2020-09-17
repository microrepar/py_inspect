import sys
import time

from PySide2.QtCore import QObject, QThread, Signal, Slot
from PySide2.QtWidgets import QApplication, QWidget

from pynput import keyboard


class OtherThread(QThread):
    over = Signal(object, object)
    off = Signal(object)

    def run(self):        

        def on_activate_h():
            self.over.emit('Global hotkey on_activate_h', self)
            self.running = True

        def on_activate_i():
            print('Global hotkey on_activate_i')
            self.running = False
            # h.stop()
                
        with keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+h': on_activate_h,
                '<ctrl>+<alt>+i': on_activate_i}) as h:
            h.join()
      
        self.off.emit('Global hotkey On_teste!')


class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()
        
        self.thread = OtherThread(self)
        self.thread.over.connect(self.on_over)
        self.thread.off.connect(self.on_off)
        self.thread.start()

        
    @Slot(object)
    def on_over(self, value, thread):
        while True:
            print('Thread Value', value)
            time.sleep(2)
            if thread.running is False:
                break

    @Slot(object)
    def on_off(self, value):
        print('Turned off')
        # self.close()



if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    myapp = MyApp()
    sys.exit(app.exec_())





