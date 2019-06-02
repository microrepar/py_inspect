## PyInspect

**Dmitry Vodopyanov, Alexander Smirnov**  
*Lobachevsky University, Nizhny Novgorod, Russia*

Simple Inspect.exe analogue for Windows using Python 3.5, pywinauto and PyQt/Kivy.

#### Requirements

- Windows OS (Windows 10 is preferable)
- [Python 3.7](https://www.python.org/downloads/release/python-373/)
- If you want use PyQt5:  
  ```pip install -r requirements_PyQt5.txt```
- If you want use Kivy:  
  ```pip install -r requirements_Kivy.txt```
- To create executable for PyQt5
  ```pyinstaller --onefile --windowed py_inspect.py```
- To create executable for Kivy
  ```pyinstaller PyInspect.spec```
  
#### Run
- If you want use PyQt5:  
```python3 py_inspect.py```
- If you want use Kivy:  
```python3 kivy_py_inspect.py```