from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton
)
from services.database_service import DatabaseService



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bejelentkezés")
        self.db = DatabaseService()
        self.init_ui()

    #felület felépítése
    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Beviteli mezők: felhasználónév és jelszó
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Felhasználónév:", self.username_input)
        form.addRow("Jelszó:", self.password_input)

        self.login_btn = QPushButton("Bejelentkezés")
        self.login_btn.clicked.connect(self.handle_login)
        form.addRow(self.login_btn)

        self.register_btn = QPushButton("Regisztráció")
        self.register_btn.clicked.connect(self.open_register)
        form.addRow(self.register_btn)

        layout.addLayout(form)
        self.setLayout(layout)
