from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

IMG_PATH = 'Frontend/assets/image/ToolbarBasePage'

class BasePage(QWidget):
    def __init__(self, parent=None, connection=None, user_info=None):
        super().__init__(parent)
        self.connection = connection
        self.user_info = user_info

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

    def create_toolbar(self):
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        # Tạo toolbar
        self.toolbar = QToolBar("Chức năng", self)
        self.toolbar.setMovable(False)  # Không cho di chuyển
        self.toolbar.setIconSize(QSize(38, 38))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)  # Chữ bên cạnh

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)

        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: white;
                spacing: 20px;
                padding: 10px;
                min-height: 70px;
                border: 1px solid #dddddd;
            }
            QToolButton {
                background-color: white;
                margin-right: 15px;
                padding: 8px 15px;
                font-size: 12pt;
                font-weight: bold;
                border: none;
            }
            QToolButton:hover {
                background-color: #f0f0f0;
            }
            QToolButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        self.add_action = QAction(QIcon(f"{IMG_PATH}/add.png"), "Thêm", self)
        self.add_action.triggered.connect(lambda: self.show_message("Thêm mới"))
        self.add_action.setFont(font)
        self.toolbar.addAction(self.add_action)

        self.toolbar.addSeparator() # Thêm khoảng cách sau nút
        
        self.delete_action = QAction(QIcon(f"{IMG_PATH}/remove.png"), "Xóa", self)
        self.delete_action.triggered.connect(lambda: self.show_message("Xóa"))
        self.delete_action.setFont(font)
        self.toolbar.addAction(self.delete_action)
        
        self.toolbar.addSeparator()
        
        self.edit_action = QAction(QIcon(f"{IMG_PATH}/edit.png"), "Sửa", self)
        self.edit_action.triggered.connect(lambda: self.show_message("Sửa"))
        self.edit_action.setFont(font)
        self.toolbar.addAction(self.edit_action)
        
        self.toolbar.addSeparator()
        
        self.save_action = QAction(QIcon(f"{IMG_PATH}/save.png"), "Ghi", self)
        self.save_action.triggered.connect(lambda: self.show_message("Ghi dữ liệu"))
        self.save_action.setFont(font)
        self.toolbar.addAction(self.save_action)
        
        self.toolbar.addSeparator()
        
        self.restore_action = QAction(QIcon(f"{IMG_PATH}/undo.png"), "Phục hồi", self)
        self.restore_action.triggered.connect(lambda: self.show_message("Phục hồi"))
        self.restore_action.setFont(font)
        self.toolbar.addAction(self.restore_action)
        
        # Thêm spacer để đẩy nút Thoát sang bên phải
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)
        
        self.exit_action = QAction(QIcon(f"{IMG_PATH}/exit.png"), "Thoát", self)
        self.exit_action.triggered.connect(lambda: self.close())
        self.exit_action.setFont(font)
        self.toolbar.addAction(self.exit_action)
        
        # Thêm toolbar vào layout của widget
        self.main_layout.addWidget(self.toolbar)

def main():
    app = QApplication(sys.argv)
    
    # Thiết lập style cho ứng dụng
    app.setStyle("Fusion")
    
    # Tạo palette sáng
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(230, 230, 230))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    # Tạo instance của BasePage
    base_page = BasePage()
    base_page.setWindowTitle("Demo BasePage")
    base_page.resize(1790, 1000)  # Sử dụng kích thước theo yêu cầu
    base_page.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()