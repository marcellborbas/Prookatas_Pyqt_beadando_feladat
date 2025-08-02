import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QFormLayout, QLineEdit, QFileDialog)
from services.database_service import DatabaseService



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

