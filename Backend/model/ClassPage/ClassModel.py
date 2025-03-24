class ClassModel:
    def __init__(self, connection):
        self.connection = connection

    def get_dept(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM Khoa')
            dept = []
            for row in cursor.fetchall():
                dept.append({
                    'MAKHOA': row[0],
                    'TENKHOA': row[1]
                })
            cursor.close()
            return dept
        except Exception as e:
            print(f'Debug: Không load được dept: {e}')
            import traceback
            traceback.print_exc()
            return []
    
    def get_classes_by_dept_code(self, dept_code):
        if not dept_code:
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM ThongTinLopHoc WHERE MAKHOA = ?',(dept_code,))
            classes = []
            for row in cursor.fetchall():
                classes.append({
                    'MALOP':row[0],
                    'TENLOP': row[1],
                    'NIENKHOA': row[2],
                    'TENKHOA': row[4],
                    'SISO':row[5]
                })
            cursor.close()
            return classes
        except Exception as e:
            print(e)
            return []

    def check_dept_exists(self, dept_id):
        if not dept_id:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("EXEC KiemTraKhoaTonTai ?", (dept_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            return 0 if count == 0 else 1
        except Exception as e:
            return False

    def check_class_exists(self, student_id):
        """Kiểm tra một lớp có tồn tại không"""
        if not student_id:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("EXEC KiemTraSinhVien ?", (student_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            return 0 if count == 0 else 1
        except Exception as e:
            return False

    def add_class(self, class_data):
        if not class_data or 'MALOP' not in class_data:
            return False, 'Dữ liệu không hợp lệ'
        try:
            if self.check_dept_exists(class_data['MAKHOA']) == 1:
                return False, f'Mã {class_data['MAKHOA']} không tồn tại.'
            if self.check_class_exists(class_data['MALOP']) == 0:
                return False, f'Mã {class_data['MALOP']} đã tồn tại.'
            # Chạy SP
            cursor = self.connection.cursor()
            cursor.execute("EXEC ThemLop ?, ?, ?, ?", (class_data['MALOP'], class_data['TENLOP'], class_data['NIENKHOA'], class_data['MAKHOA']))
            self.connection.commit()
            cursor.close()
            return True, 'Thêm lớp thành công'
        except Exception as e:
            self.connection.rollback()
            return False, f'Lỗi khi thêm lớp {e}'

    def edit_class(self, class_data):
        if not class_data or 'MALOP' not in class_data:
            return False,'Dữ liệu không hợp lệ'
        try:
            if self.check_class_exists(class_data['MALOP']) == 1:
                return False, f'Mã {class_data['MALOP']} đã tồn tại.'
            if self.check_dept_exists(class_data['MAKHOA']) == 1:
                return False, f'Mã {class_data['MAKHOA']} không tồn tại.'
            cursor = self.connection.cursor()
            cursor.execute("EXEC CapNhatLop ?,?,?,?",(class_data['MALOP'], class_data['TENLOP'],class_data['NIENKHOA'],class_data['MAKHOA']))
            self.connection.commit()
            cursor.close()
            return True, 'Cập nhật lớp thành công'
        except Exception as e:
            self.connection.rollback()
            return False, f'Lỗi khi cập nhật lớp {e}'

    def save_class(self, class_data):
        """Lưu thông tin lớp học (thêm mới hoặc cập nhật)"""
        if not class_data or 'MALOP' not in class_data:
            return False,'Dữ liệu không hợp lệ'
        exists = self.check_class_exists(class_data['MALOP'])
        return self.edit_class(class_data) if exists == 0 else self.add_class(class_data)
