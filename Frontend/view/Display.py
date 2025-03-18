from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

class Display(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self, user_type, connection, user_info):
        super().__init__()

        self.user_type = user_type
        self.connection = connection
        self.user_info = user_info
        
        # Set window properties
        self.setWindowTitle('Quản lý điểm sinh viên')
        self.setFixedSize(1800, 1000)
        
        # Initialize UI
        self.setup_ui()
        self.create_menu()
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Display user info in status bar
        if user_type == 'GV' and user_info is not None:
            try:
                self.setWindowTitle('Hệ thống Quản lý điểm Sinh viên - Giảng viên')
                self.status_bar.showMessage(f'Mã giảng viên: {user_info["MaGV"]} | Họ và Tên: {user_info["HoTen"]} | Quyền: {user_info["Role"]}')
            except (KeyError, TypeError):
                self.status_bar.showMessage('Đăng nhập với quyền Giảng viên')
        elif user_type == 'SV' and user_info is not None:
            try:
                self.setWindowTitle('Hệ thống xem điểm và đăng ký Lớp tín chỉ - Sinh viên')
                self.status_bar.showMessage(f'Mã sinh viên: {user_info["MaSV"]} | Họ và Tên: {user_info["Ten"]} | Quyền: Sinh viên')
            except (KeyError, TypeError):
                self.status_bar.showMessage('Đăng nhập với quyền Sinh viên')
        else:
            self.status_bar.showMessage('Chưa đăng nhập')

    def create_menu(self):
        """Tạo menu chính cho ứng dụng"""
        menubar = self.menuBar()
        
        # Menu hệ thống
        file_menu = menubar.addMenu('&Hệ thống')
        
        # Đổi mật khẩu
        change_password_action = QAction('Đổi mật khẩu', self)
        change_password_action.triggered.connect(self.show_change_password)
        file_menu.addAction(change_password_action)
        
        file_menu.addSeparator()
        
        # Đăng xuất
        logout_action = QAction('Đăng xuất', self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        # Thoát
        exit_action = QAction('Thoát', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Các menu khác tùy theo loại người dùng
        if self.user_type == 'GV':
            # Menu Quản lý
            manage_menu = menubar.addMenu('&Quản lý')
            
            # Action Quản lý Điểm
            manage_scores_action = QAction('Quản lý điểm', self)
            manage_scores_action.triggered.connect(lambda: self.show_page('manage_scores'))
            manage_menu.addAction(manage_scores_action)
            
            # Action Quản lý Lớp
            manage_classes_action = QAction('Quản lý lớp', self) 
            manage_classes_action.triggered.connect(lambda: self.show_page('manage_classes'))
            manage_menu.addAction(manage_classes_action)
            
            # Action Quản lý Sinh viên
            manage_students_action = QAction('Quản lý sinh viên', self)
            manage_students_action.triggered.connect(lambda: self.show_page('manage_students'))
            manage_menu.addAction(manage_students_action)
            
            # Menu Báo cáo
            report_menu = menubar.addMenu('&Báo cáo')
            
            # Action Bảng điểm
            score_reports_action = QAction('Bảng điểm', self)
            score_reports_action.triggered.connect(lambda: self.show_page('score_reports'))
            report_menu.addAction(score_reports_action)
            
            # Action Thống kê điểm
            stats_reports_action = QAction('Thống kê điểm', self)
            stats_reports_action.triggered.connect(lambda: self.show_page('stats_reports'))
            report_menu.addAction(stats_reports_action)
            
            # Menu Cấu hình (nếu có quyền admin)
            if self.user_info and self.user_info.get('Role', '') == 'admin':
                config_menu = menubar.addMenu('&Cấu hình')
                
                # Action Cấu hình hệ thống
                system_config_action = QAction('Cấu hình hệ thống', self)
                system_config_action.triggered.connect(lambda: self.show_page('system_config'))
                config_menu.addAction(system_config_action)
                
                # Action Quản lý người dùng
                user_config_action = QAction('Quản lý người dùng', self)
                user_config_action.triggered.connect(lambda: self.show_page('user_config'))
                config_menu.addAction(user_config_action)
        
        elif self.user_type == 'SV':
            # Menu Xem điểm
            view_menu = menubar.addMenu('&Xem điểm')
            
            # Action Xem điểm học kỳ
            semester_scores_action = QAction('Điểm học kỳ', self)
            semester_scores_action.triggered.connect(lambda: self.show_page('semester_scores'))
            view_menu.addAction(semester_scores_action)
            
            # Action Bảng điểm tổng hợp
            all_scores_action = QAction('Bảng điểm tổng hợp', self)
            all_scores_action.triggered.connect(lambda: self.show_page('all_scores'))
            view_menu.addAction(all_scores_action)
            
            # Menu Đăng ký học phần
            register_menu = menubar.addMenu('&Đăng ký học phần')
            
            # Action Đăng ký môn học
            register_courses_action = QAction('Đăng ký môn học', self)
            register_courses_action.triggered.connect(lambda: self.show_page('register_courses'))
            register_menu.addAction(register_courses_action)
            
            # Action Lịch sử đăng ký
            register_history_action = QAction('Lịch sử đăng ký', self)
            register_history_action.triggered.connect(lambda: self.show_page('register_history'))
            register_menu.addAction(register_history_action)

    def setup_ui(self):
        """Thiết lập giao diện chính của ứng dụng"""
        # Tạo widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        
        # Frame header
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #f8f9fa;")
        header_layout = QHBoxLayout(header_frame)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('Frontend/assets/Image/PTIT_IMAGE.png')
        logo_pixmap = logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        header_layout.addWidget(logo_label)
        
        # Tiêu đề
        title_label = QLabel("HỆ THỐNG QUẢN LÝ ĐIỂM SINH VIÊN")
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #0056b3;")
        header_layout.addWidget(title_label, 1)  # Stretch factor = 1
        
        # Thêm header vào layout chính
        main_layout.addWidget(header_frame)
        
        # Tạo stacked widget để chứa các trang
        self.stacked_widget = QStackedWidget()
        
        # Tạo các trang và thêm vào stacked widget
        self.create_pages()
        
        # Thêm stacked widget vào layout chính
        main_layout.addWidget(self.stacked_widget)

    def create_pages(self):
        """Tạo các trang khác nhau cho ứng dụng"""
        # Trang chào mừng
        welcome_page = self.create_welcome_page()
        self.stacked_widget.addWidget(welcome_page)
        
        # Các trang cho Giảng viên
        if self.user_type == 'GV':
            # Trang Quản lý điểm
            manage_scores_page = self.create_manage_scores_page()
            self.stacked_widget.addWidget(manage_scores_page)
            
            # Trang Quản lý lớp
            manage_classes_page = self.create_manage_classes_page()
            self.stacked_widget.addWidget(manage_classes_page)
            
            # Trang Quản lý sinh viên
            manage_students_page = self.create_manage_students_page()
            self.stacked_widget.addWidget(manage_students_page)
            
            # Trang Báo cáo điểm
            score_reports_page = self.create_score_reports_page()
            self.stacked_widget.addWidget(score_reports_page)
            
            # Trang Thống kê điểm
            stats_reports_page = self.create_stats_reports_page()
            self.stacked_widget.addWidget(stats_reports_page)
            
            # Trang Cấu hình hệ thống (nếu là admin)
            if self.user_info and self.user_info.get('Role', '') == 'admin':
                system_config_page = self.create_system_config_page()
                self.stacked_widget.addWidget(system_config_page)
                
                user_config_page = self.create_user_config_page()
                self.stacked_widget.addWidget(user_config_page)
        
        # Các trang cho Sinh viên
        elif self.user_type == 'SV':
            # Trang Xem điểm học kỳ
            semester_scores_page = self.create_semester_scores_page()
            self.stacked_widget.addWidget(semester_scores_page)
            
            # Trang Bảng điểm tổng hợp
            all_scores_page = self.create_all_scores_page()
            self.stacked_widget.addWidget(all_scores_page)
            
            # Trang Đăng ký môn học
            register_courses_page = self.create_register_courses_page()
            self.stacked_widget.addWidget(register_courses_page)
            
            # Trang Lịch sử đăng ký
            register_history_page = self.create_register_history_page()
            self.stacked_widget.addWidget(register_history_page)
        
        # Trang đổi mật khẩu (chung)
        change_password_page = self.create_change_password_page()
        self.stacked_widget.addWidget(change_password_page)
    
    def create_welcome_page(self):
        """Tạo trang chào mừng"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Tiêu đề chào mừng
        welcome_label = QLabel("Chào mừng bạn đến với Hệ thống Quản lý Điểm Sinh viên")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 28pt; font-weight: bold; margin-top: 100px; color: #0056b3;")
        layout.addWidget(welcome_label)
        
        # Subtitle
        if self.user_type == 'GV':
            subtitle = "Đăng nhập với tư cách Giảng viên"
        elif self.user_type == 'SV':
            subtitle = "Đăng nhập với tư cách Sinh viên"
        else:
            subtitle = ""
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 18pt; margin-top: 20px; color: #6c757d;")
        layout.addWidget(subtitle_label)
        
        # Hướng dẫn
        instruction_label = QLabel("Vui lòng sử dụng menu phía trên để điều hướng đến các chức năng của hệ thống.")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("font-size: 14pt; margin-top: 50px; color: #495057;")
        layout.addWidget(instruction_label)
        
        # Thêm khoảng trống
        layout.addStretch(1)
        
        return page
    
    # Các phương thức tạo trang khác
    def create_manage_scores_page(self):
        """Tạo trang Quản lý điểm"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title_label = QLabel("QUẢN LÝ ĐIỂM")
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #0056b3;")
        layout.addWidget(title_label)
        
        # Thêm các thành phần giao diện khác cho trang quản lý điểm
        # ...
        
        return page
    
    def create_manage_classes_page(self):
        """Tạo trang Quản lý lớp"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title_label = QLabel("QUẢN LÝ LỚP")
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #0056b3;")
        layout.addWidget(title_label)
        
        # Thêm các thành phần giao diện khác cho trang quản lý lớp
        # ...
        
        return page
    
    # Thêm các phương thức tạo trang khác tương tự...
    
    def create_change_password_page(self):
        """Tạo trang Đổi mật khẩu"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title_label = QLabel("ĐỔI MẬT KHẨU")
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #0056b3;")
        layout.addWidget(title_label)
        
        # Form đổi mật khẩu
        form_layout = QFormLayout()
        
        # Mật khẩu cũ
        old_password_input = QLineEdit()
        old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Mật khẩu cũ:", old_password_input)
        
        # Mật khẩu mới
        new_password_input = QLineEdit()
        new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Mật khẩu mới:", new_password_input)
        
        # Xác nhận mật khẩu mới
        confirm_password_input = QLineEdit()
        confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Xác nhận mật khẩu mới:", confirm_password_input)
        
        layout.addLayout(form_layout)
        
        # Button đổi mật khẩu
        button_layout = QHBoxLayout()
        change_button = QPushButton("Đổi mật khẩu")
        change_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
        """)
        button_layout.addStretch(1)
        button_layout.addWidget(change_button)
        button_layout.addStretch(1)
        
        layout.addLayout(button_layout)
        layout.addStretch(1)
        
        return page
    
    # Phương thức để chuyển đổi giữa các trang
    def show_page(self, page_name):
        """Hiển thị trang theo tên"""
        # Ánh xạ tên trang đến index trong stacked widget
        page_mapping = {
            'welcome': 0,
            'manage_scores': 1,
            'manage_classes': 2,
            'manage_students': 3,
            'score_reports': 4,
            'stats_reports': 5,
            # Các trang khác sẽ có index tương ứng
        }
        
        # Chuyển đến trang được chọn
        if page_name in page_mapping:
            self.stacked_widget.setCurrentIndex(page_mapping[page_name])
        else:
            print(f"Trang '{page_name}' không tồn tại")
    
    # Các phương thức xử lý sự kiện menu
    def show_change_password(self):
        """Hiển thị trang đổi mật khẩu"""
        # Index của trang đổi mật khẩu sẽ phụ thuộc vào số lượng trang đã thêm
        change_password_index = self.stacked_widget.count() - 1  # Giả sử đây là trang cuối cùng
        self.stacked_widget.setCurrentIndex(change_password_index)
    
    def logout(self):
        """Phát tín hiệu đăng xuất"""
        self.logout_signal.emit()

    # Tạo các phương thức khác cho các trang còn lại...
    def create_manage_students_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("QUẢN LÝ SINH VIÊN"))
        return page
        
    def create_score_reports_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("BÁO CÁO ĐIỂM"))
        return page
        
    def create_stats_reports_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("THỐNG KÊ ĐIỂM"))
        return page
        
    def create_system_config_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("CẤU HÌNH HỆ THỐNG"))
        return page
        
    def create_user_config_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("QUẢN LÝ NGƯỜI DÙNG"))
        return page
        
    def create_semester_scores_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("ĐIỂM HỌC KỲ"))
        return page
        
    def create_all_scores_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("BẢNG ĐIỂM TỔNG HỢP"))
        return page
        
    def create_register_courses_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("ĐĂNG KÝ MÔN HỌC"))
        return page
        
    def create_register_history_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("LỊCH SỬ ĐĂNG KÝ"))
        return page

# Mã để chạy và kiểm thử giao diện độc lập
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Tạo dữ liệu mẫu cho một giảng viên
    mock_teacher_info = {
        'MaGV': 'GV001',
        'HoTen': 'Nguyễn Văn A',
        'Role': 'admin'
    }
    
    # Tạo dữ liệu mẫu cho một sinh viên
    mock_student_info = {
        'MaSV': 'SV001',
        'Ten': 'Trần Thị B',
    }
    
    # Hiển thị giao diện dành cho giảng viên
    display = Display('GV', None, mock_teacher_info)
    # Hoặc hiển thị giao diện dành cho sinh viên
    # display = Display('SV', None, mock_student_info)
    
    display.show()
    sys.exit(app.exec())