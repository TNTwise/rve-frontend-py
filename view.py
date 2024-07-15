import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from mainwindow import Ui_MainWindow # Import the UI class from the converted module

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.setWindowTitle("REAL Video Enhancer")

    # connect buttons to switch menus
        self.homeBtn.clicked.connect(self.switchToHomePage)
        self.processBtn.clicked.connect(self.switchToProcessingPage)
        self.settingsBtn.clicked.connect(self.switchToSettingsPage)
        self.moreBtn.clicked.connect(self.switchToMorePage)
    # set default home page
        self.stackedWidget.setCurrentIndex(0)

    #switch menus
    def switchToHomePage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.processBtn.setChecked(False)
        self.settingsBtn.setChecked(False)
        self.moreBtn.setChecked(False)

    def switchToProcessingPage(self):
        self.stackedWidget.setCurrentIndex(1)
        self.homeBtn.setChecked(False)
        self.settingsBtn.setChecked(False)
        self.moreBtn.setChecked(False)
    
    def switchToSettingsPage(self):
        self.stackedWidget.setCurrentIndex(2)
        self.homeBtn.setChecked(False)
        self.processBtn.setChecked(False)
        self.moreBtn.setChecked(False)

    def switchToMorePage(self):
        self.stackedWidget.setCurrentIndex(3)
        self.homeBtn.setChecked(False)
        self.processBtn.setChecked(False)
        self.settingsBtn.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
