from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
from Backend.controllers.auth_login import AuthLogin


class Login(QWidget):
    login_success_signal = pyqtSignal(str, object, object)
    
    def __init__(self):
        super().__init__()
        
        # Thiết lập cửa sổ
        self.setWindowTitle('Login')
        self.setGeometry(200,200,400,400)
        self.setStyleSheet("background-color: white;")
        
        # Khởi tạo biến
        self.show_password = False
        self.user_type = "GV"  # Mặc định là Giảng viên
        self.label_username = None  # Khởi tạo trước để tránh AttributeError
        
        # Tạo giao diện chính
        self.main_content()
    
    def main_content(self):
        # Layout chính
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Các phần của giao diện
        self.title(main_layout)
        self.logo(main_layout)
        self.user_type_func(main_layout)
        self.main(main_layout)
        
        # Thêm khoảng trống ở cuối
        main_layout.addStretch()
    
    def title(self, parent_layout):
        title_label = QLabel("Học viện Công nghệ Bưu chính Viễn thông\n \n Cơ sở tại TP.Hồ Chí Minh")
        title_label.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: black; background-color: white;")
        
        parent_layout.addWidget(title_label)
    
    def logo(self, parent_layout):
        logo_label = QLabel()
        logo_pixmap = QPixmap('Frontend/assets/Image/PTIT_IMAGE.png')
        logo_pixmap = logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        parent_layout.addWidget(logo_label)
    
    def user_type_func(self, parent_layout):
        user_type_layout = QVBoxLayout()
        
        user_type_label = QLabel("Bạn là")
        user_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_type_label.setStyleSheet("background-color: white;")
        user_type_layout.addWidget(user_type_label)

        radio_layout = QHBoxLayout()
        radio_layout.setContentsMargins(0, 0, 0, 0)
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.gv_radio = QRadioButton("Giảng viên")
        self.sv_radio = QRadioButton("Sinh viên")
        self.gv_radio.setStyleSheet("background-color: white; color: black;")
        self.sv_radio.setStyleSheet("background-color: white; color: black;")
        
        self.gv_radio.setChecked(True)
        
        radio_layout.addWidget(self.gv_radio)
        radio_layout.addWidget(self.sv_radio)
        
        user_type_layout.addLayout(radio_layout)
        parent_layout.addLayout(user_type_layout)
    
    def main(self, parent_layout):
        main_frame = QFrame()
        main_frame.setStyleSheet("background-color: white;")
        
        # Sử dụng grid layout
        grid_layout = QGridLayout(main_frame)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(10)
        
        # Username label
        self.label_username = QLabel("Tài Khoản:")
        self.label_username.setStyleSheet("background-color: white; color: black;")
        grid_layout.addWidget(self.label_username, 0, 0)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("background-color: white; border: 1px solid #ddd; padding: 5px;")
        self.username_input.setFixedHeight(30)
        grid_layout.addWidget(self.username_input, 0, 1)
        
        # Password label
        label_password = QLabel("Mật khẩu:")
        label_password.setStyleSheet("background-color: white; color: black;")
        grid_layout.addWidget(label_password, 1, 0)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("background-color: white; border: 1px solid #ddd; padding: 5px;")
        self.password_input.setFixedHeight(30)
        grid_layout.addWidget(self.password_input, 1, 1)
        
        # Show password checkbox
        checkbox_password = QCheckBox("Xem mật khẩu")
        checkbox_password.setStyleSheet("background-color: white;")
        checkbox_password.toggled.connect(self.show_pass)
        grid_layout.addWidget(checkbox_password, 1, 2)
        
        # Tạo layout cho nút đăng nhập và thoát
        buttons_layout = QHBoxLayout()
        
        # Login button
        button_login = QPushButton("Đăng nhập")
        button_login.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
        """)
        button_login.setFixedSize(150, 40)
        button_login.clicked.connect(self.login)
        buttons_layout.addWidget(button_login)
        
        # Exit button
        button_exit = QPushButton("Thoát")
        button_exit.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        button_exit.setFixedSize(150, 40)
        button_exit.clicked.connect(self.exit_app)
        buttons_layout.addWidget(button_exit)
        
        # Thêm layout chứa các nút vào grid layout
        grid_layout.addLayout(buttons_layout, 2, 1, Qt.AlignmentFlag.AlignCenter)
        
        parent_layout.addWidget(main_frame)
        
        # Kết nối radio buttons sau khi đã tạo label_username
        self.gv_radio.toggled.connect(self.radio_toggled)
        self.sv_radio.toggled.connect(self.radio_toggled)
    
    def radio_toggled(self):
        # Bảo vệ khỏi AttributeError
        if not hasattr(self, 'label_username') or self.label_username is None:
            return
            
        # Cập nhật user_type và label khi thay đổi radio button
        if self.gv_radio.isChecked():
            self.user_type = "GV"
            self.label_username.setText("Tài Khoản:")
        else:
            self.user_type = "SV"
            self.label_username.setText("Mã Sinh viên:")
    
    def show_pass(self, checked):
        # Hiển thị/ẩn mật khẩu
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        print(f"Đang thử đăng nhập với: {username}, {password}")
        
        try:
            result = AuthLogin.check_login(username, password)
            print(f"Kết quả đăng nhập: {result}")
            
            if result:
                user_type, connection = result
                user_info = None
                
                if user_type == 'GV':
                    user_info = AuthLogin.get_login_info(username)
                
                print(f"Phát signal với: {user_type}, {connection}, {user_info}")
                # Phát signal đăng nhập thành công
                self.login_success_signal.emit(user_type, connection, user_info)
            else:
                # Hiển thị thông báo lỗi
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Lỗi đăng nhập", 
                                "Tên đăng nhập hoặc mật khẩu không chính xác.")
        except Exception as e:
            print(f"Lỗi khi đăng nhập: {e}")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Lỗi hệ thống", 
                            f"Có lỗi xảy ra: {e}")
            
    def exit_app(self):
        """
        Đóng ứng dụng khi người dùng nhấn nút thoát
        """
        print("Đóng ứng dụng")
        QApplication.quit()