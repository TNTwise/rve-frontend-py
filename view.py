from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUiType

# Load the .ui file
def load_ui(ui_file, base_instance=None):
   
    ui = loadUiType(ui_file, base_instance)
    return ui

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Example usage
    ui_file = "testRVEInterface.ui"
    widget = load_ui(ui_file)
    widget.show()
    
    sys.exit(app.exec_())
