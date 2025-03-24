class CRUDForm:
    def __init__(self, controller=None, name=None):
        self.controller = controller
        self.name = name
    # Xử lý nút
    def add_clicked(self):
        if self.controller:
            method_name = f'add_{self.name}'
            if hasattr(self.controller, method_name):
                getattr(self.controller, method_name)()
    
    def edit_clicked(self):
        if self.controller:
            method_name = f'edit_{self.name}'
            if hasattr(self.controller, method_name):
                getattr(self.controller, method_name)()

    def save_clicked(self):
        if not self.validate_form():
            return

        form_data = self.get_form_data()

        if self.controller:
            method_name = f'save_{self.name}'
            if hasattr(self.controller, method_name):
                getattr(self.controller, method_name)(form_data)
    
    def cancel_clicked(self):
        if self.controller:
            method_name = f'cancel_{self.name}'
            if hasattr(self.controller, method_name):
                getattr(self.controller, method_name)()
    
    def restore_clicked(self):
        if self.controller:
            method_name = f'restore_{self.name}'
            if hasattr(self.controller, method_name):
                getattr(self.controller, method_name)()

    def search_clicked(self):
        search_text = self.get_search_text()

        if self.controller:
            method_name = f'filter_{self.name}'
            if hasattr(self.controller, method_name):
                getattr(self.controller, method_name)(search_text)
    # Sự kiện khác
    def search_changed(self, text):
        if self.controller:
            method_name = f'filter_{self.name}'
            if hasattr(self.controller, method_name):
                getattr(self.controller, method_name)(text)

    def item_selected(self, item):
        if not self.controller:
            return
        item_id = self.get_selected_item()
        method_name = f'select_{self.name}'
        if hasattr(self.controller, method_name):
            getattr(self.controller, method_name)(item_id)
    
    # abstract class
    def validate_form(self):
        """ Kiểm tra dữ liệu của form"""
        raise NotImplementedError
    
    def get_form_data(self):
        """ Lấy thông tin từ form """
        raise NotImplementedError
    
    def get_search_text(self):
        raise NotImplementedError
    
    def get_selected_item(self):
        raise NotImplementedError
