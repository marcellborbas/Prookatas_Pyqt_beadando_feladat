from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QCheckBox
)

from modules.book_module import BookWindow
from services.database_service import DatabaseService
from utils.validators import is_valid_name, is_valid_username, is_valid_email, is_valid_birthdate, is_valid_phone, \
    is_valid_password


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bejelentkezés")
        self.db = DatabaseService()
        self.init_ui()

    # felület felépítése
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

    # Bejelentkezés kezelése
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.db.get_user_by_username(username)
        if not user:
            QMessageBox.warning(self, "Hiba", "Nincs ilyen felhasználó")
            return
        if user["password"] != password:
            QMessageBox.warning(self, "Hiba", "Hibás jelszó")
            return
        if int(user.get("suspended", 0)) == 1:
            QMessageBox.warning(self, "Hiba", "A felhasználó felfüggesztve van!")
            return
        self.book_window = BookWindow(user["role"], user["id"])
        self.book_window.login_window = self
        self.book_window.show()
        self.hide()

    # Regisztrációs ablak megnyitása
    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Regisztráció")
        self.db = DatabaseService()
        self.init_ui()

    # Regisztrációs űrlap létrehozása
    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.birthdate_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.admin_checkbox = QCheckBox("Admin jogosultság")

        form.addRow("Név:", self.name_input)
        form.addRow("Felhasználónév:", self.username_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Születési dátum (YYYY-MM-DD):", self.birthdate_input)
        form.addRow("Telefonszám (+36...):", self.phone_input)
        form.addRow("Jelszó:", self.password_input)
        form.addRow(self.admin_checkbox)

        self.submit_btn = QPushButton("Regisztráció")
        self.submit_btn.clicked.connect(self.handle_register)
        form.addRow(self.submit_btn)

        layout.addLayout(form)
        self.setLayout(layout)

     # Regisztrációs adatok validálása és mentése
    def handle_register(self):
        name = self.name_input.text()
        username = self.username_input.text()
        email = self.email_input.text()
        birthdate = self.birthdate_input.text()
        phone = self.phone_input.text()
        password = self.password_input.text()
        role = "admin" if self.admin_checkbox.isChecked() else "user"

        errors = []
        if not is_valid_name(name):
            errors.append("A név legalább 2 karakter legyen!")
        if not is_valid_username(username):
            errors.append("A felhasználónév legalább 3 karakter legyen, csak betű/szám!")
        if not is_valid_email(email):
            errors.append("Hibás email formátum!")
        if not is_valid_birthdate(birthdate):
            errors.append("Születési dátum formátum: YYYY-MM-DD!")
        if not is_valid_phone(phone):
            errors.append("Hibás telefonszám!")
        if not password:
            errors.append("A jelszó nem lehet üres!")
        else:
            pw_errors = is_valid_password(password)
            if pw_errors:
                errors.append("A jelszó nem elég erős:\n- " + "\n- ".join(pw_errors))

        if errors:
            QMessageBox.warning(self, "Adatellenőrzés", "\n".join(errors))
            return

        try:
            self.db.add_user(name, username, email, birthdate, phone, password, role)
            QMessageBox.information(self, "Siker", "Sikeres regisztráció! Most már bejelentkezhetsz.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Nem sikerült a regisztráció: {str(e)}")
