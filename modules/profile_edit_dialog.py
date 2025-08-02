import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QFormLayout, QLineEdit, QFileDialog,
                             QMessageBox)
from services.database_service import DatabaseService
from utils.validators import is_valid_name, is_valid_email, is_valid_birthdate, is_valid_phone, is_valid_password, \
    is_valid_username


# Profil szerkesztése adblak
class ProfileEditDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.db = DatabaseService()
        self.user_id = user_id
        self.setWindowTitle("Profil szerkesztése")
        self.setMinimumWidth(400)
        self.init_ui()
        self.setSizeGripEnabled(True)
        self.adjustSize()

    # Felhasználói felület felépítése
    def init_ui(self):
        user = self.db.get_user_by_id(self.user_id)
        layout = QVBoxLayout()

        # Profilkép
        self.pic_label = QLabel()
        self.pic_label.setFixedSize(100, 100)
        self.pic_label.setStyleSheet("border:1px solid #aaa; border-radius:50px; background:#eee;")
        if user["profile_pic"] and os.path.exists(user["profile_pic"]):
            self.pic_label.setPixmap(QPixmap(user["profile_pic"]).scaled(100, 100))
        else:
            self.pic_label.setText("Nincs kép")
        pic_btn = QPushButton("Profilkép feltöltése")
        pic_btn.clicked.connect(self.upload_pic)

        # Adatok
        form = QFormLayout()
        self.name_edit = QLineEdit(user["name"])
        self.username_edit = QLineEdit(user["username"])
        self.email_edit = QLineEdit(user["email"] or "")
        self.birthdate_edit = QLineEdit(user["birthdate"])
        self.phone_edit = QLineEdit(user["phone"])

        form.addRow("Név:", self.name_edit)
        form.addRow("Felhasználónév:", self.username_edit)
        form.addRow("Email:", self.email_edit)
        form.addRow("Születési dátum:", self.birthdate_edit)
        form.addRow("Telefonszám:", self.phone_edit)

        # Jelszó
        self.old_pw = QLineEdit()
        self.old_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pw = QLineEdit()
        self.new_pw.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Régi jelszó:", self.old_pw)
        form.addRow("Új jelszó:", self.new_pw)

        layout.addWidget(self.pic_label)
        layout.addWidget(pic_btn)
        layout.addLayout(form)

        save_btn = QPushButton("Mentés")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    # Fénykép felöltése
    def upload_pic(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Válassz profilképet", filter="Image files (*.png *.jpg *.jpeg)")
        if fname:
            self.pic_label.setPixmap(QPixmap(fname).scaled(100, 100))
            self.db.update_profile_pic(self.user_id, fname)

    # Mentés gomb működése , felhasználói adatok frissítése az adatbázisban
    def save(self):
        try:
            name = self.name_edit.text()
            username = self.username_edit.text()
            email = self.email_edit.text()
            birthdate = self.birthdate_edit.text()
            phone = self.phone_edit.text()
            old_pw = self.old_pw.text()
            new_pw = self.new_pw.text()

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

            # Jelszóváltás ellenőrzése (csak ha megadott új jelszót)
            if new_pw:  # Ha NEM üres
                if not self.db.check_user_password(self.user_id, old_pw):
                    errors.append("A régi jelszó hibás!")
                pw_errors = is_valid_password(new_pw)
                if pw_errors:
                    errors.append("Az új jelszó nem elég erős:\n- " + "\n- ".join(pw_errors))
            # Ha csak régi jelszó van megadva, de új nincs!
            elif old_pw:
                errors.append("A jelszó nem lehet üres!")

            if errors:
                QMessageBox.warning(self, "Adatellenőrzés", "\n".join(errors))
                return
            # Csak akkor frissítsen, ha tényleg van új jelszó!
            if new_pw:
                self.db.update_user_password(self.user_id, new_pw)
                QMessageBox.information(self, "Siker", "A jelszó sikeresen megváltozott!")

            self.db.update_user_profile(self.user_id, name, username, email, birthdate, phone)
            QMessageBox.information(self, "Mentés", "Profil módosítva!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Mentés hiba", f"Hiba történt:\n{str(e)}")
