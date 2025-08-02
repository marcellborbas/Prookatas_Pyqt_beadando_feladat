from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QComboBox

# Felhasználók kezelésére szolgáló ablak (admin funkciók)
class UserManagementDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Felhasználók kezelése")
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Név", "Felhasználónév", "Email", "Szerep", "Felfüggesztve"])
        layout.addWidget(self.table)
        self.load_users()

        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Törlés")
        self.delete_btn.clicked.connect(self.delete_user)
        btn_layout.addWidget(self.delete_btn)

        self.suspend_btn = QPushButton("Felfüggesztés/aktiválás")
        self.suspend_btn.clicked.connect(self.toggle_suspend)
        btn_layout.addWidget(self.suspend_btn)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "admin"])
        self.change_role_btn = QPushButton("Szerep módosítása")
        self.change_role_btn.clicked.connect(self.change_role)
        btn_layout.addWidget(self.role_combo)
        btn_layout.addWidget(self.change_role_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

