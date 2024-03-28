import sys
from PySide6.QtWidgets import QApplication
import preprocessing
from controller import NLPToolkitController
from ui import NLPToolkitUI

def main():
    app = QApplication(sys.argv)
    controller = NLPToolkitController()  # Instantiate the controller
    mainWindow = NLPToolkitUI(controller)  # Pass the controller as an argument
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
