from Frontend.view.ClassPage.BasePage import BasePage
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Frontend.utils.ClassPage.class_manager import ClassManager
from Frontend.utils.ClassPage.student_manager import StudentManager
from Backend.controllers.ClassPage.class_controller import ClassController

IMG_PATH = 'Frontend/assets/image/ToolbarBasePage'

class ClassManagementPage(BasePage):
    def __init__(self, parent=None, connection=None, user_info=None, controller=None, student_controller=None):
        super().__init__(parent, connection, user_info)

        self.controller = controller
        self.student_controller = student_controller

        self.class_manager = ClassManager(self, self.controller)
        self.student_manager = StudentManager(self, self.student_controller)

        self.setup_class_ui()
        self.connect_events()
        if self.controller:
            self.initialize_controller()

    def initialize_controller(self):
        """Khởi tạo controller và đặt các giá trị ban đầu"""
        if self.controller:
            print(f'Controller exists {self.controller}')
            self.controller.initialize_by_role()
 
    def load_style(self):
        try:
            with open('Frontend/assets/style/ClassPage.css', 'r') as f:
                style_sheet = f.read()

            self.setStyleSheet(style_sheet)
        except Exception as e:
            print(f'Lỗi khi load css: {e}')

    def setup_class_ui(self):
        self.load_style()

        self.main_container = QWidget()
        self.main_container.setObjectName("mainContainer")
        self.main_container_layout = QVBoxLayout(self.main_container)
        self.main_container_layout.setContentsMargins(10, 10, 10, 10)
        self.main_container_layout.setSpacing(10)
        
        # ============== PANEL CHỌN KHOA (TRÊN CÙNG) ==============
        self.create_department_panel()
        
        # ============== PANEL CHÍNH (CHỨA LỚP VÀ SINH VIÊN) ==============
        self.content_container = QWidget()
        self.content_container_layout = QVBoxLayout(self.content_container)
        self.content_container_layout.setContentsMargins(0, 0, 0, 0)
        self.content_container_layout.setSpacing(10)
        
        # ============== PANEL LỚP HỌC (PHÍA TRÊN) ==============
        self.create_class_panel()
        
        # # ============== PANEL SINH VIÊN (PHÍA DƯỚI) ==============
        self.create_student_panel()
        
        self.content_container_layout.addWidget(self.class_container, 1)
        self.content_container_layout.addWidget(self.student_container, 2)

        self.main_container_layout.addWidget(self.dept_container)
        self.main_container_layout.addWidget(self.content_container, 1)

        self.main_layout.addWidget(self.main_container)

    def create_department_panel(self):
        self.dept_container = QWidget()
        self.dept_container.setObjectName("deptContainer")
        self.dept_container.setMaximumHeight(80)
        
        self.dept_container_layout = QHBoxLayout(self.dept_container)
        self.dept_container_layout.setContentsMargins(5, 5, 5, 5)

        dept_label = QLabel("CHỌN KHOA:")
        dept_label.setObjectName("dept-label")
        dept_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        dept_label.setMinimumWidth(100)

        self.dept_combo = QComboBox()
        self.dept_combo.setObjectName("dept-combo")
        self.dept_combo.setMinimumWidth(300)

        self.dept_container_layout.addWidget(dept_label)
        self.dept_container_layout.addWidget(self.dept_combo, 1)

    def create_class_panel(self):
        self.class_container = QWidget()
        self.class_container.setObjectName("classContainer")

        self.class_container_layout = QHBoxLayout(self.class_container)
        self.class_container_layout.setContentsMargins(5, 5, 5, 5)
        self.class_container_layout.setSpacing(3)
        
        # ============ PHẦN TRÁI - FORM NHẬP LIỆU ============
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(3)

        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.class_header = QLabel("DANH SÁCH LỚP HỌC")
        self.class_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.class_header.setObjectName("class-header")
        self.class_header.setProperty("class", "header-label")
        
        self.selected_dept_label = QLabel("Chưa chọn khoa")
        self.selected_dept_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.selected_dept_label.setObjectName("selected-dept-label")
        
        header_layout.addWidget(self.class_header)
        header_layout.addWidget(self.selected_dept_label)

        class_form_group = QGroupBox("Thông tin lớp")
        class_form_layout = QFormLayout()
        class_form_layout.setVerticalSpacing(10)
        class_form_layout.setHorizontalSpacing(10)
        class_form_layout.setContentsMargins(10, 20, 10, 10)

        id_label = QLabel("Mã lớp:")
        self.class_id = QLineEdit()
        self.class_id.setPlaceholderText("Nhập mã lớp")
        self.class_id.setMaxLength(15)

        name_label = QLabel("Tên lớp:")
        self.class_name = QLineEdit()
        self.class_name.setPlaceholderText("Nhập tên lớp")
        self.class_name.setMaxLength(15)

        year_label = QLabel("Niên khóa:")
        self.course_year = QLineEdit()
        self.course_year.setPlaceholderText("Nhập niên khoá")
        self.class_name.setMaxLength(15)

        dept_label = QLabel("Khoa:")
        self.dept_display = QLabel("Chưa chọn khoa")
        self.dept_display.setStyleSheet("font-weight: bold; color: #006699;")

        class_form_layout.addRow(id_label, self.class_id)
        class_form_layout.addRow(name_label, self.class_name)
        class_form_layout.addRow(year_label, self.course_year)
        class_form_layout.addRow(dept_label, self.dept_display)

        button_container = QWidget()
        button_container_layout = QVBoxLayout(button_container)
        button_container_layout.setContentsMargins(0, 0, 0, 0)
        button_container_layout.setSpacing(5)  # Khoảng cách giữa 2 hàng nút
        
        # Hàng nút 1: Thêm, Sửa, Hủy
        button_row1 = QHBoxLayout()
        button_row1.setSpacing(5)  # Khoảng cách giữa các nút
        
        self.add_class_btn = QPushButton("Thêm")
        self.add_class_btn.setIcon(QIcon(f"{IMG_PATH}/add.png"))
        self.add_class_btn.setMinimumWidth(40)  # Giảm kích thước tối thiểu
        
        self.edit_class_btn = QPushButton("Sửa")
        self.edit_class_btn.setIcon(QIcon(f"{IMG_PATH}/edit.png"))
        self.edit_class_btn.setEnabled(False)
        self.edit_class_btn.setMinimumWidth(40)

        self.cancel_class_btn = QPushButton("Hủy")
        self.cancel_class_btn.setIcon(QIcon(f"{IMG_PATH}/remove.png"))
        self.cancel_class_btn.setEnabled(False)
        self.cancel_class_btn.setMinimumWidth(40)
        
        button_row1.addWidget(self.add_class_btn)
        button_row1.addWidget(self.edit_class_btn)
        button_row1.addWidget(self.cancel_class_btn)
        
        # Hàng nút 2: Lưu, Phục hồi
        button_row2 = QHBoxLayout()
        button_row2.setSpacing(5)  # Khoảng cách giữa các nút
        
        self.save_class_btn = QPushButton("Lưu")
        self.save_class_btn.setIcon(QIcon(f"{IMG_PATH}/save.png"))
        self.save_class_btn.setEnabled(False)
        self.save_class_btn.setMinimumWidth(40)

        self.restore_class_btn = QPushButton("Phục hồi")
        self.restore_class_btn.setIcon(QIcon(f"{IMG_PATH}/undo.png"))
        self.restore_class_btn.setEnabled(False)
        self.restore_class_btn.setMinimumWidth(40)
        
        button_row2.addWidget(self.save_class_btn)
        button_row2.addWidget(self.restore_class_btn)
        button_row2.addStretch(1)  # Thêm khoảng trống ở cuối để căn trái
        
        # Thêm 2 hàng vào container
        button_container_layout.addLayout(button_row1)
        button_container_layout.addLayout(button_row2)
        
        # Thêm container nút vào form
        class_form_layout.addRow("", button_container)
        
        class_form_group.setLayout(class_form_layout)

        left_layout.addWidget(header_widget)
        left_layout.addWidget(class_form_group, 1)
        
        # ============ PHẦN PHẢI - BẢNG DỮ LIỆU VÀ TÌM KIẾM ============
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)
        
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 5)
        
        self.class_search = QLineEdit()
        self.class_search.setPlaceholderText("Tìm kiếm lớp...")
        self.class_search.setClearButtonEnabled(True)
        
        self.class_search_btn = QPushButton("Tìm")
        self.class_search_btn.setIcon(QIcon.fromTheme("system-search"))
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.class_search, 1)
        search_layout.addWidget(self.class_search_btn)
        
        # Bảng dữ liệu
        self.class_table = QTableWidget()
        self.class_table.setColumnCount(5)
        self.class_table.setHorizontalHeaderLabels(["Mã lớp", "Tên lớp", "Niên khóa", "Khoa", "Sĩ số"])
        self.class_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.class_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.class_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.class_table.setMinimumHeight(300)
        self.class_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


        right_layout.addLayout(search_layout)
        right_layout.addWidget(self.class_table, 1)
        
        left_widget.setMinimumWidth(350)
        left_widget.setMaximumWidth(400)

        self.class_container_layout.addWidget(left_widget)
        self.class_container_layout.addWidget(right_widget, 1)

    def create_student_panel(self):
        self.load_style()
        self.student_container = QWidget()
        self.student_container.setObjectName("studentContainer")

        self.student_container_layout = QHBoxLayout(self.student_container)
        self.student_container_layout.setContentsMargins(5, 5, 5, 5)
        self.student_container_layout.setSpacing(2)
        
        # ============ PHẦN TRÁI - FORM NHẬP LIỆU ============
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(2)

        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.student_header = QLabel("DANH SÁCH SINH VIÊN")
        self.student_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.student_header.setObjectName("student-header")
        self.student_header.setProperty("class", "header-label")
        
        self.selected_class_label = QLabel("Chưa chọn lớp")
        self.selected_class_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.selected_class_label.setObjectName("selected-class-label")
        
        header_layout.addWidget(self.student_header)
        header_layout.addWidget(self.selected_class_label)

        student_form_group = QGroupBox("Thông tin sinh viên")
        student_form_layout = QFormLayout()
        student_form_layout.setVerticalSpacing(10)
        student_form_layout.setHorizontalSpacing(10)
        student_form_layout.setContentsMargins(10, 20, 10, 10)

        id_label = QLabel("Mã SV:")
        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("Nhập mã sinh viên")
        self.student_id.setMaxLength(10)

        lastname_label = QLabel("Họ:")
        self.student_lastname = QLineEdit()
        self.student_lastname.setPlaceholderText("Họ")

        firstname_label = QLabel("Tên:")
        self.student_firstname = QLineEdit()
        self.student_firstname.setPlaceholderText("Tên")

        birth_label = QLabel("Ngày sinh:")
        self.student_dob = QDateEdit()
        self.student_dob.setCalendarPopup(True)
        self.student_dob.setDisplayFormat("dd/MM/yyyy")
        self.student_dob.setDate(QDate.currentDate())

        gender_label = QLabel("Giới tính:")
        gender_widget = QWidget()
        gender_layout = QHBoxLayout(gender_widget)
        gender_layout.setContentsMargins(0, 0, 0, 0)
        gender_layout.setSpacing(10)

        self.radio_male = QRadioButton("Nam")
        self.radio_male.setChecked(True)
        self.radio_female = QRadioButton("Nữ")

        gender_layout.addWidget(self.radio_male)
        gender_layout.addWidget(self.radio_female)
        gender_layout.addStretch(1)

        address_label = QLabel("Địa chỉ:")
        self.student_address = QLineEdit()
        self.student_address.setPlaceholderText("Nhập địa chỉ")

        status_label = QLabel("Trạng thái:")
        self.student_is_paused = QCheckBox("Đang nghỉ học")

        class_id_label = QLabel("Mã Lớp:")
        self.student_class_id = QLineEdit()
        self.student_class_id.setPlaceholderText("Nhập mã lớp")
        self.student_class_id.setMaxLength(15)
    

        student_form_layout.addRow(id_label, self.student_id)
        student_form_layout.addRow(lastname_label, self.student_lastname)
        student_form_layout.addRow(firstname_label, self.student_firstname)
        student_form_layout.addRow(birth_label, self.student_dob)
        student_form_layout.addRow(gender_label, gender_widget)
        student_form_layout.addRow(address_label, self.student_address)
        student_form_layout.addRow(status_label, self.student_is_paused)
        student_form_layout.addRow(class_id_label, self.student_class_id)

        button_container = QWidget()
        button_container_layout = QVBoxLayout(button_container)
        button_container_layout.setContentsMargins(0, 0, 0, 0)
        button_container_layout.setSpacing(5)
        
        # Thêm, Sửa, Hủy
        button_row1 = QHBoxLayout()
        button_row1.setSpacing(5)
        
        self.add_student_btn = QPushButton("Thêm")
        self.add_student_btn.setIcon(QIcon(f"{IMG_PATH}/add.png"))
        self.add_student_btn.setFixedWidth(100)
        
        self.edit_student_btn = QPushButton("Sửa")
        self.edit_student_btn.setIcon(QIcon(f"{IMG_PATH}/edit.png"))
        self.edit_student_btn.setEnabled(False)
        self.edit_student_btn.setFixedWidth(100)

        self.cancel_student_btn = QPushButton("Hủy")
        self.cancel_student_btn.setIcon(QIcon(f"{IMG_PATH}/remove.png"))
        self.cancel_student_btn.setEnabled(False)
        self.cancel_student_btn.setFixedWidth(100)
        
        button_row1.addWidget(self.add_student_btn)
        button_row1.addWidget(self.edit_student_btn)
        button_row1.addWidget(self.cancel_student_btn)
        
        # Lưu, Phục hồi
        button_row2 = QHBoxLayout()
        button_row2.setSpacing(5)
        
        self.save_student_btn = QPushButton("Lưu")
        self.save_student_btn.setIcon(QIcon(f"{IMG_PATH}/save.png"))
        self.save_student_btn.setEnabled(False)
        self.save_student_btn.setFixedWidth(100)

        self.restore_student_btn = QPushButton("Phục hồi")
        self.restore_student_btn.setIcon(QIcon(f"{IMG_PATH}/undo.png"))
        self.restore_student_btn.setEnabled(False)
        self.restore_student_btn.setFixedWidth(100)
        
        button_row2.addWidget(self.save_student_btn)
        button_row2.addWidget(self.restore_student_btn)
        button_row2.addStretch(1)
        button_container_layout.addLayout(button_row1)
        button_container_layout.addLayout(button_row2)
        student_form_layout.addRow("", button_container)
        student_form_group.setLayout(student_form_layout)

        left_layout.addWidget(header_widget)
        left_layout.addWidget(student_form_group, 1)
        
        # ============ PHẦN PHẢI - BẢNG DỮ LIỆU VÀ TÌM KIẾM ============
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)
        
        # Thanh tìm kiếm
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 5)
        
        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Tìm kiếm theo mã, họ tên sinh viên...")
        self.student_search.setClearButtonEnabled(True)
        
        self.student_search_btn = QPushButton("Tìm")
        self.student_search_btn.setIcon(QIcon.fromTheme("system-search"))
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.student_search, 1)
        search_layout.addWidget(self.student_search_btn)
        
        # Bảng dữ liệu
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(["Mã Sinh Viên", "Họ", "Tên", "Giới tính", "Ngày sinh", "Địa chỉ", "Đang nghỉ học"])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.student_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.student_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.student_table.setMinimumHeight(300)
        self.student_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        right_layout.addLayout(search_layout)
        right_layout.addWidget(self.student_table, 1)

        left_widget.setMinimumWidth(350)
        left_widget.setMaximumWidth(400)

        self.student_container_layout.addWidget(left_widget)
        self.student_container_layout.addWidget(right_widget, 1)

    def connect_events(self):
        # ComboBox Khoa
        if hasattr (self, 'dept_combo'):
            self.dept_combo.currentIndexChanged.connect(self.dept_combo_changed)
        # Lớp với Sinh viên
        self.connect_class_events()
        self.connect_student_events()

    def connect_class_events(self):
        # Bảng với tìm kiếm
        self.class_table.itemClicked.connect(self.class_manager.item_selected)
        # self.class_search.textChanged.connect(self.class_manager.search_changed)
        # self.class_search_btn.clicked.connect(self.class_manager.search_clicked)
        # Nút
        self.add_class_btn.clicked.connect(self.class_manager.add_clicked)
        self.edit_class_btn.clicked.connect(self.class_manager.edit_clicked)
        self.save_class_btn.clicked.connect(self.class_manager.save_clicked)
        self.cancel_class_btn.clicked.connect(self.class_manager.cancel_clicked)
        self.restore_class_btn.clicked.connect(self.class_manager.restore_clicked)

    def connect_student_events(self):
        # Bảng với tìm kiếm
        self.student_table.itemClicked.connect(self.student_manager.item_selected)
        # self.student_search.textChanged.connect(self.student_manager.search_changed)
        # self.student_search_btn.clicked.connect(self.student_manager.search_clicked)
        # # Nút
        self.add_student_btn.clicked.connect(self.student_manager.add_clicked)
        self.edit_student_btn.clicked.connect(self.student_manager.edit_clicked)
        self.save_student_btn.clicked.connect(self.student_manager.save_clicked)
        self.cancel_student_btn.clicked.connect(self.student_manager.cancel_clicked)
        self.restore_student_btn.clicked.connect(self.student_manager.restore_clicked)
        pass
    # Update UI Departments and Class 
    def dept_combo_changed(self, index):
        """Xử lý khi người dùng chọn khoa từ combo box"""
        if index <= 0:
            return
        selected_dept_code = self.dept_combo.itemData(index)
        selected_dept_name = self.dept_combo.itemText(index)
        if self.controller:
            self.controller.select_dept(selected_dept_code, selected_dept_name)

    def hide_dept_combobox(self):
        if hasattr(self, 'dept_combo') and hasattr(self, 'dept_container'):
            self.dept_container.setVisible(False)

    def set_selected_dept(self, dept_code, dept_name):
        self.selected_dept_code = dept_code
        self.selected_dept_name = dept_name
        if dept_name:
            self.selected_dept_label.setText(f"Khoa: {dept_name}")
            self.dept_display.setText(dept_name)
        else:
            self.selected_dept_label.setText("Chưa chọn khoa")
            self.dept_display.setText("Chưa chọn khoa")
    
    def update_dept_combo(self, dept_data):
        self.dept_combo.clear()
        self.dept_combo.addItem('--- Chọn Khoa ---', None)
        for dept in dept_data:
            self.dept_combo.addItem(dept['TENKHOA'],dept['MAKHOA'])

    def load_classes(self, dept_code):
        if self.controller:
            self.controller.load_classes(dept_code)

    def update_class_table(self, class_data):
        self.class_table.setRowCount(0)
        if not class_data:
            return 
        for row_idx, cls in enumerate(class_data):
            self.class_table.insertRow(row_idx)
            self.class_table.setItem(row_idx, 0, QTableWidgetItem(cls.get('MALOP', '')))
            self.class_table.setItem(row_idx, 1, QTableWidgetItem(cls.get('TENLOP', '')))
            self.class_table.setItem(row_idx, 2, QTableWidgetItem(cls.get('NIENKHOA', '')))
            self.class_table.setItem(row_idx, 3, QTableWidgetItem(cls.get('TENKHOA', '')))

            siso_item = QTableWidgetItem(str(cls.get('SISO', 0)))
            siso_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.class_table.setItem(row_idx, 4, siso_item)
    
    def clear_class_form(self):
        self.class_id.clear()
        self.class_name.clear()
        self.course_year.clear()
        self.class_table.clearSelection()
        self.class_id.setFocus()

    def set_selected_class(self, class_id):
        """Cập nhật hiển thị lớp đang chọn"""
        self.selected_class_id = class_id

        if class_id:
            self.selected_class_label.setText(f"Lớp: {class_id}")
            self.student_class_id.setText(class_id)
        else:
            self.selected_class_label.setText("Chưa chọn lớp")
    # Update UI Student
    def load_student(self, class_id):
        if self.controller:
            self.controller.load_student(class_id)
    
    def update_student_table(self, student_data):
        self.student_table.setRowCount(0)
        if not student_data:
            return
        if self.student_table.columnCount() != 7:
            self.student_table.setColumnCount(7)
            self.student_table.setHorizontalHeaderLabels([
                "Mã Sinh Viên", "Họ", "Tên", "Giới tính", 
                "Ngày sinh", "Địa chỉ", "Đang nghỉ học"
            ])
        for row_idx, student in enumerate(student_data):
            self.student_table.insertRow(row_idx)
            self.student_table.setItem(row_idx, 0, QTableWidgetItem(student.get('MASV', '')))
            self.student_table.setItem(row_idx, 1, QTableWidgetItem(student.get('HO', '')))
            self.student_table.setItem(row_idx, 2, QTableWidgetItem(student.get('TEN', '')))

            gender_value = student.get('PHAI', '0')
            gender_text = 'Nam' if gender_value == 0 else 'Nữ'
            gender_item = QTableWidgetItem(gender_text)
            gender_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.student_table.setItem(row_idx, 3, gender_item)

            ngay_sinh = student.get('NGAYSINH', '')
            if ngay_sinh:
                import datetime
                if isinstance(ngay_sinh, (datetime.date, datetime.datetime)):
                    ngay_sinh = ngay_sinh.strftime("%d/%m/%Y")
                
            date_item = QTableWidgetItem(str(ngay_sinh))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.student_table.setItem(row_idx, 4, date_item)

            self.student_table.setItem(row_idx, 5, QTableWidgetItem(student.get('DIACHI', '')))

            nghi_hoc = student.get('DANGNGHIHOC', 0)
            status_item = QTableWidgetItem("✓" if nghi_hoc == 1 else "")
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.student_table.setItem(row_idx, 6, status_item)

        self.student_table.resizeColumnsToContents()

        header = self.student_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setMinimumSectionSize(100)

        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.student_table.setColumnWidth(3, 80)

        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.student_table.setColumnWidth(4, 100)

        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.student_table.setColumnWidth(6, 100)

        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

