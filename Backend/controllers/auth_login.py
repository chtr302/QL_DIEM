from Backend.database.connection import DatabaseConnection

class AuthLogin:
    @staticmethod
    def verify_student(student_id, password):
        cursor = DatabaseConnection.connection_admin().cursor()
        try:
            cursor.execute("{Call CheckSV (?, ?)}", (student_id, password))
            result = cursor.fetchone()
            if result is None:
                return False, None, None, 'Vui lòng kiểm tra lại Mã Sinh viên và mật khẩu'
            student_info = {
                'MaSV' : result[0],
                'Ten' : result[1]
            }
            connection_sv = DatabaseConnection.connection_sv()
            if connection_sv:
                return True, connection_sv, student_info, 'Đăng nhập thành công'
        except Exception as e:
            return False, None, None, 'Đăng nhập không thành công có lỗi đến từ Server'
        finally:
            cursor.close()

    @staticmethod
    def get_login_info(username):
        connection = DatabaseConnection.connection_admin()
        try:
            cursor = connection.cursor()
            cursor.execute('{Call CheckLogin (?)}', (username,))
            result = cursor.fetchone()
            if not result:
                return None
            login_info = {
                'MaGV': result[0],
                'HoTen': result[1],
                'MaKhoa': result[2],
                'TenKhoa':result[3],
                'Role': result[4]
            }
            return login_info
        except Exception as e:
            print(f'Error: {e}')
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def verify_teacher(username, password):
        login_info = AuthLogin.get_login_info(username)
        if not login_info:
            return False, None, None, "Đăng nhập không thành công. Vui lòng kiểm tra lại tài khoản và mật khẩu."
        try:
            connect_login = DatabaseConnection.connection_gv(username, password)
            if connect_login:
                return True, connect_login, login_info, "Đăng nhập thành công"
            else:
                return False, None, None, "Đăng nhập không thành công. Vui lòng kiểm tra lại tài khoản và mật khẩu."
        except Exception as e:
            return False, None, None, f"Lỗi kết nối: {e}"
