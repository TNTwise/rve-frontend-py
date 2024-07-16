import sys
import os
from PyQt6.QtCore import QPropertyAnimation, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from mainwindow import Ui_MainWindow  # Import the UI class from the converted module

# other imports
from src.util import checkValidVideo


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # set up base variables
        self.homeDir = os.path.expanduser("~")

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

        # connect file select buttons
        self.inputFileSelectButton.clicked.connect(self.openInputFile)
        self.outputFileSelectButton.clicked.connect(self.openOutputFolder)
        # connect render button
        self.startRenderButton.clicked.connect(self.startRender)
        
    # switch menus
    def switchToHomePage(self):
        self.stackedWidget.setCurrentWidget(self.homePage)
        self.processBtn.setChecked(False)
        self.settingsBtn.setChecked(False)
        self.moreBtn.setChecked(False)

    def switchToProcessingPage(self):
        self.stackedWidget.setCurrentWidget(self.procPage)
        self.homeBtn.setChecked(False)
        self.settingsBtn.setChecked(False)
        self.moreBtn.setChecked(False)

    def switchToSettingsPage(self):
        self.stackedWidget.setCurrentWidget(self.settingsPage)
        self.homeBtn.setChecked(False)
        self.processBtn.setChecked(False)
        self.moreBtn.setChecked(False)

    def switchToMorePage(self):
        self.stackedWidget.setCurrentWidget(self.morePage)
        self.homeBtn.setChecked(False)
        self.processBtn.setChecked(False)
        self.settingsBtn.setChecked(False)

    # input file button
    def openInputFile(self):
        """
        Opens a video file and checks if it is valid,

        if it is valid, it will set self.inputFile to the input file, and set the text input field to the input file path.
        if it is not valid, it will give a warning to the user.

        """

        fileFilter = "Video files (*.mp4 *.mov *.webm)"
        inputFile, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select File",
            directory=self.homeDir,
            filter=fileFilter,
            initialFilter=fileFilter,
        )

        if checkValidVideo(inputFile):
            self.inputFile = inputFile
            self.inputFileText.setText(inputFile)

    # output file button
    def openOutputFolder(self):
        """
        Opens a folder,
        sets the directory that is selected to the self.outputFolder variable
        sets the outputFileText to the output directory
        """
        self.outputFolder = QFileDialog.getExistingDirectory(
            self,
            caption="Select Output Directory",
            directory=self.homeDir,
        )
        self.outputFileText.setText(self.outputFolder)

    def startRender(self):
        """
        Function to start the rendering process
        It will initially check for any issues with the current setup, (invalid file, no permissions, etc..)
        Then, based on the settings selected, it will build a command that is then passed into rve-backend
        Finally, It will handle the render via ffmpeg. Taking in the frames from pipe and handing them into ffmpeg on a sperate thread
        """
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
