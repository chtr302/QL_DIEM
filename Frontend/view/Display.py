from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Frontend.view.ClassPage.ClassManagement import ClassManagementPage
from Backend.controllers.ClassPage.class_controller import ClassController
from Backend.controllers.ClassPage.student_controller import StudentController


IMG_PATH = 'Frontend/assets/image/ToolbarDisplay'

class Display(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self, user_type, connection, user_info):
        super().__init__()

        self.user_type = user_type
        self.connection = connection
        self.user_info = user_info
        
        self.setWindowTitle('Quản lý điểm sinh viên')
        self.setFixedSize(1800, 1050)

        self.font = QFont()
        self.font.setPointSize(12)

        self.toolbar_style = """
            QToolBar {
                background-color: #ffffff;  /* Màu nền trắng cho toolbar */
                border: 1px solid #dcdcdc;
            }
            QToolButton {
                background-color: #ffffff;  /* Màu nền mặc định cho nút */
                padding: 5px;
            }
            QToolButton:checked {
                background-color: #cce5ff;  /* Màu xanh nhạt khi được chọn */
            }
            QToolButton:hover:!checked {
                background-color: #f0f0f0;  /* Hiệu ứng hover khi không chọn */
            }
        """
        
        self.setup_ui()
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        if user_type == 'GV' and user_info is not None:
            try:
                
                if user_info['Role'] == 'KHOA':
                    self.setWindowTitle(f'Hệ thống Quản lý điểm Sinh viên - Giảng viên - {user_info['TenKhoa']}')
                    self.status_bar.showMessage(f'Mã giảng viên: {user_info["MaGV"]} | Họ và Tên: {user_info["HoTen"]} | Khoa: {user_info['TenKhoa']} | Quyền: {user_info["Role"]}')
                elif user_info['Role'] == 'PGV':
                    self.setWindowTitle('Hệ thống Quản lý điểm Sinh viên - Phòng giáo vụ')
                    self.status_bar.showMessage(f'Tài khoản: {user_info["MaGV"]} | Quyền: {user_info["Role"]}')
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

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")
        # Tạo QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        if self.user_type == 'GV':
            self.setup_teacher_toolbars()
            self.show_page("manage_scores")
        elif self.user_type == 'SV':
            self.setup_student_toolbars()
            self.show_page("view_scores")

        self.create_pages()

    def setup_teacher_toolbars(self):
        self.action_group = QActionGroup(self) # Nhóm Action
        self.action_group.setExclusive(True)  # Chỉ được chọn 1 cái

        # =================== Quản lý ===================
        self.manage_toolbar = QToolBar("Quản lý", self) # Tạo toolBar QL
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.manage_toolbar)
        self.manage_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.manage_toolbar.setIconSize(QSize(48, 48))
        self.manage_toolbar.setFont(self.font)
        self.manage_toolbar.setStyleSheet(self.toolbar_style)
        # Cấu hình các nút trong QL
        self.manage_classes_action = self.manage_toolbar.addAction(QIcon(f"{IMG_PATH}/class.png"), "Lớp Học", lambda: self.show_page("manage_classes"))
        if self.user_info.get('Role','') == 'PGV':
            self.manage_subjects_action = self.manage_toolbar.addAction(QIcon(f"{IMG_PATH}/subject.png"), "Môn Học", lambda: self.show_page("manage_subjects"))
            self.manage_subjects_action.setCheckable(True)
            self.action_group.addAction(self.manage_subjects_action)


        self.manage_credit_classes_action = self.manage_toolbar.addAction(QIcon(f"{IMG_PATH}/cc.png"), "Lớp Tín Chỉ", lambda: self.show_page("credit_classes"))
        self.enter_scores_action = self.manage_toolbar.addAction(QIcon(f"{IMG_PATH}/student.png"), "Nhập Điểm", lambda: self.show_page("enter_scores"))
        # Thêm vào Group và chỉ được 1 Action trong 1 thời điểm
        self.manage_classes_action.setCheckable(True)
        self.manage_credit_classes_action.setCheckable(True)
        self.enter_scores_action.setCheckable(True)
        
        self.action_group.addAction(self.manage_credit_classes_action)
        self.action_group.addAction(self.enter_scores_action)
        self.action_group.addAction(self.manage_classes_action)

        # =================== Báo cáo ===================
        self.report_toolbar = QToolBar("Báo cáo", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.report_toolbar)
        self.report_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.report_toolbar.setIconSize(QSize(48, 48))
        self.report_toolbar.setFont(self.font)
        self.report_toolbar.setStyleSheet(self.toolbar_style)
        
        self.stats_reports_action = self.report_toolbar.addAction(QIcon(f"{IMG_PATH}/report.png"), "Thống kê điểm", lambda: self.show_page("stats_reports"))

        self.stats_reports_action.setCheckable(True)
        self.action_group.addAction(self.stats_reports_action)

        # =================== Cấu hình ===================
        self.config_toolbar = QToolBar("Cấu hình", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.config_toolbar)
        self.config_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.config_toolbar.setIconSize(QSize(48, 48))
        self.config_toolbar.setFont(self.font)
        self.config_toolbar.setStyleSheet(self.toolbar_style)
        
        self.create_user_action = self.config_toolbar.addAction(QIcon(f"{IMG_PATH}/us.png"), "Tạo tài khoản", lambda: self.show_page("create_user"))
        self.change_password_action = self.config_toolbar.addAction(QIcon(f"{IMG_PATH}/cp.png"), "Đổi mật khẩu", lambda: self.show_page("change_password"))
        self.logout_action = self.config_toolbar.addAction(QIcon(f"{IMG_PATH}/logout.png"), "Đăng xuất", self.logout)
        self.exit_action = self.config_toolbar.addAction(QIcon(f"{IMG_PATH}/exit.png"), "Thoát", self.close)

        self.create_user_action.setCheckable(True)
        self.change_password_action.setCheckable(True)

        self.action_group.addAction(self.create_user_action)
        self.action_group.addAction(self.change_password_action)

    def setup_student_toolbars(self):
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        # =================== Xem Điểm ===================
        self.scores_toolbar = QToolBar("Xem điểm", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.scores_toolbar)
        self.scores_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.scores_toolbar.setIconSize(QSize(48, 48))
        self.scores_toolbar.setFont(self.font)
        self.scores_toolbar.setStyleSheet(self.toolbar_style)
        
        self.view_scores_action = self.scores_toolbar.addAction(QIcon(f"{IMG_PATH}/vp.png"), "Xem điểm", lambda: self.show_page("view_scores"))
        self.view_scores_action.setCheckable(True)
        self.action_group.addAction(self.view_scores_action)

        # =================== Đăng ký ===================
        self.register_toolbar = QToolBar("Đăng ký học phần", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.register_toolbar)
        self.register_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.register_toolbar.setIconSize(QSize(48, 48))
        self.register_toolbar.setFont(self.font)
        self.register_toolbar.setStyleSheet(self.toolbar_style)
        # Cấu hình các nút
        self.register_courses_action = self.register_toolbar.addAction(QIcon(f"{IMG_PATH}/rc.png"), "Đăng ký môn học", lambda: self.show_page("register_courses"))

        self.register_courses_action.setCheckable(True)
        self.action_group.addAction(self.register_courses_action)

        # =================== Cấu hình ===================
        self.config_toolbar = QToolBar("Cấu hình", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.config_toolbar)
        self.config_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.config_toolbar.setIconSize(QSize(48, 48))
        self.config_toolbar.setFont(self.font)
        self.config_toolbar.setStyleSheet(self.toolbar_style)
        
        self.change_password_action = self.config_toolbar.addAction(QIcon(f"{IMG_PATH}/cp.png"), "Đổi mật khẩu", lambda: self.show_page("change_password"))
        self.logout_action = self.config_toolbar.addAction(QIcon(f"{IMG_PATH}/logout.png"), "Đăng xuất", self.logout)
        self.exit_action = self.config_toolbar.addAction(QIcon(f"{IMG_PATH}/exit.png"), "Thoát", self.close)
        
        self.change_password_action.setCheckable(True)
        self.action_group.addAction(self.change_password_action)

    def create_pages(self):
        if self.user_type == 'GV':
            self.create_teacher_pages()
        elif self.user_type == 'SV':
            self.create_student_pages()
        
        # Trang Đổi mật khẩu (chung cho cả giáo viên và sinh viên)
        change_password_page = QWidget()
        change_password_page.setLayout(QVBoxLayout())
        change_password_page.layout().addWidget(QLabel("Trang Đổi mật khẩu"))
        self.stacked_widget.addWidget(change_password_page)

    def create_teacher_pages(self):
        # Trang Quản lý 
        self.class_controller = ClassController(connection=self.connection)
        self.student_controller = StudentController(connection=self.connection)
        self.manage_class_page = ClassManagementPage(
            parent=self,
            connection=self.connection,
            user_info=self.user_info,
            controller= self.class_controller,
            student_controller=self.student_controller
        )
        self.class_controller.set_view(self.manage_class_page)
        self.class_controller.initialize_by_role()
        self.student_controller.view = self.manage_class_page
        self.stacked_widget.addWidget(self.manage_class_page)

        # Trang Quản lý sinh viên
        manage_students_page = QWidget()
        manage_students_page.setLayout(QVBoxLayout())
        manage_students_page.layout().addWidget(QLabel("Trang Quản lý sinh viên"))
        self.stacked_widget.addWidget(manage_students_page)

        # Trang Bảng điểm
        score_reports_page = QWidget()
        score_reports_page.setLayout(QVBoxLayout())
        score_reports_page.layout().addWidget(QLabel("Trang Bảng điểm"))
        self.stacked_widget.addWidget(score_reports_page)

        # Trang Thống kê điểm
        stats_reports_page = QWidget()
        stats_reports_page.setLayout(QVBoxLayout())
        stats_reports_page.layout().addWidget(QLabel("Trang Thống kê điểm"))
        self.stacked_widget.addWidget(stats_reports_page)

    def create_student_pages(self):
        # Trang Xem điểm
        view_scores_page = QWidget()
        view_scores_page.setLayout(QVBoxLayout())
        view_scores_page.layout().addWidget(QLabel("Trang Xem điểm"))
        self.stacked_widget.addWidget(view_scores_page)

        # Trang Đăng ký môn học
        register_courses_page = QWidget()
        register_courses_page.setLayout(QVBoxLayout())
        register_courses_page.layout().addWidget(QLabel("Trang Đăng ký môn học"))
        self.stacked_widget.addWidget(register_courses_page)

    def show_page(self, page_name):
        if self.user_type == 'GV':
            if self.user_info['Role'] == 'PGV':
                page_mapping = {
                    "manage_subjects": 0,
                    "manage_classes": 1,
                    "credit_classes": 2,
                    "enter_scoes": 3,
                    "stats_reports": 4,
                    "create_user": 5,
                    "change_password": 6
                }
                action_mapping = {
                    "manage_subjects": self.manage_subjects_action,
                    "manage_classes": self.manage_classes_action,
                    "credit_classes": self.manage_credit_classes_action,
                    "enter_scoes": self.enter_scores_action,
                    "stats_reports": self.stats_reports_action,
                    "create_user": self.create_user_action,
                    "change_password": self.change_password_action
                }
            else:
                page_mapping = {
                    'credit_classes': 0,
                    'manage_classes': 1,
                    'enter_score': 2,
                    'stats_reports': 3,
                    'create_user': 4,
                    'change_password': 5
                }
                action_mapping = {
                    'credit_classes': self.manage_credit_classes_action,
                    'enter_score': self.enter_scores_action,
                    'stats_reports': self.stats_reports_action,
                    'create_user': self.create_user_action,
                    'change_password': self.change_password_action
                }
        elif self.user_type == 'SV':
            page_mapping = {
                "view_scores": 0,
                "register_courses": 1,
                "change_password": 2
            }
            action_mapping = {
                "view_scores": self.view_scores_action,
                "register_courses": self.register_courses_action,
                "change_password": self.change_password_action
            }
        else:
            return

        if page_name in page_mapping:
            self.stacked_widget.setCurrentIndex(page_mapping[page_name]) # Set Index trong stacked
            if page_name in action_mapping:
                action_mapping[page_name].setChecked(True)

    def logout(self):
        self.logout_signal.emit()
        self.close()
    