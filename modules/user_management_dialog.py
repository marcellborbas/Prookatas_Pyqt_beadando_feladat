from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QComboBox, QHeaderView, QTableWidgetItem, QMessageBox
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

    # Felhasználók adatainak betöltése az adatbázisból és megjelenítése a táblázatban
    def load_users(self):
        self.table.setRowCount(0)
        users = self.db.get_all_users()
        for row in users:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for col, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if col == 0:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # ID mező ne legyen szerkeszthető
                self.table.setItem(row_idx, col, item)

    # Kiválasztott felhasználó ID-jának lekérése
    def get_selected_user_id(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Figyelem", "Válassz ki egy felhasználót!")
            return None
        id_item = self.table.item(selected, 0)
        if id_item is None or id_item.text() == "":
            QMessageBox.warning(self, "Figyelem", "Érvénytelen sor!")
            return None
        return int(id_item.text())

    # Felhasználó törlésének kezelése
    def delete_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        reply = QMessageBox.question(self, "Megerősítés", "Biztosan törölni akarod?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        self.db.delete_user(user_id)
        self.load_users()

    # Felhasználó felfüggesztésének/aktiválásának kezelése
    def toggle_suspend(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        suspend_item = self.table.item(self.table.currentRow(), 5)
        if suspend_item is None:
            QMessageBox.warning(self, "Figyelem", "Nem található a felfüggesztés mező!")
            return
        current = int(suspend_item.text())
        self.db.suspend_user(user_id, not current)
        self.load_users()
