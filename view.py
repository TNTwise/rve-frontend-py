import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import Ui_MainWindow # Import the UI class from the converted module

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.homeBtn.clicked.connect(lambda: self.ui.homeBtn.setStyleSheet('QPushButton:checked { background-color: #6FC; }'
                           'QPushButton { background-color: #CCC; }'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
