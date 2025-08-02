from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton
)
from services.database_service import DatabaseService

# Felhasználói regisztrációs modul
class UserModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseService()
        self.setWindowTitle("Felhasználó - Regisztráció")
        self.init_ui()

# Űrlap felépítése regisztrációhoz
    def init_ui(self):
        self.form = QFormLayout()
        self.name_input = QLineEdit()
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.birthdate_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.form.addRow("Név:", self.name_input)
        self.form.addRow("Felhasználónév:", self.username_input)
        self.form.addRow("Email:", self.email_input)
        self.form.addRow("Születési dátum (YYYY-MM-DD):", self.birthdate_input)
        self.form.addRow("Telefonszám (+36...):", self.phone_input)
        self.form.addRow("Jelszó:", self.password_input)

        self.register_btn = QPushButton("Regisztráció")
        self.register_btn.clicked.connect(self.handle_register)
        self.form.addRow(self.register_btn)

        self.setLayout(self.form)
