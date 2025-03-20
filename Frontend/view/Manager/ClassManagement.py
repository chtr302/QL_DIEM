from Frontend.view.Manager.BasePage import BasePage
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

class ClassManagementPage(BasePage):
    def __init__(self, parent=None, connection=None, user_info=None, controller=None):
        super().__init__(parent, connection, user_info)

        self.controller = controller

        self.setup_class_ui()
        self.connect_events()
    
    def setup_class_ui(self):
        """Thiết lập giao diện quản lý lớp với hai container riêng biệt"""
        # Container chính chứa hai panel
        self.main_container = QWidget()
        self.main_container_layout = QHBoxLayout(self.main_container)
        self.main_container_layout.setContentsMargins(10, 10, 10, 10)
        self.main_container_layout.setSpacing(10)
        
        # ============== PANEL KHOA (BÊN TRÁI) ==============
        self.dept_container = QWidget()
        self.dept_container.setObjectName("deptContainer")
        self.dept_container.setStyleSheet("""
            #deptContainer {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 5px;
            }
        """)
        # Thiết lập kích thước cố định cho panel khoa
        self.dept_container.setMinimumWidth(350)
        self.dept_container.setMaximumWidth(400)
        
        self.dept_container_layout = QVBoxLayout(self.dept_container)
        
        # Tiêu đề panel khoa
        dept_header = QLabel("DANH SÁCH KHOA")
        dept_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dept_header.setStyleSheet("""
            font-weight: bold;
            font-size: 16pt;
            color: black;
            padding: 10px;
        """)
        
        # Thanh tìm kiếm khoa
        self.dept_search_layout = QHBoxLayout()
        self.dept_search = QLineEdit()
        self.dept_search.setPlaceholderText("Tìm kiếm khoa...")
        self.dept_search.setClearButtonEnabled(True)
        
        self.dept_search_btn = QPushButton("Tìm")
        
        self.dept_search_layout.addWidget(self.dept_search)
        self.dept_search_layout.addWidget(self.dept_search_btn)
        
        # Bảng danh sách khoa
        self.dept_table = QTableWidget()
        self.dept_table.setColumnCount(2)
        self.dept_table.setHorizontalHeaderLabels(["Mã khoa", "Tên khoa"])
        self.dept_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.dept_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.dept_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Thêm các widget vào layout của panel khoa
        self.dept_container_layout.addWidget(dept_header)
        self.dept_container_layout.addLayout(self.dept_search_layout)
        self.dept_container_layout.addWidget(self.dept_table)

        # ============== PANEL LỚP HỌC (BÊN PHẢI) ==============
        self.class_container = QWidget()
        self.class_container.setObjectName("classContainer")
        self.class_container.setStyleSheet("""
            #classContainer {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 5px;
            }
        """)
        
        self.class_container_layout = QVBoxLayout(self.class_container)
        
        # Header cho panel lớp học với thông tin khoa đang chọn
        self.class_header = QLabel("DANH SÁCH LỚP HỌC")
        self.class_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.class_header.setStyleSheet("""
            font-weight: bold;
            font-size: 16pt;
            color: #0066cc;
            padding: 10px;
        """)
        
        # Label hiển thị khoa đang được chọn
        self.selected_dept_label = QLabel("Chưa chọn khoa")
        self.selected_dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_dept_label.setStyleSheet("""
            font-weight: bold;
            font-size: 14pt;
            color: #333333;
            padding: 5px;
        """)

        # Form thông tin lớp
        class_form_group = QGroupBox("Thông tin lớp")
        class_form_layout = QFormLayout()
        
        self.class_id = QLineEdit()
        self.class_name = QLineEdit()
        self.course_year = QComboBox()
        for year in range(2020, 2031):
            self.course_year.addItem(str(year))
        
        class_form_layout.addRow("Mã lớp:", self.class_id)
        class_form_layout.addRow("Tên lớp:", self.class_name)
        class_form_layout.addRow("Niên khóa:", self.course_year)
        
        class_form_group.setLayout(class_form_layout)
        
        # Thanh tìm kiếm lớp
        class_search_layout = QHBoxLayout()
        self.class_search = QLineEdit()
        self.class_search.setPlaceholderText("Tìm kiếm lớp...")
        self.class_search.setClearButtonEnabled(True)
        
        self.class_search_btn = QPushButton("Tìm")
        
        class_search_layout.addWidget(self.class_search)
        class_search_layout.addWidget(self.class_search_btn)
        
        # Bảng danh sách lớp
        self.class_table = QTableWidget()
        self.class_table.setColumnCount(4)
        self.class_table.setHorizontalHeaderLabels(["Mã lớp", "Tên lớp", "Niên khóa", "Khoa", "Sĩ số"])
        self.class_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.class_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.class_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Thêm các widget vào layout của panel lớp
        self.class_container_layout.addWidget(self.class_header)
        self.class_container_layout.addWidget(self.selected_dept_label)
        self.class_container_layout.addWidget(class_form_group)
        self.class_container_layout.addLayout(class_search_layout)
        self.class_container_layout.addWidget(self.class_table)
        
        # Thêm hai panel vào container chính
        self.main_container_layout.addWidget(self.dept_container)
        self.main_container_layout.addWidget(self.class_container, 1)  # Stretch factor 1 để panel lớp mở rộng hơn
        
        # Thêm container chính vào layout của BasePage
        self.main_layout.addWidget(self.main_container)

    def connect_events(self):
        self.dept_table.itemClicked.connect(self.department_selected)
        
        self.class_table.itemClicked.connect(self.class_selected)
        self.class_search.textChanged.connect(self.class_search_changed)
        self.class_search_btn.clicked.connect(self.class_search_clicked)

        self.connect_action_toolbar()

    def connect_action_toolbar(self):
        if hasattr(self, 'add_action'):
            self.add_action.triggered.connect(self.add_action_clicked)
        if hasattr(self, 'edit_action'):
            self.edit_action.triggered.connect(self.edit_action_clicked)
        if hasattr(self, 'delete_action'):
            self.delete_action.triggered.connect(self.delete_action_clicked)
        if hasattr(self, 'save_action'):
            self.save_action.triggered.connect(self.save_action_clicked)
        if hasattr(self, 'restore_action'):
            self.restore_action.triggered.connect(self.restore_action_clicked)
    
    def department_selected(self, item):
        # Xử lý khi PGV chọn một khoa
        if not self.controller:
            return
        row = item.row()
        dept_code = self.dept_table.item(row, 0).text()
        dept_name = self.dept_table.item(row, 1).text()

        self.controller.select_department(dept_code, dept_name)

    def class_selected(self, item):
        # Xử lý PGV chọn lớp
        if not self.controller:
            return
        row = item.row()
        class_id = self.class_table.item(row, 0).text()

        self.controller.select_class(class_id)

    def class_search_clicked(self):
        # Xử lý tìm kiếm lớp
        if self.controller:
            self.controller.filter_classes(self.class_search.text())

    def class_search_changed(self, text):
        # Xử lý thay đổi tìm kiếm lớp
        if self.controller:
            self.controller.filter_classes(text)

    # Gọi Controller xử lí các action
    def add_action_clicked(self):
        if self.controller:
            self.controller.add_class()

    def edit_action_clicked(self):
        if self.controller:
            self.controller.edit_class()

    def delete_action_clicked(self):
        if self.controller:
            self.controller.delete_class()

    def save_action_clicked(self):
        if self.controller:
            self.controller.save_class()

    def restore_action_clicked(self):
        if self.controller:
            self.controller.restore_class_data()
    
    # Update UI
    def set_selected_department(self, dept_code, dept_name):
        self.selected_dept_code = dept_code
        self.selected_dept_name = dept_name

        if dept_name:
            self.selected_dept_label.setText(f"Khoa: {dept_name}")
        else:
            self.selected_dept_label.setText("Chưa chọn khoa")

    def update_department_table(self, dept_data):
        self.dept_table.setRowCount(0)
        
        for row_idx, dept in enumerate(dept_data):
            self.dept_table.insertRow(row_idx)

            code_item = QTableWidgetItem(dept['MAKHOA'])
            code_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dept_table.setItem(row_idx, 0, code_item)
            
            name_item = QTableWidgetItem(dept['TENKHOA'])
            self.dept_table.setItem(row_idx, 1, name_item)

    def update_class_table(self, class_data):
        self.class_table.setRowCount(0)
        
        for row_idx, cls in enumerate(class_data):
            self.class_table.insertRow(row_idx)
            self.class_table.setItem(row_idx, 0, QTableWidgetItem(cls['malop']))
            self.class_table.setItem(row_idx, 1, QTableWidgetItem(cls['tenlop']))
            self.class_table.setItem(row_idx, 2, QTableWidgetItem(cls['nienkhoa']))
            if 'tenkhoa' in cls:
                self.class_table.setItem(row_idx, 3, QTableWidgetItem(cls['tenkhoa']))

            siso_item = QTableWidgetItem(str(cls['siso']))
            siso_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.class_table.setItem(row_idx, 4, QTableWidgetItem(siso_item))

    # Thao tác với form
    def clear_class_form(self):
        self.class_id.clear()
        self.class_name.clear()
        self.course_year.setCurrentIndex(0)
        
        self.class_id.setReadOnly(False) # Cho phép điền id khi thêm mới

    def populate_class_form(self, class_data):
        self.class_id.setText(class_data['malop'])
        self.class_name.setText(class_data['tenlop'])
        
        nienkhoa = class_data.get('nienkhoa', '')
        index = self.course_year.findText(nienkhoa)
        if index >= 0:
            self.course_year.setCurrentIndex(index)
        
        self.class_id.setReadOnly(True) # edit thì không sửa được mã lớp

    def get_class_form_data(self):
        """Lấy dữ liệu từ form để gửi đến controller"""
        return {
            'malop': self.class_id.text().strip(),
            'tenlop': self.class_name.text().strip(),
            'nienkhoa': self.course_year.currentText(),
            'makhoa': self.selected_dept_code
        }
    
    # Phân quyền
    def apply_role_restrictions(self, user_info):
        if not user_info:
            return
        role = user_info.get('Role', '')
        if role == 'KHOA':
            self.dept_container.setVisible(False)

            self.class_container.setMinimumWidth(800)

            khoa_name = user_info.get('Khoa', 'Không xác định')
            self.selected_dept_label.setText(f"Khoa: {khoa_name}")
            self.class_header.setText(f"DANH SÁCH LỚP HỌC - KHOA {khoa_name}")
        else:
            self.dept_container.setVisible(True)

    # Chế độ edit
    def set_editing_mode(self, is_editing=True):
        self.class_id.setReadOnly(is_editing) # Không cho chỉnh mã lớp nếu action là edit

        if is_editing:
            self.class_name.setFocus()
        else:
            self.class_id.setFocus()