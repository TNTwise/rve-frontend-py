from PyQt6 import sip
from PyQt6.uic import compileUi

def build_gui():
    with open("mainwindow.py", 'w') as f:
        compileUi("testRVEInterface.ui",f)
        f.write('\nimport resources_rc')

build_gui()