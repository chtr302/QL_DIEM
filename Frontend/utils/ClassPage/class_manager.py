from Frontend.utils.crud import CRUDForm
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer

class FormState:
    VIEWING = "viewing"
    ADDING = "adding"
    EDITING = "editing"
    NONE = "none"

class ClassManager(CRUDForm):
    def __init__(self, parent, controller=None):
        super().__init__(controller, 'class')
        self.parent = parent
        self.current_state = FormState.NONE
        self.original_data = None
        self._search_timer = QTimer()
        self._search_timer.timeout.connect(self._do_search)
        self._search_timer.setSingleShot(True)
    
    def add_clicked(self):
        """Xử lý khi người dùng nhấn nút Thêm"""
        self.clear_form()
        self.set_form_state(FormState.ADDING)
        if hasattr(self.parent, 'selected_dept_name') and self.parent.selected_dept_name:
            self.parent.dept_display.setText(self.parent.selected_dept_name)
        self.parent.class_id.setFocus()
        if self.controller:
            self.controller.add_class()
    
    def edit_clicked(self):
        """Xử lý khi người dùng nhấn nút Sửa"""
        self.original_data = self.get_form_data()
        self.set_form_state(FormState.EDITING)
        self.parent.class_name.setFocus()
        if self.controller:
            self.controller.edit_class(self.original_data.get('MALOP'))
    
    def save_clicked(self):
        """Xử lý khi người dùng nhấn nút Lưu"""
        if not self.validate_form():
            return
        class_data = self.get_form_data()
        if self.controller:
            success = self.controller.save_class(class_data)
            if success:
                self.original_data = None
    
    def cancel_clicked(self):
        """Xử lý khi người dùng nhấn nút Hủy"""
        if self.controller:
            self.controller.cancel_class()
        else:
            if self.current_state == FormState.EDITING and self.original_data:
                self.populate_form(self.original_data)
                self.set_form_state(FormState.VIEWING)
            else:
                self.clear_form()
                self.set_form_state(FormState.NONE)
        self.original_data = None
    
    def restore_clicked(self):
        """Xử lý khi người dùng nhấn nút Phục hồi"""
        class_id = self.parent.class_id.text().strip()
        if not class_id:
            return
        if self.controller:
            self.controller.restore_class(class_id)
    
    def item_selected(self, item):
        """Xử lý khi người dùng chọn một mục trong bảng"""
        if self.current_state == FormState.ADDING or self.current_state == FormState.EDITING:
            return
        selected_class = self.get_selected_item(item)
        self.controller.select_class(selected_class['MALOP'])
        self.parent.class_id.setText(selected_class['MALOP'])
        self.parent.class_name.setText(selected_class['TENLOP'])
        self.parent.course_year.setText(selected_class['NIENKHOA'])
        self.set_form_state(FormState.VIEWING)
    
    def set_form_state(self, state):
        """Thiết lập trạng thái form và cập nhật UI"""
        self.current_state = state
        if state == FormState.VIEWING:
            self.set_form_editing_state(False, False)
            self.set_form_buttons_state("view")
            
        elif state == FormState.ADDING:
            self.set_form_editing_state(True, True)
            self.set_form_buttons_state("add")
            
        elif state == FormState.EDITING:
            self.set_form_editing_state(True, False)
            self.set_form_buttons_state("edit")
            
        else:
            self.set_form_editing_state(False, True)
            self.set_form_buttons_state("none")
    
    def set_form_editing_state(self, is_editing, allow_id_edit):
        """Cập nhật trạng thái chỉnh sửa của form"""
        self.parent.class_name.setEnabled(is_editing)
        self.parent.class_name.setReadOnly(not is_editing)
        
        self.parent.course_year.setEnabled(is_editing)
        self.parent.course_year.setReadOnly(not is_editing)
        
        self.parent.class_id.setEnabled(allow_id_edit and is_editing)
        self.parent.class_id.setReadOnly(not (allow_id_edit and is_editing))

        self.parent.class_table.setEnabled(not is_editing)
        self.parent.student_table.setEnabled(not is_editing)
        self.parent.dept_combo.setEnabled(not is_editing)

        self.parent.student_id.setReadOnly(True)
        self.parent.student_lastname.setReadOnly(True)
        self.parent.student_firstname.setReadOnly(True)
        self.parent.student_dob.setReadOnly(True)
        self.parent.radio_male.setEnabled(False)
        self.parent.radio_female.setEnabled(False)
        self.parent.student_address.setReadOnly(True)
        self.parent.student_is_paused.setEnabled(False)
    
    def set_form_buttons_state(self, mode):
        """Cập nhật trạng thái các nút"""
        if mode == "view":
            # =============== CLASS ===============
            self.parent.add_class_btn.setEnabled(True)
            self.parent.edit_class_btn.setEnabled(True)
            self.parent.save_class_btn.setEnabled(False)
            self.parent.cancel_class_btn.setEnabled(False)
            self.parent.restore_class_btn.setEnabled(True)
            # =============== STUDENT ===============
            self.parent.add_student_btn.setEnabled(True)
            self.parent.edit_student_btn.setEnabled(False)
            self.parent.save_student_btn.setEnabled(False)
            self.parent.cancel_student_btn.setEnabled(False)
            self.parent.restore_student_btn.setEnabled(False)
            
        elif mode == "add":
            # =============== CLASS ===============
            self.parent.add_class_btn.setEnabled(False)
            self.parent.edit_class_btn.setEnabled(False)
            self.parent.save_class_btn.setEnabled(True)
            self.parent.cancel_class_btn.setEnabled(True)
            self.parent.restore_class_btn.setEnabled(False)
            # =============== STUDENT ===============
            self.parent.add_student_btn.setEnabled(False)
            self.parent.edit_student_btn.setEnabled(False)
            self.parent.save_student_btn.setEnabled(False)
            self.parent.cancel_student_btn.setEnabled(False)
            self.parent.restore_student_btn.setEnabled(False)
            
        elif mode == "edit":
            # =============== CLASS ===============
            self.parent.add_class_btn.setEnabled(False)
            self.parent.edit_class_btn.setEnabled(False)
            self.parent.save_class_btn.setEnabled(True)
            self.parent.cancel_class_btn.setEnabled(True)
            self.parent.restore_class_btn.setEnabled(False)
            # =============== STUDENT ===============
            self.parent.add_student_btn.setEnabled(False)
            self.parent.edit_student_btn.setEnabled(False)
            self.parent.save_student_btn.setEnabled(False)
            self.parent.cancel_student_btn.setEnabled(False)
            self.parent.restore_student_btn.setEnabled(False)
            
        else:
            # =============== CLASS ===============
            self.parent.add_class_btn.setEnabled(True)
            self.parent.edit_class_btn.setEnabled(False)
            self.parent.save_class_btn.setEnabled(False)
            self.parent.cancel_class_btn.setEnabled(False)
            self.parent.restore_class_btn.setEnabled(False)
            # =============== STUDENT ===============
            self.parent.add_student_btn.setEnabled(True)
            self.parent.edit_student_btn.setEnabled(False)
            self.parent.save_student_btn.setEnabled(False)
            self.parent.cancel_student_btn.setEnabled(False)
            self.parent.restore_student_btn.setEnabled(False)
    
    def search_changed(self, text):
        """Xử lý khi người dùng nhập text tìm kiếm"""
        self._search_timer.stop()
        self._search_timer.start(5000)
    
    def search_clicked(self):
        """Xử lý khi người dùng nhấn nút Tìm kiếm"""
        self._do_search()
    
    def _do_search(self):
        self._search_timer.stop()
        search_text = self.get_search_text()
        if self.controller:
            self.controller.filter_classes(search_text)
    
    def populate_form(self, class_data):
        """Điền dữ liệu lớp học vào form"""
        if not class_data:
            return
        self.parent.class_id.setText(class_data.get('MALOP', ''))
        self.parent.class_name.setText(class_data.get('TENLOP', ''))
        self.parent.course_year.setText(class_data.get('NIENKHOA', ''))
        khoa_name = class_data.get('TENKHOA', self.parent.selected_dept_name if hasattr(self.parent, 'selected_dept_name') else '')
        if khoa_name:
            self.parent.dept_display.setText(khoa_name)
    
    def clear_form(self):
        """Xóa tất cả dữ liệu trên form"""
        self.parent.class_id.clear()
        self.parent.class_name.clear()
        self.parent.course_year.clear()
        self.parent.class_table.clearSelection()
    
    # Các callback được gọi bởi controller
    def prepare_for_add(self):
        """Chuẩn bị giao diện để thêm mới"""
        self.clear_form()
        self.set_form_state(FormState.ADDING)
    
    def prepare_for_edit(self):
        """Chuẩn bị giao diện để chỉnh sửa"""
        self.set_form_state(FormState.EDITING)
    
    def after_save(self):
        """Xử lý sau khi lưu thành công"""
        self.set_form_state(FormState.VIEWING)
    
    def after_cancel(self):
        """Xử lý sau khi hủy thao tác"""
        if self.controller.current_class_id:
            self.set_form_state(FormState.VIEWING)
        else:
            self.clear_form()
            self.set_form_state(FormState.NONE)
    
    def validate_form(self):
        """Kiểm tra dữ liệu nhập vào"""
        if not self.parent.class_id.text().strip():
            QMessageBox.warning(self.parent, "Lỗi", "Mã lớp không được để trống")
            self.parent.class_id.setFocus()
            return False

        if not self.parent.class_name.text().strip():
            QMessageBox.warning(self.parent, "Lỗi", "Tên lớp không được để trống")
            self.parent.class_name.setFocus()
            return False

        if not self.parent.course_year.text().strip():
            QMessageBox.warning(self.parent, "Lỗi", "Niên khóa không được để trống")
            self.parent.course_year.setFocus()
            return False

        if not hasattr(self.parent, 'selected_dept_code') or not self.parent.selected_dept_code:
            QMessageBox.warning(self.parent, "Lỗi", "Vui lòng chọn khoa")
            return False
        
        return True
    
    def get_form_data(self):
        """Lấy dữ liệu từ form"""
        data = {
            'MALOP': self.parent.class_id.text().strip(),
            'TENLOP': self.parent.class_name.text().strip(),
            'NIENKHOA': self.parent.course_year.text().strip(),
        }
        if hasattr(self.parent, 'selected_dept_code') and self.parent.selected_dept_code:
            data['MAKHOA'] = self.parent.selected_dept_code
        return data
    
    def get_search_text(self):
        """Lấy từ khóa tìm kiếm"""
        return self.parent.class_search.text().strip()
    
    def get_selected_item(self, item):
        """Lấy thông tin mục được chọn trong bảng"""
        row = item.row()
        
        # Hàm helper để lấy text an toàn
        def get_cell_text(row, col):
            cell = self.parent.class_table.item(row, col)
            return cell.text() if cell else ""
        
        selected_class_data = {
            'MALOP': get_cell_text(row, 0),
            'TENLOP': get_cell_text(row, 1),
            'NIENKHOA': get_cell_text(row, 2),
            'TENKHOA': get_cell_text(row, 3),
            'SISO': get_cell_text(row, 4)
        }
        return selected_class_data