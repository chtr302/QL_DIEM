from PyQt6.QtWidgets import QMessageBox
from Backend.model.ClassPage.ClassModel import ClassModel
from Backend.model.ClassPage.StudentModel import StudentModel

class ClassController:
    def __init__(self, view=None, connection=None):
        self.view = view
        self.connection = connection

        self.class_model = ClassModel(self.connection)
        self.student_model = StudentModel(connection)

        self.user_dept_code = None
        self.user_dept_name = None

        self.is_adding = False
        self.is_editing = False

        self.current_class_id = None

    def set_view(self, view):
        """Đặt đối tượng view cho controller sau khi đã khởi tạo"""
        self.view = view
        if self.view is not None:
            self.initialize_by_role()
        
    def initialize_by_role(self):
        """Khởi tạo dựa trên vai trò người dùng"""
        if not hasattr(self.view, 'user_info') or not self.view.user_info:
            return
        role = self.view.user_info.get('Role', '')
        if role == 'KHOA':
            self.user_dept_code = self.view.user_info.get('MaKhoa')
            self.user_dept_name = self.view.user_info.get('TenKhoa')
            
            if self.user_dept_code:
                self.view.set_selected_dept(self.user_dept_code, self.user_dept_name)
                self.view.hide_dept_combobox()
                self.load_classes(self.user_dept_code)
        else:
            self.load_departments()

    def load_departments(self):
        """Tải danh sách khoa"""
        dept = self.class_model.get_dept()
        self.view.update_dept_combo(dept)

    def select_dept(self, dept_code, dept_name):
        """Xử lý khi người dùng chọn một khoa"""
        self.user_dept_code = dept_code
        self.user_dept_name = dept_name
        self.view.set_selected_dept(dept_code, dept_name)
        self.load_classes(dept_code)
    
    def load_classes(self, dept_code):
        class_data = self.class_model.get_classes_by_dept_code(dept_code)
        self.view.update_class_table(class_data)

    def select_class(self, class_id):
        self.view.set_selected_class(class_id)
        self.current_class_id = class_id
        self.load_student(class_id)

    def load_student(self, class_id):
        student_data = self.student_model.get_students_by_class_id(class_id)
        self.view.update_student_table(student_data)

    def add_class(self):
        self.is_adding = True
        self.is_editing = False
        self.current_class_id = None
        self.view.class_manager.prepare_for_add()

    def edit_class(self, class_id = None):
        self.is_adding = False
        self.is_editing = True
        self.view.class_manager.prepare_for_edit()

    def save_class(self, class_data):
        if not class_data:
            return False
        if self.user_dept_code and not class_data.get('MAKHOA'):
            class_data['MAKHOA'] = self.user_dept_code
        
        action = 'Thêm mới' if self.is_adding else 'Cập nhật'
        class_id = class_data.get('MALOP')
        confirm_message = f'Bạn có chắc chắn muốn {action} lớp {class_id} không ?'

        if not self._comfirm_action("Xác nhận lưu", confirm_message):
            return False

        if self.is_adding:
            success, message = self.class_model.add_class(class_data)
        else:
            success, message = self.class_model.edit_class(class_data)

        if success:
            self._show_success(message)
            self.is_adding = False
            self.is_editing = False
            self.current_class_id = class_data.get('MALOP')
            self.load_classes(self.user_dept_code)
            self.view.set_selected_class(self.current_class_id)
            self.view.class_manager.after_save()
            return True
        else:
            self._show_warning(message)
            return False
    
    def cancel_class(self):
        if self.is_adding or self.is_editing:
            if not self._comfirm_action('Xác nhận huỷ','Bạn có chắc chắn muốn huỷ thao tác này không? Các thay đổi sẽ không được lưu'):
                return False
        self.is_adding = False
        self.is_editing = False
        self.view.class_manager.after_cancel()
        return True

    def _show_error(self, message):
        """Hiển thị thông báo lỗi"""
        if self.view:
            QMessageBox.critical(self.view, 'Lỗi', message)
        else:
            print(f"Lỗi: {message}")
        
    def _show_success(self, message):
        """Hiển thị thông báo thành công"""
        if self.view:
            QMessageBox.information(self.view, "Thông báo", message)
        else:
            print(f"Thành công: {message}")

    def _show_warning(self, message):
        """Hiển thị cảnh báo"""
        if self.view:
            QMessageBox.warning(self.view, "Cảnh báo", message)
        else:
            print(f"Cảnh báo: {message}")
    
    def _comfirm_action(self, title, message):
        reply = QMessageBox.question(
        self.view,
        title,
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
    
    