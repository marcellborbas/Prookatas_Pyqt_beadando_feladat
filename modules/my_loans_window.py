from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QHBoxLayout, QPushButton, QLabel, \
    QTableWidgetItem


class MyLoansWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.setWindowTitle("Kikölcsönzött könyveim")
        self.db = db
        self.user_id = user_id

        self.loans = self.get_loans()           # <--- Most elmentjük egy listába
        self.rows_per_page = 10                 # <--- Hány sor legyen egy oldalon
        self.current_page = 0                   # <--- Aktuális oldal

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Táblázat létrehozása a kölcsönzött könyvek adatainak megjelenítésére
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Cím", "Szerző(k)", "ISBN", "Kölcsönzés dátuma", "Lejárat", "Visszahozva", "Státusz"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        layout.addWidget(self.table)

        # Lapozó gombok és címke
        pagelayout = QHBoxLayout()
        self.prev_btn = QPushButton("Előző")
        self.prev_btn.clicked.connect(self.show_prev_page)
        self.next_btn = QPushButton("Következő")
        self.next_btn.clicked.connect(self.show_next_page)
        self.page_label = QLabel()
        pagelayout.addWidget(self.prev_btn)
        pagelayout.addWidget(self.page_label)
        pagelayout.addWidget(self.next_btn)
        layout.addLayout(pagelayout)

        self.setLayout(layout)
        self.resize(1200, 450)
        self.update_table()

    # Kölcsönzött könyvek lekérdezése az adatbázisból
    def get_loans(self):
        loans = self.db.conn.execute(
            '''
            SELECT b.title, b.authors, b.isbn, l.borrowed_at, l.due_date, l.returned_at
            FROM loans l
            JOIN books b ON l.book_isbn = b.isbn
            WHERE l.user_id=? 
            ORDER BY l.borrowed_at DESC
            ''', (self.user_id,)
        ).fetchall()
        return loans

    # Az aktuális oldal adatainak megjelenítése
    def update_table(self):
        start = self.current_page * self.rows_per_page
        end = start + self.rows_per_page
        data = self.loans[start:end]
        self.table.setRowCount(len(data))
        for row, rowdata in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(rowdata[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(rowdata[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(rowdata[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(rowdata[3])[:19]))
            self.table.setItem(row, 4, QTableWidgetItem(str(rowdata[4])[:10]))
            returned = rowdata[5] if rowdata[5] else ""
            self.table.setItem(row, 5, QTableWidgetItem(str(returned)[:19]))
            status = "Visszaadva" if rowdata[5] else "Kikölcsönözve"
            self.table.setItem(row, 6, QTableWidgetItem(status))

        # Lapozási információk
        total_pages = max(1, (len(self.loans) - 1) // self.rows_per_page + 1)
        self.page_label.setText(f"Oldal: {self.current_page + 1} / {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled((self.current_page + 1) * self.rows_per_page < len(self.loans))