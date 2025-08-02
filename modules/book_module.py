import csv

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QMenu, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QHeaderView,
    QMessageBox, QFileDialog, QTableWidgetItem
)

from modules.dialogs.add_book_dialog import AddBookDialog
from modules.profile_edit_dialog import ProfileEditDialog
from services.database_service import DatabaseService
from services.export_service import export_books_to_csv
from utils.filters import filter_books


class BookWindow(QMainWindow):
    def __init__(self, user_role, user_id):
        super().__init__()
        self.setWindowTitle("Könyvtár - Könyvek")
        self.db = DatabaseService()
        self.user_role = user_role
        self.user_id = user_id
        self.login_window = None
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self.filtered_books = None
        self.init_ui()
        self.load_books()

        self.resize(1100, 700)

    def init_ui(self):
        layout = QVBoxLayout(self._central_widget)

        # Menü (adminnak import funkció)
        menubar = self.menuBar()
        stat_menu = QMenu("Statisztikák", self)
        book_stats_action = QAction("Könyv toplista", self)
        book_stats_action.triggered.connect(self.show_book_stats)
        stat_menu.addAction(book_stats_action)
        reader_stats_action = QAction("Olvasó toplista", self)
        reader_stats_action.triggered.connect(self.show_reader_stats)
        stat_menu.addAction(reader_stats_action)
        menubar.addMenu(stat_menu)

        # Egyéb funkciók menü
        action_menu = QMenu("Action", self)
        if self.user_role == "admin":

            # Admin funkciók
            import_action = QAction("Importálás (CSV)", self)
            import_action.triggered.connect(self.import_books)
            action_menu.addAction(import_action)

            manage_users_action = QAction("Felhasználók kezelése", self)
            manage_users_action.triggered.connect(self.open_user_management)
            action_menu.addAction(manage_users_action)

            manage_cats_action = QAction("Kategóriák/címkék kezelése", self)
            manage_cats_action.triggered.connect(self.open_category_management)
            action_menu.addAction(manage_cats_action)

        # Minden felhasználónak elérhető menüpontok
        my_loans_action = QAction("Kikölcsönzött könyveim", self)
        my_loans_action.triggered.connect(self.show_my_loans)
        action_menu.addAction(my_loans_action)

        profile_edit_action = QAction("Profil szerkesztése", self)
        profile_edit_action.triggered.connect(self.open_profile_edit_dialog)
        action_menu.addAction(profile_edit_action)
        menubar.addMenu(action_menu)

        # Szűrőpanel létrehozása (cím, szerző, ISBN, év)
        filter_layout = QHBoxLayout()
        self.filter_title = QLineEdit()
        self.filter_title.setPlaceholderText("Cím")
        filter_layout.addWidget(self.filter_title, 2)
        self.filter_authors = QLineEdit()
        self.filter_authors.setPlaceholderText("Szerző(k)")
        filter_layout.addWidget(self.filter_authors, 2)
        self.filter_isbn = QLineEdit()
        self.filter_isbn.setPlaceholderText("ISBN")
        filter_layout.addWidget(self.filter_isbn, 1)
        self.filter_year = QLineEdit()
        self.filter_year.setPlaceholderText("Év")
        filter_layout.addWidget(self.filter_year, 1)
        filter_btn = QPushButton("Szűrés")
        filter_btn.clicked.connect(self.handle_filter)
        filter_layout.addWidget(filter_btn, 1)
        layout.addLayout(filter_layout)

        # Exportálás gomb
        export_btn = QPushButton("Keresés eredmény exportálása CSV-be")
        export_btn.clicked.connect(self.export_filtered_books)
        layout.addWidget(export_btn)

        # Súgó szöveg
        help_label = QLabel("Több könyv kijelöléséhez tartsd lenyomva a Ctrl vagy Shift billentyűt.")
        layout.addWidget(help_label)

        # Könyvlista táblázat
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Cím", "Szerző(k)", "ISBN", "Év", "Kölcsönözve"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.table)
        self.table.itemDoubleClicked.connect(self.open_detail_window)

        # Gombok (felhasználói funkciók
        btn_layout = QHBoxLayout()
        if self.user_role == "admin":
            # Csak adminnak
            add_book_btn = QPushButton("Könyv hozzáadása")
            add_book_btn.clicked.connect(self.add_book_dialog)
            btn_layout.addWidget(add_book_btn)

            delete_book_btn = QPushButton("Könyv törlése")
            delete_book_btn.clicked.connect(self.delete_book)
            btn_layout.addWidget(delete_book_btn)

        # Közös funkciók
        borrow_btn = QPushButton("Kikölcsönzés")
        borrow_btn.clicked.connect(self.borrow_book)
        btn_layout.addWidget(borrow_btn)

        return_btn = QPushButton("Visszaadás")
        return_btn.clicked.connect(self.return_book)
        btn_layout.addWidget(return_btn)

        logout_btn = QPushButton("Kijelentkezés")
        logout_btn.clicked.connect(self.logout)
        btn_layout.addWidget(logout_btn)
        layout.addLayout(btn_layout)

    # Profil szerkesztésének megnyitása
    def open_profile_edit_dialog(self):
        dialog = ProfileEditDialog(self.user_id, self)
        dialog.exec()

    # Könyvek szűrése megadott mezők alapján
    def handle_filter(self):
        all_books = self.db.get_all_books()
        title = self.filter_title.text()
        authors = self.filter_authors.text()
        isbn = self.filter_isbn.text()
        year = self.filter_year.text()
        year_val = int(year) if year.isdigit() else None
        filtered = filter_books(
            all_books,
            title=title if title else None,
            authors=authors if authors else None,
            isbn=isbn if isbn else None,
            year=year_val
        )
        self.load_books(filtered)
        self.filtered_books = filtered

    # Szűrt könyvek exportálása CSV fájlba
    def export_filtered_books(self):
        if not self.filtered_books:
            QMessageBox.warning(self, "Export", "Nincs mit exportálni! Előbb szűrj!")
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Eredmények exportálása CSV-be", filter="CSV files (*.csv)")
        if fname:
            export_books_to_csv(self.filtered_books, fname)
            QMessageBox.information(self, "Export", "Exportálás sikeres!")

    # Könyvek betöltése a táblázatba (opcionálisan szűrve)
    def load_books(self, books=None):
        if books is None:
            books = self.db.get_all_books()
        self.table.setRowCount(0)
        loans = self.db.get_borrowed_books()
        for book in books:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(book["title"]))
            self.table.setItem(row, 1, QTableWidgetItem(book["authors"]))
            self.table.setItem(row, 2, QTableWidgetItem(book["isbn"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(book["year"])))
            # Könyv státuszának meghatározása
            borrowed_str = "Nem"
            is_borrowed_by_self = False
            for l in loans:
                if l[2] == book["isbn"]:
                    borrowed_str = f"Igen ({l[4]}, {l[5][:10]})"
                    if l[3] == self.user_id:
                        is_borrowed_by_self = True
            self.table.setItem(row, 4, QTableWidgetItem(borrowed_str))
            if borrowed_str != "Nem":
                color = Qt.GlobalColor.green if is_borrowed_by_self else Qt.GlobalColor.red
                for col in range(5):
                    self.table.item(row, col).setBackground(color)

    # Könyv hozzáadása
    def add_book_dialog(self):
        dialog = AddBookDialog(self)
        if dialog.exec():
            title, authors, isbn, year, pdf_path = dialog.get_data()
            try:
                self.db.add_book(title, authors, isbn, year, pdf_path)
                QMessageBox.information(self, "Siker", "Könyv hozzáadva!")
                self.load_books()
            except Exception as e:
                QMessageBox.critical(self, "Hiba", f"Hiba: {str(e)}")

    # Könyvek importálása CSV fájlból
    def import_books(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Könyvek importálása (CSV)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        self.db.add_book(row["title"], row["authors"], row["isbn"], row["year"], row.get("pdf_path"))
                    except Exception:
                        pass
            QMessageBox.information(self, "Import", "Importálás kész!")
            self.load_books()

    # Könyv kölcsönzése
    def borrow_book(self):
        user = self.db.get_user_by_id(self.user_id)
        if user and int(user.get("suspended", 0)) == 1:
            QMessageBox.warning(self, "Hiba", "A felhasználó felfüggesztve van, nem kölcsönözhet!")
            return
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Figyelem", "Válassz ki legalább egy könyvet!")
            return
        selected_rows = set(idx.row() for idx in selected_indexes)
        success_count = 0
        fail_count = 0
        fail_messages = []
        for row in selected_rows:
            isbn = self.table.item(row, 2).text()
            try:
                self.db.borrow_book(isbn, self.user_id)
                success_count += 1
            except Exception as e:
                fail_count += 1
                fail_messages.append(f"{self.table.item(row, 0).text()} - {str(e)}")
        self.load_books()
        msg = f"Sikeresen kikölcsönöztél {success_count} könyvet."
        if fail_count:
            msg += f"\n{fail_count} könyvet nem sikerült:\n" + "\n".join(fail_messages)
        QMessageBox.information(self, "Kölcsönzés eredménye", msg)

    # Könyv visszaadása
    def return_book(self):
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Figyelem", "Válassz ki legalább egy könyvet!")
            return
        selected_rows = set(idx.row() for idx in selected_indexes)
        success_count = 0
        fail_messages = []
        for row in selected_rows:
            isbn = self.table.item(row, 2).text()
            try:
                days_late = self.db.return_book(isbn, self.user_id)
                success_count += 1
                if days_late > 0:
                    fail_messages.append(f"{self.table.item(row, 0).text()} - {days_late} nap késés!")
            except Exception as e:
                fail_messages.append(f"{self.table.item(row, 0).text()} - {str(e)}")
        self.load_books()
        msg = f"Sikeresen visszaadtál {success_count} könyvet."
        if fail_messages:
            msg += "\n" + "\n".join(fail_messages)
        QMessageBox.information(self, "Visszaadás eredménye", msg)
