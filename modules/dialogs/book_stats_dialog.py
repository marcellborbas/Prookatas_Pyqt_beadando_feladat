from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QLabel, QHeaderView

# Könyv toplista megjelenítése
class BookStatsDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Könyv toplista")
        self.stats = db.get_book_borrow_stats()
        self.rows_per_page = 10
        self.current_page = 0
        layout = QVBoxLayout(self)

        # Tábla létrehozása, amely tartalmazza a könyv statisztikákat
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Cím", "ISBN", "Olvasók száma", "Kölcsönzések száma"
        ])
        self.table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Lapozó gombok elrendezése
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
        self.update_table()
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.setSizeGripEnabled(True)

 # Tábla frissítése a statisztikák megjelenítéséhez
    def update_table(self):
        start = self.current_page * self.rows_per_page
        end = start + self.rows_per_page
        data = self.stats[start:end]
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, v in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(v)))
        self.table.resizeColumnsToContents()
        total_pages = (len(self.stats) - 1) // self.rows_per_page + 1
        self.page_label.setText(f"Oldal: {self.current_page + 1} / {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled((self.current_page + 1) * self.rows_per_page < len(self.stats))

