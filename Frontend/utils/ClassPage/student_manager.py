from Frontend.utils.crud import CRUDForm
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
from PyQt6.QtCore import QDate

class FormState:
    VIEWING = "viewing"
    ADDING = "adding"
    EDITING = "editing"
    NONE = "none"

class StudentManager(CRUDForm):
    def __init__(self, parent, controller=None):
        super().__init__(controller, "student")
        self.parent = parent

        self.current_state = FormState.NONE
        self.original_data = None

    def add_clicked(self):
        if self.controller.add_student():
            self.clear_form()
            self.set_form_state(FormState.ADDING)
            self.parent.student_id.setFocus()
            self.controller.add_student()

    def edit_clicked(self):
        if self.controller.edit_student():
            self.original_data = self.get_form_data()
            self.parent.student_lastname.setFocus()
            self.set_form_state(FormState.EDITING)
            self.controller.edit_student()
    
    def save_clicked(self):
        if not self.validate_form():
            return
        student_data = self.get_form_data()
        self.controller.save_student(student_data)
    
    def cancel_clicked(self):
        if self.controller:
            self.controller.cancel_student()
        else:
            if self.current_state == FormState.EDITING and self.original_data:
                self.populate_form(self.original_data)
                self.set_form_state(FormState.VIEWING)
            else:
                self.clear_form()
                self.set_form_state(FormState.NONE)

        self.original_data = None

    def item_selected(self, item):
        """Xử lý khi người dùng chọn một sinh viên trong bảng"""
        if self.current_state == FormState.ADDING or self.current_state == FormState.EDITING:
            return
            
        selected_student = self.get_selected_item(item)
        self.populate_form(selected_student)

        self.parent.student_id.setEnabled(False)
        self.parent.edit_student_btn.setEnabled(True)

        self.set_form_state(FormState.VIEWING)

    def validate_form(self):
        if not self.parent.student_id.text().strip():
            QMessageBox.warning(self.parent, "Lỗi", "Mã sinh viên không được để trống")
            self.parent.student_id.setFocus()
            return False
        
        if not self.parent.student_lastname.text().strip():
            QMessageBox.warning(self.parent, "Lỗi", "Họ sinh viên không được để trống")
            self.parent.student_lastname.setFocus()
            return False
        
        if not self.parent.student_firstname.text().strip():
            QMessageBox.warning(self.parent, "Lỗi", "Tên sinh viên không được để trống")
            self.parent.student_firstname.setFocus()
            return False
        
        # Kiểm tra lớp đã chọn
        if not hasattr(self.parent, 'selected_class_id') or not self.parent.selected_class_id:
            QMessageBox.warning(self.parent, "Lỗi", "Vui lòng chọn lớp trước khi thao tác với sinh viên")
            return False
        if not self.parent.student_class_id.text().strip():
            QMessageBox.warning(self.parent, "Lỗi", "Mã lớp không được để trống")
            self.parent.student_class_id.setFocus()
            return False
        return True
    
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
        """Cập nhật trạng thái chỉnh sửa của form sinh viên"""
        self.parent.student_id.setEnabled(allow_id_edit and is_editing)
        self.parent.student_id.setReadOnly(not (allow_id_edit and is_editing))

        self.parent.student_lastname.setEnabled(is_editing)
        self.parent.student_lastname.setReadOnly(not is_editing)

        self.parent.student_firstname.setEnabled(is_editing)
        self.parent.student_firstname.setReadOnly(not is_editing)

        self.parent.student_dob.setEnabled(is_editing)
        self.parent.student_dob.setReadOnly(not is_editing)

        self.parent.radio_male.setEnabled(is_editing)
        self.parent.radio_female.setEnabled(is_editing)

        self.parent.student_address.setEnabled(is_editing)
        self.parent.student_address.setReadOnly(not is_editing)

        self.parent.student_is_paused.setEnabled(is_editing)

        self.parent.student_class_id.setEnabled(is_editing)
        self.parent.student_class_id.setReadOnly(not is_editing)
        
        self.parent.student_table.setEnabled(not is_editing)
        self.parent.class_table.setEnabled(not is_editing)
        # Vô hiệu hoá form class
        self.parent.class_name.setReadOnly(True)
        self.parent.course_year.setReadOnly(True)
        self.parent.class_id.setReadOnly(True)
        

        self.parent.dept_combo.setEnabled(not is_editing)

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
            self.parent.edit_student_btn.setEnabled(True)
            self.parent.save_student_btn.setEnabled(False)
            self.parent.cancel_student_btn.setEnabled(False)
            self.parent.restore_student_btn.setEnabled(True)
            
        elif mode == "add":
            # =============== CLASS ===============
            self.parent.add_class_btn.setEnabled(False)
            self.parent.edit_class_btn.setEnabled(False)
            self.parent.save_class_btn.setEnabled(False)
            self.parent.cancel_class_btn.setEnabled(False)
            self.parent.restore_class_btn.setEnabled(False)
            # =============== STUDENT ===============
            self.parent.add_student_btn.setEnabled(False)
            self.parent.edit_student_btn.setEnabled(False)
            self.parent.save_student_btn.setEnabled(True)
            self.parent.cancel_student_btn.setEnabled(True)
            self.parent.restore_student_btn.setEnabled(False)
            
        elif mode == "edit":
            # =============== CLASS ===============
            self.parent.add_class_btn.setEnabled(False)
            self.parent.edit_class_btn.setEnabled(False)
            self.parent.save_class_btn.setEnabled(False)
            self.parent.cancel_class_btn.setEnabled(False)
            self.parent.restore_class_btn.setEnabled(False)
            # =============== STUDENT ===============
            self.parent.add_student_btn.setEnabled(False)
            self.parent.edit_student_btn.setEnabled(False)
            self.parent.save_student_btn.setEnabled(True)
            self.parent.cancel_student_btn.setEnabled(True)
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

    def populate_form(self, student_data):
        """Điền dữ liệu sinh viên vào form"""
        if not student_data:
            return
        self.parent.student_id.setText(student_data['MASV'])
        self.parent.student_lastname.setText(student_data['HO'])
        self.parent.student_firstname.setText(student_data['TEN'])
        if student_data['PHAI'] == 'Nam':
            self.parent.radio_male.setChecked(True)
        else:
            self.parent.radio_female.setChecked(True)
        self.parent.student_address.setText(student_data['DIACHI'])
        try:
            dob_field = student_data.get('NGAYSINH')
            if dob_field:
                date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]
                dob = None
                for date_format in date_formats:
                    try:
                        dob = datetime.strptime(str(dob_field), date_format)
                        break
                    except ValueError:
                        continue
                self.parent.student_dob.setDate(QDate(dob.year, dob.month, dob.day))
        except Exception as e:

            now = datetime.now()
            self.parent.student_dob.setDate(QDate(now.year, now.month, now.day))

        # Phần còn lại giữ nguyên
        if isinstance(student_data['DANGNGHIHOC'], bool):
            self.parent.student_is_paused.setChecked(student_data['DANGNGHIHOC'])
        else:
            self.parent.student_is_paused.setChecked(student_data['DANGNGHIHOC'] not in [None, '', 0, '0'])

    # Các callback được gọi bởi controller
    def prepare_for_add(self):
        """Chuẩn bị form để thêm sinh viên mới"""
        self.clear_form()
        self.set_form_state(FormState.ADDING)

        if hasattr(self.parent, 'student_form_title'):
            self.parent.student_form_title.setText("THÊM SINH VIÊN MỚI")

        self.parent.student_id.setFocus()

    def prepare_for_edit(self):
        """Chuẩn bị form để chỉnh sửa sinh viên"""
        self.original_data = self.get_form_data()

        self.set_form_state(FormState.EDITING)

        if hasattr(self.parent, 'student_form_title'):
            self.parent.student_form_title.setText("CHỈNH SỬA SINH VIÊN")
        self.parent.student_lastname.setFocus()
    
    def after_save(self):
        """Xử lý sau khi lưu thành công"""
        self.set_form_state(FormState.VIEWING)
        self.original_data = None

        if hasattr(self.parent, 'student_form_title'):
            self.parent.student_form_title.setText("THÔNG TIN SINH VIÊN")

    def after_cancel(self):
        """Xử lý sau khi hủy thao tác"""
        if self.current_state == FormState.EDITING and self.original_data:
            self.populate_form(self.original_data)
        else:
            self.clear_form()

        self.set_form_state(FormState.VIEWING)

        self.original_data = None

        if hasattr(self.parent, 'student_form_title'):
            self.parent.student_form_title.setText("THÔNG TIN SINH VIÊN")

    def clear_form(self):
        self.parent.student_id.clear()
        self.parent.student_lastname.clear()
        self.parent.student_firstname.clear()
        self.parent.radio_male.setChecked(True)
        self.parent.student_address.clear()
        self.parent.student_is_paused.setChecked(False)
    
    def get_selected_item(self, item):
        row = item.row()
        selected_stduent_info = {
            'MASV':self.parent.student_table.item(row, 0).text(),
            'HO':self.parent.student_table.item(row, 1).text(),
            'TEN':self.parent.student_table.item(row, 2).text(),
            'PHAI':self.parent.student_table.item(row, 3).text(),
            'NGAYSINH':self.parent.student_table.item(row, 4).text(),
            'DIACHI':self.parent.student_table.item(row, 5).text(),
            'DANGNGHIHOC':self.parent.student_table.item(row, 6).text()
        }
        return selected_stduent_info
    
    def get_selected_student_id(self):
        return self.parent.student_id.text().strip()

    def get_form_data(self):
        data_form = {
            'MASV': self.parent.student_id.text().strip(),
            'HO': self.parent.student_lastname.text().strip(),
            'TEN': self.parent.student_firstname.text().strip(),
            'PHAI': 'Nam' if self.parent.radio_male.isChecked() else 'Nữ',
            'NGAYSINH': self.parent.student_dob.date().toString('yyyy-MM-dd'),
            'DIACHI': self.parent.student_address.text().strip(),
            'DANGNGHIHOC': 1 if self.parent.student_is_paused.isChecked() else 0,
            'MALOP': self.parent.student_class_id.text().strip()
        }
        return data_form
    
