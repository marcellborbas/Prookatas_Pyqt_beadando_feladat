from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QComboBox, QTableWidgetItem


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

    # Felhasználók betöltése az adatbázisból a táblázatba
    def load_users(self):
        self.table.setRowCount(0)
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT id, name, username, email, role, suspended FROM users')
        for row in cursor.fetchall():
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for col, val in enumerate(row):
                self.table.setItem(row_idx, col, QTableWidgetItem(str(val)))

    # Kiválasztott felhasználó törlése
    def delete_user(self):
        selected = self.table.currentRow()
        if selected < 0:
            return
        user_id = int(self.table.item(selected, 0).text())
        self.db.delete_user(user_id)
        self.load_users()

     # Kiválasztott felhasználó felfüggesztése vagy aktiválása
    def toggle_suspend(self):
        selected = self.table.currentRow()
        if selected < 0:
            return
        user_id = int(self.table.item(selected, 0).text())
        current = int(self.table.item(selected, 5).text())
        self.db.suspend_user(user_id, not current)
        self.load_users()
