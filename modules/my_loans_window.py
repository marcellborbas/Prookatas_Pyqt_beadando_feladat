from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QHBoxLayout, QPushButton, QLabel

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
