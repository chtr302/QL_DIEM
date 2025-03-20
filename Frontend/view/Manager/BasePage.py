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

        self.add_demo_content()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.create_toolbar()
        self.create_department_panel()

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

    def create_department_panel(self):
        self.dept_panel = QWidget()
        self.dept_layout = QGridLayout(self.dept_panel)
        self.dept_layout.setContentsMargins(10, 10, 10, 10)
        
        self.dept_panel.setStyleSheet("""
            background-color: #f8f8f8;
            border: 1px solid #dddddd;
            border-radius: 5px;
        """)

        dept_label = QLabel('Khoa:')
        dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dept_label.setStyleSheet("""
            font-weight: bold;
            font-size: 16pt;
            color: black;
            padding: 5px 20px;
        """)

        self.dept_layout.addWidget(dept_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        if self.user_info and 'Role' in self.user_info:
            if self.user_info['Role'] == 'PGV':
                self.dept_combo = QComboBox()
                self.dept_combo.setMinimumWidth(400)
                self.dept_combo.setStyleSheet("""
                    padding: 8px;
                    font-size: 14pt;
                    min-height: 25px;
                    border: 1px solid #bbbbbb;
                    border-radius: 3px;
                """)
                self.dept_combo.currentIndexChanged.connect(self.on_department_changed)
                self.dept_layout.addWidget(self.dept_combo, 0, 1, 1, 1)
                
                self.load_departments()

                refresh_btn = QPushButton("Làm mới")
                refresh_btn.setIcon(QIcon(f"{IMG_PATH}/refresh.png"))
                refresh_btn.setIconSize(QSize(24, 24))
                refresh_btn.setStyleSheet("""
                    padding: 8px 15px;
                    font-size: 14pt;
                    font-weight: bold;
                    min-height: 25px;
                    background-color: #white;
                    border: 1px solid #bbbbbb;
                    border-radius: 3px;
                """)
                refresh_btn.clicked.connect(self.load_departments)
                self.dept_layout.addWidget(refresh_btn, 0, 2, 1, 1)
                
            elif self.user_info['Role'] == 'KHOA':
                if 'Khoa' in self.user_info:
                    dept_info = QLabel(f"{self.user_info['Khoa']}")
                    dept_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    dept_info.setStyleSheet("""
                        font-weight: bold;
                        font-size: 18pt;
                        color: black;
                        background: white;
                    """)
                    self.dept_layout.addWidget(dept_info, 0, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
                else:
                    dept_info = QLabel("Không có thông tin khoa")
                    dept_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    dept_info.setStyleSheet("""
                        font-style: italic;
                        font-size: 16pt;
                        color: #666666;
                        padding: 5px 20px;
                    """)
                    self.dept_layout.addWidget(dept_info, 0, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        else:
            dept_info = QLabel("Chưa đăng nhập hoặc không có quyền truy cập")
            dept_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dept_info.setStyleSheet("""
                font-style: italic;
                font-size: 16pt;
                color: #666666;
                padding: 5px 20px;
            """)
            self.dept_layout.addWidget(dept_info, 0, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.dept_layout.setColumnStretch(0, 1)
        self.dept_layout.setColumnStretch(1, 3)
        self.dept_layout.setColumnStretch(2, 1)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.dept_panel)

        self.main_layout.addWidget(container)

    def load_departments(self):
        if not hasattr(self, 'dept_combo') or not self.connection:
            return
        self.dept_combo.clear()
        try:
            self.dept_combo.addItem("Tất cả khoa", None)
            cursor = self.connection.cursor()
            cursor.execute("SELECT TENKHOA FROM Khoa ORDER BY TENKHOA")
            departments = cursor.fetchall()
            for dept in departments:
                tenkhoa = dept[0].strip() if isinstance(dept[0], str) else dept[0]
                self.dept_combo.addItem(f"{tenkhoa}")
            cursor.close()
        except Exception as e:
            print(f"Bug: {e}")

    def on_department_changed(self, index):
        """Xử lý khi người dùng thay đổi khoa được chọn"""
        selected_dept = self.dept_combo.currentData()
        self.update_ui_by_department(selected_dept)
        
    def update_ui_by_department(self, dept_code):
        message = ""
        if dept_code is None:
            message = "Đang xem dữ liệu: Tất cả khoa"
        else:
            message = f"Đang xem dữ liệu: Khoa {dept_code}"

        print(message)

    def add_demo_content(self):
        """Thêm nội dung demo để xem layout"""
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        
        # Thêm một số trường nhập liệu
        self.id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.description_edit = QTextEdit()
        
        form_layout.addRow("ID:", self.id_edit)
        form_layout.addRow("Tên:", self.name_edit)
        form_layout.addRow("Mô tả:", self.description_edit)
        
        self.main_layout.addWidget(form_widget)
        
        # Bảng dữ liệu demo
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Tên", "Mô tả"])
        
        # Thêm một số dữ liệu mẫu
        for i in range(5):
            self.table.setItem(i, 0, QTableWidgetItem(f"ID-{i+1}"))
            self.table.setItem(i, 1, QTableWidgetItem(f"Mục {i+1}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"Mô tả cho mục {i+1}"))
        
        self.main_layout.addWidget(self.table)
        
        # Trạng thái
        self.status_label = QLabel("Sẵn sàng")
        self.main_layout.addWidget(self.status_label)
    
    def show_message(self, message):
        """Hiển thị thông báo khi nhấn các nút"""
        QMessageBox.information(self, "Thông báo", f"Bạn đã nhấn: {message}")
        self.status_label.setText(f"Đã thực hiện: {message}")

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