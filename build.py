from PyQt6 import sip
from PyQt6.uic import compileUi
import os
def build_gui():
    with open("mainwindow.py", 'w') as f:
        compileUi("testRVEInterface.ui",f)
        f.write('\nimport resources_rc')
def build_resources():
    os.system("pyside6-rcc -o resources_rc.py resources.qrc")


build_gui()
build_resources()