from PyQt6.QtWidgets import (
    QWidget
)
from services.database_service import DatabaseService



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bejelentkezés")
        self.db = DatabaseService()
        self.init_ui()

