import pyodbc

# Cấu hình Driver SQL Server
DRIVER = 'ODBC Driver 18 for SQL Server'
SERVER = 'localhost'
DATABASE = 'QL_DIEM'

class DatabaseConnection:
    # Hàm connection string
    @staticmethod
    def connection_string(login,password):
        return f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={login};PWD={password};TrustServerCertificate=yes;'
    
    # Kết nối admin để gọi SP kiểm tra
    @staticmethod
    def connection_admin():
        login = 'conghau'
        password = '123456'
        connect_string = DatabaseConnection.connection_string(login,password)
        try:
            connect = pyodbc.connect(connect_string)
            return connect
        except pyodbc.Error as e:
            return None
    
    @staticmethod
    def connection_gv(login, password):
        connect_string = DatabaseConnection.connection_string(login,password)
        try:
            connect = pyodbc.connect(connect_string)
            return connect
        except pyodbc.Error as e:
            return None
    
    @staticmethod
    def connection_sv():
        login = 'SinhVien'
        password = '123456'
        connect_string = DatabaseConnection.connection_string(login,password)
        try:
            connect = pyodbc.connect(connect_string)
            return connect
        except pyodbc.Error as e:
            print(f'Failed: {e}')
            return None