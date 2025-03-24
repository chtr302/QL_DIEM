from PyQt6.QtWidgets import QMessageBox
from Backend.model.ClassPage.StudentModel import StudentModel

class StudentController:
    def __init__(self, view=None, connection=None, class_controller=None):
        self.view = view
        self.connection = connection
        self.class_controller = class_controller

        self.student_model = StudentModel(connection)

        self.is_adding = False
        self.is_editing = False
        self.current_student_id = None
        self.original_data = None

    def add_student(self):
        """Chuẩn bị thêm sinh viên mới"""
        if not hasattr(self.view, 'selected_class_id') or not self.view.selected_class_id:
            self._show_warning("Vui lòng chọn lớp trước khi thêm sinh viên")
            return False
        self.is_adding = True
        self.is_editing = False
        self.current_student_id = None
        self.original_data = None

        if hasattr(self.view, 'student_manager'):
            self.view.student_manager.prepare_for_add()
        
        return True

    def edit_student(self, student_id=None):
        """Chuẩn bị chỉnh sửa sinh viên"""
        if not student_id and hasattr(self.view, 'student_manager'):
            student_id = self.view.student_manager.get_selected_student_id()
        if not student_id:
            self._show_warning("Vui lòng chọn sinh viên trước khi sửa")
            return False
        try:
            self.original_data = self.view.student_manager.get_form_data()
            self.is_editing = True
            self.is_adding = False
            self.current_student_id = student_id

            if hasattr(self.view, 'student_manager'):
                self.view.student_manager.prepare_for_edit()
            return True
        except Exception as e:
            self._show_error(f"Lỗi khi chuẩn bị sửa sinh viên: {str(e)}")
            return False

    def save_student(self, student_data):
        """Lưu thông tin sinh viên vào database"""
        action = "Thêm mới" if self.is_adding else "Cập nhật"
        student_id = student_data.get('MASV')
        confirm_message = f"Bạn có chắc chắn muốn {action} sinh viên {student_id} không?"
        
        if not self._confirm_action("Xác nhận lưu", confirm_message):
            return False
        try:
            if self.is_adding:
                success, message = self.student_model.add_student(student_data)
            else:
                success, message = self.student_model.edit_student(student_data)
            if success:
                self._show_success(message)
                self.is_adding = False
                self.is_editing = False
                self.current_student_id = student_data.get('MASV')

                if self.class_controller and hasattr(self.view, 'selected_class_id'):
                    self.class_controller.load_student(self.view.selected_class_id)
                    if hasattr(self.view, 'dept_combo') and self.view.dept_combo.currentData():
                        dept_id = self.view.dept_combo.currentData()
                        self.class_controller.load_classes(dept_id)
                    elif hasattr(self.class_controller, 'user_dept_code'):
                        dept_id = self.class_controller.user_dept_code
                        self.class_controller.load_classes(dept_id)
                if hasattr(self.view, 'student_manager'):
                    self.view.student_manager.after_save()
                return True
            else:
                self._show_warning(message)
                return False
        except Exception as e:
            self._show_error(f"Lỗi khi lưu thông tin sinh viên: {str(e)}")
            return False

    def cancel_student(self):
        """Hủy thao tác thêm/sửa sinh viên"""
        if self.is_adding or self.is_editing:
            confirm_message = "Bạn có chắc chắn muốn hủy thao tác này không? Các thay đổi sẽ không được lưu."
            if not self._confirm_action("Xác nhận hủy", confirm_message):
                return False
        self.is_adding = False
        self.is_editing = False

        if hasattr(self.view, 'student_manager'):
            self.view.student_manager.after_cancel()
        
        return True

    def delete_student(self, student_id=None):
        """Xóa sinh viên khỏi database"""
        if not student_id and hasattr(self.view, 'student_manager'):
            student_id = self.view.student_manager.get_selected_student_id()
        
        if not student_id:
            self._show_warning("Vui lòng chọn sinh viên trước khi xóa")
            return False
        
        confirm_message = f"Bạn có chắc chắn muốn xóa sinh viên {student_id}? Hành động này không thể hoàn tác!"
        if not self._confirm_action("Xác nhận xóa", confirm_message):
            return False
        
        try:
            success, message = self.student_model.delete_student(student_id)
            
            if success:
                self._show_success(message)
                if self.class_controller and hasattr(self.view, 'selected_class_id'):
                    self.class_controller.load_student(self.view.selected_class_id)
                if hasattr(self.view, 'student_manager'):
                    self.view.student_manager.clear_form()
                    self.view.student_manager.set_form_state("none")
                return True
            else:
                self._show_warning(message)
                return False
        except Exception as e:
            self._show_error(f"Lỗi khi xóa sinh viên: {str(e)}")
            return False

    def restore_student(self, student_id=None):
        """Phục hồi thông tin sinh viên từ database"""
        if not student_id:
            student_id = self.current_student_id
            
        if not student_id and hasattr(self.view, 'student_manager'):
            student_id = self.view.student_manager.get_selected_student_id()
        
        if not student_id:
            self._show_warning("Không có sinh viên nào để phục hồi")
            return False
        
        try:
            # Lấy thông tin sinh viên từ database
            student_data = self.student_model.get_student_by_id(student_id)
            
            if not student_data:
                self._show_warning(f"Không tìm thấy thông tin của sinh viên {student_id}")
                return False
            
            # Cập nhật form
            if hasattr(self.view, 'student_manager'):
                self.view.student_manager.populate_form(student_data)
            
            return True
            
        except Exception as e:
            self._show_error(f"Lỗi khi phục hồi thông tin sinh viên: {str(e)}")
            return False

    def filter_students(self, search_text):
        """Tìm kiếm sinh viên theo từ khóa"""
        if not hasattr(self.view, 'selected_class_id') or not self.view.selected_class_id:
            return False
        try:
            if not search_text:
                if self.class_controller:
                    self.class_controller.load_student(self.view.selected_class_id)
            else:
                filtered_students = self.student_model.search_students(
                    self.view.selected_class_id, 
                    search_text
                )
                if hasattr(self.view, 'update_student_table'):
                    self.view.update_student_table(filtered_students)
            return True    
        except Exception as e:
            self._show_error(f"Lỗi khi tìm kiếm sinh viên: {str(e)}")
            return False

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
    
    def _confirm_action(self, title, message):
        """Hiển thị hộp thoại xác nhận"""
        if not self.view:
            return True
            
        reply = QMessageBox.question(
            self.view,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes