from PyQt6.QtWidgets import QApplication
from Frontend.view.Login import Login
import sys

app = QApplication(sys.argv)
login = Login()
login.show()
sys.exit(app.exec())