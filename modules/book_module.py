from PyQt6.QtWidgets import (
    QWidget, QMainWindow
)
from services.database_service import DatabaseService




class BookWindow(QMainWindow):
    def __init__(self, user_role, user_id):
        super().__init__()
        self.setWindowTitle("Könyvtár - Könyvek")
        self.db = DatabaseService()
        self.user_role = user_role
        self.user_id = user_id
        self.login_window = None
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self.filtered_books = None
        self.init_ui()
        self.load_books()

        self.resize(1100, 700)


