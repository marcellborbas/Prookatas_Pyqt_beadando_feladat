from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox
)
from services.database_service import DatabaseService
from utils.validators import is_valid_username, is_valid_email, is_valid_birthdate, is_valid_phone


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

    # Regisztráció gomb eseménykezelője
    def handle_register(self):
        # Felhasználói adatok
        name = self.name_input.text()
        username = self.username_input.text()
        email = self.email_input.text()
        birthdate = self.birthdate_input.text()
        phone = self.phone_input.text()
        password = self.password_input.text()

        # Bemenetek validálása
        if not name or not is_valid_username(username) or not is_valid_email(email) \
                or not is_valid_birthdate(birthdate) or not is_valid_phone(phone) or not password:
            QMessageBox.warning(self, "Hiba", "Kérlek, minden mezőt helyesen tölts ki!")
            return

        # Adatok mentése az adatbázisba
        try:
            self.db.conn.execute(
                "INSERT INTO users (name, username, email, birthdate, phone, password, role, suspended) VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
                (name, username, email, birthdate, phone, password, "reader")
            )
            self.db.conn.commit()
            QMessageBox.information(self, "Siker", "Sikeres regisztráció!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hiba történt: {str(e)}")
