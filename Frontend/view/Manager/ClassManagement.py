from Frontend.view.Manager.BasePage import BasePage
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class ClassManagementPage(BasePage):
    def __init__(self, parent=None, connection=None, user_info=None):
        super().__init__(parent, connection, "Quản Lý Lớp Học", user_info)
    
    def init_ui(self):
        # UI phần tìm kiếm và lọc theo khoa
        self.filter_widget = QWidget()
        self.filter_layout = QHBoxLayout()
        self.filter_widget.setLayout(self.filter_layout)
        
        self.dept_label = QLabel("Khoa:")
        self.dept_combo = QComboBox()
        self.dept_combo.currentIndexChanged.connect(self.filter_by_department)
        
        self.search_label = QLabel("Tìm kiếm:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Nhập mã lớp hoặc tên lớp...")
        self.search_edit.textChanged.connect(self.search_classes)
        
        self.filter_layout.addWidget(self.dept_label)
        self.filter_layout.addWidget(self.dept_combo)
        self.filter_layout.addStretch()
        self.filter_layout.addWidget(self.search_label)
        self.filter_layout.addWidget(self.search_edit)
        
        self.add_content_widget(self.filter_widget)
        
        # Bảng danh sách lớp
        self.class_table = QTableWidget()
        self.class_table.setColumnCount(5)
        self.class_table.setHorizontalHeaderLabels(["Mã lớp", "Tên lớp", "Khóa học", "Mã khoa", "Ghi chú"])
        self.class_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.class_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.class_table.itemClicked.connect(self.select_class)
        
        self.add_content_widget(self.class_table)
        
        # Form chi tiết lớp
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        
        self.class_id_edit = QLineEdit()
        self.class_name_edit = QLineEdit()
        self.course_edit = QLineEdit()
        self.dept_id_combo = QComboBox()
        self.note_edit = QTextEdit()
        
        self.form_layout.addRow("Mã lớp:", self.class_id_edit)
        self.form_layout.addRow("Tên lớp:", self.class_name_edit)
        self.form_layout.addRow("Khóa học:", self.course_edit)
        self.form_layout.addRow("Mã khoa:", self.dept_id_combo)
        self.form_layout.addRow("Ghi chú:", self.note_edit)
        
        self.add_content_widget(self.form_widget)
    
    def load_data(self):
        # Giả lập dữ liệu - trong thực tế, bạn sẽ lấy từ database
        # Load danh sách khoa
        departments = [
            {"MaKhoa": "CNTT", "TenKhoa": "Công nghệ thông tin"},
            {"MaKhoa": "DTVT", "TenKhoa": "Điện tử viễn thông"},
            {"MaKhoa": "ATTT", "TenKhoa": "An toàn thông tin"}
        ]
        
        self.dept_combo.clear()
        self.dept_combo.addItem("Tất cả", None)
        for dept in departments:
            self.dept_combo.addItem(dept["TenKhoa"], dept["MaKhoa"])
        
        self.dept_id_combo.clear()
        for dept in departments:
            self.dept_id_combo.addItem(dept["TenKhoa"], dept["MaKhoa"])
        
        # Load danh sách lớp
        self.load_classes()
    
    def load_classes(self, dept_id=None):
        # Trong thực tế, bạn sẽ truy vấn DB với filter theo dept_id
        # Giả lập dữ liệu
        classes = [
            {"MaLop": "D20CQCN01", "TenLop": "D20 Chính quy CN 01", "KhoaHoc": "2020-2025", "MaKhoa": "CNTT", "GhiChu": ""},
            {"MaLop": "D20CQCN02", "TenLop": "D20 Chính quy CN 02", "KhoaHoc": "2020-2025", "MaKhoa": "CNTT", "GhiChu": ""},
            {"MaLop": "D20CQVT01", "TenLop": "D20 Chính quy VT 01", "KhoaHoc": "2020-2025", "MaKhoa": "DTVT", "GhiChu": ""},
            {"MaLop": "D20CQAT01", "TenLop": "D20 Chính quy AT 01", "KhoaHoc": "2020-2025", "MaKhoa": "ATTT", "GhiChu": ""}
        ]
        
        # Lọc theo khoa nếu có
        if dept_id:
            classes = [c for c in classes if c["MaKhoa"] == dept_id]
        
        # Cập nhật bảng
        self.class_table.setRowCount(0)
        for i, cls in enumerate(classes):
            self.class_table.insertRow(i)
            self.class_table.setItem(i, 0, QTableWidgetItem(cls["MaLop"]))
            self.class_table.setItem(i, 1, QTableWidgetItem(cls["TenLop"]))
            self.class_table.setItem(i, 2, QTableWidgetItem(cls["KhoaHoc"]))
            self.class_table.setItem(i, 3, QTableWidgetItem(cls["MaKhoa"]))
            self.class_table.setItem(i, 4, QTableWidgetItem(cls["GhiChu"]))
    
    def filter_by_department(self):
        dept_id = self.dept_combo.currentData()
        self.load_classes(dept_id)
    
    def search_classes(self):
        text = self.search_edit.text().lower()
        for i in range(self.class_table.rowCount()):
            match = False
            for j in range(2):  # Tìm trong 2 cột đầu (mã và tên)
                item = self.class_table.item(i, j)
                if item and text in item.text().lower():
                    match = True
                    break
            self.class_table.setRowHidden(i, not match)
    
    def select_class(self):
        current_row = self.class_table.currentRow()
        if current_row >= 0:
            self.class_id_edit.setText(self.class_table.item(current_row, 0).text())
            self.class_name_edit.setText(self.class_table.item(current_row, 1).text())
            self.course_edit.setText(self.class_table.item(current_row, 2).text())
            
            dept_id = self.class_table.item(current_row, 3).text()
            for i in range(self.dept_id_combo.count()):
                if self.dept_id_combo.itemData(i) == dept_id:
                    self.dept_id_combo.setCurrentIndex(i)
                    break
            
            self.note_edit.setText(self.class_table.item(current_row, 4).text())
    
    # Ghi đè các phương thức CRUD
    def add_item(self):
        # Xóa trống form để nhập mới
        self.class_id_edit.clear()
        self.class_name_edit.clear()
        self.course_edit.clear()
        self.dept_id_combo.setCurrentIndex(0)
        self.note_edit.clear()
        
        # Focus vào ô đầu tiên
        self.class_id_edit.setFocus()
        self.set_modified()
    
    def delete_item(self):
        current_row = self.class_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn lớp cần xóa!")
            return
        
        class_id = self.class_table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Xác nhận", 
                                    f"Bạn có chắc muốn xóa lớp {class_id}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Trong thực tế, gọi API xóa từ DB
            self.class_table.removeRow(current_row)
            self.add_item()  # Reset form
            QMessageBox.information(self, "Thông báo", f"Đã xóa lớp {class_id}")
    
    def save_item(self):
        # Kiểm tra dữ liệu
        class_id = self.class_id_edit.text().strip()
        class_name = self.class_name_edit.text().strip()
        course = self.course_edit.text().strip()
        dept_id = self.dept_id_combo.currentData()
        note = self.note_edit.toPlainText().strip()
        
        if not class_id or not class_name or not course or not dept_id:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return
        
        # Trong thực tế, gọi API lưu vào DB
        # Kiểm tra xem là thêm mới hay cập nhật
        found = False
        for i in range(self.class_table.rowCount()):
            if self.class_table.item(i, 0).text() == class_id:
                # Cập nhật dòng hiện có
                self.class_table.item(i, 1).setText(class_name)
                self.class_table.item(i, 2).setText(course)
                self.class_table.item(i, 3).setText(dept_id)
                self.class_table.item(i, 4).setText(note)
                found = True
                break
        
        if not found:
            # Thêm dòng mới
            row = self.class_table.rowCount()
            self.class_table.insertRow(row)
            self.class_table.setItem(row, 0, QTableWidgetItem(class_id))
            self.class_table.setItem(row, 1, QTableWidgetItem(class_name))
            self.class_table.setItem(row, 2, QTableWidgetItem(course))
            self.class_table.setItem(row, 3, QTableWidgetItem(dept_id))
            self.class_table.setItem(row, 4, QTableWidgetItem(note))
        
        QMessageBox.information(self, "Thông báo", "Lưu thành công!")
        self.set_modified(False)
    
    def restore_item(self):
        current_row = self.class_table.currentRow()
        if current_row >= 0:
            self.select_class()  # Reload thông tin từ bảng
            QMessageBox.information(self, "Thông báo", "Đã phục hồi thông tin!")
        else:
            self.add_item()  # Xóa form