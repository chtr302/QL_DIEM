from Backend.model.ClassPage.ClassModel import ClassModel
class StudentModel:
    def __init__(self, connection):
        self.connection = connection

        self.class_model = ClassModel(self.connection)

    def get_students_by_class_id(self, class_id):
        """Lấy danh sách sinh viên của một lớp"""
        if not class_id:
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM Sinhvien WHERE MALOP = ?', (class_id,))
            
            students = []
            for row in cursor.fetchall():
                students.append({
                    'MASV': row[0],
                    'HO': row[1],
                    'TEN': row[2],
                    'PHAI': row[3],
                    'NGAYSINH': row[4],
                    'DIACHI': row[5],
                    'DANGNGHIHOC':row[6],
                    'MALOP': row[9]
                })
                
            cursor.close()
            return students
            
        except Exception as e:
            print(f"Error in get_students_by_class: {e}")
            return []
    
    def check_student_exists(self, student_id):
        if not student_id:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("EXEC KiemTraSinhVien ?", (student_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            print(f"Kiểm tra sinh viên {student_id}: {count > 0}")
            return count > 0
        except Exception as e:
            return False

    def add_student(self, student_info):
        if not student_info:
            return False, 'Không có thông tin sinh viên'
        try:
            Phai = 0 if student_info['PHAI'] == 'Nam' else 1
            if self.check_student_exists(student_info['MASV']):
                return False, f'Mã sinh viên {student_info['MASV']} đã tồn tại. Vui lòng nhập mã phù hợp!'
            cursor = self.connection.cursor()
            cursor.execute('EXEC ThemSinhVien ?,?,?,?,?,?,?,?',(
                student_info['MASV'],
                student_info['HO'],
                student_info['TEN'],
                0 if student_info['PHAI'] == 'Nam' else 1,
                student_info['NGAYSINH'],
                student_info['DIACHI'],
                student_info['DANGNGHIHOC'],
                student_info['MALOP'],
            ))
            self.connection.commit()
            cursor.close()
            return True,f'Thêm sinh viên {student_info['HO']} {student_info['TEN']} với mã sinh viên {student_info['MASV']} thành công.'
        except Exception as e:
            print(e)
            return False, f'Có lỗi khi thêm sinh viên'
    
    def edit_student(self, student_info):
        if not student_info:
            return False, 'Không có thông tin sinh viên'
        class_exists = self.class_model.check_class_exists(student_info['MALOP'])
        if class_exists == 1:
            return False, 'Lớp không tồn tại!'
        try:
            cursor = self.connection.cursor()
            cursor.execute('EXEC CapNhatSinhVien ?,?,?,?,?,?,?,?',(
                student_info['MASV'],
                student_info['HO'],
                student_info['TEN'],
                0 if student_info['PHAI'] == 'Nam' else 1,
                student_info['NGAYSINH'],
                student_info['DIACHI'],
                student_info['DANGNGHIHOC'],
                student_info['MALOP'],
            ))
            self.connection.commit()
            cursor.close()
            return True,f'Cập nhật sinh viên {student_info['HO']} {student_info['TEN']} với mã sinh viên {student_info['MASV']} thành công.'
        except Exception as e:
            print(e)
            return False, f'Có lỗi khi cập nhật sinh viên'

    def save_student(self, student_info):
        exists = self.check_student_exists(student_info['MASV'])
        return self.edit_student(student_info) if exists else self.add_student(student_info)