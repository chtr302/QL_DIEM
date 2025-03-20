from PyQt6.QtWidgets import QApplication
from Backend.controllers.app_controller import AppController
import sys

def main():
    app = QApplication(sys.argv)  
    controller = AppController()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()