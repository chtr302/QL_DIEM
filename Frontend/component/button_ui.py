from PyQt6.QtWidgets import QPushButton, QWidget, QApplication
from PyQt6.QtGui import QFont, QIcon, QCursor
from PyQt6.QtCore import Qt, QSize

class CustomButton(QPushButton):
    def __init__(self, text="", parent=None, icon_path=None, width=120, height=40, 
                 bg_color="#4CAF50", hover_color="#45a049", 
                 text_color="#ffffff", border_radius=5):
        super().__init__(text, parent)
        
        # Set fixed size
        self.setFixedSize(width, height)
        
        # Set font
        font = QFont("Arial", 10)
        font.setBold(True)
        self.setFont(font)
        
        # Set icon if provided
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(20, 20))
        
        # Set cursor to pointing hand
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Set style sheet
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: {border_radius}px;
                padding: 8px 16px;
            }}
            
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            
            QPushButton:pressed {{
                background-color: {bg_color};
            }}
        """)

# Các phương pháp tạo các loại button phổ biến
def create_primary_button(text, parent=None, icon_path=None, width=120, height=40):
    return CustomButton(text, parent, icon_path, width, height, 
                       bg_color="#2196F3", hover_color="#0b7dda")

def create_success_button(text, parent=None, icon_path=None, width=120, height=40):
    return CustomButton(text, parent, icon_path, width, height, 
                       bg_color="#4CAF50", hover_color="#45a049")

def create_danger_button(text, parent=None, icon_path=None, width=120, height=40):
    return CustomButton(text, parent, icon_path, width, height, 
                       bg_color="#f44336", hover_color="#da190b")

def create_warning_button(text, parent=None, icon_path=None, width=120, height=40):
    return CustomButton(text, parent, icon_path, width, height, 
                       bg_color="#ff9800", hover_color="#e68a00", text_color="#000000")

# Ví dụ sử dụng
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 300, 200)
    window.setWindowTitle("Button Demo")
    
    # Tạo các loại button
    btn1 = create_primary_button("Primary", window)
    btn1.move(80, 20)
    
    btn2 = create_success_button("Success", window)
    btn2.move(80, 70)
    
    btn3 = create_danger_button("Danger", window)
    btn3.move(80, 120)
    
    window.show()
    sys.exit(app.exec())