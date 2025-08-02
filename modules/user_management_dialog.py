from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QComboBox, QHeaderView
)


class UserManagementDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Felhasználók kezelése")
        self.setMinimumWidth(800)
        self.setMinimumHeight(400)
        self.setSizeGripEnabled(True)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Felhasználók adatainak megjelenítése táblázatban
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Név", "Felhasználónév", "Email", "Szerep", "Felfüggesztve"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        self.load_users()

        # Gombok elrendezés
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

