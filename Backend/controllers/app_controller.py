from PyQt6.QtWidgets import *
from Frontend.view.Login import Login
from Frontend.view.Display import Display

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_window = None
        self.connection = None
        self.user_info = None

        self.show_login()

    def show_login(self):
        if self.current_window:
            self.disconnect_signals()
            self.current_window.close()
            self.current_window.deleteLater()
        
        self.current_window = Login()
        self.current_window.login_success_signal.connect(self.handle_login_success)
        self.current_window.show()

    def handle_login_success(self, user_type, connection, user_info = None):
        self.connection = connection
        self.user_info = user_info

        if user_type == 'GV':
            self.show_teacher_view()
        elif user_type == 'SV':
            self.show_student_view()

    def show_teacher_view(self):
        if self.current_window:
            self.disconnect_signals()
            self.current_window.close()
            self.current_window.deleteLater()
        self.current_window = Display('GV', self.connection, self.user_info)
        if hasattr(self.current_window, 'logout_signal'):
            self.current_window.logout_signal.connect(self.show_login)
        self.current_window.show()

    def show_student_view(self):
        if self.current_window:
            self.disconnect_signals()
            self.current_window.close()
            self.current_window.deleteLater()
        self.current_window = Display('SV', self.connection, self.user_info)
        if hasattr(self.current_window, 'logout_signal'):
            self.current_window.logout_signal.connect(self.show_login)
        self.current_window.show()
        
    def disconnect_signals(self):
        """Ngắt kết nối tất cả tín hiệu từ cửa sổ hiện tại"""
        try:
            if isinstance(self.current_window, Login):
                self.current_window.login_success_signal.disconnect()
            elif isinstance(self.current_window, Display) and hasattr(self.current_window, 'logout_signal'):
                self.current_window.logout_signal.disconnect()
        except:
            pass

    # def show_class_management(self):
    #         # Tạo view
    #         self.class_page = ClassManagementPage(connection=self.db_connection, 
    #                                             user_info=self.user_info)
            
    #         # Tạo controller và liên kết với view
    #         self.class_controller = ClassController(self.class_page, self.db_connection)
            
    #         # Liên kết view với controller
    #         self.class_page.controller = self.class_controller
            
    #         # Khởi tạo controller với thông tin người dùng
    #         self.class_controller.initialize(self.user_info)
            
    #         # Hiển thị view
    #         self.class_page.show()

    def show(self):
        super().show()