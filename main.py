import sys
import os
import subprocess
from threading import Thread

from PyQt6.QtCore import QPropertyAnimation, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from mainwindow import Ui_MainWindow  # Import the UI class from the converted module

# other imports
from src.util import checkValidVideo, getDefaultOutputVideo, getVideoFPS, getVideoRes, getVideoLength, getVideoFrameCount


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # set up base variables
        self.homeDir = os.path.expanduser("~")
        self.interpolateTimes = 1
        self.upscaleTimes = 2
        self.pipeInFrames = None

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
        
        > IMPLEMENT AFTER SELECT AI >  Last, It will enable the output select button, and auto create a default output file 

        *NOTE
        This function will set self.videoWidth, self.videoHeight, and self.videoFPS

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
            # gets width and height from the res
            self.videoWidth, self.videoHeight = getVideoRes(inputFile)
            # get fps
            self.videoFps = getVideoFPS(inputFile)
            # get video length
            self.videoLength = getVideoLength(inputFile)
            # get video frame count
            self.videoFrameCount = getVideoFrameCount(inputFile)
            self.inputFileText.setText(inputFile)
            self.outputFileText.setEnabled(True)
            self.outputFileSelectButton.setEnabled(True)

    # output file button
    def openOutputFolder(self):
        """
        Opens a folder,
        sets the directory that is selected to the self.outputFolder variable
        sets the outputFileText to the output directory

        It will also read the input file name, and generate an output file based on it.
        """
        self.outputFolder = QFileDialog.getExistingDirectory(
            self,
            caption="Select Output Directory",
            directory=self.homeDir,
        )
        self.outputFileText.setText(self.outputFolder)

    def renderToPipeThread(self):
        command = [
            "./bin/python3.11",
            os.path.join("rve-backend-py","rve-backend.py"),
            "-i",
            self.inputFile,
            "-o",
            "PIPE",
            "--upscaleModel",
            "2x_ModernSpanimationV1.pth",  # put actual model here, this is a placeholder
            "--half",
            "-b",
            "tensorrt",
        ]

        self.pipeInFrames = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

    def ffmpegWriteThread(self):
        command = [
            f"{os.path.join('bin','ffmpeg')}",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-vcodec",
            "rawvideo",
            "-s",
            f"{self.videoWidth * self.upscaleTimes}x{self.videoHeight * self.upscaleTimes}",
            "-r",
            f"{self.videoFps * self.interpolateTimes}",
            "-i",
            "-",
            "-i",
            self.inputFile,  # see if audio bugs come up
            "-c:v",
            "libx264",
            f"-crf",
            f"18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            f"out10.mp4",  # placeholder
            "-y",
        ]
        writeOutFrames = subprocess.Popen(
            
            command,
            stdin=subprocess.PIPE,
            text=True,
            universal_newlines=True,
        )

        outputChunk = (
            self.videoWidth
            * self.videoHeight
            * self.upscaleTimes
            * self.upscaleTimes
            * 3
        )  # 3 is for the channels (RGB)

        totalFrames = int(self.videoFrameCount * self.interpolateTimes)
        for i in range(totalFrames-1):
            frame = self.pipeInFrames.stdout.read(outputChunk)
            writeOutFrames.stdin.buffer.write(frame)
        writeOutFrames.stdin.close()
        writeOutFrames.wait()

    def startRender(self):
        """
        Function to start the rendering process
        It will initially check for any issues with the current setup, (invalid file, no permissions, etc..)
        Then, based on the settings selected, it will build a command that is then passed into rve-backend
        Finally, It will handle the render via ffmpeg. Taking in the frames from pipe and handing them into ffmpeg on a sperate thread
        """

        # Gui changes
        self.startRenderButton.setEnabled(False)
        
        self.renderToPipeThread()
        #self.ffmpegWriteThread()
        writeThread = Thread(target=self.ffmpegWriteThread)
        writeThread.start()

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
