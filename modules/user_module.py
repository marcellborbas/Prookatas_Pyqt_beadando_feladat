from PyQt6.QtWidgets import (
    QWidget
)
from services.database_service import DatabaseService

# Felhasználói regisztrációs modul
class UserModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseService()
        self.setWindowTitle("Felhasználó - Regisztráció")
        self.init_ui()

